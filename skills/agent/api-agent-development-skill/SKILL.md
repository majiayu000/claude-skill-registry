---
name: API Agent Development
description: Create API agents that wrap external HTTP services (n8n, LangGraph, CrewAI, OpenAI endpoints). Configure request/response transforms, webhook status tracking, A2A protocol compliance. CRITICAL: Request transforms use template variables ({{userMessage}}, {{conversationId}}, etc.). Response transforms use field extraction. Status webhook URL must read from environment variables.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API Agent Development Skill

**CRITICAL**: API agents wrap external HTTP services. They use request/response transforms to adapt between Orchestrator AI's format and the external service's format. Status webhook URLs MUST read from environment variables.

## When to Use This Skill

Use this skill when:
- Wrapping n8n workflows as API agents
- Wrapping LangGraph/CrewAI/OpenAI endpoints as API agents
- Creating agents that call external HTTP services
- Configuring request/response transformations
- Setting up webhook status tracking
- Ensuring A2A protocol compliance

## API Agent Structure

API agents wrap external HTTP endpoints and transform requests/responses. They follow this structure:

### Minimal API Agent Configuration

From `demo-agents/productivity/jokes_agent/agent.yaml`:

```42:55:demo-agents/productivity/jokes_agent/agent.yaml
api_configuration:
  endpoint: "http://localhost:5678/webhook/f7387dc8-c6e4-460d-9a0c-685c86d76d1f"
  method: "POST"
  timeout: 30000
  headers:
    Content-Type: "application/json"
  authentication: null
  request_transform:
    format: "custom"
    template: '{"sessionId": "{{sessionId}}", "prompt": "{{userMessage}}"}'
  response_transform:
    format: "field_extraction"
    field: "output"
```

### Full API Agent Configuration

Complete example with all options:

```yaml
metadata:
  name: "marketing-swarm-n8n"
  displayName: "Marketing Swarm N8N"
  description: "API agent that calls n8n webhook for marketing campaign swarm processing"
  version: "0.1.0"
  type: "api"

api_configuration:
  endpoint: "http://localhost:5678/webhook/marketing-swarm-flexible"
  method: "POST"
  timeout: 120000
  headers:
    Content-Type: "application/json"
  authentication:
    type: "none"
  request_transform:
    format: "custom"
    template: |
      {
        "taskId": "{{taskId}}",
        "conversationId": "{{conversationId}}",
        "userId": "{{userId}}",
        "announcement": "{{userMessage}}",
        "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status",
        "provider": "{{payload.provider}}",
        "model": "{{payload.model}}"
      }
  response_transform:
    format: "field_extraction"
    field: "payload.content"

configuration:
  execution_capabilities:
    supports_converse: false
    supports_plan: false
    supports_build: true
  deliverable:
    format: "markdown"
    type: "marketing-campaign"
```

## Request Transform: Building API Requests

### Template Variables Available

From `apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts`:

```802:852:apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts
  private buildApiRequestBody(
    api: NonNullable<AgentRuntimeDefinition['transport']>['api'],
    options: AgentRuntimeDispatchOptions,
  ): unknown {
    const t = api?.requestTransform;
    const sessionId =
      options.request.sessionId ?? options.request.conversationId ?? null;
    const userMessage = options.prompt.userMessage ?? '';
    const conversationId = options.request.conversationId ?? null;
    const agentSlug = options.definition.slug;
    const organizationSlug = options.definition.organizationSlug ?? null;

    if (t && t.format === 'custom' && typeof t.template === 'string') {
      try {
        const rendered = t.template.replace(
          /\{\{\s*(\w+)\s*\}\}/g,
          (_m, key) => {
            switch (String(key)) {
              case 'userMessage':
              case 'prompt':
                return userMessage;
              case 'sessionId':
                return String(sessionId ?? '');
              case 'conversationId':
                return String(conversationId ?? '');
              case 'agentSlug':
                return String(agentSlug ?? '');
              case 'organizationSlug':
              case 'org':
                return String(organizationSlug ?? '');
              default:
                return '';
            }
          },
        );
        // If the template is JSON-like, parse it; otherwise send as string
        const maybeJson = rendered.trim();
        if (
          (maybeJson.startsWith('{') && maybeJson.endsWith('}')) ||
          (maybeJson.startsWith('[') && maybeJson.endsWith(']'))
        ) {
          return JSON.parse(maybeJson);
        }
        return rendered;
      } catch {
        // Fall through to minimal body
      }
    }

    // Minimal default body expected by n8n: send only prompt
    return { prompt: userMessage };
  }
```

