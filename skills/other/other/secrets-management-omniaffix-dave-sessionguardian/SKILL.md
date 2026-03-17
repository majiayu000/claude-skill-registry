---
name: secrets-management
description: Never commit secrets (API keys, passwords, tokens) to version control Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_secrets_management
---

# Secrets Management

Never commit secrets (API keys, passwords, tokens) to version control. Use environment variables or secret management services (AWS Secrets Manager, HashiCorp Vault). Add secret file patterns to .gitignore. Rotate secrets regularly. Use different secrets for development, staging, and production. Audit code for accidentally committed secrets. Consider using git-secrets or similar pre-commit hooks.