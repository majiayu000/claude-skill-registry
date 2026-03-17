---
name: linear-agent-api
description: Linear Agent API expertise - sessions, activities, signals, and best practices. Use when working with Linear agent integration, verifying dialogue population, or implementing two-way communication.
---

# Linear Agent API Skill

Comprehensive reference for Linear's Agent API, following the [Agent Interaction Guidelines (AIG)](https://linear.app/developers/aig).

## When to Use

- Verifying agent sessions are created correctly
- Checking activity streaming (thought, action, response)
- Implementing two-way communication (user input, stop signals)
- Debugging Linear integration issues

---

## Agent Session Lifecycle

Sessions track the lifecycle of an agent run:

| State | Meaning |
|-------|---------|
| `pending` | Session created, waiting for agent |
| `active` | Agent is working |
| `awaitingInput` | Agent needs user input |
| `error` | Something went wrong |
| `complete` | Work finished |

**Sessions are created automatically** when an agent is @mentioned or assigned as delegate.

---

## Agent Activity Types

| Type | Purpose | Who Creates |
|------|---------|-------------|
| `thought` | Agent reasoning, progress updates | Agent |
| `action` | Tool invocations (with optional `result`) | Agent |
| `elicitation` | Request user input or clarification | Agent |
| `response` | Final completion message | Agent |
| `error` | Report failure | Agent |
| `prompt` | User follow-up message | Human |

### Activity Payloads

```json
// thought - Agent thinking
{ 
  "content": { 
    "type": "thought", 
    "body": "Analyzing the codebase structure..." 
  } 
}

// action - Tool call
{ 
  "content": { 
    "type": "action", 
    "action": "edit_file", 
    "parameter": "src/main.rs" 
  } 
}

// action with result
{ 
  "content": { 
    "type": "action", 
    "action": "run_tests", 
    "result": "All 42 tests passed" 
  } 
}

// elicitation - Request input
{ 
  "content": { 
    "type": "elicitation", 
    "body": "Which database should I use?" 
  } 
}

// response - Completion
{ 
  "content": { 
    "type": "response", 
    "body": "Implementation complete. PR #123 created." 
  } 
}

// error - Failure
{ 
  "content": { 
    "type": "error", 
    "body": "Build failed: missing dependency" 
  } 
}
```

### Ephemeral Activities

Activities can be marked `ephemeral: true` for temporary status messages that get replaced by the next activity. Only `thought` and `action` types support this.

---

## Signals (Two-Way Communication)

### Human-to-Agent Signals

#### `stop` Signal

When user clicks "Send stop request" in Linear, agent receives a `prompt` activity with `signal: "stop"`.

**Agent MUST:**
1. **Halt immediately** - No further code changes or API calls
2. **Emit final activity** - `response` or `error` confirming stop
3. **Report current state** - What was completed, what remains

**CTO Implementation**: The `status-sync.rs` sidecar detects `signal: "stop"` in polled activities and triggers graceful shutdown via `/stop` endpoint.

### Agent-to-Human Signals

#### `auth` Signal

Used with `elicitation` to request account linking:

```json
{
  "content": { "type": "elicitation", "body": "Please authenticate" },
  "signal": "auth",
  "signalMetadata": {
    "url": "https://auth.example.com/oauth",
    "providerName": "GitHub"
  }
}
```

#### `select` Signal

Used with `elicitation` to present multiple choice options:

```json
{
  "content": { "type": "elicitation", "body": "Which repository?" },
  "signal": "select",
  "signalMetadata": {
    "options": [
      { "value": "5dlabs/cto" },
      { "value": "5dlabs/alertub" }
    ]
  }
}
```

---

## Agent Plans (Checklists)

Agents can provide session-level task checklists:

```json
{
  "plan": [
    { "content": "Parse PRD document", "status": "completed" },
    { "content": "Generate task breakdown", "status": "inProgress" },
    { "content": "Create Linear issues", "status": "pending" }
  ]
}
```

Status values: `pending`, `inProgress`, `completed`, `canceled`

**Note**: Plan updates replace the entire array, not individual items.

---

## Best Practices

### 1. First Response Within 10 Seconds

Upon receiving `created` webhook, agent MUST emit a `thought` activity within **10 seconds** or be shown as **unresponsive**.

### 2. Follow-up Activities Within 30 Minutes

After first response, activities can be sent for up to **30 minutes** before session is **stale**.

### 3. Delegate vs Assignee

- **Delegate** = The agent working on the issue
- **Assignee** = The human responsible (ownership)

Agents should set themselves as `delegate`, not `assignee`.

### 4. Status Updates

When starting work, move issue to first "started" status if not already there.

### 5. Completion

When work complete, emit `response` activity. If user action needed, emit `elicitation` or `error`.

---

## GraphQL Queries

### Get Session Activities

```graphql
query AgentSession($agentSessionId: String!) {
  agentSession(id: $agentSessionId) {
    id
    state
    createdAt
    activities {
      edges {
        node {
          updatedAt
          content {
            ... on AgentActivityThoughtContent { body }
            ... on AgentActivityActionContent { action parameter result }
            ... on AgentActivityElicitationContent { body }
            ... on AgentActivityResponseContent { body }
            ... on AgentActivityErrorContent { body }
            ... on AgentActivityPromptContent { body }
          }
        }
      }
    }
  }
}
```

### Get Team Started Statuses

```graphql
query TeamStartedStatuses($teamId: String!) {
  team(id: $teamId) {
    states(filter: { type: { eq: "started" } }) {
      nodes {
        id
        name
        position
      }
    }
  }
}
```

---

## CTO Status-Sync Implementation

The `status-sync.rs` sidecar implements:

| Function | Purpose |
|----------|---------|
| `emit_thought()` | Progress updates |
| `emit_ephemeral_thought()` | Transient status |
| `emit_action()` | Tool invocations |
| `emit_action_complete()` | Tool results |
| `emit_error()` | Error reporting |
| `emit_response()` | Final completion |
| `update_plan()` | Checklist updates |
| `get_session_activities()` | Poll for user input |

**Input Polling**: The `input_poll_task` periodically calls `get_session_activities()` to detect:
- New `prompt` activities from users
- `signal: "stop"` requests

---

## Webhook Events

| Event | Action | Description |
|-------|--------|-------------|
| `AgentSessionEvent` | `created` | Agent mentioned/delegated |
| `AgentSessionEvent` | `prompted` | User sent follow-up message |
| `AppUserNotification` | `issueAssignedToYou` | Issue delegated to agent |
| `AppUserNotification` | `issueUnassignedFromYou` | Agent removed from issue |

---

## Reference Documentation

- [Linear AIG](https://linear.app/developers/aig) - Agent Interaction Guidelines
- [Linear Getting Started](https://linear.app/developers/agents) - Agent setup
- [Linear Developing Interaction](https://linear.app/developers/agent-interaction) - Activity types
- [Linear Best Practices](https://linear.app/developers/agent-best-practices) - Recommendations
- [Linear Signals](https://linear.app/developers/agent-signals) - Two-way communication
- [CTO Linear Integration](docs/linear-integration-workflow.md) - CTO-specific implementation
