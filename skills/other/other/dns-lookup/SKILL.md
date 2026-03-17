---
name: dns-lookup
description: "Resolve hostnames to IP addresses using `dig` from bind-utils."
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["dig"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "bind-utils",
              "bins": ["dig"],
              "label": "Install bind-utils (dnf)",
            },
          ],
      },
  }
---

# DNS Lookup Skill

Resolve hostnames to IP addresses using `dig`. Provided by the `bind-utils` package.

## Basic Lookup

Resolve A records for a hostname:

```bash
dig example.com A +short
```

## IPv6 Lookup

Resolve AAAA records:

```bash
dig example.com AAAA +short
```

## Full DNS Record

Get the full DNS response with authority and additional sections:

```bash
dig example.com ANY
```

## Reverse Lookup

Find the hostname for an IP address:

```bash
dig -x 93.184.216.34 +short
```

## Install

```bash
sudo dnf install bind-utils
```
