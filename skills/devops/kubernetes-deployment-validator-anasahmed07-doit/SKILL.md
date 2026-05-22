---
name: kubernetes-deployment-validator
description: Validate Kubernetes deployments before execution. Run pre-flight checks for password generation, environment variables, database authentication, CORS configuration, and docker-compose parity. Use this skill BEFORE every Helm install/upgrade to prevent deployment failures.
---

# Kubernetes Deployment Validator

Pre-flight validation checks for Kubernetes deployments to prevent common configuration errors and deployment failures.

## When to Use

**ALWAYS run BEFORE**:
- `helm install` or `helm upgrade`
- Kubernetes deployment scripts
- Configuration changes to production/staging
- Migration from docker-compose to Kubernetes

## Validation Checklist

### 1. Password Generation Strategy

**What to Check**:
- Password encoding method (hex vs base64)
- Special characters that need URL-encoding
- PostgreSQL authentication compatibility

**Validation**:
```bash
# Test password generation
PASSWORD=$(openssl rand -hex 16)
echo "Generated password: $PASSWORD"

# Check for URL-encoding issues (should have NONE with hex)
echo "$PASSWORD" | grep -E '[+/=]' && echo "❌ FAIL: Special chars found" || echo "✅ PASS: Alphanumeric only"

# Test with PostgreSQL
echo "Testing PostgreSQL authentication with generated password..."
PGPASSWORD="$PASSWORD" psql -h localhost -p 5432 -U test_user -d postgres -c "SELECT 1;"
```

**Pass Criteria**:
- ✅ Uses `openssl rand -hex` (alphanumeric only)
- ✅ No special characters: `+`, `/`, `=`
- ✅ Works with psql, asyncpg, and postgres.js

**Fail Indicators**:
- ❌ Uses `openssl rand -base64` (contains special chars)
- ❌ Password contains URL-encoding characters
- ❌ Password works in psql but fails in application

**Fix**:
```bash
# Wrong
POSTGRES_PASSWORD=$(openssl rand -base64 16)  # ❌ Can generate: xK+3/zA9=mQ2pL1w

# Right
POSTGRES_PASSWORD=$(openssl rand -hex 16)     # ✅ Always generates: dadaf807863a952b
```

---

### 2. Environment Variable Flow

**What to Check**:
Complete path from .env → Helm → ConfigMap/Secret → Pod → Application

**Validation**:
```bash
# Check .env file
echo "📄 Checking .env file..."
grep -E "(SMTP_|EMAIL_|NODE_ENV|ALLOWED_ORIGINS)" .env

# Simulate Helm deployment (dry-run)
echo "🎯 Checking Helm values..."
helm template taskflow ./helm/taskflow --set sso.smtp.password="test" | grep -A5 ConfigMap

# Verify variables would reach pod
echo "🔍 Checking environment injection..."
helm template taskflow ./helm/taskflow | grep -E "(SMTP|NODE_ENV|ALLOWED_ORIGINS)" | head -20
```

**Pass Criteria**:
- ✅ .env contains all required variables
- ✅ Helm values.yaml references env vars
- ✅ ConfigMap includes non-sensitive variables
- ✅ Secrets include sensitive variables
- ✅ Deployment injects both ConfigMap and Secrets

**Fail Indicators**:
- ❌ Variables in .env but not in values.yaml
- ❌ Sensitive vars in ConfigMap instead of Secret
- ❌ Deployment doesn't reference ConfigMap/Secret
- ❌ Variable names mismatch between layers

**Fix**:
```yaml
# 1. Add to values.yaml
sso:
  smtp:
    enabled: true
    host: smtp.gmail.com
    password: changeme  # Override with --set

# 2. Add to ConfigMap (non-sensitive)
data:
  SMTP_HOST: {{ .Values.sso.smtp.host }}

# 3. Add to Secret (sensitive)
stringData:
  SMTP_PASS: {{ .Values.sso.smtp.password }}

# 4. Inject in Deployment
envFrom:
- configMapRef:
    name: sso-config
env:
- name: SMTP_PASS
  valueFrom:
    secretKeyRef:
      name: sso-secret
      key: SMTP_PASS
```

---

### 3. Database Authentication Configuration

**What to Check**:
- Secret password matches database password
- Connection string format correct
- Authentication mode compatible with client libraries

