---
name: plugin-builder
description: Scaffold complete elizaOS plugins with actions, providers, evaluators, and services. Triggers when user asks to "create plugin", "build elizaOS extension", or "scaffold plugin structure"
allowed-tools: [Write, Read, Edit, Grep, Glob, Bash]
---

# Plugin Builder Skill

A comprehensive skill that scaffolds production-ready elizaOS plugins with proper structure, TypeScript configuration, testing setup, and documentation.

## When to Use

This skill activates when you need to:
- Create a new elizaOS plugin from scratch
- Add custom actions, providers, or services
- Extend elizaOS with new capabilities
- Build reusable plugin packages

**Trigger phrases:**
- "Create a plugin for [capability]"
- "Build an elizaOS plugin that [does something]"
- "Scaffold a new plugin"
- "Generate plugin structure for [feature]"

## Capabilities

This skill can:
1. 🏗️ Scaffold complete plugin structure
2. ⚡ Generate actions with validation and handlers
3. 📊 Create providers for context enrichment
4. ✅ Build evaluators for response quality
5. 🔌 Implement services for platform integrations
6. 🧪 Set up comprehensive testing
7. 📦 Configure TypeScript and build tools
8. 📚 Generate complete documentation

## Plugin Architecture

```typescript
interface Plugin {
  name: string;                    // Unique plugin identifier
  description?: string;            // Plugin purpose
  dependencies?: string[];         // Required plugins

  // Extensibility Components
  actions?: Action[];              // Executable operations
  providers?: Provider[];          // Context enrichment
  evaluators?: Evaluator[];        // Response quality
  services?: typeof Service[];     // Platform integrations
  models?: ModelHandlers;          // Custom model handlers

  // Lifecycle Hooks
  init?(config: any, runtime: IAgentRuntime): Promise<void>;
  start?(runtime: IAgentRuntime): Promise<void>;
  stop?(runtime: IAgentRuntime): Promise<void>;
}
```

## Workflow

### Phase 1: Requirements Analysis

**Ask these questions:**

1. **Plugin Purpose**: "What capability does this plugin add?"
   - Platform integration (Discord, Telegram, Slack)
   - External service (API, database, search)
   - Custom action (file operations, calculations)
   - Data enrichment (context, analytics)
   - Response enhancement (formatting, validation)

2. **Components Needed**:
   - Actions: User-triggered operations?
   - Providers: Context enrichment needed?
   - Evaluators: Response validation required?
   - Services: Long-running processes?
   - Models: Custom LLM handlers?

3. **Dependencies**:
   - External npm packages?
   - API credentials required?
   - Other elizaOS plugins?
   - System requirements?

4. **Configuration**:
   - Environment variables needed?
   - Runtime settings?
   - Secrets management?

### Phase 2: Plugin Structure

```
plugin-{name}/
├── package.json
├── tsconfig.json
├── .env.example
├── README.md
├── src/
│   ├── index.ts              # Plugin export
│   ├── types.ts              # TypeScript interfaces
│   ├── actions/              # Action implementations
│   │   ├── index.ts
│   │   └── {actionName}.ts
│   ├── providers/            # Provider implementations
│   │   ├── index.ts
│   │   └── {providerName}.ts
│   ├── evaluators/           # Evaluator implementations
│   │   ├── index.ts
│   │   └── {evaluatorName}.ts
│   ├── services/             # Service implementations
│   │   ├── index.ts
│   │   └── {serviceName}.ts
│   └── utils/                # Utility functions
│       └── index.ts
├── __tests__/                # Tests
│   ├── actions.test.ts
│   ├── providers.test.ts
│   ├── evaluators.test.ts
│   └── integration.test.ts
└── examples/                 # Usage examples
    └── basic-usage.ts
```

### Phase 3: Implementation

**Step 1: Initialize Plugin**

```bash
# Create directory structure
mkdir -p plugin-{name}/{src/{actions,providers,evaluators,services,utils},__tests__,examples}
cd plugin-{name}
```

**Step 2: Package Configuration**

```json
{
  "name": "@elizaos/plugin-{name}",
  "version": "1.0.0",
  "description": "{Plugin description}",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write \"src/**/*.ts\""
  },
  "dependencies": {
    "@elizaos/core": "latest",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  },
  "keywords": [
    "elizaos",
    "plugin",
    "{keywords}"
  ],
  "author": "{Your Name}",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/{org}/plugin-{name}"
  }
}
```

**Step 3: TypeScript Configuration**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "esModuleInterop": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "__tests__"]
}
```

**Step 4: Create Types**

```typescript
// src/types.ts

import type {
  Action,
  Provider,
  Evaluator,
  Service,
  IAgentRuntime,
  Memory,
  State
} from '@elizaos/core';

// Plugin Configuration
export interface {PluginName}Config {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
  // Add your config properties
}

