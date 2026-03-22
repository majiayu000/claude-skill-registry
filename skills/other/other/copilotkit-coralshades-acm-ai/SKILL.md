---
name: copilotkit
description: Build AI copilots, chatbots, and agentic UIs in React and Next.js using CopilotKit. Use this skill when the user wants to add an AI assistant, copilot, chat interface, AI-powered textarea, or agentic UI to their app. Covers setup, hooks (useCopilotAction, useCopilotReadable, useCoAgent, useAgent), chat components (CopilotPopup, CopilotSidebar, CopilotChat), generative UI, human-in-the-loop, CoAgents with LangGraph, AG-UI protocol, MCP Apps, and Python SDK integration. Triggers on CopilotKit, copilotkit, useCopilotAction, useCopilotReadable, useCoAgent, useAgent, CopilotRuntime, CopilotChat, CopilotSidebar, CopilotPopup, CopilotTextarea, AG-UI, agentic frontend, in-app AI copilot, AI assistant React, chatbot React, useFrontendTool, useRenderToolCall, useDefaultTool, useCoAgentStateRender, useLangGraphInterrupt, useCopilotChat, useCopilotAdditionalInstructions, useCopilotChatSuggestions, useHumanInTheLoop, CopilotTask, copilot runtime, LangGraphAgent, BasicAgent, BuiltInAgent, CopilotKitRemoteEndpoint, A2UI, MCP Apps, AI textarea, AI form completion, add AI to React app.
license: MIT
metadata:
  author: nihalnihalani
  version: "1.1"
  tags: copilotkit, ai, react, nextjs, copilot, chatbot, agent, agentic-ui, langgraph, coagents, ag-ui, mcp, angular
---

# CopilotKit

Full-stack open-source framework (MIT, v1.51.3, Python SDK v0.1.78) for building agentic applications with AI copilots embedded directly in React and Angular UIs. Angular support via `@copilotkitnext/angular` (Angular 18+19). 28k+ GitHub stars.

## When to Use This Skill
- User wants to add an AI copilot, assistant, or chatbot to a React/Next.js app
- User is working with CopilotKit hooks, components, or runtime
- User asks about AI-powered text areas or form completion
- User needs to connect a Python agent (LangGraph/CrewAI) to a React frontend
- User is implementing human-in-the-loop or generative UI patterns
- User asks about AG-UI protocol or MCP Apps
- User wants to sync state between a UI and an AI agent

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   F R O N T E N D    @copilotkit/react-core + react-ui          │
│                                                                 │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│   │  <CopilotPopup>  │  │ <CopilotSidebar> │  │ <CopilotChat>│ │
│   │  <CopilotTextarea>│  │   Headless UI    │  │  Custom UI   │ │
│   └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
│            └──────────────┬──────┘                    │         │
│                           ▼                           │         │
│   ┌───────────────────────────────────────────────────┘         │
│   │  React Hooks                                                │
│   │  ├─ useCopilotAction()       → Define callable tools        │
│   │  ├─ useCopilotReadable()     → Expose app state to LLM     │
│   │  ├─ useAgent()               → Bidirectional state (v2)    │
│   │  ├─ useFrontendTool()        → Generative UI rendering     │
│   │  ├─ useCopilotChat()         → Headless chat control       │
│   │  └─ useLangGraphInterrupt()  → Human-in-the-loop           │
│   └─────────────────────────┬───────────────────────────────────│
│                             │                                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │    AG-UI Protocol  │
                    │  (HTTP event stream│
                    │   17 event types)  │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────┼───────────────────────────────────┐
│                             │                                   │
│   B A C K E N D    @copilotkit/runtime                          │
│                             ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  CopilotRuntime                                         │   │
│   │  ┌──────────────┐ ┌───────────────┐ ┌────────────────┐ │   │
│   │  │ LLM Adapters │ │ Backend       │ │ Thread         │ │   │
│   │  │ OpenAI       │ │ Actions       │ │ Persistence    │ │   │
│   │  │ Anthropic    │ │ (server-side  │ │ InMemory /     │ │   │
│   │  │ Google       │ │  tools)       │ │ SQLite         │ │   │
│   │  │ Groq         │ │               │ │                │ │   │
│   │  └──────────────┘ └───────────────┘ └────────────────┘ │   │
│   │  ┌──────────────────────────────────────────────────┐   │   │
│   │  │ Agent Router                                     │   │   │
│   │  │ ├─ BuiltInAgent   (direct LLM + middleware)      │   │   │
│   │  │ ├─ BasicAgent     (lightweight, no middleware)    │   │   │
│   │  │ └─ CustomHttpAgent (remote Python/JS agents) ────┼───┼─┐ │
│   │  └──────────────────────────────────────────────────┘   │ │ │
│   └─────────────────────────────────────────────────────────┘ │ │
│                                                               │ │
└───────────────────────────────────────────────────────────────┼─┘
                                                                │
                    ┌───────────────────┐                       │
                    │    AG-UI / HTTP    │◄──────────────────────┘
                    └─────────┬─────────┘
                              │
