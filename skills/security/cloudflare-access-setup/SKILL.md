---
name: cloudflare-access-setup
description: |
  Configures Cloudflare Access authentication with Google OAuth for protected services.
  Use when you need to set up authentication, configure Google OAuth, protect services
  with Cloudflare Access, enable remote access security, or troubleshoot Access issues.
  Triggers on "setup cloudflare access", "configure access authentication", "enable google
  oauth", "protect services", "fix access denied", "add users to access", or "why can't I
  login remotely". Works with cf-access-setup.sh, .env OAuth credentials, and Cloudflare
  Zero Trust dashboard.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Cloudflare Access Setup Skill

Configure Cloudflare Access with Google OAuth to protect services with secure authentication.

## Quick Start

To set up Cloudflare Access authentication:

```bash
# 1. Verify prerequisites
./scripts/cf-access-setup.sh list

# 2. If OAuth credentials missing, configure .env first (see Section 3.2)

# 3. Run automated setup
./scripts/cf-access-setup.sh setup
```

After setup, test by visiting https://pihole.temet.ai - you should see Google login.

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Verify Prerequisites
   - 3.2 Configure Google OAuth (if needed)
   - 3.3 Run Automated Setup
   - 3.4 Verify Applications Created
   - 3.5 Test Authentication Flow
   - 3.6 Access Monitoring
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Integration Points](#6-integration-points)
7. [Requirements](#7-requirements)
8. [Red Flags to Avoid](#8-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Set up Cloudflare Access"
- "Configure Google OAuth for access"
- "Protect my services with authentication"
- "Enable remote access authentication"
- "Run cf-access-setup"

**Implicit Triggers:**
- Setting up a new service that needs protection
- First-time infrastructure setup
- After adding new services to domains.toml

**Debugging Triggers:**
- "I get Access Denied when accessing services"
- "Google login isn't working"
- "Can't access pihole remotely"
- "OAuth redirect error"
- "Session expired errors"

## What This Skill Does

1. **Verifies Prerequisites** - Checks OAuth credentials exist in .env
2. **Guides OAuth Setup** - Provides Google Console instructions if credentials missing
3. **Runs Automation** - Executes cf-access-setup.sh to configure everything
4. **Creates Applications** - Sets up Access apps for all protected services
5. **Configures Policies** - Creates allow policies for authorized users
6. **Tests Authentication** - Verifies Google login flow works
7. **Provides Monitoring** - Shows access logs URL for audit trail

## Instructions

### 3.1 Verify Prerequisites

Check required environment variables:

```bash
cd /home/dawiddutoit/projects/network && source .env && echo "Checking OAuth credentials..."
[ -n "$GOOGLE_OAUTH_CLIENT_ID" ] && echo "GOOGLE_OAUTH_CLIENT_ID: Set" || echo "GOOGLE_OAUTH_CLIENT_ID: MISSING"
[ -n "$GOOGLE_OAUTH_CLIENT_SECRET" ] && echo "GOOGLE_OAUTH_CLIENT_SECRET: Set" || echo "GOOGLE_OAUTH_CLIENT_SECRET: MISSING"
[ -n "$ACCESS_ALLOWED_EMAIL" ] && echo "ACCESS_ALLOWED_EMAIL: $ACCESS_ALLOWED_EMAIL" || echo "ACCESS_ALLOWED_EMAIL: MISSING"
[ -n "$CLOUDFLARE_ACCESS_API_TOKEN" ] && echo "CLOUDFLARE_ACCESS_API_TOKEN: Set" || echo "CLOUDFLARE_ACCESS_API_TOKEN: MISSING"
```

If any are missing, proceed to 3.2. Otherwise, skip to 3.3.

### 3.2 Configure Google OAuth (if needed)

Guide the user through Google Console setup:

**Step 1: Access Google Cloud Console**
- URL: https://console.cloud.google.com/apis/credentials
- Sign in with the Google Workspace account (e.g., dawiddutoit@temet.ai)

**Step 2: Create OAuth Consent Screen** (if first time)
- User Type: **Internal** (for organization only) or **External** (for personal Gmail)
- App name: "Cloudflare Access - Home Network"
- Support email: Your email
- Developer contact: Your email

**Step 3: Create OAuth Client ID**
- Click "Create Credentials" -> "OAuth client ID"
- Application type: **Web application**
- Name: "Cloudflare Access - Home Network"
- Authorized redirect URI: `https://temetai.cloudflareaccess.com/cdn-cgi/access/callback`
- Click "Create"

**Step 4: Update .env**
```bash
GOOGLE_OAUTH_CLIENT_ID=<client-id>.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=<client-secret>
ACCESS_ALLOWED_EMAIL=your-email@domain.com
```

### 3.3 Run Automated Setup

Execute the setup script:

```bash
cd /home/dawiddutoit/projects/network && ./scripts/cf-access-setup.sh setup
```

The script will:
1. Verify all prerequisites
2. Configure Google OAuth identity provider
3. Create Access applications for protected services
4. Create allow policies for authorized users
5. Create bypass policy for webhook

**Protected Services:**
- pihole.temet.ai
- jaeger.temet.ai
- langfuse.temet.ai
- sprinkler.temet.ai
- ha.temet.ai
- temet.ai (root)

**Bypass Service:**
- webhook.temet.ai (no auth for GitHub)

### 3.4 Verify Applications Created

List all configured applications:

```bash
./scripts/cf-access-setup.sh list
```

Expected output shows all services with App IDs and session durations.

### 3.5 Test Authentication Flow

**Manual Test:**
1. Open incognito/private browser window
2. Navigate to: https://pihole.temet.ai
3. Expected: Redirect to Cloudflare Access login page
4. Click "Google" to authenticate
5. Sign in with authorized email
6. After authentication: Access to Pi-hole admin

**CLI Test (webhook bypass):**
```bash
curl -I https://webhook.temet.ai/hooks/health
# Should return HTTP response without authentication
```

**Verify unauthorized access blocked:**
- Try accessing with different Google account
- Should see "Access Denied" message

### 3.6 Access Monitoring

**Access Logs Dashboard:**
https://one.dash.cloudflare.com -> Logs -> Access

**View information:**
- Who accessed which service
- Timestamp of access attempts
- Allow/deny decisions
- Source IP addresses

**Quick command to show dashboard URL:**
```bash
echo "Access Logs: https://one.dash.cloudflare.com"
echo "Navigate to: Logs -> Access"
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Complete API reference, troubleshooting guide, advanced configuration |
| `examples/examples.md` | Common scenarios and configuration examples |

## Expected Outcomes

**Success:**
- Google OAuth identity provider configured
- Access applications created for all protected services
- Allow policies set for authorized email(s)
- Bypass policy configured for webhook
- Authentication flow working (Google login redirects)
- Access logs visible in Cloudflare dashboard

**Partial Success:**
- Applications created but OAuth not working (check redirect URI)
- Some services missing (re-run setup - idempotent)

**Failure Indicators:**
- "Missing GOOGLE_OAUTH_CLIENT_ID" -> Configure .env first
- "Missing CLOUDFLARE_ACCESS_API_TOKEN" -> Create API token
- API errors -> Check token permissions
- Redirect loop -> Clear cookies and retry

## Integration Points

**Cloudflare Tunnel:**
- Access works with existing tunnel configuration
- Tunnel routes traffic, Access provides authentication layer

**domains.toml:**
- Services with `require_auth = true` should have Access applications
- Run after adding new services: `./scripts/cf-access-setup.sh setup`

**manage-domains.sh:**
- Automatically syncs Access applications via sync-cloudflare-access.py
- Use `./scripts/manage-domains.sh apply` for full sync

## Requirements

**Environment Variables (in .env):**
- GOOGLE_OAUTH_CLIENT_ID - From Google Console
- GOOGLE_OAUTH_CLIENT_SECRET - From Google Console
- ACCESS_ALLOWED_EMAIL - Email(s) to authorize
- CLOUDFLARE_ACCESS_API_TOKEN - API token with Zero Trust permissions
- CLOUDFLARE_ACCOUNT_ID - Cloudflare account ID
- CLOUDFLARE_TEAM_NAME - Zero Trust team name

**API Token Permissions:**
- Account -> Zero Trust -> Edit
- Account -> Access: Apps and Policies -> Edit
- Account -> Access: Organizations, Identity Providers, and Groups -> Edit

**Tools:**
- Bash (for running setup script)
- Read (for checking .env and script output)

## Red Flags to Avoid

- [ ] Do not run setup without verifying OAuth credentials exist
- [ ] Do not use wrong redirect URI (must match exactly)
- [ ] Do not set consent screen to "Internal" if using personal Gmail accounts
- [ ] Do not delete webhook bypass policy (breaks GitHub deployments)
- [ ] Do not forget to test in incognito (cached sessions cause confusion)
- [ ] Do not skip verifying applications were created
- [ ] Do not ignore "Access Denied" errors (check allowed emails)
- [ ] Do not expose API tokens in logs or output

## Notes

- Setup script is idempotent - safe to run multiple times
- OAuth redirect URI must be exactly: `https://temetai.cloudflareaccess.com/cdn-cgi/access/callback`
- Session duration is 24 hours by default
- Multiple emails can be authorized: `ACCESS_ALLOWED_EMAIL="email1@domain.com,email2@domain.com"`
- Local network access bypasses Cloudflare Access (only remote access requires auth)
- Pi-hole may block Google domains needed for OAuth - whitelist if issues occur
