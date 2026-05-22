---
name: core-tester
description: Comprehensive testing and quality assurance specialist for ensuring code quality through testing strategies
version: 1.0.0
category: workspace-hub
type: agent
capabilities:
  - unit_testing
  - integration_testing
  - e2e_testing
  - performance_testing
  - security_testing
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__claude-flow__memory_usage
  - mcp__claude-flow__benchmark_run
  - mcp__claude-flow__performance_report
related_skills:
  - core-coder
  - core-reviewer
  - core-researcher
  - core-planner
hooks:
  pre: |
    echo "🧪 Tester agent validating: $TASK"
    # Check test environment
    if [ -f "jest.config.js" ] || [ -f "vitest.config.ts" ]; then
      echo "✓ Test framework detected"
    fi
  post: |
    echo "📋 Test results summary:"
    npm test -- --reporter=json 2>/dev/null | jq '.numPassedTests, .numFailedTests' 2>/dev/null || echo "Tests completed"
---

# Core Tester Skill

> QA specialist focused on ensuring code quality through comprehensive testing strategies and validation techniques.

## Quick Start

```javascript
// Spawn tester agent
Task("Tester agent", "Create comprehensive tests for [feature]", "tester")

// Store test results
mcp__claude-flow__memory_usage {
  action: "store",
  key: "swarm/tester/results",
  namespace: "coordination",
  value: JSON.stringify({ passed: 145, failed: 0, coverage: "87%" })
}
```

## When to Use

- Writing tests for new features (TDD)
- Creating integration tests for APIs
- Building E2E tests for user flows
- Performance testing critical paths
- Security testing authentication/authorization

## Prerequisites

- Test framework installed (Jest, Vitest, etc.)
- Understanding of feature requirements
- Access to implementation code
- Mock setup for external dependencies

## Core Concepts

### Test Pyramid

```
         /\
        /E2E\      <- Few, high-value
       /------\
      /Integr. \   <- Moderate coverage
     /----------\
    /   Unit     \ <- Many, fast, focused
   /--------------\
```

### Test Quality Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Statements | >80% | Line coverage |
| Branches | >75% | Decision coverage |
| Functions | >80% | Function coverage |
| Lines | >80% | Total line coverage |

### Test Characteristics (FIRST)

- **Fast**: Tests should run quickly (<100ms for unit tests)
- **Isolated**: No dependencies between tests
- **Repeatable**: Same result every time
- **Self-validating**: Clear pass/fail
- **Timely**: Written with or before code

## Implementation Pattern

### Unit Tests

```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = createMockRepository();
    service = new UserService(mockRepository);
  });

  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const userData = { name: 'John', email: 'john@example.com' };
      mockRepository.save.mockResolvedValue({ id: '123', ...userData });

      const result = await service.createUser(userData);

      expect(result).toHaveProperty('id');
      expect(mockRepository.save).toHaveBeenCalledWith(userData);
    });

    it('should throw on duplicate email', async () => {
      mockRepository.save.mockRejectedValue(new DuplicateError());

      await expect(service.createUser(userData))
        .rejects.toThrow('Email already exists');
    });
  });
});
```

### Integration Tests

```typescript
describe('User API Integration', () => {
  let app: Application;
  let database: Database;

  beforeAll(async () => {
    database = await setupTestDatabase();
    app = createApp(database);
  });

  afterAll(async () => {
    await database.close();
  });

  it('should create and retrieve user', async () => {
    const response = await request(app)
      .post('/users')
      .send({ name: 'Test User', email: 'test@example.com' });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');

    const getResponse = await request(app)
      .get(`/users/${response.body.id}`);

    expect(getResponse.body.name).toBe('Test User');
  });
});
```

### E2E Tests

```typescript
describe('User Registration Flow', () => {
  it('should complete full registration process', async () => {
    await page.goto('/register');

    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await page.waitForURL('/dashboard');
    expect(await page.textContent('h1')).toBe('Welcome!');
  });
});
```

### Edge Case Testing

```typescript
describe('Edge Cases', () => {
  // Boundary values
  it('should handle maximum length input', () => {
    const maxString = 'a'.repeat(255);
    expect(() => validate(maxString)).not.toThrow();
  });

  // Empty/null cases
  it('should handle empty arrays gracefully', () => {
    expect(processItems([])).toEqual([]);
  });

  // Error conditions
  it('should recover from network timeout', async () => {
    jest.setTimeout(10000);
    mockApi.get.mockImplementation(() =>
      new Promise(resolve => setTimeout(resolve, 5000))
    );

    await expect(service.fetchData()).rejects.toThrow('Timeout');
  });

  // Concurrent operations
  it('should handle concurrent requests', async () => {
    const promises = Array(100).fill(null)
      .map(() => service.processRequest());

    const results = await Promise.all(promises);
    expect(results).toHaveLength(100);
  });
});
```

## Configuration

### Performance Testing

```typescript
describe('Performance', () => {
  it('should process 1000 items under 100ms', async () => {
    const items = generateItems(1000);

    const start = performance.now();
    await service.processItems(items);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
  });

  it('should handle memory efficiently', () => {
    const initialMemory = process.memoryUsage().heapUsed;

    // Process large dataset
    processLargeDataset();
    global.gc(); // Force garbage collection

    const finalMemory = process.memoryUsage().heapUsed;
    const memoryIncrease = finalMemory - initialMemory;

    expect(memoryIncrease).toBeLessThan(50 * 1024 * 1024); // <50MB
  });
});
```

