---
name: appsec
description: Application security - OWASP, validation, secrets. Use when securing the app.
---

# AppSec Guideline

## Tech Stack

* **Rate Limiting**: Upstash Redis
* **Framework**: Next.js
* **Platform**: Vercel

## Non-Negotiables

* OWASP Top 10:2025 vulnerabilities must be addressed
* CSP, HSTS, X-Frame-Options, X-Content-Type-Options headers must be present
* CSRF protection on state-changing requests
* No plaintext passwords in logs, returns, storage, or telemetry
* MFA required for Admin/SUPER_ADMIN roles
* Required configuration must fail-fast at build/startup if missing
* Secrets must not be hardcoded or committed

## Context

Security isn't a feature — it's a foundational property. A single vulnerability can compromise everything else. The review should think like an attacker: where are the weak points? What would I exploit?

Beyond fixing vulnerabilities, consider the security architecture holistically. Is defense-in-depth implemented? Are there single points of failure? Would you trust this system with your own data?

## Driving Questions

* What would an attacker target first?
* Where is rate limiting missing or insufficient?
* What attack vectors exist in authentication flows?
* How are secrets managed and what's the rotation strategy?
* What happens when a secret is compromised — is incident response exercisable?
* Where does "security by obscurity" substitute for real controls?
