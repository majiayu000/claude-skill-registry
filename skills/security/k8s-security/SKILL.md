---
name: k8s-security
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
---

# Kubernetes / OpenShift Security Guide

## Current Versions & Security Tools (January 2026)

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

### Security Tool Installation

```bash
# Trivy - Vulnerability scanner
brew install trivy
# OR
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Kyverno CLI
brew install kyverno

# kubescape - Comprehensive security scanner
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# kube-bench - CIS benchmarks
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
```

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command in all examples. When working with:
- **OpenShift/ARO clusters**: Replace all `kubectl` commands with `oc`
- **Standard Kubernetes clusters (AKS, EKS, GKE, etc.)**: Use `kubectl` as shown

The agent will automatically detect the cluster type and use the appropriate command.

Comprehensive security assessment, hardening, and compliance for cluster-code managed clusters.

## Security Assessment Workflow

1. **Inventory**: Identify workloads, namespaces, service accounts
2. **Audit**: Run security scans, check configurations
3. **Classify**: Risk level based on exposure and sensitivity
4. **Remediate**: Apply hardening based on priority
5. **Monitor**: Continuous compliance verification

## Pod Security Standards (PSS) - Kubernetes 1.31

**Documentation**: https://kubernetes.io/docs/concepts/security/pod-security-standards/

Pod Security Admission (PSA) is now the standard for pod security in Kubernetes 1.31+, having fully replaced the deprecated PodSecurityPolicy.

### Levels

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
    # Audit for baseline (catch less severe issues)
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/audit-version: latest
    # Warn for restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

### Restricted Profile Requirements

```yaml
# Pod spec must include ALL of these for restricted compliance:
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
        # Optional but recommended:
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
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services"]
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
# List all roles/clusterroles
kubectl get roles,clusterroles -A

# Check what a service account can do
kubectl auth can-i --list --as=system:serviceaccount:${NS}:${SA}

# Check specific permission
kubectl auth can-i create deployments --as=system:serviceaccount:${NS}:${SA} -n ${NS}

# Find all bindings for a subject
kubectl get rolebindings,clusterrolebindings -A -o json | \
  jq -r '.items[] | select(.subjects[]?.name=="${SA}") | .metadata.name'

# Identify overly permissive roles
kubectl get clusterroles -o json | jq -r \
  '.items[] | select(.rules[].verbs | contains(["*"])) | .metadata.name'
```

## NetworkPolicy Zero-Trust

### Default Deny All

```yaml
# Apply to every namespace for zero-trust baseline
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

### Allow Ingress from Ingress Controller

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

### Secret Encryption at Rest

```yaml
# /etc/kubernetes/encryption-config.yaml (on control plane)
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: ${BASE64_ENCODED_32_BYTE_KEY}
      - identity: {}
```

### External Secrets Operator

**Current Version: v0.12.x (January 2026)**

**Documentation**: https://external-secrets.io/

```bash
# Install External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  --set installCRDs=true \
  --set webhook.port=9443
```

```yaml
# ClusterSecretStore for HashiCorp Vault
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
          serviceAccountRef:
            name: "external-secrets"
            namespace: "external-secrets"
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
    - secretKey: API_KEY
      remoteRef:
        key: apps/${APP_NAME}
        property: api_key
```

### Sealed Secrets (GitOps-friendly)

**Current Version: v0.27.x (January 2026)**

**Documentation**: https://sealed-secrets.netlify.app/

```bash
# Install Sealed Secrets controller
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system \
  --set fullnameOverride=sealed-secrets-controller

# Install kubeseal CLI
brew install kubeseal
# OR
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.27.0/kubeseal-0.27.0-linux-amd64.tar.gz

# Create sealed secret from existing secret
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

# Create sealed secret with specific scope
kubeseal --format=yaml --scope cluster-wide < secret.yaml > sealed-secret.yaml
kubeseal --format=yaml --scope namespace-wide < secret.yaml > sealed-secret.yaml

# Apply sealed secret (controller decrypts it)
kubectl apply -f sealed-secret.yaml

# Rotate secrets (re-encrypt with new key)
kubeseal --recovery-unseal --recovery-private-key backup-key.pem < sealed-secret.yaml
```

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: ${NAMESPACE}
spec:
  encryptedData:
    DATABASE_URL: AgBy8hCi...  # Encrypted value
    API_KEY: AgA5mKpQ...       # Encrypted value
```

