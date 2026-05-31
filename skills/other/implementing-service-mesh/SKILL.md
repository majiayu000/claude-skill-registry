---
name: implementing-service-mesh
description: Implement production-ready service mesh deployments with Istio, Linkerd, or Cilium. Configure mTLS, authorization policies, traffic routing, and progressive delivery patterns for secure, observable microservices. Use when setting up service-to-service communication, implementing zero-trust security, or enabling canary deployments.
---

# Service Mesh Implementation

## Purpose

Configure and deploy service mesh infrastructure for Kubernetes environments. Enable secure service-to-service communication with mutual TLS, implement traffic management policies, configure authorization controls, and set up progressive delivery strategies. Abstracts network complexity while providing observability, security, and resilience for microservices.

## When to Use

Invoke this skill when:

- "Set up service mesh with mTLS"
- "Configure Istio traffic routing"
- "Implement canary deployments"
- "Secure microservices communication"
- "Add authorization policies to services"
- "Traffic splitting between versions"
- "Multi-cluster service mesh setup"
- "Configure ambient mode vs sidecar"
- "Set up circuit breaker configuration"
- "Enable distributed tracing"

## Service Mesh Selection

Choose based on requirements and constraints.

**Istio Ambient (Recommended for most):**
- 8% latency overhead with mTLS (vs 166% sidecar mode)
- Enterprise features, multi-cloud, advanced L7 routing
- Sidecar-less L4 (ztunnel) + optional L7 (waypoint)

**Linkerd (Simplicity priority):**
- 33% latency overhead (lowest sidecar)
- Rust-based micro-proxy, automatic mTLS
- Best for small-medium teams, easy adoption

**Cilium (eBPF-native):**
- 99% latency overhead, kernel-level enforcement
- Advanced networking, sidecar-less by design
- Best for eBPF infrastructure, future-proof

For detailed comparison matrix and architecture trade-offs, see `references/decision-tree.md`.

## Core Concepts

### Data Plane Architectures

**Sidecar:** Proxy per pod, fine-grained L7 control, higher overhead
**Sidecar-less:** Shared node proxies (Istio Ambient) or eBPF (Cilium), lower overhead

**Istio Ambient Components:**
- ztunnel: Per-node L4 proxy for mTLS
- waypoint: Optional per-namespace L7 proxy for HTTP routing

### Traffic Management

**Routing:** Path, header, weight-based traffic distribution
**Resilience:** Retries, timeouts, circuit breakers, fault injection
**Load Balancing:** Round robin, least connections, consistent hash

### Security Model

**mTLS:** Automatic encryption, certificate rotation, zero app changes
**Modes:** STRICT (reject plaintext), PERMISSIVE (accept both)
**Authorization:** Default-deny, identity-based (not IP), L7 policies

## Istio Configuration

Istio uses Custom Resource Definitions for traffic management and security.

### VirtualService (Routing)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
```

### DestinationRule (Traffic Policy)

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-circuit-breaker
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

### PeerAuthentication (mTLS)

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

### AuthorizationPolicy (Access Control)

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

For advanced patterns (fault injection, mirroring, gateways), see `references/istio-patterns.md`.

## Linkerd Configuration

Linkerd emphasizes simplicity with automatic mTLS.

### HTTPRoute (Traffic Splitting)

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-canary
spec:
  parentRefs:
  - name: backend
    kind: Service
  rules:
  - backendRefs:
    - name: backend-v1
      port: 8080
      weight: 90
    - name: backend-v2
      port: 8080
      weight: 10
```

### ServiceProfile (Retries/Timeouts)

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: backend.production.svc.cluster.local
spec:
  routes:
  - name: GET /api/data
    condition:
      method: GET
      pathRegex: /api/data
    timeout: 3s
    retryBudget:
      retryRatio: 0.2
      minRetriesPerSecond: 10
```

### AuthorizationPolicy

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
spec:
  targetRef:
    kind: Server
    name: backend-api
  requiredAuthenticationRefs:
  - name: frontend-identity
    kind: MeshTLSAuthentication
```

For complete patterns and mTLS verification, see `references/linkerd-patterns.md`.

## Cilium Configuration

Cilium uses eBPF for kernel-level enforcement.

### CiliumNetworkPolicy (L3/L4/L7)

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: backend-access
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
      rules:
        http:
        - method: GET
          path: "/api/.*"
