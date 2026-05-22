---
name: cloudflare-access-troubleshoot
description: |
  Diagnoses and fixes Cloudflare Access authentication issues including Google OAuth
  errors, access denied after login, login loops, CookieMismatch errors, and "can only
  be used within its organization" errors. Use when authentication fails, access denied
  after Google login, redirect failures, or Pi-hole blocking Google domains. Triggers on
  "access denied", "OAuth not working", "login loop", "CookieMismatch", "can only be used
  within organization", or "fix Cloudflare Access authentication". Works with Cloudflare
  Access, Google OAuth, Pi-hole whitelist, and ACCESS_ALLOWED_EMAIL configuration.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Troubleshoot Cloudflare Access Authentication Skill

Systematic diagnosis and resolution of Cloudflare Access authentication issues including Google OAuth errors and access policy problems.

## Quick Start

Quick diagnostics for Access issues:

```bash
# Check allowed emails configured
grep ACCESS_ALLOWED_EMAIL /home/dawiddutoit/projects/network/.env

# Verify Google OAuth credentials set
grep GOOGLE_OAUTH /home/dawiddutoit/projects/network/.env

# Check if Google domains are whitelisted in Pi-hole
docker exec pihole pihole -q accounts.google.com
docker exec pihole pihole -q login.google.com

# Apply Google whitelist (fixes CookieMismatch)
/home/dawiddutoit/projects/network/scripts/setup-google-whitelist.sh
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Verify Google OAuth Configuration
   - 3.2 Check Allowed Email Configuration
   - 3.3 Verify Pi-hole Whitelist
   - 3.4 Test Google OAuth Consent Screen
   - 3.5 Check Access Policy in Dashboard
   - 3.6 Verify Redirect URI Configuration
   - 3.7 Apply Fix
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Access denied"
- "OAuth not working"
- "Login loop"
- "CookieMismatch error"
- "Can only be used within organization"
- "Fix Cloudflare Access"

**Implicit Triggers:**
- Google login succeeds but then shows "Access Denied"
- Redirected back to login after successful Google authentication
- Browser stuck in authentication loop
- "This app is not verified" but can't proceed

**Debugging Triggers:**
- "Why am I denied after login?"
- "Why is authentication not working?"
- "How to fix Google OAuth errors?"

## What This Skill Does

1. **Checks OAuth Config** - Verifies Google OAuth credentials are set
2. **Validates Emails** - Confirms allowed emails are configured
3. **Checks Whitelist** - Verifies Pi-hole not blocking Google domains
4. **Tests Consent** - Validates Google OAuth consent screen configuration
5. **Reviews Policy** - Checks Access policy in Cloudflare dashboard
6. **Verifies Redirect** - Confirms redirect URI matches team name
7. **Provides Fix** - Gives specific commands to resolve the issue

## Instructions

### 3.1 Verify Google OAuth Configuration

Check OAuth credentials are set:

```bash
# Check OAuth Client ID
grep GOOGLE_OAUTH_CLIENT_ID /home/dawiddutoit/projects/network/.env

# Check OAuth Client Secret
grep GOOGLE_OAUTH_CLIENT_SECRET /home/dawiddutoit/projects/network/.env
```

Expected: Both should show values (not empty)

**If missing:**

1. Go to Google Cloud Console: https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID if needed:
   - Application type: Web application
   - Authorized redirect URIs: `https://<TEAM_NAME>.cloudflareaccess.com/cdn-cgi/access/callback`
3. Copy Client ID and Client Secret
4. Add to .env:
```bash
GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```
5. Re-run Cloudflare Access setup:
```bash
/home/dawiddutoit/projects/network/scripts/cf-access-setup.sh setup
```

### 3.2 Check Allowed Email Configuration

Verify emails are configured:

```bash
grep ACCESS_ALLOWED_EMAIL /home/dawiddutoit/projects/network/.env
```

Expected: Shows comma-separated list of allowed email addresses

**If missing or incorrect:**

1. Edit .env:
```bash
nano /home/dawiddutoit/projects/network/.env
```

2. Add or update:
```bash
ACCESS_ALLOWED_EMAIL="your.email@gmail.com,other@gmail.com"
```

