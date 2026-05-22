---
name: adk
description: a set of guidelines to build with Botpress's Agent Development Kit (ADK) - use these whenever you're tasked with building a feature using the ADK
license: MIT
---

# Botpress ADK Guidelines

Use this skill when you've got questions about the Botpress Agent Development Kit (ADK) - like when you're building a feature that involves tables, actions, tools, workflows, conversations, files, knowledge bases, triggers, or Zai.

## What is the ADK?

The Botpress ADK is a **convention-based TypeScript framework** where **file structure maps directly to bot behavior**. Place files in the correct directories, and they automatically become available as bot capabilities.

The ADK provides primitives for:

- Actions & Tools (reusable functions and AI-callable tools)
- Workflows (long-running, resumable processes)
- Conversations (message handling)
- Tables (data storage with semantic search)
- Files (file storage with semantic search)
- Knowledge Bases (RAG implementation)
- Triggers (event-driven automation)
- **Zai** (production-ready LLM utility library for common AI operations)

### Project Structure (Convention-Based)

All primitives must be placed in `src/` directory:

```
/                      # Project root
├── src/
│   ├── actions/       # Strongly-typed functions → auto-registered
│   ├── tools/         # AI-callable tools → available via execute()
│   ├── workflows/     # Long-running processes → resumable/scheduled
│   ├── conversations/ # Message handlers → routes by channel
│   ├── tables/        # Database schemas → auto-created with search
│   ├── triggers/      # Event handlers → subscribe to events
│   ├── knowledge/     # Knowledge bases → RAG with semantic search
│   └── utils/         # Shared helpers (not auto-registered)
└── agent.config.ts    # Bot configuration (includes integrations)
```

> **Note:** `dependencies.json` was removed in ADK 1.9+. All configuration including integrations now lives in `agent.config.ts`.

> **Critical:** Files outside `src/` are not discovered. Location = behavior.

## When to Use This Skill

Activate this skill when users ask ADK-related questions like:

- "How do I create an Action/Tool/Workflow/Conversation?"
- "What is the difference between X and Y?"
- "Show me an example of..."
- "How do I configure...?"
- "What's the CLI command for...?"
- "How do I use the Context API?"
- "How do I call integration actions?"
- "How do I use Zai for [extract/check/label/etc]?"
- "What are the best practices for...?"
- "How do I avoid common mistakes?"
- "How do I handle ticket assignment/escalation?"

## How to Answer ADK Questions

ADK questions fall into two categories: **CLI queries** and **documentation lookups**.

### Option 1: Direct CLI Commands (FAST - Use First!)

For integration discovery and CLI queries, use the Bash tool to run commands directly:

**Integration Discovery:**

```bash
# Search for integrations
adk search <query>

# List all available integrations
adk list --available

# Get detailed integration info (actions, channels, events)
adk info <integration-name>

# Check installed integrations (must be in ADK project)
adk list
```

**Project Info:**

```bash
# Check CLI version
adk --version

# Show project status
adk

# Get help
adk --help
```

**When to use CLI commands:**

- "What integrations are available?"
- "Search for Slack integration"
- "Show me details about the Linear integration"
- "What actions does the Slack integration have?"
- "What version of ADK am I using?"
- "How do I add an integration?"

**Response pattern:**

1. Use Bash tool to run the appropriate `adk` command
2. Parse and present the output to the user
3. Optionally suggest next steps (e.g., "Run `adk add slack@3.0.0` to install")

### Option 2: Documentation Questions (For Conceptual Questions)

For documentation, patterns, and how-to questions, search and reference the documentation files directly:

**When to use documentation:**

- "How do I create a workflow?"
- "What's the difference between Actions and Tools?"
- "Show me an example of using Zai"
- "What are best practices for state management?"
- "How do I fix this error?"
- "What's the pattern for X?"

**How to answer documentation questions:**

1. **Find relevant files** - Use Glob to discover documentation:

   ```
   pattern: **/references/*.md
   ```

2. **Search for keywords** - Use Grep to find relevant content:

   ```
   pattern: <keyword from user question>
   path: <path to references directory from step 1>
   output_mode: files_with_matches
   ```

3. **Read the files** - Use Read to load relevant documentation

4. **Provide answer** with:
   - Concise explanation
   - Code examples from the references
   - File references with line numbers (e.g., "From references/actions.md:215")
   - Common pitfalls if relevant
   - Related topics for further reading

## Available Documentation

Documentation should be located in `./references/` directory relative to this skill. When answering questions, search for these topics:

### Core Concepts

- **actions.md** - Actions with strong typing and validation
- **tools.md** - AI-callable tools and Autonomous namespace
- **workflows.md** - Workflows and step-based execution
- **conversations.md** - Conversation handlers and message routing
- **triggers.md** - Event-driven automation
- **messages.md** - Sending messages and events

### Data & Content

- **tables.md** - Data storage with semantic search
- **files.md** - File storage and management
- **knowledge-bases.md** - RAG implementation
- **zai-complete-guide.md** - Complete ZAI developer guide
- **zai-agent-reference.md** - Quick ZAI reference

### Configuration & Integration

- **agent-config.md** - Bot configuration and state management
- **model-configuration.md** - AI model configuration reference
- **context-api.md** - Runtime context access
- **integration-actions.md** - Using integration actions
- **tags.md** - Entity tags for bot, user, conversation, and workflow
- **cli.md** - Complete CLI command reference
- **mcp-server.md** - MCP server for AI assistants

### Frontend Integration

- **frontend/botpress-client.md** - Using @botpress/client in frontends
- **frontend/calling-actions.md** - Calling bot actions from frontend
- **frontend/type-generation.md** - Type-safe integration with generated types
- **frontend/authentication.md** - Authentication with PATs

