---
name: appsec
description: Application security - OWASP, validation, secrets. Use when securing the app.
---

# AppSec Guideline

## Tech Stack

* **Rate Limiting**: Upstash Redis
* **Framework**: Next.js (with Turbopack)
* **Platform**: Vercel

## Non-Negotiables

* OWASP Top 10:2025 vulnerabilities must be addressed
* Security headers present (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
* CSRF protection on state-changing requests
* No plaintext secrets in logs, returns, storage, or telemetry
* Required configuration must fail-fast at build/startup if missing
* Secrets must not be hardcoded or committed

## Context

Security isn't a feature — it's a foundational property. A single vulnerability can compromise everything else. Think like an attacker: where are the weak points?

MFA and session security live in `account-security`. This skill focuses on application-level attack surface.

## Driving Questions

* What would an attacker target first?
* Where is rate limiting missing or insufficient?
* How are secrets managed and what's the rotation strategy?
* What happens when a secret is compromised?
* Where does "security by obscurity" substitute for real controls?
