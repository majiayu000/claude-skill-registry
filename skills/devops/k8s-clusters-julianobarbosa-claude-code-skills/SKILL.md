---
name: k8s-clusters
description: Hypera Azure AKS infrastructure reference. Use when user mentions cluster
  names (cafehyna, loyalty, sonora, painelclientes), needs kubeconfig paths, asks
  about spot tolerations, cert-manager issuers,
---

---
name: k8s-clusters
description: Hypera Azure AKS infrastructure reference. Use when user mentions cluster names (cafehyna, loyalty, sonora, painelclientes), needs kubeconfig paths, asks about spot tolerations, cert-manager issuers, or resource definition policies. Critical: Hub cluster Azure name differs from developer name.
---

# Kubernetes Clusters Skill

## Critical: Hub Cluster Naming

| Context | Name |
|---------|------|
| Developer/Docs | `cafehyna-hub` |
| Azure CLI | `aks-cafehyna-default` |

Always use Azure name in `az` commands.

## Cluster Lookup

Format: `developer-name` → Azure: `azure-name`, RG: `resource-group`, Config: `kubeconfig`

**Cafehyna**

- `cafehyna-dev` → Azure: `aks-cafehyna-dev-hlg`, RG: `RS_Hypera_Cafehyna_Dev`, Config: `aks-rg-hypera-cafehyna-dev-config`, Spot: Yes
- `cafehyna-hub` → Azure: `aks-cafehyna-default`, RG: `rs_hypera_cafehyna`, Config: `aks-rg-hypera-cafehyna-hub-config`, Spot: No
- `cafehyna-prd` → Azure: `aks-cafehyna-prd`, RG: `rs_hypera_cafehyna_prd`, Config: `aks-rg-hypera-cafehyna-prd-config`, Spot: No

**Loyalty**

- `loyalty-dev` → Azure: `Loyalty_AKS-QAS`, RG: `RS_Hypera_Loyalty_AKS_QAS`, Config: `aks-rg-hypera-loyalty-dev-config`, Spot: Yes
- `loyalty-prd` → Azure: `Loyalty_AKS-PRD`, RG: `RS_Hypera_Loyalty_AKS_PRD`, Config: `aks-rg-hypera-loyalty-prd-config`, Spot: No

**Sonora**

- `sonora-dev` → Azure: `AKS-Hypera-Sonora-Dev-Hlg`, RG: `rg-hypera-sonora-dev`, Config: `aks-rg-hypera-sonora-dev-config`, Spot: Yes
- `sonora-prd` → Azure: `AKS-Hypera-Sonora-Prod`, RG: `rg-hypera-sonora-prd`, Config: `aks-rg-hypera-sonora-prd-config`, Spot: No

**Painelclientes**

- `painelclientes-dev` → Azure: `akspainelclientedev`, RG: `rg-hypera-painelclientes-dev`, Config: `aks-rg-hypera-painelclientes-dev-config`, Spot: Yes, Region: East US2
- `painelclientes-prd` → Azure: `akspainelclientesprd`, RG: `rg-hypera-painelclientes-prd`, Config: `aks-rg-hypera-painelclientes-prd-config`, Spot: No, Region: East US2

All kubeconfigs at `~/.kube/<config-name>`.

## Mandatory Policies

### 1. Spot Tolerations & Node Affinity (dev clusters only)

Required toleration for ALL pods on spot clusters:

```yaml
tolerations:
  - key: kubernetes.azure.com/scalesetpriority
    operator: Equal
    value: "spot"
    effect: NoSchedule
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: agentpool
              operator: In
              values: ["cafedevspot"]  # cafehyna-dev: only use cafedevspot, NOT cafedev
```

**Important**: The `cafedev` nodepool has `CriticalAddonsOnly` taint and should NOT be used for workloads. Always use the spot nodepool (e.g., `cafedevspot`, `pcdevspot`).

Without this → pods stuck `Pending`. Use `scripts/patch-tolerations.sh` to fix.

### 2. Resource Definitions (all clusters)

| Resource | Requirement |
|----------|-------------|
| CPU requests | ✅ Required |
| CPU limits | ❌ Forbidden (causes throttling) |
| Memory requests | ✅ Required |
| Memory limits | ✅ Required, must equal requests |

### 3. cert-manager ClusterIssuers

| Environment | Issuer |
|-------------|--------|
| prd, hub | `letsencrypt-prod-cloudflare` |
| dev | `letsencrypt-staging-cloudflare` |

