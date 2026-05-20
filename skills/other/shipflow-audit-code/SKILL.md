---
name: shipflow-audit-code
description: Professional code review — single file (with argument) or full project audit (no argument). Architecture, performance, security, reliability, modern practices.
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -120 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json: !`cat package.json 2>/dev/null | head -80 || echo "no package.json"`
- Dependencies: !`cat package.json 2>/dev/null | grep -E '"(dependencies|devDependencies)"' -A 100 | head -80 || pip list 2>/dev/null | head -40 || echo "unknown"`
- Lockfile: !`ls -1 package-lock.json yarn.lock pnpm-lock.yaml requirements.txt Pipfile.lock 2>/dev/null | head -3 || echo "none"`
- Project structure: !`find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.astro" -o -name "*.vue" -o -name "*.py" -o -name "*.sh" \) 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -60`
- Config files: !`ls -1 tsconfig*.json astro.config.* next.config.* vite.config.* vitest.config.* .eslintrc* eslint.config.* prettier.config.* .env.example 2>/dev/null || echo "none"`
- CI/CD: !`ls -1 .github/workflows/*.yml Dockerfile docker-compose.yml 2>/dev/null || echo "none"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL projects in the workspace.
- **`$ARGUMENTS` is a file path** → FILE MODE: deep code review of that single file.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full architecture/perf/security/reliability audit.

---

## GLOBAL MODE

Audit ALL projects in the workspace for code quality, architecture, security, and reliability.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Code column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for code quality?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 7 phases: Architecture → Performance → Security → Reliability → Modern Best Practices → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project code report**:

   ```
   GLOBAL CODE AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Systemic issues in 2+ projects]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Code column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Code` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## FILE MODE

### Step 1: Gather context

1. Read the target file (`$ARGUMENTS`).
2. Read files it imports/depends on (follow the imports, 1 level deep).
3. Read the types/interfaces it uses.
4. Identify the file's role: component, page, API route, utility, config, test, etc.

### Step 2: Audit the file

Score each category **A/B/C/D**. Be strict.

#### 1. Architecture & Structure
- [ ] Single responsibility — file does one thing well
- [ ] Under 300 lines (if over, should it be split?)
- [ ] Clear function/component boundaries (each function < 50 lines)
- [ ] No circular imports
- [ ] Proper separation: logic vs presentation vs data access
- [ ] Exports are intentional (not exporting internals)

#### 2. Type Safety
- [ ] No `any` types
- [ ] Function parameters and return types are typed
- [ ] API responses / external data validated at boundary (Zod, Valibot, runtime check)
- [ ] No type assertions (`as`) that bypass safety
- [ ] Enums or const maps instead of magic strings/numbers

#### 3. Error Handling
- [ ] Every async call has error handling
- [ ] Errors are not swallowed (no empty `catch {}`)
- [ ] User-facing errors are helpful and actionable
- [ ] Edge cases handled: null, undefined, empty arrays, network failure
- [ ] No unhandled promise rejections

#### 4. Performance
- [ ] No unnecessary re-renders (React: stable callbacks, proper deps arrays)
- [ ] No expensive computations on every render (memoize if needed)
- [ ] No N+1 queries or waterfall fetches
- [ ] Large imports are tree-shakeable or lazy-loaded
- [ ] Images/assets properly optimized if referenced

#### 5. Security
- [ ] User input is validated before use
- [ ] No `dangerouslySetInnerHTML` / `set:html` with user data
- [ ] No secrets or hardcoded credentials
- [ ] No `eval()`, `new Function()`, or dynamic code execution
- [ ] Auth/authorization checked if this is an API route or mutation
- [ ] No open redirects or XSS vectors

#### 6. Modern Practices
- [ ] Uses current framework patterns (not deprecated APIs)
- [ ] Hooks over class components (React)
- [ ] Reactive queries over fetch-in-effect (Convex, React Query)
- [ ] Async/await over raw promises or callbacks
- [ ] No commented-out code
- [ ] Naming is clear and consistent

#### 7. Reliability
- [ ] Tests exist for this file (or should they?)
- [ ] Edge cases considered (empty state, max length, concurrent access)
- [ ] Cleanup on unmount (subscriptions, timers, event listeners)
- [ ] Fails gracefully — one error doesn't crash the whole page

### Step 3: Fix

For each issue rated B or worse:
1. Explain the problem with the specific line.
2. Fix it directly in the code.
3. For architectural choices, propose 2 options and ask.

### Step 4: Report

```
CODE REVIEW: [file name]
─────────────────────────────────────
Architecture       [A/B/C/D] — one-line summary
Type Safety        [A/B/C/D] — one-line summary
Error Handling     [A/B/C/D] — one-line summary
Performance        [A/B/C/D] — one-line summary
Security           [A/B/C/D] — one-line summary
Modern Practices   [A/B/C/D] — one-line summary
Reliability        [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL            [A/B/C/D]

Fixed: X issues | Needs decision: Y
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir, no `lib.sh`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for code quality?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run code audit across every project" (Recommended)
  - One option per project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### PHASE 1: ARCHITECTURE

Read the project structure, entry points, configs, and 10-15 key files. Audit:

#### 1.1 Project Structure & Organization
- [ ] Clear separation of concerns (pages/routes, components, utils, services, types)
- [ ] No circular dependencies between modules
- [ ] No god files (> 300 lines doing too many things)
- [ ] Barrel exports (`index.ts`) are not re-exporting the entire tree (bundle bloat)
- [ ] Config is centralized
- [ ] Environment variables are typed and validated at startup

#### 1.2 Data Flow & State Management
- [ ] Data flows in one direction (no prop drilling > 3 levels)
- [ ] Server state and client state separated
- [ ] No redundant state (derived values computed, not stored)
- [ ] API/database calls in a service layer, not inside components
- [ ] Real-time subscriptions cleaned up on unmount
- [ ] No stale closures in effects/callbacks

#### 1.3 Error Boundaries & Resilience
- [ ] Error boundaries at route level
- [ ] API calls have proper error handling
- [ ] Network failures show user-friendly messages
- [ ] Retry logic for transient failures
- [ ] Partial failures handled gracefully

#### 1.4 Type Safety
- [ ] `strict: true` in tsconfig
- [ ] No `any` types
- [ ] API responses validated at boundary
- [ ] Shared types between frontend/backend
- [ ] Enums or const maps instead of magic strings

#### 1.5 Dependency Health (quick check)

> Deep dependency analysis has moved to `/shipflow-deps`.

- [ ] Lock file committed

---

### PHASE 2: PERFORMANCE (quick scan)

> Deep performance analysis has moved to `/shipflow-perf`.

Quick architecture-level checks only:

- [ ] No N+1 query patterns or waterfall fetches
- [ ] No synchronous blocking operations in async code paths
- [ ] Code splitting exists at route level
- [ ] No client-side rendering for content that should be static/SSR

---

### PHASE 3: SECURITY

#### 3.1 Authentication & Authorization
- [ ] Auth tokens stored securely (httpOnly cookies)
- [ ] Every API route checks authentication
- [ ] Authorization checked per resource
- [ ] Session expiration and refresh rotation
- [ ] OAuth state parameter validated

#### 3.2 Input Validation & Injection
- [ ] All input validated server-side
- [ ] Parameterized queries (no string concatenation)
- [ ] HTML output escaped (check `dangerouslySetInnerHTML`, `set:html`)
- [ ] File uploads validate type, size, content
- [ ] No `eval()` or `new Function()` with user input

#### 3.3 Secrets & Configuration
- [ ] No secrets in source code
- [ ] `.env` files in `.gitignore`
- [ ] Secrets via env vars or secret manager
- [ ] No secrets in logs or error messages
- [ ] `.env.example` exists

#### 3.4 HTTP Security
- [ ] HTTPS enforced
- [ ] Security headers set (CSP, X-Frame-Options, etc.)
- [ ] CORS restrictive (not `*`)
- [ ] Cookies: `Secure`, `HttpOnly`, `SameSite`
- [ ] Rate limiting on auth endpoints

#### 3.5 Data Protection
- [ ] PII not logged or cached publicly
- [ ] User data deletion possible (RGPD)
- [ ] File uploads stored outside web root

---

### PHASE 4: RELIABILITY

#### 4.1 Error Handling
- [ ] Errors caught at every async boundary
- [ ] Errors logged with context
- [ ] External service failures have fallback
- [ ] Unhandled rejections caught at process level

#### 4.2 Testing
- [ ] Coverage exists for critical paths
- [ ] Tests not brittle
- [ ] E2E tests cover main journey
- [ ] Tests run in CI
- [ ] Edge cases tested

#### 4.3 Observability
- [ ] Structured logging (not just `console.log`)
- [ ] Error tracking configured or easy to add
- [ ] Health check endpoint exists

#### 4.4 Deployment & Recovery
- [ ] Build reproducible
- [ ] Zero-downtime deployment possible
- [ ] Rollback straightforward
- [ ] Database migrations backward-compatible

---

### PHASE 5: MODERN BEST PRACTICES

#### 5.1 Framework-Specific (detect and apply)

**Astro 5**: Content Collections v2, `<Image>`, View Transitions, minimal client JS, `astro:env`.

**Next.js 15+**: App Router, Server Components by default, `next/image` + `next/font`, `loading.tsx` + `error.tsx`, Metadata API.

**React**: Hooks only, Suspense for async, no `useEffect` for data fetching, stable event handlers.

**Convex**: Reactive queries, idempotent mutations, actions for external APIs only, indexes defined, Convex storage API.

**Python**: Type hints, Pydantic, async for I/O, no mutable defaults, virtual env.

#### 5.2 Code Quality
- [ ] Formatter configured (Prettier, Black)
- [ ] Linter configured and passing
- [ ] No commented-out code
- [ ] Functions < 50 lines, single purpose
- [ ] Naming clear and consistent

---

### PHASE 6: FIX

Fix all issues in code. Priority:
1. **CRITICAL SECURITY** — secrets, injection, XSS, auth bypass
2. **HIGH SECURITY** — missing validation, permissive CORS
3. **ARCHITECTURE** — circular deps, god files, untyped boundaries
4. **RELIABILITY** — silent error swallowing, missing error boundaries
5. **PERFORMANCE** — critical issues only (N+1, blocking ops); run `/shipflow-perf` for deep analysis
6. **BEST PRACTICES** — deprecated patterns, legacy APIs

### PHASE 7: REPORT

```
CODE AUDIT: [project name] — [stack detected]
═══════════════════════════════════════════════════

ARCHITECTURE                           [A/B/C/D]
  Structure & Organization             [A/B/C/D]
  Data Flow & State                    [A/B/C/D]
  Error Resilience                     [A/B/C/D]
  Type Safety                          [A/B/C/D]
  Dependency Health (quick)            [A/B/C/D]  → /shipflow-deps for full audit

PERFORMANCE (quick scan)               [A/B/C/D]  → /shipflow-perf for full audit

SECURITY                               [A/B/C/D]
  Auth & Authorization                 [A/B/C/D]
  Input Validation                     [A/B/C/D]
  Secrets Management                   [A/B/C/D]
  HTTP Security                        [A/B/C/D]

RELIABILITY                            [A/B/C/D]
  Error Handling                       [A/B/C/D]
  Testing                              [A/B/C/D]
  Observability                        [A/B/C/D]

MODERN PRACTICES                       [A/B/C/D]
  Framework Best Practices             [A/B/C/D]
  Code Quality                         [A/B/C/D]
═══════════════════════════════════════════════════
OVERALL                                [A/B/C/D]

CRITICAL fixes applied:     X
HIGH fixes applied:         X
MEDIUM fixes applied:       X
Architectural decisions needed: X (detailed below)

TOP 5 IMPROVEMENTS (by impact):
1. [description + files affected]
2. ...
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append `| date | project | scope | — | — | — | — | — | — | [score] | crit/high/med |` (fill only the Code column, `—` for others).
2. **Project-local `./AUDIT_LOG.md`**: same but without the Project column.

Create either file if missing, using the table header from the master `/audit` skill format.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: Code` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: Code` subsection with the same tasks. Update the Dashboard "Top Priority" if critical issues found.

---

## Important (all modes)

- Be ruthlessly honest. A-level means "I would deploy this to production with confidence today."
- Detect the stack automatically. Only audit relevant sections.
- Security findings are never optional — flag them regardless of focus.
- When a fix touches shared infrastructure, apply once at the source.
- For shell/Bash projects: focus on input validation, quoting, `set -euo pipefail`, ShellCheck.
- Don't refactor working code for aesthetics. Only change code with a concrete issue.
