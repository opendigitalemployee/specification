# Status and scope

Draft release **0.2.0-draft.2**, package format **0.2.0-draft**. The format describes a digital employee; it is not a runtime, marketplace, certification system, or guarantee of business outcomes.

## Current contract

The normative draft contains 34 object kinds, a manifest, exact versioned references and resource integrity rules. Three design layers describe domain expertise (DNA), a personal or shared working environment, and a specific employee. Deployment and captured state are additional records, not additional design layers. The manifest determines inventory; example filenames describe an illustrative domain rather than prescribe every employee's folder.

Export is checked internally using a private reference toolchain: package validation, schema reproduction and byte preservation across file packaging/restoration. The package/backup reference tools are not distributed. Read-only package relationship/integrity and experimental description checkers are distributed with the automated checks. Prior 0.1 schemas are preserved for version-directed validation; old example bytes are unchanged. Business quality, runtime permission enforcement and admission require separate tests. The synthetic example contains illustrative goals and evidence, not a claim of observed revenue growth.

## Experimental personal self-description

[Agent entry](docs/agents/README.md): versioned profile, composition, assessment and index; 25 design questions and 15 quality questions; a blank collection and the fictional Aster 0.2.0 example. Experimental contracts are under `spec/research/proposals/`, separate from normative object schemas. The description can finish with routed unknowns and partial answers. An assessment is part of the collection and pins the evaluated profile.

Public checks cover file structure, references, hashes and boundary regression cases. They do not establish truth, independent adoption, owner agreement, agent behavior or runtime compatibility. No private real-agent files are included. The broader [issue #4](https://github.com/opendigitalemployee/specification/issues/4) remains open. Backup traversal/cuts and migration assessment remain separate. Normative 0.2 affiliation is now available through Party and explicit service, authority and environment-control references; it does not model legal ownership or the full proposed Person/Consent system. See the [procedure index](docs/agents/procedures/README.md) and [three worked affiliation cases](docs/agents/procedures/affiliation.md).

## Adapters

Runtime adapters are not distributed in this first release. Internal prototypes are not evidence of runtime compatibility. A policy written in instructions is not an enforcement mechanism. Real connectors, credentials, remote databases and runtime sessions are not provisioned. Other environments shown on the site offer skill-format entry points; that is not equivalent to a complete adapter.

## Next-version proposals

**Work and Workflow:** Work is the result and acceptance contract. Workflow defines execution steps and transitions; skills supply methods and tools expose operations. The separation is accepted in the design, but Workflow/WorkflowBinding are not normative 0.2 kinds. No universal workflow DSL or conversion is promised.

**Person:** The proposed person model links an employee to its human participants. It separates stable qualities, contextual agreements, live state and history. Access is an independent dimension: approved work-facing information may enter a work package; personal information stays in separate storage on behalf of the person. Restoring a snapshot must not make stale observations current or reinstate revoked consent. These are design requirements; the 0.2 validator does not implement the extended Person contracts or enforce consent.

## Publication readiness

The selected license split is Apache-2.0 for the normative specification, schemas, examples and automated checks, and CC BY 4.0 for explanatory documentation and glossary. Copyright and attribution: **Taras Pustovoy and contributors**. See [license scope](LICENSING.md). Export produces a local reviewed snapshot; publication on GitHub is a separate action. `release-manifest.json` records checks actually performed; they cover schema consistency and package bytes, not model behavior.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
