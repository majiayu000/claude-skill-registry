---
name: cloudflare-api
description: Connect to Cloudflare API for DNS management, tunnels, and zone administration. Use when user needs to manage domains, DNS records, or create tunnels.
---

# Cloudflare Skill

Connect to Cloudflare API for DNS management, tunnels, and zone administration.

## Setup

```bash
# Store token
echo "YOUR_API_TOKEN" > ~/.cloudflare_token
chmod 600 ~/.cloudflare_token

# Or env var
export CLOUDFLARE_API_TOKEN="YOUR_API_TOKEN"
```

Read token in scripts:
```bash
CF_TOKEN=$(cat ~/.cloudflare_token 2>/dev/null || echo "$CLOUDFLARE_API_TOKEN")
```

## Zones (Domains)

```bash
# List all zones
curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" | jq '.result[] | {id, name, status}'

# Get zone ID for a domain
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=example.com" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')
```

## DNS Records

```bash
# List all records for a zone
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {name, type, content, proxied}'

# List by type
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=A" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {name, content}'

# Create A record
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"api","content":"1.2.3.4","ttl":1,"proxied":true}' | jq '.success'

# Create CNAME
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"www","content":"example.com","ttl":1,"proxied":true}' | jq '.success'

# Update record (need record ID first)
RECORD_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=A&name=api.example.com" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')

curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"content":"5.6.7.8"}' | jq '.success'

# Delete record
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.success'
```

## Tunnels

```bash
# List tunnels
ACCOUNT_ID=$(curl -s "https://api.cloudflare.com/client/v4/accounts" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')

curl -s "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {id, name, status}'

# Create tunnel
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"name":"my-tunnel","tunnel_secret":"base64-encoded-32-byte-secret"}' | jq '.result.id'

# Get run token
TUNNEL_ID="your-tunnel-id"
curl -s "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/token" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result'
```

## Cache Purge

```bash
# Purge everything
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' | jq '.success'

# Purge specific URLs
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://example.com/page.html","https://example.com/api/data"]}' | jq '.success'
```

## Token Permissions

| Feature | Required Permission |
|---------|-------------------|
| List zones | Zone:Read |
| Manage DNS | DNS:Edit |
| Manage tunnels | Account:Cloudflare Tunnel:Edit |
| Purge cache | Cache Purge |

## Troubleshooting

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Token inválido ou expirado |
| 403 Forbidden | Token sem a permissão necessária |
| Zone not found | Domínio não está na conta |
| Record already exists | Use PATCH para atualizar ao invés de POST |
