---
name: creating-kubernetes-deployments
description: Generate production-ready Kubernetes deployment manifests, services, and ingress configurations with health checks, auto-scaling, resource limits, and TLS termination. Use when creating Kubernetes deployments, generating k8s manifests, deploying apps to Kubernetes clusters, or setting up container orchestration with services and ingress.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(kubectl:*)
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# Creating Kubernetes Deployments

## When to Use This Skill

Use this skill when:

- Creating Kubernetes deployment manifests
- Deploying applications to Kubernetes clusters
- Configuring container orchestration
- Setting up Kubernetes services and ingress
- Managing Kubernetes resources and configurations
- Implementing Kubernetes best practices
- Troubleshooting Kubernetes deployments

## Overview

This skill provides automated assistance for the described functionality.

## Prerequisites

Before using this skill, ensure:

- Kubernetes cluster is accessible and kubectl is configured
- Container image is built and pushed to registry
- Understanding of application resource requirements
- Namespace exists or will be created
- Ingress controller is installed (if using ingress)
- TLS certificates are available (if using HTTPS)

## Instructions

1. **Gather Requirements**: Application name, image, replicas, ports, environment
2. **Create Deployment**: Generate YAML with container spec and resource limits
3. **Add Health Checks**: Configure liveness and readiness probes
4. **Define Service**: Create ClusterIP, NodePort, or LoadBalancer service
5. **Configure Ingress**: Set up routing rules and TLS termination
6. **Add ConfigMaps/Secrets**: Externalize configuration and sensitive data
7. **Enable Auto-scaling**: Create HorizontalPodAutoscaler if needed
8. **Apply Manifests**: Use kubectl apply to deploy resources

## Output

**Deployment Manifest:**

```yaml
# {baseDir}/k8s/deployment.yaml

## Error Handling

See `{baseDir}/references/errors.md` for comprehensive error handling.

## Examples

See `{baseDir}/references/examples.md` for detailed examples.

## Resources

- Kubernetes documentation: https://kubernetes.io/docs/
- kubectl reference: https://kubernetes.io/docs/reference/kubectl/
- Deployment best practices: https://kubernetes.io/docs/concepts/workloads/
- Example manifests in {baseDir}/k8s-examples/

## How to use this skill

Refer to the instructions above or standard agent usage for this skill type.
```
