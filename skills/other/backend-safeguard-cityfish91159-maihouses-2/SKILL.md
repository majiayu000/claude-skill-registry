---
name: backend_safeguard
description: Supabase schema validation, RLS enforcement, and API security best practices.
allowed-tools: Read, Edit, Write
---

# Backend Safeguard Protocol (Supabase + Vercel API)

## 1. Database Schema & Migration Safety

- **Migrations**:
  - NEVER edit a previous migration. Always create a new one.
  - Migration files must be numbered/timestamped sequentially.
  - Destructive changes (DROP COLUMN) require explicit user confirmation.
- **Supabase Specifics**:
  - Use `pg_jsonschema` (if available) or `CHECK` constraints for complex JSON data.
  - Indexes: Ensure Foreign Keys have indices if used in JOINs frequentyl.

## 2. RLS (Row Level Security) "Ironclad" Rules

- **Enablement**: `ALTER TABLE "table_name" ENABLE ROW LEVEL SECURITY;` is MANDATORY.
- **Policies**:
  - Must have separate policies for SELECT, INSERT, UPDATE, DELETE (unless absolutely identical).
  - `auth.uid()` MUST be checked for user-specific data.
  - `service_role` usage in client is FORBIDDEN.

## 3. API Design & Security

- **Input Validation (Zod)**:
  - ALL API routes must parse body/query with `Zod`.
  - `strict()` mode recommended to strip unknown fields.
- **Error Handling**:
  - Return standardized error structure: `{ error: string, code: string, details?: any }`.
  - NEVER leak Stack Traces to production response.
  - Use 4xx for client errors, 5xx for server errors.
- **Rate Limiting**:
  - Ensure sensitive endpoints (auth, email) have rate limiting (Upstash/KV).

## 4. Code Structure (Vercel Functions)

- **Separation of Concerns**:
  - `api/xxx.ts` -> Controller (Parse Req, Check Auth)
  - `src/services/xxx.ts` -> Business Logic
  - `src/data/xxx.ts` -> Database Logic (Supabase calls)
- **Secrets**:
  - Check for `process.env.XXX`. NEVER hardcode strings.

## 5. Audit Checklist

- [ ] Is RLS enabled on all touched tables?
- [ ] Is `Zod` validation wrapping the request?
- [ ] Is logging present for state changes?
- [ ] Are we leaking sensitive user data in the response?
