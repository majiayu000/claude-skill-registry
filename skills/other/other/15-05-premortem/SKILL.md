---
name: 15-05-premortem
description: Use before starting risky work — rebases, large refactors, multi-file migrations, or deploys — to identify failure modes and mitigations in advance.
---

# 15.05 Pre-Mortem

Before starting risky work, assume it has already failed. Work backwards to find why. This is the inverse of a post-mortem (20.05) — you write it *before* the work, not after.

Pre-mortems beat risk assessment because they assume failure is certain, bypassing optimism bias.

## When to Run

- Before a complex rebase or merge
- Before a large refactor touching many files
- Before a migration or breaking change
- Before any work where failure means painful recovery

**Skip for routine work.** If the blast radius is small and recovery is easy, just do the work.

## Process (5 minutes)

### 1. Set the Scene

State what you're about to do in one sentence:

> "The rebase of feature-x onto main has failed catastrophically."

### 2. List Failure Modes

Brainstorm what went wrong. Aim for 5–10 causes. Don't filter — write fast.

Think across these categories:
- **State** — dirty worktree, uncommitted changes, lost stashes
- **Conflicts** — files changed in both branches, semantic conflicts that compile but break behavior
- **Dependencies** — version mismatches, lock file conflicts, broken imports
- **Tests** — tests pass but behavior changed, tests not run, flaky tests hide regressions
- **Scope** — change was bigger than expected, touched more systems than planned
- **Recovery** — no backup branch, can't get back to known-good state

### 3. Rate and Prioritize

For each failure mode, assess:
- **Likelihood**: High / Medium / Low
- **Blast radius**: How bad is it if this happens?

Pick the top 3 risks.

### 4. Define Mitigations

For each top risk, write one concrete action to prevent or contain it:

| Risk | L | Blast | Mitigation |
|------|---|-------|------------|
| Semantic conflict in auth module | H | High | Review both branches' changes to auth before rebasing |
| Lost uncommitted work | M | High | Commit or stash everything, verify clean worktree |
| Tests pass but behavior breaks | M | Medium | Run integration tests after rebase, not just unit tests |

### 5. Set Tripwires

Define 1–3 early warning signs that tell you to stop and reassess:

- More than 5 conflict files during rebase
- A test file you didn't expect to change needs updating
- Build fails after resolving conflicts

## Output

Create a `tk` ticket tagged `premortem`:

```
tk create "Pre-mortem: <what you're about to do>" -t task --tags premortem -d "<filled template>"
```

Use this template for the ticket body:

```markdown
## Work: <one-sentence description>

## Top Risks

| # | Risk | L | Blast | Mitigation |
|---|------|---|-------|------------|
| 1 | ... | H | High | ... |
| 2 | ... | M | High | ... |
| 3 | ... | M | Med | ... |

## Tripwires (stop if)
- ...
- ...

## Pre-flight Checks
- [ ] Worktree clean
- [ ] Backup branch created
- [ ] Tests passing on current state
```

## After the Work

Add a note to the premortem ticket with what actually happened:

```
tk add-note <id> "RESULT: <what actually happened vs. predicted>"
tk close <id>
```

This feeds future pre-mortems — you learn which risks you over- or under-estimate.
