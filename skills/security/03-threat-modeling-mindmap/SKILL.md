---
name: threat-modeling-mindmap
description: Build a mental and visual map of the target application before hunting — entry points, trust boundaries, data flows, and high-value functionality. Use when user has scope parsed and wants to plan WHERE to hunt rather than diving into recon.
metadata:
  type: skill
  phase: pre-hunt
---

# Threat Modeling & Mind-Mapping

> The hunters who win don't scan more — they scan smarter. Map first, attack the right node.

## When to invoke

**Trigger phrases:**
- "threat model this app"
- "mind map this target"
- "where should I focus"
- "what's the attack surface"
- "plan my hunt on X"

**Output:** A mind map (Markmap / Markdown / plain text) + a prioritized hunt list.

## Why this matters

A target like `app.target.com` has dozens of features. **80% of bounties come from 20% of features** — typically:
- Authentication and account management
- Payment / billing flows
- File uploads
- Admin / role-based endpoints
- API endpoints exposed via JS
- Third-party integrations
- Webhook handlers
- Search / report builders

Mapping these first prevents wasted hours on static marketing pages.

## The 6-layer Mind Map

```
TARGET
├── 1. AUTHENTICATION
│   ├── Login (creds, SSO, OAuth)
│   ├── Registration
│   ├── Password reset
│   ├── 2FA / MFA
│   ├── Session management (cookies, JWT)
│   ├── Logout
│   └── Account recovery
│
├── 2. AUTHORIZATION
│   ├── Roles (user, admin, support)
│   ├── Multi-tenancy (org/team scoping)
│   ├── Permission inheritance
│   ├── Impersonation / "view as"
│   └── API key scoping
│
├── 3. USER DATA
│   ├── Profile read/update
│   ├── PII fields (email, phone, SSN, address)
│   ├── Settings (notifications, integrations)
│   ├── Avatar / profile image upload
│   └── Account deletion
│
├── 4. CORE FUNCTIONALITY (varies per target)
│   ├── Main business logic (orders, posts, projects)
│   ├── File handling (upload, download, sharing)
│   ├── Search
│   ├── Comments / messaging
│   ├── Notifications
│   └── Webhooks
│
├── 5. PAYMENTS / BILLING (if applicable)
│   ├── Add payment method
│   ├── Subscription create/cancel
│   ├── Refunds
│   ├── Coupons / discount codes
│   └── Invoices
│
└── 6. TECHNICAL SURFACE
    ├── API (REST / GraphQL / gRPC)
    ├── Webhooks
    ├── OAuth / SSO endpoints
    ├── File CDN
    ├── WebSocket / SSE
    ├── Public buckets (S3, GCS)
    └── Source maps / exposed JS
```

## Step-by-Step Workflow

### 1. Manual exploration (30-60 min)

Sign up for the target. Click EVERY feature. Note:
- What HTTP methods are used (GET/POST/PUT/DELETE/PATCH)
- What identifiers are in URLs (UUID? sequential int? slug?)
- Where files are uploaded
- Where roles are mentioned
- Where money / payments are involved
- Where third-party integrations exist

### 2. Run passive crawl

```bash
# Capture all URLs the app uses
katana -u https://app.target.com -d 3 -jc -o app-urls.txt

# Add Wayback / GAU for historical paths
echo "app.target.com" | gau --providers wayback,otx,commoncrawl > historical-urls.txt
echo "app.target.com" | waybackurls >> historical-urls.txt

# Combine and dedupe
cat app-urls.txt historical-urls.txt | sort -u > all-urls.txt
```

### 3. Mine JS for endpoints

```bash
# See [[js-analysis]] for full workflow
# Quick version:
katana -u https://app.target.com -d 2 -jc -kf all -o crawl.txt
cat crawl.txt | grep -E '\.js(\?|$)' | sort -u > js-files.txt

# Extract endpoints from each JS
while read js; do
  python3 ~/tools/LinkFinder/linkfinder.py -i "$js" -o cli
done < js-files.txt | sort -u > js-endpoints.txt
```

### 4. Identify trust boundaries

Where does data cross from one trust zone to another? These are **bug magnets**:

- **Unauthenticated → Authenticated:** login, password reset
- **Low-priv user → High-priv user:** role escalation paths
- **User → System:** webhooks, callbacks
- **System → User:** notification handlers, email templates
- **Internal → External:** SSRF candidates (URL fetchers, image proxies)
- **Tenant A → Tenant B:** multi-tenant data access

