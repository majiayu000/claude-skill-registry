---
name: pydantic-documentation
description: Pydantic model patterns for gh-pr-linear-issue-linker. Use when creating or modifying Pydantic models, webhook payloads, API responses, or any data structures.
---

# Pydantic Model Patterns

**Critical Rule**: Use Pydantic for ALL data structures - webhook payloads, API requests/responses, configuration models.

## Core Pydantic Patterns

### 1. Webhook Payload Models

**Best for**: GitHub/Linear webhook payloads, ensuring type safety.

```python
from pydantic import BaseModel, Field

class PullRequestEvent(BaseModel):
    """GitHub pull request webhook payload."""

    action: str = Field(description="Event action (opened, synchronize, etc.)")
    number: int = Field(description="Pull request number")
    pull_request: PullRequest
    sender: User

class PullRequest(BaseModel):
    """Pull request data from GitHub API."""

    number: int
    title: str
    user: User
    head: BranchRef
    base: BranchRef
```

### 2. API Response Models

**Best for**: Structuring responses from GitHub/Linear APIs.

```python
class LinearTicket(BaseModel):
    """Linear issue/ticket data."""

    id: str
    title: str
    identifier: str  # e.g., "ENG-123"
    state: str
    assignee: User | None = None

class GitHubComment(BaseModel):
    """GitHub PR comment payload."""

    body: str = Field(description="Markdown comment body")
```

### 3. Configuration Models

