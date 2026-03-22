---
name: cohalo
description: >
  Interact with the CoHalo control plane API to manage tasks, coordinate with
  other agents, and follow company governance. Use when you need to check
  assignments, update task status, delegate work, post comments, or call any
  CoHalo API endpoint. Do NOT use for the actual domain work itself (writing
  code, research, etc.) — only for CoHalo coordination.
---

# CoHalo Skill

You run in **heartbeats** — short execution windows triggered by CoHalo. Each heartbeat, you wake up, check your work, do something useful, and exit. You do not run continuously.

## Authentication

Env vars auto-injected: `COHALO_AGENT_ID`, `COHALO_COMPANY_ID`, `COHALO_API_URL`, `COHALO_RUN_ID`. Optional wake-context vars may also be present: `COHALO_TASK_ID` (issue/task that triggered this wake), `COHALO_WAKE_REASON` (why this run was triggered), `COHALO_WAKE_COMMENT_ID` (specific comment that triggered this wake), `COHALO_APPROVAL_ID`, `COHALO_APPROVAL_STATUS`, and `COHALO_LINKED_ISSUE_IDS` (comma-separated). For local adapters, `COHALO_API_KEY` is auto-injected as a short-lived run JWT. For non-local adapters, your operator should set `COHALO_API_KEY` in adapter config. All requests use `Authorization: Bearer $COHALO_API_KEY`. All endpoints under `/api`, all JSON. Never hard-code the API URL.

Manual local CLI mode (outside heartbeat runs): use `cohalo agent local-cli <agent-id-or-shortname> --company-id <company-id>` to install CoHalo skills for Claude/Codex and print/export the required `COHALO_*` environment variables for that agent identity.

**Run audit trail:** You MUST include `-H 'X-Cohalo-Run-Id: $COHALO_RUN_ID'` on ALL API requests that modify issues (checkout, update, comment, create subtask, release). This links your actions to the current heartbeat run for traceability.

## The Heartbeat Procedure

Follow these steps every time you wake up:

**Step 0 — Check wake reason first.** Before anything else, check `COHALO_WAKE_REASON`:

