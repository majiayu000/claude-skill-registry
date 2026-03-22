---
name: vaultkeeper
description: "Credential rotation reminders and API key hygiene monitoring. Tracks when credentials were last rotated, reminds you to update them, and scans for leaked keys. Use when: managing API keys, maintaining security hygiene, or rotating credentials regularly. NOT for: password management (use 1Password, Bitwarden), secrets management at scale (use Vault, AWS Secrets Manager), or compliance auditing."
homepage: https://pawhub.ai/vaultkeeper
metadata:
  {
    "openpaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["ssh"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/vaultkeeper",
              "bins": ["vaultkeeper"],
              "label": "Install VaultKeeper (npm)",
            },
          ],
      },
  }
---

# VaultKeeper 🔐

Never forget to rotate credentials again. Tracks API keys, SSH keys, tokens, and certificates. Reminds you before they expire or get stale.

## When to Use

✅ **USE when:**

- Managing API keys across services
- Rotating credentials regularly
- Tracking SSH key age
- Monitoring certificate expiration
- Maintaining security hygiene
- Scanning for leaked secrets
- Team credential management

## When NOT to Use

❌ **DON'T use when:**

- Password management → use 1Password, Bitwarden
- Enterprise secrets at scale → use HashiCorp Vault, AWS Secrets Manager
- Compliance auditing → use dedicated audit tools
- Secret scanning in CI/CD → use Gitleaks, TruffleHog
- Managing user passwords → use proper password managers

## Setup

```bash
npm install -g @pawhub/vaultkeeper
vaultkeeper init
```

## Example Interactions

**You:** Track my OpenAI API key

**Paw:** *securely adding credential*

✅ **Credential tracked:** OpenAI API Key

**Details:**
- Service: OpenAI
- Type: API Key
- Created: Today
- Last rotated: Today (new)
- Rotation policy: 90 days (recommended)

**I'll remind you to rotate:**
- 30 days before expiry (heads up)
- 7 days before expiry (urgent)
- Day of expiry (critical)

**Security check:**
- ✅ Not found in public GitHub repos
- ✅ Not in HaveIBeenPwned database
- ✅ Follows best practices (format, length)

**Want to set a custom rotation schedule?** (default is 90 days)

---

**You:** Set rotation to 60 days

**Paw:** ✅ **Rotation schedule updated**

**OpenAI API Key:**
- Rotation interval: 60 days
- Next rotation due: [Date]
- Reminder: [Date - 30 days]

I'll ping you 30 days before. You won't forget. 🔐

---

**Rotation reminder:**

**Paw:** 🔔 **Credential rotation due in 7 days**

**Service:** OpenAI API Key
**Created:** 53 days ago
**Rotation due:** In 7 days
**Last used:** 2 hours ago (active)

**Action needed:**
1. Generate new API key at platform.openai.com
2. Update in your apps/services
3. Test new key
4. Revoke old key
5. Mark as rotated in VaultKeeper

