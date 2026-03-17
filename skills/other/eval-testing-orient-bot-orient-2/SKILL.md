---
name: eval-testing
description: Develop and run agent behavior evaluations. Use this skill when asked to "write evals", "test agent behavior", "create eval cases", "run evals", "add eval tests", "test tool selection", "verify agent responses", or when developing tests for agents. Covers YAML eval case creation, assertion types, mock configuration, multi-model matrix testing, and LLM-as-judge scoring.
---

# Agent Evaluation Testing

System for testing multi-agent behavior consistency across prompts, tools, skills, models, and agent configs.

## Quick Reference - Commands

```bash
# Run all evals with default model
npm run eval

# Run with fast model (Haiku)
npm run eval:fast

# Run with all models (Sonnet, Opus, Haiku)
npm run eval:full

# CI mode (exit 1 on failure)
npm run eval:ci

# Filter by type
npm run eval -- --type tool_selection
npm run eval -- --type response_quality
npm run eval -- --type skill_invocation
npm run eval -- --type multi_step_workflow

# Filter by agent
npm run eval -- --agent pm-assistant
npm run eval -- --agent communicator

# Filter by pattern
npm run eval -- --pattern "jira-*"

# Run via Vitest
npm run test:eval
```

## Directory Structure

```
evals/
├── config/
│   └── models.yaml           # Model matrix definitions
├── schemas/
│   └── eval-schema.yaml      # JSON Schema for validation
├── tool-selection/           # Tool selection evals
├── response-quality/         # Response quality evals
├── skill-invocation/         # Skill activation evals
└── multi-step/               # Workflow evals
```

## Eval Types

| Type                  | Purpose                         | Key Assertions                                        |
| --------------------- | ------------------------------- | ----------------------------------------------------- |
| `tool_selection`      | Verify correct tools are called | `tool_called`, `tool_not_called`                      |
| `response_quality`    | Check response content          | `response_mentions`, `response_matches`, LLM-as-judge |
| `skill_invocation`    | Test skill activation           | `skill_activated`                                     |
| `multi_step_workflow` | Multi-step sequences            | `workflow_completed`                                  |

## YAML Eval Case Schema

```yaml
name: unique-eval-name
description: Human-readable description
type: tool_selection # tool_selection | response_quality | skill_invocation | multi_step_workflow
agent: pm-assistant # Agent ID to test

# Optional context
context:
  platform: slack # slack | whatsapp | opencode | cursor

# User input
input:
  prompt: 'Check for blocked tickets'
  conversationHistory: # Optional prior messages
    - role: user
      content: 'Previous message'

# Mock external service responses
mocks:
  jira:
    ai_first_get_blockers:
      response:
        count: 2
        issues: [...]
      error: null # Optional error to simulate
      delay: 100 # Optional delay in ms
  slack:
    ai_first_slack_send_message:
      response:
        success: true
        ts: '1705670400.000001'

# Expected behavior
expect:
  tool_calls:
    required:
      - name: ai_first_get_blockers
        arguments: # Optional partial match
          status: 'Blocked'
    forbidden:
      - ai_first_get_all_issues
    order: strict # strict | any

  skills:
    activated:
      - jira-management
    content_used:
      - pattern: 'blocker'

  workflow: # For multi_step_workflow type
    steps:
      - name: check_blockers
        tools: [ai_first_get_blockers]
      - name: notify_slack
        depends_on: check_blockers
        tools: [ai_first_slack_send_message]

  assertions:
    - type: response_mentions
      values: ['blocked', 'PROJ-123']
    - type: response_matches
      pattern: 'blocked|waiting'

# LLM-as-judge scoring (optional)
scoring:
  llm_judge:
    enabled: true
    criteria:
      - name: accuracy
        description: 'Correctly identifies blockers'
        weight: 0.5
      - name: clarity
        description: 'Clear and concise response'
        weight: 0.5
    threshold: 0.7
    rubric: |
      Score 1.0: Excellent - all blockers identified, clear summary
      Score 0.7: Good - most blockers found, minor issues
      Score 0.4: Needs work - incomplete or unclear
      Score 0.0: Poor - wrong information
```

## Assertion Types

