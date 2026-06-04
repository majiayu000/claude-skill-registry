---
name: bugcrowd-reporting
description: Write Bugcrowd-format reports — VRT (Vulnerability Rating Taxonomy) mapping, P1-P5 severity, impact-led writing, and Bugcrowd-specific submission etiquette. Use AFTER triage-validation passes for Bugcrowd programs.
metadata:
  type: skill
  phase: output
  platforms: [bugcrowd]
---

# Bugcrowd Reporting

> Bugcrowd uses VRT, not CVSS. Map your bug to the VRT entry first.

## When to invoke

**Trigger phrases:**
- "Bugcrowd report"
- "VRT mapping"
- "submit on Bugcrowd"
- "format for BC"

## VRT primer

Bugcrowd's **VRT** (Vulnerability Rating Taxonomy) is a hierarchical category tree. Each category has a default priority (P1-P5).

```
P1 — Critical    (e.g., RCE, SQLi data extraction)
P2 — High        (e.g., stored XSS w/ auth bypass, IDOR critical data)
P3 — Medium      (e.g., reflected XSS, IDOR less-sensitive)
P4 — Low         (e.g., minor info disclosure)
P5 — Informational
```

Reference: https://bugcrowd.com/vulnerability-rating-taxonomy

When submitting, pick the **most specific** VRT category that fits — vague mapping triggers downgrade.

## Bugcrowd report structure

The submission form has:
- **Title** — see formula
- **VRT (Bug Type)** — dropdown of categories
- **Severity** — auto-filled from VRT, but you can adjust
- **Target** — which in-scope asset
- **Description** — main body (markdown supported)

The Description should contain:

```markdown
## Summary
[1-2 sentences — the bug + its impact]

## Description
[3-5 sentences — affected feature, mechanism]

## Steps to Reproduce
1. ...
2. ...

## PoC
[Code, requests, screenshots]

## Impact
[Concrete impact statement]

## Suggested Fix
[Actionable]
```

## Title formula (same as H1)

**Format:** `<Severity tag>: <vuln class> in <endpoint> enables <impact>`

```
# Good
P1 — SSRF in document import URL leading to AWS IAM credential disclosure
P2 — Stored XSS via SVG avatar enables full session theft of profile viewers
P3 — IDOR in GraphQL user query exposes email and phone of any user
P1 — Authentication bypass via alg=none JWT acceptance

# Avoid
XSS
Bug
Possible XSS
```

## VRT category mapping (top examples)

Map each bug class to the BC VRT path:

| Bug | VRT Path | Default Priority |
|---|---|---|
| RCE via SSTI / template injection | Server Security Misconfiguration > Server-Side Template Injection > Remote Code Execution | P1 |
| RCE via deserialization | Server-Side Injection > Remote Code Execution | P1 |
| SQL injection (data extraction) | Server-Side Injection > SQL Injection > Vulnerable | P1-P2 |
| Stored XSS (high impact) | Cross-Site Scripting (XSS) > Stored | P2-P3 |
| Reflected XSS | Cross-Site Scripting (XSS) > Reflected | P3-P4 |
| DOM XSS | Cross-Site Scripting (XSS) > DOM | P3-P4 |
| IDOR (critical data) | Broken Access Control > Insecure Direct Object Reference > Critical | P2 |
| IDOR (moderate data) | Broken Access Control > IDOR > Moderate | P3 |
| Auth bypass | Broken Authentication and Session Management > Auth Bypass | P1-P2 |
| SSRF (internal access) | Server-Side Request Forgery > Internal | P2 |
| SSRF (cloud metadata) | Server-Side Request Forgery > Internal > Cloud Metadata | P1 |
| File upload RCE | Server Security Misconfiguration > Insecure File Upload > RCE | P1 |
| Stored XSS via file upload | Server Security Misconfiguration > Insecure File Upload > XSS | P2 |
| JWT alg=none | Broken Authentication > JWT > Algorithm None | P1 |
| OAuth redirect_uri bypass | Insufficient Security Configurability > OAuth Misconfig | P1-P2 |
| Account takeover | Sensitive Data Exposure > Account Takeover | P1 |
| Subdomain takeover | Server Security Misconfiguration > Subdomain Takeover | P2-P3 |
| Open redirect | Server Security Misconfiguration > Insecure URL Redirect > Open Redirect | P4-P5 |
| HTTP smuggling | Server-Side Injection > HTTP Response Smuggling | P1-P2 |
| Cache poisoning | Server Security Misconfiguration > Web Cache Poisoning | P2-P3 |
| Prototype pollution (exploitable) | Server-Side Injection > Prototype Pollution | P2-P3 |
| Mass assignment | Broken Access Control > Mass Assignment | P2-P3 |
| Race condition (real $$$) | Broken Access Control > Race Condition | P2-P3 |
| GraphQL introspection alone | Sensitive Data Exposure > GraphQL Introspection | P4-P5 |
| GraphQL IDOR | Broken Access Control > Insecure Direct Object Reference | P2-P3 |

