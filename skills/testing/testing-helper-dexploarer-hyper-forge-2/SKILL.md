---
name: testing-helper
description: Create comprehensive tests for elizaOS plugins, characters, and actions. Triggers on "create tests", "test elizaOS plugin", or "write agent tests"
allowed-tools: [Write, Read, Edit]
---

# Testing Helper Skill

Generate comprehensive test suites for elizaOS components with unit, integration, and E2E tests.

## Test Structure

```
__tests__/
├── unit/
│   ├── actions.test.ts
│   ├── providers.test.ts
│   ├── evaluators.test.ts
│   └── services.test.ts
├── integration/
│   ├── plugin.test.ts
│   └── character.test.ts
└── e2e/
    └── agent-flow.test.ts
```

## Action Tests

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { myAction } from '../src/actions/myAction';
import { createMockRuntime, createMockMessage } from '@elizaos/core/test';

describe('MyAction', () => {
  let runtime: any;
  let message: any;

  beforeEach(() => {
    runtime = createMockRuntime();
    message = createMockMessage();
  });

  it('validates correct input', async () => {
    const valid = await myAction.validate(runtime, message);
    expect(valid).toBe(true);
  });

  it('rejects invalid input', async () => {
    message.content = {};
    const valid = await myAction.validate(runtime, message);
    expect(valid).toBe(false);
  });

  it('executes successfully', async () => {
    const result = await myAction.handler(runtime, message);
    expect(result).toBeDefined();
  });

  it('handles errors gracefully', async () => {
    runtime.createMemory = () => { throw new Error('Test error'); };
    const result = await myAction.handler(runtime, message);
    expect(result).toContain('failed');
  });
});
```

## Provider Tests

```typescript
describe('MyProvider', () => {
  it('returns valid data', async () => {
    const result = await myProvider.get(runtime, message);

    expect(result).toHaveProperty('values');
    expect(result).toHaveProperty('data');
    expect(result).toHaveProperty('text');
    expect(typeof result.text).toBe('string');
  });

  it('handles missing data', async () => {
    const result = await myProvider.get(runtime, null);
    expect(result.text).toBe('');
  });
});
```

## Character Tests

```typescript
describe('Character Configuration', () => {
  it('has required fields', () => {
    expect(character.name).toBeDefined();
    expect(character.bio).toBeDefined();
  });

  it('has valid plugins', () => {
    expect(character.plugins).toContain('@elizaos/plugin-bootstrap');
  });

  it('has valid message examples', () => {
    character.messageExamples?.forEach(conversation => {
      expect(Array.isArray(conversation)).toBe(true);
      conversation.forEach(msg => {
        expect(msg).toHaveProperty('name');
        expect(msg).toHaveProperty('content');
      });
    });
  });
});
```

## Integration Tests

```typescript
describe('Plugin Integration', () => {
  let runtime: AgentRuntime;

  beforeAll(async () => {
    runtime = new AgentRuntime({
      character: testCharacter,
      plugins: [myPlugin]
    });
    await runtime.initialize();
  });

  afterAll(async () => {
    await runtime.stop();
  });

  it('loads plugin correctly', () => {
    expect(runtime.plugins).toContain(myPlugin);
  });

  it('registers actions', () => {
    const action = runtime.actions.find(a => a.name === 'MY_ACTION');
    expect(action).toBeDefined();
  });
});
```

## E2E Tests

```typescript
describe('Agent Flow', () => {
  it('processes message end-to-end', async () => {
    const response = await runtime.processMessage({
      content: { text: 'Hello' },
      senderId: 'user-1',
      roomId: 'room-1'
    });

    expect(response.content.text).toBeDefined();
  });
});
```

## Coverage Requirements

- Unit tests: >80% code coverage
- Integration tests: All components
- E2E tests: Main user flows
- Error scenarios tested
- Edge cases covered
