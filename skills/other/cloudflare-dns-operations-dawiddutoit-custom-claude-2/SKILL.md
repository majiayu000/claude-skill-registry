---
name: cloudflare-dns-operations
description: |
  Performs low-level Cloudflare DNS operations including adding, updating, deleting DNS
  records, managing zone settings, and dynamic DNS updates via Cloudflare API. Use when
  need manual DNS record management, dynamic DNS updates, zone settings configuration, or
  operations outside domain management system. Triggers on "add DNS record", "update DNS",
  "delete DNS record", "dynamic DNS", "Cloudflare API", or "manual DNS management". Works
  with Cloudflare API v4, cf-dns.sh and cf-settings.sh helper scripts, and direct curl
  API calls.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Edit
---

# Cloudflare DNS Operations Skill

Low-level Cloudflare DNS and zone management operations using Cloudflare API for manual record management and advanced configuration.

## Quick Start

Quick DNS operations:

```bash
# Load environment variables
source /home/dawiddutoit/projects/network/.env

# List all DNS records
/home/dawiddutoit/projects/network/scripts/cf-dns.sh list

# Add A record
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add A api.temet.ai 192.168.68.100

# Add CNAME record
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add CNAME www temet.ai

# Update existing record
/home/dawiddutoit/projects/network/scripts/cf-dns.sh update api.temet.ai 192.168.68.200

# Delete record
/home/dawiddutoit/projects/network/scripts/cf-dns.sh delete api.temet.ai
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Setup API Authentication
   - 3.2 List DNS Records
   - 3.3 Add DNS Records
   - 3.4 Update DNS Records
   - 3.5 Delete DNS Records
   - 3.6 Manage Zone Settings
   - 3.7 Dynamic DNS Updates
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Add DNS record"
- "Update DNS record"
- "Delete DNS record"
- "Dynamic DNS"
- "Cloudflare API operations"
- "Manual DNS management"

**Implicit Triggers:**
- Need to add DNS record outside domain management system
- Dynamic home IP updates needed
- Testing DNS configurations
- Bulk DNS operations required
- Zone settings need manual adjustment

**Debugging Triggers:**
- "How do I add a DNS record?"
- "How to update my home IP?"
- "What DNS records exist?"

## What This Skill Does

1. **Setup Auth** - Configures Cloudflare API credentials
2. **Lists Records** - Shows all DNS records in zone
3. **Adds Records** - Creates new A, AAAA, CNAME, TXT records
4. **Updates Records** - Modifies existing record values
5. **Deletes Records** - Removes DNS records
6. **Manages Settings** - Configures SSL, caching, security settings
7. **Dynamic DNS** - Automates home IP updates

## Instructions

### 3.1 Setup API Authentication

**Required credentials:**
- Cloudflare email address
- Cloudflare API token or Global API Key
- Zone ID for temet.ai domain

**Step 1: Get Zone ID**

1. Go to: https://dash.cloudflare.com
2. Select domain: **temet.ai**
3. Click: **Overview** tab
4. Find: **API** section in right sidebar
5. Copy: **Zone ID**

Example: `1234567890abcdef1234567890abcdef`

**Step 2: Get API Token**

**Recommended: Use API Token (scoped permissions)**

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click: **Create Token**
3. Select template: **Edit zone DNS**
4. Zone Resources: **Include** → **Specific zone** → **temet.ai**
5. Click: **Continue to summary** → **Create Token**
6. Copy token (shown only once)

**Alternative: Use Global API Key (full account access)**

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Scroll to: **API Keys** section
3. Click: **View** next to **Global API Key**
4. Copy key

⚠️ **Security note:** API Token is more secure (scoped permissions).

**Step 3: Add to .env**

```bash
# Edit .env
nano /home/dawiddutoit/projects/network/.env

# Add (using API Token - recommended):
CLOUDFLARE_EMAIL="your-email@example.com"
CLOUDFLARE_ZONE_ID="your-zone-id-here"
CLOUDFLARE_API_KEY="your-api-token-here"

# Or using Global API Key:
CLOUDFLARE_EMAIL="your-email@example.com"
CLOUDFLARE_ZONE_ID="your-zone-id-here"
CLOUDFLARE_GLOBAL_API_KEY="your-global-api-key-here"
```

**Step 4: Test Access**

```bash
source /home/dawiddutoit/projects/network/.env

curl -s -X GET "https://api.cloudflare.com/client/v4/user" \
    -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
    -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
    | jq '.success'
