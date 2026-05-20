---
name: lp-do-data-audit
description: Data hardening audit for Next.js and web apps in this monorepo. Checks schema validation coverage, TypeScript strictness, environment variable safety, database type safety, client-side response validation, error handling, and unsafe cast patterns. Emits a structured audit report and a PASS/FAIL verdict. Run before site launch and periodically thereafter.
---

# lp-do-data-audit — Data Hardening Audit

Audits a web app for data safety and type integrity across 7 categories. Produces a structured report with per-finding severity ratings and a binary PASS/FAIL verdict. Designed to be run before any site goes live (S9B gate) and quarterly thereafter.

## Invocation

```
/lp-do-data-audit [<app-path>]
```

**Arguments:**

- `<app-path>` (optional): Path to the app directory relative to repo root. Example: `apps/inventory-uploader`, `apps/caryina`. If omitted, defaults to the current working directory. The agent must resolve `<app-path>` to an absolute path before scanning.

**Examples:**
```
/lp-do-data-audit apps/inventory-uploader
/lp-do-data-audit apps/caryina
/lp-do-data-audit apps/brikette
```

## Operating Mode

**AUDIT ONLY (read-only)**

- Allowed: Read source files, run grep/glob searches, read config files, read tsconfig, run `tsc --noEmit` for type errors.
- Not allowed: Code changes, config changes, deployments, destructive commands, committing fixes.
- Commit allowed: Audit report artifact only (`docs/audits/data-hardening/<app-name>-<YYYY-MM-DD>.md`).

## Workflow

### 1) Resolve target and discover files

**1a) Resolve `<app-path>`** to an absolute filesystem path. Confirm the directory exists. If it does not exist, STOP with: "App path not found: <app-path>. Verify the directory exists before running the audit."

**1b) Identify source root:** Look for `src/` inside the app path. If `src/` exists, use `<app-path>/src/` as the scan root. Otherwise use `<app-path>/` directly.

**1c) Read `tsconfig.json`** at `<app-path>/tsconfig.json` (and `<app-path>/tsconfig.base.json` if present). Extract `strict`, `noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess` settings (accounting for inheritance via `extends` — check `tsconfig.base.json` or `packages/config/tsconfig.base.json` if the app extends it).

**1d) Discover API route files:** Find all files matching:
- `<scan-root>/app/api/**/*.ts` (Next.js App Router route handlers)
- `<scan-root>/pages/api/**/*.ts` (Next.js Pages Router)
- `<scan-root>/routes/**/*.ts` (generic REST routers)

**1e) Discover additional source files:**
- `<scan-root>/lib/**/*.ts`
- `<scan-root>/services/**/*.ts`
- `<scan-root>/hooks/**/*.ts`
- `<scan-root>/components/**/*.tsx`
- `<scan-root>/utils/**/*.ts`

### 2) Execute the 7 audit categories in parallel

Dispatch all 7 category checks simultaneously. Each check returns a list of findings.

---

#### CAT-01 — Schema Validation Coverage

**Goal:** All external inputs entering the app are validated with Zod (or equivalent: Yup, Valibot, custom schema) before use.

**Scope:** API route files discovered in step 1d.

**What to check:**

- **C1 — Request body validation:** For each API route handler that reads `request.json()`, `req.body`, or `formData()`, confirm a schema parse call (`z.parse`, `z.safeParse`, `schema.parse`, `schema.safeParse`) is applied before the data is used. Finding if any route reads the body and uses it without a schema parse.

- **C2 — Path/query param validation:** For each route reading `params.X`, `searchParams.get()`, `req.query.X`, check whether those values are validated (type-coerced via Zod `.coerce`, passed to a schema, or explicitly checked before use). Finding if params are passed directly to business logic or DB queries without validation.

- **C3 — External API response validation:** For each `fetch()` or external HTTP client call where the response is JSON-parsed and typed (e.g., `as SomeType`), check if the response is validated with a schema before use. Finding if the response is blindly cast or used without validation.

**How to search:**
```
# Find routes that read body without schema parse
grep -rn "request\.json()\|req\.body\|formData()" <scan-root>/app/api/ <scan-root>/pages/api/ --include="*.ts"
# Then for each file found, check for z.parse/z.safeParse/schema.parse within the same file
grep -l "z\.parse\|z\.safeParse\|schema\.parse\|schema\.safeParse\|\.parse(\|\.safeParse(" <file>

# Find routes that use params without Zod
grep -rn "params\.\|searchParams\.get\|req\.query\." <scan-root>/app/api/ --include="*.ts"
```

