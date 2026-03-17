---
name: testing
description: Comprehensive test implementation across all domains including unit, integration, e2e, security, infrastructure, data pipelines, and ML models. Covers TDD/BDD workflows, test architecture, flaky test debugging, and coverage analysis.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
trigger-keywords: test, testing, spec, assert, expect, mock, stub, spy, fixture, snapshot, coverage, TDD, BDD, red-green, regression, unit test, integration test, e2e, end-to-end, test suite, test case, pytest, jest, vitest, mocha, junit, testify, test framework
---

# Testing

## Overview

This skill provides comprehensive testing expertise across all domains and test types. Whether writing unit tests, debugging flaky tests, designing test architecture, or testing specialized systems like data pipelines and ML models, this skill guides test implementation following industry best practices.

## When to Use

- Implementing tests for any codebase (unit, integration, e2e)
- Debugging flaky or failing tests
- Improving test coverage
- Setting up test infrastructure and frameworks
- Following TDD/BDD workflows
- Testing specialized domains (data, ML, infrastructure, security)
- Designing test architecture and strategy

## Core Instructions

### 1. Analyze Code to Test

- Identify public interfaces and APIs
- Map out dependencies and side effects
- Find edge cases and boundary conditions
- Understand expected behaviors and invariants
- Review error handling paths
- Document assumptions and preconditions

### 2. Design Test Strategy

**Test Pyramid Approach:**

- Unit tests (70%): Fast, isolated, test single units
- Integration tests (20%): Test component interactions
- E2E tests (10%): Test full user workflows

**Planning:**

- Determine appropriate test types for each component
- Set coverage targets (aim for 80%+ line coverage, 100% critical paths)
- Identify mocking requirements and boundaries
- Plan test fixtures and data management
- Consider performance and flakiness risks

### 3. Write Tests Following AAA Pattern

**Arrange-Act-Assert:**

- **Arrange**: Set up test data, mocks, and conditions
- **Act**: Execute the code under test
- **Assert**: Verify expected outcomes with clear failure messages

**Naming Convention:**

```text
test_<unit>_<scenario>_<expected_outcome>
```

Example: `test_shopping_cart_add_duplicate_item_increases_quantity`

### 4. Handle Special Cases

**Async Operations:**

- Use proper async test utilities (async/await, done callbacks)
- Set appropriate timeouts
- Test race conditions and timing issues

**Error Conditions:**

- Test all error paths explicitly
- Verify error messages and types
- Test recovery mechanisms

**External Dependencies:**

- Mock HTTP clients, databases, file systems
- Use test doubles (mocks, stubs, fakes)
- Consider contract testing for APIs

**Database Testing:**

- Use transactions with rollback for isolation
- Use in-memory databases for speed
- Seed test data consistently

## Domain-Specific Testing

### Data Pipeline Testing

**Data Quality Tests:**

- Schema validation (column types, nullability, constraints)
- Data completeness (row counts, null checks)
- Data accuracy (statistical checks, business rule validation)
- Data freshness (timestamp checks)

**Pipeline Tests:**

- Idempotency: Running twice produces same result
- Incremental processing: Only new data is processed
- Failure recovery: Handles partial failures gracefully
- Performance: Processing time within SLAs

**Example:**

```python
def test_etl_pipeline_preserves_row_count():
    # Arrange
    input_data = load_fixture("sales_data_1000_rows.csv")

    # Act
    result = etl_pipeline.transform(input_data)

    # Assert
    assert len(result) == 1000, "ETL should not drop rows"
    assert result['customer_id'].notna().all(), "customer_id required"
```

### ML Model Testing

**Model Behavior Tests:**

- Invariance tests: Predictions stable under irrelevant changes
- Directional expectation: Feature changes affect predictions correctly
- Minimum functionality: Model beats baseline on key examples

**Data Tests:**

- Training/validation split integrity
- Feature distribution alignment
- Label balance and quality

**Performance Tests:**

- Accuracy/precision/recall on test set
- Inference latency requirements
- Resource usage (memory, CPU)

**Example:**

