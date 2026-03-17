---
name: hashbrown-dev
description: Building LLM-powered React applications with the Hashbrown library. Use when the user asks to (1) Build generative UI where LLMs render React components, (2) Add client-side tool calling for LLM-app interaction, (3) Stream LLM responses in React applications, (4) Execute LLM-generated JavaScript safely in a sandbox, (5) Build browser agents or AI-powered UIs with hashbrown, (6) Control React UI from LLM output, (7) Integrate with LLM providers like OpenAI, Anthropic, Google, Azure, Bedrock, or Ollama in React apps, (8) Create chatbots, form builders, predictive text inputs, or multi-threaded conversations with LLMs, (9) Transform natural language to structured data in TypeScript React applications.
---

# Hashbrown Development Skill

## Overview

Hashbrown is a React library for building LLM-powered applications with generative UI, client-side tool calling, streaming, and sandboxed JavaScript execution. It provides React hooks (`useChat`, `useUiChat`, etc.) that connect to a Node.js backend adapter, which securely communicates with LLM providers (OpenAI, Anthropic, Google, Azure, Bedrock, Ollama).

**Architecture**: React frontend (using Hashbrown hooks) + Node.js backend adapter (proxies LLM API requests)

## Quick Start Workflow

### 1. Choose the Right Hook

| Hook                      | Multi-turn Chat | Single Input | Structured Output | Tool Calling | Generate UI |
| ------------------------- | :-------------: | :----------: | :---------------: | :----------: | :---------: |
| `useChat`                 |       ✅        |      ❌      |        ❌         |      ✅      |     ❌      |
| `useStructuredChat`       |       ✅        |      ❌      |        ✅         |      ✅      |     ❌      |
| `useCompletion`           |       ❌        |      ✅      |        ❌         |      ✅      |     ❌      |
| `useStructuredCompletion` |       ❌        |      ✅      |        ✅         |      ✅      |     ❌      |
| `useUiChat`               |       ✅        |      ❌      |        ✅         |      ✅      |     ✅      |

### 2. Generate Boilerplate

Use the scripts to scaffold components and servers:

```bash
# List available templates
python scripts/list-templates.py

# Generate a component
python scripts/generate-component.py simple-chat ./src/components

# Generate a backend server
python scripts/generate-server.py basic-chat-server ./backend
```

**Available component templates:**

- `simple-chat` - Basic text-only chat with `useChat`
- `ui-chat-with-components` - Generative UI with `useUiChat` and `exposeComponent`
- `client-side-tool-calling` - Tool calling with `useTool`
- `js-runtime-chart-generator` - Sandboxed JS execution for data visualization
- `structured-data-form` - Form generation from natural language with Skillet schemas
- `streaming-chat-ui` - Streaming responses with loading states
- `multi-threaded-chat-ui` - Multi-conversation management with threads
- `predictive-text-input` - Autocomplete/suggestions powered by LLM
- `chat-with-voice-input` - Voice input with speech recognition

**Available server templates:**

- `basic-chat-server` - Simple Express server with OpenAI adapter
- `streaming-chat-server` - Streaming support for real-time responses
- `chat-server-with-data` - Server with database/context injection
- `chat-server-with-threads` - Persistent conversation threads
- `server-with-authentication` - Auth-protected endpoints

### 3. Consult References for Details

Load reference documentation as needed for deep implementation details:

- **[getting-started.md](references/getting-started.md)** - Installation, setup, hook overview
- **[core-concepts.md](references/core-concepts.md)** - Generative UI, tool calling, JS runtime, streaming
- **[structured-data.md](references/structured-data.md)** - Skillet schema language for type-safe JSON output
- **[platform-integration.md](references/platform-integration.md)** - LLM provider adapters (OpenAI, Anthropic, Google, etc.)
- **[advanced-guides.md](references/advanced-guides.md)** - Chatbots, threads, MCP, predictive actions
- **[best-practices.md](references/best-practices.md)** - Prompt engineering, model selection, ethics
- **[INDEX.md](references/INDEX.md)** - Navigation map of all documentation

## Core Capabilities

### 1. Generative UI

Expose React components to the LLM so it can render your UI dynamically.

```tsx
import { useUiChat, exposeComponent } from '@hashbrownai/react'
import { s } from '@hashbrownai/core'
import { MyCard } from './MyCard'

const exposedCard = exposeComponent(MyCard, {
  name: 'MyCard',
  description: 'A card to display information',
  props: { title: s.string('The title'), content: s.string('The body') },
})

const { messages } = useUiChat({
  components: [exposedCard],
  model: 'gpt-4',
  system: 'Render cards to show information to the user.',
})

// messages[1].ui will contain <MyCard title="..." content="..." />
```

