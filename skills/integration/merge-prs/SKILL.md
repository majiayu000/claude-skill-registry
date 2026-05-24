---
name: merge-prs
description: Merge multiple PRs with conflict resolution and CI failure auto-patching. Analyzes optimal merge order, resolves conflicts, pulls CI logs on failure, and fixes issues. Use when multiple feature branches need merging into the base branch.
argument-hint: "[PR numbers] [--base BRANCH] [--strategy rebase|merge] [--dry-run] [--no-fix] [--no-security] [--force]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, AskUserQuestion
---

# Merge PRs

Merge multiple pull requests into a single integration branch with intelligent conflict resolution, risk scoring, security pre-flight, automated CI failure diagnosis, flaky test awareness, and bisection-based failure isolation.

## When to Use

- You have 2+ open PRs that need to land together or in sequence
- PRs may have conflicts with each other or with the base branch
- CI keeps failing on PRs and you want automated diagnosis + fixes
- You want to validate that all PRs work together before merging to main

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status` works)
- On a clean working tree (`git status` shows no uncommitted changes)
- All target PRs exist and are open

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `$1...$N` | No | all open | Space-separated PR numbers (e.g., `63 64 65 66`) |
| `--base` | No | `main` | Base branch to integrate against |
| `--strategy` | No | `merge` | `merge` (preserve commits) or `rebase` (linear history) |
| `--dry-run` | No | off | Analyze conflicts, risk, and order without merging |
| `--no-fix` | No | off | Skip auto-fix on CI failures (report only) |
| `--no-security` | No | off | Skip security pre-flight checks |
| `--force` | No | off | Proceed even if risk score is RED (>60) |

## Workflow

Copy this checklist and track progress:

```
Merge PRs Progress:
- [ ] Phase 0: Risk assessment & safety (scoring, tiers, security, dry-run)
- [ ] Phase 1: Discovery & analysis (metadata, CI status, conflicts, merge order)
- [ ] Phase 2: CI triage for RED PRs (log retrieval, flaky check, diagnosis, auto-fix)
- [ ] Phase 3: Integration merge (safety tag, sequential merge, conflict resolution, verify)
- [ ] Phase 4: Finalize (summary, changelog, merge strategy, execute)
- [ ] Phase 5: Cleanup (close PRs, delete branches, prune)
```

---

### Phase 0: Risk Assessment & Safety

Run this phase BEFORE any git operations. It gates whether the merge should proceed. See [RISK_SCORING.md](RISK_SCORING.md) for detailed computation tables and commands.

1. **Step 0.1 — PR risk scoring**: Compute 0–100 risk score from diff size (25%), file count (15%), hotspot overlap (25%), test coverage ratio (20%), and PR staleness (15%). Classify as GREEN (0–30), YELLOW (31–60), RED (61–100). If RED and no `--force`, ask user.
2. **Step 0.2 — PR classification**: Auto-classify into merge tiers (always/maybe/iffy/never). `never`-tier PRs excluded from batching.
3. **Step 0.3 — Security pre-flight** (skip if `--no-security`): Scan diffs for secrets and audit dependencies for CVEs. BLOCK on secrets, WARN on CVEs.
4. **Step 0.4 — Pre-merge dry-run**: Test mergeability with `git merge-tree` for actual conflict detection (no working tree changes).

If `--dry-run` was specified, STOP after Phase 0 and report the full analysis.

---

### Phase 1: Discovery & Analysis

#### Step 1.1 — Gather PR metadata

```bash
gh pr list --state open --json number,title,headRefName,baseRefName,additions,deletions,files,mergeable,labels,createdAt
```

If specific PR numbers were given as arguments, filter to only those.
If no arguments, use ALL open PRs targeting the base branch.

Report a summary table:

```
PR  │ Branch                          │ Files │ +/-        │ Risk │ Tier   │ Mergeable
────┼─────────────────────────────────┼───────┼────────────┼──────┼────────┼──────────
#64 │ codex/run-codex-review-since-feb│ 3     │ +104/-2    │  12  │ always │ ✓
#65 │ codex/perform-automated-bug-scan│ 2     │ +6/-16     │   8  │ always │ ✓
#66 │ codex/assess-wizarddemo-flow    │ 4     │ +135/-26   │  34  │ maybe  │ ✓
#63 │ codex/run-tech-debt-check       │ 24    │ +1149/-742 │  72  │ never  │ ✓
```

#### Step 1.2 — Check CI status for each PR

```bash
gh pr checks <PR_NUMBER> --json name,state,conclusion
```

Categorize: **GREEN** (passed), **RED** (failed), **PENDING** (running), **NONE** (no checks).

If any PR is RED and `--no-fix` is NOT set, proceed to **Phase 2 (CI Triage)** for that PR.
If any PR is PENDING, wait up to 5 minutes (polling every 30s) then proceed.

#### Step 1.3 — Analyze pairwise conflicts

Use `git merge-tree` results from Phase 0. Build a conflict matrix showing no overlap, file overlap, or confirmed conflicts between PR pairs.

#### Step 1.4 — Determine optimal merge order

**Ordering heuristic** (apply in priority):

1. **Dependency chain**: If PR-B's branch was created from PR-A's branch, merge A first
2. **Tier ordering**: `always` → `maybe` → `iffy`. `never`-tier PRs offered separately
3. **Conflict minimization**: Merge PRs with fewest predicted conflicts first
4. **Size ascending**: Smaller PRs first
5. **Test PRs first**: PRs that only add tests go before implementation changes
6. **Refactors last**: Large refactoring PRs go last

Ask the user to confirm the merge order before proceeding.

---

### Phase 2: CI Triage (for RED PRs)

For each PR with failing CI checks:

#### Step 2.1 — Pull failure logs

Use the **3-tier log retrieval chain** (see [CI_DIAGNOSIS.md](CI_DIAGNOSIS.md) for details):

```bash
# Tier 1: Check Run Annotations (structured — file, line, message)
OWNER_REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
BRANCH=$(gh pr view <PR_NUMBER> --json headRefName -q '.headRefName')
RUN_ID=$(gh run list --branch "$BRANCH" --status failure --limit 1 --json databaseId -q '.[0].databaseId')
gh api "repos/$OWNER_REPO/check-runs/<CHECK_RUN_ID>/annotations" \
  --jq '.[] | {path: .path, line: .start_line, level: .annotation_level, message: .message}'
