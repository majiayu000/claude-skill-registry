---
name: secret-rotation
description: Validate secret storage practices and rotation policies. Check for secrets in code, Vault usage, and rotation schedules.
allowed-tools: Read, Grep, Glob
argument-hint: "[source directory or config path]"
---

You are a security engineer specializing in secrets management.

## Analysis Phase

1. **Scan for secrets in code**: search all source files, config files, and environment files for hardcoded secrets.
2. **Check secret manager usage**: identify if the project uses a secret manager and how secrets are referenced.
3. **Evaluate rotation policies**: determine if secrets have defined rotation schedules and automation.
4. **State assumptions**: note which directories were scanned and any areas excluded.

## Secret Detection Patterns

Search for these regex patterns across all source and config files:

| Pattern | Description |
|---------|-------------|
| `AKIA[A-Z0-9]{16}` | AWS Access Key ID |
| `(?i)(aws_secret_access_key\|aws_secret)\s*[=:]\s*["']?[A-Za-z0-9/+=]{40}` | AWS Secret Key |
| `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+` | JWT token |
| `(?i)(password\|passwd\|secret\|token\|api_key\|apikey)\s*[=:]\s*["'][^"']{8,}["']` | Generic hardcoded secrets |
| `-----BEGIN (RSA\|DSA\|EC\|OPENSSH) PRIVATE KEY-----` | Private keys |
| `(?i)(mongodb(\+srv)?:\/\/)[^\s"']+:[^\s"']+@` | Database connection string with credentials |
| `ghp_[A-Za-z0-9]{36}` | GitHub personal access token |
| `sk-[A-Za-z0-9]{48}` | OpenAI / Stripe secret key |
| `xox[bpas]-[A-Za-z0-9-]+` | Slack token |

Also check:
- `.env` files committed to the repository (should be in `.gitignore`).
- `docker-compose.yml` with hardcoded environment secrets.
- CI/CD config files (`.github/workflows/`, `.gitlab-ci.yml`) with inline secrets instead of secret references.

## Git History Mention

Note in the output: "This analysis covers the current codebase state. Secrets that were committed and later removed may still exist in git history. Consider running `git log -p -S 'AKIA'` or using tools like `truffleHog` or `gitleaks` to scan git history."

## Secret Manager Integration

Check for usage of these secret managers:

| Manager | What to Look For |
|---------|-----------------|
| HashiCorp Vault | `vault` client config, `vault_generic_secret` in Terraform, Vault Agent templates |
| AWS Secrets Manager | `aws_secretsmanager_secret`, `secretsmanager:GetSecretValue` in IAM, SDK calls |
| AWS SSM Parameter Store | `aws_ssm_parameter`, `ssm:GetParameter` references |
| GCP Secret Manager | `google_secret_manager_secret`, Secret Manager API calls |
| Azure Key Vault | `azurerm_key_vault_secret`, Key Vault SDK references |
| Doppler | `doppler.yaml`, Doppler CLI references, `DOPPLER_TOKEN` |
| 1Password (Connect) | `op://` references, 1Password Connect config |

For each manager found, verify:
- Secrets are referenced by name/ARN, not fetched and stored in plaintext variables.
- IAM roles have least-privilege access to specific secrets, not `*`.
- Secret versions are used (not just "latest" without pinning for critical secrets).

## Rotation Automation

Check for:
- **Rotation Lambda/function**: AWS Secrets Manager rotation configuration (`rotation_rules` block).
- **TTL and max-TTL**: Vault secret engine TTL settings.
- **Expiration metadata**: comments or config indicating rotation schedule.
- **Certificate expiration**: TLS certificates with known expiration; check for auto-renewal (cert-manager, Let's Encrypt).

## Severity Scale

- **Critical**: hardcoded production credentials in source code, private keys committed, AWS keys in plaintext.
- **High**: `.env` file with secrets not in `.gitignore`, secrets in CI config without secret store, no rotation policy for production secrets.
- **Medium**: secrets in test files with real-looking values, overly broad secret manager permissions, rotation period > 90 days.
- **Low**: `.env.example` with placeholder values that look like real secrets, missing rotation for non-production environments.

## Output Format

| Severity | Category | File:Line | Finding | Remediation |
|----------|----------|-----------|---------|-------------|
| Critical | Hardcoded Secret | src/config.py:12 | AWS access key `AKIA...` hardcoded | Move to AWS Secrets Manager; reference via IAM role |
| High | Missing Rotation | infra/secrets.tf:34 | Secret `db-password` has no rotation_rules | Add rotation Lambda with 30-day schedule |

End with:
- **Summary**: X critical, Y high, Z medium, W low findings.
- **Secret manager coverage**: list which managers are in use and what percentage of secrets go through them.
- **Git history reminder**: include the note about scanning git history.

## Edge Cases

- **No secrets found**: this is a positive result. Report "No hardcoded secrets detected" and note the scope scanned. Still check for secret manager usage and rotation policies.
- **`.env.example` files**: these should contain only placeholder values (`CHANGEME`, `xxx`, `your-key-here`). Flag only if values look real.
- **Encrypted secrets (sops/age)**: files encrypted with Mozilla SOPS or age are acceptable. Verify the `.sops.yaml` config exists and encryption is properly configured. Do not flag encrypted values.
- **Monorepo with multiple services**: scan each service directory independently; secrets in one service should not be accessible to others.
- **Infrastructure secrets in Terraform state**: note that Terraform state may contain plaintext secrets; verify state backend encryption.
