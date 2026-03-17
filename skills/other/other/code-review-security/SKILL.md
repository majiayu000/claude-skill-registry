---
name: code-review-security
description: >-
  Security-focused code review checklist and automated scanning patterns. Use when
  reviewing pull requests for security issues, auditing authentication/authorization
  code, checking for OWASP Top 10 vulnerabilities, or validating input sanitization.
  Covers SQL injection prevention, XSS protection, CSRF tokens, authentication flow
  review, secrets detection, dependency vulnerability scanning, and secure coding
  patterns for Python (FastAPI) and React. Does NOT cover deployment security (use
  docker-best-practices) or incident handling (use incident-response).
license: MIT
compatibility: 'Python 3.12+, FastAPI, React, TypeScript'
metadata:
  author: security-team
  version: '1.0.0'
  sdlc-phase: code-review
allowed-tools: Read Grep Glob Write Bash(python:*) Bash(npm:*)
context: fork
---

# Code Review Security

## When to Use

Activate this skill when:
- Reviewing pull requests for security vulnerabilities
- Auditing authentication or authorization code changes
- Reviewing code that handles user input, file uploads, or external data
- Checking for OWASP Top 10 vulnerabilities in new features
- Validating that secrets are not committed to the repository
- Scanning dependencies for known vulnerabilities
- Reviewing API endpoints that expose sensitive data

**Output:** Write findings to `security-review.md` with severity, file:line, description, and recommendations.

Do NOT use this skill for:
- Deployment infrastructure security (use `docker-best-practices`)
- Incident response procedures (use `incident-response`)
- General code quality review without security focus (use `pre-merge-checklist`)
- Writing implementation code (use `python-backend-expert` or `react-frontend-expert`)

## Instructions

### OWASP Top 10 Checklist

Review every PR against the OWASP Top 10 (2021 edition). Each category below includes specific checks for Python/FastAPI and React codebases.

---

#### A01: Broken Access Control

**What to look for:**
- Missing authorization checks on endpoints
- Direct object reference without ownership verification
- Endpoints that expose data without role-based filtering
- Missing `Depends()` for auth on new routes

**Python/FastAPI checks:**
```python
# BAD: No authorization check -- any authenticated user can access any user
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await user_repo.get(user_id)

# GOOD: Verify the requesting user owns the resource or is admin
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return await user_repo.get(user_id)
```

**Review checklist:**
- [ ] Every route has authentication (`Depends(get_current_user)`)
- [ ] Resource access is verified against the requesting user
- [ ] Admin-only endpoints check `role == "admin"`
- [ ] List endpoints filter by user ownership (unless admin)
- [ ] No IDOR (Insecure Direct Object Reference) vulnerabilities

---

#### A02: Cryptographic Failures

**What to look for:**
- Passwords stored in plaintext or with weak hashing
- Sensitive data in logs or error messages
- Hardcoded secrets, API keys, or tokens
- Weak JWT configuration

**Python checks:**
```python
# BAD: Weak password hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD: Use bcrypt via passlib
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = pwd_context.hash(password)

# BAD: Secret in code
SECRET_KEY = "my-super-secret-key-123"

# GOOD: Secret from environment
SECRET_KEY = os.environ["SECRET_KEY"]
```

**Review checklist:**
- [ ] Passwords hashed with bcrypt (never MD5, SHA1, or plaintext)
- [ ] JWT secret loaded from environment, not hardcoded
- [ ] Sensitive data excluded from logs (passwords, tokens, PII)
- [ ] HTTPS enforced for all external communication
- [ ] No secrets in source code (check `.env.example` has placeholders only)

---

#### A03: Injection

**What to look for:**
- Raw SQL queries with string interpolation
- `eval()`, `exec()`, `compile()` with user input
- `subprocess` calls with `shell=True`
- Template injection

**Python checks:**
```python
# BAD: SQL injection via string formatting
query = f"SELECT * FROM users WHERE email = '{email}'"
db.execute(text(query))

# GOOD: Parameterized query
db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})

# GOOD: SQLAlchemy ORM (always parameterized)
user = db.query(User).filter(User.email == email).first()

# BAD: Command injection
subprocess.run(f"convert {filename}", shell=True)

# GOOD: Pass arguments as a list
subprocess.run(["convert", filename], shell=False)

# BAD: Code execution with user input
result = eval(user_input)

# GOOD: Never eval user input. Use ast.literal_eval for safe parsing.
result = ast.literal_eval(user_input)  # Only for literal structures
```

**Review checklist:**
- [ ] No raw SQL with string interpolation (use ORM or parameterized queries)
- [ ] No `eval()`, `exec()`, or `compile()` with external input
- [ ] No `subprocess.run(..., shell=True)` with dynamic arguments
- [ ] No `pickle.loads()` on untrusted data
- [ ] All user input validated by Pydantic schemas before use

---

#### A04: Insecure Design

