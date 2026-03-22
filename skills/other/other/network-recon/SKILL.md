---
name: network-recon
description: >
  Network reconnaissance, host discovery, port scanning, and OS
  fingerprinting. Produces a port/service map that the orchestrator uses
  to route to service-specific enumeration skills.
keywords:
  - scan this network
  - nmap
  - port scan
  - host discovery
  - recon this target
  - what's running on this host
  - network scan
  - find open ports
  - scan this IP
  - scan this subnet
  - scan through tunnel
  - pivot scan
  - proxychains nmap
  - internal network recon
tools:
  - nmap
opsec: medium
---

# Network Reconnaissance

You are helping a penetration tester perform network reconnaissance and service
enumeration. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[network-recon] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers network reconnaissance — host discovery, port scanning, OS
fingerprinting, and output parsing. It produces a port/service map; the
orchestrator routes to service-specific enumeration skills for deeper checks.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (hosts, ports, services, OS)
  - Recommended next skills based on discovered services
  - Context to pass (target IP, open ports, service versions)

The orchestrator decides what runs next. Your job is to scan thoroughly and
return a clean port/service map.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

You MUST NOT:
- Enumerate individual services (SMB shares, database access, FTP anonymous) —
  the orchestrator routes to **smb-enumeration**, **database-enumeration**,
  **remote-access-enumeration**, or **infrastructure-enumeration**
- Perform web application testing — route to **web-discovery**
- Perform AD enumeration — route to **ad-discovery**
- Perform privilege escalation — route to **linux-discovery** or **windows-discovery**
- Test credentials or brute force — route to **password-spraying**
- Exploit confirmed vulnerabilities — route to the appropriate technique skill

## State Management

Call `get_state_summary()` from the state-interim MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

### Interim Writes

Write actionable findings **immediately** via state-interim so the orchestrator
can react in real time (via event watcher) instead of waiting for your full
return summary. Use these tools as you discover findings:

- `add_pivot()` — new subnets discovered from routing info or nmap traceroute
- `add_blocked()` — scan failures (host unreachable, firewall blocking)
Your return summary must include:
- All discovered hosts (with IP, OS, role)
- Open ports and services per host (formatted as per-host one-liner)
- OS fingerprinting results
- Routing recommendations based on discovered services
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Network access to target(s) — direct or via pivot tunnel
- Target IP, hostname, or CIDR range
- Scope confirmation (which IPs/ranges are authorized)
- nmap installed (core tool — all other tools optional)
- **If scanning through a tunnel:** check engagement state for tunnel details
  (type, local endpoint, requires_proxychains, proxychains config path)

## Privileged Commands

Claude Code cannot execute `sudo` commands directly. Nmap requires root for SYN
scans, UDP scans, OS detection, and most NSE scripts. How nmap runs depends on
whether the nmap MCP server is available.

### MCP nmap Server (Subagent Mode)

When running as a subagent with nmap MCP access, use the `nmap_scan` tool
directly — no sudo handoff needed. The MCP server runs `sudo nmap` in a
subprocess and returns parsed JSON.

```
nmap_scan(target="10.10.10.5", options="-A -p- -T4")
```

- Returns structured JSON: hosts, ports, services, scripts, OS detection.
- Raw XML is saved to `engagement/evidence/` automatically.
- Use `get_scan(scan_id)` to retrieve previous results.
- The **Nmap Is the Gate** principle still applies — do not run other network
  tools until `nmap_scan` completes and you've parsed the results.

### Handoff Protocol (Inline Mode)

When running inline without nmap MCP access, hand off to the user for manual
execution. This applies to:

- **nmap** — SYN scans (`-sS`), UDP scans (`-sU`), OS detection (`-O`), and most NSE scripts that need raw sockets
- **responder** — LLMNR/NBNS/mDNS poisoning (requires raw sockets)
- **mount** — NFS/SMB mounting

**Handoff protocol:**

