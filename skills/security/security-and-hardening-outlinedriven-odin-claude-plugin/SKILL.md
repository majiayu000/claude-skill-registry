---
name: security-and-hardening
description: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
---

# Security and Hardening

## Overview

Security-first development. Three standing constraints: treat every external input as hostile until validated, keep every secret out of code and logs, and check authorization on every protected action. Security is a property of each line that touches user data, authentication, or external systems, built in during construction rather than retrofitted afterward.

## When to Use

- Building anything that accepts user input
- Implementing authentication or authorization
- Storing or transmitting sensitive data
- Integrating with external APIs or services
- Adding file uploads, webhooks, or callbacks
- Handling payment or PII data

## Process: Threat Model First

A control added without a threat model is a guess. Before hardening, spend five minutes as the attacker:

1. **Map the trust boundaries.** Where does untrusted data cross into the system? HTTP requests, form fields, file uploads, webhooks, third-party APIs, message queues, and **LLM output**. Every boundary is attack surface.
2. **Name the assets.** What is worth stealing or breaking? Credentials, PII, payment data, admin actions, money movement.
3. **Run STRIDE over each boundary** — a lens, not a ceremony:

| Threat | Ask | Typical mitigation |
|---|---|---|
| **S**poofing | Can someone impersonate a user/service? | Authentication, signature verification |
| **T**ampering | Can data be altered in transit or at rest? | Integrity checks, parameterized queries, HTTPS |
| **R**epudiation | Can an action be denied later? | Audit logging of security events |
| **I**nformation disclosure | Can data leak? | Encryption, field allowlists, generic errors |
| **D**enial of service | Can it be overwhelmed? | Rate limiting, input size caps, timeouts |
| **E**levation of privilege | Can a user gain rights they shouldn't? | Authorization checks, least privilege |

4. **Write abuse cases next to use cases.** For each feature, ask "how would I misuse this?" — then make that the first test.

If you cannot name a feature's trust boundaries, you cannot secure it. This is OWASP **A04: Insecure Design**; design flaws, not code typos, drive most breaches.

## The Three-Tier Boundary System

### Always Do (No Exceptions)

- **Validate all external input** at the system boundary (API routes, form handlers)
- **Parameterize all database queries** — never concatenate user input into SQL
- **Encode output** to prevent XSS (use framework auto-escaping; do not bypass it)
- **Use HTTPS** for all external communication
- **Hash passwords** with bcrypt/scrypt/argon2 (never store plaintext)
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for sessions
- **Run the dependency audit** (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, or equivalent) before every release

### Ask First (Requires Human Approval)

- Adding new authentication flows or changing auth logic
- Storing new categories of sensitive data (PII, payment info)
- Adding new external service integrations
- Changing CORS configuration
- Adding file upload handlers
- Modifying rate limiting or throttling
- Granting elevated permissions or roles

### Never Do

- **Never commit secrets** to version control (API keys, passwords, tokens)
- **Never log sensitive data** (passwords, tokens, full credit card numbers)
- **Never trust client-side validation** as a security boundary
- **Never disable security headers** for convenience
- **Never feed user data to dynamic execution or raw markup** (`eval`, `innerHTML`, `exec`, template injection)
- **Never store sessions in client-accessible storage** (auth tokens in localStorage)
- **Never expose stack traces** or internal error details to users

## OWASP Top 10 Prevention Patterns

These are prevention patterns, not a ranking. For the 2021 ordering, see the quick-reference table in `references/security-checklist.md`. Examples appear in two language families; the mitigation is the same across stacks.

### Injection (SQL, NoSQL, OS Command)

```typescript
// BAD: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// GOOD: ORM with parameterized input
const user = await prisma.user.findUnique({ where: { id: userId } });
```

```python
# BAD: SQL injection via string formatting
cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")

# GOOD: parameterized query (driver binds the value)
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# GOOD: ORM with parameterized input
user = session.query(User).filter(User.id == user_id).one_or_none()
```

The same rule holds for OS commands: pass an argument vector (`execFile`, `subprocess.run([...])`), never a shell string built from input.

### Broken Authentication

```typescript
import { hash, compare } from 'bcrypt';

const SALT_ROUNDS = 12;
const hashedPassword = await hash(plaintext, SALT_ROUNDS);
const isValid = await compare(plaintext, hashedPassword);

// Session cookie flags
app.use(session({
  secret: process.env.SESSION_SECRET,  // from environment, not code
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,     // not readable by JavaScript
    secure: true,       // HTTPS only
    sameSite: 'lax',    // CSRF protection
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
  },
}));
```

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
hashed_password = ph.hash(plaintext)
try:
    ph.verify(hashed_password, plaintext)
    is_valid = True
except VerifyMismatchError:
    is_valid = False

