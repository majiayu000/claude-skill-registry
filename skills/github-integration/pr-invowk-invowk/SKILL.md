---
name: pr
description: GitHub pull request workflow including tests, lints, license check, branch creation, conventional commits, and PR description. Use when creating commits, pushing branches, or opening pull requests.
disable-model-invocation: true
---

# PR Workflow

- Ensure all tests pass: `make test`
- Run lints and fix any errors: `make lint`
- Check license: `make license-check`
- If not in a feature/fix branch already, create one and switch to it
- Commit with conventional commit message
- Push branch
- Create PR with description referencing the issue
