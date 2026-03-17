---
name: istio
description: Service mesh implementation with Istio for microservices traffic management, security, and observability. Use when implementing service mesh, mTLS, traffic routing, load balancing, circuit breakers, retries, timeouts, canary deployments, A/B testing, or service-to-service communication. Triggers: istio, service mesh, envoy, sidecar, virtualservice, destinationrule, gateway, mtls, peerauthentication, authorizationpolicy, serviceentry, traffic management, traffic splitting, canary, blue-green, circuit breaker, retry, timeout, load balancing, ingress, egress, observability, tracing, telemetry.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Istio Service Mesh

## Overview

Istio is an open-source service mesh that provides traffic management, security, and observability for microservices architectures. It uses a sidecar proxy pattern with Envoy proxies to intercept and control all network communication between services.

### Core Capabilities

**Traffic Management**: Load balancing, traffic splitting, canary deployments, blue-green deployments, A/B testing, retries, timeouts, circuit breakers, fault injection.

**Security**: mTLS encryption, certificate management, authentication, authorization policies, RBAC, JWT validation, service-to-service security.

**Observability**: Distributed tracing, metrics collection, access logging, service topology visualization, golden signals monitoring.

### Quick Reference: Common Tasks

| Task                         | Resources                          | Section                               |
| ---------------------------- | ---------------------------------- | ------------------------------------- |
| Enable mTLS between services | PeerAuthentication                 | mTLS PeerAuthentication               |
| Route traffic to new version | VirtualService + DestinationRule   | Traffic Splitting for Canary          |
| Add circuit breaker          | DestinationRule (outlierDetection) | Circuit Breaker and Retry             |
| Configure retries/timeouts   | VirtualService (retries, timeout)  | Circuit Breaker and Retry             |
| Expose service to internet   | Gateway + VirtualService           | Gateway and VirtualService            |
| Control egress traffic       | Sidecar + ServiceEntry             | Sidecar Resource for Egress           |
| Add authorization rules      | AuthorizationPolicy                | AuthorizationPolicy for RBAC          |
| Configure load balancing     | DestinationRule (loadBalancer)     | DestinationRule with Traffic Policies |
| Test resilience              | VirtualService (fault injection)   | Fault Injection for Testing           |

### Architecture Components

#### Control Plane (istiod)

- Service discovery and configuration distribution
- Certificate authority for mTLS
- Pilot for traffic management
- Galley for configuration validation
- Citadel for security

#### Data Plane

- Envoy proxies deployed as sidecars
- Intercept all inbound and outbound traffic
- Enforce policies and collect telemetry
- Handle traffic routing, load balancing, and retries

#### Key Resources

- `Gateway`: Configures load balancers for HTTP/TCP traffic entering the mesh
- `VirtualService`: Defines traffic routing rules
- `DestinationRule`: Configures policies after routing (load balancing, connection pools, circuit breakers)
- `ServiceEntry`: Adds external services to the mesh
- `PeerAuthentication`: Configures mTLS between services
- `AuthorizationPolicy`: Defines access control policies
- `Sidecar`: Controls sidecar proxy configuration and egress traffic

## Installation and Configuration

### Install Istio with istioctl

```bash
# Download and install istioctl
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Install Istio with production profile
istioctl install --set profile=production -y

# Verify installation
kubectl get pods -n istio-system
istioctl verify-install

# Enable automatic sidecar injection for namespace
kubectl label namespace default istio-injection=enabled
```

### Configuration Profiles

```bash
# Minimal: Control plane only, no ingress/egress
istioctl install --set profile=minimal

# Default: Recommended for production
istioctl install --set profile=default

# Production: High availability control plane
istioctl install --set profile=production

# Custom configuration
istioctl install --set profile=default \
  --set meshConfig.accessLogFile=/dev/stdout \
  --set meshConfig.enableTracing=true \
  --set meshConfig.defaultConfig.proxyMetadata.ISTIO_META_DNS_CAPTURE=true
```

### Verify Sidecar Injection

```bash
# Check if namespace has injection enabled
kubectl get namespace -L istio-injection

# Verify pod has sidecar
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].name}'
# Should show: app-container istio-proxy

# View sidecar configuration
istioctl proxy-config all <pod-name>.<namespace>
```

## Best Practices

### Gateway Configuration

#### Guidelines

- Use dedicated Gateway resources per domain or protocol
- Configure HTTPS with proper TLS certificates
- Implement health checks and timeouts
- Use wildcard domains sparingly for security
- Place gateways in dedicated namespaces (istio-system or istio-ingress)

#### Anti-patterns

