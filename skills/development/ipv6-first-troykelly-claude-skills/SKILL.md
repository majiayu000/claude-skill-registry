---
name: ipv6-first
description: IPv6 is THE first-class citizen. All code, tests, documentation, and configurations MUST be IPv6-first. IPv4 MAY be added only for legacy support as a second-class citizen.
allowed-tools: []
model: opus
---

# IPv6-First Development

## Overview

**IPv6 is the present and future of networking. IPv4 is legacy.**

This skill enforces IPv6-first development across all code, tests, documentation, and infrastructure.

**Core principle:** Design for IPv6. Add IPv4 only when legacy compatibility is explicitly required.

**Announce at start:** "I'm following ipv6-first principles - IPv6 is the primary protocol, IPv4 only for legacy support."

## The Rule

| Protocol | Status | Priority |
|----------|--------|----------|
| **IPv6** | First-class citizen | Primary, default, required |
| **IPv4** | Legacy support | Secondary, optional, deprecated path |

## What This Means

### Code

```python
# CORRECT: IPv6 first
def connect(host: str, port: int) -> Connection:
    # Try IPv6 first
    for family in [socket.AF_INET6, socket.AF_INET]:
        try:
            return _connect(host, port, family)
        except OSError:
            continue
    raise ConnectionError(f"Cannot connect to {host}:{port}")

# WRONG: IPv4 assumed
def connect(host: str, port: int) -> Connection:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 only!
    sock.connect((host, port))
```

### Socket Binding

```python
# CORRECT: Dual-stack with IPv6 primary
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)  # Accept IPv4 via mapped addresses
sock.bind(('::', port))

# WRONG: IPv4 only
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', port))
```

### Configuration Files

```yaml
# CORRECT: IPv6 addresses shown first, with examples
server:
  # Primary: IPv6 (recommended)
  bind: "::1"
  # Legacy: IPv4 (for compatibility only)
  # bind: "127.0.0.1"

  # Examples:
  # IPv6: "2001:db8::1", "::1", "::"
  # IPv4 (legacy): "192.168.1.1", "127.0.0.1", "0.0.0.0"

# WRONG: IPv4 as default with no IPv6 mention
server:
  bind: "127.0.0.1"
```

### Documentation

```markdown
## CORRECT: IPv6 first in docs

### Connecting to the Server

Connect using the server's IPv6 address:

    ssh user@2001:db8:85a3::8a2e:370:7334

For legacy IPv4 networks:

    ssh user@192.0.2.1

---

## WRONG: IPv4 assumed

### Connecting to the Server

    ssh user@192.0.2.1
```

### Tests

```python
# CORRECT: Test IPv6 primarily, IPv4 as legacy path
class TestNetworkConnection:
    def test_ipv6_connection(self):
        """Primary test: IPv6 connectivity."""
        conn = connect("::1", 8080)
        assert conn.family == socket.AF_INET6

    def test_ipv4_legacy_connection(self):
        """Legacy support: IPv4 connectivity for older networks."""
        conn = connect("127.0.0.1", 8080)
        assert conn.family == socket.AF_INET

    def test_dual_stack_prefers_ipv6(self):
        """When both available, IPv6 should be preferred."""
        conn = connect("localhost", 8080)
        assert conn.family == socket.AF_INET6

# WRONG: Only testing IPv4
class TestNetworkConnection:
    def test_connection(self):
        conn = connect("127.0.0.1", 8080)
        assert conn.is_connected()
```

### DNS and Hostname Resolution

```python
# CORRECT: Request AAAA records first
def resolve_host(hostname: str) -> list[str]:
    addresses = []

    # IPv6 first (AAAA records)
    try:
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET6):
            addresses.append(info[4][0])
    except socket.gaierror:
        pass

    # IPv4 fallback (A records) for legacy
    try:
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            addresses.append(info[4][0])
    except socket.gaierror:
        pass

    return addresses

# WRONG: Only resolving A records
def resolve_host(hostname: str) -> str:
    return socket.gethostbyname(hostname)  # IPv4 only!
```

### Environment Variables and Defaults

```bash
# CORRECT: IPv6 defaults
export SERVER_HOST="${SERVER_HOST:-::1}"
export BIND_ADDRESS="${BIND_ADDRESS:-::}"

# WRONG: IPv4 defaults
export SERVER_HOST="${SERVER_HOST:-127.0.0.1}"
export BIND_ADDRESS="${BIND_ADDRESS:-0.0.0.0}"
```

