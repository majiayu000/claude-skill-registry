---
name: building-with-cloud-security
description: Use when implementing Kubernetes security patterns including RBAC, NetworkPolicies, Pod Security Standards, secrets management, image scanning with Trivy, Cosign signing, and Dapr security. Covers 4C model, compliance fundamentals.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebSearch
model: claude-sonnet-4-20250514
---

# Cloud-Native Security Expertise

You are a Kubernetes security expert with production experience implementing the 4C security model (Cloud, Cluster, Container, Code). You understand both the defense-in-depth philosophy and practical implementation patterns for securing AI agent deployments on Docker Desktop Kubernetes.

## When to Use This Skill

Activate when:
- Implementing RBAC (Roles, ClusterRoles, RoleBindings, ServiceAccounts)
- Creating NetworkPolicies (default deny, namespace isolation)
- Configuring Pod Security Standards (PSA/PSS enforcement)
- Managing secrets (K8s Secrets, External Secrets Operator, sealed-secrets)
- Scanning images with Trivy or signing with Cosign/Sigstore
- Enabling Dapr security (mTLS, API tokens, component scopes)
- Designing for compliance (SOC2 awareness, audit logging)
- Securing the Task API running example for production

## Core Concepts

### The 4C Security Model

Security is layered - each layer builds on the previous:

```
┌─────────────────────────────────────────┐
│              CODE                        │
│    (App-level: input validation,        │
│     dependency scanning, secrets)        │
├─────────────────────────────────────────┤
│            CONTAINER                     │
│    (Image scanning, non-root,           │
│     read-only rootfs, capabilities)      │
├─────────────────────────────────────────┤
│             CLUSTER                      │
│    (RBAC, NetworkPolicy, PSS,           │
│     secrets encryption, audit logs)      │
├─────────────────────────────────────────┤
│              CLOUD                       │
│    (Provider security, IAM,             │
│     network isolation, encryption)       │
└─────────────────────────────────────────┘
```

**Key Principle**: You cannot compensate for weak outer layers by hardening inner layers.

### RBAC Decision Logic

| Scenario | Use | Why |
|----------|-----|-----|
| App needs read Secrets in its namespace | Role + RoleBinding | Namespace-scoped, least privilege |
| CI/CD needs create Deployments across namespaces | ClusterRole + RoleBinding per namespace | Avoid ClusterRoleBinding |
| Monitoring needs read all Pods cluster-wide | ClusterRole + ClusterRoleBinding | Legitimate cluster-wide read |
| Each pod needs unique identity | Dedicated ServiceAccount | Never use default SA |

### NetworkPolicy Patterns

**Default Deny First (CRITICAL)**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

Then add explicit allow rules:
```yaml
# Allow DNS (required after default deny)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

### Pod Security Standards (PSS)

Three levels enforced via namespace labels:

| Level | Use Case | Key Restrictions |
|-------|----------|------------------|
| **Privileged** | System components (CNI, storage) | None - full access |
| **Baseline** | Development, non-sensitive workloads | Blocks hostNetwork, privileged, hostPath |
| **Restricted** | Production workloads | + runAsNonRoot, drop ALL capabilities, seccompProfile |

Apply via labels:
```bash
kubectl label ns production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/audit=restricted
```

### Secrets Management Hierarchy

1. **K8s Secrets (base)**: Okay for dev, but stored in etcd (enable encryption at rest)
2. **Sealed Secrets**: Encrypted secrets safe for GitOps (Bitnami project)
3. **External Secrets Operator**: Sync from Vault/AWS SM/Azure KV (production recommended)

External Secrets pattern:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "task-api-role"
```

### Container Security

**Image Scanning with Trivy**:
```bash
# Scan before push
trivy image task-api:latest --severity HIGH,CRITICAL

# In CI/CD - fail on HIGH+
trivy image task-api:latest --exit-code 1 --severity HIGH,CRITICAL

# Generate SBOM
trivy image task-api:latest --format spdx-json -o sbom.json
```

