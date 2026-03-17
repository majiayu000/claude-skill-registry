---
name: python-development
description: Python development patterns for gh-pr-linear-issue-linker. Use when writing Python code, implementing features, fixing bugs, or working with FastAPI webhook handlers.
---

# Python Development Patterns

## Architecture Layers

```
FastAPI Handler -> Service Layer -> Integration Clients (GitHub/Linear)
```

- **FastAPI Handler** (`src/main.py`): Webhook entry point, signature verification, request/response handling
- **Service Layer** (`src/services/`): Business logic orchestration, comment formatting
- **Integration Clients**: GitHub API client, Linear GraphQL client
- **Models**: Pydantic models for webhooks, responses, and API data

## FastAPI Handler Pattern

```python
from fastapi import FastAPI, Request, HTTPException, Header
import logfire

app = FastAPI()

@app.post("/webhook")
@logfire.instrument("github_webhook")
async def handle_webhook(
    request: Request,
    x_hub_signature_256: str = Header(...),
) -> dict[str, str]:
    """Handle GitHub webhook events."""
    # 1. Verify signature
    if not await verify_signature(request, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 2. Parse payload
    payload = await request.json()

    # 3. Process event
    result = await process_pull_request_event(payload)

    return {"status": "success"}
```

## Config Module Pattern

```python
from typing import Final
import os

# Use Final type annotations for all constants
GITHUB_APP_ID: Final[str] = os.getenv("GITHUB_APP_ID", "")
GITHUB_PRIVATE_KEY: Final[str] = os.getenv("GITHUB_PRIVATE_KEY", "")
LINEAR_API_KEY: Final[str] = os.getenv("LINEAR_API_KEY", "")

# Validation
def validate_config() -> None:
    """Validate required configuration on startup."""
    required = {
        "GITHUB_APP_ID": GITHUB_APP_ID,
        "GITHUB_PRIVATE_KEY": GITHUB_PRIVATE_KEY,
        "LINEAR_API_KEY": LINEAR_API_KEY,
    }

    missing = [k for k, v in required.items() if not v]
    if missing:
        raise ValueError(f"Missing required config: {', '.join(missing)}")

# Call on import
validate_config()
```

## Logging Pattern (CRITICAL)

### Logfire Observability

This service uses **Logfire** for observability:

```python
import logfire

# Instrument FastAPI automatically
logfire.instrument_fastapi(app)

# Instrument httpx client
logfire.instrument_httpx()

# Add manual instrumentation for key operations
@logfire.instrument("fetch_linear_tickets")
async def fetch_linear_tickets(user_id: str) -> list[Ticket]:
    """Fetch in-progress Linear tickets for a user."""
    # Logfire automatically captures:
    # - Function args
    # - Return value
    # - Exceptions
    # - Duration
    ...
```

**Key rules:**
- Use `@logfire.instrument()` decorator on key business operations
- Let FastAPI/httpx auto-instrumentation handle HTTP traces
- Use structured logging for business events
- Include context (PR number, user, ticket ID) in logs

## Error Handling

```python
from fastapi import HTTPException
import logfire

# Use HTTPException for client errors
@app.post("/webhook")
async def handle_webhook(request: Request) -> dict:
    if not payload.get("pull_request"):
        raise HTTPException(status_code=400, detail="Not a PR event")

    # For external service errors, log and handle gracefully
    try:
        tickets = await fetch_linear_tickets(user_id)
    except httpx.HTTPError as e:
        logfire.error("Linear API failed", error=str(e), user_id=user_id)
        # Decide: fail gracefully or raise
        return {"status": "error", "message": "Linear API unavailable"}

    # For unexpected errors, let them propagate (500)
    # Logfire will capture the exception trace automatically
```

## Early Returns

Keep indentation flat with guard clauses:

