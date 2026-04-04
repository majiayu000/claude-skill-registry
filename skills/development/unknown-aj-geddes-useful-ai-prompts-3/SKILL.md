---
name: service-mesh-implementation
description: >
  Implement service mesh (Istio, Linkerd) for service-to-service communication,
  traffic management, security, and observability.
---

# Service Mesh Implementation

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)

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

## Quick Start

Minimal working example:

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
// ... (see reference guides for full implementation)
```

## Reference Guides

Detailed implementations in the `references/` directory:

| Guide | Contents |
|---|---|
| [Istio Core Setup](references/istio-core-setup.md) | Istio Core Setup |
| [Virtual Service and Destination Rule](references/virtual-service-and-destination-rule.md) | Virtual Service and Destination Rule |
| [Security Policies](references/security-policies.md) | Security Policies |
| [Observability Configuration](references/observability-configuration.md) | Observability Configuration |
| [Service Mesh Deployment Script](references/service-mesh-deployment-script.md) | Service Mesh Deployment Script |

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
