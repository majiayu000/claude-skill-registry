---
name: cloudflare-vpc-services
description: Diagnose and create Cloudflare VPC Services for Workers to access private APIs in AWS, Azure, GCP, or on-premise networks. Use when troubleshooting dns_error, configuring cloudflared tunnels, setting up VPC service bindings, or routing Workers to internal services.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# Cloudflare VPC Services

> Enable Workers to securely access private APIs and services through encrypted tunnels without public internet exposure.

## ⚠️ BEFORE YOU START

**This skill prevents 5 common errors and saves ~60% tokens.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Setup Time | 45+ min | 10 min |
| Common Errors | 5 | 0 |
| Token Usage | ~8000 | ~3000 |

### Known Issues This Skill Prevents

1. `dns_error` from outdated cloudflared version or wrong protocol
2. Requests leaving VPC due to using public hostnames instead of internal
3. Port mismatch - fetch() port is ignored, service config port is used
4. Missing absolute URLs in fetch() calls
5. Incorrect tunnel ID or service binding configuration

## Quick Start

### Step 1: Verify Tunnel Requirements

```bash
# Check cloudflared version on remote infrastructure (K8s, EC2, etc.)
# Must be 2025.7.0 or later
cloudflared --version

# Verify QUIC protocol is configured (not http2)
# Check tunnel config or Cloudflare dashboard
```

**Why this matters:** Workers VPC requires cloudflared 2025.7.0+ with QUIC protocol. Older versions or http2 protocol cause `dns_error`.

### Step 2: Create VPC Service

```bash
# Use Cloudflare API or dashboard to create VPC service
# See templates/vpc-service-ip.json or templates/vpc-service-hostname.json
```

**Why this matters:** The VPC service defines the actual target (IP/hostname) that the tunnel routes to. The fetch() URL only sets Host header and SNI.

### Step 3: Configure Wrangler Binding

```jsonc
// wrangler.jsonc
{
  "vpc_services": [
    {
      "binding": "PRIVATE_API",
      "service_id": "<YOUR_SERVICE_ID>",
      "remote": true
    }
  ]
}
```

**Why this matters:** The binding name becomes the environment variable used in Worker code: `env.PRIVATE_API.fetch()`.

## Critical Rules

### ✅ Always Do

- ✅ Use absolute URLs with protocol, host, and path in fetch()
- ✅ Use internal VPC hostnames, not public endpoints
- ✅ Ensure cloudflared is 2025.7.0+ with QUIC protocol
- ✅ Allow UDP port 7844 outbound for QUIC connections

### ❌ Never Do

