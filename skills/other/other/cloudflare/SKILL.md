---
name: cloudflare
description: Cloudflare services management including DNS, Tunnels (Argo), Zero Trust, WAF, CDN, Workers, and Pages. Configure domains, create tunnels for exposing local services, manage firewall rules, and optimize web performance. Use when working with Cloudflare, DNS management, reverse proxies, DDoS protection, or secure remote access.
---

# Cloudflare Services Skill

Comprehensive management of Cloudflare services including DNS, Tunnels, Zero Trust, WAF, Workers, and Pages.

## Triggers

Use this skill when you see:
- cloudflare, cf, cloudflare tunnel
- argo tunnel, cloudflared, zero trust
- cloudflare workers, cloudflare pages
- waf, ddos protection, cdn
- dns management, cloudflare dns

## Instructions

### Cloudflare Tunnel Setup

#### Install cloudflared

```bash
# Linux
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# macOS
brew install cloudflared

# Windows (winget)
winget install --id Cloudflare.cloudflared
```

#### Authenticate and Create Tunnel

```bash
# Login to Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create my-tunnel

# List tunnels
cloudflared tunnel list

# Route DNS to tunnel
cloudflared tunnel route dns my-tunnel app.example.com
```

#### Tunnel Configuration

```yaml
# ~/.cloudflared/config.yml
tunnel: <TUNNEL-ID>
credentials-file: /root/.cloudflared/<TUNNEL-ID>.json

ingress:
  # Route to local web server
  - hostname: app.example.com
    service: http://localhost:3000

  # Route to another service
  - hostname: api.example.com
    service: http://localhost:8080

  # SSH access
  - hostname: ssh.example.com
    service: ssh://localhost:22

  # Catch-all (required)
  - service: http_status:404
```

#### Run Tunnel

```bash
# Run tunnel
cloudflared tunnel run my-tunnel

# Install as service
sudo cloudflared service install

# Run with specific config
cloudflared tunnel --config ~/.cloudflared/config.yml run
```

### DNS Management

```bash
# Using Cloudflare API
# Set API token
export CF_API_TOKEN="your-api-token"
export CF_ZONE_ID="your-zone-id"

# List DNS records
curl -X GET "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json"

# Create A record
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "app",
    "content": "192.0.2.1",
    "ttl": 1,
    "proxied": true
  }'

# Create CNAME record
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "www",
    "content": "example.com",
    "ttl": 1,
    "proxied": true
  }'
```

### Cloudflare Workers

#### Basic Worker

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle different paths
    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({ message: 'Hello World' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Proxy to origin
    return fetch(request);
  },
};
```

#### Worker with KV Storage

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    if (request.method === 'GET') {
      const value = await env.MY_KV.get(key);
      return new Response(value || 'Not found', {
        status: value ? 200 : 404,
      });
    }

    if (request.method === 'PUT') {
      const value = await request.text();
      await env.MY_KV.put(key, value);
      return new Response('Saved', { status: 201 });
    }

    return new Response('Method not allowed', { status: 405 });
  },
};
```

#### wrangler.toml

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"

[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"

[triggers]
crons = ["0 * * * *"]
```

#### Deploy Worker

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Deploy
wrangler deploy

# Tail logs
wrangler tail
```

### Cloudflare Pages

```bash
# Deploy from CLI
wrangler pages deploy ./dist --project-name=my-project

# Create project
wrangler pages project create my-project

# List deployments
wrangler pages deployment list --project-name=my-project
```

### Zero Trust Access

#### Application Access Policy

```bash
# Create access application
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/access/apps" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Internal App",
    "domain": "app.example.com",
    "type": "self_hosted",
    "session_duration": "24h"
  }'
```

### WAF Rules

```bash
# Create firewall rule
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/firewall/rules" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '[{
    "filter": {
      "expression": "(ip.src ne 192.0.2.1)",
      "paused": false
    },
    "action": "block",
    "description": "Block all except allowed IP"
  }]'
```

### Page Rules

```bash
# Create page rule for caching
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/pagerules" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [{
      "target": "url",
      "constraint": {
        "operator": "matches",
        "value": "*example.com/static/*"
      }
    }],
    "actions": [{
      "id": "cache_level",
      "value": "cache_everything"
    }],
    "priority": 1,
    "status": "active"
  }'
```

## Best Practices

1. **Tunnels**: Use tunnels instead of exposing ports directly
2. **DNS**: Enable proxied (orange cloud) for DDoS protection
3. **Workers**: Use Workers for edge logic and caching
4. **Security**: Enable Zero Trust for internal applications
5. **SSL**: Use Full (Strict) SSL mode

## Common Workflows

### Expose Local Service
1. Install cloudflared
2. Create tunnel: `cloudflared tunnel create my-tunnel`
3. Configure ingress in config.yml
4. Route DNS: `cloudflared tunnel route dns my-tunnel app.example.com`
5. Run tunnel: `cloudflared tunnel run my-tunnel`

### Deploy Static Site
1. Build static site
2. Deploy with Wrangler: `wrangler pages deploy ./dist`
3. Configure custom domain in dashboard
4. Enable HTTPS
