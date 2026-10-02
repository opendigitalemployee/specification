# Open Digital Employee Specification

**Draft release 0.1.0-draft.4 · format 0.1.0-draft.** The package name and namespace remain provisional. The normative specification, schemas, examples and automated checks use Apache-2.0; explanatory documentation and glossary use CC BY 4.0. See [license scope](LICENSING.md).

Design a digital employee around a **measurable business outcome**. Agree on how its contribution will be assessed, treat work as a hypothesis for reaching that outcome, and describe the expertise, environment, permissions and checks it needs. Preserve that design independently of a runtime.

## Start here

1. [Understand the model and outcome-led method](docs/OVERVIEW.md).
2. [Read the package specification](spec/SPECIFICATION.md).
3. Inspect the synthetic [employee manifest](examples/clinic-employee/manifest.json) and follow its object paths.
4. Check [scope, maturity and next-version proposals](STATUS.md).

## Try the description

Open the [synthetic package manifest](examples/clinic-employee/manifest.json), then follow its object paths. Begin with `agents/demo/1.0.0/goals.json` and `client-brief.json`: the first names the desired outcome, the second describes a work hypothesis and acceptance criteria. Follow the selected DNA, company environment, native skills and permissions. Copy the example into a new working directory to explore it; illustrative clinic filenames are not requirements of the general format.

The [backup manifest](examples/clinic-backup/manifest.json) shows included files, context and restoration limits. No actions are launched by reading the example.

CLI tools and runtime adapters are **not included in this first release**. Schema and example checks are automated; employee execution, permissions and measurable business impact still require independent testing.

## What is included

- A versioned specification, JSON Schema, reference rules and type catalog.
- An EN/RU [glossary](spec/glossary.json); [composition notes](spec/COMPOSITION.md) currently remain in Russian.
- One synthetic employee scenario and its file backup, with native skill resources.
- [Change history](CHANGELOG.md), [contribution guidance](CONTRIBUTING.md), and a generated [release manifest](release-manifest.json) recording sources, hashes and checks.

The website is [opendigitalemployee.org](https://opendigitalemployee.org). Definitions originate in the standard source; website copy and visual explanations are separate views. This directory is generated: propose changes through review and incorporate them into the source before re-export.

## Maintainers and licensing

Copyright 2026 Taras Pustovoy and contributors. See [contributors](CONTRIBUTORS.md) and [license scope](LICENSING.md). This is the **Open Digital Employee Specification**, an experimental draft open for review and integration work.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
