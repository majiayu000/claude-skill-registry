---
name: secrets-management
description: Safe handling of API keys, Vault/AWS Secrets Manager patterns, rotation.
role: ops-security
triggers:
  - secret
  - api key
  - password
  - credential
  - rotation
  - .env
---

# secrets-management Skill

This skill enforces the zero-trust handling of credentials.

## 1. The Core Commandments
1.  **NEVER** commit secrets to Git. (Not even encrypted, if possible).
2.  **NEVER** log secrets to stdout/files.
3.  **LEAST PRIVILEGE**: An App's DB user should not be `postgres` (superuser).

## 2. Storage Patterns

### Level 1: Environment Variables (.env)
- **Dev**: `.env` file (gitignored).
- **Prod**: Injected by platform (Vercel/Heroku env vars).
- *Risk*: Shell history exposure, accidental printenv.

### Level 2: Secret Ops (SOPS / Encrypted Git)
- Secrets stored in git but encrypted with KMS/PGP.
- Decrypted only at build/deploy time.
- *Tool*: Mozilla SOPS, git-crypt.

### Level 3: Secret Manager (The Standard)
- AWS Secrets Manager, Google Secret Manager, HashiCorp Vault.
- App fetches secret at runtime via SDK or Sidecar.
- *Pros*: Rotation, Audit trails.

## 3. Secret Rotation
- **Static Secrets** (API Keys): Rotate every 90 days.
- **Dynamic Secrets** (Db Creds): Vault creates a credential *per session* that expires in 1h.

## 4. Detection (Pre-Commit)
- Use `gitleaks` or `trufflehog` in CI/CD.
- If a secret is committed:
  1.  **Revoke it immediately**.
  2.  Rotate the key.
  3.  Rewrite git history (BFG Repo Cleaner) - optional but recommended.

## 5. Kubernetes Secrets
- Default K8s Secrets are base64 encoded (NOT encrypted).
- **Requirement**: Enable Encryption-at-Rest for etcd.
- **Better**: Use "External Secrets Operator" to sync from AWS/Vault.
