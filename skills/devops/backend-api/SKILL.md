---
name: backend-api
description: >
  · Design/review HTTP APIs for FastAPI, Express, NestJS: REST, OpenAPI, pagination, OAuth/JWT. Triggers: 'fastapi', 'express', 'nestjs', 'openapi', 'pagination', 'idempotency', 'rest api', 'endpoint'. Not for schemas (use databases).
license: MIT
compatibility: "Optional: Python or Node.js framework context. Optional: OpenAPI-capable framework/docs tooling"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-06"
  effort: high
  argument_hint: "[framework-or-api-task]"
---

# Backend APIs: HTTP Service Design and Implementation

Design and review HTTP APIs that stay coherent as they grow. Focus on contracts, auth
boundaries, error models, and framework structure for Python and Node.js services.

**Target versions** (May 2026):
- FastAPI **0.135.3** (released 2026-04-01)
- Express **5.2.1** (published 2025-12-01)
- NestJS **11.1.18** (published 2026-04-03)
- OpenAPI Specification **3.2.0** (published 2025-09-19)
- HTTP Semantics: **RFC 9110** (June 2022)
- Problem Details for HTTP APIs: **RFC 9457** (July 2023)
- OAuth 2.0 Security Best Current Practice: **RFC 9700** (January 2025)

This skill works across five concerns:
- **Contract design** - resources, methods, status codes, schemas, versioning
- **API ergonomics** - pagination, filtering, sorting, idempotency, error format
- **Framework structure** - FastAPI dependencies, Express middleware, NestJS modules and guards
- **Authentication** - sessions, bearer tokens, OAuth/OIDC, BFF and token mediation
- **Review** - unstable contracts, DTO leakage, auth confusion, and HTTP misuse

## When to use

- Designing a new REST or HTTP API
- Reviewing an existing FastAPI, Express, or NestJS service
- Writing or fixing OpenAPI specifications and generated docs
- Choosing status codes, error formats, pagination, filtering, or versioning strategy
- Designing auth flows for browser, mobile, machine-to-machine, or third-party clients
- Refactoring route or controller structure that has become hard to reason about
- Planning backward-compatible API evolution
- Defining idempotency and retry behavior for write endpoints

## When NOT to use

- GraphQL schema, resolvers, federation, or persisted query work - out of scope for this skill
- gRPC, protobuf schema evolution, or streaming RPCs - out of scope for this skill
- Database schema, indexing, replication, or query tuning - use **databases**
- General bug-finding, race-condition hunting, or correctness review outside the API boundary - use **code-review**
- Security auditing for auth bypasses, injection, secrets, or OWASP findings - use **security-audit**
- Writing or debugging automated tests - use **testing**
- Deployment, containers, gateways, ingress, or cluster config - use **docker**, **kubernetes**, or **networking**
- CI/CD pipeline design for API delivery - use **ci-cd**
- MCP-specific HTTP servers and tool handlers - use **mcp**

---

## AI Self-Check

Before returning API code, route design, or OpenAPI output, verify:

- [ ] Resource names are nouns and URL shape is stable (`/users/{userId}/sessions`, not `/doUserSessionThing`)
- [ ] Method semantics follow RFC 9110 - no "GET that mutates", no PATCH used as a vague catch-all
- [ ] `401` vs `403` is correct: unauthenticated vs authenticated-but-forbidden
- [ ] Ownership-hiding behavior is deliberate and consistent: decide when out-of-scope resources return `404` vs `403`
- [ ] Error responses use one consistent format, preferably RFC 9457 problem details
- [ ] Request and response DTOs are explicit and separate from ORM or database models
- [ ] Input validation happens server-side even if clients or SDKs also validate
- [ ] Offset pagination is not used blindly on large or high-churn collections where cursor pagination is the safer default
- [ ] Write endpoints that may be retried (`POST /payments`, webhook receivers, order creation) define idempotency behavior
- [ ] OpenAPI docs match real handler behavior, examples, status codes, and auth requirements
- [ ] First-party browser apps do not get long-lived bearer tokens stored in browser storage by default
- [ ] Cookie-based browser auth accounts for cookie scope and CSRF behavior instead of assuming cookies are automatically safe
- [ ] OAuth guidance is current: authorization code + PKCE, no implicit flow, no resource owner password credentials
- [ ] Sensitive defaults are explicit: cookie flags, token TTLs, scope boundaries, and rate limits are not hand-waved
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Framework version checked**: FastAPI, Express, NestJS, and OpenAPI examples match current APIs and migration notes
- [ ] **Contract compatibility checked**: response codes, pagination, errors, and auth behavior preserve existing clients unless a version bump is explicit
- [ ] **Injection in handler body flagged as contract defect**: if injection (SQL, command, header, path traversal) is found inside a route handler, flag it as a missing validation-boundary defect at the contract layer and recommend fixing it there; route to **security-audit** for a full injection audit if the pattern is widespread

