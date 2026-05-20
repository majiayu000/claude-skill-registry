---
name: OWASP Security Testing
description: Security testing skill based on OWASP Top 10, covering ZAP scanning, security headers, input validation, authentication, and authorization testing.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [owasp, security, zap, penetration-testing, vulnerability, web-security]
testingTypes: [security]
frameworks: []
languages: [typescript, python]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# OWASP Security Testing Skill

You are an expert security tester specializing in OWASP methodologies and web application security. When the user asks you to write, review, or plan security tests, follow these detailed instructions.

## Core Principles

1. **Defense in depth** -- Test every layer: input validation, authentication, authorization, encryption.
2. **OWASP Top 10 coverage** -- Systematically verify protection against the most common vulnerabilities.
3. **Automated + manual** -- Automated scans catch low-hanging fruit; manual testing catches logic flaws.
4. **Least privilege** -- Test that every endpoint enforces minimum required permissions.
5. **Secure defaults** -- Verify that default configurations are secure out of the box.

## OWASP Top 10 (2021) Testing Checklist

### A01: Broken Access Control

Test that users cannot access resources or perform actions beyond their permissions.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Access Control Tests', () => {
  test('regular user cannot access admin endpoints', async ({ request }) => {
    // Login as regular user
    const loginRes = await request.post('/api/auth/login', {
      data: { email: 'user@example.com', password: 'UserPass123!' },
    });
    const { token } = await loginRes.json();

    // Attempt to access admin-only endpoint
    const adminRes = await request.get('/api/admin/users', {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect(adminRes.status()).toBe(403);
  });

  test('user cannot access other users data via IDOR', async ({ request }) => {
    const loginRes = await request.post('/api/auth/login', {
      data: { email: 'user1@example.com', password: 'UserPass123!' },
    });
    const { token } = await loginRes.json();

    // Try to access another user's profile (IDOR)
    const otherUserRes = await request.get('/api/users/other-user-id', {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect(otherUserRes.status()).toBe(403);
  });

  test('user cannot elevate privileges via API', async ({ request }) => {
    const loginRes = await request.post('/api/auth/login', {
      data: { email: 'user@example.com', password: 'UserPass123!' },
    });
    const { token } = await loginRes.json();

    // Try to change own role to admin
    const updateRes = await request.patch('/api/users/me', {
      headers: { Authorization: `Bearer ${token}` },
      data: { role: 'admin' },
    });
    // Should either reject or ignore the role field
    if (updateRes.status() === 200) {
      const body = await updateRes.json();
      expect(body.role).not.toBe('admin');
    }
  });

  test('cannot bypass authorization by manipulating request path', async ({ request }) => {
    const paths = [
      '/api/admin/users',
      '/api/Admin/users',
      '/api/ADMIN/users',
      '/api/admin/./users',
      '/api/admin/../admin/users',
      '/api/admin%2Fusers',
    ];

    for (const path of paths) {
      const res = await request.get(path);
      expect(res.status()).not.toBe(200);
    }
  });
});
```

### A02: Cryptographic Failures

```typescript
test.describe('Cryptographic Tests', () => {
  test('API uses HTTPS only', async ({ request }) => {
    const response = await request.get('/', {
      headers: { Accept: 'text/html' },
    });
    const url = response.url();
    expect(url).toMatch(/^https:\/\//);
  });

  test('sensitive data is not in URL parameters', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('SecurePass123!');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Password should never appear in URL
    const url = page.url();
    expect(url).not.toContain('password');
    expect(url).not.toContain('SecurePass123');
  });

  test('passwords are not returned in API responses', async ({ request }) => {
    const loginRes = await request.post('/api/auth/login', {
      data: { email: 'user@example.com', password: 'UserPass123!' },
    });
    const body = await loginRes.json();
    const bodyStr = JSON.stringify(body);
    expect(bodyStr).not.toContain('UserPass123!');
    expect(body.user?.password).toBeUndefined();
    expect(body.user?.passwordHash).toBeUndefined();
  });

  test('cookies have Secure flag', async ({ page }) => {
    await page.goto('/');
    const cookies = await page.context().cookies();
    for (const cookie of cookies) {
      if (cookie.name.includes('session') || cookie.name.includes('token')) {
        expect(cookie.secure).toBe(true);
      }
    }
  });
});
```

### A03: Injection

```typescript
test.describe('Injection Tests', () => {
  const sqlInjectionPayloads = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "1' UNION SELECT null, username, password FROM users --",
    "admin'--",
    "1; UPDATE users SET role='admin' WHERE email='attacker@evil.com'",
  ];

  const xssPayloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '"><script>alert("XSS")</script>',
    "javascript:alert('XSS')",
    '<svg onload=alert("XSS")>',
    '{{constructor.constructor("return this")()}}',
  ];

  for (const payload of sqlInjectionPayloads) {
    test(`SQL injection: ${payload.substring(0, 30)}...`, async ({ request }) => {
      const response = await request.get('/api/users/search', {
        params: { q: payload },
      });
      // Should not return 500 (indicates unhandled SQL error)
      expect(response.status()).not.toBe(500);
      const body = await response.text();
      // Should not contain SQL error messages
      expect(body).not.toContain('SQL syntax');
      expect(body).not.toContain('mysql_');
      expect(body).not.toContain('ORA-');
      expect(body).not.toContain('PostgreSQL');
    });
  }

  for (const payload of xssPayloads) {
    test(`XSS: ${payload.substring(0, 30)}...`, async ({ request }) => {
      // Submit XSS payload
      await request.post('/api/comments', {
        data: { content: payload, postId: 'test-post' },
      });

      // Retrieve and check the content is escaped
      const response = await request.get('/api/comments?postId=test-post');
      const body = await response.text();
      expect(body).not.toContain('<script>');
      expect(body).not.toContain('onerror=');
      expect(body).not.toContain('javascript:');
    });
  }

  test('NoSQL injection protection', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: { $gt: '' },
        password: { $gt: '' },
      },
    });
    expect(response.status()).not.toBe(200);
  });

  test('Command injection protection', async ({ request }) => {
    const payloads = [
      '; ls -la',
      '| cat /etc/passwd',
      '`whoami`',
      '$(cat /etc/passwd)',
    ];

    for (const payload of payloads) {
      const response = await request.get('/api/ping', {
        params: { host: `example.com${payload}` },
      });
      const body = await response.text();
      expect(body).not.toContain('root:');
      expect(body).not.toContain('/bin/bash');
    }
  });
});
```

### A04: Insecure Design

```typescript
test.describe('Insecure Design Tests', () => {
  test('rate limiting on login endpoint', async ({ request }) => {
    const attempts = [];
    for (let i = 0; i < 20; i++) {
      attempts.push(
        request.post('/api/auth/login', {
          data: { email: 'user@example.com', password: `wrong${i}` },
        })
      );
    }

    const responses = await Promise.all(attempts);
    const rateLimited = responses.some((r) => r.status() === 429);
    expect(rateLimited).toBe(true);
  });

  test('account lockout after failed attempts', async ({ request }) => {
    // Attempt login 10 times with wrong password
    for (let i = 0; i < 10; i++) {
      await request.post('/api/auth/login', {
        data: { email: 'locktest@example.com', password: `wrong${i}` },
      });
    }

    // Even with correct password, should be locked
    const response = await request.post('/api/auth/login', {
      data: { email: 'locktest@example.com', password: 'CorrectPass123!' },
    });
    expect(response.status()).toBe(423); // Locked
  });
});
```

### A05: Security Misconfiguration

```typescript
test.describe('Security Headers', () => {
  test('should have required security headers', async ({ request }) => {
    const response = await request.get('/');
    const headers = response.headers();

    // Content Security Policy
    expect(headers['content-security-policy']).toBeDefined();

    // Prevent MIME type sniffing
    expect(headers['x-content-type-options']).toBe('nosniff');

    // Prevent clickjacking
    expect(headers['x-frame-options']).toMatch(/DENY|SAMEORIGIN/);

    // HSTS
    expect(headers['strict-transport-security']).toBeDefined();
    expect(headers['strict-transport-security']).toContain('max-age=');

    // Referrer policy
    expect(headers['referrer-policy']).toBeDefined();

    // Permissions policy
    expect(headers['permissions-policy']).toBeDefined();
  });

  test('should not expose server information', async ({ request }) => {
    const response = await request.get('/');
    const headers = response.headers();

    expect(headers['server']).not.toContain('Apache');
    expect(headers['server']).not.toContain('nginx');
    expect(headers['x-powered-by']).toBeUndefined();
    expect(headers['x-aspnet-version']).toBeUndefined();
  });

  test('CORS should be restrictive', async ({ request }) => {
    const response = await request.get('/api/users', {
      headers: { Origin: 'https://evil.com' },
    });
    const corsHeader = response.headers()['access-control-allow-origin'];
    expect(corsHeader).not.toBe('*');
    if (corsHeader) {
      expect(corsHeader).not.toContain('evil.com');
    }
  });

  test('directory listing is disabled', async ({ request }) => {
    const response = await request.get('/static/');
    const body = await response.text();
    expect(body).not.toContain('Index of');
    expect(body).not.toContain('Directory listing');
  });

  test('debug endpoints are not exposed', async ({ request }) => {
    const debugPaths = [
      '/debug',
      '/actuator',
      '/actuator/env',
      '/_debug',
      '/api/debug',
      '/phpinfo.php',
      '/.env',
      '/wp-admin',
      '/graphql',  // Should require auth
    ];

    for (const path of debugPaths) {
      const response = await request.get(path);
      expect([401, 403, 404]).toContain(response.status());
    }
  });
});
```

## ZAP Integration with Python

```python
import subprocess
import json
import time
from zapv2 import ZAPv2

