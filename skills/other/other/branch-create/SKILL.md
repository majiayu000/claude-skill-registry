---
name: branch-create
description: Create a feature branch from naming convention and issue context.
---

# Branch Create

The Orchestrator drives this workflow. Create a feature branch following the workspace naming convention, from the correct base branch.

**Prerequisites:** Issue number and type known, no uncommitted changes on current branch.

---

## Branch Naming Convention

Read `workspace.config.yaml` for:

- `project.base-branch` — the branch to create from (default: `main`)
- `project.branch-pattern` — the naming pattern

### Pattern

`<type>/<issue-number>-<kebab-description>`

### Types

| Type       | When to Use                            |
| ---------- | -------------------------------------- |
| `feat`     | New feature or capability              |
| `fix`      | Bug fix                                |
| `docs`     | Documentation only                     |
| `chore`    | Maintenance, dependencies, tooling     |
| `refactor` | Code restructuring, no behavior change |
| `test`     | Test additions or corrections          |
| `perf`     | Performance improvement                |

### Examples

- `feat/42-add-redis-cache`
- `fix/99-null-pointer-on-login`
- `docs/55-api-reference-update`
- `chore/128-phase7-checkpoint`

---

## Steps

1. Determine the branch type from the issue labels or context:
   - `type:feature` → `feat`
   - `type:bug` → `fix`
   - `type:docs` → `docs`
   - `type:chore` → `chore`
   - `type:spike` → `chore`
   - If no label, infer from the issue title or ask
2. Compose the branch name: `<type>/<issue-number>-<kebab-description>`
3. Present the proposed branch name for approval

### ⛔ CHECKPOINT

**STOP.** Await approval of the branch name.

4. Checkout the base branch and pull latest:
   ```bash
   git checkout <base-branch> && git pull origin <base-branch>
   ```
5. Create the feature branch:
   ```bash
   git checkout -b <branch-name>
   ```
6. Verify the branch was created:
   ```bash
   git branch --show-current
   ```

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>
- **Branch:** `<branch-name>`

## Branch Created

- **From:** `<base-branch>`
- **Name:** `<branch-name>`

## Next Step

Branch created. Ready to begin implementation.

**Approval Required:** No
```

---

## Error Handling

| Error                     | Recovery                                              |
| ------------------------- | ----------------------------------------------------- |
| Branch already exists     | Report it; ask whether to checkout existing or rename |
| Uncommitted changes       | Report them; ask whether to stash or commit first     |
| Base branch not found     | Check workspace.config.yaml; ask for correct name     |
| Issue number unknown      | Ask for the issue number                              |
| Type cannot be determined | List the type options and ask user to pick            |
