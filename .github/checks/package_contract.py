"""Read-only package schema, inventory, typed-reference and affiliation checks.

No resources are executed, external dependencies fetched, or permission granted.
This is a structural check, not the private pack/restore tool.
"""
import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

CURRENT_VERSION = '0.2.0-draft'
SUPPORTED_VERSIONS = ('0.1.0-draft', CURRENT_VERSION)


def schema_directory(root, version):
    if version not in SUPPORTED_VERSIONS:
        raise ValueError('Unsupported specification version: '+str(version))
    root = Path(root)
    return root/'spec/schema' if version == CURRENT_VERSION else root/'spec/versions'/version/'schema'


def identity(ref):
    return ref['objectId'], ref['version']


def validate_relationships(objects, version):
    for obj in objects.values():
        spec = obj['spec']
        if version == '0.1.0-draft' and obj['kind'] in ('ClientAgent', 'ToolBinding'):
            env = objects.get(identity(spec['environmentRef']))
            if env and identity(env['spec']['organizationRef']) != identity(spec['organizationRef']):
                raise ValueError('Organization and environment disagree for '+obj['id'])
        if version == CURRENT_VERSION and obj['kind'] == 'ToolBinding':
            env = objects.get(identity(spec['environmentRef']))
            if env and identity(env['spec']['controllerRef']) != identity(spec['controllerRef']):
                raise ValueError('Tool binding and environment controllers disagree for '+obj['id'])
        # Serving a person does not require owning every environment used by them.
        # Cross-boundary access needs an explicit policy reference; its existence
        # does not prove approval, enforcement, or runtime readiness.
        if version == CURRENT_VERSION and obj['kind'] == 'ClientAgent':
            env = objects.get(identity(spec['environmentRef']))
            if env and identity(env['spec']['controllerRef']) != identity(spec['servesRef']) and not spec.get('policyRefs'):
                raise ValueError('Cross-boundary agent requires explicit policyRefs: '+obj['id'])


def read(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out: raise ValueError('Duplicate JSON key: '+key)
            out[key] = value
        return out
    def constant(value): raise ValueError('Non-finite JSON: '+value)
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=constant)


def local(root, path):
    if not isinstance(path, str) or not path or '\\' in path or ':' in path or '\0' in path or any(x in ('', '.', '..') for x in path.split('/')):
        raise ValueError('Unsafe package path: '+str(path))
    current = root
    for part in path.split('/'):
        current = current/part
        if current.is_symlink(): raise ValueError('Symlink in package: '+path)
    if not current.is_file(): raise ValueError('Missing package file: '+path)
    return current


def references(value, rules, field=None):
    if isinstance(value, dict):
        if 'objectId' in value:
            if set(value)-{'objectId','version','relation'} or not isinstance(value.get('objectId'),str) or not isinstance(value.get('version'),str):
                raise ValueError('Malformed exact reference')
            yield value, rules.get(field)
        else:
            for key, child in value.items():
                if key != 'extensions': yield from references(child,rules,key)
    elif isinstance(value,list):
        for child in value: yield from references(child,rules,field)


@lru_cache(maxsize=16)
def validator(schema_text):
    schema=json.loads(schema_text)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema,format_checker=FormatChecker())


def check(package, standard_root):
    package = Path(package).absolute()
    manifest = read(local(package,'manifest.json'))
    version = manifest.get('specVersion')
    schemas = schema_directory(standard_root,version)
    def validate(value,name):
        validator((schemas/name).read_text()).validate(value)
    validate(manifest,'manifest.schema.json')
    objects = {}; files = {'manifest.json'}
    for item in manifest['objects']:
        path = item['path']
        if path in files or path=='package.lock.json': raise ValueError('Duplicate/reserved inventory path')
        files.add(path); obj=read(local(package,path))
        if obj.get('schemaVersion') != version: raise ValueError('Object schema version disagrees with manifest')
        validate(obj,'object.schema.json')
        if any(obj[k]!=item[k] for k in ('id','version','kind')): raise ValueError('Object descriptor mismatch')
        key=(obj['id'],obj['version'])
        if key in objects: raise ValueError('Duplicate object identity')
        objects[key]=obj
    for resource in manifest['resources']:
        path=resource['path']
        if path in files or path=='package.lock.json': raise ValueError('Duplicate/reserved inventory path')
        local(package,path);files.add(path)
    external={identity(x) for x in manifest['externalDependencies']}
    if len(external)!=len(manifest['externalDependencies']) or external & objects.keys(): raise ValueError('Duplicate external dependency')
    rules=read(schemas/'reference-kinds.json')
    for owner, value in [('entrypoints',manifest['entrypoints'])]+[(o['id'],o) for o in objects.values()]:
        kind_rules=dict(rules)
        if value.get('kind') in ('Work','Skill'): kind_rules['basedOn']=[value['kind']]
        for ref, kinds in references(value,kind_rules):
            key=identity(ref); target=objects.get(key)
            if key not in objects and key not in external: raise ValueError('Unresolved reference from '+owner)
            if target and kinds and target['kind'] not in kinds: raise ValueError('Wrong target kind from '+owner)
            if target and value.get('layer')=='dna' and target['layer']!='dna': raise ValueError('DNA binds local context')
    for group, kind in [('dna','AgentDNA'),('environments','Environment'),('agents','ClientAgent')]:
        for ref in manifest['entrypoints'].get(group,[]):
            if objects.get(identity(ref),{}).get('kind')!=kind: raise ValueError('Invalid included entrypoint: '+group)
    required={'dna':'dna','environment':'environments','client':'agents','backup':'agents'}[manifest['profile']]
    if not manifest['entrypoints'].get(required): raise ValueError('Missing required package root')
    validate_relationships(objects,version)
    lock=read(local(package,'package.lock.json'))
    if lock.get('format')!='digital-employee-lock' or lock.get('specVersion')!=version or lock.get('packageId')!=manifest['id'] or lock.get('packageVersion')!=manifest['version'] or set(lock.get('files',{}))!=files:
        raise ValueError('Lock disagrees with manifest')
    for path in files:
        if hashlib.sha256(local(package,path).read_bytes()).hexdigest()!=lock['files'][path]: raise ValueError('Checksum mismatch: '+path)
    return {'valid':True,'specVersion':version,'objects':len(objects),'externalDependencies':len(external),
            'scope':'schemas, exact references, affiliation relations, inventory and hashes',
            'nativeFormatsChecked':False,'runtimeTested':False,'authorityVerified':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path);parser.add_argument('--standard-root',type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    print(json.dumps(check(args.package,args.standard_root),indent=2))
