---
name: xmpp-enumeration
description: >
  XMPP/Jabber service enumeration for Openfire, ejabberd, Prosody, and other
  XMPP servers. Trigger when ports 5222 (client), 5223 (legacy TLS), or 5269
  (server-to-server) are found open. Covers authentication testing, user
  enumeration, MUC room discovery, and server fingerprinting. Do NOT use for
  AD enumeration or credential spraying — route those to the appropriate skills.
keywords:
  - xmpp
  - jabber
  - openfire
  - ejabberd
  - prosody
  - "5222"
  - "5223"
  - "5269"
  - xep-0077
  - sasl
  - anonymous
  - muc
  - in-band registration
  - chat
  - instant messaging
tools:
  - python3
  - nmap
opsec: low
---

# XMPP/Jabber Enumeration

You are helping a penetration tester enumerate an XMPP/Jabber service. This
skill covers service detection, authentication testing, user enumeration, MUC
(Multi-User Chat) room discovery, and server fingerprinting. All testing is
under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[xmpp-enumeration] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `xmpp-users.txt`, `xmpp-rooms.txt`,
  `xmpp-server-info.txt`).

## Scope Boundary

This skill covers XMPP service enumeration only. It does NOT cover:
- AD enumeration or Kerberos attacks — route to **ad-discovery**
- Credential spraying or brute force — route to **password-spraying**
- Web application testing (even Openfire admin console) — route to **web-discovery**
- Exploitation of RCE vulnerabilities in XMPP servers — report and return

When enumeration is complete, STOP and return to the orchestrator with
discovered users, rooms, server details, and recommendations for next skills.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

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

- XMPP port open: 5222 (STARTTLS), 5223 (legacy TLS), or 5269 (S2S)
- **python3** — for raw XML socket interaction (no external libraries required)
- **nmap** — for initial service probing (via MCP nmap-server)
- Optional: `slixmpp` Python library (if installed, simplifies some steps)

### Special characters in credentials

Bash history expansion treats `!` as a special character (`!event`), even
inside double quotes. Passwords containing `!`, `$`, backticks, or other
shell metacharacters will be silently mangled when passed as command arguments.

**Canonical workaround** — write to file, read from file:

```bash
# 1. Use the Write tool (not echo/printf) to create a password file
Write("/tmp/claude-1000/cred.txt", "lDaP_1n_th3_cle4r!")

# 2. Read into a variable
PASS=$(cat /tmp/claude-1000/cred.txt)

# 3. Use the variable in commands (double-quote it)
python3 xmpp_enum.py --password "$PASS"
```

## Step 1: Service Detection

Confirm XMPP service and identify the server software.

### 1a. Nmap Service Probes

Use the nmap MCP to scan XMPP ports:

```
nmap_scan(target="<IP>", options="-sV -p 5222,5223,5269,5270,5275,5276,7070,7443,9090,9091 -sC")
```

Key ports:
| Port | Service | Notes |
|------|---------|-------|
| 5222 | XMPP client (STARTTLS) | Primary client connection |
| 5223 | XMPP client (legacy TLS) | Direct TLS, older servers |
| 5269 | XMPP server-to-server | Federation port |
| 5270 | XMPP S2S (TLS) | Secure federation |
| 5275 | XMPP component | External component interface |
| 7070 | HTTP binding (BOSH) | Web client access |
| 7443 | HTTPS binding (BOSH) | Secure web client access |
| 9090 | Openfire admin (HTTP) | Admin console — route to **web-discovery** |
| 9091 | Openfire admin (HTTPS) | Admin console — route to **web-discovery** |

### 1b. TLS Certificate Inspection

Extract hostname and organization from the TLS certificate:

