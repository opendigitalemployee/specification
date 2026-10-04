# Propose a change

People and agents are welcome. English and Russian submissions are accepted. A GitHub account is enough to open an issue in this public repository; no invitation or write access is needed.

## Start here

- [Propose a change](https://github.com/opendigitalemployee/specification/issues/new?template=01-proposal.yml).
- [Report a problem](https://github.com/opendigitalemployee/specification/issues/new?template=02-problem.yml).
- [Ask a question or share a use case](https://github.com/opendigitalemployee/specification/issues/new).

Search existing issues first. Submit one independently decidable point per issue. Name the draft version or commit and the affected section, object kind, glossary ID or file. Explain the problem with a concrete example; suggest a change or verification case if you have one. A complete solution is not required.

Start with the [specification](spec/SPECIFICATION.md) and [scope](STATUS.md). Keep outcome, output, Work, Workflow, Skill and ToolDefinition distinct. Use stable glossary IDs; English is the reference language and translations are reviewed separately. Native formats retain their own rules. Include a primary source and observed revision when proposing an integration. Separate observed evidence from assumptions and file checks from runtime trials.

## Agents

Use a GitHub account or connector you are authorized to operate. Include the agent name and responsible submitting account or person. Use the same issue forms as people. [AGENTS.md](AGENTS.md) has a submission brief and a CLI example.

GitHub Apps have separate installation and permission limits. A connector needs access to this organization's repository and `Issues: write`; public visibility alone is insufficient. If it returns `403 Resource not accessible by integration`, use the signed-in GitHub website or an independently authorized CLI session, or have the organization owner configure the app. No repository invitation is needed for a person submitting through their GitHub account.

## Review and patches

New reports receive `needs-triage`. The initial maintainer, [Taras Pustovoy](https://github.com/tvpustovoy), reviews them, asks for missing information and records the decision in the issue. Posting a proposal does not change the standard.

You may also fork the repository and submit a focused pull request to `main`, linked to its issue. This repository is exported from a curated source: the maintainer incorporates an accepted patch there and regenerates the public candidate and `release-manifest.json` before publication. Contributors do not need the private source or to regenerate release hashes. Current CI includes exported-hash checks, so a proposal patch may require maintainer re-export before those checks pass. Changes to normative semantics require a versioned specification; released objects require their own versions. An accepted proposal stays open until the implemented change is published and linked back to it.

Check [the license map](LICENSING.md). Contribute material you are authorized to publish under the license applicable to the affected file; identify third-party sources or licensing constraints. Do not submit private company or personal data, credentials or internal conversations.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
