---
name: istio
description: Istio service mesh for Kubernetes. Use for service networking.
---

# Istio

Istio is a Service Mesh. It adds observability, security (mTLS), and traffic control to microservices. 2025 sees the rise of **Ambient Mesh**, removing the heavy sidecar requirement.

## When to Use

- **Zero Trust**: Automatic mTLS between all services without code changes.
- **Traffic Splitting**: Canary deployments (send 1% of traffic to v2).
- **Observability**: Golden metrics (Request rate, Error rate, Latency) for every service automatically.

## Core Concepts

### Sidecar Mode (Classic)

Injects an Envoy proxy container into every Pod. Captures all traffic. High resource usage.

### Ambient Mode (2025)

Uses a per-node layer 4 proxy (`ztunnel`) and optional per-service layer 7 proxies (`waypoint`). Reduced cost and complexity.

### VirtualService / DestinationRule

CRDs to configure routing and policies.

## Best Practices (2025)

**Do**:

- **Use Ambient Mesh**: If starting new, Ambient checks most boxes with less overhead.
- **Use Strict mTLS**: Enforce authenticated communication everywhere.
- **Use Gateway API**: Istio fully supports the K8s Gateway API standard.

**Don't**:

- **Don't use for simple apps**: If you just need Ingress, use an Ingress Controller. Istio is for complex service-to-service communication.

## References

- [Istio Documentation](https://istio.io/)
