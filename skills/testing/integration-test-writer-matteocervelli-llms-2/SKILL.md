---
name: integration-test-writer
description: Generate comprehensive integration tests for component interactions,
  workflows, and system boundaries. Use for testing API endpoints, database operations,
  and multi-component flows.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Integration Test Writer Skill

## Purpose

This skill provides systematic guidance for writing integration tests that verify component interactions, API endpoints, database operations, and end-to-end workflows. Integration tests validate that multiple components work together correctly.

## When to Use

- Test API endpoints and routes
- Verify database interactions
- Test multi-component workflows
- Validate authentication and authorization flows
- Test external service integrations
- Verify error handling across boundaries

## Integration vs Unit Testing

**Unit Tests:**
- Test single component in isolation
- Mock all dependencies
- Fast execution (< 1 second)
- High coverage of edge cases

**Integration Tests:**
- Test multiple components together
- Use real or test doubles (minimal mocking)
- Slower execution (seconds to minutes)
- Focus on component interactions

---

## Integration Testing Workflow

### 1. Identify Integration Points

**Map the system:**
```bash
# Identify components to test together
- API controllers + Services + Database
- Services + External APIs
- Authentication + Authorization + Resources
- Multi-step workflows
```

**Integration test targets:**
- [ ] API endpoints (all HTTP methods)
- [ ] Database CRUD operations
- [ ] Authentication flows
- [ ] Authorization checks
- [ ] External service calls
- [ ] Multi-component workflows
- [ ] Error propagation across boundaries

**Deliverable:** Integration test plan

---

### 2. Setup Test Environment

**Test environment components:**

1. **Test Database:**
   - Separate database for testing
   - Reset between tests
   - Seed data for tests

2. **Test Configuration:**
   - Override production settings
   - Use test credentials
   - Mock external services

3. **Test Fixtures:**
   - Factory functions for test data
   - Reusable setup/teardown
   - Consistent test state

**Python example (pytest + FastAPI):**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.database import Base, get_db
from src.models import User, Resource

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Session:
    """
    Database fixture with setup and teardown.

    Yields:
        Database session for testing

    Notes:
        - Creates all tables before test
        - Drops all tables after test
        - Each test gets fresh database
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session) -> TestClient:
    """
    Test client with database dependency override.

    Args:
        db: Database session fixture

    Returns:
        FastAPI TestClient configured for testing
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """
    Create test user in database.

    Args:
        db: Database session

    Returns:
        Created user instance
    """
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(client: TestClient, test_user: User) -> str:
    """
    Generate authentication token for test user.

    Args:
        client: Test client
        test_user: Test user fixture

    Returns:
        JWT authentication token
    """
    response = client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "password"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """
    Generate authorization headers with token.

    Args:
        auth_token: JWT token

    Returns:
        Headers dictionary with Authorization header
    """
    return {"Authorization": f"Bearer {auth_token}"}
```

**JavaScript/TypeScript example (Jest + Express):**

```typescript
// tests/setup.ts
import { Express } from 'express';
import request from 'supertest';
import { createApp } from '../src/app';
import { setupTestDatabase, teardownTestDatabase } from './helpers/database';

let app: Express;

beforeAll(async () => {
  await setupTestDatabase();
  app = createApp();
});

afterAll(async () => {
  await teardownTestDatabase();
});

beforeEach(async () => {
  // Clean database before each test
  await clearDatabase();
});

export const getTestApp = () => app;

// tests/helpers/database.ts
import { DataSource } from 'typeorm';

let testDataSource: DataSource;

export async function setupTestDatabase() {
  testDataSource = new DataSource({
    type: 'sqlite',
    database: ':memory:',
    entities: ['src/entities/**/*.ts'],
    synchronize: true,
  });

  await testDataSource.initialize();
}

export async function teardownTestDatabase() {
  await testDataSource.destroy();
}

