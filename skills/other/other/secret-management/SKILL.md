---
name: managing-secrets
description: Managing secrets (API keys, database credentials, certificates) with Vault, cloud providers, and Kubernetes. Use when storing sensitive data, rotating credentials, syncing secrets to Kubernetes, implementing dynamic secrets, or scanning code for leaked secrets.
---

# Managing Secrets

Secure storage, rotation, and delivery of secrets (API keys, database credentials, TLS certificates) for applications and infrastructure.

## When to Use This Skill

Use when:
- Storing API keys, database credentials, or encryption keys
- Implementing secret rotation (manual or automatic)
- Syncing secrets from external stores to Kubernetes
- Setting up dynamic secrets (database, cloud providers)
- Scanning code for leaked secrets
- Implementing zero-knowledge patterns
- Meeting compliance requirements (SOC 2, ISO 27001, PCI DSS)

## Quick Decision Frameworks

### Framework 1: Choosing a Secret Store

| Scenario | Primary Choice | Alternative |
|----------|----------------|-------------|
| Kubernetes + Multi-Cloud | Vault + ESO | Cloud Secret Manager + ESO |
| Kubernetes + Single Cloud | Cloud Secret Manager + ESO | Vault + ESO |
| Serverless (AWS Lambda) | AWS Secrets Manager | AWS Parameter Store |
| Multi-Cloud Enterprise | HashiCorp Vault | Doppler (SaaS) |
| Small Team (<10 apps) | Doppler, Infisical | 1Password Secrets Automation |
| GitOps-Centric | SOPS (git-encrypted) | Sealed Secrets (K8s-only) |

**Decision Tree:**
- Kubernetes? → External Secrets Operator (ESO) with chosen backend
- Single cloud? → Cloud-native (AWS/GCP/Azure)
- Multi-cloud/on-prem? → HashiCorp Vault
- GitOps? → SOPS or Sealed Secrets

### Framework 2: Static vs. Dynamic Secrets

| Secret Type | Use Dynamic? | TTL | Solution |
|-------------|-------------|-----|----------|
| Database credentials | YES | 1 hour | Vault DB engine |
| Cloud IAM (AWS/GCP) | YES | 15 min | Vault cloud engine |
| SSH/RDP access | YES | 5 min | Vault SSH engine |
| TLS certificates | YES | 24 hours | Vault PKI / cert-manager |
| Third-party API keys | NO | Quarterly | Vault KV v2 (manual rotation) |

### Framework 3: Kubernetes Secret Delivery

| Method | Use Case | Rotation | Restart Required |
|--------|----------|----------|------------------|
| **External Secrets Operator** | Static secrets, periodic sync | Polling (1h) | Yes |
| **Secrets Store CSI Driver** | File-based, watch rotation | inotify | No |
| **Vault Secrets Operator** | Vault-specific, dynamic | Automatic renewal | Optional |

## HashiCorp Vault Fundamentals

### Core Components

- **Secrets Engines**: KV v2 (static), Database (dynamic), AWS, PKI, SSH
- **Auth Methods**: Kubernetes, JWT/OIDC, AppRole, LDAP
- **Policies**: HCL-based access control (least privilege)
- **Leases**: TTL for secrets, auto-renewal, auto-revocation

### Static Secrets (KV v2)

```bash
# Create secret
vault kv put secret/myapp/config api_key=sk_live_EXAMPLE

# Read secret
vault kv get secret/myapp/config

# List versions
vault kv metadata get secret/myapp/config
```

### Dynamic Database Credentials

```bash
# Configure PostgreSQL
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb"

# Create role
vault write database/roles/app-role \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\"..." \
  default_ttl="1h"

# Generate credentials
vault read database/creds/app-role
```

For detailed Vault architecture, see `references/vault-architecture.md`.

## Kubernetes Integration

### External Secrets Operator (ESO)

Syncs secrets from 30+ providers to Kubernetes Secrets.

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      auth:
        kubernetes:
          role: "app-role"
```

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: secret/data/database/config
```

### Vault Secrets Operator (VSO)

Kubernetes-native Vault integration with automatic lease renewal.

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: postgres-creds
spec:
  vaultAuthRef: vault-auth
  mount: database
  path: creds/app-role
  renewalPercent: 67  # Renew at 67% of TTL
  destination:
    name: dynamic-db-creds
```

For ESO vs CSI vs VSO comparison, see `references/kubernetes-integration.md`.

## Secret Rotation Patterns

### Pattern 1: Versioned Static Secrets (Blue/Green)

1. Create new secret version in Vault
2. Update staging environment
3. Monitor for errors (24-48 hours)
4. Gradual production rollout (10% → 50% → 100%)
5. Revoke old secret (after 7 days)

### Pattern 2: Dynamic Database Credentials

Vault auto-generates credentials with short TTL:
- App fetches credentials from Vault
- Vault automatically renews lease (at 67% of TTL)
- On expiration, Vault revokes access
- On renewal failure, app requests new credentials

### Pattern 3: TLS Certificate Rotation

Using cert-manager + Vault PKI:
- cert-manager requests certificate from Vault
- Automatically renews before expiration (default: 67% of duration)
- Updates Kubernetes Secret on renewal
- Optional pod restart (via Reloader)

For detailed rotation workflows, see `references/rotation-patterns.md`.

## Multi-Language Integration

### Python (hvac)

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.kubernetes(role='app-role', jwt=jwt)

# Fetch dynamic credentials
response = client.secrets.database.generate_credentials(name='postgres-role')
username = response['data']['username']
password = response['data']['password']
```

### Go (Vault API)

