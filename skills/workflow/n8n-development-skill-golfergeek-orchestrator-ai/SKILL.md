---
name: N8N Development
description: Create and manage N8N workflows in Orchestrator AI. Use Helper LLM pattern for all LLM calls, configure webhook status tracking, handle API responses. CRITICAL: All workflows using Helper LLM must include required parameters (taskId, conversationId, userId, statusWebhook, stepName, sequence, totalSteps). Status webhook URL must read from environment variables.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# N8N Development Skill

**CRITICAL**: All N8N workflows that use Helper LLM MUST include required parameters. Status webhook URL MUST read from environment variables (never hardcoded).

## When to Use This Skill

Use this skill when:
- Creating new N8N workflows
- Calling Helper LLM from workflows
- Configuring webhook status tracking
- Handling API responses from workflows
- Wrapping N8N workflows as API agents
- Setting up workflow parameters

## The Helper LLM Pattern

**Workflow ID**: `9jxl03jCcqg17oOy`  
**Name**: "Helper: LLM Task"

This is Orchestrator AI's standard building block for all LLM calls in N8N workflows. It provides:
- Multi-provider support (OpenAI, Anthropic, Ollama)
- Status tracking via webhooks
- Normalized output format
- Error handling

## How to Call Helper LLM from a Workflow

### Step 1: Extract Parameters from Webhook

When your workflow receives a webhook, extract all required parameters:

```json
{
  "taskId": "{{ $json.body.taskId }}",
  "conversationId": "{{ $json.body.conversationId }}",
  "userId": "{{ $json.body.userId }}",
  "statusWebhook": "={{ $json.body.statusWebhook || process.env.API_BASE_URL + '/webhooks/status' }}",
  "provider": "={{ $json.body.provider || 'openai' }}",
  "model": "={{ $json.body.model || 'gpt-4' }}",
  "announcement": "={{ $json.body.announcement }}"
}
```

### Step 2: Prepare Parameters for Helper LLM

Create a "Set" node that prepares all parameters for Helper LLM:

**Example from Marketing Swarm workflow** (`storage/snapshots/n8n/marketing-swarm-flexible-llm.json`):

```130:189:storage/snapshots/n8n/marketing-swarm-flexible-llm.json
            {
              "name": "announcement",
              "type": "string",
              "value": "={{ $json.body.announcement }}",
              "id": "37100b7a-3727-4855-824f-2725e80d0440"
            },
            {
              "name": "taskId",
              "type": "string",
              "value": "={{ $json.body.taskId }}",
              "id": "c26c5743-8792-41fc-807a-65cc83a14ca1"
            },
            {
              "name": "conversationId",
              "type": "string",
              "value": "={{ $json.body.conversationId }}",
              "id": "f95fd7fb-df93-4dd3-8450-2830ce517fcd"
            },
            {
              "name": "userId",
              "type": "string",
              "value": "={{ $json.body.userId }}",
              "id": "56763026-b467-4e4b-b3fb-7842b63c1caf"
            },
            {
              "name": "statusWebhook",
              "type": "string",
              "value": "={{ $json.body.statusWebHook }}",
              "id": "5b5c4d3a-93bf-4f2d-aadf-e31b89a41079"
            },
            {
              "id": "a95859db-69f5-46c2-a895-883b3659deac",
              "name": "systemMessage",
              "value": "You are a social media content strategist. Create engaging social media posts (NOT blog posts) for multiple platforms: Twitter/X (280 chars with hashtags), LinkedIn (professional tone, 1300 chars max), and Facebook (conversational, 500 chars). Focus on hooks, engagement, and platform-specific best practices. Include relevant hashtags and emojis where appropriate.",
              "type": "string"
            },
            {
              "id": "5c7b8969-c60a-42df-b9dc-84849e0f10a2",
              "name": "userMessage",
              "value": "={{ $json.body.announcement }}",
              "type": "string"
            },
            {
              "id": "7b8664d1-0f50-4a1d-ad16-3867967041f8",
              "name": "stepName",
              "value": "Create Social Media",
              "type": "string"
            },
            {
              "id": "291d34dd-2292-4cea-9432-3ae16b054053",
              "name": "sequence",
              "value": "3",
              "type": "string"
            },
            {
              "id": "8cc15d2f-cab2-4691-b5ec-954ded016211",
              "name": "totalSteps",
              "value": "3",
              "type": "string"
            }
```

**Critical Parameters:**