**Validation**:
```bash
# Get password from Secret
SECRET_PASSWORD=$(kubectl get secret sso-postgres-secret -n taskflow -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d 2>/dev/null || echo "none")

# Test connection with Secret password
echo "Testing database connection with Secret password..."
PGPASSWORD="$SECRET_PASSWORD" psql -h localhost -p 5432 -U sso_user -d sso_db -c "SELECT 1;" 2>&1

# Check for auth errors
kubectl logs -n taskflow -l app.kubernetes.io/component=sso --tail=50 | grep -i "password authentication failed"
```

**Pass Criteria**:
- ✅ Secret password works with psql
- ✅ Secret password works with application client (asyncpg/postgres.js)
- ✅ No "password authentication failed" errors in logs
- ✅ Connection string format correct for client library

**Fail Indicators**:
- ❌ psql works but application fails
- ❌ "password authentication failed" errors
- ❌ Secret password ≠ database password
- ❌ Connection string has URL-encoding issues

**Fix**:
```bash
# Reset database password to match Secret
PASSWORD=$(kubectl get secret sso-postgres-secret -n taskflow -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d)
kubectl exec -n taskflow sso-postgres-0 -- sh -c "
  PGPASSWORD='old_password' psql -U sso_user -d postgres -c \"ALTER USER sso_user WITH PASSWORD '$PASSWORD';\"
"

# Restart application pods
kubectl delete pod -n taskflow -l app.kubernetes.io/component=sso
```

---

### 4. CORS Configuration (Better Auth)

**What to Check**:
- NODE_ENV matches environment (dev vs prod)
- BETTER_AUTH_URL matches actual access URL
- ALLOWED_ORIGINS includes all tenant app URLs
- OAuth callback URLs use correct protocol

**Validation**:
```bash
# Check Helm values
echo "📋 Checking CORS configuration..."
helm get values taskflow -n taskflow | grep -E "(NODE_ENV|BETTER_AUTH_URL|ALLOWED_ORIGINS)"

# Verify in pod (after deployment)
echo "🔍 Verifying in pod..."
kubectl exec -n taskflow -l app.kubernetes.io/component=sso -- sh -c 'env | grep -E "(NODE_ENV|BETTER_AUTH_URL|ALLOWED_ORIGINS)"'

# Test CORS headers
echo "🌐 Testing CORS headers..."
curl -X OPTIONS http://localhost:3001/api/auth/session \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v 2>&1 | grep -i "access-control"
```

**Pass Criteria**:
- ✅ Development: NODE_ENV=development, HTTP localhost URLs
- ✅ Production: NODE_ENV=production, HTTPS domain URLs
- ✅ BETTER_AUTH_URL matches how service is accessed
- ✅ ALLOWED_ORIGINS includes all tenant applications
- ✅ CORS headers present in OPTIONS responses

