---
name: tech-debt
description: Run a structured technical debt scan across the STG codebase with prioritized findings
invocation: user
---

# Technical Debt Scanner

You are a technical debt analyst for Second Turn Games. Run a structured, repeatable scan and produce a concise, prioritized report.

## Modes

- **Full scan** (default): `/tech-debt` — all 12 categories
- **Focused scan**: `/tech-debt [category]` — deep dive into one category (e.g. `/tech-debt types`, `/tech-debt tests`)

## Scan Categories

| # | Category | Severity | What to Scan |
|---|----------|----------|--------------|
| 1 | Test Coverage | Critical | Glob `*.test.*` / `*.spec.*` files; check for test scripts in package.json |
| 2 | Security | Critical | Grep for hardcoded secrets, missing input validation in API routes |
| 3 | Type Safety | High | Grep for `: any`, `as any`, `@ts-ignore`, `@ts-expect-error` |
| 4 | Dead Code | High | Grep for exports not imported elsewhere; check git status for deleted files still referenced |
| 5 | Error Handling | High | Grep catch blocks; flag catch-and-ignore or console.error-only patterns |
| 6 | DB Schema | High | Use Supabase MCP `get_advisors` for both `security` and `performance` checks |
| 7 | Component Complexity | Medium | Find `.tsx` files >300 lines; list top 10 largest |
| 8 | Code Suppressions | Medium | Grep `eslint-disable`; group by rule name and count per rule |
| 9 | TODO Markers | Medium | Grep `TODO\|FIXME\|HACK\|XXX` with file paths |
| 10 | i18n Gaps | Medium | Grep for hardcoded English strings in components outside `useTranslations` |
| 11 | Dependency Health | Medium | Read package.json; identify unused and missing dependencies |
| 12 | Console Pollution | Low | Grep `console\.(log\|warn\|error)` with count per file |

## Execution Strategy

Dispatch **3 parallel Explore agents** for speed:

- **Agent 1** (Critical/High): Categories 1-3 (tests, security, types)
- **Agent 2** (High): Categories 4-5 (dead code, error handling)
- **Agent 3** (Medium/Low): Categories 7-12 (complexity, suppressions, TODOs, i18n, deps, console)

Run **Category 6 (DB Schema)** in the main context since it requires Supabase MCP tools.

For focused mode, run a single deep-dive agent on the requested category with verbose output (file paths, line numbers, code snippets).

## Report Format

```markdown
# Tech Debt Report — [date in dd.MM.yyyy]

## Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High     | X |
| Medium   | X |
| Low      | X |

## Top 5 Priority Items

1. **[Item]** (Critical) — [file path] — [why it matters]
2. ...

## Findings by Category

### [Category] — [Severity]
- [Finding with file path and line number]
- [Finding...]
**Action:** [specific next step]
```

## Severity Definitions

| Level | Criteria |
|-------|----------|
| Critical | Security risk, data loss potential, or zero safety net (e.g. no tests for financial logic) |
| High | Maintainability blocker or performance impact in production |
| Medium | Code quality issue that increases future maintenance burden |
| Low | Convention inconsistency or minor cleanup opportunity |

## Rules

- Use Grep and Glob tools (not bash grep/find)
- Use Supabase MCP `get_advisors` for DB checks (project ID: `ettbijaifahenypkmsts`)
- No exclamation marks, no emojis in the report
- No time estimates — report what exists, not how long it takes to fix
- Straightforward, actionable tone
- Include file paths as clickable markdown links: `[file.tsx](path/to/file.tsx)`
