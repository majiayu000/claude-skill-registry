---
name: cloudflare
description: "Deploy and manage Cloudflare services including Workers, Pages, R2, D1, and KV. Configure DNS, CDN, security rules, and edge computing. Use for edge deployments, CDN, and Cloudflare infrastructure."
---

# Cloudflare Skill

Complete guide for managing Cloudflare services - DNS, Tunnels, Zero Trust, and more.

## Quick Reference

### Cloudflare Services
| Service | Purpose |
|---------|---------|
| **DNS** | Domain name resolution with proxy |
| **CDN** | Content delivery and caching |
| **Tunnels** | Expose local services securely |
| **Zero Trust** | Identity-based access control |
| **WAF** | Web application firewall |
| **Workers** | Serverless edge computing |
| **Pages** | Static site hosting |

### CLI Installation
```bash
# cloudflared (Tunnels)
# macOS
brew install cloudflared

# Linux
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# Windows
winget install Cloudflare.cloudflared

# Wrangler (Workers/Pages)
npm install -g wrangler
```

---

## 1. DNS Management

### Add DNS Records
```bash
# Via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "www",
    "content": "192.0.2.1",
    "ttl": 1,
    "proxied": true
  }'
```

### Common Record Types
```yaml
# A Record (IPv4)
Type: A
Name: www
Content: 192.0.2.1
Proxied: Yes

# AAAA Record (IPv6)
Type: AAAA
Name: www
Content: 2001:db8::1
Proxied: Yes

# CNAME Record
Type: CNAME
Name: blog
Content: www.example.com
Proxied: Yes

# MX Record (Email)
Type: MX
Name: @
Content: mail.example.com
Priority: 10
Proxied: No  # MX cannot be proxied

# TXT Record
Type: TXT
Name: @
Content: "v=spf1 include:_spf.google.com ~all"
```

### Proxy Status
```yaml
# Orange Cloud (Proxied)
- Traffic goes through Cloudflare
- DDoS protection enabled
- CDN caching enabled
- SSL/TLS termination at edge
- Real IP hidden

# Grey Cloud (DNS Only)
- Direct connection to origin
- No Cloudflare protection
- Required for: MX, non-HTTP services
```

---

## 2. Cloudflare Tunnels

### Create Tunnel
```bash
# Login to Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create my-tunnel

# List tunnels
cloudflared tunnel list

# Delete tunnel
cloudflared tunnel delete my-tunnel
```

### Configure Tunnel
```yaml
# ~/.cloudflared/config.yml
tunnel: <tunnel-id>
credentials-file: /root/.cloudflared/<tunnel-id>.json

ingress:
  # Web application
  - hostname: app.example.com
    service: http://localhost:8080

  # Home Assistant
  - hostname: ha.example.com
    service: http://localhost:8123
    originRequest:
      noTLSVerify: true

  # SSH access
  - hostname: ssh.example.com
    service: ssh://localhost:22

  # Catch-all (required)
  - service: http_status:404
```

### Run Tunnel
```bash
# Run manually
cloudflared tunnel run my-tunnel

# Run with config
cloudflared tunnel --config ~/.cloudflared/config.yml run my-tunnel

# Install as service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### Docker Tunnel
```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token ${TUNNEL_TOKEN}
    environment:
      - TUNNEL_TOKEN=your-tunnel-token
```

### Quick Tunnel (Temporary)
```bash
# Expose local service instantly (no config needed)
cloudflared tunnel --url http://localhost:3000

# Output: https://random-name.trycloudflare.com
```

---

## 3. Zero Trust / Access

### Create Access Application
```bash
# Via Dashboard: Zero Trust > Access > Applications

# API example
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/access/apps" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Internal App",
    "domain": "app.example.com",
    "type": "self_hosted",
    "session_duration": "24h"
  }'
```

### Access Policies
```yaml
# Email-based access
Policy Name: Allowed Users
Decision: Allow
Include:
  - Emails ending in: @company.com

