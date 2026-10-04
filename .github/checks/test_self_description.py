"""Structural regression cases; no independent agent or behavior evaluation."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from jsonschema import ValidationError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('self_description', HERE / 'self_description.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class DescriptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ode-description-check-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'description'
        shutil.copytree(ROOT / 'examples/personal-description/0.2.0', self.root)

    def edit(self, filename, change, repin=True):
        path = self.root / filename
        value = check.load(path)
        change(value)
        path.write_text(json.dumps(value, indent=2) + '\n')
        if repin and filename != 'index.json':
            index = check.load(self.root / 'index.json')
            for item in index['artifacts'] + index['resources']:
                if item['path'] == filename:
                    item['sha256'] = check.digest(path)
            (self.root / 'index.json').write_text(json.dumps(index, indent=2) + '\n')

    def validate(self):
        return check.validate(self.root / 'index.json', ROOT)

    def rejected(self, filename, change, expected):
        self.edit(filename, change)
        with self.assertRaises((ValueError, ValidationError)) as caught:
            self.validate()
        message = caught.exception.message if isinstance(caught.exception, ValidationError) else str(caught.exception)
        self.assertIn(expected, message)

    def test_aster_with_known_gaps(self):
        result = self.validate()
        self.assertEqual(result['assessmentCounts']['design']['missing'], 2)
        self.assertFalse(result['behaviorTested'])
        self.assertEqual(result['externalResourcesRead'], 0)

    def test_blank_template_is_only_a_draft(self):
        path = ROOT / 'spec/research/proposals/personal-description-template/0.1.0/index.json'
        self.assertEqual(check.validate(path, ROOT, True)['status'], 'valid_draft')
        with self.assertRaisesRegex(ValueError, 'Draft is not'):
            check.validate(path, ROOT)

    def test_new_index_can_pin_existing_component_version(self):
        self.edit('index.json', lambda x: x.update(version='0.3.0'))
        self.assertEqual(self.validate()['profileVersion'], '0.2.0')

    def test_other_agent_with_different_paths_and_no_selected_skills(self):
        # Independently assembled author fixture, not a name/count mutation of Aster.
        other = Path(self.temp.name) / 'other'
        shutil.copytree(ROOT / 'spec/research/proposals/personal-description-template/0.1.0', other)
        p = check.load(other / 'profile.json')
        p.update(descriptionId='urn:example:quiet-reader', status='agent_self_report', describedAt='2026-10-04T12:00:00Z')
        p['statements'] = [{'claimId': 'PURPOSE', 'topic': 'purpose', 'text': 'Help a person examine a supplied note; scope still needs agreement.',
                            'basis': 'agent_self_report', 'sourceRefs': [], 'scope': 'current_assignment', 'asOf': '2026-10-04',
                            'reviewState': 'unreviewed', 'qualityAreas': ['interaction'], 'designConditions': ['outcomes-alignment'], 'storagePlacement': 'agent'}]
        (other / 'answers').mkdir()
        new_profile = other / 'answers/description.json'
        new_profile.write_text(json.dumps(p))
        c = check.load(other / 'components.json'); c.update(agentDescriptionId=p['descriptionId'], synthetic=True)
        (other / 'components.json').write_text(json.dumps(c))
        a = check.load(other / 'assessment.json')
        a.update(status='author_assessment', evaluator='fixture author', assessedAt='2026-10-04T12:00:00Z', synthetic=True)
        a['profile'].update(id=p['descriptionId'], path='answers/description.json', sha256=check.digest(new_profile))
        (other / 'assessment.json').write_text(json.dumps(a))
        i = check.load(other / 'index.json'); i.update(descriptionId=p['descriptionId'], status='agent_self_report', synthetic=True)
        for entry in i['artifacts']:
            if entry['role'] == 'reflective_profile':
                entry['path'] = 'answers/description.json'
            entry['sha256'] = check.digest(other / entry['path'])
        (other / 'index.json').write_text(json.dumps(i))
        result = check.validate(other / 'index.json', ROOT)
        self.assertEqual(result['dependencies'], 0)
        self.assertEqual(result['assessmentCounts']['design']['missing'], 25)

    def test_index_digest_drift(self):
        self.rejected('index.json', lambda x: x['artifacts'][0].update(sha256='0' * 64), 'Indexed digest mismatch')

    def test_missing_file(self):
        (self.root / 'native/IDENTITY.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing indexed file'):
            self.validate()

    def test_parent_traversal(self):
        self.rejected('index.json', lambda x: x['artifacts'][0].update(path='../outside.json'), 'Unsafe local path')

    def test_symlinked_parent(self):
        (self.root / 'native').rename(self.root / 'actual')
        (self.root / 'native').symlink_to(self.root / 'actual', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            self.validate()

    def test_duplicate_artifact_role(self):
        self.rejected('index.json', lambda x: x['artifacts'][3].update(role='assessment'), 'Exactly one artifact')

    def test_duplicate_resource_id(self):
        self.rejected('index.json', lambda x: x['resources'][1].update(id=x['resources'][0]['id']), 'Duplicate resource ID')

    def test_unresolved_source_revision(self):
        self.rejected('profile.json', lambda x: x['statements'][0]['sourceRefs'][0].update(version='unknown-pin'), 'Unresolved source reference')

    def test_assessment_profile_digest(self):
        self.rejected('assessment.json', lambda x: x['profile'].update(sha256='0' * 64), 'Assessment profile pin mismatch')

    def test_assessment_profile_version(self):
        self.rejected('assessment.json', lambda x: x['profile'].update(version='old'), 'Assessment profile identity/version mismatch')

    def test_checklist_digest(self):
        self.rejected('assessment.json', lambda x: x['checklist'].update(sha256='0' * 64), 'Checklist digest mismatch')

    def test_missing_checklist_item(self):
        self.rejected('assessment.json', lambda x: x['qualityChecklist'].pop(), 'Incomplete checklist coverage')

    def test_duplicate_checklist_item(self):
        self.rejected('assessment.json', lambda x: x['designChecklist'].append(copy.deepcopy(x['designChecklist'][0])), 'Duplicate assessment check ID')

    def test_incorrect_counts(self):
        self.rejected('assessment.json', lambda x: x['completionCounts']['design'].update(filled=25), 'Assessment counts mismatch')

    def test_claim_reference_missing(self):
        self.rejected('assessment.json', lambda x: x['designChecklist'][0].update(profileRefs=['ABSENT']), 'Unresolved assessment claim')

    def test_gap_without_route(self):
        self.rejected('assessment.json', lambda x: next(e for e in x['designChecklist'] if e['fillStatus']=='missing').update(followUpRefs=[]), 'Gap requires a follow-up')

    def test_claimed_agreement_without_evidence(self):
        self.rejected('assessment.json', lambda x: x['designChecklist'][0].update(agreementStatus='agreed'), 'Agreement needs an evidence reference')

    def test_claimed_behavior_without_evidence(self):
        self.rejected('assessment.json', lambda x: x['qualityChecklist'][0].update(behaviorEvidence='tested_with_evidence'), 'Behavior claim needs an evidence reference')

    def test_missing_method_dependency(self):
        self.rejected('components.json', lambda x: x['methods'][0].update(dependencyRefs=['MISSING']), 'Unresolved method dependency')

    def test_available_method_with_invented_evidence(self):
        self.rejected('components.json', lambda x: x['methods'][1].update(capabilityEvidence=['invented-success']), 'Unresolved capability evidence')

    def test_own_file_is_not_reclassified_by_inclusion(self):
        self.rejected('components.json', lambda x: x['dependencies'][0].update(relationship='environment_dependency'), 'Resource/dependency mismatch')

    def test_external_directory_cannot_become_included_path(self):
        self.rejected('components.json', lambda x: x['dependencies'][-1].update(locator={'path': '../environment'}), 'uri')

    def test_no_capture_policy_in_description(self):
        self.rejected('components.json', lambda x: x['dependencies'][-1].update(captureSelection='recursive_include'), 'not_selected')

    def test_explicit_external_reference_never_read(self):
        self.edit('components.json', lambda x: x['dependencies'][-1]['locator'].update(uri='file:///unavailable/never/read'))
        self.assertEqual(self.validate()['externalResourcesRead'], 0)

    def test_unindexed_file_is_outside_description(self):
        (self.root / 'outside-description.json').write_text('not even JSON; do not read')
        self.validate()

    def test_derivative_does_not_reuse_source_digest(self):
        def mutate(c):
            c['dependencies'][0]['derivation'] = {'sourceDependencyRefs': ['ORIGINAL'], 'coverage': 'summary', 'limitations': 'details omitted'}
            c['dependencies'].append({'dependencyId': 'ORIGINAL', 'relationship': 'evidence', 'purpose': 'original document',
                 'locator': {'uri': 'urn:example:original'}, 'revision': {'status': 'unknown', 'value': None},
                 'sha256': c['dependencies'][0]['sha256'], 'descriptionInclusion': 'external_reference', 'captureSelection': 'not_selected',
                 'basis': 'test fixture', 'accessStatus': 'not_verified', 'boundary': 'original is external'})
        self.rejected('components.json', mutate, 'Derivative reuses source digest')

    def test_unknown_revision_cannot_claim_value(self):
        self.rejected('components.json', lambda x: x['dependencies'][-1]['revision'].update(value='fabricated'), 'null')


if __name__ == '__main__':
    unittest.main()
