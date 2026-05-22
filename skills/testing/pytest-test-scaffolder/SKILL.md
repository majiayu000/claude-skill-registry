---
name: pytest-test-scaffolder
description: Scaffolds pytest unit tests for Python backend functions and classes. Use when creating tests for FastAPI endpoints, services, and utilities.
---

# Pytest Test Scaffolder

Generates comprehensive unit tests for Python backend code using pytest with Pydantic validation, Firestore mocking, and Genkit integration testing patterns.

## Workflow

1. **Identify function/class to test:**
   - Ask for file path (e.g., `backend/app/api/endpoints/profiles.py`)
   - Read file to extract:
     - Function/class name
     - Parameters and type annotations
     - Return types
     - Dependencies (Firestore, Genkit, services)
   - Determine test location: `backend/app/tests/{{module}}/test_{{name}}.py`

2. **Analyze code structure:**
   - Extract function signature and parameters
   - Identify external dependencies (database, API, AI services)
   - Determine input validation (Pydantic models)
   - Identify error cases (ValueError, ValidationError, HTTPException)
   - Check for async/await patterns

3. **Generate test file:**
   - Replace placeholders in template:
     - `{{FUNCTION_NAME}}` - Function being tested
     - `{{FUNCTION_MODULE}}` - Module import path
     - `{{PARAMETERS}}` - Function parameters with defaults
     - `{{RETURN_TYPE}}` - Expected return type
     - `{{HAPPY_PATH_TESTS}}` - Success scenarios
     - `{{ERROR_TESTS}}` - Exception handling
     - `{{FIXTURES}}` - Mock/fixture setup
   - Write to: `backend/app/tests/{{module}}/test_{{name}}.py`

4. **Include comprehensive test scenarios:**
   - ✅ **Happy Path**: Valid inputs produce expected output
   - ✅ **Validation Error**: Invalid Pydantic models rejected (422)
   - ✅ **Not Found Error**: Resource not found handled (404)
   - ✅ **Permission Error**: Unauthorized access rejected (401)
   - ✅ **Server Error**: Exceptions caught and logged (500)
   - ✅ **Mock Dependencies**: Firestore, Genkit, services mocked
   - ✅ **Async Support**: Use pytest-asyncio for async functions
   - ✅ **Fixture Reuse**: Shared fixtures in conftest.py

5. **Use pytest best practices:**
   - Use fixtures for mock setup (Firestore, Firebase, Genkit)
   - Use `monkeypatch` for environment variables
   - Use `@pytest.mark` for test categorization
   - Mock external services (Firestore, Genkit flows)
   - Test both sync and async functions
   - Use descriptive test names: `test_{{function}}_{{scenario}}`

6. **Report success:**
   - Show test file path
   - Display test count
   - Provide run command: `pytest backend/app/tests/{{module}}/test_{{name}}.py -v`
   - Link to mock patterns in references/

## Test Categories

### Endpoint Tests

```python
# Happy path: Valid request → 200 response
def test_create_user_success(client, monkeypatch):
    mock_firestore = monkeypatch.setattr(...)
    response = client.post("/api/users", json={...})
    assert response.status_code == 200
    assert response.json()["id"]

# Validation error: Invalid input → 422 response
def test_create_user_validation_error(client):
    response = client.post("/api/users", json={"name": ""})
    assert response.status_code == 422

# Permission error: No auth → 401 response
def test_create_user_unauthorized(client):
    response = client.post("/api/users", json={...})
    assert response.status_code == 401

# Not found: Resource missing → 404 response
def test_get_user_not_found(client):
    response = client.get("/api/users/invalid-id")
    assert response.status_code == 404
```

### Service Tests

```python
# Mock Firestore for service tests
@pytest.fixture
def mock_firestore(monkeypatch):
    mock_db = MagicMock()
    monkeypatch.setattr("app.services.firestore_client", mock_db)
    return mock_db

def test_service_with_firestore(mock_firestore):
    mock_firestore.collection.return_value.document.return_value.get.return_value.exists = True
    result = UserService.get_user("user-123")
    assert result is not None
```

### Genkit Flow Tests

```python
# Mock Genkit responses
@pytest.fixture
def mock_genkit(monkeypatch):
    mock_flow = MagicMock()
    monkeypatch.setattr("app.ai.genkit_service.flow", mock_flow)
    return mock_flow

@pytest.mark.ai_services
async def test_genkit_flow_execution(mock_genkit):
    mock_genkit.return_value = {"text": "Generated response"}
    result = await ai_service.generate_content(prompt="test")
    assert "Generated" in result
```

### Async Function Tests

```python
@pytest.mark.asyncio
async def test_async_database_query(client, monkeypatch):
    mock_db = AsyncMock()
    mock_db.get_user.return_value = {"id": "123", "name": "Test"}
    monkeypatch.setattr("app.db.get_user", mock_db)

    result = await fetch_user_profile("123")
    assert result["name"] == "Test"
```

## Fixtures & Mocking

See `references/backend-test-patterns.md` for:

- Firestore mocking patterns
- Firebase Auth mocking
- Genkit flow mocking
- TestClient setup for endpoints
- Async fixture setup
- Pydantic model factories

## Template Files

Templates located in `.claude/skills/pytest-test-scaffolder/templates/`:

- `endpoint.test.py.tpl` - FastAPI endpoint tests
- `service.test.py.tpl` - Service/utility tests
- `async.test.py.tpl` - Async function tests
- `conftest.py.tpl` - Shared fixture template

## Integration with Testing Strategy

- **testing-specialist**: Uses this skill to generate backend tests
- **test-automation-specialist**: Parallelizes backend test generation across modules
- **test-runner**: Executes generated tests via `pytest backend/app/tests/ -v`
- **fullstack-integration-specialist**: Uses alongside api-integration-test-scaffolder

## Coverage Goals

- **Current**: 85% (manual testing)
- **Target**: 95% with scaffolded tests
- **Priority**: Critical path endpoints → service layer → utilities

Run `pytest backend/app/tests/ --cov=app --cov-report=html` to measure coverage.
