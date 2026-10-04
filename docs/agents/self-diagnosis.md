# Checklists for agent self-diagnosis

**Informative application material · 0.2.0 · 4 October 2026.** Use these checklists while building or reviewing a personal-agent description in SELF-01. They are part of the agent-facing application material in the standard source, with a [machine-readable catalog](self-diagnosis.checklist.json). They do not add normative ODE kinds, fields or conformance requirements. The filled assessment is part of the experimental description collection.

Assess a declared use and a pinned description version. Record each check ID, fill status, the exact description field/claim, remaining question, reviewer and date. Keep agreement and behavioral evidence independent. Do not count a category tag as an answer. Keep a scope-specific reason for every non-applicable item.

**Fill statuses:** filled = adequate answer for this use; partial = some answer with missing details; missing = no substantive answer; not_applicable = excluded with a reason. An unknown is useful information but does not supply a missing answer. Empty, missing and not-applicable are distinct.

The profile method already separates source/proposal/clarification/agreement. The current [specification](../../spec/SPECIFICATION.md) separates definition status from evidence and authority; Environment readiness describes another axis. None defines a general description-maturity ladder.

## Five design conditions

| ID | Condition | Question to fill | Fill status | Profile reference | Open question |
|---|---|---|---|---|---|
| D01 | Outcome and alignment | Who benefits and why does this agent exist? | ___ | ___ | ___ |
| D02 | Outcome and alignment | Which roles are stable, and which assignment is current? | ___ | ___ | ___ |
| D03 | Outcome and alignment | What useful outcomes, work outputs and acceptance criteria are expected? | ___ | ___ | ___ |
| D04 | Outcome and alignment | Which priorities and decision rules resolve competing goals? | ___ | ___ | ___ |
| D05 | Outcome and alignment | How will benefit, baseline and human review/correction costs be assessed? | ___ | ___ | ___ |
| D06 | Domain expertise | Which domains, capabilities and qualification limits are claimed? | ___ | ___ | ___ |
| D07 | Domain expertise | Which repeatable professional methods and steps are used? | ___ | ___ | ___ |
| D08 | Domain expertise | What inputs, outputs and prerequisites does each selected work require? | ___ | ___ | ___ |
| D09 | Domain expertise | What professional acceptance rules and checks apply to selected work? | ___ | ___ | ___ |
| D10 | Domain expertise | What evidence and limits support each capability claim? | ___ | ___ | ___ |
| D11 | Prepared environment | Which workspaces and knowledge sources serve which tasks? | ___ | ___ | ___ |
| D12 | Prepared environment | Which tools and connections exist, and what support is verified? | ___ | ___ | ___ |
| D13 | Prepared environment | How are required data coverage, freshness and conflicts handled? | ___ | ___ | ___ |
| D14 | Prepared environment | How is memory organized and selected for the current task? | ___ | ___ | ___ |
| D15 | Prepared environment | Which data boundaries and external dependencies limit the work? | ___ | ___ | ___ |
| D16 | Governance | Who assigns work, reviews it and bears responsibility for decisions? | ___ | ___ | ___ |
| D17 | Governance | Which actions are currently allowed, forbidden or unresolved, on what basis? | ___ | ___ | ___ |
| D18 | Governance | What standing autonomy, approval and escalation rules apply? | ___ | ___ | ___ |
| D19 | Governance | What happens on revocation, cancellation, stale authority or failure? | ___ | ___ | ___ |
| D20 | Governance | Which personal information and relationships may be used or disclosed? | ___ | ___ | ___ |
| D21 | Platform and evolution | Which runtime/model/configuration versions and supported capabilities are used? | ___ | ___ | ___ |
| D22 | Platform and evolution | Which resource, attention, time and operating limits apply? | ___ | ___ | ___ |
| D23 | Platform and evolution | What is actually preserved, external or missing from this description snapshot? | ___ | ___ | ___ |
| D24 | Platform and evolution | Which checks and manual decisions precede restoration and continuation? | ___ | ___ | ___ |
| D25 | Platform and evolution | How are changes versioned, reviewed, regression-checked and rolled back? | ___ | ___ | ___ |