→ See https://bugcrowd.com/vulnerability-rating-taxonomy for the complete tree.

## VRT cheat: P-ratings (typical bounty multiples)

```
P1 — Critical  ← $1k–25k+  (program-dependent)
P2 — High      ← $500–5k
P3 — Medium    ← $100–1k
P4 — Low       ← $50–250
P5 — Info      ← $0 or swag/kudos
```

## The full report (production-grade example)

```markdown
## Summary
The `/api/v3/import/url` endpoint is vulnerable to Server-Side Request Forgery (SSRF). By supplying the AWS EC2 metadata endpoint URL, any authenticated user can retrieve IAM credentials for the EC2 role attached to the application's web servers, enabling full AWS account access.

## VRT
Server-Side Request Forgery > Internal > Cloud Metadata → P1 (Critical)

## Description
While reviewing the document import feature, I noticed it accepts any URL and fetches its content. The implementation does not validate the URL host. Sending `http://169.254.169.254/...` returns the EC2 metadata service responses, including IAM credentials. The IAM role attached (`web-prod-role`) has read/write access to S3 buckets containing user-uploaded PII.

## Steps to Reproduce

1. Log in as any user (signup is free)
2. Send the following request:
   ```http
   POST /api/v3/import/url HTTP/1.1
   Host: app.target.com
   Cookie: session=USER_SESSION
   Content-Type: application/json

   {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
   ```

3. Response:
   ```
   web-prod-role
   ```

4. Now fetch credentials:
   ```http
   POST /api/v3/import/url HTTP/1.1
   ...

   {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/web-prod-role"}
   ```

5. Response contains:
   ```json
   {
     "AccessKeyId": "ASIA...",
     "SecretAccessKey": "...",
     "Token": "...",
     "Expiration": "2026-06-02T15:42:18Z"
   }
   ```

6. Credentials verified via AWS CLI:
   ```
   $ AWS_ACCESS_KEY_ID=ASIA... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=... aws sts get-caller-identity
   {
     "UserId": "AROA...",
     "Account": "123456789012",
     "Arn": "arn:aws:sts::123456789012:assumed-role/web-prod-role/i-..."
   }
   ```

## PoC

Attached:
- `screenshot-credential-extraction.png` — the actual response with credentials (redacted)
- `aws-sts-output.png` — verification of credential validity
- `repro.har` — HAR file of the entire reproduction

## Impact

- **AWS IAM credential disclosure** for production EC2 role
- The role `web-prod-role` has:
  - Read/write to S3 bucket `target-user-uploads` (~50M files including PII)
  - SQS read on `target-jobs-queue`
  - RDS describe-instances (info disclosure)
- Confirmed via `enumerate-iam` after extraction
- Persistent: while credentials rotate, the SSRF allows re-fetching at any time
- Potential to pivot to full AWS account access if the role can be chained / privilege escalated

## Suggested Fix

1. **Allowlist URL hosts** — reject requests to RFC1918 ranges (10/8, 172.16/12, 192.168/16), 169.254/16, and localhost
2. **Enforce IMDSv2** on EC2 instances (PUT-based token required)
3. **Reduce IAM role permissions** to least privilege (this role appears over-permitted)
4. **Validate URL scheme** — accept only `https://` and only after host validation

