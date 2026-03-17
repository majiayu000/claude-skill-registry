---
name: security-testing
description: Identify security vulnerabilities through SAST, DAST, penetration testing, and dependency scanning. Use for security test, vulnerability scanning, OWASP, SQL injection, XSS, CSRF, and penetration testing.
---

# Security Testing

## Overview

Security testing identifies vulnerabilities, weaknesses, and threats in applications to ensure data protection, prevent unauthorized access, and maintain system integrity. It combines automated scanning (SAST, DAST) with manual penetration testing and code review.

## When to Use

- Testing for OWASP Top 10 vulnerabilities
- Scanning dependencies for known vulnerabilities
- Testing authentication and authorization
- Validating input sanitization
- Testing API security
- Checking for sensitive data exposure
- Validating security headers
- Testing session management

## Security Testing Types

- **SAST**: Static Application Security Testing (code analysis)
- **DAST**: Dynamic Application Security Testing (runtime)
- **IAST**: Interactive Application Security Testing
- **SCA**: Software Composition Analysis (dependencies)
- **Penetration Testing**: Manual security testing
- **Fuzz Testing**: Invalid/random input testing

## Instructions

### 1. **OWASP ZAP (DAST)**

```python
# security_scan.py
from zapv2 import ZAPv2
import time

class SecurityScanner:
    def __init__(self, target_url, api_key=None):
        self.zap = ZAPv2(apikey=api_key, proxies={
            'http': 'http://localhost:8080',
            'https': 'http://localhost:8080'
        })
        self.target = target_url

    def scan(self):
        """Run full security scan."""
        print(f"Scanning {self.target}...")

        # Spider the application
        print("Spidering...")
        scan_id = self.zap.spider.scan(self.target)
        while int(self.zap.spider.status(scan_id)) < 100:
            time.sleep(2)
            print(f"Spider progress: {self.zap.spider.status(scan_id)}%")

        # Active scan
        print("Running active scan...")
        scan_id = self.zap.ascan.scan(self.target)
        while int(self.zap.ascan.status(scan_id)) < 100:
            time.sleep(5)
            print(f"Scan progress: {self.zap.ascan.status(scan_id)}%")

        return self.get_results()

    def get_results(self):
        """Get scan results."""
        alerts = self.zap.core.alerts(baseurl=self.target)

        # Group by risk level
        results = {
            'high': [],
            'medium': [],
            'low': [],
            'informational': []
        }

        for alert in alerts:
            risk = alert['risk'].lower()
            results[risk].append({
                'name': alert['alert'],
                'description': alert['description'],
                'solution': alert['solution'],
                'url': alert['url'],
                'param': alert.get('param', ''),
                'evidence': alert.get('evidence', '')
            })

        return results

    def report(self, results):
        """Generate security report."""
        print("\n" + "="*60)
        print("SECURITY SCAN RESULTS")
        print("="*60)

        for risk_level in ['high', 'medium', 'low', 'informational']:
            issues = results[risk_level]
            if issues:
                print(f"\n{risk_level.upper()} Risk Issues: {len(issues)}")
                for issue in issues[:5]:  # Show first 5
                    print(f"  - {issue['name']}")
                    print(f"    URL: {issue['url']}")
                    if issue['param']:
                        print(f"    Parameter: {issue['param']}")

        # Fail if high risk found
        if results['high']:
            raise Exception(f"Found {len(results['high'])} HIGH risk vulnerabilities!")

# Usage
scanner = SecurityScanner('http://localhost:3000')
results = scanner.scan()
scanner.report(results)
```

### 2. **SQL Injection Testing**

```typescript
// tests/security/sql-injection.test.ts
import { test, expect } from '@playwright/test';
import request from 'supertest';
import { app } from '../../src/app';

test.describe('SQL Injection Protection', () => {
  const sqlInjectionPayloads = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' UNION SELECT * FROM users --",
    "admin'--",
    "' OR 1=1--",
    "1' AND '1'='1",
  ];

  test('login should prevent SQL injection', async () => {
    for (const payload of sqlInjectionPayloads) {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: payload,
          password: payload,
        });

      // Should return 400/401, not 500 (SQL error)
      expect([400, 401]).toContain(response.status);
      expect(response.body).not.toMatch(/SQL|syntax|error/i);
    }
  });

  test('search should sanitize input', async () => {
    for (const payload of sqlInjectionPayloads) {
      const response = await request(app)
        .get('/api/products/search')
        .query({ q: payload });

      // Should not cause SQL error
      expect(response.status).toBeLessThan(500);
      expect(response.body).not.toMatch(/SQL|syntax/i);
    }
  });

  test('numeric parameters should be validated', async () => {
    const response = await request(app)
      .get('/api/users/abc')  // Non-numeric ID
      .expect(400);

    expect(response.body.error).toBeTruthy();
  });
});
```

