---
name: secrets
description: |
  Secret management patterns for the Kubernetes homelab platform.
  Covers secret-generator, ExternalSecret, app-secrets module, and cross-namespace replication.

  Use when: (1) Adding secrets for a new application, (2) Deciding between secret-generator
  and ExternalSecret, (3) Configuring cross-namespace secret replication, (4) Creating
  persistent secrets via the app-secrets Terragrunt module, (5) Debugging secret sync failures.

  Triggers: "secret", "ExternalSecret", "secret-generator", "aws ssm", "parameter store",
  "kubernetes-replicator", "replicate secret", "app-secrets", "persistent secret",
  "cross-namespace secret", "secret not syncing", "ClusterSecretStore"
user-invocable: false
---

# Secrets Management

Comprehensive guide to secret management in the homelab Kubernetes platform. Three mechanisms
exist for provisioning secrets, each serving a distinct purpose in the lifecycle of credentials.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Secrets Data Flow                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. secret-generator (in-cluster, ephemeral)                        │
│     Secret with annotation ──► controller generates random value    │
│     Lost on cluster rebuild, auto-regenerated                       │
│                                                                      │
│  2. ExternalSecret (from AWS SSM, persistent)                       │
│     ExternalSecret CR ──► ESO pulls from SSM ──► creates Secret     │
│     Survives cluster rebuilds (data lives in AWS)                   │
│                                                                      │
│  3. app-secrets module (Terragrunt + SSM, persistent)               │
│     Terragrunt generates random ──► stores in SSM ──► ExternalSecret│
│     Best of both: generated + persistent                            │
│                                                                      │
│  4. kubernetes-replicator (cross-namespace)                         │
│     Source Secret (annotated) ──► replica Secret in target namespace │
│     Keeps shared credentials in sync across namespaces              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree

```
App needs a secret?
│
├─ Can it be randomly generated? (password, API key, token)
│   │
│   ├─ Does it need to survive cluster rebuilds?
│   │   │
│   │   ├─ YES (e.g., encryption key seed, LDAP key)
│   │   │   └─ Use app-secrets Terragrunt module + ExternalSecret
│   │   │      (See: LLDAP pattern below)
│   │   │
│   │   └─ NO (e.g., session secret, internal API key)
│   │       └─ Use secret-generator annotation
│   │          (Simplest option, auto-regenerates)
│   │
│   └─ Is it a database credential?
│       └─ Use secret-generator with type: kubernetes.io/basic-auth
│          (See: Database Credentials section)
│
├─ Must match an external value? (OAuth, cloud API, webhook URL)
│   └─ Use ExternalSecret → AWS SSM
│      User must populate SSM parameter manually or via Terragrunt
│
├─ Shared across namespaces? (DB superuser, Dragonfly password)
│   └─ Use kubernetes-replicator annotations
│      Source secret in origin namespace → replicas in consumer namespaces
│
└─ Unclear?
    └─ AskUserQuestion: "Can this secret be randomly generated,
       or must it match a specific external value?"
```

---

## Mechanism 1: secret-generator (Ephemeral, In-Cluster)

The `mittwald/kubernetes-secret-generator` controller watches for annotated Secrets and
auto-populates them with random values. Preferred for secrets that do not need to persist
across cluster rebuilds.

### Basic Pattern

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secret
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: "password,api-key"
    secret-generator.v1.mittwald.de/encoding: hex
    secret-generator.v1.mittwald.de/length: "32"
data: {}
```

### Annotation Reference

| Annotation | Required | Values | Description |
|------------|----------|--------|-------------|
| `autogenerate` | Yes | Comma-separated key names | Keys to generate random values for |
| `encoding` | No | `hex`, `base64`, `base32`, `raw` | Encoding for generated values (default: `base64`) |
| `length` | No | Integer string (e.g., `"32"`) | Length of generated value (default: `"40"`) |

### Database Credentials Pattern

For applications using the shared CNPG cluster, create a `kubernetes.io/basic-auth` Secret
with a fixed username and auto-generated password:

```yaml
# kubernetes/clusters/live/config/<app>/db-credentials.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: <app>-db-credentials
  namespace: <app-namespace>
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: password
    secret-generator.v1.mittwald.de/encoding: hex
    secret-generator.v1.mittwald.de/length: "32"