**What to look for:**
- Missing rate limiting on authentication endpoints
- No account lockout after failed login attempts
- Missing CAPTCHA on public-facing forms
- Business logic flaws (e.g., negative amounts, self-privilege-escalation)

**Review checklist:**
- [ ] Rate limiting on login, registration, and password reset
- [ ] Account lockout or exponential backoff after 5+ failed attempts
- [ ] Business logic validates constraints (positive amounts, valid transitions)
- [ ] Sensitive operations require re-authentication

---

#### A05: Security Misconfiguration

**What to look for:**
- Debug mode enabled in production
- CORS configured with wildcard `*` origins
- Default credentials or admin accounts
- Verbose error messages exposing stack traces

**Python/FastAPI checks:**
```python
# BAD: Wide-open CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# GOOD: Explicit allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# BAD: Debug mode in production
app = FastAPI(debug=True)

# GOOD: Debug only in development
app = FastAPI(debug=settings.DEBUG)  # DEBUG=False in production
```

**Review checklist:**
- [ ] CORS origins are explicit (no wildcard in production)
- [ ] Debug mode disabled in production configuration
- [ ] Error responses do not expose stack traces or internal details
- [ ] Default admin credentials are changed or removed
- [ ] Security headers set (X-Content-Type-Options, X-Frame-Options, etc.)

---

#### A06: Vulnerable and Outdated Components

**Review checklist:**
- [ ] No known CVEs in Python dependencies (`pip-audit` or `safety check`)
- [ ] No known CVEs in npm dependencies (`npm audit`)
- [ ] Dependencies pinned to specific versions in lock files
- [ ] No deprecated packages still in use

---

#### A07: Identification and Authentication Failures

**What to look for:**
- Weak password policies
- Session tokens that do not expire
- Missing multi-factor authentication for admin actions
- JWT tokens without expiration

**Python checks:**
```python
# BAD: JWT without expiration
token = jwt.encode({"sub": user_id}, SECRET_KEY, algorithm="HS256")

# GOOD: JWT with expiration
token = jwt.encode(
    {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=30)},
    SECRET_KEY,
    algorithm="HS256",
)
```

**Review checklist:**
- [ ] JWT tokens have expiration (`exp` claim)
- [ ] Refresh tokens are stored securely and can be revoked
- [ ] Password policy enforces minimum length (12+) and complexity
- [ ] Session invalidation on password change or logout
- [ ] No user enumeration via login error messages

---

#### A08: Software and Data Integrity Failures

**Review checklist:**
- [ ] CI/CD pipeline validates artifact integrity
- [ ] No unsigned or unverified packages
- [ ] Deserialization of untrusted data uses safe methods (no `pickle.loads`)
- [ ] Database migrations are reviewed before execution

---

#### A09: Security Logging and Monitoring Failures

**Review checklist:**
- [ ] Authentication events are logged (login, logout, failed attempts)
- [ ] Authorization failures are logged with context
- [ ] Sensitive data is NOT included in logs (passwords, tokens, PII)
- [ ] Log entries include timestamp, user ID, IP address, action
- [ ] Alerting configured for suspicious patterns (brute force, unusual access)

---

#### A10: Server-Side Request Forgery (SSRF)

**What to look for:**
- User-supplied URLs used in server-side requests
- Redirect endpoints that accept arbitrary URLs

**Python checks:**
```python
# BAD: Fetch arbitrary URL from user input
url = request.query_params["url"]
response = httpx.get(url)  # SSRF: can access internal services

# GOOD: Validate URL against allowlist
ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}
parsed = urlparse(url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise HTTPException(400, "URL not allowed")
response = httpx.get(url)
```

**Review checklist:**
- [ ] No server-side requests to user-controlled URLs without validation
- [ ] URL allowlists used for external integrations
- [ ] Internal service URLs not exposed in error messages

---

### Python-Specific Security Checks

Beyond OWASP, review Python code for these patterns:

| Pattern | Risk | Fix |
|---------|------|-----|
| `eval(user_input)` | Remote code execution | Remove or use `ast.literal_eval` |
| `pickle.loads(data)` | Arbitrary code execution | Use JSON or `msgpack` |
| `subprocess.run(cmd, shell=True)` | Command injection | Pass args as list, `shell=False` |
| `yaml.load(data)` | Code execution | Use `yaml.safe_load(data)` |
| `os.system(cmd)` | Command injection | Use `subprocess.run([...])` |
| Raw SQL strings | SQL injection | Use ORM or parameterized queries |
| `hashlib.md5(password)` | Weak hashing | Use `bcrypt` via `passlib` |
| `jwt.decode(token, options={"verify_signature": False})` | Auth bypass | Always verify signature |
| `open(user_path)` | Path traversal | Validate path, use `pathlib.resolve()` |
| `tempfile.mktemp()` | Race condition | Use `tempfile.mkstemp()` |