# Session cookie flags (framework-agnostic)
SESSION_COOKIE = dict(
    httponly=True,   # not readable by JavaScript
    secure=True,     # HTTPS only
    samesite="Lax",  # CSRF protection
    max_age=24 * 60 * 60,
)
```

The secret comes from the environment in both cases; never hard-code it.

### Cross-Site Scripting (XSS)

```typescript
// BAD: rendering user input as HTML
element.innerHTML = userInput;

// GOOD: framework auto-escaping (React escapes by default)
return <div>{userInput}</div>;

// If you MUST render HTML, sanitize first
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
```

```python
# BAD: concatenating input into markup (autoescape bypassed)
return render_template_string("<div>" + user_input + "</div>")

# GOOD: template autoescaping (Jinja2 escapes {{ ... }} by default)
return render_template("page.html", body=user_input)

# If you MUST allow HTML, sanitize first
import bleach
clean = bleach.clean(user_input)
```

The bypass paths (`innerHTML`, `|safe`, `mark_safe`, `render_template_string` with concatenation) are where XSS enters.

### Broken Access Control

Check authorization, not just authentication. Verify the caller owns the resource.

```typescript
app.patch('/api/tasks/:id', authenticate, async (req, res) => {
  const task = await taskService.findById(req.params.id);

  if (task.ownerId !== req.user.id) {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', message: 'Not authorized to modify this task' }
    });
  }

  const updated = await taskService.update(req.params.id, req.body);
  return res.json(updated);
});
```

```python
@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, body: TaskUpdate, user=Depends(authenticate)):
    task = await task_service.find_by_id(task_id)

    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    return await task_service.update(task_id, body)
```

Missing ownership checks are IDOR: authenticated, but acting on another user's row.

### Security Misconfiguration

```typescript
import helmet from 'helmet';
app.use(helmet());

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],  // tighten if possible
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
  },
}));

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true,
}));
```

```python
from fastapi.middleware.cors import CORSMiddleware

SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'self'; script-src 'self'",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
}

@app.middleware("http")
async def set_security_headers(request, call_next):
    response = await call_next(request)
    response.headers.update(SECURITY_HEADERS)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
)
```

CORS is an allowlist of known origins. Never reflect arbitrary origins and never pair `*` with credentials.

### Sensitive Data Exposure

```typescript
// Strip sensitive fields from API responses
function sanitizeUser(user: UserRecord): PublicUser {
  const { passwordHash, resetToken, ...publicFields } = user;
  return publicFields;
}

const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error('STRIPE_API_KEY not configured');
```

```python
from pydantic import BaseModel

# Response model defines exactly which fields leave the boundary
class PublicUser(BaseModel):
    id: str
    email: str
    # passwordHash / reset_token are absent, so they cannot be serialized

API_KEY = os.environ.get("STRIPE_API_KEY")
if not API_KEY:
    raise RuntimeError("STRIPE_API_KEY not configured")
```

Default to an explicit allowlist of returned fields rather than denylisting secrets one by one.

### Server-Side Request Forgery (SSRF)

Any time the server fetches a URL the user influenced — webhooks, "import from URL", image proxies, link previews — an attacker can aim it at internal services (cloud metadata, `localhost`, private IPs).

```typescript
// BAD: fetch whatever the user gives you
await fetch(req.body.webhookUrl);

// GOOD: allowlist scheme + host, reject if ANY resolved IP is private, forbid redirects
import { lookup } from 'node:dns/promises';
import ipaddr from 'ipaddr.js';

const ALLOWED_HOSTS = new Set(['hooks.example.com']);

async function assertSafeUrl(raw: string): Promise<URL> {
  const url = new URL(raw);
  if (url.protocol !== 'https:') throw new Error('https only');
  if (!ALLOWED_HOSTS.has(url.hostname)) throw new Error('host not allowed');
  const addrs = await lookup(url.hostname, { all: true });
  if (addrs.some((a) => ipaddr.parse(a.address).range() !== 'unicast')) {
    throw new Error('private/reserved IP');
  }
  return url;
}

await fetch(await assertSafeUrl(req.body.webhookUrl), { redirect: 'error' });
```

```python
# GOOD: allowlist scheme + host, reject if ANY resolved IP is non-global
import ipaddress, socket
from urllib.parse import urlparse

ALLOWED_HOSTS = {"hooks.example.com"}

def assert_safe_url(raw: str) -> str:
    url = urlparse(raw)
    if url.scheme != "https":
        raise ValueError("https only")
    if url.hostname not in ALLOWED_HOSTS:
        raise ValueError("host not allowed")
    for *_, sockaddr in socket.getaddrinfo(url.hostname, 443):
        if not ipaddress.ip_address(sockaddr[0]).is_global:
            raise ValueError("private/reserved IP")
    return raw
