---
name: testing-patterns
description: Testing strategies, patterns, and best practices across test types. Auto-triggers when writing tests, setting up test infrastructure, or improving test coverage.
---

# Testing Patterns Skill

## Test Pyramid

```
        /\
       /  \    E2E Tests (few, slow, expensive)
      /----\
     /      \  Integration Tests (some)
    /--------\
   /          \ Unit Tests (many, fast, cheap)
  --------------
```

## Unit Testing Patterns

### Arrange-Act-Assert (AAA)
```python
def test_user_can_change_email():
    # Arrange
    user = User(email="old@example.com")

    # Act
    user.change_email("new@example.com")

    # Assert
    assert user.email == "new@example.com"
```

### Given-When-Then (BDD Style)
```python
def test_user_can_change_email():
    # Given a user with an email
    user = User(email="old@example.com")

    # When they change their email
    user.change_email("new@example.com")

    # Then the email is updated
    assert user.email == "new@example.com"
```

### Test Data Builders
```python
class UserBuilder:
    def __init__(self):
        self.name = "Default Name"
        self.email = "default@example.com"
        self.role = "user"

    def with_name(self, name):
        self.name = name
        return self

    def with_admin_role(self):
        self.role = "admin"
        return self

    def build(self):
        return User(self.name, self.email, self.role)

# Usage
admin = UserBuilder().with_name("Admin").with_admin_role().build()
```

### Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Integration Testing Patterns

### Database Tests
```python
@pytest.fixture
def db_session():
    # Setup
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)

    yield session

    # Teardown
    session.close()

def test_user_repository(db_session):
    repo = UserRepository(db_session)
    user = repo.create(User(name="Test"))

    found = repo.find_by_id(user.id)
    assert found.name == "Test"
```

### API Tests
```python
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post("/users", json={"name": "Test"})

    assert response.status_code == 201
    assert response.json["name"] == "Test"
```

### Contract Tests
```python
# Consumer defines expected contract
def test_user_api_contract():
    # Expected response structure
    expected_schema = {
        "type": "object",
        "required": ["id", "name", "email"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        }
    }

    response = client.get("/users/1")
    validate(response.json, expected_schema)
```

## Mocking Strategies

### When to Mock
- External services (APIs, databases in unit tests)
- Non-deterministic behavior (time, randomness)
- Slow operations
- Side effects (email, notifications)

### When NOT to Mock
- Your own code (usually)
- Simple value objects
- In integration tests (test real interactions)

### Mock Patterns
```python
# Stub - returns canned response
mock_service.get_user.return_value = User(id=1, name="Test")

# Mock - verifies interaction
mock_service.send_email.assert_called_once_with("test@example.com")

# Spy - records calls but uses real implementation
with patch.object(service, 'method', wraps=service.method) as spy:
    service.method()
    spy.assert_called()
```

## E2E Testing Patterns

### Page Object Pattern
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def username_input(self):
        return self.driver.find_element(By.ID, "username")

    @property
    def password_input(self):
        return self.driver.find_element(By.ID, "password")

    def login(self, username, password):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit_button.click()
        return DashboardPage(self.driver)

# Usage in test
def test_successful_login(driver):
    login_page = LoginPage(driver)
    dashboard = login_page.login("user", "pass")
    assert dashboard.welcome_message == "Welcome, user!"
```

## Test Quality Indicators

### Good Tests Are
- **Fast**: Milliseconds for unit tests
- **Isolated**: No test depends on another
- **Repeatable**: Same result every run
- **Self-validating**: Pass or fail, no manual check
- **Timely**: Written before or with code

### Bad Test Smells
- Flaky tests (intermittent failures)
- Slow test suite
- Tests that test implementation details
- Tests requiring manual setup
- Tests that share mutable state
