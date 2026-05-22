---
name: libharness
description: >
  libharness - Test harness and mock infrastructure. createMockStorage,
  createMockConfig, createMockLogger provide framework mocks.
  createMockMemoryClient, createMockLlmClient, createMockAgentClient provide
  service client mocks. createMockGrpcCall for gRPC testing. Use for unit
  testing services and packages with isolated dependencies.
---

# libharness Skill

## When to Use

- Writing unit tests for services and packages
- Mocking external dependencies (storage, config, logging)
- Creating isolated test environments
- Testing gRPC service implementations

## Key Concepts

**Framework mocks**: createMockStorage, createMockConfig, createMockLogger
provide test doubles for core infrastructure.

**Client mocks**: createMockMemoryClient, createMockLlmClient, etc. provide test
doubles for gRPC service clients.

**Fixtures**: Pre-configured test data and assertion helpers.

## Usage Patterns

### Pattern 1: Mock infrastructure

```javascript
import {
  createMockConfig,
  createMockStorage,
  createMockLogger,
} from "@copilot-ld/libharness";

const config = createMockConfig("test-service");
const storage = createMockStorage();
const logger = createMockLogger();
```

### Pattern 2: Mock service clients

```javascript
import { createMockLlmClient } from "@copilot-ld/libharness";

const llmClient = createMockLlmClient({
  completionResponse: { content: "Hello" },
});
```

## Integration

Used across all test files. Requires libtype for generated type mocks.
