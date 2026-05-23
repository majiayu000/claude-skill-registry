---
name: ai-sdk-integration
description: Integrate Vercel AI SDK applications with You.com tools (web search, AI agent, content extraction). Use when developer mentions AI SDK, Vercel AI SDK, generateText, streamText, or You.com integration with AI SDK.
license: MIT
compatibility: Requires Node.js 18+ and npm/bun/yarn/pnpm
metadata:
  author: youdotcom-oss
  version: "0.2.0"
  category: workflow
  keywords: vercel,ai-sdk,you.com,integration,anthropic,openai, web-search, search, crawling, scraping
---

# Integrate AI SDK with You.com Tools

Interactive workflow to add You.com tools to your Vercel AI SDK application using `@youdotcom-oss/ai-sdk-plugin`.

## Workflow

1. **Ask: Package Manager**
   * Which package manager? (npm, bun, yarn, pnpm)
   * Install package using their choice:
     ```bash
     npm install @youdotcom-oss/ai-sdk-plugin
     # or bun add @youdotcom-oss/ai-sdk-plugin
     # or yarn add @youdotcom-oss/ai-sdk-plugin
     # or pnpm add @youdotcom-oss/ai-sdk-plugin
     ```

2. **Ask: Environment Variable Name**
   * Using standard `YDC_API_KEY`?
   * Or custom name? (if custom, get the name)
   * Have they set it in their environment?
   * If NO: Guide them to get key from https://you.com/platform/api-keys

3. **Ask: Which AI SDK Functions?**
   * Do they use `generateText()`?
   * Do they use `streamText()`?
   * Both?

4. **Ask: Existing Files or New Files?**
   * EXISTING: Ask which file(s) to edit
   * NEW: Ask where to create file(s) and what to name them

5. **For Each File, Ask:**
   * Which tools to add?
     - `youSearch` (web search)
     - `youExpress` (AI agent)
     - `youContents` (content extraction)
     - Multiple? (which combination?)
   * Using `generateText()` or `streamText()` in this file?
   * Which AI provider model? (to determine if stopWhen needed)

6. **Reference Templates**

   Templates are available in the skill assets directory:
   * `assets/generate-text.ts` - Template for generateText() usage
   * `assets/streaming-text.ts` - Template for streamText() usage

7. **Update/Create Files**

   For each file:
   * Reference template (generateText or streamText based on their answer)
   * Add import for selected tools
   * If EXISTING file: Find their generateText/streamText call and add tools object
   * If NEW file: Create file with template structure
   * Tool invocation pattern based on env var name:
     - Standard `YDC_API_KEY`: `youSearch()`
     - Custom name: `youSearch({ apiKey: process.env.CUSTOM_NAME })`
   * Add selected tools to tools object
   * If streamText + Anthropic: Add stopWhen parameter

## Tool Invocation Patterns

Based on env var name from step 2:

**Standard YDC_API_KEY:**
```typescript
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

tools: {
  search: youSearch(),
}
```

**Custom env var:**
```typescript
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const apiKey = process.env.THEIR_CUSTOM_NAME;

tools: {
  search: youSearch({ apiKey }),
}
```

**Multiple tools with standard env var:**
```typescript
import { youSearch, youExpress, youContents } from '@youdotcom-oss/ai-sdk-plugin';

tools: {
  search: youSearch(),
  agent: youExpress(),
  extract: youContents(),
}
```

**Multiple tools with custom env var:**
```typescript
import { youSearch, youExpress, youContents } from '@youdotcom-oss/ai-sdk-plugin';

const apiKey = process.env.THEIR_CUSTOM_NAME;

tools: {
  search: youSearch({ apiKey }),
  agent: youExpress({ apiKey }),
  extract: youContents({ apiKey }),
}
```

## Available Tools

### youSearch
Web and news search - model determines parameters (query, count, country, etc.)

### youExpress
AI agent with web context - model determines parameters (input, tools)

### youContents
Web page content extraction - model determines parameters (urls, format)

## Key Template Patterns

Templates show:
* Import statements (AI SDK + provider + You.com tools)
* Env var validation (optional for new files)
* Tool configuration based on env var
* generateText/streamText usage with tools
* Result handling (especially textStream destructuring for streamText)
* Anthropic streaming pattern (stopWhen: stepCountIs(3))

## Implementation Checklist

For each file being updated/created:

