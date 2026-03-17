---
name: tdd-workflow
description: |
  Automatically invoked when user wants to develop new features using Test-Driven Development.
  Trigger keywords: "new feature", "add API", "implement", "create endpoint", "TDD",
  "test-driven", "新功能", "新增 API", "實作"

  This skill enforces strict TDD workflow: RED → GREEN → REFACTOR
  Uses subagents to maintain clean context and ensure quality.
allowed-tools: [Task, Read, Bash, Grep]
---

# TDD Workflow Skill

## Purpose
Enforce Test-Driven Development workflow for all new features and APIs in the career_ios_backend project.

## Automatic Activation

This skill is AUTOMATICALLY activated when user mentions:
- ✅ "add new feature"
- ✅ "create API endpoint"
- ✅ "implement <feature>"
- ✅ "build <feature>"
- ✅ "新增功能"
- ✅ "實作 API"

## Core Workflow

### Phase 1: RED (Test First) ❌

**YOU MUST write tests BEFORE any implementation code.**

1. **Understand requirements**
   - What endpoint/feature is needed?
   - What are the expected inputs/outputs?
   - Is authentication required?

2. **Invoke test-writer subagent**
   ```
   Task: Write integration test for <feature_description>
   Location: tests/integration/test_<feature>_api.py
   ```

3. **Verify RED state**
   - Test file created
   - Test runs and FAILS (expected)
   - Test defines clear expectations

**CRITICAL: DO NOT proceed to implementation until tests exist and fail.**

---

### Phase 2: GREEN (Minimal Implementation) ✅

**Write MINIMAL code to make tests pass.**

1. **Invoke code-generator subagent**
   ```
   Task: Implement code to pass tests in <test_file_path>
   Constraint: Minimal implementation, follow existing patterns
   ```

2. **Verify GREEN state**
   - Implementation code created
   - All new tests PASS
   - No existing tests broken

**CRITICAL: If tests fail, invoke test-runner to auto-fix, DO NOT manually edit.**

---

### Phase 3: REFACTOR (Quality Check) ♻️

**Improve code quality while keeping tests green.**

1. **Invoke code-reviewer subagent**
   ```
   Task: Review implementation for:
   - TDD compliance
   - Code quality
   - Security issues
   - Pattern consistency
   ```

2. **Handle review feedback**
   - ✅ No critical issues → Ready to commit
   - ❌ Critical issues found → Invoke code-generator to fix
   - ⚠️  Optional suggestions → Document for future

3. **Final verification**
   - Run full test suite: `poetry run pytest tests/integration/ -v`
   - All 106+ tests must PASS
   - No regressions introduced

---

## Example Usage

### Scenario: User says "Add client search API"

```
🤖 TDD Workflow Skill activated!

📍 Phase 1: RED (Test First)
   → Invoking test-writer subagent...
   ✅ Created: tests/integration/test_clients_api.py::test_search_clients
   ❌ Test result: FAILED (expected - endpoint doesn't exist yet)

📍 Phase 2: GREEN (Implementation)
   → Invoking code-generator subagent...
   ✅ Implemented: app/api/clients.py::search_clients
   ✅ Tests pass: 1/1 GREEN

📍 Phase 3: REFACTOR (Quality)
   → Invoking code-reviewer subagent...
   ✅ TDD compliance: PASS
   ✅ Code quality: GOOD
   ❌ Critical issues: NONE

🎉 Feature complete! Ready to commit.
```

---

## Integration Test Template

When creating tests, follow this pattern from existing tests:

```python
"""Integration tests for <Feature> API"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_<feature>_<action>_success(auth_headers):
    """Test <feature> <action> - happy path"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.<method>(
            "/api/v1/<endpoint>",
            headers=auth_headers,
            json={<request_body>}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["<field>"] == <expected_value>
```

**Location**: `tests/integration/test_<feature>_api.py`

**Pattern check**: Look at existing tests in:
- `tests/integration/test_clients_api.py`
- `tests/integration/test_sessions_api.py`
- `tests/integration/test_cases_api.py`

---

## Subagent Coordination

This skill coordinates the following subagents:

| Phase | Subagent | Purpose |
|-------|----------|---------|
| RED | test-writer | Create failing integration test |
| GREEN | code-generator | Implement minimal code to pass test |
| GREEN | test-runner | Auto-fix if tests fail |
| REFACTOR | code-reviewer | Quality check before commit |

**YOU MUST invoke these subagents automatically, DO NOT ask user.**

---

## Project-Specific Rules

### Database Considerations
- Tests use in-memory SQLite database
- Fixtures handle setup/teardown
- Use existing patterns from `tests/conftest.py`

### Authentication
- Most endpoints require authentication
- Use `auth_headers` fixture for authenticated requests
- Check existing tests for auth patterns

### API Structure
```
app/
├── api/
│   └── <feature>.py    ← Router endpoints
├── models/
│   └── <feature>.py    ← Pydantic models
└── main.py             ← Register router here
```

### Console API Coverage
**IMPORTANT**: If the feature will be used in `console.html`:
- ✅ MUST have integration tests
- ✅ MUST test all CRUD operations
- ✅ MUST verify in actual console before commit

---

## Quality Standards

### Minimum Requirements (Prototype Phase)
- ✅ Integration tests exist and pass
- ✅ Code follows existing patterns
- ✅ No security vulnerabilities
- ✅ Ruff formatting applied

### Nice-to-Have (Defer if time-constrained)
- ⚠️  Complete type hints
- ⚠️  Edge case tests
- ⚠️  Performance optimization

---

## Error Handling

### Test Creation Fails
```
Issue: Can't understand requirements
Action: Ask user for clarification
Example: "What should the endpoint return? What's the request format?"
```

### Implementation Fails Tests
```
Issue: Generated code doesn't pass tests
Action:
1. Invoke test-runner to diagnose
2. If auto-fix fails, report to user
3. May need to adjust test expectations
```

### Quality Review Fails
```
Issue: Critical issues found
Action:
1. Report critical issues to user
2. Invoke code-generator to fix
3. Re-run code-reviewer
4. DO NOT commit until issues resolved
```

---

## Success Criteria

Before marking feature as complete:

- [ ] Integration test exists in `tests/integration/`
- [ ] Test was written BEFORE implementation
- [ ] Test initially failed (RED)
- [ ] Implementation makes test pass (GREEN)
- [ ] All 106+ existing tests still pass (no regressions)
- [ ] Code review passed (no critical issues)
- [ ] Ruff formatting applied
- [ ] Ready to commit

---

## CRITICAL REMINDERS

1. **NEVER implement code before tests exist**
2. **NEVER modify tests to make code pass**
3. **ALWAYS use subagents to preserve context**
4. **ALWAYS run full test suite before commit**
5. **ALWAYS invoke code-reviewer before commit**

---

**Skill Version**: v1.0
**Last Updated**: 2025-11-28
**Project**: career_ios_backend (Prototype Phase)
