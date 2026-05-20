---
name: testing
description: Testing patterns including pytest, unittest, mocking, fixtures, and test-driven development with extended thinking integration. Activate for test writing, coverage analysis, TDD, hypothesis-driven development, and quality assurance tasks.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
cross-references:
  - extended-thinking
  - deep-analysis
  - debugging
related-workflows:
  - .claude/workflows/e2e-test-suite.md
  - .claude/workflows/ci-cd-workflow.json
---

# Testing Skill

Provides comprehensive testing patterns and best practices with extended thinking integration for deliberate, hypothesis-driven test design.

## When to Use This Skill

Activate this skill when working with:
- Writing unit tests
- Integration testing
- Test fixtures and mocking
- Coverage analysis
- Test-driven development (TDD)
- Hypothesis-driven development (HDD)
- Test strategy design
- Pytest configuration
- Property-based testing
- Mutation testing

## Quick Reference

### Pytest Commands
```bash
# Run all tests
pytest

# Run specific file/directory
pytest tests/test_agent.py
pytest tests/unit/

# Run specific test
pytest tests/test_agent.py::test_health_endpoint
pytest -k "health"           # Match pattern

# Verbose output
pytest -v                    # Verbose
pytest -vv                   # Extra verbose
pytest -s                    # Show print statements

# Coverage
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html

# Stop on first failure
pytest -x
pytest --maxfail=3

# Parallel execution
pytest -n auto               # Requires pytest-xdist
```

## Test Structure

```python
# tests/test_agent.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from agent import app, AgentService

class TestHealthEndpoint:
    """Tests for /health endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_health_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get('/health')

        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

    def test_health_includes_agent_name(self, client):
        """Health response should include agent name."""
        response = client.get('/health')

        assert 'agent' in response.json
```

## Fixtures

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='session')
def engine():
    """Create test database engine."""
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='function')
def db_session(engine):
    """Create fresh database session for each test."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def sample_agent(db_session):
    """Create sample agent for testing."""
    agent = Agent(name='test-agent', type='claude')
    db_session.add(agent)
    db_session.commit()
    return agent

# Parametrized fixtures
@pytest.fixture(params=['claude', 'gpt', 'gemini'])
def agent_type(request):
    return request.param
```

## Mocking

```python
from unittest.mock import Mock, patch, MagicMock, AsyncMock

# Basic mock
def test_with_mock():
    mock_service = Mock()
    mock_service.process.return_value = {'status': 'ok'}
    result = handler(mock_service)
    mock_service.process.assert_called_once()

# Patch decorator
@patch('module.external_api')
def test_with_patch(mock_api):
    mock_api.fetch.return_value = {'data': 'test'}
    result = service.get_data()
    assert result == {'data': 'test'}

# Async mock
@pytest.mark.asyncio
async def test_async_function():
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {'result': 'success'}
    result = await async_handler(mock_client)
    assert result['result'] == 'success'
```

## Parametrized Tests

```python
@pytest.mark.parametrize('input,expected', [
    ('hello', 'HELLO'),
    ('world', 'WORLD'),
    ('', ''),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected

@pytest.mark.parametrize('agent_type,expected_model', [
    ('claude', 'claude-sonnet-4-20250514'),
    ('gpt', 'gpt-4'),
    ('gemini', 'gemini-pro'),
])
def test_model_selection(agent_type, expected_model):
    agent = create_agent(agent_type)
    assert agent.model == expected_model
```

## Coverage Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=term-missing --cov-fail-under=80"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]
```

## Using Extended Thinking for Test Design

**Integration with Extended Thinking Skill:** Before writing tests for complex functionality, use deliberate reasoning to design comprehensive test strategies that cover edge cases, error paths, and system behaviors.

### Why Extended Thinking Improves Testing

1. **Deeper Coverage Analysis**: Systematic reasoning identifies edge cases that intuitive testing misses
2. **Hypothesis Formation**: Formulate testable hypotheses about system behavior
3. **Risk Assessment**: Identify high-risk areas requiring more thorough testing
4. **Test Strategy Optimization**: Balance coverage depth with execution time and maintenance cost
5. **Mutation Testing Insights**: Reason about what changes should/shouldn't break tests

### Extended Thinking Process for Test Design

```python
"""
EXTENDED THINKING TEMPLATE FOR TEST DESIGN
Use this template when designing tests for complex functionality.

