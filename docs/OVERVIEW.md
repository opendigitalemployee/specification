# An outcome-led design for digital employees

A digital employee is a repeatable contribution to a business, supported by expertise, context, tools, decision rights and checks. An agent completing a task is evidence of execution; deciding whether it moves the needle requires a measurable business outcome and a way to assess its contribution.

## Design backward from the outcome

1. Name the business outcome: who owns it, which metric matters, its baseline, target and time horizon. Distinguish the desired change from the artifact the employee produces.
2. Propose work that could contribute. State the causal assumption, expected output, acceptance criteria, resources and cost. Work is a hypothesis, not proof of impact.
3. Identify the expertise and prepare the working environment: trusted data, systems, people, rules and dependencies.
4. Assign permissions, escalation and checks for performance, reliability and alignment. Select a runtime and record gaps.
5. Test the work, measure its contribution, learn from evidence and revise the design for the next cycle.

This is an informative design method. It does not add required schema fields or claim that a trial proves a business outcome. Current GoalMap and Work contracts capture a typed minimum; domain-specific measurement detail needs its own agreed content.

## People, company, employee, environment and runtime

A company sets goals and operating rules. A person participates as an owner, colleague, client or approver. Reusable domain expertise (DNA) supplies methods and professional quality standards. A specific employee selects that expertise for a company and receives its goals, work, interactions and authority. A prepared environment supplies the business model, knowledge, sources, systems and connections. A runtime executes supported parts of the description. Personal storage is a separate boundary; a link to a person does not grant access. Person contracts and personal backup are next-version proposals.

## Five conditions, three layers, three quality pillars

Five business conditions guide the design: **purpose and company alignment; governance; a prepared working environment; domain expertise; and an execution platform capable of delivering results**. They describe what has to come together.

Three design layers explain where descriptions belong: **DNA**, **working environment**, and **a specific employee**. Their composition forms the package. Definitions are distinct from observations and captured state.

Three pillars assess quality: **performance, reliability and alignment**. They are applied across work and outcomes, interaction, knowledge and memory, authority and safety, and oversight and development. These activity areas are a separate dimension from the five business conditions. A stored description or successful format validation does not itself demonstrate any pillar.

## Four uses of one package

- **Describe and improve:** version work, methods, context, permissions and acceptance criteria together.
- **Back up and restore:** preserve selected descriptions and actual included context; declare what remains external. File restoration does not recover external databases or executing jobs.
- **Migrate between runtimes:** retain requirements and native resources; inspect adapter support and retest missing mechanisms. Portability of a description does not guarantee equivalent behavior.
- **Build together:** let business owners, domain experts and technology teams agree on outcomes, requirements, implementation and acceptance.

## Existing formats

| Component | Role and current boundary |
|---|---|
| Agent Skills | Native `SKILL.md` directories retain their bytes. Our Skill object adds identity, version, business relationships and activation. A skill is not a tool or a Work contract. |
| JSON Schema | Data and object contracts. The reference tools validate included schemas and resources; integrity is a separate check. |
| MCP | Tool interfaces and runtime connections. The package describes requirements and access; it does not implement an MCP connection by itself. |
| A2A / OASF | Agent exchange and capability descriptions. These are possible integration boundaries, not implemented full exports. |
| Workflow formats | Execution graphs or native definitions may remain authoritative in their own format. Workflow integration is a next-version proposal; no common DSL or runtime conversion is implemented. |

See the [normative draft](../spec/SPECIFICATION.md) and [current status](../STATUS.md) for exact requirements and limits. The standard connects these components without replacing their native formats.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
