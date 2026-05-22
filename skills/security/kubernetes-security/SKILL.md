---
name: kubernetes-security
description: |
  Kubernetes and OpenShift security assessment, hardening, and compliance. Use this skill when:
  (1) Auditing cluster or workload security posture
  (2) Implementing Pod Security Standards/Admission
  (3) Configuring RBAC roles and permissions
  (4) Setting up NetworkPolicies for zero-trust
  (5) Managing Secrets securely (encryption, external secrets)
  (6) Scanning images for vulnerabilities
  (7) Implementing OCP SecurityContextConstraints
  (8) Compliance checking (CIS benchmarks, SOC2, PCI-DSS)
  (9) Security incident investigation
  (10) Hardening cluster components
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes / OpenShift Security Guide

Comprehensive security assessment, hardening, and compliance for production clusters.

## Current Security Tools (January 2026)

| Tool | Version | Purpose | Documentation |
|------|---------|---------|---------------|
| **Trivy** | 0.58.x | Vulnerability scanning | https://aquasecurity.github.io/trivy/ |
| **Kyverno** | 1.13.x | Policy engine | https://kyverno.io/ |
| **OPA Gatekeeper** | 3.18.x | Policy engine | https://open-policy-agent.github.io/gatekeeper/ |
| **Falco** | 0.39.x | Runtime security | https://falco.org/ |
| **kube-bench** | 0.8.x | CIS benchmarks | https://github.com/aquasecurity/kube-bench |
| **kubescape** | 3.0.x | Security posture | https://kubescape.io/ |
| **External Secrets** | 0.12.x | Secret management | https://external-secrets.io/ |
| **Sealed Secrets** | 0.27.x | GitOps secrets | https://sealed-secrets.netlify.app/ |

### Tool Installation

```bash
# Trivy
brew install trivy

# Kyverno CLI
brew install kyverno

# kubescape
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# kube-bench (as a Job)
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
```

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command. When working with:
- **OpenShift/ARO clusters**: Replace `kubectl` with `oc`
- **Standard Kubernetes (AKS, EKS, GKE)**: Use `kubectl` as shown

## Security Assessment Workflow

1. **Inventory**: Identify workloads, namespaces, service accounts
2. **Audit**: Run security scans, check configurations
3. **Classify**: Risk level based on exposure and sensitivity
4. **Remediate**: Apply hardening based on priority
5. **Monitor**: Continuous compliance verification

## Pod Security Standards (PSS) - Kubernetes 1.31

### Security Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `privileged` | Unrestricted policy | System workloads only |
| `baseline` | Minimally restrictive | Standard workloads |
| `restricted` | Heavily restricted | Security-sensitive workloads |

### Enforcement Modes

| Mode | Behavior |
|------|----------|
| `enforce` | Reject violating pods |
| `audit` | Log violations, allow pods |
| `warn` | Warn user, allow pods |

### Namespace Configuration

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    # Enforce restricted standard
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Audit for baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/audit-version: latest
    # Warn for restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

### Restricted Profile Requirements

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        # Recommended:
        readOnlyRootFilesystem: true
        runAsNonRoot: true
```

## RBAC Best Practices

### Principle of Least Privilege

```yaml
# BAD: Overly permissive
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]

# GOOD: Specific permissions
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
    resourceNames: ["app-config"]  # Even more specific
```

### Role vs ClusterRole

| Type | Scope | Use When |
|------|-------|----------|
| `Role` | Namespace | App-specific permissions |
| `ClusterRole` | Cluster-wide | Cross-namespace or cluster resources |

### Common RBAC Patterns

#### Read-Only Application Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
  namespace: ${NAMESPACE}
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]
```

