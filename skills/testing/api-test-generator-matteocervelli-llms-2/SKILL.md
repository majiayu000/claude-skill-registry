---
name: api-test-generator
description: Generate comprehensive API endpoint tests for REST and GraphQL APIs.
  Creates tests for all HTTP methods, status codes, authentication, and validation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# API Test Generator Skill

## Purpose

This skill generates comprehensive integration tests for API endpoints, covering all HTTP methods, status codes, authentication, authorization, request/response validation, and error handling.

## When to Use

- Generate tests for REST API endpoints
- Test GraphQL API queries and mutations
- Validate API request/response contracts
- Test API authentication and authorization
- Verify API error handling and status codes

## API Test Coverage

For each endpoint, test:

- ✅ **Success cases** (200, 201, 204)
- ✅ **Validation errors** (400, 422)
- ✅ **Authentication errors** (401)
- ✅ **Authorization errors** (403)
- ✅ **Not found errors** (404)
- ✅ **Conflict errors** (409)
- ✅ **Server errors** (500)
- ✅ **Request body validation**
- ✅ **Query parameter validation**
- ✅ **Response schema validation**

---

## API Test Generation Workflow

### 1. Analyze API Routes

**Identify endpoints:**

```bash
# Read route definitions
cat src/routes/users.py
cat src/controllers/user_controller.py

# Identify:
# - Endpoints and HTTP methods
# - Path parameters
# - Query parameters
# - Request body schemas
# - Response schemas
# - Authentication requirements
# - Authorization requirements
```

**Map endpoints:**

```
GET    /api/users              - List users (public)
GET    /api/users/:id          - Get user (public)
POST   /api/users              - Create user (admin only)
PUT    /api/users/:id          - Update user (auth required, owner or admin)
DELETE /api/users/:id          - Delete user (auth required, owner or admin)
```

**Deliverable:** API endpoint inventory

---

### 2. Generate REST API Test Suite

**Test file structure:**