┌─────────────────────────────┼───────────────────────────────────┐
│                             ▼                                   │
│   A G E N T   L A Y E R   (optional, any AG-UI framework)      │
│                                                                 │
│   Python: copilotkit SDK v0.1.78 + FastAPI / Flask              │
│                                                                 │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│   │ LangGraph  │ │  CrewAI    │ │ Google ADK │ │ AWS Strands│  │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘  │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│   │  Mastra    │ │ PydanticAI │ │    AG2     │ │ LlamaIndex │  │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘  │
│                                                                 │
│   Protocols:  AG-UI (↔ user)  ·  MCP (↔ tools)  ·  A2A (↔ agents)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### New project
```bash
npx copilotkit@latest create -f next
```

### Existing project
```bash
npm install @copilotkit/react-core @copilotkit/react-ui @copilotkit/runtime
```

### Environment
```bash
# .env.local
OPENAI_API_KEY="sk-..."
# or ANTHROPIC_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY
```

### Backend API route (`app/api/copilotkit/route.ts`)
```typescript
import {
  CopilotRuntime,
  OpenAIAdapter, // or AnthropicAdapter, GoogleGenerativeAIAdapter, GroqAdapter, LangChainAdapter
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const serviceAdapter = new OpenAIAdapter({ model: "gpt-4o" });
const runtime = new CopilotRuntime();

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};
```

### Frontend provider (`layout.tsx`)
```typescript
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### Chat UI (`page.tsx`)
```typescript
import { CopilotPopup } from "@copilotkit/react-ui"; // or CopilotSidebar, CopilotChat

export default function Home() {
  return (
    <>
      <YourApp />
      <CopilotPopup
        instructions="You are an AI assistant for this app."
        labels={{ title: "Assistant", initial: "How can I help?" }}
      />
    </>
  );
}
```

## Core Hooks

### `useCopilotReadable` -- Expose app state to LLM
```typescript
useCopilotReadable({
  description: "Current user profile and preferences",
  value: { name: user.name, role: user.role, preferences },
});
```

### `useCopilotAction` -- Define executable actions
```typescript
useCopilotAction({
  name: "addItem",
  description: "Add a new item to the list",
  parameters: [
    { name: "title", type: "string", required: true },
    { name: "priority", type: "string", description: "low, medium, or high" },
  ],
  handler: async ({ title, priority = "medium" }) => {
    setItems(prev => [...prev, { id: Date.now().toString(), title, priority }]);
    return `Added "${title}" with ${priority} priority`;
  },
});
```

### `useCopilotChat` -- Programmatic chat control
```typescript
const { appendMessage, stopGeneration, reset, reloadMessages } = useCopilotChat();
```

### `useCopilotAdditionalInstructions` -- Dynamic context-aware prompts
```typescript
useCopilotAdditionalInstructions({
  instructions: "User is on the settings page. Help them configure preferences.",
});
```

### `useCopilotChatSuggestions` -- Auto-generate suggestions from app state
```typescript
useCopilotChatSuggestions({
  instructions: "Suggest actions based on the current app state.",
});
```

### `useAgent` -- v2 agent state sync (superset of useCoAgent)
```typescript
const { state, setState, run, stop } = useAgent({ name: "my_agent" });
```
`useAgent` is the v2 replacement for `useCoAgent`. It includes all `useCoAgent` functionality plus time-travel debugging and improved state management. Prefer `useAgent` for new projects.

### `CopilotTask` -- Run one-off programmatic tasks
```typescript
import { CopilotTask } from "@copilotkit/react-core";

