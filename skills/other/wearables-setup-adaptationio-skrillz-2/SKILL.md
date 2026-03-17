---
name: wearables-setup
description: Samsung Galaxy Watch integration via Google Drive for Dr. Sophia AI. Covers Health Sync app setup, OAuth configuration, multi-user management, data sync verification. Use when setting up Samsung Health wearables, adding new users to wearables system, troubleshooting Samsung Health sync, or configuring Google Drive OAuth.
---

# Samsung Health Wearables Setup

## Overview

Guide for integrating Samsung Galaxy Watch data with Dr. Sophia AI using Google Drive and Health Sync app (bypassing Terra API limitations). This skill covers OAuth setup, multi-user management, and sync verification.

**Keywords**: Samsung Health, Galaxy Watch, wearables, Google Drive, Health Sync, OAuth, multi-user, data sync

**Status**: ✅ Fully implemented and working (User2: 33,636 steps tracked as of Sept 30, 2025)

## When to Use This Skill

- Setting up Samsung Health integration
- Adding new users to wearables system
- Troubleshooting sync issues
- Configuring Google Drive OAuth
- Verifying wearables data sync

## Quick Setup Overview

**Integration Method**: Google Drive + Health Sync App
**Why**: Bypasses Terra API SDK limitation (Samsung requires native SDK)
**Cost**: FREE (no Terra subscription needed)
**Sync Interval**: Every 5 minutes
**Setup Time**: 10 minutes per user (one-time)

## Architecture

```
Samsung Watch → Samsung Health App (phone)
     ↓
Health Sync App (automatic export)
     ↓
Google Drive (CSV/GPX files)
     ↓
Our Backend (OAuth API)
     ↓
Frontend Display (real-time updates)
```

## Quick Setup Steps

### 1. Install Health Sync App

On Android phone with Samsung Health:
- Install "Health Sync" app from Google Play
- Configure export to Google Drive
- Select metrics: Steps, Heart Rate, Sleep, Activities
- Set sync interval: 5 minutes

### 2. Configure Google Drive OAuth

Get OAuth credentials from Google Cloud Console:
- Create OAuth 2.0 Client ID
- Add authorized redirect URIs
- Download credentials JSON
- Extract client ID, client secret, refresh token

### 3. Add to Railway Environment

Add these to Railway backend service variables:

```bash
GOOGLE_CLIENT_ID=492699022293-fh2a1hhcvs96tbp6mub46f6fh2cvcr5e.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REFRESH_TOKEN_USER1=1//04ZHPrIbWyyQTCgYIARAAGAQSNwF-L9Ir...
USER1_NAME=Willie (Primary)
USER1_EMAIL=willie@adaptation.io
```

### 4. Verify Data Sync

```bash
# Check active users
curl http://localhost:8202/api/health-users

# Get user data
curl http://localhost:8202/api/health-data/user1

# Expected response: steps, HR, sleep data
```

## Multi-User Configuration

**Current Users**:

### User 1: Willie
- **Email**: willie@adaptation.io
- **Wearables Email**: willie@adaptation.io (SAME)
- **Sync**: Active
- **Last Verified**: Sept 29, 2025

### User 2: Dwayne
- **Supabase Email**: dwayne@drsophia.ai
- **Wearables Email**: dwayneboyes8341@gmail.com (DIFFERENT!)
- **Sync**: ✅ Active with fresh data (Sept 30, 2025)
- **Data**: 33,636 steps, 123 HR readings

**CRITICAL**: Dwayne has TWO different emails!
- Supabase/MediRecords: `dwayne@drsophia.ai`
- Wearables: `dwayneboyes8341@gmail.com`
- Stored in: `profiles.metadata.wearables_email` field

## Available Metrics

**Currently Tracking**:
- **Steps**: Daily count with calories
- **Heart Rate**: BPM readings with timestamps
- **Sleep**: Duration, stages (deep/REM/light)
- **Activities**: Type, distance, calories

**Data Format**: CSV/GPX files parsed by backend

## Backend Files

- `/backend/src/services/googleDriveHealthSync.js` - Core integration
- `/backend/multi-user-health-sync.js` - Multi-user management
- `/backend/src/services/userHealthManager.js` - Credential storage
- `/backend/parse-samsung-health.js` - CSV/GPX parser

## Frontend Components

- `/frontend/src/components/SamsungHealthDisplay.jsx` - UI display
- `/frontend/src/components/HealthUserManager.jsx` - User switching

## Quick Commands

```bash
# Start auto-sync (current user)
node health-sync-with-oauth.js

# List all users
node multi-user-health-sync.js list-users

# Add new user
node multi-user-health-sync.js add-user "Name" "email" "refresh_token"

# Switch active user
node multi-user-health-sync.js switch-user user2

# Parse latest data
node parse-samsung-health.js
```

## OAuth Setup Guide

For detailed OAuth flow and Google Cloud Console setup, see:

- **OAuth Setup**: [references/oauth-setup-guide.md](references/oauth-setup-guide.md)

## Verification

Check sync status:

```bash
curl http://localhost:8202/api/health-data/user1 | jq .

# Expected output:
{
  "steps": [...],
  "heartRate": [...],
  "sleep": [...],
  "activities": [...]
}
```

## Troubleshooting

**No data returned**:
- Check Railway environment variables set
- Verify refresh token not expired
- Check Health Sync app is running on phone

**Sync not updating**:
- Health Sync interval set to 5 minutes
- Check Google Drive has new files
- Verify OAuth credentials valid

**Wrong user data**:
- Check wearables_email field in Supabase
- Use correct user ID in API call (user1, user2)

## Terra API Status

**Why not using Terra**:
- Samsung Health requires native SDK
- Google Fit requires native SDK
- Terra web API doesn't support these without native app

**Solution**: Bypassed Terra completely using Google Drive API
**Result**: Full functionality without Terra subscription

---

**Integration**: Google Drive + Health Sync app
**Sync Frequency**: Every 5 minutes
**Cost**: FREE
**Setup Time**: 10 minutes per user
**Status**: Production-ready (Sept 30, 2025)