```python
"""
Integration tests for Users API endpoints.

Endpoints tested:
- GET    /api/users
- GET    /api/users/:id
- POST   /api/users
- PUT    /api/users/:id
- PATCH  /api/users/:id
- DELETE /api/users/:id
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models import User


# ============================================================================
# GET /api/users - List Users
# ============================================================================

class TestGetUsers:
    """Tests for GET /api/users endpoint."""

    def test_get_users_empty_returns_empty_list(self, client: TestClient):
        """Test GET /api/users with no users returns empty list."""
        # Act
        response = client.get("/api/users")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_get_users_returns_user_list(
        self, client: TestClient, db: Session
    ):
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
        assert all("email" in user for user in data)

    def test_get_users_with_pagination(
        self, client: TestClient, db: Session
    ):
        """Test GET /api/users with pagination parameters."""
        # Arrange: Create 10 users
        users = [
            User(name=f"User {i}", email=f"user{i}@example.com")
            for i in range(10)
        ]
        db.add_all(users)
        db.commit()

        # Act
        response = client.get("/api/users?limit=5&offset=0")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_users_with_search_filter(
        self, client: TestClient, db: Session
    ):
        """Test GET /api/users with search query."""
        # Arrange
        users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
            User(name="Alice Smith", email="asmith@example.com"),
        ]
        db.add_all(users)
        db.commit()

        # Act
        response = client.get("/api/users?search=alice")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("alice" in user["name"].lower() for user in data)

    def test_get_users_invalid_limit_returns_400(self, client: TestClient):
        """Test GET /api/users with invalid limit parameter."""
        # Act
        response = client.get("/api/users?limit=-1")

        # Assert
        assert response.status_code == 400
        assert "limit" in response.json()["detail"].lower()


# ============================================================================
# GET /api/users/:id - Get User by ID
# ============================================================================

class TestGetUserById:
    """Tests for GET /api/users/:id endpoint."""

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
        assert "password" not in data  # Sensitive data not included

    def test_get_user_nonexistent_id_returns_404(self, client: TestClient):
        """Test GET /api/users/:id with nonexistent ID returns 404."""
        # Act
        response = client.get("/api/users/99999")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_user_invalid_id_format_returns_400(self, client: TestClient):
        """Test GET /api/users/:id with invalid ID format returns 400."""
        # Act
        response = client.get("/api/users/invalid-id")

        # Assert
        assert response.status_code == 400


# ============================================================================
# POST /api/users - Create User
# ============================================================================

class TestCreateUser:
    """Tests for POST /api/users endpoint."""

    def test_create_user_valid_data_returns_created(
        self, client: TestClient, db: Session, admin_headers: dict
    ):
        """Test POST /api/users with valid data creates user."""
        # Arrange
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "SecurePass123"
        }

        # Act
        response = client.post(
            "/api/users",
            json=user_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password not returned
        assert "created_at" in data

        # Verify in database
        user = db.query(User).filter_by(email=user_data["email"]).first()
        assert user is not None
        assert user.name == user_data["name"]

    def test_create_user_missing_required_field_returns_400(
        self, client: TestClient, admin_headers: dict
    ):
        """Test POST /api/users with missing required field returns 400."""
        # Arrange: Missing email
        invalid_data = {
            "name": "User",
            "password": "password"
        }

        # Act
        response = client.post(
            "/api/users",
            json=invalid_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_create_user_invalid_email_returns_400(
        self, client: TestClient, admin_headers: dict
    ):
        """Test POST /api/users with invalid email format returns 400."""
        # Arrange
        invalid_data = {
            "name": "User",
            "email": "not-an-email",
            "password": "password"
        }

        # Act
        response = client.post(
            "/api/users",
            json=invalid_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

    def test_create_user_weak_password_returns_400(
        self, client: TestClient, admin_headers: dict
    ):
        """Test POST /api/users with weak password returns 400."""
        # Arrange
        invalid_data = {
            "name": "User",
            "email": "user@example.com",
            "password": "123"  # Too short
        }

        # Act
        response = client.post(
            "/api/users",
            json=invalid_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 400
        assert "password" in response.json()["detail"].lower()

    def test_create_user_duplicate_email_returns_409(
        self, client: TestClient, test_user: User, admin_headers: dict
    ):
        """Test POST /api/users with duplicate email returns 409."""
        # Arrange
        duplicate_data = {
            "name": "Another User",
            "email": test_user.email,  # Duplicate
            "password": "password"
        }

        # Act
        response = client.post(
            "/api/users",
            json=duplicate_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_without_auth_returns_401(
        self, client: TestClient
    ):
        """Test POST /api/users without authentication returns 401."""
        # Arrange
        user_data = {
            "name": "User",
            "email": "user@example.com",
            "password": "password"
        }

        # Act
        response = client.post("/api/users", json=user_data)

        # Assert
        assert response.status_code == 401

    def test_create_user_as_non_admin_returns_403(
        self, client: TestClient, auth_headers: dict
    ):
        """Test POST /api/users as non-admin user returns 403."""
        # Arrange
        user_data = {
            "name": "User",
            "email": "user@example.com",
            "password": "password"
        }

        # Act
        response = client.post(
            "/api/users",
            json=user_data,
            headers=auth_headers  # Regular user, not admin
        )

        # Assert
        assert response.status_code == 403


# ============================================================================
# PUT /api/users/:id - Update User (Full Replace)
# ============================================================================

class TestUpdateUser:
    """Tests for PUT /api/users/:id endpoint."""

    def test_update_user_own_account_returns_updated(
        self, client: TestClient, test_user: User, auth_headers: dict, db: Session
    ):
        """Test PUT /api/users/:id to update own account."""
        # Arrange
        update_data = {
            "name": "Updated Name",
            "email": test_user.email  # Same email
        }

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

    def test_update_user_other_account_as_admin_succeeds(
        self, client: TestClient, test_user: User, admin_headers: dict, db: Session
    ):
        """Test PUT /api/users/:id as admin to update other user."""
        # Arrange
        update_data = {
            "name": "Admin Updated",
            "email": test_user.email
        }

        # Act
        response = client.put(
            f"/api/users/{test_user.id}",
            json=update_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 200

    def test_update_user_other_account_as_regular_user_returns_403(
        self, client: TestClient, db: Session, auth_headers: dict
    ):
        """Test PUT /api/users/:id to update other user returns 403."""
        # Arrange: Create another user
        other_user = User(name="Other", email="other@example.com")
        db.add(other_user)
        db.commit()

        update_data = {"name": "Unauthorized Update"}

        # Act
        response = client.put(
            f"/api/users/{other_user.id}",
            json=update_data,
            headers=auth_headers  # Regular user, not admin
        )

        # Assert
        assert response.status_code == 403

    def test_update_user_nonexistent_returns_404(
        self, client: TestClient, admin_headers: dict
    ):
        """Test PUT /api/users/:id with nonexistent ID returns 404."""
        # Arrange
        update_data = {"name": "Updated"}

        # Act
        response = client.put(
            "/api/users/99999",
            json=update_data,
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 404


# ============================================================================
# PATCH /api/users/:id - Partial Update User
# ============================================================================

class TestPatchUser:
    """Tests for PATCH /api/users/:id endpoint."""

    def test_patch_user_single_field_updates(
        self, client: TestClient, test_user: User, auth_headers: dict, db: Session
    ):
        """Test PATCH /api/users/:id updates only specified field."""
        # Arrange
        original_email = test_user.email
        patch_data = {"name": "Patched Name"}

        # Act
        response = client.patch(
            f"/api/users/{test_user.id}",
            json=patch_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Patched Name"
        assert data["email"] == original_email  # Unchanged

        # Verify in database
        db.refresh(test_user)
        assert test_user.name == "Patched Name"
        assert test_user.email == original_email


# ============================================================================
# DELETE /api/users/:id - Delete User
# ============================================================================

class TestDeleteUser:
    """Tests for DELETE /api/users/:id endpoint."""

    def test_delete_user_own_account_returns_no_content(
        self, client: TestClient, test_user: User, auth_headers: dict, db: Session
    ):
        """Test DELETE /api/users/:id to delete own account."""
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

    def test_delete_user_as_admin_succeeds(
        self, client: TestClient, test_user: User, admin_headers: dict, db: Session
    ):
        """Test DELETE /api/users/:id as admin."""
        # Act
        response = client.delete(
            f"/api/users/{test_user.id}",
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 204

    def test_delete_user_other_account_returns_403(
        self, client: TestClient, db: Session, auth_headers: dict
    ):
        """Test DELETE /api/users/:id to delete other user returns 403."""
        # Arrange
        other_user = User(name="Other", email="other@example.com")
        db.add(other_user)
        db.commit()

        # Act
        response = client.delete(
            f"/api/users/{other_user.id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 403

    def test_delete_user_without_auth_returns_401(
        self, client: TestClient, test_user: User
    ):
        """Test DELETE /api/users/:id without auth returns 401."""
        # Act
        response = client.delete(f"/api/users/{test_user.id}")

        # Assert
        assert response.status_code == 401

    def test_delete_user_nonexistent_returns_404(
        self, client: TestClient, admin_headers: dict
    ):
        """Test DELETE /api/users/:id with nonexistent ID returns 404."""
        # Act
        response = client.delete(
            "/api/users/99999",
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 404
```

