---
name: "Convex Agents Playground"
description: "Sets up a web UI for testing, debugging, and developing agents without code. Use this to manually test agents, browse conversation history, and verify behavior in real-time."
---

## Purpose

The Playground is a graphical interface for interacting with agents. It lets you browse threads, send messages, inspect tool calls, and adjust context parameters without writing code.

## When to Use This Skill

- Testing agents during development
- Manually verifying agent behavior
- Debugging unexpected responses
- Experimenting with prompts and context options
- Demoing agents to stakeholders
- Inspecting tool calls and results
- Analyzing message structure and metadata

## Set Up Playground API Endpoint

Create a Convex function that exposes playground APIs:

```typescript
// convex/playground.ts
import { definePlaygroundAPI } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { weatherAgent, supportAgent, creativeAgent } from "./agents";

export const {
  isApiKeyValid,
  listAgents,
  listUsers,
  listThreads,
  listMessages,
  createThread,
  generateText,
  fetchPromptContext,
} = definePlaygroundAPI(components.agent, {
  agents: [weatherAgent, supportAgent, creativeAgent],
});
```

## Generate API Key

```bash
# Generate API key from CLI
npx convex run --component agent apiKeys:issue '{"name":"my-key"}'

# Output:
# { "id": "abc123def456", "name": "my-key" }
```

## Use Hosted Playground

Access the online playground:

```
1. Visit: https://get-convex.github.io/agent/
2. Enter your Convex deployment URL (from .env.local)
3. Enter your API key
4. Select your playground path (default: "playground")
5. Choose an agent and user to test
```

## Run Playground Locally

```bash
# Install and run local playground
npx @convex-dev/agent-playground

# Uses VITE_CONVEX_URL from .env.local
# Open browser to http://localhost:5173
```

## Playground Features

```
1. User Selection
   - Pick a user to view their threads
   - See all conversations for that user

2. Thread Browsing
   - List all threads for selected user
   - View thread metadata (title, summary)
   - Click to open a thread

3. Message History
   - View all messages in thread
   - See message ordering and step order
   - Inspect message metadata
   - View tool call details

4. Send Message
   - Type a message to test agent
   - Configure save options
   - Send and see response in real-time
   - View usage information

5. Context Configuration
   - Adjust recentMessages count
   - Enable/disable text search
   - Enable/disable vector search
   - Set search result limits
   - Test different context options

6. Tool Call Analysis
   - View tool calls and parameters
   - See tool results
   - Inspect tool execution details
```

## Test Multiple Agents

Switch between agents in playground:

```typescript
// convex/playground.ts
export const {
  isApiKeyValid,
  listAgents,
  // ...
} = definePlaygroundAPI(components.agent, {
  agents: [fastAgent, creativeAgent, analyticalAgent, supportAgent],
});
```

## Manage API Keys

Generate and revoke keys:

```bash
# Generate new key (or reissue existing)
npx convex run --component agent apiKeys:issue '{"name":"dev-key"}'

# Reusing a name revokes and reissues

# Multiple keys for different environments:
npx convex run --component agent apiKeys:issue '{"name":"prod-key"}'
npx convex run --component agent apiKeys:issue '{"name":"staging-key"}'
```

## Key Principles

- **Security via API keys**: Keys needed to access playground
- **Read-only by default**: Doesn't modify data unless you send messages
- **Real-time updates**: See agent responses immediately
- **Context control**: Experiment with context settings live
- **No code needed**: Use without writing any code

## Development Workflow

```
1. Define agent (convex/agents.ts)
2. Export in playground (convex/playground.ts)
3. Generate API key
4. Open playground
5. Test agent
6. Debug behavior
7. Adjust agent
8. Repeat
```

## Next Steps

- See **debugging** for logging context
- See **fundamentals** for agent setup
- See **rate-limiting** for understanding costs
