---
name: generate-helm-chart
description: Generate Helm chart for Kubernetes deployment
argument-hint: "<service-name> [--with-ingress] [--with-hpa]"
tags: [codegen, helm, kubernetes, deploy]
user-invocable: true
---

# Generate Helm Chart

Generate a Kubernetes Helm chart with deployment, service, ingress, and HPA.

## What To Do

1. **Create chart structure**:
   ```
   deploy/helm/{service}/
     Chart.yaml
     values.yaml
     values.production.yaml
     templates/
       deployment.yaml
       service.yaml
       ingress.yaml    (if --with-ingress)
       hpa.yaml        (if --with-hpa)
       configmap.yaml
       secrets.yaml
   ```

2. **Configure values.yaml** with sensible defaults
3. **Add health checks** (liveness, readiness, startup probes)
4. **Add resource limits** (CPU, memory)

## Arguments
- `<service-name>`: Kubernetes service name
- `--with-ingress`: Add ingress template
- `--with-hpa`: Add horizontal pod autoscaler