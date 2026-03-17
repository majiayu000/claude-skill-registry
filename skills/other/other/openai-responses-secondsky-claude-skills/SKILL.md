---
name: openai-responses
description: OpenAI Responses API for stateful agentic applications with reasoning preservation. Use for MCP integration, built-in tools, background processing, or migrating from Chat Completions.

  Keywords: responses api, openai responses, stateful openai, openai mcp, code interpreter openai, file search openai, web search openai, image generation openai, reasoning preservation, agentic workflows, conversation state, background mode, chat completions migration, gpt-5, polymorphic outputs
license: MIT
metadata:
  version: "2.0.0"
  last_verified: "2025-11-18"
  api_launch: "March 2025"
  sdk_version: "openai@5.19.1+"
  templates_included: 10
  references_included: 8
---

# OpenAI Responses API

**Status**: Production Ready | **API Launch**: March 2025 | **SDK**: openai@5.19.1+

---

## Quick Start (5 Minutes)

### Node.js

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'What are the 5 Ds of dodgeball?',
});

console.log(response.output_text);
```

### Cloudflare Workers

```typescript
const response = await fetch('https://api.openai.com/v1/responses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gpt-5',
    input: 'Hello, world!',
  }),
});

const data = await response.json();
console.log(data.output_text);
```

**Load `references/setup-guide.md` for complete setup with stateful conversations and built-in tools.**

---

## What Is the Responses API?

The Responses API (`/v1/responses`) is OpenAI's unified interface for agentic applications launched March 2025. **Key Innovation**: Preserved reasoning state across turns (unlike Chat Completions which discards it), improving multi-turn performance by ~5% on TAUBench.

**Why Use Responses Over Chat Completions?** Automatic state management, preserved reasoning, server-side tools, 40-80% better cache utilization, and built-in MCP support.

**Load `references/responses-vs-chat-completions.md` for complete comparison and decision guide.**

---

## Top 3 Critical Rules

### Always Do ✅

1. **Store conversation_id** - Preserve state between turns (most critical)
2. **Use environment variables** for API keys (NEVER hardcode)
3. **Handle polymorphic outputs** - Check `output.type` (message, reasoning, function_call)

### Never Do ❌

1. **Never ignore conversation_id** - State will be lost
2. **Never assume single output type** - Always check `output.type`
3. **Never mix Chat Completions and Responses** in same conversation

**Load `references/setup-guide.md` for complete rules and best practices.**

---

## Top 5 Use Cases

### Use Case 1: Stateful Conversation

```typescript
// First turn
const response1 = await openai.responses.create({
  model: 'gpt-5',
  input: 'My favorite color is blue.',
});

const conversationId = response1.conversation_id;

// Second turn - model remembers
const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation_id: conversationId,
  input: 'What is my favorite color?',
});
// Output: "Your favorite color is blue."
```

**Load**: `references/stateful-conversations.md` + `templates/stateful-conversation.ts`

---

### Use Case 2: Web Search Agent

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Search the web for latest AI news.',
  tools: {
    web_search: { enabled: true },
  },
});
```

**Load**: `references/built-in-tools-guide.md` + `templates/web-search.ts`

---

### Use Case 3: Code Interpreter

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Calculate the sum of squares from 1 to 100.',
  tools: {
    code_interpreter: { enabled: true },
  },
});
```

**Load**: `references/built-in-tools-guide.md` + `templates/code-interpreter.ts`

---

### Use Case 4: File Search (RAG)

```typescript
// Upload file
const file = await openai.files.create({
  file: fs.createReadStream('document.pdf'),
  purpose: 'user_data',
});

// Search file
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Summarize key points from the uploaded document.',
  tools: {
    file_search: {
      enabled: true,
      file_ids: [file.id],
    },
  },
});
```

**Load**: `references/built-in-tools-guide.md` + `templates/file-search.ts`

---

### Use Case 5: MCP Server Integration

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Get weather for San Francisco.',
  tools: {
    mcp_servers: [
      {
        url: 'https://weather-mcp.example.com',
        tool_choice: 'auto',
      },
    ],
  },
});
```

**Load**: `references/mcp-integration-guide.md` + `templates/mcp-integration.ts`

---

## Built-in Tools

All tools run server-side: **Code Interpreter** (Python execution), **File Search** (RAG), **Web Search** (real-time), **Image Generation** (DALL-E).

Enable explicitly:

```typescript
tools: {
  code_interpreter: { enabled: true },
  file_search: { enabled: true, file_ids: ['file-123'] },
  web_search: { enabled: true },
  image_generation: { enabled: true },
}
```

**Load `references/built-in-tools-guide.md` for complete guide with examples and configuration options.**

---

## Stateful Conversations

Automatic state management with conversation IDs eliminates manual message tracking, preserves reasoning, and improves cache utilization by 40-80%.

```typescript
// Create conversation
const response1 = await openai.responses.create({
  model: 'gpt-5',
  input: 'Remember: my name is Alice.',
});

// Continue conversation
const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation_id: response1.conversation_id,
  input: 'What is my name?',
});
```

**Load `references/stateful-conversations.md` for persistence patterns (Node.js/Redis/KV) and lifecycle management.**

---

## Migration from Chat Completions

Quick changes: `messages` → `input`, `system` role → `developer`, `choices[0].message.content` → `output_text`, `/v1/chat/completions` → `/v1/responses`.

**Before (Chat Completions):**

```typescript
const messages = [{ role: 'user', content: 'Hello' }];
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: messages,
});
messages.push(response.choices[0].message); // Manual history
```

**After (Responses API):**

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Hello',
});

