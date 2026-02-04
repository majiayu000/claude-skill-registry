---
name: vercel-ai-cortex-integrator
description: Analyzes codebase for structural, contextual, and semantic understanding, then fully integrates Vercel AI SDK 6 and Cortex Memory features using Nia for documentation research
triggers:
  - integrate vercel ai sdk
  - integrate cortex
  - integrate cortex memory
  - ai sdk 6 integration
  - cortex memory integration
  - upgrade to ai sdk 6
  - add persistent memory
  - add agent memory
---

# Vercel AI SDK 6 + Cortex Memory Full Integration Skill

## Overview

This skill performs comprehensive codebase analysis and integrates ALL features of Vercel AI SDK 6 and Cortex Memory (persistent memory SDK for AI agents). It uses Nia Knowledge Agent for real-time documentation lookup.

**Cortex Memory** (https://docs.cortexmemory.dev/) provides:
- Memory Spaces - per-user/per-project isolated memory containers
- Conversation History - automatic context injection from past messages
- Fact Extraction - distill and store discrete facts from conversations
- Semantic Search - vector similarity with recency bias
- Context Chains - multi-step retrieval and MoE routing
- Hive Mode - multiple AI agents sharing global memory
- A2A Communication - agent-to-agent coordination

## Execution Workflow

### Phase 1: Codebase Analysis (MANDATORY)

```
┌─────────────────────────────────────────────────────────────────┐
│                    STRUCTURAL ANALYSIS                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Directory Structure Mapping                                  │
│    - Identify src/, lib/, app/, components/, api/ directories   │
│    - Map file relationships and import graphs                   │
│    - Detect monorepo structure (apps/, packages/)               │
│                                                                 │
│ 2. Dependency Analysis                                          │
│    - Parse package.json for existing AI packages                │
│    - Check for: ai, @ai-sdk/*, openai, anthropic, etc.         │
│    - Identify version conflicts and peer dependencies          │
│                                                                 │
│ 3. Framework Detection                                          │
│    - Next.js (App Router vs Pages Router)                       │
│    - React/Vue/Svelte/Node.js patterns                         │
│    - TypeScript configuration                                   │
│    - Convex backend presence                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Execute these commands:**
```bash
# Find all AI-related files
Glob "**/*.{ts,tsx,js,jsx}" | Grep "ai|openai|anthropic|llm|chat|stream"

# Check package.json
Read package.json

# Find existing AI implementations
Grep "generateText|streamText|useChat|createAI" --type ts

# Check for MCP configurations
Glob "**/mcp*.{ts,json,js}"

# Check for existing memory implementations
Grep "cortex|memory|memorySpace|facts" --type ts
```

### Phase 2: Contextual Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONTEXTUAL UNDERSTANDING                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. Existing AI Patterns                                         │
│    - Chat implementations (useChat, useCompletion)              │
│    - Tool definitions and executions                            │
│    - Streaming patterns (streamText, streamObject)              │
│    - Agent patterns (if any)                                    │
│                                                                 │
│ 2. API Route Analysis                                           │
│    - /api/chat routes                                           │
│    - /api/completion routes                                     │
│    - Middleware and authentication                              │
│                                                                 │
│ 3. State Management                                             │
│    - Message persistence patterns                               │
│    - Context/conversation management                            │
│    - Tool state handling                                        │
│                                                                 │
│ 4. Memory Architecture                                          │
│    - User identification patterns                               │
│    - Session management                                         │
│    - Multi-tenant considerations                                │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 3: Nia Documentation Research (MANDATORY)

**ALWAYS execute these Nia commands before integration:**

```typescript
// 1. Search AI SDK 6 specific features
mcp__nia__search({
  query: "AI SDK 6 ToolLoopAgent tool approval structured output streaming",
  data_sources: "ai-sdk.dev"
})

// 2. Search Cortex Memory integration patterns
mcp__nia__search({
  query: "Cortex Memory integration memory spaces fact extraction hive mode",
  data_sources: "docs.cortexmemory.dev"
})

// 3. Read specific documentation pages
mcp__nia__doc_read({
  source_identifier: "ai-sdk.dev",
  path: "/agents/building-agents.md"
})

// 4. Read Cortex Memory getting started
mcp__nia__doc_read({
  source_identifier: "docs.cortexmemory.dev",
  path: "/integrations/vercel-ai-sdk/getting-started.md"
})

// 5. Deep research for complex patterns
mcp__nia__nia_deep_research_agent({
  query: "How to implement persistent memory for AI agents with Cortex Memory and Vercel AI SDK 6"
})
```

### Phase 4: Integration Implementation

## AI SDK 6 + Cortex Memory Features Checklist

Use TodoWrite to track all integration tasks:

```
[ ] Core SDK Installation
    - ai@beta
    - @ai-sdk/openai@beta (or other providers)
    - @ai-sdk/react@beta
    - @ai-sdk/mcp
    - @cortexmemory/sdk
    - @cortexmemory/vercel-ai-provider
    - convex

[ ] Agent Implementation (ToolLoopAgent)
    - Create agent definitions with instructions
    - Configure stopWhen conditions
    - Set up tool registrations
    - Add memory context injection

[ ] Cortex Memory Integration
    - Initialize CortexMemory client
    - Configure memory spaces (per-user/per-project)
    - Set up fact extraction
    - Implement semantic search
    - Configure conversation history

[ ] Memory-Aware Tools
    - Create recallMemory tool
    - Create storeMemory tool
    - Add memory context to prompts
    - Implement context chains

[ ] Tool Execution Approval
    - Add needsApproval to sensitive tools
    - Implement dynamic approval logic
    - Create approval UI components

[ ] Hive Mode (Multi-Agent)
    - Configure shared memory spaces
    - Set up A2A communication
    - Implement agent coordination

[ ] Structured Output
    - Add Output.object() configurations
    - Define Zod schemas for outputs
    - Handle partialOutputStream

[ ] MCP Integration
    - Set up MCP client (HTTP transport)
    - Configure tool schema discovery
    - Implement resource handling

[ ] UI Integration
    - Update useChat hooks with memory
    - Implement tool invocation views
    - Add streaming UI components

[ ] Verification
    - All tests pass
    - TypeScript types correct
    - Build succeeds
    - Memory persists across sessions
```

## Implementation Templates

### 1. Cortex Memory Client Setup

```typescript
// src/lib/ai/memory/cortex-client.ts
import { CortexMemory } from '@cortexmemory/sdk';

export const cortex = new CortexMemory({
  convexUrl: process.env.CONVEX_URL!,
});

// Memory space management
export async function getOrCreateMemorySpace(userId: string) {
  return await cortex.memorySpaces.getOrCreate({
    id: `user:${userId}`,
    metadata: { type: 'user' },
  });
}

// Project-specific sub-spaces
export async function createProjectSpace(userId: string, projectId: string) {
  return await cortex.memorySpaces.create({
    id: `user:${userId}:project:${projectId}`,
    parentId: `user:${userId}`,
    metadata: { projectId },
  });
}
```

### 2. Memory-Enhanced ToolLoopAgent

```typescript
// src/lib/ai/agents/memory-agent.ts
import { ToolLoopAgent, Output, tool, stepCountIs } from 'ai';
import { z } from 'zod';
import { cortex } from '../memory/cortex-client';

export function createMemoryAgent(memorySpaceId: string) {
  return new ToolLoopAgent({
    model: "anthropic/claude-sonnet-4.5",
    instructions: `You are a helpful assistant with persistent memory.
      Always check memory before answering personal questions.
      Store important user information for future reference.`,
    tools: {
      recallMemory: tool({
        description: 'Recall information from memory about the user or past conversations',
        inputSchema: z.object({
          query: z.string().describe('What to remember'),
        }),
        execute: async ({ query }) => {
          const memories = await cortex.search({
            memorySpaceId,
            query,
            options: { limit: 5, recencyBias: 0.3 },
          });
          return memories;
        },
      }),

      storeMemory: tool({
        description: 'Store new information in memory for future reference',
        inputSchema: z.object({
          content: z.string().describe('Information to remember'),
        }),
        execute: async ({ content }) => {
          await cortex.facts.extract({
            memorySpaceId,
            content,
          });
          return { success: true, message: 'Memory stored' };
        },
      }),
    },
    stopWhen: stepCountIs(20),
    output: Output.object({
      schema: z.object({
        response: z.string(),
        memoriesUsed: z.array(z.string()).optional(),
        newMemoriesStored: z.array(z.string()).optional(),
      }),
    }),
  });
}
```

### 3. API Route with Memory Context

```typescript
// src/app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { CortexMemoryProvider } from '@cortexmemory/vercel-ai-provider';

const cortexProvider = new CortexMemoryProvider({
  convexUrl: process.env.CONVEX_URL!,
});

export async function POST(request: Request) {
  const { messages, userId, sessionId } = await request.json();

  // Get memory context for this user
  const memoryContext = await cortexProvider.getContext({
    memorySpaceId: userId || 'default',
    sessionId,
  });

  const result = await streamText({
    model: openai('gpt-4o'),
    system: `You are a helpful assistant with access to the user's memory.

Here is relevant context from previous conversations:
${memoryContext}

Use this context to provide personalized, contextual responses.`,
    messages,
  });

  // Store new memories from this conversation
  await cortexProvider.storeMemories({
    memorySpaceId: userId || 'default',
    messages,
  });

  return result.toDataStreamResponse();
}
```

### 4. Hive Mode for Multi-Agent Systems

```typescript
// src/lib/ai/memory/hive.ts
import { cortex } from './cortex-client';

export async function createAgentHive(agentIds: string[]) {
  const hive = await cortex.hive.create({
    id: `hive-${Date.now()}`,
    agents: agentIds,
    shareMode: 'full',
  });

  return {
    write: async (agentId: string, content: string, tags: string[]) => {
      await cortex.hive.write({
        hiveId: hive.id,
        agentId,
        content,
        tags,
      });
    },
    read: async (agentId: string, filter?: { tags?: string[] }) => {
      return await cortex.hive.read({
        hiveId: hive.id,
        agentId,
        filter,
      });
    },
  };
}

// A2A Communication
export async function sendToAgent(fromAgent: string, toAgent: string, message: any) {
  await cortex.a2a.send({
    fromAgent,
    toAgent,
    message,
  });
}

export async function receiveMessages(agentId: string, filter?: { type?: string }) {
  return await cortex.a2a.receive({
    agentId,
    filter,
  });
}
```

### 5. Tool with Approval

```typescript
// src/lib/ai/tools/sensitive-tool.ts
import { tool } from 'ai';
import { z } from 'zod';

export const sensitiveActionTool = tool({
  description: 'Performs a sensitive action that requires user approval',
  inputSchema: z.object({
    action: z.string().describe('The action to perform'),
    target: z.string().describe('Target of the action'),
    severity: z.enum(['low', 'medium', 'high']),
  }),
  // Dynamic approval based on severity
  needsApproval: async ({ severity }) => severity === 'high',
  execute: async ({ action, target, severity }) => {
    return { success: true, action, target };
  },
});
```

### 6. MCP Client Setup

```typescript
// src/lib/ai/mcp/client.ts
import { experimental_createMCPClient as createMCPClient } from '@ai-sdk/mcp';

export async function createMCPConnection(serverUrl: string) {
  const mcpClient = await createMCPClient({
    transport: {
      type: 'http',
      url: serverUrl,
      headers: {
        Authorization: `Bearer ${process.env.MCP_API_KEY}`,
      },
    },
  });

  return mcpClient;
}

export async function getMCPTools(serverUrl: string) {
  const client = await createMCPConnection(serverUrl);
  return await client.tools();
}
```

### 7. Client-Side Chat with Memory

```typescript
// src/components/chat/chat-interface.tsx
'use client';

import { useChat } from '@ai-sdk/react';

export function ChatInterface({ userId }: { userId: string }) {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
  } = useChat({
    api: '/api/chat',
    body: {
      userId,
      sessionId: crypto.randomUUID(),
    },
  });

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl mb-4">Chat with Memory</h1>
      <div className="space-y-4 mb-4">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`p-3 rounded ${
              m.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'
            }`}
          >
            <strong>{m.role === 'user' ? 'You' : 'Assistant'}:</strong>{' '}
            {m.content}
          </div>
        ))}
        {isLoading && (
          <div className="p-3 rounded bg-gray-100 animate-pulse">
            Thinking...
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message..."
          className="flex-1 p-2 border rounded"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
}
```

## Verification Checklist

After integration, verify:

```
[ ] All tests pass (pnpm test)
[ ] TypeScript types are correct (pnpm check-types)
[ ] Build succeeds (pnpm build)
[ ] Memory persists across sessions
[ ] Facts are extracted correctly
[ ] Semantic search returns relevant memories
[ ] Hive mode works for multi-agent scenarios
[ ] A2A communication functions properly
[ ] Tool approvals work in UI
[ ] Streaming responses render properly
[ ] MCP tools connect successfully
[ ] Error handling is robust
```

## Rollback Plan

If integration fails:
1. Revert package.json changes
2. Restore original AI implementation files
3. Clear node_modules and reinstall
4. Document failure reason for future attempts

## References

For progressive disclosure, see:
- `references/ai-sdk-6-features.md` - Complete AI SDK 6 feature reference
- `references/cortex-memory-integration.md` - Cortex Memory integration patterns
- `references/mcp-patterns.md` - MCP tool and resource patterns
- `references/migration-guide.md` - Migration from AI SDK 5 to 6

## Nia Quick Commands

```bash
# Search AI SDK 6 docs
mcp__nia__search: "AI SDK 6 [your query]" data_sources: "ai-sdk.dev"

# Search Cortex Memory docs
mcp__nia__search: "[your query]" data_sources: "docs.cortexmemory.dev"

# Read Cortex Memory page
mcp__nia__doc_read: docs.cortexmemory.dev /[path]

# Deep research
mcp__nia__nia_deep_research_agent: "How to implement [feature] with Cortex Memory"
```
