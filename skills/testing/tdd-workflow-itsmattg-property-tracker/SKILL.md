---
name: tdd-workflow
description: Use when implementing features or bugfixes with test-driven development. Provides the full TDD workflow with environment spin-up, red-green-refactor, and PR creation.
disable-model-invocation: true
---

# TDD Development Workflow

Every feature must be test-driven and E2E validated. See `e2e/CLAUDE.md` for test standards and failure protocol.

## Steps

1. **Pick task** → `bd ready` / `bd show <id>`
2. **Create worktree** → branch from `develop`
   ```bash
   git worktree add ~/worktrees/property-tracker/<name> -b feature/<name> develop
   cp "$CLAUDE_PROJECT_DIR/.env.local" ~/worktrees/property-tracker/<name>/.env.local
   cd ~/worktrees/property-tracker/<name>
   ```
3. **Brainstorm** → use context7 for research + design exploration
4. **Plan** → `/feature-dev` or write plan manually following project conventions
   - For autonomous execution: follow with `/plan-to-epic` then `/ralph-execute`
5. **Write tests FIRST (Red)** → unit (Vitest) + E2E (Playwright)
6. **Spin up env** → confirm tests fail (invoke `/env-spinup`)
7. **Implement (Green)** → use context7, frontend-design, typescript-lsp, supabase as needed
8. **Validate** → full env restart, all tests pass
9. **Verify** → `npm run lint && npx tsc --noEmit && npm run build` (lint, types, build)
10. **PR** → `gh pr create --base develop` → `/code-review` → `gh pr checks --watch` → merge
11. **Cleanup** → remove worktree → `bd close <id>` → `/clear`

## Writer/Reviewer Pattern (for complex features)

After implementation (step 8), consider opening a second Claude Code session for review:
- Session B reviews with fresh context (no bias toward its own code)
- Use `/code-review` in Session B
- Address feedback in the original session (Session A)
