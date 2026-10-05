# Decision-making in an imperfect world

**Experimental contract 0.1.0 · package format 0.2.0-draft.** This opt-in extension describes professional judgment. It adds no mandatory core object kind and prescribes no universal decision algorithm. The requirements below apply to documents claiming this extension, not to every ODE package.

Digital employees are designed to achieve **agreed, measurable outcomes in an imperfect world**. Knowledge is incomplete, consequences are uncertain, interests can conflict, resources are finite, conditions change, and execution can fail. A description makes these conditions and responsibilities explicit; an implementation must actually respond to them. Neither a valid description nor a completed task proves the agreed outcome.

## 1. Expertise includes choosing the next step

Domain expertise includes both **how to perform work** and **how to decide what to do next**. A good next step may produce a deliverable, obtain missing information, reconcile interests, obtain authorization, reduce exposure, wait for a meaningful event, or stop. Research can reduce an information gap without eliminating uncertainty about the outcome.

The outcome gives direction. A plan organizes work hypotheses over a horizon. A bounded step tests or advances one of them. The next review updates the plan and the forecast; it does not silently change the commitment. Several compatible experiments may run within a shared budget, with interference and dependencies considered. An authority or consent boundary is an admissibility condition, not a cost that can be outweighed by a benefit score.

## 2. Keep five levels distinct

| Level | What it supplies | What it does not establish |
|---|---|---|
| ODE specification | Shared description contracts, references and checks | The best next step for every domain |
| Domain method | Professional selection principles and applicability | Authority in a particular company |
| Method profile | Selected method version, goals, context, limits and human roles | A running implementation; this is not `manifest.profile` |
| Implementation | Forecasting, execution, enforcement and review mechanisms | Business effectiveness without evidence |
| Application history | Dated decisions, actions, outcomes and corrections | Universal validity from one successful case |

An implementation may use a different method in each domain. The product example links Next Move Theory as one optional source of professional method. ODE's operational supplement is separate and is not attributed to that author.

## 3. Three parts of the description

The [JSON Schema](extensions/decision-making.schema.json) defines one document with a method, a contextual profile and zero or more decision episodes. The extension ID is `org.opendigitalemployee.decision-making`; its version is `0.1.0`.

| Part | Required substance |
|---|---|
| Method logic | Required inputs, candidate generation, selection principles, forecast approach, resource limits, authority handling, stopping and review rules |
| Applicability | Domain and decision class, entry conditions, exclusions, horizon, evidence freshness and fallback when the method does not fit |
| Application history | Exact method/profile versions, context and source pins, conditions assessed, alternatives, grounds, forecast, responsible actor, authorization, actual execution and later review |

Record concise, verifiable grounds and evidence references. This contract does not request hidden reasoning traces. Record unknowns explicitly; do not convert them to zero, confidence or approval.

## 4. Conditions and their instances

The versioned [operating-conditions catalog](catalogs/operating-conditions.json) supplies six initial codes: `knowledge-limits`, `outcome-uncertainty`, `goal-interest-conflicts`, `resource-dependency-limits`, `changing-conditions`, and `capability-execution-limits`. They overlap and are not an exhaustive theory of the world. They are independent of the five design conditions, five activity areas and three quality pillars.

Each episode MUST assess every catalog group as present, absent or unknown. A present condition records its evidence, impact and next response. One present condition is selected as the leading focus of the bounded step; other conditions and constraints remain visible. Where no catalog condition is present, focus may be null. Local additions use `x-<namespace>:<code>`, a definition and the same assessment fields; a global catalog change requires a new catalog version.

The catalog is shared vocabulary. A missing-data instance belongs to a particular situation, not to the global catalog. Catalog examples suggest possible responses, not automatic prescriptions. Policy and human responsibility remain cross-cutting checks.

## 5. Responsibility and the human cooperation meta-skill

Both autonomous and paired employees need to recognize whether they may act, need a person, or must stop. A human request distinguishes **information, expert assessment, priorities, conflicting interests, resources and authorization**. It includes a focused question, options, recommendation, consequences, deadline and permitted behavior while waiting. Silence MUST NOT count as approval. Actions already within mandate do not require repetitive confirmation.

Use the existing `Skill` with `skillKind: meta-skill`, `InteractionContract`, `Policy` and the concrete `ClientAgent` relationship. The human role MUST be explicit even when a step is executed autonomously. A schema checks the record; the deployed runtime must enforce the boundary.

## 6. Forecast, commitment and review

Before a material step, record whether the agreed outcome remains feasible, given the current situation and remaining resources. A forecast states its target, horizon, assumptions, basis, uncertainty and next review trigger. It may be qualitative or explicitly unknown. A numerical probability additionally requires a named estimation method and calibration evidence; otherwise no probability should be emitted. A well-formed probability is still not proof of calibration.

Keep the forecast made before an action. Compare it with later observations, recording limitations, changed conditions and implications for the method. Append a new episode linked to its predecessor; do not rewrite the old forecast after seeing the result. Correcting a record preserves the previous version. If the forecast deteriorates, change the next step, seek a human decision or propose renegotiation. Only an authorized agreement changes the commitment itself.

## 7. Files and existing ODE objects

| File in the example | Content | Status / ODE connection |
|---|---|---|
| `manifest.json`, `objects/*.json`, `package.lock.json` | Employee, parties, environment, work, skill, policies and references | Current ODE 0.2 package contracts |
| `decision-making.json` | Versioned method, applicability, profile and two synthetic episodes | New experimental ODE extension |
| `objects/style.json` | DecisionStyle with namespaced extension pointing to the decision document | Current core object plus opt-in resource binding |
| `native/skills/human-decision-brief/SKILL.md` | Human cooperation instructions | Agent Skills native form; ODE defines participation and responsibilities |
| `inputs/*.json` | Dated synthetic context evidence | Package resources, not live connections |
| `README.md` | What is illustrated, how to inspect it and what remains untested | Explanatory example documentation |

Logic maps to `DecisionStyle`, `Work`, `Skill` and `Check`; context to `GoalMap`, `ClientAgent`, `WorldModel` and dated resources; responsibility to `Policy` and `InteractionContract`; observations may also connect to `Run`, `Decision`, `Evidence` and `ChangeSet`. This extension is a resource, not a substitute core kind. Its nested references are opaque to generic package validators; use the extension checker as well.

All referenced local artifacts MUST be package resources with integrity pins. Consumers that preserve the optional extension may round-trip it without understanding it. A consumer must understand and enforce it before claiming decision-making support. If required for a deployment, declare it in `requiredExtensions`; unsupported consumers then block admission under the core specification. Describing it alone never starts an execution.

## 8. Validation and limits

The [public checker](../.github/checks/decision_making.py) checks the schema, object kinds and versions, condition coverage, applicability, source hashes and freshness, candidate references, resource budgets, authority status, human requests, forecast chronology and decision/action separation. Contrastive tests are published beside it. Static checks cannot establish that an assertion is true, a method is professionally sound or a runtime enforces permissions.

Review separately: format and references; professional reasoning in contrasting situations; actual execution and authority; measured business effects. The [product employee example](../examples/product-employee/README.md) is authored synthetic evidence for the first layer only. Follow [DECISION-01](../docs/agents/procedures/decision-making.md) to describe your own approach.

This first contract keeps episodes for one selected method/profile version in a document. When either changes, create a new versioned document and preserve the earlier one. Cross-version history aggregation and multi-actor resource reservation are implementation responsibilities; this checker validates declared per-step budgets, not a live shared ledger.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
