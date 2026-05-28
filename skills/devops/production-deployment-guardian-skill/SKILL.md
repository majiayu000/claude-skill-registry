---
name: production-deployment-guardian
description: Prevents production deployment failures through pre-deployment validation and environment-specific configuration checks. Use before ANY production deployment to catch CORS misconfigurations, trust proxy issues, environment variable mismatches, and missing production URLs. Based on real production incidents from PDFLab v1.1.0-v1.1.1 deployments.
---

# Production Deployment Guardian

**Mission:** Prevent production deployment disasters by validating environment-specific configurations, CORS settings, reverse proxy requirements, and production URLs BEFORE deployment. Catches issues that cause 100% service outages in production.

**Historical Context**: Created after v1.1.1 emergency hotfix (Nov 9, 2025) - CORS and trust proxy misconfigurations caused 15-minute production outage affecting 100% of users.

---

## Activation Triggers

- **MANDATORY: Before EVERY production deployment**
- Deploying to new environment (staging, production)
- Changing server infrastructure (adding Nginx, CloudFlare, etc.)
- Updating CORS configuration
- Switching domains (development → production)
- After infrastructure changes
- "CORS error" in production
- "Not allowed by CORS" errors
- Rate limiting not working
- Wrong client IPs in logs

---

## 🔴 CRITICAL: Pre-Deployment Validation Checklist (MANDATORY)

**Run this checklist BEFORE EVERY production deployment. Non-negotiable.**

### Phase 1: CORS Configuration (Critical - Blocks Authentication)

**Historical Failure**: v1.1.0 deployed without production domain in CORS origins → 100% authentication failure → v1.1.1 emergency hotfix in 15 minutes

```bash
# Step 1: List ALL CORS origins in your server configuration
□ Verify localhost:3000 (development)
□ Verify localhost:3002 (alternative dev port if used)
□ ✅ MANDATORY: Verify https://pdflab.pro (PRODUCTION)
□ ✅ MANDATORY: Verify http://pdflab.pro (HTTP fallback)
□ Verify https://staging.pdflab.pro (if staging exists)
□ Check CORS_ORIGIN environment variable
□ Verify CORS middleware applied BEFORE routes

# Step 2: Inspect server.ts CORS configuration code
□ Open backend/src/server.ts
□ Find CORS configuration section
□ Verify production domain explicitly listed
□ Verify no "process.env.NODE_ENV === 'development'" bypass in production

# Step 3: Test CORS from production domain (BEFORE DEPLOYMENT)
□ Use curl to test CORS preflight request
□ Check browser DevTools Network tab
□ Verify "Access-Control-Allow-Origin" header present
□ Test actual API call from production domain
```

**Real Production Issue (Nov 9, 2025):**

```typescript
// ❌ BROKEN: v1.1.0 - Missing production domain
const corsOrigins = process.env['CORS_ORIGIN']?.split(',') || [
  'http://localhost:3000',
  'http://localhost:3002'
  // ❌ MISSING: 'https://pdflab.pro'
]

app.use(cors({
  origin: (origin, callback) => {
    if (corsOrigins.includes(origin) || process.env.NODE_ENV === 'development') {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))  // ← BLOCKS PRODUCTION
    }
  }
}))

// Deployment Impact:
// - Time: Nov 9, 2025 19:50 UTC
// - Error: "Error: Not allowed by CORS" (500 status)
// - User Impact: 100% authentication blocked
// - Downtime: 15 minutes until v1.1.1 hotfix
// - Root Cause: Production domain not in CORS origins

// ✅ FIXED: v1.1.1 - Production domains included
const corsOrigins = process.env['CORS_ORIGIN']?.split(',') || [
  'http://localhost:3000',
  'http://localhost:3002',
  'https://pdflab.pro',      // ✅ ADDED
  'http://pdflab.pro'        // ✅ ADDED
]

app.use(cors({
  origin: (origin, callback) => {
    if (corsOrigins.includes(origin)) {  // ← Removed dev bypass
      callback(null, true)
    } else {
      console.warn(`[CORS] Blocked request from origin: ${origin}`)
      callback(new Error('Not allowed by CORS'))
    }
  },
  credentials: true
}))

// Result: Production working, authentication successful
```

**CORS Testing Commands:**

```bash
# Test CORS preflight from production domain
curl -H "Origin: https://pdflab.pro" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type,Authorization" \
     -X OPTIONS \
     https://pdflab.pro/api/auth/login

# Expected response (SUCCESS):
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://pdflab.pro
Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
Access-Control-Allow-Headers: Content-Type,Authorization
Access-Control-Allow-Credentials: true

# Failed response (BLOCKED):
HTTP/1.1 500 Internal Server Error
# No CORS headers present

# Test actual API call from production
curl -X POST https://pdflab.pro/api/auth/login \
     -H "Origin: https://pdflab.pro" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test123"}'

# Should NOT return: "Error: Not allowed by CORS"
```