```python
def test_sentiment_model_invariance_to_punctuation():
    model = load_model("sentiment_classifier")

    text_base = "This product is amazing"
    text_with_punct = "This product is amazing!!!"

    pred_base = model.predict(text_base)
    pred_punct = model.predict(text_with_punct)

    assert abs(pred_base - pred_punct) < 0.1, \
        "Punctuation should not significantly change sentiment"
```

### Infrastructure Testing

**Infrastructure as Code Tests:**

- Syntax validation (terraform validate, yaml lint)
- Policy compliance (security groups, IAM policies)
- Resource tagging and naming conventions
- Cost estimation thresholds

**Integration Tests:**

- Deployment smoke tests
- Health check endpoints
- Service connectivity
- Configuration validation

**Example:**

```python
def test_terraform_no_public_s3_buckets():
    tf_plan = load_terraform_plan("main.tfplan.json")

    for resource in tf_plan.get_resources("aws_s3_bucket"):
        acl = resource.get("acl", "private")
        assert acl != "public-read", \
            f"S3 bucket {resource['name']} must not be public"
```

## Best Practices

### Test Quality

1. **Test One Thing**: Each test verifies a single behavior or condition
2. **Descriptive Names**: Test names describe scenario and expected outcome
3. **Independent Tests**: No shared state between tests, any order execution
4. **Fast Execution**: Unit tests < 100ms, integration tests < 5s
5. **Deterministic**: Same input always produces same result (no random data)
6. **Avoid Test Logic**: Tests should be simple assertions, not algorithms
7. **Test Edge Cases**: Boundary conditions, empty inputs, max values, nulls
8. **Readable Assertions**: Use clear assertion messages for debugging

### Test Coverage

- Aim for 80%+ line coverage, 100% for critical paths
- Focus on behavior coverage, not just line coverage
- Use coverage tools to find untested code
- Prioritize testing business logic and error paths

### Debugging Flaky Tests

**Common Causes:**

- Race conditions and timing dependencies
- Shared mutable state between tests
- External service dependencies
- Non-deterministic inputs (timestamps, random values)
- Test execution order dependencies

**Solutions:**

- Add explicit waits instead of sleep
- Reset state in setup/teardown
- Mock external dependencies
- Use fixed seeds for random generation
- Run tests in isolation to identify order dependencies

### TDD Workflow

**Red-Green-Refactor Cycle:**

1. **Red**: Write failing test for desired behavior
2. **Green**: Write minimal code to make test pass
3. **Refactor**: Improve code while keeping tests passing

**Benefits:**

- Forces thinking about design before implementation
- Ensures tests actually catch failures
- Provides fast feedback loop
- Creates comprehensive test suite

## Framework-Specific Patterns

### Python (pytest)

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (5, 120),
])
def test_factorial(input, expected):
    assert factorial(input) == expected