```bash
# STARTTLS on 5222
echo | openssl s_client -starttls xmpp -connect <IP>:5222 -servername <domain> 2>/dev/null | openssl x509 -noout -subject -issuer -dates

# Direct TLS on 5223
echo | openssl s_client -connect <IP>:5223 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

The certificate CN or SAN fields often reveal the XMPP domain (e.g.,
`jab.htb`, `chat.corp.local`).

### 1c. Raw XMPP Stream Probe

Send an initial stream header to identify the server and supported features:

```python
#!/usr/bin/env python3
"""XMPP stream probe — identifies server software and SASL mechanisms."""
import socket
import ssl
import sys

TARGET = sys.argv[1]  # IP or hostname
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def probe(target, port, domain, use_tls=False):
    sock = socket.create_connection((target, port), timeout=10)
    if use_tls:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=domain)

    sock.sendall(STREAM_HEADER.encode())
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            # Stop once we have features or stream error
            if b"</stream:features>" in data or b"</stream:error>" in data:
                break
        except socket.timeout:
            break
    sock.close()
    return data.decode(errors="replace")

# Try plain first (STARTTLS), then direct TLS
for use_tls in [False, True]:
    try:
        label = "TLS" if use_tls else "plain"
        print(f"[*] Probing {TARGET}:{PORT} ({label})...")
        resp = probe(TARGET, PORT, DOMAIN, use_tls)
        print(resp)
        break
    except Exception as e:
        print(f"[-] {label} failed: {e}")
```

**What to look for in the response:**
- `<stream:features>` block lists supported authentication mechanisms
- SASL mechanisms: `PLAIN`, `SCRAM-SHA-1`, `ANONYMOUS`, `EXTERNAL`, `DIGEST-MD5`
- `<register xmlns='http://jabber.org/features/iq-register'/>` = in-band registration enabled (XEP-0077)
- Server identification in stream header attributes or error messages

## Step 2: Authentication Testing

Test what authentication options are available without credentials.

### 2a. SASL ANONYMOUS

If `ANONYMOUS` appears in the SASL mechanisms, the server allows anonymous
login — this is a significant finding:

```python
#!/usr/bin/env python3
"""Test SASL ANONYMOUS authentication."""
import socket
import ssl
import base64
import sys

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def recv_until(sock, marker, timeout=10):
    sock.settimeout(timeout)
    data = b""
    while marker.encode() not in data:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

sock = socket.create_connection((TARGET, PORT), timeout=10)

# Start stream
sock.sendall(STREAM_HEADER.encode())
features = recv_until(sock, "</stream:features>")
print("[*] Features:", features[:500])

# Check for STARTTLS and upgrade if available
if "<starttls" in features:
    sock.sendall(b"<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
    resp = recv_until(sock, "/>")
    if "<proceed" in resp:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=DOMAIN)
        # Restart stream after TLS
        sock.sendall(STREAM_HEADER.encode())
        features = recv_until(sock, "</stream:features>")
        print("[*] Post-TLS features:", features[:500])

if "ANONYMOUS" not in features:
    print("[-] SASL ANONYMOUS not supported")
    sock.close()
    sys.exit(1)

# Authenticate as anonymous
sock.sendall(b"<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='ANONYMOUS'/>")
resp = recv_until(sock, ">")
print("[*] Auth response:", resp)

if "<success" in resp:
    print("[+] ANONYMOUS authentication succeeded!")
    # Restart stream to get bound JID
    sock.sendall(STREAM_HEADER.encode())
    features = recv_until(sock, "</stream:features>")
    # Bind resource
    sock.sendall(b"<iq type='set' id='bind1'><bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'><resource>enum</resource></bind></iq>")
    resp = recv_until(sock, "</iq>")
    print("[+] Bound JID:", resp)
else:
    print("[-] ANONYMOUS auth failed:", resp)

