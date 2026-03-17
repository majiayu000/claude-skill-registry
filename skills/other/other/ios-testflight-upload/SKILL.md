---
description: Build, archive, upload iOS app to TestFlight, auto-distribute to external testers, submit for Beta App Review, and update server version. Full automated pipeline via App Store Connect API.
---

# iOS TestFlight Upload & Distribution

## Overview

Fully automated TestFlight deployment:
1. Syncs tunable constants
2. Increments build number
3. Builds and archives the iOS app
4. Exports for App Store
5. Uploads to App Store Connect
6. Waits for Apple processing
7. Adds build to external beta group and submits for Beta App Review
8. Updates server's LATEST_BUILD from Apple's confirmed build number

## When to Use

Invoke this skill when the user:
- Asks to "upload to TestFlight"
- Wants to "deploy to TestFlight"
- Says "push a new build" or "send to beta testers"
- Mentions uploading for beta testing

## Prerequisites

- Xcode installed with valid signing identity
- App Store Connect Admin API key at `~/.appstoreconnect/private_keys/AuthKey_TF37RTPFSZ.p8`
- ExportOptions.plist configured in the iOS project directory
- Python 3 with `requests` module installed
- SSH access to microserver@185.96.221.52 (for server version update)

## Quick Method (Recommended)

Run the consolidated Python script:

```bash
cd /Users/asnaroo/Desktop/experiments/miso/apps/firefly/product/client/imp/ios
python3 testflight-deploy.py
```

This script performs all 8 steps automatically:
1. **sync_tunables()** - Syncs live-constants.json to iOS bundle
2. **increment_build_number()** - Bumps build number via agvtool
3. **build_and_archive()** - Archives with xcodebuild
4. **export_for_app_store()** - Exports IPA with ExportOptions.plist
5. **upload_to_testflight()** - Uploads via altool
6. **wait_for_processing()** - Polls Apple API until build is VALID
7. **distribute_to_testers()** - Adds to beta group, submits for review, returns confirmed build number
8. **update_server_version()** - Updates remote server's LATEST_BUILD via SSH

**Key feature:** The build number is read back from Apple's API (not assumed from local state), ensuring the server version is always accurate.

## Expected Output

```
============================================================
TestFlight Deployment Pipeline
============================================================
Working directory: /Users/asnaroo/Desktop/experiments/miso/apps/firefly/product/client/imp/ios

============================================================
Step 1: Syncing tunables
============================================================
   Synced live-constants.json to iOS bundle

============================================================
Step 2: Incrementing build number
============================================================
   New build number: 18

============================================================
Step 3: Building and archiving
============================================================
   Archive complete

============================================================
Step 4: Exporting for App Store
============================================================
   Export complete

============================================================
Step 5: Uploading to TestFlight
============================================================
   Uploading... (this may take a minute)
   Upload complete

============================================================
Step 6: Waiting for Apple to process build 18
============================================================
   (This typically takes 5-15 minutes)
   Status: PROCESSING (elapsed: 0s)
   Status: PROCESSING (elapsed: 30s)
   Status: VALID (elapsed: 60s)
   Build is ready!

============================================================
Step 7: Distributing to external testers
============================================================
   Getting beta groups...
   Target group: marylebone test group
   Getting latest build from Apple...
   Latest build: 18
   Adding build to marylebone test group...
   Build added to group
   Checking beta review status...
   Submitted! Status: APPROVED
   Distribution complete!

============================================================
Step 8: Updating server version to 18
============================================================
   Restarting server...
   Verifying...
   Server now reports build 18

============================================================
Deployment Complete!
============================================================
Build 18 is now available to external testers.
Server version updated to 18.
```

## How External TestFlight Distribution Works

External testers (unlike internal team members) require builds to go through **Beta App Review**:

1. **Upload** - Build appears in App Store Connect with "Processing" status
2. **Processing complete** - Build state becomes "VALID"
3. **Add to group** - Build associated with external beta group
4. **Submit for review** - Creates `betaAppReviewSubmission` via API
5. **Review** - Apple reviews (first build: up to 24h, subsequent: usually auto-approved in minutes)
6. **Approved** - Build appears in TestFlight app on testers' devices

## Common Issues

**"Missing Compliance" resolved:**
- Info.plist includes `ITSAppUsesNonExemptEncryption = false`
- Compliance popup no longer appears

**"Invalid bundle - orientations":**
- Add UISupportedInterfaceOrientations to Info.plist with all orientations

**Authentication failed (401) for upload:**
- Verify Issuer ID is correct: `2e5cbf08-b1a5-4857-b013-30fb6eec002e`
- Verify API key file exists at `~/.appstoreconnect/private_keys/AuthKey_TF37RTPFSZ.p8`

**Build number already exists:**
- The script auto-increments, but if needed: `agvtool next-version -all`

**Distribution fails:**
- Check build is in VALID state (not still processing)
- Ensure external beta group exists in App Store Connect

**Build shows "Ready to Submit" (yellow) instead of "Testing":**
- This means Beta App Review submission is missing
- Run the script again - it will submit for review
- First review may take up to 24 hours; subsequent builds are usually auto-approved

**Server version update fails:**
- Check SSH access: `ssh microserver@185.96.221.52 "echo ok"`
- Manually update: edit `~/firefly-server/.env` and restart server

## Timing

- Sync tunables: ~1 second
- Increment build: ~1 second
- Archive: ~10-15 seconds
- Export: ~5 seconds
- Upload: ~5-30 seconds depending on size
- **Local subtotal: ~30 seconds to 1 minute**
- Apple processing: ~5-15 minutes
- Distribution + review submission: ~2 seconds
- Server update: ~3 seconds
- Beta App Review: minutes (if previously approved) to 24 hours (first time)

## API Credentials

- **Admin Key (for REST API):** TF37RTPFSZ
- **Issuer ID:** 2e5cbf08-b1a5-4857-b013-30fb6eec002e
- **Key Path:** `~/.appstoreconnect/private_keys/AuthKey_TF37RTPFSZ.p8`

**Important:** The REST API requires tokens generated by `altool --generate-jwt`, not PyJWT. The script handles this automatically.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `testflight-deploy.py` | Full pipeline (build + upload + wait + distribute + review + server update) |
| `sync-tunables.sh` | Sync live-constants.json from source of truth |

**Deprecated scripts (kept for reference):**
- `testflight-deploy.sh` - Old bash script, replaced by Python version
- `distribute-testflight.py` - Old distribution-only script, now integrated

## API Endpoints Used

- `GET /v1/apps` - Find app by bundle ID
- `GET /v1/apps/{id}/betaGroups` - List beta groups
- `GET /v1/builds` - Get latest build (used to confirm build number from Apple)
- `POST /v1/betaGroups/{id}/relationships/builds` - Add build to group
- `GET /v1/builds/{id}/betaAppReviewSubmission` - Check review status
- `POST /v1/betaAppReviewSubmissions` - Submit for Beta App Review