export async function clearDatabase() {
  const entities = testDataSource.entityMetadatas;
  for (const entity of entities) {
    const repository = testDataSource.getRepository(entity.name);
    await repository.clear();
  }
}
```

**Deliverable:** Test environment configured

---

### 3. Write API Integration Tests

**Test structure for API endpoints:**

```python
# tests/integration/test_users_api.py
"""
Integration tests for Users API.

Tests cover:
- CRUD operations
- Authentication and authorization
- Validation and error handling
- Database interactions
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models import User


class TestUsersAPI:
    """Tests for /api/users endpoints."""

    def test_get_users_returns_list(self, client: TestClient, db: Session):
        """Test GET /api/users returns list of users."""
        # Arrange: Create test users
        users = [
            User(name=f"User {i}", email=f"user{i}@example.com")
            for i in range(3)
        ]
        db.add_all(users)
        db.commit()

        # Act
        response = client.get("/api/users")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in user for user in data)
        assert all("name" in user for user in data)

    def test_get_user_by_id_returns_user(
        self, client: TestClient, test_user: User
    ):
        """Test GET /api/users/:id returns specific user."""
        # Act
        response = client.get(f"/api/users/{test_user.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["name"] == test_user.name
        assert data["email"] == test_user.email

    def test_get_user_nonexistent_returns_404(self, client: TestClient):
        """Test GET /api/users/:id with invalid ID returns 404."""
        # Act
        response = client.get("/api/users/99999")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_create_user_returns_created(
        self, client: TestClient, db: Session
    ):
        """Test POST /api/users creates new user."""
        # Arrange
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "SecurePass123"
        }

        # Act
        response = client.post("/api/users", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password not returned

        # Verify in database
        user = db.query(User).filter_by(email=user_data["email"]).first()
        assert user is not None
        assert user.name == user_data["name"]

    def test_create_user_duplicate_email_returns_400(
        self, client: TestClient, test_user: User
    ):
        """Test POST /api/users with duplicate email returns 400."""
        # Arrange
        duplicate_data = {
            "name": "Another User",
            "email": test_user.email,
            "password": "password"
        }

        # Act
        response = client.post("/api/users", json=duplicate_data)

        # Assert
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_create_user_invalid_email_returns_400(self, client: TestClient):
        """Test POST /api/users with invalid email returns 400."""
        # Arrange
        invalid_data = {
            "name": "User",
            "email": "not-an-email",
            "password": "password"
        }

        # Act
        response = client.post("/api/users", json=invalid_data)

        # Assert
        assert response.status_code == 400

    def test_update_user_returns_updated(
        self, client: TestClient, test_user: User, auth_headers: dict, db: Session
    ):
        """Test PUT /api/users/:id updates user."""
        # Arrange
        update_data = {"name": "Updated Name"}

        # Act
        response = client.put(
            f"/api/users/{test_user.id}",
            json=update_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

        # Verify in database
        db.refresh(test_user)
        assert test_user.name == "Updated Name"

    def test_update_user_without_auth_returns_401(
        self, client: TestClient, test_user: User
    ):
        """Test PUT /api/users/:id without auth returns 401."""
        # Arrange
        update_data = {"name": "Updated Name"}

        # Act
        response = client.put(
            f"/api/users/{test_user.id}",
            json=update_data
        )

        # Assert
        assert response.status_code == 401

    def test_delete_user_returns_no_content(
        self, client: TestClient, test_user: User, auth_headers: dict, db: Session
    ):
        """Test DELETE /api/users/:id deletes user."""
        # Act
        response = client.delete(
            f"/api/users/{test_user.id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 204

        # Verify in database
        deleted_user = db.query(User).filter_by(id=test_user.id).first()
        assert deleted_user is None
```

**Deliverable:** API integration tests

---

### 4. Write Database Integration Tests

**Test database operations:**

```python
# tests/integration/test_user_repository.py
"""
Integration tests for User repository database operations.
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models import User
from src.repositories import UserRepository


class TestUserRepository:
    """Tests for UserRepository database operations."""

    @pytest.fixture
    def repository(self, db: Session) -> UserRepository:
        """Create repository instance."""
        return UserRepository(db)

    def test_create_user_saves_to_database(
        self, repository: UserRepository, db: Session
    ):
        """Test create saves user to database."""
        # Arrange
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password"
        }

        # Act
        user = repository.create(user_data)

        # Assert
        assert user.id is not None

        # Verify in database
        saved_user = db.query(User).filter_by(id=user.id).first()
        assert saved_user is not None
        assert saved_user.name == user_data["name"]

    def test_create_duplicate_email_raises_error(
        self, repository: UserRepository
    ):
        """Test creating user with duplicate email raises error."""
        # Arrange
        user_data = {"name": "User", "email": "test@example.com"}
        repository.create(user_data)

        # Act & Assert
        with pytest.raises(IntegrityError):
            repository.create(user_data)

    def test_find_by_id_returns_user(
        self, repository: UserRepository, test_user: User
    ):
        """Test find_by_id returns correct user."""
        # Act
        user = repository.find_by_id(test_user.id)

        # Assert
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_find_by_email_returns_user(
        self, repository: UserRepository, test_user: User
    ):
        """Test find_by_email returns correct user."""
        # Act
        user = repository.find_by_email(test_user.email)

        # Assert
        assert user is not None
        assert user.id == test_user.id

    def test_update_modifies_user(
        self, repository: UserRepository, test_user: User, db: Session
    ):
        """Test update modifies user in database."""
        # Arrange
        update_data = {"name": "Updated Name"}

        # Act
        updated_user = repository.update(test_user.id, update_data)

        # Assert
        assert updated_user.name == "Updated Name"

        # Verify in database
        db.refresh(test_user)
        assert test_user.name == "Updated Name"

    def test_delete_removes_user(
        self, repository: UserRepository, test_user: User, db: Session
    ):
        """Test delete removes user from database."""
        # Act
        repository.delete(test_user.id)

        # Assert - Verify removed from database
        deleted_user = db.query(User).filter_by(id=test_user.id).first()
        assert deleted_user is None