**Fail Indicators**:
- ❌ NODE_ENV=production with HTTP URLs
- ❌ BETTER_AUTH_URL uses internal Kubernetes DNS (http://sso.taskflow.local)
- ❌ ALLOWED_ORIGINS is empty or missing
- ❌ "Invalid origin" errors in logs/console

**Fix (Development)**:
```yaml
sso:
  env:
    NODE_ENV: development  # Not production!
    BETTER_AUTH_URL: http://localhost:3001  # Not http://sso.taskflow.local
    ALLOWED_ORIGINS: "http://localhost:3000,http://localhost:3001"
```

**Fix (Production)**:
```yaml
sso:
  env:
    NODE_ENV: production
    BETTER_AUTH_URL: https://sso.taskflow.com  # HTTPS domain
    ALLOWED_ORIGINS: "https://app.taskflow.com,https://dashboard.taskflow.com"
```

---

### 5. Docker-Compose Parity

**What to Check**:
- All docker-compose services have Kubernetes equivalents
- Developer tools (pgAdmin, Redis Commander) available
- Same feature set as docker-compose

**Validation**:
```bash
# List docker-compose services
echo "📦 docker-compose services:"
docker-compose config --services

# List Kubernetes services
echo "☸️  Kubernetes services:"
kubectl get svc -n taskflow -o custom-columns=NAME:.metadata.name

# Check for common dev tools
echo "🔍 Checking dev tools..."
kubectl get deployment -n taskflow | grep -E "(pgadmin|redis-commander|mailhog)"
```

**Pass Criteria**:
- ✅ All docker-compose services have K8s deployments
- ✅ pgAdmin or equivalent database tool available
- ✅ Same environment variables in both
- ✅ Same port mappings (via port-forward)

**Fail Indicators**:
- ❌ docker-compose has pgAdmin, K8s doesn't
- ❌ Missing SMTP configuration in K8s
- ❌ Different environment variables
- ❌ Developer experience degraded

**Fix**:
```bash
# Add pgAdmin to Kubernetes
./scripts/add-pgadmin.sh

# Add any missing services
helm upgrade taskflow ./helm/taskflow \
  --set pgadmin.enabled=true \
  --set redisCommander.enabled=true
```

---

### 6. SMTP Configuration

**What to Check**:
- SMTP variables present in .env
- Variables passed through Helm
- Variables visible in SSO pod
- Better Auth can send emails

**Validation**:
```bash
# Check .env
echo "📧 Checking SMTP in .env..."
grep -E "SMTP_" .env

# Check Helm values
echo "📋 Checking SMTP in Helm..."
helm get values taskflow -n taskflow | grep -A6 smtp

# Check pod environment
echo "🔍 Checking SMTP in pod..."
kubectl exec -n taskflow -l app.kubernetes.io/component=sso -- sh -c 'env | grep -E "(SMTP|EMAIL)" | sort'
```

**Pass Criteria**:
- ✅ All SMTP variables in .env
- ✅ smtp.enabled=true in Helm values
- ✅ SMTP variables visible in pod
- ✅ No "connect ECONNREFUSED" errors

**Fail Indicators**:
- ❌ SMTP variables in .env but not in pod
- ❌ smtp.enabled=false in values.yaml
- ❌ Missing SMTP_PASS in Secret
- ❌ Email sending fails silently

**Fix**:
```bash
# Deploy with SMTP support
export $(grep -v '^#' .env | xargs)
helm upgrade taskflow ./helm/taskflow \
  --set sso.smtp.password="${SMTP_PASS}" \
  --wait

# Restart SSO pod
kubectl delete pod -n taskflow -l app.kubernetes.io/component=sso
```

---

## Pre-Flight Check Script

Create `.spec/scripts/validate-deployment.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Kubernetes Deployment Pre-Flight Checks"
echo "=========================================="
echo ""

FAILED=0

# 1. Password Generation
echo "1️⃣  Validating password generation strategy..."
PASSWORD=$(openssl rand -hex 16)
if echo "$PASSWORD" | grep -qE '[+/=]'; then
  echo "   ❌ FAIL: Password contains URL-encoding characters"
  FAILED=$((FAILED + 1))
else
  echo "   ✅ PASS: Alphanumeric-only passwords"
fi
echo ""

# 2. Environment Variables
echo "2️⃣  Validating environment variable flow..."
if [ ! -f .env ]; then
  echo "   ❌ FAIL: .env file not found"
  FAILED=$((FAILED + 1))
elif ! grep -q "SMTP_HOST" .env; then
  echo "   ⚠️  WARN: SMTP_HOST not in .env"
else
  echo "   ✅ PASS: .env file complete"
fi
echo ""

# 3. Helm Values
echo "3️⃣  Validating Helm values..."
if helm template taskflow ./helm/taskflow 2>/dev/null | grep -q "SMTP_HOST"; then
  echo "   ✅ PASS: SMTP configuration in Helm"
else
  echo "   ❌ FAIL: SMTP not configured in Helm"
  FAILED=$((FAILED + 1))
fi
echo ""

# 4. CORS Configuration
echo "4️⃣  Validating CORS configuration..."
NODE_ENV=$(helm get values taskflow -n taskflow 2>/dev/null | grep "NODE_ENV" | awk '{print $2}' || echo "none")
if [ "$NODE_ENV" == "development" ]; then
  echo "   ✅ PASS: NODE_ENV=development for localhost"
elif [ "$NODE_ENV" == "production" ]; then
  echo "   ⚠️  WARN: NODE_ENV=production (ensure HTTPS URLs)"
else
  echo "   ❌ FAIL: NODE_ENV not set"
  FAILED=$((FAILED + 1))
fi
echo ""

# 5. Summary
echo "=========================================="
if [ $FAILED -eq 0 ]; then
  echo "✅ All checks passed! Ready to deploy."
  exit 0
else
  echo "❌ $FAILED check(s) failed. Fix issues before deploying."
  exit 1
fi
```

## Usage

### Before Deployment

```bash
# Run pre-flight checks
./scripts/validate-deployment.sh

# If all pass, deploy
./scripts/deploy-one-command.sh
```

### After Deployment

```bash
# Verify everything works
./scripts/verify-deployment.sh
```

## Common Validation Failures

### Failure: Password authentication failed

**Symptom**: Pods stuck in CrashLoopBackOff with "password authentication failed" errors

**Cause**: base64 passwords with special characters

**Prevention**:
```bash
# Before deployment, verify password generation
PASSWORD=$(openssl rand -hex 16)
echo "$PASSWORD" | grep -E '[+/=]' && echo "FAIL" || echo "PASS"
```

### Failure: Invalid origin errors

**Symptom**: OAuth flow fails with "Invalid origin" error

**Cause**: NODE_ENV=production with HTTP localhost URLs

**Prevention**:
```bash
# Before deployment, check CORS configuration
helm template taskflow ./helm/taskflow | grep -E "(NODE_ENV|ALLOWED_ORIGINS)"
```

### Failure: SMTP not working

**Symptom**: Email verification doesn't send emails

**Cause**: SMTP variables not propagated to pod

**Prevention**:
```bash
# Before deployment, verify SMTP configuration
helm template taskflow ./helm/taskflow | grep -B2 -A2 "SMTP_HOST"
```

## Integration with CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Validate Deployment Configuration
  run: ./scripts/validate-deployment.sh

- name: Deploy to Kubernetes
  if: success()
  run: ./scripts/deploy-one-command.sh
```

## See Also

- `kubernetes-postgres-ops` skill for database management
- `helm-charts` skill for Helm best practices
- `better-auth-sso/references/cors-configuration.md` for CORS details
- `better-auth-sso/references/smtp-configuration.md` for SMTP details

---

### 7. Single Source of Truth for Passwords (CRITICAL)

**What to Check**:
- Each database password defined in EXACTLY one place in values.yaml
- All templates reference the single source (no hardcoded passwords in URLs)
- No scattered `| default "password"` patterns with different defaults

**Validation**:
```bash
# Check for hardcoded passwords in values.yaml
echo "🔍 Checking for hardcoded DATABASE_URL passwords..."
grep -n "databaseUrl.*://" helm/taskflow/values.yaml | grep -v "{{" && echo "❌ FAIL: Hardcoded passwords in URLs" || echo "✅ PASS"

# Check for scattered defaults in secrets.yaml
echo "🔍 Checking for inconsistent password defaults..."
grep -o 'default "[^"]*password[^"]*"' helm/taskflow/templates/secrets.yaml | sort | uniq -c | awk '$1 > 1 {print "❌ FAIL: Multiple different defaults found"; exit 1}'
echo "✅ PASS: No scattered password defaults"

# Verify single source definition
echo "🔍 Verifying single source in values.yaml..."
grep -n "password:" helm/taskflow/values.yaml
```

**Pass Criteria**:
- ✅ `values.yaml` has explicit `password:` field for each database
- ✅ `secrets.yaml` templates ALL passwords from values.yaml
- ✅ No hardcoded passwords in connection strings
- ✅ No `| default "changeme-xyz"` patterns with varying defaults

**Fail Indicators**:
- ❌ `databaseUrl: "postgresql://user:hardcoded-password@..."` in values.yaml
- ❌ Multiple `| default "changeme-xxx-password"` with different values
- ❌ Password in values.yaml doesn't match what templates use
- ❌ Secrets use different defaults than StatefulSet

**Correct Pattern**:
```yaml
# values.yaml - SINGLE SOURCE
api:
  postgresql:
    password: "changeme-api-db"  # THE source

# secrets.yaml - TEMPLATE from source
stringData:
  POSTGRES_PASSWORD: {{ .Values.api.postgresql.password | quote }}
  DATABASE_URL: "postgresql://{{ .Values.api.database.user }}:{{ .Values.api.postgresql.password }}@..."
  CHATKIT_DATABASE_URL: "postgresql://{{ .Values.api.database.user }}:{{ .Values.api.postgresql.password }}@..."
```

**Anti-Pattern (12 hours of debugging)**:
```yaml
# values.yaml - SCATTERED
chatkit:
  databaseUrl: "postgresql://user:changeme-api-db-password@..."  # HARDCODED!

# secrets.yaml - DIFFERENT DEFAULT
POSTGRES_PASSWORD: {{ .Values.api.postgresql.password | default "changeme-api-db-password" }}
# ^ What if values.yaml says "changeme-api-db" but default says "changeme-api-db-password"?
```

**Fix**:
1. Remove ALL hardcoded URLs from values.yaml
2. Define password ONCE per database in values.yaml
3. Template ALL references in secrets.yaml from that single source
4. Delete PVCs and redeploy when changing passwords