### React-Specific Security Checks

| Pattern | Risk | Fix |
|---------|------|-----|
| `dangerouslySetInnerHTML` | XSS | Use text content or sanitize with DOMPurify |
| `javascript:` in href | XSS | Validate URLs, allow only `https:` |
| `window.location = userInput` | Open redirect | Validate against allowlist |
| Storing tokens in localStorage | Token theft via XSS | Use httpOnly cookies |
| Inline event handlers from data | XSS | Use React event handlers |
| `eval()` or `Function()` | Code execution | Remove entirely |
| Rendering user HTML | XSS | Use a sanitization library |

**React code review:**
```tsx
// BAD: XSS via dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userBio }} />

// GOOD: Sanitize first, or use text content
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userBio) }} />

// BETTER: Use text content when HTML is not needed
<p>{userBio}</p>

// BAD: javascript: URL
<a href={userLink}>Click</a>  // userLink could be "javascript:alert(1)"

// GOOD: Validate protocol
const safeHref = /^https?:\/\//.test(userLink) ? userLink : "#";
<a href={safeHref}>Click</a>
```

### Severity Classification

Classify each finding by severity for prioritization:

| Severity | Description | Examples | SLA |
|----------|-------------|----------|-----|
| **Critical** | Exploitable remotely, no auth needed, data breach | SQL injection, RCE, auth bypass | Block merge, fix immediately |
| **High** | Exploitable with auth, privilege escalation | IDOR, broken access control, XSS (stored) | Block merge, fix before release |
| **Medium** | Requires specific conditions to exploit | CSRF, XSS (reflected), open redirect | Fix within sprint |
| **Low** | Defense-in-depth, informational | Missing headers, verbose errors | Fix when convenient |
| **Info** | Best practice recommendations | Dependency updates, code style | Track in backlog |

### Finding Report Format

When reporting security findings, use this format for consistency:

```markdown
## Security Finding: [Title]

**Severity:** Critical | High | Medium | Low | Info
**Category:** OWASP A01-A10 or custom category
**File:** path/to/file.py:42
**CWE:** CWE-89 (if applicable)

### Description
Brief description of the vulnerability and its impact.

### Vulnerable Code
```python
# The problematic code
vulnerable_function(user_input)
```

### Recommended Fix
```python
# The secure alternative
safe_function(sanitize(user_input))
```

### Impact
What an attacker could achieve by exploiting this vulnerability.

### References
- Link to relevant OWASP page
- Link to relevant CWE entry
```

### Automated Scanning

Use `scripts/security-scan.py` to perform AST-based scanning for common vulnerability patterns in Python code. The script scans for:
- `eval()` / `exec()` / `compile()` calls
- `subprocess` with `shell=True`
- `pickle.loads()` on potentially untrusted data
- Raw SQL string construction
- `yaml.load()` without `Loader=SafeLoader`
- Hardcoded secret patterns (API keys, passwords)
- Weak hash functions (MD5, SHA1 for passwords)

Run: `python scripts/security-scan.py --path ./app --output-dir ./security-results`

**Dependency scanning (run separately):**
```bash
# Python dependencies
pip-audit --requirement requirements.txt --output json > dep-audit.json

# npm dependencies
npm audit --json > npm-audit.json
```

## Examples

### Example Review Comment (Critical)

> **SECURITY: SQL Injection (Critical, OWASP A03)**
>
> File: `app/repositories/user_repository.py:47`
>
> ```python
> query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
> ```
>
> This constructs a raw SQL query with string interpolation, allowing SQL injection.
> An attacker could input `'; DROP TABLE users; --` to destroy data.
>
> **Fix:** Use SQLAlchemy ORM filtering:
> ```python
> users = db.query(User).filter(User.name.ilike(f"%{search_term}%")).all()
> ```

### Example Review Comment (Medium)

> **SECURITY: Missing Rate Limiting (Medium, OWASP A04)**
>
> File: `app/routes/auth.py:12`
>
> The `/auth/login` endpoint has no rate limiting. An attacker could perform brute-force
> password attacks at unlimited speed.
>
> **Fix:** Add rate limiting middleware:
> ```python
> from slowapi import Limiter
> limiter = Limiter(key_func=get_remote_address)
>
> @router.post("/login")
> @limiter.limit("5/minute")
> async def login(request: Request, ...):
> ```

### Output File

Write security findings to `security-review.md`:

```markdown
# Security Review: [Feature/PR Name]

## Summary
- Critical: 0 | High: 1 | Medium: 2 | Low: 1

## Findings

### [CRITICAL] SQL Injection in user search
- **File:** app/routes/users.py:45
- **OWASP:** A03 Injection
- **Description:** Raw SQL with string interpolation
- **Recommendation:** Use SQLAlchemy ORM filtering

### [HIGH] Missing authorization check
...

## Passed Checks
- No hardcoded secrets found
- Dependencies up to date
```