1. Present the full command including `sudo` to the user
2. Specify the output file path (ensure commands include `-oA`, `-oG`, or `-oL` flags)
3. Ask the user to run it in their terminal
4. Read the output file when the user confirms completion
5. Continue analysis based on the parsed output

**nmap always requires either MCP or the handoff protocol.** Do not run nmap
directly from Bash — not even non-privileged scan types like `-sT` or `-sV`.
Unprivileged nmap produces unreliable results (connect scans miss filtered
ports, no OS detection, no raw-socket NSE scripts).

### Nmap Is the Gate — Hard Stop

**After starting an nmap scan (via MCP or handoff), STOP. Do nothing else until
scan results are available.** No httpx, no curl, no netexec, no nuclei, no
"quick triage" — nothing touches the network until nmap results are parsed.
The nmap scan is the foundation. Every subsequent decision — which services to
enumerate, which skills to route to, which quick wins to check — depends on
knowing the full port and service landscape. Running tools before nmap completes
wastes time on assumptions, produces duplicate traffic, and risks missing the
ports that actually matter.

**Non-privileged commands** that CAN be executed directly by Claude for
**post-scan** service enumeration (only AFTER nmap results are parsed):
- `httpx`, `netexec`, `nuclei`, `whatweb`, `ffuf`
- `ldapsearch`, `smbclient`, `rpcclient`, `snmpwalk`

Batch all pending privileged commands so the user can run them in one pass.
Present them as a numbered list, each with its output file path.

## Step 1: Host Discovery

Identify live hosts in the target range. Skip for single-host targets.

```bash
# ARP ping (fastest — same subnet only)
sudo nmap -sn -PR 10.10.10.0/24 -oG discovery.gnmap

# ICMP echo + TCP SYN(80,443) + TCP ACK(80) + ICMP timestamp (default -sn)
sudo nmap -sn 10.10.10.0/24 -oG discovery.gnmap

# TCP-only host discovery (ICMP blocked)
sudo nmap -sn -PS22,80,135,443,445,3389,8080 10.10.10.0/24 -oG discovery.gnmap

# UDP host discovery
sudo nmap -sn -PU53,161,137 10.10.10.0/24 -oG discovery.gnmap

# Combined — most thorough
sudo nmap -sn -PE -PP -PS21,22,25,80,113,135,443,445,3389,8080 -PU53,111,137,161 10.10.10.0/24 -oG discovery.gnmap
```

**Parse live hosts for next steps:**

```bash
# Extract live hosts from nmap greppable output
grep "Status: Up" discovery.gnmap | awk '{print $2}' > live_hosts.txt
```

Present the list of live hosts. Ask which to scan further or proceed with all.

## Pivot Mode — Scanning Through a Tunnel

When the orchestrator says you're scanning through a tunnel (chisel SOCKS, SSH
dynamic forward, ligolo, etc.), **everything changes**. Nmap through proxychains
is extremely slow — a /24 with top-1000 ports means 256,000 TCP connect attempts
through SOCKS, each timeout ~15 seconds. A full subnet scan can take hours and
often times out.

**Check the engagement state** (`get_state_summary()`) for tunnel details. The
Tunnels section tells you the tunnel type, local endpoint, whether proxychains
is required, and which hosts are already known-live.

### The nmap MCP Server Does NOT Support Proxychains

The `nmap_scan` MCP tool runs nmap directly — it cannot route through SOCKS
proxies. When scanning through a tunnel that requires proxychains, you MUST use
Bash with `dangerouslyDisableSandbox: true` instead of the nmap MCP server.