3. Update Access policies:
```bash
/home/dawiddutoit/projects/network/scripts/update-access-emails.sh
```

**Common mistake:** Email in policy doesn't match Google account used for login.

### 3.3 Verify Pi-hole Whitelist

Pi-hole must allow Google domains for OAuth to work:

**Check if Google domains are whitelisted:**
```bash
# Check essential auth domains
docker exec pihole pihole -q accounts.google.com
docker exec pihole pihole -q login.google.com
docker exec pihole pihole -q id.google.com
docker exec pihole pihole -q doubleclick.net
```

Expected: Each shows "Exact whitelist match"

**If blocked or not whitelisted:**

Apply Google/YouTube whitelist (automatic via docker-compose.yml pihole-init service):
```bash
/home/dawiddutoit/projects/network/scripts/setup-google-whitelist.sh
```

**Whitelisted domains include:**
- Authentication: `accounts.google.com`, `login.google.com`, `id.google.com`
- Cookie sync: `doubleclick.net`, `google-analytics.com`, `googlesyndication.com`
- YouTube: `youtube.com`, `googlevideo.com`, `ytimg.com`
- OAuth/API: `googleapis.com`, `gstatic.com`, `googleusercontent.com`

**After whitelisting:**
1. Clear browser cache and cookies for Google domains
2. Flush DNS cache on client device
3. Restart browser completely
4. Try authentication again

### 3.4 Test Google OAuth Consent Screen

Verify OAuth consent screen configuration:

1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Check "Publishing status"

**Common issue: "Can only be used within its organization"**

**Cause:** OAuth consent screen set to "Internal" but using personal Gmail account

**Fix:**
1. Click "Edit App"
2. Change "User Type" from "Internal" to "External"
3. Save and continue through wizard
4. Status should show "In production" or "Testing"

**If using External + Testing mode:**
- Add test users in "Test users" section
- Must include all ACCESS_ALLOWED_EMAIL addresses

### 3.5 Check Access Policy in Dashboard

Verify policy in Cloudflare Zero Trust:

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: Access → Applications
3. Find your application (e.g., "Pi-hole Access")
4. Click "Edit" → "Policies"

**Verify policy settings:**
- Action: "Allow"
- Include rule: "Emails" with your email addresses
- Or: "Emails ending in" with your domain

**Common issue:** Email in policy doesn't match exactly

**Example:**
- Policy has: `john.doe@gmail.com`
- Login uses: `johndoe@gmail.com`
- Result: Access denied (email mismatch)

**Fix:** Update policy to use correct email addresses:
```bash
/home/dawiddutoit/projects/network/scripts/update-access-emails.sh
```

### 3.6 Verify Redirect URI Configuration

OAuth redirect URI must match Cloudflare team name:

**Check team name:**
```bash
grep CLOUDFLARE_TEAM_NAME /home/dawiddutoit/projects/network/.env
```

**Verify redirect URI in Google Console:**

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth 2.0 Client ID
3. Check "Authorized redirect URIs"

**Expected:**
```
https://<TEAM_NAME>.cloudflareaccess.com/cdn-cgi/access/callback
```

**If mismatch:**

1. Update redirect URI in Google Console to match team name
2. Or re-run Access setup to sync:
```bash
/home/dawiddutoit/projects/network/scripts/cf-access-setup.sh setup
```

### 3.7 Apply Fix

**Fix A: Access Denied After Login**

**Symptoms:** Google login succeeds, then immediately shows "Access Denied"

**Causes:**
- Email not in ACCESS_ALLOWED_EMAIL
- Email in policy doesn't match login email

**Fix:**
```bash
# 1. Verify email configuration
grep ACCESS_ALLOWED_EMAIL /home/dawiddutoit/projects/network/.env

# 2. Update if needed
nano /home/dawiddutoit/projects/network/.env
# Add: ACCESS_ALLOWED_EMAIL="correct.email@gmail.com"

# 3. Update Access policies
/home/dawiddutoit/projects/network/scripts/update-access-emails.sh

# 4. Clear browser cookies
# Browser → Settings → Privacy → Clear browsing data → Cookies (*.cloudflareaccess.com)

# 5. Try again in incognito window
```

