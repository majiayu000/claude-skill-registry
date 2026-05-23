---
name: teams-anthropic-integration
description: Use @youdotcom-oss/teams-anthropic to add Anthropic Claude models (Opus, Sonnet, Haiku) to Microsoft Teams.ai applications. Optionally integrate You.com MCP server for web search and content extraction.
license: MIT
compatibility: Node.js 18+, @microsoft/teams.ai
metadata:
  author: youdotcom-oss
  category: enterprise-integration
  version: "1.1.0"
  keywords: microsoft-teams,teams-ai,anthropic,claude,mcp,you.com,web-search,content-extraction
---

# Build Teams.ai Apps with Anthropic Claude

Use `@youdotcom-oss/teams-anthropic` to add Claude models (Opus, Sonnet, Haiku) to Microsoft Teams.ai applications. Optionally integrate You.com MCP server for web search and content extraction.

## Choose Your Path

**Path A: Basic Setup** (Recommended for getting started)
- Use Anthropic Claude models in Teams.ai
- Chat, streaming, function calling
- No additional dependencies

**Path B: With You.com MCP** (For web search capabilities)
- Everything in Path A
- Web search and content extraction via You.com
- Real-time information access

## Decision Point

**Ask: Do you need web search and content extraction in your Teams app?**

- **NO** → Use **Path A: Basic Setup** (simpler, faster)
- **YES** → Use **Path B: With You.com MCP**

---

## Path A: Basic Setup

Use Anthropic Claude models in your Teams.ai app without additional dependencies.

### A1. Install Package

```bash
npm install @youdotcom-oss/teams-anthropic @anthropic-ai/sdk @microsoft/teams.ai
```

### A2. Get Anthropic API Key

Get your API key from [console.anthropic.com](https://console.anthropic.com/)

```bash
# Add to .env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### A3. Ask: New or Existing App?

- **New Teams app**: Use entire template below
- **Existing app**: Add Claude model to existing setup

### A4. Basic Template

**For NEW Apps:**

```typescript
import { App } from '@microsoft/teams.apps';
import { AnthropicChatModel, AnthropicModel } from '@youdotcom-oss/teams-anthropic';

if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY environment variable is required');
}

const model = new AnthropicChatModel({
  model: AnthropicModel.CLAUDE_SONNET_4_5,
  apiKey: process.env.ANTHROPIC_API_KEY,
  requestOptions: {
    max_tokens: 2048,
    temperature: 0.7,
  },
});

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });

  const response = await model.send(
    { role: 'user', content: activity.text }
  );

  if (response.content) {
    await send(response.content);
  }
});

