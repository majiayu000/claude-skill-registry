---
name: deployment-guide
description: Complete deployment guide for Dr. Sophia AI on Railway. Covers environment-aware build system, frontend dist/ compilation, backend auto-deploy, Railway configuration, troubleshooting build/deployment issues. Use when deploying to Railway, building frontend for production, debugging deployment failures, or setting up environment variables.
---

# Railway Deployment Guide

## Overview

Complete guide for deploying Dr. Sophia AI to Railway with environment-aware builds, proper dist/ compilation, and backend auto-deployment. This skill covers the critical differences between frontend and backend deployment workflows.

**Keywords**: Railway deployment, build process, environment configuration, dist folder, production deployment, frontend build, backend deploy, npm run build

## When to Use This Skill

- Deploying frontend to Railway
- Deploying backend to Railway
- Building dist/ folder for production
- Debugging deployment failures
- Setting up environment variables
- Troubleshooting Railway issues

## Critical Deployment Fact

🚨 **FRONTEND**: Railway deploys the pre-built `dist/` folder, NOT source files!
- Changing `/frontend/src/*.jsx` alone = ❌ NO DEPLOYMENT
- Must run `npm run build` + commit `dist/` = ✅ DEPLOYMENT

✅ **BACKEND**: Railway deploys directly from source (NO build step needed)

## Frontend Deployment Process

### Step 1: Make Changes
```bash
# Edit frontend source files
nano frontend/src/ModernApp.jsx
```

### Step 2: Build (MANDATORY!)
```bash
cd frontend
npm run build  # Auto-detects branch, builds for correct environment
```

**What This Does:**
- Detects current git branch (dev/main/prototype)
- Sets correct backend URL automatically
- Creates optimized dist/ folder (~55KB)
- Includes password protection
- Injects API keys from .env

### Step 3: Verify Build
```bash
ls -lh dist/assets/*.css  # Must be ~60KB (not 9KB!)
ls -lh dist/assets/*.js   # Must be ~450KB
```

### Step 4: Commit & Deploy
```bash
git add -A                  # Includes BOTH src/ and dist/
git commit -m "feat: your changes"
git push origin dev         # Railway auto-deploys from dist/
```

## Backend Deployment Process

### Step 1: Make Changes
```bash
# Edit backend files
nano backend/backend-proxy-enhanced-current.js
```

### Step 2: Commit & Deploy (That's It!)
```bash
git add backend/
git commit -m "fix: backend improvement"
git push origin dev         # Railway auto-deploys from source
```

**No build step required** - Backend runs directly from source.

## Environment Detection

Build script automatically detects branch and configures backend URL:

| Branch | Frontend URL | Backend URL |
|--------|--------------|-------------|
| **dev** | frontend-dev-8670.up.railway.app | backend-dev-d231.up.railway.app |
| **main** | botaniqal-medtech-frontend.up.railway.app | backend-production-5c38.up.railway.app |
| **prototype** | frontend-prototype.up.railway.app | backend-prototype.up.railway.app |

**Override if needed:**
```bash
BUILD_ENV=production npm run build  # Force specific environment
```

## Deployment Checklist

### Frontend Deployment
- [ ] Run `npm run build` from frontend/ directory
- [ ] Verify CSS is ~60KB (not 9KB = Tailwind not working)
- [ ] Verify JS is ~450KB
- [ ] `git add -A` (include dist/ folder!)
- [ ] Commit with descriptive message
- [ ] Push to Railway (auto-deploys)
- [ ] Wait 2-3 minutes for build/deploy
- [ ] Verify deployment at Railway URL

### Backend Deployment
- [ ] Edit backend files
- [ ] `git add backend/`
- [ ] Commit changes
- [ ] Push to Railway (auto-deploys)
- [ ] Railway rebuilds automatically
- [ ] No build step needed

## Common Deployment Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| Frontend changes don't appear | Forgot to build dist/ | Run `npm run build` |
| dist/ not deployed | Forgot `git add dist/` | `git add -A` includes dist/ |
| CSS broken (tiny file) | Wrong build command | Use `npm run build` (not `npm run build:vite`) |
| Voice feature not working | Missing API keys in dist/config.js | Rebuild with `npm run build` |
| Backend points to wrong URL | Built on wrong branch | Check git branch before building |

## Detailed Documentation

For environment configuration, build troubleshooting, and Railway setup, see:

- **Environment Config**: [references/environment-config.md](references/environment-config.md)
- **Build Troubleshooting**: [references/build-troubleshooting.md](references/build-troubleshooting.md)
- **Railway Configuration**: [references/railway-config.md](references/railway-config.md)

## Verification Script

Run post-deployment verification:
```bash
.claude/skills/deployment-guide/scripts/verify-deployment.sh dev
```

Expected output:
```
✅ Backend health check passed
✅ Version matches: v13.2.7
✅ API keys configured
```

## Quick Reference

### Frontend Build Commands
```bash
cd frontend
npm run build          # Environment-aware (recommended)
BUILD_ENV=dev npm run build     # Force dev environment
BUILD_ENV=production npm run build  # Force production
```

### Backend Version Check
```bash
# Check deployed version
curl https://backend-dev-d231.up.railway.app/health | jq .version

# Should match local version
grep "BACKEND_VERSION" backend/backend-proxy-enhanced-current.js
```

### Railway Dashboard
- **Dev Frontend**: https://railway.app/project/frontend-dev-8670
- **Dev Backend**: https://railway.app/project/backend-dev-d231
- **Prod Frontend**: https://railway.app/project/botaniqal-medtech-frontend
- **Prod Backend**: https://railway.app/project/backend-production-5c38

---

**Build System**: Environment-aware (auto-detects branch)
**Deployment**: Git push triggers Railway auto-deploy
**Last Updated**: September 21, 2025
