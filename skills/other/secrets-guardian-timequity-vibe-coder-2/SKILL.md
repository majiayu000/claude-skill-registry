---
name: secrets-guardian
description: |
  Protect repositories from accidental secret commits. Essential when working with AI agents.
  Use when: setting up new project, adding pre-commit hooks, scanning for secrets, fixing leaked credentials.
  Triggers: "настрой защиту секретов", "setup secrets", "check secrets", "scan secrets", "проверь секреты", "pre-commit", "gitleaks".
  PROACTIVELY suggest when creating new projects or when .pre-commit-config.yaml is missing.
---

# Secrets Guardian

Multi-layered protection against accidental secret commits. Critical for AI-assisted development where agents may not recognize sensitive data.

## Quick Setup

For new projects, run this setup:

```bash
# 1. Check if pre-commit is installed
which pre-commit || pip install pre-commit

# 2. Copy pre-commit config from assets
# See assets/pre-commit-config.yaml

# 3. Create secrets baseline
echo '{"version": "1.5.0", "results": {}}' > .secrets.baseline

# 4. Install hooks
pre-commit install
pre-commit install --hook-type pre-push

# 5. Verify .gitignore has secret patterns
# See assets/gitignore-secrets
```

## Commands

### Setup Protection

When user says "настрой защиту секретов" or "setup secrets protection":

1. **Check existing setup:**
```bash
ls -la .pre-commit-config.yaml .secrets.baseline .gitignore 2>/dev/null
```

2. **If .pre-commit-config.yaml missing:**
   - Copy from `assets/pre-commit-config.yaml`
   - Or add secret scanning hooks to existing config

3. **Check .gitignore for secret patterns:**
```bash
grep -E "\.env|\.key|API_KEY|secret" .gitignore
```
   - If missing, append patterns from `assets/gitignore-secrets`

4. **Create .secrets.baseline:**
```bash
echo '{"version": "1.5.0", "results": {}}' > .secrets.baseline
```

5. **Install hooks:**
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

6. **Ask about CI/CD:**
   - "Добавить GitHub Actions workflow для проверки секретов в CI?"
   - If yes, copy `assets/security-workflow.yaml` to `.github/workflows/`

### Scan for Secrets

When user says "проверь секреты" or "check secrets":

```bash
# Quick scan with gitleaks
gitleaks detect --no-git -v

# Detailed scan with detect-secrets
detect-secrets scan --all-files
```

Report findings and suggest fixes.

### Fix Leaked Secret

When secret is detected:

1. **Identify the secret type** (API key, password, private key, etc.)

2. **Suggest remediation:**
   - Move to `.env` file (ensure it's in .gitignore)
   - Use environment variable: `os.environ.get("API_KEY")`
   - For false positives: update `.secrets.baseline`

3. **If already committed:**
   - Rotate the credential immediately
   - Consider git history cleanup (if not pushed)
   - Warn about exposed secrets in git history

### Update Baseline

For false positives, update the baseline:

```bash
detect-secrets scan --baseline .secrets.baseline
```

## Proactive Checks

**IMPORTANT:** When working in any project, check for secret protection:

```bash
# Quick check
if [ ! -f .pre-commit-config.yaml ]; then
  echo "WARNING: No pre-commit config found"
fi
```

If missing, ask user: "В проекте нет защиты от утечки секретов. Настроить?"

## Reference Files

- [Setup Guide](references/setup-guide.md) - Detailed installation steps
- [Tools Reference](references/tools-reference.md) - gitleaks, detect-secrets, etc.

## Asset Files

Copy these to project as needed:

- `assets/pre-commit-config.yaml` - Pre-commit hooks configuration
- `assets/gitignore-secrets` - Patterns to add to .gitignore
- `assets/security-workflow.yaml` - GitHub Actions CI workflow