// Action Types
export interface {Action}Input {
  // Input parameters
}

export interface {Action}Output {
  // Output structure
}

// Provider Types
export interface {Provider}Data {
  // Provider data structure
}

// Service Types
export interface {Service}Config {
  // Service configuration
}

// Export plugin type
export interface {PluginName}Plugin {
  name: string;
  description: string;
  actions?: Action[];
  providers?: Provider[];
  evaluators?: Evaluator[];
  services?: typeof Service[];
}
```

**Step 5: Create Action**

```typescript
// src/actions/{actionName}.ts

import {
  type Action,
  type IAgentRuntime,
  type Memory,
  type State,
  type HandlerCallback
} from '@elizaos/core';
import { z } from 'zod';

// Input validation schema
const {action}Schema = z.object({
  param1: z.string().min(1),
  param2: z.number().optional(),
  // Add your parameters
});

export const {action}Action: Action = {
  name: '{ACTION_NAME}',

  // Similar action names for triggering
  similes: [
    'SIMILAR_NAME_1',
    'SIMILAR_NAME_2',
    'ALTERNATIVE_NAME'
  ],

  description: '{What this action does and when to use it}',

  // Usage examples for training
  examples: [
    [
      {
        user: "{{user}}",
        content: { text: "Can you {action example}?" }
      },
      {
        user: "{{agentName}}",
        content: {
          text: "{I'll {action} for you}",
          action: "{ACTION_NAME}"
        }
      }
    ],
    [
      {
        user: "{{user}}",
        content: { text: "{Another way to trigger action}" }
      },
      {
        user: "{{agentName}}",
        content: {
          text: "{Response}",
          action: "{ACTION_NAME}"
        }
      }
    ]
  ],

  // Validate if action should execute
  validate: async (
    runtime: IAgentRuntime,
    message: Memory,
    state?: State
  ): Promise<boolean> => {
    try {
      // Extract parameters from message
      const params = extractParams(message);

      // Validate with Zod
      {action}Schema.parse(params);

      // Additional validation logic
      if (!hasRequiredPermissions(runtime, message)) {
        return false;
      }

      return true;
    } catch (error) {
      console.error('Validation failed:', error);
      return false;
    }
  },

  // Execute action
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state?: State,
    options?: any,
    callback?: HandlerCallback
  ): Promise<string | null> => {
    try {
      // Extract and validate parameters
      const params = extractParams(message);
      const validated = {action}Schema.parse(params);

      // Send progress update
      if (callback) {
        callback({
          text: 'Processing {action}...',
          action: '{ACTION_NAME}'
        });
      }

      // Execute action logic
      const result = await performAction(validated, runtime);

      // Store result in memory if needed
      await runtime.createMemory({
        entityId: runtime.agentId,
        roomId: message.roomId,
        content: {
          text: `Action {ACTION_NAME} completed`,
          metadata: { result }
        }
      });

      // Return success message
      return formatSuccessResponse(result);

    } catch (error) {
      console.error('Action failed:', error);

      // Return error message
      return formatErrorResponse(error);
    }
  }
};

// Helper functions
function extractParams(message: Memory): any {
  // Extract parameters from message content
  return {
    param1: message.content.param1,
    param2: message.content.param2
  };
}

async function performAction(params: any, runtime: IAgentRuntime): Promise<any> {
  // Implement action logic
  // Access runtime.getService() for services
  // Use runtime.createMemory() for storing data

  return {
    success: true,
    data: {}
  };
}

function hasRequiredPermissions(runtime: IAgentRuntime, message: Memory): boolean {
  // Check permissions
  return true;
}

function formatSuccessResponse(result: any): string {
  return `✅ {Action} completed successfully: ${JSON.stringify(result)}`;
}

function formatErrorResponse(error: any): string {
  return `❌ {Action} failed: ${error.message}`;
}
```

**Step 6: Create Provider**

```typescript
// src/providers/{providerName}.ts

import {
  type Provider,
  type IAgentRuntime,
  type Memory,
  type State
} from '@elizaos/core';

export const {provider}Provider: Provider = {
  name: '{PROVIDER_NAME}',

  description: '{What context this provider adds}',

  // Optional: only execute when explicitly requested
  dynamic: false,

  // Optional: hide from public context
  private: false,

  // Execution order (lower = earlier)
  position: 100,

  // Gather and format context
  get: async (
    runtime: IAgentRuntime,
    message: Memory,
    state?: State
  ): Promise<{
    values: Record<string, any>;
    data: Record<string, any>;
    text: string;
  }> => {
    try {
      // Gather data
      const data = await gatherData(runtime, message);

      // Format for template usage
      const values = {
        key1: data.value1,
        key2: data.value2
      };

      // Format as text for LLM context
      const text = formatAsText(data);

      return {
        values,  // For template variables
        data,    // For programmatic access
        text     // For LLM context
      };

    } catch (error) {
      console.error('Provider failed:', error);

      // Return empty result on error
      return {
        values: {},
        data: {},
        text: ''
      };
    }
  }
};

