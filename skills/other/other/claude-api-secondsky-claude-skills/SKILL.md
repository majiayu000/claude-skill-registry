---
name: claude-api
description: Anthropic Messages API (Claude API) for integrations, streaming, prompt caching, tool use, vision. Use for chatbots, assistants, or encountering rate limits, 429 errors.

  Keywords: claude api, anthropic api, messages api, @anthropic-ai/sdk, claude streaming, prompt caching, tool use, vision, extended thinking, claude 3.5 sonnet, claude 3.7 sonnet, claude sonnet 4, function calling, SSE, rate limits, 429 errors
license: MIT
metadata:
  version: "2.0.0"
  last_verified: "2025-11-21"
  sdk_version: "@anthropic-ai/sdk@0.70.1"
  templates_included: 12
  references_included: 7
---

# Claude API (Anthropic Messages API)

**Status**: Production Ready | **SDK**: @anthropic-ai/sdk@0.70.1

---

## Quick Start (5 Minutes)

### Node.js

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' },
  ],
});

console.log(message.content[0].text);
```

### Cloudflare Workers

```typescript
const response = await fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {
    'x-api-key': env.ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json',
  },
  body: JSON.stringify({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 1024,
    messages: [{ role: 'user', content: 'Hello!' }],
  }),
});

const data = await response.json();
console.log(data.content[0].text);
```

**Load `references/setup-guide.md` for complete setup with streaming, caching, and tools.**

---

## Critical Rules

### Always Do ✅

1. **Use environment variables** for API keys (NEVER hardcode)
2. **Set max_tokens** explicitly (required parameter)
3. **Pin model version** (`claude-sonnet-4-5-20250929`, not `claude-3-5-sonnet-latest`)
4. **Enable prompt caching** for repeated content (90% cost savings)
5. **Stream long responses** (`stream: true`) for better UX
6. **Handle errors** - Implement retry logic for 429, 529 errors
7. **Validate inputs** - Sanitize user messages before sending
8. **Monitor costs** - Track token usage
9. **Set timeouts** - Prevent hanging requests
10. **Use tool use properly** - Return tool_result in follow-up message

### Never Do ❌

1. **Never expose API key** in client-side code
2. **Never skip max_tokens** - API will error without it
3. **Never ignore stop_reason** - Check for `tool_use`, `end_turn`, `max_tokens`
4. **Never assume single content block** - `content` is an array
5. **Never use outdated models** - Pin to specific version
6. **Never skip error handling** - API calls can fail
7. **Never mix message roles** - Alternate user/assistant correctly
8. **Never ignore rate limits** - Implement exponential backoff
9. **Never store API keys** in logs or databases
10. **Never skip input validation** - Prevent injection attacks

---

## Top 3 Errors (Prevent 80% of Issues)

### Error #1: Rate Limit 429

**Symptom**: `429 Too Many Requests: Number of request tokens has exceeded your per-minute rate limit`

**Solution**: Implement exponential backoff with retry-after header

```typescript
async function handleRateLimit(requestFn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      if (error.status === 429) {
        const retryAfter = error.response?.headers?.['retry-after'];
        const delay = retryAfter ? parseInt(retryAfter) * 1000 : 1000 * Math.pow(2, attempt);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
}
```

**Prevention**: Monitor rate limit headers, upgrade tier, implement backoff

---

### Error #2: Prompt Caching Not Activating

**Symptom**: High costs despite `cache_control` blocks, `cache_read_input_tokens: 0`

**Solution**: Place `cache_control` on LAST block with >= 1024 tokens

```typescript
// ❌ Wrong - cache_control not at end
{
  type: 'text',
  text: DOCUMENT,
  cache_control: { type: 'ephemeral' },  // Wrong position
},
{
  type: 'text',
  text: 'Additional text',
}

// ✅ Correct - cache_control at end
{
  type: 'text',
  text: DOCUMENT + '\n\nAdditional text',
  cache_control: { type: 'ephemeral' },  // Correct position
}
```

**Prevention**: Ensure content >= 1024 tokens, keep cached content identical, monitor usage

**Load `references/prompt-caching-guide.md` for complete caching strategy.**

---

### Error #3: Tool Use Response Format Errors

**Symptom**: `invalid_request_error: tools[0].input_schema is invalid`

**Solution**: Valid tool schema with proper JSON Schema

```typescript
// ✅ Valid tool schema
{
  name: 'get_weather',
  description: 'Get current weather',
  input_schema: {
    type: 'object',           // Must be 'object'
    properties: {
      location: {
        type: 'string',       // Valid JSON Schema types
        description: 'City'   // Optional but recommended
      }
    },
    required: ['location']    // List required fields
  }
}

// ✅ Valid tool result
{
  type: 'tool_result',
  tool_use_id: block.id,      // Must match tool_use id
  content: JSON.stringify(result)  // Convert to string
}
```

**Prevention**: Validate schemas, match tool_use_id exactly, stringify results

**Load `references/tool-use-patterns.md` + `references/top-errors.md` for all 12 errors.**

---

## Common Use Cases (Quick Patterns)

### Streaming Responses

```typescript
const stream = await client.messages.stream({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Write a story.' }],
});

for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text);
  }
}
```

**Load**: `templates/streaming-chat.ts`

---

### Prompt Caching (90% Cost Savings)

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  system: [
    {
      type: 'text',
      text: 'Long system prompt...',
      cache_control: { type: 'ephemeral' },
    },
  ],
  messages: [{ role: 'user', content: 'Question?' }],
});
```

