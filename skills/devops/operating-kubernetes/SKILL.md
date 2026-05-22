---
name: operating-kubernetes
description: Operating production Kubernetes clusters effectively with resource management, advanced scheduling, networking, storage, security hardening, and autoscaling. Use when deploying workloads to Kubernetes, configuring cluster resources, implementing security policies, or troubleshooting operational issues.
---

# Kubernetes Operations

## Purpose

Operating Kubernetes clusters in production requires mastery of resource management, scheduling patterns, networking architecture, storage strategies, security hardening, and autoscaling. This skill provides operations-first frameworks for right-sizing workloads, implementing high-availability patterns, securing clusters with RBAC and Pod Security Standards, and systematically troubleshooting common failures.

Use this skill when deploying applications to Kubernetes, configuring cluster resources, implementing NetworkPolicies for zero-trust security, setting up autoscaling (HPA, VPA, KEDA), managing persistent storage, or diagnosing operational issues like CrashLoopBackOff or resource exhaustion.

## When to Use This Skill

**Common Triggers:**
- "Deploy my application to Kubernetes"
- "Configure resource requests and limits"
- "Set up autoscaling for my pods"
- "Implement NetworkPolicies for security"
- "My pod is stuck in Pending/CrashLoopBackOff"
- "Configure RBAC with least privilege"
- "Set up persistent storage for my database"
- "Spread pods across availability zones"

**Operations Covered:**
- Resource management (CPU/memory, QoS classes, quotas)
- Advanced scheduling (affinity, taints, topology spread)
- Networking (NetworkPolicies, Ingress, Gateway API)
- Storage operations (StorageClasses, PVCs, CSI)
- Security hardening (RBAC, Pod Security Standards, policies)
- Autoscaling (HPA, VPA, KEDA, cluster autoscaler)
- Troubleshooting (systematic debugging playbooks)

## Resource Management

### Quality of Service (QoS) Classes

Kubernetes assigns QoS classes based on resource requests and limits:

**Guaranteed (Highest Priority):**
- Requests equal limits for CPU and memory
- Never evicted unless exceeding limits
- Use for critical production services

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "512Mi"  # Same as request
    cpu: "500m"
```

**Burstable (Medium Priority):**
- Requests less than limits (or only requests set)
- Can burst above requests
- Evicted under node pressure
- Use for web servers, most applications

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"  # 2x request
    cpu: "500m"
```

**BestEffort (Lowest Priority):**
- No requests or limits set
- First to be evicted under pressure
- Use only for development/testing

### Decision Framework: Which QoS Class?

| Workload Type | QoS Class | Configuration |
|---------------|-----------|---------------|
| Critical API/Database | Guaranteed | requests == limits |
| Web servers, services | Burstable | limits 1.5-2x requests |
| Batch jobs | Burstable | Low requests, high limits |
| Dev/test environments | BestEffort | No limits |

### Resource Quotas and LimitRanges

Enforce multi-tenancy with ResourceQuotas (namespace limits) and LimitRanges (per-container defaults):

```yaml
# ResourceQuota: Namespace-level limits
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
```

For detailed resource management patterns including Vertical Pod Autoscaler (VPA), see `references/resource-management.md`.

## Advanced Scheduling

### Node Affinity

Control which nodes pods schedule on with required (hard) or preferred (soft) constraints:

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: node.kubernetes.io/instance-type
          operator: In
          values:
          - g4dn.xlarge  # GPU instance
```

### Taints and Tolerations

Reserve nodes for specific workloads (inverse of affinity):

```bash
# Taint GPU nodes to prevent non-GPU workloads
kubectl taint nodes gpu-node-1 workload=gpu:NoSchedule
```

```yaml
# Pod tolerates GPU taint
tolerations:
- key: "workload"
  operator: "Equal"
  value: "gpu"
  effect: "NoSchedule"
