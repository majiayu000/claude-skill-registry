---
name: environment-configuration-guardian
description: Validates environment-specific configurations across development, staging, and production environments. Prevents mismatched environment variables, localhost references in production, wrong API keys, and configuration drift. Use before ANY deployment to catch environment-specific issues that cause production failures.
---

# Environment Configuration Guardian

**Mission:** Ensure environment-specific configurations are correct for target environment (dev/staging/production). Prevents localhost references in production, wrong API keys, missing environment variables, and configuration mismatches that cause deployments to fail.

**Historical Context**: Created after analyzing v1.1.0-v1.1.1 incidents where environment-specific configurations (CORS, trust proxy, API keys) were incorrect for production.

---

## Activation Triggers

- **MANDATORY: Before EVERY deployment to new environment**
- Switching from development to production
- Setting up staging environment
- Deploying to new server/infrastructure
- Changing environment variables
- Updating API keys or credentials
- "localhost" errors in production
- API returning 401 Unauthorized in production
- Configuration not matching environment

---

## 🔴 CRITICAL: Environment Variable Validation Matrix

### Standard Environment Comparison

**Run this comparison BEFORE deployment:**

```bash
# Generate environment variable report
./scripts/compare-env-variables.sh development production

# Output shows differences:
```

| Variable | Development | Production | Status |
|----------|-------------|------------|--------|
| **NODE_ENV** | development | production | ✅ Correct |
| **CORS_ORIGIN** | localhost:3000 | https://pdflab.pro | ✅ Correct |
| **Trust Proxy** | false | true | ✅ Correct |
| **DB_HOST** | localhost | docker-container | ✅ Correct |
| **CLOUDCONVERT_SANDBOX** | true | ❌ **true** | ❌ **WRONG** |
| **PAYFAST_MERCHANT_ID** | 10000100 | ❌ **10000100** | ❌ **WRONG** |

---

## Environment-Specific Configuration Checklist

### Development Environment

```bash
# .env.development
NODE_ENV=development
PORT=3006

# Database (Local)
DB_HOST=localhost
DB_PORT=3306
DB_USER=pdflab
DB_PASSWORD=***REMOVED***
DB_NAME=pdflab

# Redis (Local)
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS (Localhost)
CORS_ORIGIN=http://localhost:3000,http://localhost:3002

# Trust Proxy (Not behind proxy)
# No need to set - defaults to false

# CloudConvert (Sandbox)
CLOUDCONVERT_API_KEY=sandbox_key_here
CLOUDCONVERT_SANDBOX=true

# PayFast (Sandbox)
PAYFAST_MERCHANT_ID=10000100
PAYFAST_MERCHANT_KEY=46f0cd694581a
PAYFAST_PASSPHRASE=jt7NOE43FZPn
PAYFAST_MODE=sandbox

# JWT (Development Secret)
JWT_SECRET=dev-secret-not-for-production
JWT_EXPIRATION=7d

# Sentry (Optional in dev)
SENTRY_DSN=  # Empty or dev project

# Frontend URL (Local)
FRONTEND_URL=http://localhost:3000
```

### Production Environment

```bash
# .env.production
NODE_ENV=production
PORT=3006

# Database (Docker Container)
DB_HOST=8731b5f977d0_pdflab-mysql-prod  # Docker hostname
DB_PORT=3306
DB_USER=pdflab
DB_PASSWORD=***REMOVED***  # ✅ Different from dev
DB_NAME=pdflab_production

# Redis (Docker Container)
REDIS_HOST=f18c830e3d31_pdflab-redis-prod  # Docker hostname
REDIS_PORT=6379

# CORS (Production Domain)
CORS_ORIGIN=https://pdflab.pro,http://pdflab.pro  # ✅ MANDATORY

# Trust Proxy (Behind Nginx)
# Set in code: app.set('trust proxy', true)  # ✅ MANDATORY

# CloudConvert (Production)
CLOUDCONVERT_API_KEY=live_production_key_here  # ✅ Different key
CLOUDCONVERT_SANDBOX=false  # ✅ CRITICAL

# PayFast (Production)
PAYFAST_MERCHANT_ID=25263515  # ✅ Different from sandbox
PAYFAST_MERCHANT_KEY=***REMOVED***  # ✅ Different from sandbox
PAYFAST_PASSPHRASE=  # ✅ Empty for production
PAYFAST_MODE=production  # ✅ CRITICAL

# JWT (Strong Production Secret)
JWT_SECRET=pdflab-production-jwt-secret-2024  # ✅ Strong unique secret
JWT_EXPIRATION=7d

# Sentry (Production Project)
SENTRY_DSN=https://...@sentry.io/...  # ✅ Production project

# Frontend URL (Production)
FRONTEND_URL=https://pdflab.pro  # ✅ Production domain
```

---

