---
name: istio:ambient-waypoint
description: Configure L7 AuthorizationPolicy in Istio Ambient mode using waypoint proxies
---

# Istio Ambient Waypoint Authorization

Configure L7 AuthorizationPolicy in Istio Ambient mode using waypoint proxies.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Waypoint Gateway Configuration](#waypoint-gateway-configuration)
- [Service Configuration](#service-configuration)
- [AuthorizationPolicy with targetRefs](#authorizationpolicy-with-targetrefs)
- [Complete Example](#complete-example)
- [Troubleshooting](#troubleshooting)

## Overview

In Istio Ambient mode:
- **ztunnel**: Handles L4 traffic (TCP, mTLS) - cannot evaluate HTTP paths
- **Waypoint**: Handles L7 traffic (HTTP) - can evaluate paths, methods, headers

To enforce path-based authorization, you need a waypoint proxy.

## Architecture

```
Client -> ztunnel (L4 mTLS) -> Waypoint (L7 HTTP) -> Service
                                    |
                              AuthorizationPolicy
                              (evaluates path, method)
```

## Waypoint Gateway Configuration

Create a waypoint for the service that needs L7 authorization:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: mlflow-waypoint
  namespace: kagenti-system
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
```

**Key points**:
- `istio.io/waypoint-for: service` - This waypoint handles service traffic
- `gatewayClassName: istio-waypoint` - Uses the Istio waypoint class
- Port 15008 with HBONE protocol is standard for waypoints

## Service Configuration

Label the service to use the waypoint:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mlflow
  namespace: kagenti-system
  labels:
    istio.io/use-waypoint: mlflow-waypoint
spec:
  ports:
    - port: 5000
  selector:
    app: mlflow
```

## AuthorizationPolicy with targetRefs

In Ambient mode, use `targetRefs` instead of `selector`:

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: mlflow-traces-from-otel
  namespace: kagenti-system
spec:
  targetRefs:
    - kind: Service
      group: ""
      name: mlflow
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/kagenti-system/sa/otel-collector"
      to:
        - operation:
            methods: ["POST"]
            paths: ["/v1/traces"]
```

**Key points**:
- `targetRefs` points to the Service, not a selector
- `group: ""` is required for core Kubernetes resources
- `principals` uses SPIFFE ID format

## Multiple Rules Example

Allow different sources for different paths:

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: mlflow-api-access
  namespace: kagenti-system
spec:
  targetRefs:
    - kind: Service
      group: ""
      name: mlflow
  action: ALLOW
  rules:
    # OTEL collector can POST traces
    - from:
        - source:
            principals:
              - "cluster.local/ns/kagenti-system/sa/otel-collector"
      to:
        - operation:
            methods: ["POST"]
            paths: ["/v1/traces"]

    # UI can access all endpoints
    - from:
        - source:
            principals:
              - "cluster.local/ns/kagenti-system/sa/kagenti-ui"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/*"]
```

## Complete Example

Full configuration for MLflow with OAuth2 and Istio authorization:

```yaml
---
# Waypoint Gateway
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: mlflow-waypoint
  namespace: kagenti-system
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
---
# Service with waypoint label
apiVersion: v1
kind: Service
metadata:
  name: mlflow
  namespace: kagenti-system
  labels:
    istio.io/use-waypoint: mlflow-waypoint
spec:
  ports:
    - port: 5000
  selector:
    app: mlflow
---
# Authorization Policy
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: mlflow-traces-from-otel
  namespace: kagenti-system
spec:
  targetRefs:
    - kind: Service
      group: ""
      name: mlflow
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/kagenti-system/sa/otel-collector"
      to:
        - operation:
            methods: ["POST"]
            paths: ["/v1/traces"]
```

## Troubleshooting

### Authorization Denied

1. Check waypoint is running:
```bash
kubectl get pods -n kagenti-system -l gateway.networking.k8s.io/gateway-name=mlflow-waypoint
```

2. Check service has waypoint label:
```bash
kubectl get svc mlflow -n kagenti-system -o yaml | grep waypoint
```

3. Check principal format:
```bash
istioctl proxy-config secret <pod> -n kagenti-system
```

### Waypoint Not Processing Traffic

1. Verify ambient mode is enabled:
```bash
kubectl get namespace kagenti-system -o yaml | grep ambient
```

2. Check ztunnel logs:
```bash
kubectl logs -n istio-system -l app=ztunnel
```

### Policy Not Evaluated

1. Ensure `targetRefs` is used (not `selector`)
2. Verify `group: ""` for core resources
3. Check policy is in same namespace as service

## Sidecar vs Ambient

| Feature | Sidecar Mode | Ambient Mode |
|---------|--------------|--------------|
| AuthorizationPolicy target | `selector` | `targetRefs` |
| L7 processing | Automatic | Requires waypoint |
| Resource overhead | Per-pod sidecar | Shared waypoint |

## Related Skills

- `auth:keycloak-confidential-client`
- `auth:otel-oauth2-exporter`
