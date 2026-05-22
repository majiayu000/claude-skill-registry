---
name: kubernetes-patterns
description: Provides Kubernetes resource management, Helm chart patterns, service mesh configuration, and autoscaling strategies. Covers HPA, VPA, KEDA, operators, security contexts, and namespace isolation. Use when user mentions 'kubernetes', 'k8s', 'helm', 'istio', 'linkerd', 'service mesh', 'HPA', 'VPA', 'KEDA', 'pod security', 'resource quotas', 'operators'.
type: skill
category: patterns
status: stable
origin: tibsfox
modified: false
first_seen: 2026-02-07
first_path: examples/kubernetes-patterns/SKILL.md
superseded_by: null
---
# Kubernetes Patterns

Best practices for deploying, scaling, securing, and managing workloads on Kubernetes. This skill covers resource management, Helm chart structure, service mesh configuration, autoscaling strategies, and security hardening.

## Resource Management

Every container must declare resource requests and limits. Without them, the scheduler cannot make informed placement decisions and nodes can become overcommitted.

| Resource Type | Request (Guaranteed) | Limit (Maximum) | What Happens at Limit |
|---------------|---------------------|-----------------|----------------------|
| CPU | Reserved on node | Throttled (not killed) | Container slows down |
| Memory | Reserved on node | OOM-killed | Container restarts |
| Ephemeral Storage | Reserved on node | Evicted | Pod removed from node |
| GPU | Reserved on node | Hard limit | Cannot exceed |

### QoS Classes

Kubernetes assigns QoS classes based on resource declarations. This determines eviction priority.

| QoS Class | Condition | Eviction Priority |
|-----------|-----------|-------------------|
| Guaranteed | requests == limits for all containers | Last (highest priority) |
| Burstable | requests < limits for at least one container | Middle |
| BestEffort | No requests or limits set | First (lowest priority) |

### Resource Declaration Best Practices

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
        version: v2.1.0
    spec:
      # Topology spread for high availability
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api-server
      containers:
        - name: api
          image: ghcr.io/our-org/api@sha256:a1b2c3d4e5f6
          ports:
            - containerPort: 8080
              protocol: TCP
          resources:
            requests:
              cpu: 250m        # 0.25 cores -- baseline
              memory: 256Mi    # baseline memory
            limits:
              cpu: "1"         # burst to 1 core
              memory: 512Mi    # hard cap prevents OOM cascade
          # Probes are essential for rolling updates
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 2
```

## Namespace Isolation Strategies

Namespaces provide logical boundaries. Combine with NetworkPolicies and RBAC for true isolation.

| Strategy | Isolation Level | Use Case |
|----------|----------------|----------|
| Per-team | Medium | Small org, shared cluster |
| Per-environment | Medium | Dev/staging/prod in one cluster |
| Per-application | High | Microservices with strict boundaries |
| Per-tenant | Highest | Multi-tenant SaaS |

### Resource Quotas and Limit Ranges

```yaml
# ResourceQuota: caps total resource consumption per namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-alpha-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
    services: "20"
    persistentvolumeclaims: "10"
    secrets: "30"
    configmaps: "30"
---
# LimitRange: sets defaults and bounds per container
apiVersion: v1
kind: LimitRange
metadata:
  name: team-alpha-limits
  namespace: team-alpha
spec:
  limits:
    - type: Container
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      min:
        cpu: 50m
        memory: 64Mi
      max:
        cpu: "4"
        memory: 4Gi
    - type: PersistentVolumeClaim
      min:
        storage: 1Gi
      max:
        storage: 50Gi
```

### Network Policy for Namespace Isolation

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: team-alpha
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
# Allow only within namespace + DNS
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-intra-namespace
  namespace: team-alpha
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector: {}
  egress:
    - to:
        - podSelector: {}
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

## Helm Chart Structure

Helm charts package Kubernetes manifests with templating and dependency management.

### Standard Chart Layout

```
my-app/
  Chart.yaml              # Chart metadata, version, dependencies
  Chart.lock              # Locked dependency versions
  values.yaml             # Default configuration values
  values-staging.yaml     # Environment-specific overrides
  values-production.yaml  # Environment-specific overrides
  templates/
    _helpers.tpl          # Template helper functions
    deployment.yaml       # Deployment manifest
    service.yaml          # Service manifest
    ingress.yaml          # Ingress manifest
    hpa.yaml              # HorizontalPodAutoscaler
    configmap.yaml        # ConfigMap
    secret.yaml           # Secret (sealed or external)
    serviceaccount.yaml   # ServiceAccount
    networkpolicy.yaml    # NetworkPolicy
    pdb.yaml              # PodDisruptionBudget
    tests/
      test-connection.yaml  # Helm test hooks
  charts/                 # Dependency charts (vendored)