| Parameter | Type | Required | Example | Description |
|-----------|------|----------|---------|-------------|
| `taskId` | string | ✅ Yes | `"uuid"` | Task identifier for tracking |
| `conversationId` | string | ✅ Yes | `"uuid"` | Conversation context |
| `userId` | string | ✅ Yes | `"uuid"` | User identifier |
| `statusWebhook` | string | ✅ Yes* | `"${API_BASE_URL}/webhooks/status"` | Webhook URL (from env) |
| `stepName` | string | ✅ Yes | `"Create Social Media"` | Descriptive step name |
| `sequence` | number | ✅ Yes | `3` | Step number (1-based) |
| `totalSteps` | number | ✅ Yes | `3` | Total steps in workflow |
| `userMessage` | string | ✅ Yes | `"Write a blog post about..."` | The prompt/message |
| `systemMessage` | string | ❌ No | `"You are an expert..."` | System prompt |
| `provider` | string | ❌ No | `"openai"` | LLM provider |
| `model` | string | ❌ No | `"gpt-4"` | Model name |
| `temperature` | number | ❌ No | `0.7` | Temperature (0.0-1.0) |
| `maxTokens` | number | ❌ No | `1000` | Max tokens |

**Note**: `statusWebhook` is REQUIRED if you want status tracking to work.

### Step 3: Call Helper LLM via Execute Workflow Node

Configure the "Execute Workflow" node:

```json
{
  "source": "database",
  "workflowId": "9jxl03jCcqg17oOy",
  "fieldMapping": {
    "fields": [
      { "name": "taskId", "value": "={{ $json.taskId }}" },
      { "name": "conversationId", "value": "={{ $json.conversationId }}" },
      { "name": "userId", "value": "={{ $json.userId }}" },
      { "name": "statusWebhook", "value": "={{ $json.statusWebhook }}" },
      { "name": "stepName", "value": "={{ $json.stepName }}" },
      { "name": "sequence", "value": "={{ $json.sequence }}" },
      { "name": "totalSteps", "value": "={{ $json.totalSteps }}" },
      { "name": "userMessage", "value": "={{ $json.userMessage }}" },
      { "name": "systemMessage", "value": "={{ $json.systemMessage }}" },
      { "name": "provider", "value": "={{ $json.provider || 'openai' }}" },
      { "name": "model", "value": "={{ $json.model || 'gpt-4' }}" },
      { "name": "temperature", "value": "={{ $json.temperature || 0.7 }}" },
      { "name": "maxTokens", "value": "={{ $json.maxTokens || 1000 }}" }
    ]
  }
}
```

## API Call: How Workflows Are Called

### From API Agent Configuration

When an API agent wraps an N8N workflow, here's the agent configuration from `storage/snapshots/agents/demo_marketing_swarm_n8n.json`:

```11:11:storage/snapshots/agents/demo_marketing_swarm_n8n.json
  "yaml": "\n{\n    \"metadata\": {\n        \"name\": \"marketing-swarm-n8n\",\n        \"displayName\": \"Marketing Swarm N8N\",\n        \"description\": \"API agent that calls n8n webhook for marketing campaign swarm processing\",\n        \"version\": \"0.1.0\",\n        \"type\": \"api\"\n    },\n    \"configuration\": {\n        \"api\": {\n            \"endpoint\": \"http://localhost:5678/webhook/marketing-swarm-flexible\",\n            \"method\": \"POST\",\n            \"headers\": {\n                \"Content-Type\": \"application/json\"\n            },\n            \"body\": {\n                \"taskId\": \"{{taskId}}\",\n                \"conversationId\": \"{{conversationId}}\",\n                \"userId\": \"{{userId}}\",\n                \"announcement\": \"{{userMessage}}\",\n                \"statusWebhook\": \"http://host.docker.internal:7100/webhooks/status\",\n                \"provider\": \"{{payload.provider}}\",\n                \"model\": \"{{payload.model}}\"\n            },\n            \"authentication\": {\n                \"type\": \"none\"\n            },\n            \"response_mapping\": {\n                \"status_field\": \"status\",\n                \"result_field\": \"payload\"\n            },\n            \"timeout\": 120000\n        },\n        \"deliverable\": {\n            \"format\": \"markdown\",\n            \"type\": \"marketing-campaign\"\n        },\n        \"execution_capabilities\": {\n            \"supports_converse\": false,\n            \"supports_plan\": false,\n            \"supports_build\": true\n        }\n    }\n}\n",
```

**Key Points:**
- Endpoint: `http://localhost:5678/webhook/marketing-swarm-flexible` (N8N webhook URL)
- Method: `POST`
- Body uses template variables: `{{taskId}}`, `{{conversationId}}`, `{{userMessage}}`, etc.
- **CRITICAL**: `statusWebhook` is hardcoded here but should read from env (will be fixed)

### Request Body Sent to N8N

When the API agent calls the N8N webhook, the request body looks like:

```json
{
  "taskId": "123e4567-e89b-12d3-a456-426614174000",
  "conversationId": "123e4567-e89b-12d3-a456-426614174001",
  "userId": "123e4567-e89b-12d3-a456-426614174002",
  "announcement": "We're launching our new AI agent platform!",
  "statusWebhook": "http://host.docker.internal:7100/webhooks/status",
  "provider": "openai",
  "model": "gpt-4"
}
```

### Status Webhook URL Configuration

**❌ WRONG - Hardcoded:**
```json
{
  "statusWebhook": "http://host.docker.internal:7100/webhooks/status"
}
```

**✅ CORRECT - From Environment:**
```json
{
  "statusWebhook": "={{ process.env.API_BASE_URL || process.env.VITE_API_BASE_URL || 'http://host.docker.internal:7100' }}/webhooks/status"
}
```

**In API Agent YAML:**
```yaml
"statusWebhook": "{{env.API_BASE_URL}}/webhooks/status"
```

## Response Handling: What Helper LLM Returns

### Normalized Response Format

Helper LLM returns a **normalized format** regardless of provider:

```json
{
  "text": "LLM response content here...",
  "provider": "openai|ollama|anthropic",
  "model": "gpt-4|llama2|claude-3-sonnet-20240229",
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 456
  }
}
```

**Key Points:**
- ✅ All providers return the SAME format
- ✅ `text` contains the actual response
- ✅ `provider` and `model` identify what was used
- ✅ `usage` contains token counts (if available)

### Accessing Response in Workflow

After Helper LLM executes, access the response:

```json
{
  "result": "={{ $json.text }}",
  "provider": "={{ $json.provider }}",
  "model": "={{ $json.model }}",
  "tokens": "={{ $json.usage.prompt_tokens + $json.usage.completion_tokens }}"
}
```

### Example: Complete Workflow Response

When Marketing Swarm workflow completes, it returns:

```json
{
  "webPost": "Full blog post content...",
  "seoContent": "Meta tags, keywords, JSON-LD...",
  "socialMedia": "Twitter: ...\nLinkedIn: ...\nFacebook: ...",
  "status": "completed",
  "taskId": "123e4567-e89b-12d3-a456-426614174000",
  "conversationId": "123e4567-e89b-12d3-a456-426614174001"
}
```

## How API Agent Handles N8N Response

### Response Transformation

From `apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts`:

```422:441:apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts
    const end = Date.now();
    // Normalize content (apply response transform if configured)
    const content = this.extractApiResponseContent(api, res.data);
    const isOk = res.status >= 200 && res.status < 300;
    const response = {
      content,
      metadata:
```

The API agent runner:
1. Receives response from N8N webhook
2. Applies `response_transform` if configured (field extraction)
3. Formats as deliverable
4. Returns to caller

### Response Mapping Example

If API agent YAML has:
```yaml
"response_mapping": {
  "status_field": "status",
  "result_field": "payload"
}
```

Then:
- `status` field from N8N response → API response status
- `payload` field from N8N response → API response content

## Complete Example: Marketing Swarm Workflow

### 1. Webhook Receives Request

```json
POST http://localhost:5678/webhook/marketing-swarm-flexible
Content-Type: application/json

{
  "taskId": "uuid",
  "conversationId": "uuid",
  "userId": "uuid",
  "announcement": "We're launching our new AI agent platform!",
  "statusWebhook": "${API_BASE_URL}/webhooks/status",
  "provider": "openai",
  "model": "gpt-4"
}
```

### 2. Workflow Extracts Parameters

Three "Set" nodes prepare parameters for three Helper LLM calls:
- **Web Post** (sequence: 1, temperature: 0.7)
- **SEO Content** (sequence: 2, temperature: 0.5)
- **Social Media** (sequence: 3, temperature: 0.8)

### 3. Each Helper LLM Call

**Web Post Call:**
```json
{
  "workflowId": "9jxl03jCcqg17oOy",
  "fieldMapping": {
    "fields": [
      { "name": "taskId", "value": "={{ $json.taskId }}" },
      { "name": "conversationId", "value": "={{ $json.conversationId }}" },
      { "name": "userId", "value": "={{ $json.userId }}" },
      { "name": "statusWebhook", "value": "={{ $json.statusWebhook }}" },
      { "name": "stepName", "value": "Write Blog Post" },
      { "name": "sequence", "value": 1 },
      { "name": "totalSteps", "value": 3 },
      { "name": "userMessage", "value": "={{ $json.announcement }}" },
      { "name": "systemMessage", "value": "You are a brilliant blog post writer..." },
      { "name": "provider", "value": "={{ $json.provider }}" },
      { "name": "model", "value": "={{ $json.model }}" },
      { "name": "temperature", "value": 0.7 },
      { "name": "maxTokens", "value": 1000 }
    ]
  }
}
```

