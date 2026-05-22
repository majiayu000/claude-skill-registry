---
name: code-review
description: Senior PHP Laravel code reviewer. Use when reviewing pull requests, examining code changes vs master branch, or when the user asks for a code review. Read-only review — never modifies code.
---

# Code Review

**Role:** Senior PHP Laravel code reviewer. Review changes vs `master` branch. Apply all `.cursor/rules/*.mdc` rules.

**Constraint:** Review only. Never modify code.

---

<<<<<<< Updated upstream
- DynamoDB used as NoSQL database and cache layer
- All changes must comply with `.cursor/rules/*.mdc`
- Understand what has changed and pay attention to the structural quality of the code defined in the rules
- Ensure SRP in this class and apply SOLID principles so that the code is readable for developers.
=======
## 1. General
>>>>>>> Stashed changes

**Assumptions:**
- PHPStan (level max), Rector (pekral/rector-rules), PHPCS (pekral/phpcs-rules), and Pint are in use and passing.
- Do not duplicate their checks: types, null safety, formatting, style, naming, dead code, automated refactors.
- Focus only on what tools do not cover: architecture, design, security logic, runtime/operational concerns.

**Review priorities (in order):**
1. Optimizations for processing large amounts of data
2. Security risks
3. SQL optimizations
4. Performance

**Compliance:** All changes must comply with `.cursor/rules/*.mdc`.

---

## 2. Git Analysis

**Check:**
- Identify changes vs `master` (list commits).
- Evaluate whether changes match the original assignment.
- Assess impact on other parts of the application.
- Suggest improvements and optimizations.
- Identify security risks.

**Commits:**
- Clear messages; small, focused commits; meaningful branch names.
- Format: `type(scope): description`.
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

---

## 3. Large Data Processing

**Check:**
- Prefer `chunk()` or `cursor()` over `get()` for large result sets. `get()` loads everything into memory and does not scale.
- **chunk(size):** Use when memory must stay bounded and you do bulk updates or batch work. Tune size (e.g. 200–500) to balance memory vs round-trips.
- **cursor():** Use for read-only iteration over very large datasets (e.g. exports); single row at a time, generator-based, safe under concurrent writes.
- Do not process large collections in a single request: offload to jobs/queues, process in batches, consider rate limiting or backpressure.
- Inside chunks/cursors: check for N+1; eager-load relations used in the loop. Prefer set-based updates over row-by-row in PHP.

---

## 4. Database Review (SQL Optimizations)

Apply rules from `.cursor/rules/*.mdc`.

**Schema:**
- Primary keys on every table; fitting data types (INT, DECIMAL, VARCHAR(n), TIMESTAMP); InnoDB; `lower_case_snake_case`; normalized; partition large tables by range where beneficial.
- When reviewing schema: drop unused or redundant indexes; aim for 3–5 well-chosen indexes per table.

**Queries:**
- Run EXPLAIN on new or changed queries. Flag: type ALL, high rows, Using filesort, Using temporary. Fix “ugly duckling” plans.
- Indexes: columns in WHERE, JOIN, ORDER BY, GROUP BY; composite index order must match query; avoid low-cardinality-only indexes; use covering indexes where useful.
- Never `SELECT *`. Use prepared statements or ORM; never concatenate user input into SQL.
- Prefer set-based operations in SQL over row-by-row in application code. Avoid functions on indexed columns in WHERE (e.g. `DATE(col)`, `LOWER(col)`).

**Transactions and locking:**
- Short transactions; batch writes in one transaction where appropriate.
- Use `SHOW ENGINE INNODB STATUS` to diagnose lock waits when investigating issues.

**Migrations:**
- Index additions on large tables: prefer non-blocking/parallel where supported; keep transactions short.

---

## 5. Architecture

**Laravel:**
- Controllers: slim; delegate to Services; accept FormRequest only; never `validate()` in controller.
- Services: hold business logic; return DTOs or models.
- Repositories: read-only. ModelManagers: write-only.
- Jobs, Events, Commands: slim; delegate to Services.
- New controller actions must have corresponding Request classes.

**Migrations:**
- Only `up()` methods. When adding columns, update model `$fillable`.
- Do not chain multiple migration commands (e.g. `make:model -m` then `make:migration`) in one shell line; run separately to avoid identical timestamps.

**Filament (if present):**
- Smoke tests for every Resource; when changing a Resource, tests must exist and pass.
- Use `->authorize('ability')` on actions.
- No deprecated v3 APIs (e.g. `->form()` → `->schema()`).
- Enums: use HasLabel, HasColor, HasIcon where applicable.

**Cross-project:** Check impact on other parts of the application.

---

## 6. UI / Templates

Apply when reviewing views.

**Check:**
- Consistency with existing UI: layout, colors, typography; human-friendly and understandable.
- Blade: 4-space indent; no space after control structures (`@if`, `@endif`).

---

## 7. Stability Checks

**Check for:**
- Race conditions
- Cache stampede risks
- Backward compatibility
- Performance issues
- Security concerns
- Memory leaks
- Timezone handling
- N+1 queries

