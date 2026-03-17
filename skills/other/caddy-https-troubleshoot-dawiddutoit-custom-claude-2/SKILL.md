---
name: caddy-https-troubleshoot
description: |
  Diagnoses and fixes HTTPS/SSL certificate issues in the network infrastructure by checking
  API tokens, validating Caddy configuration, and testing certificates. Use when certificates
  are not obtained, HTTPS is not working, seeing SSL errors, "Invalid Authorization header",
  or Caddy restart loops. Triggers on "HTTPS not working", "SSL certificate issue", "certificate
  error", "Caddy not starting", "fix HTTPS", "troubleshoot certificates", or "Invalid format
  for Authorization header". Works with Caddy, Cloudflare DNS-01 challenge, and Let's Encrypt.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Troubleshoot HTTPS Skill

Systematic diagnosis and resolution of HTTPS/SSL certificate issues in the Caddy reverse proxy with Cloudflare DNS-01 challenge.

## Quick Start

Run the diagnostic script to identify issues:

```bash
/home/dawiddutoit/projects/network/.claude/skills/troubleshoot-https/scripts/diagnose-https.sh
```

Or follow the step-by-step diagnosis in [Instructions](#3-instructions).

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Check API Key Configuration
   - 3.2 Verify Cloudflare DNS Plugin
   - 3.3 Analyze Caddy Logs
   - 3.4 Validate Caddyfile Syntax
   - 3.5 Test Certificate Validity
   - 3.6 Diagnose Specific Error
   - 3.7 Apply Fix
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Common Error Reference](#6-common-error-reference)
7. [Requirements](#7-requirements)
8. [Red Flags to Avoid](#8-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "HTTPS not working"
- "SSL certificate error"
- "Certificate not obtained"
- "Caddy keeps restarting"
- "Fix HTTPS certificates"
- "Invalid format for Authorization header"

**Implicit Triggers:**
- Browser shows "Your connection is not private"
- Services accessible via HTTP but not HTTPS
- Caddy container in restart loop
- New domain not getting certificate

**Debugging Triggers:**
- "Why is my certificate expired?"
- "Why can't Caddy get a certificate?"
- "Cloudflare DNS challenge failing"

## What This Skill Does

1. **Checks API Key** - Verifies CLOUDFLARE_API_KEY is set and passed to container
2. **Verifies Plugin** - Confirms Cloudflare DNS plugin is compiled into Caddy
3. **Analyzes Logs** - Searches for certificate errors in Caddy logs
4. **Validates Config** - Tests Caddyfile syntax
5. **Tests Certificates** - Checks certificate validity for each domain
6. **Identifies Error** - Matches symptoms to known issues
7. **Provides Fix** - Gives specific commands to resolve the issue

## Instructions

### 3.1 Check API Key Configuration

**Step 1: Verify API key is set in .env**

```bash
grep "CLOUDFLARE_API_KEY" /home/dawiddutoit/projects/network/.env | head -1
```

Expected: `CLOUDFLARE_API_KEY="Xv5MOdOT...` (starts with alphanumeric, not `v4:`)

**Step 2: Verify API key is passed to container**

```bash
docker exec caddy env | grep CLOUDFLARE_API_KEY
```

Expected: Shows the API key value (not empty)

**If empty or missing:**
```bash
# Recreate container to pick up .env changes
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d --force-recreate caddy
```

**Key distinction:**
- API Token format: `Xv5MOdOT...` (alphanumeric string) - CORRECT
- Global API Key format: `v4:...` or long hex string - WRONG

### 3.2 Verify Cloudflare DNS Plugin

```bash
docker exec caddy caddy list-modules | grep cloudflare
```

Expected: `dns.providers.cloudflare`

**If not present:** Plugin not compiled into Caddy. Rebuild:

```bash
cd /home/dawiddutoit/projects/network && \
docker compose build --no-cache caddy && \
docker compose up -d --force-recreate caddy
```

### 3.3 Analyze Caddy Logs

**Check for certificate-related messages:**

```bash
docker logs caddy 2>&1 | grep -i -E "certificate|error|failed|invalid" | tail -30
```

**Look for success messages:**

```bash
docker logs caddy 2>&1 | grep "certificate obtained successfully"
```

Expected for each domain: `certificate obtained successfully {"identifier": "domain.temet.ai"}`

### 3.4 Validate Caddyfile Syntax

```bash
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
```

Expected: `Valid configuration` (no errors)

**If syntax error:**
1. Read the Caddyfile to identify the error
2. Fix the syntax issue
3. Reload Caddy

### 3.5 Test Certificate Validity

**Test a single domain:**

```bash
echo | openssl s_client -servername pihole.temet.ai -connect pihole.temet.ai:443 2>/dev/null | openssl x509 -noout -dates -issuer
```

Expected output:
```
notBefore=<date>
notAfter=<date>
issuer=C = US, O = Let's Encrypt, CN = R3
```

**Test all domains:**

```bash
for domain in pihole jaeger langfuse sprinkler ha; do
  echo "=== $domain.temet.ai ==="
  echo | openssl s_client -servername $domain.temet.ai -connect $domain.temet.ai:443 2>/dev/null | \
    openssl x509 -noout -dates 2>&1 || echo "FAILED to get certificate"
  echo
done
```

### 3.6 Diagnose Specific Error

Match error message to diagnosis:

| Error Message | Diagnosis | Go to Fix |
|---------------|-----------|-----------|
| `Invalid format for Authorization header` | Using Global API Key instead of API Token | Fix A |
| `missing API token` | Environment variable not set | Fix B |
| `unknown directive 'dns'` | Cloudflare plugin not compiled | Fix C |
| `certificate obtain error` | Rate limit or DNS propagation | Fix D |
| `403 Forbidden` from Cloudflare | API token lacks permissions | Fix E |
| Container restart loop | Caddyfile syntax error | Fix F |

### 3.7 Apply Fix

**Fix A: Wrong API Key Type**

The error "Invalid format for Authorization header" means you're using the Global API Key instead of an API Token.

1. Create new API Token:
   - Go to: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"
   - Select template: "Edit zone DNS"
   - Zone Resources: Include -> Specific zone -> temet.ai
   - Click "Continue to summary" -> "Create Token"

2. Update .env:
   ```bash
   # Edit .env and replace CLOUDFLARE_API_KEY with the new token
   nano /home/dawiddutoit/projects/network/.env
   ```

3. Recreate Caddy:
   ```bash
   docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d --force-recreate caddy
   ```

4. Verify:
   ```bash
   docker logs caddy 2>&1 | grep "certificate obtained successfully"
   ```

**Fix B: Environment Variable Not Set**

1. Verify .env has the key:
   ```bash
   grep CLOUDFLARE_API_KEY /home/dawiddutoit/projects/network/.env
   ```

2. Verify docker-compose.yml passes it:
   ```bash
   grep -A5 "caddy:" /home/dawiddutoit/projects/network/docker-compose.yml | grep CLOUDFLARE
   ```

3. Recreate container:
   ```bash
   docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d --force-recreate caddy
   ```

**Fix C: Cloudflare Plugin Not Compiled**

```bash
cd /home/dawiddutoit/projects/network && \
docker compose build --no-cache caddy && \
docker compose up -d --force-recreate caddy
```

Build takes approximately 5 minutes on Raspberry Pi.

**Fix D: Rate Limit or DNS Propagation**

1. Wait 5 minutes for DNS propagation
2. Restart Caddy:
   ```bash
   docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart caddy
   ```

3. If still failing, check Let's Encrypt rate limits:
   - Limit: 50 certificates per domain per week
   - Check: https://crt.sh/?q=temet.ai

**Fix E: API Token Missing Permissions**

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Find your token and click "Edit"
3. Verify permissions:
   - Zone -> DNS -> Edit (required)
   - Zone Resources -> Include -> Specific zone -> temet.ai
4. If missing, create new token with correct permissions

**Fix F: Caddyfile Syntax Error**

1. Check error in logs:
   ```bash
   docker logs caddy 2>&1 | tail -50
   ```

2. Validate Caddyfile:
   ```bash
   docker exec caddy caddy validate --config /etc/caddy/Caddyfile
   ```

3. Common syntax issues:
   - Missing closing braces `}`
   - Invalid directive names
   - Wrong environment variable syntax

4. Fix the Caddyfile and reload:
   ```bash
   docker exec caddy caddy reload --config /etc/caddy/Caddyfile
   ```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Complete error reference, API token creation guide, rate limit details |
| `scripts/diagnose-https.sh` | Automated diagnostic script |

## Expected Outcomes

**Success:**
- All diagnostic checks pass
- `certificate obtained successfully` for each domain
- HTTPS working with valid Let's Encrypt certificates
- Certificate shows issuer: `C = US, O = Let's Encrypt`

**Partial Success:**
- Issue identified but fix requires manual action (e.g., create new API token)
- Certificate pending (DNS propagation in progress)

**Failure Indicators:**
- API key format is wrong (Global API Key vs API Token)
- Cloudflare plugin not compiled into Caddy
- Caddyfile syntax errors blocking startup
- Let's Encrypt rate limit exceeded

## Common Error Reference

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| `Invalid format for Authorization header` | Wrong API key type (Global vs Token) | Create new API Token with "Edit zone DNS" template |
| `missing API token` | Env var not passed to container | `docker compose up -d --force-recreate caddy` |
| `unknown directive 'dns'` | Plugin not compiled | `docker compose build --no-cache caddy` |
| `certificate obtain error` | Rate limit or DNS delay | Wait 5 minutes, restart Caddy |
| `403 Forbidden` | Token lacks DNS edit permission | Check/update token permissions |
| Container restart loop | Caddyfile syntax error | Check logs, fix syntax, reload |

## Requirements

- Docker running with Caddy container
- Valid Cloudflare API Token with "Edit zone DNS" permission
- `.env` file with `CLOUDFLARE_API_KEY` set
- Internet access for Cloudflare API calls

## Red Flags to Avoid

- [ ] Do not use Global API Key (format: `v4:...` or long hex) - use API Token instead
- [ ] Do not skip verifying the plugin is compiled before troubleshooting further
- [ ] Do not delete caddy_data volume unless absolutely necessary (certificates stored there)
- [ ] Do not exceed Let's Encrypt rate limits (50 certs/domain/week)
- [ ] Do not forget to recreate container after .env changes
- [ ] Do not use `--no-verify` to bypass certificate errors
- [ ] Do not commit API tokens to git

## Notes

- Certificates are stored in Docker volume `network_caddy_data`
- Certificates auto-renew 30 days before expiry
- DNS-01 challenge allows certificates for internal-only services
- Caddy checks renewals every 12 hours
- Build with `--no-cache` if plugin changes aren't taking effect
- API Token (not Global API Key) is required for Caddy Cloudflare DNS plugin