**Best for**: Application settings and environment config.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration from environment variables."""

    github_app_id: str
    github_private_key: str
    linear_api_key: str
    webhook_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## Patterns to Follow

### Pattern 1: Enums for Webhook Events

```python
from enum import StrEnum

class GitHubEvent(StrEnum):
    """GitHub webhook event types we handle."""
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    ISSUE_COMMENT = "issue_comment"

class PullRequestAction(StrEnum):
    """Pull request webhook actions."""
    OPENED = "opened"
    SYNCHRONIZE = "synchronize"
    REOPENED = "reopened"
    CLOSED = "closed"
```

### Pattern 2: Nested Models for Complex Payloads

```python
class User(BaseModel):
    """GitHub/Linear user data."""
    id: int | str
    login: str
    email: str | None = None

class BranchRef(BaseModel):
    """Git branch reference."""
    ref: str  # Branch name
    sha: str  # Commit SHA

class PullRequest(BaseModel):
    """GitHub pull request data."""
    number: int
    title: str
    state: str
    user: User  # Nested model
    head: BranchRef  # Nested model
    base: BranchRef  # Nested model
```

### Pattern 3: Optional Fields with Defaults

```python
class LinearTicket(BaseModel):
    """Linear issue data."""

    id: str
    title: str
    identifier: str
    state: str

    # Optional fields
    assignee: User | None = None
    description: str | None = None
    priority: int = 0
    labels: list[str] = []  # Empty list default

    # Use Field for validation
    url: str = Field(pattern=r"^https://linear\.app/.*")
```

### Pattern 4: Validation and Serialization

```python
from pydantic import field_validator, field_serializer

class GitHubWebhook(BaseModel):
    """GitHub webhook payload with validation."""

    event: str
    signature: str
    payload: dict

    @field_validator("signature")
    @classmethod
    def validate_signature(cls, v: str) -> str:
        """Ensure signature has correct format."""
        if not v.startswith("sha256="):
            raise ValueError("Invalid signature format")
        return v

    @field_serializer("payload")
    def serialize_payload(self, value: dict) -> str:
        """Serialize payload to JSON string."""
        return json.dumps(value)
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Using @dataclass Instead of Pydantic

```python
# ❌ BAD - No runtime validation
from dataclasses import dataclass

@dataclass
class PullRequest:
    number: int
    title: str
```

**Why it's bad**: No validation, no JSON serialization, no FastAPI integration.

**Fix**: Use Pydantic BaseModel.

### ❌ Anti-Pattern 2: Missing Type Hints

```python
# ❌ BAD - No type safety
class PullRequest(BaseModel):
    number = 0  # What type is this?
    title = ""  # String? Optional?
```

**Why it's bad**: Loses all benefits of type checking and validation.

**Fix**: Always use explicit type hints.

### ❌ Anti-Pattern 3: Overly Permissive Types

```python
# ❌ BAD - Accepts anything
class WebhookPayload(BaseModel):
    data: dict  # What's in this dict?
    metadata: Any  # Completely untyped
```

**Why it's bad**: Defeats the purpose of using Pydantic - no structure validation.

**Fix**: Define specific nested models.

```python
# ✅ GOOD - Specific types
class WebhookPayload(BaseModel):
    data: PullRequestData
    metadata: WebhookMetadata
```

### ❌ Anti-Pattern 4: Mutable Defaults

```python
# ❌ BAD - Mutable default argument
class Config(BaseModel):
    tags: list[str] = []  # Shared across instances!
```

**Why it's bad**: Pydantic handles this correctly, but use Field(default_factory) to be explicit.

**Fix**: Use default_factory for mutable types.

```python
# ✅ GOOD - Explicit default factory
class Config(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

### ❌ Anti-Pattern 5: Manual JSON Parsing

```python
# ❌ BAD - Manual dict manipulation
data = json.loads(request.body)
pr_number = data["pull_request"]["number"]
title = data["pull_request"]["title"]
```

**Why it's bad**: Error-prone, no validation, tedious.

**Fix**: Use Pydantic model parsing.

```python
# ✅ GOOD - Pydantic handles it
event = PullRequestEvent.model_validate(data)
pr_number = event.pull_request.number
title = event.pull_request.title
```

## Quality Checklist

When creating or modifying Pydantic models:

### ✅ Model Structure
- [ ] Use BaseModel, never @dataclass
- [ ] Every field has explicit type hints
- [ ] Class docstring describes the model's purpose
- [ ] Optional fields use `| None` and have defaults
- [ ] Use specific types, not dict/Any unless truly dynamic

### ✅ Field Definitions
- [ ] Use Field() for validation constraints
- [ ] Use Field(description=...) for API documentation
- [ ] Mutable defaults use Field(default_factory=...)
- [ ] Pattern validation for strings (URLs, emails, etc.)

### ✅ Nested Models
- [ ] Complex objects use nested BaseModel, not raw dicts
- [ ] Shared models extracted to common module
- [ ] Clear hierarchy (Event -> PullRequest -> User)

### ✅ Enums
- [ ] Use StrEnum for string constants
- [ ] Class docstring explains purpose
- [ ] Values match external API exactly (GitHub/Linear)

## Examples from Project

### Webhook Event Model

```python
# src/models/github.py
class PullRequestEvent(BaseModel):
    """GitHub pull_request webhook event."""

    action: PullRequestAction
    number: int
    pull_request: PullRequest
    repository: Repository
    sender: User
```

### API Response Model

```python
# src/models/linear.py
class LinearTicket(BaseModel):
    """Linear issue from GraphQL API."""

    id: str
    identifier: str = Field(pattern=r"^[A-Z]+-\d+$")  # e.g., "ENG-123"
    title: str
    state: str
    assignee: User | None = None
```

## Testing Models

```python
import pytest
from pydantic import ValidationError

def test_pull_request_validation():
    """Test PullRequest model validates correctly."""
    # Valid data
    pr = PullRequest(number=123, title="Fix bug", user=user, ...)
    assert pr.number == 123

    # Invalid data
    with pytest.raises(ValidationError):
        PullRequest(number="not-a-number", ...)
```

## Summary

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use Pydantic BaseModel for all data | Use @dataclass or plain dicts |
| Add explicit type hints to all fields | Rely on implicit types |
| Use Field() for validation/defaults | Use mutable defaults directly |
| Parse JSON with model_validate() | Manual dict access |
| Define nested models for complex data | Use dict or Any |

**Golden Rule**: Every piece of external data (webhooks, API responses, config) should have a corresponding Pydantic model.