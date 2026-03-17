---
name: security-antipatterns-javascript
description: Code generation guard for Node.js/TypeScript/Next.js - prevents OWASP Top 10 vulnerabilities while writing code
version: "1.0.0"
allowed-tools: "Read"
metadata:
  short-description: Prevents OWASP Top 10 vulnerabilities in JavaScript/Node.js
---

# Security Anti-Patterns Guard for Node.js/TypeScript/Next.js

## When to Activate

Activate this skill when generating ANY code involving:
- Node.js backend code
- TypeScript applications
- Next.js (App Router or Pages Router)
- Express/Fastify APIs
- Database queries (Prisma, Drizzle, raw SQL, MongoDB)
- Authentication/authorization logic
- File uploads or user input handling
- API endpoints or Server Actions

## Critical Rules (Top 10)

1. **NEVER** use string concatenation for SQL/NoSQL queries - use parameterized queries or ORM methods
2. **NEVER** use `dangerouslySetInnerHTML` with user input without DOMPurify sanitization
3. **ALWAYS** verify resource ownership (BOLA) - `where: { id, userId: session.user.id }`
4. **ALWAYS** validate ALL external input with zod/yup at API boundaries
5. **NEVER** hardcode secrets - use `process.env` (not `NEXT_PUBLIC_*` for secrets)
6. **ALWAYS** use `crypto.randomBytes()` or `crypto.randomUUID()` - never `Math.random()` for security
7. **NEVER** trust middleware alone for auth - verify in route handlers (defense in depth)
8. **ALWAYS** hash passwords with bcrypt/argon2 - never MD5/SHA1/unsalted
9. **NEVER** use `exec()` with user input - use `execFile()` with argument arrays
10. **ALWAYS** validate file uploads: extension, MIME type, size limits

## Module Index

Reference these modules for specific vulnerability patterns:

| Module | Covers | OWASP Reference |
|--------|--------|-----------------|
| [injection.md](references/injection.md) | SQL, Command, NoSQL, Template, LDAP injection | A03:2021 |
| [xss-output.md](references/xss-output.md) | XSS (Reflected, Stored, DOM), output encoding | A03:2021 |
| [auth-access.md](references/auth-access.md) | BOLA, BFLA, auth, sessions, JWT | API1-3, API5 |
| [crypto-secrets.md](references/crypto-secrets.md) | Secrets management, encryption, hashing | A02:2021 |
| [input-validation.md](references/input-validation.md) | Validation, mass assignment, path traversal, uploads | A03:2021, API3 |
| [prototype-pollution.md](references/prototype-pollution.md) | JS prototype pollution attacks | CWE-1321 |
| [typescript-safety.md](references/typescript-safety.md) | Type safety gaps, runtime validation | CWE-843 |
| [nextjs-security.md](references/nextjs-security.md) | Middleware bypass, Server Actions, SSRF | CVE-2025-29927, CVE-2025-66478 |
| [rsc-security.md](references/rsc-security.md) | RSC deserialization (React2Shell), DoS, Server Action abuse | CVE-2025-55182, CVE-2025-55184 |
| [api-infra.md](references/api-infra.md) | Rate limiting, CORS, headers, error handling | API4, API6-7 |
| [dependencies.md](references/dependencies.md) | Supply chain, slopsquatting, NPM malware, PhantomRaven | A06:2021, CWE-506 |
| [nodejs-runtime.md](references/nodejs-runtime.md) | ReDoS, async hooks exhaustion, HTTP/2 DoS, child processes | CWE-1333, CVE-2025-59466 |

## How to Use This Skill

When generating code:

1. **Identify applicable modules** based on what you're writing
2. **Reference the specific module** for detailed BAD/GOOD patterns
3. **Apply the GOOD pattern** - never generate code matching BAD patterns
4. **Verify the output** against the Critical Rules above

### Quick Reference by Task

| Writing... | Reference |
|------------|-----------|
| Database queries | references/injection.md, references/input-validation.md |
| API route/endpoint | references/auth-access.md, references/api-infra.md, references/input-validation.md |
| User authentication | references/auth-access.md, references/crypto-secrets.md |
| Form handling | references/input-validation.md, references/xss-output.md |
| File operations | references/input-validation.md, references/nodejs-runtime.md |
| Next.js Server Actions | references/nextjs-security.md, references/rsc-security.md, references/auth-access.md |
| React Server Components | references/rsc-security.md, references/nextjs-security.md |
| Third-party package usage | references/dependencies.md |
| Rendering user content | references/xss-output.md |
| Environment/config | references/crypto-secrets.md |
| Child processes | references/nodejs-runtime.md, references/injection.md |

## Response Format

When this skill is active, ensure generated code:

1. Includes necessary imports (zod, bcrypt, etc.)
2. Shows the secure pattern being used
3. Includes brief comments explaining security measure if non-obvious
4. Does NOT include insecure alternatives "for reference"