PHASE 1: UNDERSTAND THE SYSTEM
<thinking>
What is the core functionality being tested?
- Input requirements and valid ranges
- Expected outputs and side effects
- Dependencies and external interactions
- State transitions and invariants

What are the system boundaries?
- Valid/invalid input boundaries
- Resource limits (memory, time, connections)
- Concurrency boundaries
- Security boundaries

What assumptions exist in the code?
- Preconditions that must hold
- Postconditions that should be verified
- Invariants that should never be violated
</thinking>

PHASE 2: IDENTIFY TEST SCENARIOS
<thinking>
Happy path scenarios:
- Most common use cases
- Expected input/output pairs
- Normal state transitions

Edge cases:
- Boundary values (min, max, zero, empty)
- Off-by-one scenarios
- First/last element handling
- State boundary transitions

Error paths:
- Invalid inputs
- Missing dependencies
- Resource exhaustion
- Concurrent access violations
- Network/IO failures

Integration scenarios:
- Component interaction patterns
- Data flow through system
- Side effects on other components
</thinking>

PHASE 3: FORMULATE TEST HYPOTHESES
<thinking>
For each scenario, formulate testable hypotheses:

H1: "When given valid input X, the system produces output Y"
H2: "When input exceeds maximum value, the system raises ValidationError"
H3: "When concurrent requests modify the same resource, only one succeeds"
H4: "When external API fails, the system retries 3 times with exponential backoff"

Each hypothesis should be:
- Specific and measurable
- Falsifiable through testing
- Linked to a requirement or behavior
</thinking>

PHASE 4: DESIGN TEST STRATEGY
<thinking>
Test pyramid considerations:
- Unit tests: Fast, isolated, numerous (70-80%)
- Integration tests: Medium speed, component interaction (15-20%)
- E2E tests: Slow, full system, critical paths only (5-10%)

Property-based testing opportunities:
- Invariants that should hold for all inputs
- Commutative/associative properties
- Round-trip properties (serialize/deserialize)

Mock vs real dependencies:
- Mock: Fast feedback, isolate failures, but may miss integration issues
- Real: Higher confidence, but slower and more complex setup

Coverage targets:
- Critical paths: 100% coverage
- Error handling: 90%+ coverage
- Edge cases: Identified through boundary analysis
</thinking>

PHASE 5: IMPLEMENTATION PLAN
<thinking>
Test execution order:
1. Unit tests for core logic
2. Integration tests for component boundaries
3. E2E tests for critical user journeys
4. Performance tests for scalability requirements
5. Security tests for authentication/authorization

Fixture strategy:
- Session-scoped: Database connections, external service mocks
- Function-scoped: Test data, isolated state
- Parametrized: Test multiple scenarios with same logic

Assertion strategy:
- Positive assertions: Verify expected behavior
- Negative assertions: Verify error handling
- State assertions: Verify side effects
- Performance assertions: Verify timing/resource usage
</thinking>
"""
```

### Hypothesis-Driven Development (HDD) Pattern

HDD combines TDD with scientific method thinking for more robust test design.

```python
# Example: Testing a multi-tenant authorization system

"""
HYPOTHESIS: Users can only access resources within their organization.

TEST STRATEGY:
H1: User A in Org 1 can access Resource R1 in Org 1 → SHOULD PASS
H2: User A in Org 1 cannot access Resource R2 in Org 2 → SHOULD DENY
H3: Admin in Org 1 can access all resources in Org 1 → SHOULD PASS
H4: System admin can access resources across all orgs → SHOULD PASS
H5: Deleted user cannot access any resources → SHOULD DENY
H6: User with expired session cannot access resources → SHOULD DENY

RISK ASSESSMENT:
- High Risk: Cross-org data leakage (H2) - REQUIRES THOROUGH TESTING
- Medium Risk: Role escalation (H3, H4) - TEST ALL ROLE COMBINATIONS
- Medium Risk: Session management (H6) - TEST EXPIRATION EDGE CASES
- Low Risk: Normal access (H1) - BASIC COVERAGE SUFFICIENT
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from auth.service import AuthService, AuthorizationError
from models import User, Resource, Organization

