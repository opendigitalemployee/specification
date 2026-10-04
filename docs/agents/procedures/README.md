# Procedures for agents

**Informative index · 0.1.0 · 4 October 2026.** This is the maintained entrypoint for published procedures and proposed application scenarios. A procedure is an instruction for a result; a schema defines its file contract. An application profile selects several relevant tasks; it is not an agent category or `manifest.profile`.

## Available procedures

| ID / version | When to use | Prerequisites | Result / completion |
|---|---|---|---|
| [SELF-01 / 0.3.0](self-description.md) | Describe an existing agent, its purpose, composition and gaps | An explicit purpose and authorized sources; unknown facts may remain unknown | Profile, composition, linked 25+15 assessment and pinned index; structural check passes; unfilled items have next steps. Experimental; independent repetition and behavior remain unverified. |
| [AFFILIATION-01 / 0.1.0](affiliation.md) | Create a normative package for a personal or collective agent | Known served party and environment controller; exact objects or explicit external dependencies | 0.2 ClientAgent/Environment relationships and package pass structural validation. No Organization required for a person, family or team. |

Composition, self-diagnosis and collection checking are stages of SELF-01, supported by the [composition guide](../component-description.md), [checklist](../self-diagnosis.md) and [collection contract](../self-description-contract.md). They do not require separately completing other application scenarios.

## How to choose an order

- For an existing agent whose description is missing: SELF-01 → review the description and its open items. Use AFFILIATION-01 only if a normative DEP package is needed.
- For a package whose purpose and parties are already known: begin with AFFILIATION-01 directly. SELF-01 is helpful input, not a mandatory dependency.
- Before a package check: identify parties → distinguish service/authority/environment control → create or pin the objects → validate references and integrity. Resolve external dependencies and actual permissions before runtime admission.
- Preservation/recovery is a later, separately scoped task when requested. It does not follow automatically from finishing either procedure.

These are conditional routes, not a compulsory pipeline. Completing a self-description does not assert responsible-party agreement, readiness, backup completion or observed capability.

## Proposed scenarios from issue #2

The [original proposal](https://github.com/opendigitalemployee/specification/issues/2) contains nine scenarios and four suggested profiles. It did not report nine executed experiments. Status below describes the material available in this release.

| Scenario | Current coverage / next work |
|---|---|
| SELF-01 — understand my role | Experimental published procedure above; covers description, not runtime proof |
| PARTS-01 — separate my components | Composition stage within SELF-01; no separate standalone procedure version |
| MEMORY-01 — continue across sessions | Memory is described in SELF-01; tested continuation procedure remains proposed |
| RESTORE-01 — plan preservation/recovery | [Description/recovery boundary](../description-and-restoration.md) and [normative backup rules](../../../spec/SPECIFICATION.md#7-backup-and-restoration); no published backup traversal/cutting tool or complete operational procedure |
| USER-01 — understand my user | Proposed; personal-data and decision experiment not implemented |
| WORK-01 — improve professional work | Proposed; Work/Skill/Check definitions exist, comparative procedure remains open |
| ENV-01 — organize my environment | Proposed; environment schema and affiliation procedure cover only part of the need |
| TEAM-01 — coordinate people/agents | Proposed; no tested handoff procedure |
| IMPROVE-01 — evaluate a change | Proposed; no longitudinal improvement procedure |

Suggested profiles remain personal foundation (SELF/USER/MEMORY), team coordination (SELF/TEAM/ENV), professional practice (SELF/WORK/IMPROVE), and environment/portability (PARTS/ENV/RESTORE). One agent may use several profiles. Their universal contract and exact dependency pins remain a separate issue #2 decision; this index does not ratify the entire proposal.

## Maintenance

Keep each maintained procedure here with an ID, version, prerequisites, result, completion check and evidence limits. Changes to steps or meaning increment its procedure version; output schema and normative package versions change only when their own contracts change. Record additions and moves in the release changelog. Preserve old paths as pointers when published examples use them. Add proposed scenarios to this index with their status before presenting them as available procedures. The website should consume this entrypoint from a pinned public release.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
