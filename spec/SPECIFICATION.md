# Digital Employee Package specification draft

Version `0.2.0-draft`. The names and namespace are provisional. This draft defines a package for designing, preserving and adapting digital employees. It describes independently versioned objects, included resources and exact dependencies. It does not equate successful import with successful work.

Informative future proposals separate Work (the outcome contract) from Workflow (execution), and describe extended personal profiles and consent. See [status and proposals](../STATUS.md#next-version-proposals). Party affiliation is normative in 0.2; the broader proposals are not implemented by these schemas or validators.

The model has three design layers: **Agent DNA + contextual goals + working environment → client agent**. Deployment records and operational state are additional package contents, not additional DNA inheritance layers.

## 1. Three design layers

**Agent DNA** describes a professional foundation: possible outcomes, roles, work definitions, skills and meta-skills, decision styles, quality checks, policies and environment requirements. Person-, family-, team- or organization-specific choices require deliberate generalization before becoming reusable DNA.

**Working environment** describes the concepts and operating resources controlled by a person, family, team, organization or another named party. It includes party boundaries, the environment, entity types, world-model instances, sources, storage, transformations, data-product contracts, connections and knowledge governance. An environment definition is separate from the records and bytes held in its systems.

**Client agent** pins a DNA version, the party it serves and an environment. It selects work, goals, methods and styles, records local customizations, and binds tools, skill activations and interaction contracts to that context. Several client agents may share an environment. Updating DNA or a shared object MUST NOT silently change these pins.

The package may also contain receipts, records, facts, data snapshots, runs and evidence. Their provenance and input/definition pins MUST remain explicit. A world-model instance has its own identity; selecting an instance as current is distinct from creating a new version of a definition.

### 1.1. Affiliation, authority and environment control

`Party` identifies a person or collective involved in these relationships. Its `category` MUST be one of `person`, `family`, `team`, `organization` or `other`. For `other`, `categoryLabel` MUST name the local category. A Party's object ID and title identify the described party; no organization, registry number, legal name, contact details or membership roster is required. A pseudonymous identity is permitted. The [party category catalog](schema/party-categories.json) records the codes, names and definitions and is generated from the same source as the schema. Adding or redefining a global code requires a new specification version; local categories use `other` with categoryLabel. Particular party instances are kept in packages or owner-controlled libraries, not in the global category directory. Category describes the party, not the agent's role, class, ownership rights, jurisdiction or capabilities. `Role` continues to describe assistant, manager or professional responsibilities.

| Relationship | Meaning | Target |
|---|---|---|
| `ClientAgent.spec.servesRef` (required) | Party served in this concrete agent context | Party or Organization |
| `ClientAgent.spec.authorityRef` (optional) | Party responsible for assigning/reviewing work and deciding authority within this context | Party or Organization |
| `Environment.spec.controllerRef` (required) | Party responsible for this environment boundary | Party or Organization |
| `ToolBinding.spec.controllerRef` (required) | Controller of the environment containing the binding | Party or Organization |
| `WorldModel.spec.controllerRef` (required) | Party responsible for this model instance and its governance | Party or Organization |

An existing `Organization` kind remains usable at these references when its richer organization identity/access boundary is needed. It is not required for personal agents. Do not create both a Party and an Organization for the same entity without an explicit reason and identity mapping. One concrete ClientAgent has one served-party context; a team or family can represent a collective. Multiple independent service contexts use distinct agent configurations. This draft does not specify membership, legal ownership or multi-party authority resolution.

Served party, authority party and environment controller MAY differ. A ToolBinding controller MUST match its referenced Environment controller by exact identity/version when included. A ClientAgent serving a different party from its Environment controller MUST declare nonempty `policyRefs` describing the access boundary. A policy reference alone MUST NOT be treated as approval or runtime enforcement. External party/environment dependencies remain unresolved requirements; consumers MUST resolve and check these relationships before admission. An omitted `authorityRef` means authority is not supplied; it MUST NOT be inferred from `servesRef` or environment control. Actual permitted actions, approvals, enforcement and revocation belong in Policy and related agreements. `ownerRef` remains separate provenance/ownership metadata; it is not a substitute for these relationships. `Policy.principalRef` and `Deployment.principal` keep their existing actor/runtime meanings.

## 2. Objects and identity

The normative machine-readable contracts are `schema/object.schema.json`, `schema/manifest.schema.json` and the named target-kind rules in `schema/reference-kinds.json`. `schema/type-catalog.json` is generated documentation of the type catalog. The schema generator must regenerate identical schema files after a change.

Each object MUST have `schemaVersion`, `kind`, `layer`, `id`, `version`, `title`, `status`, `provenance` and `spec`. `ownerRef`, additional semantic `refs` and namespaced `extensions` are optional. Object identity is the pair `(id, version)`; an ID is stable across revisions. Published content at an existing identity/version MUST NOT be replaced with different content. Authors create a new version for semantic changes.

References use `{ "objectId": "…", "version": "…" }`, optionally with a relationship. The `objectId` member is reserved for this reference shape in canonical object contracts; native artifacts and optional extensions remain opaque to graph traversal. Floating versions and unresolved implicit lookup are not part of this draft. References MUST resolve to an included object or an explicit external dependency. Package consumers MUST verify the kinds of mandatory root references and the known named relationships. Object IDs should be namespaced; filenames are locations, not identities.

`draft`, `proposed`, `agreed` and `retired` describe definition status. They do not prove successful execution or technical authorization. Evidence and deployment admission are independent records. An unfilled parameter or unavailable measurement must not become a successful result or numeric zero.

## 3. Package manifest and profiles

The root MUST contain `manifest.json`. It identifies the package, version, specification version, profile, roots, object inventory, resource inventory, external dependencies and adopted standards. All object descriptors MUST agree with the actual object ID, version and kind. Included paths MUST be relative, unambiguous, stay within the package and contain no symbolic links.

The four profiles are:

| Profile | Required root | Intended use |
|---|---|---|
| `dna` | AgentDNA | Publish or edit a professional foundation |
| `environment` | Environment | Describe or preserve a personal or shared working environment |
| `client` | ClientAgent | Design or adapt a concrete employee with declared environment dependencies |
| `backup` | ClientAgent and explicit backup scope | Preserve the selected employee, knowledge and optional state for restoration |

A package can include multiple independently versioned roots. Inclusion does not transfer ownership or grant runtime permissions. A portable client package can bundle selected environment objects while declaring infrastructure resources that must be provided at the destination.

Included dependency closure MUST be explicit. An unresolved dependency MUST cause a validation failure. An explicitly declared external dependency is a visible requirement; validators must report it, and adapters must resolve it or report a blocking gap before launch. Merely declaring it does not make a package self-contained.

## 4. Physical storage

Objects use JSON. Human instructions and explanations use Markdown resources. Native artifacts retain the external standard's representation. Recommended authoring layout:

```text
manifest.json
package.lock.json
dna/<name>/<version>/*.json
environments/<environment-id>/<version>/*.json
agents/<name>/<version>/*.json
native/skills/<skill-name>/SKILL.md
native/skills/<skill-name>/references/*
assets/*
snapshots/*
deployments/*
```

The layout is a convention; the manifest inventory is authoritative. Every file in an included native skill directory MUST be included in the resource inventory. Resources MUST preserve their original bytes unless the author deliberately edits them.

An authoring directory may be edited without a fresh lock. A portable release MUST contain `package.lock.json` with exact SHA-256 digests for `manifest.json` and every declared object/resource file. The lock MUST agree with the inventory. Editing content invalidates the lock; the author validates and regenerates it before packaging. The lock is not a signature and does not establish publisher authenticity.

The reference implementation provides ZIP archives and a single JSON bundle containing base64 file bytes. These are transport representations of the same directory. They MUST preserve included files, object identities and pins. Tools MUST reject conflicting destinations and inconsistent inventories. Schema-valid objects, content integrity, complete resource inclusion and successful execution are distinct checks.

## 5. Composition with existing standards

The package describes how native artifacts participate in employee work. Their native files remain authoritative for their own format. A Skill object's artifact points to an Agent Skills directory entrypoint; its input/output contract, activation, version and business relationships are described by our objects. See `COMPOSITION.md`.

The manifest records a standard identifier, primary specification URL, observed revision and whether support is required. An importer may preserve unsupported optional artifacts with a visible limitation. It MUST NOT claim support for an unknown required format or discard it silently. Unknown optional namespaced extensions MUST be preserved during editing and transfer. Unknown required extensions MUST block unsupported consumers; requirements are declared in `requiredExtensions`.

## 6. Versioned composition and local changes

A client agent selects exact objects rather than copying an entire DNA catalog. A local Work or Skill may declare `basedOn` and receive its own identity/version. The client refers to this selected object. This draft does not define automatic deep merging, executable inheritance or a language-specific patch engine.

A full view of the agent resolves this composition. It remains a view of the existing objects. Provenance records why a value or method changed. Goals, metric definitions, thresholds and work methods are definitions; measurements and observations are separate state. Changed definitions require reviewing affected checks and consumers.

## 7. Backup and restoration

A backup MUST declare `capturedAt`, consistency mode, selected scope, missing resources and `resumePolicy: manual`. Selected knowledge may include receipts, facts, master records and data snapshots. Each data snapshot MUST record its subject, as-of time, coverage, quality state and actual included artifact.

The backup MUST distinguish included bytes, reconstructible derivatives and externally retained resources. A Source descriptor alone is not a copy of its database. Indexes, caches, connector credentials and model-dependent state may require reconstruction or separate provisioning. Secret values are outside the public package format; connection and tool objects declare secret references and requirements.

Restoration preserves identities and exact selected versions. It MUST NOT start schedules, resume unfinished actions or replay effects automatically. Continuation requires checking whether the previous executor is still active, inspecting unfinished obligations and reconciling action receipts. Creating a new employee from an existing package is a clone operation: it creates a new client identity with recorded lineage and rebinds ownership and access. These two operations must be distinguishable to users.

The reference restore tool verifies and restores the declared file snapshot only. It does not restore remote databases, runtime sessions, credentials or executing jobs. A best-effort backup must report its consistency limitations.

## 8. Runtime adaptation and conformance

An adapter consumes pinned objects and resources, maps requirements to runtime capabilities, generates native configuration and emits a support report. Requirements MUST remain traceable to their source objects. Unsupported mandatory capabilities MUST block a launch-ready claim. Instruction text and a runtime mechanism that enforces a restriction must be distinguished.

Conformance is scoped: a reader may preserve packages, an editor may round-trip supported objects, a packager may verify inventory and integrity, and an adapter may support specified requirements on pinned runtime versions. None of these proves business performance. Quality is assessed separately through work cases and evidence across performance, reliability and alignment.

## 9. Migration and changes to the draft

Migrating legacy formats MUST retain the source and report inferred mappings, unresolved decisions and unsupported semantics. Extracting client-specific content into a DNA object must remain a reviewed proposal. A migration MUST NOT fabricate verified environment connections or successful evidence.

The schemas specify a typed minimum contract for 34 object kinds. Several domain-specific structures remain open JSON contracts in this draft; their detailed vocabularies require further examples and review. The initial implementation must describe these limits rather than claim complete coverage of every domain. Changes to normative semantics go through a documented proposal and a new specification version.

### 9.1. Compatibility with 0.1.0-draft

The previous contracts remain byte-preserved under `versions/0.1.0-draft/schema/`. A consumer MUST select schemas by `manifest.specVersion` and MUST reject unknown versions or included objects whose `schemaVersion` differs from the manifest. Locks and single-file bundles MUST carry the same specification version as their package. The published clinic examples remain 0.1 packages and retain their original bytes. The new [personal package](../examples/personal-agent/manifest.json) uses 0.2 without any Organization object or organizationRef.

Migration to 0.2 is explicit: review the former ClientAgent organizationRef as a candidate served party and separately identify authority; review Environment, ToolBinding and WorldModel organizationRef as candidate controllerRef. An organization may remain an Organization object. Do not infer a person, team or family from a missing organization. Preserve old definitions; issue new object/package versions, update exact references and regenerate integrity records. Merely replacing schemaVersion is not a valid migration. The experimental self-description collection retains its independent 0.1 contract and Aster 0.2.0 example; it is not a DEP package and receives no automatic conversion.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
