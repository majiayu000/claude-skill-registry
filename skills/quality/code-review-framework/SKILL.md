---
name: code-review-framework
description: Automatically applies when reviewing code. Ensures structured review checklist covering correctness, security, performance, maintainability, testing, and documentation.
category: python
---

# Code Review Framework

When reviewing code, follow this structured framework for comprehensive, consistent reviews.

**Trigger Keywords**: code review, PR review, pull request, review checklist, code quality, review comments, review feedback

**Agent Integration**: Used by `code-reviewer`, `backend-architect`, `security-engineer`

## ✅ Correct Pattern: Review Checklist

```python
"""
Code Review Checklist
===================

Use this checklist for every code review.
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class ReviewCategory(str, Enum):
    """Review categories."""
    CORRECTNESS = "correctness"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


class ReviewSeverity(str, Enum):
    """Issue severity levels."""
    BLOCKING = "blocking"      # Must fix before merge
    MAJOR = "major"            # Should fix
    MINOR = "minor"            # Nice to have
    NITPICK = "nitpick"        # Style/preference


@dataclass
class ReviewComment:
    """Single review comment."""
    category: ReviewCategory
    severity: ReviewSeverity
    file: str
    line: int
    message: str
    suggestion: str = ""


class CodeReview:
    """Structured code review."""

    def __init__(self):
        self.comments: List[ReviewComment] = []

    def add_comment(
        self,
        category: ReviewCategory,
        severity: ReviewSeverity,
        file: str,
        line: int,
        message: str,
        suggestion: str = ""
    ):
        """Add review comment."""
        self.comments.append(ReviewComment(
            category=category,
            severity=severity,
            file=file,
            line=line,
            message=message,
            suggestion=suggestion
        ))

    def check_correctness(self, code: str):
        """Check correctness issues."""
        checks = [
            self._check_error_handling,
            self._check_edge_cases,
            self._check_logic_errors,
            self._check_type_safety,
        ]
        for check in checks:
            check(code)

    def check_security(self, code: str):
        """Check security issues."""
        checks = [
            self._check_input_validation,
            self._check_sql_injection,
            self._check_secret_exposure,
            self._check_authentication,
        ]
        for check in checks:
            check(code)

    def check_performance(self, code: str):
        """Check performance issues."""
        checks = [
            self._check_n_plus_one,
            self._check_inefficient_loops,
            self._check_memory_leaks,
            self._check_async_usage,
        ]
        for check in checks:
            check(code)

    def get_blocking_issues(self) -> List[ReviewComment]:
        """Get blocking issues that prevent merge."""
        return [
            c for c in self.comments
            if c.severity == ReviewSeverity.BLOCKING
        ]

    def generate_summary(self) -> Dict[str, int]:
        """Generate review summary."""
        summary = {
            "total_comments": len(self.comments),
            "blocking": 0,
            "major": 0,
            "minor": 0,
            "nitpick": 0,
        }

        for comment in self.comments:
            summary[comment.severity.value] += 1

        return summary
```

## Correctness Review

```python
"""
Correctness Review Checklist
===========================

1. Error Handling
"""

# ❌ Missing error handling
async def fetch_user(user_id: int):
    response = await http_client.get(f"/users/{user_id}")
    return response.json()  # What if request fails?

# ✅ Proper error handling
async def fetch_user(user_id: int) -> Dict:
    """
    Fetch user by ID.

    Args:
        user_id: User ID

    Returns:
        User data dict

    Raises:
        UserNotFoundError: If user doesn't exist
        APIError: If API request fails
    """
    try:
        response = await http_client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise UserNotFoundError(f"User {user_id} not found")
        raise APIError(f"API request failed: {e}")
    except httpx.RequestError as e:
        raise APIError(f"Network error: {e}")


"""
2. Edge Cases
"""

# ❌ No edge case handling
def divide(a: float, b: float) -> float:
    return a / b  # What if b is 0?

# ✅ Edge cases handled
def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Result of division

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


"""
3. Logic Errors
"""

# ❌ Logic error
def calculate_discount(price: float, discount_percent: float) -> float:
    return price - price * discount_percent  # Should divide by 100!

# ✅ Correct logic
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate price after discount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price - (price * discount_percent / 100)


"""
4. Type Safety
"""

# ❌ No type hints
def process_data(data):  # What type is data?
    return data.upper()

# ✅ Type hints
def process_data(data: str) -> str:
    """Process string data."""
    return data.upper()
```

## Security Review

```python
"""
Security Review Checklist
========================

1. Input Validation
"""

# ❌ No input validation
@app.post("/users")
async def create_user(email: str, password: str):
    user = User(email=email, password=password)
    db.add(user)
    return user

# ✅ Input validation with Pydantic
class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(min_length=8, max_length=100)

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

@app.post("/users")
async def create_user(user: UserCreate):
    # Input is validated
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    return db_user


"""
2. SQL Injection Prevention
"""

# ❌ SQL injection vulnerability
def get_user(email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query)  # Vulnerable!

# ✅ Parameterized queries
def get_user(email: str):
    query = text("SELECT * FROM users WHERE email = :email")
    return db.execute(query, {"email": email})


"""
3. Secret Exposure
"""

# ❌ Hardcoded secrets
API_KEY = "sk-1234567890abcdef"  # Exposed!
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ Environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = Field(alias="API_KEY")
    database_url: str = Field(alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


"""
4. Authentication & Authorization
"""

# ❌ No authentication
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db.delete(User, user_id)  # Anyone can delete!

# ✅ Proper authentication and authorization
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Check authorization
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(403, "Not authorized")

    db.delete(User, user_id)
```