## 🔴 CRITICAL: Configuration Validation Rules

### Rule 1: No Localhost References in Production

**Scan for localhost:**

```bash
# Check environment files
grep -i "localhost" .env.production
# Should return: NO MATCHES

# Check codebase
grep -r "localhost" backend/src/ --exclude-dir=node_modules | grep -v "comment"
# Should return: NO MATCHES or only in development-specific code

# Check for 127.0.0.1
grep -r "127.0.0.1" backend/src/ --exclude-dir=node_modules
# Should return: NO MATCHES
```

**Violations that WILL cause production failure:**

```typescript
// ❌ WRONG: Hardcoded localhost
const API_URL = "http://localhost:3006"

// ❌ WRONG: Localhost in CORS
const corsOrigins = ['http://localhost:3000']

// ❌ WRONG: Database localhost
const DB_HOST = process.env.DB_HOST || 'localhost'  // Fallback to localhost

// ✅ CORRECT: Use environment variables
const API_URL = process.env.API_URL || (
  process.env.NODE_ENV === 'production'
    ? 'https://pdflab.pro'
    : 'http://localhost:3006'
)

// ✅ CORRECT: Production CORS
const corsOrigins = process.env.CORS_ORIGIN?.split(',') || []

// ✅ CORRECT: Required environment variable (no fallback)
const DB_HOST = process.env.DB_HOST
if (!DB_HOST) {
  throw new Error('DB_HOST environment variable is required')
}
```

---

### Rule 2: API Keys Match Environment

**Validation Checklist:**

```bash
# CloudConvert
□ Development: CLOUDCONVERT_SANDBOX=true
□ Production: CLOUDCONVERT_SANDBOX=false  # ✅ CRITICAL
□ API key is production key (not sandbox key)

# PayFast
□ Development: PAYFAST_MERCHANT_ID=10000100 (sandbox)
□ Production: PAYFAST_MERCHANT_ID=25263515 (live merchant ID)
□ Development: PAYFAST_MODE=sandbox
□ Production: PAYFAST_MODE=production

# Database
□ Development: DB_NAME=pdflab
□ Production: DB_NAME=pdflab_production
□ Production password is DIFFERENT from development

# JWT
□ Development: JWT_SECRET=dev-secret
□ Production: JWT_SECRET is strong (>32 chars) and unique
□ Verify JWT_SECRET is NOT default/example value
```

**Test API Keys:**

```bash
# Test CloudConvert API key
curl -X GET https://api.cloudconvert.com/v2/users/me \
  -H "Authorization: Bearer $CLOUDCONVERT_API_KEY"
# Should return: 200 OK with account info (not 401)

# Test PayFast credentials (signature generation)
./scripts/test-payfast-signature.sh
# Should generate valid signature
```

---

### Rule 3: Required Environment Variables Present

**Production Required Variables (MANDATORY):**

```bash
# Application
✅ NODE_ENV=production
✅ PORT=3006

# Database
✅ DB_HOST (not localhost)
✅ DB_PORT
✅ DB_USER
✅ DB_PASSWORD (strong password)
✅ DB_NAME (production database name)

# Redis
✅ REDIS_HOST (not localhost)
✅ REDIS_PORT

# CORS
✅ CORS_ORIGIN (includes production domain)

# CloudConvert
✅ CLOUDCONVERT_API_KEY (production key)
✅ CLOUDCONVERT_SANDBOX=false

# PayFast
✅ PAYFAST_MERCHANT_ID (production merchant ID)
✅ PAYFAST_MERCHANT_KEY (production key)
✅ PAYFAST_MODE=production

# JWT
✅ JWT_SECRET (strong unique secret)

# Frontend
✅ FRONTEND_URL (production URL)
```

**Validation Script:**

```typescript
// backend/src/config/validate-env.ts

const requiredEnvVars = [
  'NODE_ENV',
  'DB_HOST',
  'DB_PASSWORD',
  'REDIS_HOST',
  'CLOUDCONVERT_API_KEY',
  'PAYFAST_MERCHANT_ID',
  'JWT_SECRET'
]

export function validateEnvironment() {
  const missing: string[] = []

  for (const varName of requiredEnvVars) {
    if (!process.env[varName]) {
      missing.push(varName)
    }
  }

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(', ')}`
    )
  }

  // Validate production-specific requirements
  if (process.env.NODE_ENV === 'production') {
    // Check CORS includes production domain
    const corsOrigins = process.env.CORS_ORIGIN?.split(',') || []
    if (!corsOrigins.some(origin => origin.includes('pdflab.pro'))) {
      throw new Error('CORS_ORIGIN must include production domain')
    }

    // Check CloudConvert sandbox is false
    if (process.env.CLOUDCONVERT_SANDBOX !== 'false') {
      throw new Error('CLOUDCONVERT_SANDBOX must be false in production')
    }

    // Check PayFast mode is production
    if (process.env.PAYFAST_MODE !== 'production') {
      throw new Error('PAYFAST_MODE must be production')
    }

    // Check JWT secret is strong
    if (process.env.JWT_SECRET.length < 32) {
      throw new Error('JWT_SECRET must be at least 32 characters in production')
    }
  }

  console.log('✅ Environment variables validated successfully')
}