**Error handling** (only where static analysis does not apply):
- Unhandled or swallowed exceptions in critical paths; overly broad catch blocks; silent failures; poor logging.
- Defensive code: timeouts, invalid input, empty responses, failed API calls. Suggest safer error paths and guard clauses.

**Performance and scalability:**
- N+1: relationships used in loops must be eager-loaded (`with()`, `load()`); no DB or model calls inside loops that could be batched.
- Avoid nested loops over large data; prefer chunk/cursor and set-based or batched work; cache repeated lookups (e.g. config, reference data).
- Long or heavy work: run in queues/jobs, not in the request; avoid blocking I/O in the hot path.
- Memory: unresolved references, uncleared timers/listeners/closures; for large datasets ensure chunk/cursor (not `get()`) and bounded batch size.
- Scalability: locking, queue depth, missing caching for hot paths, data structures or algorithms that do not scale with volume.

---

## 8. Code Quality & Technical Debt

**Compliance with project standards:**
- Naming: purpose-revealing; PascalCase/camelCase/kebab-case per type.
- Single responsibility; DTOs not `array<mixed>`; DRY; clear interfaces; no magic numbers (use constants).
- Do not re-check style, types, or issues that PHPStan/Rector/PHPCS/Pint already report.

**Focus on design:**
- Unnecessary complexity; large functions; repeated logic; oversized classes; mixed responsibilities.
- Recommend: simplify structure, improve cohesion, split large units.
- Rank issues by impact (highest technical debt first) when listing findings.

---

## 9. Security Review

**Focus on:** Issues static analysis may not fully trace: business-logic flaws, missing authorization checks, data flow to sensitive sinks.

**OWASP-oriented:** Injection (SQL, command, LDAP); XSS (stored/reflected); broken auth/session; sensitive data exposure; CSRF where state-changing actions lack protection.

**SQL injection:** Any raw SQL with user/request input must use prepared statements or ORM with bound parameters. Skip if PHPStan/plugins already flag.

**XSS:** Unescaped output, dynamic HTML, user input in UI require encoding/sanitization (e.g. Blade escaping, CSP).

**Auth and access control:** Permission checks on every sensitive action; server-side validation; safe token/session storage and rotation; no trust in client-only flags.

---

## 10. Tests

**Check:**
- Coverage for changed files only (target 100% for changes). Run tests only for changed files.
- New code is tested: arrange-act-assert; error cases first; descriptive names; data providers via argument; mock only external services.
- Identify missing test variations.
- Laravel: prefer `Http::fake()` over Mockery.

---

## 11. Output

**Deliver:** Brief summary: issues, risks, improvements. No code changes.

**Review best practices:**
- Give concrete fixes or code snippets where relevant; not only “something is wrong”.
- Evaluate code in project context and against `.cursor/rules/*.mdc`.
- Findings are recommendations; final decisions remain with the human reviewer.

---

## 12. Review Prompts (Scenarios)

Use these prompts to run a focused review for each priority area. Assume PHPStan, Rector, PHPCS, and Pint are already passing.

### 12.1 Large data processing

Review this code for handling large datasets. Check: (1) Is `get()` used on potentially large result sets? If yes, recommend `chunk()` or `cursor()` and explain when to use which. (2) Are there N+1 queries inside loops or chunk callbacks? Suggest eager loading or set-based updates. (3) Should this run in a queued job instead of the request? (4) Is batch size or memory bounded? Give concrete suggestions and code snippets where applicable.

### 12.2 Security risks

Review this code for security. Check: (1) All user/request input reaching SQL — is it parameterized or ORM-bound? Flag any concatenation or raw input in queries. (2) Output that includes user-controlled data — is it escaped/sanitized to prevent XSS? (3) State-changing actions — is CSRF protection present where needed? (4) Sensitive operations — is authorization checked on the server for the current user/role? (5) Tokens, secrets, or sensitive data — are they logged, exposed in responses, or stored insecurely? List only real risks and suggest concrete fixes.

### 12.3 SQL optimizations

Review the SQL and database usage in this code. Check: (1) Run EXPLAIN (or equivalent) mentally or note where it should be run; flag full table scans, high row estimates, Using filesort/temporary. (2) Are WHERE/JOIN/ORDER BY/GROUP BY columns indexed? Is there a composite index that matches the query shape? (3) Is `SELECT *` used? Recommend selecting only needed columns. (4) Is filtering/sorting/aggregation done in PHP instead of in the database? (5) Are there functions on indexed columns in WHERE (e.g. `DATE(col)`, `LOWER(col)`) that prevent index use? Suggest indexed-friendly alternatives and index changes.

### 12.4 Performance

Review this code for performance. Check: (1) N+1 queries — are relationships used in loops eager-loaded with `with()` or `load()`? (2) Are there nested loops over large collections or repeated DB/service calls that could be batched or cached? (3) Is heavy or long-running work done in the request instead of in a queue? (4) Are there obvious memory risks (e.g. loading large result sets with `get()`, or unbounded collections)? (5) For hot paths, is repeated data (e.g. config, reference data) cached? Give specific, actionable recommendations with code examples where helpful.