type: kubernetes.io/basic-auth
stringData:
  username: <app>
```

**Real examples:**
- `kubernetes/clusters/live/config/authelia-prereqs/authelia-db-credentials.yaml`
- `kubernetes/clusters/live/config/authelia-prereqs/lldap-db-credentials.yaml`
- `kubernetes/clusters/live/config/zipline/zipline-db-credentials.yaml`

### Application Secret Pattern

For non-auth secrets (encryption keys, session tokens):

```yaml
# kubernetes/clusters/live/config/<app>/secret.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: <app>-secret
  namespace: <app-namespace>
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: CORE_SECRET
    secret-generator.v1.mittwald.de/length: "32"
    secret-generator.v1.mittwald.de/encoding: base64
data: {}
```

**Real example:** `kubernetes/clusters/live/config/zipline/secret.yaml`

### Platform-Level Secrets

Shared platform secrets that need cross-namespace replication combine both `secret-generator`
and `replicator` annotations:

```yaml
# kubernetes/platform/config/database/superuser-secret.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: cnpg-platform-superuser
  annotations:
    secret-generator.v1.mittwald.de/autogenerate: password
    secret-generator.v1.mittwald.de/length: "32"
    secret-generator.v1.mittwald.de/encoding: base64
    replicator.v1.mittwald.de/replication-allowed: "true"
    replicator.v1.mittwald.de/replication-allowed-namespaces: "zipline,authelia"
type: kubernetes.io/basic-auth
stringData:
  username: postgres
```

---

## Mechanism 2: ExternalSecret (Persistent, from AWS SSM)

Use External Secrets Operator (ESO) when secrets must come from outside the cluster or
persist across cluster rebuilds. ESO pulls values from AWS SSM Parameter Store via the
`aws-ssm` ClusterSecretStore.

### Infrastructure

The ClusterSecretStore is defined at:
`kubernetes/platform/config/secrets/cluster-secret-store.yaml`

```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: aws-ssm
spec:
  provider:
    aws:
      service: ParameterStore
      region: us-east-2
```

### SSM Path Convention

```
/homelab/kubernetes/${cluster_name}/<app-or-secret-name>
```

- **Cluster-specific:** `/homelab/kubernetes/live/cloudflare-api-token`
- **Shared across clusters:** `/homelab/kubernetes/shared/istio-mesh-ca`
- **App-secrets module:** `/homelab/kubernetes/live/lldap-secrets` (JSON with multiple keys)
- **Test:** `/homelab/kubernetes/test-secret`

### Basic ExternalSecret

```yaml
# yaml-language-server: $schema=https://kubernetes-schemas.pages.dev/external-secrets.io/externalsecret_v1.json
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: <app>-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-ssm
  target:
    name: <app>-credentials
  data:
    - secretKey: api-token
      remoteRef:
        key: /homelab/kubernetes/${cluster_name}/<app>/api-token
```

### Multi-Key JSON Pattern

When a single SSM parameter stores multiple keys as JSON (created by the `app-secrets` module),
extract individual properties:

```yaml
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: lldap-secrets
  namespace: authelia
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-ssm
  target:
    name: lldap-secrets
  data:
    - secretKey: LLDAP_KEY_SEED
      remoteRef:
        key: /homelab/kubernetes/live/lldap-secrets
        property: LLDAP_KEY_SEED
    - secretKey: LLDAP_JWT_SECRET
      remoteRef:
        key: /homelab/kubernetes/live/lldap-secrets
        property: LLDAP_JWT_SECRET
    - secretKey: LLDAP_LDAP_USER_PASS
      remoteRef:
        key: /homelab/kubernetes/live/lldap-secrets
        property: LLDAP_LDAP_USER_PASS
