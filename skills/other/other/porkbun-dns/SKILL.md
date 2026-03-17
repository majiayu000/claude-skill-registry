---
name: porkbun-dns
description: Manages DNS records for abaci.one via the Porkbun API. Use when asked to add subdomains, update DNS records, check DNS configuration, or manage domain settings.
allowed-tools: Bash, Read
---

# Porkbun DNS Management

This skill manages DNS records for `abaci.one` using the Porkbun API.

## API Credentials Location

The Porkbun API credentials are stored on the NAS:

```
/volume1/homes/antialias/projects/abaci.one/ddns-data/ddns-config.json
```

To retrieve them:

```bash
ssh nas.home.network 'cat /volume1/homes/antialias/projects/abaci.one/ddns-data/ddns-config.json'
```

The file contains:

- `api_key`: Public API key (starts with `pk1_`)
- `secret_api_key`: Secret API key (starts with `sk1_`)

## Common Operations

### List All DNS Records

```bash
curl -s -X POST "https://api.porkbun.com/api/json/v3/dns/retrieve/abaci.one" \
  -H "Content-Type: application/json" \
  -d '{
    "secretapikey": "SECRET_KEY",
    "apikey": "API_KEY"
  }' | python3 -m json.tool
```

### Create a CNAME Record (Subdomain)

Best for subdomains that should follow the main domain's IP (useful with DDNS):

```bash
curl -s -X POST "https://api.porkbun.com/api/json/v3/dns/create/abaci.one" \
  -H "Content-Type: application/json" \
  -d '{
    "secretapikey": "SECRET_KEY",
    "apikey": "API_KEY",
    "name": "subdomain-name",
    "type": "CNAME",
    "content": "abaci.one",
    "ttl": "300"
  }'
```

### Create an A Record

For direct IP pointing:

```bash
curl -s -X POST "https://api.porkbun.com/api/json/v3/dns/create/abaci.one" \
  -H "Content-Type: application/json" \
  -d '{
    "secretapikey": "SECRET_KEY",
    "apikey": "API_KEY",
    "name": "subdomain-name",
    "type": "A",
    "content": "IP_ADDRESS",
    "ttl": "300"
  }'
```

### Delete a DNS Record

First list records to get the record ID, then:

```bash
curl -s -X POST "https://api.porkbun.com/api/json/v3/dns/delete/abaci.one/RECORD_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "secretapikey": "SECRET_KEY",
    "apikey": "API_KEY"
  }'
```

### Update a DNS Record

```bash
curl -s -X POST "https://api.porkbun.com/api/json/v3/dns/edit/abaci.one/RECORD_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "secretapikey": "SECRET_KEY",
    "apikey": "API_KEY",
    "name": "subdomain-name",
    "type": "A",
    "content": "NEW_IP_ADDRESS",
    "ttl": "300"
  }'
```

## Verify DNS Propagation

After making changes, verify propagation:

```bash
# Check against your local resolver
dig +short subdomain.abaci.one

# Check against Google's DNS (bypasses local cache)
dig +short subdomain.abaci.one @8.8.8.8

# Check against Porkbun's nameservers directly
dig +short subdomain.abaci.one @maceio.porkbun.com
```

## Current DNS Setup

The domain has these key records:

| Type  | Host      | Purpose                                |
| ----- | --------- | -------------------------------------- |
| A     | abaci.one | Main domain → home IP (DDNS managed)   |
| CNAME | blue      | Blue container instance                |
| CNAME | green     | Green container instance               |
| CNAME | \*        | Wildcard parking page (can be deleted) |

## Notes

- **CNAME vs A record**: Use CNAME for subdomains so they automatically follow DDNS updates to the main domain's IP
- **TTL**: 300 seconds (5 minutes) is good for records that might change; use 3600+ for stable records
- **Wildcard record**: The `*.abaci.one` → `pixie.porkbun.com` is Porkbun's default parking page. Explicit records take precedence over wildcards.
- **Propagation**: DNS changes typically propagate within 5-15 minutes, though local caches may retain old values longer

## API Documentation

Full Porkbun API docs: https://porkbun.com/api/json/v3/documentation
