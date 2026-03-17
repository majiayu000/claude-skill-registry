---
name: ln-775-api-docs-generator
description: Configures Swagger/OpenAPI documentation
---

# ln-775-api-docs-generator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-770-crosscutting-setup

Configures API documentation with Swagger/OpenAPI.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Context Store from ln-770 |
| **Output** | Swagger/OpenAPI configuration |
| **Stacks** | .NET (Swashbuckle), Python (FastAPI built-in) |

---

## Phase 1: Receive Context + Analyze API Structure

Accept Context Store and scan for API endpoints.

**Required Context:**
- `STACK`: .NET or Python
- `PROJECT_ROOT`: Project directory path

**Idempotency Check:**
- .NET: Grep for `AddSwaggerGen` or `UseSwagger`
- Python: FastAPI has built-in OpenAPI, check for custom configuration
- If found: Return `{ "status": "skipped" }`

**API Analysis:**
1. Scan for controller/router files
2. Identify authentication method (JWT, OAuth2, API Key)
3. Check for API versioning

---

## Phase 2: Research Documentation Standards

Use MCP tools for current documentation.

**For .NET:**
```
MCP ref: "Swashbuckle ASP.NET Core OpenAPI Swagger configuration"
Context7: /domaindrivendev/Swashbuckle.AspNetCore
```

**For Python:**
```
MCP ref: "FastAPI OpenAPI documentation customization"
Context7: /tiangolo/fastapi
```

**Key Patterns to Research:**
1. OpenAPI 3.0/3.1 specification
2. Security scheme definitions
3. XML comments integration (.NET)
4. Response examples and schemas
5. API versioning documentation

---

## Phase 3: Decision Points

### Q1: API Information

| Field | Description | Required |
|-------|-------------|----------|
| Title | API name | ✓ Yes |
| Version | API version (v1, v2) | ✓ Yes |
| Description | Brief description | Optional |
| Contact | Support contact | Optional |
| License | API license | Optional |

### Q2: Security Scheme

| Scheme | Use Case | OpenAPI Type |
|--------|----------|--------------|
| **JWT Bearer** (Recommended) | Token in Authorization header | `http` + `bearer` |
| **API Key** | Key in header or query | `apiKey` |
| **OAuth2** | Full OAuth2 flow | `oauth2` |
| **None** | Public API | No security |

### Q3: Documentation Features

| Feature | .NET | Python | Default |
|---------|------|--------|---------|
| XML Comments | ✓ Supported | N/A | ✓ Enable |
| Response Examples | ✓ Manual | ✓ Pydantic | ✓ Enable |
| Request Validation | ✓ Annotations | ✓ Pydantic | ✓ Enable |
| Try It Out | ✓ Yes | ✓ Yes | ✓ Enable |

---

## Phase 4: Generate Configuration

### .NET Output Files

| File | Purpose |
|------|---------|
| `Extensions/SwaggerExtensions.cs` | Swagger service registration |
| `*.csproj` (update) | Enable XML documentation |

**Generation Process:**
1. Use MCP ref for current Swashbuckle API
2. Generate SwaggerExtensions with:
   - AddEndpointsApiExplorer
   - AddSwaggerGen with OpenApiInfo
   - Security definition (if auth detected)
   - XML comments inclusion
3. Update csproj for documentation generation

**Packages to Add:**
- `Swashbuckle.AspNetCore`

**Registration Code:**
```csharp
builder.Services.AddSwaggerServices();
// ...
app.UseSwaggerServices();
```

**csproj Update:**
```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
```

### Python Output Files

| File | Purpose |
|------|---------|
| `core/openapi_config.py` | OpenAPI customization |

**Generation Process:**
1. Use MCP ref for FastAPI OpenAPI customization
2. Generate openapi_config.py with:
   - Custom OpenAPI schema
   - Security scheme definitions
   - Tags and descriptions
3. FastAPI generates OpenAPI automatically

**Note:** FastAPI has built-in OpenAPI support. This worker customizes the default configuration.

**Registration Code:**
```python
from core.openapi_config import custom_openapi
app.openapi = lambda: custom_openapi(app)
```

---

## Phase 5: Validate

**Validation Steps:**

1. **Syntax check:**
   - .NET: `dotnet build --no-restore`
   - Python: `python -m py_compile core/openapi_config.py`

2. **Access documentation:**
   | Stack | URL |
   |-------|-----|
   | .NET | http://localhost:5000/swagger |
   | Python | http://localhost:5000/docs |
   | Python (ReDoc) | http://localhost:5000/redoc |

3. **Verify content:**
   - [ ] All endpoints visible
   - [ ] Request/response schemas displayed
   - [ ] Security scheme shown (if configured)
   - [ ] Try It Out functional

4. **OpenAPI spec validation:**
   ```bash
   # .NET
   curl http://localhost:5000/swagger/v1/swagger.json | jq .

   # Python
   curl http://localhost:5000/openapi.json | jq .
   ```

---

## Security Scheme Examples

### JWT Bearer (.NET)

```csharp
// Structure only - actual code generated via MCP ref
options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
{
    Description = "JWT Authorization header using Bearer scheme",
    Name = "Authorization",
    In = ParameterLocation.Header,
    Type = SecuritySchemeType.Http,
    Scheme = "bearer",
    BearerFormat = "JWT"
});
```

### JWT Bearer (Python/FastAPI)

```python
# Structure only - actual code generated via MCP ref
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

---

## Return to Coordinator

```json
{
  "status": "success",
  "files_created": [
    "Extensions/SwaggerExtensions.cs"
  ],
  "packages_added": [
    "Swashbuckle.AspNetCore"
  ],
  "registration_code": "builder.Services.AddSwaggerServices();",
  "message": "Configured Swagger/OpenAPI documentation"
}
```

---

## Reference Links

- [Swashbuckle.AspNetCore](https://github.com/domaindrivendev/Swashbuckle.AspNetCore)
- [FastAPI OpenAPI](https://fastapi.tiangolo.com/tutorial/metadata/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

---

## Critical Rules

- **Use MCP ref for current Swashbuckle/FastAPI API** — do not hardcode configuration from memory
- **Auto-detect auth scheme** — scan for JWT, OAuth2, or API Key and configure security definition accordingly
- **Enable XML documentation in .NET** — update csproj with `GenerateDocumentationFile` and suppress warning 1591
- **FastAPI: customize, not replace** — built-in OpenAPI works by default, only add custom schema/security
- **Idempotent** — if `AddSwaggerGen`/`UseSwagger` exists, return `status: "skipped"`

## Definition of Done

- Context Store received (stack, project root)
- API structure analyzed (controllers/routers, auth method, versioning)
- Documentation standards researched via MCP tools
- Swagger/OpenAPI configuration generated with API info and security scheme
- XML comments enabled (.NET) or custom OpenAPI schema configured (Python)
- Syntax validated (`dotnet build` or `py_compile`)
- Structured JSON response returned to ln-770 coordinator

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
