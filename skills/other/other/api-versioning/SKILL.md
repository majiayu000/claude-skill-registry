---
name: api-versioning
model: standard
description: API versioning strategies — URL path, header, query param, content negotiation — with breaking change classification, deprecation timelines, migration patterns, and multi-version support. Use when evolving APIs, planning breaking changes, or managing version lifecycles.
---

# API Versioning Patterns

Evolve your API confidently. Version correctly, deprecate gracefully, migrate safely — without breaking existing consumers.

## Versioning Strategies

Pick one strategy and apply it consistently across your entire API surface.

| Strategy | Format | Visibility | Cacheability | Best For |
|----------|--------|------------|--------------|----------|
| **URL Path** | `/api/v1/users` | High | Excellent | Public APIs, third-party integrations |
| **Query Param** | `/api/users?v=1` | Medium | Moderate | Simple APIs, prototyping |
| **Header** | `Accept-Version: v1` | Low | Good | Internal APIs, coordinated consumers |
| **Content Negotiation** | `Accept: application/vnd.api.v1+json` | Low | Good | Enterprise, strict REST compliance |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install api-versioning
```


---

## URL Path Versioning

The most common strategy. Version lives in the URL, making it immediately visible.

```python
from fastapi import FastAPI, APIRouter

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

@v1.get("/users")
async def list_users_v1():
    return {"users": [...]}

@v2.get("/users")
async def list_users_v2():
    return {"data": {"users": [...]}, "meta": {...}}

app = FastAPI()
app.include_router(v1)
app.include_router(v2)
```

**Rules:**

- Always prefix: `/api/v1/...` not `/v1/api/...`
- Major version only: `/api/v1/`, never `/api/v1.2/` or `/api/v1.2.3/`
- Every endpoint must be versioned — no mixing versioned and unversioned paths

## Header Versioning

Version specified via request headers, keeping URLs clean.

```javascript
function versionRouter(req, res, next) {
  const version = req.headers['accept-version'] || 'v2'; // default to latest
  req.apiVersion = version;
  next();
}

app.get('/api/users', versionRouter, (req, res) => {
  if (req.apiVersion === 'v1') return res.json({ users: [...] });
  if (req.apiVersion === 'v2') return res.json({ data: { users: [...] }, meta: {} });
  return res.status(400).json({ error: `Unsupported version: ${req.apiVersion}` });
});
```

Always define fallback behavior when no version header is sent — default to latest stable or return `400 Bad Request`.

## Semantic Versioning for APIs

| SemVer Component | API Meaning | Action Required |
|------------------|-------------|-----------------|
| **MAJOR** (v1 → v2) | Breaking changes — remove field, rename endpoint, change auth | Clients must migrate |
| **MINOR** (v1.1 → v1.2) | Additive, backward-compatible — new optional field, new endpoint | No client changes |
| **PATCH** (v1.1.0 → v1.1.1) | Bug fixes, no behavior change | No client changes |

Only MAJOR versions appear in URL paths. Communicate MINOR and PATCH through changelogs.

---

## Breaking vs Non-Breaking Changes

### Breaking — Require New Version

| Change | Why It Breaks |
|--------|---------------|
| Remove a response field | Clients reading that field get `undefined` |
| Rename a field | Same as removal from the client's perspective |
| Change a field's type | `"id": 123` → `"id": "123"` breaks typed clients |
| Remove an endpoint | Clients calling it get `404` |
| Make optional param required | Existing requests missing it start failing |
| Change URL structure | Bookmarked/hardcoded URLs break |
| Change error response format | Client error-handling logic breaks |
| Change authentication mechanism | Existing credentials stop working |

### Non-Breaking — Safe Under Same Version

| Change | Why It's Safe |
|--------|---------------|
| Add new optional response field | Clients ignore unknown fields |
| Add new endpoint | Doesn't affect existing endpoints |
| Add new optional query/body param | Existing requests work without it |
| Add new enum value | Safe if clients handle unknown values gracefully |
| Relax a validation constraint | Previously valid requests remain valid |
| Improve performance | Same interface, faster response |

---

## Deprecation Strategy

Never remove a version without warning. Follow this timeline:

```
Phase 1: ANNOUNCE
  • Sunset header on responses  • Changelog entry
  • Email/webhook to consumers  • Docs marked "deprecated"

Phase 2: SUNSET PERIOD
  • v1 still works but warns     • Monitor v1 traffic
  • Contact remaining consumers  • Provide migration support

Phase 3: REMOVAL
  • v1 returns 410 Gone
  • Response body includes migration guide URL
  • Redirect docs to v2
