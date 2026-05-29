---
name: pm-retrospective-playtest-session
description: Request and process playtest session from Game Designer after retrospective synthesis
category: retrospective
---

# Playtest Session Skill

> "Separate playtest phase enables context reset and focused Game Designer validation."

**IMPORTANT FOR EVENT-DRIVEN MODE:**
Use native Read/Write tools for all message operations. Messages are stored as JSON files in `.claude/session/messages/`.

## When to Use This Skill

Use when:

- `currentTask.status === "retrospective_synthesized"`
- Worker retrospective is complete and committed
- Ready to validate implementation through Game Designer playtest
- Before PRD refinement phase

## Quick Start

```json
// Phase 1: Request Playtest
// Check currentTask.status from prd.json using Read tool
// If status is "retrospective_synthesized":

// Write to: .claude/session/messages/gamedesigner/cmd/{timestamp}.json
{
  "id": "msg-playtest-{timestamp}",
  "from": "pm",
  "to": "gamedesigner",
  "type": "playtest_session_request",
  "payload": {
    "taskId": "{taskId}",
    "taskTitle": "{taskTitle}",
    "retrospectiveComplete": true,
    "context": "Retrospective synthesis complete, validate implementation through playtest",
    "focus": "all",
    "gddReference": "docs/design/gdd.md"
  },
  "timestamp": "{ISO-8601-UTC}"
}

// Then use Edit tool to set status to "playtest_phase"
// Exit for context reset

// Phase 2: Process Playtest Report (on wake-up)
// Use Glob to check for messages: Glob(".claude/session/messages/pm/msg-*.json")
// Read each message using Read tool
// Look for type "playtest_session_report"
```

## State Flow

```
retrospective_synthesized → playtest_phase → playtest_complete
```

## Decision Framework

| Status                             | Action                                                                       |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| `retrospective_synthesized`        | Send `playtest_session_request`, set `playtest_phase`, exit                  |
| `playtest_phase`                   | Wait for `playtest_session_report`                                           |
| `playtest_session_report` received | Review findings, update PRD if needed, commit, set `playtest_complete`, exit |
| `playtest_complete`                | Proceed to PRD refinement phase                                              |

## Progressive Guide

### Level 1: Send Playtest Request

After worker retrospective synthesis is complete:

```json
// Write to: .claude/session/messages/gamedesigner/cmd/{timestamp}.json
{
  "id": "msg-playtest-{timestamp}",
  "from": "pm",
  "to": "gamedesigner",
  "type": "playtest_session_request",
  "payload": {
    "taskId": "{taskId}",
    "taskTitle": "{taskTitle}",
    "retrospectiveComplete": true,
    "context": "Retrospective synthesis complete, validate implementation through playtest",
    "focus": "all",
    "gddReference": "docs/design/gdd.md"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

Then use Edit tool to update `prd.json`: set `currentTask.status = "playtest_phase"`
Exit for context reset.

### Level 2: Process Playtest Report

When Game Designer sends `playtest_session_report`:

```bash
# Check for playtest_session_report message
# Use Glob: Glob(".claude/session/messages/pm/msg-*.json")
# Read each message using Read tool
# Look for type "playtest_session_report"

# Verify mandatory fields: playwrightUsed=true, visionMcpUsed=true

# If validation failed:
# Write to .claude/session/messages/gamedesigner/cmd/{timestamp}.json:
{
  "id": "msg-playtest-reject-{timestamp}",
  "from": "pm",
  "to": "gamedesigner",
  "type": "question",
  "payload": {
    "question": "Playtest must use Playwright MCP and Vision MCP. Please re-run playtest."
  },
  "timestamp": "{ISO-8601-UTC}"
}
# Exit and wait for new playtest

# If validation passed:
# Review findings, screenshots, GDD compliance
# If issues found: create tasks using Edit tool on prd.json
# If recommendations: update PRD using Edit tool
# Commit PRD changes: git add prd.json && git commit -m "..."

# Use Edit tool to set status to "playtest_complete"
# Exit for context reset
```

## Message Types

### playtest_session_request (PM → Game Designer)

```json
{
  "id": "msg-playtest-session-{timestamp}",
  "from": "pm",
  "to": "gamedesigner",
  "type": "playtest_session_request",
  "payload": {
    "taskId": "feat-001",
    "taskTitle": "Completed task title",
    "retrospectiveComplete": true,
    "context": "Retrospective synthesis complete, validate implementation through playtest",
    "focus": "all",
    "gddReference": "docs/design/gdd.md"
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

### playtest_session_report (Game Designer → PM)

```json
{
  "id": "msg-playtest-report-{timestamp}",
  "from": "gamedesigner",
  "to": "pm",
  "type": "playtest_session_report",
  "payload": {
    "taskId": "feat-001",
    "screenshots": [
      "playtest-feat-001-start.png",
      "playtest-feat-001-during.png",
      "playtest-feat-001-end.png"
    ],
    "playwrightUsed": true,
    "visionMcpUsed": true,
    "findings": "Gameplay mechanics working as expected, visual polish needs improvement",
    "gddCompliance": "pass",
    "issues": [],
    "recommendations": []
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

## Anti-Patterns

❌ **DON'T:**

- Skip playtest session and go directly to PRD refinement
- Accept playtest without verifying Playwright MCP was used
- Accept playtest without verifying Vision MCP was used
- Forget to commit PRD changes if issues were found
- Skip updating PRD with playtest findings

✅ **DO:**

- Always request playtest after retrospective synthesis
- Verify `playwrightUsed: true` in playtest report
- Verify `visionMcpUsed: true` in playtest report
- Commit PRD changes if issues were found
- Update PRD with playtest findings and recommendations
- Exit after each step for context reset

## Checklist

**Before sending playtest request:**

- [ ] Worker retrospective is complete
- [ ] Retrospective synthesis is committed
- [ ] Current task status is `retrospective_synthesized`

**After receiving playtest report:**

- [ ] Playwright MCP was used (`playwrightUsed: true`)
- [ ] Vision MCP was used (`visionMcpUsed: true`)
- [ ] At least 3 screenshots included
- [ ] GDD compliance status is documented
- [ ] PRD updated if issues found
- [ ] PRD changes committed (if applicable)
- [ ] Status set to `playtest_complete`
- [ ] Exited for context reset

## Post-Playtest

After playtest is complete:

1. Set `currentTask.status = "playtest_complete"`
2. Proceed to PRD refinement phase
3. Use `pm-prd-organization` skill to extract/update tasks
4. Send `prd_analysis_request` to Game Designer

## Reference

- [pm-retrospective-facilitation](../pm-retrospective-facilitation/SKILL.md) — Worker retrospective phase
- [pm-organization-prd-reorganization](../pm-organization-prd-reorganization/SKILL.md) — PRD refinement phase
- [shared-messaging](../shared-messaging/SKILL.md) — Message protocol
