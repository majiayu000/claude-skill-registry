---
name: containerd-multi-registry-pull-through-cache
description: |
  Set up pull-through caches for multiple container registries (ghcr.io, quay.io,
  registry.k8s.io, reg.kyverno.io) using Docker Registry v2 instances. Use when:
  (1) ImagePullBackOff for non-Docker-Hub images routed through a wildcard mirror,
  (2) containerd has deprecated `registry.mirrors."*"` catching all image pulls,
  (3) need to add pull-through cache for a new upstream registry,
  (4) `mirrors` cannot be set when `config_path` is provided error in containerd,
  (5) containerd 1.6.x vs 1.7.x config_path compatibility issues.
  Docker Registry v2 can only proxy ONE upstream per instance, so multiple
  containers are needed for multiple registries.
author: Claude Code
version: 1.0.0
date: 2026-02-14
---

# Containerd Multi-Registry Pull-Through Cache

## Problem

Docker Registry v2 can only proxy **one upstream registry per instance**. A common
misconfiguration is using a containerd wildcard mirror (`registry.mirrors."*"`) pointing
to a single Docker Hub proxy, which breaks pulls from ghcr.io, quay.io, registry.k8s.io,
and other registries — they get routed to the Docker Hub proxy which can't serve them,
causing `ImagePullBackOff`.

## Context / Trigger Conditions

- `ImagePullBackOff` for images from ghcr.io, quay.io, registry.k8s.io, or other non-Docker-Hub registries
- Containerd config has deprecated `[plugins."io.containerd.grpc.v1.cri".registry.mirrors."*"]`
- Error: `failed to load plugin io.containerd.grpc.v1.cri: invalid plugin config: mirrors cannot be set when config_path is provided`
- Need to migrate from deprecated wildcard mirrors to modern `config_path` approach

## Solution

### 1. Run one Registry v2 container per upstream

Each upstream needs its own Docker Registry v2 instance on a different port:

| Port | Registry | Container Name |
|------|----------|---------------|
| 5000 | docker.io | registry |
| 5010 | ghcr.io | registry-ghcr |
| 5020 | quay.io | registry-quay |
| 5030 | registry.k8s.io | registry-k8s |
| 5040 | reg.kyverno.io | registry-kyverno |

Config for non-Docker-Hub proxies (no auth needed — they're public):

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

### 2. Replace deprecated wildcard mirror with `config_path`

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

### 3. Critical: `config_path` and `mirrors` cannot coexist

Containerd will **refuse to start the CRI plugin** if both `config_path` and any
`mirrors` entries exist in `config.toml`. You must remove ALL `mirrors` entries
(including the `[plugins."...registry.mirrors"]` parent section) before setting
`config_path`.

This is especially dangerous on containerd 1.6.x (used on older nodes like k8s-master)
where the config format is slightly different. If unsure, either:
- Don't use config_path on that node (skip the pull-through cache)
- Remove the entire `mirrors` section first, then add `config_path`

### 4. Static IP for registry VM

If the registry VM uses DHCP and gets the wrong IP, all mirrors break. Use static IP
via cloud-init `ipconfig0 = "ip=10.0.20.10/24,gw=10.0.20.1"` instead of DHCP.

## Verification

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

## Notes

- **Fallback behavior**: If the local mirror is unreachable, containerd falls through to
  direct pull from the upstream `server` URL. This provides graceful degradation.
- **GC crontabs**: Add weekly garbage collection for each registry container, staggered
  to avoid I/O spikes.
- **Hourly restart**: Registry v2 has known memory leak issues; hourly restart mitigates.
- **Cache is ephemeral**: VM recreation clears the cache. Images re-cache on demand.

See also: `k8s-docker-registry-cache-bypass` (for stale cached image issues)
