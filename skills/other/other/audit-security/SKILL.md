---
description: Run security audit checks (rate limiting, webhook validation, SQL injection, XSS)
handoffs:
  - label: Fix Security Issues
    agent: security-auditor
    prompt: Fix the security vulnerabilities identified
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: empty (run all checks)

## Task

Run comprehensive security tests to identify vulnerabilities.

### Steps

1. **Test Rate Limiting**:
   ```bash
   cd backend

   # Test email verification rate limit (60s cooldown)
   python -c "
   import requests
   import time

   url = 'http://localhost:8000/v1/email/send-verification-code'
   email = 'ratetest@example.com'

   # Send 2 requests rapidly
   r1 = requests.post(url, json={'email': email})
   r2 = requests.post(url, json={'email': email})

   if r1.status_code == 200 and r2.status_code == 429:
       print('✅ Email verification rate limit working')
   else:
       print(f'❌ Rate limit bypass: {r1.status_code}, {r2.status_code}')
   "

   # Test download rate limit (10 per 24h)
   # Test recovery rate limit (5 per IP per hour)
   # Test magic link rate limit (3 per email per 24h)
   ```

2. **Test Webhook Signature Validation** (FR-P-002):
   ```bash
   # Test invalid signature rejection
   curl -X POST http://localhost:8000/webhooks/paddle \
     -H "Content-Type: application/json" \
     -H "Paddle-Signature: invalid_signature" \
     -H "Paddle-Timestamp: $(date +%s)" \
     -d '{"event_type":"payment.succeeded","payment_id":"test"}' \
     -w "\nStatus: %{http_code}\n"

   # Expected: 401 Unauthorized

   # Test expired timestamp rejection (>5 min)
   OLD_TIMESTAMP=$(($(date +%s) - 400))
   curl -X POST http://localhost:8000/webhooks/paddle \
     -H "Paddle-Timestamp: ${OLD_TIMESTAMP}" \
     -d '{"event_type":"payment.succeeded"}' \
     -w "\nStatus: %{http_code}\n"

   # Expected: 401 Unauthorized
   ```

3. **Test SQL Injection Protection**:
   ```bash
   # Test quiz submission with SQL injection attempt
   curl -X POST http://localhost:8000/v1/quiz/submit \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com'"'"'; DROP TABLE users; --",
       "step_1": "male"
     }'

   # Should return validation error, not execute SQL
   # Check database: users table still exists
   python -c "
   from src.lib.database import engine
   result = engine.execute('SELECT 1 FROM users LIMIT 1')
   print('✅ SQL injection prevented - users table intact')
   "
   ```

4. **Test XSS Protection** (dietary restrictions field):
   ```bash
   # Test XSS in step_17 (dietary restrictions)
   curl -X POST http://localhost:8000/v1/quiz/submit \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "step_1": "male",
       "step_17": "<script>alert(\"XSS\")</script>"
     }'

   # Verify script is sanitized in database
   python -c "
   from src.models.quiz_response import QuizResponse
   from src.lib.database import SessionLocal

   db = SessionLocal()
   quiz = db.query(QuizResponse).filter_by(email='test@example.com').first()

   if '<script>' not in str(quiz.quiz_data.get('step_17', '')):
       print('✅ XSS sanitization working')
   else:
       print('❌ XSS vulnerability: script tag not sanitized')
   "
   ```

5. **Test Magic Link Brute Force Protection**:
   ```bash
   # Test 256-bit token entropy
   python -c "
   from src.services.magic_link import generate_token
   import secrets

   token = generate_token()
   token_bytes = secrets.token_bytes(32)

   if len(token) == 64:  # 32 bytes = 64 hex chars
       print('✅ Magic link token has 256-bit entropy')
   else:
       print(f'❌ Weak token: {len(token)} chars')

   # Test brute force protection (should be computationally infeasible)
   print('   Brute force attempts needed: 2^256')
   "
   ```

6. **Test Email Normalization Bypass**:
   ```bash
   # Test Gmail dot/plus bypass attempts
   python -c "
   from src.lib.email_utils import normalize_email

   test_cases = [
       ('User.Name+tag@Gmail.com', 'username@gmail.com'),
       ('user.name@googlemail.com', 'username@gmail.com'),
       ('TEST@EXAMPLE.COM', 'test@example.com'),
   ]

   for input_email, expected in test_cases:
       result = normalize_email(input_email)
       if result == expected:
           print(f'✅ {input_email} → {result}')
       else:
           print(f'❌ {input_email} → {result} (expected {expected})')
   "
   ```

7. **Test Secrets Exposure**:
   ```bash
   # Check for exposed secrets in codebase
   cd ../..

   # Search for common secret patterns
   echo "Checking for exposed secrets..."

   git grep -i "api_key.*=" -- "*.py" "*.ts" "*.js" | grep -v ".env" && \
     echo "⚠️ Potential hardcoded API keys found" || \
     echo "✅ No hardcoded API keys detected"

   git grep -i "password.*=" -- "*.py" "*.ts" "*.js" | grep -v "password_hash" && \
     echo "⚠️ Potential hardcoded passwords found" || \
     echo "✅ No hardcoded passwords detected"
   ```

8. **Output Summary**:
   ```
   ✅ Security Audit Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Rate Limiting:
   ✅ Email verification: 60s cooldown enforced
   ✅ Download limit: 10 per 24h working
   ✅ Recovery limit: 5 per IP per hour working
   ✅ Magic link: 3 per email per 24h working

   Webhook Security (FR-P-002):
   ✅ HMAC-SHA256 signature validation working
   ✅ Timestamp validation (5-min window) working
   ✅ Invalid signature rejected (401)
   ✅ Expired timestamp rejected (401)

   Injection Protection:
   ✅ SQL injection: Parameterized queries prevent injection
   ✅ XSS: HTML sanitization working

   Authentication:
   ✅ Magic link: 256-bit entropy (computationally secure)
   ✅ Email normalization: Bypass attempts prevented

   Secrets Management:
   ✅ No hardcoded API keys found
   ✅ No hardcoded passwords found
   ✅ All secrets in .env files (not committed)

   Critical Issues: 0
   Warnings: 0

   Recommendation: ✅ All security checks passed
   ```

## Example Usage

```bash
/audit-security    # Run all security checks
```

## Exit Criteria

- All rate limits tested and working
- Webhook signature validation tested
- SQL injection protection verified
- XSS sanitization working
- Magic link security confirmed
- No exposed secrets in codebase

## Critical Security Requirements

- FR-P-002: Webhook HMAC + timestamp validation
- FR-P-010: Email normalization to prevent blacklist bypass
- FR-R-002: Magic link 256-bit entropy, single-use, 24h expiry
- FR-R-005: Download rate limiting (10 per 24h)
