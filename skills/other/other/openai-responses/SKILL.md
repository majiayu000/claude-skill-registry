---
name: openai-responses
description: |
  Build agentic AI with OpenAI Responses API - stateful conversations with preserved reasoning, built-in tools (Code Interpreter, File Search, Web Search), and MCP integration. Prevents 11 documented errors.

  Use when: building agents with persistent reasoning, using server-side tools, or migrating from Chat Completions/Assistants for better multi-turn performance.
user-invocable: true
---

# OpenAI Responses API

**Status**: Production Ready
**Last Updated**: 2026-01-21
**API Launch**: March 2025
**Dependencies**: openai@6.16.0 (Node.js) or fetch API (Cloudflare Workers)

---

## What Is the Responses API?

OpenAI's unified interface for agentic applications, launched **March 2025**. Provides **stateful conversations** with **preserved reasoning state** across turns.

**Key Innovation:** Unlike Chat Completions (reasoning discarded between turns), Responses **preserves the model's reasoning notebook**, improving performance by **5% on TAUBench** and enabling better multi-turn interactions.

**vs Chat Completions:**

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| State | Manual history tracking | Automatic (conversation IDs) |
| Reasoning | Dropped between turns | Preserved across turns (+5% TAUBench) |
| Tools | Client-side round trips | Server-side hosted |
| Output | Single message | Polymorphic (8 types) |
| Cache | Baseline | **40-80% better utilization** |
| MCP | Manual | Built-in |

---

## Quick Start

```bash
npm install openai@6.16.0
```

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'What are the 5 Ds of dodgeball?',
});

console.log(response.output_text);
```

**Key differences from Chat Completions:**
- Endpoint: `/v1/responses` (not `/v1/chat/completions`)
- Parameter: `input` (not `messages`)
- Role: `developer` (not `system`)
- Output: `response.output_text` (not `choices[0].message.content`)

---

## When to Use Responses vs Chat Completions

**Use Responses:**
- Agentic applications (reasoning + actions)
- Multi-turn conversations (preserved reasoning = +5% TAUBench)
- Built-in tools (Code Interpreter, File Search, Web Search, MCP)
- Background processing (60s standard, 10min extended timeout)

**Use Chat Completions:**
- Simple one-off generation
- Fully stateless interactions
- Legacy integrations

---

## Stateful Conversations

**Automatic State Management** using conversation IDs:

```typescript
// Create conversation
const conv = await openai.conversations.create({
  metadata: { user_id: 'user_123' },
});

// First turn
const response1 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id,
  input: 'What are the 5 Ds of dodgeball?',
});

// Second turn - model remembers context + reasoning
const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id,
  input: 'Tell me more about the first one',
});
```

**Benefits:** No manual history tracking, reasoning preserved, 40-80% better cache utilization

**Conversation Limits:** 90-day expiration

---

## Built-in Tools (Server-Side)

**Server-side hosted tools** eliminate backend round trips:

| Tool | Purpose | Notes |
|------|---------|-------|
| `code_interpreter` | Execute Python code | Sandboxed, 30s timeout (use `background: true` for longer) |
| `file_search` | RAG without vector stores | Max 512MB per file, supports PDF/Word/Markdown/HTML/code |
| `web_search` | Real-time web information | Automatic source citations |
| `image_generation` | DALL-E integration | DALL-E 3 default |
| `mcp` | Connect external tools | OAuth supported, tokens NOT stored |

**Usage:**
```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Calculate mean of: 10, 20, 30, 40, 50',
  tools: [{ type: 'code_interpreter' }],
});
```

### Web Search TypeScript Note

**TypeScript Limitation**: The `web_search` tool's `external_web_access` option is missing from SDK types (as of v6.16.0).

**Workaround**:
```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Search for recent news',
  tools: [{
    type: 'web_search',
    external_web_access: true,
  } as any],  // ✅ Type assertion to suppress error
});
```

**Source**: [GitHub Issue #1716](https://github.com/openai/openai-node/issues/1716)

---

## MCP Server Integration

Built-in support for **Model Context Protocol (MCP)** servers to connect external tools (Stripe, databases, custom APIs).

### User Approval Requirement

**By default, explicit user approval is required** before any data is shared with a remote MCP server (security feature).

**Handling Approval**:
```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Get my Stripe balance',
  tools: [{
    type: 'mcp',
    server_label: 'stripe',
    server_url: 'https://mcp.stripe.com',
    authorization: process.env.STRIPE_TOKEN,
  }],
});