```

### Topology Spread Constraints

Distribute pods evenly across failure domains (zones, nodes):

```yaml
topologySpreadConstraints:
- maxSkew: 1  # Max difference in pod count
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: critical-app
```

For advanced scheduling patterns including pod priority and preemption, see `references/scheduling-patterns.md`.

## Networking

### NetworkPolicies (Zero-Trust Security)

Implement default-deny security with NetworkPolicies:

```yaml
# Default deny all traffic
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

```yaml
# Allow specific ingress (frontend → backend)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### Ingress vs. Gateway API

**Ingress (Legacy):**
- Widely supported, mature ecosystem
- Limited expressiveness
- Use for existing applications

**Gateway API (Modern):**
- Role-oriented design (cluster ops vs. app devs)
- More expressive (HTTPRoute, TCPRoute, TLSRoute)
- Recommended for new applications (GA in Kubernetes 1.29+)

```yaml
# Gateway API example
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-routes
spec:
  parentRefs:
  - name: production-gateway
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: backend
      port: 8080
```

For detailed networking patterns including service mesh integration, see `references/networking.md`.

## Storage

### StorageClasses (Define Performance Tiers)

StorageClasses define storage tiers for different workload needs:

```yaml
# AWS EBS SSD (high performance)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iopsPerGB: "50"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Storage Decision Matrix

| Workload | Performance | Access Mode | Storage Class |
|----------|-------------|-------------|---------------|
| Database | High | ReadWriteOnce | SSD (gp3/io2) |
| Shared files | Medium | ReadWriteMany | NFS/EFS |
| Logs (temp) | Low | ReadWriteOnce | Standard HDD |
| ML models | High | ReadOnlyMany | Object storage (S3) |

**Access Modes:**
- **ReadWriteOnce (RWO):** Single node read-write (most common)
- **ReadOnlyMany (ROX):** Multiple nodes read-only
- **ReadWriteMany (RWX):** Multiple nodes read-write (requires network storage)

For detailed storage operations including volume snapshots and CSI drivers, see `references/storage.md`.

## Security

### RBAC (Role-Based Access Control)

Implement least-privilege access with RBAC:

```yaml
# Role (namespace-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding (assign role to user)
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards

Enforce secure pod configurations at the namespace level:

```yaml
# Namespace with Restricted PSS (most secure)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Pod Security Levels:**
- **Restricted:** Most secure, removes all privilege escalations (use for applications)
- **Baseline:** Minimally restrictive, prevents known escalations
- **Privileged:** Unrestricted (only for system workloads)

For detailed security patterns including policy enforcement (Kyverno/OPA) and secrets management, see `references/security.md`.

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

Scale pod replicas based on CPU, memory, or custom metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5min before scaling down
```

### KEDA (Event-Driven Autoscaling)

Scale based on events beyond CPU/memory (queues, cron schedules, Prometheus metrics):

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-scaler
spec:
  scaleTargetRef:
    name: message-processor
  minReplicaCount: 0   # Scale to zero when queue empty
  maxReplicaCount: 30
  triggers:
  - type: rabbitmq
    metadata:
      queueName: tasks
      queueLength: "10"  # Scale up when >10 messages
```

### Autoscaling Decision Matrix

| Scenario | Use HPA | Use VPA | Use KEDA | Use Cluster Autoscaler |
|----------|---------|---------|----------|------------------------|
| Stateless web app with traffic spikes | ✅ | ❌ | ❌ | Maybe |
| Single-instance database | ❌ | ✅ | ❌ | Maybe |
| Queue processor (event-driven) | ❌ | ❌ | ✅ | Maybe |
| Pods pending (insufficient nodes) | ❌ | ❌ | ❌ | ✅ |

For detailed autoscaling patterns including VPA and cluster autoscaler configuration, see `references/autoscaling.md`.

## Troubleshooting

### Common Pod Issues