### 3. **XSS Testing**

```javascript
// tests/security/xss.test.js
describe('XSS Protection', () => {
  const xssPayloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg onload=alert("XSS")>',
    'javascript:alert("XSS")',
    '<iframe src="javascript:alert(\'XSS\')">',
    '<body onload=alert("XSS")>',
  ];

  test('user input should be escaped', async () => {
    const { page } = await browser.newPage();

    for (const payload of xssPayloads) {
      await page.goto('/');

      // Submit comment with XSS payload
      await page.fill('[name="comment"]', payload);
      await page.click('[type="submit"]');

      // Wait for comment to appear
      await page.waitForSelector('.comment');

      // Check that script was not executed
      const dialogAppeared = await page.evaluate(() => {
        return window.xssDetected || false;
      });

      expect(dialogAppeared).toBe(false);

      // Check HTML is escaped
      const commentHTML = await page.$eval('.comment', el => el.innerHTML);
      expect(commentHTML).not.toContain('<script>');
      expect(commentHTML).toContain('&lt;script&gt;');
    }
  });

  test('URLs should be validated', async () => {
    const response = await request(app)
      .post('/api/links')
      .send({ url: 'javascript:alert("XSS")' })
      .expect(400);

    expect(response.body.error).toMatch(/invalid url/i);
  });
});
```

### 4. **Authentication & Authorization Testing**

```typescript
// tests/security/auth.test.ts
describe('Authentication Security', () => {
  test('should reject weak passwords', async () => {
    const weakPasswords = [
      'password',
      '12345678',
      'qwerty',
      'abc123',
      'password123',
    ];

    for (const password of weakPasswords) {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          password,
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toMatch(/password.*weak|password.*requirements/i);
    }
  });

  test('should rate limit login attempts', async () => {
    const credentials = {
      email: 'test@example.com',
      password: 'wrongpassword',
    };

    // Try 10 failed logins
    for (let i = 0; i < 10; i++) {
      await request(app)
        .post('/api/auth/login')
        .send(credentials);
    }

    // 11th attempt should be rate limited
    const response = await request(app)
      .post('/api/auth/login')
      .send(credentials);

    expect(response.status).toBe(429);
    expect(response.body.error).toMatch(/too many attempts|rate limit/i);
  });

  test('should prevent unauthorized access', async () => {
    const response = await request(app)
      .get('/api/admin/users')
      .expect(401);
  });

  test('should prevent privilege escalation', async () => {
    const regularUserToken = await getRegularUserToken();

    const response = await request(app)
      .delete('/api/users/999')  // Try to delete another user
      .set('Authorization', `Bearer ${regularUserToken}`)
      .expect(403);
  });

  test('JWT tokens should expire', async () => {
    // Create expired token
    const expiredToken = jwt.sign(
      { userId: '123' },
      JWT_SECRET,
      { expiresIn: '-1s' }
    );

    const response = await request(app)
      .get('/api/protected')
      .set('Authorization', `Bearer ${expiredToken}`)
      .expect(401);
  });
});
```

### 5. **CSRF Protection Testing**

```python
# tests/security/test_csrf.py
import pytest
from flask import session

class TestCSRFProtection:
    def test_post_without_csrf_token_rejected(self, client):
        """POST requests without CSRF token should be rejected."""
        response = client.post('/api/users', json={
            'email': 'test@example.com',
            'name': 'Test'
        })

        assert response.status_code == 403
        assert 'CSRF' in response.json['error']

    def test_post_with_invalid_csrf_token_rejected(self, client):
        """POST with invalid CSRF token should be rejected."""
        response = client.post('/api/users',
            json={'email': 'test@example.com'},
            headers={'X-CSRF-Token': 'invalid-token'}
        )

        assert response.status_code == 403

    def test_post_with_valid_csrf_token_accepted(self, client):
        """POST with valid CSRF token should be accepted."""
        # Get CSRF token
        response = client.get('/api/csrf-token')
        csrf_token = response.json['csrfToken']

        # Use token in POST
        response = client.post('/api/users',
            json={'email': 'test@example.com', 'name': 'Test'},
            headers={'X-CSRF-Token': csrf_token}
        )

        assert response.status_code == 201
```

### 6. **Dependency Vulnerability Scanning**

