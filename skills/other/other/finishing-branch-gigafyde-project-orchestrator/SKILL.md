---
name: project-orchestrator:finishing-branch
description: Use when implementation is complete and ready to merge/PR — handles git repos, auto-deploy awareness, multi-service PR ordering, and changelog.
user-invocable: false
---

# Finishing a Development Branch

## Overview

Guide completion of development work.

**Core principle:** Verify tests → Changelog → Present options → Execute choice → Move plan → Clean up.

**Announce at start:** "I'm using the finishing-branch skill to complete this work."

## Config Loading

1. Check if `.project-orchestrator/project.yml` exists
2. If yes: parse and extract `services`, `structure` (polyrepo/monorepo), `plans_dir`, `plans_structure`
3. If no: use defaults (monorepo, single service at root, `docs/plans/` flat)

---

## Step 0: Detect Worktree

Check the living state doc for a `## Worktree` (monorepo) or `## Worktrees` (polyrepo) section.

If neither section exists: skip to Step 1 (normal flow).

**Monorepo (single worktree):**
1. Note the worktree path (absolute path from design doc)
2. Before presenting options, rebase onto base branch:
   ```bash
   git -C {worktree-path} fetch origin
   git -C {worktree-path} rebase origin/{base-branch}
   ```
3. If rebase conflicts:
   - Run `git -C {worktree-path} rebase --abort` to restore clean state
   - Report the conflicted files to the user
   - Tell user:
     "Rebase has conflicts in: {file list}
     Options:
     1. Resolve manually: run `git -C {worktree-path} rebase origin/{base-branch}`,
        fix conflicts, `git -C {worktree-path} rebase --continue`, then re-run `/project:finish`
     2. Skip rebase and create PR as-is (GitHub will show conflicts)
     3. Keep the branch and handle it later"
   - Wait for user choice. Do NOT auto-resolve.
4. After successful finish (Option 1 or 2):
   - Verify worktree is clean: `git -C {worktree-path} status --porcelain`
   - If clean: `git worktree remove {worktree-path}`
   - If dirty: warn user — "Worktree has uncommitted changes. Force remove, or clean up manually?"
     - Force: `git worktree remove --force {worktree-path}`
     - Manual: keep worktree, user handles it
5. Remove `## Worktree` section from living state doc
6. Run `git worktree prune` to clean up any stale entries

**Polyrepo (per-service worktrees):**
Process each service worktree from the `## Worktrees` table, in merge order
(migrations → producers → consumers — same order as existing Step 6):
1. For each service row in the table:
   - Note the service worktree path from the table
   - Rebase onto base branch: `git -C {worktree-path} fetch origin && git -C {worktree-path} rebase origin/{base-branch}`
   - If rebase conflicts: same conflict handling as monorepo, but per-service.
     Other services can continue independently.
   - Present finish options per service (merge/PR/keep/discard)
   - After finish: verify clean, remove worktree, prune
2. For services NOT in the `## Worktrees` table (skipped during creation):
   - Process in the main service directory as normal (existing Step 1+ flow)
3. After all services processed:
   - Remove `## Worktrees` section from living state doc
   - Update living state doc with per-service results:
     "backend: PR #42 created, frontend: PR #43 created, admin: merged locally"

---

## Step 1: Identify Affected Services

**Polyrepo** (`config.structure: polyrepo`): Each service folder is its own git repo. "Finish branch" means **per-service**.

**Monorepo** (`config.structure: monorepo`): Single repo, single branch operation.

### Service discovery

1. Call `list_branches(pattern: "feature/*")` → aggregate feature branches across all repos (if MCP available)
2. For each affected service, check git state manually:
   ```bash
   git -C <service> branch --show-current
   git -C <service> status
   git -C <service> log --oneline -5
   ```
3. Present findings to user

**Repeat Steps 2-5 for each affected service.**

---

## Step 2: Verify Tests

**Before presenting options, verify tests pass in EACH affected service.**

Test commands come from `config.services[name].test`, the project's root CLAUDE.md, or auto-detection.

**If tests fail:** Stop. Fix before proceeding. Cannot merge/PR with failing tests.

**If tests pass:** Continue to Step 3.

---

## Step 3: Changelog

If `config.services[name].changelog` is configured, invoke the `project-orchestrator:changelog` skill for each affected service before finishing.

If no changelog configured, skip this step.

---

## Step 4: Present Options

Present exactly these 4 options per service:

```
[service-name] implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Use `config.services[name].branch` for the base branch (default: `main`).

---

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
git -C <service> checkout <base-branch>   # from config.services[name].branch
git -C <service> pull
git -C <service> merge <feature-branch>

# Verify tests on merged result (run from service directory)
(cd <service> && <test command>)

# If tests pass
git -C <service> branch -d <feature-branch>
```

**Auto-deploy warning:** If `config.services[name].auto_deploy` is `true`:

```
Warning: Pushing <service> to <base-branch> will trigger auto-deploy.
Push now, or keep local?
```

### Option 2: Push and Create PR

```bash
git -C <service> push -u origin <feature-branch>

(cd <service> && gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets>

## Test Plan
- [ ] <verification steps>
EOF
)")
```

**Never force push** — teammates may be working on the same repos.

### Option 3: Keep As-Is

Report: "Keeping branch `<name>` in `<service>/`. No changes made."

### Option 4: Discard

**Confirm first:**
```
This will permanently delete branch <name> in <service>/.
All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact confirmation. Then:
```bash
git -C <service> checkout <base-branch>
git -C <service> branch -D <feature-branch>
```

---

## Step 6: Multi-Service PR Ordering

When changes span multiple services, suggest merge order:

```
1. Database migrations first
2. Producers next (API endpoints, event publishers)
3. Consumers last (frontend, admin, downstream services)
```

This prevents consumers from deploying against an API that doesn't exist yet.

---

## Step 7: Living State Doc

If working from a plan in `{config.plans_dir}/`:

1. **Update status** in the design doc: `## Status: complete`
2. **Move doc** (if `config.plans_structure` is `standard`):
   ```bash
   mv {plans_dir}/<filename>.md {plans_dir}/completed/
   ```
3. **Update `{plans_dir}/INDEX.md`** (if standard structure):
   - Remove the entry from `## Active`
   - Add it to `## Completed` (use `completed/` path prefix, keep description)

**If flat structure:** Just update the status in the doc, no moving needed.

---

## Step 8: Worktree Cleanup

Worktree cleanup is handled in Step 0 above.

---

## Quick Reference

| Option | Merge | Push | Cleanup Branch | Auto-deploy Risk |
|--------|-------|------|----------------|------------------|
| 1. Merge locally | Yes | User decides | Yes | If pushed + auto_deploy=true |
| 2. Create PR | No | Yes | No | On PR merge only |
| 3. Keep as-is | No | No | No | None |
| 4. Discard | No | No | Yes (force) | None |

---

## Red Flags

**Never:**
- Proceed with failing tests
- Force-push (teammates on same repos)
- Merge without verifying tests on result
- Delete work without typed confirmation
- Push auto-deploy service without warning user
- Skip changelog (when configured)

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Warn about auto-deploy before pushing (check `config.services[name].auto_deploy`)
- Get typed confirmation for Option 4
- Invoke `project-orchestrator:changelog` before finishing (when changelog configured)
- Move plan to `completed/` and update INDEX.md (when standard structure)
- Handle each service separately in polyrepo structure

---

## Related Commands & Skills

| When | Action |
|------|--------|
| Need to verify work first | Suggest user run `/project:verify` |
| Writing changelog entries | Suggest user run `/project:changelog` |
