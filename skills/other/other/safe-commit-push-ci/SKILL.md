---
name: safe-commit-push-ci
description: Ship local changes to origin/dev with hard-enforced git safety policy, integrator-shell lock/guard flow, validate-changes gating, and CI watch-fix loops until required checks pass.
---

# Safe Commit Push CI

Use this skill when the goal is to ship local work safely to `origin/dev`, fix CI failures quickly, and repeat until required checks are green.

## Hardcoded Safety Baseline (non-negotiable)

This skill must align with enforced repo controls, not just documentation:

- `.claude/hooks/pre-tool-use-git-safety.sh`
- `scripts/agent-bin/git`
- `scripts/git-hooks/require-writer-lock.sh`
- `scripts/git-hooks/pre-push-safety.sh`
- `scripts/git-hooks/prepare-commit-msg-safety.sh`
- `scripts/git-hooks/pre-rebase-safety.sh`
- `AGENTS.md`
- `docs/git-safety.md`
- `scripts/__tests__/git-safety-policy.test.ts`

### Hard-blocked command classes

Never use:

- destructive resets and cleans (`git reset --hard|--merge|--keep`, `git clean -f*`)
- history rewrite (`git rebase`, `git commit --amend`, force-push variants)
- hook bypass (`--no-verify`, `-n`, `-c core.hooksPath`, `git config core.hooksPath`)
- bulk discard (`git checkout -- .`, directory/glob/multi-path checkout/restore, `git switch --discard-changes`, `checkout -f`)
- stash mutation operations (`git stash` bare, `git stash push|pop|apply|drop|clear`)
- `git worktree` (repo policy forbids worktrees for agent flow)

### Bypass flags/env (human-only, never for agent flow)

Do not use:

- `SKIP_WRITER_LOCK=1`
- `SKIP_SIMPLE_GIT_HOOKS=1`
- `ALLOW_GIT_REBASE=1`
- `ALLOW_COMMIT_MSG_REUSE=1`
- `ALLOW_COMMIT_ON_PROTECTED_BRANCH=1`
- `--no-verify` / `-n`

### Safe sharp tools (allowed, still use carefully)

- `git reset HEAD <file>` (unstage only)
- `git restore --staged <file>` (unstage only)
- `git clean --dry-run` / `git clean -n` (preview only)
- `git stash list|show` (read-only only; see stash policy)

## Runtime Bounds

- `max_attempts`: 3 push/fix loops per request
- `max_duration`: 90 minutes wall clock
- On bound hit, stop and report blocker, attempted fixes, and next highest-leverage action

## Required Execution Mode

In non-interactive agent mode, run each write-related command through integrator command mode:

```bash
scripts/agents/integrator-shell.sh -- <command> [args...]
```

This gives both:

- single-writer lock
- git guard wrapper

Do not use plain `git commit`/`git push` without integrator wrapper.

## Workflow

### 1) Preflight

Run:

```bash
git status --short
git branch --show-current
git fetch origin --prune
```

Rules:

- default shipping branch is `dev`
- if current branch is `main`, `master`, or `staging`, switch to `dev` before committing
- never push directly to protected branches (`pre-push-safety.sh` blocks it anyway)

Optional mode:

- `dry-run`: perform checks/analysis and propose fixes, but do not commit/push

### 2) Lock Readiness and Wait Handling

Before first write command:

```bash
scripts/git/writer-lock.sh status
```

If lock is held:

```bash
scripts/git/writer-lock.sh clean-stale   # only if holder PID is dead on this host
```

Then proceed with `integrator-shell` write commands; it waits for lock availability.

If wait is unexpectedly long, re-check status and report lock holder details.

### 3) Mixed Local Edits and Stash Policy

Default policy is **no new stashes**.

Rationale:

- hard guards block all stash mutations (`stash` bare, `push|pop|apply|drop|clear`)
- creating a stash that cannot be safely restored/cleared creates hidden debt

Required behavior:

- stage only intended files with explicit paths
- leave unrelated edits unstaged and untouched
- if unrelated edits make safe shipping impossible, stop and ask user for direction
- if pre-existing stash entries exist, report them but do not mutate them

### 4) Stage Intended Changes

Use explicit paths:

```bash
scripts/agents/integrator-shell.sh -- git add <file1> <file2> ...
```

Avoid broad staging when unrelated work is present.

### 5) Validate Before Commit

Run:

```bash
bash scripts/validate-changes.sh
```

If validation fails:

- fix root cause locally
- re-run `bash scripts/validate-changes.sh` until green

Testing guardrails while fixing:

- do not run unfiltered `pnpm test`
- use targeted tests and `--maxWorkers=2` for broader test runs
- check for orphaned test processes first (`ps aux | grep jest | grep -v grep`)