```

**Real example:** `kubernetes/clusters/live/config/authelia-prereqs/lldap-secrets.yaml`

### Templated ExternalSecret

For secrets that need transformation (e.g., generating a config file from credentials):

```yaml
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: hardware-monitoring-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-ssm
  target:
    name: hardware-monitoring-credentials
    template:
      engineVersion: v2
      data:
        ipmi-config.yml: |
          modules:
            default:
              user: "{{ .ipmiUsername }}"
              pass: "{{ .ipmiPassword }}"
  data:
    - secretKey: ipmiUsername
      remoteRef:
        key: /homelab/kubernetes/${cluster_name}/ipmi-username
    - secretKey: ipmiPassword
      remoteRef:
        key: /homelab/kubernetes/${cluster_name}/ipmi-password
```

**Real example:** `kubernetes/platform/config/monitoring/hardware-monitoring-secrets.yaml`

### ExternalSecret Placement

| Scope | Location | Example |
|-------|----------|---------|
| Platform-wide (all clusters) | `kubernetes/platform/config/<subsystem>/` | cloudflare-api-token, longhorn-s3-backup |
| Cluster-specific | `kubernetes/clusters/<cluster>/config/<app>/` | lldap-secrets |

---

## Mechanism 3: app-secrets Terragrunt Module (Generated + Persistent)

For secrets that must be randomly generated AND survive cluster rebuilds. The `app-secrets`
module generates random values with OpenTofu and stores them as a JSON SecureString in AWS SSM.

### Module Location

`infrastructure/modules/app-secrets/`

### How It Works

1. **Terragrunt unit** defines the secret names and generation parameters
2. **OpenTofu** generates random passwords and stores as JSON in SSM
3. **Local backup** is written for disaster recovery
4. **ExternalSecret** in Kubernetes pulls individual keys from the JSON parameter

### Step 1: Create a Terragrunt Unit

```hcl
# infrastructure/units/<app>-secrets/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../.././/modules/app-secrets"
}

inputs = {
  name = "<app>"

  secrets = {
    SECRET_KEY_1 = { length = 32, special = false }
    SECRET_KEY_2 = { length = 32, special = false }
  }

  ssm_parameter_path = "/homelab/kubernetes/live/<app>-secrets"

  local_backup_path = pathexpand("~/.secrets/homelab/<app>-secrets.json")
}
```

**Real example:** `infrastructure/units/lldap-secrets/terragrunt.hcl`

### Step 2: Add Unit to Stack

Add the unit to the relevant stack in `infrastructure/stacks/<stack>/terragrunt.stack.hcl`:

```hcl
unit "<app>_secrets" { source = "../../units/<app>-secrets" }
```

### Step 3: Apply and Create ExternalSecret

```bash
task tg:apply-<stack>  # Apply with human approval
```

Then create the ExternalSecret in Kubernetes using the multi-key JSON pattern (see above).

### Module Behavior

- `lifecycle.prevent_destroy = true` protects the SSM parameter from accidental deletion
- `lifecycle.ignore_changes = [value]` prevents re-generating secrets on subsequent applies
- Local backup at `~/.secrets/homelab/<app>-secrets.json` for disaster recovery

---

## Mechanism 4: kubernetes-replicator (Cross-Namespace)

The `mittwald/kubernetes-replicator` copies Secrets from one namespace to another.
Used when a shared resource (database, cache) generates a secret that consumer namespaces need.

### Source Secret Annotations

Add to the **source** Secret (in the originating namespace):

```yaml
annotations:
  replicator.v1.mittwald.de/replication-allowed: "true"
  replicator.v1.mittwald.de/replication-allowed-namespaces: "app1,app2"
```

### Replica Secret

Create an empty Secret in the **target** namespace that references the source:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: <source-secret-name>
  namespace: <target-namespace>
  annotations:
    replicator.v1.mittwald.de/replicate-from: <source-namespace>/<source-secret-name>
data: {}
```

### Common Replication Patterns