**Want a rotation checklist?** (I'll guide you through it)

---

**You:** Yes

**Paw:** **OpenAI API Key Rotation Checklist**

**Step 1: Generate New Key**
- [ ] Go to platform.openai.com/api-keys
- [ ] Click "Create new secret key"
- [ ] Copy new key immediately (shown once)

**Step 2: Update Services**
- [ ] Update .env files
- [ ] Update CI/CD secrets (GitHub Actions, etc.)
- [ ] Update production secrets (Railway, Vercel, etc.)
- [ ] Update local dev environments

**Step 3: Test**
- [ ] Test API calls with new key
- [ ] Verify all services still work
- [ ] Check error logs for auth failures

**Step 4: Revoke Old Key**
- [ ] Delete old key from OpenAI dashboard
- [ ] Confirm old key no longer works

**Step 5: Mark Complete**
- [ ] Run: `vaultkeeper rotate openai --confirm`

**Want me to track this checklist?** (I'll remind you of incomplete steps)

---

**You:** Yes, track it

**Paw:** ✅ **Rotation checklist active**

**Status:** 0/5 steps completed

I'll check in tomorrow to see how it's going. Reply with step numbers as you complete them.

Example: "done step 1" or "completed 1,2,3"

Let's get this key rotated safely. 🔐

---

**Next day:**

**Paw:** 🔔 **Rotation progress check: OpenAI API Key**

**Checklist:** 0/5 steps completed
**Due:** In 6 days

How's it going? Reply with completed steps.

---

**You:** Done steps 1-4

**Paw:** ✅ **Progress updated:** 4/5 steps completed

**Completed:**
- ✅ Generate new key
- ✅ Update services
- ✅ Test
- ✅ Revoke old key

**Remaining:**
- [ ] Mark complete in VaultKeeper

Ready to mark this rotation complete? (yes/no)

---

**You:** Yes

**Paw:** ✅ **Rotation complete!**

**OpenAI API Key:**
- Status: Rotated ✅
- Last rotation: Today
- Next rotation due: [60 days from now]

**Security posture:** Excellent 🔐

I'll remind you again in 30 days (60 days - 30 day reminder).

Good job staying secure. 🐾

---

**Leaked key alert:**

**Paw:** 🚨 **SECURITY ALERT: Potential leaked credential**

**Service:** GitHub Personal Access Token
**Severity:** CRITICAL

**Detection:**
- Found in public GitHub repo: yourusername/project-demo
- File: `config.json` (line 12)
- Exposed: ~2 hours ago
- Commit: `abc1234`

**Immediate actions needed:**
1. ⚠️ **REVOKE TOKEN NOW** (github.com/settings/tokens)
2. Remove from git history (`git filter-branch` or BFG)
3. Generate new token
4. Update services
5. Review recent account activity

**This is urgent.** That token is live and exposed publicly.

Want me to help you revoke it? 🚨

---

**You:** Help me revoke it

**Paw:** **Revoking GitHub token...**

**Option 1: Via GitHub CLI (fastest)**
```bash
gh api -X DELETE /authorizations/YOUR_TOKEN_ID
```

**Option 2: Web interface**
1. Go to github.com/settings/tokens
2. Find token (created [date])
3. Click "Delete"
4. Confirm deletion

**Option 3: I can do it** (requires GitHub auth)
Want me to revoke it via API? (yes/no)

---

**Weekly security digest:**

**Paw:** 🔐 **VaultKeeper Weekly Digest**

**Credentials tracked:** 12

**Status:**
- ✅ Up to date: 9
- ⚠️ Expiring soon: 2 (within 30 days)
- 🚨 Overdue: 1 (rotation missed)

**Action needed:**

**1. Stripe API Key (OVERDUE)**
- Last rotated: 127 days ago
- Policy: 90 days
- Status: 37 days overdue ⚠️

**2. AWS Access Key (expiring soon)**
- Rotation due: 12 days
- Reminder: Now

**3. SSH Key (server-prod) (expiring soon)**
- Rotation due: 28 days
- Reminder: Now

**Security scans:**
- ✅ No leaked credentials detected
- ✅ All keys follow best practices
- ✅ No suspicious activity

**Recommendation:**
Rotate the Stripe key ASAP (overdue). Then handle AWS and SSH before their deadlines.

Want rotation checklists for these? 🔐

## Commands

```bash
# Add credential
vaultkeeper add "Service Name" \
  --type api-key \
  --rotation 90d

# List all credentials
vaultkeeper list

# Show credential details
vaultkeeper show "Service Name"

# Mark as rotated
vaultkeeper rotate "Service Name" --confirm

# Check for leaks
vaultkeeper scan --leaked

# Security audit
vaultkeeper audit

# Export report
vaultkeeper report --format pdf
```

## Credential Types

```bash
# API Keys
vaultkeeper add "OpenAI" --type api-key --rotation 90d

# SSH Keys
vaultkeeper add "server-prod" --type ssh-key --rotation 180d

# OAuth Tokens
vaultkeeper add "GitHub PAT" --type oauth-token --rotation 365d

# Certificates
vaultkeeper add "SSL Cert" --type certificate --expiry 2026-12-31

# Database Passwords
vaultkeeper add "Postgres" --type db-password --rotation 30d

# Signing Keys
vaultkeeper add "JWT Secret" --type signing-key --rotation 180d
```

## Leak Detection

```bash
# Scan for leaked keys
vaultkeeper scan --leaked

# Scan specific service
vaultkeeper scan --leaked --service "OpenAI"

# Scan git history
vaultkeeper scan --git-history

# Scan specific repo
vaultkeeper scan --repo ~/projects/myapp

# Continuous monitoring
vaultkeeper monitor --enable
```

## Rotation Policies

```bash
# Set default rotation policy
vaultkeeper policy set --default 90d

# Service-specific policies
vaultkeeper policy set "Production DB" --rotation 30d

# Certificate monitoring
vaultkeeper policy set "SSL Certs" --expiry-warning 30d

# SSH key policies
vaultkeeper policy set "SSH Keys" --rotation 180d
```

## Team Management

```bash
# Add team member
vaultkeeper team add user@example.com

# Share credential responsibility
vaultkeeper share "AWS Keys" --with user@example.com

# Rotation assignments
vaultkeeper assign "Database Password" --to user@example.com

# Audit log
vaultkeeper audit-log --user user@example.com
```

## Telegram Integration

**Quick status:**

**You:** `/vault status`

**Paw:** **Credentials:** 12 tracked

✅ Up to date: 9
⚠️ Expiring soon: 2
🚨 Overdue: 1

React to details or `/vault list` for full breakdown.

---

**Rotation reminder:**

**Paw:** 🔔 **Rotation due:** OpenAI API Key (7 days)

Reply with:
- `/vault rotate openai` — Start checklist
- `/vault snooze 3d` — Remind in 3 days
- `/vault info openai` — Show details

---

**Leaked credential alert:**

**Paw:** 🚨 **LEAKED CREDENTIAL DETECTED**

**Service:** GitHub PAT
**Location:** Public repo
**Severity:** CRITICAL

⚠️ REVOKE NOW: github.com/settings/tokens

Reply `/vault help-revoke` for step-by-step guide.

## Security Features

### Leak Detection
- Scans public GitHub repos
- Checks HaveIBeenPwned database
- Monitors paste sites
- Analyzes git history
- Continuous monitoring mode

### Best Practices
- Warns about weak keys
- Suggests rotation intervals
- Enforces key format standards
- Tracks last used date
- Monitors access patterns

### Compliance
- Generates audit reports
- Tracks rotation history
- Team activity logs
- Policy enforcement
- Certificate monitoring

## Configuration

```bash
# Show config
vaultkeeper config show

# Default rotation interval
vaultkeeper config set default-rotation 90d

# Reminder timing
vaultkeeper config set reminder-advance 30d

# Notification channels
vaultkeeper config set notify telegram,email

# Leak scanning frequency
vaultkeeper config set scan-interval 24h

# Auto-scan on credential add
vaultkeeper config set auto-scan true
```

## Reports

```bash
# Security audit report
vaultkeeper report audit --format pdf

# Compliance report
vaultkeeper report compliance --format csv

# Rotation history
vaultkeeper report history --service "OpenAI"

# Team activity report
vaultkeeper report activity --month 2026-02
```

## Pricing

- **Free tier:** 5 credentials, basic reminders
- **Pro:** $10/month — unlimited credentials, leak scanning, team features
- **Team:** $29/month — 10 users, compliance reports, API access

Install: [pawhub.ai/vaultkeeper](https://pawhub.ai/vaultkeeper)

## Security & Privacy

- Credentials stored locally (encrypted at rest using AES-256)
- Optional cloud sync (E2E encrypted, zero-knowledge)
- Leak detection uses hashed/partial key matching (keys never sent in full)
- No credential values stored on servers
- Audit logs kept locally
- You can export/delete all data anytime

## Notes

- VaultKeeper tracks metadata, not the actual secrets
- Rotation is manual (VaultKeeper reminds, you execute)
- Leak detection scans public sources only
- Not a password manager (use 1Password, Bitwarden for that)
- Works alongside existing secret management tools
- Certificate expiry monitoring included
- SSH key rotation tracking supported

---

Stop using sticky notes for credential tracking. Let Paw remember for you. 🔐🐾
