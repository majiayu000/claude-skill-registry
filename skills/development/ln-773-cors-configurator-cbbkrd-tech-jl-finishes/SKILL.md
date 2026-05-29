---
name: ln-773-cors-configurator
description: Configures CORS policy for development and production
---

# ln-773-cors-configurator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-770-crosscutting-setup

Configures Cross-Origin Resource Sharing (CORS) policy with security-first approach.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Context Store from ln-770 |
| **Output** | CORS configuration with environment-specific policies |
| **Stacks** | .NET (ASP.NET Core CORS), Python (FastAPI CORSMiddleware) |

---

## Phase 1: Receive Context

Accept Context Store from coordinator.

**Required Context:**
- `STACK`: .NET or Python
- `PROJECT_ROOT`: Project directory path
- `ENVIRONMENT`: Development or Production

**Idempotency Check:**
- .NET: Grep for `AddCors` or `UseCors`
- Python: Grep for `CORSMiddleware`
- If found: Return `{ "status": "skipped" }`

---

## Phase 2: Analyze Project Structure

Determine frontend configuration.

**Detection Steps:**
1. Check for frontend in same repository (`/frontend`, `/client`, `/web`)
2. Read `.env` or `appsettings.json` for CORS_ORIGINS
3. Identify common frontend ports (3000, 5173, 4200)

**Detected Frontend Origins:**

| Framework | Default Port | Origin |
|-----------|--------------|--------|
| React (CRA) | 3000 | http://localhost:3000 |
| Vite | 5173 | http://localhost:5173 |
| Angular | 4200 | http://localhost:4200 |
| Next.js | 3000 | http://localhost:3000 |

---

## Phase 3: Decision Points

### Q1: Allowed Origins

| Environment | Strategy |
|-------------|----------|
| **Development** | Allow localhost origins (configurable) |
| **Production** | Explicit origins from environment variables only |

**Security Warning:** Never use `*` (wildcard) with credentials.

### Q2: Allowed Methods

| Method | Default | Notes |
|--------|---------|-------|
| GET | ✓ Yes | Read operations |
| POST | ✓ Yes | Create operations |
| PUT | ✓ Yes | Update operations |
| DELETE | ✓ Yes | Delete operations |
| PATCH | Optional | Partial updates |
| OPTIONS | ✓ Yes | Preflight requests (automatic) |

### Q3: Credentials Support

| Scenario | AllowCredentials | Notes |
|----------|------------------|-------|
| Cookie-based auth | ✓ Yes | Required for cookies |
| JWT in header | ✗ No | Not needed |
| OAuth2 | Depends | Check documentation |

**Warning:** AllowCredentials = true prohibits `*` origin.

### Q4: Preflight Cache Duration

| Environment | MaxAge | Rationale |
|-------------|--------|-----------|
| Development | 0 | Immediate config changes |
| Production | 86400 (24h) | Reduce preflight requests |

---

## Phase 4: Generate Configuration

### .NET Output Files

| File | Purpose |
|------|---------|
| `Extensions/CorsExtensions.cs` | CORS service registration |
| `appsettings.json` (update) | Origins configuration |
| `appsettings.Development.json` (update) | Dev origins |

**Generation Process:**
1. Use MCP ref for current ASP.NET Core CORS API
2. Generate CorsExtensions with:
   - Development policy (permissive)
   - Production policy (restrictive)
   - Environment-based policy selection
3. Update appsettings with CORS:Origins

**Registration Code:**
```csharp
builder.Services.AddCorsPolicy(builder.Configuration);
// ...
app.UseCors(builder.Environment.IsDevelopment() ? "Development" : "Production");
```

### Python Output Files

| File | Purpose |
|------|---------|
| `middleware/cors_config.py` | CORS middleware configuration |
| `.env` (update) | CORS_ORIGINS variable |

**Generation Process:**
1. Use MCP ref for FastAPI CORSMiddleware
2. Generate cors_config.py with:
   - Origin parsing from environment
   - Method and header configuration
   - Credentials handling
3. Update .env with CORS_ORIGINS

**Registration Code:**
```python
from middleware.cors_config import configure_cors
configure_cors(app)
```

---

## Phase 5: Validate

**Validation Steps:**

1. **Syntax check:**
   - .NET: `dotnet build --no-restore`
   - Python: `python -m py_compile middleware/cors_config.py`

2. **CORS test:**
   ```bash
   # Test preflight request
   curl -X OPTIONS http://localhost:5000/api/test \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -v
   ```

3. **Verify headers:**
   - `Access-Control-Allow-Origin`: Should match request origin
   - `Access-Control-Allow-Methods`: Should list allowed methods
   - `Access-Control-Allow-Credentials`: true (if enabled)
   - `Access-Control-Max-Age`: Cache duration

---

## Security Checklist

Before completing, verify:

- [ ] No wildcard `*` origin in production
- [ ] Explicit allowed methods (not `AllowAnyMethod` in prod)
- [ ] Credentials only if needed
- [ ] Origins from environment variables in production
- [ ] Preflight caching enabled in production

---

## Return to Coordinator

```json
{
  "status": "success",
  "files_created": [
    "Extensions/CorsExtensions.cs"
  ],
  "packages_added": [],
  "registration_code": "builder.Services.AddCorsPolicy(configuration);",
  "message": "Configured CORS with Development and Production policies"
}
```

---

## Reference Links

- [ASP.NET Core CORS](https://learn.microsoft.com/aspnet/core/security/cors)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS)

---

## Critical Rules

- **Never use wildcard `*` origin with credentials** — security violation per CORS spec
- **Production origins from environment variables only** — no hardcoded URLs in code
- **Separate Development and Production policies** — permissive locally, restrictive in production
- **Idempotent** — if `AddCors`/`UseCors` or `CORSMiddleware` exists, return `status: "skipped"`
- **Enable preflight caching in Production** — MaxAge 86400 (24h) to reduce OPTIONS requests

## Definition of Done

- Context Store received (stack, project root, environment)
- Frontend origins detected (port/framework auto-detection)
- User decisions collected (origins, methods, credentials, cache duration)
- CORS configuration generated with environment-specific policies
- Security checklist verified (no wildcard + credentials, explicit methods, env-based origins)
- Syntax validated (`dotnet build` or `py_compile`)
- Structured JSON response returned to ln-770 coordinator

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
