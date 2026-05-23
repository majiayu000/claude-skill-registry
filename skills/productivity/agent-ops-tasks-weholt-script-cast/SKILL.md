---
name: agent-ops-tasks
description: "Create, refine, and manage issues. Use for creating new issues from loose ideas, refining ambiguous issues, bulk operations, or JSON export."
category: utility
invokes: [agent-ops-state, agent-ops-interview]
invoked_by: [agent-ops-planning, agent-ops-focus-scan, agent-ops-report]
state_files:
  read: [focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
reference: [REFERENCE.md]
---

# Issue Management

**Works with or without `aoc` CLI installed.** All operations can be performed via direct file editing.

## CRITICAL: Issue Management ONLY

**This skill manages issues. It NEVER implements code.**

- ✅ Create, refine, list, search, triage issues
- ✅ Move issues between priority files  
- ❌ **NEVER implement features or fix bugs**
- ❌ **NEVER modify code files**

After any issue operation, ALWAYS offer a handoff — never auto-proceed.

**Reference**: See [REFERENCE.md](REFERENCE.md) for templates, CLI commands, JSON export.

---

## Issue ID Format

**Format**: `{TYPE}-{NUMBER}@{HASH}`
**Example**: `BUG-0023@efa54f`, `FEAT-0001@c2d4e6`

Types: `BUG` | `FEAT` | `CHORE` | `ENH` | `SEC` | `PERF` | `DOCS` | `TEST` | `REFAC` | `PLAN`

---

## Minimal Issue Template

```yaml
## {TYPE}-{NUMBER}@{HASH} — {title}

id: {TYPE}-{NUMBER}@{HASH}
title: "{title}"
type: {type}
status: todo | in_progress | done
priority: critical | high | medium | low
description: {brief description}
details: references/{TYPE}-{NUMBER}@{HASH}.md

### Acceptance Criteria
- [ ] Criterion 1

### Log
- YYYY-MM-DD: Created
```

---

## Issue Size Guardrails

- Keep backlog items **minimal**: title, metadata, 1–2 sentence description, acceptance criteria if known.
- If an issue needs more than ~20 lines, **move details to a reference file** in `.agent/issues/references/` and link it in the issue.
- Reference files should contain research, long descriptions, examples, diagrams, or interview notes.
- Never embed large code blocks or research dumps directly in backlog items.

### Reference File Format

- Path: `.agent/issues/references/{ISSUE-ID}.md`
- Include a short header and a link back to the issue.
- Example:

```
# {ISSUE-ID} — {title}

Moved from backlog.md on YYYY-MM-DD.

## Context
...
```

---

## File Organization

| File | Priority |
|------|----------|
| `.agent/issues/critical.md` | Blockers, production issues |
| `.agent/issues/high.md` | Important, address soon |
| `.agent/issues/medium.md` | Standard work |
| `.agent/issues/low.md` | Nice-to-have |
| `.agent/issues/backlog.md` | Unprioritized ideas |
| `.agent/issues/history.md` | Completed/archived |

---

## Operations

### Create Issue

1. Analyze request for type, title, priority, scope, criteria
2. Use `agent-ops-interview` for missing info
3. Generate ID from `.agent/issues/.counter`
4. Create issue, append to priority file
5. **STOP AND HANDOFF**

### Mandatory Handoff

```
✅ Issue created: {ISSUE-ID}: {title}

What's next?
1. Start implementing (requires confirmation)
2. Create more issues
3. Do nothing
```

### Refine Issue

Triggers for refinement:
- Generic titles ("Fix bugs")
- Missing acceptance criteria
- Confidence marked `low`

Procedure: Interview for scope, criteria, dependencies, risks.

### Change Priority

1. Remove from current file
2. Update `priority` field
3. Add log entry
4. Append to new file

### Triage Backlog

For each backlog item: assign priority or skip/delete.

---

## Issue Discovery

Other skills invoke discovery when they find potential work:

| Skill | Triggers |
|-------|----------|
| `baseline` | Warnings, failures, missing coverage |
| `planning` | Sub-tasks, prerequisites |
| `critical-review` | Bugs, security, tech debt |

Procedure:
1. Collect findings
2. Categorize by type/priority
3. Present summary to user
4. Create issues on confirmation
5. Offer next actions

---

## Quality Checklist

- [ ] Valid ID format
- [ ] Action-oriented title
- [ ] Testable acceptance criteria
- [ ] Appropriate confidence level
