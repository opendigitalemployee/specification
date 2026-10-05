import copy
import json
from pathlib import Path
import unittest
from jsonschema import ValidationError
from decision_making import check_data

ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'examples/product-employee'


class DecisionContractTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((PACKAGE/'decision-making.json').read_text())

    def valid(self):
        return check_data(self.data,PACKAGE,ROOT)

    def rejects(self, change):
        change(self.data)
        with self.assertRaises((ValueError,ValidationError)):
            self.valid()

    def test_worked_history(self): self.assertEqual(self.valid(),2)
    def test_unused_method(self): self.data['episodes']=[];self.assertEqual(self.valid(),0)
    def test_missing_category(self): self.rejects(lambda d:d['episodes'][0]['conditions'].pop())
    def test_unknown_catalog_version(self): self.rejects(lambda d:d['catalog'].update(version='99'))
    def test_focus_cannot_hide_other_conditions(self): self.rejects(lambda d:d['episodes'][0].update(focus='changing-conditions'))
    def test_no_undefined_local_code(self): self.rejects(lambda d:d['episodes'][0]['conditions'].append(dict(d['episodes'][0]['conditions'][0],code='custom')))
    def test_namespaced_condition_is_extensible(self):
        self.data['episodes'][0]['conditions'].append(dict(self.data['episodes'][0]['conditions'][0],code='x-example:local-condition',definition='A local condition'))
        self.valid()
    def test_version_pin(self): self.rejects(lambda d:d['episodes'][0].update(methodVersion='2'))
    def test_wrong_object_kind(self): self.rejects(lambda d:d['profile']['bindings'].update(goalRef=d['profile']['bindings']['agentRef']))
    def test_unknown_input_blocks_execution(self): self.rejects(lambda d:d['episodes'][0]['inputs'][0].update(status='unknown'))
    def test_hash_mismatch(self): self.rejects(lambda d:d['episodes'][0]['inputs'][0]['artifact'].update(sha256='0'*64))
    def test_future_evidence(self): self.rejects(lambda d:d['episodes'][0]['inputs'][0].update(observedAt='2026-10-02T08:00:00Z'))
    def test_stale_at_execution(self): self.rejects(lambda d:d['method']['applicability'].update(maxEvidenceAgeHours=1))
    def test_outside_applicability(self): self.rejects(lambda d:d['episodes'][0]['applicability'].update(status='not-applicable'))
    def test_outside_domain(self): self.rejects(lambda d:d['profile'].update(domain='Clinical decisions'))
    def test_unselected_execution(self): self.rejects(lambda d:d['episodes'][0]['execution'].update(candidateIds=['interviews']))
    def test_parallel_budget(self): self.rejects(lambda d:d['episodes'][0]['selection'].update(candidateIds=['review','interviews']))
    def test_remaining_budget(self): self.rejects(lambda d:d['episodes'][0]['selection']['remainingResources'].update(hours=4))
    def test_blocked_candidate(self): self.rejects(lambda d:d['episodes'][0]['candidates'][0].update(admissibility='blocked'))
    def test_pending_permission_no_action(self): self.rejects(lambda d:d['episodes'][0]['authorization'].update(status='pending'))
    def test_silence_is_not_approval(self):
        self.rejects(lambda d:d['episodes'][1].update(execution=dict(d['episodes'][0]['execution'],candidateIds=['interviews'],startedAt='2026-10-01T14:00:00Z',endedAt='2026-10-01T15:00:00Z')))
    def test_human_required_action_needs_approval(self): self.rejects(lambda d:d['episodes'][0]['candidates'][0].update(admissibility='requires-human'))
    def test_pending_has_question(self): self.rejects(lambda d:d['episodes'][1].pop('humanRequest'))
    def test_wrong_human(self): self.rejects(lambda d:d['episodes'][1]['humanRequest'].update(recipientRef=d['profile']['bindings']['agentRef']))
    def approve_second(self):
        e=self.data['episodes'][1]
        e['authorization'].update(status='approved',basis='Synthetic explicit scoped authorization',recordedAt='2026-10-01T13:30:00Z')
        e['execution']={'status':'completed','candidateIds':['interviews'],'startedAt':'2026-10-01T14:00:00Z','endedAt':'2026-10-01T17:00:00Z','receipt':'Synthetic test receipt only'}
    def test_scoped_approval_allows_action(self):
        self.approve_second();self.valid()
    def test_information_response_cannot_grant_permission(self):
        self.approve_second();self.rejects(lambda d:d['episodes'][1]['humanRequest'].update(type='information'))
    def test_no_mandate_from_approval_policy(self): self.rejects(lambda d:d['episodes'][0]['authorization'].update(policyRef=d['profile']['bindings']['policyRefs'][1]))
    def test_probability_needs_calibration_basis(self): self.rejects(lambda d:d['episodes'][0]['forecast'].update(estimateKind='probability',probability=.8))
    def test_unknown_is_not_zero(self): self.rejects(lambda d:d['episodes'][0]['forecast'].update(probability=0))
    def test_forecast_must_precede_action(self): self.rejects(lambda d:d['episodes'][0]['forecast'].update(madeAt='2026-10-01T11:00:00Z'))
    def test_review_cannot_precede_execution(self): self.rejects(lambda d:d['episodes'][0]['review'].update(observedAt='2026-10-01T09:00:00Z'))
    def test_review_cannot_invent_action(self): self.rejects(lambda d:d['episodes'][1].update(review=copy.deepcopy(d['episodes'][0]['review'])))
    def test_history_cannot_point_forward(self): self.rejects(lambda d:d['episodes'][0].update(previousEpisodeId='step-2'))
    def test_next_step_follows_review(self): self.rejects(lambda d:d['episodes'][1].update(decidedAt='2026-10-01T11:00:00Z'))


if __name__=='__main__': unittest.main()
