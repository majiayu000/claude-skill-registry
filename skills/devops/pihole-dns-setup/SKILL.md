---
name: pihole-dns-setup
description: |
  Configures Pi-hole local DNS records to enable local network resolution of *.temet.ai
  domains. Use when you need to set up DNS, add local DNS entries, configure Pi-hole DNS,
  troubleshoot DNS resolution, or make services resolve locally. Triggers on "setup DNS",
  "configure Pi-hole DNS", "add DNS record", "DNS not resolving", "local DNS setup", or
  "why can't I access [service].temet.ai locally". Works with Pi-hole container, domains.toml,
  docker-compose.yml, and manage-domains.sh.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Pi-hole DNS Setup Skill

Configure Pi-hole local DNS records for local network resolution of temet.ai domains.

## Quick Start

Run automated DNS setup from domains.toml:

```bash
cd /home/dawiddutoit/projects/network && ./scripts/manage-domains.sh apply
```

Or manually add a single DNS record:

```bash
# Get Pi IP
PI_IP=$(hostname -I | awk '{print $1}')

# Test DNS resolution
dig @localhost pihole.temet.ai +short
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Detect Pi IP Address
   - 3.2 Get Domains from Configuration
   - 3.3 Apply DNS Changes
   - 3.4 Verify DNS Resolution
   - 3.5 Router DNS Reminder
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## 1. When to Use This Skill

**Explicit Triggers:**
- "Set up Pi-hole DNS"
- "Configure local DNS"
- "Add DNS record for [domain]"
- "Set up DNS entries"
- "Make [service].temet.ai resolve locally"

**Implicit Triggers:**
- After adding a new service to domains.toml
- When local resolution fails for temet.ai domains
- Setting up a fresh Pi-hole installation
- Migrating services to new IP addresses

**Debugging Triggers:**
- "DNS not resolving"
- "Can't access [service].temet.ai on local network"
- "dig returns wrong IP"
- "Works remotely but not locally"

## 2. What This Skill Does

1. **Detects Pi IP** - Auto-discovers the Raspberry Pi's local IP address
2. **Reads Configuration** - Gets domain list from domains.toml
3. **Updates DNS** - Configures Pi-hole with local DNS entries via docker-compose.yml
4. **Verifies Resolution** - Tests DNS resolution works correctly
5. **Provides Guidance** - Reminds about router DNS configuration

## 3. Instructions

### 3.1 Detect Pi IP Address

Get the Pi's local IP automatically:

```bash
hostname -I | awk '{print $1}'
```

Expected output: `192.168.68.135` (or similar)

Alternative methods if needed:

```bash
# From network interface
ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'

# From Pi-hole container environment
docker exec pihole printenv | grep PIHOLE_INTERFACE
```

### 3.2 Get Domains from Configuration

Read domains from `domains.toml`:

```bash
# List all configured services with DNS entries
./scripts/manage-domains.sh list
```

Or parse directly:

```bash
grep -E "^subdomain = |^dns_ip = " /home/dawiddutoit/projects/network/domains.toml
```

**Current domains defined in domains.toml:**

| Service | Domain | DNS IP |
|---------|--------|--------|
| Pi-hole | pihole.temet.ai | 192.168.68.135 |
| Jaeger | jaeger.temet.ai | 192.168.68.135 |
| Langfuse | langfuse.temet.ai | 192.168.68.135 |
| Home Assistant | ha.temet.ai | 192.168.68.135 |
| Code Server | code.temet.ai | 192.168.68.135 |
| Sprinkler | sprinkler.temet.ai | 192.168.68.105 |
| Webhook | webhook.temet.ai | 192.168.68.135 |
| Root | temet.ai | 192.168.68.135 |

### 3.3 Apply DNS Changes

**Automated Method (Recommended):**

```bash
cd /home/dawiddutoit/projects/network && ./scripts/manage-domains.sh apply
```

This runs `generate-pihole-dns.py` which:
1. Reads domains.toml
2. Updates `FTLCONF_dns_hosts` in docker-compose.yml
3. Restarts Pi-hole to apply changes

**Manual DNS Entry (Single Domain):**

If you need to add a single entry without full apply:

```bash
# Edit docker-compose.yml FTLCONF_dns_hosts section
# Then restart Pi-hole
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart pihole
```

**How DNS Configuration Works:**

Pi-hole v6 uses `FTLCONF_dns_hosts` environment variable for custom DNS:

```yaml
environment:
  FTLCONF_dns_hosts: |
    192.168.68.135 pihole.temet.ai
    192.168.68.135 jaeger.temet.ai
    192.168.68.105 sprinkler.temet.ai
```

### 3.4 Verify DNS Resolution

After applying changes, verify DNS works:

**Test individual domain:**

```bash
dig @localhost pihole.temet.ai +short
# Expected: 192.168.68.135
```

**Test all configured domains:**

```bash
for domain in pihole jaeger langfuse ha code webhook; do
  echo -n "$domain.temet.ai -> "
  dig @localhost $domain.temet.ai +short
done
```

**Test from another device on the network:**

```bash
# Replace 192.168.68.135 with Pi's IP
dig @192.168.68.135 pihole.temet.ai +short
```

**Check Pi-hole DNS logs:**

```bash
docker exec pihole pihole -t
# Watch live DNS queries
```

### 3.5 Router DNS Reminder

**Important:** For DNS to work network-wide, configure your router:

1. Set router's DHCP to use Pi-hole as primary DNS:
   - Primary DNS: `192.168.68.135` (Pi's IP)
   - Secondary DNS: `1.1.1.1` (fallback)

2. Or configure each device individually to use Pi-hole DNS

**Verify device is using Pi-hole:**

```bash
# On the device, check what DNS server it's using
cat /etc/resolv.conf
# Should show: nameserver 192.168.68.135
```

## 4. Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | DNS configuration deep-dive, Pi-hole internals, troubleshooting |
| `examples/examples.md` | Common scenarios and configurations |
| `scripts/verify-dns.sh` | DNS verification script |

## 5. Expected Outcomes

**Success:**
- All domains resolve to correct IPs locally
- `dig @localhost domain.temet.ai` returns expected IP
- Services accessible at `https://domain.temet.ai` on local network

**Partial Success:**
- DNS works from Pi but not from other devices
- Cause: Router not configured to use Pi-hole as DNS

**Failure Indicators:**
- `dig` returns NXDOMAIN -> DNS entry not configured
- `dig` returns wrong IP -> Stale configuration
- Pi-hole not responding -> Container not running

## 6. Requirements

**Environment:**
- Pi-hole container running: `docker ps | grep pihole`
- Docker Compose available
- domains.toml configured

**Tools needed:**
- Read (configuration files)
- Bash (dig, docker commands)
- Grep (parsing domains)

## 7. Red Flags to Avoid

- [ ] Do not add DNS entries directly to Pi-hole web UI (use domains.toml)
- [ ] Do not forget to restart Pi-hole after config changes
- [ ] Do not skip the router DNS configuration reminder
- [ ] Do not use `127.0.0.1` as DNS IP (use actual Pi IP)
- [ ] Do not assume DNS propagates instantly (may take 1-2 minutes)
- [ ] Do not forget IoT devices may need different IPs (sprinkler -> 192.168.68.105)

## Notes

- DNS entries are stored in docker-compose.yml `FTLCONF_dns_hosts`
- The `generate-pihole-dns.py` script reads domains.toml and updates docker-compose.yml
- Local DNS resolution allows fast LAN access without internet roundtrip
- Remote access uses Cloudflare DNS (separate from Pi-hole)
- Always verify DNS after changes with `dig @localhost domain +short`
