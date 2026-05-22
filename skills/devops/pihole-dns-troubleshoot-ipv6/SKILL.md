---
name: pihole-dns-troubleshoot-ipv6
description: |
  Diagnoses and fixes IPv6 DNS issues causing clients to connect to Cloudflare OAuth
  instead of using local network access. Use when services show OAuth login prompt on
  local WiFi, slow initial connection followed by authentication, or Chrome shows "error
  with retry". Triggers on "connecting to Cloudflare instead of local", "OAuth prompt on
  WiFi", "IPv6 DNS issue", "clients prefer IPv6", "disable IPv6 DNS", or "fix local access".
  Works with Pi-hole FTLCONF_misc_dnsmasq_lines filter-AAAA configuration and client DNS
  cache management.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Troubleshoot IPv6 DNS Issues Skill

Systematic diagnosis and resolution of IPv6 DNS issues that cause clients to bypass local network access and connect via Cloudflare Tunnel with OAuth authentication.

## Quick Start

Diagnose IPv6 DNS issue:

```bash
# Check if client is getting IPv6 addresses (should show ONLY IPv4)
getent ahosts ha.temet.ai

# Check Pi-hole is blocking IPv6 DNS responses
docker exec pihole nslookup -query=AAAA ha.temet.ai 127.0.0.1

# Check filter-AAAA is configured
docker exec pihole env | grep FTLCONF_misc_dnsmasq_lines
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Understanding the Problem
   - 3.2 Verify IPv6 Filtering Configuration
   - 3.3 Test Pi-hole IPv6 Blocking
   - 3.4 Test Client DNS Resolution
   - 3.5 Clear Client DNS Cache
   - 3.6 Disable Browser DNS-over-HTTPS
   - 3.7 Verify Fix
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Connecting to Cloudflare instead of local"
- "OAuth prompt on local WiFi"
- "Services work but require authentication"
- "IPv6 DNS issue"
- "Clients prefer IPv6"

**Implicit Triggers:**
- Services show Cloudflare Access OAuth login on home WiFi
- Slow initial connection, then works after authentication
- Chrome shows "error with retry" then connects
- Services work remotely but require OAuth locally

**Debugging Triggers:**
- "Why am I seeing OAuth on local network?"
- "Why is local access slow?"
- "How to disable IPv6 DNS?"

## What This Skill Does

1. **Explains Problem** - Details how IPv6 DNS causes Cloudflare routing
2. **Verifies Config** - Checks FTLCONF_misc_dnsmasq_lines is set to filter-AAAA
3. **Tests Pi-hole** - Confirms Pi-hole blocks IPv6 DNS responses
4. **Tests Client** - Verifies client only receives IPv4 addresses
5. **Clears Cache** - Guides client-side DNS cache clearing
6. **Checks DoH** - Verifies browser DNS-over-HTTPS is disabled
7. **Confirms Fix** - Tests local access works without OAuth

## Instructions

### 3.1 Understanding the Problem

**Root Cause:**

Cloudflare DNS has both IPv4 and IPv6 records for tunnel hostnames:
- IPv4 (A record): `192.168.68.136` (local, from Pi-hole custom DNS)
- IPv6 (AAAA record): `2606:4700:...` (Cloudflare tunnel, from upstream CNAME)

When clients query for `*.temet.ai`, they receive both addresses. Modern clients prefer IPv6 → connect to Cloudflare → require OAuth authentication instead of using local network.

**Solution:**

Configure Pi-hole to block all IPv6 (AAAA) DNS responses using `filter-AAAA` directive, forcing clients to use IPv4 only.

### 3.2 Verify IPv6 Filtering Configuration

Check Pi-hole environment variable:

```bash
docker exec pihole env | grep FTLCONF_misc_dnsmasq_lines
```

Expected output:
```
FTLCONF_misc_dnsmasq_lines=filter-AAAA
```

**If missing or incorrect:**

1. Edit docker-compose.yml:
```bash
nano /home/dawiddutoit/projects/network/docker-compose.yml
```

2. Add/update under pihole service environment:
```yaml
FTLCONF_misc_dnsmasq_lines: "filter-AAAA"
```

3. Restart Pi-hole:
```bash
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d pihole
```

**Technical background:**
- Pi-hole v6 uses FTL (not dnsmasq directly)
- `FTLCONF_misc_dnsmasq_lines` injects dnsmasq config into FTL
- `filter-AAAA` blocks all IPv6 DNS responses

### 3.3 Test Pi-hole IPv6 Blocking

Verify Pi-hole blocks IPv6 DNS queries:

```bash
# Test single domain (should return "No answer" or no AAAA records)
docker exec pihole nslookup -query=AAAA ha.temet.ai 127.0.0.1