---

### Phase 2: Express Trust Proxy Configuration (Critical - Breaks Rate Limiting)

**Historical Failure**: v1.1.0 trust proxy not enabled → Rate limiter ValidationError → rate limiting broken in production

```bash
# Step 1: Identify if deployment is behind reverse proxy
□ Check if using Nginx (YES → requires trust proxy)
□ Check if using Apache (YES → requires trust proxy)
□ Check if using CloudFlare (YES → requires trust proxy)
□ Check if using AWS ALB/ELB (YES → requires trust proxy)
□ Check if direct to internet (NO → do NOT enable trust proxy)

# Step 2: Verify trust proxy enabled in server.ts
□ Open backend/src/server.ts
□ Find: app.set('trust proxy', true)
□ Verify it's called IMMEDIATELY after Express app creation
□ Verify it's called BEFORE rate limiting middleware

# Step 3: Verify rate limiting configuration
□ Check express-rate-limit configuration
□ Verify no ValidationError in logs
□ Test rate limiting works with X-Forwarded-For header

# Step 4: Verify correct client IPs in logs
□ Check server logs for client IPs
□ Should show real client IPs, not proxy IP (e.g., not 172.x.x.x)
```

**Real Production Issue (Nov 9, 2025):**

```typescript
// ❌ BROKEN: v1.1.0 - Trust proxy not enabled
const app = express()
// ❌ MISSING: app.set('trust proxy', true)

// Rate limiter configuration
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
})
app.use('/api/', apiLimiter)

// Production Error:
// ValidationError: The 'X-Forwarded-For' header is set but the Express
// 'trust proxy' setting is false

// Impact:
// - Rate limiting broken in production
// - Logs show Nginx proxy IP instead of real client IPs
// - All users treated as same IP address
// - Rate limits applied incorrectly

// ✅ FIXED: v1.1.1 - Trust proxy enabled
const app = express()
app.set('trust proxy', true)  // ✅ ADDED - Must be BEFORE rate limiting

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false
})
app.use('/api/', apiLimiter)

// Result: Rate limiting working correctly
```

**Trust Proxy Verification:**

```bash
# Check if Nginx sets X-Forwarded headers
curl -I https://pdflab.pro/api/health
# Look for: X-Forwarded-For, X-Forwarded-Proto, X-Forwarded-Host

# Test rate limiting works (should succeed)
for i in {1..5}; do curl https://pdflab.pro/api/health; done

# Check server logs for correct client IPs
docker logs pdflab-backend-prod --tail 100 | grep "Client IP"
# Should show real IPs like: 102.x.x.x, 197.x.x.x
# Should NOT show: 172.x.x.x (Docker network IP)
```

---

### Phase 3: Environment Variable Validation

```bash
# Step 1: Compare .env files (dev vs production)
□ List all environment variables in .env
□ Verify production has equivalent values
□ Check for hardcoded localhost references
□ Verify all API keys are production keys (not sandbox)

# Step 2: Critical environment variables for production
□ NODE_ENV=production (NOT development)
□ CORS_ORIGIN includes production domain(s)
□ Database host is production host (not localhost)
□ Redis host is production host (not localhost)
□ CloudConvert: CLOUDCONVERT_SANDBOX=false
□ PayFast: Production merchant ID (not 10000100)
□ JWT_SECRET is strong and unique (not default)

# Step 3: Verify no localhost references
grep -r "localhost" backend/src/ --exclude-dir=node_modules
# Should return zero results in production code
```

**Environment Variable Matrix:**

| Variable | Development | Staging | Production |
|----------|-------------|---------|------------|
| **NODE_ENV** | development | staging | **production** |
| **CORS_ORIGIN** | localhost:3000 | staging.pdflab.pro | **https://pdflab.pro** |
| **Trust Proxy** | false | **true** | **true** |
| **DB_HOST** | localhost | docker-hostname | docker-hostname |
| **REDIS_HOST** | localhost | docker-hostname | docker-hostname |
| **CLOUDCONVERT_SANDBOX** | true | true | **false** |
| **PAYFAST_MERCHANT_ID** | 10000100 | 10000100 | **25263515** |
| **SSL** | none | Let's Encrypt | Let's Encrypt |

---

### Phase 4: Production URL Validation

