---
name: fastapi-web-framework
description: Create FastAPI web server with standard middleware, JWT authentication, and REST API endpoints
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T23:01:15.231Z"
  updated_at: "2026-01-29T23:01:15.231Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Create a FastAPI web server with standard production-ready middleware and authentication.

# When To Use
- Building FastAPI web backend
- Creating API server for web frontend
- Ticket requires web framework implementation

# Procedure

## Dependencies
Add to pyproject.toml:
```toml
fastapi>=0.128.0
uvicorn[standard]>=0.40.0
python-jose[cryptography]>=3.5.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.22
email-validator>=2.0.0
```

## Project Structure
```bash
src/vibe_piper/web/
├── __init__.py              # Main FastAPI app
├── api/
│   ├── router.py             # API router
│   └── endpoints/
│       ├── auth.py          # Authentication endpoints
│       ├── health.py        # Health check endpoints
│       └── pipelines.py     # Feature endpoints
└── middleware/
    ├── error_handler.py   # Structured error handling
    ├── rate_limit.py     # Rate limiting
    └── request_id.py     # Request ID for tracing
```

## App Creation
`src/vibe_piper/web/__init__.py`:
```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from vibe_piper.web.api.router import api_router
from vibe_piper.web.middleware.error_handler import add_error_handlers
from vibe_piper.web.middleware.rate_limit import RateLimitMiddleware
from vibe_piper.web.middleware.request_id import RequestIDMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Name",
        version="0.1.0",
        docs_url="/docs",
        lifespan=lifespan,
    )

    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"])
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RateLimitMiddleware)
    add_error_handlers(app)
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()
```

## Authentication
Use JWT with python-jose:
- SECRET_KEY from env (production)
- ACCESS_TOKEN_EXPIRE_MINUTES = 30
- REFRESH_TOKEN_EXPIRE_DAYS = 7
- bcrypt for password hashing
- OAuth2PasswordBearer for token scheme

## Error Handling
Create structured error responses:
```python
class ErrorResponse(BaseModel):
    error: str
    message: str
    detail: dict | None
    request_id: str | None
```

## Rate Limiting
Token bucket algorithm:
- 60 requests per minute
- 1000 requests per hour
- Client by IP or X-Forwarded-For

## Testing
```bash
uv run vibepiper-server --reload
curl http://127.0.0.1:8000/api/v1/health
```

## Acceptance Criteria
- [ ] FastAPI server runs on port 8000
- [ ] CORS configured for frontend
- [ ] JWT authentication implemented
- [ ] Rate limiting configured
- [ ] Structured error responses
- [ ] OpenAPI/Swagger UI at /docs
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
