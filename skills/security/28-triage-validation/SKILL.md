---
name: triage-validation
description: Validate a bug bounty finding before writing a report — the 7-Question Gate, 4 pre-submission gates, always-rejected list, conditional chain table, CVSS 3.1 quick reference, and severity decision guide. Use BEFORE writing any report to avoid N/A and low quality submissions.
metadata:
  type: skill
  phase: output
  always_use: before_report
---

# Triage & Validation

> One wrong answer = kill the finding. Saves your N/A ratio.

## When to invoke

**Trigger phrases:**
- "validate finding"
- "is this reportable"
- "should I submit this"
- "7 question gate"
- "run the gates"

**Always invoke this BEFORE `[[hackerone-reporting]]` or `[[bugcrowd-reporting]]`.**

## The 7-Question Gate

Before writing ANY report, answer all 7. If you can't, kill or improve the finding.

### Q1: Is this in scope?

- [ ] The vulnerable asset is explicitly listed in scope OR matches a wildcard (`*.target.com`)
- [ ] The asset is NOT in the out-of-scope list
- [ ] The asset is NOT an acquisition < 6 months old (often excluded)
- [ ] The vulnerability class is NOT in the program's "Excluded vulnerabilities"

**If any "No" → don't submit. Re-read program scope.**

### Q2: Is the vuln class accepted?

Check the program's "What we DO accept" and "What we DO NOT accept" sections.

Common always-rejected:
- Self-XSS only
- Missing security headers without exploit
- CSRF on logout
- Subdomain takeover (if excluded)
- Open redirect (if excluded or no chain)
- Email enumeration without bypass
- Rate limiting alone
- TLS/SSL config without exploit
- Clickjacking without sensitive action
- Outdated software without exploit
- Stack trace / version disclosure alone
- Banner grabbing
- DoS / DDoS
- Physical / social engineering
- Spam / phishing email send
- "Theoretical" without working PoC

→ See `docs/always-rejected-list.md` for complete list.

### Q3: Do I have a working PoC?

- [ ] Step-by-step reproduces the bug
- [ ] Works with fresh accounts (not just my long-lived test account)
- [ ] Works in a clean browser (no extensions modifying behavior)
- [ ] Reproduces consistently (3+ attempts)
- [ ] Includes exact request/response, not just description

**If not → don't submit yet. Make it bulletproof.**

### Q4: What is the real-world impact?

The bug must have one of:
- **Confidentiality:** unauthorized data access (PII, financials, internal data)
- **Integrity:** unauthorized data modification (write/delete)
- **Availability:** affecting other users (DoS via crafted payload)
- **Auth bypass:** privilege escalation, ATO
- **Cost:** measurable financial impact (refund abuse, coupon stacking)

If you can't write a single sentence describing the impact to the business, it's not a bug.

**Bad impact:**
- "An attacker could potentially..."
- "Theoretically, this might..."
- "If an attacker had X..."

**Good impact:**
- "Any unauthenticated user can read all other users' email addresses by iterating IDs from 1-2M."
- "An attacker can refund a $5,000 purchase to their own account."
- "Logged-in users can elevate themselves to admin by sending a single PATCH request."

### Q5: Is this a duplicate?

Check before submitting:
- Program's disclosed reports for similar issues
- Recent fixes mentioned in their security blog
- Browser cache: have YOU seen this elsewhere?
- Public databases: WPScan vuln DB, etc., for known issues

If the same bug was disclosed 6 months ago and still works → may be a regression (report it).
If just fixed → don't submit. Look for variants.

### Q6: What severity will the program assign?

Match CVSS 3.1 + the program's published bounty table:

```
                    Confidentiality  Integrity  Availability
Network attack    +
Low complexity    +
No privileges     +
No user interact  +
Changed scope     +
High impact       +     C:H            I:H        A:H
                    = Critical (9.0-10.0)
```

→ See `docs/cvss-3.1-quick-reference.md` for fast scoring.

Don't inflate. Conservative scoring → better triager relationship.

### Q7: Does it pass the "would I pay for this" test?

Pretend you're the program manager with a $50k/year bug bounty budget.
- Would YOU pay $X for this bug?
- Is the impact worth the time you're asking triage to spend?

If the answer is "barely" → consider chaining it with another finding for better severity.

## The 4 Pre-Submit Gates (after 7Q passes)

### Gate 1: PoC reproducibility
- Test on a fresh account
- Test from a different browser
- Test from a different IP if possible
- Document the EXACT request (cookies, headers, body)
- Time the entire reproduction (target: < 5 minutes)

### Gate 2: Report quality
- Title is specific and impact-led
- Steps are numbered and self-contained
- Request/response examples are precise
- Impact section is concrete, not theoretical
- "Suggested fix" is present and actionable

### Gate 3: Affected scope
- Single user vs all users — clear
- Affected versions / endpoints listed
- "What does this NOT affect" noted (limits chest-thumping)

### Gate 4: Disclosure ethics
- Did you cause harm during testing?
- Did you access more data than necessary?
- Did you delete what you accessed during PoC?
- Are you compliant with the program's testing rules?

## Always-Rejected Quick List

Don't submit these without serious chain potential:

| Class | Why rejected | When OK |
|---|---|---|
| Self-XSS | Only attacker affected | Chain to ATO of attacker |
| Missing security headers | No exploit | Chain to actual XSS / clickjack of sensitive action |
| Clickjacking on non-sensitive page | Low impact | Sensitive action + PoC video |
| CSRF on logout | Low impact | If logout triggers other security action |
| Open redirect | Often noisy | Chain to OAuth / SSRF |
| Subdomain takeover | If excluded | If allowed AND you took it over |
| Email enumeration | Common, low | Bypass of intentionally hidden enum |
| Rate limiting | Often weak | Specific business impact (e.g., brute auth) |
| Version disclosure | Banner | CVE that hits this version |
| Stack trace on errors | Info disclosure | Sensitive info in trace |
| TLS/SSL config | Tooling | Specific exploitable cipher with PoC |
| DoS via large request | Excluded usually | Permanent damage |

→ See `docs/always-rejected-list.md` for full table.

## Conditional Chain Table

Some findings are weak alone but strong chained. Look for these multipliers:

| Weak finding | Chain potential | Combined severity |
|---|---|---|
| Open redirect | OAuth callback abuse | Critical |
| IDOR (read email) | Password reset → ATO | Critical |
| XSS (low impact) | Cookie steal → session hijack | High-Critical |
| Subdomain takeover | Cookie scope `.target.com` → cookie steal | High-Critical |
| SSRF (localhost only) | Internal admin endpoint | Critical |
| Cache poisoning | Reflected XSS unkeyed | Critical |
| File upload (PNG/JPG) | SVG XSS → admin viewer ATO | Critical |
| CRLF injection | Set-Cookie injection → session fixation | High |
| CORS misconfig | + creds reflected + sensitive endpoint | High |
| JWT info disclosure | + alg=none accepted | Critical |
| Stored XSS (own profile) | Admin views profile → admin ATO | Critical |

→ See `docs/conditional-chain-table.md` for the full table.

## CVSS 3.1 Quick Reference

Mental shortcut:

```
ATTACK VECTOR
  Network = N      Adjacent = A     Local = L    Physical = P

ATTACK COMPLEXITY
  Low = L          High = H

PRIVILEGES REQUIRED
  None = N         Low = L          High = H

USER INTERACTION
  None = N         Required = R

SCOPE
  Unchanged = U    Changed = C

CIA Impact (each)
  None = N         Low = L          High = H

Format: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
```

Quick mental scoring:

- All N/L/N/N + S:U + C:H = ~7.5 (High)
- All N/L/N/N + S:C + C:H = ~9.1 (Critical)
- N/L/L/N + C:H = ~6.5 (Medium)
- N/L/L/R + C:H = ~6.1 (Medium)

CVSS Calculator: https://www.first.org/cvss/calculator/3.1

## Severity Decision Guide

```
                    Yes ─→ Critical
                   /
       Unauth?  ──/
       /         \
      /            No ─→  Could the bug allow an attacker to
   Yes              \    affect MANY users at once? 
   /                 \
  /                   Yes ─→ High
 /                  /
Bug                /
 \              No
  \              \
   No             \─→  Medium / Low
    \
     "informative" or "not applicable"
```

## Title formula

**Bad:**
- "XSS"
- "I found a bug"
- "Reflected XSS in q parameter"

**Good (impact-led):**
- "Stored XSS in profile bio enables session theft of any user viewing the profile"
- "IDOR in /api/v3/orders/{id} exposes financial records of all 2M+ users"
- "Race condition in /coupon/apply allows unlimited redemption of single-use coupons"

Formula: `<vuln class>` in `<endpoint/feature>` enables `<concrete impact>` to `<who/what>`

## Impact statement formula

```
By [doing X], an attacker can [achieve Y], affecting [Z users/data/systems], 
resulting in [concrete business impact: dollar loss / data exposure / reputation].
```

Example:
> By sending a crafted GET request to `/api/v3/user/{id}/notifications` with the user ID of any victim, an unauthenticated attacker can read all notifications including embedded email addresses for any of the 2M+ registered users. This constitutes a GDPR breach (personal data exposed) and enables mass-scale phishing campaigns against affected users.

## Pre-submit checklist (60 seconds)

```
[ ] Re-read program scope and OOS list
[ ] PoC reproducible from cold start
[ ] All requests/responses sanitized of YOUR data only
[ ] Title is impact-led, specific
[ ] Impact section is concrete
[ ] CVSS conservatively estimated
[ ] No accidentally disclosed others' data
[ ] No screenshots with your account's real PII (if shared platform)
[ ] Suggested fix is realistic
[ ] You'd accept this report if you were the triager
```

## Cross-references

- `[[hackerone-reporting]]` — write the report (after this passes)
- `[[bugcrowd-reporting]]` — Bugcrowd version
- `[[program-selection]]` — done long before this
- All vuln-class skills — back-reference impact sections

## Common pitfalls

1. **Skipping Q5 (duplicate check).** 30% of N/A is duplicates that disclosed reports would've shown.
2. **Inflating severity.** Triagers downgrade, your reputation suffers.
3. **Reporting "theoretical" issues without PoC.** Always have a working demo.
4. **Self-XSS or self-only issues.** Save your N/A ratio.
5. **Missing the "what does this NOT affect" disclosure.** Honesty builds trust with triage.

## When to ditch a finding

- Fails 7Q
- Already disclosed within last 6 months
- Impact is theoretical only
- Severity would be at most Informative
- Effort to write report > expected payout

Move on. Tomorrow is another target.
