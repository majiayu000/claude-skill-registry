---
name: helm
description: Helm Kubernetes package manager with charts. Use for K8s deployments.
---

# Helm

Helm helps you manage Kubernetes applications via Charts (packages of pre-configured K8s resources). Helm v4 (2025) improves OCI integration and enables server-side apply.

## When to Use

- **Packaging**: Distribute your K8s app to others.
- **Templating**: Manage complexity. One `deployment.yaml` template for Dev, Staging, and Prod.
- **Management**: Easy upgrades/rollbacks (`helm rollback`).

## Quick Start

```bash
# Install a chart
helm install my-release oci://registry-1.docker.io/bitnamicharts/nginx

# Create a chart
helm create my-chart
```

```yaml
# values.yaml
replicaCount: 2
image:
  repository: nginx
  tag: "1.25"
```

## Core Concepts

### Charts

A collection of files that describe a related set of Kubernetes resources.
`Chart.yaml`, `values.yaml`, `templates/`.

### OCI Registries

Helm v4 treats OCI (Docker) registries as first-class citizens. You push Charts to Docker Hub/ECR/GHCR just like container images.

### Release

An instance of a chart running in a cluster.

## Best Practices (2025)

**Do**:

- **Store Charts in OCI**: Push charts to your container registry (`helm push`). Deprecate HTTP chart repositories.
- **Use `helm upgrade --install`**: Idempotent command for CI/CD pipelines.
- **Use `helm lint` & `kubeval`**: Validate templates before deploying.

**Don't**:

- **Don't overuse logic in templates**: If your Go templates look like spaghetti code, consider using a simpler tool (Kustomize) or an Operator.

## References

- [Helm Documentation](https://helm.sh/)
