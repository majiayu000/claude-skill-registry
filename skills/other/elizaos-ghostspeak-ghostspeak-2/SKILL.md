---
name: elizaos-expert-2026
description: Expert ElizaOS plugin and agent development (January 2026). Use when (1) Building ElizaOS plugins, (2) Creating AI agent characters, (3) Implementing actions, providers, evaluators, (4) Integrating with AgentRuntime, (5) Building platform clients (Discord, Telegram), (6) Testing plugins, or any ElizaOS architecture questions.
---

# ElizaOS Expert Guide - January 2026

## What is ElizaOS?

ElizaOS is a framework for building AI agents with:
- **Plugin System** - Modular actions, providers, evaluators, services
- **Multi-Platform** - Discord, Telegram, Twitter, Direct clients
- **Character System** - Personality, knowledge, examples
- **Memory Management** - Vector database, conversation history
- **Model Flexibility** - OpenAI, Anthropic, local models

**Version**: 1.7.0+
**GhostSpeak Plugin**: `@ghostspeak/plugin-elizaos`

## When to Use This Skill

- Building custom ElizaOS plugins
- Creating agent characters (like Caisper)
- Implementing custom actions or providers
- Integrating with GhostSpeak smart contracts
- Setting up Telegram/Discord bots
- Managing agent memory and context

## Core Concepts

### Plugin Structure
```typescript
import { Plugin } from "@elizaos/core";

const myPlugin: Plugin = {
  name: "my-plugin",
  description: "My custom plugin",
  actions: [myAction],
  providers: [myProvider],
  evaluators: [myEvaluator],
  services: [myService],
};

export default myPlugin;
```

### Actions (Agent Capabilities)
```typescript
import { Action, HandlerCallback } from "@elizaos/core";

export const myAction: Action = {
  name: "MY_ACTION",
  similes: ["DO_THING", "PERFORM_ACTION"],
  description: "Does something useful",

  validate: async (runtime, message) => {
    // Return true if action should be triggered
    return message.content.text.includes("do thing");
  },

  handler: async (runtime, message, state, options, callback) => {
    // Perform action
    const result = await doSomething();

    // Send response
    if (callback) {
      await callback({
        text: `Done! Result: ${result}`,
      });
    }

    return true;
  },

  examples: [
    [
      {
        user: "{{user1}}",
        content: { text: "Please do the thing" },
      },
      {
        user: "{{agentName}}",
        content: { text: "I'll do that right away!" },
      },
    ],
  ],
};
```

### Providers (Data Sources)
```typescript
import { Provider } from "@elizaos/core";

export const myProvider: Provider = {
  get: async (runtime, message, state) => {
    // Fetch data
    const data = await fetchSomeData();

    // Return context to inject into prompts
    return `Relevant data: ${JSON.stringify(data)}`;
  },
};
```

### Character Definition
```typescript
import { Character } from "@elizaos/core";

export const caisperCharacter: Character = {
  name: "Caisper",
  username: "caisper",
  bio: [
    "A friendly ghost AI that helps users navigate the GhostSpeak platform",
    "Expert in Solana, verifiable credentials, and reputation systems",
  ],
  lore: [
    "Born from the blockchain mists",
    "Guardian of agent reputations",
  ],
  messageExamples: [
    [
      {
        user: "{{user1}}",
        content: { text: "What's my Ghost Score?" },
      },
      {
        user: "Caisper",
        content: {
          text: "Let me check your reputation on-chain... Your Ghost Score is 750! That's pretty good!",
        },
      },
    ],
  ],
  postExamples: [],
  topics: ["solana", "blockchain", "reputation", "ai-agents"],
  adjectives: ["friendly", "helpful", "knowledgeable", "ethereal"],
  style: {
    all: ["Be friendly and helpful", "Use ghost emoji occasionally ={"],
    chat: ["Keep responses concise", "Be conversational"],
    post: ["Share insights about Web3 and AI"],
  },
  plugins: ["@ghostspeak/plugin-elizaos"],
};
```

## GhostSpeak Integration

### Using @ghostspeak/sdk in Actions
```typescript
import { GhostSpeakClient } from "@ghostspeak/sdk";

export const checkReputationAction: Action = {
  name: "CHECK_REPUTATION",

  handler: async (runtime, message, state) => {
    // Initialize SDK
    const client = new GhostSpeakClient({
      cluster: "devnet",
    });

    // Get user's wallet address from message
    const walletAddress = extractWalletAddress(message);

    // Fetch reputation
    const agent = await client.agents.getByOwner(walletAddress);

    return {
      text: `Your Ghost Score is ${agent.ghostScore}!`,
    };
  },
};
```

### Telegram Integration (apps/web)
```typescript
// apps/web/lib/telegram/adapter.ts
import { TelegramClient } from "@elizaos/client-telegram";
import { AgentRuntime } from "@elizaos/core";

export async function setupTelegramBot(runtime: AgentRuntime) {
  const client = new TelegramClient(
    runtime,
    process.env.TELEGRAM_BOT_TOKEN!
  );

  await client.start();
}
```

## Testing Plugins

```typescript
import { describe, test, expect } from "bun:test";
import { AgentRuntime } from "@elizaos/core";

describe("My Plugin", () => {
  test("action triggers correctly", async () => {
    const runtime = new AgentRuntime({
      token: "test",
      character: testCharacter,
    });

    const result = await myAction.validate(runtime, testMessage);
    expect(result).toBe(true);
  });
});
```

## Development Workflow

```bash
# Install ElizaOS
pnpm add @elizaos/core @elizaos/client-telegram

# Create plugin
mkdir packages/plugin-my-plugin
cd packages/plugin-my-plugin
pnpm init

# Build plugin
pnpm build

# Test plugin
pnpm test

# Use in agent
import myPlugin from "@my-org/plugin-my-plugin";
const runtime = new AgentRuntime({
  plugins: [myPlugin],
});
```

## Best Practices

1. **Validate inputs** - Always validate user input in actions
2. **Handle errors gracefully** - Don't crash on API failures
3. **Use providers for context** - Keep actions simple, providers rich
4. **Test thoroughly** - Test all action paths
5. **Document examples** - Good examples improve agent behavior

## Additional Resources

- Full plugin guide: `/pluginskill` slash command
- ElizaOS Docs: https://github.com/elizaOS/eliza
- GhostSpeak Plugin: `packages/plugin-ghostspeak/`
- Caisper Character: `apps/web/server/elizaos/characters/caisper.ts`
