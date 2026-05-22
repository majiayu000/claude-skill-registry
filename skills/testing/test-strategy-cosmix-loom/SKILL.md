---
name: test-strategy
description: Comprehensive test strategy guidance including test pyramid design, coverage goals, test categorization, flaky test diagnosis, test infrastructure architecture, and risk-based prioritization. Absorbed expertise from eliminated senior-qa-engineer. Use when planning testing approaches, setting up test infrastructure, optimizing test suites, diagnosing flaky tests, or designing test architecture across domains (API, data pipelines, ML models, infrastructure). Trigger keywords: test strategy, test pyramid, test plan, what to test, how to test, test architecture, test infrastructure, coverage goals, test organization, CI/CD testing, test prioritization, testing approach, flaky test, test optimization, test parallelization, API testing strategy, data pipeline testing, ML model testing, infrastructure testing.
---

# Test Strategy

## Overview

Test strategy defines how to approach testing for a project, balancing thoroughness with efficiency. A well-designed strategy ensures critical functionality is covered while avoiding over-testing trivial code. This skill covers the test pyramid, coverage metrics, test categorization, and integration with CI/CD pipelines.

## Instructions

### 1. Design the Test Pyramid

Structure tests in layers with appropriate ratios:

```
         /\
        /  \        E2E Tests (5-10%)
       /----\       - Critical user journeys
      /      \      - Cross-system integration
     /--------\     Integration Tests (15-25%)
    /          \    - API contracts
   /------------\   - Database interactions
  /              \  - Service boundaries
 /----------------\ Unit Tests (65-80%)
                    - Business logic
                    - Pure functions
                    - Edge cases
```

**Recommended Ratios:**

- Unit tests: 65-80% of test suite
- Integration tests: 15-25%
- E2E tests: 5-10%

### 2. Set Coverage Goals

**Coverage Targets by Component Type:**

| Component Type | Line Coverage | Branch Coverage | Notes                          |
| -------------- | ------------- | --------------- | ------------------------------ |
| Business Logic | 90%+          | 85%+            | Critical paths fully covered   |
| API Handlers   | 80%+          | 75%+            | All endpoints tested           |
| Utilities      | 95%+          | 90%+            | Pure functions easily testable |
| UI Components  | 70%+          | 60%+            | Focus on behavior over markup  |
| Infrastructure | 60%+          | 50%+            | Integration tests preferred    |

**Coverage Anti-patterns to Avoid:**

- Chasing 100% coverage for coverage's sake
- Testing getters/setters without logic
- Testing framework or library code
- Writing tests that don't verify behavior

### 3. Decide What to Test vs What Not to Test

**Always Test:**

- Business logic and domain rules
- Input validation and error handling
- Security-sensitive operations
- Data transformations
- State transitions
- Edge cases and boundary conditions
- Regression scenarios from bug fixes

**Consider Not Testing:**

- Simple pass-through functions
- Framework-generated code
- Third-party library internals
- Trivial getters/setters
- Configuration constants
- Logging statements (unless critical)

**Test Smell Detection:**

```typescript
// BAD: Testing trivial code
test("getter returns value", () => {
  const user = new User("John");
  expect(user.getName()).toBe("John");
});

// GOOD: Testing meaningful behavior
test("user cannot change name to empty string", () => {
  const user = new User("John");
  expect(() => user.setName("")).toThrow(ValidationError);
});
```

### 4. Categorize and Organize Tests

**Directory Structure:**

```
tests/
├── unit/
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/
│   ├── api/
│   ├── database/
│   └── external-services/
├── e2e/
│   ├── flows/
│   └── pages/
├── fixtures/
│   ├── factories/
│   └── mocks/
└── helpers/
    ├── setup.ts
    └── assertions.ts
```

**Test Tagging System:**

```typescript
// Jest example with tags
describe("[unit][fast] UserService", () => {});
describe("[integration][slow] DatabaseRepository", () => {});
describe("[e2e][critical] CheckoutFlow", () => {});

// Run specific categories
// npm test -- --grep="\[unit\]"
// npm test -- --grep="\[critical\]"
```

**Naming Conventions:**