### 5. Build the mind map

Use [Markmap](https://markmap.js.org/) for visual, or plain markdown:

```markdown
# Target: app.target.com (mind map)

## Auth
- /login (POST, email+password)
- /sso/google (OAuth)
- /reset (POST, email-based token)
  - **HUNT:** token entropy? predictable?
- /2fa/verify (POST, TOTP)
  - **HUNT:** rate limit? backup codes?

## Multi-tenancy
- /api/v3/org/{org_id}/users
  - **HUNT:** IDOR — can org_A see org_B's users?
- /api/v3/org/{org_id}/billing
  - **HUNT:** IDOR — billing access cross-org?

## File handling
- /upload (POST, multipart)
  - Allowed types: jpg, png, pdf?
  - **HUNT:** polyglot? SVG XSS? content-type bypass?
- /api/v3/files/{file_id}/download
  - **HUNT:** path traversal? IDOR?

## Payments
- /billing/payment-method (POST)
- /billing/refund (POST, admin-only)
  - **HUNT:** can user trigger? race condition?
```

### 6. Prioritize hunt order

Rank by (impact × ease):

| Feature | Class to try | Effort | Likely bounty if found |
|---|---|---|---|
| Multi-tenant API | IDOR | Low | $$$$ |
| Password reset | Token / race | Med | $$$ |
| File upload | RCE / XSS | Med-High | $$$$ |
| OAuth flow | redirect_uri | Low | $$$ |
| Admin endpoints | Forced browse | Low | $$$ |
| Search | SQLi / RCE | High | $$$$$ |
| Webhook | SSRF | Med | $$$$ |

## Output template

```markdown
# Threat Model: app.target.com

**Scope:** in-scope (per scope-analysis)
**Date:** YYYY-MM-DD

## Surface summary
- 47 routes discovered
- 3 user roles identified: guest, user, admin
- 2 tenant levels: org, team
- File upload: yes (avatar + project attachments)
- Payments: Stripe-based, custom backend
- OAuth: Google, Microsoft
- Webhooks: yes (Slack, Zapier integrations)

## High-priority hunt targets

### 1. Cross-tenant IDOR (priority: P0)
Endpoints:
- `GET /api/v3/org/{org_id}/projects`
- `GET /api/v3/org/{org_id}/users`
- `GET /api/v3/org/{org_id}/billing/invoices`
Test plan: Create 2 accounts in different orgs; cross-fetch.

### 2. Password reset token analysis (priority: P0)
- 32-char token; check entropy & expiry
- Race-condition on reset endpoint

### 3. File upload (priority: P1)
- Endpoint: POST /api/v3/files
- Test SVG XSS, polyglot, content-type spoofing

### 4. OAuth redirect_uri (priority: P1)
- /oauth/authorize?redirect_uri=...
- Test open redirect → token theft

### 5. Webhook SSRF (priority: P2)
- /integrations/webhook/test endpoint
- Test internal IP / metadata access

## De-prioritized (later or skip)
- Static marketing pages
- Public blog
- Status page (out of scope anyway)

## Time budget: 10 days
- Days 1-2: IDOR + password reset
- Days 3-4: File upload + OAuth
- Days 5-7: Webhook SSRF + business logic
- Days 8-10: Edge cases + report writing
```

## Cross-references

- `[[scope-analysis]]` — runs before this
- `[[subdomain-enum]]` — for the asset list
- `[[js-analysis]]` — for endpoint extraction
- All Phase 3 skills — apply mind map to specific vuln classes

## Common pitfalls

1. **Diving into scanning before manual exploration.** You miss the workflow.
2. **Treating all features equally.** Marketing pages rarely pay. Auth/payment always do.
3. **Not signing up for the app.** Authenticated surface is 10x bigger than unauthenticated.
4. **Ignoring mobile / API.** They're often less-tested than the web UI.
5. **No prioritization.** Without ranking, you hunt randomly.

## Pro tips

- **"View source" + Ctrl+F for `api`/`fetch`/`axios`** — fast endpoint discovery.
- **Burp's site map after a manual walk** is a poor man's mind map. Group by host.
- **Save the mind map per target** in `~/loot/<target>/mindmap.md`. Update as you learn.
- **A good mind map is reusable** across re-tests when scope updates.
