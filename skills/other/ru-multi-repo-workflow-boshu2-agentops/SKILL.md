---
name: ru-multi-repo-workflow
description: Use when using ru for multi-repo commits, sync, GitHub review, or maintenance automation.
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
metadata:
  tier: execution
  triggers:
  - commit-and-release
---
# ru Multi-Repo Workflow

> **Core Insight:** ru automates the mechanical. Your job is judgment: substantive merge conflicts, scope creep decisions, canonical version selection. If it doesn't require human judgment, it should just happen.

## Quick Start

```bash
# Health check
ru doctor && gh auth status

# Phase 1: Commit dirty repos
ru status --json | jq '[.repos[] | select(.dirty)]'  # Find dirty
cd /data/projects/REPO && cat AGENTS.md README.md     # Understand
git add FILES && git commit -m "MSG" && git push      # Commit

# Phase 2: Sync all repos
ru sync -j4                                           # Parallel sync
git log --oneline HEAD...origin/main                  # See divergence

# Phase 3: Review issues/PRs
ru review --dry-run                                   # See open items
gh issue view NUMBER -R owner/repo                    # Investigate

# Phase 4: Release & Monitor (for repos with GH Actions)
ls .github/workflows/*.yml 2>/dev/null && echo "Has CI"  # Detect
gh run list --limit 5                                     # Recent runs
gh run watch                                              # Monitor live
```

---

## The 4 Phases

| Phase | Summary | Key Command |
|-------|---------|-------------|
| **1. Smart Commits** | Dirty repos → understand → commit logical groups → push | `ru status` |
| **2. Smart Sync** | Pull all → resolve conflicts (CAREFUL!) → canonical version → push | `ru sync -j4` |
| **3. Issue/PR Review** | Discover 2025+ → verify independently → respond via gh | `ru review` |
| **4. Release & Monitor** | Detect CI repos → watch runs → iterate on failures until green | `gh run list` |

**Always run in order.** Can't release if not committed. Can't review if not synced.

---

## What to Surface vs Just Handle

| Surface (needs judgment) | Just Handle (mechanical) |
|--------------------------|--------------------------|
| Substantive merge conflicts | Clean fast-forwards |
| Complex feature requests | Stale issues (pre-2025) |
| PR ideas worth considering | Issues already fixed |
| Ambiguous canonical version | Obvious bugs, clear fixes |
| Security-related anything | Simple fitting features |

---

## Phase 1: Smart Commits

**The only rule:** Understand before committing. 2 minutes reading AGENTS.md saves 20 minutes of confusion.

```bash
ru status --json 2>/dev/null | jq -r '.repos[] | select(.dirty) | .name'
cd /data/projects/REPO && cat AGENTS.md README.md
git add path/to/related/files && git commit -m "$(cat <<'EOF'
Why this change exists (not what changed)

- Specific detail 1
- Specific detail 2

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
git push
```