**Cache lasts 5 minutes, 90% savings on cached tokens**

**Load**: `references/prompt-caching-guide.md` + `templates/prompt-caching.ts`

---

### Tool Use (Function Calling)

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  tools: [{
    name: 'get_weather',
    description: 'Get weather for a location',
    input_schema: {
      type: 'object',
      properties: { location: { type: 'string' } },
      required: ['location'],
    },
  }],
  messages: [{ role: 'user', content: 'Weather in SF?' }],
});

if (message.stop_reason === 'tool_use') {
  const toolUse = message.content.find(b => b.type === 'tool_use');
  // Execute tool and send result back...
}
```

**Load**: `references/tool-use-patterns.md` + `templates/tool-use-basic.ts`

---

### Vision (Image Understanding)

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: [
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: base64Image,
        },
      },
      { type: 'text', text: 'What is in this image?' },
    ],
  }],
});
```

**Supports**: JPEG, PNG, WebP, GIF (max 5MB)

**Load**: `references/vision-capabilities.md` + `templates/vision-image.ts`

---

### Extended Thinking Mode

```typescript
const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 4096,
  thinking: {
    type: 'enabled',
    budget_tokens: 2000,
  },
  messages: [{ role: 'user', content: 'Solve complex problem...' }],
});

const thinking = message.content.find(b => b.type === 'thinking')?.thinking;
const answer = message.content.find(b => b.type === 'text')?.text;
```

**Load**: `templates/extended-thinking.ts`

---

## Model Versions (Current)

**Latest models:**
- `claude-sonnet-4-5-20250929` - Recommended (best performance)
- `claude-sonnet-4-20250514` - Stable version
- `claude-3-7-sonnet-20250219` - Previous generation
- `claude-3-5-sonnet-20241022` - Legacy

**Always pin to specific version** (not `-latest` suffix)

---

## When to Load References

### Load `references/setup-guide.md` when:
- First-time Claude API user needing complete setup walkthrough
- Setting up Node.js or Cloudflare Workers from scratch
- Need production deployment checklist and platform-specific tips
- Troubleshooting basic setup issues (API keys, authentication, environment)

### Load `references/prompt-caching-guide.md` when:
- Want to reduce costs by 90% on repeated content
- Using large system prompts, documents, or codebases in context
- Need detailed caching strategy with benchmarks and cost calculations
- Optimizing multi-turn conversations with conversation history caching
- Troubleshooting cache activation issues or cache misses

