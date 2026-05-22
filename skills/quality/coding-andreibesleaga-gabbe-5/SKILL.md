---
name: code-review
description: Systematic code review covering security, performance, architecture, and style
triggers: [review, PR, audit, code quality, pull request, check this code]
context_cost: medium
---

# Code Review Skill

## Goal
Produce a structured, actionable code review covering: security vulnerabilities, performance issues, architectural violations, and code style — in that priority order.

## Steps

1. **Gather diff**
   - Run `git diff main...HEAD` (or the target branch) to see all changes
   - Note the files changed and their layers (domain, application, infrastructure, etc.)

2. **Security review** (highest priority)
   - Scan for: SQL injection, XSS, CSRF, path traversal, command injection
   - Check: secrets or API keys hardcoded in code
   - Check: authentication/authorization logic bypasses
   - Check: input validation at system boundaries (HTTP, file upload, CLI)
   - Check: `npm audit` / `composer audit` output for new vulnerable deps
   - Flag severity: CRITICAL | HIGH | MEDIUM | LOW

3. **Architecture review**
   - Verify layer imports: does any inner layer import from an outer layer?
   - Check for circular dependencies (run `madge --circular src` or `deptrac`)
   - Check: are new classes/functions in the correct layer?
   - Check: does any new code violate AGENTS.md architecture rules?

4. **Performance review**
   - Identify N+1 query patterns in any database access code
   - Check: are expensive operations cached where appropriate?
   - Check: are there unnecessary synchronous operations that could be async?
   - Check: unbounded loops over large datasets without pagination

5. **Code quality review**
   - Check: Cyclomatic complexity (functions > 10 → flag for refactor)
   - Check: function/class length (functions > 30 lines, files > 300 lines → flag)
   - Check: code duplication (same logic > 3 occurrences → suggest abstraction)
   - Check: naming (variables, functions, classes follow project conventions)
   - Check: dead code (unused variables, unreachable branches, unused exports)

6. **Test coverage review**
   - Check: are new public functions covered by tests?
   - Check: are new edge cases covered (null inputs, error paths, boundaries)?
   - Check: no test bypasses (`.skip`, `.only` left in production branch)

7. **Produce structured report**
   ```markdown
   ## Code Review Report

   ### Security Findings
   - [CRITICAL/HIGH/MEDIUM/LOW] file.ts:42 — Description + fix recommendation

   ### Architecture Violations
   - file.ts:15 imports from infrastructure layer — violates Clean Architecture

   ### Performance Concerns
   - N+1 query pattern in UserService.getAll() — add eager loading

   ### Code Quality
   - getUserData() has complexity 14 — extract validation into separate function

   ### Tests
   - Missing test for null email edge case in UserValidator

   ### Approved Changes
   - [list of changes that look good]

   ### Summary
   MERGE: [YES/NO/WITH_CHANGES]
   Blocking issues: [count]
   ```

## Constraints
- Security findings are always blocking (must be fixed before merge)
- Architecture violations are always blocking
- Performance and quality findings may be non-blocking based on severity
- Never approve a PR with hardcoded secrets or critical CVEs

## Output Format
Structured markdown report with severity-tagged findings and specific file:line references.
