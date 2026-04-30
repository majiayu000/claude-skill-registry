---
name: cloudflare-agents
description: Build AI agents on Cloudflare Workers with MCP integration, tool use, and LLM providers.
license: MIT
---

# Cloudflare Agents

**Last Updated**: 2025-11-21

## Quick Start

```typescript
export default {
  async fetch(request, env, ctx) {
    const agent = {
      tools: [
        { name: 'getTodo', handler: async ({id}) => ({id, title: 'Task'}) }
      ],
      async run(input) {
        return await processWithLLM(input, this.tools);
      }
    };
    
    return Response.json(await agent.run(await request.text()));
  }
};
```

## Core Features

- **Tool Integration**: Register and execute tools
- **LLM Providers**: OpenAI, Anthropic, Google Gemini
- **MCP Protocol**: Model Context Protocol support
- **Cloudflare Bindings**: D1, KV, R2, Durable Objects

## Agent Pattern

```typescript
const agent = {
  tools: [...],
  systemPrompt: 'You are a helpful assistant',
  model: 'gpt-4o',
  async run(input) {
    // Process with LLM
  }
};
```

## Resources

### Core Documentation
- `references/patterns-concepts.md` (317 lines) - What is Cloudflare Agents, patterns & concepts, critical rules, known issues prevention
- `references/configuration-guide.md` (152 lines) - Complete configuration deep dive
- `references/agent-api.md` (115 lines) - Complete Agent Class API reference

### Integration Guides
- `references/http-sse-guide.md` (74 lines) - HTTP & Server-Sent Events
- `references/websockets-guide.md` (110 lines) - WebSocket integration
- `references/state-management.md` (388 lines) - State management, scheduled tasks, workflows
- `references/mcp-integration.md` (130 lines) - Model Context Protocol integration

### Advanced Features
- `references/advanced-features.md` (637 lines) - Browser automation, RAG, AI model integration, calling agents, client APIs

### Error Reference
- `references/error-catalog.md` (10 lines) - Common errors and solutions

### Templates
- `templates/basic-agent.ts` - Basic agent setup
- `templates/browser-agent.ts` - Browser automation
- `templates/calling-agents-worker.ts` - Calling other agents
- `templates/chat-agent-streaming.ts` - Streaming chat agent
- `templates/hitl-agent.ts` - Human-in-the-loop
- `templates/mcp-server-basic.ts` - MCP server integration
- `templates/rag-agent.ts` - RAG implementation
- `templates/react-useagent-client.tsx` - React client integration
- `templates/scheduled-agent.ts` - Scheduled tasks
- `templates/state-sync-agent.ts` - State synchronization
- `templates/websocket-agent.ts` - WebSocket agent
- `templates/workflow-agent.ts` - Workflows integration
- `templates/wrangler-agents-config.jsonc` - Wrangler configuration

**Official Docs**: https://developers.cloudflare.com/cloudflare-for-platforms/cloudflare-agents/