if (response.status === 'requires_approval') {
  // Show user: "This action requires sharing data with Stripe. Approve?"
  // After user approves, retry with approval token
}
```

**Alternative**: Pre-approve MCP servers in OpenAI dashboard (users configure trusted servers via settings)

**Source**: [Official MCP Guide](https://platform.openai.com/docs/guides/tools-connectors-mcp)

### Basic MCP Usage

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Roll 2d6 dice',
  tools: [{
    type: 'mcp',
    server_label: 'dice',
    server_url: 'https://example.com/mcp',
    authorization: process.env.TOKEN, // ⚠️ NOT stored, required each request
  }],
});
```

**MCP Output Types:**
- `mcp_list_tools` - Tools discovered on server
- `mcp_call` - Tool invocation + result
- `message` - Final response

---

## Reasoning Preservation

**Key Innovation:** Model's internal reasoning state survives across turns (unlike Chat Completions which discards it).

**Visual Analogy:**
- Chat Completions: Model tears out scratchpad page before responding
- Responses API: Scratchpad stays open for next turn

**Performance:** +5% on TAUBench (GPT-5) purely from preserved reasoning

**Reasoning Summaries** (free):
```typescript
response.output.forEach(item => {
  if (item.type === 'reasoning') console.log(item.summary[0].text);
  if (item.type === 'message') console.log(item.content[0].text);
});
```

### Important: Reasoning Traces Privacy

**What You Get**: Reasoning summaries (not full internal traces)
**What OpenAI Keeps**: Full chain-of-thought reasoning (proprietary, for security/privacy)

For GPT-5-Thinking models:
- OpenAI preserves reasoning **internally** in their backend
- This preserved reasoning improves multi-turn performance (+5% TAUBench)
- But developers only receive **summaries**, not the actual chain-of-thought
- Full reasoning traces are not exposed (OpenAI's IP protection)

**Source**: [Sean Goedecke Analysis](https://www.seangoedecke.com/responses-api/)

---

## Background Mode

For long-running tasks, use `background: true`:

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Analyze 500-page document',
  background: true,
  tools: [{ type: 'file_search', file_ids: [fileId] }],
});

// Poll for completion (check every 5s)
const result = await openai.responses.retrieve(response.id);
if (result.status === 'completed') console.log(result.output_text);
```

**Timeout Limits:**
- Standard: 60 seconds
- Background: 10 minutes

### Performance Considerations

**Time-to-First-Token (TTFT) Latency:**
Background mode currently has higher TTFT compared to synchronous responses. OpenAI is working to reduce this gap.

**Recommendation:**
- For user-facing real-time responses, use sync mode (lower latency)
- For long-running async tasks, use background mode (latency acceptable)

**Source**: [OpenAI Background Mode Docs](https://platform.openai.com/docs/guides/background)

---

## Data Retention and Privacy

**Default Retention**: 30 days when `store: true` (default)
**Zero Data Retention (ZDR)**: Organizations with ZDR automatically enforce `store: false`
**Background Mode**: NOT ZDR compatible (stores data ~10 minutes for polling)

**Timeline**:
- September 26, 2025: OpenAI court-ordered retention ended
- Current: 30-day default retention with `store: true`

**Control Storage**:
```typescript
// Disable storage (no retention)
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Hello!',
  store: false,  // ✅ No retention
});