**Deliverable:** Comprehensive REST API tests

---

### 3. Generate GraphQL API Tests

**GraphQL test structure:**

```python
"""
Integration tests for GraphQL API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestGraphQLQueries:
    """Tests for GraphQL queries."""

    def test_query_users_returns_list(
        self, client: TestClient, db: Session
    ):
        """Test users query returns list."""
        # Arrange
        create_test_users(db, count=3)

        query = """
        query {
            users {
                id
                name
                email
            }
        }
        """

        # Act
        response = client.post("/graphql", json={"query": query})

        # Assert
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data["users"]) == 3

    def test_query_user_by_id_returns_user(
        self, client: TestClient, test_user: User
    ):
        """Test user query by ID returns specific user."""
        # Arrange
        query = f"""
        query {{
            user(id: {test_user.id}) {{
                id
                name
                email
            }}
        }}
        """

        # Act
        response = client.post("/graphql", json={"query": query})

        # Assert
        assert response.status_code == 200
        data = response.json()["data"]["user"]
        assert data["id"] == test_user.id
        assert data["name"] == test_user.name


class TestGraphQLMutations:
    """Tests for GraphQL mutations."""

    def test_create_user_mutation_creates_user(
        self, client: TestClient, db: Session, admin_headers: dict
    ):
        """Test createUser mutation creates new user."""
        # Arrange
        mutation = """
        mutation {
            createUser(input: {
                name: "New User",
                email: "newuser@example.com",
                password: "SecurePass123"
            }) {
                user {
                    id
                    name
                    email
                }
            }
        }
        """

        # Act
        response = client.post(
            "/graphql",
            json={"query": mutation},
            headers=admin_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()["data"]["createUser"]["user"]
        assert data["name"] == "New User"
        assert data["email"] == "newuser@example.com"

        # Verify in database
        user = db.query(User).filter_by(email="newuser@example.com").first()
        assert user is not None
```

