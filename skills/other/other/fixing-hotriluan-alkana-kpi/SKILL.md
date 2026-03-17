---
name: fixing
description: This skill should be used when fixing bugs, errors, issues, or problems of any complexity. It provides intelligent issue resolution with mode selection (autonomous/human-in-the-loop/quick). The skill auto-classifies issue complexity (simple/moderate/complex/parallel), activates relevant skills (debugging, problem-solving, sequential-thinking, brainstorming, context-engineering), and routes to appropriate workflow. This skill should be activated when users report bugs, test failures, type errors, CI/CD failures, log errors, UI issues, or any code that needs fixing.
version: 1.0.0
---

# Fixing

Unified skill for fixing issues of any complexity with intelligent routing.

## Step 0: Mode Selection

**First action:** Use `AskUserQuestion` to determine workflow mode:

| Option | Recommend When | Behavior |
|--------|----------------|----------|
| **Autonomous** | Simple/moderate issues | Auto-approve if score >= 9.5 & 0 critical |
| **Human-in-the-loop** | Critical/production code | Pause for approval at each step |
| **Quick** | Type errors, lint, trivial bugs | Fast debug → fix → review cycle |

See `references/mode-selection.md` for AskUserQuestion format.

## Step 1: Complexity Assessment

Classify before routing. See `references/complexity-assessment.md`.

| Level | Indicators | Workflow |
|-------|------------|----------|
| **Simple** | Single file, clear error, type/lint | `references/workflow-quick.md` |
| **Moderate** | Multi-file, root cause unclear | `references/workflow-standard.md` |
| **Complex** | System-wide, architecture impact | `references/workflow-deep.md` |
| **Parallel** | 2+ independent issues | Parallel `fullstack-developer` agents |

## Skill Activation Matrix

See `references/skill-activation-matrix.md` for complete matrix.

**Always activate:** `debugging` (all workflows)
**Conditional:** `problem-solving`, `sequential-thinking`, `brainstorming`, `context-engineering`
**Subagents:** `debugger`, `researcher`, `planner`, `code-reviewer`, `tester`, `git-manager`
**Parallel:** Multiple `Explore` agents for scouting, `Bash` agents for verification

## Output Format

Unified step markers:
```
✓ Step 0: [Mode] selected - [Complexity] detected
✓ Step 1: Root cause identified - [summary]
✓ Step 2: Fix implemented - [N] files changed
✓ Step 3: Tests [X/X passed]
✓ Step 4: Review [score]/10 - [status]
✓ Step 5: Complete - [action taken]
```

## References

Load as needed:
- `references/mode-selection.md` - AskUserQuestion format for mode
- `references/complexity-assessment.md` - Classification criteria
- `references/workflow-quick.md` - Quick: debug → fix → review
- `references/workflow-standard.md` - Standard: full pipeline
- `references/workflow-deep.md` - Deep: research + brainstorm + plan
- `references/review-cycle.md` - Review logic (autonomous vs HITL)
- `references/skill-activation-matrix.md` - When to activate each skill
- `references/parallel-exploration.md` - Parallel Explore/Bash patterns