**Severity:**
- CRITICAL: Route reads body/params and passes directly to a DB query or write operation without any validation
- HIGH: Route reads body/params without validation but uses them only for reads or non-destructive logic
- MEDIUM: External API response cast without validation (`as SomeType` on a fetch response)
- LOW: Minor inconsistency (validation present but partial — e.g., body validated, params not)

---

#### CAT-02 — TypeScript Strictness

**Goal:** The app's TypeScript config enforces maximum type safety. Source files do not disable that safety via `as any` or related unsafe patterns.

**Scope:** `tsconfig.json` + all `.ts`/`.tsx` files in the scan root.

**What to check:**

- **T1 — `strict: true` in tsconfig:** Read `<app-path>/tsconfig.json`. If it `extends` a base config, read that too. Confirm `"strict": true` is set and not overridden. Finding if `strict` is false or absent.

- **T2 — `as any` casts:** Scan all source files for ` as any` pattern. Each occurrence is a finding.
  ```
  grep -rn " as any" <scan-root> --include="*.ts" --include="*.tsx"
  ```

- **T3 — `as unknown as X` double casts:** These signal a type system escape hatch. Scan for ` as unknown as `.
  ```
  grep -rn " as unknown as " <scan-root> --include="*.ts" --include="*.tsx"
  ```

- **T4 — `@ts-ignore` / `@ts-expect-error` suppressions:** Each suppression hides a type error. Scan for these comments.
  ```
  grep -rn "@ts-ignore\|@ts-expect-error" <scan-root> --include="*.ts" --include="*.tsx"
  ```

- **T5 — Unsafe index access:** Patterns like `arr[0]` used without null check when `noUncheckedIndexedAccess` is off, or `(obj as Record<string, unknown>)[key]` patterns. Scan for:
  ```
  grep -rn " as Record<string" <scan-root> --include="*.ts" --include="*.tsx"
  ```

**Severity:**
- HIGH: `strict: true` absent from tsconfig (affects entire codebase)
- HIGH: `as any` in an API route handler or data processing function (lib, services)
- MEDIUM: `as any` in a component or utility outside the data path
- MEDIUM: `as unknown as X` (double cast) anywhere in source
- MEDIUM: `@ts-ignore` suppressing a type error (not `@ts-expect-error` with a known-unresolvable issue)
- LOW: `@ts-expect-error` with explanatory comment; `as Record<string, unknown>` where intent is clear

---

#### CAT-03 — Environment Variable Schema

**Goal:** All required environment variables are validated at startup using a schema, not lazily read via bare `process.env.X` throughout the codebase.

**Scope:** All source files.

**What to check:**

- **E1 — Bare `process.env` access outside a validation module:** Scan for `process.env.` usage. Distinguish between: (a) a dedicated env schema/config module that validates all vars once (acceptable), vs. (b) ad-hoc reads scattered across route handlers, lib files, and components (finding).
  ```
  grep -rn "process\.env\." <scan-root> --include="*.ts" --include="*.tsx" | grep -v "\.env\.\(test\|spec\|config\)"
  ```

- **E2 — Missing env validation module:** Check if the app has a dedicated env validation file (commonly `src/env.ts`, `src/lib/env.ts`, `src/config/env.ts`, or similar that uses `z.object()` or equivalent to parse `process.env` once). Finding if no such file exists AND bare `process.env.X` calls are scattered.

- **E3 — Optional chaining on env vars:** `process.env.X?.trim()` or `process.env.X ?? ''` used without a prior parse — these indicate the code handles `undefined` but never enforces the variable's presence. Finding where critical service env vars (database URLs, API keys, signing secrets) use optional chaining.

**How to check for a validation module:**
```
# Look for an env validation module
ls <scan-root>/env.ts <scan-root>/lib/env.ts <scan-root>/config/env.ts <scan-root>/lib/env/index.ts 2>/dev/null
grep -rln "z\.object\(\|process\.env\)" <scan-root> --include="*.ts" | grep -i "env"
```

**Severity:**
- HIGH: No env validation module AND ≥3 bare `process.env.X` calls for secrets/DB URLs/API keys in non-test files
- MEDIUM: Env validation module exists but some routes/services bypass it with direct `process.env.X`
- LOW: `process.env.NODE_ENV` or `process.env.NEXT_PUBLIC_*` reads without schema (acceptable for build-time flags)