### 6) Commit

Commit with integrator wrapper:

```bash
scripts/agents/integrator-shell.sh -- git commit -m "<message>"
```

If hooks fail, fix and retry with a new commit (no amend flow).

### 7) Push

Push with integrator wrapper:

```bash
scripts/agents/integrator-shell.sh -- git push origin dev
```

If rejected (non-fast-forward), follow conflict-safe merge flow below.

### 8) Conflict-Safe Merge Flow (no-loss)

When remote advanced:

1. Create a safety anchor:

```bash
git rev-parse HEAD
scripts/agents/integrator-shell.sh -- git branch "backup/pre-merge-$(date +%Y%m%d-%H%M%S)"
```

2. Merge remote branch additively:

```bash
git fetch origin --prune
scripts/agents/integrator-shell.sh -- git merge --no-ff origin/dev
```

3. If conflicts exist:

```bash
git diff --name-only --diff-filter=U
```

- resolve file-by-file manually
- do not use bulk ours/theirs checkout
- inspect 3-way content when needed:

```bash
git show :1:path/to/file   # base
git show :2:path/to/file   # ours
git show :3:path/to/file   # theirs
```

4. Lockfile conflicts:

- prefer regeneration over manual splice when appropriate (example: `pnpm-lock.yaml` via `pnpm install --lockfile-only`)
- re-run validation after regeneration

5. Post-merge loss check:

```bash
git diff --name-status ORIG_HEAD..HEAD
```

If unexpected deletions or broad rewrites appear, stop and escalate.

6. Re-run `bash scripts/validate-changes.sh`, then push again.

### 9) CI Watch and Auto-Fix Loop

After each push:

1. Capture pushed SHA:

```bash
git rev-parse HEAD
```

2. Poll runs:

```bash
gh run list --branch dev --limit 50 --json databaseId,headSha,workflowName,status,conclusion,url
```

3. Filter to `headSha == <current sha>` only.
4. Ignore stale failures from older SHAs.
5. Wait for required workflows for current SHA to finish.

On failure:

- fetch failed logs:

```bash
gh run view <run-id> --log-failed
```

- reproduce locally
- implement fix
- run `bash scripts/validate-changes.sh`
- commit + push
- restart CI watch for new SHA

Exit only when required workflows for current SHA are green.

### Required Workflow Policy

Evaluate required checks in this order:

1. If `Merge Gate` exists for current SHA, treat it as required gate.
2. Always require `Core Platform CI` for dev shipping.
3. Also require any of these if they ran for current SHA:
   - `Deploy Prime`
   - `Deploy Brikette`
   - `Deploy CMS`
   - `Deploy Skylar`
   - `Deploy Business OS`
   - `Deploy Product Pipeline`
   - `Deploy XA (Stealth Staging)`
   - `Validate Reception`
   - `Lighthouse CI`

### 10) Failure Classification Policy

Classify before changing code:

- `code`: deterministic test/lint/type/runtime failure reproducible locally
  - fix in code, validate, commit, push
- `infra`: runner/network/cache/API timeout/transient platform issue
  - rerun once:

```bash
gh run rerun <run-id> --failed
```

  - if same infra signature repeats, escalate with logs
- `unknown`: cannot classify with confidence
  - gather logs + repro attempts, then escalate

Do not produce code churn for clear infra-only failures.

### 11) CI Improvement Scan

At completion (or bound hit), report top 3 CI improvement opportunities:

- repeated failure classes and where to shift-left checks
- flaky tests and stabilization options
- slowest workflows/jobs and cache miss hotspots
- missing local preflight checks that could prevent remote failures

## Output to User

Always report:

- branch + SHA pushed
- attempts used and elapsed duration
- workflows evaluated and final CI result
- fixes applied during loop
- CI improvement opportunities
- blocker + next step if not green

Use this report shape:

```markdown
## Ship Report
- Mode: [normal|dry-run]
- Branch: dev
- SHA: <head-sha>
- Attempts: <n>/<max_attempts>
- Duration: <elapsed>
- Required workflows: [list]
- CI result: [pass|fail|partial]

## Changes
- Commit: <sha> - <message>
- Commit: <sha> - <message>

## Failures Handled
- Workflow: <name>
- Root cause: <code|infra|unknown>
- Action: <fix|rerun|escalate>
- Outcome: <passed|failed|pending>

## CI Improvements (Top 3)
1. <improvement> - Impact: <...> - Proposed change: <...>
2. <improvement> - Impact: <...> - Proposed change: <...>
3. <improvement> - Impact: <...> - Proposed change: <...>

## If Not Green
- Blocker: <specific blocker>
- Next step: <single highest-leverage action>
```
