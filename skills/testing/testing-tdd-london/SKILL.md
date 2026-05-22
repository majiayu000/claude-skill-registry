---
name: testing-tdd-london
description: TDD London School (mockist) specialist for mock-driven, outside-in development. Use for behavior verification testing, contract-driven development, testing object collaborations, or when focusing on HOW objects interact rather than WHAT they contain.
version: 1.0.0
category: development
type: hybrid
capabilities:
  - mock_driven_development
  - outside_in_tdd
  - behavior_verification
  - contract_testing
  - interaction_testing
  - swarm_test_coordination
tools:
  - Read
  - Write
  - Bash
  - Task
  - mcp__claude-flow__memory_usage
related_skills:
  - testing-production
  - planning-code-goal
  - webapp-testing
hooks:
  pre: |
    echo "TDD London School session starting..."
    if command -v npx >/dev/null 2>&1; then
      echo "Coordinating with swarm test agents..."
    fi
  post: |
    echo "London School TDD complete - mocks verified"
    if [ -f "package.json" ]; then
      npm test --if-present
    fi
---

# TDD London School (Mockist)

> Outside-in, mock-driven development focusing on object collaborations and behavior verification

## Quick Start

```typescript
// 1. Start with acceptance test (outside)
describe('User Registration', () => {
  it('should register new user successfully', async () => {
    const mockRepository = { save: jest.fn().mockResolvedValue({ id: '123' }) };
    const mockNotifier = { sendWelcome: jest.fn() };

    const service = new UserService(mockRepository, mockNotifier);
    await service.register({ email: 'test@example.com' });

    // 2. Verify behavior (interactions)
    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'test@example.com' })
    );
    expect(mockNotifier.sendWelcome).toHaveBeenCalledWith('123');
  });
});
```

## When to Use

- Testing object collaborations and message passing
- Contract-driven development with clear interfaces
- Outside-in development starting from user behavior
- When isolation of units is critical
- Service orchestration testing
- Testing HOW objects work together (not WHAT they contain)

## Prerequisites

- Understanding of mock objects vs stubs
- Jest, Vitest, or similar testing framework with mocking support
- Clear separation of concerns in architecture
- Dependency injection pattern in codebase

## Core Concepts

### London vs Chicago School

| Aspect | London (Mockist) | Chicago (Classicist) |
|--------|------------------|----------------------|
| Focus | Behavior/Interactions | State |
| Isolation | Mock all collaborators | Use real objects |
| Direction | Outside-in | Inside-out |
| Test What | HOW objects talk | WHAT objects produce |
| Coupling | To implementation | To behavior |

### Outside-In Development Flow

```
Acceptance Test (failing)
    |
    v
Controller Test (failing)
    |
    v
Service Test (failing)
    |
    v
Repository Test (failing)
    |
    v
Implement (make tests pass from bottom up)
```

### Mock Types

```typescript
// Stub: Returns canned responses
const stubRepo = { findById: jest.fn().mockResolvedValue(user) };

// Mock: Verifies interactions
const mockNotifier = { send: jest.fn() };
// Later: expect(mockNotifier.send).toHaveBeenCalledWith(expectedArgs);

// Spy: Wraps real object, records calls
const spyLogger = jest.spyOn(logger, 'info');
```

## Implementation Pattern

### 1. Outside-In Development

```typescript
// Start with acceptance test (outermost layer)
describe('User Registration Feature', () => {
  it('should register new user successfully', async () => {
    // Mock all collaborators
    const mockRepository = {
      save: jest.fn().mockResolvedValue({ id: '123', email: 'test@example.com' }),
      findByEmail: jest.fn().mockResolvedValue(null)
    };

    const mockNotifier = {
      sendWelcome: jest.fn().mockResolvedValue(true)
    };

    const userService = new UserService(mockRepository, mockNotifier);
    const result = await userService.register({
      email: 'test@example.com',
      password: 'secure123'
    });

    // Verify the conversation between objects
    expect(mockRepository.findByEmail).toHaveBeenCalledWith('test@example.com');
    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'test@example.com' })
    );
    expect(mockNotifier.sendWelcome).toHaveBeenCalledWith('123');
    expect(result.success).toBe(true);
  });
});
```

### 2. Interaction Testing

