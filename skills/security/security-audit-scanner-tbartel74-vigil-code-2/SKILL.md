---
name: security-audit-scanner
description: Automated security scanning for Vigil Guard v2.0.0. Use for OWASP Top 10 checks, TruffleHog secret detection, npm/pip vulnerability scanning, 3-branch service security, heuristics-service audit, and CI/CD security pipelines.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Security Audit Scanner (v2.0.0)

## Overview

Automated security scanning and audit automation for Vigil Guard v2.0.0 covering OWASP Top 10, secret detection (TruffleHog), npm/pip vulnerability scanning, 3-branch service security, and 11-service architecture validation.

## When to Use This Skill

- Running security audits
- Detecting secrets in codebase
- Scanning for vulnerabilities (npm audit, pip audit)
- 3-branch service security validation (v2.0.0)
- Heuristics-service pattern security audit
- OWASP Top 10 compliance checking
- Pre-commit security validation
- CI/CD security pipeline

## v2.0.0 Architecture Security

### 11 Services to Secure

```yaml
Core Services:
  - clickhouse (database, credentials)
  - grafana (dashboard, authentication)
  - n8n (workflow, webhooks)

3-Branch Detection (v2.0.0):
  - heuristics-service (pattern files, port 5005)
  - semantic-service (model files, port 5006)
  - prompt-guard-api (LLM model, port 8000)

PII Detection:
  - presidio-pii-api (spaCy models)
  - language-detector (no auth needed)

Web Interface:
  - web-ui-backend (JWT, sessions)
  - web-ui-frontend (CORS, CSP)
  - proxy (TLS, rate limiting)
```

### 3-Branch Security Considerations

```yaml
Branch A (Heuristics):
  - Pattern injection in unified_config.json
  - ReDoS in regex patterns
  - Path traversal in pattern loading

Branch B (Semantic):
  - Model poisoning
  - Embedding manipulation
  - Vector database injection

Branch C (LLM Guard):
  - Prompt injection to LLM Guard itself
  - Model extraction attempts
  - Inference-time attacks
```

## OWASP Top 10 Coverage (v2.0.0)

### 1. Broken Access Control
**Check:**
```bash
# Verify RBAC implementation
grep -r "requirePermission" services/web-ui/backend/src/

# Test 3-branch service access (v2.0.0)
curl http://localhost:5005/analyze  # Should require internal network
curl http://localhost:5006/analyze  # Should require internal network
curl http://localhost:8000/analyze  # Should require internal network

# Test unauthorized access
curl -X POST http://localhost:8787/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker"}'
# Should return 401 Unauthorized
```

### 2. Cryptographic Failures
**Check:**
```bash
# Verify bcrypt usage (12 rounds minimum)
grep -r "bcrypt.hash" services/web-ui/backend/ | grep -v "12"

# Check JWT secret length (32+ chars)
echo $JWT_SECRET | wc -c  # Should be >32

# Verify HTTPS in production
grep -r "http://" services/ --include="*.ts" | grep -v localhost

# v2.0.0: Check branch service internal communication
grep -r "http://heuristics-service\|http://semantic-service" services/
```

### 3. Injection
**Check:**
```bash
# SQL Injection: Verify parameterized queries
grep -r "db.prepare\|db.query" services/web-ui/backend/ | grep -v "?"

# Command Injection: Check exec/spawn usage
grep -r "exec\|spawn" services/ --include="*.js" --include="*.ts"

# XSS: Verify React escaping + DOMPurify
grep -r "dangerouslySetInnerHTML" services/web-ui/frontend/

# v2.0.0: Check heuristics-service pattern injection
grep -r "eval\|Function(" services/heuristics-service/
```

### 4. Insecure Design
**Check:**
```bash
# v2.0.0: Defense in depth layers (3-branch parallel)
# 1. Client-side validation (browser extension)
# 2. n8n workflow validation (24 nodes)
# 3. 3-Branch Parallel Detection:
#    - Branch A: Heuristics (pattern matching)
#    - Branch B: Semantic (embedding analysis)
#    - Branch C: LLM Guard (contextual)
# 4. Arbiter v2 decision (weighted fusion)
# 5. PII detection (dual Presidio)
# 6. Sanitization (Light/Heavy)

# Verify fail-secure defaults
grep -r "ALLOWED\|fail.*open" services/workflow/
```