```
[ComponentName].[scenario].[expected_result].test.ts

Examples:
UserService.createUser.returnsNewUser.test.ts
PaymentProcessor.invalidCard.throwsPaymentError.test.ts
```

### 5. Integrate with CI/CD

**Pipeline Stage Configuration:**

```yaml
# .github/workflows/test.yml
name: Test Pipeline

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Unit Tests
        run: npm test -- --grep="\[unit\]" --coverage
      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - name: Run Integration Tests
        run: npm test -- --grep="\[integration\]"

  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4
      - name: Run E2E Tests
        run: npm run test:e2e
```

**CI Test Optimization:**

- Run unit tests first (fast feedback)
- Parallelize test suites
- Cache dependencies and build artifacts
- Use test splitting for large suites
- Fail fast on critical tests

### 6. Risk-Based Test Prioritization

**Risk Matrix for Prioritization:**

| Impact ↓ / Likelihood → | Low             | Medium          | High            |
| ----------------------- | --------------- | --------------- | --------------- |
| High                    | Medium Priority | High Priority   | Critical        |
| Medium                  | Low Priority    | Medium Priority | High Priority   |
| Low                     | Skip/Manual     | Low Priority    | Medium Priority |

**Risk Factors to Consider:**

- **Business Impact:** Revenue, user trust, legal compliance
- **Complexity:** Code complexity, integration points
- **Change Frequency:** Actively developed areas
- **Historical Bugs:** Components with bug history
- **Dependencies:** Critical external services

**Prioritized Test Categories:**

1. **Critical (P0):** Run on every commit
   - Authentication/authorization
   - Payment processing
   - Data integrity

2. **High (P1):** Run on PR merge
   - Core business workflows
   - API contract tests

3. **Medium (P2):** Run nightly
   - Edge cases
   - Performance tests

4. **Low (P3):** Run weekly
   - Backward compatibility
   - Deprecated feature coverage

### 7. Domain-Specific Testing Strategies

#### API Testing Strategy

**Test Layers:**

1. **Contract Tests (P0)**
   - Request/response schema validation
   - HTTP status codes for all endpoints
   - Error response formats
   - Authentication/authorization rules

2. **Business Logic Tests (P0)**
   - Valid input processing
   - Business rule enforcement
   - State transitions via API calls

3. **Integration Tests (P1)**
   - Database operations via API
   - External service integration
   - Transaction rollback scenarios

4. **Performance Tests (P2)**
   - Response time under load
   - Concurrent request handling
   - Rate limiting behavior

**API Test Organization:**

```
tests/api/
├── contracts/          # Schema validation tests
├── endpoints/          # Per-endpoint behavior tests
├── auth/               # Authentication flows
├── integration/        # Cross-service scenarios
└── performance/        # Load and stress tests
```

#### Data Pipeline Testing Strategy

**Test Focus Areas:**

1. **Data Quality Tests (P0)**
   - Schema validation at each stage
   - Data type correctness
   - Null/missing value handling
   - Duplicate detection

2. **Transformation Tests (P0)**
   - Input → output correctness
   - Edge case handling
   - Data loss detection
   - Aggregation accuracy

3. **Integration Tests (P1)**
   - Source extraction correctness
   - Sink loading verification
   - Idempotency checks
   - Failure recovery

4. **Performance Tests (P2)**
   - Processing throughput
   - Memory usage with large datasets
   - Partition handling

**Data Pipeline Test Pattern:**

```python
def test_user_data_transformation():
    # Arrange: Create test input data
    raw_input = create_test_dataset(
        rows=1000,
        include_nulls=True,
        include_duplicates=True
    )

    # Act: Run transformation
    result = transform_user_data(raw_input)

    # Assert: Verify output quality
    assert_no_nulls(result, required_fields=["user_id", "email"])
    assert_no_duplicates(result, key="user_id")
    assert_schema_matches(result, UserSchema)
    assert len(result) == expected_output_count(raw_input)
```

#### ML Model Testing Strategy

**Test Layers:**

1. **Data Validation Tests (P0)**
   - Feature schema validation
   - Label distribution checks
   - Data leakage detection
   - Train/test split correctness

2. **Model Behavior Tests (P0)**
   - Prediction on known examples
   - Invariance tests (e.g., case-insensitive text)
   - Directional expectation tests
   - Boundary condition handling

