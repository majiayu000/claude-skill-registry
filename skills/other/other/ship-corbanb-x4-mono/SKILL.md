---
name: ship
description: Branch, commit, and open a pull request with quality checks
---

# Ship Skill

Create a branch, commit changes, and open a pull request with quality checks.

## Arguments

The user describes what they're shipping. If unclear, ask for:

- What changed (feature, fix, refactor, etc.)
- Branch name (or auto-generate from description)

## Workflow

### 1. Pre-flight Checks

Run these in parallel to validate the codebase:

```bash
bun turbo type-check    # TypeScript
bun turbo lint          # ESLint + boundaries
bun turbo test          # All tests
```

If any fail, stop and report. Do not ship broken code.

### 2. Review Changes

```bash
git status              # See what's changed
git diff                # Review unstaged changes
git diff --staged       # Review staged changes
```

Review the changes for:

- Accidental files (`.env.local`, `node_modules`, etc.)
- Unrelated changes mixed in
- Missing files that should be included

### 3. Create Branch

If not already on a feature branch:

```bash
git checkout -b {type}/{short-description}
```

Branch naming conventions:

- `feat/add-user-notifications`
- `fix/login-redirect-loop`
- `refactor/extract-auth-middleware`
- `docs/update-api-reference`
- `chore/update-dependencies`

### 4. Stage and Commit

Stage specific files (never `git add -A` blindly):

```bash
git add apps/api/src/routers/comments.ts
git add packages/shared/utils/validators.ts
# etc.
```

Commit with a descriptive message:

```bash
git commit -m "$(cat <<'EOF'
feat: add comment router with CRUD operations

- Create comments router with list/get/create/update/delete
- Add Zod schemas for comment validation
- Wire into appRouter
- Add ownership checks for mutations

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### 5. Push and Create PR

```bash
git push -u origin {branch-name}
```

Create PR with structured description:

```bash
gh pr create --title "feat: add comment router" --body "$(cat <<'EOF'
## Summary
- Add CRUD router for comments with ownership checks
- Create Zod schemas for comment input/output validation
- Register in appRouter with OpenAPI meta

## Test plan
- [ ] `bun turbo type-check` passes
- [ ] `bun turbo lint` passes
- [ ] `bun test --cwd apps/api` passes
- [ ] Manual test: create/read/update/delete comments via API

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## Rules

- **Never force push** — coordinate with the team
- **Never push to main directly** — always use a PR
- **Never commit `.env.local`** — only `.env.example` is tracked
- **Never commit with `--no-verify`** — let hooks run
- **Always stage specific files** — review what you're including
- **Always run checks first** — don't ship broken code
- **Never skip tests** — if tests fail, fix them first

## Commit Message Format

```
type: short description

- Detail 1
- Detail 2

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `perf`