// Call on server startup
validateEnvironment()
```

---

### Rule 4: No Secrets in Code or Logs

**Scan for exposed secrets:**

```bash
# Check for API keys in code
grep -r "CLOUDCONVERT_API_KEY.*=" backend/src/ --exclude-dir=node_modules
# Should only show: process.env.CLOUDCONVERT_API_KEY

# Check for passwords in code
grep -r "password.*=" backend/src/ --exclude-dir=node_modules | grep -v "req.body"
# Should NOT show hardcoded passwords

# Check for JWT secrets in code
grep -r "JWT_SECRET.*=" backend/src/ --exclude-dir=node_modules
# Should only show: process.env.JWT_SECRET

# Check git history for secrets (use git-secrets or truffleHog)
git log -p | grep -i "api_key\|password\|secret"
```

**Red Flags:**

```typescript
// ❌ DANGER: Hardcoded API key
const CLOUDCONVERT_API_KEY = "eyJ0eXAiOiJKV1Q..."

// ❌ DANGER: Logged password
console.log('User password:', user.password)

// ❌ DANGER: Logged JWT token
console.log('Auth token:', req.headers.authorization)

// ✅ SAFE: Use environment variables
const CLOUDCONVERT_API_KEY = process.env.CLOUDCONVERT_API_KEY

// ✅ SAFE: Never log sensitive data
console.log('User authenticated:', user.id)

// ✅ SAFE: Redact tokens in logs
console.log('Auth header:', req.headers.authorization?.replace(/Bearer .+/, 'Bearer [REDACTED]'))
```

---

## Configuration Drift Detection

### Problem: Configurations Diverge Over Time

**Symptoms:**
- Features work in dev but fail in production
- Different behavior between environments
- Intermittent production issues
- "It works on my machine" syndrome

**Solution: Regular Configuration Audits**

```bash
# Compare environment files
diff .env.development .env.production

# Generate configuration report
node scripts/generate-config-report.js

# Output:
=== Environment Configuration Report ===
Environment: production
Generated: 2025-11-10

Configuration Differences from Development:
  NODE_ENV: development → production ✅
  CORS_ORIGIN: localhost → pdflab.pro ✅
  DB_HOST: localhost → docker-container ✅
  CLOUDCONVERT_SANDBOX: true → false ✅

Configuration Risks:
  ⚠️  JWT_SECRET is only 16 chars (recommend 32+)
  ⚠️  No SENTRY_DSN configured (monitoring disabled)

Missing Variables:
  ❌ SMTP_HOST (email notifications disabled)
  ❌ BACKUP_ENABLED (automatic backups disabled)

=== End Report ===
```

---

## Pre-Deployment Environment Validation

### Step-by-Step Validation Process

**Step 1: Export Current Environment**

```bash
# Development
cd backend
node -e "console.log(JSON.stringify(process.env, null, 2))" > /tmp/dev-env.json

# Production (on VPS)
ssh root@141.136.44.168
cd /path/to/app
node -e "console.log(JSON.stringify(process.env, null, 2))" > /tmp/prod-env.json
```

**Step 2: Compare Environments**

```bash
# Download production env
scp root@141.136.44.168:/tmp/prod-env.json /tmp/

# Compare
node scripts/compare-environments.js /tmp/dev-env.json /tmp/prod-env.json

# Output highlights differences and flags risks
```

**Step 3: Validate Critical Values**

```bash
# CORS Origins
✅ Check: Production domain included
❌ Fail: Only localhost origins

# Trust Proxy
✅ Check: Enabled for production
❌ Fail: Disabled or missing

# API Keys
✅ Check: Production keys configured
❌ Fail: Sandbox keys in production

# Database
✅ Check: Production database host
❌ Fail: localhost or development database
```

**Step 4: Test Configuration**

```bash
# Test database connection
npm run test:db-connection

# Test Redis connection
npm run test:redis-connection

# Test CloudConvert API
npm run test:cloudconvert-api

# Test PayFast signature generation
npm run test:payfast-signature

# All tests must pass before deployment
```

---

## Common Environment Configuration Issues

### Issue 1: Localhost in Production CORS

**Symptom**: "Not allowed by CORS" in production
**Cause**: CORS_ORIGIN only has localhost
**Fix**: Add production domain to CORS_ORIGIN

```bash
# Wrong
CORS_ORIGIN=http://localhost:3000