3. **Model Quality Tests (P1)**
   - Accuracy/precision/recall thresholds
   - Fairness metrics across groups
   - Performance on edge cases
   - Regression detection (vs baseline)

4. **Integration Tests (P1)**
   - Model loading and serving
   - Prediction API contract
   - Feature engineering pipeline
   - Model versioning

**ML Test Example:**

```python
def test_sentiment_model_invariance():
    """Model should be case-insensitive"""
    model = load_sentiment_model()

    test_cases = [
        ("This is GREAT!", "This is great!"),
        ("TERRIBLE service", "terrible service"),
    ]

    for text1, text2 in test_cases:
        pred1 = model.predict(text1)
        pred2 = model.predict(text2)
        assert pred1 == pred2, f"Case sensitivity detected: {text1} vs {text2}"
```

#### Infrastructure Testing Strategy

**Test Focus:**

1. **Infrastructure-as-Code Tests (P0)**
   - Syntax validation (terraform validate)
   - Security policy checks
   - Resource naming conventions
   - Cost estimation validation

2. **Deployment Tests (P1)**
   - Smoke tests post-deployment
   - Health check endpoints
   - Configuration validation
   - Rollback procedures

3. **Resilience Tests (P2)**
   - Service restart handling
   - Network partition recovery
   - Resource exhaustion scenarios
   - Chaos engineering tests

4. **Observability Tests (P1)**
   - Metrics collection verification
   - Log aggregation correctness
   - Alert rule validation
   - Dashboard functionality

**Infrastructure Test Pattern:**

```hcl
# terraform test example
run "verify_security_group_rules" {
  command = plan

  assert {
    condition     = length([for rule in aws_security_group.main.ingress : rule if rule.cidr_blocks[0] == "0.0.0.0/0"]) == 0
    error_message = "Security group should not allow ingress from 0.0.0.0/0"
  }
}
```

### 8. Flaky Test Diagnosis and Prevention

**Common Causes of Flakiness:**

| Cause                    | Symptoms                                | Solution                                  |
| ------------------------ | --------------------------------------- | ----------------------------------------- |
| Race conditions          | Fails intermittently on timing          | Add proper synchronization                |
| Async operations         | Fails with "element not found"          | Use explicit waits, not sleeps            |
| Shared state             | Fails when run with other tests         | Isolate test data, reset state            |
| External dependencies    | Fails when service unavailable          | Mock external calls, use test doubles     |
| Time-dependent logic     | Fails at specific times/dates           | Inject time, use fake clocks              |
| Resource cleanup         | Fails after certain test order          | Ensure teardown always runs               |
| Nondeterministic data    | Fails with random data variations       | Use fixed seeds, deterministic generators |
| Environment differences  | Fails in CI but passes locally          | Containerize test environment             |
| Insufficient timeouts    | Fails under load/slow machines          | Make timeouts configurable                |
| Parallel execution races | Fails only when parallelized            | Use unique identifiers per test           |

**Flaky Test Diagnosis Workflow:**

```
1. Reproduce Locally
   ├─ Run test 100 times: `for i in {1..100}; do npm test -- TestName || break; done`
   ├─ Run with different seeds: `npm test -- --seed=$RANDOM`
   └─ Run in parallel: `npm test -- --maxWorkers=4`

2. Identify Pattern
   ├─ Always fails at same point? → Logic bug, not flaky
   ├─ Fails under load? → Timing/resource issue
   ├─ Fails with other tests? → Shared state pollution
   └─ Fails on specific data? → Data-dependent bug

3. Instrument Test
   ├─ Add verbose logging
   ├─ Capture timing information
   ├─ Record test environment state
   └─ Save failure artifacts (screenshots, logs)

4. Fix Root Cause
   ├─ Eliminate race conditions
   ├─ Add proper synchronization
   ├─ Isolate test state
   └─ Mock external dependencies

5. Verify Fix
   ├─ Run fixed test 1000 times
   ├─ Run in CI 10 times
   └─ Monitor over 1 week
```

**Flaky Test Prevention Checklist:**