#### CI/CD Deployment Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployer
  namespace: ${NAMESPACE}
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["configmaps", "secrets", "services"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
```

#### Monitoring Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-reader
rules:
  - apiGroups: [""]
    resources: ["pods", "nodes", "services", "endpoints"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]
  - apiGroups: ["metrics.k8s.io"]
    resources: ["pods", "nodes"]
    verbs: ["get", "list"]
```

### RBAC Audit Commands

```bash
# Check what a service account can do
kubectl auth can-i --list --as=system:serviceaccount:${NS}:${SA}

# Check specific permission
kubectl auth can-i create deployments --as=system:serviceaccount:${NS}:${SA}

# Find overly permissive roles
kubectl get clusterroles -o json | jq -r \
  '.items[] | select(.rules[].verbs | contains(["*"])) | .metadata.name'
```

## NetworkPolicy Zero-Trust

### Default Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Allow DNS Egress (Required)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
        - podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

### Allow Ingress from Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-controller
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
```

### Allow Inter-Service Communication

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: frontend
      ports:
        - protocol: TCP
          port: 8080
```

## Secrets Management

### External Secrets Operator (v0.12.x)

```bash
# Install
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  --set installCRDs=true
```

```yaml
# ClusterSecretStore for Vault
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "external-secrets"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: ${NAMESPACE}
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: apps/${APP_NAME}
        property: database_url
```

### Sealed Secrets (GitOps-friendly, v0.27.x)

```bash
# Install
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system

# Install CLI
brew install kubeseal

# Create sealed secret
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

# Apply (controller decrypts it)
kubectl apply -f sealed-secret.yaml
```

## OpenShift Security Context Constraints

### SCC Hierarchy (Most to Least Restrictive)

1. `restricted-v2` - Default, most restrictive
2. `nonroot-v2` - Must run as non-root
3. `hostnetwork-v2` - Allow host network
4. `anyuid` - Run as any UID
5. `privileged` - Full privileges (avoid!)

### Check SCC Assignment

```bash
# See which SCC a pod is using
oc get pod ${POD} -n ${NS} -o yaml | grep scc

# List available SCCs
oc get scc

# Check SA SCC permissions
oc adm policy who-can use scc restricted-v2
```

### Grant SCC to Service Account

```bash
oc adm policy add-scc-to-user ${SCC} -z ${SERVICE_ACCOUNT} -n ${NAMESPACE}
```

```yaml
# Via RoleBinding (GitOps-friendly)
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${SA}-scc-${SCC}
  namespace: ${NAMESPACE}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:openshift:scc:${SCC}
subjects:
  - kind: ServiceAccount
    name: ${SERVICE_ACCOUNT}
    namespace: ${NAMESPACE}
```

## Image Security

### Trivy Scanning

```bash
# Scan image for vulnerabilities
trivy image ${IMAGE}:${TAG}

# Scan with severity filter
trivy image --severity HIGH,CRITICAL ${IMAGE}:${TAG}

# Scan and output JSON
trivy image -f json -o results.json ${IMAGE}:${TAG}

# Scan Kubernetes cluster
trivy k8s --report summary cluster
```

### Kyverno Policy Examples

```yaml
# Require non-root containers
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-run-as-nonroot
spec:
  validationFailureAction: enforce
  rules:
    - name: run-as-non-root
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Containers must run as non-root"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
---
# Block privileged containers
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged
spec:
  validationFailureAction: enforce
  rules:
    - name: deny-privileged
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Privileged containers are not allowed"
        pattern:
          spec:
            containers:
              - securityContext:
                  privileged: "!true"
```

## Security Audit Script

```bash
#!/bin/bash
echo "=== KUBERNETES SECURITY AUDIT ==="

# Check for privileged containers
echo "### Privileged Containers ###"
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.containers[].securityContext.privileged == true) |
   "\(.metadata.namespace)/\(.metadata.name)"'

# Check for root containers
echo -e "\n### Containers Running as Root ###"
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.containers[].securityContext.runAsUser == 0) |
   "\(.metadata.namespace)/\(.metadata.name)"'

# Check for host namespace access
echo -e "\n### Host Namespace Access ###"
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.hostNetwork == true or .spec.hostPID == true) |
   "\(.metadata.namespace)/\(.metadata.name)"'

# Check for default service accounts
echo -e "\n### Pods Using Default SA ###"
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.serviceAccountName == "default") |
   "\(.metadata.namespace)/\(.metadata.name)"'

# Check for overly permissive RBAC
echo -e "\n### Wildcard RBAC Roles ###"
kubectl get clusterroles -o json | jq -r \
  '.items[] | select(.rules[].verbs | contains(["*"])) | .metadata.name'

# Check namespaces without NetworkPolicy
echo -e "\n### Namespaces Without NetworkPolicy ###"
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
  [ "$count" -eq 0 ] && echo "$ns"
done
```

## CIS Benchmark Compliance

```bash
# Run kube-bench
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -f job/kube-bench

# Run kubescape
kubescape scan framework nsa --exclude-namespaces kube-system
kubescape scan framework cis-v1.23-t1.0.1
```