- [ ] Import added for selected tools
- [ ] If custom env var: Variable declared with correct name
- [ ] tools object added to generateText/streamText
- [ ] Each selected tool invoked correctly:
  - Standard env: `toolName()`
  - Custom env: `toolName({ apiKey })`
- [ ] If streamText: Destructured `const { textStream } = ...`
- [ ] If Anthropic + streamText: Added `stopWhen: stepCountIs(3)`

Global checklist:

- [ ] Package installed with their package manager
- [ ] Env var set in their environment
- [ ] All files updated/created
- [ ] Ready to test

## Common Issues

**Issue**: "Cannot find module @youdotcom-oss/ai-sdk-plugin"
**Fix**: Install with their package manager

**Issue**: "YDC_API_KEY (or custom name) environment variable is required"
**Fix**: Set in their environment (get key: https://you.com/platform/api-keys)

**Issue**: "Tool execution fails with 401"
**Fix**: Verify API key is valid

**Issue**: "Incomplete or missing response"
**Fix**: If using streamText, increase the step count. Start with 3 and iterate up as needed (see README troubleshooting)

**Issue**: "textStream is not iterable"
**Fix**: Destructure: `const { textStream } = streamText(...)`

**Issue**: "Custom env var not working"
**Fix**: Pass to each tool: `youSearch({ apiKey })`

## Advanced: Tool Development Patterns

For developers creating custom AI SDK tools or contributing to @youdotcom-oss/ai-sdk-plugin:

### Tool Function Structure

Each tool function follows this pattern:

```typescript
export const youToolName = (config: YouToolsConfig = {}) => {
  const apiKey = config.apiKey ?? process.env.YDC_API_KEY;

  return tool({
    description: 'Tool description for AI model',
    inputSchema: ZodSchema,
    execute: async (params) => {
      if (!apiKey) {
        throw new Error('YDC_API_KEY is required');
      }

      const response = await callApiUtility({
        params,
        YDC_API_KEY: apiKey,
        getUserAgent,
      });

      // Return raw API response for maximum flexibility
      return response;
    },
  });
};
```

### Input Schemas Enable Smart Queries

Always use schemas from `@youdotcom-oss/mcp`:

```typescript
// ✅ Import from @youdotcom-oss/mcp
import { SearchQuerySchema } from '@youdotcom-oss/mcp';

export const youSearch = (config: YouToolsConfig = {}) => {
  return tool({
    description: '...',
    inputSchema: SearchQuerySchema,  // Enables AI to use all search parameters
    execute: async (params) => { ... },
  });
};

// ❌ Don't duplicate or simplify schemas
const MySearchSchema = z.object({ query: z.string() });  // Missing filters!
```

**Why this matters:**
- Rich schemas enable AI to use advanced query parameters (filters, freshness, country, etc.)
- AI can construct more intelligent queries based on user intent
- Prevents duplicating schema definitions across packages
- Ensures consistency with MCP server schemas

### API Key Handling

Always provide environment variable fallback and validate before API calls:

```typescript
// ✅ Automatic environment variable fallback
const apiKey = config.apiKey ?? process.env.YDC_API_KEY;

// ✅ Check API key in execute function
execute: async (params) => {
  if (!apiKey) {
    throw new Error('YDC_API_KEY is required');
  }
  const response = await callApi(...);
}
```

### Response Format

Always return raw API response for maximum flexibility:

```typescript
// ✅ Return raw API response
execute: async (params) => {
  const response = await fetchSearchResults({
    searchQuery: params,
    YDC_API_KEY: apiKey,
    getUserAgent,
  });

  return response;  // Raw response for maximum flexibility
}

// ❌ Don't format or transform responses
return {
  text: formatResponse(response),
  data: response,
};
```

**Why raw responses?**
- Maximum flexibility for AI SDK to process results
- No information loss from formatting
- AI SDK handles presentation layer
- Easier to debug (see actual API response)

### Tool Descriptions

Write descriptions that guide AI behavior:

```typescript
// ✅ Clear guidance for AI model
description: 'Search the web for current information, news, articles, and content using You.com. Returns web results with snippets and news articles. Use this when you need up-to-date information or facts from the internet.'

// ❌ Too brief
description: 'Search the web'
```

## Additional Resources

* Package README: https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/ai-sdk-plugin
* Vercel AI SDK Docs: https://sdk.vercel.ai/docs
* You.com API: https://you.com/platform/api-keys