```

### Chart.yaml Best Practices

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for the My App API service
type: application
version: 1.4.0        # Chart version (bump on chart changes)
appVersion: "2.1.0"   # Application version (bump on app changes)

dependencies:
  - name: postgresql
    version: "13.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: "18.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled

maintainers:
  - name: Platform Team
    email: platform@company.com
```

### Helm Template with Guards

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        # Force rollout on config changes
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "my-app.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          {{- with .Values.resources }}
          resources:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.env }}
          env:
            {{- toYaml . | nindent 12 }}
          {{- end }}
```

## Service Mesh: Istio Configuration

Service meshes handle traffic management, security, and observability at the infrastructure layer.

### Istio vs Linkerd Comparison

| Aspect | Istio | Linkerd |
|--------|-------|---------|
| Complexity | High (many CRDs, control plane components) | Low (minimal, opinionated) |
| Resource Overhead | ~100MB per sidecar | ~25MB per sidecar |
| mTLS | Configurable (permissive/strict) | On by default |
| Traffic Management | Very flexible (VirtualService, DestinationRule) | Basic (TrafficSplit, ServiceProfile) |
| Multi-cluster | Built-in | Supported with multicluster extension |
| Learning Curve | Steep | Gentle |
| Best For | Complex routing, advanced policies | Simple mTLS + observability |

### Istio VirtualService: Canary with Header Routing

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-server
  namespace: production
spec:
  hosts:
    - api-server
    - api.company.com
  gateways:
    - mesh                    # In-mesh traffic
    - api-gateway             # External traffic
  http:
    # Route internal testers to canary via header
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: api-server
            subset: canary
          weight: 100

    # Weighted canary for production traffic
    - route:
        - destination:
            host: api-server
            subset: stable
          weight: 90
        - destination:
            host: api-server
            subset: canary
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,reset,connect-failure
      timeout: 10s

---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: api-server
  namespace: production
spec:
  host: api-server
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        maxRequestsPerConnection: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: stable
      labels:
        version: v2.0.0
    - name: canary
      labels:
        version: v2.1.0
```

## Autoscaling Strategies

### HPA with Custom Metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 3
  maxReplicas: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100            # Double capacity per minute
          periodSeconds: 60
        - type: Pods
          value: 5              # Or add 5 pods, whichever is higher
          periodSeconds: 60
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 25             # Remove 25% per 2 minutes
          periodSeconds: 120
      selectPolicy: Min
  metrics:
    # CPU-based scaling
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

    # Memory-based scaling
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

    # Custom metric: requests per second from Prometheus
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
```

### KEDA ScaledObject: Event-Driven Autoscaling

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor
  namespace: production
spec:
  scaleTargetRef:
    name: order-processor
  pollingInterval: 15          # Check triggers every 15s
  cooldownPeriod: 60           # Wait 60s after last trigger before scale-down
  minReplicaCount: 1           # Minimum replicas (0 for scale-to-zero)
  maxReplicaCount: 100
  fallback:
    failureThreshold: 3
    replicas: 5                # Fallback if scaler fails
  triggers:
    # Scale based on Kafka consumer lag
    - type: kafka
      metadata:
        bootstrapServers: kafka.production:9092
        consumerGroup: order-processor
        topic: orders
        lagThreshold: "50"     # Scale up when lag > 50 per partition

    # Scale based on RabbitMQ queue depth
    - type: rabbitmq
      metadata:
        host: amqp://rabbitmq.production:5672
        queueName: order-queue
        queueLength: "100"

    # Scale based on Prometheus metric
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.monitoring:9090
        query: |
          sum(rate(http_requests_total{service="order-processor"}[2m]))
        threshold: "500"
---
# Scale-to-zero for batch jobs
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: report-generator
  namespace: batch
spec:
  scaleTargetRef:
    name: report-generator
  minReplicaCount: 0           # Scale to zero when idle
  maxReplicaCount: 10
  triggers:
    - type: cron
      metadata:
        timezone: America/New_York
        start: 0 2 * * *       # Scale up at 2 AM
        end: 0 6 * * *         # Scale down at 6 AM
        desiredReplicas: "5"
```

### Autoscaling Strategy Comparison

| Strategy | Scales On | Scale-to-Zero | Latency | Best For |
|----------|-----------|---------------|---------|----------|
| HPA (CPU/Memory) | Resource utilization | No | Seconds | Steady traffic patterns |
| HPA (Custom) | Application metrics | No | Seconds | API servers, web apps |
| VPA | Historical usage | No | Pod restart | Right-sizing resources |
| KEDA | External events | Yes | Seconds | Event-driven workloads |
| Cluster Autoscaler | Node pressure | No | Minutes | Node pool management |
| Karpenter | Pod scheduling needs | No | Seconds | Fast, flexible node scaling |

## Pod Security Best Practices