### 4. Helper LLM Returns Response

```json
{
  "text": "Full blog post content here...",
  "provider": "openai",
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 800
  }
}
```

### 5. Workflow Combines Results

```json
{
  "webPost": "Full blog post...",
  "seoContent": "SEO content...",
  "socialMedia": "Social media posts...",
  "status": "completed"
}
```

### 6. API Agent Returns to Caller

```json
{
  "success": true,
  "mode": "build",
  "payload": {
    "content": "Full blog post...\n\nSEO content...\n\nSocial media posts...",
    "metadata": {
      "provider": "external_api",
      "model": "n8n_workflow",
      "status": "completed"
    }
  }
}
```

## Status Webhook Format

### Start Status (Sent by Helper LLM)

```json
{
  "taskId": "uuid",
  "status": "running",
  "timestamp": "2025-01-12T10:00:00.000Z",
  "step": "Write Blog Post",
  "message": "Starting Write Blog Post",
  "sequence": 1,
  "totalSteps": 3,
  "conversationId": "uuid",
  "userId": "uuid"
}
```

### End Status (Sent by Helper LLM)

```json
{
  "taskId": "uuid",
  "status": "completed",
  "timestamp": "2025-01-12T10:01:00.000Z",
  "step": "Write Blog Post",
  "message": "Completed Write Blog Post",
  "sequence": 1,
  "totalSteps": 3,
  "conversationId": "uuid",
  "userId": "uuid"
}
```

## Temperature Guidelines

| Use Case | Temperature | Max Tokens | Example |
|----------|-------------|------------|---------|
| Factual/Analytical | `0.5` | `800` | SEO content, data analysis |
| General Purpose | `0.7` | `1000` | Blog posts, general content |
| Creative | `0.8` | `1200` | Social media, marketing copy |

## Common Mistakes

### ❌ Mistake 1: Missing Required Parameters

```json
// ❌ WRONG - Missing status tracking parameters
{
  "userMessage": "Write a blog post",
  "provider": "openai"
}
```

**Fix:** Include all required parameters:
```json
{
  "userMessage": "Write a blog post",
  "provider": "openai",
  "taskId": "uuid",
  "conversationId": "uuid",
  "userId": "uuid",
  "statusWebhook": "${API_BASE_URL}/webhooks/status",
  "stepName": "write_blog",
  "sequence": 1,
  "totalSteps": 1
}
```

### ❌ Mistake 2: Hardcoded Status Webhook

```json
// ❌ WRONG
{
  "statusWebhook": "http://host.docker.internal:7100/webhooks/status"
}
```

**Fix:** Read from environment:
```json
{
  "statusWebhook": "={{ process.env.API_BASE_URL + '/webhooks/status' }}"
}
```

### ❌ Mistake 3: Wrong Sequence Numbers

```json
// ❌ WRONG - Sequence starts at 0
{
  "sequence": 0,
  "totalSteps": 3
}
```

**Fix:** Sequence is 1-based:
```json
{
  "sequence": 1,
  "totalSteps": 3
}
```

### ❌ Mistake 4: Not Using Helper LLM

```json
// ❌ WRONG - Direct LLM API call
{
  "url": "https://api.openai.com/v1/chat/completions",
  "body": { ... }
}
```

**Fix:** Use Helper LLM workflow (`9jxl03jCcqg17oOy`)

## Checklist for N8N Workflows

When creating workflows that use Helper LLM:

- [ ] Webhook extracts all required parameters from `$json.body`
- [ ] Status webhook reads from environment (not hardcoded)
- [ ] All Helper LLM calls include: `taskId`, `conversationId`, `userId`, `statusWebhook`, `stepName`, `sequence`, `totalSteps`
- [ ] `stepName` is descriptive and unique
- [ ] `sequence` is 1-based and sequential
- [ ] `totalSteps` matches actual number of steps
- [ ] Helper LLM workflow ID is `9jxl03jCcqg17oOy`
- [ ] Response handling accesses `$json.text` for content
- [ ] Temperature set appropriately (0.5 factual, 0.7 general, 0.8 creative)
- [ ] Workflow returns normalized format

## Related Documentation

- **Parameters Reference**: [PARAMETERS.md](PARAMETERS.md) - Complete parameter documentation
- **Helper LLM Pattern**: `obsidian/Team Vaults/Matt/AI Coding Environment/n8n-Workflow-Patterns.md`
- **API Agent Development**: See API Agent Development Skill for wrapping workflows as agents

