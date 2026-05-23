---
name: micro-task-workflow
description: Micro-task development patterns with 50% context budget. Use for task decomposition, context management, escape hatch protocols, and orchestration patterns.
---

# micro-task-workflow Skill

**Micro-task constraints and context budget management.**

> For workflow entry point, run `./worktree.py start`

## When to Use This Skill

- Understanding micro-task constraints
- Escape hatch protocol when hitting context limits
- Planning dependencies between tasks

---

## The Problem: Context Exhaustion

Agents running out of context mid-task produce broken, incomplete work:

```
❌ OLD: Issue #100 "Implement Feature X"
├── Read 8 files to understand (~20% context)
├── Plan changes (~10% context)
├── Edit 4 files (~30% context)
├── Debug issues (~20% context)
├── Run tests (~15% context)
└── CONTEXT EXHAUSTED at 95% - work incomplete, uncommitted
```

## The Solution: 50% Budget

```
✅ NEW: Issue #100 "Implement Feature X"
├── Micro-Task 100.1: Setup + config changes (45% context) ✓ committed
├── Micro-Task 100.2: Core implementation (45% context) ✓ committed
├── Micro-Task 100.3: Tests + documentation (45% context) ✓ committed
└── All work committed, PR ready
```

---

## Micro-Task Constraints

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| File reads | ≤ 5 files | Minimize exploration |
| File edits | ≤ 3 files | Single logical change |
| Tool calls | ≤ 80 total | ~50% of context capacity |
| Commits | 1-2 | Checkpoint + final |
| Scope | Single concern | Complete in one session |

### Context Budget Breakdown

| Phase | Budget | Purpose |
|-------|--------|---------|
| Startup overhead | ~20% | Load AGENTS.md, read issue, read source files |
| Productive work | ~50% | Actual implementation |
| Safety margin | ~30% | Unexpected complexity, debugging |

---

## Escape Hatch Protocol

**At 60% context usage (or ~60 tool calls):**

1. **Commit current progress** (even if incomplete):
   ```bash
   git add -A && git commit -m "WIP(#100): partial progress"
   git push
   ```

2. **Write session state** to `.claude/session-state.md`

3. **Exit cleanly** - do not continue until fresh session

---

## Dependency Types

**Serial micro-tasks** (must run sequentially):
- Same file modified by both (merge conflicts)
- Output of one is input to another
- Database schema changes before queries
- API endpoint before frontend integration

**Parallel micro-tasks** (can run simultaneously):
- Different files entirely
- Same issue, independent concerns (e.g., tests vs docs)
- Different issues with no shared files
- Frontend and backend on different endpoints

### Parallelization Rules

| Scenario | Parallel? | Reason |
|----------|-----------|--------|
| Different issues, different files | Yes | No conflicts |
| Same issue, independent files | Yes | No conflicts |
| Same file modified | No | Merge conflicts |
| Sequential dependency | No | Output needed |
| Database migration + queries | No | Schema dependency |

---

## Worktree Strategy

**Single worktree per issue** (recommended):
- All micro-tasks for issue #51 run in worktree `51-feature-name`
- Sequential micro-tasks commit to same branch
- Squash to single commit before PR

**Squash before PR:**
```bash
git rebase -i main           # Squash all commits
git push --force-with-lease
```