- [ ] Tests use deterministic test data (fixed seeds, no random())
- [ ] Async operations use explicit waits (not setTimeout/sleep)
- [ ] Tests create unique resources (UUIDs in names/IDs)
- [ ] Cleanup always runs (try/finally, afterEach hooks)
- [ ] No hardcoded timing assumptions (sleep(100) is a code smell)
- [ ] External services are mocked or use test doubles
- [ ] Time-dependent logic uses injected/fake clocks
- [ ] Tests do not depend on execution order
- [ ] Shared state is reset between tests
- [ ] Test environment is reproducible (containerized)

**Example: Fixing a Flaky Test**

```typescript
// FLAKY: Race condition with async operation
test("user profile loads", async () => {
  renderUserProfile(userId);
  // Race: profile might not be loaded yet
  expect(screen.getByText("John Doe")).toBeInTheDocument();
});

// FIXED: Proper async handling
test("user profile loads", async () => {
  renderUserProfile(userId);
  // Wait for async operation to complete
  const userName = await screen.findByText("John Doe");
  expect(userName).toBeInTheDocument();
});

// FLAKY: Shared state pollution
test("creates user with default role", () => {
  const user = createUser({ name: "Alice" });
  expect(user.role).toBe("user"); // Fails if previous test modified default
});

// FIXED: Isolated state
test("creates user with default role", () => {
  resetDefaultRole(); // Ensure clean state
  const user = createUser({ name: "Alice" });
  expect(user.role).toBe("user");
});

// FLAKY: Time-dependent logic
test("expires session after 1 hour", () => {
  const session = createSession();
  // Flaky: Depends on current time
  expect(session.expiresAt).toBe(Date.now() + 3600000);
});

// FIXED: Inject time dependency
test("expires session after 1 hour", () => {
  const mockClock = installFakeClock();
  mockClock.setTime(new Date("2024-01-01T12:00:00Z"));

  const session = createSession();
  expect(session.expiresAt).toBe(new Date("2024-01-01T13:00:00Z").getTime());

  mockClock.uninstall();
});
```

### 9. Test Infrastructure Architecture

**Test Environment Management:**

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data  # In-memory for speed

  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"

  test-app:
    build: .
    environment:
      DATABASE_URL: postgres://test_user:test_pass@test-db:5432/test_db
      REDIS_URL: redis://test-redis:6379
    depends_on:
      - test-db
      - test-redis
```

**Test Data Management:**

```typescript
// Factory pattern for test data
class UserFactory {
  private sequence = 0;

  create(overrides?: Partial<User>): User {
    return {
      id: overrides?.id ?? `user-${this.sequence++}`,
      email: overrides?.email ?? `user${this.sequence}@test.com`,
      name: overrides?.name ?? `Test User ${this.sequence}`,
      role: overrides?.role ?? "user",
      createdAt: overrides?.createdAt ?? new Date(),
    };
  }

  createBatch(count: number, overrides?: Partial<User>): User[] {
    return Array.from({ length: count }, () => this.create(overrides));
  }
}

// Usage ensures unique data per test
test("user search works", () => {
  const factory = new UserFactory();
  const users = factory.createBatch(10);
  // Each test gets unique users, no conflicts
});
```

**Test Parallelization Strategy:**

| Strategy             | When to Use                           | Configuration                                  |
| -------------------- | ------------------------------------- | ---------------------------------------------- |
| File-level parallel  | Tests in different files independent  | Jest: `--maxWorkers=4`                         |
| Database per worker  | Tests need database isolation         | Postgres: Create schema per worker             |
| Test sharding        | CI with multiple machines             | Split tests by shard: `--shard=1/4`            |
| Test prioritization  | Want fast feedback                    | Run fast tests first, slow tests in parallel   |
| Smart test selection | Only run affected tests               | Use dependency graph to select changed tests   |

**Example: Parallel Test Configuration**

```javascript
// jest.config.js with parallel optimization
module.exports = {
  maxWorkers: process.env.CI ? "50%" : "75%", // Conservative in CI
  testTimeout: 30000, // Longer timeout for CI

  // Run fast tests first
  testSequencer: "./custom-sequencer.js",

  // Database isolation per worker
  globalSetup: "./tests/setup/create-test-dbs.js",
  globalTeardown: "./tests/setup/drop-test-dbs.js",

  // Shard tests in CI
  shard: process.env.CI_NODE_INDEX
    ? `${process.env.CI_NODE_INDEX}/${process.env.CI_NODE_TOTAL}`
    : undefined,
};
```

**Test Optimization Techniques:**

1. **Reduce Test Startup Time**
   - Cache compiled code
   - Lazy-load test dependencies
   - Use in-memory databases for unit tests

2. **Optimize Test Execution**
   - Batch database operations
   - Reuse expensive fixtures (connections, containers)
   - Skip unnecessary setup for focused tests

3. **Parallelize Safely**
   - Unique identifiers per test (UUIDs)
   - Separate database schemas per worker
   - Avoid shared file system access

4. **Smart Test Selection**
   - Run only affected tests during development
   - Use coverage mapping to determine affected tests
   - Cache test results for unchanged code

```bash
# Run only tests affected by changes
npm test -- --changedSince=origin/main