```

**Deliverable:** Database integration tests

---

### 5. Write Multi-Component Workflow Tests

**Test end-to-end workflows:**

```python
# tests/integration/test_user_workflows.py
"""
Integration tests for user-related workflows.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models import User, EmailVerification


class TestUserRegistrationWorkflow:
    """Tests for complete user registration workflow."""

    def test_complete_registration_flow(
        self, client: TestClient, db: Session
    ):
        """Test complete user registration and verification flow."""
        # Step 1: Register new user
        register_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "SecurePass123"
        }
        response = client.post("/api/register", json=register_data)

        assert response.status_code == 201
        user_data = response.json()
        user_id = user_data["id"]
        assert user_data["email_verified"] is False

        # Step 2: Verify email verification record created
        verification = db.query(EmailVerification).filter_by(
            user_id=user_id
        ).first()
        assert verification is not None
        assert verification.is_used is False

        # Step 3: Verify email with token
        verify_response = client.post(
            "/api/verify-email",
            json={"token": verification.token}
        )
        assert verify_response.status_code == 200

        # Step 4: Verify user is now verified
        user = db.query(User).filter_by(id=user_id).first()
        assert user.email_verified is True

        # Step 5: Verify can login
        login_response = client.post(
            "/api/login",
            json={
                "email": register_data["email"],
                "password": register_data["password"]
            }
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        # Step 6: Access protected resource with token
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = client.get("/api/profile", headers=headers)

        assert profile_response.status_code == 200
        profile = profile_response.json()
        assert profile["email"] == register_data["email"]
        assert profile["email_verified"] is True
```

**Deliverable:** Workflow integration tests

---

### 6. Test Authentication & Authorization

**Authentication tests:**

```python
class TestAuthentication:
    """Tests for authentication flows."""

    def test_login_valid_credentials_returns_token(
        self, client: TestClient, test_user: User
    ):
        """Test login with valid credentials returns token."""
        # Arrange
        login_data = {
            "email": test_user.email,
            "password": "password"  # Assuming test_user has this password
        }

        # Act
        response = client.post("/api/login", json=login_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password_returns_401(
        self, client: TestClient, test_user: User
    ):
        """Test login with invalid password returns 401."""
        # Arrange
        login_data = {
            "email": test_user.email,
            "password": "wrong_password"
        }

        # Act
        response = client.post("/api/login", json=login_data)

        # Assert
        assert response.status_code == 401

    def test_protected_endpoint_without_token_returns_401(
        self, client: TestClient
    ):
        """Test protected endpoint without token returns 401."""
        # Act
        response = client.get("/api/profile")

        # Assert
        assert response.status_code == 401

    def test_protected_endpoint_with_valid_token_returns_data(
        self, client: TestClient, auth_headers: dict
    ):
        """Test protected endpoint with valid token returns data."""
        # Act
        response = client.get("/api/profile", headers=auth_headers)

        # Assert
        assert response.status_code == 200


class TestAuthorization:
    """Tests for authorization checks."""

    def test_admin_endpoint_with_admin_user_succeeds(
        self, client: TestClient, admin_user: User, admin_headers: dict
    ):
        """Test admin endpoint allows admin user."""
        # Act
        response = client.get("/api/admin/users", headers=admin_headers)

        # Assert
        assert response.status_code == 200

    def test_admin_endpoint_with_regular_user_returns_403(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test admin endpoint denies regular user."""
        # Act
        response = client.get("/api/admin/users", headers=auth_headers)

        # Assert
        assert response.status_code == 403
```

**Deliverable:** Auth/authz integration tests

---

## Best Practices

1. **Use test database:** Separate from dev/production
2. **Reset state:** Clean database between tests
3. **Test real interactions:** Use actual database, minimal mocking
4. **Test both paths:** Success and error scenarios
5. **Verify side effects:** Check database, logs, notifications
6. **Test security:** Authentication and authorization
7. **Test transactions:** Ensure atomicity and rollback
8. **Keep tests focused:** One workflow or integration per test
9. **Use factories:** Consistent test data creation
10. **Document contracts:** Tests show API usage

---

## Running Integration Tests

```bash
# Python (pytest)
pytest tests/integration/ -v
pytest tests/integration/test_api.py -v
pytest tests/integration/ -v --cov=src

# JavaScript/TypeScript (Jest)
npm run test:integration
jest tests/integration/**/*.test.ts --coverage

# Run with test database
DATABASE_URL=sqlite:///./test.db pytest tests/integration/
```

---

## Quality Checklist

Before completing integration tests:

- [ ] All API endpoints tested
- [ ] CRUD operations verified
- [ ] Authentication tested
- [ ] Authorization tested
- [ ] Error handling validated
- [ ] Database state verified
- [ ] Multi-component workflows tested
- [ ] Tests are isolated and independent
- [ ] Test database separate from dev
- [ ] All tests pass
- [ ] Performance acceptable (< 5 minutes)

---

## Integration with Testing Workflow

**Input:** System components to test together
**Process:** Setup → Test interactions → Verify → Cleanup
**Output:** Integration test suite validating component interactions
**Next Step:** End-to-end testing or deployment

---

## Remember

- **Test component interactions**, not isolated units
- **Use real database** (test instance)
- **Mock only external services** (APIs, third-party)
- **Verify database state** after operations
- **Test authentication and authorization flows**
- **Test both success and error paths**
- **Keep tests isolated** with cleanup between tests
- **Tests should be deterministic** and repeatable