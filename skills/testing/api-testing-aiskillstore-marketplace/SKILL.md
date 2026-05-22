---
name: api-testing
description: |
  Use when writing tests for backend APIs or frontend flows.
  Triggers for: unit tests, integration tests, E2E tests, pytest fixtures,
  TestClient setup, mock data factories, or test coverage analysis.
  NOT for: testing business logic that doesn't involve API endpoints.
---

# API Testing Skill

Expert testing for FastAPI backends and React/Next.js frontends with unit, integration, and E2E test patterns.

## Quick Reference

| Test Type | Tool | Purpose | Scope |
|-----------|------|---------|-------|
| Unit | pytest | Pure functions, services | Isolated |
| Integration | pytest + TestClient | DB + auth + routes | Combined |
| E2E | Playwright/Cypress | Browser flows | Full stack |

## Project Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── test_services.py     # Business logic tests
│   │   └── test_utils.py        # Utility function tests
│   ├── integration/
│   │   ├── test_students.py     # Student API tests
│   │   ├── test_fees.py         # Fee API tests
│   │   └── test_auth.py         # Authentication tests
│   └── fixtures/
│       ├── students.json        # Test data
│       └── users.json
frontend/
├── e2e/
│   ├── specs/
│   │   ├── student.spec.ts
│   │   └── fee.spec.ts
│   ├── pages/
│   │   ├── DashboardPage.ts
│   │   └── StudentPage.ts
│   └── utils/
│       └── test-data.ts
└── playwright.config.ts
```

## Backend: Pytest Setup

### conftest.py (Shared Fixtures)

```python
# backend/tests/conftest.py
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.database import get_db, Base
from app.models import User, Student
from app.auth.jwt import create_access_token
from passlib.context import CryptContext


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("testpassword123")

    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Generate JWT token for test user."""
    return create_access_token(data={"sub": test_user.email, "roles": ["admin"]})


@pytest.fixture
def auth_headers(auth_token):
    """Headers with authentication token."""
    return {"Authorization": f"Bearer {auth_token}"}
```

### Unit Tests (Pure Functions)

```python
# backend/tests/unit/test_services.py
import pytest
from app.services.fee_calculator import calculate_fee, FeeCalculationError


class TestCalculateFee:
    """Unit tests for fee calculation logic."""

    def test_basic_fee_calculation(self):
        """Test basic fee calculation without discounts."""
        result = calculate_fee(
            base_amount=1000.00,
            grade_level=9,
            has_sibling_discount=False,
            is_new_student=False,
        )
        assert result == 1000.00

    def test_sibling_discount(self):
        """Test 10% sibling discount."""
        result = calculate_fee(
            base_amount=1000.00,
            grade_level=9,
            has_sibling_discount=True,
            is_new_student=False,
        )
        assert result == 900.00

    def test_new_student_discount(self):
        """Test 15% new student discount."""
        result = calculate_fee(
            base_amount=1000.00,
            grade_level=9,
            has_sibling_discount=False,
            is_new_student=True,
        )
        assert result == 850.00

    def test_combined_discounts(self):
        """Test combined sibling and new student discounts."""
        result = calculate_fee(
            base_amount=1000.00,
            grade_level=9,
            has_sibling_discount=True,
            is_new_student=True,
        )
        # 10% + 15% = 25% discount
        assert result == 750.00

    def test_invalid_base_amount(self):
        """Test that negative amounts raise error."""
        with pytest.raises(FeeCalculationError):
            calculate_fee(
                base_amount=-100.00,
                grade_level=9,
                has_sibling_discount=False,
                is_new_student=False,
            )

    def test_grade_level_multipliers(self):
        """Test different grade level multipliers."""
        # Elementary (1-5): 1.0x
        assert calculate_fee(1000.00, grade_level=3) == 1000.00
        # Middle (6-8): 1.1x
        assert calculate_fee(1000.00, grade_level=7) == 1100.00
        # High (9-12): 1.2x
        assert calculate_fee(1000.00, grade_level=10) == 1200.00
```

### Integration Tests (API Endpoints)

```python
# backend/tests/integration/test_students.py
import pytest
from fastapi import status


class TestStudentEndpoints:
    """Integration tests for student CRUD endpoints."""

    @pytest.fixture
    def create_student_payload(self):
        """Sample student creation payload."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.edu",
            "date_of_birth": "2008-05-15T00:00:00Z",
            "grade_level": 9,
        }

    def test_create_student_success(self, client, auth_headers, create_student_payload):
        """Test successful student creation."""
        response = client.post(
            "/api/v1/students/",
            json=create_student_payload,
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert "id" in data
        assert data["is_active"] is True

    def test_create_student_unauthorized(self, client, create_student_payload):
        """Test that unauthenticated requests are rejected."""
        response = client.post(
            "/api/v1/students/",
            json=create_student_payload,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_student_invalid_email(self, client, auth_headers, create_student_payload):
        """Test validation error for invalid email."""
        payload = {**create_student_payload, "email": "invalid-email"}
        response = client.post(
            "/api/v1/students/",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_student_missing_required_field(self, client, auth_headers):
        """Test validation error for missing required field."""
        payload = {
            "first_name": "John",
            # Missing last_name, email, date_of_birth, grade_level
        }
        response = client.post(
            "/api/v1/students/",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_student_success(self, client, auth_headers, create_student_payload):
        """Test retrieving a student by ID."""
        # Create student first
        create_response = client.post(
            "/api/v1/students/",
            json=create_student_payload,
            headers=auth_headers,
        )
        student_id = create_response.json()["id"]

        # Retrieve student
        response = client.get(
            f"/api/v1/students/{student_id}",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == student_id

    def test_get_student_not_found(self, client, auth_headers):
        """Test 404 for non-existent student."""
        response = client.get(
            "/api/v1/students/99999",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_students_pagination(self, client, auth_headers, db_session):
        """Test student list with pagination."""
        # Create multiple students
        for i in range(5):
            payload = {
                "first_name": f"Student{i}",
                "last_name": "Test",
                "email": f"student{i}@test.edu",
                "date_of_birth": "2008-05-15T00:00:00Z",
                "grade_level": 9,
            }
            client.post("/api/v1/students/", json=payload, headers=auth_headers)

        # Get first page
        response = client.get(
            "/api/v1/students/?skip=0&limit=3",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["total"] == 5
        assert data["has_more"] is True

    def test_update_student(self, client, auth_headers, create_student_payload):
        """Test partial update of student."""
        # Create student
        create_response = client.post(
            "/api/v1/students/",
            json=create_student_payload,
            headers=auth_headers,
        )
        student_id = create_response.json()["id"]

        # Update student
        update_payload = {"first_name": "Jane", "grade_level": 10}
        response = client.patch(
            f"/api/v1/students/{student_id}",
            json=update_payload,
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["grade_level"] == 10

    def test_delete_student(self, client, auth_headers, create_student_payload):
        """Test soft delete of student."""
        # Create student
        create_response = client.post(
            "/api/v1/students/",
            json=create_student_payload,
            headers=auth_headers,
        )
        student_id = create_response.json()["id"]

        # Delete student
        response = client.delete(
            f"/api/v1/students/{student_id}",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify student is not in active list
        list_response = client.get(
            "/api/v1/students/",
            headers=auth_headers,
        )
        student_ids = [s["id"] for s in list_response.json()["data"]]
        assert student_id not in student_ids
```

### Test Fixtures (JSON Data)

```json
// backend/tests/fixtures/students.json
{
  "valid_student": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@test.edu",
    "date_of_birth": "2008-05-15T00:00:00Z",
    "grade_level": 9
  },
  "invalid_students": [
    {
      "description": "Missing first_name",
      "data": {
        "last_name": "Doe",
        "email": "test@test.edu",
        "date_of_birth": "2008-05-15T00:00:00Z",
        "grade_level": 9
      }
    },
    {
      "description": "Invalid email format",
      "data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "not-an-email",
        "date_of_birth": "2008-05-15T00:00:00Z",
        "grade_level": 9
      }
    },
    {
      "description": "Grade level out of range",
      "data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@test.edu",
        "date_of_birth": "2008-05-15T00:00:00Z",
        "grade_level": 15
      }
    }
  ]
}
```

## Frontend: E2E Tests (Playwright)

### playwright.config.ts

```typescript
// frontend/playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e/specs",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

### E2E Test Specification

```typescript
// frontend/e2e/specs/student.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Student Management", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to login page
    await page.goto("/login");

    // Login as admin
    await page.fill('input[name="email"]', "admin@test.edu");
    await page.fill('input[name="password"]', "adminpassword");
    await page.click('button[type="submit"]');

    // Verify login success
    await expect(page).toHaveURL(/\/dashboard/);
    await expect(page.locator("text=Admin")).toBeVisible();
  });

  test("should create a new student successfully", async ({ page }) => {
    // Navigate to students page
    await page.click('a[href="/students"]');
    await expect(page).toHaveURL(/\/students/);

    // Click add student button
    await page.click('button:has-text("Add Student")');

    // Fill in student form
    await page.fill('input[name="firstName"]', "John");
    await page.fill('input[name="lastName"]', "Doe");
    await page.fill('input[name="email"]', "john.doe@test.edu");
    await page.fill('input[name="dateOfBirth"]', "2008-05-15");

    // Select grade level
    await page.selectOption('select[name="gradeLevel"]', "9");

    // Submit form
    await page.click('button:has-text("Create")');

    // Verify student was created
    await expect(page.locator("text=Student created successfully")).toBeVisible();

    // Verify student appears in list
    await expect(page.locator("text=John Doe")).toBeVisible();
  });

  test("should show validation errors for invalid input", async ({ page }) => {
    await page.click('a[href="/students"]');
    await page.click('button:has-text("Add Student")');

    // Submit empty form
    await page.click('button:has-text("Create")');

    // Verify validation errors
    await expect(page.locator("text=First name is required")).toBeVisible();
    await expect(page.locator("text=Last name is required")).toBeVisible();
    await expect(page.locator("text=Invalid email address")).toBeVisible();
  });

  test("should filter students by grade level", async ({ page }) => {
    await page.click('a[href="/students"]');

    // Filter by grade 9
    await page.selectOption('select[name="gradeFilter"]', "9");
    await page.click('button:has-text("Apply")');

    // Verify only grade 9 students shown
    const rows = page.locator("table.student-list tbody tr");
    await expect(rows).toHaveCount(3); // Assuming 3 grade 9 students
  });

  test("should view student details", async ({ page }) => {
    await page.click('a[href="/students"]');

    // Click on first student
    await page.click('table.student-list tbody tr:first-child a');

    // Verify details page
    await expect(page).toHaveURL(/\/students\/\d+/);
    await expect(page.locator("h1")).toContainText("Student Details");
  });
});
```

### Page Object Model

```typescript
// frontend/e2e/pages/StudentsPage.ts
import { Page, Locator, expect } from "@playwright/test";

export class StudentsPage {
  readonly page: Page;
  readonly addButton: Locator;
  readonly studentTable: Locator;
  readonly gradeFilter: Locator;
  readonly searchInput: Locator;

  constructor(page: Page) {
    this.page = page;
    this.addButton = page.locator('button:has-text("Add Student")');
    this.studentTable = page.locator("table.student-list");
    this.gradeFilter = page.locator('select[name="gradeFilter"]');
    this.searchInput = page.locator('input[name="search"]');
  }

  async goto() {
    await this.page.goto("/students");
  }

  async createStudent(data: {
    firstName: string;
    lastName: string;
    email: string;
    gradeLevel: string;
    dateOfBirth?: string;
  }) {
    await this.addButton.click();
    await this.page.fill('input[name="firstName"]', data.firstName);
    await this.page.fill('input[name="lastName"]', data.lastName);
    await this.page.fill('input[name="email"]', data.email);
    await this.page.selectOption('select[name="gradeLevel"]', data.gradeLevel);
    if (data.dateOfBirth) {
      await this.page.fill('input[name="dateOfBirth"]', data.dateOfBirth);
    }
    await this.page.click('button:has-text("Create")');
  }

  async getStudentNames(): Promise<string[]> {
    const rows = this.studentTable.locator("tbody tr");
    const names: string[] = [];
    for (const row of await rows.all()) {
      names.push(await row.locator("td:first-child").textContent());
    }
    return names;
  }

  async filterByGrade(grade: string) {
    await this.gradeFilter.selectOption(grade);
    await this.page.click('button:has-text("Apply")');
  }

  async searchByName(name: string) {
    await this.searchInput.fill(name);
    await this.page.keyboard.press("Enter");
  }
}
```

## Test Pyramid

```
        /\
       /  \      E2E Tests (10%)
      /    \     - Critical user journeys
     /______\
    /        \
   /          \   Integration Tests (30%)
  /            \  - API endpoints with DB
 /______________\
/                \
/                  \ Unit Tests (60%)
/                    \ - Services, utilities
/______________________\
```

## Quality Checklist

- [ ] **Happy path + edge cases**: Test both success and error scenarios
- [ ] **CI compatible**: Tests run in CI pipeline without manual setup
- [ ] **Deterministic**: No flaky tests, no random failures
- [ ] **Coverage**: 80%+ for core modules, 90%+ for critical paths
- [ ] **No real secrets**: Use test credentials, never production keys
- [ ] **No production DB**: Use test database or in-memory SQLite
- [ ] **Isolated**: Tests don't depend on each other
- [ ] **Fast**: Unit tests < 100ms, integration < 1s

## Running Tests

```bash
# Backend tests
pytest                           # Run all tests
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest -v                       # Verbose output
pytest --cov=app               # With coverage

# Frontend E2E tests
npx playwright install           # Install browsers
npx playwright test             # Run E2E tests
npx playwright test --reporter=line
```

## CI Configuration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npm run test
      - run: npm run build
```

## Integration Points

| Skill | Integration |
|-------|-------------|
| `@sqlmodel-crud` | Test CRUD operations with test database |
| `@jwt-auth` | Test authenticated endpoints with test tokens |
| `@api-route-design` | Test all CRUD routes with various status codes |
| `@error-handling` | Test error responses and edge cases |
| `@data-validation` | Test validation error messages |
