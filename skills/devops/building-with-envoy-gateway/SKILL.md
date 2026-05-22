---
name: building-with-envoy-gateway
description: Build production traffic engineering for Kubernetes with Envoy Gateway, Gateway API, KEDA autoscaling, and Envoy AI Gateway. Use when implementing ingress, rate limiting, traffic routing, TLS, autoscaling, or LLM traffic management.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
model: claude-sonnet-4-20250514
---

# Traffic Engineering with Envoy Gateway

## Persona

You are a Platform Engineer specializing in Kubernetes traffic management and API gateway patterns. You've deployed Envoy Gateway in production for high-traffic AI agent platforms. You understand Gateway API as the new Kubernetes standard, Envoy Gateway's extension CRDs, KEDA event-driven autoscaling, and Envoy AI Gateway for LLM traffic. You follow CNCF best practices and can implement the full traffic stack: ingress routing, rate limiting, circuit breaking, TLS/mTLS, autoscaling, and AI-specific traffic management.

## When to Use This Skill

Activate when the user mentions:
- Envoy Gateway, Gateway API, GatewayClass
- HTTPRoute, GRPCRoute, TCPRoute, TLSRoute
- BackendTrafficPolicy, ClientTrafficPolicy, SecurityPolicy
- Rate limiting, circuit breaking, retries, load balancing
- TLS termination, mTLS, CertManager
- KEDA, ScaledObject, event-driven autoscaling
- Envoy AI Gateway, token-based rate limiting, provider fallback
- Ingress replacement, Traefik, Kong migration
- Canary deployments, blue-green, traffic splitting
- HPA, VPA, autoscaling for AI agents

## Core Concepts

### Gateway API: The New Kubernetes Standard

| Resource | Purpose | Scope |
|----------|---------|-------|
| **GatewayClass** | Defines gateway implementation (like StorageClass for networking) | Cluster |
| **Gateway** | Traffic entry point with listeners (ports, protocols, hostnames) | Namespace |
| **HTTPRoute** | L7 routing rules (path, headers, query params, methods) | Namespace |
| **GRPCRoute** | gRPC-specific routing with Protocol Buffers | Namespace |
| **ReferenceGrant** | Cross-namespace resource access control | Namespace |

### Envoy Gateway Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Control Plane                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Gateway    │  │     xDS      │  │    Infra     │       │
│  │  Translator  │──│   Server     │──│   Manager    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                 │                                  │
│         ▼                 │                                  │
│    Gateway API            │                                  │
│    + Extensions           │                                  │
└───────────────────────────│──────────────────────────────────┘
                            │ xDS Protocol
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Plane                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Envoy Proxy  │  │ Envoy Proxy  │  │ Envoy Proxy  │       │
│  │  (replica)   │  │  (replica)   │  │  (replica)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Envoy Gateway Extension CRDs

| CRD | Purpose | Target | Key Features |
|-----|---------|--------|--------------|
| **BackendTrafficPolicy** | Gateway-to-backend traffic | HTTPRoute, Gateway | Rate limiting, retries, circuit breaker, load balancing |
| **ClientTrafficPolicy** | Client-to-gateway connections | Gateway | TLS, timeouts, keepalive, connection limits |
| **SecurityPolicy** | Authentication & authorization | HTTPRoute, Gateway | JWT, OIDC, Basic Auth, IP allowlist, CORS |
| **EnvoyProxy** | Proxy deployment config | GatewayClass | Replicas, resources, telemetry |
| **Backend** | Advanced endpoint config | - | FQDN, mTLS client certs |

## Decision Logic

### Which Policy for Which Scenario?

| Scenario | Policy | Configuration |
|----------|--------|---------------|
| Rate limit all traffic globally | BackendTrafficPolicy | `rateLimit.global` with Redis backend |
| Rate limit per-instance (cost-effective) | BackendTrafficPolicy | `rateLimit.local` |
| Retry transient failures | BackendTrafficPolicy | `retry.attempts`, `retry.retryOn` |
| Circuit breaker for unreliable backends | BackendTrafficPolicy | `healthChecks` + outlier detection |
| TLS termination at gateway | ClientTrafficPolicy | `tls.certificateRefs` |
| Client connection timeouts | ClientTrafficPolicy | `timeout.http` |
| JWT token validation | SecurityPolicy | `jwt.providers` with JWKS |
| SSO with identity provider | SecurityPolicy | `oidc.provider` |
| IP-based access control | SecurityPolicy | `authorization.rules` with `ipAddress` |

### Authentication Method Selection

```
Is enterprise SSO needed?
├── Yes → Use OIDC (delegate to identity provider)
└── No → Is stateless API auth acceptable?
    ├── Yes → Use JWT (validate JWKS locally)
    └── No → Is it simple internal API?
        ├── Yes → Use Basic Auth or API Key
        └── No → Use External Authorization service
```

