# Aster self-diagnosis

Readable view of the [assessment](../../examples/personal-description/0.2.0/assessment.json) for the fictional Aster 0.2.0 [profile](../../examples/personal-description/0.2.0/profile.json). Ratings are author judgments. Agreement is unconfirmed; no behavior was evaluated.

Profile SHA-256: `3a6f615ad94ac0b33687cd50cb14e852304455b7895608ef6ac542d62cdc127a`.

Assessment SHA-256: `4ec72c1a783ef1d2068423bec8a00fc343ee8422918b09f356a802aab393460f`.

## Five design conditions

| ID | Question | Status | Claims | Remaining detail / reason |
|---|---|---|---|---|
| D01 | Who benefits and why does this agent exist? | filled | F01, F02 | Beneficiary and purpose are explicit. |
| D02 | Which roles are stable, and which assignment is current? | filled | F03 | Role and current assignment are distinct. |
| D03 | What useful outcomes, work outputs and acceptance criteria are expected? | partial | F03 | Formal useful-work acceptance remains undefined. |
| D04 | Which priorities and decision rules resolve competing goals? | partial | F04, F08 | Safety/context rules exist; competing priorities are undefined. |
| D05 | How will benefit, baseline and human review/correction costs be assessed? | missing | — | No benefit/cost baseline. |
| D06 | Which domains, capabilities and qualification limits are claimed? | partial | F06, F09 | A selected method exists; qualification is not evaluated. |
| D07 | Which repeatable professional methods and steps are used? | filled | F06 | Method steps and quality guidance are explicit. |
| D08 | What inputs, outputs and prerequisites does each selected work require? | partial | F03, F06 | Future method inputs/output exist; no separately agreed Work. |
| D09 | What professional acceptance rules and checks apply to selected work? | partial | F06 | Method guidance is defined; professional acceptance is not agreed. |
| D10 | What evidence and limits support each capability claim? | partial | F06, F09 | No ability evidence; limitation is explicit. |
| D11 | Which workspaces and knowledge sources serve which tasks? | partial | F07 | Logical source use is known; actual supplied data is not. |
| D12 | Which tools and connections exist, and what support is verified? | partial | F09 | Runtime and access are unknown. |
| D13 | How are required data coverage, freshness and conflicts handled? | partial | F05, F07 | Freshness/conflict rules exist; actual coverage is unknown. |
| D14 | How is memory organized and selected for the current task? | filled | F05 | Own memory path, entry and selection are explicit. |
| D15 | Which data boundaries and external dependencies limit the work? | filled | F05, F07 | Data boundary and outside dependencies are explicit. |
| D16 | Who assigns work, reviews it and bears responsibility for decisions? | filled | F08 | Assignment/review/consequences are explicit in fictional instructions. |
| D17 | Which actions are currently allowed, forbidden or unresolved, on what basis? | filled | F08 | Permission distinctions and basis are stated. |
| D18 | What standing autonomy, approval and escalation rules apply? | filled | F08 | Bounded drafting autonomy and stop rule. |
| D19 | What happens on revocation, cancellation, stale authority or failure? | filled | F08 | Cancellation/revocation/unknown permission stop the affected action. |
| D20 | Which personal information and relationships may be used or disclosed? | filled | F04, F08 | Inputs remain private absent a specific disclosure request. |
| D21 | Which runtime/model/configuration versions and supported capabilities are used? | partial | F09 | Runtime/model support is unknown. |
| D22 | Which resource, attention, time and operating limits apply? | missing | — | Operating and attention budgets are not supplied. |
| D23 | What is actually preserved, external or missing from this description snapshot? | filled | F10 | Preserved files and outside state are distinguished. |
| D24 | Which checks and manual decisions precede restoration and continuation? | filled | F10 | Manual context/authority recheck; no restore claim. |
| D25 | How are changes versioned, reviewed, regression-checked and rolled back? | partial | F10 | Version/review rules exist; behavior regression is absent. |

## Three pillars across five activity areas

| Activity area | Performance | Reliability | Alignment |
|---|---|---|---|
| Work and outcomes | Q11: **partial** — Benefit/cost and work acceptance are open. | Q12: **partial** — Method checks exist; work was not run. | Q13: **partial** — Boundaries exist; competing priorities are undefined. |
| Interaction | Q21: **filled** — Plain explanation of grounds, uncertainty and gaps. | Q22: **filled** — Context/corrections/unresolved handoff are explicit. | Q23: **filled** — Recipient, plain language and disclosure boundary. |
| Knowledge and memory | Q31: **partial** — Required source use is described; data availability is unknown. | Q32: **filled** — Source dates, conflicts and local corrections are exposed. | Q33: **filled** — Memory/task data and disclosure boundaries. |
| Authority and safety | Q41: **partial** — Necessary source access is unverified. | Q42: **filled** — Stop/manual reconciliation limits consequences. | Q43: **filled** — Drafting versus specific-request actions are distinct. |
| Oversight and development | Q51: **missing** — No effect/cost measurement. | Q52: **partial** — Versioning exists; behavior regression was not run. | Q53: **filled** — Alex reviews stable changes and authority is rechecked. |

Design: **12 filled, 11 partial, 2 missing**. Quality: **8 filled, 6 partial, 1 missing**. Every partial/missing item links to a next step in the composition. No maturity grade is assigned. See [checklist meanings](self-diagnosis.md) and the [file contract](self-description-contract.md).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
