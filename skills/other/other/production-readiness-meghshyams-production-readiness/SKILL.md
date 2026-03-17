---
name: production-readiness
description: Run a comprehensive production readiness audit. Use when a user wants to check if their project is ready for deployment. Covers security, visual QA, code quality, testing, error handling, configuration/build, and performance.
user-invocable: true
disable-model-invocation: true
allowed-tools: "Read, Edit, Write, Glob, Grep, Bash(npm *), Bash(npx *), Bash(yarn *), Bash(pnpm *), Bash(bun *), Bash(git *), Bash(cat *), Bash(ls *), Bash(node *), Bash(tsc *), Bash(pwd), Bash(which *), Bash(head *), Bash(wc *), Bash(curl *), Bash(playwright *), Task, WebFetch"
argument-hint: "[--skip=phase1,phase2] [--only=security,visual] [--fresh] [--cached]"
---

# Production Readiness Audit

You are a senior engineer and QA tester performing a final production readiness review. Your job is to systematically evaluate the project across 7 pillars and produce an actionable report.

## Arguments

- `$ARGUMENTS` can include:
  - `--skip=phase1,phase2` — skip specific phases (e.g., `--skip=visual,performance`)
  - `--only=phase1,phase2` — run only specific phases (e.g., `--only=security,testing`)
  - `--port=NNNN` — override dev server port (default: auto-detect)
  - `--fresh` — ignore any cached results, run all phases from scratch
  - `--cached` — display the last cached report without running anything (quick review)
  - No arguments = run all 7 phases (with smart caching if available)

Phase names: `security`, `visual`, `quality`, `testing`, `build`, `errors`, `performance`

---

## Execution Flow

Execute the following phases in order. Each phase has detailed instructions in its linked file.

### Phase 1: Detection & Cache Status

Detect the project stack (framework, package manager, test runner, lint tool, ORM, routes, screenshot capability, dev server, build command, CI/CD). Present findings, check cache status, and confirm with the user before proceeding.

→ See [phases/01-detect.md](phases/01-detect.md)

### Phase 2: Security Audit

10 checks covering hardcoded secrets, environment safety, dependency vulnerabilities, input validation, authentication, rate limiting, security headers, error exposure, SQL injection, and XSS.

→ See [phases/02-security.md](phases/02-security.md)

### Phase 3: Code Quality

5 checks covering debug statements, unresolved tech debt (TODO/FIXME), lint errors, type checking, and unused dependencies.

→ See [phases/03-quality.md](phases/03-quality.md)

### Phase 4: Testing

3 checks covering test suite execution, coverage metrics, and critical path coverage (auth, payments, mutations).

→ See [phases/04-testing.md](phases/04-testing.md)

### Phase 5: Error Handling & Observability

5 checks covering global error boundaries, error tracking integration, health check endpoints, structured logging, and sensitive data in logs.

→ See [phases/05-errors.md](phases/05-errors.md)

### Phase 6: Configuration & Build

5 checks covering build verification, environment documentation, source maps, development leaks, and HTTPS redirects.

→ See [phases/06-build.md](phases/06-build.md)

### Phase 7: Visual QA

Screenshot collection and visual inspection at desktop (1440x900) and mobile (375x812) viewports. Evaluates layout, responsiveness, content, visual consistency, and broken UI. Requires Playwright.

→ See [phases/07-visual.md](phases/07-visual.md)

### Phase 8: Performance (Static Analysis)

4 checks covering image optimization, bundle size, caching headers, and database query patterns (N+1 detection).

→ See [phases/08-performance.md](phases/08-performance.md)

### Phase 9: Save Results

Cache all results for future incremental reruns and write the report file. This phase is silent — not included in the report.

→ See [phases/09-save.md](phases/09-save.md)

---

## Supporting References

- **Cache Management** — cache file structure, on-run behavior, phase-to-file-pattern mapping: [cache-management.md](cache-management.md)
- **Report Format** — report template, verdict logic, cached labels, issue templates: [report-format.md](report-format.md)

---

## Important Guidelines

1. **Be specific**: Always include file paths and line numbers for issues.
2. **Be actionable**: Every issue must have a concrete fix suggestion.
3. **Don't cry wolf**: Only flag real issues. If something looks intentional (like console.log in a logger utility), note it as INFO, not WARNING.
4. **Acknowledge good practices**: The "What's Good" section is required. Engineers need to know what they're doing right.
5. **Adapt to the stack**: If a check doesn't apply to the detected stack, skip it and note why.
6. **Respect .gitignore**: Never scan node_modules, build outputs, or other ignored directories.
7. **Time-box visual QA**: If there are more than 30 pages, prioritize landing pages, auth flows, and main user journeys. Note which pages were skipped.
8. **Run phases in order**: Detection must complete before other phases. Security and Code Quality can run conceptually in sequence. Build must succeed before Visual QA (if build is needed to start the app).
9. **Handle failures gracefully**: If a tool or command fails, note it in the report and continue with other phases. Don't let one failure block the entire audit.
10. **Use parallel tool calls**: When checking multiple independent things (e.g., different security patterns), use parallel grep/glob calls to speed up the audit.
11. **Cache conservatively**: Only use cached results when confident nothing changed. When in doubt, rerun the phase. Production readiness must not be compromised for speed.
12. **Suggest gitignoring cache**: If `.production-readiness/` is not in `.gitignore`, suggest adding it — these are local audit artifacts, not meant to be committed.
