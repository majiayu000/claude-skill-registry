---
name: elizaos-plugin-dev
description: Expert-level guide for elizaOS plugin development. Use when (1) Creating new plugins with actions, services, providers, evaluators, (2) Integrating with AgentRuntime for memory, models, events, (3) Building platform clients or external integrations, (4) Writing component and E2E tests for plugins, (5) Publishing plugins to npm and elizaOS registry, or any elizaOS plugin architecture questions.
---

# elizaOS Plugin Development

## Core Interfaces

### Plugin
```typescript
interface Plugin {
  name: string;
  description: string;
  init?: (config: Record<string, string>, runtime: IAgentRuntime) => Promise<void>;
  config?: { [key: string]: string };
  services?: typeof Service[];
  actions?: Action[];
  providers?: Provider[];
  evaluators?: Evaluator[];
  adapter?: IDatabaseAdapter;
  models?: { [K in ModelTypeName]?: ModelHandler };
  events?: { [E in EventType]?: EventHandler[] };
  routes?: Route[];
  priority?: number;
  schema?: object;
}
```

### Action
```typescript
interface Action {
  name: string;
  description: string;
  similes?: string[];
  examples?: ActionExample[];
  validate: (runtime: IAgentRuntime, message: Memory, state: State) => Promise<boolean>;
  handler: (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    options: HandlerOptions,
    callback: HandlerCallback,
    responses: Memory[]
  ) => Promise<ActionResult>;
}

interface ActionResult {
  success: boolean;
  data?: Record<string, unknown>;
  values?: Record<string, unknown>;
  text?: string;
}
```

### Provider
```typescript
interface Provider {
  name: string;
  description?: string;
  position?: number;
  get: (runtime: IAgentRuntime, message: Memory, state: State) => 
    Promise<string | { text: string; data?: Record<string, unknown> }>;
}
```

### Service
```typescript
abstract class Service {
  static serviceType: string;
  abstract capabilityDescription: string;
  config?: Record<string, unknown>;
  abstract stop(): Promise<void>;
  static start(runtime: IAgentRuntime): Promise<Service>;
}
```

### State
```typescript
interface State {
  [key: string]: unknown;
  values: { [key: string]: unknown };  // Template variables
  data: StateData;                      // Typed cache
  text: string;                         // Context string
}

interface StateData {
  room?: Room;
  world?: World;
  entity?: Entity;
  actionPlan?: ActionPlan;
  actionResults?: ActionResult[];
  providers?: Record<string, ProviderResult>;
}
```

## Quick Patterns

### Minimal Plugin
```typescript
export const myPlugin: Plugin = {
  name: 'my-plugin',
  description: 'Does X',
  actions: [myAction],
  services: [MyService],
};
export default myPlugin;
```

### Action with Validation
```typescript
const myAction: Action = {
  name: 'MY_ACTION',
  description: 'Performs X when Y',
  validate: async (runtime, message, state) => {
    return message.content.text?.includes('trigger');
  },
  handler: async (runtime, message, state, options, callback) => {
    await callback({ text: 'Response', action: 'MY_ACTION' });
    return { success: true, text: 'Completed' };
  },
};
```

### Provider Pattern
```typescript
const myProvider: Provider = {
  name: 'MY_CONTEXT',
  description: 'Supplies X context',
  position: 10,
  get: async (runtime, message, state) => {
    const data = await fetchData();
    return { text: `Context: ${data}`, data: { raw: data } };
  },
};
```

### Service Pattern
```typescript
class MyService extends Service {
  static serviceType = 'my-service';
  capabilityDescription = 'Provides X integration';
  
  static async start(runtime: IAgentRuntime) {
    const instance = new MyService();
    await instance.initialize(runtime);
    return instance;
  }
  
  async stop() { /* cleanup */ }
}
```

## Reference Files

Load based on task:

- **Plugin structure & lifecycle**: See [plugin-interface.md](references/plugin-interface.md)
- **Actions, Evaluators, Providers, Services**: See [components.md](references/components.md)
- **Runtime API (memory, models, events)**: See [runtime-api.md](references/runtime-api.md)
- **State composition & providers**: See [state-composition.md](references/state-composition.md)
- **Testing patterns**: See [testing.md](references/testing.md)
- **CLI workflow**: See [cli-workflow.md](references/cli-workflow.md)

## Project Structure

```
plugin-name/
├── src/
│   ├── index.ts              # Plugin export
│   ├── actions/              # Action implementations
│   ├── services/             # Service classes
│   ├── providers/            # Provider functions
│   ├── evaluators/           # Evaluator implementations
│   └── __tests__/
│       ├── *.test.ts         # Component tests
│       └── e2e/*.e2e.ts      # E2E tests
├── images/
│   ├── logo.jpg              # Required for registry
│   └── banner.jpg
├── package.json              # With agentConfig section
├── tsconfig.json
└── tsup.config.ts
```

## CLI Quick Reference

```bash
# Create
elizaos create my-plugin --type plugin

# Develop
elizaos dev

# Test
elizaos test              # Both component + E2E
elizaos test component    # Unit tests only
elizaos test e2e          # Integration tests only

# Publish
elizaos publish --npm --github
```

## Key Runtime Methods

```typescript
// Memory
runtime.createMemory(memory, tableName)
runtime.searchMemories({ embedding, roomId, count, match_threshold })
runtime.addEmbeddingToMemory(memory)

// Models
runtime.generateText(input, options)
runtime.generateObject({ prompt, schema, modelType })
runtime.useModel(modelType, params)
runtime.registerModel(modelType, handler, provider, priority)

// State
runtime.composeState(message, includeList?, onlyInclude?, skipCache?)

// Services
runtime.getService<T>(serviceName)
runtime.registerService(serviceClass)

// Events
runtime.emitEvent(eventType, payload)
runtime.registerEvent(eventType, handler)
```

## Event Types

`MESSAGE_RECEIVED`, `MESSAGE_SENT`, `VOICE_MESSAGE_RECEIVED`, `WORLD_JOINED`, `WORLD_CONNECTED`, `WORLD_LEFT`, `ENTITY_JOINED`, `ENTITY_LEFT`, `ROOM_JOINED`, `ROOM_LEFT`, `ACTION_STARTED`, `ACTION_COMPLETED`, `RUN_STARTED`, `RUN_ENDED`, `RUN_TIMEOUT`, `EVALUATOR_STARTED`, `EVALUATOR_COMPLETED`, `MODEL_USED`, `CONTROL_MESSAGE`

## Model Types

`TEXT_SMALL`, `TEXT_LARGE`, `TEXT_EMBEDDING`, `OBJECT_SMALL`, `OBJECT_LARGE`, `IMAGE`, `AUDIO`, `VIDEO`
