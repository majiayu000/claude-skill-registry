---
name: python-code-review
description: Master Python code review patterns including type hints, async/await issues, exception handling, mutable defaults, security vulnerabilities, and testing patterns. Use PROACTIVELY when reviewing Python PRs.
---

# Python Code Review

Comprehensive code review checklist and patterns for Python applications, focusing on type safety, async programming, exception handling, and security.

## When to Use This Skill

- Reviewing Python pull requests
- Establishing Python code review standards
- Training reviewers on Python-specific issues
- Catching common Python bugs and anti-patterns
- Security review of Python applications

## Quick Checklist

```markdown
## Python Review Checklist

- [ ] Type hints on all functions and complex types
- [ ] No mutable default arguments
- [ ] Exceptions caught specifically, not broadly
- [ ] Context managers used for resources
- [ ] No blocking calls in async code
- [ ] Tests use pytest with proper fixtures
- [ ] Security: No eval/exec, inputs validated
- [ ] PEP 8 compliant (run ruff/black first)
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Type Hints

### Missing Type Hints

```python
# ❌ Missing type hints - hard to understand and maintain
def process_data(data, config):
    return data.get("value") * config.factor

# ✅ Complete type hints - clear contract
def process_data(data: dict[str, Any], config: Config) -> float:
    return data.get("value", 0.0) * config.factor
```

### Overly Broad Types

```python
# ❌ Overly broad Any defeats type checking
def fetch_user(user_id: Any) -> Any:
    ...

# ✅ Specific types enable IDE support and catch bugs
def fetch_user(user_id: int) -> User | None:
    ...
```

### Complex Return Types

```python
# ❌ Missing return type on complex returns
def get_items(include_inactive):
    if include_inactive:
        return get_all_items()
    return get_active_items()

# ✅ Explicit return type
def get_items(include_inactive: bool) -> list[Item]:
    if include_inactive:
        return get_all_items()
    return get_active_items()
```

### Generic Types

```python
# ❌ Losing type information
def first_item(items: list) -> Any:
    return items[0] if items else None

# ✅ Preserve type with generics
from typing import TypeVar

T = TypeVar('T')