```

The non-unicast / non-global check covers loopback, link-local `169.254.169.254` (cloud metadata, the #1 SSRF target), private, and unique-local ranges across IPv4 and IPv6.

**Caveat — this still has a TOCTOU gap.** The HTTP client resolves DNS again after the check, so an attacker using a short-TTL record can rebind to an internal IP between validation and connection. For high-risk surfaces, resolve once and connect to the pinned IP, or put a request-filtering proxy in front of all outbound fetches.

## Input Validation Patterns

### Schema Validation at Boundaries

```typescript
import { z } from 'zod';

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: { code: 'VALIDATION_ERROR', message: 'Invalid input', details: result.error.flatten() },
    });
  }
  const task = await taskService.create(result.data);  // typed and validated
  return res.status(201).json(task);
});
```

```python
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, ValidationError

class CreateTask(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[datetime] = None

@app.post("/api/tasks", status_code=201)
async def create_task(raw: dict):
    try:
        data = CreateTask.model_validate(raw)  # typed and validated
    except ValidationError as e:
        raise HTTPException(422, detail={"code": "VALIDATION_ERROR", "details": e.errors()})
    return await task_service.create(data)
```

Validate at the boundary with an allowlist schema; reject anything that does not parse.

### File Upload Safety

```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: UploadedFile) {
  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new ValidationError('File type not allowed');
  }
  if (file.size > MAX_SIZE) {
    throw new ValidationError('File too large (max 5MB)');
  }
  // Don't trust the file extension — check magic bytes if critical
}
```

```python
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def validate_upload(file):
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError("File type not allowed")
    if file.size > MAX_SIZE:
        raise ValidationError("File too large (max 5MB)")
    # Don't trust the file extension — check magic bytes if critical
```

## Triaging Dependency Audit Results

Not every audit finding needs immediate action. Use this decision tree:

```
the dependency audit reports a vulnerability
├── Severity: critical or high
│   ├── Is the vulnerable code reachable in your app?
│   │   ├── YES --> Fix immediately (update, patch, or replace the dependency)
│   │   └── NO (dev-only dep, unused code path) --> Fix soon, but not a blocker
│   └── Is a fix available?
│       ├── YES --> Update to the patched version
│       └── NO --> Find a workaround, replace the dependency, or allowlist with a review date
├── Severity: moderate
│   ├── Reachable in production? --> Fix in the next release cycle
│   └── Dev-only? --> Fix when convenient, track in backlog
└── Severity: low
    └── Track and fix during regular dependency updates
```

**Key questions:**
- Is the vulnerable function actually called in your code path?
- Is the dependency a runtime dependency or dev-only?
- Is the vulnerability exploitable in your deployment context (e.g. a server-side flaw in a client-only app)?

When you defer a fix, document the reason and set a review date.

### Supply-Chain Hygiene

A vulnerability audit catches known CVEs; it will not catch a malicious or typosquatted package. Also:

- **Commit the lockfile and install reproducibly in CI** — `npm ci`, `pip install --require-hashes`, `cargo build --locked`, or the equivalent for your toolchain. No silent version drift.
- **Review new dependencies before adding them** — maintenance, download counts, and whether they earn their place. Every dependency is attack surface (OWASP **A06: Vulnerable Components**, **LLM03: Supply Chain**).
- **Be wary of install-time scripts** in unfamiliar packages (`postinstall`, `setup.py`, `build.rs`) — they run arbitrary code at install time.
- **Watch for typosquats** — `cross-env` vs `crossenv`, `requests` vs `request`, `python-dateutil` vs `dateutil`.

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                 // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
}));

// Stricter limit for auth endpoints
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,  // 10 attempts per 15 minutes
}));
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# General API rate limit
@app.get("/api/resource")
@limiter.limit("100/15minutes")
async def resource(request: Request):
    ...

# Stricter limit for auth endpoints
@app.post("/api/auth/login")
@limiter.limit("10/15minutes")
async def login(request: Request):
    ...
```

Always apply a tighter limit to authentication endpoints than to general traffic.

## Secrets Management

```
.env files:
  ├── .env.example  → committed (template with placeholder values)
  ├── .env          → NOT committed (contains real secrets)
  └── .env.local    → NOT committed (local overrides)

.gitignore must include:
  .env
  .env.local
  .env.*.local
  *.pem
  *.key
```

**Always check before committing:**
```bash
# Catch accidentally staged secrets
git diff --cached | grep -i "password\|secret\|api_key\|token"
```

**If a secret is ever committed, rotate it.** Deleting the line or rewriting history is not enough — assume it is compromised the moment it reaches a remote. Revoke and reissue the key first, then purge it from history.

## Securing AI / LLM Features

If the app calls an LLM — chatbots, summarizers, agents, RAG — it inherits a new attack surface. Map it to the [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/):

