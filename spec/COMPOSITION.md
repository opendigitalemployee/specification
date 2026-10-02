# Compose with existing formats

The package connects existing formats to a digital employee's **measurable business outcomes**, work, company context, and decision rights. JSON describes our objects, references, and package inventory. Embedded formats keep their own files and rules; the package does not turn them into a competing format.

The [standards map](../docs/OVERVIEW.md#existing-formats) connects these integration boundaries to the wider design. [Work, Workflow, Skill, and ToolDefinition](../docs/OVERVIEW.md#existing-formats) have different roles:

- **Work** defines a deliverable, its inputs, and acceptance criteria. Selecting that work is a hypothesis about how to contribute to an outcome.
- **Workflow** defines an execution process with steps and transitions. A process can use skills, tools, and human actions.
- **Skill** provides a reusable method for carrying out work.
- **ToolDefinition** describes an action interface, such as reading data or calling a system. Tool access and permission are separate from knowing a method.

A `SKILL.md` file previously used as work instructions can remain a `Work.instructions` resource. Its filename alone does not make the business object a Skill.

## Native Agent Skills resources

```text
dna/<dna-id>/<version>/<skill-id>.skill.json
native/skills/<skill-name>/
  SKILL.md
  references/
  scripts/
```

The optional resource subdirectories follow the embedded format. These placeholder paths explain the general layout; the synthetic example uses concrete names.

The JSON `Skill` object records identity, version, provenance, input/output contracts, checks, and a reference to the native `SKILL.md`. The skill's name, description, and instructions remain in its native file. Work references the skill; an `ActivationBinding` describes a specific activation point for the employee.

The manifest identifies the upstream Agent Skills specification and the revision read. The resource inventory lists the included skill files with checksums. Preserving a package preserves the YAML front matter, instructions, supporting resources, and executable files byte for byte. Reading or preserving these files does not execute them.

A runtime-specific implementation places the skill directory where that runtime expects it and connects the method to the employee's selected work and data. Outcome requirements, acceptance criteria, and authority remain separate package objects. Supporting a skill format does not by itself establish support for the whole employee design.

## Integration boundaries

| Component | Existing representation | What the package adds | Public draft 0.1 scope |
|---|---|---|---|
| Skill | Agent Skills `SKILL.md` and supporting directory | Object identity and version, input/output contracts, work references, activation, and provenance | Native resources in the synthetic example; structural checks during release verification |
| Data or tool schema | JSON Schema | References to a business concept, dataset, operation, or check | Schemas for package objects and manifests; automated schema/example checks |
| MCP connection | MCP protocol and runtime configuration | Tool contract, connection purpose, and permission/secret requirements | Integration boundary; no live MCP connector distributed |
| Agent discovery and communication | A2A / OASF and their own representations | Mapping of the employee's identity, capabilities, and interaction requirements | Research and mapping; no protocol compatibility certified |
| Agent Spec description | Its JSON/YAML | A projection of supported design requirements and an explicit support report | Integration candidate; no exporter distributed |
| Agent Companies package | Its Markdown and configuration sidecars | An organization and employee projection for Paperclip | Integration candidate; no exporter distributed |
| Workflow | An existing workflow definition in its native format | Business work references, requirements, and runtime bindings | Next-version proposal; not a normative kind in draft 0.1 |

The public release contains **documentation, schemas, and synthetic examples**. CLI tools and runtime adapters remain outside this release. Automated description checks do not certify execution, enforce permissions, or establish business outcomes.

## Workflow: next-version design

The proposed extension separates `Workflow` from `WorkflowBinding`. Native definitions are planned under `native/workflows/<name>/<version>/`. The common JSON description would reference the native graph rather than duplicate it as a second source of truth.

Candidate formats include Serverless Workflow / Open Workflow Specification, BPMN, Arazzo, and Agent Spec Flow. n8n, LangGraph, and Temporal are execution platforms with their own artifacts. No single mandatory workflow DSL has been selected. Workflow validation, execution, and conversion are not implemented by this public draft. See the [next-version design](../STATUS.md#next-version-proposals).

## Validation and extension

Keep separate checks for package schemas, exact typed references, the resource inventory, embedded formats, checksums, and runtime capabilities. A minimal Agent Skills structural check does not evaluate the quality of its instructions or guarantee identical behavior across models.

Preserve unknown optional extensions. An unknown required format or extension is a blocking support gap. Future validators and adapters should identify the format they support and report the scope actually checked.

Native metadata should not be copied into JSON as an independent source of truth. Package fields describe a different level: business-object identity and version, intended use, outcome contribution, authority, and company context. When representations disagree, surface the conflict before accepting a change.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