```bash
# Run npm audit
npm audit

# Fix vulnerabilities
npm audit fix

# For Python - Safety
pip install safety
safety check

# For Java - OWASP Dependency Check
mvn org.owasp:dependency-check-maven:check
```

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  sast-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten

  dast-scan:
    runs-on: ubuntu-latest
    steps:
      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:3000'
```

### 7. **Security Headers Testing**

```typescript
// tests/security/headers.test.ts
test.describe('Security Headers', () => {
  test('should have required security headers', async () => {
    const response = await request(app).get('/');

    expect(response.headers).toMatchObject({
      'x-frame-options': 'DENY',
      'x-content-type-options': 'nosniff',
      'x-xss-protection': '1; mode=block',
      'strict-transport-security': expect.stringMatching(/max-age=/),
      'content-security-policy': expect.any(String),
    });
  });

  test('should not expose sensitive headers', async () => {
    const response = await request(app).get('/');

    expect(response.headers['x-powered-by']).toBeUndefined();
    expect(response.headers['server']).not.toMatch(/express|nginx|apache/i);
  });

  test('CSP should prevent inline scripts', async ({ page }) => {
    await page.goto('/');

    const cspViolations = [];
    page.on('console', msg => {
      if (msg.type() === 'error' && msg.text().includes('Content Security Policy')) {
        cspViolations.push(msg.text());
      }
    });

    // Try to inject inline script
    await page.evaluate(() => {
      const script = document.createElement('script');
      script.textContent = 'alert("test")';
      document.body.appendChild(script);
    });

    expect(cspViolations.length).toBeGreaterThan(0);
  });
});
```

### 8. **Secrets Detection**

```bash
# Install detect-secrets
pip install detect-secrets

# Scan repository
detect-secrets scan --all-files --force-use-all-plugins

# Check for hardcoded secrets
git secrets --scan

# TruffleHog for git history
trufflehog git https://github.com/user/repo --only-verified
```

## OWASP Top 10 Testing

1. **Broken Access Control**: Test authorization, privilege escalation
2. **Cryptographic Failures**: Check for weak encryption, exposed secrets
3. **Injection**: SQL, NoSQL, Command injection
4. **Insecure Design**: Architecture flaws
5. **Security Misconfiguration**: Default configs, unnecessary features
6. **Vulnerable Components**: Outdated dependencies
7. **Authentication Failures**: Weak passwords, session management
8. **Software & Data Integrity**: Unsigned packages, insecure CI/CD
9. **Logging Failures**: Insufficient logging, sensitive data in logs
10. **SSRF**: Server-side request forgery

## Best Practices

### ✅ DO
- Run security scans in CI/CD
- Test with real attack vectors
- Scan dependencies regularly
- Use security headers
- Implement rate limiting
- Validate and sanitize all input
- Use parameterized queries
- Test authentication/authorization thoroughly

### ❌ DON'T
- Store secrets in code
- Trust user input
- Expose detailed error messages
- Skip dependency updates
- Use default credentials
- Ignore security warnings
- Test only happy paths
- Commit sensitive data

## Tools

### SAST
- **Semgrep**: Multi-language static analysis
- **SonarQube**: Code quality and security
- **Bandit**: Python security linter
- **ESLint plugins**: JavaScript security

### DAST
- **OWASP ZAP**: Web app security scanner
- **Burp Suite**: Security testing platform
- **Nikto**: Web server scanner

### SCA
- **Snyk**: Dependency vulnerability scanning
- **npm audit**: Node.js dependencies
- **OWASP Dependency-Check**: Multi-language
- **Safety**: Python dependencies

### Secrets
- **detect-secrets**: Pre-commit hook
- **GitGuardian**: Secrets detection
- **TruffleHog**: Git history scanning

## Penetration Testing Checklist

### Input Validation
- [ ] SQL injection attempts blocked
- [ ] XSS payloads escaped
- [ ] Command injection prevented
- [ ] Path traversal blocked
- [ ] File upload restrictions

### Authentication
- [ ] Strong password policy
- [ ] Account lockout after failed attempts
- [ ] Session timeout implemented
- [ ] Password reset secure
- [ ] MFA available

### Authorization
- [ ] Role-based access control
- [ ] Privilege escalation prevented
- [ ] Direct object reference secure
- [ ] API endpoints protected

### Data Protection
- [ ] Sensitive data encrypted
- [ ] HTTPS enforced
- [ ] Secure cookies (HttpOnly, Secure)
- [ ] No secrets in logs
- [ ] PII properly handled

## Examples

See also: continuous-testing, api-contract-testing, code-review-analysis for comprehensive security practices.