# Run tests for specific module and dependents
npm test -- --selectProjects=user-service --testPathPattern=user

# Watch mode with smart re-running
npm test -- --watch --changedSince=HEAD
```

## Best Practices

1. **Test Behavior, Not Implementation**
   - Tests should verify outcomes, not internal mechanics
   - Refactoring should not break tests if behavior unchanged

2. **Keep Tests Independent**
   - No shared mutable state between tests
   - Each test sets up its own context
   - Tests can run in any order

3. **Use Test Doubles Appropriately**
   - Stubs for providing test data
   - Mocks for verifying interactions
   - Fakes for complex dependencies
   - Real implementations when feasible

4. **Maintain Test Quality**
   - Apply same code quality standards to tests
   - Refactor test code for readability
   - Remove obsolete tests promptly

5. **Fast Feedback Loop**
   - Optimize for quick local test runs
   - Use watch mode during development
   - Prioritize fast tests in CI

6. **Document Test Intent**
   - Clear test names describe behavior
   - Add comments for non-obvious setup
   - Link tests to requirements/tickets

## Examples

### Example: Feature Test Strategy Document

```markdown
# Feature: User Registration

## Risk Assessment

- Business Impact: HIGH (user acquisition)
- Complexity: MEDIUM (email validation, password rules)
- Change Frequency: LOW (stable feature)

## Test Coverage Plan

### Unit Tests (P0)

- [ ] Email format validation
- [ ] Password strength requirements
- [ ] Username uniqueness check logic
- [ ] Profile data sanitization

### Integration Tests (P1)

- [ ] Database user creation
- [ ] Email service integration
- [ ] Duplicate email handling

### E2E Tests (P0)

- [ ] Happy path: complete registration flow
- [ ] Error path: duplicate email shows error

## Coverage Targets

- Line coverage: 85%
- Branch coverage: 80%
- Critical paths: 100%
```

### Example: Test Organization Configuration

```javascript
// jest.config.js
module.exports = {
  projects: [
    {
      displayName: "unit",
      testMatch: ["<rootDir>/tests/unit/**/*.test.ts"],
      setupFilesAfterEnv: ["<rootDir>/tests/helpers/unit-setup.ts"],
    },
    {
      displayName: "integration",
      testMatch: ["<rootDir>/tests/integration/**/*.test.ts"],
      setupFilesAfterEnv: ["<rootDir>/tests/helpers/integration-setup.ts"],
      globalSetup: "<rootDir>/tests/helpers/db-setup.ts",
      globalTeardown: "<rootDir>/tests/helpers/db-teardown.ts",
    },
  ],
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    "./src/services/": {
      branches: 90,
      lines: 90,
    },
  },
};
```

### Example: Risk-Based Test Selection Script

```typescript
// scripts/select-tests.ts
interface TestFile {
  path: string;
  priority: "P0" | "P1" | "P2" | "P3";
  tags: string[];
}

function selectTestsForPipeline(
  context: "commit" | "pr" | "nightly" | "weekly",
): TestFile[] {
  const allTests = getTestManifest();

  const priorityMap = {
    commit: ["P0"],
    pr: ["P0", "P1"],
    nightly: ["P0", "P1", "P2"],
    weekly: ["P0", "P1", "P2", "P3"],
  };

  return allTests.filter((test) =>
    priorityMap[context].includes(test.priority),
  );
}
```
