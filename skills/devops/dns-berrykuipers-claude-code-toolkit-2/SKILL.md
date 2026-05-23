---
name: dns
description: |
  Cloudflare DNS and infrastructure management. Manage DNS records, tunnels,
  Access policies, SSL certificates, and CDN caching.
examples:
  - "/dns list"
  - "/dns add staging.project.com A 1.2.3.4"
  - "/dns purge project.com"
  - "/dns ssl-status"
  - "/dns tunnel status"
---

# DNS & Cloudflare Skill

Manage Cloudflare DNS, tunnels, Access, and CDN configuration.

## Usage

```bash
/dns                           # Show DNS status for current project domains
/dns list                      # List all DNS records for project domain
/dns add <subdomain> <type> <value>    # Add DNS record
/dns update <subdomain> <type> <value> # Update DNS record
/dns delete <subdomain> <type>         # Delete DNS record
/dns ssl-status                # Check SSL certificate status
/dns purge [path]              # Purge Cloudflare cache
/dns tunnel status             # Check Cloudflare Tunnel status
/dns access list               # List Access applications
```

## DNS Management

### List Records

```bash
# Using wrangler CLI
wrangler dns list ${DOMAIN}

# Or using Cloudflare API
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json"
```

### Add/Update Records

```bash
# Add A record (proxied through Cloudflare)
wrangler dns create ${DOMAIN} A staging --content ${IP} --proxied

# Add CNAME record
wrangler dns create ${DOMAIN} CNAME api --content ${TARGET} --proxied

# Update existing record
wrangler dns update ${DOMAIN} A staging --content ${NEW_IP}
```

### Delete Records

```bash
# Delete specific record
wrangler dns delete ${DOMAIN} A staging
```

## SSL Certificate Management

```bash
# Check certificate expiry
echo | openssl s_client -servername ${DOMAIN} -connect ${DOMAIN}:443 2>/dev/null | \
  openssl x509 -noout -dates

# Force SSL renewal (via Cloudflare dashboard or API)
# Cloudflare auto-renews Universal SSL certificates
```

## Cloudflare Tunnel

```bash
# List tunnels
cloudflared tunnel list

# Create new tunnel
cloudflared tunnel create ${TUNNEL_NAME}

# Route DNS to tunnel
cloudflared tunnel route dns ${TUNNEL_NAME} ${SUBDOMAIN}.${DOMAIN}

# Check tunnel status on VPS
ssh ${USER}@${HOST} "sudo systemctl status cloudflared"

# View tunnel logs
ssh ${USER}@${HOST} "sudo journalctl -u cloudflared -n 50"
```

## Cloudflare Access (Zero-Trust)

```bash
# List Access applications
wrangler access list-apps

# Create Access application (usually via dashboard)
# - Set application name
# - Set domain (e.g., seq.tribevibe.events)
# - Configure identity providers (email, GitHub, etc.)
# - Set session duration

# After Access is configured, nginx needs CORS headers:
# add_header Access-Control-Allow-Origin "${ALLOWED_ORIGIN}" always;
# add_header Access-Control-Allow-Credentials "true" always;
```

## Cache Management

```bash
# Purge specific URL
wrangler purge https://${DOMAIN}/api/v1/users

# Purge everything for domain
wrangler purge --everything --zone ${ZONE_ID}

# Purge by cache tags (if configured)
wrangler purge --tags "static-assets"
```

## Common Tasks

### Setup New Subdomain

```bash
# 1. Add DNS record pointing to VPS
wrangler dns create ${DOMAIN} A ${SUBDOMAIN} --content ${VPS_IP} --proxied

# 2. Configure nginx on VPS
ssh ${USER}@${HOST} << 'EOF'
cat > /etc/nginx/sites-available/${SUBDOMAIN}.conf << 'NGINX'
server {
    listen 443 ssl;
    server_name ${SUBDOMAIN}.${DOMAIN};

    location / {
        proxy_pass http://localhost:${PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX
ln -sf /etc/nginx/sites-available/${SUBDOMAIN}.conf /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
EOF

# 3. Verify SSL (Cloudflare provides automatic SSL)
curl -I https://${SUBDOMAIN}.${DOMAIN}
```

### Add Zero-Trust Protection

```bash
# 1. Create Access application in Cloudflare dashboard
# 2. Add allowed emails/groups
# 3. Update nginx for CORS (if needed)
# 4. Test authentication flow
```

## Project Domain Lookup

Domains are defined in `deployments.registry.json`:

```json
{
  "projects": {
    "tribevibe": {
      "environments": {
        "production": { "domain": "tribevibe.events" },
        "staging": { "domain": "staging.tribevibe.events" }
      }
    }
  }
}
```

## Safety

- NEVER delete production DNS records without backup plan
- ALWAYS verify DNS changes propagate (use dig or nslookup)
- Be aware of DNS propagation delays (up to 48h, usually minutes)
- Cloudflare proxy provides DDoS protection - don't bypass unnecessarily
