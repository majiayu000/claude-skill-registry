---
name: Coding Conventions
description: Automatically apply standard coding conventions when writing or modifying code. Use this skill when working with Python, TypeScript, JavaScript, Go, PHP, or creating git commits. Triggers include writing new code, refactoring existing code, or committing changes in supported languages.
---

# Coding Conventions

## Supported Languages

- **Python** - PEP 8
- **TypeScript** - Google & Microsoft Style Guide
- **JavaScript** - Airbnb Style Guide
- **Go** - Effective Go & Google Style Guide
- **PHP** - PSR Standards
- **Git Commits** - Conventional Commits

## Workflow

When writing or modifying code:

1. **Identify the language** of the file being edited
2. **Read the appropriate convention file** from `references/` directory
3. **Apply conventions consistently** to naming, formatting, documentation, and organization

### Convention Files

- `references/python-conventions.md` - Python (PEP 8)
- `references/typescript-conventions.md` - TypeScript
- `references/javascript-conventions.md` - JavaScript (Airbnb)
- `references/golang-conventions.md` - Go
- `references/php-conventions.md` - PHP (PSR)
- `references/git-commit-conventions.md` - Git commit format

### Git Commit Quick Reference

Follow Conventional Commits format:

```
<type>(<scope>): <subject>
```

**Common types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Rules:**
- Imperative present tense: "add" not "added"
- Lowercase subject, no period
- Keep subject under 50 characters
- Include `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

**Example:**
```bash
feat(auth): add user authentication

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

For complete git commit guidelines, see `references/git-commit-conventions.md`.

## Priority Rules

1. **Project-specific conventions** override language defaults
2. **Existing code style** should be matched for consistency
3. **Automatic tools** (ESLint, Prettier, gofmt) should be respected if configured
4. **Convention files** provide the default standards