**Available Template Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `{{userMessage}}` | User's message/prompt | `"Write a blog post about AI"` |
| `{{prompt}}` | Alias for `userMessage` | Same as above |
| `{{sessionId}}` | Session identifier | `"session-123"` |
| `{{conversationId}}` | Conversation identifier | `"conv-456"` |
| `{{taskId}}` | Task identifier | `"task-789"` |
| `{{agentSlug}}` | Agent slug | `"marketing-swarm-n8n"` |
| `{{organizationSlug}}` | Organization slug | `"demo"` |
| `{{org}}` | Alias for `organizationSlug` | Same as above |
| `{{env.API_BASE_URL}}` | Environment variable | `"http://localhost:7100"` |

### Request Transform Examples

**Example 1: Simple Prompt Forwarding**

```yaml
request_transform:
  format: "custom"
  template: '{"prompt": "{{userMessage}}"}'
```

**Example 2: Full Context Forwarding (N8N Pattern)**

```yaml
request_transform:
  format: "custom"
  template: |
    {
      "taskId": "{{taskId}}",
      "conversationId": "{{conversationId}}",
      "userId": "{{userId}}",
      "announcement": "{{userMessage}}",
      "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status",
      "provider": "{{payload.provider}}",
      "model": "{{payload.model}}"
    }
```

**Example 3: Session-Based API**

```yaml
request_transform:
  format: "custom"
  template: '{"sessionId": "{{sessionId}}", "prompt": "{{userMessage}}", "agent": "{{agentSlug}}"}'
```

**Example 4: GraphQL Query**

```yaml
request_transform:
  format: "custom"
  template: |
    {
      "query": "query($input: String!) { search(query: $input) { results } }",
      "variables": {
        "input": "{{userMessage}}"
      }
    }
```

## Response Transform: Extracting Content

### Field Extraction Pattern

From `apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts`:

```854:913:apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts
  private extractApiResponseContent(
    api: NonNullable<AgentRuntimeDefinition['transport']>['api'],
    data: unknown,
  ): string {
    const rt = api?.responseTransform;
    if (
      rt &&
      rt.format === 'field_extraction' &&
      typeof rt.field === 'string' &&
      rt.field.trim()
    ) {
      const fieldPath = rt.field.trim();
      try {
        // Support dotted/bracket paths like "a.b[0].c"
        const tryExtract = (obj: unknown, path: string): unknown => {
          if (!obj || typeof obj !== 'object') return undefined;
          const objRecord = obj as Record<string | number, unknown>;
          // direct field hit
          if (Object.prototype.hasOwnProperty.call(objRecord, path)) {
            return objRecord[path];
          }
          // dotted/bracket notation
          const normalized = path.replace(/\[(\d+)\]/g, '.$1');
          const parts: Array<string | number> = normalized
            .split('.')
            .filter((segment) => segment.length > 0)
            .map((segment) => {
              const numeric = Number(segment);
              return Number.isNaN(numeric) ? segment : numeric;
            });
          let cur: unknown = obj;
          for (const p of parts) {
            if (cur == null) return undefined;
            const curRecord = cur as Record<string | number, unknown>;
            cur = curRecord[p];
          }
          return cur;
        };

        const fromRoot = tryExtract(data, fieldPath);
        if (fromRoot !== undefined) {
          return typeof fromRoot === 'string'
            ? fromRoot
            : this.stringifyContent(fromRoot);
        }
        const dataRecord = data as Record<string, unknown> | undefined;
        if (dataRecord && typeof dataRecord === 'object' && dataRecord.result) {
          const fromResult = tryExtract(dataRecord.result, fieldPath);
          if (fromResult !== undefined) {
            return typeof fromResult === 'string'
              ? fromResult
              : this.stringifyContent(fromResult);
          }
        }
      } catch {
        // fallthrough to generic stringify
      }
    }
    return this.stringifyContent(data);
  }
```

**Key Points:**
- Supports dotted paths: `"data.answer.text"`
- Supports bracket notation: `"data.items[0].text"`
- Falls back to `result` field if path not found at root
- Stringifies non-string values

### Response Transform Examples

**Example 1: Simple Field Extraction**

```yaml
response_transform:
  format: "field_extraction"
  field: "output"
```

**Example 2: Nested Field Extraction**

```yaml
response_transform:
  format: "field_extraction"
  field: "data.answer.text"
```

**Example 3: Array Element Extraction**

