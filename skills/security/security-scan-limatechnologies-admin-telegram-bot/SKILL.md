---
name: security-scan
description: Audits code security against OWASP Top 10. Validates user ID from session, detects sensitive data leaks, verifies Zod validation. HAS VETO POWER - blocks insecure code.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Scan - Security Audit System

## VETO POWER

> **WARNING:** This skill HAS VETO POWER.
> If critical vulnerability detected, MUST:
>
> 1. STOP implementation
> 2. REPORT vulnerability
> 3. REQUIRE fix before proceeding

---

## Purpose

This skill audits code security:

- **Validates** user ID comes from session (NEVER from request)
- **Detects** sensitive data being sent to frontend
- **Verifies** Zod validation on all routes
- **Audits** against OWASP Top 10
- **Blocks** commits with critical vulnerabilities

---

## Critical Security Rules

### 1. USER ID ALWAYS FROM SESSION

> **NEVER** trust user ID from frontend.
> **ALWAYS** extract from `ctx.session.userId` or `ctx.user._id`.

```typescript
// WRONG - VULNERABLE (IMMEDIATE VETO)
async function getData({ userId }: { userId: string }) {
	return db.find({ userId }); // userId can be manipulated!
}

// CORRECT
async function getData({ ctx }: { ctx: Context }) {
	const userId = ctx.user._id; // Always from session
	return db.find({ userId });
}
```

### 2. SENSITIVE DATA NEVER TO FRONTEND

> **NEVER** send to frontend:
>
> - Passwords (even hashed)
> - API tokens
> - Secret keys
> - Other users' data
> - Stack traces in production

```typescript
// WRONG - DATA LEAK (IMMEDIATE VETO)
return {
	user: await UserModel.findById(id), // Includes passwordHash!
};

// CORRECT
return {
	user: user.toPublic(), // Sanitization method
};
```

### 3. ZOD VALIDATION REQUIRED

> **EVERY** tRPC route MUST have `.input(z.object({...}))`.
> Unvalidated inputs are attack vectors.

```typescript
// WRONG - NO VALIDATION (IMMEDIATE VETO)
.mutation(async ({ input }) => {
  await db.create(input); // input can have anything!
})

// CORRECT
.input(createSchema) // Zod schema
.mutation(async ({ input }) => {
  await db.create(input); // input is validated
})
```

---

## OWASP Top 10 Checklist

### A01: Broken Access Control

- [ ] All protected routes use `protectedProcedure`?
- [ ] User ID from session, not input?
- [ ] Resources filtered by user/tenant?

### A02: Cryptographic Failures

- [ ] Passwords hashed with bcrypt (salt >= 10)?
- [ ] Tokens generated with crypto.randomBytes?
- [ ] Cookies with HttpOnly, Secure, SameSite?
- [ ] No secrets in code (use env vars)?

### A03: Injection

- [ ] Queries use Mongoose (prevents NoSQL injection)?
- [ ] Inputs validated with Zod?
- [ ] No string concatenation in queries?

### A07: Authentication Failures

- [ ] Passwords with minimum requirements?
- [ ] Brute force protection?
- [ ] Sessions invalidated on logout?
- [ ] Tokens with expiration?

---

## Detection Patterns

### Detect User ID from Input (VETO)

```bash
grep -r "input\.userId\|input\.user_id\|{ userId }" server/ --include="*.ts"
```

### Detect Password Return (VETO)

```bash
grep -r "passwordHash\|password:" server/ --include="*.ts"
```

### Detect Route Without Validation (VETO)

```bash
grep -A5 "Procedure\." server/ --include="*.ts" | grep -v ".input("
```

---

## Output Format

### Approved

```markdown
## SECURITY SCAN - APPROVED

### Scope

- **Files:** X
- **Routes:** Y

### Checks

- [x] User ID always from session
- [x] No sensitive data in response
- [x] All routes with Zod validation
- [x] OWASP Top 10 OK

**STATUS: APPROVED**
```

### Vetoed

```markdown
## SECURITY SCAN - VETOED

### CRITICAL VULNERABILITY

**Type:** User ID from Input
**File:** `server/routers/example.ts:45`
**Risk:** Any user can access other users' data

**Fix:** Use `ctx.user._id` instead of `input.userId`

**STATUS: VETOED** - Fix before proceeding
```

---

## VETO Rules

### IMMEDIATE VETO

1. User ID from input/request body
2. Password returned in response
3. API tokens exposed
4. Protected route without `protectedProcedure`
5. Query without user/tenant filter

### VETO BEFORE MERGE

1. Route without Zod validation
2. Unsanitized sensitive data
3. bun audit (or npm audit) with critical vulnerabilities

---

## Progressive Disclosure

For detailed information, see:

- **[reference/owasp-top-10.md](reference/owasp-top-10.md)** - Complete OWASP Top 10 checklist with examples
- **[scripts/scan.py](scripts/scan.py)** - Automated security scanner

### Quick Scan

```bash
python .claude/skills/security-scan/scripts/scan.py server/
```

---

## Version

- **v2.1.0** - Added progressive disclosure with reference files and scan script
- **v2.0.0** - Generic template
