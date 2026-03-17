---
name: testing-workflow
description: Write comprehensive tests following project conventions (tiers, patterns, anti-patterns). Use when writing tests, improving test coverage, fixing failing tests, or reviewing test quality.
---

# Testing Workflow Skill

## Quick Decision: Which Test Tier?

Ask yourself:
- **Fast local iteration?** → Tier 0 (`pytest --tier=0`)
- **Before commit?** → Tier 1 (`pytest`, default)
- **Integration validation?** → Tier 2 (`pytest --tier=2`)
- **Pre-deployment?** → Tier 3 (`pytest --tier=3`)
- **Release validation?** → Tier 4 (`pytest --tier=4`)

## Quick Decision: Which Test Strategy?

For Lambda/infrastructure testing (layers beyond pytest):
- **Quick dev iteration?** → Unit tests only (`just test-scheduler-unit`, 15s)
- **Before commit?** → Quick validation layers 1-5 (`just test-scheduler`, 2 min)
- **Lambda changes?** → Docker tests (`just test-scheduler-docker`, 90s)
- **Step Functions changes?** → Contract tests (`just test-scheduler-contracts`, 10s)
- **Pre-deployment?** → Full validation (`just test-scheduler-all`, 5 min)
- **AWS integration?** → Integration tests (`just test-scheduler-integration`, 60s)

See [Progressive Testing Strategy](PROGRESSIVE-TESTING.md) for the 7-layer approach.

---

## Docker-Based Testing for Lambda Functions

**NEW: Docker-based testing prevents "filesystem unaware" deployment failures**

For Lambda functions (LINE bot, Telegram API), run tests in Docker to match production runtime:

```bash
# LINE bot Docker import validation
./scripts/test_line_bot_docker.sh

# Pre-commit validation (syntax + unit tests + Docker imports)
./scripts/test_line_bot_pre_commit.sh
```

**Why Docker tests matter**:
- ✅ **Runtime fidelity**: Tests run in exact Lambda Python 3.11 environment
- ✅ **Filesystem aware**: Validates deployment package structure (`/var/task`)
- ✅ **Catches import errors**: "cannot import handle_webhook" caught before production
- ✅ **2 birds 1 stone**: Tests logic AND validates deployment environment

**CI/CD integration**:
- GitHub Actions runs Docker import tests automatically (`.github/workflows/deploy-line-dev.yml`)
- Tests block deployment if imports fail
- Prevents false positive deployments (tests pass but Lambda fails)

**Anti-pattern prevented**:
❌ Running tests in dev environment (setup-python) but deploying to Lambda (Docker container)
✅ Run tests in Docker container that matches deployed environment

See: `.claude/specifications/workflow/2025-12-29-implement-test-workflow-to-reduce-false-positive-deployment.md`

---

## Loop Pattern: Synchronize Loop (Test-Code Alignment)

**Escalation Trigger**:
- Tests pass but code still buggy (drift between test intent and reality)
- `/validate` shows tests don't actually test the claim
- Knowledge drift: Test assumptions outdated

**Tools Used**:
- `/validate` - Verify tests actually test what they claim (sabotage code, test should fail)
- `/consolidate` - Align test intent with code reality (update tests or fix code)
- `/trace` - Understand test failure causality (why did this test fail?)
- `/reflect` - Assess test quality (are we testing outcomes or just execution?)

**Why This Works**: Testing naturally involves synchronize loop—ensuring tests align with code behavior, not just pass.