### Security Testing

```typescript
describe('Security', () => {
  it('should prevent SQL injection', async () => {
    const maliciousInput = "'; DROP TABLE users; --";

    const response = await request(app)
      .get(`/users?name=${maliciousInput}`);

    expect(response.status).not.toBe(500);
    // Verify table still exists
    const users = await database.query('SELECT * FROM users');
    expect(users).toBeDefined();
  });

  it('should sanitize XSS attempts', () => {
    const xssPayload = '<script>alert("XSS")</script>';
    const sanitized = sanitizeInput(xssPayload);

    expect(sanitized).not.toContain('<script>');
    expect(sanitized).toBe('&lt;script&gt;alert("XSS")&lt;/script&gt;');
  });
});
```

## Usage Examples

### Example 1: TDD Workflow

```typescript
// Step 1: Write failing test
describe('calculateDiscount', () => {
  it('should return 10% discount for users with 10+ purchases', () => {
    const user = { purchases: 15 };
    expect(calculateDiscount(user)).toBe(0.1);
  });
});

// Step 2: Run test (fails)
// Step 3: Implement minimal code
function calculateDiscount(user) {
  return user.purchases >= 10 ? 0.1 : 0;
}

// Step 4: Run test (passes)
// Step 5: Refactor if needed
```

### Example 2: Complete Test Suite

```typescript
/**
 * @test User Registration
 * @description Validates the complete user registration flow
 * @prerequisites
 *   - Database is empty
 *   - Email service is mocked
 * @steps
 *   1. Submit registration form with valid data
 *   2. Verify user is created in database
 *   3. Check confirmation email is sent
 *   4. Validate user can login
 * @expected User successfully registered and can access dashboard
 */
describe('User Registration', () => {
  it('should register user successfully', async () => {
    // Implementation
  });
});
```

## Execution Checklist

- [ ] Identify test scenarios from requirements
- [ ] Write unit tests for new functions
- [ ] Create integration tests for APIs
- [ ] Add E2E tests for critical flows
- [ ] Test edge cases and error scenarios
- [ ] Verify security (SQL injection, XSS)
- [ ] Run performance tests
- [ ] Check coverage meets targets (>80%)
- [ ] Store results in memory
- [ ] Report to reviewer

## Best Practices

1. **Test First**: Write tests before implementation (TDD)
2. **One Assertion**: Each test should verify one behavior
3. **Descriptive Names**: Test names should explain what and why
4. **Arrange-Act-Assert**: Structure tests clearly
5. **Mock External Dependencies**: Keep tests isolated
6. **Test Data Builders**: Use factories for test data
7. **Avoid Test Interdependence**: Each test should be independent
8. **Report Results**: Always share test results via memory

## Error Handling

| Scenario | Recovery |
|----------|----------|
| Test timeout | Increase timeout or optimize test |
| Flaky test | Add retries or fix race condition |
| Mock failure | Verify mock setup |
| Coverage gap | Add missing tests |

## Metrics & Success Criteria

- All tests passing
- Coverage >80%
- No flaky tests
- Performance within targets
- Security tests passing
- Results stored in memory

## Integration Points

### MCP Tools

```javascript
// Report test status
mcp__claude-flow__memory_usage {
  action: "store",
  key: "swarm/tester/status",
  namespace: "coordination",
  value: JSON.stringify({
    agent: "tester",
    status: "running tests",
    test_suites: ["unit", "integration", "e2e"],
    timestamp: Date.now()
  })
}

// Share test results
mcp__claude-flow__memory_usage {
  action: "store",
  key: "swarm/shared/test-results",
  namespace: "coordination",
  value: JSON.stringify({
    passed: 145,
    failed: 2,
    coverage: "87%",
    failures: ["auth.test.ts:45", "api.test.ts:123"]
  })
}

// Check implementation status
mcp__claude-flow__memory_usage {
  action: "retrieve",
  key: "swarm/coder/status",
  namespace: "coordination"
}
```

### Performance Testing

```javascript
// Run performance benchmarks
mcp__claude-flow__benchmark_run {
  type: "test",
  iterations: 100
}

// Monitor test execution
mcp__claude-flow__performance_report {
  format: "detailed"
}
```

### Hooks

```bash
# Pre-execution
echo "🧪 Tester agent validating: $TASK"
if [ -f "jest.config.js" ] || [ -f "vitest.config.ts" ]; then
  echo "✓ Test framework detected"
fi

# Post-execution
echo "📋 Test results summary:"
npm test -- --reporter=json 2>/dev/null | jq '.numPassedTests, .numFailedTests' 2>/dev/null || echo "Tests completed"
```

### Related Skills

- [core-coder](../core-coder/SKILL.md) - Provides implementation to test
- [core-reviewer](../core-reviewer/SKILL.md) - Reviews test quality
- [core-researcher](../core-researcher/SKILL.md) - Provides edge cases
- [core-planner](../core-planner/SKILL.md) - Test planning

Remember: Tests are a safety net that enables confident refactoring and prevents regressions. Invest in good tests--they pay dividends in maintainability. Coordinate with other agents through memory.

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from tester.md agent
