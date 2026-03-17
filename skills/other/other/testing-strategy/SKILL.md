---
name: testing-strategy
description: Comprehensive testing strategies and coverage standards. Use when testing strategy guidance is required.
---
## Purpose

Provide comprehensive testing strategies and coverage standards that can be applied across services, including thresholds, critical path tests, and environment setup.

## IO Semantics

Input: Test suites, coverage reports, and service architectures that require structured testing guidance.

Output: Concrete coverage targets, configuration examples, and critical path testing patterns that can be enforced in CI.

Side Effects: Raising coverage thresholds or enforcing new critical paths may require additional tests and refactoring.

## Deterministic Steps

### 1. Coverage Requirements Enforcement

Apply mandatory coverage thresholds:
- Overall code coverage: ≥ 80%
- Critical business logic coverage: ≥ 95%
- Security-related code coverage: ≥ 90%
- New feature coverage: ≥ 85% before merge

Apply coverage configuration examples:
```yaml
# .pytest.ini for Python
[tool:pytest]
addopts =
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
    --cov-branch
    --cov-context=test

# Go coverage configuration
# Makefile
.PHONY: test test-coverage
test:
	go test -v ./...

test-coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	go tool cover -func=coverage.out | grep "total:" | awk '{print $3}' | sed 's/%//' | \
		awk '{if ($1 < 80) {print "Coverage below 80%: " $1 "%"; exit 1} else {print "Coverage: " $1 "%"}}'
```

### 2. Critical Path Testing

Identify and prioritize critical paths:
```python
# test_critical_paths.py
import pytest
from unittest.mock import Mock, patch
from app.payment import PaymentProcessor
from app.user_management import UserService

class TestCriticalPaths:
    def test_payment_processing_complete_flow(self):
        """Test complete payment flow with real dependencies"""
        processor = PaymentProcessor()

        # Test successful payment
        result = processor.process_payment(
            user_id=123,
            amount=100.00,
            payment_method="credit_card"
        )

        assert result.success is True
        assert result.transaction_id is not None
        assert result.amount == 100.00

    def test_user_registration_with_validation(self):
        """Test user registration with all validation rules"""
        user_service = UserService()

        # Test valid registration
        user = user_service.register_user(
            email="test@example.com",
            password="SecurePass123!",
            name="Test User"
        )

        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.id is not None

    @pytest.mark.parametrize("status_code,expected_result", [
        (200, {"status": "success"}),
        (400, {"status": "error", "message": "Invalid request"}),
        (500, {"status": "error", "message": "Internal server error"})
    ])
    def test_api_endpoint_error_handling(self, status_code, expected_result):
        """Test API error handling scenarios"""
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = status_code
            mock_post.return_value.json.return_value = expected_result

            response = self.client.call_external_api({"data": "test"})

            assert response == expected_result
```

## Testing Framework Configuration

### Multi-Language Testing Setup

Python Testing Configuration:
```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80"
]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow running tests",
    "network: Tests requiring network access",
    "database: Tests requiring database"
]
```

Go Testing Configuration:
```go
// testing_setup.go
package testsetup

import (
	"testing"
	"time"
)

// Test configuration
type TestConfig struct {
	DatabaseURL string
	RedisURL    string
	Timeout     time.Duration
}

// Global test configuration
var Config TestConfig

func TestMain(m *testing.M) {
	// Setup test environment
	setupTestEnvironment()

	// Run tests
	code := m.Run()

	// Cleanup
	cleanupTestEnvironment()

	os.Exit(code)
}

func setupTestEnvironment() {
	Config = TestConfig{
		DatabaseURL: "postgres://test:test@localhost:5432/testdb?sslmode=disable",
		RedisURL:    "redis://localhost:6379/1",
		Timeout:     30 * time.Second,
	}

	// Wait for services to be ready
	waitForServices()
}
```

## Test Quality Assurance

### AAA Pattern Implementation

Apply Arrange-Act-Assert consistently:
```python
import pytest
from calculator import Calculator

class TestCalculator:
    def test_addition_positive_numbers(self):
        # Arrange
        calculator = Calculator()
        operand_a = 5
        operand_b = 3

        # Act
        result = calculator.add(operand_a, operand_b)

        # Assert
        assert result == 8
        assert isinstance(result, (int, float))

    def test_division_by_zero_raises_error(self):
        # Arrange
        calculator = Calculator()
        dividend = 10
        divisor = 0

        # Act & Assert
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calculator.divide(dividend, divisor)

    def test_complex_calculation_chain(self):
        # Arrange
        calculator = Calculator()
        initial_value = 10

        # Act
        result = (calculator
                  .add(initial_value, 5)
                  .multiply(2)
                  .subtract(3)
                  .divide(4))

        # Assert
        assert result == 5.5
```

### Test Isolation and Independence

Ensure tests run independently:
```python
import pytest
import tempfile
import shutil
from pathlib import Path

class TestFileOperations:
    @pytest.fixture
    def temp_directory(self):
        """Create isolated temporary directory for each test"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_file_creation_and_read(self, temp_directory):
        """Test file operations in isolated environment"""
        test_file = temp_directory / "test.txt"
        test_content = "Hello, World!"

        # Act
        test_file.write_text(test_content)
        read_content = test_file.read_text()

        # Assert
        assert read_content == test_content
        assert test_file.exists()

    def test_file_operations_persistence(self, temp_directory):
        """This test uses different temp_directory, ensuring isolation"""
        # This test cannot interfere with previous test due to separate temp_directory
        another_file = temp_directory / "another.txt"
        another_file.write_text("Different content")

        assert another_file.read_text() == "Different content"
```

## Performance and Load Testing