## Runtime Access Patterns

Quick reference for accessing ADK runtime services:

### Imports

```typescript
// Always import from @botpress/runtime
import {
  Action,
  Autonomous,
  Workflow,
  Conversation,
  z,
  actions,
  adk,
  user,
  bot,
  conversation,
  context,
} from "@botpress/runtime";
```

### State Management

```typescript
// Bot state (defined in agent.config.ts)
bot.state.maintenanceMode = true;
bot.state.lastDeployedAt = new Date().toISOString();

// User state (defined in agent.config.ts)
user.state.preferredLanguage = "en";
user.state.onboardingComplete = true;

// User tags
user.tags.email; // Access user metadata
```

### Calling Actions

```typescript
// Call bot actions
await actions.fetchUser({ userId: "123" });
await actions.processOrder({ orderId: "456" });

// Call integration actions
await actions.slack.sendMessage({ channel: "...", text: "..." });
await actions.linear.issueList({ teamId: "..." });

// Convert action to tool
tools: [fetchUser.asTool()];
```

### Context API

```typescript
// Get runtime services
const client = context.get("client"); // Botpress client
const cognitive = context.get("cognitive"); // AI model client
const citations = context.get("citations"); // Citation manager
```

### File Naming

- **Actions/Tools/Workflows**: `myAction.ts`, `searchDocs.ts` (camelCase)
- **Tables**: `Users.ts`, `Orders.ts` (PascalCase)
- **Conversations/Triggers**: `chat.ts`, `slack.ts` (lowercase)

## Critical ADK Patterns (Always Reference in Answers)

When answering questions, always verify these patterns against the documentation:

### Package Management

```bash
# All package managers are supported
bun install       # Recommended (fastest)
npm install       # Works fine
yarn install      # Works fine
pnpm install      # Works fine

# ADK auto-detects based on lock files
# - bun.lockb → uses bun
# - package-lock.json → uses npm
# - yarn.lock → uses yarn
# - pnpm-lock.yaml → uses pnpm
```

### Imports

```typescript
// ✅ CORRECT - Always from @botpress/runtime
import { Action, Autonomous, Workflow, z } from "@botpress/runtime";

// ❌ WRONG - Never from zod or @botpress/sdk
import { z } from "zod"; // ❌ Wrong
import { Action } from "@botpress/sdk"; // ❌ Wrong
```

### Export Patterns

```typescript
// ✅ Both patterns work - export const is recommended
export const myAction = new Action({ ... });  // Recommended
export default new Action({ ... });           // Also valid

// Why export const?
// - Enables direct imports: import { myAction } from "./actions/myAction"
// - Can pass to execute(): tools: [myAction.asTool()]
```

### Actions

```typescript
// ✅ CORRECT - Handler receives { input, client }
export const fetchUser = new Action({
  name: "fetchUser",
  async handler({ input, client }) {  // ✅ Destructure from props
    const { userId } = input;         // ✅ Then destructure fields
    return { name: userId };
  }
});

// ❌ WRONG - Cannot destructure input fields directly
handler({ userId }) {  // ❌ Wrong - must be { input }
  return { name: userId };
}
```

### Tools

```typescript
// ✅ CORRECT - Tools CAN destructure directly
export const myTool = new Autonomous.Tool({
  handler: async ({ query, maxResults }) => {
    // ✅ Direct destructuring OK
    return search(query, maxResults);
  },
});
```

### Conversations

```typescript
// ✅ CORRECT - Use conversation.send() method
await conversation.send({
  type: "text",
  payload: { text: "Hello!" }
});

// ❌ WRONG - Never use client.createMessage() directly
await client.createMessage({ ... });  // ❌ Wrong
```

## Examples of Questions This Skill Answers

### Beginner Questions

- "What is an Action?"
- "How do I create my first workflow?"
- "What's the difference between Actions and Tools?"

### Implementation Questions

- "How do I access the Botpress client?"
- "How do I use citations in RAG?"
- "What's the syntax for searchable table columns?"
- "How do I call a Slack integration action?"
- "How do I use Zai to extract structured data?"
- "How do I validate content with Zai?"

### Advanced Pattern Questions

- "How do I add guardrails to prevent hallucinations?"
- "How do I implement admin authentication?"
- "How do I add logging and observability?"
- "How do I compose multiple extensions?"
- "How do I manage context in async tool handlers?"

### Troubleshooting Questions

- "Why am I getting 'Cannot destructure property' error?"
- "How do I fix import errors?"
- "What's wrong with my workflow state access?"

### Best Practices Questions

- "What are common mistakes to avoid?"
- "How should I structure my project?"
- "What's the recommended pattern for X?"

## Response Format

When answering ADK questions, follow this structure:

1. **Start with a concise explanation** - Answer the core question directly
2. **Provide working code examples** - Use examples from references or create based on patterns
3. **Include file references** - Cite documentation (e.g., "From actions.md:215")
4. **Highlight common pitfalls** - Reference the troubleshooting section if relevant
5. **Security & best practices** - Mention security considerations when applicable
6. **Link to related topics** - Suggest further reading or related concepts

**Example Response Structure:**

```
Actions are strongly-typed functions that can be called from anywhere in your bot.

**Example:**
[code example]

**Common Pitfall:** Remember to destructure `input` first (see troubleshooting section)

**Related:** You can convert Actions to Tools using `.asTool()` - see the "When to Use What" decision tree.

**Next Steps:** Create your action in `src/actions/myAction.ts` and it will be auto-registered.
```