**When to use**: Build browser agents, dynamic dashboards, form builders, or any UI that should adapt based on LLM decisions.

**Reference**: See [core-concepts.md](references/core-concepts.md) for detailed component exposure patterns.

### 2. Client-Side Tool Calling

Allow the LLM to call client-side functions to access app state or perform actions.

```tsx
import { useChat, useTool } from '@hashbrownai/react'

const getUserTool = useTool({
  name: 'getUser',
  description: 'Get current user information',
  handler: async () => ({ name: 'Jane Doe' }),
  deps: [],
})

const { messages } = useChat({
  tools: [getUserTool],
  model: 'gpt-4',
})
```

**When to use**: Let the LLM access application state, trigger actions, or interact with external APIs.

**Reference**: See [core-concepts.md](references/core-concepts.md) for tool definition patterns.

### 3. Structured Data Output

Use Skillet schemas to get type-safe, validated JSON from the LLM.

```tsx
import { useStructuredCompletion } from '@hashbrownai/react'
import { s } from '@hashbrownai/core'

const schema = s.object('Response', {
  name: s.string('User name'),
  age: s.number('User age'),
  interests: s.array('List of interests', s.string('An interest')),
})

const { data } = useStructuredCompletion({
  schema,
  model: 'gpt-4',
  prompt: 'Extract user info: John is 30 and likes hiking and reading.',
})

// data will be typed as { name: string; age: number; interests: string[] }
```

**When to use**: Extract structured information, build forms from natural language, parse documents, or transform unstructured text to JSON.

**Reference**: See [structured-data.md](references/structured-data.md) for Skillet schema language details.

### 4. Sandboxed JavaScript Execution

Execute LLM-generated JavaScript safely in a WASM-based QuickJS sandbox.

```tsx
import { useRuntime, useToolJavaScript, useChat } from '@hashbrownai/react'

const runtime = useRuntime({ functions: [] })
const jsTool = useToolJavaScript({ runtime })
const chat = useChat({ tools: [jsTool], model: 'gpt-4' })
```

**When to use**: Let the LLM perform complex calculations, data transformations, or generate visualizations using code.

**Reference**: See [core-concepts.md](references/core-concepts.md) for runtime configuration.

### 5. Platform Integration

Connect to any LLM provider via backend adapters:

```typescript
// Backend server (Node.js)
import { HashbrownOpenAI } from '@hashbrownai/openai'

const stream = HashbrownOpenAI.stream.text({
  apiKey: process.env.OPENAI_API_KEY,
  request,
})
```

**Supported platforms**: OpenAI, Anthropic, Google, Azure, Bedrock, Ollama, Writer, and custom adapters.

**Reference**: See [platform-integration.md](references/platform-integration.md) for all adapter configurations.

## Common Patterns

### Building a Chat Interface

1. Generate component: `python scripts/generate-component.py simple-chat ./src`
2. Generate server: `python scripts/generate-server.py basic-chat-server ./backend`
3. Wrap app in `<HashbrownProvider url="/api/chat">`
4. Customize system prompt and model in component

### Adding Generative UI

1. Generate: `python scripts/generate-component.py ui-chat-with-components ./src`
2. Create presentational React components
3. Expose with `exposeComponent(Component, { name, description, props })`
4. Pass to `useUiChat({ components: [...] })`
5. Write system prompt instructing when to use components

### Implementing Tool Calling

1. Define tools with `useTool({ name, description, handler })`
2. Pass to chat hook: `useChat({ tools: [...] })`
3. Tools are automatically called by the LLM when needed
4. Tool results are sent back to LLM in the conversation

### Streaming Structured Data

1. Use `s.streaming` modifier in Skillet schema:
   ```tsx
   const schema = s.object('Response', {
     items: s.streaming.array('Items', s.string('Item')),
   })
   ```
2. Render partial data as it arrives

## Pitfalls

- **Forgetting backend adapter**: Hashbrown React library requires a Node.js backend to proxy LLM requests
- **Prompt injection**: Don't concatenate user input directly into system instructions
- **Over-exposing components**: Only expose components that are safe for the LLM to render
- **Unbounded runtime execution**: Always provide an `AbortSignal` with timeout to JS runtime
- **Wrong hook choice**: Use the hook decision table above to pick the right one

## Resources

- **scripts/**: Template generation utilities (list-templates.py, generate-component.py, generate-server.py)
- **references/**: In-depth documentation on all Hashbrown features (load as needed)
- **assets/**: Complete component and server templates ready to copy