---

#### CAT-04 — Prisma / Database Type Safety

**Goal:** Database client calls are typed; no `as any` is applied to Prisma results; no raw SQL is constructed with user-supplied string interpolation.

**Scope:** All source files that import `@prisma/client`, use `db.`, `prisma.`, or raw SQL.

**What to check:**

- **D1 — `as any` on Prisma results:** Scan for `as any` on lines that also reference `prisma.`, `db.`, or Prisma result variable names.
  ```
  grep -rn "prisma\.\|db\." <scan-root> --include="*.ts" | grep " as any"
  grep -rn "\.findMany\|\.findFirst\|\.findUnique\|\.create\|\.update\|\.delete" <scan-root> --include="*.ts" | grep " as any"
  ```

- **D2 — Raw SQL with string interpolation (SQL injection risk):** Scan for template literals in raw query calls.
  ```
  grep -rn "\$queryRaw\|\$executeRaw\|raw\`\|knex\.raw\|sql\`" <scan-root> --include="*.ts"
  ```
  For each match: check if user-supplied variables (from request body, params, or query string) appear in the template literal without parameterized binding.

- **D3 — Untyped DB result spread:** `const result = await db.query(...); return result as SomeType[]` — blind cast of query results.
  ```
  grep -rn "as \w\+\[\]" <scan-root> --include="*.ts" | grep -v "test\|spec"
  ```

**Severity:**
- CRITICAL: Raw SQL template literal with user-supplied value (SQL injection risk)
- HIGH: `as any` applied to a Prisma result used in a public-facing response
- MEDIUM: Blind cast (`as SomeType[]`) of a DB result without Zod validation
- LOW: `as any` on Prisma results used only internally with no public exposure

---

#### CAT-05 — Client-Side Response Validation

**Goal:** API responses consumed by client components are validated (not blindly cast) before use.

**Scope:** Client-side files: `*.client.tsx`, `*.client.ts`, files in `components/`, `hooks/`, and any file that calls `fetch()` or uses a data-fetching hook.

**What to check:**

- **R1 — Blind cast of `fetch` response:** Pattern: `const data = await res.json() as SomeType` — the response JSON is cast directly without validation.
  ```
  grep -rn "\.json() as \|\.json()\s*as " <scan-root> --include="*.ts" --include="*.tsx"
  ```

- **R2 — No schema parse on external data:** For any `fetch()` call or `useQuery`/`useSWR`/`useEffect` fetch pattern where the returned data is typed without a schema parse. Look for `as SomeType` or `as unknown as SomeType` following JSON-parsing.
  ```
  grep -rn " as unknown as " <scan-root>/hooks <scan-root>/components --include="*.ts" --include="*.tsx" 2>/dev/null
  ```

- **R3 — Missing error shape validation:** For client-side error handling on API responses, check if the error response shape is validated before accessing `error.message` or `error.code`. Pattern to flag: `const err = await res.json(); throw new Error(err.message)` without schema parse on `err`.

**Severity:**
- HIGH: Blind cast of `fetch` response in a hook or component used across multiple pages
- MEDIUM: Blind cast of `fetch` response in a single isolated component
- LOW: Missing error-shape validation (accesses `.message` on untyped error object)

---

#### CAT-06 — Error Handling

**Goal:** `catch` blocks use `unknown` type; errors are sanitized (not forwarded raw) before being sent to clients; catch-all error handlers don't expose stack traces or internal details.

**Scope:** All source files.

**What to check:**

- **H1 — Typed catch variables (not `unknown`):** In TypeScript ≥4.0, caught errors are `unknown` by default when `useUnknownInCatchVariables` is set (part of `strict`). Scan for explicit `catch (e: Error)` or `catch (e: any)` typing.
  ```
  grep -rn "catch (e:" <scan-root> --include="*.ts" --include="*.tsx"
  grep -rn "catch (err:" <scan-root> --include="*.ts" --include="*.tsx"
  grep -rn "catch (error:" <scan-root> --include="*.ts" --include="*.tsx"
  ```
  Flag any that use a concrete type other than `unknown`.

