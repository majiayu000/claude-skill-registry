---
name: committing-changes
description: Stage, validate, and commit changes with a clear message, optionally pushing to remote and monitoring CI. Use when committing code, creating a commit, pushing changes, or doing a commit-and-push workflow.
argument-hint: "[--push] [message hint]"
---

# Committing Changes

Auto-stage, validate, and commit changes. Pass `--push` to also push and monitor CI.

## Workflow

### 1. Detect VCS

```bash
if jj root 2>/dev/null; then
  # USE JJ WORKFLOW
else
  # USE GIT WORKFLOW
fi
```

**CRITICAL: Always use `-m` flag with jj** to prevent editor from blocking.

### 2. Clean Up Checkpoints

Abandon/squash any "checkpoint:" commits from Claude's Stop hook.

### 3. Check Branch Safety

Read `./CLAUDE.md` for project permissions. If on a protected branch without permission, suggest a feature branch. Cache decisions for future runs.

### 4. Run Validation

Auto-detect project type and run: format -> lint -> typecheck. Stop on failure.

### 5. Craft Commit Message

Use **conventional commits** format: `type(scope): description`

Valid types: `feat`, `fix`, `refactor`, `docs`, `style`, `perf`, `test`, `build`, `ci`, `chore`.

Choose type from the diff:

- New functionality → `feat`
- Bug fix → `fix`
- Code restructuring without behavior change → `refactor`
- CI/CD config → `ci`
- Build system, deps → `build`
- Documentation → `docs`

Scope is optional but encouraged for multi-module repos. Keep subject under 50 chars, use imperative mood ("add" not "added"). Focus on the "why" not the "what".

### 6. Commit

**jj workflow (preferred)**:

```bash
jj status && jj diff --stat
jj describe -m "feat: message here"
```

**git workflow (fallback)**:

```bash
git add <specific-files>
git commit -F /tmp/commit-msg.txt
```

Use the Write tool for commit message files (avoids shell escaping). Handle pre-commit hook failures by re-staging and retrying once.

### 7. Push (if --push or explicitly requested)

**jj**:

```bash
jj bookmark set <branch> -r @
jj git push --bookmark <branch>
```

**git**:

```bash
git push -u origin HEAD
```

### 8. Monitor CI (after push)

If `.github/workflows/` exists and `ci=github-actions` in hook output:

```bash
uv run ~/.claude/skills/monitoring-ci/ci-monitor.py --branch <branch-name>
```

Run in background. Tell user: "CI monitor running in background."

## Error Handling

- Ask user about unknown project permissions
- Stop on protected branch violations
- Auto-fix code quality issues using detected formatters/linters
- Re-stage once if pre-commit hooks fail (git only)
- For jj: use `jj op restore` if something goes wrong

## Safety Rules

- Never commit to protected branches without permission
- Use temporary files for all commit message operations
- Stop on merge conflicts
- Check branch protection before making changes