---

## Performance

- Paginate and filter at the data store; never load full collections just to slice in the handler.
- Set timeouts and body limits at the framework, proxy, and client layers.
- Measure p95/p99 latency and error rates for changed endpoints before optimizing internals.


---

## Best Practices

- Design idempotency for retries on create, payment, provisioning, and webhook endpoints.
- Generate or validate OpenAPI from the implementation contract and keep examples executable.
- Use explicit auth scopes and tenancy checks in handlers, not only in route grouping or UI state.


## Workflow

**Build vs. Review:** when reviewing an existing service, still walk the same steps. Determine the API boundary, audit the contract, trace auth, then compare the implementation against the published behavior instead of jumping straight into handler code.

### Step 1: Determine the boundary

Clarify the API before picking framework patterns:
- **Who calls it?** Browser app, mobile app, third-party integrator, internal service, webhook sender
- **What kind of API is it?** Public API, private app backend, internal service, admin API
- **Is the task greenfield or review?** New design, incremental change, migration, or bug fix
- **What stability promise exists?** Internal-only, versioned public API, or "best effort"
- **What auth model already exists?** Session cookies, JWT bearer, API keys, OAuth/OIDC, or none yet
- **What house style already exists?** Error format, pagination shape, versioning scheme, auth boundary, DTO naming

If the user asks to "just add an endpoint", inspect the surrounding service first. Most bad API
work happens when one route lands with a different error model, auth rule, pagination shape, or
DTO style than the rest of the service.

### Step 2: Choose the framework pattern

Pick the framework that matches the codebase and team constraints. Do not switch frameworks for fashion.

| Framework | Best fit | Watch for |
|-----------|----------|-----------|
| **FastAPI** | Python services with typed request/response models and strong OpenAPI output | Leaking ORM models directly, async confusion, piling business logic into route functions |
| **Express** | Thin Node.js services, custom middleware stacks, existing mature codebases | No built-in structure, validation scattered across middleware, inconsistent error handling |
| **NestJS** | Larger TypeScript services that benefit from modules, guards, pipes, interceptors, and DI | Over-abstraction, decorator-heavy indirection, hiding simple flows behind too many layers |

Framework rules:
- **FastAPI** - keep dependencies explicit, use response models, and centralize exception handling
- **Express** - keep routing, validation, auth, and business logic separated; add one error middleware path
- **NestJS** - keep controllers thin, move auth into guards, validation into pipes, and cross-cutting behavior into interceptors or filters

### Step 3: Design the contract first

Define the API contract before writing handlers:

For changes to an existing service, match the current URL, error, pagination, and auth house
style unless the task explicitly includes a migration.

1. Pick resource shapes and URIs
2. Choose methods and status codes
3. Define request and response schemas
4. Define error shapes
5. Decide pagination, filtering, sorting, and versioning rules
6. Only then wire the framework implementation

Prefer:
- Noun-based resources: `/users/{userId}/sessions`
- Predictable list endpoints: `GET /orders?cursor=...&limit=...&status=paid`
- Explicit write semantics: `POST` for create/commands, `PUT` for full replacement, `PATCH` for partial update, `DELETE` for delete
- Explicit retry semantics for command endpoints like `POST /orders/{orderId}/cancel`
- One canonical error model across the whole service

Read `references/http-api-patterns.md` for method semantics, pagination, idempotency, and versioning rules.

### Step 4: Design auth around the client, not around JWT hype

Start from the client type:

| Client | Default choice | Why |
|--------|----------------|-----|
| **First-party browser app** | Session cookie or BFF/token-mediating backend | Keeps tokens off the browser as much as possible |
| **Native/mobile app** | OAuth/OIDC authorization code + PKCE | Current standard path for public clients |
| **Third-party integrator** | OAuth/OIDC or scoped API keys if OAuth is overkill | Explicit delegation and revocation story |
| **Internal service-to-service** | Platform identity or short-lived service credentials | Avoid user-style auth flows between services |

Auth rules:
- Use sessions by default for first-party web apps unless there is a clear reason not to
- Use bearer tokens when the client really is a token-holding client
- Treat API keys as machine credentials, not as a universal auth shortcut
- Define scope or role boundaries at the API boundary, not ad hoc inside random handlers
- If the browser app talks to third-party identity providers, follow authorization code + PKCE and current browser-app guidance rather than resurrecting implicit flow patterns

BFF token mediation (first-party browser app calling an external API):
```
Browser -> BFF (session cookie) -> BFF attaches Bearer token -> Upstream API
```
The BFF holds the access token server-side; the browser never sees it.