- **H2 — Raw error forwarded to client:** Pattern: API route `catch (e) { return Response.json({ error: e.message }) }` or `return NextResponse.json(e)` — forwards raw error detail to the client.
  ```
  grep -rn "Response\.json.*error\|NextResponse\.json.*error\|res\.json.*error\|res\.status.*json.*message" <scan-root>/app/api <scan-root>/pages/api --include="*.ts" 2>/dev/null
  ```
  For each match: check if the error is sanitized (wrapped in a custom message) or forwarded raw.

- **H3 — Stack trace exposure in response:** Scan for `stack` being included in API responses.
  ```
  grep -rn "\.stack" <scan-root>/app/api <scan-root>/pages/api --include="*.ts" 2>/dev/null
  ```

- **H4 — Unhandled promise rejections in route handlers:** Route handlers that call async functions without try/catch and without the framework's error boundary (Next.js auto-wraps some, but not all patterns). Look for `async function` route handlers that lack `try/catch`.
  ```
  grep -rn "export async function\|export default async function" <scan-root>/app/api <scan-root>/pages/api --include="*.ts" 2>/dev/null
  ```
  For each: verify try/catch is present or the function body is short enough that all async calls are wrapped.

**Severity:**
- CRITICAL: Raw exception (with `.stack` or `.message` from unknown input) forwarded to client response
- HIGH: `catch (e: any)` in a route handler (removes type safety from error handling path)
- MEDIUM: `catch (e: Error)` where `e` might not be an `Error` instance (wrong assumption)
- LOW: Missing try/catch on a non-critical async call in a non-route context

---

#### CAT-07 — Unsafe Cast Patterns

**Goal:** Identify patterns that bypass TypeScript's type system outside of the categories above.

**Scope:** All source files.

**What to check:**

- **U1 — `as SomeType[]` without Zod guard:** Any cast of an array type applied to runtime data (not a static constant). Particularly dangerous on data from external sources.
  ```
  grep -rn " as [A-Z][a-zA-Z]*\[\]" <scan-root> --include="*.ts" --include="*.tsx" | grep -v "test\|spec\|\.d\.ts"
  ```

- **U2 — `as Record<string, unknown>`:** Used as a workaround for unknown object shapes. Each occurrence should be reviewed to determine if a Zod schema would be more appropriate.
  ```
  grep -rn " as Record<string" <scan-root> --include="*.ts" --include="*.tsx" | grep -v "test\|spec"
  ```

- **U3 — Non-null assertion operator `!` on external data:** `data!.field`, `res!.json()` — asserting non-null without a runtime check.
  ```
  grep -rn "\w!\." <scan-root> --include="*.ts" --include="*.tsx" | grep -v "test\|spec\|\.d\.ts"
  ```
  For each match: determine if the `!` is applied to a known-safe local variable (constructor initialization, narrow scope) or to external/runtime data.

- **U4 — `Object.keys(x).forEach` without type guard:** Iterating object keys from external data without validating that the values match expected types.
  ```
  grep -rn "Object\.keys\|Object\.entries\|Object\.values" <scan-root>/app/api <scan-root>/lib --include="*.ts" 2>/dev/null
  ```

**Severity:**
- HIGH: `as SomeType[]` on data from a DB query, external API, or request body
- HIGH: Non-null assertion `!` on a value sourced from request body or external API response
- MEDIUM: `as Record<string, unknown>` used to bypass typing on external data
- LOW: `Object.keys()` iteration without value type assertion (low-risk if values are not used in typed context)

---

### 3) Aggregate findings

Collect all findings from the 7 categories. For each finding, record:
- `id`: e.g., `C1-001`, `T2-003`
- `category`: CAT-01 through CAT-07
- `check`: the specific check ID (C1, T2, D1, etc.)
- `file`: relative path from repo root (e.g., `apps/inventory-uploader/src/app/api/upload/route.ts`)
- `line`: line number (if grep found it)
- `code_snippet`: the relevant line(s) — maximum 3 lines
- `severity`: CRITICAL / HIGH / MEDIUM / LOW
- `remediation`: specific action to fix (e.g., "Add `z.object({ name: z.string() }).parse(body)` before line 24")

### 4) Determine verdict

- **PASS:** Zero CRITICAL findings AND zero HIGH findings
- **FAIL:** One or more CRITICAL or HIGH findings

Record counts by severity: `{ critical: N, high: N, medium: N, low: N }`.

### 5) Write audit report

Write the report to:
```
docs/audits/data-hardening/<app-name>-<YYYY-MM-DD>.md
```

