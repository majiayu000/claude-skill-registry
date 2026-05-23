---
name: workflow-postmortem
description: Dual-mode workflow issue logger. Use with mode=log to append mistakes during waves. Use with mode=summary at workflow end to review accumulated issues. Use when completing /build, /audit, or /ms workflows.
---

# Workflow Postmortem Skill

> **ROOT AGENT ONLY** - Called by commands only, never by subagents.

**Purpose:** Track workflow deviations as they happen, summarize at end
**Output:** `docs/epics/in-progress/{project-folder}/post-mortem.md`

## Modes

| Mode      | When to Use                 | Action                            |
| --------- | --------------------------- | --------------------------------- |
| `log`     | Before compact at each wave | Quick append of obvious mistakes  |
| `summary` | At workflow end             | Read log, present summary to user |

---

## Quick Log Mode (mode=log)

**Time budget:** 30 seconds max - observation only

### Steps

1. **Observe:** What wave completed? Any obvious mistakes?
2. **Append:** If issues, add to post-mortem.md (create if missing)
3. **Continue:** No report, return control for compact

### File Format

```markdown
# Post-Mortem Log

**Workflow:** {command} - {description}
**Started:** {YYYY-MM-DD HH:MM}

## Issues

- Wave 1: Wrong agent - used coder for analysis instead of code-explorer
- Wave 2: Skipped HITL approval on FULL path
- Wave 3: Task failed - test runner not found
```

**Rules:** One line per issue, wave number, under 80 chars, append only

---

## Full Summary Mode (mode=summary)

**Trigger:** After all phases complete, BEFORE final report

### Steps

1. **Read:** Load post-mortem.md (missing/empty = clean workflow)
2. **Analyze:** Count by category, identify patterns
3. **Report:** Present summary to user
4. **Append:** Add summary section to file

### Output Format

**Clean:** `Workflow Postmortem: No issues logged`

**Issues found:**

```
Workflow Postmortem: 3 issues logged across 2 waves
By Category: Wrong agent (1), Skipped step (1), Failed task (1)
Details in: docs/epics/in-progress/{folder}/post-mortem.md
```

---

## Issue Categories

| Category      | Example                                          |
| ------------- | ------------------------------------------------ |
| Wrong agent   | Used coder for analysis instead of code-explorer |
| Skipped step  | HITL approval skipped on FULL path               |
| Out of order  | Validation before execution                      |
| Failed task   | Task failed but workflow continued               |
| Missing skill | Expected skill not invoked                       |
| Incomplete    | Workflow aborted early                           |

---

## Example

**Wave 1 (log):** Append `- Wave 1: Wrong agent - used coder for analysis`
**Wave 2 (log):** No issues, nothing appended
**Wave 3 (log):** Append `- Wave 3: Skipped HITL` and `- Wave 3: Task failed`
**End (summary):** Read file, output "3 issues across 2 waves", append summary section
