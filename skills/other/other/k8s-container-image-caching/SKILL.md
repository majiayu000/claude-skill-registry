---
name: k8s-container-image-caching
description: |
  Set up and troubleshoot container image pull-through caches in Kubernetes. Use when:
  (1) ImagePullBackOff for non-Docker-Hub images routed through a wildcard mirror,
  (2) containerd has deprecated `registry.mirrors."*"` catching all image pulls,
  (3) need to add pull-through cache for a new upstream registry,
  (4) `mirrors` cannot be set when `config_path` is provided error in containerd,
  (5) containerd 1.6.x vs 1.7.x config_path compatibility issues,
  (6) kubectl shows correct image tag but container runs old code,
  (7) local registry mirror caches stale images,
  (8) imagePullPolicy: Always doesn't force fresh pulls,
  (9) containerd config has mirror that intercepts pulls serving stale images.
  Covers multi-registry pull-through cache setup (Docker Registry v2) and cache bypass
  via image digest pinning.
author: Claude Code
version: 1.0.0
date: 2026-02-22
---

# Kubernetes Container Image Caching

## Pull-Through Cache Setup

### Problem

Docker Registry v2 can only proxy **one upstream registry per instance**. A common
misconfiguration is using a containerd wildcard mirror (`registry.mirrors."*"`) pointing
to a single Docker Hub proxy, which breaks pulls from ghcr.io, quay.io, registry.k8s.io,
and other registries -- they get routed to the Docker Hub proxy which can't serve them,
causing `ImagePullBackOff`.

### Context / Trigger Conditions

- `ImagePullBackOff` for images from ghcr.io, quay.io, registry.k8s.io, or other non-Docker-Hub registries
- Containerd config has deprecated `[plugins."io.containerd.grpc.v1.cri".registry.mirrors."*"]`
- Error: `failed to load plugin io.containerd.grpc.v1.cri: invalid plugin config: mirrors cannot be set when config_path is provided`
- Need to migrate from deprecated wildcard mirrors to modern `config_path` approach

### Solution

#### 1. Run one Registry v2 container per upstream

Each upstream needs its own Docker Registry v2 instance on a different port:

| Port | Registry | Container Name |
|------|----------|---------------|
| 5000 | docker.io | registry |
| 5010 | ghcr.io | registry-ghcr |
| 5020 | quay.io | registry-quay |
| 5030 | registry.k8s.io | registry-k8s |
| 5040 | reg.kyverno.io | registry-kyverno |

