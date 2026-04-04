---
name: claude-typescript-sdk
description: Build AI applications with the Anthropic TypeScript SDK. Use when creating Claude integrations, building agents, implementing tool use, streaming responses, or working with the @anthropic-ai/sdk package.
---

# Claude TypeScript SDK

## Quick Start

```bash
npm install @anthropic-ai/sdk
export ANTHROPIC_API_KEY='your-key'
```

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
const message = await client.messages.create({
  model: 'claude-opus-4-5-20251101',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

## Core Patterns

### Basic Message
```typescript
const message = await client.messages.create({
  model: 'claude-opus-4-5-20251101',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Your prompt' }],
});
console.log(message.content[0].type === 'text' && message.content[0].text);
```

### Streaming
```typescript
const stream = client.messages.stream({
  model: 'claude-opus-4-5-20251101',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Write a poem' }],
});
stream.on('text', (text) => process.stdout.write(text));
const final = await stream.finalMessage();
```

### Tool Use
```typescript
const tools: Anthropic.Tool[] = [{
  name: 'get_weather',
  description: 'Get weather for a location',
  input_schema: {
    type: 'object',
    properties: {
      location: { type: 'string', description: 'City name' },
    },
    required: ['location'],
  },
}];

const response = await client.messages.create({
  model: 'claude-opus-4-5-20251101',
  max_tokens: 1024,
  tools,
  messages: [{ role: 'user', content: 'Weather in NYC?' }],
});
```

For detailed examples, see [REFERENCE.md](REFERENCE.md).

## Available Models

- `claude-opus-4-5-20251101` - Most capable
- `claude-sonnet-4-5-20250929` - Balanced
- `claude-haiku-4-5-20251001` - Fastest

## Error Handling

```typescript
try {
  const message = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error(`Status: ${error.status}, Message: ${error.message}`);
  }
}
```

## Resources

- [TypeScript SDK GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
- [API Documentation](https://docs.claude.com)
- [Agent SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)