| Type                 | Purpose                        | Required Fields  |
| -------------------- | ------------------------------ | ---------------- |
| `tool_called`        | Verify tool was invoked        | `tool`           |
| `tool_not_called`    | Verify tool was NOT invoked    | `tool`           |
| `tool_arguments`     | Check tool arguments           | `tool`, `values` |
| `skill_activated`    | Verify skill loaded            | `skill`          |
| `response_mentions`  | Check response contains values | `values`         |
| `response_matches`   | Regex match on response        | `pattern`        |
| `workflow_completed` | Multi-step verification        | `steps`          |

## Mock Services

Available mock services: `jira`, `slack`, `google`, `whatsapp`

### Common Tool Mocks

**JIRA:**

- `ai_first_get_blockers`
- `ai_first_get_in_progress`
- `ai_first_get_all_issues`
- `ai_first_get_weekly_summary`
- `ai_first_jira_create_issue`

**Slack:**

- `ai_first_slack_send_message`
- `ai_first_slack_send_dm`
- `ai_first_slack_lookup_user_by_email`

**Google Slides:**

- `ai_first_slides_get_presentation`
- `ai_first_slides_duplicate_template`
- `ai_first_slides_update_slide_text`

**WhatsApp:**

- `ai_first_whatsapp_search_messages`
- `ai_first_whatsapp_get_chat_history`

## Examples by Type

### Tool Selection Eval

```yaml
name: jira-blockers-detection
description: Agent should use blockers tool when asked about blocked tickets
type: tool_selection
agent: pm-assistant

input:
  prompt: 'Are there any blocked tickets?'

mocks:
  jira:
    ai_first_get_blockers:
      response:
        count: 2
        issues:
          - key: PROJ-190
            summary: 'Waiting for API access'
            status: 'Blocked'
            blockedDays: 5

expect:
  tool_calls:
    required:
      - name: ai_first_get_blockers
    forbidden:
      - ai_first_get_all_issues
  assertions:
    - type: response_mentions
      values: ['PROJ-190', 'blocked']
```

### Response Quality Eval

```yaml
name: communicator-slack-format
description: Communicator should use Slack mrkdwn correctly
type: response_quality
agent: communicator

context:
  platform: slack

input:
  prompt: 'Format a standup: Yesterday I finished PROJ-150, today PROJ-151'

expect:
  assertions:
    - type: response_matches
      pattern: 'yesterday|today'

scoring:
  llm_judge:
    enabled: true
    criteria:
      - name: slack_formatting
        description: 'Uses *single asterisks* for bold, not **double**'
        weight: 0.5
      - name: structure
        description: 'Clear Yesterday/Today/Blockers format'
        weight: 0.5
    threshold: 0.7
```

### Multi-Step Workflow Eval

```yaml
name: weekly-report-workflow
description: Agent should gather data and update slides
type: multi_step_workflow
agent: pm-assistant

input:
  prompt: 'Update the weekly presentation with the latest sprint data'

mocks:
  jira:
    ai_first_get_weekly_summary:
      response:
        sprint: 'Sprint 12'
        velocity: 42
        completedStories: 8
  google:
    ai_first_slides_duplicate_template:
      response:
        slideId: 'slide_123'
    ai_first_slides_update_slide_text:
      response:
        success: true

expect:
  workflow:
    steps:
      - name: gather_data
        tools: [ai_first_get_weekly_summary]
      - name: create_slide
        depends_on: gather_data
        tools: [ai_first_slides_duplicate_template]
      - name: update_content
        depends_on: create_slide
        tools: [ai_first_slides_update_slide_text]
  assertions:
    - type: workflow_completed
      steps: [gather_data, create_slide, update_content]
```

## Model Matrix Configuration

Edit `evals/config/models.yaml`:

```yaml
models:
  default:
    - anthropic/claude-sonnet-4-20250514
  full_matrix:
    - anthropic/claude-sonnet-4-20250514
    - anthropic/claude-opus-4-20250514
    - anthropic/claude-haiku-3-5-20241022
  fast:
    - anthropic/claude-haiku-3-5-20241022
```

## LLM-as-Judge Setup

