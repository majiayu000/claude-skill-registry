---
name: magento-security
description: Implement Magento 2 security — CSP, 2FA, CSRF protection, ACL, admin security configuration, input validation, and security best practices. Use when hardening a Magento installation or reviewing security posture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Security

## Before writing code

**Fetch live docs**:
1. Web-search `site:experienceleague.adobe.com commerce security` for security best practices
2. Web-search `site:developer.adobe.com commerce php development security` for developer security guide
3. Web-search `magento 2 security patches latest` for recent security updates

## Content Security Policy (CSP)

### What It Does

Protects against XSS and code injection by restricting which resources (scripts, styles, images, fonts) can load.

### Configuration

- `etc/csp_whitelist.xml` — whitelist external domains per CSP directive
- Modes: **report-only** (logs violations) and **restrict** (blocks violations)
- Directives: `script-src`, `style-src`, `img-src`, `font-src`, `connect-src`, `frame-src`

### Adding Allowed Sources

Whitelist third-party domains for payment gateways, analytics, CDNs:
- Declare in `csp_whitelist.xml` under the appropriate directive
- Use `report-only` mode first to identify missing whitelists

## Two-Factor Authentication (2FA)

- **Mandatory** for all admin users since Magento 2.4.0
- Supported providers: Google Authenticator, Duo Security, Authy, U2F keys
- Rate limiting on OTP validation (configurable retry limit and lockout)
- Cannot be disabled in production (security requirement)

## CSRF Protection

- `form_key` — 16-character token included in all admin forms
- Validated on every POST request in admin
- **SameSite** cookie attribute prevents cross-site request forgery
- Admin Secret Key in URLs adds additional protection

## Admin Security Configuration

Available at Stores > Settings > Configuration > Advanced > Admin > Security:
- Custom admin URL path (obscure the `/admin` path)
- Add Secret Key to URLs
- Password lifetime (force periodic changes)
- Max login failures before lockout
- Lockout duration
- Session lifetime
- Allowed countries for admin access

## Input Validation and Output Escaping

### Input Validation

- Validate all user input on the server side
- Use Magento's validation classes and form validators
- Never trust client-side validation alone
- Validate types, lengths, formats, and allowed values

### Output Escaping (XSS Prevention)

In PHTML templates, always escape output:
- `$escaper->escapeHtml($value)` — HTML context
- `$escaper->escapeUrl($url)` — URL context
- `$escaper->escapeJs($value)` — JavaScript context
- `$escaper->escapeHtmlAttr($value)` — HTML attribute context
- `$escaper->escapeCss($value)` — CSS context
- Never use `echo $value` directly in templates

## reCAPTCHA

- Native Google reCAPTCHA v2/v3 support since 2.3
- Configurable per form: login, registration, forgot password, checkout, contact
- Admin configuration at Stores > Configuration > Security > reCAPTCHA

## API Security

- Bearer token authentication for REST/SOAP
- ACL-based authorization for all endpoints
- Rate limiting on authentication endpoints
- OAuth 1.0a for third-party integrations

## Best Practices

- Apply security patches promptly — subscribe to Adobe Security Bulletins
- Use a custom admin URL (not `/admin`)
- Enable 2FA for all admin accounts
- Set strong password policies (length, complexity, expiry)
- Use HTTPS everywhere (frontend + admin)
- Restrict admin access by IP where possible
- Enable CSP in restrict mode (not just report-only)
- Escape all output in templates
- Keep Magento and all extensions up to date
- Run periodic security scans (Adobe Security Scan Tool)
- Review third-party extensions for security before installing

Fetch the security documentation for current CSP directives, 2FA configuration options, and latest security patches before implementing.