async function gatherData(runtime: IAgentRuntime, message: Memory): Promise<any> {
  // Fetch data from external sources
  // Query database
  // Process information

  return {
    value1: 'data',
    value2: 123
  };
}

function formatAsText(data: any): string {
  // Format data as natural language for LLM
  return `
{Provider Name} Context:
- Value 1: ${data.value1}
- Value 2: ${data.value2}
`.trim();
}
```

**Step 7: Create Service**

```typescript
// src/services/{serviceName}.ts

import {
  Service,
  ServiceTypeName,
  type IAgentRuntime
} from '@elizaos/core';

export class {Service}Service extends Service {
  static serviceType: ServiceTypeName = '{SERVICE_TYPE}' as ServiceTypeName;

  capabilityDescription: string = '{What this service provides}';

  private client: any;
  private config: any;

  constructor(runtime: IAgentRuntime) {
    super(runtime);

    // Initialize configuration
    this.config = {
      apiKey: runtime.character.settings.{service}ApiKey,
      baseUrl: runtime.character.settings.{service}BaseUrl || 'https://api.example.com',
      timeout: runtime.character.settings.{service}Timeout || 30000
    };
  }

  // Start service
  static async start(runtime: IAgentRuntime): Promise<Service> {
    const service = new {Service}Service(runtime);
    await service.initialize();
    return service;
  }

  // Initialize service
  async initialize(): Promise<void> {
    try {
      // Initialize client
      this.client = createClient(this.config);

      // Test connection
      await this.client.healthCheck();

      console.log('✅ {Service} initialized successfully');
    } catch (error) {
      console.error('❌ {Service} initialization failed:', error);
      throw error;
    }
  }

  // Stop service
  async stop(): Promise<void> {
    try {
      // Cleanup resources
      if (this.client) {
        await this.client.close();
      }

      console.log('✅ {Service} stopped successfully');
    } catch (error) {
      console.error('❌ {Service} stop failed:', error);
    }
  }

  // Service methods
  async doSomething(params: any): Promise<any> {
    try {
      return await this.client.request(params);
    } catch (error) {
      console.error('Service request failed:', error);
      throw error;
    }
  }
}

function createClient(config: any): any {
  // Create and return API client
  return {
    healthCheck: async () => true,
    request: async (params: any) => ({ success: true }),
    close: async () => {}
  };
}
```

**Step 8: Create Plugin Index**

```typescript
// src/index.ts

import type { Plugin } from '@elizaos/core';

// Import components
import { {action}Action } from './actions/{actionName}.js';
import { {provider}Provider } from './providers/{providerName}.js';
import { {Service}Service } from './services/{serviceName}.js';

// Export types
export * from './types.js';

// Export plugin
export const {plugin}Plugin: Plugin = {
  name: '@elizaos/plugin-{name}',
  description: '{Plugin description}',

  // Optional: Dependencies
  dependencies: [],

  // Components
  actions: [{action}Action],
  providers: [{provider}Provider],
  services: [{Service}Service],

  // Lifecycle hooks
  async init(config: any, runtime: any): Promise<void> {
    console.log('Initializing {plugin} plugin...');
    // Initialization logic
  },

  async start(runtime: any): Promise<void> {
    console.log('Starting {plugin} plugin...');
    // Startup logic
  },

  async stop(runtime: any): Promise<void> {
    console.log('Stopping {plugin} plugin...');
    // Cleanup logic
  }
};

export default {plugin}Plugin;
```

**Step 9: Create Tests**

```typescript
// __tests__/actions.test.ts

import { describe, it, expect, beforeEach } from 'vitest';
import { {action}Action } from '../src/actions/{actionName}';
import { createMockRuntime, createMockMessage } from '@elizaos/core/test';

describe('{Action} Action', () => {
  let runtime: any;
  let message: any;

  beforeEach(() => {
    runtime = createMockRuntime();
    message = createMockMessage({
      content: {
        text: 'test message',
        param1: 'value1'
      }
    });
  });

  it('validates correct input', async () => {
    const isValid = await {action}Action.validate(runtime, message);
    expect(isValid).toBe(true);
  });

  it('rejects invalid input', async () => {
    message.content.param1 = '';
    const isValid = await {action}Action.validate(runtime, message);
    expect(isValid).toBe(false);
  });

  it('executes successfully', async () => {
    const result = await {action}Action.handler(runtime, message);
    expect(result).toContain('success');
  });

  it('handles errors gracefully', async () => {
    // Force an error
    runtime.createMemory = () => {
      throw new Error('Test error');
    };

    const result = await {action}Action.handler(runtime, message);
    expect(result).toContain('failed');
  });
});
```

**Step 10: Create Documentation**

```markdown
# @elizaos/plugin-{name}