### Database Connection Strings

```python
# CORRECT: IPv6 address format (brackets required for port separation)
DATABASE_URL = "postgresql://user:pass@[2001:db8::1]:5432/mydb"

# Also correct: IPv6 localhost
DATABASE_URL = "postgresql://user:pass@[::1]:5432/mydb"

# Legacy IPv4
DATABASE_URL = "postgresql://user:pass@192.168.1.100:5432/mydb"
```

### URL Construction

```python
# CORRECT: Handle IPv6 addresses in URLs (require brackets)
def build_url(host: str, port: int, path: str = "") -> str:
    if ":" in host:  # IPv6 address
        return f"http://[{host}]:{port}{path}"
    return f"http://{host}:{port}{path}"

# Usage:
# build_url("2001:db8::1", 8080, "/api") -> "http://[2001:db8::1]:8080/api"
# build_url("192.168.1.1", 8080, "/api") -> "http://192.168.1.1:8080/api"
```

## Validation Patterns

### IP Address Validation

```python
import ipaddress

def validate_ip(addr: str) -> tuple[str, str]:
    """
    Validate IP address and return (normalized_address, version).
    IPv6 is preferred.
    """
    try:
        ip = ipaddress.ip_address(addr)
        version = "ipv6" if ip.version == 6 else "ipv4-legacy"
        return (str(ip), version)
    except ValueError as e:
        raise ValueError(f"Invalid IP address: {addr}") from e

def is_ipv6(addr: str) -> bool:
    """Check if address is IPv6 (the preferred protocol)."""
    try:
        return ipaddress.ip_address(addr).version == 6
    except ValueError:
        return False
```

### Network Range Validation

```python
# CORRECT: Support both, prefer IPv6
ALLOWED_NETWORKS = [
    # IPv6 networks (primary)
    ipaddress.ip_network("2001:db8::/32"),
    ipaddress.ip_network("fd00::/8"),  # ULA

    # IPv4 networks (legacy support)
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("192.168.0.0/16"),
]
```

## Comments and Naming

When IPv4 is included for legacy support, comment it as such:

```python
# Bind to all interfaces
# IPv6 (primary) - handles both IPv6 and IPv4-mapped addresses
server.bind("::", port)

# Legacy IPv4-only fallback (deprecated path)
if not ipv6_available:
    server.bind("0.0.0.0", port)
```

```python
# Variable naming should reflect the hierarchy
primary_address: str  # IPv6
legacy_address: str   # IPv4 (only when needed)

# NOT:
ipv4_address: str
ipv6_address: str  # This implies equal status
```

## Error Messages

```python
# CORRECT: IPv6-first messaging
raise ConnectionError(
    f"Cannot connect to {host}. "
    f"Ensure the server is accessible via IPv6 (preferred) or IPv4 (legacy)."
)

# WRONG: IPv4 assumed
raise ConnectionError(
    f"Cannot connect to {host}. Check your network connection."
)
```

## When IPv4 is Required

Add IPv4 support **only** when:

1. Interfacing with legacy systems that don't support IPv6
2. Required by external API or service constraints
3. Explicitly requested for backward compatibility
4. Cloud provider or infrastructure limitation (document this!)

**Always document why IPv4 is needed:**

```python
# IPv4 required: AWS Classic Load Balancer doesn't support IPv6
# TODO: Migrate to ALB when possible for IPv6 support
# See: https://github.com/org/repo/issues/123
legacy_endpoint = "http://192.0.2.1:8080/api"
```

## Checklist

When writing network code:

- [ ] Default addresses use IPv6 (`::`/`::1` not `0.0.0.0`/`127.0.0.1`)
- [ ] Socket creation uses `AF_INET6` by default
- [ ] Dual-stack is enabled where appropriate
- [ ] Tests cover IPv6 primarily, IPv4 as legacy path
- [ ] Documentation shows IPv6 examples first
- [ ] Configuration examples use IPv6 addresses
- [ ] URL handling accounts for IPv6 bracket notation
- [ ] IPv4 code paths are commented as "legacy"
- [ ] Any IPv4-only code has documented justification