# Group-based access
Policy Name: Admin Group
Decision: Allow
Include:
  - Access Groups: Administrators
Require:
  - Country: United States

# One-time PIN
Policy Name: Contractors
Decision: Allow
Include:
  - Emails: contractor@external.com
Authentication Method: One-time PIN
```

### Service Tokens
```bash
# Create service token for API/automation access
# Zero Trust > Access > Service Auth > Service Tokens

# Use in requests
curl -H "CF-Access-Client-Id: {client_id}" \
     -H "CF-Access-Client-Secret: {client_secret}" \
     https://app.example.com/api
```

### WARP Client
```bash
# Install WARP for device tunnel
# Connects device to Zero Trust network

# Enroll device
# Zero Trust > Settings > WARP Client > Device enrollment

# Device posture checks
- Require disk encryption
- Require firewall enabled
- Require specific OS version
```

---

## 4. WAF (Web Application Firewall)

### Managed Rulesets
```yaml
# Enable in Dashboard: Security > WAF > Managed rules

Rulesets:
  - Cloudflare Managed Ruleset (OWASP)
  - Cloudflare OWASP Core Ruleset
  - Exposed Credentials Check
```

### Custom Rules
```bash
# Block specific countries
(ip.geoip.country in {"CN" "RU" "KP"})
Action: Block

# Rate limiting
(http.request.uri.path contains "/api/")
Rate: 100 requests per minute
Action: Challenge

# Block bad bots
(cf.client.bot and not cf.verified_bot_category in {"Search Engine Crawler"})
Action: Block

# Protect admin area
(http.request.uri.path contains "/admin" and not ip.src in {192.168.1.0/24})
Action: Block
```

### Firewall Rules
```bash
# Allow only specific IPs
(not ip.src in {192.168.1.100 10.0.0.0/8})
Action: Block

# Challenge suspicious requests
(cf.threat_score gt 30)
Action: Managed Challenge

# Skip WAF for trusted paths
(http.request.uri.path eq "/health")
Action: Skip (all remaining rules)
```

---

## 5. Page Rules & Cache

### Page Rules
```yaml
# Force HTTPS
URL: http://*example.com/*
Setting: Always Use HTTPS

# Cache everything
URL: *example.com/static/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month

