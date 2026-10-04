"""Read-only structural checks for experimental self-description collections.

No model execution, external resource access, transitive capture or backup.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, ValidationError


PROPOSALS = 'spec/research/proposals/'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root, raw):
    require(isinstance(raw, str) and raw, 'Empty local path')
    require(not PurePosixPath(raw).is_absolute() and '\\' not in raw and ':' not in raw,
            'Unsafe local path: ' + raw)
    require(all(p not in ('', '.', '..') for p in raw.split('/')), 'Unsafe local path: ' + raw)
    path = root
    for part in raw.split('/'):
        path = path / part
        require(not path.is_symlink(), 'Symlink in included path: ' + raw)
    require(root.resolve() in path.resolve().parents, 'Path escapes collection: ' + raw)
    require(path.is_file(), 'Missing indexed file: ' + raw)
    return path


def load(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def unique(items, field, label):
    values = {item[field]: item for item in items}
    require(len(values) == len(items), 'Duplicate ' + label)
    return values


def date(value, label):
    require(isinstance(value, str) and bool(value), label + ' is missing')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(label + ' must be an ISO date/time') from None
    require(parsed.tzinfo is not None, label + ' requires a timezone')


def validate(index_path, standard_root, allow_draft=False):
    require(not index_path.is_symlink(), 'Index must not be a symlink')
    root = index_path.parent.resolve()
    standard_root = standard_root.resolve()
    index = load(index_path)

    def shape(value, name):
        schema = load(contained(standard_root, PROPOSALS + name + '.schema.json'))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(value)

    shape(index, 'personal-description-index')
    paths = unique(index['artifacts'] + index['resources'], 'path', 'indexed path')
    require(index_path.name not in paths, 'Index must not include itself')
    for raw, item in paths.items():
        require(digest(contained(root, raw)) == item['sha256'], 'Indexed digest mismatch: ' + raw)

    roles = {}
    for role in ['reflective_profile', 'structured_composition', 'assessment']:
        entries = [a for a in index['artifacts'] if a['role'] == role]
        require(len(entries) == 1, 'Exactly one artifact required for ' + role)
        roles[role] = entries[0]
    profile = load(contained(root, roles['reflective_profile']['path']))
    comp = load(contained(root, roles['structured_composition']['path']))
    assessment = load(contained(root, roles['assessment']['path']))
    shape(profile, 'personal-self-description')
    shape(comp, 'personal-description-components')
    shape(assessment, 'personal-self-diagnosis')
    require(index['descriptionId'] == profile['descriptionId'] == comp['agentDescriptionId'], 'Description identity mismatch')
    require(index['status'] == profile['status'], 'Profile/index status mismatch')
    require(index['synthetic'] == comp['synthetic'] == assessment['synthetic'], 'Synthetic marker mismatch')
    require(index['dependencyView'] == roles['structured_composition']['path'] + '#/dependencies', 'Dependency view mismatch')
    draft = index['status'] == 'draft'
    if draft:
        require(allow_draft, 'Draft is not a completed description; use --allow-draft to check an unfinished template')
    else:
        require(profile['descriptionId'] and profile['statements'], 'Completed profile requires identity and claims')
        date(profile['describedAt'], 'Description date')
        date(assessment['assessedAt'], 'Assessment date')
        require(assessment['evaluator'] and assessment['status'] != 'draft', 'Completed assessment requires evaluator and status')

    sources = {(s['sourceId'], s['version']): s for s in profile['sources']}
    require(len(sources) == len(profile['sources']), 'Duplicate source identity/version')
    for source in sources.values():
        if 'location' in source:
            require(source['location'] in paths, 'Source location is not indexed')
            require(source['version'] == paths[source['location']]['sha256'], 'Local source version must pin its file digest')
    claims = unique(profile['statements'], 'claimId', 'claim ID')
    unique(profile['unknowns'], 'id', 'unknown ID')
    for item in profile['statements'] + profile['authority'] + profile['unknowns']:
        for ref in item['sourceRefs']:
            require((ref['sourceId'], ref['version']) in sources, 'Unresolved source reference')
        if item.get('reviewState') in ['source_checked', 'owner_confirmed']:
            require(item['sourceRefs'], 'Reviewed claim requires source references')

    resources = unique(index['resources'], 'id', 'resource ID')
    dependencies = unique(comp['dependencies'], 'dependencyId', 'dependency ID')
    included = set()
    for dep in dependencies.values():
        if dep['descriptionInclusion'] == 'included_file':
            rid = dep['dependencyId']
            require(rid in resources, 'Included dependency is absent from resources')
            res = resources[rid]
            require((dep['locator']['path'], dep['sha256'], dep['relationship']) ==
                    (res['path'], res['sha256'], res['relationship']), 'Resource/dependency mismatch')
            included.add(rid)
        else:
            require(bool(urlsplit(dep['locator']['uri']).scheme), 'External locator must be a URI')
        if 'derivation' in dep:
            for source_id in dep['derivation']['sourceDependencyRefs']:
                require(source_id != dep['dependencyId'] and source_id in dependencies, 'Invalid derivative source identity')
                origin = dependencies[source_id]
                if dep.get('sha256') and origin.get('sha256'):
                    require(dep['sha256'] != origin['sha256'], 'Derivative reuses source digest')
    require(included == set(resources), 'Resource lacks its explicit dependency description')
    require(set(comp['entryRoute']) <= set(dependencies), 'Unresolved entry route')

    def visit(rid, stack):
        require(rid not in stack, 'Cyclic derivative provenance')
        for sid in dependencies[rid].get('derivation', {}).get('sourceDependencyRefs', []):
            visit(sid, stack | {rid})
    for rid in dependencies:
        visit(rid, set())

    evidence = {rid for rid, dep in dependencies.items() if dep['relationship'] == 'evidence'}
    unique(comp['methods'], 'methodId', 'method ID')
    for method in comp['methods']:
        require(set(method['dependencyRefs']) <= set(dependencies), 'Unresolved method dependency')
        require(set(method['capabilityEvidence']) <= evidence, 'Unresolved capability evidence')
        if method['availability'] == 'included_native_files':
            require(set(method['dependencyRefs']) <= included, 'Included method points outside included resources')
        if method['applicationStatus'] == 'not_selected':
            require(not method['selected'], 'Selected method marked not_selected')
    work_refs = {(r['objectId'], r['version']) for r in comp['formalWorks']}
    require(len(work_refs) == len(comp['formalWorks']), 'Duplicate Work reference')
    require(bool(work_refs) == (comp['formalWorkStatus'] == 'defined'), 'Formal Work status mismatch')
    followups = unique(comp['followUps'], 'id', 'follow-up ID')
    if profile['unknowns']:
        require(followups, 'Unknowns require a follow-up route')

    ap = assessment['profile']
    require(ap['id'] == profile['descriptionId'] and ap['version'] == profile['version'], 'Assessment profile identity/version mismatch')
    require(ap['path'] == roles['reflective_profile']['path'] and ap['sha256'] == roles['reflective_profile']['sha256'], 'Assessment profile pin mismatch')
    checklist = assessment['checklist']
    cp = contained(standard_root, checklist['path'])
    require(checklist['path'] == 'docs/agents/self-diagnosis.checklist.json', 'Unsupported checklist catalog')
    require(digest(cp) == checklist['sha256'], 'Checklist digest mismatch')
    catalog = load(cp)
    require(catalog['version'] == checklist['version'], 'Checklist version mismatch')
    for group, count_key in [('designChecklist', 'design'), ('qualityChecklist', 'quality')]:
        entries = unique(assessment[group], 'checkId', 'assessment check ID')
        require(set(entries) == {e['checkId'] for e in catalog[group]}, 'Incomplete checklist coverage')
        for item in entries.values():
            require(set(item['profileRefs']) <= set(claims), 'Unresolved assessment claim')
            if item['fillStatus'] in ['filled', 'partial']:
                require(item['profileRefs'], 'Filled/partial answer requires claims')
            require(set(item['followUpRefs']) <= set(followups), 'Unresolved follow-up')
            if item['fillStatus'] in ['partial', 'missing']:
                require(item['followUpRefs'], 'Gap requires a follow-up route')
            require(set(item['agreementRefs']) <= evidence, 'Unresolved agreement evidence')
            require(set(item['behaviorEvidenceRefs']) <= evidence, 'Unresolved behavior evidence')
            if item['agreementStatus'] == 'agreed':
                require(item['agreementRefs'], 'Agreement needs an evidence reference')
            if item['behaviorEvidence'] != 'not_evaluated':
                require(item['behaviorEvidenceRefs'], 'Behavior claim needs an evidence reference')
        actual = Counter(e['fillStatus'] for e in entries.values())
        reported = {k: v for k, v in assessment['completionCounts'][count_key].items() if v}
        require(dict(actual) == reported, 'Assessment counts mismatch')

    definitions = load(contained(standard_root, PROPOSALS + 'personal-self-description.checks.json'))['objects']
    known_checks = {(o['id'], o['version']) for o in definitions if o['kind'] == 'Check'}
    require(len({(r['objectId'], r['version']) for r in profile['checkRefs']}) == len(profile['checkRefs']), 'Duplicate Check reference')
    for ref in profile['checkRefs']:
        require((ref['objectId'], ref['version']) in known_checks, 'Unresolved Check definition')
    return {'status': 'valid_draft' if draft else 'structurally_valid_author_description',
            'descriptionId': profile['descriptionId'], 'profileVersion': profile['version'],
            'indexedFiles': len(paths), 'dependencies': len(dependencies),
            'assessmentCounts': assessment['completionCounts'],
            'substantiveReview': 'not_performed_by_this_check', 'independentAgentRepetition': 'not_performed',
            'behaviorTested': False, 'backupCreated': False, 'externalResourcesRead': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--standard-root', type=Path, required=True)
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--allow-draft', action='store_true')
    args = parser.parse_args()
    try:
        result = validate(args.index, args.standard_root, args.allow_draft)
    except (ValueError, OSError, KeyError, ValidationError) as error:
        # Avoid dumping the contents of a private profile in a schema error.
        detail = ('Schema validation failed at ' + '/'.join(map(str, error.absolute_path))) if isinstance(error, ValidationError) else str(error)
        print(json.dumps({'status': 'failed', 'reason': detail}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
