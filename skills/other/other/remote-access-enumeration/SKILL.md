---
name: remote-access-enumeration
description: >
  Enumeration of remote access services: FTP, SSH, RDP, VNC, and WinRM.
  Checks anonymous access, default credentials, version vulnerabilities,
  and authentication methods. Use after network-recon identifies remote
  access ports.
keywords:
  - FTP anonymous
  - SSH version
  - RDP BlueKeep
  - VNC no auth
  - WinRM
  - remote access
  - ftp-anon
  - ssh-auth-methods
  - rdp-ntlm-info
tools:
  - nmap
  - ftp
  - ssh
opsec: low
---

# Remote Access Enumeration

You are helping a penetration tester enumerate remote access services (FTP, SSH,
RDP, VNC, WinRM) on discovered targets. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[remote-access-enumeration] Activated → <target>` on activation.
- **Evidence** → save output to `engagement/evidence/` (e.g., `ftp-anon-listing.txt`).

## Scope Boundary

This skill covers **enumeration only** — version detection, auth method checks,
anonymous access, and known CVE identification. NOT brute force.

- Credential brute force → route to **password-spraying**
- SMB-based RCE → route to **smb-exploitation**
- Exploiting confirmed RCE vulns → return to orchestrator with CVE details

## State Management

Call `get_state_summary()` on activation. Skip already-enumerated services, use
known credentials where relevant, check Blocked for previous failures.

**Interim writes** — write critical discoveries immediately via state-interim:
- FTP anonymous access → `add_vuln(title="FTP anonymous access on <host>", host="<host>", vuln_type="anonymous-access", severity="medium")`
- Credentials in FTP files → `add_credential(username=..., secret=..., source="FTP file on <host>")`
- SSH default creds → `add_credential(username=..., secret=..., source="SSH default creds on <host>")`
- BlueKeep confirmed → `add_vuln(title="BlueKeep CVE-2019-0708 on <host>", host="<host>", vuln_type="rce", severity="critical")`
- NTLM info leak → `add_pivot(from_host="<host>", to_host="<domain>", pivot_type="ntlm-info", details="Domain: <domain>, Hostname: <hostname>, FQDN: <fqdn>")`
- VNC no-auth → `add_vuln(title="VNC no-auth on <host>", host="<host>", vuln_type="anonymous-access", severity="medium")`

Report all findings in your return summary for orchestrator deduplication.

## Prerequisites

- Network access to target host(s)
- Open port list from orchestrator or network-recon
- nmap available via MCP nmap-server

## Port-Based Execution

**Only run sections for ports confirmed open.** Skip any service section whose
port is not in the orchestrator's port list.

## Step 1: FTP (Port 21)

```bash
nmap -sV -p21 --script ftp-anon,ftp-bounce,ftp-syst TARGET_IP
```

**Manual anonymous check:**
```bash
ftp TARGET_IP
# login: anonymous / anonymous@
# If connected: ls -la, pwd, cd / && ls -la
```

If anonymous access succeeds:
1. List all accessible directories recursively
2. Check for writable directories (`put test.txt` then `del test.txt`)
3. Look for config files with credentials (`.htpasswd`, `web.config`, `wp-config.php`)
4. Check if FTP root overlaps with a web root (write test file, check via HTTP)

**Quick wins:**
- **Anonymous write to webroot** — file upload = RCE path
- **ProFTPD mod_copy** (CVE-2019-12815) — copy files without auth:
  `SITE CPFR /etc/passwd` → `SITE CPTO /var/www/html/passwd.txt`
- **vsftpd 2.3.4 backdoor** — username ending in `:)` triggers shell on port 6200

## Step 2: SSH (Port 22)

```bash
nmap -sV -p22 --script ssh2-enum-algos,ssh-hostkey,ssh-auth-methods TARGET_IP
```

**Auth method check:**
```bash
ssh -o PreferredAuthentications=none -o ConnectTimeout=5 root@TARGET_IP 2>&1
```

Look for `publickey,password` (password auth enabled) vs `publickey` only.
Password auth → note for **password-spraying**.

**Quick wins:**
- **User enum** (OpenSSH < 7.7 — CVE-2018-15473): timing-based enumeration
- **regreSSHion** (CVE-2024-6387): OpenSSH 8.5p1–9.7p1 on glibc Linux, pre-auth RCE
- **Key reuse**: matching host keys across hosts → pivot mapping

## Step 3: RDP (Port 3389)

```bash
nmap -sV -p3389 --script rdp-ntlm-info,rdp-enum-encryption TARGET_IP
```

**NTLM info leak** — parse `rdp-ntlm-info` for Target_Name (NetBIOS domain),
DNS_Domain_Name, DNS_Computer_Name, Product_Version. Passive domain discovery.

**NLA check** — from `rdp-enum-encryption`, check if NLA is required.
NLA disabled = brute force viable without valid domain creds.

**BlueKeep** (CVE-2019-0708):
```bash
nmap -p3389 --script rdp-vuln-ms12-020 TARGET_IP
```
Affects Windows 7, Server 2008/2008R2. Pre-auth RCE. If confirmed, write
interim vuln and return to orchestrator immediately.

## Step 4: VNC (Ports 5900-5910)

```bash
nmap -sV -p5900-5910 --script vnc-info,vnc-brute TARGET_IP
```

**No-auth check** — if `vnc-info` reports security type 1 (None): full desktop
access without credentials. Write interim vuln, confirm with `vncviewer TARGET_IP::5900`.

**CVE-2006-2369** — RealVNC 4.1.1 and earlier: auth bypass by requesting
security type None even when server requires authentication.

## Step 5: WinRM (Ports 5985/5986)

```bash
nmap -sV -p5985,5986 TARGET_IP
```

Port 5985 = HTTP, 5986 = HTTPS. No anonymous access possible — credential
testing routes to **password-spraying**.

If valid credentials already in state, test access:
```bash
evil-winrm -i TARGET_IP -u 'USER' -p 'PASS'
```

## Step 6: Escalate or Pivot

Return to orchestrator with findings:

- **FTP anon write + webroot** for stack ID, then file upload RCE
- **FTP credentials found** against other services
- **SSH password auth enabled** with known/default creds
- **BlueKeep confirmed** → return CVE details for orchestrator routing
- **regreSSHion in range** → return version details for orchestrator routing
- **NTLM info leak** → pass domain/hostname to **ad-discovery**
- **VNC no-auth** → return access details for orchestrator routing
- **WinRM + valid creds** → confirm access, recommend post-exploitation
- **No findings** → report what was checked, mark services as enumerated

## Troubleshooting

### FTP connection refused or timeout
Try passive mode: `ftp -p TARGET_IP`. If still failing, note as filtered.

### SSH connection timeout
May indicate port knocking or IP allowlisting. Note as filtered and move on.

### RDP NSE scripts return no output
Try `--script-args rdp.domain=DOMAIN` if a domain name is known.

### VNC connection refused on 5900
VNC may be on a non-standard port in 5900-5910. Scan the full range.
