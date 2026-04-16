---
name: nw-tdd-methodology
description: Deep knowledge for Outside-In TDD - double-loop architecture, ATDD integration, port-to-port testing, walking skeletons, and test doubles policy
user-invocable: false
disable-model-invocation: true
---

# Outside-In TDD Methodology

## Double-Loop TDD Architecture

Outer loop: ATDD/E2E Tests (customer view) - business requirements, hours-days to green.
Inner loop: Unit Tests (developer view) - technical implementation, minutes to green, RED->GREEN->REFACTOR.

Outer stays red while inner cycles. Outer drives WHAT to build, inner drives HOW.
Never build components not needed by actual user scenarios.

## Outside-In vs Inside-Out

Inside-Out (Classic/bottom-up): discovers collaborators through refactoring. TDD guides design completely.
Outside-In (London/top-down/mockist): knows collaborators upfront, mocks them, implements each moving inward.

Use Outside-In when: architectural boundaries known (hexagonal), program to interface not implementation.

## ATDD Integration (Lightweight)

Original 2008 heavyweight ATDD was "too heavyweight for most real teams." Updated approach (Hendrickson 2024):
- Few Given/When/Then examples, not many | Separate requirements from tests
- Smallest subset of team with relevant skills | Value = shared understanding, not executable specs
- Automate only where high-value

## BDD Integration

BDD emerged from Outside-In TDD. Given(context)->When(action)->Then(outcome) maps to outside-in mindset.
BDD reframes TDD as design/specification technique, not just testing. More accessible to stakeholders.
Gherkin: structured format bridging technical/non-technical. Use pragmatically - automate only where high value.

## Outside-In Development Workflow (Bache)
1. Write Guiding Test (acceptance) from user perspective - thick slice of functionality
2. Start at top-level entry point, design collaborating classes incrementally
3. Use mocks to experiment with interfaces/protocols
4. As each layer implemented, move to previously mocked collaborators, TDD again
5. Never build what isn't needed for actual user scenarios

## Port-to-Port Testing (ALL test levels)

ALL tests — acceptance, unit, integration — enter through a driving port and assert outcomes at driven port boundaries. No exceptions.
Internal classes (entities, value objects, domain services) exercised indirectly — never instantiated directly in test code.

- **Acceptance test**: enters from application service driving port, asserts at driven port boundary (port-to-port)
- **Unit test**: enters from domain function driving port (pure function public API), asserts on return value (port-to-port at domain scope)
- **Integration test**: verifies adapter correctly implements port contract against real infrastructure (adapter-to-port, NOT port-to-port). Tests the bridge between infrastructure and port.

Unit tests are NOT "isolated object tests." They are port-to-port at a smaller scope. The driving port for a pure domain function IS the function's public signature.

Flow: Driving Port -> Application -> Domain -> Driven Port (mocked)

```python
def test_order_service_processes_payment():
    # Setup - mock driven port (external dependency)
    payment_gateway = MockPaymentGateway()
    order_repo = InMemoryOrderRepository()

    # Test through driving port (application service)
    order_service = OrderService(payment_gateway, order_repo)
    result = order_service.place_order(customer_id, items)

    # Assert observable outcomes
    assert result.is_confirmed()
    payment_gateway.verify_charge_called(amount=100.00)
```

## No Code Without a Requiring Test

Every line of production code exists because a test required it. No speculative implementation.

- Acceptance test drives WHAT is needed (observable behavior)
- Unit test drives HOW to decompose (inner loop, only when GREEN is complex)
- If the acceptance test passes without a unit test, no unit test is needed
- If a step finds "already implemented from WS, just remove @skip" — that's CORRECT

The test pyramid is not a quota system. Write the minimum tests that give confidence at the right level.

## Unit of Behavior (not Unit of Code)

Test = story about the problem your code solves. Granularity related to stakeholder needs.
A unit of behavior may span multiple classes. Test from driving port to driven port boundary.
Key question: "Can you explain this test to a stakeholder?" If not, you're testing implementation details.

## Classical vs Mockist Verification

Classical TDD: real objects | state verification | less coupled to implementation | survives refactoring better.
Mockist TDD: mocks for objects with behavior | behavior verification | lighter setup | more coupled to impl.
Best practice: combine strategically. Behavior verification at layer boundaries, state verification within layers.

## Test Doubles Taxonomy (Meszaros)
- Dummy: passed but never used
- Fake: working impl with shortcuts (in-memory DB)
- Stub: predefined answers
- Spy: stub that records interactions
- Mock: pre-programmed with expectations for behavior verification

Choose type by need: mock for interaction design | stub when don't care about interaction | fake for integration bridge.

## Hexagonal Architecture Testing Strategy

### Domain Layer
Tested indirectly through driving port (application service) unit tests with real domain objects.
Domain entities, value objects, domain services are implementation details. Testing them directly couples tests to internal structure.

