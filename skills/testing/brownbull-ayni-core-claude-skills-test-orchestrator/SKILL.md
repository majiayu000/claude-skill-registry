---
name: test-orchestrator
description: Coordinates testing strategy and execution across all test types. Use when creating test plans, implementing tests (unit/integration/E2E), or enforcing coverage requirements (80% minimum). Applies testing-requirements.md.
---

# Test Orchestrator Skill

## Role
Acts as QA Lead, coordinating all testing activities across the system.

## Responsibilities

1. **Test Strategy**
   - Define test plans
   - Coordinate test execution
   - Manage test environments
   - Track coverage metrics

2. **Test Automation**
   - Unit test coordination
   - Integration test suites
   - E2E test scenarios
   - Performance testing

3. **Quality Gates**
   - Define acceptance criteria
   - Enforce coverage thresholds
   - Block failing builds
   - Report quality metrics

4. **Context Maintenance**
   ```
   ai-state/active/testing/
   ├── test-plans.json     # Test strategies
   ├── coverage.json       # Coverage metrics
   ├── results.json        # Test results
   └── tasks/             # Active test tasks
   ```

## Skill Coordination

### Available Test Skills
- `unit-test-skill` - Unit test creation
- `integration-test-skill` - Integration testing
- `e2e-test-skill` - End-to-end scenarios
- `performance-test-skill` - Load/stress testing
- `security-test-skill` - Security validation

### Context Package to Skills
```yaml
context:
  task_id: "task-004-testing"
  component: "authentication"
  test_requirements:
    unit: ["all public methods", ">80% coverage"]
    integration: ["database operations", "API calls"]
    e2e: ["login flow", "password reset"]
    performance: ["100 concurrent users", "<200ms response"]
  standards:
    - "testing-requirements.md"
  existing_tests:
    coverage: 65%
    failing: ["test_login_invalid"]
```

## Task Processing Flow

1. **Receive Task**
   - Identify component
   - Review requirements
   - Check existing tests

2. **Create Test Plan**
   - Define test scenarios
   - Set coverage goals
   - Identify test data

3. **Assign to Skills**
   - Distribute test types
   - Set priorities
   - Define timelines

4. **Execute Tests**
   - Run test suites
   - Monitor execution
   - Collect results

5. **Validate Quality**
   - Check coverage
   - Review failures
   - Verify fixes
   - Generate reports

## Test Categories

### Unit Testing
- [ ] All public methods tested
- [ ] Edge cases covered
- [ ] Mocks properly used
- [ ] Fast execution (<1s)
- [ ] Isolated tests
- [ ] Clear assertions

### Integration Testing
- [ ] Component interactions
- [ ] Database operations
- [ ] API integrations
- [ ] Message queues
- [ ] File operations
- [ ] External services

### E2E Testing
- [ ] User workflows
- [ ] Critical paths
- [ ] Cross-browser
- [ ] Mobile responsive
- [ ] Error scenarios
- [ ] Recovery flows

### Performance Testing
- [ ] Load testing
- [ ] Stress testing
- [ ] Spike testing
- [ ] Volume testing
- [ ] Endurance testing
- [ ] Scalability testing

## Test Standards

### Test Quality Checklist
- [ ] Descriptive test names
- [ ] AAA pattern (Arrange, Act, Assert)
- [ ] Single assertion focus
- [ ] No test interdependencies
- [ ] Deterministic results
- [ ] Meaningful failures

### Coverage Requirements
- **Unit Tests:** >80% code coverage
- **Integration:** All APIs tested
- **E2E:** Critical paths covered
- **Performance:** Meets SLAs
- **Security:** OWASP top 10

## Integration Points

### With Development Orchestrators
- Test requirements from tasks
- Failure feedback loops
- Coverage reporting
- Quality gates

### With CI/CD Pipeline
- Automated test execution
- Build blocking on failures
- Test result reporting
- Coverage trends

### With Human-Docs
Updates testing documentation:
- Test plan changes
- Coverage reports
- Quality metrics
- Test guidelines

## Event Communication

### Listening For
```json
{
  "event": "code.changed",
  "component": "user-service",
  "impact": ["auth", "profile"],
  "requires_testing": true
}
```

### Broadcasting
```json
{
  "event": "tests.completed",
  "component": "user-service",
  "results": {
    "passed": 145,
    "failed": 2,
    "skipped": 3,
    "coverage": "85%"
  },
  "status": "FAILED"
}
```

## Test Execution Strategy

### Parallel Execution
```python
class TestOrchestrator:
    def run_tests(self, suites):
        # 1. Identify independent tests
        # 2. Distribute across workers
        # 3. Collect results
        # 4. Aggregate coverage
        # 5. Generate report
```

### Test Retry Logic
```python
def retry_failed_tests(failures):
    MAX_RETRIES = 3
    for test in failures:
        for attempt in range(MAX_RETRIES):
            if run_test(test).passed:
                break
        else:
            mark_as_flaky(test)
```

## Success Metrics

- Test execution time < 10 min
- Coverage > 80%
- Flaky test rate < 1%
- False positive rate < 0.1%
- Test maintenance time < 10%

## Test Data Management

### Strategies
1. **Fixtures** - Predefined test data
2. **Factories** - Dynamic data generation
3. **Snapshots** - Baseline comparisons
4. **Mocks** - External service simulation
5. **Stubs** - Simplified implementations

### Best Practices
- Isolate test data
- Clean up after tests
- Use realistic data
- Version test data
- Document data requirements

## Common Testing Patterns

### Page Object Pattern (E2E)
```typescript
class LoginPage {
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

### Test Builder Pattern
```python
def test_user_creation():
    user = UserBuilder()
        .with_email("test@example.com")
        .with_role("admin")
        .build()

    assert user.is_valid()
```

## Anti-Patterns to Avoid

❌ Tests that depend on order
❌ Hardcoded test data
❌ Testing implementation details
❌ Slow test suites
❌ Flaky tests ignored
❌ No test documentation