---
name: safe-repo
description: Check for sensitive data in repository. Use when user asks to "check for sensitive data", "/safe-repo", or wants to verify no company/credential data is in the repository.
---

# Safe Repository Check

## Context

Security audit for sensitive data in repository. Check for credentials, API keys, company-specific information, and PII.

## Workflow

1. Get tracked files: `git ls-files` (avoids local gitignored files)
2. Search for credential patterns (see `patterns.md`):
   - API keys, passwords, tokens, AWS credentials
   - Private key files (.pem, .key, _rsa)
3. Check for sensitive tracked files (.env, secrets)
4. Analyze git history for removed secrets
5. Review `.gitignore` for proper patterns
6. Report findings (see `report-template.md`)

## Rules

- **Only check git-tracked files** (`git ls-files`) - ignore local configs
- Check current tracked files AND git history
- Filter false positives: minified JS, node_modules, test fixtures, docs
- Verify `.gitignore` covers sensitive patterns
- Report tracked files with secrets and historical commits
- Never output actual secret values in report