Pure domain functions (e.g., evaluate_gate, check_tier) ARE their own driving ports — calling them directly in tests IS port-to-port testing because the function signature IS the public interface. This is not an exception; it's the correct application of port-to-port to the domain layer.

### Application Layer
Classical TDD within layer, Mockist TDD at port boundaries.
Use real Order, Money, Customer objects in application service tests.
Mock IPaymentGateway, IEmailService ports when testing orchestration.

### Infrastructure Layer (Adapters)
Integration tests ONLY — no unit tests for adapters. Mocking infrastructure inside an adapter test is testing the mock, not the adapter.
Use real infrastructure (testcontainers, in-memory databases, real filesystem via tmp_path, real subprocess) to verify actual behavior.

Adapter integration tests are typically created to make the Walking Skeleton pass — the WS requires real adapters, which drives the implementation of the adapter AND its integration test. Additional adapter tests for specific error conditions (disk full, timeout, permission denied) are created in subsequent focused scenarios tagged `@infrastructure-failure` (see Mandate 6). Subsequent happy-path scenarios use InMemory doubles for speed; the adapter correctness is proven by the WS + infrastructure failure scenarios.

### E2E Tests
Minimal mocking - only truly external systems (3rd party APIs beyond your control).
Use real domain services, application services, repositories.

## Test Doubles Policy

Acceptable (port boundaries only):
- `Mock<IPaymentGateway>` - external payment service port
- `Mock<IEmailService>` - external email provider port
- `InMemoryUserRepository` - fake for fast tests (implements IUserRepository port)

Do not mock inside the hexagon:
- Domain entities (Order, Customer) - use real objects
- Value objects (Money, Email) - cheap to create, deterministic
- Application services (OrderProcessor) - use real with mocked ports
- Domain services (PricingService) - use real objects

## Integration Test Contract: Test Doubles Must Validate Inputs

Every InMemory test double MUST enforce the same input preconditions as the real adapter. A test double that accepts inputs the real adapter would reject creates invisible wiring bugs that only surface in production.

**The rule**: if the real adapter crashes on an input, the test double must also fail on that input.

**What to validate in every test double:**
- Required parameters are not None
- Required string fields are not empty
- Numeric fields are within valid ranges (turns > 0, timeout > 0, budget >= 0)
- Enum fields contain valid values
- Complex objects have required nested fields populated

**Why**: DES 3.0 dogfood found 3 wiring bugs that 96 acceptance tests missed — because InMemoryVendorAdapter accepted None config, empty prompt file, and wrong field names. The real ClaudeCliAdapter crashed on all 3. The tests were green but the system was broken.

**Example**:
```python
# WRONG — too permissive, hides wiring bugs
class InMemoryVendorAdapter:
    def dispatch(self, config):
        return Success(self._canned_result)  # accepts anything

# CORRECT — validates like the real adapter
class InMemoryVendorAdapter:
    def dispatch(self, config):
        assert config is not None, "PhaseDispatchConfig required"
        assert config.assembled_prompt_file, "Prompt file must be set"
        assert config.max_turns > 0, "max_turns must be positive"
        return Success(self._canned_result)
```

This is not optional. A test double without input validation is a test double that lies.

## Walking Skeleton Protocol

At most one walking skeleton per new feature. When `is_walking_skeleton: true` in roadmap:
- Write exactly ONE E2E/acceptance test proving end-to-end wiring with REAL adapters
- Implement thinnest possible slice — hardcoded values, minimal branching
- Unit tests are written ONLY if needed to decompose complex GREEN implementation
- Do NOT add error handling, edge cases, or validation beyond what the AT requires
- No code without a test that requires it — the AT drives ALL implementation

The WS is an acceptance test on steroids: it proves wiring AND drives implementation of adapters, domain logic, and application services. If the WS AT requires 5 functions to pass, those 5 functions are justified. Subsequent steps that find "already implemented, just remove @skip" confirms the WS was well-designed.

Integration tests for adapters (real filesystem, real subprocess) are naturally created during WS — the WS REQUIRES real adapters, which drives their implementation and testing.

## Post-GREEN Wiring Verification (MANDATORY)

After ALL tests pass in GREEN phase and BEFORE proceeding to COMMIT:

1. Run `git diff --name-only` and verify that EVERY file listed in the step's
   `files_to_modify` appears in the diff. If a production file is NOT modified
   but tests flipped from RED to GREEN, this is **Fixture Theater** — the test
   fixtures are implementing the feature, not production code. BLOCK the COMMIT.

2. **Deletion test**: Mentally (or actually) revert production changes. Would
   tests still pass? If yes, the test is exercising fixture state, not production code.

