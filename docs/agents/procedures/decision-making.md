# DECISION-01 — Describe a decision-making approach

**Version 0.1.0 · experimental · description procedure.**

Use this route when an employee needs a reviewable way to choose its next step under incomplete knowledge, uncertainty, competing interests or limited resources. It does not require SELF-01 first. Use AFFILIATION-01 when packaging the result as a normative ODE package.

## Inputs

An agreed or explicitly proposed outcome, selected domain method, authorized context sources, resource limits and responsible human roles. Missing information is a finding; do not invent approval, performance data or a forecast.

## Steps

1. **Define the outcome and responsibility.** Identify the measure, horizon, baseline, target, limits and who can change the agreement. Mark unknowns and assign their resolution.
2. **Describe the professional method.** Capture both execution expertise and next-step judgment. State inputs, alternatives, selection principles, forecast method and stopping/review rules. Pin its version.
3. **State applicability.** Name the domain, decision classes, entry conditions, exclusions, freshness window and fallback. Include one case where this method should not be used.
4. **Create a contextual profile.** Bind the method to the employee, goal, environment, work, policies, human interaction contract and meta-skill. Separate method selection from authorization.
5. **Describe contrasting episodes.** Assess the operating conditions. Show an authorized step and a case requiring a person or a stop. Preserve forecast, selection, authorization, action and observation separately. Mark authored scenarios as synthetic.
6. **Check and review.** Validate against the schema and public checker; ask the responsible domain expert to review the method and applicability. Record that review as pending when it has not occurred. A runtime trial remains a separate activity.

## Output and completion

A [decision description](../../../spec/DECISION-MAKING.md) with a versioned method, applicability, profile and at least two contrasting episodes for this procedure. The general schema allows an empty history for an unused method. A completed DECISION-01 description has explicit unknowns and next actions; structural checking passes. Human agreement, external expert review, independent repetition and runtime performance retain their own statuses.

Use the [synthetic product example](../../../examples/product-employee/README.md) as a shape, not as facts about your agent. Check a local package from the specification repository:

```sh
python -B .github/checks/decision_making.py --standard-root . --package examples/product-employee
```

The checker is read-only. It does not call a model, run a skill, grant access or execute a proposed action. Failures remain visible; a partial collection may be saved but must not be presented as a completed checked description.

## Missing information and escalation

State which input is missing, why it matters, who can supply or authorize it, and what is allowed meanwhile. A prepared human request includes options, recommendation and consequences. No response means no additional permission. Do not publish private context while asking for review.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
