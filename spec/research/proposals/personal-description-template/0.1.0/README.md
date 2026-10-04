# Start a private self-description collection

Experimental template 0.1.0. Copy this directory into owner-controlled storage. Read the [procedure](../../personal-starter-slice.md) and [collection contract](../../../../../docs/agents/self-description-contract.md) in the release you use. This is a valid draft; all answers start as missing.

1. Choose description ID, version, intended use and date. Fill `profile.json` from authorized sources, with exact source versions and unknowns.
2. Fill `components.json`: native entry route, selected composition, methods, dependency boundaries and follow-ups. Files that stay elsewhere use external references. Do not copy a whole environment to finish this step.
3. Fill `assessment.json`: evaluator/date, each question's status, claim references, reasons and next steps. Pin the completed profile digest. The checklist path is relative to the standard checkout supplied to the checker.
4. Update `index.json`: pin the three output files and each deliberately included resource. Optional prose can be indexed as walkthroughs. The index never hashes itself. Calculate digests from final bytes; later edits require refreshed pins.
5. When author-completion criteria are met, set profile/index status to `agent_self_report` and assessment status to `author_assessment`. Run the structural check. Seek the person's review for agreements; keep partial/missing answers and their routes.

See [Aster](../../../../../examples/personal-description/0.2.0/README.md). Collection, format and normative ODE versions are distinct. Keep the originating release in maintenance notes. This README is usage guidance outside the template's indexed output. Copying it does not make it part of the agent's identity or backup.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