const task = new CopilotTask({ instructions: "Summarize the data" });
await task.run(context);
```

## Advanced Patterns

Detailed guides organized by topic -- load only what's needed:

- **Generative UI** (static AG-UI, declarative A2UI, open-ended MCP Apps): See [references/generative-ui.md](references/generative-ui.md)
- **Shared State & CoAgents** (useCoAgent, useAgent, bidirectional sync, LangGraph): See [references/coagents-shared-state.md](references/coagents-shared-state.md)
- **Human-in-the-Loop** (buildtime/runtime HITL, approval flows, agent steering): See [references/human-in-the-loop.md](references/human-in-the-loop.md)
- **Runtime & Adapters** (all LLM adapters, framework endpoints, backend actions): See [references/runtime-adapters.md](references/runtime-adapters.md)
- **Python SDK** (LangGraphAgent, FastAPI, actions, state, events): See [references/python-sdk.md](references/python-sdk.md)
- **Styling & Customization** (CSS, custom components, headless mode): See [references/styling-customization.md](references/styling-customization.md)
- **Troubleshooting** (common issues, CORS, env vars, Docker): See [references/troubleshooting.md](references/troubleshooting.md)
- **AG-UI Protocol** (events, architecture, CLI scaffolding): See [references/ag-ui-protocol.md](references/ag-ui-protocol.md)

## UI Components

| Component | Import | Use case |
|-----------|--------|----------|
| `CopilotChat` | `@copilotkit/react-ui` | Embedded inline chat panel |
| `CopilotSidebar` | `@copilotkit/react-ui` | Collapsible sidebar chat |
| `CopilotPopup` | `@copilotkit/react-ui` | Floating popup chat |
| `CopilotTextarea` | `@copilotkit/react-ui` | AI-powered textarea drop-in |

All accept `instructions`, `labels`, `suggestions`, custom message/input components, and `observabilityHooks`.

## CopilotKit Provider Props

| Prop | Type | Purpose |
|------|------|---------|
| `runtimeUrl` | `string` | Self-hosted runtime endpoint |
| `publicApiKey` | `string` | Copilot Cloud API key |
| `headers` | `object` | Custom auth headers |
| `credentials` | `string` | Cookie handling (`"include"` for cross-origin) |
| `agent` | `string` | Default agent name |
| `properties` | `object` | Thread metadata, authorization |
| `onError` | `function` | Error handler callback |
| `showDevConsole` | `boolean` | Dev error banners |
| `enableInspector` | `boolean` | Debugging inspector tool |
| `renderActivityMessages` | `array` | Custom renderers (A2UI, etc.) |

## Agent Protocols

| Protocol | Purpose | Package |
|----------|---------|---------|
| **AG-UI** | Agent <-> User interaction, event streaming | `@ag-ui/core`, `@ag-ui/client` |
| **MCP** | Agent <-> External tools | MCP server integration |
| **A2A** | Agent <-> Agent communication | A2A protocol support |

## Supported Agent Frameworks

LangGraph, CrewAI, Google ADK, AWS Strands, Microsoft Agent Framework, Mastra, PydanticAI, AG2, LlamaIndex, Agno, VoltAgent, Blaxel.

## LLM Adapters

`OpenAIAdapter`, `AnthropicAdapter`, `GoogleGenerativeAIAdapter`, `GroqAdapter`, `LangChainAdapter`, `OpenAIAssistantAdapter`.

## Key Packages

| Package | Purpose |
|---------|---------|
| `@copilotkit/react-core` | Provider + all hooks |
| `@copilotkit/react-ui` | Chat UI components + styles |
| `@copilotkit/runtime` | Backend runtime + LLM adapters + framework endpoints |
| `copilotkit` (Python) | Python SDK for LangGraph/CrewAI agents |
| `@copilotkitnext/angular` | Angular SDK (Angular 18+19) |
| `@ag-ui/core` | AG-UI protocol types/events |
| `@ag-ui/client` | AG-UI client implementation |

## Error Handling

### Frontend `onError` callback

```typescript
<CopilotKit
  runtimeUrl="/api/copilotkit"
  onError={(error) => {
    console.error("CopilotKit error:", error);
    toast.error("AI assistant encountered an error");
  }}
>
```

### Tool render `"failed"` status

All render functions receive `status === "failed"` when a tool errors. Always handle this:

```typescript
render: ({ status, args, result }) => {
  if (status === "failed") return <ErrorCard message="Tool execution failed" />;
  // ...
}
```

### Python SDK exception types

| Exception | Meaning |
|-----------|---------|
| `ActionNotFoundException` | Requested action not registered |
| `AgentNotFoundException` | Requested agent not found in endpoint |

## Versioning

Current version: **v1.51.3** (Python SDK **v0.1.78**). The v2 runtime interface is available at the `/v2` path. Next-generation packages use the `@copilotkitnext/*` namespace (e.g., `@copilotkitnext/angular`).

## Common Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Put API keys in client-side code | Use server-side env vars + runtime endpoint |
| Create a new CopilotRuntime per request | Instantiate once, reuse across requests |
| Skip `status` checks in render functions | Always handle "inProgress", "complete", "failed" |
| Use `useCoAgent` for new projects | Prefer `useAgent` (v2 superset with time travel) |
| Hardcode instructions in every component | Use `useCopilotAdditionalInstructions` for page-specific context |
| Forget to import styles | Add `import "@copilotkit/react-ui/styles.css"` in layout |
| Mix `runtimeUrl` and `publicApiKey` without reason | Pick one deployment mode unless you need hybrid |
| Put heavy computation in action handlers | Return data from handlers, compute in render |

## Common Patterns Cheat Sheet

| Want to... | Use |
|-----------|-----|
| Show a chat bubble | `<CopilotPopup>` |
| Give LLM app context | `useCopilotReadable()` |
| Let LLM call functions | `useCopilotAction()` |
| Render UI from tool calls | `useFrontendTool()` or `useRenderToolCall()` |
| Default fallback tool renderer | `useDefaultTool()` |
| Sync state bidirectionally | `useCoAgent()` |
| Use v2 agent state sync | `useAgent()` (superset of useCoAgent) |
| Show agent progress | `useCoAgentStateRender()` |
| Ask user for approval | `useHumanInTheLoop()` |
| Handle LangGraph interrupts | `useLangGraphInterrupt()` |
| Control chat programmatically | `useCopilotChat()` |
| Run one-off tasks | `CopilotTask` |
| Connect Python agent | `CopilotKitRemoteEndpoint` + `LangGraphAgent` |
| Scaffold AG-UI app | `npx create-ag-ui-app` |
| Persist conversations | Thread model + StorageRunners |