class ZapSecurityScanner:
    def __init__(self, target_url: str, zap_api_key: str = ''):
        self.target = target_url
        self.zap = ZAPv2(apikey=zap_api_key, proxies={
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
        })

    def spider_scan(self, max_duration: int = 60):
        """Crawl the application to discover endpoints."""
        scan_id = self.zap.spider.scan(self.target)
        timeout = time.time() + max_duration
        while int(self.zap.spider.status(scan_id)) < 100:
            if time.time() > timeout:
                self.zap.spider.stop(scan_id)
                break
            time.sleep(2)
        return self.zap.spider.results(scan_id)

    def active_scan(self, max_duration: int = 300):
        """Run active security scan."""
        scan_id = self.zap.ascan.scan(self.target)
        timeout = time.time() + max_duration
        while int(self.zap.ascan.status(scan_id)) < 100:
            if time.time() > timeout:
                self.zap.ascan.stop(scan_id)
                break
            time.sleep(5)
        return scan_id

    def get_alerts(self, risk_level: str = 'High'):
        """Get security alerts filtered by risk level."""
        alerts = self.zap.core.alerts()
        risk_map = {'Informational': 0, 'Low': 1, 'Medium': 2, 'High': 3}
        min_risk = risk_map.get(risk_level, 0)
        return [
            a for a in alerts
            if risk_map.get(a['risk'], 0) >= min_risk
        ]

    def generate_report(self, output_path: str = 'security-report.html'):
        """Generate HTML security report."""
        report = self.zap.core.htmlreport()
        with open(output_path, 'w') as f:
            f.write(report)
        return output_path