// ZDR organizations: store always treated as false
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Hello!',
  store: true,  // ⚠️ Ignored by OpenAI for ZDR orgs, treated as false
});
```

**ZDR Compliance**:
- Avoid background mode (requires temporary storage)
- Explicitly set `store: false` for clarity
- Note: 60s timeout applies in sync mode

**Source**: [OpenAI Data Controls](https://platform.openai.com/docs/guides/your-data)

---

## Polymorphic Outputs

Returns **8 output types** instead of single message:

| Type | Example |
|------|---------|
| `message` | Final answer, explanation |
| `reasoning` | Step-by-step thought process (free!) |
| `code_interpreter_call` | Python code + results |
| `mcp_call` | Tool name, args, output |
| `mcp_list_tools` | Tool definitions from MCP server |
| `file_search_call` | Matched chunks, citations |
| `web_search_call` | URLs, snippets |
| `image_generation_call` | Image URL |

**Processing:**
```typescript
response.output.forEach(item => {
  if (item.type === 'reasoning') console.log(item.summary[0].text);
  if (item.type === 'web_search_call') console.log(item.results);
  if (item.type === 'message') console.log(item.content[0].text);
});

// Or use helper for text-only
console.log(response.output_text);
```

---

## Migration from Chat Completions

**Breaking Changes:**

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| Endpoint | `/v1/chat/completions` | `/v1/responses` |
| Parameter | `messages` | `input` |
| Role | `system` | `developer` |
| Output | `choices[0].message.content` | `output_text` |
| State | Manual array | Automatic (conversation ID) |
| Streaming | `data: {"choices":[...]}` | SSE with 8 item types |

**Example:**
```typescript
// Before
const response = await openai.chat.completions.create({
  model: 'gpt-5',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});
console.log(response.choices[0].message.content);

// After
const response = await openai.responses.create({
  model: 'gpt-5',
  input: [
    { role: 'developer', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' },
  ],
});
console.log(response.output_text);
```

---

## Migration from Assistants API

**CRITICAL: Assistants API Sunset Timeline**

- **August 26, 2025**: Assistants API officially deprecated
- **2025-2026**: OpenAI providing migration utilities
- **August 26, 2026**: Assistants API sunset (stops working)

**Migrate before August 26, 2026** to avoid breaking changes.

**Source**: [Assistants API Sunset Announcement](https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666)

**Key Breaking Changes:**

| Assistants API | Responses API |
|----------------|---------------|
| Assistants (created via API) | Prompts (created in dashboard) |
| Threads | Conversations (store items, not just messages) |
| Runs (server-side lifecycle) | Responses (stateless calls) |
| Run-Steps | Items (polymorphic outputs) |

**Migration Example:**
```typescript
// Before (Assistants API - deprecated)
const assistant = await openai.beta.assistants.create({
  model: 'gpt-4',
  instructions: 'You are helpful.',
});

const thread = await openai.beta.threads.create();

const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: assistant.id,
});

// After (Responses API - current)
const conversation = await openai.conversations.create({
  metadata: { purpose: 'customer_support' },
});