# Test all domains
for domain in pihole ha jaeger langfuse sprinkler code webhook; do
  echo "=== Testing $domain.temet.ai (AAAA) ==="
  docker exec pihole nslookup -query=AAAA $domain.temet.ai 127.0.0.1
  echo
done
```

Expected: "No answer" or empty response (no IPv6 addresses returned)

**If IPv6 addresses returned:**
- `filter-AAAA` not working
- Pi-hole FTL hasn't loaded configuration
- Wrong Pi-hole version (needs v6+)

### 3.4 Test Client DNS Resolution

From your computer/device:

```bash
# Check what addresses DNS returns (should show ONLY IPv4)
getent ahosts ha.temet.ai

# Or use dig
dig ha.temet.ai A
dig ha.temet.ai AAAA
```

**Expected:**
- `getent ahosts` shows only `192.168.68.136`
- `dig AAAA` returns no AAAA records or NOERROR with empty answer

**If IPv6 addresses appear (2606:4700:...):**
- Client has cached DNS from before filter-AAAA was applied
- Client is using DNS-over-HTTPS (bypassing Pi-hole)
- Client has manual DNS override

### 3.5 Clear Client DNS Cache

DNS cache persists for hours. Must clear after configuration changes.

**macOS:**
```bash
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```

**Linux (systemd-resolved):**
```bash
sudo systemd-resolve --flush-caches
```

**Linux (no systemd-resolved):**
Usually no DNS cache, or:
```bash
sudo service nscd restart  # If nscd installed
```

**Windows:**
```bash
ipconfig /flushdns
```

**Mobile devices:**
- iPhone/Android: Restart WiFi connection
- Or wait 5-60 minutes for cache to expire naturally

**After clearing cache:**
Wait 10-30 seconds, then re-test with `getent ahosts`.

### 3.6 Disable Browser DNS-over-HTTPS

Modern browsers can bypass local DNS entirely using DNS-over-HTTPS (DoH).

**Chrome/Edge:**
1. Settings → Privacy and security → Security
2. Scroll to "Use secure DNS"
3. Turn OFF (or select "With your current service provider")

**Firefox:**
1. Settings → Privacy & Security
2. Scroll to "DNS over HTTPS"
3. Select "Off" or "Default Protection"

**Safari:**
- Doesn't use DoH by default (no action needed)

**Verification:**
After disabling DoH, restart browser completely and re-test access.

### 3.7 Verify Fix

Test local access works without OAuth:

1. **Clear browser cookies** for `*.cloudflareaccess.com`
2. **Open incognito/private window** (avoids cached sessions)
3. **Navigate to service:** `https://ha.temet.ai`

**Expected:**
- Connects immediately without OAuth prompt
- Fast connection (<1 second)
- No redirect to Cloudflare Access

**If still seeing OAuth:**
- DNS cache not cleared
- Browser using DoH
- Wrong DNS server configured on client

Re-check steps 3.4, 3.5, and 3.6.

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | IPv6 DNS filtering technical details, FTL configuration |
| `examples/examples.md` | Example configurations, troubleshooting scenarios |

## Expected Outcomes

**Success:**
- Pi-hole blocks all IPv6 DNS responses
- Clients receive only IPv4 addresses (192.168.68.136)
- Local network access works without OAuth authentication
- Fast connection times (<1 second)

**Partial Success:**
- Configuration correct but clients have cached DNS (clear cache)
- Browser using DoH (disable and restart)

**Failure Indicators:**
- `getent ahosts` shows IPv6 addresses (2606:4700:...)
- Services still require OAuth on local WiFi
- Pi-hole returning IPv6 addresses

## Requirements

- Pi-hole v6+ using FTL DNS server
- Docker running with Pi-hole container
- FTLCONF_misc_dnsmasq_lines environment variable access
- Client device access to clear DNS cache

## Red Flags to Avoid

- [ ] Do not disable IPv6 at network level (breaks other services)
- [ ] Do not delete IPv6 DNS records in Cloudflare (needed for remote access)
- [ ] Do not skip clearing client DNS cache (changes won't take effect)
- [ ] Do not forget to check browser DNS-over-HTTPS settings
- [ ] Do not test in same browser tab (use incognito window)
- [ ] Do not expect instant propagation (DNS cache can persist 5-60 minutes)
- [ ] Do not use Pi-hole v5 or earlier (filter-AAAA requires FTL in v6+)

## Notes

- IPv6 filtering is network-wide (affects all clients)
- Cloudflare tunnel still uses IPv6 for remote access (this is correct)
- filter-AAAA only blocks IPv6 DNS responses, not IPv6 connectivity
- Client cache persistence varies: 5 minutes (Windows) to 60 minutes (mobile)
- DoH bypasses ALL local DNS settings (must be disabled)
- Configuration is persistent across Pi-hole restarts (stored in FTL config)
- Use domains.toml for automated DNS management, but IPv6 filtering is manual