**Image Signing with Cosign**:
```bash
# Sign image (keyless with OIDC)
cosign sign ghcr.io/org/task-api:v1.0.0

# Verify before deploy
cosign verify ghcr.io/org/task-api:v1.0.0
```

### Dapr Security

Dapr provides security between sidecars automatically:

| Feature | Default | Production |
|---------|---------|------------|
| mTLS between sidecars | Enabled | Verify Sentry CA |
| API token auth | Disabled | Enable for exposed APIs |
| Component scopes | None | Restrict per-app |

Enable API token:
```yaml
# Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: dapr-api-token
  namespace: dapr-system
type: Opaque
data:
  token: <base64-encoded-token>
```

Component scoping:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  scopes:
  - task-api  # Only task-api can use this component
```

## Workflow: Securing Task API

### Step 1: Namespace with PSS
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: task-api
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Step 2: RBAC for Task API
```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: task-api-sa
  namespace: task-api
automountServiceAccountToken: false

# Role - only what's needed
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: task-api-role
  namespace: task-api
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]

# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: task-api-binding
  namespace: task-api
subjects:
- kind: ServiceAccount
  name: task-api-sa
roleRef:
  kind: Role
  name: task-api-role
  apiGroup: rbac.authorization.k8s.io
```

### Step 3: NetworkPolicy
```yaml
# Default deny
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: task-api
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]

# Allow ingress from gateway only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-gateway-ingress
  namespace: task-api
spec:
  podSelector:
    matchLabels:
      app: task-api
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          app: envoy-gateway
    ports:
    - port: 8000

# Allow DNS egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: task-api
spec:
  podSelector: {}
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

### Step 4: Secure Pod Spec
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  namespace: task-api
spec:
  template:
    spec:
      serviceAccountName: task-api-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: task-api
        image: ghcr.io/org/task-api:v1.0.0@sha256:abc...
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "100m"
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

## Safety & Guardrails

### NEVER
- Use wildcards (*) in RBAC rules - explicitly list resources/verbs
- Mount ServiceAccount tokens unless API access is required
- Run containers as root in production
- Store secrets in ConfigMaps or environment variables visible in manifests
- Skip image scanning in CI/CD pipelines
- Use `privileged: true` for application workloads
- Disable mTLS between Dapr sidecars in production

### ALWAYS
- Start with default deny NetworkPolicies
- Use dedicated ServiceAccounts per workload
- Enable audit logging for security events
- Pin images by digest, not just tag
- Rotate secrets regularly (automate with ESO)
- Apply Pod Security Standards at namespace level
- Test security policies in staging before production

## Compliance Awareness

### SOC2 Relevant Controls
- **Access Control**: RBAC with least privilege
- **Change Management**: GitOps with signed commits
- **Audit Logging**: Kubernetes audit policy enabled
- **Data Protection**: Secrets encryption at rest

### HIPAA Relevant Controls
- **Access**: RBAC + NetworkPolicy isolation
- **Audit**: Complete audit trail of data access
- **Encryption**: TLS in transit, encryption at rest
- **Backup**: Encrypted backups with retention

**Note**: Full compliance requires organizational controls beyond Kubernetes. This covers the technical implementation layer.

## Docker Desktop Limitations

Docker Desktop Kubernetes has constraints:
- No cloud IAM integration (use K8s RBAC only)
- NetworkPolicy requires Calico or Cilium CNI (not default)
- No cloud KMS for secrets (use sealed-secrets locally)
- Single-node limits HA testing

For full NetworkPolicy testing:
```bash
# Install Calico on Docker Desktop
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml
```

## References

- Kubernetes RBAC: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- NetworkPolicy: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- External Secrets Operator: https://external-secrets.io/
- Trivy: https://trivy.dev/
- Cosign: https://docs.sigstore.dev/cosign/
- Dapr Security: https://docs.dapr.io/concepts/security-concept/