app.start().catch(console.error);
```

**For EXISTING Apps:**

Add to your existing imports:
```typescript
import { AnthropicChatModel, AnthropicModel } from '@youdotcom-oss/teams-anthropic';
```

Replace your existing model:
```typescript
const model = new AnthropicChatModel({
  model: AnthropicModel.CLAUDE_SONNET_4_5,
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

### A5. Choose Your Model

```typescript
// Most capable - best for complex tasks
AnthropicModel.CLAUDE_OPUS_4_5

// Balanced intelligence and speed (recommended)
AnthropicModel.CLAUDE_SONNET_4_5

// Fast and efficient
AnthropicModel.CLAUDE_HAIKU_3_5
```

### A6. Test Basic Setup

```bash
npm start
```

Send a message in Teams to verify Claude responds.

---

## Path B: With You.com MCP

Add web search and content extraction to your Claude-powered Teams app.

### B1. Install Packages

```bash
npm install @youdotcom-oss/teams-anthropic @anthropic-ai/sdk @microsoft/teams.ai @microsoft/teams.mcpclient
```

### B2. Get API Keys

- **Anthropic API key**: [console.anthropic.com](https://console.anthropic.com/)
- **You.com API key**: [you.com/platform/api-keys](https://you.com/platform/api-keys)

```bash
# Add to .env
ANTHROPIC_API_KEY=your-anthropic-api-key
YDC_API_KEY=your-you-com-api-key
```

### B3. Ask: New or Existing App?

- **New Teams app**: Use entire template below
- **Existing app**: Add MCP to existing Claude setup

### B4. MCP Template

**For NEW Apps:**

```typescript
import { App } from '@microsoft/teams.apps';
import { ChatPrompt } from '@microsoft/teams.ai';
import { ConsoleLogger } from '@microsoft/teams.common';
import { McpClientPlugin } from '@microsoft/teams.mcpclient';
import {
  AnthropicChatModel,
  AnthropicModel,
  getYouMcpConfig,
} from '@youdotcom-oss/teams-anthropic';

// Validate environment
if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY environment variable is required');
}

if (!process.env.YDC_API_KEY) {
  throw new Error('YDC_API_KEY environment variable is required');
}

// Configure logger
const logger = new ConsoleLogger('mcp-client', { level: 'info' });

// Create prompt with MCP integration
const prompt = new ChatPrompt(
  {
    instructions: 'You are a helpful assistant with access to web search and content extraction. Use these tools to provide accurate, up-to-date information.',
    model: new AnthropicChatModel({
      model: AnthropicModel.CLAUDE_SONNET_4_5,
      apiKey: process.env.ANTHROPIC_API_KEY,
      requestOptions: {
        max_tokens: 2048,
      },
    }),
  },
  [new McpClientPlugin({ logger })],
).usePlugin('mcpClient', getYouMcpConfig());

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });

  const result = await prompt.send(activity.text);
  if (result.content) {
    await send(result.content);
  }
});

app.start().catch(console.error);
```

**For EXISTING Apps with Claude:**

If you already have Path A setup, add MCP integration:

1. **Install MCP dependencies:**
   ```bash
   npm install @microsoft/teams.mcpclient
   ```

2. **Add imports:**
   ```typescript
   import { ChatPrompt } from '@microsoft/teams.ai';
   import { ConsoleLogger } from '@microsoft/teams.common';
   import { McpClientPlugin } from '@microsoft/teams.mcpclient';
   import { getYouMcpConfig } from '@youdotcom-oss/teams-anthropic';
   ```

3. **Validate You.com API key:**
   ```typescript
   if (!process.env.YDC_API_KEY) {
     throw new Error('YDC_API_KEY environment variable is required');
   }
   ```

4. **Replace model with ChatPrompt:**
   ```typescript
   const logger = new ConsoleLogger('mcp-client', { level: 'info' });

   const prompt = new ChatPrompt(
     {
       instructions: 'Your instructions here',
       model: new AnthropicChatModel({
         model: AnthropicModel.CLAUDE_SONNET_4_5,
         apiKey: process.env.ANTHROPIC_API_KEY,
       }),
     },
     [new McpClientPlugin({ logger })],
   ).usePlugin('mcpClient', getYouMcpConfig());
   ```

5. **Use prompt.send() instead of model.send():**
   ```typescript
   const result = await prompt.send(activity.text);
   ```

### B5. Test MCP Integration

```bash
npm start
```

Ask Claude a question that requires web search:
- "What are the latest developments in AI?"
- "Search for React documentation"
- "Extract content from https://example.com"

---

## Available Claude Models

| Model | Enum | Best For |
|-------|------|----------|
| Claude Opus 4.5 | `AnthropicModel.CLAUDE_OPUS_4_5` | Complex tasks, highest capability |
| Claude Sonnet 4.5 | `AnthropicModel.CLAUDE_SONNET_4_5` | Balanced intelligence and speed (recommended) |
| Claude Haiku 3.5 | `AnthropicModel.CLAUDE_HAIKU_3_5` | Fast responses, efficiency |
| Claude Sonnet 3.5 | `AnthropicModel.CLAUDE_SONNET_3_5` | Previous generation, stable |

## Advanced Features

### Streaming Responses

```typescript
const response = await model.send(
  { role: 'user', content: 'Write a short story' },
  {
    onChunk: async (delta) => {
      // Stream each token as it arrives
      process.stdout.write(delta);
    },
  }
);
```

### Function Calling

```typescript
const response = await model.send(
  { role: 'user', content: 'What is the weather in San Francisco?' },
  {
    functions: {
      get_weather: {
        description: 'Get the current weather for a location',
        parameters: {
          location: { type: 'string', description: 'City name' },
        },
        handler: async (args: { location: string }) => {
          // Your API call here
          return { temperature: 72, conditions: 'Sunny' };
        },
      },
    },
  }
);
```

### Conversation Memory

```typescript
import { LocalMemory } from '@microsoft/teams.ai';

const memory = new LocalMemory();

// First message
await model.send(
  { role: 'user', content: 'My name is Alice' },
  { messages: memory }
);

// Second message - Claude remembers
const response = await model.send(
  { role: 'user', content: 'What is my name?' },
  { messages: memory }
);
// Response: "Your name is Alice."
```

## Validation Checklist

### Path A Checklist

- [ ] Package installed: `@youdotcom-oss/teams-anthropic`
- [ ] Environment variable set: `ANTHROPIC_API_KEY`
- [ ] Model configured with `AnthropicChatModel`
- [ ] Model selection chosen (Opus/Sonnet/Haiku)
- [ ] App tested with basic messages

### Path B Checklist

- [ ] All Path A items completed
- [ ] Additional package installed: `@microsoft/teams.mcpclient`
- [ ] Environment variable set: `YDC_API_KEY`
- [ ] Logger configured
- [ ] ChatPrompt configured with `getYouMcpConfig()`
- [ ] App tested with web search queries

## Common Issues

### Path A Issues

**"Cannot find module @youdotcom-oss/teams-anthropic"**
```bash
npm install @youdotcom-oss/teams-anthropic @anthropic-ai/sdk
```

**"ANTHROPIC_API_KEY environment variable is required"**
- Get key from: https://console.anthropic.com/
- Add to .env: `ANTHROPIC_API_KEY=your-key-here`

**"Invalid model identifier"**
- Use enum: `AnthropicModel.CLAUDE_SONNET_4_5`
- Don't use string: `'claude-sonnet-4-5-20250929'`

### Path B Issues

**"YDC_API_KEY environment variable is required"**
- Get key from: https://you.com/platform/api-keys
- Add to .env: `YDC_API_KEY=your-key-here`

**"MCP connection fails"**
- Verify API key is valid at https://you.com/platform/api-keys
- Check network connectivity
- Review logger output for details

**"Cannot find module @microsoft/teams.mcpclient"**
```bash
npm install @microsoft/teams.mcpclient
```

## getYouMcpConfig() Utility

Automatically configures You.com MCP connection:
- **URL**: `https://api.you.com/mcp`
- **Authentication**: Bearer token from `YDC_API_KEY`
- **User-Agent**: Includes package version for telemetry

```typescript
// Option 1: Use environment variable (recommended)
getYouMcpConfig()

// Option 2: Custom API key
getYouMcpConfig({ apiKey: 'your-custom-key' })
```

## Resources

* **Package**: https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/teams-anthropic
* **You.com MCP**: https://documentation.you.com/developer-resources/mcp-server
* **Anthropic API**: https://console.anthropic.com/
* **You.com API Keys**: https://you.com/platform/api-keys