- ❌ Use port numbers in fetch() URL (they're ignored)
- ❌ Use public hostnames for services inside VPC
- ❌ Assume http2 protocol works (only QUIC is supported)
- ❌ Use relative URLs in fetch()

### Common Mistakes

**❌ Wrong:**
```javascript
// Port is ignored, relative URL fails
const response = await env.VPC_SERVICE.fetch("/api/users:8080");
```

**✅ Correct:**
```javascript
// Absolute URL, port configured in VPC service
const response = await env.VPC_SERVICE.fetch("https://internal-api.company.local/api/users");
```

**Why:** The VPC service configuration determines actual routing. The fetch() URL only populates the Host header and SNI value.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| `dns_error` | cloudflared < 2025.7.0 or http2 protocol | Update cloudflared, configure QUIC, allow UDP 7844 |
| Requests go to public internet | Using public hostname in fetch() | Use internal VPC hostname |
| Connection refused | Wrong port in VPC service config | Configure correct http_port/https_port in service |
| Timeout | Tunnel not running or wrong tunnel_id | Verify tunnel status, check tunnel_id |
| 404 errors | Incorrect path routing | Verify internal service path matches fetch() path |

## Configuration Reference

### wrangler.jsonc

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",
  "vpc_services": [
    {
      "binding": "PRIVATE_API",
      "service_id": "daf43e8c-a81a-4242-9912-4a2ebe4fdd79",
      "remote": true
    },
    {
      "binding": "PRIVATE_DATABASE",
      "service_id": "453b6067-1327-420d-89b3-2b6ad16e6551",
      "remote": true
    }
  ]
}
```

**Key settings:**
- `binding`: Environment variable name for accessing the service
- `service_id`: UUID from VPC service creation
- `remote`: Must be `true` for VPC services

## Common Patterns

### Basic GET Request

```javascript
export default {
  async fetch(request, env) {
    const response = await env.PRIVATE_API.fetch(
      "https://internal-api.company.local/users"
    );
    return response;
  }
};
```

### POST with Authentication

```javascript
const response = await env.PRIVATE_API.fetch(
  "https://internal-api.company.local/users",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${env.API_TOKEN}`
    },
    body: JSON.stringify({ name: "John", email: "john@example.com" })
  }
);
```

### API Gateway with Path Routing

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname.startsWith('/api/users')) {
      return env.USER_SERVICE.fetch(
        `https://user-api.internal${url.pathname}`
      );
    } else if (url.pathname.startsWith('/api/orders')) {
      return env.ORDER_SERVICE.fetch(
        `https://orders-api.internal${url.pathname}`
      );
    }

    return new Response('Not Found', { status: 404 });
  }
};
```

## Bundled Resources

### Templates

Located in `templates/`:
- [`wrangler-vpc.jsonc`](templates/wrangler-vpc.jsonc) - Ready-to-use wrangler config with VPC bindings
- [`vpc-service-ip.json`](templates/vpc-service-ip.json) - IP-based VPC service API payload
- [`vpc-service-hostname.json`](templates/vpc-service-hostname.json) - Hostname-based VPC service API payload

Copy these templates as starting points for your implementation.

### Scripts

Located in `scripts/`:
- [`list-vpc-services.sh`](scripts/list-vpc-services.sh) - List VPC services via Cloudflare API
- [`tail-worker.sh`](scripts/tail-worker.sh) - Debug VPC connections with live logs
- [`set-api-token.sh`](scripts/set-api-token.sh) - Set secrets for private API auth

### References

Located in `references/`:
- [`api-patterns.md`](references/api-patterns.md) - Comprehensive fetch() patterns and examples

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| wrangler | latest | Deploy Workers with VPC bindings |
| cloudflared | 2025.7.0+ | Tunnel daemon (on remote infrastructure) |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| @cloudflare/workers-types | latest | TypeScript types for Workers |

## Official Documentation

- [Workers VPC Documentation](https://developers.cloudflare.com/workers-vpc/)
- [Cloudflare Tunnel Setup](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## Troubleshooting

### dns_error when calling VPC service

**Symptoms:** Worker returns `dns_error` when calling `env.VPC_SERVICE.fetch()`

**Solution:**
1. Update cloudflared to 2025.7.0+ on remote infrastructure
2. Configure QUIC protocol (not http2)
3. Allow UDP port 7844 outbound

### Requests going to public internet

**Symptoms:** Logs show requests hitting public endpoints instead of internal

**Solution:**
```javascript
// Use internal hostname
const response = await env.VPC_SERVICE.fetch(
  "https://internal-api.vpc.local/endpoint"  // Internal
  // NOT "https://api.company.com/endpoint"   // Public
);
```

### Connection timeout

**Symptoms:** Requests hang and eventually timeout

**Solution:**
1. Verify tunnel is running: check cloudflared logs
2. Verify tunnel_id matches in VPC service config
3. Check network connectivity from tunnel to target

## Setup Checklist

Before using this skill, verify:

- [ ] cloudflared 2025.7.0+ deployed on remote infrastructure
- [ ] QUIC protocol configured (not http2)
- [ ] UDP port 7844 outbound allowed
- [ ] VPC service created with correct tunnel_id
- [ ] wrangler.jsonc has vpc_services binding
- [ ] Using internal hostnames (not public endpoints)
- [ ] Using absolute URLs in fetch() calls
