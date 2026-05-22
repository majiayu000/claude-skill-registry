---
name: ai-sdk-core
description: Vercel AI SDK v5 for backend AI (text generation, structured output, tools, agents). Multi-provider. Use for server-side AI or encountering AI_APICallError, AI_NoObjectGeneratedError, streaming failures.

  Keywords: ai sdk core, vercel ai sdk, generateText, streamText, generateObject, streamObject,
  ai sdk node, ai sdk server, zod ai schema, ai tools calling, ai agent class, openai sdk, anthropic sdk,
  google gemini sdk, workers-ai-provider, ai streaming backend, multi-provider ai, ai sdk errors,
  AI_APICallError, AI_NoObjectGeneratedError, streamText fails, worker startup limit ai
license: MIT
---

# AI SDK Core

Production-ready backend AI with Vercel AI SDK v5.

**Last Updated**: 2025-11-21

## Table of Contents
1. [Quick Start](#quick-start-5-minutes)
2. [Core Functions](#core-functions)
3. [Provider Setup & Configuration](#provider-setup--configuration)
4. [Tool Calling & Agents](#tool-calling--agents)
5. [Critical v4→v5 Migration](#critical-v4v5-migration)
6. [Top 12 Errors & Solutions](#top-12-errors--solutions)
7. [Production Best Practices](#production-best-practices)
8. [When to Load References](#when-to-load-references)
9. [When to Use This Skill](#when-to-use-this-skill)
10. [Dependencies & Versions](#dependencies--versions)
11. [Links to Official Documentation](#links-to-official-documentation)
12. [Templates & References](#templates--references)

---

## Quick Start (5 Minutes)

### Installation

```bash
bun add ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google workers-ai-provider zod  # preferred
# or: npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google workers-ai-provider zod
```

### Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENERATIVE_AI_API_KEY=...
```

### First Example: Generate Text

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'What is TypeScript?',
});

console.log(result.text);
```

### First Example: Streaming Chat

```typescript
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const stream = streamText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  messages: [
    { role: 'user', content: 'Tell me a story' },
  ],
});

for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

### First Example: Structured Output

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const result = await generateObject({
  model: openai('gpt-4'),
  schema: z.object({
    name: z.string(),
    age: z.number(),
    skills: z.array(z.string()),
  }),
  prompt: 'Generate a person profile for a software engineer',
});

console.log(result.object);
// { name: "Alice", age: 28, skills: ["TypeScript", "React"] }
```

---

## Core Functions

**Load `references/core-functions.md` for complete API reference** of all 4 core functions.

### Quick Overview

AI SDK v5 provides 4 core functions:

| Function | Output | Streaming | Use Case |
|----------|--------|-----------|----------|
| `generateText()` | Text | No | Batch processing, simple completions |
| `streamText()` | Text | Yes | Chat UIs, long responses |
| `generateObject()` | Structured | No | Data extraction, JSON generation |
| `streamObject()` | Structured | Yes | Real-time forms, progressive UIs |

### Basic Example

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Explain quantum computing',
});

console.log(result.text);
```

**→ Load `references/core-functions.md` for:** Complete signatures, tool usage patterns, error handling, streaming examples, comparison table

---

## Provider Setup & Configuration

**Load `references/provider-setup.md` for complete setup instructions** for all providers.

### Quick Overview

AI SDK v5 supports 4 major providers:

| Provider | Environment Variable | Latest Models |
|----------|---------------------|---------------|
| OpenAI | `OPENAI_API_KEY` | GPT-5, GPT-4 Turbo |
| Anthropic | `ANTHROPIC_API_KEY` | Claude Sonnet 4.5, Opus 4 |
| Google | `GOOGLE_GENERATIVE_AI_API_KEY` | Gemini 2.5 Pro/Flash |
| Cloudflare | Workers AI binding | Llama 3.1, Qwen 2.5 |

### Basic Setup

```typescript
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

// API key from environment
const result = await generateText({
  model: openai('gpt-4-turbo'),
  prompt: 'Hello',
});
```

**→ Load `references/provider-setup.md` for:** Complete API configuration, rate limiting, error handling, Cloudflare Workers optimization, model selection guides

---

## Tool Calling & Agents

**Load `references/tools-and-agents.md` for complete tool and agent documentation**.

### Quick Overview

Tools allow models to call external functions. Agents manage multi-step workflows.

**v5 Tool Changes:**
- `parameters` → `inputSchema` (Zod schema)
- Tool properties: `args` → `input`, `result` → `output`
- `maxSteps` → `stopWhen(stepCountIs(n))`

### Basic Tool Example

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

const result = await generateText({
  model: openai('gpt-4'),
  tools: {
    weather: tool({
      description: 'Get weather for a location',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => {
        return { temperature: 72, condition: 'sunny' };
      },
    }),
  },
  prompt: 'What is the weather in Tokyo?',
});
```

**→ Load `references/tools-and-agents.md` for:** Agent class usage, multi-step execution, dynamic tools, stop conditions

---

## Critical v4→v5 Migration

**Load `references/v4-to-v5-migration.md` for complete migration guide**.

### Key Breaking Changes

AI SDK v5 has 9 major breaking changes:
- `maxTokens` → `maxOutputTokens`
- `parameters` → `inputSchema` (Zod)
- `maxSteps` → `stopWhen(stepCountIs(n))`
- `CoreMessage` → `ModelMessage`
- Package reorganization (`ai/rsc` → `@ai-sdk/rsc`)

### Automated Migration

```bash
bunx ai migrate  # Auto-migrates most changes
```

**→ Load `references/v4-to-v5-migration.md` for:** Complete breaking changes list, migration examples, checklist, official migration guide link

---

## Top 12 Errors & Solutions

### 1. AI_APICallError

**Cause:** API request failed (network, auth, rate limit).

**Solution:**
```typescript
import { AI_APICallError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_APICallError) {
    console.error('API call failed:', error.message);
    console.error('Status code:', error.statusCode);
    console.error('Response:', error.responseBody);

    // Check common causes
    if (error.statusCode === 401) {
      // Invalid API key
    } else if (error.statusCode === 429) {
      // Rate limit - implement backoff
    } else if (error.statusCode >= 500) {
      // Provider issue - retry
    }
  }
}
```

**Prevention:**
- Validate API keys at startup
- Implement retry logic with exponential backoff
- Monitor rate limits
- Handle network errors gracefully

---

### 2. AI_NoObjectGeneratedError

**Cause:** Model didn't generate valid object matching schema.

**Solution:**
```typescript
import { AI_NoObjectGeneratedError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4'),
    schema: z.object({ /* complex schema */ }),
    prompt: 'Generate data',
  });
} catch (error) {
  if (error instanceof AI_NoObjectGeneratedError) {
    console.error('No valid object generated');

    // Solutions:
    // 1. Simplify schema
    // 2. Add more context to prompt
    // 3. Provide examples in prompt
    // 4. Try different model (gpt-4 better than gpt-3.5 for complex objects)
  }
}
```

**Prevention:**
- Start with simple schemas, add complexity incrementally
- Include examples in prompt: "Generate a person like: { name: 'Alice', age: 30 }"
- Use GPT-4 for complex structured output
- Test schemas with sample data first

---

### 3. Worker Startup Limit (270ms+)

**Cause:** AI SDK v5 + Zod initialization overhead in Cloudflare Workers exceeds startup limits.

**Solution:**
```typescript
// BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
import { complexSchema } from './schemas';

const workersai = createWorkersAI({ binding: env.AI });

// GOOD: Lazy initialization inside handler
export default {
  async fetch(request, env) {
    const { createWorkersAI } = await import('workers-ai-provider');
    const workersai = createWorkersAI({ binding: env.AI });

    // Use workersai here
  }
}
```

**Prevention:**
- Move AI SDK imports inside route handlers
- Minimize top-level Zod schemas
- Monitor Worker startup time (must be <400ms)
- Use Wrangler's startup time reporting

**GitHub Issue:** Search for "Workers startup limit" in Vercel AI SDK issues

---

**→ Load `references/error-catalog.md` for errors #4-#12** with complete solutions.

**Remaining 9 errors:**
4. streamText Fails Silently (RESOLVED in v4.1.22)
5. AI_LoadAPIKeyError
6. AI_InvalidArgumentError
7. AI_NoContentGeneratedError
8. AI_TypeValidationError
9. AI_RetryError
10. Rate Limiting Errors
11. TypeScript Performance with Zod
12. Invalid JSON Response (Provider-Specific)

**For complete error catalog:**
See complete error reference at https://ai-sdk.dev/docs/reference/ai-sdk-errors

---

## Production Best Practices

**Load `references/production-guide.md` for complete production deployment guide**.

### Key Categories

1. **Performance**: Streaming patterns, token limits, provider caching, Zod optimization
2. **Error Handling**: try-catch patterns, retry logic, proper logging
3. **Cost Optimization**: Model selection, token limits, response caching
4. **Cloudflare Workers**: Lazy imports, startup monitoring, streaming responses
5. **Next.js/Vercel**: Server Actions, Server Components, loading states

### Quick Example

```typescript
// Use streaming for user-facing responses
const stream = streamText({
  model: openai('gpt-4'),
  prompt: 'Long essay',
  maxOutputTokens: 500,
  maxRetries: 3,
});

return stream.toDataStreamResponse();
```

**→ Load `references/production-guide.md` for:** Platform-specific patterns, deployment checklists, optimization strategies

---

## When to Load References

**Load `references/core-functions.md` when:**
- User needs complete API documentation for generateText, streamText, generateObject, or streamObject
- Questions about function signatures, parameters, or return types
- Need detailed tool usage patterns or streaming examples
- Troubleshooting function-specific errors

**Load `references/provider-setup.md` when:**
- Setting up OpenAI, Anthropic, Google, or Cloudflare Workers AI
- Configuring API keys or environment variables
- Troubleshooting provider-specific errors (rate limits, authentication)
- Questions about model selection or best practices for each provider
- Cloudflare Workers startup optimization needed

**Load `references/tools-and-agents.md` when:**
- Implementing tool calling or agent workflows
- Questions about Agent class vs raw generateText
- Setting up multi-step execution with stopWhen
- Dynamic tools or complex agentic patterns

**Load `references/v4-to-v5-migration.md` when:**
- Migrating existing v4 codebase to v5
- Questions about breaking changes
- Need migration examples or automated migration tool
- Troubleshooting migration-related errors

**Load `references/error-catalog.md` when:**
- User encounters any of the 12 common errors (beyond top 3 shown inline)
- Need complete error solutions with code examples
- Troubleshooting production errors
- Questions about error prevention strategies

**Load `references/production-guide.md` when:**
- Deploying to production (any platform)
- Performance optimization needed
- Cost optimization questions
- Platform-specific patterns (Cloudflare Workers, Next.js/Vercel)
- Error handling or logging strategies

---

## When to Use This Skill

### Use ai-sdk-core when:

- Building backend AI features (server-side text generation)
- Implementing server-side text generation (Node.js, Workers, Next.js)
- Creating structured AI outputs (JSON, forms, data extraction)
- Building AI agents with tools (multi-step workflows)
- Integrating multiple AI providers (OpenAI, Anthropic, Google, Cloudflare)
- Migrating from AI SDK v4 to v5
- Encountering AI SDK errors (AI_APICallError, AI_NoObjectGeneratedError, etc.)
- Using AI in Cloudflare Workers (with workers-ai-provider)
- Using AI in Next.js Server Components/Actions
- Need consistent API across different LLM providers

### Don't use this skill when:

- Building React chat UIs (use **ai-sdk-ui** skill instead)
- Need frontend hooks like useChat (use **ai-sdk-ui** skill instead)
- Need advanced topics like embeddings or image generation (check official docs)
- Building native Cloudflare Workers AI apps without multi-provider (use **cloudflare-workers-ai** skill instead)
- Need Generative UI / RSC (see https://ai-sdk.dev/docs/ai-sdk-rsc)

---

## Dependencies & Versions

```json
{
  "dependencies": {
    "ai": "^5.0.116",
    "@ai-sdk/openai": "^2.0.88",
    "@ai-sdk/anthropic": "^2.0.56",
    "@ai-sdk/google": "^2.0.51",
    "workers-ai-provider": "^2.0.0",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^24.10.1",
    "typescript": "^5.9.3"
  }
}
```

**Version Notes:**
- AI SDK v5.0.116+ (stable, latest as of December 2025)
- v6 is in beta - not covered in this skill
- **Zod compatibility**: This skill uses Zod 3.x, but AI SDK 5 officially supports both Zod 3.x and Zod 4.x (4.1.12 latest)
  - Zod 4 recommended for new projects (released August 2025)
  - Zod 4 has breaking changes: error APIs, `.default()` behavior, `ZodError.errors` removed
  - Some peer dependency warnings may occur with `zod-to-json-schema` when using Zod 4
  - See https://zod.dev/v4/changelog for migration guide
- Provider packages at 2.0+ for v5 compatibility

**Check Latest Versions:**
```bash
npm view ai version
npm view @ai-sdk/openai version
npm view @ai-sdk/anthropic version
npm view @ai-sdk/google version
npm view workers-ai-provider version
npm view zod version  # Check for Zod 4.x updates
```

---

## Links to Official Documentation

### Core Documentation

- **AI SDK Introduction:** https://ai-sdk.dev/docs/introduction
- **AI SDK Core Overview:** https://ai-sdk.dev/docs/ai-sdk-core/overview
- **Generating Text:** https://ai-sdk.dev/docs/ai-sdk-core/generating-text
- **Generating Structured Data:** https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
- **Tools and Tool Calling:** https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
- **Agents Overview:** https://ai-sdk.dev/docs/agents/overview
- **Foundations:** https://ai-sdk.dev/docs/foundations/overview

### Advanced Topics (Not Replicated in This Skill)

- **Embeddings:** https://ai-sdk.dev/docs/ai-sdk-core/embeddings
- **Image Generation:** https://ai-sdk.dev/docs/ai-sdk-core/generating-images
- **Transcription:** https://ai-sdk.dev/docs/ai-sdk-core/generating-transcriptions
- **Speech:** https://ai-sdk.dev/docs/ai-sdk-core/generating-speech
- **MCP Tools:** https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
- **Telemetry:** https://ai-sdk.dev/docs/ai-sdk-core/telemetry
- **Generative UI:** https://ai-sdk.dev/docs/ai-sdk-rsc

### Migration & Troubleshooting

- **v4→v5 Migration Guide:** https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- **All Error Types (28 total):** https://ai-sdk.dev/docs/reference/ai-sdk-errors
- **Troubleshooting Guide:** https://ai-sdk.dev/docs/troubleshooting

### Provider Documentation

- **OpenAI Provider:** https://ai-sdk.dev/providers/ai-sdk-providers/openai
- **Anthropic Provider:** https://ai-sdk.dev/providers/ai-sdk-providers/anthropic
- **Google Provider:** https://ai-sdk.dev/providers/ai-sdk-providers/google
- **All Providers (25+):** https://ai-sdk.dev/providers/overview
- **Community Providers:** https://ai-sdk.dev/providers/community-providers

### Cloudflare Integration

- **Workers AI Provider (Community):** https://ai-sdk.dev/providers/community-providers/cloudflare-workers-ai
- **Cloudflare Workers AI Docs:** https://developers.cloudflare.com/workers-ai/
- **workers-ai-provider GitHub:** https://github.com/cloudflare/ai/tree/main/packages/workers-ai-provider
- **Cloudflare AI SDK Configuration:** https://developers.cloudflare.com/workers-ai/configuration/ai-sdk/

### Vercel / Next.js Integration

- **Vercel AI SDK 5.0 Blog:** https://vercel.com/blog/ai-sdk-5
- **Next.js App Router Integration:** https://ai-sdk.dev/docs/getting-started/nextjs-app-router
- **Next.js Pages Router Integration:** https://ai-sdk.dev/docs/getting-started/nextjs-pages-router
- **Vercel Functions:** https://vercel.com/docs/functions
- **Vercel Streaming:** https://vercel.com/docs/functions/streaming

### GitHub & Community

- **GitHub Repository:** https://github.com/vercel/ai
- **GitHub Issues:** https://github.com/vercel/ai/issues
- **Discord Community:** https://discord.gg/vercel

---

## Templates & References

This skill includes:

- **13 Templates:** Ready-to-use code examples in `templates/`
- **5 Reference Docs:** Detailed guides in `references/`
- **1 Script:** Version checker in `scripts/`

All files are optimized for copy-paste into your project.

---

**Last Updated:** 2025-12-22
**Skill Version:** 1.1.0
**AI SDK Version:** 5.0.116+