❌ Never use issuers without `-cloudflare` suffix.

### 4. Storage Class Policy (CRITICAL - ALL WORKLOADS)

**MANDATORY for ALL stateful workloads across ALL clusters:**

| Access Mode | StorageClass | Use Case |
|-------------|--------------|----------|
| ReadWriteOnce (RWO) | `managed-premium-zrs` | Databases, caches, single-pod storage |
| ReadWriteMany (RWX) | `azurefile-csi-premium` | Shared storage, media files, multi-pod access |

**Rules:**

| Rule | Requirement |
|------|-------------|
| Helm values `storageClass` | ✅ MUST be explicitly set (never omit or use null) |
| `storageClass: null` or omitted | ❌ FORBIDDEN - causes zone affinity conflicts |
| Default StorageClass reliance | ❌ FORBIDDEN - not guaranteed across clusters |

**Why Zone-Redundant Storage (ZRS)?**

- **High Availability**: Synchronous replication across 3 availability zones
- **Zero RPO**: No data loss during zone failures
- **12 nines durability**: 99.9999999999% data durability
- **No zone conflicts**: Prevents "volume node affinity conflict" errors
- **Proper binding**: Works with `WaitForFirstConsumer` binding mode

**This applies to ALL workloads including:**

- Observability: Loki, Tempo, Mimir, Prometheus, Grafana
- Security: DefectDojo, SonarQube, Vault
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Message Queues: RabbitMQ, Kafka
- Any Helm chart with persistence enabled
- Any StatefulSet, any PersistentVolumeClaim

**Creating managed-premium-zrs StorageClass**

Run on each cluster that doesn't have it:

```bash
# Quick check and create
.claude/skills/k8s-clusters/scripts/create-storageclass.sh <cluster-name>

# Or manually:
KUBECONFIG=~/.kube/<config> kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium-zrs
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_ZRS
  kind: Managed
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF
```

**Example Helm values pattern:**

```yaml
# For databases, caches (RWO)
persistence:
  storageClass: managed-premium-zrs  # NEVER omit this

# For shared/media storage (RWX)
persistence:
  storageClass: azurefile-csi-premium
  accessMode: ReadWriteMany
```

### 5. Robusta CSI Secret Store Pattern (ALL clusters)

**MANDATORY for ALL Robusta deployments:**

Robusta requires secrets from Azure Key Vault. The CSI Secret Store driver syncs these secrets to Kubernetes Secrets that the Robusta runner pod references.

