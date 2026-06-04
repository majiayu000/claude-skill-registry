---
name: hackerone-reporting
description: Write production-grade HackerOne reports — title formula, impact-led writing, CVSS 3.1 scoring, complete PoC formatting, attached files, and submission etiquette. Use AFTER triage-validation passes and you're ready to submit on HackerOne.
metadata:
  type: skill
  phase: output
  platforms: [hackerone]
---

# HackerOne Reporting

> A great report turns a $1,500 medium into a $3,500 medium-with-warm-relationship.

## When to invoke

**Trigger phrases:**
- "write H1 report"
- "HackerOne template"
- "submit on HackerOne"
- "format for H1"

## Prerequisites
- Passed `[[triage-validation]]` 7-Question Gate
- Working PoC, reproduced from cold start
- Clear severity in mind (don't inflate)

## HackerOne report structure (the template)

```markdown
**Summary:**
[1-2 sentence executive summary — what's the bug, what's the impact]

**Description:**
[3-5 sentences on the affected feature, root cause, and how it was discovered]

**Steps To Reproduce:**
1. [first step]
2. [next step]
3. [next step]
4. [observed outcome]

**Supporting Material/References:**
- Screenshot: attached as `screenshot-1.png`
- Video: attached as `poc-recording.mp4`
- HAR file: attached as `repro.har`
- Burp requests: included inline below

**Impact:**
[3-5 sentences. Concrete. Concrete. Concrete.]
- What does this allow an attacker to do?
- How many users / records / dollars are affected?
- What's the worst-case scenario?
- Is there a chain to a higher-severity attack?
```

The default H1 template has these fields. Fill all of them.

## Title formula

**Format:** `<Severity-implication>: <Vuln-class> in <endpoint/feature> enables <impact>`

Examples:

```
# Good titles
Critical: IDOR in GraphQL `user` query enables PII disclosure of all 2M+ users
High: Stored XSS via SVG avatar upload leads to session theft on profile view
High: SSRF in document import URL → AWS IAM credential disclosure
High: Race condition in coupon redemption enables unlimited single-use coupon abuse
Critical: alg=none JWT acceptance enables authentication bypass to any user
Critical: Web cache poisoning via X-Forwarded-Host injects phishing link on /home

# Avoid
XSS                                  ← too vague
IDOR found on website                ← no impact
Possible XSS in search               ← weak language
Vulnerability                        ← useless
```

The title sells the report. It's the first thing the triager sees on their dashboard.

## The full report (production-grade example)

```markdown
**Summary:**
The `/api/v3/user/{user_id}/notifications` endpoint does not validate that the requesting user matches the path's `user_id`, allowing any authenticated user to read any other user's notifications. Notifications contain email addresses, internal IDs, and message previews, enabling PII enumeration of all 2M+ user accounts.

**Description:**
While reviewing the user dashboard's network traffic, I observed a request to `/api/v3/user/{user_id}/notifications` that returned the user's own notifications. The endpoint uses the `user_id` from the URL path rather than from the authenticated session. By substituting another user's ID (obtained via UUID enumeration from referrer headers in past disclosed bugs), I was able to retrieve their notifications without authorization.

The root cause appears to be missing authorization middleware on this specific REST route — other routes under `/api/v3/user/*` correctly compare `request.user.id === request.params.user_id`.

**Steps To Reproduce:**

1. Create two test accounts:
   - Account A (attacker): `attacker+bbarsenal-1@example.com` — user_id `AAAA-1111-2222-3333-4444`
   - Account B (victim): `attacker+bbarsenal-2@example.com` — user_id `BBBB-5555-6666-7777-8888`

2. Log in as Account A in a clean browser, capture the `session_cookie`:
   ```
   session_cookie=eyJhbGc...  (32-character session token)
   ```

3. Send the following request:
   ```http
   GET /api/v3/user/BBBB-5555-6666-7777-8888/notifications HTTP/1.1
   Host: app.target.com
   Cookie: session_cookie=eyJhbGc...
   Accept: application/json
   ```

4. Response (200 OK) — contains Account B's notifications:
   ```json
   {
     "user_id": "BBBB-5555-6666-7777-8888",
     "email": "attacker+bbarsenal-2@example.com",
     "notifications": [
       {
         "id": 47239,
         "type": "invoice_paid",
         "subject": "Your invoice #5039 has been paid",
         "preview": "Hello Test User B...",
         "received_at": "2026-06-01T10:14:55Z",
         "read": false
       },
       ...8 more notifications...
     ]
   }
   ```

5. Repeated with arbitrary user IDs (UUID brute or via leaked IDs from features like @-mentions in comments) returns each user's data.

**Supporting Material/References:**
- screenshot-1.png — Browser developer tools showing the IDOR request and response
- video-repro.mp4 — 90-second walkthrough of reproduction from scratch
- repro.har — HAR file of the entire reproduction session
- attached.curl — raw curl command for one-line reproduction

**Impact:**

Any authenticated user (signup is free and immediate) can enumerate the notifications of every registered user on the platform. Notifications contain:
- Email addresses (PII — GDPR/CCPA scope)
- Invoice IDs (which are sequential and let attackers infer total order volume)
- Message previews (may include internal mentions or task descriptions)
- Notification timestamps (activity patterns)

Concrete impact:
1. **Mass PII collection**: With 2.3M+ users (per the "About" page), an attacker can scrape emails + activity metadata for all of them.
2. **GDPR exposure**: Email + activity metadata pairing is identifiable personal data; compliance breach.
3. **Phishing setup**: Attackers learn what notifications look like (subject lines, sender), enabling indistinguishable phishing emails.
4. **Chain potential**: Combined with the `email` exposure here, password reset (email-only flow per the Help Center) becomes a viable ATO vector — see also report #XXXXXX [reference past dupe if any].

**Suggested Fix:**
Add an authorization check at the controller for `/api/v3/user/{user_id}/notifications`:
```javascript
// pseudo
if (req.session.user_id !== req.params.user_id && !req.session.is_admin) {
  return res.status(403).json({ error: 'forbidden' });
}
```
Audit other endpoints under `/api/v3/user/*` for the same pattern — initial review suggests `/profile`, `/billing`, and `/sessions` may have the same issue.

**Test accounts and artifacts will be retained for verification or removed upon request.**
```

## Best practices

### 1. Lead with impact
Hooks the triager: "*This bug allows ATO of any user with one request.*" — triager pays attention.

### 2. Use exact requests and responses
Copy-paste the actual HTTP traffic. Don't summarize. Triagers verify by replaying.

### 3. Reproduction with TWO accounts
For any cross-user bug (IDOR, ATO, multi-tenant): provide both account credentials or use the program's test accounts.

### 4. Attachments
- **Screenshots:** Annotated with arrows/circles. Show the affected vs expected behavior.
- **Videos:** Keep under 2 minutes. Start with the bug demo, not the long setup.
- **HAR files:** Use Burp's "Save HAR" or browser dev tools. Includes everything triager needs.
- **Burp requests:** Copy raw HTTP to make replay trivial.

### 5. Severity & CVSS
Use the CVSS field with a vector string:
```
CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N → 6.5 (Medium)
```

Match the program's table. Conservative scoring builds trust.

### 6. Don't bury the lead
Triagers spend < 60 seconds on first read. The Summary section is everything. If it's vague, the report is closed.

### 7. Single-bug per report
One issue per submission. If you found 3 IDORs, file 3 reports (or 1 with "found on multiple endpoints" — varies by program).

### 8. Markdown formatting
H1 supports markdown. Use it:
- `**bold**` for emphasis
- Code blocks with triple-backticks
- Lists (`-` and `1.`)
- Headers (`##`)

### 9. Don't include exploit binaries
Attach text PoCs. Triage may sandbox; binaries trigger security flags.

### 10. Authorization context (note for offensive demos)
"For PoC, I created Account A and B (both test accounts in my control). No real user data was accessed."

## Severity → bounty mapping (typical H1)

```
Critical:   $2,000 - $30,000+   (CVSS 9.0-10.0)
High:       $700  - $5,000      (CVSS 7.0-8.9)
Medium:     $200  - $1,500      (CVSS 4.0-6.9)
Low:        $50   - $400        (CVSS 0.1-3.9)
Informative: $0                 (acknowledgment only)
```

Match against the program's stated table.

## After submission — etiquette

### Wait for triage (be patient)
- Most H1 programs: 24-48h first response
- Don't ping unless > 7 days with no update
- If pinged for clarification: respond fast, specific

### Negotiation tactics

**Triager says "severity Medium":**
- Don't argue tone. Argue specifics.
- ✗ "This is clearly High, you don't understand."
- ✓ "Thanks for the assessment. I'd like to push back on the severity given:
  1. Affects all 2M+ users (not 'some')
  2. No authentication required (unauth class)
  3. PII disclosed (GDPR scope)
  
  By the CVSS:3.1 vector AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N = 7.5 (High).
  
  Could you reconsider with these in mind?"

**Triager says "duplicate":**
- Ask politely for the original report ID
- Verify it's actually the same bug (or just same class)
- If not actually a dupe: explain why

**Triager closes as Informative:**
- Ask what would change their mind
- Often: more impact framing, chain demo, or stronger PoC

### If awarded
Thank the team. Briefly. Don't gush.

### If disputed
Stay calm. State facts. Reference the original PoC. Most disputes resolve via more PoC.

## Cross-references

- `[[triage-validation]]` — run before this
- `[[bugcrowd-reporting]]` — Bugcrowd variant
- `[[program-selection]]` — choose programs with fair triage history
- All vuln-class skills — back-reference for impact statements

## Common pitfalls

1. **Wall of text Summary.** Keep it 1-2 sentences.
2. **PoC that requires triager to assume / fill in.** Be explicit.
3. **No attachments.** Triagers love HAR + screenshots.
4. **Inflated severity.** Hurts your H1 reputation score.
5. **Multiple bugs in one report.** Confuses triage, may get partial bounty.

## Hot tips

- **Get H1 verified.** Verified researchers get faster triage.
- **Stay in the Top X% of resolvers.** Reputation = priority queue.
- **Public disclosure later.** Once paid + fixed, request disclosure → builds your portfolio.
- **Link to your past disclosed reports** in the description (if relevant chain) — shows depth.

## H1 metadata fields

H1 form has these structured fields:
- **Title** — see formula above
- **Weakness** — CWE category (e.g., CWE-639 for IDOR, CWE-79 for XSS)
- **Severity** — your CVSS-implied severity
- **Affected URL(s)** — comma-separated
- **Asset Identifier** — match to the in-scope asset from program scope
- **Attachments** — drop-zone for PNG/MP4/PDF/HAR

Fill all of them. Missing structured fields can delay triage.

## Quick markdown report skeleton

Copy-paste this into the H1 report form, then fill:

```markdown
## Summary
[1-2 sentences — what + impact in plain English]

## Description
[3-5 sentences — affected feature, root cause hypothesis]

## Steps To Reproduce

1. Create test accounts:
   - Account A (attacker): `<email>` user_id `<id>`
   - Account B (victim): `<email>` user_id `<id>`

2. As Account A, send:
   ```http
   <full request including cookies>
   ```

3. Response (200 OK):
   ```json
   <response showing the IDOR / bypass / leak>
   ```

4. Reproducibility: tested in Chrome 124, Firefox 125; works fresh.

## Supporting Material
- screenshot-1.png — [what it shows]
- video-repro.mp4 — [90 second walkthrough]
- repro.har — [HAR file of session]

## Impact

[Concrete, business-grade impact.]
- Users affected: [number]
- Data class: [PII / financial / system]
- Chain potential: [yes/no, what next]

## Suggested Fix

[Specific, actionable. Show code if possible.]

## CVSS
`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` (7.5 High)

## Notes
- Tested with my own test accounts only
- No real user data was accessed
- Test accounts will be retained / deleted as needed
```
