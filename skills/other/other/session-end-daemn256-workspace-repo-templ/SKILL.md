---
name: session-end
description: End the session, save context, and produce a handoff artifact.
---

# Session End

The Orchestrator drives this workflow, producing the handoff artifact directly — session operations run inline because they need conversation context. Produce a session handoff artifact that captures work completed, decisions made, and concrete next steps for continuity.

**Prerequisites:** Work performed during the session.

---

## Phase 1: Inventory Session Work

Gather the session state.

### Steps

1. List all files created, modified, or deleted during the session
2. Enumerate decisions made and their rationale
3. Identify any open questions or blockers
4. Note the current branch and its status
5. Check board status for tracked issues — ensure it reflects reality
   - Read `workspace.config.yaml` for `board.project_id`, `board.fields.status.field_id`, and status option IDs

---

## Phase 2: Produce Handoff Artifact

Write the session file.

### Required Sections

| Section        | Required | Content                                              |
| -------------- | -------- | ---------------------------------------------------- |
| Context        | Yes      | Issue/PR links, branch, prior sessions               |
| Summary        | Yes      | What was accomplished this session                   |
| Files Touched  | Yes      | Files created, modified, or deleted (relative paths) |
| Decisions Made | If any   | Key decisions with rationale                         |
| Work Completed | Yes      | Checkboxes; unchecked = partial progress             |
| Open Questions | If any   | Unresolved items the next session should address     |
| Next Steps     | Yes      | Concrete actions, ordered by priority                |
| Blocked On     | If any   | What blocks further progress                         |
| Active Branch  | If any   | Git branch being worked on                           |

### File Convention

**Location:** `.tmp/sessions/`
**Format:** `YYYY-MM-DD-<kebab-title>.md`

### When to Create

| Trigger                            | Example                                     |
| ---------------------------------- | ------------------------------------------- |
| Multi-turn work on a tracked issue | Working on #42 across several conversations |
| Decisions that need to persist     | Chose architecture A over B                 |
| Complex multi-step implementation  | 5+ step plan spanning sessions              |
| Context approaching token limit    | Long conversation near context window       |
| Explicit user request              | "Save session state"                        |

**Skip for:** quick one-off questions, simple single-turn edits, work fully captured by commits.

### Output

```markdown
## Session Handoff

### Summary

<What was accomplished>

### Files Touched

| File   | Action                   |
| ------ | ------------------------ |
| <path> | Created/Modified/Deleted |

### Decisions Made

- <Decision>: <Rationale>

### Work Completed

- [x] <completed item>
- [ ] <incomplete item>

### Open Questions

- <question needing human input>

### Next Steps

1. <highest priority>
2. <second priority>

### Active Branch

`<branch-name>`
```

---

## Phase 3: Verify and Close

### Checklist

- [ ] All sections current and accurate
- [ ] Board status verified for tracked issues
- [ ] Next steps are concrete and actionable
- [ ] Handoff file saved to `.tmp/sessions/`

**Critical:** Session is not complete until the handoff artifact is produced and verified.

### Output

```markdown
## Session Handoff — Closure

**Handoff artifact:** `.tmp/sessions/<filename>.md`
**Board status:** Verified current for all tracked issues

## Next Step

Session complete. Handoff artifact produced.

**Approval Required:** No
```

### ⛔ CHECKPOINT

**STOP.** Verify the handoff artifact is complete and saved before closing session.

---

## Error Handling

| Situation                     | Recovery                                        |
| ----------------------------- | ----------------------------------------------- |
| Files touched list incomplete | Re-check git status and diff for missed changes |
| Board status can't be updated | Report failure, document in handoff             |
| Handoff file write fails      | Retry, or present content for manual save       |
| Prior session file conflicts  | Use a distinct filename with topic suffix       |
| Missing issue/PR links        | Search git log and forge for references         |
