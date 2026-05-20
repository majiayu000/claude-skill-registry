---
name: dev-workflow
description: >
  Comprehensive TDD development workflow for FuzzyCat. Enforces test-driven development,
  post-implementation review, ripple-effect analysis, technical debt check, and Playwright
  UI verification. Use this for any non-trivial code change.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent
---

# FuzzyCat Development Workflow

This skill enforces a mature, disciplined development process for every non-trivial change.
Follow ALL phases in order. Do not skip phases.

## Phase 1: Understand & Plan

1. **Read the requirement** thoroughly. Understand what is being asked.
2. **Explore the codebase** to understand existing patterns and affected areas.
   - Use Ollama (`ollama.sh summarize`) to quickly understand files.
   - Identify ALL files that will need changes (not just the obvious ones).
3. **Identify ripple effects** — what other parts of the app reference or depend on the code
   being changed? Use `Grep` to find all callers, importers, and test files.
4. **Write the plan** in a TaskList before writing any code.

## Phase 2: Test-Driven Development

5. **Write tests FIRST** — before any implementation code.
   - Unit tests for new functions/services (`server/services/*.test.ts`)
   - Integration tests for tRPC procedures if applicable
   - Tests should cover: happy path, edge cases, error cases, boundary values
   - Use `bun:test` (not Jest/Vitest). Follow existing test patterns.
   - Tests MUST fail initially (red phase of TDD).
6. **Run the failing tests** to confirm they fail for the right reason:
   ```bash
   bun run test -- --filter "test-file-name"
   ```

## Phase 3: Implement

7. **Write the minimum code** to make tests pass (green phase).
8. **Run the specific tests** to verify they pass:
   ```bash
   bun run test -- --filter "test-file-name"
   ```
9. **Refactor** if needed while keeping tests green.

## Phase 4: Verify Locally

10. **Run the full test suite**:
    ```bash
    bun run test
    ```
11. **Run isolated tests** (files that need process-level isolation):
    ```bash
    for f in tests/isolated/*.test.ts; do bun test "$f"; done
    ```
12. **Run type checker and linter**:
    ```bash
    bun run typecheck && bun run check
    ```
    Fix any issues. If Biome formatting fails, run `bun run check:fix`.

## Phase 5: Self-Review

13. **Review your own diff** — examine every changed line:
    ```bash
    git diff | .claude/skills/ollama/ollama.sh diff
    ```
    Then also review it yourself. Check for:
    - Accidental debug code (console.log, TODO comments)
    - Security issues (SQL injection, XSS, exposed secrets)
    - Missing null checks or error handling at boundaries
    - Correct integer cents for all monetary values
    - Audit trail logging for payment state changes

14. **Ripple-effect analysis** — search for things you might have missed:
    - Grep for any functions/types/constants you renamed or removed
    - Check if any other pages, components, or API routes reference changed code
    - Check if `lib/constants.ts` values need updating
    - Check if `.env.example` needs new vars
    - Check if CLAUDE.md documentation needs updating

15. **Technical debt check** — did your changes introduce or reveal:
    - Duplicate code that should be extracted?
    - Dead code that should be removed?
    - Missing types (any `any` in financial logic)?
    - Inconsistent patterns vs the rest of the codebase?

## Phase 6: Playwright UI Verification

16. **Start dev server** (if not running) and verify in browser:
    ```bash
    bun run dev &
    ```
17. **Navigate to affected pages** using Playwright MCP and verify:
    - Pages render without errors
    - Interactive elements work (buttons, forms, dropdowns)
    - Data displays correctly
    - No console errors (check with `browser_console_messages`)
    - Mobile responsiveness (resize to 375px width)
18. **Test the full user flow** — don't just check the page you changed. Walk through
    the user journey that touches your changes.

## Phase 7: Commit & PR

19. **Commit** with conventional format:
    ```bash
    git add <specific-files>
    git commit -m "feat: description" # or fix:, chore:, etc.
    ```
20. **Push and create PR** with summary, test plan, and verification notes.
21. **Wait for CI** — all checks must pass.
22. **Merge** via squash merge.

## Phase 8: Production Verification

23. **Wait for Vercel deployment** to complete.
24. **Verify on production** using Playwright MCP:
    - Navigate to affected pages on `https://www.fuzzycatapp.com`
    - Check console for errors
    - Test the user flow end-to-end
25. **Check Sentry** for any new errors:
    ```bash
    npx @sentry/cli issues list --project javascript-nextjs -s unresolved
    ```
26. **Check production health**:
    ```bash
    curl -sL https://www.fuzzycatapp.com/api/health | jq .status
    ```

## Quick Reference: Commands

```bash
# Tests
bun run test                          # All unit tests
bun run test -- --filter "name"       # Specific test
for f in tests/isolated/*.test.ts; do bun test "$f"; done  # Isolated tests

# Quality
bun run typecheck                     # TypeScript check
bun run check                         # Biome lint + format
bun run check:fix                     # Auto-fix formatting

# Review
git diff --staged | .claude/skills/ollama/ollama.sh diff   # AI diff review
.claude/skills/ollama/ollama.sh review <file>              # AI code review

# Production
curl -sL https://www.fuzzycatapp.com/api/health | jq .status
npx @sentry/cli issues list --project javascript-nextjs -s unresolved
vercel ls | head -5
```
