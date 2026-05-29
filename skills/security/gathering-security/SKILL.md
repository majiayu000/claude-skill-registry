---
name: gathering-security
description: The drum sounds. Spider, Raccoon, and Turtle gather for complete security work. Use when implementing auth, auditing security, or hardening code end-to-end.
---

# Gathering Security 🌲🕷️🦝🐢

The drum echoes in the shadows. The Spider weaves intricate webs of authentication, each strand placed with precision. The Raccoon rummages through every corner, finding what doesn't belong, cleaning what could harm. The Turtle moves with ancient patience, layering defense upon defense, testing every plate of the shell. Together they secure the forest — doors locked tight, secrets safe, paths protected, and the ground itself hardened against anything that comes.

## When to Summon

- Implementing authentication systems
- Adding OAuth or session management
- Security auditing before launch
- After security incidents
- Preparing for production deployment
- When auth, security audit, and deep hardening must work together
- Building a new feature that handles sensitive data
- Hardening existing code for defense in depth

---

## Grove Tools for This Gathering

Use `gw` and `gf` throughout. Quick reference for security work:

```bash
# Find security-relevant code patterns
gf --agent search "sanitize|escape|validate"  # Security patterns
gf --agent auth                     # Find auth code and middleware

# Verify security changes don't break anything
gw ci --affected --diagnose         # Run CI on affected packages
```

---

## The Gathering

```
SUMMON --> ORGANIZE --> EXECUTE --> VALIDATE --> COMPLETE
   |          |           |           |            |
Receive   Dispatch     Animals     Verify      Security
Request   Animals      Work        Check       Hardened
```

### Animals Mobilized

1. **🕷️ Spider** — Weave authentication webs with patient precision
2. **🦝 Raccoon** — Rummage for security risks and cleanup
3. **🐢 Turtle** — Harden with layered, defense-in-depth protection

---

### Phase 1: SUMMON

_The drum sounds. The shadows shift..._

Receive and parse the request:

**Clarify the Security Work:**

- Adding new auth provider? (OAuth, SSO)
- Securing routes and APIs?
- General security audit?
- Deep security hardening?
- Post-incident cleanup?
- Pre-production hardening?

**Error Codes as Security Posture:**
All errors MUST use Signpost codes — this is a security requirement, not just a convention:

- All server errors use codes from the appropriate catalog (`API_ERRORS`, `AUTH_ERRORS`, etc.)
- `userMessage` is always generic and warm — no technical details leak to clients
- `adminMessage` is detailed — stays in server logs only
- Auth errors NEVER reveal user existence ("Invalid credentials" — not "user not found")
- `logGroveError()` for all server errors — never `console.error` alone

**Scope Check:**

> "I'll mobilize a security gathering for: **[security work]**
>
> This will involve:
>
> - 🕷️ Spider weaving authentication
>   - OAuth/PKCE flow
>   - Session management
>   - Route protection
>   - Token handling
> - 🦝 Raccoon auditing security
>   - Secret scanning
>   - Vulnerability check
>   - Dependency audit
>   - Dead code removal
> - 🐢 Turtle hardening defenses
>   - Input/output validation
>   - Security headers & CSP
>   - Defense-in-depth enforcement
>   - Exotic attack vector testing
>   - Hardening report
>
> Proceed with the gathering?"

**Selective Mobilization:**
Not every gathering needs all three animals:

| Situation                            | Animals Needed                                    |
| ------------------------------------ | ------------------------------------------------- |
| New auth system + full security      | All three: Spider → Raccoon → Turtle              |
| Auth already exists, need hardening  | Raccoon → Turtle                                  |
| New feature, ensure secure by design | Turtle only (or Turtle → Raccoon)                 |
| Secrets leak / incident response     | Raccoon → Spider (rotate creds) → Turtle (verify) |
| Pre-production deploy                | Raccoon → Turtle                                  |

---

### Phase 2: ORGANIZE

_The animals take their positions in the shadows..._

Dispatch in sequence:

**Full Dispatch Order:**

```
Spider ──→ Raccoon ──→ Turtle
   │          │            │
   │          │            │
Weave      Audit       Harden
Auth       Secrets     Defenses
```

**Dependencies:**

- Spider must complete before Raccoon (needs auth to audit)
- Raccoon should complete before Turtle (clean first, then harden)
- May iterate: Turtle findings → Spider/Raccoon fixes → Turtle re-verify

**Iteration Cycle (When Vulnerabilities Found):**

```
┌──────────────────────────────────────────────────────────────────┐
│                   SECURITY ITERATION                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  🕷️ Spider ──► 🦝 Raccoon ──► 🐢 Turtle                       │
│  weaves auth    audits          hardens & tests                   │
│       ▲                              │                            │
│       │                              ▼                            │
│       │                     Deep vulnerabilities?                 │
│       │                        /          \                       │
│       │                     Yes            No                     │
│       │                      │              │                     │
│       │         ┌────────────┘              ▼                     │
│       │         ▼                     ✅ Hardened                 │
│       │    Auth issue?                                            │
│       │    /         \                                            │
│       │  Yes          No                                          │
│       │   │           │                                           │
│       └───┘    Raccoon/Turtle                                   │
│                fixes directly                                     │
└──────────────────────────────────────────────────────────────────┘
```