- **Treat all model output as untrusted input (LLM05: Improper Output Handling).** Never pass LLM output straight into `eval`, SQL, a shell, raw markup, or a file path. Validate and encode it exactly as you would raw user input.
- **Assume prompts can be hijacked (LLM01: Prompt Injection).** Untrusted text in the context window — a user message, a fetched web page, a PDF — can carry instructions. The system prompt is not a security boundary; enforce permissions in code, not in the prompt.
- **Keep secrets and other users' data out of prompts (LLM02 / LLM07).** Anything in the context can be echoed back. Do not place API keys, cross-tenant data, or the full system prompt where the model can repeat it.
- **Constrain tool and agent permissions (LLM06: Excessive Agency).** Scope tools to the minimum, require confirmation for destructive or irreversible actions, and validate every tool argument.
- **Bound consumption (LLM10: Unbounded Consumption).** Cap tokens, request rate, and loop/recursion depth so a crafted input cannot run up cost or hang the system.
- **Isolate retrieval data (LLM08: Vector and Embedding Weaknesses).** In RAG, treat the vector store as a trust boundary: partition embeddings per tenant so one user cannot retrieve another's data, and validate documents before indexing so poisoned content cannot steer answers.

```typescript
// BAD: trusting model output as a command or as markup
const sql = await llm.generate(`Write SQL for: ${userQuestion}`);
await db.query(sql);                                  // arbitrary query execution
container.innerHTML = await llm.reply(userMessage);  // stored XSS, via the model

// GOOD: model output is data — parse defensively, then validate, then encode
let intent;
try {
  intent = CommandSchema.parse(JSON.parse(await llm.replyJson(userMessage)));
} catch {
  throw new ValidationError('unexpected model output');
}
await runAllowlistedAction(intent.action, intent.params);
container.textContent = await llm.reply(userMessage);
```

```python
# BAD: trusting model output as a command or as markup
sql = llm.generate(f"Write SQL for: {user_question}")
db.execute(sql)  # arbitrary query execution

# GOOD: model output is data — parse defensively, then validate, then encode
try:
    intent = CommandSchema.model_validate_json(llm.reply_json(user_message))
except (ValueError, ValidationError):
    raise ValidationError("unexpected model output")
run_allowlisted_action(intent.action, intent.params)
```

## Security Review Checklist

```markdown
### Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (salt rounds ≥ 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
- [ ] HTML output is encoded/escaped
- [ ] Server-side URL fetches are allowlisted (no SSRF to internal services)

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses
- [ ] PII encrypted at rest (if applicable)

### Infrastructure
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] Dependencies audited for vulnerabilities
- [ ] Error messages don't expose internals

### Supply Chain
- [ ] Lockfile committed; CI uses a reproducible, locked install
- [ ] New dependencies reviewed (maintenance, downloads, install-time scripts)

### AI / LLM (if used)
- [ ] Model output treated as untrusted (no eval/SQL/raw-markup/shell)
- [ ] Secrets and other users' data kept out of prompts
- [ ] Tool/agent permissions scoped; destructive actions require confirmation
```

## See Also

Detailed security checklists and pre-commit verification steps: `references/security-checklist.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is an internal tool, security doesn't matter" | Internal tools get compromised. Attackers target the weakest link. |
| "We'll add security later" | Retrofitting security costs far more than building it in. Add it now. |
| "No one would try to exploit this" | Automated scanners will find it. Security by obscurity is not security. |
| "The framework handles security" | Frameworks provide tools, not guarantees. You still have to use them correctly. |
| "It's just a prototype" | Prototypes become production. Security habits from day one. |
| "Threat modeling is overkill here" | Five minutes of "how would I attack this?" prevents the design flaws no control can patch later. |
| "It's just LLM output, it's only text" | That "text" can be a SQL statement, a script tag, or a shell command. Treat it like any untrusted input. |

## Red Flags

- User input passed directly to database queries, shell commands, or HTML rendering
- Secrets in source code or commit history
- API endpoints without authentication or authorization checks
- Missing CORS configuration or wildcard (`*`) origins
- No rate limiting on authentication endpoints
- Stack traces or internal errors exposed to users
- Dependencies with known critical vulnerabilities
- Server fetches user-supplied URLs without an allowlist (SSRF)
- LLM/model output passed into a query, the DOM, a shell, or `eval`
- Secrets, PII, or the full system prompt placed inside an LLM context window

## Verification

After implementing security-relevant code:

- [ ] Dependency audit shows no critical or high vulnerabilities
- [ ] No secrets in source code or git history
- [ ] All user input validated at system boundaries
- [ ] Authentication and authorization checked on every protected endpoint
- [ ] Security headers present in response (check with browser DevTools)
- [ ] Error responses don't expose internal details
- [ ] Rate limiting active on auth endpoints
- [ ] Server-side URL fetches validated against an allowlist (no SSRF)
- [ ] LLM/model output validated and encoded before use (if AI features present)