## OpenShift Security Context Constraints

### SCC Hierarchy (Most to Least Restrictive)

1. `restricted-v2` - Default, most restrictive
2. `restricted` - Legacy restricted
3. `nonroot-v2` - Must run as non-root
4. `nonroot` - Legacy non-root
5. `hostnetwork-v2` - Allow host network
6. `hostnetwork` - Legacy host network
7. `hostmount-anyuid` - Host mounts, any UID
8. `hostaccess` - Host access
9. `anyuid` - Run as any UID
10. `privileged` - Full privileges (avoid!)

### Check SCC Assignment

```bash
# See which SCC a pod is using
oc get pod ${POD} -n ${NS} -o yaml | grep scc

# List available SCCs
oc get scc

# Describe SCC requirements
oc describe scc restricted-v2

# Check SA SCC permissions
oc adm policy who-can use scc restricted-v2
```

### Grant SCC to Service Account

```bash
# Add SCC to SA (requires admin)
oc adm policy add-scc-to-user ${SCC} -z ${SERVICE_ACCOUNT} -n ${NAMESPACE}

# Via RoleBinding (preferred for GitOps)
```

```yaml
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

### Custom SCC Template

```yaml
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: custom-restricted
allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegeEscalation: false
allowPrivilegedContainer: false
allowedCapabilities: []
defaultAddCapabilities: []
fsGroup:
  type: MustRunAs
  ranges:
    - min: 1000
      max: 65534
priority: null
readOnlyRootFilesystem: true
requiredDropCapabilities:
  - ALL
runAsUser:
  type: MustRunAsRange
  uidRangeMin: 1000
  uidRangeMax: 65534
seLinuxContext:
  type: MustRunAs
seccompProfiles:
  - runtime/default
supplementalGroups:
  type: MustRunAs
  ranges:
    - min: 1000
      max: 65534
users: []
groups: []
volumes:
  - configMap
  - downwardAPI
  - emptyDir
  - persistentVolumeClaim
  - projected
  - secret
```

## Image Security

### Image Scanning Integration

**Trivy v0.58.x (January 2026)** - Industry-standard vulnerability scanner

```bash
# Basic vulnerability scan
trivy image ${IMAGE}:${TAG}

# Scan with severity filter
trivy image --severity HIGH,CRITICAL ${IMAGE}:${TAG}

# Scan for misconfigurations (Dockerfile, K8s manifests)
trivy config .
trivy fs --scanners misconfig .

# Output as JSON for CI/CD processing
trivy image -f json -o results.json ${IMAGE}:${TAG}

# Output as SARIF for GitHub Security
trivy image -f sarif -o trivy-results.sarif ${IMAGE}:${TAG}

# Scan with SBOM generation (Software Bill of Materials)
trivy image --format spdx-json -o sbom.json ${IMAGE}:${TAG}

# Scan Kubernetes cluster for vulnerabilities
trivy k8s --report summary cluster

# Scan specific namespace
trivy k8s -n ${NAMESPACE} --report all

# Generate compliance report
trivy k8s cluster --compliance k8s-cis-1.8
trivy k8s cluster --compliance k8s-nsa-1.0

# Use in CI/CD (fail on HIGH/CRITICAL)
trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE}:${TAG}
```

### Trivy Operator (Continuous Scanning in Cluster)

```bash
# Install Trivy Operator via Helm
helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm repo update

helm install trivy-operator aqua/trivy-operator \
  --namespace trivy-system \
  --create-namespace \
  --set trivy.ignoreUnfixed=true \
  --set operator.scanJobTimeout=10m

# View vulnerability reports
kubectl get vulnerabilityreports -A
kubectl get configauditreports -A
kubectl get exposedsecretreports -A

# Get summary
kubectl get vulnerabilityreports -A -o json | jq -r '
  .items[] | 
  "\(.metadata.namespace)/\(.metadata.name): Critical=\(.report.summary.criticalCount) High=\(.report.summary.highCount)"'
```

### Additional Scanning Tools

```bash
# kubescape - Comprehensive security posture
kubescape scan framework nsa --submit --account ${ACCOUNT_ID}
kubescape scan framework mitre
kubescape scan framework cis-v1.23-t1.0.1