```

### DNS-Based Egress

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: external-api-access
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  - toFQDNs:
    - matchName: "api.github.com"
    toPorts:
    - ports:
      - port: "443"
```

For mTLS with SPIRE and eBPF patterns, see `references/cilium-patterns.md`.

## Security Implementation

### Zero-Trust Architecture

1. Enable strict mTLS (encrypt all traffic)
2. Default-deny authorization policies
3. Explicit allow rules (least privilege)
4. Identity-based access control
5. Audit logging

**Example (Istio):**

```yaml
# Strict mTLS
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Deny all by default
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec: {}
```

### Certificate Management

- Automatic rotation (24h TTL default)
- Zero-downtime updates
- External CA integration (cert-manager)
- SPIFFE/SPIRE for workload identity

For JWT authentication and external authorization (OPA), see `references/security-patterns.md`.

## Progressive Delivery

### Canary Deployment

Gradually shift traffic with monitoring.

**Stages:**
1. Deploy v2 with 0% traffic
2. Route 10% to v2, monitor metrics
3. Increase: 25% → 50% → 75% → 100%
4. Cleanup v1 deployment

**Monitor:** Error rate, latency (P95/P99), throughput

### Blue/Green Deployment

Instant cutover with quick rollback.

**Process:**
1. Deploy green alongside blue
2. Test green with header routing
3. Instant cutover to green
4. Rollback to blue if needed

### Automated Rollback (Flagger)

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: backend
spec:
  targetRef:
    kind: Deployment
    name: backend
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
```

For A/B testing and detailed patterns, see `references/progressive-delivery.md`.

## Multi-Cluster Mesh

Extend mesh across Kubernetes clusters.

**Use Cases:** HA, geo-distribution, compliance, DR

**Istio Multi-Primary:**

```bash
# Install on cluster 1
istioctl install --set values.global.meshID=mesh1 \
  --set values.global.multiCluster.clusterName=cluster1

# Exchange secrets for service discovery
istioctl x create-remote-secret --context=cluster2 | \
  kubectl apply -f - --context=cluster1
```

**Linkerd Multi-Cluster:**

```bash
# Link clusters
linkerd multicluster link --cluster-name cluster2 | \
  kubectl apply -f -

# Export service
kubectl label svc/backend mirror.linkerd.io/exported=true
```

For complete setup and cross-cluster patterns, see `references/multi-cluster.md`.

## Installation

### Istio Ambient Mode

```bash
curl -L https://istio.io/downloadIstio | sh -
istioctl install --set profile=ambient -y
kubectl label namespace production istio.io/dataplane-mode=ambient
```

### Linkerd

```bash
curl -sL https://run.linkerd.io/install-edge | sh
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
kubectl annotate namespace production linkerd.io/inject=enabled
```

### Cilium

```bash
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set meshMode=enabled \
  --set authentication.mutual.spire.enabled=true
```

## Troubleshooting

### mTLS Issues

```bash
# Istio: Check mTLS status
istioctl authn tls-check frontend.production.svc.cluster.local

# Linkerd: Check edges
linkerd edges deployment/frontend -n production

# Cilium: Check auth
cilium bpf auth list
```

### Traffic Routing Issues

```bash
# Istio: Analyze config
istioctl analyze -n production

# Linkerd: Tap traffic
linkerd tap deployment/backend -n production

# Cilium: Observe flows
hubble observe --namespace production
```

For complete debugging guide and solutions, see `references/troubleshooting.md`.

## Integration with Other Skills

**kubernetes-operations:** Cluster setup, namespaces, RBAC
**security-hardening:** Container security, secret management
**infrastructure-as-code:** Terraform/Helm for mesh deployment
**building-ci-pipelines:** Automated canary, integration tests
**performance-engineering:** Latency benchmarking, optimization

## Reference Files

- `references/decision-tree.md` - Service mesh selection and comparison
- `references/istio-patterns.md` - Istio configuration examples
- `references/linkerd-patterns.md` - Linkerd patterns and best practices
- `references/cilium-patterns.md` - Cilium eBPF policies and mTLS
- `references/security-patterns.md` - Zero-trust and authorization
- `references/progressive-delivery.md` - Canary, blue/green, A/B testing
- `references/multi-cluster.md` - Multi-cluster setup and federation
- `references/troubleshooting.md` - Common issues and debugging
