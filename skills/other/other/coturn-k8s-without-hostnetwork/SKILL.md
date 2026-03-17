---
name: coturn-k8s-without-hostnetwork
description: |
  Deploy coturn (TURN/STUN server) on Kubernetes without hostNetwork by using a
  narrow relay port range and MetalLB LoadBalancer service. Use when: (1) deploying
  a WebRTC relay server on k8s, (2) want coturn to run on any node (not pinned),
  (3) avoiding hostNetwork for better pod scheduling and multi-replica support,
  (4) need TURN for NAT traversal in WebRTC apps (video streaming, conferencing).
  Covers relay port range sizing, MetalLB IP sharing, ephemeral TURN credentials
  via HMAC-SHA1, and pfSense port forwarding.
author: Claude Code
version: 1.0.0
date: 2026-02-21
---

# coturn on Kubernetes Without hostNetwork

## Problem
TURN servers traditionally require hostNetwork because they relay media over a wide
UDP port range (49152-65535). This pins the server to a single node, prevents rolling
updates, and wastes cluster flexibility.

## Context / Trigger Conditions
- Deploying a TURN/STUN server for WebRTC applications on Kubernetes
- Want the TURN pod to be schedulable on any node
- Need to avoid hostNetwork for better availability and scheduling

## Solution

### Key insight: Narrow the relay port range
A home lab with ~20 concurrent WebRTC viewers needs ~40 relay ports (2 per viewer).
Use 100 ports (49152-49252) instead of 16K. This makes it practical to expose via
a K8s LoadBalancer service.

### Terraform module structure

```hcl
locals {
  turn_port = 3478
  min_port  = 49152
  max_port  = 49252  # 100 ports — enough for ~50 concurrent streams
}

resource "kubernetes_deployment" "coturn" {
  spec {
    # No hostNetwork, no nodeSelector — runs anywhere
    template {
      spec {
        container {
          image = "coturn/coturn:latest"
          args  = ["-c", "/etc/turnserver/turnserver.conf"]
          port {
            container_port = 3478
            protocol       = "UDP"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "coturn" {
  metadata {
    annotations = {
      # Share an existing MetalLB IP to avoid consuming a new one
      "metallb.universe.tf/loadBalancerIPs"  = "10.0.20.200"
      "metallb.universe.tf/allow-shared-ip" = "shared"
    }
  }
  spec {
    type = "LoadBalancer"
    # Signaling port
    port {
      name     = "turn-udp"
      port     = 3478
      protocol = "UDP"
    }
    # Relay ports — dynamic block generates 100 port definitions
    dynamic "port" {
      for_each = range(49152, 49253)
      content {
        name        = "relay-${port.value}"
        port        = port.value
        target_port = port.value
        protocol    = "UDP"
      }
    }
  }
}
```

### coturn config (turnserver.conf)

```
listening-port=3478
fingerprint
lt-cred-mech
use-auth-secret
static-auth-secret=YOUR_SECRET_HERE
realm=yourdomain.com
listening-ip=0.0.0.0
min-port=49152
max-port=49252
no-multicast-peers
no-cli
```

### MetalLB IP sharing
To reuse an existing MetalLB IP (e.g., the WireGuard/Shadowsocks shared IP):
1. Add `metallb.universe.tf/allow-shared-ip: shared` to the coturn service
2. The same annotation must exist on all other services sharing that IP
3. **Port conflicts are not allowed** — verify no other service uses 3478 or 49152-49252
4. After changing the IP annotation, **delete and recreate** the service — MetalLB won't reassign IPs on annotation changes alone

### Ephemeral TURN credentials
coturn's `use-auth-secret` mode generates time-limited credentials via HMAC-SHA1:

```javascript
const crypto = require('crypto');
const TURN_SECRET = 'your-shared-secret';

function getTurnCredentials(name = 'user', ttl = 86400) {
  const timestamp = Math.floor(Date.now() / 1000) + ttl;
  const username = `${timestamp}:${name}`;
  const credential = crypto.createHmac('sha1', TURN_SECRET)
    .update(username).digest('base64');
  return { username, credential };
}
```

## Verification

```bash
# STUN binding request (raw UDP probe)
echo -ne '\x00\x01\x00\x00\x21\x12\xa4\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
  | nc -u -w2 <METALLB_IP> 3478 | xxd | head -3
# Response starting with 0101 = successful STUN binding response
```

## Notes
- 100 relay ports supports ~50 concurrent streams (2 ports per stream)
- If you need more, increase `max_port` and add more ports to the service
- coturn auto-detects pod IP — no need to set `relay-ip` or `external-ip` explicitly
- For public access, add NAT port forwards on pfSense for UDP 3478 + 49152-49252
- See also: `pfsense-nat-rule-creation` skill for adding the port forwards