```

Expected output: `true`

### 3.2 List DNS Records

**Using helper script:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh list
```

Expected output:
```
DNS Records for temet.ai:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type    Name                 Value
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CNAME   pihole               tunnel-id.cfargotunnel.com
CNAME   jaeger               tunnel-id.cfargotunnel.com
A       home                 1.2.3.4
...
```

**Using direct API call:**

```bash
source /home/dawiddutoit/projects/network/.env

curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records" \
    -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
    -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
    | jq -r '.result[] | "\(.type)\t\(.name)\t\(.content)"'
```

**Filter by type:**

```bash
# List only A records
/home/dawiddutoit/projects/network/scripts/cf-dns.sh list | grep "^A"

# List only CNAME records
/home/dawiddutoit/projects/network/scripts/cf-dns.sh list | grep "^CNAME"
```

### 3.3 Add DNS Records

**Add A record (IPv4):**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add A api.temet.ai 192.168.68.100
```

**Add AAAA record (IPv6):**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add AAAA ipv6.temet.ai 2001:db8::1
```

**Add CNAME record:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add CNAME www temet.ai
```

**Add TXT record (verification/SPF):**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh add TXT _verification "verification-code"
```

**Add record with proxy enabled (orange cloud):**

```bash
# Using direct API call
source /home/dawiddutoit/projects/network/.env

curl -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records" \
    -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
    -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
    -H "Content-Type: application/json" \
    --data '{
      "type": "A",
      "name": "proxied.temet.ai",
      "content": "192.168.68.100",
      "ttl": 1,
      "proxied": true
    }' | jq '.'
```

**Common record types:**

| Type | Example | Purpose |
|------|---------|---------|
| A | `192.168.68.100` | IPv4 address |
| AAAA | `2001:db8::1` | IPv6 address |
| CNAME | `target.example.com` | Alias to another domain |
| TXT | `"verification-code"` | Text records (verification, SPF) |
| MX | `10 mail.example.com` | Mail exchange |

### 3.4 Update DNS Records

**Update existing record:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh update api.temet.ai 192.168.68.200
```

Script automatically:
1. Finds existing record by name
2. Gets record ID
3. Updates content to new value
4. Preserves type and proxy settings

**Update with direct API call:**

```bash
source /home/dawiddutoit/projects/network/.env

# Step 1: Get record ID
record_id=$(curl -s -X GET \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records?name=api.temet.ai" \
  -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
  | jq -r '.result[0].id')

# Step 2: Update record
curl -X PUT \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records/${record_id}" \
  -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "api.temet.ai",
    "content": "192.168.68.200",
    "ttl": 1,
    "proxied": false
  }' | jq '.'
```

### 3.5 Delete DNS Records

**Delete record by name:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-dns.sh delete api.temet.ai
```

**Confirm before deletion:**

Script will show:
```
Found record: A api.temet.ai → 192.168.68.100
Delete this record? (y/N):
```

**Using direct API call:**

```bash
source /home/dawiddutoit/projects/network/.env

# Step 1: Get record ID
record_id=$(curl -s -X GET \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records?name=api.temet.ai" \
  -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
  | jq -r '.result[0].id')

# Step 2: Delete record
curl -X DELETE \
  "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records/${record_id}" \
  -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
  | jq '.'
```

### 3.6 Manage Zone Settings

**View all zone settings:**

```bash
/home/dawiddutoit/projects/network/scripts/cf-settings.sh all
```

**View specific setting:**

```bash
# SSL/TLS mode
/home/dawiddutoit/projects/network/scripts/cf-settings.sh get ssl

# Security level
/home/dawiddutoit/projects/network/scripts/cf-settings.sh get security_level

# Caching level
/home/dawiddutoit/projects/network/scripts/cf-settings.sh get cache_level
```

**Update setting:**

```bash
# Set SSL to Full
/home/dawiddutoit/projects/network/scripts/cf-settings.sh set ssl full

# Enable always HTTPS
/home/dawiddutoit/projects/network/scripts/cf-settings.sh set always_use_https on

# Enable HTTP/3
/home/dawiddutoit/projects/network/scripts/cf-settings.sh set http3 on
```

**Enable security suite:**

```bash
# Enables: SSL Full, Always HTTPS, WAF
/home/dawiddutoit/projects/network/scripts/cf-settings.sh enable-security
```

**Enable performance suite:**

```bash
# Enables: Brotli, HTTP/2, HTTP/3
/home/dawiddutoit/projects/network/scripts/cf-settings.sh enable-performance
```

