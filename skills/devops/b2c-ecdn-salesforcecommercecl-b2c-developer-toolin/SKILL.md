---
name: b2c-ecdn
description: Manage eCDN (embedded Content Delivery Network) settings. Use when purging cache, configuring WAF rules, managing SSL certificates, setting rate limits, or creating CDN zones for storefronts.
---

# B2C eCDN Skill

Use the `b2c` CLI plugin to manage eCDN (embedded Content Delivery Network) zones, certificates, security settings, and more.

## Prerequisites

- OAuth credentials with `sfcc.cdn-zones` scope (read operations)
- OAuth credentials with `sfcc.cdn-zones.rw` scope (write operations)
- Tenant ID for your B2C Commerce organization

## Examples

### List CDN Zones

```bash
# list all CDN zones for a tenant
b2c ecdn zones list --tenant-id zzxy_prd

# list with JSON output
b2c ecdn zones list --tenant-id zzxy_prd --json
```

### Create a Storefront Zone

```bash
# create a new storefront zone
b2c ecdn zones create --tenant-id zzxy_prd --storefront-hostname www.example.com --origin-hostname origin.example.com
```

### Purge Cache

```bash
# purge cache for specific paths
b2c ecdn cache purge --tenant-id zzxy_prd --zone my-zone --path /products --path /categories

# purge by cache tags
b2c ecdn cache purge --tenant-id zzxy_prd --zone my-zone --tag product-123 --tag category-456

# purge everything
b2c ecdn cache purge --tenant-id zzxy_prd --zone my-zone --purge-everything
```

### Manage Certificates

```bash
# list certificates for a zone
b2c ecdn certificates list --tenant-id zzxy_prd --zone my-zone

# add a new certificate
b2c ecdn certificates add --tenant-id zzxy_prd --zone my-zone --hostname www.example.com --certificate-file ./cert.pem --private-key-file ./key.pem

# get certificate details
b2c ecdn certificates get --tenant-id zzxy_prd --zone my-zone --certificate-id abc123

# validate a custom hostname
b2c ecdn certificates validate --tenant-id zzxy_prd --zone my-zone --certificate-id abc123
```

### Security Settings

```bash
# get security settings
b2c ecdn security get --tenant-id zzxy_prd --zone my-zone

# update security settings
b2c ecdn security update --tenant-id zzxy_prd --zone my-zone --ssl-mode full --min-tls-version 1.2 --always-use-https
```

### Speed Settings

```bash
# get speed optimization settings
b2c ecdn speed get --tenant-id zzxy_prd --zone my-zone

# update speed settings
b2c ecdn speed update --tenant-id zzxy_prd --zone my-zone --browser-cache-ttl 14400 --auto-minify-html --auto-minify-css
```

### WAF (Web Application Firewall)

```bash
# list WAF v1 groups
b2c ecdn waf groups list --tenant-id zzxy_prd --zone my-zone

# update WAF v1 group mode
b2c ecdn waf groups update --tenant-id zzxy_prd --zone my-zone --group-id abc123 --mode on

# list WAF v1 rules in a group
b2c ecdn waf rules list --tenant-id zzxy_prd --zone my-zone --group-id abc123

# list WAF v2 rulesets
b2c ecdn waf rulesets list --tenant-id zzxy_prd --zone my-zone

# update WAF v2 ruleset
b2c ecdn waf rulesets update --tenant-id zzxy_prd --zone my-zone --ruleset-id abc123 --action block

# migrate zone to WAF v2
b2c ecdn waf migrate --tenant-id zzxy_prd --zone my-zone
```

### Firewall Rules

```bash
# list custom firewall rules
b2c ecdn firewall list --tenant-id zzxy_prd --zone my-zone

# create a firewall rule
b2c ecdn firewall create --tenant-id zzxy_prd --zone my-zone --description "Block bad bots" --action block --filter '(cf.client.bot)'

# update a firewall rule
b2c ecdn firewall update --tenant-id zzxy_prd --zone my-zone --rule-id abc123 --action challenge

# reorder firewall rules
b2c ecdn firewall reorder --tenant-id zzxy_prd --zone my-zone --rule-ids id1,id2,id3
```

### Rate Limiting

```bash
# list rate limiting rules
b2c ecdn rate-limit list --tenant-id zzxy_prd --zone my-zone

# create a rate limiting rule
b2c ecdn rate-limit create --tenant-id zzxy_prd --zone my-zone --description "API rate limit" --threshold 100 --period 60 --action block --match-url '/api/*'

# delete a rate limiting rule
b2c ecdn rate-limit delete --tenant-id zzxy_prd --zone my-zone --rule-id abc123
```

