---
name: rule-pull-request
description: 'Rule mapping for pull-request'
---

# Rule pull-request

Apply this rule whenever work touches:
- `*`

Pull requests are created exclusively through the `gh` CLI to ensure consistent metadata.

### Creating a PR

```bash
gh pr create \
  -a @me \
  -r @carrot-foundation/developers \
  --label feature \
  -R carrot-foundation/methodology-rules \
  -t "feat(rule): add vehicle weight validation"
```

Adjust `--label` to match the change type:

| Label         | When to use                       |
|---------------|-----------------------------------|
| `feature`     | New functionality                 |
| `bug`         | Bug fix                           |
| `chore`       | Tooling, CI, dependencies         |
| `docs`        | Documentation changes             |
| `refactoring` | Code restructuring                |

### PR summary

The summary should be brief and action-oriented:

- Start with a verb: "Add", "Fix", "Refactor", "Remove"
- 1-3 sentences covering the what and why
- Link related issues if applicable

### Pre-submission checklist

Before opening the PR, verify locally:

```bash
pnpm lint:affected
pnpm ts:affected
pnpm test:affected
```

These same checks run in CI, but catching failures early saves review cycles.
