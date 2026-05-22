---
name: generic-code-reviewer
description: Review code for bugs, security vulnerabilities, performance issues, accessibility gaps, and CLAUDE.md workflow compliance. Supports any tech stack - HTML/CSS/JS, React, TypeScript, Node.js, Python, NestJS, Next.js, and more. Use when completing features, before commits, or reviewing pull requests.
---

# Generic Code Reviewer

Review code against production quality standards. Adapts to any project's tech stack.

**Full Standards:** See [Code Review Standards](./../_shared/CODE_REVIEW_STANDARDS.md)

## CLAUDE.md Compliance

**Always check the project's CLAUDE.md for specific rules.**

**Before ANY Commit:**

- Task file exists in `tasks/[feature-name].md`
- All tests passing
- Type checking passing (if TypeScript)
- No console errors/warnings
- Bundle size within limits

## Tech Stack Detection

| Detection               | Stack    | Key Checks                |
| ----------------------- | -------- | ------------------------- |
| React in package.json   | React/TS | Components, hooks, state  |
| Next.js in package.json | Next.js  | SSR, API routes           |
| NestJS in package.json  | NestJS   | Guards, DTOs, services    |
| .html files, no build   | Vanilla  | Semantic HTML, minimal JS |
| .py files               | Python   | Type hints, validation    |

## P0 Issues (Block Merge)

### Security - Frontend

- Sanitize input (textContent, not innerHTML)
- `unknown` type for external data
- No exposed API keys
- HTTPS for external requests

### Security - Backend

- Input validation on all endpoints
- Auth on protected routes
- Parameterized queries (no raw SQL)
- Secrets in environment variables

### Correctness

- Logic errors that break functionality
- Type errors in strict mode
- Unhandled promise rejections

## P1 Issues (Should Fix)

### Performance

| Project Type | Target                   |
| ------------ | ------------------------ |
| Static site  | < 50KB (excluding media) |
| SPA/React    | < 100KB gzipped initial  |
| Full-stack   | < 200KB gzipped initial  |

**Animation:**

- GPU-accelerated only (transform, opacity)
- 60fps target
- Use requestAnimationFrame

### Accessibility (WCAG AA)

- Focus indicators on interactive elements
- Keyboard navigation (Tab, Enter, Escape)
- Color contrast >= 4.5:1
- ARIA labels on icon-only buttons
- Alt text for meaningful images
- Semantic HTML structure

## P2 Issues (Nice to Have)

### Code Quality

- DRY, Single Responsibility
- No magic numbers/strings
- Self-documenting code
- Follow existing patterns
- No commented-out/dead code

## Review Output Format

Only report issues found (don't list empty categories):

**Blocking Issues (P0):**

- [Only if found - security, correctness issues]

**Should Fix (P1):**

- [Only if found - performance, accessibility issues]

**Consider (P2):**

- [Only if found - code quality polish]

**If no issues:** "Code review passed. Ready to merge."

## Judgment Calls

When user asks "Is this OK?", consider:

| Context         | Stricter                       | More Lenient                    |
| --------------- | ------------------------------ | ------------------------------- |
| **Environment** | Production                     | Prototype/POC                   |
| **Path**        | Hot path, frequently executed  | One-time setup, admin only      |
| **Visibility**  | Public API, external interface | Internal helper, private method |
| **Timeline**    | Feature complete               | Active iteration                |

Adjust severity accordingly. P0 security issues are never lenient.

## Quick Checklist

**Pre-Commit:**

- [ ] Tests pass
- [ ] Type/lint pass
- [ ] Build succeeds
- [ ] No console errors

**Before Merge:**

- [ ] All P0 issues resolved
- [ ] P1 issues addressed or tracked
- [ ] P2 issues noted for future

## See Also

- [Code Review Standards](./../_shared/CODE_REVIEW_STANDARDS.md) - Full requirements
- [Design Patterns](./../_shared/DESIGN_PATTERNS.md) - UI consistency
- Project `CLAUDE.md` - Workflow rules