**Pod Stuck in Pending:**
```bash
kubectl describe pod <pod-name>

# Common causes:
# - Insufficient CPU/memory: Reduce requests or add nodes
# - Node selector mismatch: Fix nodeSelector or add labels
# - PVC not bound: Create PVC or fix name
# - Taint intolerance: Add toleration or remove taint
```

**CrashLoopBackOff:**
```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Check previous crash

# Common causes:
# - Application crash: Fix code or configuration
# - Missing environment variables: Add to deployment
# - Liveness probe failing: Increase initialDelaySeconds
# - OOMKilled: Increase memory limit or fix leak
```

**ImagePullBackOff:**
```bash
kubectl describe pod <pod-name>

# Common causes:
# - Image doesn't exist: Fix image name/tag
# - Authentication required: Create imagePullSecrets
# - Network issues: Check NetworkPolicies, firewall rules
```

**Service Not Accessible:**
```bash
kubectl get endpoints <service-name>  # Should list pod IPs

# If endpoints empty:
# - Service selector doesn't match pod labels
# - Pods aren't ready (readiness probe failing)
# - Check NetworkPolicies blocking traffic
```

For systematic troubleshooting playbooks including networking and storage issues, see `references/troubleshooting.md`.

## Reference Documentation

### Deep Dives
- **references/resource-management.md** - Resource requests/limits, QoS classes, ResourceQuotas, VPA
- **references/scheduling-patterns.md** - Node affinity, taints/tolerations, topology spread, priority
- **references/networking.md** - NetworkPolicies, Ingress, Gateway API, service mesh integration
- **references/storage.md** - StorageClasses, PVCs, CSI drivers, volume snapshots
- **references/security.md** - RBAC, Pod Security Standards, policy enforcement, secrets
- **references/autoscaling.md** - HPA, VPA, KEDA, cluster autoscaler configuration
- **references/troubleshooting.md** - Systematic debugging playbooks for common failures

### Examples
- **examples/manifests/** - Copy-paste ready YAML manifests
- **examples/python/** - Automation scripts (audit, cost analysis, validation)
- **examples/go/** - Operator development examples

### Tools
- **scripts/validate-resources.sh** - Audit pods without resource limits
- **scripts/audit-networkpolicies.sh** - Find namespaces without NetworkPolicies
- **scripts/cost-analysis.sh** - Resource cost breakdown by namespace

## Related Skills

- **building-ci-pipelines** - Deploy to Kubernetes from CI/CD (kubectl apply, Helm, GitOps)
- **observability** - Monitor clusters and workloads (Prometheus, Grafana, tracing)
- **secret-management** - Secure secrets in Kubernetes (External Secrets, Sealed Secrets)
- **testing-strategies** - Test manifests and deployments (Kubeval, Conftest, Kind)
- **infrastructure-as-code** - Provision Kubernetes clusters (Terraform, Cluster API)
- **gitops-workflows** - Declarative cluster management (Flux, ArgoCD)

## Best Practices Summary

**Resource Management:**
- Always set CPU/memory requests and limits
- Use VPA for automated rightsizing
- Implement resource quotas per namespace
- Monitor actual usage vs. requests

**Scheduling:**
- Use topology spread constraints for high availability
- Apply taints for workload isolation (GPU, spot instances)
- Set pod priority for critical workloads

**Networking:**
- Implement NetworkPolicies with default-deny
- Use Gateway API for new applications
- Apply rate limiting at ingress layer

**Storage:**
- Use CSI drivers (not legacy provisioners)
- Define StorageClasses per performance tier
- Enable volume snapshots for stateful apps

**Security:**
- Enforce Pod Security Standards (Restricted for apps)
- Implement RBAC with least privilege
- Use policy engines for guardrails (Kyverno/OPA)
- Scan images for vulnerabilities

**Autoscaling:**
- Use HPA for stateless workloads
- Use KEDA for event-driven workloads
- Enable cluster autoscaler with limits
- Set PodDisruptionBudgets to prevent over-disruption