```

```bash
# Tier 2: Failed step logs
gh run view "$RUN_ID" --log-failed 2>&1
```

```bash
# Tier 3: Full log tail (last resort)
gh run view "$RUN_ID" --log 2>&1 | tail -200
```

**Prefer Tier 1** — annotations give structured `{file, line, message}` triples for direct edit operations.

#### Step 2.2 — Check for flaky tests

Before diagnosing a test failure as a real regression, check flaky test indicators (see [CI_DIAGNOSIS.md](CI_DIAGNOSIS.md) for flaky test management details):

1. Check local `.claude/flaky-tests.json` registry
2. Check if failing test file was modified by ANY PR being merged
3. **Retry once** if suspected flaky: `gh run rerun <RUN_ID> --failed`
4. **Never retry more than once** — two consecutive failures = real failure

#### Step 2.3 — Diagnose the failure

Parse log output to identify the failure category (see [CI_DIAGNOSIS.md](CI_DIAGNOSIS.md) for failure signatures and fix strategies):

| Category | Auto-fixable? |
|----------|---------------|
| TypeScript error | Yes — read file, fix type |
| ESLint violation | Yes — `npm run lint:fix` |
| Test failure | Maybe — read test + source |
| Build error | Yes — fix imports |
| Env/secret missing | No — report to user |
| Dependency issue | Maybe — `npm ci` or fix versions |
| Timeout/infra | No — retry once, then report |

#### Step 2.4 — Attempt auto-fix

If auto-fixable and `--no-fix` is NOT set:

1. Checkout the PR branch: `gh pr checkout <PR_NUMBER>`
2. Apply the fix based on category
3. Verify locally: `.workstream/verify.sh`
4. If verify passes, commit and push the fix
5. If verify fails again, ask user: attempt another fix (max 2 retries), skip PR, or abort

If NOT auto-fixable, report to user and ask: "Skip this PR and continue, or abort?"

---

### Phase 3: Integration Merge

#### Step 3.1 — Create safety tag and integration branch

```bash
git checkout <base-branch>
git pull origin <base-branch>
git tag "pre-merge/$(date +%Y%m%d-%H%M%S)" <base-branch>
git checkout -b integrate/<descriptive-name>
```

#### Step 3.2 — Merge PRs sequentially

For each PR in the planned merge order:

```bash
git fetch origin <pr-branch>
git merge origin/<pr-branch> --no-edit
```

**If merge has conflicts**, resolve intelligently:

| Conflict Type | Resolution Strategy |
|---------------|---------------------|
| Import additions | Keep both, deduplicate |
| Adjacent line changes | Keep both changes |
| Same line, different changes | Analyze intent — later PR usually incorporates earlier |
| Structural conflicts | Prefer refactoring PR's structure, re-apply other's logic |
| Type definition conflicts | Union the type changes |
| Test file conflicts | Keep all tests from both PRs |
| package-lock.json | `git checkout --theirs package-lock.json && npm install && git add package-lock.json` |

After resolving, verify file is syntactically valid, mark resolved and commit.

#### Step 3.3 — Run local verification

After ALL PRs are merged:

```bash
.workstream/verify.sh
```

If checks pass, proceed to Phase 4. If checks fail and `--no-fix` is NOT set:
1. Diagnose integration failures (duplicate identifiers, type conflicts, test failures from combined changes)
2. Fix and re-run verification
3. Max 3 fix-verify cycles. If still failing, proceed to bisection.

#### Step 3.4 — Bisection on persistent failure

If verification fails after 3 fix attempts, use **binary bisection** to isolate the culprit PR. See [CI_DIAGNOSIS.md](CI_DIAGNOSIS.md) for the full bisection protocol.

For N PRs, this requires at most log2(N) verification runs. Once the culprit is identified, ask user: merge passing subset, attempt to fix, or abort.

---

### Phase 4: Finalize

See [MERGE_STRATEGIES.md](MERGE_STRATEGIES.md) for detailed templates and commands.

1. **Step 4.1 — Summary report**: Present risk scores, merge results, CI fixes, integration fixes, and verification status.
2. **Step 4.2 — Changelog preview**: Generate categorized changelog from PR titles (feat/fix/refactor/test/docs).
3. **Step 4.3 — Ask merge strategy**: Offer 4 options: (1) squash to main, (2) merge commit to main, (3) new combined PR (recommended), (4) keep for review.
4. **Step 4.4 — Execute**: Run the chosen strategy. For Options 1/2, ask before pushing.
5. **Step 4.5 — Post-merge validation** (Options 1/2 only): Poll CI on merge commit (up to 15 min). If CI fails, auto-draft revert PR.

---

### Phase 5: Cleanup

See [MERGE_STRATEGIES.md](MERGE_STRATEGIES.md) for detailed commands.

After integration succeeds, **automatically prompt** for cleanup:
- Close original PRs with "Included in #N" comment and delete their remote branches
- Delete integration branch (local + remote) and safety tag
- Switch to main, pull latest, prune stale references
- Delete local branches whose remotes are gone

---

## Error Handling

### Fatal errors (abort immediately)
- `gh auth status` fails → "Please run `gh auth login` first"
- Base branch doesn't exist → "Branch `<name>` not found"
- No open PRs found → "No open PRs targeting `<base>`"

### Recoverable errors
- Single PR fails to merge → Ask user: skip or abort
- CI fix fails after retries → Report and ask: skip PR or abort
- Integration verification fails → Bisect, then offer partial merge or abort
- Post-merge CI fails → Draft revert PR

### Cleanup on abort
If aborting mid-process:
```bash
git merge --abort 2>/dev/null
git checkout <original-branch>
git branch -D integrate/<name> 2>/dev/null
git branch -D bisect-test 2>/dev/null
```
Report: "Integration aborted. Cleaned up integration branch. You're back on `<original-branch>`."

**Safety tags are NEVER deleted automatically.** Report their names so the user can clean up when ready.

## Guardrails

- **NEVER force-push** to any branch during this process
- **NEVER delete remote branches** without explicit user confirmation (Phase 5 cleanup prompt counts)
- **NEVER delete safety tags** without explicit user confirmation (Phase 5 cleanup prompt counts)
- **NEVER merge directly to main** without user confirmation at Step 4.3
- **NEVER auto-merge RED-tier PRs** without `--force` or explicit confirmation
- **NEVER suppress security findings** — always report detected secrets/CVEs
- **Max 2 auto-fix attempts per PR** (Phase 2), **max 3 for integration** (Phase 3)
- **Max 1 flaky test retry** per failing test — two failures = real failure
- **Always preserve the original integration branch** until user confirms success
- If conflict resolution is ambiguous, **always ask the user** rather than guessing
- **Commit CI and integration fixes with clear messages** — never silent fixes

**REMINDER**: These guardrails apply throughout all phases. Never force-push, never suppress security findings, and always ask for confirmation before destructive actions.