const response = await openai.responses.create({
  model: 'gpt-5',
  conversation: conversation.id,
  input: [
    { role: 'developer', content: 'You are helpful.' },
    { role: 'user', content: 'Hello!' },
  ],
});
```

**Migration Guide**: [Official Assistants Migration Docs](https://platform.openai.com/docs/guides/migrate-to-responses)

---

## Known Issues Prevention

This skill prevents **11** documented errors:

**1. Session State Not Persisting**
- Cause: Not using conversation IDs or using different IDs per turn
- Fix: Create conversation once (`const conv = await openai.conversations.create()`), reuse `conv.id` for all turns

**2. MCP Server Connection Failed** (`mcp_connection_error`)
- Causes: Invalid URL, missing/expired auth token, server down
- Fix: Verify URL is correct, test manually with `fetch()`, check token expiration

**3. Code Interpreter Timeout** (`code_interpreter_timeout`)
- Cause: Code runs longer than 30 seconds
- Fix: Use `background: true` for extended timeout (up to 10 min)

**4. Image Generation Rate Limit** (`rate_limit_error`)
- Cause: Too many DALL-E requests
- Fix: Implement exponential backoff retry (1s, 2s, 3s delays)

**5. File Search Relevance Issues**
- Cause: Vague queries return irrelevant results
- Fix: Use specific queries ("pricing in Q4 2024" not "find pricing"), filter by `chunk.score > 0.7`

**6. Cost Tracking Confusion**
- Cause: Responses bills for input + output + tools + stored conversations (vs Chat Completions: input + output only)
- Fix: Set `store: false` if not needed, monitor `response.usage.tool_tokens`

**7. Conversation Not Found** (`invalid_request_error`)
- Causes: ID typo, conversation deleted, or expired (90-day limit)
- Fix: Verify exists with `openai.conversations.list()` before using

**8. Tool Output Parsing Failed**
- Cause: Accessing wrong output structure
- Fix: Use `response.output_text` helper or iterate `response.output.forEach(item => ...)` checking `item.type`

**9. Zod v4 Incompatibility with Structured Outputs**
- **Error**: `Invalid schema for response_format 'name': schema must be a JSON Schema of 'type: "object"', got 'type: "string"'.`
- **Source**: [GitHub Issue #1597](https://github.com/openai/openai-node/issues/1597)
- **Why It Happens**: SDK's vendored `zod-to-json-schema` library doesn't support Zod v4 (missing `ZodFirstPartyTypeKind` export)
- **Prevention**: Pin to Zod v3 (`"zod": "^3.23.8"`) or use custom `zodTextFormat` with `z.toJSONSchema({ target: "draft-7" })`

```typescript
// Workaround: Pin to Zod v3 (recommended)
{
  "dependencies": {
    "openai": "^6.16.0",
    "zod": "^3.23.8"  // DO NOT upgrade to v4 yet
  }
}
```

**10. Background Mode Web Search Missing Sources**
- **Error**: `web_search_call` output items contain query but no sources/results
- **Source**: [GitHub Issue #1676](https://github.com/openai/openai-node/issues/1676)
- **Why It Happens**: When using `background: true` + `web_search` tool, OpenAI doesn't return sources in the response
- **Prevention**: Use synchronous mode (`background: false`) when web search sources are needed

```typescript
// ✅ Sources available in sync mode
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Latest AI news?',
  background: false,  // Required for sources
  tools: [{ type: 'web_search' }],
});
```

**11. Streaming Mode Missing output_text Helper**
- **Error**: `finalResponse().output_text` is `undefined` in streaming mode
- **Source**: [GitHub Issue #1662](https://github.com/openai/openai-node/issues/1662)
- **Why It Happens**: `stream.finalResponse()` doesn't include `output_text` convenience field (only available in non-streaming responses)
- **Prevention**: Listen for `output_text.done` event or manually extract from `output` items

```typescript
// Workaround: Listen for event
const stream = openai.responses.stream({ model: 'gpt-5', input: 'Hello!' });
let outputText = '';
for await (const event of stream) {
  if (event.type === 'output_text.done') {
    outputText = event.output_text;  // ✅ Available in event
  }
}
```

---

## Critical Patterns

**✅ Always:**
- Use conversation IDs for multi-turn (40-80% better cache)
- Handle all 8 output types in polymorphic responses
- Use `background: true` for tasks >30s
- Provide MCP `authorization` tokens (NOT stored, required each request)
- Monitor `response.usage.total_tokens` for cost control

**❌ Never:**
- Expose API keys in client-side code
- Assume single message output (use `response.output_text` helper)
- Reuse conversation IDs across users (security risk)
- Ignore error types (handle `rate_limit_error`, `mcp_connection_error` specifically)
- Poll faster than 1s for background tasks (use 5s intervals)

---

## References

**Official Docs:**
- Responses API Guide: https://platform.openai.com/docs/guides/responses
- API Reference: https://platform.openai.com/docs/api-reference/responses
- MCP Integration: https://platform.openai.com/docs/guides/tools-connectors-mcp
- Blog Post: https://developers.openai.com/blog/responses-api/
- Starter App: https://github.com/openai/openai-responses-starter-app

**Skill Resources:** `templates/`, `references/responses-vs-chat-completions.md`, `references/mcp-integration-guide.md`, `references/built-in-tools-guide.md`, `references/migration-guide.md`, `references/top-errors.md`

---

**Last verified**: 2026-01-21 | **Skill version**: 2.1.0 | **Changes**: Added 3 TIER 1 issues (Zod v4, background web search, streaming output_text), 2 TIER 2 findings (MCP approval, reasoning privacy), Data Retention & ZDR section, Assistants API sunset timeline, background mode TTFT note, web search TypeScript limitation. Updated SDK version to 6.16.0.