3. If `git diff --stat` shows ONLY test file changes, STOP. Go back to GREEN
   and implement the production code. Tests passing without production changes
   is a DES integrity violation.

## E2E Test Management

Enable ONE E2E test at a time to prevent commit blocks:
1. All E2E tests except first one marked with skip/ignore
2. Complete first scenario through Outside-In TDD
3. Commit working implementation
4. Enable next E2E test
5. Repeat until all scenarios implemented

## Step Method Pattern

Step methods call production services, not test infrastructure:

```csharp
[When("business action occurs")]
public async Task WhenBusinessActionOccurs()
{
    var service = _serviceProvider.GetRequiredService<IBusinessService>();
    _result = await service.PerformBusinessActionAsync(_testData);
}
```

Scaffold unimplemented collaborators with `NotImplementedException`:
```csharp
throw new NotImplementedException(
    "Business capability not yet implemented - driven by outside-in TDD"
);
```

## Business-Focused Testing

### Unit Test Naming
- Class pattern: `<DrivingPort>Should`
- Method pattern: `<ExpectedOutcome>_When<SpecificBehavior>[_Given<Preconditions>]`
- Example: `AccountServiceShould.IncreaseBalance_WhenDepositMade_GivenSufficientFunds`

### Behavior Types
- Command behavior: changes system state (Given-When-Then)
- Query behavior: returns state projection (Given-Then)
- Process behavior: orchestrates multiple commands/queries

### Test Structure
- Arrange: set up business context and test data
- Act: perform business action
- Assert: validate business outcome and state changes

## Environment-Adaptive Testing
- Local development: in-memory infrastructure for fast feedback (~100ms)
- CI/CD pipeline: production-like infrastructure for integration validation (~2-5s)
- Same scenarios: single source of truth across all environments

## Mandate 5: Walking Skeleton E2E Strategy

The DISTILL acceptance designer determines the WS adapter strategy for each feature. This is auto-detected with user confirmation, not a question to the user.

### Decision Tree

```
Feature is pure domain (no driven ports with I/O)? → Strategy A (InMemory)
Feature has only local resources (filesystem, git, in-process)? → Strategy C (Real local)
Feature has costly external dependencies (paid APIs, LLM calls)? → Strategy B (Real local + fake costly)
Team needs CI flexibility? → Strategy D (Configurable via env var)
```

### Resource Classification Table

| Resource Type | WS Local | WS CI | Adapter Integration Test |
|--------------|----------|-------|------------------------|
| Filesystem | real (tmp_path) | real (tmp_path) | real (tmp_path) — ALWAYS |
| Git repo | real (tmp_path + git init) | real | real — ALWAYS |
| Local subprocess (pytest, ruff, grep) | real | real | real — ALWAYS |
| Costly subprocess (claude -p, LLM) | fake (mock Popen) | fake | contract smoke (@requires_external) |
| Paid external API (Stripe, Blumberg) | fake server | fake server | contract test with recorded fixtures |
| Database | real (SQLite/testcontainers) | real (testcontainers) | real — ALWAYS |
| Container services | optional (docker-compose) | testcontainers | real if available |

### Walking Skeleton Adapter Rule

Under strategies B/C/D, the WS uses real adapters for local resources. InMemory is ONLY for costly external resources that have a separate contract test.

### Determinism Contract

Real-adapter WS tests accept non-determinism as a trade-off for environmental realism. InMemory acceptance tests remain the fast deterministic inner loop. The WS is the slow truth-checking outer loop. Both are necessary. If WS fails, triage: logic failure (fix code) or environment failure (retry, investigate infra).

### Rollback Policy

If WS with Strategy C fails due to infrastructure issues (not code bugs), downgrade to Strategy B for that step. Document the downgrade in wave-decisions.md with justification.

## Mandate 6: Adapter Integration Tests Are Real I/O

Every driven adapter has at least ONE integration test with real I/O. This is not optional regardless of WS strategy.

### Adapter Type Minimum Real I/O Test

| Adapter Type | Minimum Real I/O Test |
|-------------|----------------------|
| Filesystem adapter | tmp_path fixture, real read/write/delete |
| Subprocess adapter (local) | real subprocess call, real exit codes |
| Subprocess adapter (costly) | contract smoke test with @requires_external marker |
| Config/env adapter | real env vars or real config file on tmp_path |
| Git adapter | real temp git repo (tmp_path + git init + git commit) |
| Database adapter | real DB (SQLite in-memory or testcontainers) |
| Network/HTTP adapter | contract test against recorded fixture or fake server |

"Real" means: the test would FAIL if the adapter's actual system dependency is absent or broken.

### Tagging Convention for Enforcement

- Scenarios using real adapters: `@real-io`
- Scenarios using InMemory: `@in-memory`
- Walking skeleton: `@walking_skeleton` + `@real-io` (for strategies B/C/D)