**Iteration Rules:**

- Turtle finds auth vulnerability → Spider patches → Turtle re-verifies
- Turtle finds non-auth vulnerability → Fix directly → Turtle re-verifies
- Raccoon finds secrets → Raccoon cleans → Turtle verifies no residual exposure
- Maximum 3 iterations per issue (if more needed, architectural review required)
- Each iteration focuses only on newly found/fixed items
- Document all iterations in final report

---

### Phase 3: EXECUTE

_The web is woven. The audit begins. The shell hardens..._

Execute each animal's phase:

**🕷️ SPIDER — WEAVE**

```
"Spinning the authentication threads..."

Phase: SPIN
- Choose auth pattern (OAuth 2.0 + PKCE, JWT, Session)
- Set up infrastructure (client registration, secrets)

Phase: CONNECT
- Implement OAuth flow (login/callback)
- Session/token management
- User info fetching

Phase: SECURE
- Route protection middleware
- CSRF protection
- Rate limiting
- Security headers

Phase: TEST
- Auth flow end-to-end
- Error handling
- Edge cases

Phase: BIND
- Documentation
- Environment variables
- Monitoring

Output:
- Working authentication system
- Protected routes
- Session management
```

**🦝 RACCOON — AUDIT**

```
"Rummaging through every corner..."

Phase: RUMMAGE
- Search for secrets in code
- Check git history
- Scan dependencies for vulnerabilities

Phase: INSPECT
- Validate auth implementation
- Check input validation
- Review access controls
- Examine error messages

Phase: SANITIZE
- Remove any secrets found
- Rotate exposed credentials
- Patch vulnerabilities

Phase: PURGE
- Clean git history if needed
- Remove dead code
- Clear old tokens

Phase: VERIFY
- Re-scan for secrets
- Verify fixes
- Install pre-commit hooks

Output:
- Security audit report
- Issues fixed
- Preventive measures in place
```

**🐢 TURTLE — HARDEN**

```
"Withdrawing to study the terrain..."

Phase: WITHDRAW
- Survey the attack surface
- Map all entry/exit points
- Catalog data flows
- Identify tech-stack-specific risks

Phase: LAYER
- Input validation (Zod schemas, allowlists)
- Output encoding (context-aware)
- Parameterized queries (zero concatenation)
- Type safety (strict mode, no 'any')
- Error handling (generic messages, no leaks)

Phase: FORTIFY
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- CORS strict configuration
- Session/cookie hardening
- CSRF enforcement
- Rate limiting
- Multi-tenant isolation
- File upload security
- Data protection (encryption, least privilege)

Phase: SIEGE
- Test for exotic attacks:
  Prototype pollution, timing attacks, race conditions,
  ReDoS, SSRF bypasses, CRLF injection, Unicode attacks,
  deserialization, postMessage vulns, WebSocket hijacking,
  CSS injection, SVG XSS, cache poisoning, HTTP verb
  tampering, second-order vulnerabilities, supply chain

Phase: SEAL
- Defense-in-depth compliance (2+ layers per critical function)
- Logging & monitoring verification
- Final scan for remaining issues
- Generate hardening report

Output:
- Defense-in-depth verified
- Exotic attack vectors tested
- Complete hardening report
```

---

### Phase 4: VALIDATE

_The web holds. The audit confirms. The shell endures..._

**Validation Checklist:**

- [ ] Spider: Auth flow works end-to-end
- [ ] Spider: Routes properly protected
- [ ] Spider: Sessions expire correctly
- [ ] Spider: CSRF protection active
- [ ] Raccoon: No secrets in codebase
- [ ] Raccoon: Dependencies up to date
- [ ] Raccoon: No sensitive data in logs
- [ ] Raccoon: Pre-commit hooks installed
- [ ] Turtle: Input validation on all entry points
- [ ] Turtle: Output encoding on all exit points
- [ ] Turtle: Security headers complete
- [ ] Turtle: CSP enforced (nonce-based)
- [ ] Turtle: CORS restricted to exact origins
- [ ] Turtle: Defense-in-depth verified (2+ layers per critical function)
- [ ] Turtle: Exotic attack vectors tested and clear
- [ ] Turtle: Multi-tenant isolation verified (if applicable)

**Security Test Cases:**

```
Authentication:
[ ] Login redirects to provider
[ ] Callback exchanges code for tokens
[ ] Sessions created correctly
[ ] Logout clears sessions server-side
[ ] Expired tokens rejected
[ ] Session fixation prevented

Authorization:
[ ] Protected routes require auth
[ ] Admin routes check roles
[ ] API endpoints verify tokens
[ ] Users can't access others' data (IDOR tested)
[ ] Horizontal escalation prevented
[ ] Vertical escalation prevented

Hardening:
[ ] SQL injection prevented (parameterized queries)
[ ] XSS prevented (output encoding + CSP)
[ ] CSRF prevented (tokens + SameSite cookies)
[ ] File uploads sanitized (type + size + rename)
[ ] Rate limiting active on all sensitive endpoints
[ ] Prototype pollution vectors blocked
[ ] Timing attacks mitigated (constant-time comparison)
[ ] Race conditions prevented (atomic operations)
[ ] SSRF prevented (URL allowlist, no redirect following)
```