def first_item(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## Mutable Default Arguments

### The Classic Bug

```python
# ❌ CRITICAL BUG: Mutable default argument
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)  # Shared across ALL calls!
    return items

# First call: add_item("a") returns ["a"]
# Second call: add_item("b") returns ["a", "b"]  # BUG!

# ✅ Use None as default
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### Dict Default Arguments

```python
# ❌ Same issue with dict
def update_config(key: str, value: str, config: dict = {}):
    config[key] = value
    return config

# ✅ Factory pattern
def update_config(
    key: str,
    value: str,
    config: dict[str, str] | None = None
) -> dict[str, str]:
    if config is None:
        config = {}
    config[key] = value
    return config
```

### Set Default Arguments

```python
# ❌ Set is also mutable
def add_tag(tag: str, tags: set = set()):
    tags.add(tag)
    return tags

# ✅ None default with factory
def add_tag(tag: str, tags: set[str] | None = None) -> set[str]:
    if tags is None:
        tags = set()
    tags.add(tag)
    return tags
```

---

## Exception Handling

### Catching Everything

```python
# ❌ Catching everything - hides bugs, catches KeyboardInterrupt!
try:
    result = process_data(data)
except:
    pass

# ❌ Too broad - still catches SystemExit, KeyboardInterrupt
try:
    result = process_data(data)
except Exception:
    logger.error("Failed")

# ✅ Catch specific exceptions
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
    raise DataValidationError(f"Processing failed: {e}") from e
except KeyError as e:
    logger.error(f"Missing required field: {e}")
    raise DataValidationError(f"Missing field: {e}") from e
```

### Losing Exception Context

```python
# ❌ Losing exception context - traceback is lost
try:
    fetch_data()
except HTTPError as e:
    raise ApplicationError("Fetch failed")  # Lost original traceback!

# ✅ Chain exceptions to preserve context
try:
    fetch_data()
except HTTPError as e:
    raise ApplicationError("Fetch failed") from e  # Preserves traceback
```

### Silent Failures

```python
# ❌ Silent failure - bugs go unnoticed
try:
    save_to_database(data)
except DatabaseError:
    pass  # Data lost silently!

# ✅ At minimum, log the error
try:
    save_to_database(data)
except DatabaseError as e:
    logger.error(f"Failed to save data: {e}")
    # Re-raise, return error, or handle appropriately
    raise
```

### Using Wrong Exception Types

```python
# ❌ Raising generic exceptions
def validate_user(user: User) -> None:
    if not user.email:
        raise Exception("Invalid user")  # Too generic!

# ✅ Use or create specific exceptions
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

def validate_user(user: User) -> None:
    if not user.email:
        raise ValidationError("User email is required")
```

---

## Async/Await Issues

### Blocking Calls in Async

```python
# ❌ Blocking call in async function - blocks entire event loop!
async def fetch_and_process(url: str) -> dict:
    response = requests.get(url)  # BLOCKS event loop!
    time.sleep(1)  # BLOCKS event loop!
    return response.json()

# ✅ Use async libraries
async def fetch_and_process(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    await asyncio.sleep(1)
    return response.json()
```

### Sequential When Parallel is Possible

```python
# ❌ Sequential awaits when parallel is possible
async def get_user_data(user_id: int) -> UserData:
    profile = await fetch_profile(user_id)
    posts = await fetch_posts(user_id)       # Waits for profile!
    followers = await fetch_followers(user_id)  # Waits for posts!
    return UserData(profile, posts, followers)

# ✅ Parallel execution with gather
async def get_user_data(user_id: int) -> UserData:
    profile, posts, followers = await asyncio.gather(
        fetch_profile(user_id),
        fetch_posts(user_id),
        fetch_followers(user_id),
    )
    return UserData(profile, posts, followers)
```

### TaskGroup (Python 3.11+)

```python
# ✅ Even better with TaskGroup for error handling
async def get_user_data(user_id: int) -> UserData:
    async with asyncio.TaskGroup() as tg:
        profile_task = tg.create_task(fetch_profile(user_id))
        posts_task = tg.create_task(fetch_posts(user_id))
        followers_task = tg.create_task(fetch_followers(user_id))

    return UserData(
        profile_task.result(),
        posts_task.result(),
        followers_task.result(),
    )
```

### Fire and Forget

```python
# ❌ Fire and forget without error handling
async def process_webhook(data: dict) -> None:
    asyncio.create_task(send_notification(data))  # Errors silently lost!

# ✅ Handle task errors
async def process_webhook(data: dict) -> None:
    task = asyncio.create_task(send_notification(data))
    task.add_done_callback(lambda t: log_if_error(t))

def log_if_error(task: asyncio.Task) -> None:
    if task.exception():
        logger.error(f"Task failed: {task.exception()}")
```

---

## Security Issues

### SQL Injection

```python
# ❌ SQL Injection vulnerability
def get_user(username: str) -> User:
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query).fetchone()
    # Input: "' OR '1'='1" returns all users!

# ✅ Parameterized query
def get_user(username: str) -> User | None:
    query = "SELECT * FROM users WHERE username = :username"
    return db.execute(query, {"username": username}).fetchone()
```

### Command Injection

```python
# ❌ Command injection vulnerability
def run_command(filename: str) -> str:
    return os.system(f"cat {filename}")
    # Input: "; rm -rf /" deletes everything!

# ✅ Use subprocess with list args
def run_command(filename: str) -> str:
    result = subprocess.run(
        ["cat", filename],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout
```

### Dangerous eval/exec

```python
# ❌ Dangerous eval - arbitrary code execution
def calculate(expression: str) -> float:
    return eval(expression)
    # Input: "__import__('os').system('rm -rf /')" - disaster!

# ✅ Use safe alternatives
import ast

def calculate(expression: str) -> float:
    # Only allow literals
    return ast.literal_eval(expression)

# Or use a proper expression parser
import numexpr
def calculate(expression: str) -> float:
    return numexpr.evaluate(expression)
```

### Hardcoded Secrets

```python
# ❌ Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgres://user:password@localhost/db"

# ✅ Environment variables
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# Or use a secrets manager
from my_app.config import settings
API_KEY = settings.api_key
```

### Path Traversal

```python
# ❌ Path traversal vulnerability
def read_file(filename: str) -> str:
    with open(f"/uploads/{filename}") as f:
        return f.read()
    # Input: "../../../etc/passwd" reads system files!

# ✅ Validate and sanitize paths
from pathlib import Path

UPLOADS_DIR = Path("/uploads").resolve()

def read_file(filename: str) -> str:
    file_path = (UPLOADS_DIR / filename).resolve()

    # Ensure path is still under uploads directory
    if not file_path.is_relative_to(UPLOADS_DIR):
        raise ValueError("Invalid file path")

    with open(file_path) as f:
        return f.read()
```

---

## Testing Patterns

### Test Naming and Structure

```python
# ❌ Test with unclear purpose
def test_user():
    user = User("test")
    assert user.name == "test"

# ✅ Descriptive test name with AAA pattern
def test_user_creation_sets_name_correctly():
    # Arrange
    expected_name = "john_doe"

    # Act
    user = User(name=expected_name)

    # Assert
    assert user.name == expected_name
```

### Testing Implementation Details

```python
# ❌ Testing implementation details - brittle tests
def test_user_internal_id_format():
    user = User("test")
    assert user._internal_id.startswith("usr_")  # Private!

# ✅ Test behavior, not implementation
def test_user_has_unique_identifier():
    user1 = User("test")
    user2 = User("test")
    assert user1.id != user2.id
```

### Mocking External Dependencies

```python
# ❌ No mocking of external dependencies
def test_fetch_user():
    user = fetch_user_from_api(123)  # Calls real API!
    assert user.name == "expected"

# ✅ Mock external calls
def test_fetch_user(mocker):
    # Arrange
    mock_response = {"id": 123, "name": "expected"}
    mocker.patch("httpx.get", return_value=Mock(json=lambda: mock_response))

    # Act
    user = fetch_user_from_api(123)

    # Assert
    assert user.name == "expected"
```

### Parameterized Tests

```python
# ❌ Repetitive tests
def test_validate_email_valid():
    assert validate_email("user@example.com") is True

def test_validate_email_invalid_no_at():
    assert validate_email("userexample.com") is False

def test_validate_email_invalid_no_domain():
    assert validate_email("user@") is False

# ✅ Parameterized tests
import pytest

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.name@domain.co.uk", True),
    ("userexample.com", False),
    ("user@", False),
    ("@example.com", False),
    ("", False),
])
def test_validate_email(email: str, expected: bool):
    assert validate_email(email) is expected
