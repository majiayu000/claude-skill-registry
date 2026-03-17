---
name: api-testing
description: Test FastAPI endpoints with pytest and generate API documentation. Use when creating new APIs or verifying existing endpoints work correctly.
allowed-tools: Read, Write, Bash, Glob, Grep
---

You help test FastAPI endpoints for the QA Team Portal backend using pytest and manual testing tools.

## When to Use This Skill

- Testing new API endpoints after creation
- Verifying authentication/authorization works
- Testing CRUD operations
- Checking error handling and validation
- Load/stress testing APIs
- Generating API documentation examples

## Testing Approaches

### 1. Automated Testing with Pytest

#### Unit Tests (Fast, Isolated)

```python
# tests/unit/test_team_service.py
import pytest
from app.services.team_service import TeamService

def test_validate_team_member_data():
    service = TeamService()
    data = {"name": "John Doe", "role": "QA Lead"}
    assert service.validate(data) is True

def test_validate_rejects_invalid_email():
    service = TeamService()
    data = {"name": "John", "email": "invalid"}
    with pytest.raises(ValueError):
        service.validate(data)
```

#### Integration Tests (Full API Flow)

```python
# tests/integration/test_api_team_members.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_team_members():
    response = client.get("/api/v1/team-members")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_team_member_requires_auth():
    data = {"name": "John Doe", "role": "QA Lead"}
    response = client.post("/api/v1/team-members", json=data)
    assert response.status_code == 401

def test_create_team_member_with_auth(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {
        "name": "John Doe",
        "role": "QA Lead",
        "email": "john@example.com"
    }
    response = client.post("/api/v1/team-members", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_update_team_member(admin_token, test_team_member):
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {"name": "Jane Doe"}
    response = client.put(
        f"/api/v1/team-members/{test_team_member.id}",
        json=data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_delete_team_member(admin_token, test_team_member):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(
        f"/api/v1/team-members/{test_team_member.id}",
        headers=headers
    )
    assert response.status_code == 204
```

#### Pytest Fixtures

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.api.deps import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def admin_token(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

@pytest.fixture
def test_team_member(db):
    from app.models.team_member import TeamMember
    member = TeamMember(
        name="Test User",
        role="QA Engineer",
        email="test@test.com"
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member
```

### 2. Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Get all team members (public)
curl http://localhost:8000/api/v1/team-members

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"pass"}' \
  | jq -r '.access_token')

# Create team member (admin)
curl -X POST http://localhost:8000/api/v1/team-members \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "role": "QA Lead",
    "email": "john@example.com"
  }'

# Upload profile photo
curl -X POST http://localhost:8000/api/v1/team-members/123/photo \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@profile.jpg"

# Get with filters
curl "http://localhost:8000/api/v1/team-members?role=QA%20Lead&active=true"
```

### 3. Testing with HTTPie (Prettier Output)

```bash
# Install httpie
pip install httpie

# Login
http POST localhost:8000/api/v1/auth/login email=admin@test.com password=pass

# Create with auth
http POST localhost:8000/api/v1/team-members \
  Authorization:"Bearer $TOKEN" \
  name="John Doe" \
  role="QA Lead" \
  email="john@example.com"

# Pretty print JSON
http GET localhost:8000/api/v1/team-members | jq '.'
```

## Running Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/integration/test_api_team_members.py

# Run specific test
uv run pytest tests/integration/test_api_team_members.py::test_create_team_member

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run only integration tests
uv run pytest tests/integration/

# Show print statements
uv run pytest -s

# Stop on first failure
uv run pytest -x

# Run tests matching pattern
uv run pytest -k "team_member"
```

## Test Coverage

```bash
# Generate coverage report
uv run pytest --cov=app --cov-report=term-missing

# Generate HTML report
uv run pytest --cov=app --cov-report=html
open htmlcov/index.html

# Coverage for specific module
uv run pytest --cov=app.api.v1.endpoints --cov-report=term
```

## Load Testing

```bash
# Install locust
uv pip install locust

# Create locustfile.py
cat > locustfile.py <<'EOF'
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_team_members(self):
        self.client.get("/api/v1/team-members")

    @task(3)
    def get_updates(self):
        self.client.get("/api/v1/updates")
EOF

# Run load test
uv run locust -f locustfile.py --host=http://localhost:8000

# Or headless mode
uv run locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 1m --headless
```

## API Documentation Testing

```bash
# Access interactive docs
open http://localhost:8000/api/v1/docs

# Get OpenAPI schema
curl http://localhost:8000/api/v1/openapi.json | jq '.' > openapi.json

# Validate OpenAPI schema
npx @stoplight/spectral-cli lint openapi.json
```

## Test Checklist

For each endpoint, verify:

- [ ] **Success cases** - Returns 200/201/204 as expected
- [ ] **Authentication** - Returns 401 without token
- [ ] **Authorization** - Returns 403 for insufficient permissions
- [ ] **Validation** - Returns 422 for invalid data
- [ ] **Not Found** - Returns 404 for non-existent resources
- [ ] **Edge cases** - Empty lists, null values, boundary conditions
- [ ] **Error handling** - Doesn't expose sensitive info in errors
- [ ] **Rate limiting** - Enforced on sensitive endpoints
- [ ] **CORS** - Allows configured origins only
- [ ] **Response format** - Matches schema definition

## Common Test Patterns

### Testing Authentication

```python
def test_endpoint_requires_authentication(client):
    response = client.post("/api/v1/admin/users")
    assert response.status_code == 401

def test_endpoint_rejects_expired_token(client, expired_token):
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 401
```

### Testing Validation

```python
def test_rejects_invalid_email(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    data = {"name": "John", "email": "invalid"}
    response = client.post("/api/v1/team-members", json=data, headers=headers)
    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]
```

### Testing Pagination

```python
def test_pagination_limits_results(client):
    response = client.get("/api/v1/team-members?limit=5")
    assert len(response.json()) <= 5

def test_pagination_skip_offset(client):
    response1 = client.get("/api/v1/team-members?skip=0&limit=2")
    response2 = client.get("/api/v1/team-members?skip=2&limit=2")
    assert response1.json()[0]["id"] != response2.json()[0]["id"]
```

## Output Format

After testing, report:

1. **Tests Run**: X passed, Y failed
2. **Coverage**: X% of code covered
3. **Failed Tests**: List with error messages
4. **Performance**: Average response time for key endpoints
5. **Issues Found**: Any bugs or unexpected behavior
6. **Recommendations**: Suggested improvements

## Best Practices

1. **Test pyramid**: More unit tests, fewer integration tests
2. **Independent tests**: Each test should be isolated
3. **Descriptive names**: `test_create_team_member_requires_admin_role`
4. **Use fixtures**: Share test data setup
5. **Test error cases**: Not just happy path
6. **Mock external services**: Don't depend on external APIs
7. **Fast tests**: Keep test suite under 1 minute if possible