### Logpush

```bash
# create ownership challenge for S3 destination
b2c ecdn logpush ownership --tenant-id zzxy_prd --zone my-zone --destination-path 's3://my-bucket/logs?region=us-east-1'

# list logpush jobs
b2c ecdn logpush jobs list --tenant-id zzxy_prd --zone my-zone

# create a logpush job
b2c ecdn logpush jobs create --tenant-id zzxy_prd --zone my-zone --name "HTTP logs" --destination-path 's3://my-bucket/logs?region=us-east-1' --log-type http_requests

# update a logpush job (enable/disable)
b2c ecdn logpush jobs update --tenant-id zzxy_prd --zone my-zone --job-id 123456 --enabled

# delete a logpush job
b2c ecdn logpush jobs delete --tenant-id zzxy_prd --zone my-zone --job-id 123456
```

### Page Shield

```bash
# list Page Shield notification webhooks (organization level)
b2c ecdn page-shield notifications list --tenant-id zzxy_prd

# create a notification webhook
b2c ecdn page-shield notifications create --tenant-id zzxy_prd --url https://example.com/webhook --secret my-secret --zones zone1,zone2

# list Page Shield policies (zone level)
b2c ecdn page-shield policies list --tenant-id zzxy_prd --zone my-zone

# create a CSP policy
b2c ecdn page-shield policies create --tenant-id zzxy_prd --zone my-zone --action allow --value script-src

# list detected scripts
b2c ecdn page-shield scripts list --tenant-id zzxy_prd --zone my-zone
```

### MRT Rules

```bash
# get MRT ruleset for a zone
b2c ecdn mrt-rules get --tenant-id zzxy_prd --zone my-zone

# create MRT rules to route to a Managed Runtime environment
b2c ecdn mrt-rules create --tenant-id zzxy_prd --zone my-zone --mrt-hostname customer-pwa.mobify-storefront.com --expressions '(http.host eq "example.com")'

# update MRT ruleset hostname
b2c ecdn mrt-rules update --tenant-id zzxy_prd --zone my-zone --mrt-hostname new-customer-pwa.mobify-storefront.com

# delete MRT ruleset
b2c ecdn mrt-rules delete --tenant-id zzxy_prd --zone my-zone
```

### mTLS Certificates

```bash
# list mTLS certificates (organization level)
b2c ecdn mtls list --tenant-id zzxy_prd

# create mTLS certificate for code upload authentication
b2c ecdn mtls create --tenant-id zzxy_prd --name "Build Server" --ca-certificate-file ./ca.pem --leaf-certificate-file ./leaf.pem

# get mTLS certificate details
b2c ecdn mtls get --tenant-id zzxy_prd --certificate-id abc123

# delete mTLS certificate
b2c ecdn mtls delete --tenant-id zzxy_prd --certificate-id abc123
```

### Cipher Suites

```bash
# get cipher suites configuration
b2c ecdn cipher-suites get --tenant-id zzxy_prd --zone my-zone

# update to Modern cipher suite
b2c ecdn cipher-suites update --tenant-id zzxy_prd --zone my-zone --suite-type Modern

# update to Custom cipher suite with specific ciphers
b2c ecdn cipher-suites update --tenant-id zzxy_prd --zone my-zone --suite-type Custom --ciphers "ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-GCM-SHA256"
```

### Origin Headers

```bash
# get origin header modification
b2c ecdn origin-headers get --tenant-id zzxy_prd --zone my-zone

# set origin header modification (for MRT)
b2c ecdn origin-headers set --tenant-id zzxy_prd --zone my-zone --header-value my-secret-value

# delete origin header modification
b2c ecdn origin-headers delete --tenant-id zzxy_prd --zone my-zone
```

## Configuration

The tenant ID can be set via environment variable:
- `SFCC_TENANT_ID`: B2C Commerce tenant ID

The `--zone` flag accepts either:
- Zone ID (32-character hex string)
- Zone name (human-readable, case-insensitive lookup)

### OAuth Scopes

| Operation | Required Scope |
|-----------|---------------|
| Read operations | `sfcc.cdn-zones` |
| Write operations | `sfcc.cdn-zones.rw` |

### More Commands

See `b2c ecdn --help` for a full list of available commands and options in the `ecdn` topic.