```bash
# Step 1: Search codebase for hardcoded URLs
□ grep -r "localhost" --exclude-dir=node_modules
□ grep -r "127.0.0.1" --exclude-dir=node_modules
□ grep -r "http://" backend/src/ (should use https in prod)

# Step 2: Verify all URLs point to production
□ CORS origins → https://pdflab.pro
□ Return URLs → https://pdflab.pro/api/payfast/return
□ Webhook URLs → https://pdflab.pro/api/payfast/webhook
□ Frontend API calls → https://pdflab.pro

# Step 3: Test all public-facing URLs
□ curl https://pdflab.pro (should return 200)
□ curl https://pdflab.pro/api/health (should return 200)
□ Test in browser with DevTools Network tab
```

---

### Phase 5: Post-Deployment Smoke Tests (MANDATORY)

**Run these tests IMMEDIATELY after deployment:**

```bash
# Test 1: Frontend loads
□ Open https://pdflab.pro in browser
□ Check for no CORS errors in console (F12)
□ Verify page loads completely

# Test 2: Authentication works
□ Navigate to https://pdflab.pro/login
□ Attempt login with test user
□ Check Network tab for CORS errors
□ Verify login succeeds (not 500 error)

# Test 3: API endpoints respond
□ curl https://pdflab.pro/api/health
□ Should return: 200 OK with {"status":"healthy"}

# Test 4: Rate limiting works
□ Make 10 requests to API endpoint
□ Should NOT see ValidationError
□ Should NOT see CORS errors

# Test 5: Check server logs
□ docker logs pdflab-backend-prod --tail 50
□ Look for: "Not allowed by CORS" warnings
□ Look for: ValidationError from rate limiter
□ Look for: Correct client IPs (not Docker IPs)
```

**If ANY test fails → ROLLBACK IMMEDIATELY**

---

## 🟡 Pre-Deployment Checklist (Full Version)

### Infrastructure Verification

- [ ] **Server Access**: Can SSH to production server
- [ ] **Docker Running**: `docker ps` shows all containers
- [ ] **Disk Space**: At least 5GB free (`df -h`)
- [ ] **Database Backup**: Created backup within last hour
- [ ] **Previous Images**: Old Docker images saved for rollback

### Code Review

- [ ] **TypeScript Compiles**: `npm run typecheck` passes (zero errors)
- [ ] **Tests Pass**: All tests passing locally
- [ ] **No Console Logs**: No debug console.log() in production code
- [ ] **Error Handling**: All async operations have try-catch
- [ ] **Git Clean**: No uncommitted changes

### Configuration Review

- [ ] **CORS Origins**: Production domain(s) included
- [ ] **Trust Proxy**: Enabled if behind reverse proxy
- [ ] **Environment Variables**: All production values set
- [ ] **API Keys**: Production keys (not sandbox)
- [ ] **Secrets Secure**: No secrets in code or logs

### Deployment Preparation

- [ ] **Docker Images Built**: Latest images built and tagged
- [ ] **Images Pushed**: Pushed to Docker Hub
- [ ] **Database Migration**: Tested locally, rollback script ready
- [ ] **Rollback Plan**: Documented procedure for rolling back
- [ ] **Team Notified**: Team aware of deployment

### Post-Deployment

- [ ] **Smoke Tests**: All 5 smoke tests pass
- [ ] **Logs Checked**: No errors in server logs
- [ ] **Monitoring**: Sentry receiving events (if configured)
- [ ] **Documentation**: Deployment report created
- [ ] **Team Notified**: Deployment success confirmed

---

## 🚨 Emergency Rollback Procedure

**If deployment causes production issues:**

### Step 1: Assess Impact (30 seconds)

```bash
# Check if site is accessible
curl https://pdflab.pro/api/health

# Check recent errors in logs
docker logs pdflab-backend-prod --tail 100 | grep -i error
```

### Step 2: Decide to Rollback (if any of these true)

- [ ] 100% of users cannot authenticate
- [ ] Site returns 500 errors
- [ ] CORS errors blocking all API calls
- [ ] Database connection failures
- [ ] Payment processing broken

### Step 3: Execute Rollback (2-3 minutes)

```bash
# Stop new containers
docker stop pdflab-backend-prod pdflab-frontend-prod
docker rm pdflab-backend-prod pdflab-frontend-prod

# Start previous working containers
docker run -d --name pdflab-backend-prod \
  --network app_pdflab-network \
  --restart unless-stopped \
  -p 3006:3006 \
  [environment variables...] \
  mkelam/pdflab-backend:previous-tag

docker run -d --name pdflab-frontend-prod \
  --network app_pdflab-network \
  --restart unless-stopped \
  -p 3000:3000 \
  mkelam/pdflab-frontend:previous-tag

# Verify rollback successful
curl https://pdflab.pro/api/health
# Should return 200 OK
```