Where `<app-name>` is the last path segment of `<app-path>` (e.g., `inventory-uploader`, `caryina`).

If the directory `docs/audits/data-hardening/` does not exist, create it.

### 6) Commit the report

Commit the report file only. No source code changes.

```bash
git add docs/audits/data-hardening/<app-name>-<YYYY-MM-DD>.md
git commit -m "audit(data-hardening): <app-name> data hardening audit <YYYY-MM-DD>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

## Output Format

The report at `docs/audits/data-hardening/<app-name>-<YYYY-MM-DD>.md` must contain the following sections:

```markdown
---
Type: Data-Hardening-Audit
App: <app-name>
Date: <YYYY-MM-DD>
Verdict: PASS | FAIL
Critical: <count>
High: <count>
Medium: <count>
Low: <count>
---

# Data Hardening Audit — <app-name> (<YYYY-MM-DD>)

## Executive Summary

**Verdict: PASS / FAIL**

| Severity | Count |
|---|---|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |

<1–3 sentence plain-language summary of the most important findings, or "No CRITICAL/HIGH findings. App meets data hardening baseline." if passing.>

## Finding Matrix

| ID | Category | Check | File | Line | Severity |
|---|---|---|---|---|---|
| C1-001 | CAT-01 Schema Validation | C1 Request body | src/app/api/upload/route.ts | 24 | HIGH |
| ... | ... | ... | ... | ... | ... |

## Findings

### <ID> — <short description> [CRITICAL / HIGH / MEDIUM / LOW]

**File:** `<relative/path/to/file.ts>:<line>`

**Code:**
\`\`\`typescript
<code snippet — max 3 lines>
\`\`\`

**Issue:** <plain-language description of what is wrong and why it matters>

**Remediation:** <specific action to fix, with example if helpful>

---

(repeat per finding, ordered CRITICAL → HIGH → MEDIUM → LOW)

## Categories With No Findings

- CAT-02 TypeScript Strictness — no findings
- CAT-04 Prisma / Database Type Safety — no findings (no Prisma in this app)
- ...

## Audit Scope

- **App path:** `<app-path>`
- **Scan root:** `<scan-root>`
- **API route files scanned:** <count>
- **Total source files scanned:** <count>
- **tsconfig strict:** <true | false | inherited-true | not-set>
- **Prisma detected:** <yes | no>
- **Audited by:** lp-do-data-audit
```

## Quality Checks

A data hardening audit run is complete only if:

- [ ] App path resolved and confirmed to exist
- [ ] `tsconfig.json` read (accounting for `extends`)
- [ ] All 7 categories checked (not skipped without documented reason)
- [ ] Every grep command run against the actual scan root (not a sample)
- [ ] Each finding includes: file, line, code snippet, severity, remediation
- [ ] Finding IDs follow `<check-code>-<NNN>` format (e.g., `T2-001`)
- [ ] Verdict correctly reflects: FAIL if any CRITICAL or HIGH; PASS otherwise
- [ ] Report written to canonical path `docs/audits/data-hardening/<app-name>-<YYYY-MM-DD>.md`
- [ ] Report frontmatter contains: `Type`, `App`, `Date`, `Verdict`, severity counts
- [ ] Report committed (audit report file only — no source code changes in this commit)

## Remediation Guidance (Reference)

For agents fixing findings after a FAIL:

| Category | Common fix pattern |
|---|---|
| CAT-01 (Schema validation) | Add `const body = RequestSchema.parse(await request.json())` at top of handler |
| CAT-02 (TS strictness) | Remove `as any`; use type narrowing or Zod parse; add `strict: true` to tsconfig |
| CAT-03 (Env vars) | Create `src/env.ts` with `z.object({...}).parse(process.env)`; import from there |
| CAT-04 (Prisma safety) | Remove casts on query results; use parameterized `$queryRaw` with tagged template |
| CAT-05 (Client validation) | Add `ResponseSchema.parse(await res.json())` after each `fetch` call |
| CAT-06 (Error handling) | Wrap error messages: `return Response.json({ error: 'Operation failed' }, { status: 500 })` |
| CAT-07 (Unsafe casts) | Replace `as SomeType[]` with `z.array(SomeTypeSchema).parse(data)` |

After fixes: re-run `/lp-do-data-audit <app-path>` to confirm all CRITICAL/HIGH findings are resolved before declaring the gate passed.
