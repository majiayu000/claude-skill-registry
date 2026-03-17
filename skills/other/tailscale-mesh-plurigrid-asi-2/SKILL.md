---
name: tailscale-mesh
description: "Tailscale mesh VPN for secure peer-to-peer networking. WireGuard-based overlay network with MagicDNS and ACLs."
metadata:
  trit: 0
  version: "1.0.0"
  bundle: networking
---

# Tailscale Mesh Skill

**Trit**: 0 (ERGODIC - mediates network topology)  
**Foundation**: Tailscale + WireGuard + DERP  

## Core Concept

Tailscale creates a mesh VPN:
- WireGuard encryption
- NAT traversal via DERP relays
- MagicDNS for hostname resolution
- ACLs for access control

## Common Commands

```bash
# Status
tailscale status
tailscale netcheck

# Connect/disconnect
tailscale up
tailscale down

# Send files
tailscale file cp file.txt hostname:

# SSH
tailscale ssh hostname

# Funnel (public exposure)
tailscale funnel 8080
```

## ACL Configuration

```jsonc
{
  "acls": [
    {"action": "accept", "src": ["group:dev"], "dst": ["*:*"]},
    {"action": "accept", "src": ["tag:server"], "dst": ["tag:db:5432"]}
  ],
  "tagOwners": {
    "tag:server": ["group:ops"],
    "tag:db": ["group:dba"]
  }
}
```

## GF(3) Integration

```python
def trit_from_connection(conn):
    """Map connection type to GF(3) trit."""
    if conn.type == "direct":
        return 1   # PLUS: optimal path
    elif conn.type == "derp":
        return 0   # ERGODIC: relayed
    else:
        return -1  # MINUS: failed/blocked
```

## Canonical Triads

```
bisimulation-game (-1) ⊗ tailscale-mesh (0) ⊗ localsend-mcp (+1) = 0 ✓
spi-parallel-verify (-1) ⊗ tailscale-mesh (0) ⊗ tailscale-file-transfer (+1) = 0 ✓
```

## See Also

- `tailscale-file-transfer` - File transfer with open games semantics
- `localsend-mcp` - P2P transfer via LocalSend