- Avoid multiple Gateways binding to the same port/host combination
- Don't expose internal services directly without authentication
- Never hardcode credentials in Gateway specs

### Traffic Management Patterns

#### Progressive Delivery

- Use weighted routing for canary deployments
- Implement blue-green deployments with instant traffic switching
- Apply header-based routing for testing new versions
- Monitor metrics before promoting canaries

#### Resilience

- Configure retries with exponential backoff
- Implement circuit breakers to prevent cascade failures
- Set connection pool limits to protect services
- Use outlier detection to remove unhealthy instances

#### Routing Strategy

- Route based on headers, URI paths, or query parameters
- Use subset-based routing for version management
- Implement fault injection for chaos testing
- Apply timeouts at every service boundary

### Security Policies

#### mTLS Configuration

- Enable STRICT mode in production for all services
- Use PERMISSIVE mode only during migration
- Scope PeerAuthentication to specific namespaces or workloads
- Verify mTLS status with `istioctl authn tls-check`

#### Authorization

- Default deny all traffic, then explicitly allow
- Use namespace-level policies for broad rules
- Apply workload-specific policies for fine-grained control
- Leverage JWT authentication for end-user identity
- Audit authorization policies regularly

#### Certificate Management

- Rotate certificates automatically (default 90 days)
- Use external CA for production (cert-manager, Vault)
- Monitor certificate expiration
- Test certificate renewal procedures

### Observability Integration

#### Metrics

- Deploy Prometheus for metrics collection
- Use Grafana dashboards for visualization
- Monitor golden signals: latency, traffic, errors, saturation
- Set up alerts for SLO violations

#### Tracing

- Integrate with Jaeger, Zipkin, or Datadog
- Propagate trace headers in application code
- Sample traces intelligently (not 100% in production)
- Use tracing for debugging latency issues

#### Logging

- Enable access logs selectively (performance impact)
- Structure logs in JSON format
- Send logs to centralized logging (ELK, Splunk)
- Include trace IDs in application logs

## Production-Ready Examples

### Gateway and VirtualService

```yaml
# gateway.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: public-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
    # HTTPS configuration
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: tls-cert-secret # Secret in istio-system namespace
      hosts:
        - "api.example.com"
        - "app.example.com"
    # HTTP to HTTPS redirect
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "api.example.com"
        - "app.example.com"
      tls:
        httpsRedirect: true
---
# virtualservice.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routes
  namespace: default
spec:
  hosts:
    - "api.example.com"
  gateways:
    - istio-system/public-gateway
  http:
    # Route /v2 to new service
    - match:
        - uri:
            prefix: "/v2/"
      rewrite:
        uri: "/"
      route:
        - destination:
            host: api-v2.default.svc.cluster.local
            port:
              number: 8080
      timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s
        retryOn: 5xx,reset,connect-failure,refused-stream
    # Route /v1 to legacy service
    - match:
        - uri:
            prefix: "/v1/"
      route:
        - destination:
            host: api-v1.default.svc.cluster.local
            port:
              number: 8080
      timeout: 60s
    # Default route
    - route:
        - destination:
            host: api-v2.default.svc.cluster.local
            port:
              number: 8080
```

### DestinationRule with Traffic Policies

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-destination
  namespace: default
spec:
  host: api.default.svc.cluster.local
  trafficPolicy:
    # Load balancing
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id # Session affinity
    # Connection pool settings
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
        tcpKeepalive:
          time: 7200s
          interval: 75s
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
        maxRetries: 3
    # Outlier detection (circuit breaker)
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
    # TLS settings for upstream
    tls:
      mode: ISTIO_MUTUAL # Use Istio mTLS
  # Define subsets for version-based routing
  subsets:
    - name: v1
      labels:
        version: v1
      trafficPolicy:
        loadBalancer:
          simple: ROUND_ROBIN
    - name: v2
      labels:
        version: v2
      trafficPolicy:
        loadBalancer:
          simple: LEAST_REQUEST
```

### Traffic Splitting for Canary Deployment

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: canary-rollout
  namespace: default
spec:
  hosts:
    - reviews.default.svc.cluster.local
  http:
    # Send 10% of traffic to canary
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: reviews.default.svc.cluster.local
            subset: v2
    - route:
        - destination:
            host: reviews.default.svc.cluster.local
            subset: v1
          weight: 90
        - destination:
            host: reviews.default.svc.cluster.local
            subset: v2
          weight: 10
---
# Blue-Green Deployment (instant switch)
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: blue-green
  namespace: default
spec:
  hosts:
    - orders.default.svc.cluster.local
  http:
    - route:
        # Switch to green by changing weight to 100
        - destination:
            host: orders.default.svc.cluster.local
            subset: blue
          weight: 100
        - destination:
            host: orders.default.svc.cluster.local
            subset: green
          weight: 0
```