All nmap commands through proxychains require these flags:
```bash
proxychains4 -f <config_path> nmap -sT -Pn -n [other options] TARGET
```
- `-sT` — TCP connect scan (only scan type that works through SOCKS)
- `-Pn` — skip host discovery (ICMP doesn't work through SOCKS)
- `-n` — no DNS resolution (avoid DNS leaks outside the tunnel)
- No `-sS`, `-sU`, `-O`, or raw-socket features — SOCKS is TCP-only

### Two-Phase Approach (Required for Pivot Scanning)

**Never scan an entire subnet with nmap through proxychains.** Instead, use a
fast Phase 1 to find live hosts, then targeted Phase 2 for port/service detail.

#### Phase 1: Fast Host Discovery

Use lightweight methods that are much faster than nmap through SOCKS. Try these
in order — use whichever works for your access level on the pivot host.

**Option A — Commands on the pivot host via existing shell session.**
If you have a shell on the pivot host (WinRM, SSH, reverse shell), run discovery
commands directly on it. No proxychains overhead — these execute locally on the
internal network.

Windows pivot host:
```powershell
# ARP cache — already-known neighbors (instant)
arp -a

# DNS zone dump — if pivot host is a DC or has DNS access
Get-DnsServerResourceRecord -ZoneName <domain> -RRType A | Select-Object HostName, @{N='IP';E={$_.RecordData.IPv4Address}}

# Ping sweep (fast, covers the subnet)
1..254 | ForEach-Object { $ip="192.168.100.$_"; if(Test-Connection -Count 1 -Quiet -TimeoutSeconds 1 $ip){$ip} }

# PowerShell TCP port check on specific hosts (confirm specific services)
Test-NetConnection -ComputerName 192.168.100.2 -Port 445 -InformationLevel Quiet
```

Linux pivot host:
```bash
# ARP cache
arp -a

# Ping sweep
for i in $(seq 1 254); do ping -c1 -W1 192.168.100.$i &>/dev/null && echo "192.168.100.$i alive" & done; wait

# Bash TCP check (no tools needed)
for port in 22 80 135 445 3389 5985; do
  (echo >/dev/tcp/192.168.100.2/$port) 2>/dev/null && echo "192.168.100.2:$port open"
done
```

**Option B — Single-port sweep through proxychains.**
If you can't run commands on the pivot host, sweep one common port across the
subnet. Much faster than scanning many ports per host.

```bash
# SMB sweep — fast, catches Windows hosts
proxychains4 -f <config> nxc smb 192.168.100.0/24 --timeout 5 2>&1 | grep -v "timeout"

# Or nmap with a SINGLE port — minimize SOCKS overhead
proxychains4 -f <config> nmap -sT -Pn -n -p 445 192.168.100.0/24 --open -oG pivot_discovery.gnmap
```

**Option C — Combined approach (best results).**
Run ARP + ping sweep on the pivot host first, then validate with a single-port
proxychains sweep to catch hosts that block ICMP.

After Phase 1, collect the list of confirmed live hosts. **Only these hosts
proceed to Phase 2.**

#### Phase 2: Targeted Port Scanning

Scan ONLY the live hosts found in Phase 1. Use focused port lists, not `-p-`.

```bash
# Common Windows ports — covers most AD/enterprise services
proxychains4 -f <config> nmap -sT -Pn -n -p 21,22,25,53,80,88,110,135,139,143,389,443,445,464,587,636,993,995,1433,2049,3268,3306,3389,5432,5985,5986,8080,8443,9389 <live_host> -oA pivot_scan_HOSTNAME

# If you already know the OS (e.g., from Phase 1 SMB banner), narrow further:
# Windows server — core ports
proxychains4 -f <config> nmap -sT -Pn -n -p 80,88,135,139,389,443,445,636,1433,3268,3389,5985,5986,8080 <live_host> -oA pivot_scan_HOSTNAME

# Linux server — core ports
proxychains4 -f <config> nmap -sT -Pn -n -p 21,22,25,53,80,110,139,143,443,445,993,2049,3306,5432,8080 <live_host> -oA pivot_scan_HOSTNAME
```

**Service version detection** — only on confirmed open ports:
```bash
# After finding open ports, run -sV on JUST those ports
proxychains4 -f <config> nmap -sT -Pn -n -sV -p <open_ports_csv> <live_host> -oA pivot_svc_HOSTNAME
```

**Timing matters.** Through SOCKS, `-T4` can cause excessive timeouts. Use `-T3`
or even `-T2` for reliability. Add `--max-retries 2 --host-timeout 300s` to
prevent individual hosts from stalling the entire scan.

### Alternative: Static nmap on Pivot Host

For the fastest results, upload a static nmap binary to the pivot host and scan
locally. This avoids all SOCKS overhead.

```bash
# Download static nmap on attackbox (NOT on target)
# https://github.com/andrew-d/static-binaries or compile yourself

# Transfer to pivot host (via existing shell session)
# Use base64, certutil, or python http server + curl/wget

# Run locally on pivot host — full speed, no proxychains
./nmap -sT -Pn -p- 192.168.100.0/24 -oG /tmp/internal_scan.gnmap

# Pull results back to attackbox for analysis
```

This is more invasive (leaves artifacts on the pivot host) but orders of
magnitude faster. Use when speed matters more than stealth.

### Pivot Mode Summary

| Method | Speed | Invasiveness | When to use |
|--------|-------|--------------|-------------|
| Commands on pivot host | Fast | Low | Have shell access, quick discovery |
| Single-port proxychains sweep | Medium | Low | No shell, need to find hosts |
| Targeted nmap through proxychains | Slow | Low | Port/service detail on known hosts |
| Static nmap on pivot host | Fastest | High | Large subnet, speed critical |
| Full subnet nmap through proxychains | **Never** | N/A | **Don't do this** |

After pivot scanning, return findings to the orchestrator. The orchestrator
routes to service-specific enumeration skills for discovered hosts.

## Step 2: Port Scanning

Check the orchestrator's prompt for a `Scan type:` directive. This tells you
what the operator chose:

- **`quick`** — top 1000 ports + service detection:
  ```bash
  sudo nmap -sV -sC --top-ports 1000 -T4 -oA scan_HOSTNAME -vvv TARGET_IP
  ```

- **`full`** — all 65535 ports, full enumeration:
  ```bash
  sudo nmap -A -p- -T4 -oA scan_HOSTNAME -vvv TARGET_IP
  ```

- **`Custom scan request: ...`** — the operator described a custom scan.
  Translate their description into appropriate nmap options. Preserve `-oA`
  for output and add `-vvv` for verbose results.

If no scan type is specified, **return and ask the orchestrator** — never assume.

The full scan is the go-to for most engagements. `-A` enables OS detection,
version detection, script scanning, and traceroute. `-p-` scans all 65535
ports. `-T4` is aggressive timing suitable for most networks. `-oA` saves in
all formats (`.nmap`, `.gnmap`, `.xml`).

### Host Appears Down — `-Pn` Retry

If the scan returns **0 hosts up** (nmap's host discovery probes got no
response), retry with `-Pn` added to the **same scan options**. Many targets
(especially HTB/CTF, cloud instances, and firewalled hosts) block ICMP and
TCP discovery probes but have open ports.

**Rules:**
- Add `-Pn` to the ORIGINAL scan options. Do NOT change the scan type, port
  range, or any other flags. If the operator chose quick (`--top-ports 1000`),
  retry as quick + `-Pn`. If full (`-p-`), retry as full + `-Pn`.
- This retry happens **once**. If the `-Pn` scan also returns no open ports,
  **STOP and return to the orchestrator** with:
  - What was tried (both scans with exact options)
  - That the host appears unreachable or has no open ports in the scanned range
  - A recommendation to check network connectivity (VPN, routing, firewall)
- Do NOT escalate to a different scan type (e.g., quick → full). Do NOT add
  `-p-` to a quick scan. Do NOT run additional scans beyond the one `-Pn`
  retry. The orchestrator decides next steps — not you.

**Parse scan results:**

```bash
# Extract open ports from greppable output
grep "open" scan_HOSTNAME.gnmap | awk -F'[/ ]' '{for(i=1;i<=NF;i++) if($i=="open") print $(i-1)}' | sort -un

# Parse nmap XML (useful for piping to other tools)
xmlstarlet sel -t -m "//port[state/@state='open']" -v "@portid" -o ":" -v "service/@name" -n scan_HOSTNAME.xml
```

## Step 3: OS Fingerprinting

If `-A` didn't provide reliable OS detection:

```bash
# Aggressive OS detection
sudo nmap -O --osscan-guess -oA os_HOSTNAME TARGET_IP

# TCP/IP stack fingerprinting
sudo nmap -O -sV --version-intensity 5 -oA os_HOSTNAME TARGET_IP
```

**Quick heuristics from open ports:**

| Signature | Likely OS |
|-----------|-----------|
| 135, 139, 445, 3389 | Windows |
| 22, 111, 2049 | Linux/Unix |
| 22, 80/443 only | Linux (hardened/web server) |
| 88, 389, 445, 636, 3268 | Domain Controller |
| 5985, 5986 | Windows (WinRM enabled) |
| 548 (AFP) | macOS |

**TTL heuristics (from ping or nmap):**

| TTL Range | Likely OS |
|-----------|-----------|
| 64 | Linux/macOS |
| 128 | Windows |
| 254-255 | Network device (Cisco, etc.) |

## Step 4: Output Parsing and State Update

After scanning, parse results into structured form for state management and
next-step routing.

**Parse nmap XML for structured data:**

```bash
# List all hosts with open ports (from XML)
xmlstarlet sel -t -m "//host[ports/port/state/@state='open']" \
  -v "address[@addrtype='ipv4']/@addr" -o " " \
  -m "ports/port[state/@state='open']" -v "@portid" -o "/" -v "service/@name" -o " " \
  -b -n scan_HOSTNAME.xml

# Quick summary
grep "Ports:" scan_HOSTNAME.gnmap | sed 's/Ports: //' | tr ',' '\n'
```

**Report scan results in return summary (format per-host one-liner):**

```

## Targets
- 10.10.10.1 | Windows Server 2019 | DC | 53,88,135,139,389,445,636,3268,3389,5985
- 10.10.10.5 | Ubuntu 22.04 | Web | 22,80,443
- 10.10.10.10 | Windows 10 | Workstation | 135,139,445,3389,5985
```

## Troubleshooting

### Nmap scan runs slowly or hangs
- Use `-T4` for speed. Drop to `-T3` if getting rate-limited or missing ports.
- On large subnets, start with `--top-ports 1000` before doing `-p-`.

### Host appears down (0 hosts up)
- Retry with `-Pn` added to the same scan options (see "Host Appears Down"
  in Step 2). Do NOT change the scan type or port range.
- If `-Pn` also finds nothing, return to orchestrator — do not improvise.

### UDP scan takes too long
- UDP scans are inherently slow. Limit to key ports: `-sU -p 53,67,69,123,161,162,500,623,1434,5353`.
- Combine with TCP: `-sS -sU --top-ports 100`.

### Service version detection returns "tcpwrapped"
- Target is accepting TCP connections but dropping them before service negotiation.
- Try connecting manually: `nc -nv TARGET_IP PORT` to see if there's a banner.
- May indicate a firewall or IPS is interfering.

### Nmap XML parsing fails
- Ensure scan completed (check for `</nmaprun>` closing tag).
- If scan was interrupted, partial XML is unusable — re-run with `-oA` to get all formats.

### Nmap through proxychains times out or takes forever
- **Never scan an entire /24 with nmap through proxychains.** Use the two-phase
  approach in the Pivot Mode section.
- Use `-T3` or `-T2` instead of `-T4` — aggressive timing causes SOCKS timeouts.
- Add `--max-retries 2 --host-timeout 300s` to bound individual hosts.
- Scan fewer ports: use a targeted list instead of `--top-ports 1000` or `-p-`.
- If all else fails, upload a static nmap binary to the pivot host and scan locally.