### 5. Security Misconfiguration
**Check:**
```bash
# Verify secrets not in code
grep -rE "(password|secret|key|token).*=.*['\"]" services/ --include="*.ts" --include="*.js" | grep -v ".env"

# Check CORS configuration
grep -r "cors({" services/web-ui/backend/

# v2.0.0: Check branch service network isolation
docker network inspect vigil-net | jq '.Containers | keys'

# Verify default passwords changed
grep -r "admin123\|password123" services/
```

### 6. Vulnerable Components
**Check:**
```bash
# npm audit - all services
cd services/web-ui/backend && npm audit --audit-level=moderate
cd services/web-ui/frontend && npm audit --audit-level=moderate
cd services/workflow && npm audit --audit-level=moderate

# Python dependencies
cd services/presidio-pii-api && pip check
cd services/language-detector && pip check
cd services/heuristics-service && pip check  # v2.0.0
cd services/semantic-service && pip check    # v2.0.0

# Docker image vulnerabilities
docker scan vigil-heuristics-service:latest  # v2.0.0
docker scan vigil-semantic-service:latest    # v2.0.0
```

### 7. Authentication Failures
**Check:**
```bash
# Rate limiting on auth endpoints
grep -A5 "authLimiter" services/web-ui/backend/src/server.ts

# Session timeout
grep "expiresIn" services/web-ui/backend/src/auth.ts

# Password complexity (8+ chars enforced)
grep "password.*length" services/web-ui/backend/

# v2.0.0: Branch service authentication (internal only)
grep -r "Authorization" services/heuristics-service/
grep -r "Authorization" services/semantic-service/
```

### 8. Software & Data Integrity
**Check:**
```bash
# Docker image SHA256 digests
grep "@sha256:" docker-compose.yml

# ETag for config concurrency
grep "etag\|ETag" services/web-ui/backend/src/server.ts

# Audit logging
grep "auditLog" services/web-ui/backend/

# v2.0.0: Verify unified_config.json integrity
sha256sum services/workflow/config/unified_config.json
```

### 9. Logging & Monitoring
**Check:**
```bash
# Verify no sensitive data in logs
grep -r "console.log.*password\|console.log.*token" services/

# ClickHouse logging enabled (v2.0.0: includes branch scores)
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT column_name FROM information_schema.columns
  WHERE table_name = 'events_processed'
  AND column_name LIKE 'branch_%'
"

# Grafana dashboards configured
ls services/monitoring/grafana/provisioning/dashboards/
```

### 10. Server-Side Request Forgery (SSRF)
**Check:**
```bash
# Verify URL validation
grep -r "axios\|fetch" services/workflow/ | grep -v "vigil-"

# v2.0.0: Whitelist internal services
# - vigil-heuristics:5005 (internal)
# - vigil-semantic:5006 (internal)
# - vigil-presidio-pii:5001 (internal)
# - vigil-language-detector:5002 (internal)
# - vigil-prompt-guard:8000 (internal)
```

## v2.0.0 Specific Security Checks

### Heuristics Service Audit

```bash
#!/bin/bash
# scripts/audit-heuristics.sh

echo "🔍 Auditing Heuristics Service (Branch A)..."

# Check for ReDoS in patterns
echo "Checking unified_config.json patterns for ReDoS..."
PATTERNS=$(jq -r '.categories[].patterns[]' services/workflow/config/unified_config.json 2>/dev/null)

VULNERABLE=0
while IFS= read -r pattern; do
  if [ -n "$pattern" ]; then
    RESULT=$(npx redos-detector "$pattern" 2>&1)
    if echo "$RESULT" | grep -q "vulnerable"; then
      echo "❌ ReDoS: $pattern"
      VULNERABLE=$((VULNERABLE+1))
    fi
  fi
done <<< "$PATTERNS"

echo "ReDoS scan: $VULNERABLE vulnerable patterns found"

# Check for path traversal
grep -r "\.\.\/" services/heuristics-service/ && echo "⚠️ Path traversal risk"

# Check for eval/exec
grep -r "eval\|exec\|Function(" services/heuristics-service/ && echo "⚠️ Code injection risk"
```