| Source | Source Namespace | Consumers | Purpose |
|--------|-----------------|-----------|---------|
| `cnpg-platform-superuser` | `database` | zipline, authelia | Shared DB superuser |
| `dragonfly-password` | `database` | immich, authelia | Shared cache password |
| `immich-database-app` | `database` | immich | Dedicated DB app credentials |
| `heartbeat-ping-url` | `kube-system` | monitoring | Health check URL |

### Adding a New Replication

1. **Source side** - add/update replication annotations:
   ```yaml
   replicator.v1.mittwald.de/replication-allowed: "true"
   replicator.v1.mittwald.de/replication-allowed-namespaces: "existing-ns,new-ns"
   ```

2. **Consumer side** - create replica Secret:
   ```yaml
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: <source-secret-name>
     namespace: <consumer-namespace>
     annotations:
       replicator.v1.mittwald.de/replicate-from: <source-ns>/<source-secret-name>
   data: {}
   ```

3. Add both files to their respective `kustomization.yaml`

---

## Three-Tier Secret Pattern (Exemplar: Authelia)

The `kubernetes/clusters/live/config/authelia-prereqs/` directory demonstrates the complete
secret pattern for an application that needs all three types:

| File | Mechanism | Purpose |
|------|-----------|---------|
| `lldap-secrets.yaml` | ExternalSecret (from app-secrets module) | Persistent LLDAP encryption keys |
| `authelia-db-credentials.yaml` | secret-generator | Ephemeral DB password |
| `lldap-db-credentials.yaml` | secret-generator | Ephemeral DB password |
| `cnpg-superuser-replica.yaml` | kubernetes-replicator | Replicated from database namespace |
| `dragonfly-secret-replication.yaml` | kubernetes-replicator | Replicated from database namespace |

---

## Debugging

### ExternalSecret Not Syncing

```bash
# Check ExternalSecret status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get externalsecret -A

# Describe for detailed error
KUBECONFIG=~/.kube/<cluster>.yaml kubectl describe externalsecret <name> -n <namespace>

# Check ClusterSecretStore health
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get clustersecretstore aws-ssm

# Check ESO operator logs
KUBECONFIG=~/.kube/<cluster>.yaml kubectl logs -n kube-system -l app.kubernetes.io/name=external-secrets --tail=50
```

### Common Failure Causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `SecretSyncedError` | SSM parameter does not exist | Create parameter: `aws ssm put-parameter --name <path> --type SecureString --value <json>` |
| `SecretSyncedError` with property error | JSON key missing | Verify SSM parameter JSON has expected keys |
| `ClusterSecretStore not ready` | AWS credentials invalid | Check `external-secrets-access-key` in kube-system |
| Secret exists but empty | Replicator source not annotated | Add `replication-allowed` annotations to source |
| Stale secret value | refreshInterval too long | Default is `1h`; reduce if needed |

### Verify SSM Parameter Exists

```bash
aws ssm get-parameter --name "/homelab/kubernetes/<cluster>/<secret>" --with-decryption
```

### PrometheusRule Alerts

ExternalSecret health is monitored by alerts defined in:
`kubernetes/platform/config/monitoring/external-secrets-alerts.yaml`

| Alert | Condition | Severity |
|-------|-----------|----------|
| `ExternalSecretSyncFailure` | Sync errors increasing over 5m | critical |
| `ExternalSecretNotReady` | Not ready for 10m+ | warning |
| `ClusterSecretStoreUnhealthy` | Store not ready for 5m | critical |

---

## Cross-References

| Document | Relevance |
|----------|-----------|
| [kubernetes/platform/CLAUDE.md](../../../kubernetes/platform/CLAUDE.md) | Secrets management overview, SSM parameters for bootstrap |
| [kubernetes/platform/config/CLAUDE.md](../../../kubernetes/platform/config/CLAUDE.md) | Config subsystem organization |
| [deploy-app skill](../deploy-app/SKILL.md) | Secrets decision tree for new deployments |
| [cnpg-database skill](../cnpg-database/SKILL.md) | Database credential chain |
| [terragrunt skill](../terragrunt/SKILL.md) | Infrastructure operations for app-secrets module |
