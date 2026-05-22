---
name: service-mesh-integrator
description: Configure service mesh solutions including Istio, Linkerd, and Consul for traffic management, security, and observability in microservices. Activates for service mesh setup, mTLS, traffic routing, and mesh configuration.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Service Mesh Integrator

Configure enterprise service mesh for secure, observable microservices communication.

## When to Use

- Setting up Istio, Linkerd, or Consul service mesh
- Implementing mTLS between services
- Configuring traffic routing and load balancing
- Setting up canary deployments
- Implementing circuit breakers and retries
- Configuring observability (metrics, tracing, logging)

## Istio Configuration

```yaml
# Install Istio
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-control-plane
spec:
  profile: production
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2Gi
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          replicas: 3

---
# Virtual Service for traffic routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
    - user-service
  http:
    - match:
        - headers:
            version:
              exact: v2
      route:
        - destination:
            host: user-service
            subset: v2
          weight: 100
    - route:
        - destination:
            host: user-service
            subset: v1
          weight: 90
        - destination:
            host: user-service
            subset: v2
          weight: 10

---
# Destination Rule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
      trafficPolicy:
        loadBalancer:
          simple: ROUND_ROBIN
```

## mTLS Configuration

```yaml
# Enable mTLS globally
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT

---
# Authorization policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: user-service-authz
spec:
  selector:
    matchLabels:
      app: user-service
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/default/sa/order-service
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/users/*"]
```

## Best Practices

- ✅ Enable mTLS for all service-to-service communication
- ✅ Use traffic splitting for canary deployments
- ✅ Configure circuit breakers and retries
- ✅ Implement rate limiting per service
- ✅ Use observability features (tracing, metrics)
- ✅ Regular security policy audits

## Related Skills

- `microservices-orchestrator`
- `distributed-tracing-setup`
- `sla-monitor-generator`
