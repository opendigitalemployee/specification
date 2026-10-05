# Product employee — choosing a bounded next step

**Authored synthetic example.** No real customer data, human approval, agent execution or measured business improvement is reported. The complete ODE 0.2 package combines existing kinds with an opt-in decision resource.

A fictional product team proposes improving seven-day activation from an illustrative 40% to 50%, without increasing support hours per activated team. The baseline is not yet confirmed. Its digital employee must select a useful next step before anyone can responsibly promise that improvement.

```text
Proposed outcome + context + resource limits
                 ↓
Method + applicability + responsibility
                 ↓
Review local evidence ── or ── ask to contact customers
                 ↓                    ↓
Within mandate: review       Product owner must authorize
                 ↓                    ↓
Synthetic observation       Pending: no contact made
                 └──────→ revise forecast and next step
```

## Inspect the files

- [manifest.json](manifest.json): all selected objects and resources.
- [objects/goal.json](objects/goal.json): outcome, baseline, measure and guardrail.
- [objects/work.json](objects/work.json): work as a contribution hypothesis and result contract.
- [objects/style.json](objects/style.json): professional judgment and extension binding.
- [decision-making.json](decision-making.json): method logic, applicability, contextual profile and two contrasting episodes.
- [objects/human-skill.json](objects/human-skill.json) and [native skill](native/skills/human-decision-brief/SKILL.md): human cooperation meta-skill.
- [objects/interaction.json](objects/interaction.json), [read policy](objects/read-policy.json) and [contact policy](objects/contact-policy.json): responsibilities and boundaries.
- [inputs/funnel.json](inputs/funnel.json) and [inputs/review.json](inputs/review.json): dated, hash-pinned fictional evidence.

The first episode depicts a local evidence review within mandate. The second proposes customer interviews and waits for the product owner's authorization. Both preserve the target, forecast, alternatives and resource budget. Feasibility is explicitly unknown; there is no invented probability. Running both proposed experiments at once would exceed the four-hour step budget.

The global [conditions catalog](../../spec/catalogs/operating-conditions.json) defines shared codes. The episode keeps the context-specific assessments, including unknown conditions. The six codes are not the five design conditions or the three quality pillars.

## Method source and ODE supplement

[Next Move Theory by Ivan Zamesin](https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills/tree/f8e87d10255b48d381ebc7fa65172960eb6d483f/Next-Move-Theory-Canon) is one optional source for product-domain method. This example links a reviewed revision and independently illustrates an ODE description. It does not distribute that canon or its skills, assert endorsement, or claim a complete NMT implementation. External material retains its own licensing terms.

The explicit applicability contract, permission boundary, forecast history, resource accounting and human handoff are an **ODE operational supplement**. Other professional methods may fill the same description contract.

## Check and interpret

From the specification repository, with `jsonschema` installed:

```sh
python -B .github/checks/decision_making.py --standard-root . --package examples/product-employee
python -B -m unittest discover -s .github/checks -p test_decision_making.py
```

Checks cover structure and declared relationships. Professional adequacy, independent repetition, actual permission enforcement and business effects remain untested. The [DECISION-01 procedure](../../docs/agents/procedures/decision-making.md) describes how to create a reviewed description for a different employee.
