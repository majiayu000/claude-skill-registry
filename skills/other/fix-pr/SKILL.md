---
name: fix-pr
description: Fix a failing PR by analyzing CI logs and fixing errors. Autonomous workflow that identifies failures, rebases, fixes issues, and pushes.
argument-hint: <PR number>
---

# Fix Failing PR

Autonomous workflow to fix CI failures for a PR. Delegates failure identification to subagent, then applies fixes.

## Usage

```
/fix-pr 19882
```

## Workflow

### Phase 0: Validate PR

Before doing anything, verify the PR is valid:

```bash
gh pr view <PR> --repo AztecProtocol/aztec-packages --json state,baseRefName,headRefName
```

**Abort if:**
- `state` is not `OPEN` → "PR #\<N> is \<state>, nothing to fix."

### Phase 1: Identify Failures

Spawn the `identify-ci-failures` subagent:

```
Use Task tool with subagent_type: "identify-ci-failures"
Prompt: "Identify CI failures for PR <number>"
```

This returns:
- Failure type (build/format/lint/unit-test/e2e-test)
- Test names, hashes, error snippets
- Local file paths for logs

**If the subagent cannot find CI logs**, ask the user for:
- The CI log URL directly
- Or the CI password if authentication is needed

### Phase 2: Checkout and Rebase

```bash
gh pr checkout <PR>
git fetch origin <base-branch>
git rebase origin/<base-branch>
```

If there are conflicts:
1. Resolve the conflicts
2. `git add <resolved-files>`
3. `git rebase --continue`

**Important**: Always REBASE, never merge.

### Phase 3: Bootstrap (if needed)

Check if changes exist outside `yarn-project`:
```bash
git diff origin/<base-branch>...HEAD --name-only | grep -v '^yarn-project/'
```

If yes, run bootstrap:
```bash
(cd $(git rev-parse --show-toplevel) && BOOTSTRAP_TO=yarn-project ./bootstrap.sh)
```

### Phase 4: Fix Based on Failure Type

Run from `yarn-project` directory.

| Failure Type | Fix Action |
|-------------|------------|
| **FORMAT** | `yarn format` |
| **LINT** | `yarn lint` |
| **BUILD** | `yarn build`, fix TypeScript errors, repeat |
| **UNIT TEST** | `yarn workspace @aztec/<package> test <file>`, fix, repeat |
| **E2E TEST** | For simple failures, fix. For complex failures, suggest `/debug-e2e` |

### Phase 5: Quality Checklist

Before committing, run from `yarn-project`:

```bash
yarn build
yarn format
yarn lint
```

Run tests for modified files:
```bash
yarn workspace @aztec/<package> test <file>.test.ts
```

### Phase 6: Commit and Push

If the PR targets `next`, amend to keep it as a single commit:

```bash
git add .
git commit --amend --no-edit
git push --force-with-lease
```

Otherwise, create a normal commit:

```bash
git add .
git commit -m "fix: <description of fix>"
git push
```

## Key Points

- **Validate first**: Only fix PRs that are open
- **Delegate identification**: Use `identify-ci-failures` subagent, don't analyze logs directly
- **Rebase, don't merge**: Always rebase on the base branch
- **Amend only for PRs targeting `next`**: Other PRs use normal commits
- **Bootstrap when needed**: Only if changes outside yarn-project
- **Escalate e2e failures**: Complex e2e issues need `/debug-e2e`

## Reference

- See `CLAUDE.md` for project conventions
- See `/debug-e2e` skill for complex e2e failure analysis
