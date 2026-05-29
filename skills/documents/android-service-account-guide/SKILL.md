---
name: android-service-account-guide
description: Step-by-step guide for creating Google Cloud service account for Play Store API access
category: android
version: 1.0.0
inputs:
  - package_name: Android app package name
outputs:
  - Service account JSON (user downloads manually)
  - Documentation: distribution/PLAY_CONSOLE_SETUP.md
verify: "User confirms service account created"
---

# Android Service Account Guide

Step-by-step guide for creating a Google Cloud service account with Play Store API access. This is a manual process with documentation.

## Prerequisites

- Google Play Developer account ($25 one-time)
- Google Cloud Platform account (free)
- Admin access to Play Console

## Process

### Step 1: Create Documentation

Create `distribution/PLAY_CONSOLE_SETUP.md`:

```markdown
# Google Play Console Setup

Complete guide for setting up service account and API access.

## Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "Android App Deployment"
4. Click "Create"
5. Wait for project creation (30 seconds)

## Step 2: Create Service Account

1. In Cloud Console, go to: IAM & Admin → Service Accounts
2. Click "Create Service Account"
3. Name: `playstore-deploy`
4. Description: "Automated Play Store deployment"
5. Click "Create and Continue"
6. Skip role assignment (click "Continue")
7. Click "Done"

## Step 3: Create Service Account Key

1. Find your service account in the list
2. Click ⋮ (three dots) → "Manage keys"
3. Click "Add Key" → "Create new key"
4. Select "JSON"
5. Click "Create"
6. **CRITICAL:** Save the downloaded JSON file securely
   - Store in password manager
   - Never commit to git
   - This is your only copy!

## Step 4: Enable Play Developer API

1. In Cloud Console, go to: APIs & Services → Library
2. Search: "Google Play Android Developer API"
3. Click on it
4. Click "Enable"
5. Wait for activation (30 seconds)

## Step 5: Link to Play Console

1. Go to: https://play.google.com/console/
2. Select your app
3. Go to: Setup → API access
4. Click "Link a Google Cloud project"
5. Select your project from dropdown
6. Click "Link"

## Step 6: Grant Service Account Access

1. Still in Play Console → API access
2. Find your service account in "Service accounts" section
3. Click "Grant access"
4. Check: "Release to production, exclude devices, and use Play App Signing"
5. Click "Apply"
6. Click "Invite user"

## Step 7: Verify Setup

Service account email format:
`playstore-deploy@PROJECT_ID.iam.gserviceaccount.com`

✅ Checklist:
- [ ] Service account created
- [ ] JSON key downloaded and stored securely
- [ ] Play Developer API enabled
- [ ] Cloud project linked to Play Console
- [ ] Service account has "Release" permission
- [ ] Permissions have propagated (wait 5-10 minutes)

## Security Notes

🔒 **Service Account JSON:**
- Contains sensitive credentials
- Store in password manager
- Never commit to version control
- Rotate keys annually
- One key per environment (dev/prod)

🔒 **Permissions:**
- Grant minimum required permissions only
- Review access logs regularly
- Revoke unused accounts
- Use 2FA on Google account
```

### Step 2: Guide User Through Process

**Interactive guidance:**
1. Ask: "Do you have a Google Play Developer account?"
2. Ask: "What is your app's package name?"
3. Display the step-by-step instructions
4. Wait for user confirmation at each major step
5. Verify service account email format

**No automated actions** - this skill is pure documentation and guidance.

### Step 3: Create GitHub Secrets Documentation

Create `distribution/GITHUB_SECRETS.md`:

```markdown
# GitHub Secrets Setup

Add these secrets to your GitHub repository for automated deployment.

## Required Secrets

Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

### 1. SERVICE_ACCOUNT_JSON_PLAINTEXT

**Value:** Entire plaintext contents of the JSON file downloaded in service account setup (not base64 encoded)

**How to add:**
1. Open the service account JSON file
2. Copy entire contents (including { and })
3. Paste as secret value
4. Click "Add secret"

### 2. SIGNING_KEY_STORE_BASE64

**Value:** Base64-encoded production keystore

**How to create:**
```bash
base64 -w 0 keystores/production-release.jks
# OR on macOS:
base64 -i keystores/production-release.jks
```

### 3. SIGNING_KEY_ALIAS

**Value:** `upload` (from KEYSTORE_INFO.txt)

### 4. SIGNING_STORE_PASSWORD

**Value:** Production keystore password (from KEYSTORE_INFO.txt)

### 5. SIGNING_KEY_PASSWORD

**Value:** Production key password (same as store password for PKCS12)

## Verification

After adding secrets:
1. Go to: Repository → Settings → Secrets and variables → Actions
2. Verify all 5 secrets are listed
3. Secrets are encrypted and cannot be viewed after creation
4. Use workflow runs to verify secrets work

## Security Notes

- Never log secret values
- Rotate SERVICE_ACCOUNT_JSON_PLAINTEXT annually
- Keep KEYSTORE_INFO.txt secure (not in git)
- Use environment protection for production deployments
```

## Verification

**User confirmation required:**

Ask user to confirm:
- [ ] Service account created in Google Cloud
- [ ] JSON key downloaded and stored in password manager
- [ ] Play Developer API enabled
- [ ] Service account linked to Play Console
- [ ] Service account has "Release" permission
- [ ] Waited 5-10 minutes for permissions to propagate

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Setup guide | distribution/PLAY_CONSOLE_SETUP.md | Complete setup instructions |
| Secrets guide | distribution/GITHUB_SECRETS.md | GitHub Secrets documentation |
| Service account JSON | User's secure storage | Downloaded by user manually |

## Troubleshooting

### "Cannot create service account"
**Cause:** Billing not enabled
**Fix:** Link billing account in Google Cloud (API is free)

### "Service account not appearing in Play Console"
**Cause:** Propagation delay
**Fix:** Wait 1-2 minutes, refresh page, clear browser cache

### "API enable button grayed out"
**Cause:** Wrong project selected or insufficient permissions
**Fix:** Verify project selection, check you have Owner/Editor role

## Completion Criteria

- [ ] distribution/PLAY_CONSOLE_SETUP.md created
- [ ] distribution/GITHUB_SECRETS.md created
- [ ] User confirms service account created
- [ ] User confirms JSON key downloaded and secured
- [ ] User confirms permissions granted in Play Console