```yaml
response_transform:
  format: "field_extraction"
  field: "data.items[0].text"
```

**Example 4: Deep Nested Path**

```yaml
response_transform:
  format: "field_extraction"
  field: "payload.content[0].message"
```

## Complete Example: N8N Workflow Wrapper

### API Agent Configuration

From `storage/snapshots/agents/demo_marketing_swarm_n8n.json`:

```11:11:storage/snapshots/agents/demo_marketing_swarm_n8n.json
  "yaml": "\n{\n    \"metadata\": {\n        \"name\": \"marketing-swarm-n8n\",\n        \"displayName\": \"Marketing Swarm N8N\",\n        \"description\": \"API agent that calls n8n webhook for marketing campaign swarm processing\",\n        \"version\": \"0.1.0\",\n        \"type\": \"api\"\n    },\n    \"configuration\": {\n        \"api\": {\n            \"endpoint\": \"http://localhost:5678/webhook/marketing-swarm-flexible\",\n            \"method\": \"POST\",\n            \"headers\": {\n                \"Content-Type\": \"application/json\"\n            },\n            \"body\": {\n                \"taskId\": \"{{taskId}}\",\n                \"conversationId\": \"{{conversationId}}\",\n                \"userId\": \"{{userId}}\",\n                \"announcement\": \"{{userMessage}}\",\n                \"statusWebhook\": \"http://host.docker.internal:7100/webhooks/status\",\n                \"provider\": \"{{payload.provider}}\",\n                \"model\": \"{{payload.model}}\"\n            },\n            \"authentication\": {\n                \"type\": \"none\"\n            },\n            \"response_mapping\": {\n                \"status_field\": \"status\",\n                \"result_field\": \"payload\"\n            },\n            \"timeout\": 120000\n        },\n        \"deliverable\": {\n            \"format\": \"markdown\",\n            \"type\": \"marketing-campaign\"\n        },\n        \"execution_capabilities\": {\n            \"supports_converse\": false,\n            \"supports_plan\": false,\n            \"supports_build\": true\n        }\n    }\n}\n",
```

**Note**: This example has hardcoded `statusWebhook`. The correct format should use `{{env.API_BASE_URL}}`.

### How the Request is Built

**Step 1: User calls agent**

```json
POST /agent-to-agent/demo/marketing-swarm-n8n/tasks
{
  "mode": "build",
  "conversationId": "conv-123",
  "userMessage": "We're launching our new AI agent platform!",
  "payload": {
    "provider": "openai",
    "model": "gpt-4"
  }
}
```

**Step 2: Request transform applies template**

The `buildApiRequestBody` function processes the template:

```typescript
// Template variables replaced:
{
  "taskId": "task-789",              // From request.taskId
  "conversationId": "conv-123",       // From request.conversationId
  "userId": "user-456",               // From request.userId
  "announcement": "We're launching...", // From prompt.userMessage
  "statusWebhook": "http://localhost:7100/webhooks/status", // From env
  "provider": "openai",                // From payload.provider
  "model": "gpt-4"                     // From payload.model
}
```

**Step 3: HTTP request sent to N8N**

```typescript
POST http://localhost:5678/webhook/marketing-swarm-flexible
Content-Type: application/json

{
  "taskId": "task-789",
  "conversationId": "conv-123",
  "userId": "user-456",
  "announcement": "We're launching our new AI agent platform!",
  "statusWebhook": "http://localhost:7100/webhooks/status",
  "provider": "openai",
  "model": "gpt-4"
}
```

### How the Response is Handled

**Step 1: N8N returns response**

```json
{
  "status": "completed",
  "payload": {
    "webPost": "Full blog post content...",
    "seoContent": "SEO content...",
    "socialMedia": "Social media posts..."
  }
}
```

**Step 2: Response transform extracts content**

If `response_transform.field` is `"payload"`:

```typescript
// extractApiResponseContent extracts:
{
  "webPost": "Full blog post content...",
  "seoContent": "SEO content...",
  "socialMedia": "Social media posts..."
}
```

**Step 3: Content stringified and returned**

```json
{
  "success": true,
  "mode": "build",
  "payload": {
    "content": "{\"webPost\":\"Full blog post...\",\"seoContent\":\"SEO content...\",\"socialMedia\":\"Social media posts...\"}",
    "metadata": {
      "provider": "external_api",
      "model": "api_endpoint",
      "status": "completed"
    }
  }
}
```

## Status Webhook Configuration

### ❌ WRONG - Hardcoded URL