```

**Minimum deprecation periods:** Public API: 12 months · Partner API: 6 months · Internal API: 1–3 months

### Sunset HTTP Header (RFC 8594)

Include on every response from a deprecated version:

```
HTTP/1.1 200 OK
Sunset: Sat, 01 Mar 2025 00:00:00 GMT
Deprecation: true
Link: <https://api.example.com/docs/migrate-v1-v2>; rel="sunset"
X-API-Warn: "v1 is deprecated. Migrate to v2 by 2025-03-01."
```

### Retired Version Response

When past sunset, return `410 Gone`:

```json
{
  "error": "VersionRetired",
  "message": "API v1 was retired on 2025-03-01.",
  "migration_guide": "https://api.example.com/docs/migrate-v1-v2",
  "current_version": "v2"
}
```

---

## Migration Patterns

### Adapter Pattern

Shared business logic, version-specific serialization:

```python
class UserService:
    async def get_user(self, user_id: str) -> User:
        return await self.repo.find(user_id)

def to_v1(user: User) -> dict:
    return {"id": user.id, "name": user.full_name, "email": user.email}

def to_v2(user: User) -> dict:
    return {
        "id": user.id,
        "name": {"first": user.first_name, "last": user.last_name},
        "emails": [{"address": e, "primary": i == 0} for i, e in enumerate(user.emails)],
        "created_at": user.created_at.isoformat(),
    }
```

### Facade Pattern

Single entry point delegates to the correct versioned handler:

```python
async def get_user(user_id: str, version: int):
    user = await user_service.get_user(user_id)
    serializers = {1: to_v1, 2: to_v2}
    serialize = serializers.get(version)
    if not serialize:
        raise UnsupportedVersionError(version)
    return serialize(user)
```

### Versioned Controllers

Separate controller files per version, shared service layer:

```
api/
  v1/
    users.py      # v1 request/response shapes
    orders.py
  v2/
    users.py      # v2 request/response shapes
    orders.py
  services/
    user_service.py   # version-agnostic business logic
    order_service.py
```

### API Gateway Routing

Route versions at infrastructure layer:

```yaml
routes:
  - match: /api/v1/*
    upstream: api-v1-service:8080
  - match: /api/v2/*
    upstream: api-v2-service:8080
```

---

## Multi-Version Support

**Architecture:**

```
Request → API Gateway → Version Router → v1 Handler → Shared Service Layer → DB
                                        → v2 Handler ↗
```

**Principles:**

1. **Business logic is version-agnostic.** Services, repositories, and domain models are shared.
2. **Serialization is version-specific.** Each version has its own request validators and response serializers.
3. **Transformations are explicit.** A `v1_to_v2` transformer documents every field mapping.
4. **Tests cover all active versions.** Every supported version has its own integration test suite.

**Maximum concurrent versions:** 2–3 active (current + 1–2 deprecated). More than 3 creates unsustainable maintenance burden.

---

## Client Communication

### Changelog

Publish a changelog for every release, tagged by version and change type:

```markdown
## v2.3.0 — 2025-02-01
### Added
- `avatar_url` field on User response
- `GET /api/v2/users/{id}/activity` endpoint
### Deprecated
- `name` field on User — use `first_name` and `last_name` (removal in v3)
```

### Migration Guides

For every major version bump, provide:

- Field-by-field mapping table (v1 → v2)
- Before/after request and response examples
- Code snippets for common languages/SDKs
- Timeline with key dates (announcement, sunset, removal)

### SDK Versioning

Align SDK major versions with API major versions:

```
api-client@1.x  →  /api/v1
api-client@2.x  →  /api/v2
```

Ship the new SDK before announcing API deprecation.

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| **Versioning too frequently** | Batch breaking changes into infrequent major releases |
| **Breaking without notice** | Always follow the deprecation timeline |
| **Eternal version support** | Set and enforce sunset dates |
| **Inconsistent versioning** | One version scheme, applied uniformly |
| **Version per endpoint** | Version the entire API surface together |
| **Using versions to gate features** | Use feature flags separately; versions are for contracts |
| **No default version** | Always define a default or return explicit 400 |

---

## NEVER Do

1. **NEVER** remove a field, endpoint, or change a type without bumping the major version
2. **NEVER** sunset a public API version with less than 6 months notice
3. **NEVER** mix versioning strategies in the same API (URL path for some, headers for others)
4. **NEVER** use minor or patch versions in URL paths (`/api/v1.2/` is wrong — use `/api/v1/`)
5. **NEVER** version individual endpoints independently — version the entire API surface as a unit
6. **NEVER** deploy a breaking change under an existing version number, even if "nobody uses that field"
7. **NEVER** skip documenting differences between versions — every breaking change needs a migration guide entry
