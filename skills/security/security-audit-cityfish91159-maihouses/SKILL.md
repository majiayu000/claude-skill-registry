---
name: security_audit
description: Checklist for security-sensitive coding, ensuring MaiHouses guards and policies are respected.
allowed-tools: Read, Grep, Glob
---

# Security Audit Protocol

## 1. Critical "Guard" Files

**WARNING**: The following files are **OFF-LIMITS** for modification without explicit user approval.

- `scripts/ai-diff-gate.ts`
- `.github/workflows/**`
- Any file with `midlaw` or `policy` in the name.

## 2. Database Security (Supabase)

- **RLS (Row Level Security)**:
  - EVERY table must have RLS enabled.
  - Policies must explicitly define `USING` and `WITH CHECK` clauses.
  - NEVER use `service_role` key in frontend client code.
- **SQL Injection**:
  - Use parameterized queries or ORM methods (Supabase JS client) only.
  - Avoid raw SQL string concatenation.

## 3. API Security

- **Authentication**:
  - Verify `user` exists in `req` (usually populated by middleware/auth helper).
  - Check permissions before performing actions (e.g. `checkPermission(user.id, 'post.create')`).
- **Input Validation**:
  - Validate ALL inputs using `zod` schemas.
  - Sanitize HTML inputs if rendering user content (use `DOMPurify`).

## 4. Audit Checklist

- [ ] Are guards/policies untouched?
- [ ] Is RLS enabled and tested?
- [ ] Is input validation (`zod`) in place?
- [ ] Are no secrets committed to code?
- [ ] Did I run `/security-review` (if available) or manual check?