```yaml
request_transform:
  format: "custom"
  template: |
    {
      "statusWebhook": "http://host.docker.internal:7100/webhooks/status"
    }
```

### ✅ CORRECT - Environment Variable

```yaml
request_transform:
  format: "custom"
  template: |
    {
      "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status"
    }
```

**Fallback Pattern:**
```yaml
template: |
  {
    "statusWebhook": "{{env.API_BASE_URL || env.VITE_API_BASE_URL || 'http://host.docker.internal:7100'}}/webhooks/status"
  }
```

## A2A Protocol Compliance

### Required Endpoints

API agents must expose:

```
GET /agents/:orgSlug/:agentSlug/.well-known/agent.json
POST /agents/:orgSlug/:agentSlug/tasks
GET /agents/:orgSlug/:agentSlug/health
```

### .well-known/agent.json Format

```json
{
  "name": "marketing-swarm-n8n",
  "displayName": "Marketing Swarm N8N",
  "description": "API agent that calls n8n webhook",
  "type": "api",
  "version": "0.1.0",
  "capabilities": {
    "modes": ["build"],
    "inputModes": ["application/json"],
    "outputModes": ["application/json"]
  }
}
```

## Complete API Call Flow

### From Backend Runtime Dispatch

From `apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts`:

```373:476:apps/api/src/agent-platform/services/agent-runtime-dispatch.service.ts
  private async dispatchApi(
    options: AgentRuntimeDispatchOptions,
  ): Promise<AgentRuntimeDispatchResult> {
    const api = options.definition.transport!.api!;
    const method = (api.method || 'POST').toUpperCase();
    const url = api.endpoint;

    const payloadOptions = options.request.payload?.options as
      | Record<string, unknown>
      | undefined;
    const mergedHeaders: Record<string, unknown> = {
      'content-type': 'application/json',
      ...(api.headers ?? {}),
      ...((payloadOptions?.headers as Record<string, unknown>) || {}),
    };
    const headers = this.sanitizeForwardHeaders(mergedHeaders);

    const body: unknown = this.buildApiRequestBody(api, options);

    const start = Date.now();
    const defaultTimeout = this.resolveDefaultTimeout('api');
    let res;
    try {
      res = await this.performWithRetry(() =>
        this.http.axiosRef.request({
          url,
          method: method as 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
          headers: headers as Record<string, string>,
          timeout: api.timeout ?? defaultTimeout,
          data: body,
          validateStatus: () => true,
        }),
      );
    } catch (err: unknown) {
      const end = Date.now();
      const errObj = err as { response?: { status?: number } };
      const status = Number(errObj?.response?.status ?? -1);
      this.safeLog('api', url, status, end - start);
      this.metrics.record(
        'api',
        options.definition.slug,
        false,
        end - start,
        status,
      );
      throw err;
    }

    const end = Date.now();
    // Normalize content (apply response transform if configured)
    const content = this.extractApiResponseContent(api, res.data);
    const isOk = res.status >= 200 && res.status < 300;
    const response = {
      content,
      metadata: {
        provider: 'external_api',
        model: 'api_endpoint',
        requestId: (res.headers['x-request-id'] as string | undefined) || '',
        timestamp: new Date(end).toISOString(),
        usage: { inputTokens: 0, outputTokens: 0, totalTokens: 0 },
        timing: { startTime: start, endTime: end, duration: end - start },
        tier: 'external',
        status: isOk ? 'completed' : 'error',
        providerSpecific: { status: res.status },
        ...(isOk
          ? {}
          : { errorMessage: this.buildHttpErrorMessage(res.status, res.data) }),
      },
    } as const;

    // Observability: log sanitized outcome
    this.safeLog('api', url, res.status, end - start);
    this.metrics.record(
      'api',
      options.definition.slug,
      isOk,
      end - start,
      res.status,
    );

    if (options.onStreamChunk) {
      options.onStreamChunk({
        type: 'final',
        content: response.content,
        metadata: response.metadata as unknown as Record<string, unknown>,
      });
    }

    return {
      response,
      config: {
        provider: 'external_api',
        model: 'api_endpoint',
        timeout: api.timeout ?? 30_000,
        baseUrl: url,
      },
      params: {
        systemPrompt: options.prompt.systemPrompt,
        userMessage: options.prompt.userMessage,
        config: { provider: 'external_api', model: 'api_endpoint' },
      },
      routingDecision: options.routingDecision,
    };
  }
```