## Notes
- All testing performed on my own test account
- No third-party / real user data was accessed via the extracted credentials
- Extracted credentials NOT used to access S3 contents beyond `aws sts get-caller-identity`
- Available for verification or remediation discussion
```

## VRT-specific considerations

### Always map specifically

Bad: "Misc Server Security Misconfiguration"
Good: "Server-Side Request Forgery > Internal > Cloud Metadata"

Specific mapping = correct default priority = correct bounty.

### Justify VRT upgrade if needed

If you think the bug deserves higher than VRT default:
```
## Severity Note
The default VRT priority for "OAuth Misconfiguration > Redirect URI Bypass" is P3, but in this 
implementation it enables one-click ATO of any user. I'm proposing P1 / Critical given:
- Zero credentials required
- Affects all 2M+ users
- Full session token capture
- Chained with the existing open redirect at /redirect?url= (no separate vuln)
```

### CVSS optional but useful

Bugcrowd accepts a CVSS vector in the report. Include it as additional evidence:
```
CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N = 8.1 (High)
```

## Bugcrowd-specific etiquette

### "Researcher Comments"
Bugcrowd has a comments section beneath the report. Use it for:
- Clarifications when triage asks
- "I noticed X also has same issue, want me to submit separately?"
- Negotiation around VRT mapping

### Reasonable response time
Bugcrowd has SLAs published per program. Don't ping early.

### Crowd messaging
Don't share details outside the platform (Discord, Twitter) before disclosure.

### Disclosure
After fix + payout, you can request disclosure. Builds your portfolio.

## VRT references to memorize

The 20 most-common VRT categories you'll use:

```
1. Cross-Site Scripting (XSS) > Stored
2. Cross-Site Scripting (XSS) > Reflected  
3. Cross-Site Scripting (XSS) > DOM
4. Server-Side Injection > SQL Injection
5. Server-Side Injection > Command Injection
6. Server-Side Injection > Code Injection
7. Server-Side Injection > XML External Entities
8. Server-Side Request Forgery > Internal
9. Server-Side Request Forgery > Internal > Cloud Metadata
10. Broken Access Control > Insecure Direct Object Reference
11. Broken Access Control > Privilege Escalation
12. Broken Access Control > Mass Assignment
13. Broken Authentication > Authentication Bypass
14. Broken Authentication > JWT > Algorithm None
15. Server Security Misconfiguration > Insecure File Upload
16. Server Security Misconfiguration > Subdomain Takeover
17. Server Security Misconfiguration > Web Cache Poisoning
18. Sensitive Data Exposure > Account Takeover
19. Insufficient Security Configurability > OAuth Misconfiguration
20. Cross-Site Request Forgery > Authenticated Action
```

## H1 vs Bugcrowd quick diff

| Aspect | H1 | BC |
|---|---|---|
| Severity model | CVSS 3.1 | VRT + P1-P5 |
| Categorization | CWE | VRT tree |
| Markdown | Yes | Yes |
| Bounty table | Per program | Per program (VRT-driven) |
| Triage style | Often faster | Tends to follow VRT defaults strictly |
| Disclosure | Researcher-initiated post-payout | Same |

The report content is the same. The category field is different — use VRT for BC.

## Cross-references

- `[[triage-validation]]` — run before this
- `[[hackerone-reporting]]` — H1 equivalent
- All vuln-class skills — back-reference impact

## Common pitfalls

1. **Wrong VRT mapping.** "Misc" category → P5 default → minimal bounty.
2. **No P1/P2 justification for high-impact bugs.** Argue the upgrade.
3. **Confusing VRT priority with CVSS.** They differ. Use both.
4. **Reporting same bug under multiple categories.** Pick one (the most-specific).
5. **Inflating to P1 when the bug is P2.** Reputation suffers.

## Bugcrowd reward tiers (illustrative — varies by program)

```
P1 Critical  →  often $1k–25k+, top programs $5k+ minimum
P2 High      →  often $500–5k
P3 Medium    →  often $150–1k
P4 Low       →  often $50–250
P5 Info      →  $0 + kudos
```

Pick programs with strong P-rating bounty tables. Check before hunting.

## Bugcrowd-only features

- **Researcher leaderboard** — top hunters get exclusive private invites
- **VRT votes** — researchers can propose VRT updates
- **Bug Bash events** — sponsored events with bonus bounties
- **Crowd Control** for orgs — researchers don't see this but it's how triage queues work
- **Asset bonuses** — some programs add bonuses for hunting specific assets

## Quick markdown skeleton

```markdown
## Summary
[1-2 sentences — bug + impact]

## VRT
[Specific VRT path]
Suggested Priority: P[1-5] (Critical/High/Medium/Low/Info)

## Description
[Affected feature + root cause hypothesis]

## Steps to Reproduce
1. ...
2. ...
3. ...

## PoC
[code blocks, attachment list]

## Impact
[Concrete, business-grade]

## Suggested Fix
[Actionable]

## CVSS (Optional supplementary)
[CVSS vector]

## Notes
- Test accounts used; no real user data accessed
- Available for verification questions
```
