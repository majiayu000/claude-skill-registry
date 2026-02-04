---
name: cook
description: Implement features end-to-end with smart intent detection. Accepts natural language or plan paths. Auto-routes to appropriate workflow (fast, auto, parallel, code).
version: 2.0.0
---

# Cook - Smart Feature Implementation

End-to-end implementation with automatic workflow detection.

**Principles:** YAGNI, KISS, DRY | Token efficiency | Concise reports

## Usage

```
/cook <natural language task OR plan path>
```

**Optional flags:** `--fast`, `--parallel`, `--no-test`, `--auto`

## Smart Intent Detection

| Input Pattern | Detected Mode | Behavior |
|---------------|---------------|----------|
| Path to `plan.md` or `phase-*.md` | code | Execute existing plan |
| Contains "fast", "quick" | fast | Skip research, scout→plan→code |
| Contains "trust me", "auto" | auto | Auto-approve all steps |
| Lists 3+ features OR "parallel" | parallel | Multi-agent execution |
| Contains "no test", "skip test" | no-test | Skip testing step |
| Default | interactive | Full workflow with user input |

See `references/intent-detection.md` for detection logic.

## Workflow Overview

```
[Intent Detection] → [Research?] → [Plan] → [Implement] → [Test?] → [Review] → [Finalize]
```

| Mode | Research | Testing | Review | All Phases |
|------|----------|---------|--------|------------|
| interactive | ✓ | ✓ | User approval | One at a time |
| auto | ✓ | ✓ | Auto if score≥9.5 | All at once |
| fast | ✗ | ✓ | Simplified | One at a time |
| parallel | Optional | ✓ | User approval | Parallel groups |
| no-test | ✓ | ✗ | User approval | One at a time |
| code | ✗ | ✓ | User approval | Per plan |

## Step Output Format

```
✓ Step [N]: [Brief status] - [Key metrics]
```

## Blocking Gates

- **Testing:** 100% pass required (unless no-test mode)
- **Review:** User approval OR auto-approve (score≥9.5, 0 critical)
- **Finalize:** project-manager AND docs-manager must complete

## Required Subagents

| Phase | Subagent |
|-------|----------|
| Research | `researcher` (parallel, optional in fast) |
| Scout | `scout` |
| Plan | `planner` |
| UI Work | `ui-ux-designer` |
| Testing | `tester`, `debugger` |
| Review | `code-reviewer` |
| Finalize | `project-manager`, `docs-manager`, `git-manager` |

## References

- `references/intent-detection.md` - Detection rules and routing logic
- `references/workflow-steps.md` - Detailed step definitions for all modes
- `references/review-cycle.md` - Interactive and auto review processes
- `references/subagent-patterns.md` - Subagent invocation patterns
