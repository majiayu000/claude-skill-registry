---
name: k8s-docker-registry-cache-bypass
description: |
  Fix for Kubernetes pods running old Docker images despite pushing new versions.
  Use when: (1) kubectl shows correct image tag but container runs old code,
  (2) Local registry mirror caches stale images, (3) imagePullPolicy: Always
  doesn't force fresh pulls, (4) containerd config has mirror that intercepts pulls.
  Solution: Use image digest instead of tag to bypass cache entirely.
author: Claude Code
version: 1.0.0
date: 2025-01-31
---

# Kubernetes Docker Registry Cache Bypass

## Problem
Kubernetes pods continue running old Docker images even after pushing new versions with
the same tag (e.g., `:latest`). This happens when a local registry mirror caches images
and serves stale versions, ignoring `imagePullPolicy: Always`.

## Context / Trigger Conditions
- Pod is running but application code is outdated
- `docker push` succeeded with new layers
- `kubectl describe pod` shows correct image tag
- Cluster has a local registry mirror configured (e.g., in containerd config)
- `imagePullPolicy: Always` doesn't fix the issue
- Nodes configured with registry mirrors at `/etc/containerd/certs.d/` or similar

## Solution

### 1. Get the image digest after pushing
```bash
docker push viktorbarzin/myimage:latest
# Output includes: latest: digest: sha256:abc123... size: 856
```

### 2. Use digest instead of tag in deployment
```hcl
# Terraform
container {
  # Use digest to bypass local registry cache
  image             = "docker.io/viktorbarzin/myimage@sha256:abc123..."
  image_pull_policy = "Always"
  name              = "myimage"
}
```

```yaml
# Kubernetes YAML
containers:
  - name: myimage
    image: docker.io/viktorbarzin/myimage@sha256:abc123...
    imagePullPolicy: Always
```

### 3. Apply and restart
```bash
terraform apply -target=module.kubernetes_cluster.module.myservice
kubectl rollout restart deployment/myservice -n mynamespace
```

## Why This Works
- Registry mirrors match by tag, not digest
- When you specify a digest, the node must fetch that exact manifest
- The mirror may not have the digest cached, forcing a pull from upstream
- Even if cached, the digest guarantees the exact image version

## Verification
```bash
# Check the pod is using the new image
kubectl get pod -n mynamespace -o jsonpath='{.items[*].spec.containers[*].image}'

# Verify application behavior reflects new code
kubectl exec -n mynamespace deploy/myservice -- <verification-command>
```

## Example

Before (problematic):
```hcl
image = "docker.io/viktorbarzin/audiblez-web:latest"
```

After (fixed):
```hcl
image = "docker.io/viktorbarzin/audiblez-web@sha256:4d0e2c839555e2229bc91a0b1273569bac88529e8b3c3cadad3c3cf9d865fa29"
```

## Notes
- You must update the digest each time you push a new image
- Consider automating digest extraction in CI/CD pipelines
- This is a workaround; ideally fix the registry mirror configuration
- To find your registry mirror config: `cat /etc/containerd/config.toml` on nodes
- Common mirror locations: `/etc/containerd/certs.d/docker.io/hosts.toml`

## Diagnosing Registry Mirror Issues
```bash
# On a k8s node, check containerd config
cat /etc/containerd/config.toml | grep -A5 mirrors

# Check if mirror is intercepting
crictl pull docker.io/library/alpine:latest --debug 2>&1 | grep -i mirror

# List cached images on node
crictl images | grep myimage
```

## References
- [Kubernetes imagePullPolicy documentation](https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy)
- [containerd registry configuration](https://github.com/containerd/containerd/blob/main/docs/hosts.md)