### Rate Limiting Strategy

```
Need cross-instance coordination?
├── Yes → Global Rate Limit (requires Redis)
│         Use for: org-wide limits, preventing resource exhaustion
└── No → Local Rate Limit (per-proxy bucket)
         Use for: per-region limits, cost-effective protection
```

## Workflow: Full Traffic Stack Setup

### 1. Install Envoy Gateway via Helm

```bash
# Add Helm repo
helm install eg oci://docker.io/envoyproxy/gateway-helm \
  --version v1.6.1 \
  -n envoy-gateway-system \
  --create-namespace

# Verify installation
kubectl wait --for=condition=Available deployment/envoy-gateway \
  -n envoy-gateway-system --timeout=120s

# Install Gateway API CRDs if not present
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml
```

### 2. Create GatewayClass and Gateway

```yaml
# gateway-class.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: envoy-gateway
spec:
  controllerName: gateway.envoyproxy.io/gatewayclass-controller
---
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: task-api-gateway
  namespace: default
spec:
  gatewayClassName: envoy-gateway
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - kind: Secret
        name: tls-cert
    allowedRoutes:
      namespaces:
        from: Same
```

### 3. Create HTTPRoute for Application

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: task-api-route
  namespace: default
spec:
  parentRefs:
  - name: task-api-gateway
  hostnames:
  - "api.example.com"
  rules:
  # API endpoints with versioning
  - matches:
    - path:
        type: PathPrefix
        value: /api/v1/tasks
    backendRefs:
    - name: task-api
      port: 8000

  # Health check endpoint
  - matches:
    - path:
        type: Exact
        value: /health
    backendRefs:
    - name: task-api
      port: 8000

  # Traffic splitting for canary
  - matches:
    - path:
        type: PathPrefix
        value: /api/v2/tasks
    backendRefs:
    - name: task-api-v2
      port: 8000
      weight: 10
    - name: task-api-v1
      port: 8000
      weight: 90
```

### 4. Apply Rate Limiting (BackendTrafficPolicy)

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: BackendTrafficPolicy
metadata:
  name: task-api-rate-limit
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: task-api-route

  rateLimit:
    type: Global
    global:
      rules:
      # Per-user rate limit (distinct header)
      - clientSelectors:
        - headers:
          - type: Distinct
            name: x-user-id
        limit:
          requests: 100
          unit: Minute

      # Anonymous users (no x-user-id header)
      - clientSelectors:
        - headers:
          - name: x-user-id
            invert: true
        limit:
          requests: 10
          unit: Minute

  # Retry policy
  retry:
    numRetries: 3
    perRetryTimeout: 5s
    retryOn:
    - "5xx"
    - "reset"
    - "connect-failure"
    backoff:
      baseInterval: 100ms
      maxInterval: 10s
```

### 5. Configure Circuit Breaking

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: BackendTrafficPolicy
metadata:
  name: task-api-resilience
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: task-api-route

  healthCheck:
    active:
      type: HTTP
      http:
        path: /health
        expectedStatuses:
        - 200
      interval: 10s
      timeout: 1s
      unhealthyThreshold: 3
      healthyThreshold: 1

  circuitBreaker:
    maxConnections: 100
    maxPendingRequests: 50
    maxRequests: 1000
```

### 6. Configure TLS with CertManager

```yaml
# Install CertManager first
# kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.0/cert-manager.yaml

# cluster-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          ingressClassName: envoy
---
# certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls
  namespace: default
spec:
  secretName: tls-cert
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.example.com
```

### 7. JWT Authentication (SecurityPolicy)

```yaml
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: SecurityPolicy
metadata:
  name: jwt-auth
  namespace: default
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: task-api-route

  jwt:
    providers:
    - name: auth0
      issuer: https://your-tenant.auth0.com/
      audiences:
      - https://api.example.com
      remoteJWKS:
        uri: https://your-tenant.auth0.com/.well-known/jwks.json
      claimToHeaders:
      - claim: sub
        header: x-user-id
      - claim: permissions
        header: x-user-permissions
```

### 8. Install KEDA for Autoscaling

```bash
# Install KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda \
  --namespace keda \
  --create-namespace
```

### 9. Configure KEDA ScaledObject

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: task-api-scaler
  namespace: default
spec:
  scaleTargetRef:
    name: task-api
    kind: Deployment
  minReplicaCount: 1
  maxReplicaCount: 20

  triggers:
  # Scale based on Prometheus metrics (request rate)
  - type: prometheus
    metadata:
      serverAddress: http://prometheus.monitoring:9090
      metricName: http_requests_per_second
      query: sum(rate(envoy_http_downstream_rq_total{envoy_cluster_name="task-api"}[1m]))
      threshold: "100"

  # Scale based on Kafka consumer lag
  - type: kafka
    metadata:
      bootstrapServers: kafka.default:9092
      consumerGroup: task-processors
      topic: task-events
      lagThreshold: "50"
```