### Circuit Breaker and Retry Configuration

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: circuit-breaker
  namespace: default
spec:
  host: backend.default.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 10
      http:
        http1MaxPendingRequests: 1
        http2MaxRequests: 10
        maxRequestsPerConnection: 1
    outlierDetection:
      # Remove instance after 5 consecutive errors
      consecutive5xxErrors: 5
      consecutiveGatewayErrors: 5
      # Check every 1 second
      interval: 1s
      # Keep instance ejected for 30 seconds
      baseEjectionTime: 30s
      # Maximum 100% of instances can be ejected
      maxEjectionPercent: 100
      # Minimum 0% must be healthy (allows full ejection for testing)
      minHealthPercent: 0
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: retry-policy
  namespace: default
spec:
  hosts:
    - payment.default.svc.cluster.local
  http:
    - route:
        - destination:
            host: payment.default.svc.cluster.local
      timeout: 10s
      retries:
        attempts: 3
        perTryTimeout: 3s
        # Retry on these conditions
        retryOn: 5xx,reset,connect-failure,refused-stream,retriable-4xx
        # Retry only on idempotent methods
        retryRemoteLocalities: true
```

### mTLS PeerAuthentication

```yaml
# Namespace-wide STRICT mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Mesh-wide mTLS (apply to istio-system)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: mesh-mtls
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
# Workload-specific PERMISSIVE (migration)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-service
  namespace: default
spec:
  selector:
    matchLabels:
      app: legacy-app
  mtls:
    mode: PERMISSIVE # Accept both mTLS and plaintext
  # Port-level override
  portLevelMtls:
    8080:
      mode: DISABLE # Health check port
---
# Verify mTLS status
# istioctl authn tls-check <pod-name>.<namespace> <service-name>.<namespace>.svc.cluster.local
```

### AuthorizationPolicy for RBAC

```yaml
# Default deny all
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec: {} # Empty spec denies all requests
---
# Allow specific service-to-service communication
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
    # Allow from frontend service
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/frontend"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]
---
# JWT authentication and authorization
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: default
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
    - from:
        - source:
            requestPrincipals: ["*"] # Valid JWT required
      when:
        - key: request.auth.claims[role]
          values: ["admin", "user"]
---
# IP-based allow list
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-internal-ips
  namespace: default
spec:
  selector:
    matchLabels:
      app: admin-panel
  action: ALLOW
  rules:
    - from:
        - source:
            ipBlocks: ["10.0.0.0/8", "172.16.0.0/12"]
---
# Method and path-based restrictions
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: read-only-access
  namespace: default
spec:
  selector:
    matchLabels:
      app: database-api
  action: ALLOW
  rules:
    - to:
        - operation:
            methods: ["GET", "HEAD"]
  # DENY takes precedence over ALLOW
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-delete
  namespace: default
spec:
  selector:
    matchLabels:
      app: database-api
  action: DENY
  rules:
    - to:
        - operation:
            methods: ["DELETE"]
```

### Sidecar Resource for Egress Control

```yaml
# Default sidecar for namespace (restrict egress)
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default-sidecar
  namespace: production
spec:
  # Apply to all workloads in namespace
  egress:
    # Allow access to services in same namespace
    - hosts:
        - "./*"
    # Allow access to istio-system
    - hosts:
        - "istio-system/*"
    # Allow specific external services
    - hosts:
        - "*/external-api.external.svc.cluster.local"
---
# Workload-specific sidecar
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: frontend-sidecar
  namespace: default
spec:
  workloadSelector:
    labels:
      app: frontend
  ingress:
    - port:
        number: 8080
        protocol: HTTP
        name: http
      defaultEndpoint: 127.0.0.1:8080
  egress:
    # Only allow access to backend service
    - hosts:
        - "./backend.default.svc.cluster.local"
    # Allow access to external API
    - hosts:
        - "*/api.external.com"
---
# Optimize sidecar for external service access
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-api
  namespace: default
spec:
  hosts:
    - api.external.com
  ports:
    - number: 443
      name: https
      protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
---
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: external-egress
  namespace: default
spec:
  workloadSelector:
    labels:
      app: worker
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY # Only allow registered ServiceEntry
  egress:
    - hosts:
        - "*/api.external.com"
