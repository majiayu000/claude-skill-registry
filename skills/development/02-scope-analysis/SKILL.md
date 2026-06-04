---
name: scope-analysis
description: Parse HackerOne / Bugcrowd / Intigriti scope into a structured asset list with in-scope, out-of-scope, and excluded-vuln-class breakdowns. Use when the user has chosen a program and needs to understand exactly what's allowed before recon.
metadata:
  type: skill
  phase: pre-hunt
  platforms: [hackerone, bugcrowd, intigriti]
---

# Scope Analysis

> Hunting out-of-scope = wasted time + banned account.

## When to invoke

**Trigger phrases:**
- "parse this scope"
- "what's in scope"
- "extract assets from this program"
- "is X in scope"
- "what vuln classes are excluded"

## What we extract

From the program page, produce a structured breakdown:

```yaml
program: target-inc
platform: hackerone
last_updated: 2026-06-02

in_scope:
  domains:
    - "*.target.com"
    - "*.target-internal.io"
  ip_ranges:
    - "203.0.113.0/24"
  mobile:
    - "com.target.android"
    - "id1234567 (iOS)"
  api:
    - "api.target.com"
    - "graphql.target.com"
  source_code:
    - "https://github.com/target-inc/oss-app"

out_of_scope:
  domains:
    - "marketing.target.com"
    - "blog.target.com"
    - "status.target.com"
  acquisitions: "Anything acquired < 6 months ago"

excluded_vuln_classes:
  - subdomain_takeover            # explicit
  - csrf_logout                   # implicit (always)
  - missing_security_headers      # explicit
  - self_xss                      # explicit
  - email_enumeration             # explicit
  - rate_limiting_alone           # explicit
  - clickjacking_no_impact        # explicit
  - tls_ssl_config_only           # explicit

bounty_table:
  critical: { min: 5000, max: 15000 }
  high:     { min: 1500, max: 5000 }
  medium:   { min: 500,  max: 1500 }
  low:      { min: 100,  max: 500 }

special_rules:
  - "PoC required — no theoretical reports"
  - "Use test accounts only (provided in private invite)"
  - "Do not test production payment flows with real cards"
  - "Rate-limit your scanners to 5 req/sec"
```

## Step-by-Step Workflow

### 1. Locate the scope document

- **HackerOne:** Program page → "Scope" tab → "In-scope" and "Out-of-scope" sections
- **Bugcrowd:** Program brief → "Targets" section + "Out of scope" + "Focus areas"
- **Intigriti:** Program page → "Scope" tab + "Rules"

### 2. Parse domain patterns

Watch for:
- `*.target.com` — all subdomains allowed
- `target.com` (no asterisk) — root only
- `*.eu.target.com` — limited to EU subsidiary
- `subdomain1.target.com, subdomain2.target.com` — explicit list, not all subs

### 3. Identify wildcards & inclusions

Build the wildcard list:
```bash
# Save in-scope wildcards
cat > scope-wildcards.txt <<EOF
*.target.com
*.target-internal.io
api.target.com
EOF

# Save explicit out-of-scope (subtract these later)
cat > scope-oos.txt <<EOF
marketing.target.com
blog.target.com
status.target.com
support.target.com
EOF
```

### 4. Subtract OOS from recon results

After `subdomain-enum` runs, filter:
```bash
# Pseudo:
cat all-subdomains.txt | grep -vFf scope-oos.txt > in-scope-subs.txt
```

Or with Python for nested matching:
```python
import re

oos_patterns = [re.compile(r'^marketing\.target\.com$'),
                re.compile(r'.*\.acquired-recently\.com$')]

with open('all-subdomains.txt') as f:
    for sub in f:
        sub = sub.strip()
        if not any(p.match(sub) for p in oos_patterns):
            print(sub)
```

### 5. Map excluded vuln classes

For each program, build the **always-reject-here** list. Add to your hunt config:

```yaml
# .ccs-config/target-inc.yaml
skip_classes:
  - subdomain_takeover
  - missing_security_headers
  - csrf_no_impact
  - self_xss

require_impact_chain_for:
  - open_redirect
  - clickjacking
```

### 6. Cross-check against `[[triage-validation]]`

If the program excludes a class you found, **do not submit**. Look for chain potential to bypass exclusion:

- "Open redirect excluded" → chain to OAuth token theft → now critical
- "Subdomain takeover excluded" → chain to cookie scope / CORS → may pass
- "CSRF on logout excluded" → chain to forced auth + state change → may pass

→ See `docs/conditional-chain-table.md` for the full chain table.

## Output template

```markdown
# Scope Analysis: <program>

**Date:** YYYY-MM-DD
**Platform:** H1 / BC / Intigriti

## In-Scope Assets
- *.target.com (wildcard)
- api.target.com (explicit)
- com.target.android (mobile)

## Out-of-Scope (DO NOT TEST)
- marketing.target.com
- *.acquired-co.com (acquisitions)

## Excluded Vuln Classes
- subdomain takeover
- self-XSS
- CSRF (logout only)
- missing security headers

## Bounty Table
| Severity | Min | Max |
|---|---|---|
| Critical | $5k | $15k |
| High | $1.5k | $5k |
| Medium | $500 | $1.5k |
| Low | $100 | $500 |

## Special Rules
- PoC required
- Test accounts: provided in program
- Rate limit: 5 req/sec
- No payment-flow testing in prod

## Recon Plan
1. Subdomain enum on *.target.com
2. Filter against OOS list
3. Probe live hosts (httpx)
4. Tech fingerprint
5. Focus on api.target.com + mobile (highest payout match)

## Time budget: 5 days
```

## Cross-references

- `[[program-selection]]` — runs before this
- `[[subdomain-enum]]` — uses the scope list as input
- `[[continuous-monitoring]]` — set up alerts only on in-scope assets
- `[[triage-validation]]` — references excluded-class list

## Common pitfalls

1. **Treating `*.target.com` as including acquired domains.** Acquisitions usually need explicit listing.
2. **Ignoring "tier" structures.** Some programs say "Tier 1 = full scope, Tier 2 = lesser" — payouts differ.
3. **Missing IP ranges in scope.** Some programs list IPs not just domains; you can hit those too.
4. **Not noting time-of-day rules.** Some require testing only during certain hours to avoid prod impact.
5. **Skipping the "private bug bounty rules" attached to invites.** Re-read on every new invite.

## When scope is unclear

If a domain "looks in-scope" but isn't explicitly listed, **do not test**. Ask the program manager via HackerOne or Bugcrowd's secure channel:

> "Hi, evaluating scope. Is `legacy-api.target.com` in scope? It's not listed but I see it returns target's branding. Please advise."

Wait for confirmation. Document the response.