## Key Patterns

### Traffic Splitting for Canary Deployments

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: canary-route
spec:
  parentRefs:
  - name: api-gateway
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    # Stable version: 90%
    - name: api-stable
      port: 8000
      weight: 90
    # Canary version: 10%
    - name: api-canary
      port: 8000
      weight: 10
```

### Header-Based A/B Testing

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: ab-test-route
spec:
  parentRefs:
  - name: api-gateway
  rules:
  # Beta users (header match)
  - matches:
    - headers:
      - name: x-beta-user
        value: "true"
    backendRefs:
    - name: api-v2
      port: 8000

  # All other users
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: api-v1
      port: 8000
```

### Envoy AI Gateway for LLM Traffic

```yaml
# For AI agent traffic management
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: AIGatewayRoute
metadata:
  name: llm-router
spec:
  backends:
  # Primary: OpenAI
  - name: openai
    priority: 0
    provider: openai
    model: gpt-4
    auth:
      type: APIKey
      apiKeyRef:
        name: openai-key

  # Fallback: Anthropic
  - name: anthropic
    priority: 1
    provider: anthropic
    model: claude-3-opus
    modelNameOverride: gpt-4
    auth:
      type: APIKey
      apiKeyRef:
        name: anthropic-key

  # Token-based rate limiting
  rateLimit:
    tokenBudget:
      perUser: 100000
      perMinute: 10000
```

## Safety & Guardrails

### NEVER
- Expose management endpoints (health checks, metrics) without authentication
- Use LocalRateLimit when cross-instance coordination is required
- Skip TLS for production traffic
- Set rate limits too high initially (start conservative, increase based on monitoring)
- Use weight 0 for all backends in traffic splitting (will fail)
- Deploy without health checks on backends

### ALWAYS
- Start with strict rate limits and loosen based on actual usage
- Use ReferenceGrant for cross-namespace access
- Configure health checks before enabling circuit breakers
- Test canary deployments with small traffic percentages first
- Monitor 429 (rate limit) and 503 (circuit breaker) responses
- Use mTLS for backend traffic in production
- Set appropriate timeouts (start with 30s, tune based on P99)

### Cost Engineering
- KEDA scale-to-zero saves 40-70% on idle workloads
- Token-based rate limiting prevents LLM cost overruns
- Local rate limiting avoids Redis costs when global isn't needed
- Schedule non-production gateways to scale down outside business hours

## TaskManager Example

Complete traffic engineering setup for Task API:

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
  namespace: default
  labels:
    app: task-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: task-api
  template:
    metadata:
      labels:
        app: task-api
    spec:
      containers:
      - name: task-api
        image: task-api:latest
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: task-api
  namespace: default
spec:
  selector:
    app: task-api
  ports:
  - port: 8000
    targetPort: 8000
```

### Full Gateway Configuration

```yaml
# Gateway with TLS
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: task-gateway
spec:
  gatewayClassName: envoy-gateway
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - kind: Secret
        name: task-api-tls
---
# HTTPRoute with versioned paths
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: task-route
spec:
  parentRefs:
  - name: task-gateway
  hostnames:
  - tasks.example.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api/v1
    backendRefs:
    - name: task-api
      port: 8000
---
# Rate limiting + retries
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: BackendTrafficPolicy
metadata:
  name: task-traffic
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: task-route
  rateLimit:
    type: Global
    global:
      rules:
      - limit:
          requests: 100
          unit: Second
  retry:
    numRetries: 3
    retryOn: ["5xx", "reset"]
---
# JWT authentication
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: SecurityPolicy
metadata:
  name: task-auth
spec:
  targetRefs:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    name: task-route
  jwt:
    providers:
    - name: task-auth
      issuer: https://auth.example.com
      remoteJWKS:
        uri: https://auth.example.com/.well-known/jwks.json
---
# KEDA autoscaling
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: task-scaler
spec:
  scaleTargetRef:
    name: task-api
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      query: sum(rate(http_requests_total{app="task-api"}[1m]))
      threshold: "50"
```

## References

For detailed patterns, see:
- `references/gateway-api-patterns.md` - HTTPRoute matching examples
- `references/envoy-gateway-crds.md` - Full CRD reference
- `references/keda-scalers.md` - KEDA scaler configurations
- `references/ai-gateway.md` - Envoy AI Gateway patterns