# Grype (Anchore) - Alternative vulnerability scanner
grype ${IMAGE}:${TAG}
grype dir:/path/to/project

# Syft - SBOM generator
syft ${IMAGE}:${TAG} -o spdx-json > sbom.spdx.json
```

```yaml
# Trivy Operator - Automatic vulnerability scanning
apiVersion: aquasecurity.github.io/v1alpha1
kind: VulnerabilityReport
metadata:
  name: ${POD_NAME}-${CONTAINER_NAME}
  namespace: ${NAMESPACE}
spec:
  # Auto-generated by operator
```

```bash
# Manual scan with trivy
trivy image ${IMAGE}:${TAG}

# Scan with severity filter
trivy image --severity HIGH,CRITICAL ${IMAGE}:${TAG}

# Output as JSON for processing
trivy image -f json -o results.json ${IMAGE}:${TAG}
```

### Image Policy (OCP)

```yaml
apiVersion: config.openshift.io/v1
kind: Image
metadata:
  name: cluster
spec:
  registrySources:
    # Block all registries except allowed
    allowedRegistries:
      - quay.io
      - registry.redhat.io
      - image-registry.openshift-image-registry.svc:5000
    # Or block specific registries
    blockedRegistries:
      - docker.io
```

### Admission Controller for Image Verification

```yaml
# Kyverno policy example
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: enforce
  rules:
    - name: verify-signature
      match:
        resources:
          kinds:
            - Pod
      verifyImages:
        - imageReferences:
            - "registry.example.com/*"
          attestors:
            - entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      ${PUBLIC_KEY}
                      -----END PUBLIC KEY-----
```

## Security Audit Scripts

### Cluster Security Scan

```bash
#!/bin/bash
# security-audit.sh - Comprehensive security audit

echo "=== Privileged Pods ==="
kubectl get pods -A -o json | jq -r '
  .items[] | select(.spec.containers[].securityContext.privileged==true) |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Pods Running as Root ==="
kubectl get pods -A -o json | jq -r '
  .items[] | select(.spec.securityContext.runAsNonRoot!=true) |
  select(.spec.containers[].securityContext.runAsNonRoot!=true) |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Pods Without Security Context ==="
kubectl get pods -A -o json | jq -r '
  .items[] | select(.spec.securityContext==null) |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Pods Without Resource Limits ==="
kubectl get pods -A -o json | jq -r '
  .items[] | select(.spec.containers[].resources.limits==null) |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Namespaces Without NetworkPolicy ==="
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
  if [ "$count" -eq 0 ]; then
    echo "$ns"
  fi
done

echo -e "\n=== ServiceAccounts with Secrets Auto-mounted ==="
kubectl get sa -A -o json | jq -r '
  .items[] | select(.automountServiceAccountToken!=false) |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Secrets in Environment Variables ==="
kubectl get pods -A -o json | jq -r '
  .items[] | select(.spec.containers[].env[]?.valueFrom.secretKeyRef!=null) |
  "\(.metadata.namespace)/\(.metadata.name)"'
```

### RBAC Audit

```bash
#!/bin/bash
# rbac-audit.sh - RBAC security audit

echo "=== ClusterRoles with Wildcard Permissions ==="
kubectl get clusterroles -o json | jq -r '
  .items[] | 
  select(.rules[]? | (.apiGroups[]? == "*") or (.resources[]? == "*") or (.verbs[]? == "*")) |
  .metadata.name'

echo -e "\n=== ClusterRoleBindings to default ServiceAccount ==="
kubectl get clusterrolebindings -o json | jq -r '
  .items[] | select(.subjects[]? | .name=="default" and .kind=="ServiceAccount") |
  "\(.metadata.name) -> \(.roleRef.name)"'

echo -e "\n=== Roles Granting Secret Access ==="
kubectl get roles -A -o json | jq -r '
  .items[] | select(.rules[]? | .resources[]? == "secrets") |
  "\(.metadata.namespace)/\(.metadata.name)"'

echo -e "\n=== Users/Groups with cluster-admin ==="
kubectl get clusterrolebindings -o json | jq -r '
  .items[] | select(.roleRef.name=="cluster-admin") |
  .subjects[]? | "\(.kind): \(.name)"'