Config for non-Docker-Hub proxies (no auth needed -- they're public):

```yaml
version: 0.1
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
proxy:
  remoteurl: https://ghcr.io  # change per registry
```

```bash
docker run -p 5010:5000 -d --restart always --name registry-ghcr \
  -v /etc/docker-registry/ghcr/config.yml:/etc/docker/registry/config.yml registry:2
```

#### 2. Replace deprecated wildcard mirror with `config_path`

Instead of:
```toml
# DEPRECATED - breaks non-Docker-Hub registries
[plugins."io.containerd.grpc.v1.cri".registry.mirrors."*"]
  endpoint = ["http://10.0.20.10:5000"]
```

Use the modern `config_path` approach:
```toml
[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"
```

Then create per-registry `hosts.toml` files:
```bash
mkdir -p /etc/containerd/certs.d/docker.io
cat > /etc/containerd/certs.d/docker.io/hosts.toml <<'EOF'
server = "https://registry-1.docker.io"

[host."http://10.0.20.10:5000"]
  capabilities = ["pull", "resolve"]
EOF
```

Registries without a `hosts.toml` entry **fall through to direct pull** (no breakage).

#### 3. Critical: `config_path` and `mirrors` cannot coexist

Containerd will **refuse to start the CRI plugin** if both `config_path` and any
`mirrors` entries exist in `config.toml`. You must remove ALL `mirrors` entries
(including the `[plugins."...registry.mirrors"]` parent section) before setting
`config_path`.

This is especially dangerous on containerd 1.6.x (used on older nodes like k8s-master)
where the config format is slightly different. If unsure, either:
- Don't use config_path on that node (skip the pull-through cache)
- Remove the entire `mirrors` section first, then add `config_path`

#### 4. Static IP for registry VM

If the registry VM uses DHCP and gets the wrong IP, all mirrors break. Use static IP
via cloud-init `ipconfig0 = "ip=10.0.20.10/24,gw=10.0.20.1"` instead of DHCP.

### Verification

```bash
# Test each proxy responds
for port in 5000 5010 5020 5030 5040; do
  curl -s http://10.0.20.10:$port/v2/_catalog
done

# Test containerd can pull through cache
crictl pull ghcr.io/some/image:tag

# Check containerd logs for mirror usage
journalctl -u containerd --since "5 minutes ago" | grep -i "mirror\|registry"
```

### Notes

- **Fallback behavior**: If the local mirror is unreachable, containerd falls through to
  direct pull from the upstream `server` URL. This provides graceful degradation.
- **GC crontabs**: Add weekly garbage collection for each registry container, staggered
  to avoid I/O spikes.
- **Hourly restart**: Registry v2 has known memory leak issues; hourly restart mitigates.
- **Cache is ephemeral**: VM recreation clears the cache. Images re-cache on demand.

---

## Cache Bypass / Stale Image Fix

### Problem
Kubernetes pods continue running old Docker images even after pushing new versions with
the same tag (e.g., `:latest`). This happens when a local registry mirror caches images
and serves stale versions, ignoring `imagePullPolicy: Always`.

### Context / Trigger Conditions
- Pod is running but application code is outdated
- `docker push` succeeded with new layers
- `kubectl describe pod` shows correct image tag
- Cluster has a local registry mirror configured (e.g., in containerd config)
- `imagePullPolicy: Always` doesn't fix the issue
- Nodes configured with registry mirrors at `/etc/containerd/certs.d/` or similar

### Solution

#### 1. Get the image digest after pushing
```bash
docker push viktorbarzin/myimage:latest
# Output includes: latest: digest: sha256:abc123... size: 856
```

#### 2. Use digest instead of tag in deployment
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

#### 3. Apply and restart
```bash
terraform apply -target=module.kubernetes_cluster.module.myservice
kubectl rollout restart deployment/myservice -n mynamespace
```

### Why This Works
- Registry mirrors match by tag, not digest
- When you specify a digest, the node must fetch that exact manifest
- The mirror may not have the digest cached, forcing a pull from upstream
- Even if cached, the digest guarantees the exact image version

### Verification
```bash
# Check the pod is using the new image
kubectl get pod -n mynamespace -o jsonpath='{.items[*].spec.containers[*].image}'

# Verify application behavior reflects new code
kubectl exec -n mynamespace deploy/myservice -- <verification-command>
```

### Example

Before (problematic):
```hcl
image = "docker.io/viktorbarzin/audiblez-web:latest"
```

After (fixed):
```hcl
image = "docker.io/viktorbarzin/audiblez-web@sha256:4d0e2c839555e2229bc91a0b1273569bac88529e8b3c3cadad3c3cf9d865fa29"
```

### Notes
- You must update the digest each time you push a new image
- Consider automating digest extraction in CI/CD pipelines
- This is a workaround; ideally fix the registry mirror configuration
- To find your registry mirror config: `cat /etc/containerd/config.toml` on nodes
- Common mirror locations: `/etc/containerd/certs.d/docker.io/hosts.toml`

### Diagnosing Registry Mirror Issues
```bash
# On a k8s node, check containerd config
cat /etc/containerd/config.toml | grep -A5 mirrors

# Check if mirror is intercepting
crictl pull docker.io/library/alpine:latest --debug 2>&1 | grep -i mirror

# List cached images on node
crictl images | grep myimage
```

---

## References

- [Kubernetes imagePullPolicy documentation](https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy)
- [containerd registry configuration](https://github.com/containerd/containerd/blob/main/docs/hosts.md)