const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation_id: response.conversation_id, // Automatic state
  input: 'Follow-up question',
});
```

**Load `references/migration-guide.md` for complete migration checklist with tool migration patterns.**

---

## Polymorphic Outputs

Responses can return multiple output types (message, reasoning, function_call, image). Handle each type or use `output_text` convenience property.

```typescript
for (const output of response.output) {
  if (output.type === 'message') {
    console.log('Message:', output.content);
  } else if (output.type === 'reasoning') {
    console.log('Reasoning:', output.summary);
  } else if (output.type === 'function_call') {
    console.log('Function:', output.name, output.arguments);
  }
}

// Or use convenience property
console.log(response.output_text);
```

**Load `references/reasoning-preservation.md` for reasoning output details and debugging patterns.**

---

## Background Mode

For long-running tasks (>60 seconds), use `background: true` to run asynchronously and poll for completion.

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Analyze this 50-page document.',
  background: true,
});

// Poll for completion
const completed = await openai.responses.retrieve(response.id);
```

**Load `templates/background-mode.ts` for complete polling pattern with exponential backoff.**

---

## Top 3 Errors & Solutions

### Error 1: Session State Not Persisting

**Symptom**: Model doesn't remember previous turns.

**Cause**: Not using conversation IDs or creating new conversation each time.

**Solution**:

```typescript
// ✅ GOOD: Reuse conversation ID
const conv = await openai.conversations.create();
const response1 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id, // Same ID
  input: 'Question 1',
});
const response2 = await openai.responses.create({
  model: 'gpt-5',
  conversation: conv.id, // Same ID - remembers previous
  input: 'Question 2',
});
```

---

### Error 2: MCP Server Connection Failed

**Cause**: Invalid server URL, missing/expired authorization token.

**Solution**:

```typescript
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Test MCP',
  tools: [
    {
      type: 'mcp',
      server_url: 'https://mcp.stripe.com', // ✅ Full HTTPS URL
      authorization: process.env.STRIPE_OAUTH_TOKEN, // ✅ Valid token
    },
  ],
});
```

**Prevention**: Use environment variables for secrets, implement token refresh logic, add retry with exponential backoff.

---

### Error 3: Code Interpreter Timeout

**Cause**: Code runs longer than 30 seconds (standard mode limit).

**Solution**:

```typescript
// ✅ GOOD: Use background mode for long tasks
const response = await openai.responses.create({
  model: 'gpt-5',
  input: 'Process this massive dataset',
  background: true, // ✅ Up to 10 minutes
  tools: [{ type: 'code_interpreter' }],
});

// Poll for results
let result = await openai.responses.retrieve(response.id);
while (result.status === 'in_progress') {
  await new Promise(r => setTimeout(r, 5000));
  result = await openai.responses.retrieve(response.id);
}
```

**Load `references/top-errors.md` for all 8 errors with detailed solutions and prevention strategies.**

---

## When to Load References

### Load `references/setup-guide.md` when:
- First-time Responses API user needing complete Node.js or Cloudflare Workers setup
- Want production deployment checklist with environment-specific best practices
- Troubleshooting setup issues or implementing streaming/background patterns

### Load `references/responses-vs-chat-completions.md` when:
- Deciding between Responses and Chat Completions APIs
- Understanding performance benchmarks (TAUBench results, cache utilization)
- Evaluating migration effort or comparing cost structures

### Load `references/migration-guide.md` when:
- Migrating from Chat Completions API with step-by-step checklist
- Need code comparison examples (before/after patterns)
- Migrating tools from custom functions to built-in/MCP

### Load `references/built-in-tools-guide.md` when:
- Using Code Interpreter, File Search, Web Search, or Image Generation
- Need tool configuration options, combining multiple tools, or troubleshooting

### Load `references/mcp-integration-guide.md` when:
- Integrating external MCP servers or building custom MCP tools
- Need MCP configuration examples or authentication patterns

### Load `references/stateful-conversations.md` when:
- Implementing conversation persistence with KV/Redis/database
- Need conversation lifecycle management or metadata tracking patterns

### Load `references/reasoning-preservation.md` when:
- Want to access model reasoning for debugging or transparency
- Building auditable AI systems or need reasoning output examples

### Load `references/top-errors.md` when:
- Encountering API errors (8 common errors covered with solutions)
- Need error code reference, prevention strategies, or error handling patterns

---

## Production Checklist

Before deploying:

- [ ] API key stored securely (environment variable or secret)
- [ ] Error handling implemented (401, 429, 400, 500)
- [ ] Rate limiting handled (exponential backoff)
- [ ] Conversation IDs persisted (database/KV)
- [ ] Streaming enabled for long responses
- [ ] Tools enabled explicitly
- [ ] Polymorphic output handling

**Load `references/setup-guide.md` for complete production checklist with platform-specific considerations.**

---

## Related Skills

- **openai-api** - Classic Chat Completions API
- **openai-agents** - OpenAI Agents SDK (wrapper for Responses)
- **claude-api** - Claude API for comparison
- **ai-sdk-core** - Vercel AI SDK (supports Responses)

---

## Official Documentation

- **Responses API**: https://platform.openai.com/docs/api-reference/responses
- **Migration Guide**: https://platform.openai.com/docs/guides/responses-migration
- **Built-in Tools**: https://platform.openai.com/docs/guides/responses-tools
- **MCP Integration**: https://platform.openai.com/docs/guides/mcp

---

**Questions? Issues?**

1. Check `references/top-errors.md` for error solutions
2. Review `references/setup-guide.md` for complete setup
3. See `references/migration-guide.md` for Chat Completions migration
4. Load templates from `templates/` for working examples