**Key Steps:**
1. Build request body using `buildApiRequestBody()` (applies template)
2. Sanitize headers (only allowlisted headers forwarded)
3. Make HTTP request with retry logic
4. Extract content using `extractApiResponseContent()` (applies field extraction)
5. Return normalized response

## Header Sanitization

Only these headers are forwarded to external APIs:

```typescript
const base = [
  'authorization',
  'x-user-key',
  'x-api-key',
  'x-agent-api-key',
  'content-type',
];
```

Additional headers can be added via `AGENT_EXTERNAL_HEADER_ALLOWLIST` environment variable.

## Common Patterns

### Pattern 1: Wrapping N8N Workflow

```yaml
api_configuration:
  endpoint: "http://localhost:5678/webhook/workflow-name"
  method: "POST"
  request_transform:
    format: "custom"
    template: |
      {
        "taskId": "{{taskId}}",
        "conversationId": "{{conversationId}}",
        "userId": "{{userId}}",
        "prompt": "{{userMessage}}",
        "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status",
        "provider": "{{payload.provider}}",
        "model": "{{payload.model}}"
      }
  response_transform:
    format: "field_extraction"
    field: "payload.content"
```

### Pattern 2: Wrapping LangGraph/CrewAI/OpenAI Endpoint

```yaml
api_configuration:
  endpoint: "http://localhost:8000/api/orchestrate"
  method: "POST"
  request_transform:
    format: "custom"
    template: |
      {
        "conversationId": "{{conversationId}}",
        "userMessage": "{{userMessage}}",
        "provider": "{{payload.provider}}",
        "model": "{{payload.model}}",
        "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status"
      }
  response_transform:
    format: "field_extraction"
    field: "result.content"
```

### Pattern 3: Simple REST API

```yaml
api_configuration:
  endpoint: "https://api.example.com/v1/generate"
  method: "POST"
  headers:
    Authorization: "Bearer {{env.API_KEY}}"
  request_transform:
    format: "custom"
    template: '{"prompt": "{{userMessage}}"}'
  response_transform:
    format: "field_extraction"
    field: "data.text"
```

## Common Mistakes

### ❌ Mistake 1: Hardcoded Status Webhook

```yaml
# ❌ WRONG
"statusWebhook": "http://host.docker.internal:7100/webhooks/status"
```

**Fix:**
```yaml
# ✅ CORRECT
"statusWebhook": "{{env.API_BASE_URL}}/webhooks/status"
```

### ❌ Mistake 2: Missing Required Parameters (for N8N)

```yaml
# ❌ WRONG - Missing status tracking parameters
template: '{"prompt": "{{userMessage}}"}'
```

**Fix:**
```yaml
# ✅ CORRECT - Include all required parameters
template: |
  {
    "taskId": "{{taskId}}",
    "conversationId": "{{conversationId}}",
    "userId": "{{userId}}",
    "prompt": "{{userMessage}}",
    "statusWebhook": "{{env.API_BASE_URL}}/webhooks/status"
  }
```

### ❌ Mistake 3: Wrong Field Path

```yaml
# ❌ WRONG - Field doesn't exist
response_transform:
  field: "response.data.text"  # But actual response is {"result": {"text": "..."}}
```

**Fix:**
```yaml
# ✅ CORRECT - Use correct path
response_transform:
  field: "result.text"
```

### ❌ Mistake 4: Template Syntax Errors

```yaml
# ❌ WRONG - Invalid JSON
template: '{"prompt": {{userMessage}}}'  # Missing quotes
```

**Fix:**
```yaml
# ✅ CORRECT - Valid JSON
template: '{"prompt": "{{userMessage}}"}'
```

## Checklist for API Agents

When creating API agents:

- [ ] `endpoint` URL is correct (webhook URL for n8n, API URL for others)
- [ ] `method` matches endpoint requirements (usually POST)
- [ ] `request_transform.template` includes all required parameters
- [ ] `statusWebhook` reads from environment (not hardcoded)
- [ ] `response_transform.field` matches actual response structure
- [ ] Field path supports dotted/bracket notation if needed
- [ ] `timeout` is appropriate (120000 for n8n workflows)
- [ ] Headers include `Content-Type: application/json`
- [ ] `.well-known/agent.json` endpoint is configured
- [ ] A2A protocol compliance verified

## Related Documentation

- **N8N Development**: See N8N Development Skill for workflow parameter requirements
- **A2A Protocol**: See Back-End Structure Skill for protocol details
- **Transport Types**: `@orchestrator-ai/transport-types` package