```python
async def process_message(request: ChatRequest) -> str:
    if not request.user_message:
        return "Empty message"

    tenant_config = await get_tenant_config(request.tenant_id)
    if tenant_config is None:
        return "Tenant not found"

    if not tenant_config.is_active:
        return "Tenant inactive"

    # Main logic here (minimal indentation)
    return await run_agent(request, tenant_config)
```

## Async/Await Patterns

```python
import asyncio
import httpx

async def fetch_pr_context(
    github_client: httpx.AsyncClient,
    linear_client: httpx.AsyncClient,
    pr_number: int,
    user_id: str,
) -> tuple[PullRequest, list[Ticket]]:
    """Fetch PR details and Linear tickets concurrently."""
    pr, tickets = await asyncio.gather(
        fetch_pull_request(github_client, pr_number),
        fetch_linear_tickets(linear_client, user_id),
    )
    return pr, tickets

# FastAPI is async-native
@app.post("/webhook")
async def handle_webhook(request: Request) -> dict:
    async with httpx.AsyncClient() as client:
        result = await process_event(client, payload)
    return result
```

## Data Conventions

| Context                    | Convention   |
|----------------------------|--------------|
| Database columns           | `snake_case` |
| HTTP JSON fields           | `snake_case` |
| S3 keys                    | `snake_case` |
| Python classes             | `PascalCase` |
| Python variables/functions | `snake_case` |

## Package Structure

**All `__init__.py` files MUST be empty.** No exceptions.

- Create `__init__.py` in every directory that should be a Python package
- Never add imports, re-exports, or any code to `__init__.py`
- Import directly from the module: `from src.agents.product_analyzer.agent import create_agent`

## Data Models

**Use Pydantic BaseModel for ALL data structures.** Never use @dataclass.

```python
from pydantic import BaseModel, Field, ConfigDict

# Simple model
class PageContext(BaseModel):
    url: str
    title: str | None = None
    semantic_dom_id: str | None = None

# Frozen (immutable) model
class IntentDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    examples: list[Example]

# Model with default factory
class RetryContext(BaseModel):
    attempt: int = 0
    audit_trail: list[str] = Field(default_factory=list)
```

**Why Pydantic over dataclass:**
- Runtime validation
- JSON serialization/deserialization
- Schema generation
- Better IDE support
- Consistent with Pydantic AI agent framework

## Type Annotations and Imports

**NEVER use `TYPE_CHECKING` conditional imports.**

```python
# ❌ WRONG - DO NOT USE TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.github.models import PRCommit

# ✅ CORRECT - Use regular runtime imports
from src.github.models import PRCommit
```

**Why TYPE_CHECKING is forbidden:**
- Pydantic models need types available at runtime for validation
- `TYPE_CHECKING` imports are only available during static type checking (mypy/pyright)
- Causes runtime errors: `PydanticUserError: Model is not fully defined`
- Creates confusing debugging scenarios
- No performance benefit for imports in production

**Rules:**
- Always import types at runtime (normal imports)
- Never use `if TYPE_CHECKING:` blocks
- Never use forward references - if you need them, restructure the code
- All type annotations must reference runtime-available classes

## HTTP Client Pattern

**Use httpx for all HTTP calls** (not requests):

```python
import httpx

# Prefer async client
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()

# With automatic Logfire instrumentation
import logfire
logfire.instrument_httpx()  # Call once at startup

# All httpx requests are now traced automatically
```

## Quality Checklist

Before delivering code:

- [ ] All functions have type hints
- [ ] Pydantic BaseModel for all data structures (NEVER @dataclass)
- [ ] NEVER use `TYPE_CHECKING` conditional imports (use runtime imports)
- [ ] Single responsibility is clear for each component
- [ ] Early returns flatten indentation
- [ ] No file exceeds 200 lines
- [ ] FastAPI handlers use HTTPException for client errors
- [ ] Key operations use `@logfire.instrument()` decorator
- [ ] Config module uses `Final` constants
- [ ] All `__init__.py` files are empty
- [ ] httpx (not requests) for HTTP calls
- [ ] Code passes `make check` (ruff format + lint + pytest)
