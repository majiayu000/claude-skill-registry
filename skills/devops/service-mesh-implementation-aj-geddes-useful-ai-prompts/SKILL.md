---
name: service-mesh-implementation
description: Implement service mesh (Istio, Linkerd) for service-to-service communication, traffic management, security, and observability.
---

# Service Mesh Implementation

## Overview

Deploy and configure a service mesh to manage microservice communication, enable advanced traffic management, implement security policies, and provide comprehensive observability across distributed systems.

## When to Use

- Microservice communication management
- Cross-cutting security policies
- Traffic splitting and canary deployments
- Service-to-service authentication
- Request routing and retries
- Distributed tracing integration
- Circuit breaker patterns
- Mutual TLS between services

## Implementation Examples

### 1. **Istio Core Setup**

```yaml
# istio-setup.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: istio-system
  labels:
    istio-injection: enabled

---
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-config
  namespace: istio-system
spec:
  profile: production
  revision: "1-13"

  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2048Mi
          limits:
            cpu: 2000m
            memory: 4096Mi
        replicaCount: 3

    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 2000m
              memory: 1024Mi
          service:
            type: LoadBalancer
            ports:
              - port: 80
                targetPort: 8080
                name: http2
              - port: 443
                targetPort: 8443
                name: https

    egressGateways:
      - name: istio-egressgateway
        enabled: true

  meshConfig:
    enableAutoMTLS: true
    outboundTrafficPolicy:
      mode: ALLOW_ANY

    accessLogFile: /dev/stdout
    accessLogFormat: |
      [%START_TIME%] "%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%"
      %RESPONSE_CODE% %RESPONSE_FLAGS% %BYTES_RECEIVED% %BYTES_SENT%
      "%DURATION%" "%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%"

---
# Enable sidecar injection for namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio-injection: enabled
```

### 2. **Virtual Service and Destination Rule**

```yaml
# virtual-service-config.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-service
  namespace: production
spec:
  hosts:
    - api-service
    - api-service.production.svc.cluster.local
  http:
    # Canary: 10% to v2, 90% to v1
    - match:
        - uri:
            prefix: /api/v1
      route:
        - destination:
            host: api-service
            subset: v1
          weight: 90
        - destination:
            host: api-service
            subset: v2
          weight: 10
      timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s

    # API v2 for testing
    - match:
        - headers:
            user-agent:
              regex: ".*Chrome.*"
      route:
        - destination:
            host: api-service
            subset: v2
      timeout: 30s

    # Default route
    - route:
        - destination:
            host: api-service
            subset: v1
          weight: 100
      timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-service
  namespace: production
spec:
  host: api-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
        maxRequestsPerConnection: 2
        h2UpgradePolicy: UPGRADE

    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minRequestVolume: 10

  subsets:
    - name: v1
      labels:
        version: v1
      trafficPolicy:
        connectionPool:
          http:
            http1MaxPendingRequests: 50

    - name: v2
      labels:
        version: v2
      trafficPolicy:
        connectionPool:
          http:
            http1MaxPendingRequests: 100
```

### 3. **Security Policies**

```yaml
# security-config.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT  # Enforce mTLS for all workloads

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/web-service"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/*"]

    # Allow health checks
    - to:
        - operation:
            methods: ["GET"]
            paths: ["/health"]

---
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: api-service-authn
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  jwtRules:
    - issuer: https://auth.mycompany.com
      jwksUri: https://auth.mycompany.com/.well-known/jwks.json
      audiences: api-service
```

### 4. **Observability Configuration**

```yaml
# observability-config.yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: custom-logging
  namespace: production
spec:
  metrics:
    - providers:
        - name: prometheus
      dimensions:
        - request.path
        - response.code
        - destination.service.name

---
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: custom-tracing
  namespace: production
spec:
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 100.0
      useRequestIdForTraceSampling: true

---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-dashboard
  namespace: monitoring
data:
  istio-mesh.json: |
    {
      "dashboard": {
        "title": "Istio Mesh",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(istio_requests_total[5m])"
              }
            ]
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "rate(istio_requests_total{response_code=~\"5..\"}[5m])"
              }
            ]
          },
          {
            "title": "Latency P95",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(istio_request_duration_milliseconds_bucket[5m]))"
              }
            ]
          }
        ]
      }
    }
```

### 5. **Service Mesh Deployment Script**

```bash
#!/bin/bash
# deploy-istio.sh - Install and configure Istio

set -euo pipefail

VERSION="1.13.0"
NAMESPACE="istio-system"

echo "Installing Istio $VERSION..."

# Download Istio
if [ ! -d "istio-$VERSION" ]; then
    echo "Downloading Istio..."
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=$VERSION sh -
fi

cd "istio-$VERSION"

# Add istioctl to PATH
export PATH=$PWD/bin:$PATH

# Verify cluster
echo "Verifying cluster compatibility..."
istioctl analyze

# Install Istio
echo "Installing Istio on cluster..."
istioctl install --set profile=production -y

# Verify installation
echo "Verifying installation..."
kubectl get ns $NAMESPACE
kubectl get pods -n $NAMESPACE

# Label namespaces for sidecar injection
echo "Configuring sidecar injection..."
kubectl label namespace production istio-injection=enabled --overwrite

# Wait for sidecars
echo "Waiting for sidecars to be injected..."
kubectl rollout restart deployment -n production

echo "Istio installation complete!"

# Show status
istioctl version
```

## Service Mesh Patterns

### Traffic Management
- **Canary Deployments**: Gradually shift traffic
- **A/B Testing**: Route based on headers
- **Circuit Breaking**: Fail fast with outlier detection
- **Rate Limiting**: Control request flow

### Security
- **mTLS**: Mutual authentication
- **Authorization Policies**: Fine-grained access control
- **JWT Validation**: Token verification
- **Encryption**: Automatic in-transit encryption

## Best Practices

### ✅ DO
- Enable mTLS for all workloads
- Implement proper authorization policies
- Use virtual services for traffic management
- Enable distributed tracing
- Monitor resource usage (CPU, memory)
- Use appropriate sampling rates for tracing
- Implement circuit breakers
- Use namespace isolation

### ❌ DON'T
- Disable mTLS in production
- Allow permissive traffic policies
- Ignore observability setup
- Deploy without resource requests/limits
- Skip sidecar injection validation
- Use 100% sampling in high-traffic systems
- Mix service versions without proper routing
- Neglect authorization policies

## Resources

- [Istio Official Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2/overview/)
- [Service Mesh Interface (SMI)](https://smi-spec.io/)
- [Istio Security Best Practices](https://istio.io/latest/docs/concepts/security/)