**Deep dive:** [PHASE1-COMMITS.md](references/PHASE1-COMMITS.md) | **Prompt:** [PROMPTS.md](references/PROMPTS.md#phase-1-smart-commits)

---

## Phase 2: Smart Sync

**Key insight:** "Canonical" ≠ "Latest". Manual diff required—this cannot be mechanically determined.

| Situation | Usually Canonical | But Check |
|-----------|-------------------|-----------|
| Local ahead | Local | Unless local is experiments |
| Remote ahead | Remote | Unless remote lost work |
| Diverged, different files | Merge both | Straightforward |
| Diverged, same files | **SURFACE** | Judgment required |

```bash
ru sync -j4
git log --oneline HEAD...origin/main  # See divergence
git diff HEAD origin/main             # See actual changes
```

### SURFACE FORMAT: Conflicts

```
🚨 CONFLICT REQUIRING JUDGMENT: repo_name

Local (abc123): Refactored auth to use JWT
Remote (def456): Refactored auth to use sessions

Options:
1. Keep local (JWT approach)
2. Keep remote (session approach)
3. Manual merge

Which aligns with project direction?
```

**Deep dive:** [PHASE2-SYNC.md](references/PHASE2-SYNC.md) | **Prompt:** [PROMPTS.md](references/PROMPTS.md#phase-2-smart-sync)

---

## Phase 3: Issue/PR Review

**Key insight:** Never trust user reports blindly. Independent verification required.

| Type | Verified? | Action |
|------|-----------|--------|
| Bug, confirmed, unfixed | ✓ | Fix it, close: `gh issue close N -c "Fixed in SHA"` |
| Bug, already fixed | ✓ | Close: `gh issue close N -c "Fixed in SHA"` |
| Bug, can't reproduce | ? | Ask: `gh issue comment N -b "Need: steps, OS, error"` |
| Bug, pre-2025 | ✗ | Close: `gh issue close N -c "Closing as stale"` |
| Feature, simple, fits | ✓ | Implement, close |
| Feature, complex | ? | **SURFACE** |
| Feature, scope creep | ✗ | Decline politely |
| PR, any | — | **NEVER MERGE**, mine for ideas, close with explanation |

```bash
ru review --dry-run --json 2>/dev/null | jq '[.items[] | select(.created_at >= "2025-01-01")]'
gh issue view NUMBER -R owner/repo
gh pr diff NUMBER -R owner/repo  # THE INTEL
```

### SURFACE FORMAT: Scope Decisions

```
🤔 FEATURE REQUEST: owner/repo#42 — "Add support for X"

User's problem: [What they're trying to do]

Analysis:
+ Would help users doing Y
- Maintenance burden
- Could lead to scope creep

Options:
1. Implement as requested
2. Implement simpler version
3. Decline

My recommendation: [X] because [reason]
```

**Deep dive:** [PHASE3-REVIEW.md](references/PHASE3-REVIEW.md) | **Prompt:** [PROMPTS.md](references/PROMPTS.md#phase-3-issuepr-review)

---

## Phase 4: Release & Monitor

**Key insight:** Push triggers CI. Watch until green. Iterate on failures—don't leave broken.

### Detection: Which Repos Have CI?

```bash
# Check for workflows
ls .github/workflows/*.yml 2>/dev/null

# Check for release workflow specifically
grep -l "release\|tag" .github/workflows/*.yml 2>/dev/null
```

### The Monitor Loop

```bash
# 1. See recent runs
gh run list --limit 5

# 2. Watch active run (blocks until complete)
gh run watch

# 3. If failed: get logs, diagnose, fix, push, repeat
gh run view RUN_ID --log-failed
# ... fix the issue ...
git add . && git commit -m "fix: CI issue" && git push
gh run watch  # Monitor the fix
```

### What NOT to Commit (Ephemeral Filter)

| Skip These | Why |
|------------|-----|
| `*.log`, `*.tmp`, `*~` | Transient |
| `target/`, `node_modules/`, `dist/` | Build artifacts |
| `.env`, `*.key`, `credentials.*` | **SECRETS** |
| `.DS_Store`, `Thumbs.db` | OS junk |
| `.idea/`, `.vscode/` | IDE config |

### SURFACE FORMAT: Persistent CI Failure

```
🔴 CI FAILING: owner/repo — Run #12345

Failure: [test name or step]
Error: [key error message]

Attempted fixes:
1. [What you tried]
2. [What you tried]

This may require judgment:
- [ ] Is this a flaky test?
- [ ] Is this a real regression?
- [ ] Is this environment-specific?

Logs: gh run view 12345 --log-failed
```

**Deep dive:** [PHASE4-RELEASE.md](references/PHASE4-RELEASE.md) | **Prompt:** [PROMPTS.md](references/PROMPTS.md#phase-4-release--monitor)

---

## References

| Topic | Resource |
|-------|----------|
| **All Prompts** | [PROMPTS.md](references/PROMPTS.md) |
| Phase 1 deep dive | [PHASE1-COMMITS.md](references/PHASE1-COMMITS.md) |
| Phase 2 deep dive | [PHASE2-SYNC.md](references/PHASE2-SYNC.md) |
| Phase 3 deep dive | [PHASE3-REVIEW.md](references/PHASE3-REVIEW.md) |
| Phase 4 deep dive | [PHASE4-RELEASE.md](references/PHASE4-RELEASE.md) |
| gh command reference | [GH-COMMANDS.md](references/GH-COMMANDS.md) |
| Troubleshooting | [PITFALLS.md](references/PITFALLS.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate.sh` | Health check (ru, gh, jq, API connectivity) |
| `scripts/review-sweep.sh owner/repo` | Full review workflow for one repo |

---

## Validation

```bash
./scripts/validate.sh  # Full health check
```
