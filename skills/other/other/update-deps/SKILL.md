---
skill: update-deps
description: Update npm packages to latest versions with validation in isolated worktree
arguments: specific packages, glob pattern, or '.' for all
---

# Update Dependencies: $ARGUMENTS

Updates npm packages to their latest versions with automated testing and validation in an isolated worktree.

## Arguments

- **Specific packages**: `jest @types/jest`
- **All packages**: `.`
- **Glob patterns**: `@testing-library/* jest*`

## Process

### 1. Create Isolated Worktree

```bash
WORKTREE_NAME="npm-update-$(date +%Y%m%d-%H%M%S)"
WORKTREE_PATH="../$WORKTREE_NAME"
git worktree add "$WORKTREE_PATH" -b "$WORKTREE_NAME"
cd "$WORKTREE_PATH"
```

### 2. Identify Packages

- Parse `$ARGUMENTS` to determine packages
- For globs, expand against package.json dependencies
- For `.`, update all packages

### 3. Check and Update Versions

```bash
# Check latest version
npm view <package> version

# Prefer LTS when available
npm view <package> dist-tags

# Update packages
npm install <package>@latest
```

### 4. Run Security Audit

```bash
npm audit
npm audit fix
```

### 5. Validate Updates

Run in order, continue on failure to collect all errors:

```bash
npm run build
npm run lint
npm test
```

### 6. Handle Results

**On success:**
- Create commit with version changes
- Use AskUserQuestion to prompt:
  - "Yes, merge and clean up (Recommended)"
  - "No, I'll review first"
  - "Discard changes"

**On failure:**
- Categorize errors (build/lint/test/audit)
- Provide specific remediation steps
- Offer options: isolate problem, revert specific updates, or abandon

### 7. Cleanup

```bash
git worktree remove "$WORKTREE_PATH"
git branch -D "$WORKTREE_NAME"
```

## Error Categories

| Category | Examples | Remediation |
|----------|----------|-------------|
| Build | Type errors, missing deps | Update @types/*, check changelogs |
| Lint | Code style issues | Run `npm run lint -- --fix` |
| Test | Breaking API changes | Review migration guides |
| Audit | Vulnerabilities | Manual remediation steps |

## Edge Cases

- No package.json: Error with clear message
- Not a git repo: Error - worktree requires git
- Package not found: Suggest checking package name
- Glob matches nothing: Warn and list available packages