**Deliverable:** GraphQL API tests

---

## HTTP Status Code Testing

**Test all relevant status codes:**

```python
# 200 OK - Successful GET/PUT/PATCH
def test_returns_200_on_success(client):
    response = client.get("/api/resource")
    assert response.status_code == 200

# 201 Created - Successful POST
def test_returns_201_on_create(client):
    response = client.post("/api/resource", json=data)
    assert response.status_code == 201

# 204 No Content - Successful DELETE
def test_returns_204_on_delete(client):
    response = client.delete("/api/resource/1")
    assert response.status_code == 204

# 400 Bad Request - Validation error
def test_returns_400_on_invalid_input(client):
    response = client.post("/api/resource", json=invalid_data)
    assert response.status_code == 400

# 401 Unauthorized - Missing/invalid auth
def test_returns_401_without_auth(client):
    response = client.get("/api/protected")
    assert response.status_code == 401

# 403 Forbidden - Insufficient permissions
def test_returns_403_without_permission(client, user_token):
    response = client.delete("/api/admin/resource", headers=user_token)
    assert response.status_code == 403

# 404 Not Found - Resource doesn't exist
def test_returns_404_for_nonexistent(client):
    response = client.get("/api/resource/99999")
    assert response.status_code == 404

# 409 Conflict - Duplicate resource
def test_returns_409_on_duplicate(client):
    response = client.post("/api/resource", json=existing_data)
    assert response.status_code == 409

# 422 Unprocessable Entity - Semantic error
def test_returns_422_on_semantic_error(client):
    response = client.post("/api/resource", json=invalid_semantic_data)
    assert response.status_code == 422

# 500 Internal Server Error - Server error
def test_returns_500_on_server_error(client, mock_error):
    response = client.get("/api/resource")
    assert response.status_code == 500
```

---

## Best Practices

1. **Test all HTTP methods:** GET, POST, PUT, PATCH, DELETE
2. **Test all status codes:** Success and error responses
3. **Validate request bodies:** Required fields, formats, constraints
4. **Validate response bodies:** Schema, fields, data types
5. **Test authentication:** With/without tokens, expired tokens
6. **Test authorization:** Different user roles and permissions
7. **Test edge cases:** Empty lists, null values, max limits
8. **Verify database state:** Check data persisted correctly
9. **Use descriptive test names:** Clearly state what's being tested
10. **Group by endpoint:** Organize tests by API endpoint

---

## Quality Checklist

Before completing API tests:

- [ ] All endpoints tested
- [ ] All HTTP methods tested
- [ ] Success cases (200, 201, 204) covered
- [ ] Error cases (400, 401, 403, 404, 409) covered
- [ ] Request validation tested
- [ ] Response schema validated
- [ ] Authentication tested
- [ ] Authorization tested
- [ ] Edge cases covered
- [ ] Database state verified
- [ ] All tests pass
- [ ] Tests are independent

---

## Integration with Testing Workflow

**Input:** API routes and endpoints
**Process:** Analyze → Generate tests → Run & verify
**Output:** Comprehensive API test suite
**Next Step:** API documentation or deployment

---

## Remember

- **Test all endpoints** and HTTP methods
- **Test success and error cases**
- **Validate request and response schemas**
- **Test authentication and authorization**
- **Verify database state** after operations
- **Use appropriate status codes**
- **Keep tests focused** on one scenario
- **Tests serve as API documentation**