class TestMultiTenantAuthorization:
    """
    Tests for multi-tenant authorization system.
    Based on hypothesis-driven test design for security-critical functionality.
    """

    @pytest.fixture
    def org1(self, db_session):
        """Create Organization 1 for isolation testing."""
        org = Organization(id="org-1", name="Organization One")
        db_session.add(org)
        db_session.commit()
        return org

    @pytest.fixture
    def org2(self, db_session):
        """Create Organization 2 for cross-org testing."""
        org = Organization(id="org-2", name="Organization Two")
        db_session.add(org)
        db_session.commit()
        return org

    @pytest.fixture
    def user_org1(self, db_session, org1):
        """Create standard user in Org 1."""
        user = User(
            id="user-1",
            org_id=org1.id,
            email="user1@org1.com",
            role="member"
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def resource_org1(self, db_session, org1):
        """Create resource in Org 1."""
        resource = Resource(
            id="resource-1",
            org_id=org1.id,
            name="Sensitive Data Org 1"
        )
        db_session.add(resource)
        db_session.commit()
        return resource

    @pytest.fixture
    def resource_org2(self, db_session, org2):
        """Create resource in Org 2."""
        resource = Resource(
            id="resource-2",
            org_id=org2.id,
            name="Sensitive Data Org 2"
        )
        db_session.add(resource)
        db_session.commit()
        return resource

    # H1: User A in Org 1 can access Resource R1 in Org 1
    def test_same_org_access_allowed(
        self, auth_service, user_org1, resource_org1
    ):
        """
        HYPOTHESIS: Users can access resources within their own organization.
        RISK: Low - Expected behavior
        COVERAGE: Happy path
        """
        result = auth_service.can_access(user_org1, resource_org1)

        assert result is True, "User should access resource in same org"

    # H2: User A in Org 1 cannot access Resource R2 in Org 2
    def test_cross_org_access_denied(
        self, auth_service, user_org1, resource_org2
    ):
        """
        HYPOTHESIS: Users cannot access resources in other organizations.
        RISK: HIGH - Security critical, data leakage prevention
        COVERAGE: Security boundary, negative test
        """
        with pytest.raises(AuthorizationError) as exc_info:
            auth_service.can_access(user_org1, resource_org2)

        assert "different organization" in str(exc_info.value).lower()
        assert exc_info.value.code == "CROSS_ORG_ACCESS_DENIED"

    # H3: Admin in Org 1 can access all resources in Org 1
    def test_admin_org_access(
        self, auth_service, db_session, org1, resource_org1
    ):
        """
        HYPOTHESIS: Admins can access all resources within their organization.
        RISK: Medium - Role escalation check
        COVERAGE: Permission elevation, positive test
        """
        admin = User(
            id="admin-1",
            org_id=org1.id,
            email="admin@org1.com",
            role="admin"
        )
        db_session.add(admin)
        db_session.commit()

        result = auth_service.can_access(admin, resource_org1)

        assert result is True, "Admin should access all org resources"

    # H4: System admin can access resources across all orgs
    def test_system_admin_global_access(
        self, auth_service, db_session, resource_org1, resource_org2
    ):
        """
        HYPOTHESIS: System admins have global access across all organizations.
        RISK: Medium - Highest privilege level
        COVERAGE: Global permission, multi-scenario test
        """
        system_admin = User(
            id="sys-admin",
            org_id=None,  # No org affiliation
            email="admin@system.com",
            role="system_admin"
        )
        db_session.add(system_admin)
        db_session.commit()

        # Should access resources in any org
        assert auth_service.can_access(system_admin, resource_org1) is True
        assert auth_service.can_access(system_admin, resource_org2) is True

    # H5: Deleted user cannot access any resources
    def test_deleted_user_access_denied(
        self, auth_service, user_org1, resource_org1, db_session
    ):
        """
        HYPOTHESIS: Soft-deleted users lose all access immediately.
        RISK: Medium - Security, account lifecycle
        COVERAGE: State transition, negative test
        """
        user_org1.deleted_at = datetime.utcnow()
        db_session.commit()

        with pytest.raises(AuthorizationError) as exc_info:
            auth_service.can_access(user_org1, resource_org1)

        assert "user deleted" in str(exc_info.value).lower()

    # H6: User with expired session cannot access resources
    def test_expired_session_access_denied(
        self, auth_service, user_org1, resource_org1
    ):
        """
        HYPOTHESIS: Expired sessions are rejected before authorization check.
        RISK: Medium - Session security
        COVERAGE: Time-based boundary, security check
        """
        expired_session = Mock(
            user_id=user_org1.id,
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )

        with pytest.raises(AuthorizationError) as exc_info:
            auth_service.can_access_with_session(
                expired_session, resource_org1
            )

        assert "session expired" in str(exc_info.value).lower()

    # PROPERTY-BASED TEST: Invariant checking
    @pytest.mark.parametrize("execution_count", range(100))
    def test_authorization_invariant_org_isolation(
        self, auth_service, db_session, execution_count
    ):
        """
        PROPERTY: For any user U in org O1 and resource R in org O2 where O1 != O2,
        authorization MUST fail.

        RISK: High - Core security invariant
        COVERAGE: Property-based, randomized inputs
        """
        # Generate random organizations
        org1 = Organization(id=f"org-{execution_count}-1")
        org2 = Organization(id=f"org-{execution_count}-2")
        db_session.add_all([org1, org2])

        # Generate random user and resource in different orgs
        user = User(id=f"user-{execution_count}", org_id=org1.id)
        resource = Resource(id=f"res-{execution_count}", org_id=org2.id)
        db_session.add_all([user, resource])
        db_session.commit()

        # INVARIANT: Cross-org access must always fail
        with pytest.raises(AuthorizationError):
            auth_service.can_access(user, resource)
```

## Test Strategy Templates

### Template 1: Feature Test Strategy

Use this template when implementing a new feature with tests.

```python
"""
FEATURE: {Feature Name}
REQUIREMENT: {Link to requirement/ticket}
RISK LEVEL: {High/Medium/Low}

EXTENDED THINKING ANALYSIS:
<thinking>
1. What is the core functionality?
   - {Description}

2. What are the critical success criteria?
   - {Criterion 1}
   - {Criterion 2}

3. What could go wrong?
   - {Risk 1}
   - {Risk 2}

4. What are the edge cases?
   - {Edge case 1}
   - {Edge case 2}

5. What are the integration points?
   - {System 1}
   - {System 2}

6. What performance characteristics matter?
   - {Performance requirement 1}
</thinking>

TEST PYRAMID ALLOCATION:
- Unit Tests: {X}% ({N} tests) - Core logic isolation
- Integration Tests: {Y}% ({M} tests) - Component interaction
- E2E Tests: {Z}% ({K} tests) - Critical user journeys

COVERAGE TARGETS:
- Line Coverage: {X}%
- Branch Coverage: {Y}%
- Critical Paths: 100%

TESTING APPROACH:
1. {Test category 1}: {Description}
2. {Test category 2}: {Description}
3. {Test category 3}: {Description}
"""

class TestFeatureName:
    """Tests for {Feature Name}."""

    # Unit tests
    def test_happy_path(self):
        """Test primary use case."""
        pass

    def test_edge_case_boundary_min(self):
        """Test minimum boundary value."""
        pass

    def test_edge_case_boundary_max(self):
        """Test maximum boundary value."""
        pass

    def test_error_invalid_input(self):
        """Test error handling for invalid input."""
        pass

    # Integration tests
    def test_integration_with_dependency(self):
        """Test interaction with external dependency."""
        pass

    # Performance tests
    def test_performance_within_sla(self):
        """Verify operation completes within SLA."""
        pass
```

### Template 2: Bug Fix Test Strategy

Use this template when fixing a bug to prevent regression.

```python
"""
BUG FIX: {Bug Title}
TICKET: {Bug tracker reference}
ROOT CAUSE: {Brief description}

EXTENDED THINKING ANALYSIS:
<thinking>
1. Why did this bug occur?
   - {Root cause analysis}

2. Why didn't existing tests catch it?
   - {Gap in test coverage}

3. What similar bugs could exist?
   - {Related scenarios to check}

4. How can we prevent this class of bugs?
   - {Preventive measures}
</thinking>

REGRESSION PREVENTION STRATEGY:
1. Reproduce bug with failing test
2. Fix implementation
3. Verify test passes
4. Add related edge case tests
5. Review similar code paths for same issue

TESTS TO ADD:
- [ ] Exact bug reproduction test
- [ ] Boundary cases around bug
- [ ] Related scenarios that could have same issue
- [ ] Integration test if bug involved multiple components
"""

class TestBugFix{BugId}:
    """
    Regression tests for bug #{BugId}.

    BUG: {Brief description}
    ROOT CAUSE: {Root cause}
    """

    def test_bug_reproduction_{bug_id}(self):
        """
        REPRODUCTION: Exact scenario that triggered the bug.
        This test should FAIL before fix, PASS after fix.
        """
        pass

    def test_related_scenario_1(self):
        """Related edge case that could have same issue."""
        pass

    def test_related_scenario_2(self):
        """Another related edge case."""
        pass
```

### Template 3: Refactoring Test Strategy

Use this template when refactoring to ensure behavior preservation.

```python
"""
REFACTORING: {Refactoring Name}
GOAL: {What we're improving}
SCOPE: {Files/modules affected}

EXTENDED THINKING ANALYSIS:
<thinking>
1. What behavior must be preserved?
   - {Behavior 1}
   - {Behavior 2}

2. What new behaviors are introduced?
   - {New behavior 1}

3. What could break during refactoring?
   - {Risk 1}
   - {Risk 2}

4. How do we verify equivalence?
   - {Verification approach}
</thinking>

REFACTORING SAFETY NET:
1. Run full test suite BEFORE refactoring (establish baseline)
2. Add characterization tests for unclear behavior
3. Refactor incrementally, running tests after each change
4. Add tests for new abstractions introduced
5. Verify performance hasn't regressed

EQUIVALENCE VERIFICATION:
- [ ] All existing tests still pass
- [ ] No new warnings or errors
- [ ] Performance within acceptable range
- [ ] API contracts unchanged (if public interface)
"""

class TestRefactoring{Name}:
    """
    Tests ensuring refactoring preserves existing behavior.
    """

    def test_preserves_behavior_scenario_1(self):
        """Verify behavior X unchanged after refactoring."""
        pass

    def test_new_abstraction_correct(self):
        """Test new abstraction introduced by refactoring."""
        pass
```

## Hypothesis-Driven Development Integration

HDD extends TDD by making test assumptions explicit and measurable.

### HDD Workflow

```
1. FORMULATE HYPOTHESIS
   "I believe that [system behavior] will [expected outcome] when [condition]"

2. DESIGN EXPERIMENT (TEST)
   - What inputs will test this hypothesis?
   - What outputs indicate hypothesis is correct/incorrect?
   - What side effects should be observed?

3. IMPLEMENT TEST
   - Write test that would pass if hypothesis is correct
   - Make hypothesis explicit in docstring
   - Include risk assessment

4. IMPLEMENT FUNCTIONALITY
   - Write minimal code to make test pass
   - Verify hypothesis was correct

5. REFINE HYPOTHESIS
   - If test fails, was hypothesis wrong or implementation wrong?
   - What new hypotheses does this suggest?
   - What edge cases does this reveal?
```

### HDD Example: Payment Processing

```python
"""
DOMAIN: Payment Processing
CRITICAL REQUIREMENT: Idempotent payment operations

HYPOTHESES:
H1: Duplicate payment requests with same idempotency key return same result
H2: Payment fails if insufficient funds, balance unchanged
H3: Successful payment updates balance atomically
H4: Concurrent payments with different keys both succeed
H5: Concurrent payments with same key only process once

RISK MATRIX:
H1, H5: HIGH RISK - Money duplication/loss
H2, H3: MEDIUM RISK - Financial accuracy
H4: LOW RISK - Throughput optimization
"""

class TestPaymentIdempotency:
    """
    Hypothesis-driven tests for payment idempotency.

    CRITICAL: Payment operations must be idempotent to prevent
    duplicate charges or money loss.
    """

    # H1: Duplicate payment requests return same result
    def test_duplicate_payment_same_result(self, payment_service, db_session):
        """
        HYPOTHESIS: Submitting identical payment request twice with same
        idempotency key returns the same payment_id and charges only once.

        RISK: HIGH - Could result in double charging customer
        TEST TYPE: Idempotency verification
        """
        idempotency_key = "pay-123-abc"
        payment_request = {
            "amount": 100.00,
            "currency": "USD",
            "customer_id": "cust-1",
            "idempotency_key": idempotency_key
        }

        # First request
        result1 = payment_service.create_payment(payment_request)

        # Duplicate request with same idempotency key
        result2 = payment_service.create_payment(payment_request)

        # VERIFY: Same payment returned, only charged once
        assert result1.payment_id == result2.payment_id
        assert result1.amount == result2.amount
        assert result1.status == result2.status

        # VERIFY: Only one charge in database
        charges = db_session.query(Charge).filter_by(
            idempotency_key=idempotency_key
        ).all()
        assert len(charges) == 1, "Should only create one charge"

    # H5: Concurrent payments with same key only process once
    @pytest.mark.asyncio
    async def test_concurrent_duplicate_payments_processed_once(
        self, payment_service, db_session
    ):
        """
        HYPOTHESIS: Concurrent payment requests with identical idempotency
        keys result in only one payment being processed.

        RISK: HIGH - Race condition could cause duplicate charges
        TEST TYPE: Concurrency, idempotency
        MECHANISM: Database-level locking or unique constraint
        """
        import asyncio

        idempotency_key = "pay-concurrent-123"
        payment_request = {
            "amount": 500.00,
            "currency": "USD",
            "customer_id": "cust-2",
            "idempotency_key": idempotency_key
        }

        # Launch 10 concurrent payment requests with same idempotency key
        tasks = [
            payment_service.create_payment_async(payment_request)
            for _ in range(10)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # VERIFY: All successful results have same payment_id
        successful_results = [
            r for r in results if not isinstance(r, Exception)
        ]
        payment_ids = {r.payment_id for r in successful_results}
        assert len(payment_ids) == 1, "All requests should return same payment"

        # VERIFY: Only one charge in database
        charges = db_session.query(Charge).filter_by(
            idempotency_key=idempotency_key
        ).all()
        assert len(charges) == 1, "Only one charge should be created"
        assert charges[0].amount == 500.00
```

## Property-Based Testing with Hypothesis

Property-based testing generates random inputs to verify system invariants.

```python
from hypothesis import given, strategies as st
import hypothesis

# Configure hypothesis settings
hypothesis.settings.register_profile(
    "ci",
    max_examples=1000,
    deadline=None,
)
hypothesis.settings.load_profile("ci")

class TestPropertiesOrganizationIsolation:
    """
    Property-based tests for multi-tenant isolation invariants.

    These tests verify that security properties hold for ALL possible inputs,
    not just hand-picked examples.
    """

    @given(
        org1_id=st.text(min_size=1, max_size=50),
        org2_id=st.text(min_size=1, max_size=50),
        user_id=st.text(min_size=1, max_size=50),
        resource_id=st.text(min_size=1, max_size=50),
    )
    def test_property_cross_org_access_always_denied(
        self, org1_id, org2_id, user_id, resource_id, auth_service, db_session
    ):
        """
        PROPERTY: For ANY user in org A and ANY resource in org B where A != B,
        access MUST be denied.

        INVARIANT: org_isolation(user.org_id, resource.org_id) => access_denied
        RISK: HIGH - Core security property
        """
        # Ensure orgs are different
        hypothesis.assume(org1_id != org2_id)

        # Create entities with hypothesis-generated IDs
        org1 = Organization(id=org1_id)
        org2 = Organization(id=org2_id)
        user = User(id=user_id, org_id=org1_id)
        resource = Resource(id=resource_id, org_id=org2_id)

        db_session.add_all([org1, org2, user, resource])
        db_session.commit()

        # INVARIANT: Cross-org access must always fail
        with pytest.raises(AuthorizationError):
            auth_service.can_access(user, resource)

    @given(
        amount=st.floats(min_value=0.01, max_value=1000000.0),
        currency=st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
    )
    def test_property_payment_amount_round_trip(self, amount, currency):
        """
        PROPERTY: Converting amount to cents and back preserves value within
        acceptable precision (0.01 for decimal currencies).

        INVARIANT: round_trip(amount) ≈ amount (within precision)
        """
        # Convert to cents (integer)
        cents = payment_service.to_cents(amount, currency)

        # Convert back to decimal
        recovered_amount = payment_service.from_cents(cents, currency)

        # VERIFY: Round-trip preserves value within precision
        precision = 0.01 if currency != "JPY" else 1.0
        assert abs(recovered_amount - amount) < precision

    @given(
        items=st.lists(
            st.tuples(st.text(min_size=1), st.floats(min_value=0, max_value=1000)),
            min_size=0,
            max_size=100
        )
    )
    def test_property_cart_total_commutative(self, items):
        """
        PROPERTY: Cart total is commutative - order of items doesn't matter.

        INVARIANT: total(items) == total(shuffled(items))
        """
        import random

        cart1 = ShoppingCart()
        for item_id, price in items:
            cart1.add_item(item_id, price)

        cart2 = ShoppingCart()
        shuffled_items = items.copy()
        random.shuffle(shuffled_items)
        for item_id, price in shuffled_items:
            cart2.add_item(item_id, price)

        # VERIFY: Total is independent of item order
        assert cart1.total() == cart2.total()
```

## Mutation Testing

Mutation testing verifies that your tests actually detect bugs by introducing intentional bugs (mutations) and checking if tests fail.

```bash
# Install mutation testing tool
pip install mutmut

# Run mutation testing
mutmut run

# Show results
mutmut results

# Show specific mutation
mutmut show <mutation_id>
```

```python
"""
MUTATION TESTING STRATEGY

Mutation testing introduces code changes (mutations) to verify tests catch bugs:
- Replace + with - (arithmetic mutations)
- Replace == with != (comparison mutations)
- Remove if conditions (conditional mutations)
- Replace True with False (boolean mutations)

MUTATION SCORE TARGET: 80%+

If mutations survive (don't fail tests):
1. Add test case for that scenario
2. Or: Remove unreachable/unnecessary code
"""

# Example: Code that should have high mutation coverage
def calculate_discount(price: float, customer_type: str) -> float:
    """
    Calculate discount based on customer type.

    This function has high mutation coverage because:
    - All branches are tested
    - All operators are exercised
    - All return values are verified
    """
    if price < 0:
        raise ValueError("Price cannot be negative")

    if customer_type == "premium":
        return price * 0.20  # 20% discount
    elif customer_type == "standard":
        return price * 0.10  # 10% discount
    else:
        return 0.0  # No discount

# Tests that achieve high mutation coverage
class TestCalculateDiscountMutationCoverage:
    """
    Tests designed to kill all mutations in calculate_discount.
    """

    def test_negative_price_raises_error(self):
        """Kills mutations: price < 0 -> price <= 0, price > 0"""
        with pytest.raises(ValueError, match="negative"):
            calculate_discount(-1.0, "standard")

    def test_zero_price_allowed(self):
        """Kills mutations: price < 0 -> price <= 0"""
        result = calculate_discount(0.0, "standard")
        assert result == 0.0

    def test_premium_discount_rate(self):
        """Kills mutations: 0.20 -> 0.19, 0.21, etc."""
        result = calculate_discount(100.0, "premium")
        assert result == 20.0  # Exact value verification

    def test_standard_discount_rate(self):
        """Kills mutations: 0.10 -> 0.09, 0.11, etc."""
        result = calculate_discount(100.0, "standard")
        assert result == 10.0  # Exact value verification

    def test_unknown_customer_no_discount(self):
        """Kills mutations: return 0.0 -> return 1.0, etc."""
        result = calculate_discount(100.0, "unknown")
        assert result == 0.0

    def test_premium_string_exact_match(self):
        """Kills mutations: == "premium" -> != "premium", etc."""
        # Should not give discount for near-matches
        assert calculate_discount(100.0, "Premium") == 0.0
        assert calculate_discount(100.0, "premium ") == 0.0
```

## Advanced Pytest Patterns

### Async Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_api_call():
    """Test asynchronous API call."""
    client = AsyncAPIClient()
    result = await client.fetch_data()
    assert result['status'] == 'success'

# Test with timeout
@pytest.mark.asyncio
@pytest.mark.timeout(5)  # Requires pytest-timeout
async def test_with_timeout():
    """Test that completes within timeout."""
    result = await slow_operation()
    assert result is not None

# Test concurrent operations
@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test multiple concurrent async operations."""
    tasks = [
        async_operation(i)
        for i in range(10)
    ]
    results = await asyncio.gather(*tasks)
    assert len(results) == 10
    assert all(r['success'] for r in results)
```

### Dynamic Fixtures with Factory Pattern

```python
import pytest
from factory import Factory, Faker, SubFactory
from models import User, Organization, Membership

# Factory definitions
class OrganizationFactory(Factory):
    class Meta:
        model = Organization

    id = Faker('uuid4')
    name = Faker('company')
    created_at = Faker('date_time')

class UserFactory(Factory):
    class Meta:
        model = User

    id = Faker('uuid4')
    email = Faker('email')
    organization = SubFactory(OrganizationFactory)

# Fixture using factories
@pytest.fixture
def user_with_org(db_session):
    """Create user with associated organization."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def multiple_users_same_org(db_session):
    """Create multiple users in same organization."""
    org = OrganizationFactory()
    users = [UserFactory(organization=org) for _ in range(5)]
    db_session.add(org)
    db_session.add_all(users)
    db_session.commit()
    return users
```

### Snapshot Testing

```python
import pytest

def test_api_response_snapshot(snapshot, client):
    """
    Test API response matches snapshot.

    Useful for testing complex JSON responses or rendered output.
    First run creates snapshot, subsequent runs compare against it.
    """
    response = client.get('/api/user/123')

    # Compare full response against snapshot
    snapshot.assert_match(response.json(), 'user_response.json')

def test_rendered_template_snapshot(snapshot, client):
    """Test rendered HTML matches snapshot."""
    response = client.get('/profile')

    snapshot.assert_match(response.data.decode(), 'profile_page.html')
```

### Test Tagging and Organization

```python
import pytest

# Smoke tests - critical path only
@pytest.mark.smoke
def test_critical_user_login():
    """Critical path test run in every build."""
    pass

# Slow tests - run nightly
@pytest.mark.slow
def test_full_data_migration():
    """Slow test run in nightly builds."""
    pass

# Integration tests
@pytest.mark.integration
def test_payment_gateway_integration():
    """Integration test with external service."""
    pass

# Security tests
@pytest.mark.security
def test_sql_injection_prevention():
    """Security-focused test."""
    pass

# Run specific markers:
# pytest -m smoke          # Run only smoke tests
# pytest -m "not slow"     # Skip slow tests
# pytest -m "integration"  # Run only integration tests
```

## Test Data Management

### Test Data Builders

```python
class UserBuilder:
    """
    Builder pattern for creating test users with fluent interface.

    Provides explicit, readable test data construction.
    """

    def __init__(self):
        self._user = User(
            email="test@example.com",
            role="member",
            status="active"
        )

    def with_email(self, email: str):
        self._user.email = email
        return self

    def as_admin(self):
        self._user.role = "admin"
        return self

    def in_organization(self, org_id: str):
        self._user.org_id = org_id
        return self

    def deleted(self):
        self._user.status = "deleted"
        self._user.deleted_at = datetime.utcnow()
        return self

    def build(self) -> User:
        return self._user

# Usage in tests
def test_admin_can_delete_users():
    admin = UserBuilder().as_admin().build()
    target_user = UserBuilder().build()

    result = admin.delete_user(target_user)

    assert result.success is True
```

### Database Test Isolation Strategies

```python
# Strategy 1: Transaction rollback (fastest)
@pytest.fixture(scope='function')
def db_session_rollback(engine):
    """
    Create session that rolls back after each test.
    FASTEST but doesn't catch transaction-related bugs.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Strategy 2: Truncate tables (medium speed)
@pytest.fixture(scope='function')
def db_session_truncate(engine):
    """
    Truncate all tables after each test.
    MEDIUM speed, catches more transaction issues.
    """
    session = Session(bind=engine)

    yield session

    session.close()
    # Truncate all tables
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

# Strategy 3: Drop and recreate (slowest, most isolated)
@pytest.fixture(scope='function')
def db_session_recreate(engine):
    """
    Drop and recreate all tables for each test.
    SLOWEST but complete isolation.
    """
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    yield session

    session.close()
    Base.metadata.drop_all(engine)
```

## Cross-References

### Related Skills
- **extended-thinking**: Use for complex test strategy design and hypothesis formulation
- **deep-analysis**: Use for analyzing test coverage gaps and mutation testing results
- **debugging**: Use when tests fail to identify root causes

### Related Workflows
- `.claude/workflows/e2e-test-suite.md`: End-to-end testing workflow
- `.claude/workflows/ci-cd-workflow.json`: Continuous integration with automated testing

### Integration Points
- Use extended thinking BEFORE writing tests for complex features
- Use hypothesis-driven development for security-critical code
- Use property-based testing for verifying system invariants
- Use mutation testing to verify test quality

## Best Practices Summary

1. **Think Before Testing**: Use extended thinking for complex test design
2. **Make Hypotheses Explicit**: Document what you're testing and why
3. **Property-Based Testing**: Verify invariants with random inputs
4. **Mutation Testing**: Verify tests actually catch bugs
5. **Test Pyramid**: 70% unit, 20% integration, 10% E2E
6. **Isolation**: Use appropriate database isolation strategy
7. **Readability**: Test code is documentation - make it clear
8. **Performance**: Fast tests run more often - optimize test execution
9. **Coverage**: Target 80%+ line coverage, 100% critical path coverage
10. **Continuous**: Run tests on every commit, extended tests nightly