```typescript
describe('Order Processing', () => {
  it('should follow proper workflow interactions', async () => {
    const mockPayment = { charge: jest.fn().mockResolvedValue({ success: true }) };
    const mockInventory = { reserve: jest.fn().mockResolvedValue(true) };
    const mockShipping = { schedule: jest.fn().mockResolvedValue({ trackingId: 'ABC' }) };

    const service = new OrderService(mockPayment, mockInventory, mockShipping);
    await service.processOrder(order);

    // Verify call order matters
    const callOrder = [];
    mockInventory.reserve.mockImplementation(() => {
      callOrder.push('reserve');
      return Promise.resolve(true);
    });
    mockPayment.charge.mockImplementation(() => {
      callOrder.push('charge');
      return Promise.resolve({ success: true });
    });
    mockShipping.schedule.mockImplementation(() => {
      callOrder.push('schedule');
      return Promise.resolve({ trackingId: 'ABC' });
    });

    await service.processOrder(order);
    expect(callOrder).toEqual(['reserve', 'charge', 'schedule']);
  });
});
```

### 3. Contract Definition Through Mocks

```typescript
// Define contracts for collaborators
const userServiceContract = {
  register: {
    input: { email: 'string', password: 'string' },
    output: { success: 'boolean', id: 'string' },
    collaborators: ['UserRepository', 'NotificationService'],
    interactions: [
      { method: 'findByEmail', args: ['email'], returns: 'null|User' },
      { method: 'save', args: ['User'], returns: 'User' },
      { method: 'sendWelcome', args: ['userId'], returns: 'boolean' }
    ]
  }
};

// Generate mocks from contract
function createMockFromContract(contract) {
  return Object.fromEntries(
    contract.interactions.map(i => [i.method, jest.fn()])
  );
}
```

## Configuration

```yaml
london_tdd_config:
  testing:
    framework: jest
    mock_library: jest  # or sinon, testdouble
    strict_mocks: true  # fail on unexpected calls

  coverage:
    interaction_coverage: true
    verify_all_mocks: true

  swarm_coordination:
    share_contracts: true
    sync_mock_definitions: true

  patterns:
    verify_call_order: true
    verify_call_count: true
    verify_call_args: true
```

## Usage Examples

### Example 1: Service Orchestration Test

```typescript
describe('Service Collaboration', () => {
  let mockServiceA: jest.Mocked<ServiceA>;
  let mockServiceB: jest.Mocked<ServiceB>;
  let mockServiceC: jest.Mocked<ServiceC>;
  let orchestrator: ServiceOrchestrator;

  beforeEach(() => {
    mockServiceA = {
      prepare: jest.fn().mockResolvedValue({ data: 'prepared' })
    };
    mockServiceB = {
      process: jest.fn().mockResolvedValue({ result: 'processed' })
    };
    mockServiceC = {
      finalize: jest.fn().mockResolvedValue({ status: 'complete' })
    };

    orchestrator = new ServiceOrchestrator(
      mockServiceA,
      mockServiceB,
      mockServiceC
    );
  });

  it('should coordinate dependencies in correct order', async () => {
    await orchestrator.execute(task);

    // Verify coordination sequence
    expect(mockServiceA.prepare).toHaveBeenCalledBefore(mockServiceB.process);
    expect(mockServiceB.process).toHaveBeenCalledBefore(mockServiceC.finalize);

    // Verify data flow between services
    expect(mockServiceB.process).toHaveBeenCalledWith(
      expect.objectContaining({ data: 'prepared' })
    );
    expect(mockServiceC.finalize).toHaveBeenCalledWith(
      expect.objectContaining({ result: 'processed' })
    );
  });
});
```

### Example 2: Error Handling Verification

```typescript
describe('Error Handling', () => {
  it('should handle repository failure gracefully', async () => {
    const mockRepository = {
      save: jest.fn().mockRejectedValue(new Error('Connection failed'))
    };
    const mockLogger = {
      error: jest.fn()
    };
    const mockRetry = {
      attempt: jest.fn().mockResolvedValue(false)
    };

    const service = new UserService(mockRepository, mockLogger, mockRetry);

    await expect(service.register(userData)).rejects.toThrow('Registration failed');

    // Verify error handling interactions
    expect(mockLogger.error).toHaveBeenCalledWith(
      'Repository save failed',
      expect.objectContaining({ error: expect.any(Error) })
    );
    expect(mockRetry.attempt).toHaveBeenCalledTimes(3);
  });
});
```