```

## CIS Benchmark Checks

**Current CIS Benchmarks (January 2026):**
- **CIS Kubernetes Benchmark v1.9.0** (for K8s 1.27-1.31)
- **CIS Amazon EKS Benchmark v1.5.0**
- **CIS Azure AKS Benchmark v1.4.0**
- **CIS Google GKE Benchmark v1.6.0**
- **CIS Red Hat OpenShift Benchmark v1.6.0**

### Automated CIS Scanning

```bash
# Using kube-bench (v0.8.x)
# Run as a Job in cluster
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench

# Run locally with Docker
docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro \
  -v $(which kubectl):/usr/local/bin/kubectl \
  -v ~/.kube:/root/.kube \
  aquasec/kube-bench:latest --benchmark cis-1.9

# EKS-specific benchmark
docker run --pid=host aquasec/kube-bench:latest run --targets node --benchmark eks-1.5.0

# GKE-specific benchmark
docker run --pid=host aquasec/kube-bench:latest run --benchmark gke-1.6.0

# AKS-specific benchmark
docker run --pid=host aquasec/kube-bench:latest run --benchmark aks-1.4.0

# OpenShift Compliance Operator
oc get compliancescan -n openshift-compliance
oc get compliancecheckresult -n openshift-compliance
oc get complianceremediation -n openshift-compliance

# Using kubescape
kubescape scan framework cis-v1.23-t1.0.1 --submit --account ${ACCOUNT_ID}
kubescape scan control 1.1.1,1.2.1,1.2.2  # Specific controls
```

### Key Control Plane Checks

| ID | Check | Command |
|----|-------|---------|
| 1.1.1 | API server pod spec permissions | `stat -c %a /etc/kubernetes/manifests/kube-apiserver.yaml` |
| 1.2.1 | Anonymous auth disabled | Check `--anonymous-auth=false` |
| 1.2.6 | RBAC enabled | Check `--authorization-mode` includes RBAC |
| 1.2.16 | Audit logging enabled | Check `--audit-log-path` |

### Key Worker Node Checks

| ID | Check | Command |
|----|-------|---------|
| 4.1.1 | Kubelet service file permissions | `stat -c %a /etc/systemd/system/kubelet.service.d/` |
| 4.2.1 | Anonymous auth disabled | Check kubelet config `authentication.anonymous.enabled=false` |
| 4.2.6 | Protect kernel defaults | Check `--protect-kernel-defaults=true` |

### Automated CIS Scanning

```bash
# Using kube-bench
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench

# OpenShift Compliance Operator
oc get compliancescan -n openshift-compliance
oc get compliancecheckresult -n openshift-compliance
```

## Incident Response

### Compromised Pod Investigation

```bash
# 1. Isolate the pod (NetworkPolicy)
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: isolate-${POD}
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      $(kubectl get pod ${POD} -n ${NS} -o jsonpath='{.metadata.labels}' | jq -r 'to_entries | map("\(.key): \(.value)") | .[0]')
  policyTypes:
    - Ingress
    - Egress
EOF

# 2. Capture pod state
kubectl get pod ${POD} -n ${NS} -o yaml > pod-evidence.yaml
kubectl describe pod ${POD} -n ${NS} > pod-describe.txt
kubectl logs ${POD} -n ${NS} --all-containers > pod-logs.txt

# 3. Check for suspicious processes
kubectl exec ${POD} -n ${NS} -- ps aux
kubectl exec ${POD} -n ${NS} -- netstat -tulpn

# 4. Check file system changes (if possible)
kubectl exec ${POD} -n ${NS} -- find / -mtime -1 -type f 2>/dev/null

# 5. Review RBAC for the pod's service account
SA=$(kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.serviceAccountName}')
kubectl auth can-i --list --as=system:serviceaccount:${NS}:${SA}
```

### Security Event Timeline

```bash
# Get events sorted by time
kubectl get events -A --sort-by='.lastTimestamp' -o custom-columns=\
TIME:.lastTimestamp,\
TYPE:.type,\
NAMESPACE:.metadata.namespace,\
REASON:.reason,\
MESSAGE:.message | grep -i "fail\|error\|deny\|forbidden"
```