**Required Azure Key Vault Secrets** (must exist in each cluster's Key Vault):

| Secret Name | Description | Required By |
|-------------|-------------|-------------|
| `robusta-ms-teams-webhook` | MS Teams incoming webhook URL | MS Teams sink |
| `robusta-ui-token` | Robusta SaaS UI authentication token | Robusta UI sink |
| `robusta-signing-key` | Signing key for Robusta authentication | globalConfig |
| `robusta-account-id` | Robusta account identifier | globalConfig |
| `azure-openai-key` | Azure OpenAI API key | HolmesGPT |

**Create missing secrets** (if any are missing, pod will fail with `FailedMount`):

```bash
# Check existing secrets in Key Vault
az keyvault secret list --vault-name <keyvault-name> --query "[?starts_with(name,'robusta') || starts_with(name,'azure-openai')].name" -o tsv

# Create missing secrets (get values from Hub KV or Robusta SaaS)
az keyvault secret set --vault-name <keyvault-name> --name robusta-ms-teams-webhook --value "<webhook-url>"
az keyvault secret set --vault-name <keyvault-name> --name robusta-ui-token --value "<ui-token>"
az keyvault secret set --vault-name <keyvault-name> --name robusta-signing-key --value "<signing-key>"
az keyvault secret set --vault-name <keyvault-name> --name robusta-account-id --value "<account-id>"
az keyvault secret set --vault-name <keyvault-name> --name azure-openai-key --value "<openai-key>"
```

**Required SecretProviderClass** (`secretproviderclass.yaml` in each cluster's robusta directory):

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: robusta-secrets-kv
  namespace: monitoring
spec:
  provider: azure
  secretObjects:
    - data:
        - key: ms-teams-webhook
          objectName: robusta-ms-teams-webhook
        - key: robusta-ui-token
          objectName: robusta-ui-token
        - key: azure-openai-key
          objectName: azure-openai-key
        - key: robusta-signing-key
          objectName: robusta-signing-key
        - key: robusta-account-id
          objectName: robusta-account-id
      secretName: robusta-secrets
      type: Opaque
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "<cluster-managed-identity>"  # From cluster lookup
    keyvaultName: "<cluster-keyvault>"                     # From cluster lookup
    tenantId: "3f7a3df4-f85b-4ca8-98d0-08b1034e6567"
    objects: |
      array:
        - |
          objectName: robusta-ms-teams-webhook
          objectType: secret
        - |
          objectName: robusta-ui-token
          objectType: secret
        - |
          objectName: azure-openai-key
          objectType: secret
        - |
          objectName: robusta-signing-key
          objectType: secret
        - |
          objectName: robusta-account-id
          objectType: secret
```

**Required Helm values** (in `values.yaml` under `runner:` section):

```yaml
runner:
  # CSI volume mount to trigger robusta-secrets creation from Azure Key Vault
  extraVolumes:
    - name: robusta-secrets-store
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: robusta-secrets-kv
  extraVolumeMounts:
    - name: robusta-secrets-store
      mountPath: /mnt/secrets-store/robusta
      readOnly: true
```

**How it works:**

1. CSI driver mounts the SecretProviderClass volume to the runner pod
2. On mount, driver fetches secrets from Azure Key Vault using Managed Identity
3. Driver creates Kubernetes Secret `robusta-secrets` in monitoring namespace
4. Runner pod references this secret for environment variables

**Common issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| `FailedMount` with `SecretNotFound` | Secret missing in Key Vault | Create the missing secret with `az keyvault secret set` |
| Pod stuck `ContainerCreating` | SecretProviderClass name mismatch | Ensure `secretProviderClass: robusta-secrets-kv` matches metadata.name |
| Secret not created | Missing extraVolumes/extraVolumeMounts | Add CSI volume configuration to values.yaml |
| Auth error in pod events | Wrong Managed Identity ID | Check `userAssignedIdentityID` matches cluster's identity |

### 6. HolmesGPT Azure OpenAI Configuration

**Reference**: [HolmesGPT Azure OpenAI Docs](https://holmesgpt.dev/ai-providers/azure-openai/)

HolmesGPT uses the LiteLLM API to support Azure OpenAI. Configuration is done via Helm values.

**Required environment variables** (in `values.yaml` under `holmes:` section):

```yaml
enableHolmesGPT: true
holmes:
  additionalEnvVars:
    - name: ROBUSTA_AI
      value: "true"
    - name: AZURE_API_KEY
      valueFrom:
        secretKeyRef:
          name: robusta-secrets
          key: azure-openai-key
    - name: MODEL
      value: "azure/<deployment-name>"  # e.g., azure/gpt-4o or azure/claude-sonnet-4-5
    - name: AZURE_API_VERSION
      value: "2024-12-01-preview"  # Use latest stable version
    - name: AZURE_API_BASE
      value: "https://<resource>.openai.azure.com/"  # Or AI Foundry endpoint
```

**Advanced: Multiple models with modelList** (2025 approach):

```yaml
holmes:
  additionalEnvVars:
    - name: AZURE_API_KEY
      valueFrom:
        secretKeyRef:
          name: robusta-secrets
          key: azure-openai-key
  modelList:
    azure-gpt-4o:
      api_key: "{{ env.AZURE_API_KEY }}"
      model: azure/gpt-4o
      api_base: https://your-resource.openai.azure.com/
      api_version: "2024-12-01-preview"
      temperature: 0
  config:
    model: "azure-gpt-4o"  # References key name in modelList
```

**Important notes:**

- Increase token limit in Azure Portal to at least 450K for your deployment
- The `MODEL` value uses format `azure/<deployment-name>` (keep the `azure/` prefix)
- For AI Foundry projects, use the full project endpoint as `AZURE_API_BASE`

## Quick Troubleshooting

| Symptom | Fix |
|---------|-----|
| Pod Pending on dev | Add spot toleration + nodeAffinity to `cafedevspot` |
| Volume node affinity conflict | Set explicit `storageClass: managed-premium-zrs`, delete stuck PVC |
| PVC stuck Pending | 1) Check StorageClass exists 2) Run `create-storageclass.sh` 3) Delete and recreate PVC |
| StorageClass not found | Run `scripts/create-storageclass.sh <cluster>` |
| Certificate stuck | Change to `*-cloudflare` issuer |
| Connection timeout | Check VPN, run `scripts/diagnose.sh` |
| Auth failed | `az login` then re-get credentials |
| ArgoCD sync error: `podReplacementPolicy: field not declared in schema` | See ArgoCD SSA troubleshooting below |
| Robusta pod stuck ContainerCreating | Check SecretProviderClass name matches `robusta-secrets-kv`, add CSI volumes |

## ArgoCD Server-Side Apply (SSA) Troubleshooting

### Issue: `podReplacementPolicy` / `status.terminating` Schema Error

**Error message:**

```
ComparisonError: error calculating structured merge diff: error building typed value from live resource:
errors: .spec.podReplacementPolicy: field not declared in schema .status.terminating: field not declared in schema
```

**Root Cause:** ArgoCD issue [#18778](https://github.com/argoproj/argo-cd/issues/18778). Kubernetes 1.29+ Job resources have new fields (`podReplacementPolicy`, `status.terminating`) that ArgoCD's embedded schema doesn't recognize when using Server-Side Diff.

**Important:** `ignoreDifferences` does NOT work for this issue because the error occurs during schema validation before diff comparison.

**Solution:** Disable Server-Side Diff at the Application level:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application  # or ApplicationSet template
metadata:
  annotations:
    # Workaround for ArgoCD issue #18778
    argocd.argoproj.io/compare-options: ServerSideDiff=false
```

**For ApplicationSets:**

```yaml
spec:
  template:
    metadata:
      annotations:
        argocd.argoproj.io/compare-options: ServerSideDiff=false
```

**Affected resources:** Any application deploying Jobs, CronJobs, or Helm charts that create Jobs (e.g., DefectDojo initializer, database migrations).

**References:**

- [ArgoCD Issue #18778](https://github.com/argoproj/argo-cd/issues/18778)
- [ArgoCD Diff Strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/diff-strategies/)

## Quick Commands

### Get Cluster Credentials

```bash
# cafehyna clusters (hypera-pharma subscription)
az aks get-credentials --resource-group RS_Hypera_Cafehyna_Dev --name aks-cafehyna-dev-hlg --file ~/.kube/aks-rg-hypera-cafehyna-dev-config --overwrite-existing
az aks get-credentials --resource-group rs_hypera_cafehyna --name aks-cafehyna-default --file ~/.kube/aks-rg-hypera-cafehyna-hub-config --overwrite-existing
az aks get-credentials --resource-group rs_hypera_cafehyna_prd --name aks-cafehyna-prd --file ~/.kube/aks-rg-hypera-cafehyna-prd-config --overwrite-existing

# painelclientes (requires subscription switch)
az account set --subscription "56bb103c-1075-4536-b6fc-abf6df80b15c"  # operation-dev
az aks get-credentials --resource-group rg-hypera-painelclientes-dev --name akspainelclientedev --file ~/.kube/aks-rg-hypera-painelclientes-dev-config --overwrite-existing

az account set --subscription "1e705d23-900f-471e-b18d-7e0eb94d8c7a"  # operation
az aks get-credentials --resource-group rg-hypera-painelclientes-prd --name akspainelclientesprd --file ~/.kube/aks-rg-hypera-painelclientes-prd-config --overwrite-existing
```

### Create StorageClass (if missing)

```bash
KUBECONFIG=~/.kube/<config> kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium-zrs
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_ZRS
  kind: Managed
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF
```

### Diagnose Connection

```bash
# Check Azure login
az account show

# Test DNS resolution (for private clusters)
nslookup <api-server-fqdn>

# Test connectivity
nc -zv <api-server-fqdn> 443

# Check RBAC
kubectl --kubeconfig ~/.kube/<config> auth can-i --list
```

## Detailed Reference

For API endpoints, Key Vaults, nodepool details, and extended troubleshooting:

- **[references/clusters-detail.md](references/clusters-detail.md)** - Extended cluster info, resource templates

### Related Documentation

- **[docs/clusters/](../../../docs/clusters/)** - Detailed per-cluster documentation
- **[docs/operations/access-authentication.md](../../../docs/operations/access-authentication.md)** - Full access guide
- **[docs/operations/troubleshooting.md](../../../docs/operations/troubleshooting.md)** - Troubleshooting guide
- **[docs/storage/managed-premium-zrs.md](../../../docs/storage/managed-premium-zrs.md)** - Storage class details