# Correct
CORS_ORIGIN=http://localhost:3000,https://pdflab.pro
```

### Issue 2: Sandbox API Keys in Production

**Symptom**: API returns 401 or "Invalid credentials"
**Cause**: Using sandbox API keys in production
**Fix**: Use production API keys

```bash
# Wrong (sandbox)
CLOUDCONVERT_SANDBOX=true
PAYFAST_MERCHANT_ID=10000100

# Correct (production)
CLOUDCONVERT_SANDBOX=false
PAYFAST_MERCHANT_ID=25263515
```

### Issue 3: Weak JWT Secret

**Symptom**: Security vulnerability, easy token forgery
**Cause**: Short or predictable JWT secret
**Fix**: Use strong random secret (32+ characters)

```bash
# Wrong
JWT_SECRET=secret

# Correct
JWT_SECRET=pdflab-prod-jwt-a8f3c9e2b7d1f4a6c8e9b2d5f1a3c6e8
```

### Issue 4: Docker Container Hostnames

**Symptom**: "ECONNREFUSED" errors in production
**Cause**: Using localhost instead of Docker container hostnames
**Fix**: Use Docker container hostnames or service names

```bash
# Wrong
DB_HOST=localhost
REDIS_HOST=localhost

# Correct (Docker hostnames)
DB_HOST=8731b5f977d0_pdflab-mysql-prod
REDIS_HOST=f18c830e3d31_pdflab-redis-prod

# Or use Docker Compose service names
DB_HOST=mysql
REDIS_HOST=redis
```

---

## Environment Variable Security Best Practices

### 1. Never Commit .env Files to Git

```bash
# .gitignore
.env
.env.local
.env.development
.env.production
.env.*.local

# Exception: .env.example (template only)
.env.example  # ✅ OK to commit (no real values)
```

### 2. Use .env.example as Template

```bash
# .env.example (committed to repo)
NODE_ENV=
PORT=
DB_HOST=
DB_USER=
DB_PASSWORD=
CLOUDCONVERT_API_KEY=
# ... all required variables, no actual values
```

### 3. Rotate Secrets Regularly

```bash
# Schedule secret rotation
- [ ] JWT_SECRET: Every 6 months
- [ ] Database passwords: Every 6 months
- [ ] API keys: When compromised or yearly
- [ ] Session secrets: Every 6 months
```

### 4. Use Secret Management Tools

**Options:**
- **Docker Secrets** (for Docker Swarm)
- **AWS Secrets Manager** (for AWS)
- **HashiCorp Vault** (enterprise)
- **Environment variables** (encrypted at rest)

---

## Automated Environment Validation Script

```bash
#!/bin/bash
# scripts/validate-environment.sh

ENV=$1  # development, staging, production

echo "=== Validating $ENV Environment ==="

# Check required variables
REQUIRED_VARS=("NODE_ENV" "DB_HOST" "REDIS_HOST" "CLOUDCONVERT_API_KEY")

for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "❌ Missing required variable: $VAR"
    exit 1
  else
    echo "✅ $VAR is set"
  fi
done

# Check environment-specific requirements
if [ "$ENV" = "production" ]; then
  # Check no localhost references
  if [[ "$DB_HOST" == *"localhost"* ]]; then
    echo "❌ DB_HOST contains localhost in production"
    exit 1
  fi

  # Check CORS includes production domain
  if [[ ! "$CORS_ORIGIN" == *"pdflab.pro"* ]]; then
    echo "❌ CORS_ORIGIN missing production domain"
    exit 1
  fi

  # Check CloudConvert sandbox is false
  if [ "$CLOUDCONVERT_SANDBOX" != "false" ]; then
    echo "❌ CLOUDCONVERT_SANDBOX must be false in production"
    exit 1
  fi

  echo "✅ All production-specific checks passed"
fi

echo ""
echo "=== Environment Validation Complete ==="
echo "Safe to deploy to $ENV: YES"
```

**Usage:**

```bash
# Before deployment, run validation
./scripts/validate-environment.sh production

# If any checks fail, deployment is blocked
```

---

## Key Principles

1. **Never hardcode environment-specific values** - Always use environment variables
2. **Validate environment on startup** - Fail fast if misconfigured
3. **No localhost in production** - Ever
4. **Production keys are different from sandbox** - Always
5. **Strong secrets in production** - 32+ character random strings
6. **Regular configuration audits** - Catch drift early

---

## When to Escalate

- Moving to multi-region deployment
- Implementing CI/CD pipelines
- Setting up infrastructure as code (Terraform, etc.)
- Migrating to Kubernetes or container orchestration
- Implementing secret rotation automation
- Compliance requirements (SOC 2, PCI-DSS)

---

**Skill Version**: 1.0.0
**Created**: November 10, 2025
**Last Updated**: November 10, 2025