sock.close()
```

### 2b. In-Band Registration (XEP-0077)

If the stream features include `<register>`, test in-band registration:

```python
#!/usr/bin/env python3
"""Test XEP-0077 in-band registration and register an account."""
import socket
import ssl
import sys

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET
USERNAME = sys.argv[4] if len(sys.argv) > 4 else "testuser123"
PASSWORD = sys.argv[5] if len(sys.argv) > 5 else "TestPass123!"

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def recv_until(sock, marker, timeout=10):
    sock.settimeout(timeout)
    data = b""
    while marker.encode() not in data:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

sock = socket.create_connection((TARGET, PORT), timeout=10)
sock.sendall(STREAM_HEADER.encode())
features = recv_until(sock, "</stream:features>")

# STARTTLS upgrade if available
if "<starttls" in features:
    sock.sendall(b"<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
    resp = recv_until(sock, "/>")
    if "<proceed" in resp:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=DOMAIN)
        sock.sendall(STREAM_HEADER.encode())
        features = recv_until(sock, "</stream:features>")

# Query registration fields
sock.sendall(f"<iq type='get' id='reg1' to='{DOMAIN}'><query xmlns='jabber:iq:register'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print("[*] Registration fields:", resp)

if "error" in resp.lower() and "not-allowed" in resp.lower():
    print("[-] In-band registration is disabled")
    sock.close()
    sys.exit(1)

# Attempt registration
reg_iq = f'''<iq type='set' id='reg2'>
  <query xmlns='jabber:iq:register'>
    <username>{USERNAME}</username>
    <password>{PASSWORD}</password>
  </query>
</iq>'''
sock.sendall(reg_iq.encode())
resp = recv_until(sock, "</iq>")
print("[*] Registration response:", resp)

if "<error" not in resp:
    print(f"[+] Account registered: {USERNAME}@{DOMAIN}")
elif "conflict" in resp.lower():
    print(f"[!] Username '{USERNAME}' already exists (conflict error)")
    print("[+] This confirms in-band registration is enabled and can be used for user enumeration")
else:
    print(f"[-] Registration failed: {resp}")

sock.close()
```

**If registration succeeds**, you now have valid credentials. Report the
registered account and proceed to user enumeration with authenticated access.

## Step 3: User Enumeration

Enumerate valid usernames on the XMPP server. Multiple techniques available
depending on access level.

### 3a. Registration Conflict Enumeration (Unauthenticated)

If in-band registration is enabled, you can enumerate users by attempting to
register known usernames and checking for `<conflict/>` errors:

```python
#!/usr/bin/env python3
"""Enumerate XMPP users via registration conflict errors."""
import socket
import ssl
import sys
import time

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET
USERFILE = sys.argv[4] if len(sys.argv) > 4 else "/usr/share/seclists/Usernames/xato-net-10-million-usernames-dup.txt"

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def recv_until(sock, marker, timeout=10):
    sock.settimeout(timeout)
    data = b""
    while marker.encode() not in data:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

def connect_and_tls():
    sock = socket.create_connection((TARGET, PORT), timeout=10)
    sock.sendall(STREAM_HEADER.encode())
    features = recv_until(sock, "</stream:features>")
    if "<starttls" in features:
        sock.sendall(b"<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
        resp = recv_until(sock, "/>")
        if "<proceed" in resp:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=DOMAIN)
            sock.sendall(STREAM_HEADER.encode())
            recv_until(sock, "</stream:features>")
    return sock

found_users = []
with open(USERFILE) as f:
    usernames = [line.strip() for line in f if line.strip()]

print(f"[*] Testing {len(usernames)} usernames against {DOMAIN}")

sock = connect_and_tls()
count = 0

for username in usernames:
    try:
        reg_iq = f'''<iq type='set' id='enum{count}'>
          <query xmlns='jabber:iq:register'>
            <username>{username}</username>
            <password>EnumPass123!</password>
          </query>
        </iq>'''
        sock.sendall(reg_iq.encode())
        resp = recv_until(sock, "</iq>")

        if "conflict" in resp.lower():
            print(f"[+] EXISTS: {username}@{DOMAIN}")
            found_users.append(username)
        elif "<error" not in resp:
            # Account was actually created — also valid info
            print(f"[+] REGISTERED: {username}@{DOMAIN} (new account created)")
            found_users.append(username)

        count += 1
        # Reconnect periodically to avoid stream timeouts
        if count % 100 == 0:
            try:
                sock.close()
            except Exception:
                pass
            sock = connect_and_tls()
            print(f"[*] Progress: {count}/{len(usernames)} tested, {len(found_users)} found")

    except Exception as e:
        print(f"[!] Error on {username}: {e}")
        try:
            sock.close()
        except Exception:
            pass
        sock = connect_and_tls()

sock.close()

print(f"\n[*] Enumeration complete: {len(found_users)}/{len(usernames)} users found")
for u in found_users:
    print(f"  {u}@{DOMAIN}")
```

**Note:** This technique registers accounts for non-existent usernames. Use a
small, targeted username list (top 1000) rather than a massive wordlist to
avoid creating thousands of accounts. If the engagement scope allows it, clean
up registered accounts afterward.

### 3b. Roster/Contact Queries (Authenticated)

With authenticated access (from registration or provided credentials):

```python
#!/usr/bin/env python3
"""Query user roster and service discovery with authenticated XMPP session."""
import socket
import ssl
import base64
import sys

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET
USERNAME = sys.argv[4]
PASSWORD = sys.argv[5]

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def recv_until(sock, marker, timeout=10):
    sock.settimeout(timeout)
    data = b""
    while marker.encode() not in data:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

sock = socket.create_connection((TARGET, PORT), timeout=10)
sock.sendall(STREAM_HEADER.encode())
features = recv_until(sock, "</stream:features>")

# STARTTLS
if "<starttls" in features:
    sock.sendall(b"<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
    resp = recv_until(sock, "/>")
    if "<proceed" in resp:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=DOMAIN)
        sock.sendall(STREAM_HEADER.encode())
        features = recv_until(sock, "</stream:features>")

# SASL PLAIN authentication
auth_str = f"\x00{USERNAME}\x00{PASSWORD}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()
sock.sendall(f"<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='PLAIN'>{auth_b64}</auth>".encode())
resp = recv_until(sock, ">")

if "<success" not in resp:
    print(f"[-] Authentication failed: {resp}")
    sock.close()
    sys.exit(1)

print(f"[+] Authenticated as {USERNAME}@{DOMAIN}")

# Restart stream post-auth
sock.sendall(STREAM_HEADER.encode())
features = recv_until(sock, "</stream:features>")

# Bind resource
sock.sendall(b"<iq type='set' id='bind1'><bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'><resource>enum</resource></bind></iq>")
resp = recv_until(sock, "</iq>")
print(f"[*] Bound: {resp}")

# Query roster
sock.sendall(b"<iq type='get' id='roster1'><query xmlns='jabber:iq:roster'/></iq>")
resp = recv_until(sock, "</iq>")
print(f"[*] Roster:\n{resp}")

# Service discovery — discover server items (MUC, users directory, etc.)
sock.sendall(f"<iq type='get' id='disco1' to='{DOMAIN}'><query xmlns='http://jabber.org/protocol/disco#items'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print(f"[*] Server items:\n{resp}")

# Service discovery — server info
sock.sendall(f"<iq type='get' id='disco2' to='{DOMAIN}'><query xmlns='http://jabber.org/protocol/disco#info'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print(f"[*] Server info:\n{resp}")

# Search for users directory (XEP-0055)
sock.sendall(f"<iq type='get' id='search1' to='search.{DOMAIN}'><query xmlns='jabber:iq:search'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print(f"[*] User search service:\n{resp}")

# If search service exists, search for all users (wildcard)
if "error" not in resp.lower():
    sock.sendall(f'''<iq type='set' id='search2' to='search.{DOMAIN}'>
      <query xmlns='jabber:iq:search'>
        <x xmlns='jabber:x:data' type='submit'>
          <field var='FORM_TYPE' type='hidden'><value>jabber:iq:search</value></field>
          <field var='search'><value>*</value></field>
          <field var='Username'><value>1</value></field>
          <field var='Name'><value>1</value></field>
          <field var='Email'><value>1</value></field>
        </x>
      </query>
    </iq>'''.encode())
    resp = recv_until(sock, "</iq>", timeout=30)
    print(f"[*] User search results:\n{resp}")

sock.close()
```

**Large user directories:** If the search returns hundreds or thousands of
users, save the full output to `engagement/evidence/xmpp-users.txt` and
extract usernames for further use:

```bash
# Extract usernames from search results (adapt grep pattern to output format)
grep -oP 'value>\K[^<]+' engagement/evidence/xmpp-users.txt | sort -u > engagement/evidence/xmpp-usernames.txt
```

## Step 4: MUC Room Discovery

Discover Multi-User Chat rooms and check for accessible rooms with message
history.

```python
#!/usr/bin/env python3
"""Discover MUC rooms and retrieve history from open rooms."""
import socket
import ssl
import base64
import sys
import re

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5222
DOMAIN = sys.argv[3] if len(sys.argv) > 3 else TARGET
USERNAME = sys.argv[4]
PASSWORD = sys.argv[5]
MUC_SERVICE = sys.argv[6] if len(sys.argv) > 6 else f"conference.{DOMAIN}"

STREAM_HEADER = f'''<?xml version='1.0'?>
<stream:stream xmlns='jabber:client'
  xmlns:stream='http://etherx.jabber.org/streams'
  to='{DOMAIN}' version='1.0'>'''

def recv_until(sock, marker, timeout=10):
    sock.settimeout(timeout)
    data = b""
    while marker.encode() not in data:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

# Connect + TLS + Auth (same pattern as Step 3b)
sock = socket.create_connection((TARGET, PORT), timeout=10)
sock.sendall(STREAM_HEADER.encode())
features = recv_until(sock, "</stream:features>")

if "<starttls" in features:
    sock.sendall(b"<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>")
    resp = recv_until(sock, "/>")
    if "<proceed" in resp:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=DOMAIN)
        sock.sendall(STREAM_HEADER.encode())
        features = recv_until(sock, "</stream:features>")

auth_str = f"\x00{USERNAME}\x00{PASSWORD}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()
sock.sendall(f"<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='PLAIN'>{auth_b64}</auth>".encode())
resp = recv_until(sock, ">")
if "<success" not in resp:
    print(f"[-] Auth failed: {resp}")
    sys.exit(1)

sock.sendall(STREAM_HEADER.encode())
recv_until(sock, "</stream:features>")
sock.sendall(b"<iq type='set' id='bind1'><bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'><resource>enum</resource></bind></iq>")
recv_until(sock, "</iq>")

print(f"[+] Authenticated as {USERNAME}@{DOMAIN}")

# Discover MUC rooms
sock.sendall(f"<iq type='get' id='muc1' to='{MUC_SERVICE}'><query xmlns='http://jabber.org/protocol/disco#items'/></iq>".encode())
resp = recv_until(sock, "</iq>", timeout=15)
print(f"[*] MUC rooms:\n{resp}")

# Extract room JIDs
rooms = re.findall(r"jid='([^']+)'", resp)
if not rooms:
    rooms = re.findall(r'jid="([^"]+)"', resp)

print(f"\n[*] Found {len(rooms)} rooms")

# Try to join each room and read history
for room in rooms[:20]:  # Limit to first 20 rooms
    print(f"\n[*] Joining {room}...")
    # Join with history request
    join = f'''<presence to='{room}/{USERNAME}'>
      <x xmlns='http://jabber.org/protocol/muc'>
        <history maxstanzas='50'/>
      </x>
    </presence>'''
    sock.sendall(join.encode())

    # Read messages (may include history)
    resp = recv_until(sock, "</presence>", timeout=5)
    # Also read any message history
    try:
        sock.settimeout(3)
        extra = sock.recv(65536).decode(errors="replace")
        resp += extra
    except socket.timeout:
        pass

    if "not-allowed" in resp or "forbidden" in resp:
        print(f"  [-] Access denied to {room}")
    else:
        msg_count = resp.count("<message")
        print(f"  [+] Joined {room} — {msg_count} messages in history")
        if msg_count > 0:
            print(f"  [!] Room has readable history — save to evidence")

    # Leave room
    sock.sendall(f"<presence to='{room}/{USERNAME}' type='unavailable'/>".encode())
    recv_until(sock, ">", timeout=3)

sock.close()
```

**Interesting findings in MUC rooms:**
- Credentials shared in chat messages (passwords, tokens, API keys)
- Internal hostnames, IP addresses, and infrastructure details
- Employee names mapping to AD usernames
- Application URLs, deployment details, internal documentation links

Save any interesting room history to `engagement/evidence/xmpp-room-<name>.txt`.

## Step 5: Information Gathering

### 5a. Server Version and Plugins

With authenticated access, query the server for detailed information:

```python
# Query server version (XEP-0092)
sock.sendall(f"<iq type='get' id='ver1' to='{DOMAIN}'><query xmlns='jabber:iq:version'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print(f"[*] Server version: {resp}")

# Query server uptime/stats (admin feature, may be restricted)
sock.sendall(f"<iq type='get' id='stats1' to='{DOMAIN}'><query xmlns='http://jabber.org/protocol/stats'/></iq>".encode())
resp = recv_until(sock, "</iq>")
print(f"[*] Server stats: {resp}")
```

### 5b. Known Vulnerabilities by Server Version

| Server | Version | CVE | Impact |
|--------|---------|-----|--------|
| Openfire | < 4.7.5 | CVE-2023-32315 | Auth bypass → admin console → RCE |
| Openfire | < 4.6.8 | CVE-2023-32315 | Same — path traversal in admin |
| ejabberd | < 23.01 | Various | Check NVD for version-specific |
| Prosody | < 0.12.3 | CVE-2022-0217 | Memory exhaustion DoS |

If the server version matches a known vulnerable version, **report it and
return** — do not attempt exploitation. The orchestrator will route to the
appropriate technique skill.

### 5c. Admin Interface Detection

Openfire exposes admin consoles on separate ports:
- HTTP: `http://<target>:9090`
- HTTPS: `https://<target>:9091`

If these ports were found in the nmap scan, note them for **web-discovery**.
Do not test the web admin interface from this skill.

## Troubleshooting

### Connection refused on 5222
- Server may only listen on 5223 (legacy TLS) — try direct TLS connection
- Check if a firewall is blocking — try from a different source IP
- Server may use non-standard ports — check nmap results for XMPP on other ports

### STARTTLS fails
- Try direct TLS connection on port 5223
- Server may not support TLS — try plain connection (not recommended for auth)
- Certificate hostname mismatch — use `-servername` flag with openssl

### Registration returns "not-allowed"
- In-band registration is disabled (server policy)
- Try SASL ANONYMOUS as an alternative for unauthenticated access
- Report finding and return — user enumeration requires credentials

### Stream error: host-unknown
- Wrong domain in stream header — use the domain from TLS certificate or nmap
- Try variations: `jab.htb`, `jabber.jab.htb`, `chat.jab.htb`
- Check DNS/hosts file for the correct hostname mapping

### Python socket timeout
- Increase timeout values in the scripts (default 10s may be too short)
- Server may be rate-limiting — add delays between requests
- Network latency — try direct TLS (5223) which skips the STARTTLS handshake

### Large user directories (>1000 users)
- The search query may return paginated results — check for result set management
- Save output in chunks to avoid memory issues
- Focus on usernames that match AD naming patterns (first.last, flast, etc.)