```

## Security Test Data Patterns

### Common Attack Payloads

```typescript
export const SECURITY_PAYLOADS = {
  sqlInjection: [
    "' OR '1'='1",
    "1' UNION SELECT null--",
    "'; EXEC xp_cmdshell('dir')--",
    "1' AND SLEEP(5)--",
  ],
  xss: [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '"><svg/onload=alert(1)>',
    "'-alert(1)-'",
  ],
  pathTraversal: [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\config\\sam',
    '....//....//etc/passwd',
    '%2e%2e%2f%2e%2e%2fetc%2fpasswd',
  ],
  headerInjection: [
    'value\r\nInjected-Header: malicious',
    'value%0d%0aInjected: header',
  ],
  xxe: [
    '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
  ],
};
```

## Best Practices

1. **Test in isolated environments** -- Never run security tests against production.
2. **Get written authorization** -- Always have explicit permission before security testing.
3. **Start with passive scanning** -- Spider and passive scan before active scanning.
4. **Test all input vectors** -- Headers, query params, body, cookies, file uploads.
5. **Verify fixes** -- After remediation, re-test to confirm the vulnerability is resolved.
6. **Document everything** -- Record steps to reproduce every finding.
7. **Classify severity** -- Use CVSS or a similar framework for consistent risk rating.
8. **Test authentication flows** -- Password reset, session management, MFA bypass.
9. **Check error handling** -- Error messages should not leak stack traces or internal info.
10. **Automate regression** -- Add security tests to CI/CD to prevent regressions.

## Anti-Patterns to Avoid

1. **Testing only the happy path** -- Security bugs live in edge cases.
2. **Skipping authorization tests** -- Access control bugs are the #1 OWASP risk.
3. **Only using automated scanners** -- Scanners miss business logic vulnerabilities.
4. **Testing in production** -- Active scanning can cause outages or data corruption.
5. **Ignoring client-side security** -- CSP, CORS, and cookie flags matter.
6. **Assuming HTTPS is enough** -- Encryption does not prevent injection or access control flaws.
7. **Not testing file uploads** -- Uploaded files can contain malware or be used for path traversal.
8. **Trusting client-side validation** -- All validation must also occur server-side.
9. **Not testing rate limiting** -- Brute force and credential stuffing are common attacks.
10. **Reporting without proof** -- Always include evidence and reproduction steps.
