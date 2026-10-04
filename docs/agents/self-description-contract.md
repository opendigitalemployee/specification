# Experimental self-description collection

**Contract 0.1.0 · 4 October 2026.** This application contract connects a reflective profile, composition and self-diagnosis. A collection's `version` is independent of its `formatVersion`. Changing published collection bytes requires a new collection version.

## Files and references

| Role | Content | Schema |
|---|---|---|
| `reflective_profile` | Claims, basis, exact source references, authority, continuity and unknowns | [Profile 0.1.0](../../spec/research/proposals/personal-self-description.schema.json) |
| `structured_composition` | Native entry route, dependencies, methods, existing Work references and follow-ups | [Composition 0.1.0](../../spec/research/proposals/personal-description-components.schema.json) |
| `assessment` | Dated evaluation of the exact profile; 25 design and 15 quality records | [Assessment 0.1.0](../../spec/research/proposals/personal-self-diagnosis.schema.json) |
| Index | Exact paths and SHA-256 digests, description identity and completion state | [Index 0.1.0](../../spec/research/proposals/personal-description-index.schema.json) |

The [blank collection](../../spec/research/proposals/personal-description-template/0.1.0/README.md) supplies all four files. Roles determine meaning; filenames are flexible. Exactly one profile, composition and current assessment is selected per index; earlier assessments belong to earlier indices or additional `audit` artifacts. Walkthroughs and audits are optional.

The assessment pins the profile; the index pins both. The profile does not hash the assessment, and the index does not hash itself. Human-readable tables are views of the assessment records.

Included paths are relative to the index directory: files only, no traversal, absolute paths or symlinks. The checker reads only indexed files, never executes native instructions and never follows external locators. Non-indexed files are outside this declared inventory; the check is not a completeness certificate for the surrounding directory.

`assessment.checklist.path` resolves within the explicitly supplied standard checkout. The checker also reads the release's schemas and [Check definitions](../../spec/research/proposals/personal-self-description.checks.json). These shared validation inputs are not the agent's identity/environment. A source's optional `location` identifies an indexed file and its `version` is that file's SHA-256. External sources can retain an ID/version without a local `location`.

## Composition boundary

Each dependency has an ID, purpose, locator, revision and relationship: `agent_component`, `shared_basis`, `environment_dependency` or `evidence`. Relationship and inclusion are independent. These enums belong to this experiment, not the normative kind catalog.

`included_file` resolves to `index.resources` with the same ID, path, digest and relationship. `external_reference` records a URI, access status and boundary; the checker does not read it. Private external files may use `file:` URIs. Their containing directories are never selected. Unknown revision is `status: unknown, value: null`; a digest and a human version are separate facts.

`captureSelection: not_selected` and the description-only preservation block mark the output boundary. Backup plans, traversal depth, inclusion cuts, archives and restoration results belong to separate artifacts. A description does not select every available skill or repository.

A derived explanatory resource has its own ID/digest, plus `derivation.sourceDependencyRefs`, coverage and limitations. It cannot be substituted for its source under the same identity/digest. This describes an already authored resource; it does not generate backup summaries.

Method availability, selection and application status are independent. `capabilityEvidence` contains IDs of described evidence dependencies. An unresolved string or installed file is not evidence. Linked evidence requires substantive review. Empty `formalWorks` with `formalWorkStatus: not_defined` is valid. Defined works use exact ODE references; this checker does not resolve a separate Work package.

## Assessment and completion

Use the [checklist meanings](self-diagnosis.md). Each record has claim references, a reason and independent agreement/behavior fields. Partial/missing items require `followUpRefs` into composition follow-ups: source analysis, owner conversation or standard design. Non-applicable items need a scope-specific reason. Filled/partial answers require claim references; tags are not answers.

`agreementRefs` and `behaviorEvidenceRefs` resolve to evidence dependencies and are required when agreement or observed/tested behavior is asserted. The checker establishes reference consistency, not their truth. `descriptionMaturity: not_assigned` leaves the guide's maturity proposal open.

A draft can have missing identity/date. For author completion, use `agent_self_report` in profile/index, supply identity/date, assess every item and route gaps. `owner_reviewed` requires actual responsible-party review; the checker cannot authenticate it. Passing does not require every answer to be filled.

## Reproduce structural checks

Use Python 3.9+ and `jsonschema>=4.25,<5`, as in this repository's automated checks. From the public specification checkout:

```sh
python -B .github/checks/self_description.py --standard-root . --index examples/personal-description/0.2.0/index.json
python -B .github/checks/self_description.py --standard-root . --index /path/to/private/description/index.json
```

Add `--allow-draft` for the template; it reports `valid_draft`. The checker validates shapes, indexed bytes, sources, dependency boundaries, assessment pins, coverage and counters. It performs no model execution, network access, backup or restoration. CI includes negative cases and a second independently constructed minimal fixture; that fixture is an author test, not independent agent repetition.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