**Purge cache:**

```bash
# Purge all cached files
/home/dawiddutoit/projects/network/scripts/cf-settings.sh purge-cache
```

**Enable development mode:**

```bash
# Bypass cache for 3 hours
/home/dawiddutoit/projects/network/scripts/cf-settings.sh dev-mode on

# Disable development mode
/home/dawiddutoit/projects/network/scripts/cf-settings.sh dev-mode off
```

### 3.7 Dynamic DNS Updates

**Scenario:** Home internet IP changes, need to update DNS automatically.

**Manual update:**

```bash
# Get current public IP
current_ip=$(curl -s https://api.ipify.org)

# Update DNS record
/home/dawiddutoit/projects/network/scripts/cf-dns.sh update home.temet.ai $current_ip
```

**Automated script:**

```bash
#!/bin/bash
# /home/dawiddutoit/scripts/dynamic-dns-update.sh

source /home/dawiddutoit/projects/network/.env

# Get current public IP
current_ip=$(curl -s https://api.ipify.org)

# Get DNS record IP
dns_ip=$(dig +short home.temet.ai @1.1.1.1)

# Update if different
if [ "$current_ip" != "$dns_ip" ]; then
  echo "IP changed: $dns_ip → $current_ip"
  /home/dawiddutoit/projects/network/scripts/cf-dns.sh update home.temet.ai $current_ip
else
  echo "IP unchanged: $current_ip"
fi
```

**Schedule with cron:**

```bash
# Edit crontab
crontab -e

# Check every 5 minutes
*/5 * * * * /home/dawiddutoit/scripts/dynamic-dns-update.sh >> /var/log/dynamic-dns.log 2>&1
```

**Notification on change:**

```bash
#!/bin/bash
# With notification

current_ip=$(curl -s https://api.ipify.org)
dns_ip=$(dig +short home.temet.ai @1.1.1.1)

if [ "$current_ip" != "$dns_ip" ]; then
  /home/dawiddutoit/projects/network/scripts/cf-dns.sh update home.temet.ai $current_ip

  # Send notification (if ntfy configured)
  if [ -n "$NTFY_TOPIC" ]; then
    curl -d "Home IP updated: $current_ip" https://ntfy.sh/$NTFY_TOPIC
  fi
fi
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Cloudflare API reference, authentication methods, record types |
| `scripts/cf-dns.sh` | DNS record management helper script |
| `scripts/cf-settings.sh` | Zone settings management helper script |
| `examples/examples.md` | Example API calls, automation scripts, common patterns |

## Expected Outcomes

**Success:**
- DNS records listed successfully
- New records added and propagate within minutes
- Existing records updated correctly
- Deleted records removed from DNS
- Zone settings applied successfully
- Dynamic DNS updates working

**Partial Success:**
- Records created but propagation slow (normal, wait 5-10 minutes)
- Settings applied but not effective immediately (cache may need purging)

**Failure Indicators:**
- Authentication failed (403 errors)
- Zone ID not found
- Record already exists (can't add duplicate)
- Record not found (can't update/delete non-existent)

## Requirements

- Cloudflare account with temet.ai domain
- Cloudflare API token or Global API Key
- Zone ID for temet.ai
- curl and jq installed
- .env file with credentials
- Network access to Cloudflare API

## Red Flags to Avoid

- [ ] Do not use Global API Key if API Token suffices (security best practice)
- [ ] Do not commit API credentials to git (use .env)
- [ ] Do not delete records without confirmation (irreversible)
- [ ] Do not create duplicate records (causes DNS issues)
- [ ] Do not enable proxy on internal IPs (192.168.x.x) - won't work
- [ ] Do not set TTL < 60 seconds (Cloudflare minimum for free plans)
- [ ] Do not purge cache frequently (rate limits apply)

## Notes

- DNS propagation typically takes 1-5 minutes globally
- Cloudflare proxied records (orange cloud) hide real IP
- TTL of 1 means "Auto" (Cloudflare manages)
- Free plan limits: 1000 DNS records per zone
- API rate limits: 1200 requests per 5 minutes
- cf-dns.sh and cf-settings.sh scripts located in `scripts/` directory
- Use API Token over Global API Key (better security with scoped permissions)
- Zone settings changes may require cache purge to take effect immediately
- Dynamic DNS useful for home servers with changing IPs
- Cloudflare DNS is authoritative after migration from GoDaddy
- Use domain management system (`manage-domains.sh`) for service subdomains
- Use this skill for one-off DNS operations or non-service records
