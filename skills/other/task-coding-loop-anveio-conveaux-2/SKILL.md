---
name: task-coding-loop
description: Earn trust through verification. Invoke at session start to establish verifiable checkpoints (environment, baseline, completion). Trust comes from gates, not claims.
---

# Coding Loop

Trust is earned, not assumed.

## Context: Where Coding-Loop Fits

This skill operates within the **Execute** stage of RSID:

```
USER-DRIVEN:    Listen → Execute ← YOU ARE HERE → Reflect
AUTONOMOUS:     Ideate → Execute ← YOU ARE HERE → Reflect
```

After completing Execute (PR merged), invoke **rsid** skill to Reflect and record learnings.

## The Principle

You have autonomy to change code. That autonomy requires accountability:

| Claim | Gate |
|-------|------|
| "Environment is safe" | devcontainer OR explicit host acknowledgment |
| "Starting state is clean" | `./verify.sh --agent` passes |
| "Changes are correct" | `./verify.sh --agent` passes |
| "Work is complete" | PR merged + main verified |

**No gate, no trust.**

## Session Gates

1. **Start**: Verify baseline green before writing code
2. **Design**: Invoke **coding-patterns** before creating new packages (see Pre-Design Gate below)
3. **Implement**: Verify after significant changes
4. **Pre-PR**: Pass hard gates (see below) before creating PR
5. **Review**: Spawn **tsc-reviewer** subagent (MANDATORY - do NOT self-review)
6. **Complete**: PR merged (not just created) + main verified post-merge
7. **Reflect**: Invoke **rsid** to record learnings in memory.yaml
8. **Stuck**: After 3 failed attempts → escalate, don't loop

## Hard Gates (Blocking)

These gates MUST be satisfied before PR creation:

### 0. Pre-Design Gate (for new packages)

Before designing new contract/port packages, invoke **coding-patterns** skill and answer:

- [ ] Is this a **capability** (interface with methods) or **data structure** (pure types)?
- [ ] If data structure: are operations in port as pure functions (not methods on contract)?
- [ ] Does this follow existing package patterns in the monorepo?

**If creating packages without this gate**: Design will likely conflate data and operations. Stop, invoke skill, redesign.

### 1. Commit Atomicity Gate

```bash
# Check commit count and size
git log --oneline main..HEAD
git diff --stat main..HEAD
```

| Commits | Lines Changed | Action Required |
|---------|---------------|-----------------|
| 1 | > 200 | SPLIT: Use `git rebase -i main` per **effective-git** |
| Any | > 500 total | SPLIT: Break into logical units |

**If gate fails**: Invoke **effective-git** skill and restructure before PR.

### 2. Subagent Review Gate

Before merge, the **tsc-reviewer** subagent MUST approve:

```
Spawn: "Use the tsc-reviewer agent to review this PR"

Loop until:
  - Verdict = APPROVED
  - Blockers = 0

Only then: gh pr merge
```

**If subagent not spawned**: Review is incomplete. Do not merge.
**If blockers remain**: Address findings, re-spawn subagent, repeat.

### 3. Size-Based Skill Invocation

| Change Size | Required Skills |
|-------------|-----------------|
| < 50 lines | coding-loop (this) |
| 50-200 lines | + **tsc-reviewer** (agent for review) |
| > 200 lines | + **effective-git** (restructure first) |
| > 10 files | Consider human review escalation |

## Commands

```bash
./verify.sh --agent    # Minimal output: VERIFY:PASS or structured failure
git status -sb         # Know your state
gh pr diff <n>         # Review before merge (mandatory)
```

## Slash Commands

Use these for accelerated workflows:

| Command | Purpose |
|---------|---------|
| `/verify` | Run full pipeline or specific stage |
| `/verify-lint [package]` | Quick lint check with optional scope |
| `/lint-and-learn` | Auto-fix lint + extract lessons + create PR |
| `/tsc-review <pr>` | Spawn TSC reviewer with auto-merge on APPROVED |

## Deeper Guidance

- **rsid** → outer context, post-merge reflection
- **plan-writing** → rigorous plans for distinguished engineers
- **coding-patterns** → architecture patterns
- **tsc-reviewer** (agent) → mandatory PR review before merge (contains all review criteria)
- **effective-git** → commit discipline
- **verification-pipeline** → debugging failures
- **devcontainer-sandboxing** → environment safety
- **pull-request** → PR authoring and review workflow