### Load Testing Implementation

Automated performance validation:
```python
import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from app.api_server import app

class TestPerformance:
    @pytest.mark.slow
    def test_api_response_time_under_load(self):
        """Test API response time under concurrent load"""
        url = "http://localhost:8000/api/test"
        concurrent_requests = 50
        max_response_time = 1.0  # seconds

        def make_request():
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            return end_time - start_time, response.status_code

        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(concurrent_requests)]
            results = [future.result() for future in futures]

        # Assert all requests succeeded
        status_codes = [result[1] for result in results]
        assert all(code == 200 for code in status_codes)

        # Assert response times are within limits
        response_times = [result[0] for result in results]
        assert max(response_times) < max_response_time
        assert sum(response_times) / len(response_times) < max_response_time * 0.8

    @pytest.mark.performance
    def test_memory_usage_stability(self):
        """Test memory usage remains stable during extended operation"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Perform many operations
        for _ in range(1000):
            self.heavy_operation()

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase is minimal (< 10MB)
        assert memory_increase < 10 * 1024 * 1024, f"Memory increased by {memory_increase} bytes"

    def heavy_operation(self):
        """Simulate memory-intensive operation"""
        data = list(range(1000))
        processed_data = [x * 2 for x in data]
        return sum(processed_data)
```

## Integration and E2E Testing

### Integration Test Architecture

Comprehensive integration testing:
```python
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from app.database import DatabaseConnection
from app.cache import RedisCache

@pytest.mark.integration
class TestDatabaseIntegration:
    @pytest.fixture(scope="class")
    def postgres_container(self):
        """Start PostgreSQL container for integration tests"""
        with PostgresContainer("postgres:15-alpine") as postgres:
            yield postgres

    @pytest.fixture(scope="class")
    def redis_container(self):
        """Start Redis container for integration tests"""
        with RedisContainer("redis:7-alpine") as redis:
            yield redis

    @pytest.fixture(scope="class")
    def database(self, postgres_container):
        """Configure database connection with test container"""
        db = DatabaseConnection(
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(5432),
            database="test",
            user="test",
            password="test"
        )
        db.create_tables()
        yield db
        db.close()

    def test_user_creation_and_retrieval(self, database):
        """Test complete user creation and retrieval flow"""
        user_data = {
            "email": "test@example.com",
            "name": "Test User"
        }

        # Create user
        user_id = database.create_user(user_data)
        assert user_id is not None

        # Retrieve user
        retrieved_user = database.get_user(user_id)
        assert retrieved_user["email"] == user_data["email"]
        assert retrieved_user["name"] == user_data["name"]

    def test_transaction_rollback(self, database):
        """Test transaction rollback on error"""
        initial_count = database.count_users()

        with pytest.raises(ValueError):
            with database.transaction():
                database.create_user({"email": "good@example.com", "name": "Good User"})
                raise ValueError("Simulated error")

        # Ensure no user was created due to rollback
        final_count = database.count_users()
        assert final_count == initial_count
```

### End-to-End Testing

Full application workflow testing:
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
class TestUserWorkflows:
    @pytest.fixture
    def browser(self):
        """Setup browser for E2E tests"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

        yield driver

        driver.quit()

    def test_complete_user_registration_flow(self, browser):
        """Test complete user registration from UI"""
        # Navigate to registration page
        browser.get("http://localhost:3000/register")

        # Fill registration form
        browser.find_element(By.ID, "email").send_keys("test@example.com")
        browser.find_element(By.ID, "password").send_keys("SecurePass123!")
        browser.find_element(By.ID, "confirm_password").send_keys("SecurePass123!")
        browser.find_element(By.ID, "name").send_keys("Test User")

        # Submit form
        browser.find_element(By.ID, "register-button").click()

        # Verify successful registration
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )

        # Verify redirect to dashboard
        assert "dashboard" in browser.current_url

    def test_login_with_registered_user(self, browser):
        """Test login with previously registered user"""
        # First register a user
        self.register_test_user(browser)

        # Navigate to login page
        browser.get("http://localhost:3000/login")

        # Fill login form
        browser.find_element(By.ID, "email").send_keys("test@example.com")
        browser.find_element(By.ID, "password").send_keys("SecurePass123!")
        browser.find_element(By.ID, "login-button").click()

        # Verify successful login
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-dashboard"))
        )

    def register_test_user(self, browser):
        """Helper method to register test user"""
        browser.get("http://localhost:3000/register")
        browser.find_element(By.ID, "email").send_keys("test@example.com")
        browser.find_element(By.ID, "password").send_keys("SecurePass123!")
        browser.find_element(By.ID, "confirm_password").send_keys("SecurePass123!")
        browser.find_element(By.ID, "name").send_keys("Test User")
        browser.find_element(By.ID, "register-button").click()
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
```

## Continuous Integration Testing

### Automated Test Pipeline

Comprehensive CI/CD testing workflow:
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run Python unit tests
        run: |
          pytest tests/unit/ -v \
            --cov=src \
            --cov-report=xml \
            --cov-fail-under=80

      - name: Run Python integration tests
        run: |
          pytest tests/integration/ -v \
            --cov=src \
            --cov-append \
            --cov-report=xml

      - name: Run Go tests
        run: |
          go test -v -race -coverprofile=coverage.out ./...
          go tool cover -html=coverage.out -o coverage.html

      - name: Run E2E tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 30
          pytest tests/e2e/ -v
          docker-compose -f docker-compose.test.yml down

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml,coverage.out

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run security scan
        run: |
          pip install bandit safety
          bandit -r src/ -f json -o bandit-report.json
          safety check --json --output safety-report.json

      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json
```