Read `references/auth-and-session-patterns.md` for sessions, bearer tokens, OAuth, BFF, refresh tokens, and machine auth.

### Step 5: Implement the framework surface

Convert the contract into framework code without letting the framework dictate the contract.

**FastAPI**
- Define Pydantic models for requests and responses
- Use dependency injection for auth, DB/session acquisition, and shared request context
- Register exception handlers for consistent RFC 9457 output
- Keep route handlers thin; move business rules into services or domain modules

**Express**
- Validate inputs before controller logic
- Attach auth and request context in middleware
- Use one shared error-handling middleware path
- Keep controllers as transport adapters, not the place where every rule in the system lives

**NestJS**
- Use DTO classes for transport boundaries
- Put validation in pipes and auth in guards
- Use exception filters or interceptors to normalize response and error behavior
- Keep module boundaries meaningful; one module per vague concept is not architecture

### Step 6: Validate behavior and docs

Before returning the result:
- Compare OpenAPI docs against the real routes
- Verify auth requirements per endpoint
- Check all non-2xx responses, not just the happy path
- Verify list endpoints under empty, partial, and end-of-cursor states
- Check retries and duplicate submissions for create/payment/webhook paths
- Check repeat-call behavior for command endpoints (`cancel`, `resend`, `approve`) instead of leaving retries implicit
- Compare new endpoints with neighboring endpoints for naming, DTO shape, pagination params, and error consistency
- Route follow-up testing work to **testing** and follow-up security review to **security-audit**

---

## Contract Guardrails

### Versioning

- Prefer additive change over version churn
- Version only when you need a breaking change
- Keep one versioning scheme for the service: path versioning (`/v1/...`) is the clearest default for public APIs
- Do not mix path versioning, header versioning, and ad hoc `?version=` query params in one API

### OpenAPI authoring

- OpenAPI `3.2.0` is the current spec, but much of the framework and Swagger ecosystem still centers on `3.1.x`
- Default to authoring for `3.1` compatibility unless the actual toolchain in the project proves `3.2` support end-to-end
- Do not advertise `3.2` features in generated specs just because the top-level standard moved

### Error model

- Prefer RFC 9457 problem details with stable `type`, `title`, `status`, and domain-specific extension fields
- Do not return one error shape from validation, another from auth, and a third from business rules
- Never leak raw stack traces or ORM internals to clients

Minimal RFC 9457 problem detail response:
```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Account balance is $10.00; transfer requires $50.00."
}
```

Status code decision matrix (pick the narrowest correct code):

| Scenario | Code | Notes |
|----------|------|-------|
| Malformed JSON, missing required field, wrong type | `400` | Client request is syntactically wrong |
| Well-formed input but fails domain rule (insufficient funds, invalid state) | `422` | Semantic validation |
| No credentials, expired token | `401` | Include `WWW-Authenticate` header |
| Authenticated but not permitted | `403` | Do not challenge for credentials |
| Resource does not exist, or exists but caller must not know | `404` | Pick one policy per resource and keep it |
| Write conflicts with current state (stale ETag, duplicate unique key) | `409` | Problem detail should name the conflict |
| Idempotency-Key reused with a different body | `422` | Not `409` - the key contract is broken |
| Too many requests | `429` | Include `Retry-After` |
| Unhandled server error | `500` | Never leak stack traces in the body |

FastAPI exception handler wiring for consistent problem+json:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        media_type="application/problem+json",
        content={
            "type": "https://api.example.com/errors/validation",
            "title": "Invalid request",
            "status": 400,
            "errors": exc.errors(),
        },
    )
```

### Pagination and filtering

- Offset pagination is fine for small, stable backoffice lists
- Cursor pagination is the default for user-facing or high-write collections
- Sort order must be stable and documented
- Filter names should reflect resource fields or clear domain concepts, not internal SQL column names

### Idempotency and retries

- Define idempotency for writes that clients or gateways may retry
- Use explicit idempotency keys for payment-like or request-replay-prone operations
- Distinguish "request accepted" from "side effect completed" when async workflows exist

Idempotency key header pattern (Express/NestJS):
```typescript
const key = req.headers['idempotency-key'];
if (key) {
  const cached = await cache.get(`idem:${key}`);
  if (cached) return res.status(cached.status).json(cached.body);
}
// ... execute, then store result keyed by idempotency-key before returning
```

Idempotency key header pattern (FastAPI):
```python
from fastapi import Header, HTTPException