```

## Advanced Patterns

### Fault Injection for Testing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: fault-injection
  namespace: default
spec:
  hosts:
    - ratings.default.svc.cluster.local
  http:
    - match:
        - headers:
            x-test:
              exact: "chaos"
      fault:
        # Inject 5 second delay for 50% of requests
        delay:
          percentage:
            value: 50.0
          fixedDelay: 5s
        # Abort 10% of requests with HTTP 500
        abort:
          percentage:
            value: 10.0
          httpStatus: 500
      route:
        - destination:
            host: ratings.default.svc.cluster.local
    - route:
        - destination:
            host: ratings.default.svc.cluster.local
```

### Multi-Cluster Service Mesh

```yaml
# Primary cluster configuration
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: primary-cluster
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: primary
      network: network1
---
# Remote cluster configuration
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: remote-cluster
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: remote
      network: network2
      remotePilotAddress: istiod.istio-system.svc.cluster.local
```

### Locality-Based Load Balancing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: locality-lb
  namespace: default
spec:
  host: service.default.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        # Prefer same region/zone
        distribute:
          - from: us-west/zone1/*
            to:
              "us-west/zone1/*": 80
              "us-west/zone2/*": 20
        # Failover configuration
        failover:
          - from: us-west
            to: us-east
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

## Troubleshooting Commands

```bash
# Check Istio installation
istioctl verify-install

# Analyze configuration issues
istioctl analyze --all-namespaces

# Inspect proxy configuration
istioctl proxy-config cluster <pod-name>.<namespace>
istioctl proxy-config route <pod-name>.<namespace>
istioctl proxy-config listener <pod-name>.<namespace>
istioctl proxy-config endpoint <pod-name>.<namespace>

# Check mTLS status
istioctl authn tls-check <pod-name>.<namespace> <service-name>.<namespace>.svc.cluster.local

# View proxy logs
kubectl logs <pod-name> -c istio-proxy -n <namespace>

# Debug routing
istioctl experimental describe pod <pod-name> -n <namespace>

# Check certificate expiration
istioctl proxy-config secret <pod-name>.<namespace> -o json | jq '.dynamicActiveSecrets[0].secret.tlsCertificate.certificateChain.inlineBytes' -r | base64 -d | openssl x509 -text -noout

# Test traffic routing
kubectl exec <pod-name> -c istio-proxy -- curl -v http://service:port/path

# Export proxy configuration for debugging
istioctl proxy-config all <pod-name>.<namespace> -o json > proxy-config.json
```

## Performance Tuning

### Resource Requests and Limits

```yaml
# Sidecar proxy resources
apiVersion: v1
kind: Namespace
metadata:
  name: production
  annotations:
    # Set default sidecar resources
    sidecar.istio.io/proxyCPU: "100m"
    sidecar.istio.io/proxyCPULimit: "2000m"
    sidecar.istio.io/proxyMemory: "128Mi"
    sidecar.istio.io/proxyMemoryLimit: "1024Mi"
```

### Control Plane Tuning

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    # Reduce config push time
    defaultConfig:
      holdApplicationUntilProxyStarts: true
      proxyMetadata:
        ISTIO_META_DNS_CAPTURE: "true"
        ISTIO_META_DNS_AUTO_ALLOCATE: "true"
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        env:
          - name: PILOT_PUSH_THROTTLE
            value: "100"
          - name: PILOT_ENABLE_WORKLOAD_ENTRY_HEALTH_CHECKS
            value: "true"
```

## Security Hardening

### Disable Privileged Containers

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    defaultConfig:
      # Run as non-root
      runAsUser: 1337
      runAsGroup: 1337
      # Drop all capabilities
      securityContext:
        capabilities:
          drop:
            - ALL
        readOnlyRootFilesystem: true
```

### Egress Traffic Control

```yaml
# Block all egress by default
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    outboundTrafficPolicy:
      mode: REGISTRY_ONLY # Only allow registered ServiceEntry
```

## Migration Strategy

### Phase 1: Install Istio (No Injection)

```bash
istioctl install --set profile=default
# Don't enable automatic injection yet
```

### Phase 2: Enable Injection Per Workload

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    metadata:
      annotations:
        sidecar.istio.io/inject: "true"
```

### Phase 3: Enable PERMISSIVE mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: PERMISSIVE
```

### Phase 4: Verify All Services Use mTLS

```bash
# Check each service
for pod in $(kubectl get pods -n production -o name); do
  istioctl authn tls-check $pod
done
```

### Phase 5: Enable STRICT mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

## Additional Resources

- [Istio Documentation](https://istio.io/latest/docs/)
- [Istio Best Practices](https://istio.io/latest/docs/ops/best-practices/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs)
- [Service Mesh Patterns](https://www.oreilly.com/library/view/istio-up-and/9781492043775/)