## Performance Review

```python
"""
Performance Review Checklist
===========================

1. N+1 Queries
"""

# ❌ N+1 query problem
async def get_orders():
    orders = db.query(Order).all()
    for order in orders:
        print(order.user.email)  # N queries!

# ✅ Eager loading
async def get_orders():
    orders = db.query(Order).options(joinedload(Order.user)).all()
    for order in orders:
        print(order.user.email)  # Single query


"""
2. Inefficient Loops
"""

# ❌ Inefficient loop
def find_duplicates(items: List[str]) -> List[str]:
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other:
                duplicates.append(item)  # O(n²)
    return duplicates

# ✅ Efficient with set
def find_duplicates(items: List[str]) -> List[str]:
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)  # O(n)


"""
3. Async Usage
"""

# ❌ Blocking I/O in async
async def fetch_data():
    response = requests.get("https://api.example.com")  # Blocks!
    return response.json()

# ✅ Async I/O
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()


"""
4. Memory Usage
"""

# ❌ Loading entire file
def process_file(filepath: str):
    with open(filepath) as f:
        content = f.read()  # All in memory!
        for line in content.split('\n'):
            process_line(line)

# ✅ Streaming
def process_file(filepath: str):
    with open(filepath) as f:
        for line in f:  # One line at a time
            process_line(line)
```

## Review Comment Template

```markdown
## Review Summary

### Overview
- **Files Changed**: 5
- **Lines Changed**: +150, -30
- **Blocking Issues**: 0
- **Major Issues**: 2
- **Minor Issues**: 3

### Blocking Issues
None

### Major Issues

1. **File: `api/users.py`, Line 45** (Security)
   ```python
   # Current
   query = f"SELECT * FROM users WHERE id = {user_id}"

   # Suggestion
   query = text("SELECT * FROM users WHERE id = :id")
   result = db.execute(query, {"id": user_id})
   ```
   **Reason**: SQL injection vulnerability. Always use parameterized queries.

2. **File: `services/orders.py`, Line 78** (Performance)
   ```python
   # Current
   orders = db.query(Order).all()
   for order in orders:
       print(order.user.email)  # N+1 query

   # Suggestion
   orders = db.query(Order).options(joinedload(Order.user)).all()
   ```
   **Reason**: N+1 query problem. Use eager loading.

### Minor Issues

1. **File: `models/user.py`, Line 12** (Type Safety)
   - Missing return type hint on `get_full_name` method
   - Add: `-> str`

2. **File: `tests/test_users.py`, Line 34** (Testing)
   - Missing test for edge case: empty email
   - Add test case

3. **File: `utils/helpers.py`, Line 56** (Documentation)
   - Missing docstring for `format_date` function
   - Add Google-style docstring

### Positive Feedback
- ✅ Good use of Pydantic models for validation
- ✅ Comprehensive error handling
- ✅ Well-structured code
- ✅ Good test coverage (85%)

### Next Steps
1. Address major issues (SQL injection, N+1)
2. Consider minor improvements
3. Update tests
4. Update documentation

**Overall Assessment**: Approve after addressing major issues.
```

## ❌ Anti-Patterns in Reviews

```python
# ❌ Vague comments
"This doesn't look right"

# ✅ Better: Specific with suggestion
"SQL injection vulnerability on line 45. Use parameterized queries:
query = text('SELECT * FROM users WHERE id = :id')"


# ❌ No severity indication
"You should add error handling"

# ✅ Better: Clear severity
"[BLOCKING] Missing error handling. API calls can fail and crash the app."


# ❌ Only pointing out negatives
"You forgot type hints, missing tests, bad variable names"

# ✅ Better: Balance with positives
"Good use of Pydantic! One suggestion: add type hints to helper functions"


# ❌ Style preferences as blocking
"[BLOCKING] Use single quotes instead of double quotes"

# ✅ Better: Appropriate severity
"[NITPICK] Consider single quotes for consistency"
```

## Best Practices Checklist

### Reviewer
- ✅ Use structured review checklist
- ✅ Categorize comments (correctness, security, etc.)
- ✅ Indicate severity (blocking, major, minor)
- ✅ Provide specific suggestions with code examples
- ✅ Balance criticism with positive feedback
- ✅ Focus on important issues first
- ✅ Be respectful and constructive
- ✅ Test the code if possible
- ✅ Check for security vulnerabilities
- ✅ Review tests and documentation

### Author
- ✅ Self-review before requesting review
- ✅ Provide context in PR description
- ✅ Keep PRs focused and small (<400 lines)
- ✅ Respond to all comments
- ✅ Don't take feedback personally
- ✅ Ask questions if unclear
- ✅ Mark resolved comments
- ✅ Update tests and docs
- ✅ Verify all blocking issues fixed
- ✅ Request re-review after changes

## Auto-Apply

When reviewing code:
1. Use structured checklist (correctness, security, performance)
2. Categorize and prioritize issues
3. Provide specific suggestions with code
4. Mark severity (blocking, major, minor, nitpick)
5. Include positive feedback
6. Focus on impact, not style
7. Be respectful and constructive

## Related Skills

- `type-safety` - For type checking
- `async-await-checker` - For async patterns
- `structured-errors` - For error handling
- `pytest-patterns` - For test review
- `fastapi-patterns` - For API review
- `pydantic-models` - For validation review
