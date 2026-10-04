"""Regression cases for normative affiliation and version-preserving validation."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from jsonschema import ValidationError
import package_contract as contract

ROOT=Path(__file__).resolve().parents[2]


class AffiliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'personal'
        shutil.copytree(ROOT/'examples/personal-agent',self.root)

    def change(self,path,update):
        p=self.root/path;value=json.loads(p.read_text());update(value)
        p.write_text(json.dumps(value,indent=2)+'\n')

    def verify(self):
        lock=json.loads((self.root/'package.lock.json').read_text())
        lock['files']={p:hashlib.sha256((self.root/p).read_bytes()).hexdigest() for p in lock['files']}
        (self.root/'package.lock.json').write_text(json.dumps(lock))
        return contract.check(self.root,ROOT)

    def test_person_requires_no_organization(self):
        self.assertNotIn('organizationRef', ''.join(p.read_text() for p in self.root.rglob('*.json')))
        self.assertEqual(self.verify()['specVersion'],'0.2.0-draft')

    def test_three_documented_cases_have_complete_reference_paths(self):
        for name,category in [('personal-agent','person'),('family-agent','family'),('project-agent','team'),('company-agent','organization')]:
            with self.subTest(name=name):
                root=ROOT/'examples'/name
                self.assertEqual(contract.check(root,ROOT)['externalDependencies'],0)
                manifest=contract.read(root/'manifest.json')
                objects={o['id']:o for o in (contract.read(root/x['path']) for x in manifest['objects'])}
                agent=next(o for o in objects.values() if o['kind']=='ClientAgent')['spec']
                served=objects[agent['servesRef']['objectId']]
                self.assertEqual(served['spec']['category'],category)
                self.assertEqual(objects[agent['authorityRef']['objectId']]['spec']['category'],'person')
                if category!='person':self.assertNotEqual(agent['servesRef'],agent['authorityRef'])
                env=objects[agent['environmentRef']['objectId']]['spec']
                self.assertEqual(env['controllerRef'],agent['servesRef'])
                for ref in agent['toolBindingRefs']:
                    binding=objects[ref['objectId']]['spec']
                    self.assertEqual(binding['environmentRef'],agent['environmentRef'])
                    self.assertEqual(binding['controllerRef'],env['controllerRef'])
                for ref in env['worldModelRefs']:
                    self.assertEqual(objects[ref['objectId']]['spec']['controllerRef'],env['controllerRef'])

    def test_all_affiliation_categories(self):
        for category in ('person','family','team','organization','other'):
            with self.subTest(category=category):
                self.change('objects/person.json',lambda o:o['spec'].update(category=category,categoryLabel='Cooperative'))
                self.verify()

    def test_category_catalog_matches_normative_schema(self):
        catalog=contract.read(ROOT/'spec/schema/party-categories.json')
        schema=contract.read(ROOT/'spec/schema/object.schema.json')
        party=next(item['then']['properties']['spec'] for item in schema['allOf'] if item['if']['properties']['kind']['const']=='Party')
        self.assertEqual(catalog['specVersion'],contract.CURRENT_VERSION)
        self.assertEqual([x['id'] for x in catalog['categories']],party['properties']['category']['enum'])

    def test_other_category_needs_label(self):
        self.change('objects/person.json',lambda o:o['spec'].update(category='other'))
        with self.assertRaises(ValidationError):self.verify()

    def test_agent_role_is_not_affiliation_category(self):
        self.change('objects/person.json',lambda o:o['spec'].update(category='manager'))
        with self.assertRaises(ValidationError):self.verify()

    def test_served_party_is_required(self):
        self.change('objects/agent.json',lambda o:o['spec'].pop('servesRef'))
        with self.assertRaises(ValidationError):self.verify()

    def test_authority_can_be_unknown(self):
        self.change('objects/agent.json',lambda o:o['spec'].pop('authorityRef'))
        self.assertFalse(self.verify()['authorityVerified'])

    def test_wrong_party_target_rejected_for_all_four_objects(self):
        original={p.name:p.read_text() for p in (self.root/'objects').glob('*.json')}
        for name,field in [('agent','servesRef'),('agent','authorityRef'),('environment','controllerRef'),('binding','controllerRef'),('world','controllerRef')]:
            with self.subTest(name=name,field=field):
                self.change('objects/'+name+'.json',lambda o:o['spec'][field].update(objectId='urn:ode:example:personal:dna'))
                with self.assertRaisesRegex(ValueError,'Wrong target kind'):self.verify()
                (self.root/'objects'/ (name+'.json')).write_text(original[name+'.json'])

    def test_organization_object_still_usable(self):
        self.change('objects/person.json',lambda o:o.update(kind='Organization',spec={'identity':{'name':'Example team company'},'accessBoundary':'Example only'}))
        self.change('manifest.json',lambda m:next(x for x in m['objects'] if x['path']=='objects/person.json').update(kind='Organization'))
        self.verify()

    def cross_boundary(self):
        other={'objectId':'urn:ode:example:external:team','version':'1.0.0'}
        self.change('manifest.json',lambda m:m['externalDependencies'].append(dict(other,reason='Team controls environment; resolve before admission')))
        for name in ['environment','binding']:
            self.change('objects/'+name+'.json',lambda o:o['spec'].update(controllerRef=other))

    def test_cross_boundary_requires_policy(self):
        self.cross_boundary()
        self.change('objects/agent.json',lambda o:o['spec'].pop('policyRefs'))
        with self.assertRaisesRegex(ValueError,'Cross-boundary'):self.verify()

    def test_cross_boundary_with_policy_is_structural_only(self):
        self.cross_boundary();result=self.verify()
        self.assertEqual(result['externalDependencies'],1)
        self.assertFalse(result['authorityVerified']);self.assertFalse(result['runtimeTested'])

    def test_binding_controller_must_match_environment(self):
        self.cross_boundary()
        self.change('objects/binding.json',lambda o:o['spec']['controllerRef'].update(objectId='urn:ode:example:personal:person'))
        with self.assertRaisesRegex(ValueError,'controllers disagree'):self.verify()

    def test_ref_relation_annotation_does_not_change_identity(self):
        self.change('objects/binding.json',lambda o:o['spec']['controllerRef'].update(relation='controlled-by'))
        self.verify()

    def test_mixed_versions_rejected(self):
        self.change('objects/dna.json',lambda o:o.update(schemaVersion='0.1.0-draft'))
        with self.assertRaisesRegex(ValueError,'schema version'):self.verify()

    def test_old_organization_field_not_silently_reinterpreted(self):
        self.change('objects/agent.json',lambda o:o['spec'].update(organizationRef=o['spec'].pop('servesRef')))
        with self.assertRaises(ValidationError):self.verify()

    def test_previous_clinic_packages_unchanged_and_valid(self):
        for name in ('clinic-employee','clinic-backup'):
            result=contract.check(ROOT/'examples'/name,ROOT)
            self.assertEqual(result['specVersion'],'0.1.0-draft')

    def test_unknown_version_rejected(self):
        self.change('manifest.json',lambda m:m.update(specVersion='9.0.0'))
        with self.assertRaisesRegex(ValueError,'Unsupported specification'):self.verify()

    def test_checksum_required(self):
        self.change('objects/person.json',lambda o:o['spec'].update(category='family'))
        with self.assertRaisesRegex(ValueError,'Checksum mismatch'):contract.check(self.root,ROOT)


if __name__=='__main__':unittest.main()
