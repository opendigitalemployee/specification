"""Read-only structural checks for the experimental ODE decision extension.

These checks validate declared relationships, not truth, professional quality,
legal authority, calibration or enforcement by a running agent.
"""
import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import re
from jsonschema import Draft202012Validator, FormatChecker


def require(condition, message):
    if not condition:
        raise ValueError(message)


def at(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def read(root, relative):
    path = root / relative
    require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
            'Unsafe resource path')
    require(not path.is_symlink() and path.resolve().is_relative_to(root.resolve()),
            'Resource escapes package')
    return path.read_bytes()


def check_data(data, package, standard_root):
    schema = json.loads((standard_root / 'spec/extensions/decision-making.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    catalog = json.loads((standard_root / 'spec/catalogs/operating-conditions.json').read_text())
    require(data['catalog'] == {k: catalog[k] for k in ('id', 'version')}, 'Catalog pin mismatch')
    codes = {item['code'] for item in catalog['conditions']}
    require(len(codes) == len(catalog['conditions']), 'Duplicate catalog code')
    manifest = json.loads((package / 'manifest.json').read_text())
    inventory = {d['path'] for d in manifest['resources']}
    objects = {}
    for entry in manifest['objects']:
        value = json.loads(read(package, entry['path']))
        objects[(value['id'], value['version'])] = value

    def resolve(pin, kinds):
        key = (pin['objectId'], pin['version'])
        require(key in objects, 'Unresolved object pin: ' + str(key))
        value = objects[key]
        require(value['kind'] in kinds, 'Wrong referenced object kind: ' + value['kind'])
        return value

    profile = data['profile']; method = data['method']; bindings = profile['bindings']
    expected = dict(agentRef=['ClientAgent'], goalRef=['GoalMap'],
                    environmentRef=['Environment'], workRef=['Work'], styleRef=['DecisionStyle'],
                    interactionRef=['InteractionContract'], metaSkillRef=['Skill'])
    resolved = {key: resolve(bindings[key], kinds) for key, kinds in expected.items()}
    policies = [resolve(pin, ['Policy']) for pin in bindings['policyRefs']]
    require(resolved['metaSkillRef']['spec'].get('skillKind') == 'meta-skill', 'Expected a meta-skill')
    agent = resolved['agentRef']['spec']
    require(agent['environmentRef'] == bindings['environmentRef'], 'Profile environment differs from agent')
    for scalar, plural in [('goalRef','goalRefs'), ('workRef','workRefs'), ('styleRef','styleRefs'), ('interactionRef','interactionRefs')]:
        require(bindings[scalar] in agent.get(plural, []), 'Profile binding not selected by agent: ' + scalar)
    require(all(pin in agent.get('policyRefs', []) for pin in bindings['policyRefs']), 'Unselected profile policy')
    require(bindings['metaSkillRef'] in resolved['workRef']['spec'].get('skillRefs', []), 'Work omits human meta-skill')
    extension = resolved['styleRef'].get('extensions', {}).get('org.opendigitalemployee.decision-making', {})
    require(extension == {'version':data['extensionVersion'], 'artifact':'decision-making.json'}, 'DecisionStyle extension binding missing')
    require('decision-making.json' in inventory, 'Decision description is not an inventoried resource')
    limits = profile['limits']; history = {}
    for episode in data['episodes']:
        eid = episode['id']; require(eid not in history, 'Duplicate episode ID')
        require(episode['methodVersion'] == method['version'] and episode['profileVersion'] == profile['version'], 'Method/profile version mismatch')
        decided = at(episode['decidedAt']); previous = episode['previousEpisodeId']
        if previous is not None:
            require(previous in history, 'Unknown or forward previous episode')
            require(at(history[previous]['decidedAt']) < decided, 'History chronology mismatch')
            if history[previous]['review']['status'] == 'recorded':
                require(at(history[previous]['review']['observedAt']) <= decided, 'Next step predates predecessor review')
        resolve(episode['responsibleActorRef'], ['ClientAgent','Party','Organization'])
        inputs = {i['id']:i for i in episode['inputs']}
        require(len(inputs) == len(episode['inputs']), 'Duplicate input ID')
        for item in inputs.values():
            artifact = item['artifact']
            require(artifact['path'] in inventory, 'Input not in package resources')
            require(hashlib.sha256(read(package, artifact['path'])).hexdigest() == artifact['sha256'], 'Input hash mismatch')
            require(at(item['observedAt']) <= decided, 'Future input at decision time')
        conditions = {c['code']:c for c in episode['conditions']}
        require(len(conditions) == len(episode['conditions']), 'Duplicate condition code')
        require(codes <= set(conditions), 'Missing condition assessment')
        for code, condition in conditions.items():
            if code not in codes:
                require(bool(re.fullmatch(r'x-[a-z0-9.-]+:[a-z0-9-]+', code)) and bool(condition.get('definition')), 'Undefined local condition')
            require(set(condition['evidenceIds']) <= set(inputs), 'Unknown condition evidence')
        focus = episode['focus']
        if any(c['status'] == 'present' for c in conditions.values()):
            require(focus in conditions and conditions[focus]['status'] == 'present', 'Focus must select a present condition')
        else:
            require(focus is None, 'No present condition for focus')
        candidates = {c['id']:c for c in episode['candidates']}
        require(len(candidates) == len(episode['candidates']), 'Duplicate candidate ID')
        for candidate in candidates.values():
            resolve(candidate['workRef'], ['Work'])
        selected = episode['selection']['candidateIds']
        require(len(set(selected)) == len(selected) and set(selected) <= set(candidates), 'Invalid selected candidates')
        require(all(candidates[c]['admissibility'] != 'blocked' for c in selected), 'Blocked candidate selected')
        if episode['applicability']['status'] != 'applicable':
            require(not selected, 'Method selected work outside applicability')
        else:
            require(profile['domain'] in method['applicability']['domains'], 'Profile domain outside method applicability')
        for resource, limit in [('hours','hoursPerStep'),('budget','budgetPerStep')]:
            spent = sum(candidates[c]['cost'][resource] for c in selected)
            require(spent <= limits[limit], 'Resource budget exceeded')
            require(abs(episode['selection']['remainingResources'][resource] - (limits[limit]-spent)) < 1e-8, 'Remaining resources inconsistent')
        forecast = episode['forecast']
        require(set(forecast['basisInputIds']) <= set(inputs), 'Unknown forecast evidence')
        require(at(forecast['madeAt']) <= decided <= at(forecast['horizon']), 'Forecast chronology invalid')
        for key in forecast['basisInputIds']:
            require(at(inputs[key]['observedAt']) <= at(forecast['madeAt']), 'Forecast uses later evidence')
        authorization = episode['authorization']
        responsible = resolve(authorization['responsibleRef'], ['Party','Organization'])
        require(agent.get('authorityRef') == authorization['responsibleRef'], 'Human responsibility differs from configured authority')
        require(authorization['policyRef'] in bindings['policyRefs'], 'Authorization uses undeclared policy')
        policy = resolve(authorization['policyRef'], ['Policy'])['spec']
        require(at(authorization['recordedAt']) >= decided, 'Authorization record predates decision')
        if authorization['status'] == 'within-mandate':
            require(policy['mode'] == 'allow', 'Within-mandate requires an allowing policy')
        if authorization['status'] in ['within-mandate','approved']:
            require(policy['mode'] != 'deny', 'Deny policy cannot grant authority')
        if authorization['status'] == 'pending':
            require('humanRequest' in episode, 'Pending authority has no human request')
        if 'humanRequest' in episode:
            request = episode['humanRequest']
            resolve(request['recipientRef'], ['Party','Organization'])
            require(request['recipientRef'] == authorization['responsibleRef'], 'Human request goes to a different authority')
            require(at(request['deadline']) >= decided, 'Request deadline predates decision')
        execution = episode['execution']
        require(set(execution['candidateIds']) <= set(selected) and len(set(execution['candidateIds'])) == len(execution['candidateIds']), 'Executed unselected or duplicate action')
        if execution['status'] != 'not-started':
            require(authorization['status'] in ['within-mandate','approved'], 'Execution without authority')
            require(decided <= at(authorization['recordedAt']) <= at(execution['startedAt']) <= at(execution['endedAt']), 'Execution chronology invalid')
            if any(candidates[c]['admissibility'] == 'requires-human' for c in execution['candidateIds']):
                require(authorization['status'] == 'approved' and 'humanRequest' in episode, 'Human-required action lacks explicit approval/request')
                require(episode['humanRequest']['type'] == 'authorization', 'Information request is not an authorization request')
            for item in inputs.values():
                require(item['status'] == 'known', 'Execution with unknown required input')
                age = at(execution['startedAt']) - at(item['observedAt'])
                require(age <= timedelta(hours=method['applicability']['maxEvidenceAgeHours']), 'Execution uses stale evidence')
        review = episode['review']
        require(at(review['dueAt']) >= decided, 'Review due before decision')
        if review['status'] == 'recorded':
            require(execution['status'] != 'not-started', 'Recorded execution review without action')
            require(at(execution['endedAt']) <= at(review['observedAt']), 'Review predates action end')
        history[eid] = episode
    return len(history)


def check(package, standard_root):
    from package_contract import check as check_package
    check_package(package, standard_root)
    data = json.loads(read(package, 'decision-making.json'))
    count = check_data(data, package, standard_root)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--standard-root', type=Path, default=Path('.'))
    parser.add_argument('--package', type=Path, required=True)
    args = parser.parse_args()
    count = check(args.package.resolve(), args.standard_root.resolve())
    print(f'PASS: {count} decision episodes; structural checks only, no execution or business effect established')
