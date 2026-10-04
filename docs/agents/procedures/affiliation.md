# AFFILIATION-01: describe whom an agent serves

**Procedure · 0.1.0 · specification 0.2.0-draft · 4 October 2026.** Use this when creating a normative ClientAgent package. The [self-description collection](self-description.md) may supply reviewed facts but is not automatically converted to a package.

## Prerequisites and result

Identify the served party and working environment, or their explicit external dependencies. If either is unknown, retain the gap in the description and do not invent a person or organization to pass validation. Result: exact Party/Organization, ClientAgent, Environment and applicable ToolBinding/WorldModel relationships, with a valid inventory and lock. This describes an affiliation; it does not establish legal ownership or authorize execution.

## Steps

1. **Identify whom the agent serves.** Create or pin a Party with category `person`, `family`, `team`, `organization` or `other`. For `other`, supply `categoryLabel`. ID and title can be pseudonymous; neither a legal identity nor an organization ID is required. A role such as assistant, manager or specialist belongs in Role. A family/team party denotes that collective without requiring its member list.
2. **Separate the relationships.** Set ClientAgent.servesRef. Record authorityRef only when the responsible assigning/reviewing party is known. Set Environment.controllerRef, then the same controller on its ToolBinding objects. A WorldModel records its own controllerRef. Do not assume the served person controls every environment or can authorize another party's resources.
3. **State authority and access separately.** Use Policy for actions, scope, approval, enforcement and revocation. A personal agent using a team's environment needs policyRefs describing that boundary. A structurally valid approval-required policy may still be awaiting approval. External dependencies need resolution and checks before admission.
4. **Compose the package.** Pin DNA and environment, selected roles/methods and any defined work. An empty workRefs list is permitted when no formal Work has been established. Inventory all included object/resource files and preserve exact versions. Do not bundle surrounding repositories or credentials merely because they are dependencies.
5. **Check it.** Use the current schemas and the read-only package checker below. Review the actual meaning, authority and external dependencies separately. Missing responsible-party agreement remains a gap after structural validation.

```sh
python -B .github/checks/package_contract.py examples/personal-agent --standard-root .
```

The checker requires Python and jsonschema (the same dependency used by repository CI). For your own package, replace the example path. It validates schemas, included typed references, affiliation relationships, inventory and hashes. It does not validate every native format, fetch dependencies, construct a backup, execute tools or certify readiness.

## Party category directory

The versioned [party category catalog](../../../spec/schema/party-categories.json) is distributed with the normative schemas. Its codes constrain Party.spec.category. It is generated together with the schema from one source; a release check rejects divergence. This small core vocabulary describes the party served or responsible for a context, not an application profile or agent skill.

| Code | Party described | Example |
|---|---|---|
| `person` | An individual | My personal agent serves me |
| `family` | A family or household as a collective | Our family agent serves our household |
| `team` | A collaborating group, including a project team | Our project agent serves the project team |
| `organization` | A company, institution or other organization | The company agent serves the company |
| `other` | A separately named party outside these categories | Supply categoryLabel and explain its boundary |

Choose the category relevant to the identified party in this context. The vocabulary is not a list of mutually exclusive real-world identities: family members may also form a project team, but those are different described contexts. Use separate identities when the boundaries differ, with explicit provenance rather than automatic equivalence. Serving a party does not prove benefit to it; outcomes and evidence address that question. Benefiting other stakeholders does not silently change servesRef.

Adding or redefining a global category changes the normative contract and requires a new specification version plus schema/catalog updates and migration notes. Local experiments use `other` with categoryLabel; they do not silently add global codes. Particular people, families, teams and companies are Party instances stored in the user's own package or private library. The public catalog contains category definitions and fictional examples, not a register of clients. Extended industry/role catalogs and best-practice libraries can have their own identities and release cycles; this small foundational catalog ships with the core.

## Minimal personal example

The [package manifest](../../../examples/personal-agent/manifest.json) pins eight synthetic objects. Its [Party](../../../examples/personal-agent/objects/person.json) is a person; its [agent](../../../examples/personal-agent/objects/agent.json), [environment](../../../examples/personal-agent/objects/environment.json), [binding](../../../examples/personal-agent/objects/binding.json) and [world model](../../../examples/personal-agent/objects/world.json) contain no organizationRef. It has no collected personal records, no invented formal work and no observed runtime verification.

## Three worked cases

These are fictional teaching packages. Replace their identities only in your own new versions. The same relationships work in all three cases; the category belongs to the party served, not to the agent role.

| Case | Party served (`servesRef`) | Assigning/reviewing party (`authorityRef`) | Environment / binding / world-model controller | Checked package |
|---|---|---|---|---|
| My personal agent | Party, `person` | The same person | The same person | [personal-agent](../../../examples/personal-agent/manifest.json) |
| Our family agent or project agent | Party, `family` for a family; Party, `team` for a project team | A separately identified responsible person | The family or project team | [family-agent](../../../examples/family-agent/manifest.json), [project-agent](../../../examples/project-agent/manifest.json) |
| A company agent | Party, `organization` | A separately identified responsible person | The company | [company-agent](../../../examples/company-agent/manifest.json) |

For example, the personal agent selects its person without an organization ID:

```json
{
  "servesRef": {"objectId": "urn:ode:example:personal:person", "version": "1.0.0"},
  "authorityRef": {"objectId": "urn:ode:example:personal:person", "version": "1.0.0"}
}
```

The family agent serves the collective and identifies a distinct reviewer:

```json
{
  "servesRef": {"objectId": "urn:ode:example:family-agent:party", "version": "1.0.0"},
  "authorityRef": {"objectId": "urn:ode:example:family-agent:reviewer", "version": "1.0.0"}
}
```

The company agent uses the same shape:

```json
{
  "servesRef": {"objectId": "urn:ode:example:company-agent:party", "version": "1.0.0"},
  "authorityRef": {"objectId": "urn:ode:example:company-agent:reviewer", "version": "1.0.0"}
}
```

These snippets show only the relationship fields. Each linked package supplies the complete graph: ClientAgent → served/authority parties and Environment → controller and WorldModel; ClientAgent → ToolBinding → the same Environment/controller plus ToolDefinition and Policy. All exact references resolve inside each example, and all included bytes are pinned in its lock. The three collective examples use a Party rather than requiring a second Organization object; an Organization target is also supported and regression-tested.

For a personal agent using a team's environment, keep servesRef on the person and controllerRef on the team. The binding follows the team's controller. Add policyRefs for access across that boundary; structural validation accepts this arrangement only with that declared policy and does not assert that approval has already been given. A project itself is a work context, not automatically a person or legal entity: use `team` for its responsible collective, or `other` with a categoryLabel for a separately identified project party.

Run the same check on each of the four linked package directories. CI performs these checks and positive/negative reference tests. These are schema/graph/integrity exercises, not executed family, project or company work.

The [specification](../../../spec/SPECIFICATION.md#11-affiliation-authority-and-environment-control) defines the normative relationships and [migration rules](../../../spec/SPECIFICATION.md#91-compatibility-with-010-draft). Existing 0.1 packages keep their old version and schema. Migration requires reviewed new object versions and updated references; changing the version label alone is insufficient.

Return to the [procedure index](README.md).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