{Brief description of plugin purpose and capabilities}

## Features

- ✨ {Feature 1}
- ⚡ {Feature 2}
- 🔒 {Feature 3}

## Installation

```bash
npm install @elizaos/plugin-{name}
```

## Configuration

Add the plugin to your character configuration:

```typescript
import { {plugin}Plugin } from '@elizaos/plugin-{name}';

export const character: Character = {
  // ... other config
  plugins: [
    '@elizaos/plugin-bootstrap',
    {plugin}Plugin
  ],
  settings: {
    {service}ApiKey: process.env.{SERVICE}_API_KEY,
    {service}BaseUrl: 'https://api.example.com',
    {service}Timeout: 30000
  }
};
```

## Environment Variables

```bash
# Required
{SERVICE}_API_KEY=your-api-key

# Optional
{SERVICE}_BASE_URL=https://api.example.com
{SERVICE}_TIMEOUT=30000
```

## Actions

### {ACTION_NAME}

{Action description}

**Usage:**
```
User: Can you {action}?
Agent: {I'll do the action}
```

**Parameters:**
- `param1` (string, required): {Description}
- `param2` (number, optional): {Description}

## Providers

### {PROVIDER_NAME}

{Provider description}

Adds the following to agent context:
- {Context item 1}
- {Context item 2}

## Services

### {Service}Service

{Service description}

**Methods:**
- `doSomething(params)`: {Method description}

## Usage Examples

### Basic Usage

```typescript
import { AgentRuntime } from '@elizaos/core';
import { {plugin}Plugin } from '@elizaos/plugin-{name}';
import character from './character';

const runtime = new AgentRuntime({
  character,
  plugins: [{plugin}Plugin]
});

await runtime.initialize();
```

### Using Actions Programmatically

```typescript
import { {action}Action } from '@elizaos/plugin-{name}';

const result = await {action}Action.handler(
  runtime,
  message,
  state,
  options,
  callback
);
```

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Development

```bash
# Build
npm run build

# Watch mode
npm run dev

# Lint
npm run lint

# Format
npm run format
```

## API Reference

{Detailed API documentation}

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT

## Support

- 📚 [Documentation](https://docs.elizaos.ai)
- 💬 [Discord](https://discord.gg/elizaos)
- 🐛 [Issues](https://github.com/{org}/plugin-{name}/issues)
```

## Plugin Templates

### 1. Platform Integration Plugin

For integrating new chat platforms (Slack, WhatsApp, etc.):

- Service for platform connection
- Actions for platform-specific features
- Message formatting providers
- Platform event handlers

### 2. External API Plugin

For accessing external services:

- Actions for API operations
- Providers for data enrichment
- Error handling and retries
- Rate limiting and caching

### 3. Data Processing Plugin

For data transformation and analysis:

- Actions for processing operations
- Providers for context enrichment
- Evaluators for result validation
- Caching for performance

### 4. Custom Model Plugin

For integrating custom LLMs:

- Model handlers for inference
- Token counting utilities
- Streaming support
- Fallback mechanisms

## Best Practices

1. **Type Safety**: Use TypeScript strictly, no `any` types
2. **Error Handling**: Catch and log all errors gracefully
3. **Validation**: Use Zod for input validation
4. **Testing**: Achieve >80% code coverage
5. **Documentation**: Document all public APIs
6. **Security**: Never log sensitive data
7. **Performance**: Implement caching where appropriate
8. **Compatibility**: Test with multiple elizaOS versions
9. **Dependencies**: Minimize external dependencies
10. **Versioning**: Follow semantic versioning

## Output Checklist

After generating a plugin:

✅ Directory structure created
✅ Package configuration
✅ TypeScript configuration
✅ Type definitions
✅ Actions implemented
✅ Providers implemented
✅ Services implemented
✅ Tests written (>80% coverage)
✅ Documentation complete
✅ Examples provided
✅ Environment template
✅ Build scripts configured

Then display:

```
🔌 Plugin "@elizaos/plugin-{name}" created successfully!

📋 Summary:
   Name: @elizaos/plugin-{name}
   Actions: {count}
   Providers: {count}
   Services: {count}
   Dependencies: {list}

📂 Structure:
   ✅ src/index.ts - Plugin entry point
   ✅ src/actions/ - Action implementations
   ✅ src/providers/ - Provider implementations
   ✅ src/services/ - Service implementations
   ✅ __tests__/ - Test suite
   ✅ README.md - Documentation

🚀 Next steps:
   1. Install dependencies: npm install
   2. Build plugin: npm run build
   3. Run tests: npm test
   4. Test integration with character
   5. Publish to npm: npm publish

📖 Read README.md for usage instructions
```