### Step 4: Post-Rollback

- [ ] Verify site working (smoke tests)
- [ ] Notify team of rollback
- [ ] Document what failed
- [ ] Update deployment checklist
- [ ] Fix issue before re-deployment

---

## 📊 Production Deployment Success Metrics

### Deployment Speed
- **Fast**: <10 minutes (ideal)
- **Medium**: 10-30 minutes (acceptable)
- **Slow**: >30 minutes (needs optimization)

### Downtime
- **Zero**: 0 seconds (perfect)
- **Minimal**: <30 seconds (excellent)
- **Acceptable**: <5 minutes (good)
- **Critical**: >5 minutes (requires immediate action)

### Error Rate Post-Deployment
- **Perfect**: 0 errors in first hour
- **Good**: <5 errors in first hour (non-critical)
- **Concerning**: >10 errors in first hour
- **Critical**: Continuous errors or 500s

---

## 🎯 Lessons Learned from v1.1.0 → v1.1.1 Incident

**Timeline:**
- **19:50 UTC**: v1.1.0 deployed to production
- **19:51 UTC**: Users report login failures
- **19:52 UTC**: CORS errors identified in logs
- **19:55 UTC**: Trust proxy ValidationError found
- **19:57 UTC**: v1.1.1 hotfix code written
- **20:05 UTC**: v1.1.1 deployed to production
- **20:06 UTC**: Production stable, all services working

**Total Downtime**: 15 minutes
**User Impact**: 100% authentication blocked

**What Went Wrong:**
1. ❌ Did not test API call from production domain before deployment
2. ❌ Did not verify CORS origins included production domain
3. ❌ Did not enable trust proxy for Nginx deployment
4. ❌ Did not run post-deployment smoke tests

**What Went Right:**
1. ✅ Fast detection (1 minute)
2. ✅ Fast diagnosis (5 minutes)
3. ✅ Fast hotfix (10 minutes)
4. ✅ Clear rollback plan available
5. ✅ Database not affected
6. ✅ Zero data loss

**Prevention for Future:**
- ✅ **This Skill Created**: production-deployment-guardian.SKILL.md
- ✅ **Mandatory Checklist**: Run before EVERY deployment
- ✅ **Automated Tests**: Add CORS tests to CI/CD
- ✅ **Staging Environment**: Test with production-like domain first

---

## 🔧 Automation Opportunities

### Pre-Deployment Script

```bash
#!/bin/bash
# pre-deployment-checks.sh

echo "=== Production Deployment Pre-Flight Checks ==="

# Check 1: CORS origins
echo "Checking CORS configuration..."
grep -q "https://pdflab.pro" backend/src/server.ts
if [ $? -eq 0 ]; then
  echo "✅ CORS: Production domain found"
else
  echo "❌ CORS: Production domain MISSING"
  exit 1
fi

# Check 2: Trust proxy
echo "Checking trust proxy..."
grep -q "app.set('trust proxy', true)" backend/src/server.ts
if [ $? -eq 0 ]; then
  echo "✅ Trust Proxy: Enabled"
else
  echo "❌ Trust Proxy: NOT enabled"
  exit 1
fi

# Check 3: TypeScript compilation
echo "Checking TypeScript..."
npm run typecheck > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ TypeScript: No errors"
else
  echo "❌ TypeScript: Compilation errors found"
  exit 1
fi

# Check 4: No localhost references
echo "Checking for localhost references..."
LOCALHOST_COUNT=$(grep -r "localhost" backend/src/ --exclude-dir=node_modules | grep -v "comment" | wc -l)
if [ $LOCALHOST_COUNT -eq 0 ]; then
  echo "✅ No localhost references found"
else
  echo "⚠️  Warning: Found $LOCALHOST_COUNT localhost references"
fi

echo ""
echo "=== Pre-Flight Checks Complete ==="
echo "Safe to deploy: YES"
```

---

## Key Principles

1. **Test with production domain BEFORE deploying** - Non-negotiable
2. **CORS origins must include production domains** - Always
3. **Trust proxy required behind reverse proxy** - No exceptions
4. **Run smoke tests AFTER deployment** - Catch issues immediately
5. **Have rollback plan ready** - Murphy's law applies
6. **Document everything** - Future you will thank you

---

## When to Escalate

- Multiple failed deployments
- Infrastructure changes (new proxy, CDN, etc.)
- Moving to new hosting provider
- Changing domain names
- Complex database migrations
- Multi-region deployments

---

**Skill Version**: 1.0.0
**Created**: November 10, 2025
**Based On**: v1.1.0 → v1.1.1 production incident
**Last Updated**: November 10, 2025
