# Submit feedback as an agent

Read [CONTRIBUTING.md](CONTRIBUTING.md), [STATUS.md](STATUS.md) and the relevant section of [spec/SPECIFICATION.md](spec/SPECIFICATION.md). Review the current public draft for a concrete problem or improvement.

Search existing issues first. Submit one independently decidable point per issue, in English or Russian. Include:

- draft version or commit and the affected section, object kind or glossary ID;
- the problem or need and a concrete example;
- a suggested change, if known, and compatibility implications;
- evidence or a way to verify the improvement;
- agent name and the responsible submitting account or person.

A partial finding is useful when its uncertainty is clear. File checks, runtime trials and observed business impact are different evidence. Informative next-version proposals are distinct from the current package format.

Use an authorized GitHub account, CLI or connector. Open an issue through the forms at [the submission page](https://github.com/opendigitalemployee/specification/issues/new/choose). For API or CLI submissions, put the fields above in the body; the web form is not required.

A public repository does not grant write permission to a GitHub App token. If a connector returns `403 Resource not accessible by integration`, check that its app is installed for `opendigitalemployee`, includes `specification`, and has `Issues: write`. An installation only on a personal account does not cover this organization. Use the GitHub website while signed in or a separately authorized `gh` session to submit without that connector; confirm `gh auth status` before using the CLI. Do not retry the same denied connector request or request the maintainer's credentials. See [GitHub's app access rules](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-with-a-github-app-on-behalf-of-a-user).

```sh
gh issue list --repo opendigitalemployee/specification --state all --search 'your topic'
gh issue create --repo opendigitalemployee/specification \
  --title '[Proposal] A precise improvement' --body-file proposal.md
```

You may propose a patch through a pull request from your fork. Leave release metadata and source reconciliation to the maintainer. Submit only material you are authorized to publish under [the applicable license](LICENSING.md). The maintainer records the adoption decision; submitting feedback does not authorize publishing a new standard version.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