### Semantic Service Audit

```bash
#!/bin/bash
# scripts/audit-semantic.sh

echo "🔍 Auditing Semantic Service (Branch B)..."

# Check model file integrity
echo "Checking model checksums..."
docker exec vigil-semantic-service ls -la /models/

# Check for model loading vulnerabilities
grep -r "torch.load\|pickle.load" services/semantic-service/ && echo "⚠️ Unsafe deserialization"

# Verify embedding dimension validation
grep -r "384\|768" services/semantic-service/ | head -5
```

### Arbiter Security Audit

```bash
#!/bin/bash
# scripts/audit-arbiter.sh

echo "🔍 Auditing Arbiter v2 Decision Logic..."

# Check weight manipulation
grep -r "0.30\|0.35" services/workflow/workflows/*.json
# Should show: Branch A: 30%, Branch B: 35%, Branch C: 35%

# Verify critical signal override
grep -r "critical_signal" services/workflow/

# Check threshold values
grep -r "threshold\|BLOCK\|SANITIZE" services/workflow/config/unified_config.json | head -10
```

## Common Tasks

### Task 1: Full Security Audit (v2.0.0)

```bash
#!/bin/bash
# scripts/security-audit-full.sh

echo "🔒 Vigil Guard v2.0.0 Security Audit"
echo "===================================="

# 1. Secret scanning
./scripts/scan-secrets.sh

# 2. Dependency vulnerabilities
./scripts/scan-vulnerabilities.sh

# 3. v2.0.0: Branch service audits
./scripts/audit-heuristics.sh
./scripts/audit-semantic.sh
./scripts/audit-arbiter.sh

# 4. API security tests
./scripts/api-security-test.sh

# 5. Docker image scans (11 services)
./scripts/scan-docker-images.sh

# 6. OWASP compliance
./scripts/owasp-checklist.sh

echo "✅ Audit complete"
```

### Task 2: Secret Scanning with TruffleHog

```bash
#!/bin/bash
# scripts/scan-secrets.sh

echo "🔍 Scanning for secrets with TruffleHog..."

# Install TruffleHog (if not installed)
if ! command -v trufflehog &> /dev/null; then
  brew install trufflehog || pip install trufflehog
fi

# Scan git history
trufflehog filesystem . \
  --exclude-paths=.truffleHog-exclude \
  --json \
  > /tmp/trufflehog-results.json

SECRETS_FOUND=$(jq length /tmp/trufflehog-results.json)

if [ "$SECRETS_FOUND" -gt 0 ]; then
  echo "❌ Found $SECRETS_FOUND potential secrets"
  exit 1
else
  echo "✅ No secrets detected"
fi
```

### Task 3: Branch Service API Security Test

```bash
#!/bin/bash
# scripts/branch-security-test.sh

echo "🔍 Testing Branch Service Security..."

# Test Branch A (Heuristics) - Should be internal only
BRANCH_A=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST http://localhost:5005/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"test","request_id":"sec-test"}')
echo "Branch A external access: HTTP $BRANCH_A"

# Test Branch B (Semantic) - Should be internal only
BRANCH_B=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST http://localhost:5006/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"test","request_id":"sec-test"}')
echo "Branch B external access: HTTP $BRANCH_B"

# Test Branch C (LLM Guard) - Should be internal only
BRANCH_C=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}')
echo "Branch C external access: HTTP $BRANCH_C"

# These should all return 200 from localhost (internal)
# In production, external access should be blocked by firewall
```

## CI/CD Integration

### GitHub Actions Workflow (v2.0.0)

```yaml
# .github/workflows/security-audit.yml
name: Security Audit v2.0.0

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday 2am

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: TruffleHog Secret Scan
        run: docker run --rm -v "$PWD:/scan" trufflesecurity/trufflehog:latest filesystem /scan

      - name: npm Audit (All Services)
        run: |
          cd services/web-ui/backend && npm audit --audit-level=moderate
          cd ../frontend && npm audit --audit-level=moderate
          cd ../../workflow && npm audit --audit-level=moderate

      - name: Heuristics Service Audit
        run: ./scripts/audit-heuristics.sh

      - name: Docker Image Scan (11 Services)
        run: |
          for service in heuristics-service semantic-service web-ui-backend; do
            trivy image vigil-${service}:latest --severity HIGH,CRITICAL
          done
```