### Security Context Configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  # Pod-level security context
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  serviceAccountName: app-service-account
  automountServiceAccountToken: false    # Disable unless needed
  containers:
    - name: app
      image: ghcr.io/our-org/app@sha256:abc123
      # Container-level security context
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
          # Only add specific capabilities if absolutely needed
          # add:
          #   - NET_BIND_SERVICE
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  volumes:
    # Writable dirs for read-only root filesystem
    - name: tmp
      emptyDir:
        sizeLimit: 100Mi
    - name: cache
      emptyDir:
        sizeLimit: 500Mi
```

### Pod Security Standards (PSS)

| Level | Description | Key Restrictions |
|-------|-------------|-----------------|
| Privileged | Unrestricted | None (cluster admin workloads) |
| Baseline | Minimally restrictive | No hostNetwork, hostPID, hostIPC, privileged containers |
| Restricted | Heavily restricted | runAsNonRoot, drop ALL capabilities, readOnlyRootFilesystem, seccomp |

```yaml
# Enforce restricted standard on namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Operator Pattern

Operators extend Kubernetes with domain-specific controllers that encode operational knowledge.

### When to Build an Operator

| Use Operator | Don't Use Operator |
|-------------|-------------------|
| Stateful applications (databases, caches) | Stateless apps (use Deployment) |
| Complex lifecycle management | Simple CRUD workloads |
| Custom scaling logic | Standard HPA is sufficient |
| Automated backup/restore | Manual operations are fine |
| Multi-step provisioning | Single manifest applies cleanly |

### Operator Maturity Model

| Level | Capability | Example |
|-------|-----------|---------|
| 1 - Basic Install | Automated install, lifecycle hooks | Helm chart with operator |
| 2 - Seamless Upgrades | Patch and minor version upgrades | Rolling update strategy |
| 3 - Full Lifecycle | Backup, restore, failure recovery | Automated database failover |
| 4 - Deep Insights | Metrics, alerts, log processing | Custom Prometheus exporters |
| 5 - Auto Pilot | Auto-scaling, tuning, anomaly detection | Self-healing database cluster |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No resource requests/limits | Node overcommit, OOM kills, unpredictable scheduling | Set requests and limits on every container |
| `latest` image tag | Non-reproducible deployments, silent breakage | Use immutable tags or `@sha256:` digest |
| Running as root | Container escape leads to host compromise | `runAsNonRoot: true`, `runAsUser: 10001` |
| No readiness probe | Traffic sent to unready pods, user-facing errors | Always define readinessProbe with appropriate thresholds |
| No PodDisruptionBudget | Cluster upgrades kill all replicas simultaneously | Set PDB with `minAvailable` or `maxUnavailable` |
| Single replica in production | Any disruption causes downtime | Minimum 3 replicas with topology spread |
| Hardcoded config in images | Rebuilds needed for config changes | Use ConfigMaps, Secrets, environment variables |
| ClusterRole for app workloads | Excessive permissions across all namespaces | Namespace-scoped Roles with least privilege |
| No NetworkPolicy | All pods can talk to all pods (flat network) | Default-deny with explicit allow rules |
| Helm values in CI pipeline | Config scattered, hard to audit | `values-{env}.yaml` files in Git |
| `kubectl apply` in production | No rollback tracking, no drift detection | GitOps with Argo CD or Flux |
| Ignoring pod topology spread | All replicas on same node/zone | `topologySpreadConstraints` for HA |
| No seccomp profile | Containers can use any syscall | `seccompProfile.type: RuntimeDefault` |
| Mounting service account tokens | Compromised pod can access API server | `automountServiceAccountToken: false` unless needed |

## Kubernetes Security Checklist

- [ ] All containers define resource requests and limits
- [ ] Images pinned by digest (`@sha256:`) not mutable tags
- [ ] `runAsNonRoot: true` on all pods
- [ ] `allowPrivilegeEscalation: false` on all containers
- [ ] `readOnlyRootFilesystem: true` with explicit writable mounts
- [ ] All capabilities dropped (`drop: [ALL]`), add back only as needed
- [ ] `seccompProfile.type: RuntimeDefault` on all pods
- [ ] `automountServiceAccountToken: false` unless API access is needed
- [ ] NetworkPolicies enforce default-deny with explicit allow rules
- [ ] Pod Security Standards enforced at namespace level (`restricted`)
- [ ] RBAC uses namespace-scoped Roles (not ClusterRoles) for workloads
- [ ] Secrets encrypted at rest (EncryptionConfiguration or KMS provider)
- [ ] PodDisruptionBudgets defined for all production workloads
- [ ] Topology spread constraints distribute pods across zones
- [ ] Readiness, liveness, and startup probes configured on all containers
- [ ] Helm charts use `values-{env}.yaml` per environment, reviewed in PRs
- [ ] Image pull policies set to `IfNotPresent` for tagged, `Always` for `latest`
- [ ] Service mesh mTLS enabled for inter-service communication
- [ ] Audit logging enabled on API server with appropriate retention
- [ ] Cluster upgrades tested in staging before production rollout