**Fix B: Login Loop**

**Symptoms:** Redirected back to login after successful authentication

**Causes:**
- Browser cookies blocked or cleared
- Pi-hole blocking Google domains
- Redirect URI mismatch

**Fix:**
```bash
# 1. Apply Google whitelist
/home/dawiddutoit/projects/network/scripts/setup-google-whitelist.sh

# 2. Clear all browser data
# Clear cache, cookies, and site data completely

# 3. Flush DNS cache
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder  # macOS
sudo systemd-resolve --flush-caches  # Linux

# 4. Restart browser completely

# 5. Try incognito window
```

**Fix C: CookieMismatch Error**

**Symptoms:** Error message about cookie mismatch during OAuth

**Cause:** Pi-hole blocking Google cookie sync domains

**Fix:**
```bash
# Apply Google whitelist
/home/dawiddutoit/projects/network/scripts/setup-google-whitelist.sh

# Verify domains whitelisted
docker exec pihole pihole -q doubleclick.net
docker exec pihole pihole -q google-analytics.com

# Clear browser cookies
# Browser → Settings → Clear browsing data

# Try again
```

**Fix D: "Can only be used within its organization"**

**Symptoms:** Error message when trying to authenticate

**Cause:** OAuth consent screen set to "Internal" with personal Gmail

**Fix:**
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Click "Edit App"
3. Change "User Type" from "Internal" to "External"
4. Click "Save and Continue" through wizard
5. Publish app if needed
6. Try authentication again

**Fix E: OAuth Redirect Failure**

**Symptoms:** Redirect fails or goes to wrong URL

**Cause:** Redirect URI doesn't match team name

**Fix:**
```bash
# 1. Get team name
grep CLOUDFLARE_TEAM_NAME /home/dawiddutoit/projects/network/.env

# 2. Update redirect URI in Google Console
# Go to: https://console.cloud.google.com/apis/credentials
# Update to: https://<TEAM_NAME>.cloudflareaccess.com/cdn-cgi/access/callback

# 3. Or re-run setup to sync
/home/dawiddutoit/projects/network/scripts/cf-access-setup.sh setup
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Google OAuth setup details, Access policy configuration |
| `examples/examples.md` | Example configurations, common error scenarios |

## Expected Outcomes

**Success:**
- Google OAuth login succeeds
- User redirected to protected service
- Access granted without "Access Denied"
- Session persists (no login loops)

**Partial Success:**
- Login works but shows "not verified" warning (cosmetic, can proceed)
- Authentication works in incognito but not regular browser (clear cookies)

**Failure Indicators:**
- Access Denied after successful Google login
- Login loops continuously
- CookieMismatch errors persist
- "Can only be used within organization" error
- Redirect to wrong URL

## Requirements

- Cloudflare Zero Trust account with Access configured
- Google Cloud Console project with OAuth 2.0 credentials
- Valid ACCESS_ALLOWED_EMAIL in .env
- Pi-hole with Google domains whitelisted
- Browser with cookies enabled

## Red Flags to Avoid

- [ ] Do not use "Internal" OAuth consent screen with personal Gmail accounts
- [ ] Do not block Google domains in Pi-hole (breaks OAuth)
- [ ] Do not skip clearing browser cookies after configuration changes
- [ ] Do not use email wildcards if specific emails intended (security risk)
- [ ] Do not test in same browser session (use incognito window)
- [ ] Do not forget to update both .env and Access policies
- [ ] Do not commit OAuth credentials to git

## Notes

- Google whitelist is automatically applied via pihole-init service in docker-compose.yml
- Access policies support wildcards: `*@yourdomain.com`
- Session duration default: 24 hours (configurable in Access policy)
- OAuth consent screen can show "not verified" warning (safe to proceed if you trust app)
- Redirect URI is case-sensitive and must exactly match team name
- Clear cookies for `*.cloudflareaccess.com` domain when troubleshooting
- Test authentication in incognito window to avoid cached sessions
- View Access logs: https://one.dash.cloudflare.com → Logs → Access
