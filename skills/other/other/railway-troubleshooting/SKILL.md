---
name: railway-troubleshooting
description: Railway Docker cache troubleshooting for Dr. Sophia AI deployments. Covers cache detection, force rebuild methods, version verification, deployment validation. Use when Railway shows old code after deployment, deployments not updating, Docker cache issues, or version mismatches between local and deployed code.
---

# Railway Docker Cache Troubleshooting

## Overview

Guide for detecting and fixing Railway's aggressive Docker caching that can cause old code to deploy even after pushing new changes. This skill provides quick fixes to force rebuilds and verify deployments.

**Keywords**: Railway, Docker cache, deployment issues, force rebuild, version mismatch, cache busting, Dockerfile, Railway dashboard

## When to Use This Skill

- Railway shows old code after deployment
- New features not appearing despite successful deploy
- Version mismatch (local vs deployed)
- Railway build logs show "CACHED" everywhere
- Console logs show old version numbers

## Quick Detection

Check if Railway is serving old code:

```bash
# 1. Check local version
grep "BACKEND_VERSION" backend/backend-proxy-enhanced-current.js

# 2. Check deployed version
curl https://backend-dev-d231.up.railway.app/health | jq .version

# If versions don't match = CACHE PROBLEM!
```

## Symptoms of Cache Problem

- ✅ Railway build logs show "Using cache" or "CACHED" for most steps
- ✅ `/health` endpoint returns old version number
- ✅ New features/fixes not working despite successful deployment
- ✅ Console logs show old version (e.g., v11.4 when you pushed v11.6.1)
- ✅ Railway dashboard shows "Deployed" but code behavior hasn't changed

## Force Rebuild Methods

### Method 1: Update Dockerfile Timestamp (RECOMMENDED)

**Fastest** - Takes 30 seconds:

```bash
# Edit Dockerfile.unified
# Update the timestamp comment at the top:

# Dr. Jarvis Unified Backend Docker Image
# Force rebuild: Oct 24, 2025 1:30 PM - Fix xyz feature  # <-- Update this line

git add Dockerfile.unified
git commit -m "build: Force Railway rebuild - bypass cache"
git push origin dev
```

**Or use the automated script**:
```bash
.claude/skills/railway-troubleshooting/scripts/force-rebuild.sh
```

### Method 2: Update Multiple Version References

**More thorough** - Updates version everywhere:

```bash
# 1. Update version in backend file (line ~1066)
BACKEND_VERSION = '13.2.8';  # Increment version

# 2. Update console banner
console.log('🔥 DR. JARVIS UNIFIED BACKEND v13.2.8 🔥');

# 3. Update /health endpoint
app.get('/health', (req, res) => {
  res.json({
    version: '13.2.8',  # Update this
    ...
  });
});

# 4. Update Dockerfile comment (as in Method 1)

# 5. Commit all changes
git add -A
git commit -m "build: Force Railway rebuild - v13.2.8"
git push origin dev
```

### Method 3: Railway Dashboard Manual Rebuild

**Last resort** - Slowest:

1. Go to Railway Dashboard → Your Service
2. Click Settings → Redeploy
3. Select "Redeploy without cache"
4. Wait for complete rebuild from scratch

## Deployment Verification Checklist

After pushing, **ALWAYS** verify the deployment:

```bash
# 1. Wait for Railway to build/deploy (2-3 minutes)
sleep 180

# 2. Check deployed version
curl -s https://backend-dev-d231.up.railway.app/health | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Deployed Version: {data.get(\"version\")}')
print(f'Status: {data.get(\"status\")}')
"

# 3. If wrong version, force rebuild using Method 1
```

## Prevention Best Practices

1. **Always update version numbers** in both code AND Dockerfile comment
2. **Verify deployment** using /health endpoint after every push
3. **Use timestamp comments** in Dockerfile to force rebuilds
4. **Monitor Railway build logs** - too much "CACHED" = potential problem
5. **Test critical features** immediately after deployment

## Quick Fix One-Liner

Use this to instantly force a rebuild:

```bash
echo "# Force rebuild: $(date '+%Y-%m-%d %H:%M')" >> Dockerfile.unified && \
git add Dockerfile.unified && \
git commit -m "build: Force Railway rebuild - bypass cache" && \
git push origin dev
```

## Automated Script

Run the force rebuild script:

```bash
.claude/skills/railway-troubleshooting/scripts/force-rebuild.sh
```

This automatically:
- Adds timestamp to Dockerfile
- Commits changes
- Pushes to Railway
- Initiates rebuild

## Real Example (Sep 24, 2025)

**Problem**: Prescription PDF button wasn't appearing
**Root Cause**: Railway cached old v11.4, wouldn't deploy new v11.6.1
**Solution**: Updated Dockerfile comment + version numbers everywhere
**Result**: Forced complete rebuild, new code deployed successfully
**Time Wasted**: 2+ hours debugging a non-existent code issue

## Railway Build Log Analysis

Look for these in Railway build logs:

### Good Signs ✅
```
Step 1/10 : FROM node:20-alpine
Step 2/10 : WORKDIR /app
Step 3/10 : COPY package*.json ./
```

### Warning Signs ⚠️
```
Step 3/10 : COPY package*.json ./
 ---> Using cache  # Too much of this = problem
Step 4/10 : RUN npm install
 ---> Using cache
```

If > 70% of steps show "Using cache", force rebuild!

---

**Prevention**: Update Dockerfile comment with every push
**Detection**: Check /health endpoint version
**Quick Fix**: Automated force-rebuild script
**Last Updated**: September 24, 2025
