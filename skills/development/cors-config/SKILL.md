# Skill: CORS Configuration for FastAPI

**Purpose**: Configure CORS (Cross-Origin Resource Sharing) for FastAPI to allow frontend requests.

## Trigger Conditions

Invoke this skill when:
- Setting up FastAPI backend that will receive requests from a separate frontend
- User encounters "CORS error" or "blocked by CORS policy"
- Phase II requires frontend-backend communication

## Capabilities

### 1. Generate CORS Configuration

Add to `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application",
    version="1.0.0"
)

# Parse CORS origins from settings
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight for 10 minutes
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "cors": "enabled"}
```

### 2. Environment Configuration

In `.env`:
```env
# Single origin
CORS_ORIGINS=http://localhost:3000

# Multiple origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### 3. Development vs Production

**Development:**
```env
CORS_ORIGINS=http://localhost:3000
```

**Production:**
```env
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

## Common CORS Errors & Solutions

### Error: "Access-Control-Allow-Origin missing"

**Cause**: Frontend origin not in allowed list.

**Solution**:
1. Add frontend URL to `CORS_ORIGINS`
2. Restart backend server
3. Check for trailing slashes (use `http://localhost:3000` not `http://localhost:3000/`)

### Error: "Preflight request fails"

**Cause**: OPTIONS request not handled.

**Solution**:
```python
allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
```

### Error: "Credentials flag is true but Access-Control-Allow-Credentials is not 'true'"

**Cause**: Credentials not allowed.

**Solution**:
```python
allow_credentials=True,
```

### Error: "Request header field Authorization is not allowed"

**Cause**: Authorization header not allowed.

**Solution**:
```python
allow_headers=["*"],
# Or specifically:
allow_headers=["Authorization", "Content-Type"],
```

## Debug CORS Issues

Add debug logging:

```python
@app.middleware("http")
async def log_cors(request, call_next):
    origin = request.headers.get("origin", "no-origin")
    print(f"Request from origin: {origin}")
    response = await call_next(request)
    print(f"CORS headers: {dict(response.headers)}")
    return response
```

## Frontend Configuration

For Next.js API calls:
```typescript
// lib/api.ts
const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    credentials: 'include',  // Important for cookies
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
});
```

## Checklist

- [ ] Add CORSMiddleware to FastAPI app
- [ ] Set CORS_ORIGINS in .env (frontend URL)
- [ ] Include credentials if using cookies
- [ ] Allow necessary HTTP methods
- [ ] Test preflight (OPTIONS) requests
- [ ] Verify in browser DevTools Network tab