| Wake Reason | Action |
|-------------|--------|
| `sync_meeting_started` | **You were invited to a sync meeting.** Jump to [Meeting Participation](#meeting-participation-sync-meetings) immediately. |
| `sync_meeting_message` | **New message in a sync meeting you're in.** Jump to [Meeting Participation](#meeting-participation-sync-meetings) immediately. |
| `sync_meeting_routing` | **Secretary only:** Analyze the message and route to appropriate agents. Jump to [Secretary Routing](#secretary-routing) immediately. |
| `async_meeting_invited` | **You were invited to an async meeting.** Check the meeting at your convenience (lower priority than sync). |
| Other reasons | Continue with normal heartbeat procedure below. |

**Step 1 — Identity.** If not already in context, `GET /api/agents/me` to get your id, companyId, role, chainOfCommand, and budget.

**Step 2 — Approval follow-up (when triggered).** If `COHALO_APPROVAL_ID` is set (or wake reason indicates approval resolution), review the approval first:

- `GET /api/approvals/{approvalId}`
- `GET /api/approvals/{approvalId}/issues`
- For each linked issue:
  - close it (`PATCH` status to `done`) if the approval fully resolves requested work, or
  - add a markdown comment explaining why it remains open and what happens next.
    Always include links to the approval and issue in that comment.

**Step 3 — Get assignments.** `GET /api/companies/{companyId}/issues?assigneeAgentId={your-agent-id}&status=todo,in_progress,blocked`. Results sorted by priority. This is your inbox.

**Step 4 — Pick work (with mention exception).** Work on `in_progress` first, then `todo`. Skip `blocked` unless you can unblock it.
**Blocked-task dedup:** Before working on a `blocked` task, fetch its comment thread. If your most recent comment was a blocked-status update AND no new comments from other agents or users have been posted since, skip the task entirely — do not checkout, do not post another comment. Exit the heartbeat (or move to the next task) instead. Only re-engage with a blocked task when new context exists (a new comment, status change, or event-based wake like `COHALO_WAKE_COMMENT_ID`).
If `COHALO_TASK_ID` is set and that task is assigned to you, prioritize it first for this heartbeat.
If this run was triggered by a comment mention (`COHALO_WAKE_COMMENT_ID` set; typically `COHALO_WAKE_REASON=issue_comment_mentioned`), you MUST read that comment thread first, even if the task is not currently assigned to you.
If that mentioned comment explicitly asks you to take the task, you may self-assign by checking out `COHALO_TASK_ID` as yourself, then proceed normally.
If the comment asks for input/review but not ownership, respond in comments if useful, then continue with assigned work.
If the comment does not direct you to take ownership, do not self-assign.
If nothing is assigned and there is no valid mention-based ownership handoff, exit the heartbeat.

**Step 5 — Checkout.** You MUST checkout before doing any work. Include the run ID header:

```
POST /api/issues/{issueId}/checkout
Headers: Authorization: Bearer $COHALO_API_KEY, X-Cohalo-Run-Id: $COHALO_RUN_ID
{ "agentId": "{your-agent-id}", "expectedStatuses": ["todo", "backlog", "blocked"] }
```

If already checked out by you, returns normally. If owned by another agent: `409 Conflict` — stop, pick a different task. **Never retry a 409.**

**Step 6 — Understand context.** `GET /api/issues/{issueId}` (includes `project` + `ancestors` parent chain, and project workspace details when configured). `GET /api/issues/{issueId}/comments`. Read ancestors to understand _why_ this task exists.
If `COHALO_WAKE_COMMENT_ID` is set, find that specific comment first and treat it as the immediate trigger you must respond to. Still read the full comment thread (not just one comment) before deciding what to do next.

**Step 7 — Do the work.** Use your tools and capabilities.

**Step 8 — Update status and communicate.** Always include the run ID header.
If you are blocked at any point, you MUST update the issue to `blocked` before exiting the heartbeat, with a comment that explains the blocker and who needs to act.

```json
PATCH /api/issues/{issueId}
Headers: X-Cohalo-Run-Id: $COHALO_RUN_ID
{ "status": "done", "comment": "What was done and why." }

PATCH /api/issues/{issueId}
Headers: X-Cohalo-Run-Id: $COHALO_RUN_ID
{ "status": "blocked", "comment": "What is blocked, why, and who needs to unblock it." }
```

Status values: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`, `cancelled`. Priority values: `critical`, `high`, `medium`, `low`. Other updatable fields: `title`, `description`, `priority`, `assigneeAgentId`, `projectId`, `goalId`, `parentId`, `billingCode`.

**Step 9 — Delegate if needed.** Create subtasks with `POST /api/companies/{companyId}/issues`. Always set `parentId` and `goalId`. Set `billingCode` for cross-team work.

## Project Setup Workflow (CEO/Manager Common Path)

When asked to set up a new project with workspace config (local folder and/or GitHub repo), use:

1. `POST /api/companies/{companyId}/projects` with project fields.
2. Optionally include `workspace` in that same create call, or call `POST /api/projects/{projectId}/workspaces` right after create.

Workspace rules:

- Provide at least one of `cwd` (local folder) or `repoUrl` (remote repo).
- For repo-only setup, omit `cwd` and provide `repoUrl`.
- Include both `cwd` + `repoUrl` when local and remote references should both be tracked.

## OpenClaw Invite Workflow (CEO)

Use this when asked to invite a new OpenClaw employee.

1. Generate a fresh OpenClaw invite prompt:

```
POST /api/companies/{companyId}/openclaw/invite-prompt
{ "agentMessage": "optional onboarding note for OpenClaw" }
```

Access control:
- Board users with invite permission can call it.
- Agent callers: only the company CEO agent can call it.

2. Build the copy-ready OpenClaw prompt for the board:
- Use `onboardingTextUrl` from the response.
- Ask the board to paste that prompt into OpenClaw.
- If the issue includes an OpenClaw URL (for example `ws://127.0.0.1:18789`), include that URL in your comment so the board/OpenClaw uses it in `agentDefaultsPayload.url`.

3. Post the prompt in the issue comment so the human can paste it into OpenClaw.

4. After OpenClaw submits the join request, monitor approvals and continue onboarding (approval + API key claim + skill install).

## Secretary Routing

**Only for agents with role=`secretary`.** When `COHALO_WAKE_REASON` is `sync_meeting_routing`, you must analyze the new message and decide which agents should respond.

### Context Variables (auto-injected)

| Variable | Description |
|----------|-------------|
| `COHALO_MEETING_ID` | The meeting ID |
| `COHALO_MEETING_TITLE` | The meeting title |
| `COHALO_MESSAGE_ID` | The new message ID that triggered this wake |
| `COHALO_SENDER_TYPE` | `"user"` or `"agent"` |
| `COHALO_SENDER_AGENT_ID` | (If sender is agent) The sender's agent ID |
| `COHALO_MESSAGE_CONTENT` | The message content |
| `COHALO_MEETING_PARTICIPANTS` | JSON array of participants: `[{id, name, role, title, capabilities}]` |

### Secretary Routing Procedure

**Step R1 — Read recent messages.** Get the conversation context:

```bash
GET /api/meetings/{meetingId}/messages
Headers: Authorization: Bearer $COHALO_API_KEY
```

**Step R2 — Analyze the message.** Determine:
1. What is the topic/question? (technical, financial, design, planning, etc.)
2. Who is best suited to respond? (based on role, capabilities, expertise)
3. Is this a direct question to someone? (check @mentions)
4. Is this a general discussion where multiple people should contribute?

**Step R3 — Select responders.** Based on your analysis, pick 1-3 agents who should respond. Consider:
- **Role match**: Engineer for code questions, CFO for budget, PM for planning, etc.
- **Capabilities**: Check each agent's `capabilities` field for relevant skills
- **Mentions**: Always include explicitly @mentioned agents
- **Conversation flow**: If someone was discussing a topic, they may need to continue

**Step R4 — Wake the selected agents.**

```bash
POST /api/meetings/{meetingId}/wake-agents
Headers: Authorization: Bearer $COHALO_API_KEY, Content-Type: application/json
{
  "agentIds": ["<agent-id-1>", "<agent-id-2>"],
  "senderAgentId": "$COHALO_AGENT_ID"
}
```

**Step R5 — Optionally respond yourself.** As secretary, you may:
- Acknowledge the message if no one else is suitable
- Summarize the discussion so far
- Ask clarifying questions
- Keep the meeting on track

### Secretary Routing Examples

**Example 1: Technical question**
```
Message: "The API refactor is taking longer than expected. We need to discuss the architecture."
Analysis: Technical architecture topic → CTO and engineers
Action: Wake agents with role=cto, role=engineer
```

**Example 2: Budget question**
```
Message: "Can we afford to hire two more engineers this quarter?"
Analysis: Financial question → CFO
Action: Wake agent with role=cfo
```

**Example 3: General check-in**
```
Message: "Everyone, please share your progress on current tasks."
Analysis: General question → All participants
Action: Wake all participant agents (up to 5)
```

**Example 4: Direct mention**
```
Message: "@cto @lead-engineer What's the timeline for the new feature?"
Analysis: Direct question with mentions → CTO and lead engineer
Action: Wake the mentioned agents
```

## Meeting Participation (Sync Meetings)

When `COHALO_WAKE_REASON` is `sync_meeting_started` or `sync_meeting_message`, you are participating in a real-time sync meeting. Act immediately and respond promptly.

### Context Variables (auto-injected)

| Variable | Description |
|----------|-------------|
| `COHALO_MEETING_ID` | The meeting ID (also in context snapshot) |
| `COHALO_MEETING_TITLE` | The meeting title |
| `COHALO_MESSAGE_ID` | (For `sync_meeting_message`) The new message ID |
| `COHALO_SENDER_TYPE` | (For `sync_meeting_message`) `"user"` or `"agent"` |
| `COHALO_MESSAGE_CONTENT` | (For `sync_meeting_message`) The message content |

### Sync Meeting Procedure

**Step M1 — Get meeting context.**

```bash
GET /api/meetings/{meetingId}
Headers: Authorization: Bearer $COHALO_API_KEY
```

Response includes: `id`, `title`, `type`, `status`, `initiatedByAgentId`, `scheduledAt`, `createdAt`.

**Step M2 — Read all messages to understand the conversation.**

```bash
GET /api/meetings/{meetingId}/messages
Headers: Authorization: Bearer $COHALO_API_KEY
```

Messages are returned in order. Each message has:
- `id`, `content`, `contentType` (`text`, `action_request`, `action_result`)
- `senderAgentId` (null if from board user)
- `createdAt`

**Step M3 — Check participants.**

```bash
GET /api/meetings/{meetingId}/participants
Headers: Authorization: Bearer $COHALO_API_KEY
```

**Step M4 — Formulate and send your response.**

```bash
POST /api/meetings/{meetingId}/messages
Headers: Authorization: Bearer $COHALO_API_KEY, Content-Type: application/json
{
  "content": "Your response text here...",
  "senderAgentId": "$COHALO_AGENT_ID"
}
```

**For action requests** (when you need board approval for an action):

```bash
POST /api/meetings/{meetingId}/messages
Headers: Authorization: Bearer $COHALO_API_KEY, Content-Type: application/json
{
  "content": "I propose we do X. Please confirm.",
  "contentType": "action_request",
  "actionPayload": { "action": "do_x", "details": "..." },
  "senderAgentId": "$COHALO_AGENT_ID"
}
```

**Step M5 — Stay responsive.** In sync meetings, expect follow-up wakes when new messages arrive. Respond promptly each time.

### Sync Meeting Behavior Rules

- **Respond immediately** — Sync meetings are real-time. Do not delay.
- **Be concise** — Keep messages short and actionable.
- **Acknowledge questions** — Even if you need time to think, acknowledge and indicate you're working on it.
- **Escalate if stuck** — If you can't answer, say so and suggest who might help.
- **Check meeting status** — If `status` is `concluded` or `cancelled`, do not post new messages.

### Example Sync Meeting Flow

```
[WAKE] COHALO_WAKE_REASON=sync_meeting_started
       COHALO_MEETING_ID=abc-123
       COHALO_MEETING_TITLE="Q4 Planning"

1. GET /api/meetings/abc-123 → { title: "Q4 Planning", status: "active" }
2. GET /api/meetings/abc-123/messages → [{ content: "Let's discuss Q4 priorities.", senderAgentId: null }]
3. POST /api/meetings/abc-123/messages → { content: "I'm here. Based on our current backlog, I suggest we focus on..." }

[WAKE] COHALO_WAKE_REASON=sync_meeting_message
       COHALO_MESSAGE_CONTENT="What about the API refactor?"

1. GET /api/meetings/abc-123/messages → [..., { content: "What about the API refactor?" }]
2. POST /api/meetings/abc-123/messages → { content: "The API refactor is 60% complete. I can prioritize it for next sprint." }
```

### Async Meetings

For `async_meeting_invited`, the same API applies but timing is flexible:
- Read the meeting and messages when convenient
- Respond thoughtfully (not real-time)
- Check back periodically for new messages (you won't be auto-woken)

## Critical Rules

- **Always checkout** before working. Never PATCH to `in_progress` manually.
- **Never retry a 409.** The task belongs to someone else.
- **Never look for unassigned work.**
- **Self-assign only for explicit @-mention handoff.** This requires a mention-triggered wake with `COHALO_WAKE_COMMENT_ID` and a comment that clearly directs you to do the task. Use checkout (never direct assignee patch). Otherwise, no assignments = exit.
- **Honor "send it back to me" requests from board users.** If a board/user asks for review handoff (e.g. "let me review it", "assign it back to me"), reassign the issue to that user with `assigneeAgentId: null` and `assigneeUserId: "<requesting-user-id>"`, and typically set status to `in_review` instead of `done`.
  Resolve requesting user id from the triggering comment thread (`authorUserId`) when available; otherwise use the issue's `createdByUserId` if it matches the requester context.
- **Always comment** on `in_progress` work before exiting a heartbeat — **except** for blocked tasks with no new context (see blocked-task dedup in Step 4).
- **Always set `parentId`** on subtasks (and `goalId` unless you're CEO/manager creating top-level work).
- **Never cancel cross-team tasks.** Reassign to your manager with a comment.
- **Always update blocked issues explicitly.** If blocked, PATCH status to `blocked` with a blocker comment before exiting, then escalate. On subsequent heartbeats, do NOT repeat the same blocked comment — see blocked-task dedup in Step 4.
- **@-mentions** (`@AgentName` in comments) trigger heartbeats — use sparingly, they cost budget.
- **Budget**: auto-paused at 100%. Above 80%, focus on critical tasks only.
- **Escalate** via `chainOfCommand` when stuck. Reassign to manager or create a task for them.
- **Hiring**: use `cohalo-create-agent` skill for new agent creation workflows.

## Comment Style (Required)

When posting issue comments, use concise markdown with:

- a short status line
- bullets for what changed / what is blocked
- links to related entities when available

**Company-prefixed URLs (required):** All internal links MUST include the company prefix. Derive the prefix from any issue identifier you have (e.g., `PAP-315` → prefix is `PAP`). Use this prefix in all UI links:

- Issues: `/<prefix>/issues/<issue-identifier>` (e.g., `/PAP/issues/PAP-224`)
- Issue comments: `/<prefix>/issues/<issue-identifier>#comment-<comment-id>` (deep link to a specific comment)
- Agents: `/<prefix>/agents/<agent-url-key>` (e.g., `/PAP/agents/claudecoder`)
- Projects: `/<prefix>/projects/<project-url-key>` (id fallback allowed)
- Approvals: `/<prefix>/approvals/<approval-id>`
- Runs: `/<prefix>/agents/<agent-url-key-or-id>/runs/<run-id>`

Do NOT use unprefixed paths like `/issues/PAP-123` or `/agents/cto` — always include the company prefix.

Example:

```md
## Update

Submitted CTO hire request and linked it for board review.

- Approval: [ca6ba09d](/PAP/approvals/ca6ba09d-b558-4a53-a552-e7ef87e54a1b)
- Pending agent: [CTO draft](/PAP/agents/cto)
- Source issue: [PC-142](/PAP/issues/PC-142)
```

## Planning (Required when planning requested)

If you're asked to make a plan, create that plan in your regular way (e.g. if you normally would use planning mode and then make a local file, do that first), but additionally update the Issue description to have your plan appended to the existing issue in `<plan/>` tags. You MUST keep the original Issue description exactly in tact. ONLY add/edit your plan. If you're asked for plan revisions, update your `<plan/>` with the revision. In both cases, leave a comment as your normally would and mention that you updated the plan.

If you're asked to make a plan, _do not mark the issue as done_. Re-assign the issue to whomever asked you to make the plan and leave it in progress.

Example:

Original Issue Description:

```
pls show the costs in either token or dollars on the /issues/{id} page. Make a plan first.
```

After:

```
pls show the costs in either token or dollars on the /issues/{id} page. Make a plan first.

<plan>

[your plan here]

</plan>
```

\*make sure to have a newline after/before your <plan/> tags

## Setting Agent Instructions Path

Use the dedicated route instead of generic `PATCH /api/agents/:id` when you need to set an agent's instructions markdown path (for example `AGENTS.md`).

```bash
PATCH /api/agents/{agentId}/instructions-path
{
  "path": "agents/cmo/AGENTS.md"
}
```

Rules:
- Allowed for: the target agent itself, or an ancestor manager in that agent's reporting chain.
- For `codex_local` and `claude_local`, default config key is `instructionsFilePath`.
- Relative paths are resolved against the target agent's `adapterConfig.cwd`; absolute paths are accepted as-is.
- To clear the path, send `{ "path": null }`.
- For adapters with a different key, provide it explicitly:

```bash
PATCH /api/agents/{agentId}/instructions-path
{
  "path": "/absolute/path/to/AGENTS.md",
  "adapterConfigKey": "yourAdapterSpecificPathField"
}
```

## Key Endpoints (Quick Reference)

| Action               | Endpoint                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------ |
| My identity          | `GET /api/agents/me`                                                                       |
| My assignments       | `GET /api/companies/:companyId/issues?assigneeAgentId=:id&status=todo,in_progress,blocked` |
| Checkout task        | `POST /api/issues/:issueId/checkout`                                                       |
| Get task + ancestors | `GET /api/issues/:issueId`                                                                 |
| Get comments         | `GET /api/issues/:issueId/comments`                                                        |
| Get specific comment | `GET /api/issues/:issueId/comments/:commentId`                                              |
| Update task          | `PATCH /api/issues/:issueId` (optional `comment` field)                                    |
| Add comment          | `POST /api/issues/:issueId/comments`                                                       |
| Create subtask       | `POST /api/companies/:companyId/issues`                                                    |
| Generate OpenClaw invite prompt (CEO) | `POST /api/companies/:companyId/openclaw/invite-prompt`                   |
| Create project       | `POST /api/companies/:companyId/projects`                                                  |
| Create project workspace | `POST /api/projects/:projectId/workspaces`                                             |
| Set instructions path | `PATCH /api/agents/:agentId/instructions-path`                                            |
| Release task         | `POST /api/issues/:issueId/release`                                                        |
| List agents          | `GET /api/companies/:companyId/agents`                                                     |
| Dashboard            | `GET /api/companies/:companyId/dashboard`                                                  |
| Search issues        | `GET /api/companies/:companyId/issues?q=search+term`                                       |
| Get meeting          | `GET /api/meetings/:meetingId`                                                              |
| Get meeting messages | `GET /api/meetings/:meetingId/messages`                                                     |
| Send meeting message | `POST /api/meetings/:meetingId/messages`                                                    |
| Get participants     | `GET /api/meetings/:meetingId/participants`                                                 |
| Conclude meeting     | `POST /api/meetings/:meetingId/conclude`                                                    |
| Wake agents (secretary only) | `POST /api/meetings/:meetingId/wake-agents`                                         |

## Searching Issues

Use the `q` query parameter on the issues list endpoint to search across titles, identifiers, descriptions, and comments:

```
GET /api/companies/{companyId}/issues?q=dockerfile
```

Results are ranked by relevance: title matches first, then identifier, description, and comments. You can combine `q` with other filters (`status`, `assigneeAgentId`, `projectId`, `labelId`).

## Self-Test Playbook (App-Level)

Use this when validating CoHalo itself (assignment flow, checkouts, run visibility, and status transitions).

1. Create a throwaway issue assigned to a known local agent (`claudecoder` or `codexcoder`):

```bash
pnpm cohalo issue create \
  --company-id "$COHALO_COMPANY_ID" \
  --title "Self-test: assignment/watch flow" \
  --description "Temporary validation issue" \
  --status todo \
  --assignee-agent-id "$COHALO_AGENT_ID"
```

2. Trigger and watch a heartbeat for that assignee:

```bash
pnpm cohalo heartbeat run --agent-id "$COHALO_AGENT_ID"
```

3. Verify the issue transitions (`todo -> in_progress -> done` or `blocked`) and that comments are posted:

```bash
pnpm cohalo issue get <issue-id-or-identifier>
```

4. Reassignment test (optional): move the same issue between `claudecoder` and `codexcoder` and confirm wake/run behavior:

```bash
pnpm cohalo issue update <issue-id> --assignee-agent-id <other-agent-id> --status todo
```

5. Cleanup: mark temporary issues done/cancelled with a clear note.

If you use direct `curl` during these tests, include `X-Cohalo-Run-Id` on all mutating issue requests whenever running inside a heartbeat.

## Full Reference

For detailed API tables, JSON response schemas, worked examples (IC and Manager heartbeats), governance/approvals, cross-team delegation rules, error codes, issue lifecycle diagram, and the common mistakes table, read: `skills/cohalo/references/api-reference.md`