These conditions ask what needs to be designed. Storage placement remains DNA, environment and concrete agent, with state/evidence separately recorded.

## Three pillars across five activity areas

| Area | Performance | Reliability | Alignment |
|---|---|---|---|
| Work and outcomes | Q11: What useful output, contribution and cost are expected? | Q12: How is work output checked and how are exceptions handled? | Q13: How does work follow priorities and commitments? |
| Interaction | Q21: What response or initiative helps the person take the next decision? | Q22: How is context retained and a handoff or misunderstanding reconciled? | Q23: Who is addressed, what tone is appropriate and what can be disclosed? |
| Knowledge and memory | Q31: Which knowledge must be available for the chosen work? | Q32: How are source revisions, dates, contradictions and staleness exposed? | Q33: What privacy, consent and data-boundary rules apply? |
| Authority and safety | Q41: Which access is necessary and actually available for the work? | Q42: How are consequences limited and stop/recovery behavior defined? | Q43: Which permission and approval constrains each action? |
| Oversight and development | Q51: How are effect and total human/agent costs measured? | Q52: What monitoring, regression checks and rollback follow a change? | Q53: Who approves changes and how are goals and permissions preserved? |

For every cell, record what is described and what evidence, if any, supports behavior. A complete answer may describe an untested capability; an actual scoped test does not fill unrelated questions. Reuse the same facts through references across views.

## Description maturity: proposal for discussion

Start with three levels rather than inventing distinctions for five unobserved stages. This is a proposed application model, not an adopted normative ladder or an agent/person quality score.

| Level | Description criterion |
|---|---|
| 1 — Orientation | Purpose, beneficiary, roles, current boundaries, sources and unknowns are explicit. |
| 2 — Working description | All applicable questions for the declared use have adequate answers, relationships and dependencies. Exceptions and blocking gaps are explicit; non-applicable items have reasons. |
| 3 — Maintained description | Level 2 plus responsible-party review, consistent source/version pins, ownership, revision triggers and a change/review cycle. |

Levels are scoped to a description version and use. They do not imply tested behavior, permission, runtime support or certification. Compare descriptions using the same selected checks; do not silently exempt missing answers to reach a higher level. Add levels only after recurring cases require a meaningful distinction.

## Include self-diagnosis in the profile collection

A completed self-diagnosis belongs to the profile collection alongside its description and composition. Record the assessment in the output index. It retains the exact description ID/version/digest, checklist version, evaluator/date, every check status, claim references and remaining question, with agreement and behavior evidence separately represented.

The assessment may be a separate versioned JSON artifact; its tables are views of the same records. The index pins the description and assessment, and the assessment pins the description. This avoids circular content hashes and allows additional dated assessments without rewriting the description being evaluated. Physical embedding into profile.json is not required by this application guide; no normative field is added.

The [Aster tables](aster-self-diagnosis.md) show the existing assessment already listed in that example’s index. The view does not change ratings or simulate responsible-party agreement or executed behavior.

## Review procedure

1. Pin the description and checklist versions, declare the intended use and selected applicable checks.
2. Follow the five-condition checklist and record answers or gaps without inventing context.
3. Inspect the 15 quality questions; reference the same description facts and separate any actual behavioral evidence.
4. Resolve lifecycle, authority and source conflicts; obtain responsible-party review for agreements.
5. Save the dated assessment as a linked part of the profile collection and list it in the output index. A later description version gets a new assessment; prior ratings remain traceable.

A private completed assessment stays in owner-controlled storage. It is not an export input by default. Use the [collection contract](self-description-contract.md) to link it to the profile and its composition. Partial/missing answers refer to follow-up items; agreement or behavior assertions require separately described evidence. Review a disclosure copy before publication.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
