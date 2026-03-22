---
name: reflex-fastapi
description: "Guide for building custom FastAPI endpoints within Reflex applications. Use when creating webhooks, external API integrations, JWT authentication, or any endpoint that lives outside the Reflex state/event system. Covers integration pattern, Pydantic V2 schemas, async endpoints, dependency injection, security rules, and endpoint testing with httpx."
---

# Reflex FastAPI Custom Endpoints

This skill covers building custom FastAPI endpoints within a Reflex application. Use it for logic that lives outside the Reflex state/event system: webhooks, external integrations, JWT auth, REST APIs for third-party consumers, etc.

For Reflex core (state, components, routing) → see skill `reflex-core`.
For visual design and aesthetics → see skill `reflex-design`.

---

## FastAPI Custom Endpoints

Reflex exposes the underlying FastAPI server. Use it for custom endpoints outside of the Reflex state/event system (webhooks, external integrations, JWT auth, etc.).

### Integration Pattern

```python
app = rx.App()

# Access the underlying FastAPI server
fastapi_app = app.api

@fastapi_app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@fastapi_app.post("/api/webhook")
async def webhook(payload: MyPydanticModel):
    return {"received": True}
```

### Core Workflow

1. **Analyze requirements** — Identify endpoints, data models, auth needs
2. **Design schemas** — Create Pydantic V2 models for validation
3. **Implement** — Write async endpoints with proper dependency injection
4. **Secure** — Add authentication, authorization, rate limiting
5. **Test** — Write async tests with pytest and httpx

### Reference Guide

| Topic | Load When |
|-------|-----------|
| Pydantic V2 | Creating schemas, validation, model_config |
| Async DB drivers | asyncpg, aiomysql, models, CRUD operations using Raw SQL |
| Endpoints & Routing | APIRouter, dependencies, routing |
| Authentication | JWT, OAuth2, get_current_user |
| Testing | pytest-asyncio, httpx, fixtures |

### MUST DO
- Use type hints everywhere (FastAPI requires them)
- Use Pydantic V2 syntax (`field_validator`, `model_validator`, `model_config`)
- Use `Annotated` pattern for dependency injection
- Use `async/await` for all I/O operations
- Use `X | None` instead of `Optional[X]`
- Return proper HTTP status codes
- Document endpoints (auto-generated OpenAPI)

### MUST NOT DO
- Use synchronous database operations
- Skip Pydantic validation
- Store passwords in plain text
- Expose sensitive data in responses
- Use Pydantic V1 syntax (`@validator`, `class Config`)
- Mix sync and async code improperly
- Hardcode configuration values

### Pydantic V2 Schema Example

```python
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Annotated

class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    email: str
    age: int | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()
```

### Output Templates

When implementing FastAPI features, provide:
1. Schema file (Pydantic models)
2. Endpoint file (router with endpoints)
3. CRUD operations if database involved
4. Brief explanation of key decisions

---

## Testing FastAPI Endpoints (httpx)

```python
import pytest
from httpx import AsyncClient, ASGITransport
from my_app.my_app import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app.api), base_url="http://test"
    ) as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_endpoint_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app.api), base_url="http://test"
    ) as client:
        response = await client.post("/api/users", json={"name": ""})
    assert response.status_code == 422
```

---

## References

- FastAPI Docs: https://fastapi.tiangolo.com/
- Pydantic V2 Docs: https://docs.pydantic.dev/latest/
