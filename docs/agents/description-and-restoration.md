# Description views and restoration

**Informative agent-facing design proposal · 0.2.0 · 4 October 2026.** This material extends the CHG-0003 discussion using the existing [composition](../../spec/COMPOSITION.md) and [package/backup rules](../../spec/SPECIFICATION.md). It does not add normative kinds, fields, profile values or a certified personal backup. The current ClientAgent still requires Organization relationships.

## Two views of one agent

| View | Question | Content | What the view supports |
|---|---|---|---|
| Reflective description | Who am I, whom do I serve, why and within what boundaries? | Purpose, identity, roles, values, hypotheses, limits and uncertainties, with basis/date | Discussion, reflection and choosing work |
| Composition with evidence | What concretely makes up this agent, which version and what does each part depend on? | Native instructions and identity artifacts, selected class basis, memory zones, methods, work/data relationships, runtime requirements and scoped state; exact references and observed evidence | Inspecting claims, finding gaps and designing a preservation/restoration scope |

These are complementary views, not mandatory successive maturity grades. A concise answer can be well-evidenced; a long answer can contain unverified assumptions. Keep the same identities and references across views rather than separate conflicting sources of truth. A native identity file may be SOUL.md or another name; assign its semantic role from content and owner decisions, not its filename alone.

## Component map

A proposed map records each selected component's purpose, reusable/local placement, native source and version, relationships, lifecycle, current-use status, observed evidence, missing detail and disclosure boundary. Distinguish current instructions from historical bootstrap files; selected memory from the whole corpus; available methods from selected skills and tested abilities; provenance sources from work-data stores.

Use existing Skill/native resources, Work references, Source/Storage/Environment and relevant policies/decisions where their semantics fit. The map is a view of this composition. Personal principal/ownership and the semantics of a shared identity/class basis remain design questions; do not invent an Organization or silently redefine professional AgentDNA. A map and a metadata audit remain separate from a normative package manifest.

The concrete map belongs in the owner's agent collection, beside its description and dated audits. The [experimental collection contract](self-description-contract.md) supplies an indexed composition view; local folder names remain a convention. Reusable guidance belongs here in the standard source. A private map's source paths and selected relationships are independently reviewed before disclosure.

<a id="description-capture-boundary"></a>

## Description and backup have separate deliverables

| Stage | Deliverable | Completion boundary |
|---|---|---|
| Self-description | Answer/profile/component files, indexed versions, native/source references and meaningful known dependency relationships | Selected known composition and unknowns are explicit; no recursive capture required |
| Backup | Contextual dependency plan, selected cut, included bytes/derivatives, outside/missing resources, manifest/lock and archive report | Completeness is checked against the declared preservation purpose and scope |
| Restoration | Destination provisioning, scoped restored resources and permitted continuation evidence | Successful file transfer alone does not establish working capability or renewed authority |

Ownership/semantic placement and byte inclusion are independent. Shared basis or an environment dependency may be captured for a chosen scope without becoming the agent's own identity. A source locator is not an instruction to include the surrounding repository, all available skills or all reachable projects.

Traversal limits and summaries belong to the backup policy. A derived summary retains its source revisions, its own identity/digest, coverage and loss boundaries; it cannot be substituted silently for an exact required resource. A self-contained description set, a complete scoped snapshot and a runnable destination are separate claims. The existing manifest/resources/lock and explicit dependency contracts should serve packaging; the personal experimental description remains distinct from a normative ClientAgent.

## Restoration is an independently assessed result

Detailed composition enables a restoration plan. To restore a selected target, the actual required resources or resolvable external dependencies, a procedure and scoped evidence are also needed. A source reference or hash alone cannot reconstruct missing bytes.

| Check | Required distinction | Evidence to record |
|---|---|---|
| Target and scope | Description files, selected native configuration/memory, restored working capability and active process state are different targets | Declared target, required scope, explicitly excluded/missing parts |
| Capture and dependency closure | Included bytes, reproducible derivatives and external resources | Exact object/resource inventory, pins/checksums, as-of dates, consistency, full selected skill directories and snapshot coverage |
| Destination and procedure | File restoration versus runtime support/access provisioning | Target environment/configuration, dependency support report, reconstruction steps and separately provisioned secret/access requirements |
| File restoration | Preserved resources versus a readable description of them | Scoped import/restore result and verified bytes/identities |
| Permitted continuation | Successful file restoration versus safe work continuation | Current authority/freshness checks, unfinished obligations and other executor reconciliation, then results of the selected continuation checks |

The existing specification requires manual continuation and forbids automatic resumption/replay. Restoration cannot reinstate revoked rights. Restore and clone are distinct: a new agent identity and rebound ownership/access need to be explicit. A scoped trial does not prove unchanged model behavior or continuous preservation of an executing process.

Report each check as not assessed, partial, passed or failed with scope/date/evidence; these are proposed assessment labels, not new normative enums. A description-maturity level from [self-diagnosis](self-diagnosis.md) does not imply a passing restore. Agreement, behavior, current authority and runtime readiness retain separate evidence.

## Current scope and later work

The [synthetic description](../../examples/personal-description/0.2.0/README.md) includes profile, composition, native files, explicit dependencies and assessment. Structural checks verify declared references and bytes. No personal backup, restore trial or running-agent evaluation is produced by this route.

Backup traversal, tail cutting and packaging are a separate product need. A restoration target and trial require their own scope. Migration exam design remains deferred. Keep description, captured resources and actual test results independently versioned and linked.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
