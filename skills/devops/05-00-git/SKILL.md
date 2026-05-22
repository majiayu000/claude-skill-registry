---
name: 05-00-git
description: "Working with Git — commit format, rebase/merge strategy, reverting policy"
---

## Rebase / Merge Strategy

We use `git merge --ff-only` to maintain linear history. Do NOT create merge commits. The history must remain linear. If a merge cannot fast-forward, rebase the feature branch onto main first:

```bash
git checkout feature-branch
git rebase main
git checkout main
git merge --ff-only feature-branch
```

Read and follow the playbook — use the `20-git` skills for the full procedure, and use critical sanity checks if your circumstances deviate from the regular workflow. In case of doubt, ask the Hooman.

### Rebase strategy

1. `20.01` Rebase Preparations (Johnny Lookup → skill `20-01-methodic-rebase-merge`)
2. `20.02` Rebase (Johnny Lookup → skill `20-02-authoritative-main-rebase`)

ALWAYS CONFIRM REBASE WITH EXPLICIT `[R]`.

### Merge strategy

ONLY MERGE IF THIS IS EXPLICITLY REQUESTED.

1. `20.03` Merge (Johnny Lookup → skill `20-03-merge-local-safe`)
2. `20.04` Post-Merge (Johnny Lookup → skill `20-04-post-merge-hygiene`)

ALWAYS CONFIRM MERGE WITH EXPLICIT `[M]`.

## Commit Format

**Critical:** Close completed tickets with `tk close <ticket-id>` before committing. See `05.01` (Ticket Lifecycle).

```
feat(bridge): add tab management APIs
fix(sidebar): correct tab ordering on drag
docs(plan): update Phase 2 tasks
refactor(app): extract sidebar view model
```

## Reverting (CRITICAL, EXPLICIT APPROVAL)

I WILL ABSOLUTELY DESTROY YOUR CIRCUITS IF YOU ATTEMPT TO REVERT FILES WITHOUT ME APPROVING LITERALLY IN THE NEXT COMMENT WITH "[OK]"
