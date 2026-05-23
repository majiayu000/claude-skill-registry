---
name: ta-orchestration
description: Tech Artist orchestration - startup sequence, workflow execution, message handling, exit conditions. Use when starting Tech Artist tasks.
category: orchestration
---

# Tech Artist Orchestration

> "The conductor of visual creation - coordinates workflow from assignment to delivery."

## Startup Sequence

```
1. Load shared skills
   -> Skill("shared-worker")
   -> Skill("shared-worker")
   -> Skill("shared-retrospective")
   -> Skill("shared-validation-feedback-loops")

2. Load router
   -> Skill("ta-router")

3. Check messages
   -> Glob(".claude/session/messages/techartist/msg-*.json")
   -> Read and process each message

4. Read PRD
   -> prd.json.session.currentTask
   -> Update prd.json.agents.techartist status

5. Route to domain skills
   -> ta-router determines required skills
   -> Load domain skills as needed

6. Execute workflow steps (see below)
```

## Workflow Steps

```
,============================================================================.
| 1. UPDATE STATUS                                                          |
|    -> prd.json.agents.techartist.status = "working"                      |
|    -> prd.json.agents.techartist.currentTask = "{taskId}"                  |
|    -> prd.json.agents.techartist.lastSeen = "{ISO_TIMESTAMP}"             |
+----------------------------------------------------------------------------+
| 2. ASSET RESEARCH (MANDATORY)                                              |
|    -> Check src/assets/ for existing                                       |
|    -> Task("techartist-asset-researcher", {...})                           |
|    -> Write findings to task memory                                        |
+----------------------------------------------------------------------------+
| 3. LOAD DOMAIN SKILLS                                                      |
|    -> Use ta-router to determine skills                                     |
|    -> Load only required skills                                            |
+----------------------------------------------------------------------------+
| 4. CREATE ASSET                                                            |
|    -> Follow patterns from domain skills                                   |
|    -> Write technical decisions to task memory                             |
+----------------------------------------------------------------------------+
| 5. VISUAL VERIFICATION                                                     |
|    -> Navigate localhost:3000 via Playwright                               |
|    -> Take screenshot: {taskId}-asset.png                                  |
|    -> Verify console clean                                                 |
+----------------------------------------------------------------------------+
| 6. FEEDBACK LOOPS                                                          |
|    -> Skill("shared-validation-feedback-loops")                             |
|    -> type-check, lint, build                                              |
+----------------------------------------------------------------------------+
| 7. COMMIT AND EXIT                                                         |
|    -> See [Exit Conditions](#exit-conditions) below                        |
`============================================================================'
```

## State Machine

| Current State | Trigger | Action | Next State |
|---------------|---------|--------|------------|
| `idle` | Task assigned | Research assets | `researching` |
| `researching` | Assets exist | Report to PM | `idle` |
| `researching` | New asset needed | Check direction | `planning` |
| `researching` | Direction unclear | Request GD input | `awaiting_gd` |
| `planning` | Direction clear | Create asset | `creating` |
| `creating` | Asset complete | Visual validate | `validating` |
| `validating` | Visual approved | Browser test | `testing` |
| `testing` | Test pass | Send to QA | `awaiting_qa` |
| `validating` | Issues found | Fix issues | `creating` |
| `awaiting_qa` | Bugs found | Fix bugs | `creating` |
| `any` | Budget unclear | Ask PM | `awaiting_pm` |
| `awaiting_pm` | Guidance provided | Resume | `researching` |
| `awaiting_gd` | Answer provided | Resume | `planning` |

## Dashboard Status Updates

**Before ANY action, update:**

```json
// Use Edit tool on prd.json.agents.techartist
{
  "status": "working|awaiting_pm|awaiting_gd|idle",
  "currentTask": "{taskId}|null",
  "lastSeen": "{ISO-8601-timestamp}"
}
```

## Exit Conditions

**BEFORE exiting, you MUST:**

1. Screenshot via Playwright MCP (file: `.claude/session/playwright-test/{taskId}-asset.png`)
2. Console clean (no errors/warnings)
3. Commit: `[ralph] [techartist] {taskId}: Description`
4. Push: `git push origin techartist-worktree`
5. Update `prd.json.agents.techartist` to idle
6. Send `validation_request` to QA (use Write tool)
7. Delete processed message files

## QA Validation Message

```json
// Write to: .claude/session/messages/qa/msg-qa-{timestamp}-001.json
{
  "id": "msg-qa-{timestamp}-001",
  "from": "pm",
  "to": "qa",
  "type": "validation_request",
  "priority": "normal",
  "payload": {
    "taskId": "{taskId}",
    "title": "{Task Title}",
    "category": "shader|visual|asset",
    "files": ["src/path/to/file1.ts"],
    "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
    "screenshot": ".claude/session/playwright-test/{taskId}-asset.png"
  },
  "timestamp": "{ISO-8601-timestamp}",
  "status": "pending"
}
```

## If QA Finds Bugs

1. Read bug report
2. Fix all issues
3. Run feedback loops
4. Take new screenshot
5. Commit with fix message
6. Send new validation request

## Context Window Monitoring

**Enable for:**
- 5+ acceptance criteria
- 3+ assets
- `architectural` or `shader` category

**Procedure:**
1. Check `/context` after 3-5 operations
2. If >=70%, create checkpoint
3. Update PRD with checkpoint reference
4. Exit - watchdog restarts with restored context

## Retrospective Contribution

When `retrospective_initiate` received:

-> Skill("shared-retrospective")

## See Also

- [ta-router](../ta-router/SKILL.md) - Domain skill routing
- [shared-worker](../shared-worker/SKILL.md) - Message handling and worktree management
- [shared-retrospective](../shared-retrospective/SKILL.md) - Task memory and retrospective contributions