---

### Phase 5: COMPLETE

_The gathering ends. The forest is fortified..._

**Completion Report:**

```markdown
## GATHERING SECURITY COMPLETE

### Security Work: [Description]

### Animals Mobilized

🕷️ Spider → 🦝 Raccoon → 🐢 Turtle

### Authentication Implemented

- **Provider:** [OAuth 2.0 / GitHub / Google / etc.]
- **Flow:** [PKCE / Authorization Code]
- **Session Type:** [Token / Session Cookie]
- **Routes Protected:** [count]

### Security Audit Results

- Secrets found: [count] (all rotated/removed)
- Dependencies patched: [count]
- Dead code removed: [lines]
- Pre-commit hooks: Installed

### Hardening Applied

| Defense Layer    | Status          | Details                                |
| ---------------- | --------------- | -------------------------------------- |
| Input Validation | [PASS/FAIL]     | Zod schemas on all endpoints           |
| Output Encoding  | [PASS/FAIL]     | Context-aware, DOMPurify for rich text |
| SQL Injection    | [PASS/FAIL]     | All queries parameterized              |
| Security Headers | [PASS/FAIL]     | CSP, HSTS, X-Frame, etc.               |
| CORS             | [PASS/FAIL]     | Exact origin allowlist                 |
| Session Security | [PASS/FAIL]     | HttpOnly, Secure, SameSite             |
| CSRF Protection  | [PASS/FAIL]     | Tokens + SameSite                      |
| Rate Limiting    | [PASS/FAIL]     | Per-endpoint limits configured         |
| Multi-Tenant     | [PASS/FAIL/N/A] | Tenant scoping verified                |
| File Uploads     | [PASS/FAIL/N/A] | Type/size/rename enforced              |

### Exotic Attack Vectors Tested

| Vector              | Status        |
| ------------------- | ------------- |
| Prototype Pollution | [CLEAR/FOUND] |
| Timing Attacks      | [CLEAR/FOUND] |
| Race Conditions     | [CLEAR/FOUND] |
| ReDoS               | [CLEAR/FOUND] |
| SSRF                | [CLEAR/FOUND] |
| Unicode Attacks     | [CLEAR/FOUND] |
| Cache Poisoning     | [CLEAR/FOUND] |
| SVG XSS             | [CLEAR/FOUND] |

### Defense-in-Depth Compliance

- **Layers verified:** [X/5] (Network, Application, Data, Infrastructure, Process)
- **Critical functions with 2+ layers:** [X/Y]

### Vulnerabilities Found & Fixed

| Severity | Count | Status           |
| -------- | ----- | ---------------- |
| CRITICAL | [n]   | All fixed        |
| HIGH     | [n]   | All fixed        |
| MEDIUM   | [n]   | [fixed/accepted] |
| LOW      | [n]   | [fixed/deferred] |

### Files Created/Modified

- Auth routes: [files]
- Middleware: [files]
- Configuration: [files]
- Security tests: [files]

_Woven tight, audited clean, hardened deep — the forest endures._ 🌲
```

---

## Example Gathering

**User:** "/gathering-security Add GitHub OAuth, audit everything, and harden for production"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing full security gathering: GitHub OAuth + audit + hardening. All three animals needed."

2. 🌲 **ORGANIZE** — "Spider implements auth → Raccoon audits for secrets/vulns → Turtle hardens everything"

3. 🌲 **EXECUTE** —
   - 🕷️ Spider: "OAuth client registered, PKCE flow implemented, sessions working, routes protected"
   - 🦝 Raccoon: "No secrets found, 2 dependency vulns patched, dead debug endpoint removed"
   - 🐢 Turtle: "CSP configured with nonces, CORS locked to exact origins, all inputs validated with Zod, constant-time token comparison added, prototype pollution vector in config merge fixed, defense-in-depth verified at 3 layers per critical function"

4. 🌲 **VALIDATE** — "Auth works, audit clean, hardening verified, all exotic vectors tested clear"

5. 🌲 **COMPLETE** — "GitHub OAuth live, secrets clean, shell hardened. The forest endures."

---

## Quick Decision Guide

| Situation                        | Animals to Mobilize                 |
| -------------------------------- | ----------------------------------- |
| New auth + full security         | Spider → Raccoon → Turtle           |
| Auth exists, need deep hardening | Raccoon → Turtle                    |
| New feature, secure by design    | Turtle (optionally + Raccoon)       |
| Incident response                | Raccoon → Spider → Turtle           |
| Pre-production deploy            | Raccoon → Turtle                    |
| Auth-only work                   | Spider → Raccoon (no Turtle needed) |

---

_Woven tight, audited clean, hardened deep — the forest endures._ 🌲