async def create_order(
    body: OrderCreate,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key:
        cached = await cache.get(f"idem:{idempotency_key}")
        if cached:
            return JSONResponse(status_code=cached["status"], content=cached["body"])
    result = await orders.create(body)
    if idempotency_key:
        await cache.set(f"idem:{idempotency_key}", {"status": 201, "body": result}, ttl=86400)
    return result
```

Cursor pagination response envelope:
```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTIzfQ",
  "has_more": true
}
```
Decode the cursor server-side (`WHERE id > :cursor_id ORDER BY id LIMIT :limit`). Never expose raw DB offsets or row numbers in the cursor.

Opaque cursor encode/decode (FastAPI, HMAC-signed to prevent client tampering):
```python
import base64, hmac, hashlib, json, os

SECRET = os.environ["CURSOR_SECRET"].encode()

def encode_cursor(payload: dict) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    sig = base64.urlsafe_b64encode(hmac.new(SECRET, body, hashlib.sha256).digest()[:8]).rstrip(b"=")
    return f"{body.decode()}.{sig.decode()}"

def decode_cursor(token: str) -> dict:
    body, sig = token.split(".", 1)
    expected = base64.urlsafe_b64encode(hmac.new(SECRET, body.encode(), hashlib.sha256).digest()[:8]).rstrip(b"=").decode()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("invalid cursor")
    return json.loads(base64.urlsafe_b64decode(body + "=="))
```
Clients treat `next_cursor` as opaque; the server controls shape and can change it without a breaking contract.

### Graceful shutdown and rolling deploys

Rolling deploys send SIGTERM to old instances while new ones come up. Handle it on the API side or expect 502s under load:

- Trap SIGTERM, stop accepting new connections, drain in-flight requests, then exit. FastAPI/Uvicorn: configure `--timeout-graceful-shutdown` (default 30s); Express 5: `server.close()` then `server.closeAllConnections()` after the drain window; NestJS: `app.enableShutdownHooks()` plus `onApplicationShutdown` handlers
- Keep the app-side shutdown window shorter than the orchestrator's termination grace (Kubernetes default 30s). `app_shutdown < terminationGracePeriodSeconds` or the kernel kills in-flight work
- Set HTTP keep-alive timeout shorter than any upstream idle timeout (load balancer, ingress). If the LB holds a connection the server already closed, the next request hits a dead socket. Typical safe pair: server keep-alive 65s behind an LB with 60s idle
- Add a readiness probe that flips to failing on SIGTERM before the drain starts. The orchestrator stops routing new traffic while in-flight requests finish

## What NOT to Force

- Do not force cursor pagination onto every small internal list or backoffice table
- Do not cut `/v2` just because a new field got added
- Do not insist on OAuth for every internal automation path if scoped API keys or platform identity fit better
- Do not push first-party browser apps toward bearer-token-in-local-storage patterns because "JWT auth" sounds modern
- Do not turn simple Express services into pseudo-enterprise architectures with needless layers and decorators

---

## Reference Files

- `references/http-api-patterns.md` - resource design, method semantics, status codes, versioning, pagination, filtering, idempotency
- `references/auth-and-session-patterns.md` - sessions vs bearer tokens, OAuth/OIDC, BFF, refresh tokens, machine clients

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** BACKEND-API
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/backend-api/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **databases** - schema design, query tuning, migrations, and persistence concerns behind the API
- **code-review** - correctness bugs, logic errors, and non-API-specific review findings
- **security-audit** - auth bypasses, OWASP findings, secrets, and security review after the API design exists
- **testing** - route, integration, contract, and end-to-end verification
- **docker** - containerizing API services
- **kubernetes** - deploying API services on clusters
- **networking** - reverse proxies, TLS termination, CORS-adjacent network boundaries, and gateway behavior
- **ci-cd** - delivery pipelines for API services
- **mcp** - MCP-specific HTTP servers and auth patterns

## Rules

1. **Contract before handlers.** Design the resource model, schemas, errors, and auth boundary before writing route code.
2. **Do not let transport leak persistence.** Database tables, ORM entities, and internal enums are not public API contracts.
3. **Pick one error format.** Prefer RFC 9457 and apply it consistently.
4. **Use current auth guidance.** Authorization code + PKCE for public OAuth clients, sessions or BFF patterns for first-party browser apps, no implicit flow, no password grant.
5. **Keep framework structure boring.** Thin controllers or routes, explicit validation, explicit auth, centralized error handling.
6. **Backward compatibility is a feature.** New fields are cheap; breaking clients is expensive.
7. **Write for real retries.** Assume clients, proxies, and job runners will replay requests.
8. **Keep scope on HTTP APIs.** When the problem is GraphQL or gRPC-specific, say so and stop pretending the same rules apply.
9. **Match service conventions unless migrating them.** A one-off endpoint with a different error, auth, or pagination model is usually a contract bug.