```go
import vault "github.com/hashicorp/vault/api"

client, _ := vault.NewClient(vault.DefaultConfig())
k8sAuth, _ := auth.NewKubernetesAuth("app-role")
client.Auth().Login(context.Background(), k8sAuth)

secret, _ := client.Logical().Read("database/creds/postgres-role")
```

### TypeScript (node-vault)

```typescript
import vault from 'node-vault';

const client = vault({ endpoint: 'https://vault.example.com' });
await client.kubernetesLogin({ role: 'app-role', jwt });

const response = await client.read('database/creds/postgres-role');
```

For complete examples, see `examples/dynamic-db-credentials/`.

## Secret Scanning

### Pre-Commit Hooks (Gitleaks)

```bash
# Install Gitleaks
brew install gitleaks

# Run on staged files
gitleaks protect --staged --verbose
```

Pre-commit hook prevents secrets from being committed.
For setup, see `examples/secret-scanning/pre-commit`.

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
```

### Remediation Workflow

When a secret is leaked:
1. **Rotate immediately** (within 1 hour)
2. **Revoke at provider**
3. **Remove from Git history** (BFG Repo-Cleaner)
4. **Force push** (notify team)
5. **Audit access** (who had access during leak window)
6. **Document incident**

For detailed remediation, see `references/secret-scanning.md`.

## Zero-Knowledge Patterns

### Client-Side Encryption (E2EE)

User password → PBKDF2 → encryption key → encrypt secret → send to server

Server stores only encrypted blobs (cannot decrypt).

### Shamir's Secret Sharing

Split secret into N shares, require M to reconstruct (e.g., 3 of 5).

```bash
# Initialize Vault with Shamir shares
vault operator init -key-shares=5 -key-threshold=3

# Unseal requires 3 of 5 key shares
vault operator unseal <KEY_1>
vault operator unseal <KEY_2>
vault operator unseal <KEY_3>
```

For implementations, see `references/zero-knowledge.md`.

## Library Recommendations (2025)

### Secret Stores

| Library | Use Case | Trust Score |
|---------|----------|-------------|
| HashiCorp Vault | Enterprise, multi-cloud | High (73.3/100) |
| External Secrets Operator | Kubernetes integration | High (85.0/100) |
| AWS Secrets Manager | AWS workloads | High |
| GCP Secret Manager | GCP workloads | High |
| Azure Key Vault | Azure workloads | High |

### Secret Scanning

| Library | Use Case | Trust Score |
|---------|----------|-------------|
| Gitleaks | Pre-commit, CI/CD | High (89.9/100) |
| TruffleHog | Git history scanning | Medium |

### Client Libraries

| Language | Library | Version |
|----------|---------|---------|
| Python | `hvac` | 2.2.0+ |
| Go | `vault/api` | Latest |
| TypeScript | `node-vault` | 0.10.2+ |
| Rust | `vaultrs` | 0.7+ |

## Common Workflows

### Workflow 1: Vault + ESO on Kubernetes

1. Install Vault (Helm chart)
2. Initialize and unseal Vault
3. Enable Kubernetes auth
4. Install External Secrets Operator
5. Create SecretStore (Vault connection)
6. Create ExternalSecret (secret mapping)

For step-by-step guide, see `examples/vault-eso-setup/`.

### Workflow 2: Dynamic Database Credentials

1. Enable database secrets engine
2. Configure database connection
3. Create role with TTL
4. App fetches credentials
5. Vault auto-renews lease

For implementation, see `examples/dynamic-db-credentials/`.

### Workflow 3: Secret Scanning Remediation

1. Gitleaks detects secret
2. Block commit (pre-commit hook)
3. Developer removes secret
4. Developer stores in Vault
5. Developer references Vault path

For setup, see `examples/secret-scanning/`.

## Integration with Related Skills

- **auth-security**: OAuth client secrets, JWT signing keys
- **databases-***: Dynamic database credentials
- **deploying-applications**: Container registry credentials
- **observability**: Grafana/Datadog API keys
- **infrastructure-as-code**: Cloud provider credentials

## Security Best Practices

1. Never commit secrets to Git (use Gitleaks pre-commit hook)
2. Use dynamic secrets where possible
3. Rotate secrets regularly (quarterly for static, hourly for dynamic)
4. Implement least privilege (Vault policies, RBAC)
5. Enable audit logging
6. Encrypt at rest (Vault storage, etcd encryption)
7. Use short TTLs (< 24 hours for dynamic secrets)
8. Monitor failed access attempts

## Common Pitfalls

### Secrets in Environment Variables

Environment variables visible in process lists.
**Solution:** Use file-based secrets (Kubernetes volumes, CSI driver).

### Hardcoded Secrets in Manifests

Base64 is not encryption.
**Solution:** Use External Secrets Operator.

### No Secret Rotation

Stale credentials increase breach risk.
**Solution:** Use dynamic secrets or automate rotation.

### Root Token in Production

Unlimited permissions.
**Solution:** Use auth methods with least privilege policies.

## For Detailed Information, See

- `references/vault-architecture.md` - Vault internals, HA setup, policies
- `references/kubernetes-integration.md` - ESO, CSI driver, VSO comparison
- `references/rotation-patterns.md` - Detailed rotation workflows
- `references/secret-scanning.md` - Gitleaks, remediation procedures
- `references/zero-knowledge.md` - E2EE, Shamir's secret sharing
- `references/cloud-providers.md` - AWS, GCP, Azure secret managers
- `examples/vault-eso-setup/` - Complete Kubernetes setup
- `examples/dynamic-db-credentials/` - Multi-language examples
- `examples/secret-scanning/` - Pre-commit hooks, CI/CD
- `scripts/setup_vault.sh` - Automated Vault installation