### Load `references/tool-use-patterns.md` when:
- Implementing function calling and tool definitions
- Need tool execution loop patterns and multi-turn tool use
- Want Zod validation examples for type-safe tools
- Troubleshooting tool use response format errors

### Load `references/vision-capabilities.md` when:
- Processing images with Claude (OCR, analysis, description)
- Need image format requirements and validation logic
- Want vision use cases and best practices
- Combining vision with tools or prompt caching

### Load `references/api-reference.md` when:
- Need complete API parameter reference and request/response schemas
- Looking up specific fields or content block types
- Want endpoint details, authentication headers, or model IDs
- Need streaming event types and SSE format details

### Load `references/top-errors.md` when:
- Encountering API errors (all 12 documented errors with solutions)
- Need error code reference (400, 401, 429, 529, etc.)
- Want comprehensive prevention strategies
- Implementing robust error handling and retry logic

### Load `references/rate-limits.md` when:
- Planning high-volume usage and scaling strategy
- Encountering 429 rate limit errors repeatedly
- Need tier limits information and upgrade path
- Optimizing request patterns to stay within limits

---

## Using Bundled Resources

### References (references/)

- **setup-guide.md** - Complete setup (Node.js + Cloudflare Workers + Next.js)
- **api-reference.md** - Complete API parameter reference + schemas
- **prompt-caching-guide.md** - 90% cost savings guide + benchmarks
- **tool-use-patterns.md** - Function calling patterns + Zod examples
- **vision-capabilities.md** - Image understanding guide + validation
- **top-errors.md** - All 12 errors with solutions + prevention
- **rate-limits.md** - Limits by tier + best practices

### Templates (templates/)

- **basic-chat.ts** - Simple chat example
- **streaming-chat.ts** - Streaming implementation with SSE
- **prompt-caching.ts** - Caching example with benchmarks
- **tool-use-basic.ts** - Basic tool use pattern
- **tool-use-advanced.ts** - Advanced multi-turn tool patterns
- **vision-image.ts** - Vision example with validation
- **extended-thinking.ts** - Extended thinking mode
- **error-handling.ts** - Complete error handling
- **nodejs-example.ts** - Complete Node.js app
- **cloudflare-worker.ts** - Complete CF Worker
- **nextjs-api-route.ts** - Next.js API route
- **package.json** - Dependencies

---

## Platform Integration

**Node.js**: `bun add @anthropic-ai/sdk` → Use templates: `nodejs-example.ts`, `basic-chat.ts`

**Cloudflare Workers**: Use fetch API → Use templates: `cloudflare-worker.ts`

**Next.js**: `bun add @anthropic-ai/sdk` → Use templates: `nextjs-api-route.ts`

---

## Production Checklist

- [ ] API key stored securely (environment variable)
- [ ] Error handling implemented (401, 429, 400, 529)
- [ ] Rate limiting with exponential backoff
- [ ] Prompt caching enabled for repeated content
- [ ] Streaming for long responses
- [ ] Input validation + output sanitization
- [ ] Monitoring and cost tracking
- [ ] Timeouts configured
- [ ] Model version pinned
- [ ] max_tokens set appropriately

---

## Related Skills

- **openai-api** - OpenAI Chat Completions for comparison
- **claude-agent-sdk** - Higher-level Claude SDK
- **ai-sdk-core** - Vercel AI SDK (supports Claude)

---

## Official Documentation

- **Messages API**: https://docs.anthropic.com/en/api/messages
- **Prompt Caching**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- **Tool Use**: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- **Vision**: https://docs.anthropic.com/en/docs/build-with-claude/vision
- **Extended Thinking**: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking

---

**Questions? Issues?**

1. Check `references/top-errors.md` for error solutions
2. Review `references/setup-guide.md` for complete setup
3. See `references/prompt-caching-guide.md` for cost optimization
4. Load templates from `templates/` for working examples
