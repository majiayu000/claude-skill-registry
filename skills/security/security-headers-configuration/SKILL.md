---
name: security-headers-configuration
description: Configures HTTP security headers to protect against XSS, clickjacking, and MIME sniffing attacks. Use when hardening web applications, passing security audits, or implementing Content Security Policy.
---

# Security Headers Configuration

Implement HTTP security headers to defend against common browser-based attacks.

## Essential Headers

| Header | Purpose | Value |
|--------|---------|-------|
| HSTS | Force HTTPS | `max-age=31536000; includeSubDomains` |
| CSP | Restrict resources | `default-src 'self'` |
| X-Frame-Options | Prevent clickjacking | `DENY` |
| X-Content-Type-Options | Prevent MIME sniffing | `nosniff` |

## Express Implementation

```javascript
const helmet = require('helmet');

app.use(helmet());

// Custom CSP
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
    frameAncestors: ["'none'"]
  }
}));
```

## Nginx Configuration

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'" always;
```

## Verification Tools

- [Security Headers](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [CSP Evaluator](https://csp-evaluator.withgoogle.com/)

## Security Headers Checklist

- [ ] HSTS enabled with long max-age
- [ ] CSP configured and tested
- [ ] X-Frame-Options set to DENY
- [ ] X-Content-Type-Options set to nosniff
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy disables unused features

## Additional Implementations

See [references/python-apache.md](references/python-apache.md) for:
- Python Flask security headers middleware
- Flask-Talisman library configuration
- Apache .htaccess configuration
- Header testing script

## Common Mistakes

- Setting CSP to report-only permanently
- Using overly permissive policies
- Forgetting to test after changes
- Not including all subdomains in HSTS