Requires `ANTHROPIC_API_KEY` environment variable set in `.env`. The CLI automatically loads dotenv, so ensure your API key is configured:

```bash
# In .env file
ANTHROPIC_API_KEY=sk-ant-api03-...
```

The judge uses Claude to evaluate response quality against defined criteria.

**Criteria weights must sum to 1.0.**

```yaml
scoring:
  llm_judge:
    enabled: true
    criteria:
      - name: accuracy
        description: 'Information is correct'
        weight: 0.4
      - name: completeness
        description: 'All requested info included'
        weight: 0.3
      - name: clarity
        description: 'Easy to understand'
        weight: 0.3
    threshold: 0.7 # Minimum score to pass
```

## Creating New Evals

1. Choose appropriate type based on what you're testing
2. Create YAML file in correct subdirectory (`evals/<type>/`)
3. Define mocks for any external services
4. Add assertions for expected behavior
5. Optionally add LLM-as-judge for quality scoring
6. Run with `npm run eval -- --pattern "your-eval-name"`

## Debugging Failed Evals

Check the JSON output in `eval-results/` for:

- `executionTrace.toolCalls` - what tools were actually called
- `executionTrace.skillActivations` - which skills loaded
- `executionTrace.responseText` - full response text
- `assertions` - which assertions failed and why
- `judgeScore.criteria` - per-criterion scores with reasoning

## Key Files

| File                             | Purpose                                  |
| -------------------------------- | ---------------------------------------- |
| `src/eval/types.ts`              | Type definitions                         |
| `src/eval/runner/index.ts`       | Main runner                              |
| `src/eval/runner/assertions.ts`  | Assertion logic                          |
| `src/eval/judge/index.ts`        | LLM-as-judge                             |
| `src/eval/mocks/registry.ts`     | Mock service registry                    |
| `src/eval/cli.ts`                | CLI interface                            |
| `src/services/openCodeClient.ts` | OpenCode API client for agent invocation |

## How Tool Tracking Works

Tool calls are extracted from the OpenCode session history, not the immediate response. The flow is:

1. Agent receives prompt via `POST /chat`
2. OpenCode returns response with `step-start`, `reasoning`, `text`, `step-finish` parts
3. **Tool calls appear only in session history** (not in immediate response)
4. After response completes, the eval runner fetches `GET /session/{id}/message`
5. Tool parts have `type: "tool"` with the tool name in the `tool` field
6. Tool names are prefixed with MCP server name (e.g., `orienter_ai_first_get_blockers`)
7. The prefix is stripped to get the canonical tool name (`ai_first_get_blockers`)

This is why mocks in eval YAML files don't directly return data to the agent - the agent calls real APIs through OpenCode, and the eval system verifies which tools were called.

## Best Practices for Assertions

### Test Behavior, Not Mock Data

Since agents call real APIs (not mocks), assertions should test behavior patterns rather than specific mock values:

```yaml
# BAD - Tests specific mock IDs that won't exist in real API
assertions:
  - type: response_mentions
    values: ["PROJ-123", "PROJ-124"]

# GOOD - Tests that agent discusses the right concepts
assertions:
  - type: response_matches
    pattern: "block|stuck|impediment|waiting"
```

### Use Flexible Regex Patterns

Match word stems to catch variations:

```yaml
# Matches: "completed", "complete", "completion", "completing"
pattern: "complet|finish|done"

# Matches: "notification", "notified", "notify", "notifying"
pattern: "notif|sent|posted|messag"
```

### One Behavior Per Assertion

Keep assertions focused on single behaviors for clearer failure diagnostics:

```yaml
assertions:
  # Tests blocker detection
  - type: response_matches
    pattern: 'block|stuck|waiting'

  # Tests notification action (separate assertion)
  - type: response_matches
    pattern: 'sent|posted|notif'
```

### Use `tool_calls.required` Over Assertions

For tool selection tests, prefer the structured `tool_calls` section:

```yaml
# GOOD - Clear, structured
expect:
  tool_calls:
    required:
      - name: ai_first_get_blockers

# Less preferred - assertion-based
expect:
  assertions:
    - type: tool_called
      tool: ai_first_get_blockers
```
