---
name: qa-expert
version: 1.0.0
description: Expert-level quality assurance, testing strategies, automation, and QA processes
category: qa
tags: [qa, testing, test-automation, quality-assurance, selenium]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# Quality Assurance Expert

Expert guidance for quality assurance, testing strategies, test automation, and QA best practices.

## Core Concepts

### Testing Types
- Unit testing
- Integration testing
- System testing
- Acceptance testing
- Regression testing
- Performance testing
- Security testing

### Test Automation
- Selenium WebDriver
- Cypress, Playwright
- API testing (Postman, REST Assured)
- Mobile testing (Appium)
- CI/CD integration
- Test frameworks (JUnit, pytest, Jest)

### QA Processes
- Test planning
- Test case design
- Defect management
- Test metrics and reporting
- Risk-based testing
- Exploratory testing

## Test Automation Framework

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List

class BasePage:
    """Base page object"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.find_element(locator)
        element.click()

    def type_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

class LoginPage(BasePage):
    """Login page object"""

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")

    def login(self, username: str, password: str):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

class TestRunner:
    """Test execution framework"""

    def __init__(self, browser: str = "chrome"):
        self.browser = browser
        self.driver = None
        self.results = []

    def setup(self):
        if self.browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(10)

    def teardown(self):
        if self.driver:
            self.driver.quit()

    def run_test(self, test_func, test_name: str):
        try:
            test_func()
            self.results.append({"test": test_name, "status": "PASS"})
        except Exception as e:
            self.results.append({
                "test": test_name,
                "status": "FAIL",
                "error": str(e)
            })

    def generate_report(self) -> Dict:
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = total - passed

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "results": self.results
        }

# Pytest fixtures
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    driver.get("https://example.com/login")
    return LoginPage(driver)

# Test cases
def test_successful_login(login_page):
    login_page.login("testuser", "password123")
    assert "Dashboard" in login_page.driver.title

def test_invalid_credentials(login_page):
    login_page.login("invalid", "wrong")
    error = login_page.get_error_message()
    assert "Invalid credentials" in error
```

## API Testing

```python
import requests
from typing import Dict, Any

class APITestClient:
    """API testing client"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def test_get_endpoint(self, endpoint: str, expected_status: int = 200,
                         expected_keys: List[str] = None) -> Dict:
        """Test GET endpoint"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url)

        result = {
            "endpoint": endpoint,
            "method": "GET",
            "status_code": response.status_code,
            "passed": response.status_code == expected_status
        }

        if expected_keys and response.status_code == 200:
            data = response.json()
            missing_keys = [k for k in expected_keys if k not in data]
            result["missing_keys"] = missing_keys
            result["passed"] = result["passed"] and len(missing_keys) == 0

        self.test_results.append(result)
        return result

    def test_post_endpoint(self, endpoint: str, payload: Dict,
                          expected_status: int = 201) -> Dict:
        """Test POST endpoint"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=payload)

        result = {
            "endpoint": endpoint,
            "method": "POST",
            "status_code": response.status_code,
            "passed": response.status_code == expected_status,
            "response_time_ms": response.elapsed.total_seconds() * 1000
        }

        self.test_results.append(result)
        return result

    def test_authentication(self, login_endpoint: str,
                           credentials: Dict) -> bool:
        """Test API authentication"""
        response = self.session.post(
            f"{self.base_url}{login_endpoint}",
            json=credentials
        )

        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                return True

        return False

    def test_rate_limiting(self, endpoint: str, requests_count: int = 100):
        """Test rate limiting"""
        url = f"{self.base_url}{endpoint}"
        rate_limited = False

        for i in range(requests_count):
            response = self.session.get(url)
            if response.status_code == 429:
                rate_limited = True
                break

        return {
            "rate_limited": rate_limited,
            "requests_before_limit": i if rate_limited else requests_count
        }
```

## Test Data Management

```python
import random
from faker import Faker
from typing import Dict, List

class TestDataGenerator:
    """Generate test data"""

    def __init__(self):
        self.faker = Faker()

    def generate_user(self) -> Dict:
        """Generate user test data"""
        return {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone": self.faker.phone_number(),
            "address": {
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state(),
                "zip": self.faker.zipcode()
            }
        }

    def generate_users(self, count: int) -> List[Dict]:
        """Generate multiple users"""
        return [self.generate_user() for _ in range(count)]

    def generate_order(self, user_id: str) -> Dict:
        """Generate order test data"""
        return {
            "order_id": self.faker.uuid4(),
            "user_id": user_id,
            "items": [
                {
                    "product_id": self.faker.uuid4(),
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(10, 500), 2)
                }
                for _ in range(random.randint(1, 5))
            ],
            "total": 0,  # Calculate based on items
            "status": random.choice(["pending", "processing", "shipped", "delivered"])
        }

    def generate_invalid_data(self, field: str) -> Any:
        """Generate invalid test data for boundary testing"""
        invalid_patterns = {
            "email": ["not-an-email", "missing@domain", "@nodomain.com"],
            "phone": ["123", "abc-def-ghij", "+++"],
            "zip": ["ABC", "123", "12345678"],
            "date": ["99/99/9999", "2023-13-45", "invalid"]
        }

        return random.choice(invalid_patterns.get(field, ["invalid"]))
```

## Defect Tracking

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Priority(Enum):
    P0 = "p0"
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"

@dataclass
class Defect:
    defect_id: str
    title: str
    description: str
    severity: Severity
    priority: Priority
    status: str
    reported_by: str
    assigned_to: str
    created_at: datetime
    environment: str
    steps_to_reproduce: List[str]
    expected_result: str
    actual_result: str

class DefectTracker:
    """Track and manage defects"""

    def __init__(self):
        self.defects: Dict[str, Defect] = {}

    def create_defect(self, defect: Defect) -> str:
        """Create new defect"""
        self.defects[defect.defect_id] = defect
        return defect.defect_id

    def update_status(self, defect_id: str, new_status: str):
        """Update defect status"""
        if defect_id in self.defects:
            self.defects[defect_id].status = new_status

    def get_critical_defects(self) -> List[Defect]:
        """Get all critical defects"""
        return [d for d in self.defects.values()
                if d.severity == Severity.CRITICAL and d.status != "closed"]

    def generate_metrics(self) -> Dict:
        """Generate defect metrics"""
        total = len(self.defects)
        by_severity = {}
        by_status = {}

        for defect in self.defects.values():
            severity = defect.severity.value
            status = defect.status

            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total_defects": total,
            "by_severity": by_severity,
            "by_status": by_status,
            "critical_open": len(self.get_critical_defects())
        }
```

## Best Practices

### Test Strategy
- Define clear test objectives
- Use risk-based testing
- Maintain test coverage metrics
- Automate regression tests
- Perform exploratory testing
- Test early and often
- Review and update test cases

### Automation
- Follow Page Object Model
- Make tests independent
- Use explicit waits
- Implement proper error handling
- Maintain test data separately
- Use CI/CD integration
- Monitor test stability

### Defect Management
- Write clear bug reports
- Include reproduction steps
- Attach screenshots/logs
- Prioritize appropriately
- Track to closure
- Analyze root causes
- Share lessons learned

## Anti-Patterns

❌ Testing only happy paths
❌ No test automation strategy
❌ Vague bug reports
❌ Testing without requirements
❌ Ignoring flaky tests
❌ No regression testing
❌ Testing in production only

## Resources

- Selenium: https://www.selenium.dev/
- Pytest: https://docs.pytest.org/
- Cypress: https://www.cypress.io/
- ISTQB: https://www.istqb.org/
- Test Automation University: https://testautomationu.applitools.com/