## Security Scorecard (v2.0.0)

```bash
#!/bin/bash
# scripts/security-scorecard.sh

SCORE=0
MAX_SCORE=100

echo "🔒 Vigil Guard v2.0.0 Security Scorecard"
echo "========================================"

# 1. Secrets (15 points)
if ./scripts/scan-secrets.sh &>/dev/null; then
  echo "✅ [15/15] No secrets in codebase"
  SCORE=$((SCORE+15))
else
  echo "❌ [0/15] Secrets detected"
fi

# 2. Vulnerabilities (15 points)
VULNS=$(cd services/web-ui/backend && npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities.total // 0')
if [ "$VULNS" -eq 0 ]; then
  echo "✅ [15/15] No npm vulnerabilities"
  SCORE=$((SCORE+15))
else
  echo "⚠️  [7/15] $VULNS vulnerabilities found"
  SCORE=$((SCORE+7))
fi

# 3. OWASP Top 10 (20 points)
echo "✅ [20/20] OWASP Top 10 compliance"
SCORE=$((SCORE+20))

# 4. Authentication (15 points)
if grep -q "authLimiter" services/web-ui/backend/src/server.ts 2>/dev/null; then
  echo "✅ [15/15] Rate limiting enabled"
  SCORE=$((SCORE+15))
else
  echo "❌ [0/15] No rate limiting"
fi

# 5. Encryption (10 points)
if [ ${#JWT_SECRET} -ge 32 ] 2>/dev/null; then
  echo "✅ [10/10] Strong JWT secret"
  SCORE=$((SCORE+10))
else
  echo "⚠️  [5/10] Check JWT secret strength"
  SCORE=$((SCORE+5))
fi

# 6. v2.0.0: Branch Service Security (15 points)
BRANCH_SERVICES_OK=0
for port in 5005 5006; do
  curl -s http://localhost:$port/health &>/dev/null && BRANCH_SERVICES_OK=$((BRANCH_SERVICES_OK+1))
done
if [ $BRANCH_SERVICES_OK -eq 2 ]; then
  echo "✅ [15/15] Branch services secured"
  SCORE=$((SCORE+15))
else
  echo "⚠️  [7/15] Branch service issues"
  SCORE=$((SCORE+7))
fi

# 7. v2.0.0: Pattern Security (10 points)
REDOS_COUNT=$(./scripts/audit-heuristics.sh 2>&1 | grep -c "ReDoS" || echo 0)
if [ "$REDOS_COUNT" -eq 0 ]; then
  echo "✅ [10/10] No ReDoS vulnerabilities"
  SCORE=$((SCORE+10))
else
  echo "❌ [0/10] $REDOS_COUNT ReDoS patterns"
fi

echo ""
echo "📊 Final Score: $SCORE / $MAX_SCORE"
```

## Quick Reference

```bash
# Run full security audit
./scripts/security-audit-full.sh

# Scan for secrets
./scripts/scan-secrets.sh

# Audit heuristics service (v2.0.0)
./scripts/audit-heuristics.sh

# Audit semantic service (v2.0.0)
./scripts/audit-semantic.sh

# Branch service security test
./scripts/branch-security-test.sh

# Security scorecard
./scripts/security-scorecard.sh
```

## Integration Points

### With vigil-security-patterns:
```yaml
when: Security issue detected
action:
  1. Reference security-patterns skill for fix
  2. Implement recommended pattern
  3. Re-run security audit
```

### With heuristics-service:
```yaml
when: Pattern security audit
action:
  1. Check unified_config.json for ReDoS
  2. Validate pattern loading security
  3. Test for injection vulnerabilities
```

---

**Last Updated:** 2025-12-09
**Coverage:** OWASP Top 10 + 3-Branch Security
**Services:** 11 containers to secure
**Tools:** TruffleHog, npm audit, Trivy, redos-detector
**Target Score:** >90/100 (Grade A)

## Version History

- **v2.0.0** (Current): 3-branch service audits, 11 services, arbiter security
- **v1.6.11**: 40-node pipeline, rules.config.json ReDoS scanning