See [Thinking Process Architecture - Feedback Loops](../../.claude/diagrams/thinking-process-architecture.md#11-feedback-loop-types-self-healing-properties) for structural overview.

---

## Test Structure

```
tests/
├── conftest.py         # Shared fixtures ONLY
├── shared/             # Agent, workflow, data tests
├── telegram/           # Telegram API tests
├── line_bot/           # LINE Bot tests (mark: legacy)
├── e2e/                # Playwright browser tests
├── integration/        # External API tests
└── infrastructure/     # S3, DynamoDB tests
```

## When to Use Each Tier

| Tier | Command | Includes | Use Case |
|------|---------|----------|----------|
| 0 | `pytest --tier=0` | Unit only | Fast local |
| 1 | `pytest` (default) | Unit + mocked | Deploy gate |
| 2 | `pytest --tier=2` | + integration | Nightly |
| 3 | `pytest --tier=3` | + smoke | Pre-deploy |
| 4 | `pytest --tier=4` | + e2e | Release |

## Writing a Test: Checklist

1. **Choose test location** based on component under test
2. **Use class-based structure**: `class TestComponent:`
3. **Follow canonical pattern**: See [PATTERNS.md](PATTERNS.md)
4. **Avoid anti-patterns**: Check [ANTI-PATTERNS.md](ANTI-PATTERNS.md)
5. **Apply defensive validation**: See [DEFENSIVE.md](DEFENSIVE.md)
6. **Verify test can fail**: Sabotage code, test should fail

## Common Workflows

### Writing a Unit Test
1. Create `class TestComponent` in appropriate test file
2. Add `setup_method()` if component needs initialization
3. Write test method: `def test_behavior_description(self):`
4. Use fixtures from conftest.py for shared data
5. Assert outcomes, not just execution
6. Sabotage code to verify test catches failures

### Adding Integration Tests
1. Mark with `@pytest.mark.integration`
2. Use real external APIs (LLM, yfinance, Aurora)
3. Validate multi-layer outcomes (status code → logs → data state)
4. Consider rate limits (`@pytest.mark.ratelimited`)

### Improving Test Coverage
1. Run `pytest --cov` to see coverage report
2. Identify untested branches and edge cases
3. Write tests for failure modes (not just success)
4. Add boundary condition tests

### Fixing Failing Tests
1. Read test failure message carefully
2. Check if code behavior changed (update test)
3. Check if test has anti-pattern (fix test)
4. Verify test isolation (no shared state between tests)

## Test Markers

```python
@pytest.mark.integration   # External APIs (LLM, yfinance)
@pytest.mark.smoke         # Requires live server
@pytest.mark.e2e           # Requires browser
@pytest.mark.legacy        # LINE bot (skip in Telegram CI)
@pytest.mark.ratelimited   # API rate limited (--run-ratelimited to include)
pytestmark = pytest.mark.legacy  # Mark entire file
```

## Quick Reference Commands

```bash
# Deploy gate (Tier 1)
just test-deploy

# Integration + Telegram only (Tier 2)
pytest --tier=2 tests/telegram

# Skip LINE bot and browser tests
pytest -m "not legacy and not e2e"

# Include rate-limited tests
pytest --run-ratelimited

# Coverage report
pytest --cov
```

## Rules (DO / DON'T)

| DO | DON'T |
|----|-------|
| `class TestComponent:` | `def test_foo()` at module level |
| `assert x == expected` | `return True/False` (pytest ignores!) |
| `assert isinstance(r, dict)` | `assert r is not None` (weak) |
| Define mocks in `conftest.py` | Duplicate mocks per file |
| Patch where USED: `@patch('src.api.module.lib')` | Patch where defined: `@patch('lib')` |
| `AsyncMock` for async methods | `Mock` for async (breaks await) |

## Next Steps

- **For test patterns**: See [PATTERNS.md](PATTERNS.md)
- **For anti-patterns to avoid**: See [ANTI-PATTERNS.md](ANTI-PATTERNS.md)
- **For defensive programming**: See [DEFENSIVE.md](DEFENSIVE.md)
- **For progressive testing (7-layer strategy)**: See [PROGRESSIVE-TESTING.md](PROGRESSIVE-TESTING.md)
- **For Lambda/Docker/contract testing**: See [LAMBDA-TESTING.md](LAMBDA-TESTING.md)