@patch('requests.get')
def test_api_client(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_status()
    assert result == "ok"
```

### JavaScript (Vitest/Jest)

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('UserService', () => {
  let mockDb

  beforeEach(() => {
    mockDb = {
      query: vi.fn()
    }
  })

  it('finds user by email', async () => {
    mockDb.query.mockResolvedValue([{ id: 1, email: 'test@example.com' }])

    const service = new UserService(mockDb)
    const user = await service.findByEmail('test@example.com')

    expect(user.id).toBe(1)
    expect(mockDb.query).toHaveBeenCalledWith(
      'SELECT * FROM users WHERE email = ?',
      ['test@example.com']
    )
  })
})
```

### Rust (built-in + mockall)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;
    use mockall::mock;

    mock! {
        Database {}
        impl DatabaseTrait for Database {
            fn get_user(&self, id: i64) -> Result<User, Error>;
        }
    }

    #[test]
    fn test_user_service_fetches_from_db() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_get_user()
            .with(eq(1))
            .return_once(|_| Ok(User { id: 1, name: "Alice".into() }));

        let service = UserService::new(mock_db);
        let user = service.get_user(1).unwrap();

        assert_eq!(user.name, "Alice");
    }
}
```

## Anti-Patterns to Avoid

1. **Test Interdependence**: Tests that must run in specific order
2. **Testing Implementation**: Testing private methods or internal state
3. **Excessive Mocking**: Mocking everything makes tests brittle
4. **Assertion Roulette**: Multiple unrelated assertions in one test
5. **Hidden Dependencies**: Tests that rely on external files or services
6. **Slow Tests**: Tests that take seconds to run due to real I/O
7. **Brittle Tests**: Tests that break with minor refactoring
8. **Duplicate Logic**: Copying production code into tests

## Test Architecture

### Test Organization

```text
tests/
├── unit/              # Fast, isolated unit tests
│   ├── models/
│   ├── services/
│   └── utils/
├── integration/       # Component interaction tests
│   ├── api/
│   ├── database/
│   └── external_services/
├── e2e/              # Full workflow tests
│   └── user_scenarios/
├── fixtures/         # Shared test data
└── helpers/          # Test utilities
```

### Continuous Integration

- Run unit tests on every commit
- Run integration tests on PRs
- Run e2e tests before deployment
- Fail builds on coverage decrease
- Parallelize test execution
- Report flaky tests for investigation

## Examples

### Example 1: Unit Test with Mocking

```python
from unittest.mock import Mock, patch
import pytest
from payment_processor import PaymentProcessor

class TestPaymentProcessor:
    @patch('payment_processor.stripe')
    def test_successful_payment_creates_charge(self, mock_stripe):
        # Arrange
        mock_stripe.Charge.create.return_value = Mock(
            id='ch_123',
            status='succeeded'
        )
        processor = PaymentProcessor(api_key='test_key')

        # Act
        result = processor.charge(amount=1000, token='tok_visa')

        # Assert
        assert result.success is True
        assert result.charge_id == 'ch_123'
        mock_stripe.Charge.create.assert_called_once_with(
            amount=1000,
            currency='usd',
            source='tok_visa'
        )

    @patch('payment_processor.stripe')
    def test_declined_payment_raises_payment_error(self, mock_stripe):
        # Arrange
        mock_stripe.Charge.create.side_effect = Exception("Card declined")
        processor = PaymentProcessor(api_key='test_key')

        # Act & Assert
        with pytest.raises(PaymentError) as exc_info:
            processor.charge(amount=1000, token='tok_declined')

        assert "Card declined" in str(exc_info.value)
```

### Example 2: Integration Test with Database

```javascript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { createServer } from '../server'
import { db } from '../database'

describe('User API Integration', () => {
  let server

  beforeEach(async () => {
    server = await createServer()
    await db.migrate.latest()
    await db.seed.run()
  })

  afterEach(async () => {
    await db.migrate.rollback()
    await server.close()
  })

  it('creates user and returns 201 with user data', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'new@example.com',
        name: 'New User'
      }
    })

    expect(response.statusCode).toBe(201)
    expect(response.json()).toMatchObject({
      email: 'new@example.com',
      name: 'New User'
    })

    // Verify database state
    const user = await db('users').where({ email: 'new@example.com' }).first()
    expect(user).toBeDefined()
  })

  it('returns 400 for invalid email format', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'invalid-email',
        name: 'Test User'
      }
    })

    expect(response.statusCode).toBe(400)
    expect(response.json().error).toContain('email')
  })
})
```

### Example 3: Snapshot Testing

```javascript
import { render } from '@testing-library/react'
import { UserCard } from './UserCard'

it('renders user card correctly', () => {
  const user = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    avatar: '/avatars/alice.jpg'
  }

  const { container } = render(<UserCard user={user} />)

  // Snapshot testing for UI components
  expect(container.firstChild).toMatchSnapshot()
})
```

## Summary

This skill provides comprehensive testing expertise across:

- All test types (unit, integration, e2e)
- All domains (backend, frontend, data, ML, infrastructure)
- Test architecture and strategy
- Debugging and maintenance
- TDD/BDD workflows

The goal is production-quality tests that catch bugs, document behavior, and enable confident refactoring.