```

### Async Test Support

```python
# ❌ Not using async test support
def test_async_function():
    result = asyncio.run(fetch_data())  # Works but not ideal
    assert result is not None

# ✅ Use pytest-asyncio
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data()
    assert result is not None
```

---

## Resource Management

### Missing Context Managers

```python
# ❌ Resource not properly closed
def read_file(path: str) -> str:
    f = open(path)
    content = f.read()
    return content  # File never closed!

# ✅ Use context manager
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()
```

### Database Connections

```python
# ❌ Connection leak
def query_database(sql: str) -> list:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
    # Connection never closed!

# ✅ Proper resource management
def query_database(sql: str) -> list:
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
```

---

## Common Pitfalls

| Pitfall             | Problem                   | Solution                         |
| ------------------- | ------------------------- | -------------------------------- |
| Mutable defaults    | Shared state across calls | Use `None` default + factory     |
| Bare `except`       | Catches KeyboardInterrupt | Catch specific exceptions        |
| `requests` in async | Blocks event loop         | Use `httpx` or `aiohttp`         |
| f-string in SQL     | SQL injection             | Parameterized queries            |
| Missing type hints  | Hard to maintain          | Add hints, run mypy              |
| `eval()`            | Code injection            | Use `ast.literal_eval` or parser |
| No test isolation   | Flaky tests               | Mock external dependencies       |

## Best Practices Summary

1. **Type Everything** - Use type hints on all functions
2. **No Mutable Defaults** - Use `None` with factory pattern
3. **Specific Exceptions** - Catch and handle specifically
4. **Async All The Way** - Use async libraries in async code
5. **Parameterize Queries** - Never use f-strings in SQL
6. **Context Managers** - For all resources that need cleanup
7. **Test Behavior** - Not implementation details
8. **Validate Input** - Especially from external sources


## Parent Hub
- [_data-ai-mastery](../_data-ai-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