### Example 3: Swarm Coordination Testing

```typescript
describe('Swarm Test Coordination', () => {
  let swarmCoordinator: SwarmCoordinator;

  beforeAll(async () => {
    // Signal other swarm agents
    await swarmCoordinator.notifyTestStart('unit-tests');
  });

  afterAll(async () => {
    // Share test results with swarm
    await swarmCoordinator.shareResults(testResults);
  });

  it('should share mock contracts across swarm', () => {
    const sharedMocks = {
      userRepository: createSwarmMock('UserRepository', {
        save: jest.fn(),
        findByEmail: jest.fn()
      }),
      notificationService: createSwarmMock('NotificationService', {
        sendWelcome: jest.fn()
      })
    };

    // Other swarm agents can verify against these contracts
    swarmCoordinator.publishContracts(sharedMocks);
  });
});
```

## Execution Checklist

- [ ] Write failing acceptance test (outside)
- [ ] Define mock contracts for all collaborators
- [ ] Write failing unit test for next layer
- [ ] Implement minimal code to pass test
- [ ] Verify all mock interactions
- [ ] Refactor while keeping tests green
- [ ] Move to next inner layer
- [ ] Share contracts with swarm if coordinating

## Best Practices

### Mock Management
- Keep mocks simple and focused on single behavior
- Verify interactions, not implementation details
- Use `jest.fn()` for behavior verification
- Avoid over-mocking internal details
- Reset mocks between tests

### Contract Design
- Define clear interfaces through mock expectations
- Focus on object responsibilities and collaborations
- Use mocks to DRIVE design decisions
- Keep contracts minimal and cohesive

### Common Pitfalls

```typescript
// BAD: Over-mocking internal details
const mock = {
  _internalState: {},
  _privateMethod: jest.fn()  // Don't mock private methods
};

// GOOD: Mock only public interface
const mock = {
  publicMethod: jest.fn().mockReturnValue(expectedResult)
};

// BAD: Verifying too many implementation details
expect(mock.method).toHaveBeenCalledTimes(3);  // Fragile

// GOOD: Verify essential behavior
expect(mock.method).toHaveBeenCalledWith(expectedArgs);
```

## Error Handling

### Missing Mock Verification

```typescript
// Always verify mocks were called as expected
afterEach(() => {
  // Fail if any mock was called unexpectedly
  expect(unexpectedCallsDetected()).toBe(false);
});

// Use strict mocks
const strictMock = jest.fn().mockImplementation(() => {
  throw new Error('Unexpected call');
});
```

### Mock Leakage Between Tests

```typescript
// Always reset mocks
beforeEach(() => {
  jest.clearAllMocks();  // Clears call history
  // or
  jest.resetAllMocks();  // Also resets implementation
});
```

## Metrics & Success Criteria

| Metric | Target | Description |
|--------|--------|-------------|
| Interaction Coverage | 100% | All collaborator calls verified |
| Mock Isolation | 100% | No real dependencies in unit tests |
| Contract Consistency | 100% | Mocks match real interfaces |
| Test Speed | < 100ms | Per test (no I/O) |

## Integration Points

### MCP Tools

```javascript
// Store successful test patterns
mcp__claude-flow__memory_usage({
  action: "store",
  namespace: "test-patterns",
  key: "order_processing_mocks",
  value: JSON.stringify(mockDefinitions)
});

// Share contracts across swarm
mcp__claude-flow__memory_usage({
  action: "store",
  namespace: "test-contracts",
  key: "user_service_contract",
  value: JSON.stringify(userServiceContract)
});
```

### Hooks

```bash
# Pre-test: Coordinate with swarm
npx claude-flow@alpha hooks pre-task --description "TDD London: $TEST_SUITE"

# Post-test: Share results
npx claude-flow@alpha hooks post-task --task-id "tdd-$SESSION_ID"
```

### Related Skills

- [testing-production](../testing-production/SKILL.md) - Production validation
- [planning-code-goal](../../planning/planning-code-goal/SKILL.md) - TDD integration in SPARC
- [webapp-testing](../../webapp-testing/SKILL.md) - Web application testing

## References

- [London School TDD](https://github.com/testdouble/contributing-tests/wiki/London-school-TDD)
- [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Growing Object-Oriented Software](http://www.growing-object-oriented-software.com/)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from tdd-london-swarm agent