# Bypass cache for API
URL: *example.com/api/*
Settings:
  - Cache Level: Bypass

# Redirect
URL: old.example.com/*
Setting: Forwarding URL (301)
Destination: https://new.example.com/$1
```

### Cache Settings
```yaml
# Browser Cache TTL
Respect Existing Headers / Override with: 4 hours

# Edge Cache TTL
2 hours (default) to 1 month

# Cache by device type
Mobile, Desktop, Tablet variations

# Purge cache
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```

---

## 6. Workers

### Create Worker
```bash
# Initialize project
wrangler init my-worker
cd my-worker

# Login
wrangler login

# Deploy
wrangler deploy
```

### Basic Worker
```javascript
// src/index.js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Simple response
    if (url.pathname === "/") {
      return new Response("Hello from Cloudflare Workers!");
    }

    // Proxy request
    if (url.pathname.startsWith("/api/")) {
      const apiUrl = "https://api.backend.com" + url.pathname;
      return fetch(apiUrl, request);
    }

    return new Response("Not Found", { status: 404 });
  },
};
```

### Worker with KV Storage
```javascript
// wrangler.toml
// [[kv_namespaces]]
// binding = "MY_KV"
// id = "xxx"

export default {
  async fetch(request, env) {
    // Read from KV
    const value = await env.MY_KV.get("key");

    // Write to KV
    await env.MY_KV.put("key", "value");

    return new Response(value);
  },
};
```

### wrangler.toml
```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

[vars]
API_KEY = "secret"

[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

---

## 7. Pages (Static Sites)

### Deploy Static Site
```bash
# Connect to Git (Dashboard)
# Pages > Create a project > Connect to Git

# Direct upload
wrangler pages deploy ./dist

# Deploy with build
wrangler pages deploy ./dist --project-name my-site
```

### Build Configuration
```yaml
# Framework presets available:
- Next.js
- Nuxt
- SvelteKit
- Astro
- Hugo
- Jekyll
- Gatsby

# Custom build
Build command: npm run build
Build output directory: dist
Root directory: /
```

### Environment Variables
```bash
# Via Dashboard or wrangler.toml
[env.production.vars]
API_URL = "https://api.example.com"

[env.preview.vars]
API_URL = "https://staging-api.example.com"
```

---

## 8. SSL/TLS

### SSL Modes
```yaml
Off: No encryption (not recommended)
Flexible: HTTPS to Cloudflare, HTTP to origin
Full: HTTPS end-to-end (self-signed OK)
Full (Strict): HTTPS end-to-end (valid cert required)
```

### Origin Certificates
```bash
# Generate origin certificate
# SSL/TLS > Origin Server > Create Certificate

# Valid for up to 15 years
# Only trusted by Cloudflare (not browsers)
# Use for origin server to Cloudflare connection
```

### Edge Certificates
```yaml
# Automatic (free)
Universal SSL - covers *.example.com and example.com

# Advanced (paid)
- Custom hostnames
- Dedicated certificates
- Total TLS
```

---

## 9. API Usage

### Authentication
```bash
# API Token (recommended)
curl -H "Authorization: Bearer {api_token}" \
  "https://api.cloudflare.com/client/v4/user/tokens/verify"

# API Key (legacy)
curl -H "X-Auth-Email: {email}" \
     -H "X-Auth-Key: {api_key}" \
  "https://api.cloudflare.com/client/v4/user"
```

### Common API Calls
```bash
# List zones
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer {token}"

# Get zone details
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}" \
  -H "Authorization: Bearer {token}"

# List DNS records
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -H "Authorization: Bearer {token}"

# Update DNS record
curl -X PUT "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"www","content":"192.0.2.2","ttl":1,"proxied":true}'

# Purge cache
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```

---

## 10. Troubleshooting

### Common Issues

**DNS not propagating:**
```bash
# Check DNS propagation
dig +short example.com @1.1.1.1

# Verify Cloudflare nameservers
dig NS example.com

# Clear DNS cache
# Cloudflare Dashboard > DNS > clear cache
```

**Tunnel not connecting:**
```bash
# Check tunnel status
cloudflared tunnel info my-tunnel

# View logs
cloudflared tunnel --loglevel debug run my-tunnel

# Verify credentials
ls ~/.cloudflared/

# Re-authenticate
cloudflared tunnel login
```

**SSL errors:**
```yaml
# Error 525: SSL handshake failed
- Ensure origin has valid SSL certificate
- Check SSL mode (try Full instead of Full Strict)

# Error 526: Invalid SSL certificate
- Origin certificate expired or invalid
- Use Cloudflare Origin Certificate

# Mixed content
- Ensure all resources use HTTPS
- Enable Automatic HTTPS Rewrites
```

**5xx errors:**
```yaml
# Error 520: Web server returned unknown error
- Check origin server is running
- Verify origin responds on correct port

# Error 521: Web server is down
- Origin server not responding
- Check firewall allows Cloudflare IPs

# Error 522: Connection timed out
- Origin server overloaded
- Check origin firewall

# Error 524: A timeout occurred
- Origin took too long (>100s)
- Optimize origin response time
```

---

## Best Practices

1. **Use API tokens** with minimal permissions (not global API key)
2. **Enable 2FA** on Cloudflare account
3. **Use Full (Strict) SSL** mode with valid origin certificates
4. **Whitelist Cloudflare IPs** at origin firewall
5. **Enable Under Attack Mode** during DDoS
6. **Use Page Rules** sparingly (3 free, use Transform Rules instead)
7. **Monitor analytics** for unusual traffic patterns
8. **Keep tunnels updated** with automatic updates or regular manual updates
9. **Use Zero Trust** for internal applications
10. **Cache static assets** aggressively at edge
