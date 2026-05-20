---
name: pfsense
description: |
  Manage the pfSense firewall at 10.0.20.1 via SSH. Use when:
  (1) User asks about firewall rules, NAT, port forwarding,
  (2) User asks about network diagnostics (ARP, routing, DNS, ping),
  (3) User asks about DHCP leases or static mappings,
  (4) User asks about VPN status (WireGuard, Tailscale),
  (5) User asks about pfSense services (Snort, FRR/BGP/OSPF, etc.),
  (6) User asks about firewall states, connections, or traffic,
  (7) User mentions "pfsense", "firewall", "gateway", or network troubleshooting,
  (8) User wants to check system health (CPU, memory, disk, temp) of pfSense.
  pfSense CE 2.7.2 on FreeBSD 14.0, VMID 101 on Proxmox.
author: Claude Code
version: 1.0.0
date: 2026-02-14
---

# pfSense Firewall Management

## Overview
- **Host**: `10.0.20.1` (Kubernetes VLAN gateway)
- **SSH**: `ssh admin@10.0.20.1`
- **Version**: pfSense CE 2.7.2, FreeBSD 14.0
- **Proxmox VMID**: 101 (8 CPU, 16GB RAM, 32G disk)
- **Web UI**: `https://pfsense.viktorbarzin.me` (via reverse proxy) or `https://10.0.20.1`
- **Installed packages**: FRR (BGP/OSPF), Tailscale, Snort, WireGuard, REST API, FreeRADIUS

## Interfaces

| Name | Description | Physical | IP | Network |
|------|-------------|----------|-----|---------|
| wan | WAN | vtnet0 | 192.168.1.2/24 | Physical network |
| lan | Management VMs | vtnet1 | 10.0.10.1/24 | VLAN 10 |
| opt1 | Kubernetes | vtnet2 | 10.0.20.1/24 | VLAN 20 |
| opt2 | WireGuard | tun_wg0 | 10.3.2.1/24 | VPN tunnel |
| tailscale0 | Tailscale | tailscale0 | 100.64.0.x | Headscale mesh |

## CLI Script

**Script**: `.claude/pfsense.py`

### Execution Pattern
```bash
cd ~/code/infra && python3 .claude/pfsense.py <command> [options]
```

### Available Commands

#### System Information
```bash
python3 .claude/pfsense.py status          # Full system overview
python3 .claude/pfsense.py uptime          # Uptime
python3 .claude/pfsense.py cpu             # CPU info and load
python3 .claude/pfsense.py memory          # Memory breakdown
python3 .claude/pfsense.py disk            # Disk usage
python3 .claude/pfsense.py temp            # CPU temperature
python3 .claude/pfsense.py pkg-list        # Installed packages
```

#### Network & Interfaces
```bash
python3 .claude/pfsense.py interfaces      # Interface list with IPs
python3 .claude/pfsense.py gateways        # Gateway status
python3 .claude/pfsense.py arp             # ARP table
python3 .claude/pfsense.py routes          # Routing table
python3 .claude/pfsense.py dns-resolve <host>  # DNS lookup via pfSense
python3 .claude/pfsense.py diag <host>     # Ping test
```

#### Firewall
```bash
python3 .claude/pfsense.py rules           # All firewall rules
python3 .claude/pfsense.py rules opt1      # Rules for Kubernetes interface
python3 .claude/pfsense.py nat             # NAT / port forwarding rules
python3 .claude/pfsense.py aliases         # List all aliases
python3 .claude/pfsense.py alias <name>    # Show alias members
python3 .claude/pfsense.py states          # State table summary
python3 .claude/pfsense.py states-top 20   # Top 20 IPs by connection count
```

#### DHCP
```bash
python3 .claude/pfsense.py dhcp-leases         # All DHCP leases
python3 .claude/pfsense.py dhcp-leases opt1    # Kubernetes network leases only
```

#### Services
```bash
python3 .claude/pfsense.py services                    # List all services + status
python3 .claude/pfsense.py service restart snort        # Restart a service
python3 .claude/pfsense.py service stop wireguard       # Stop a service
python3 .claude/pfsense.py service start wireguard      # Start a service
```

#### VPN & Routing
```bash
python3 .claude/pfsense.py wireguard       # WireGuard tunnel status
python3 .claude/pfsense.py tailscale       # Tailscale/Headscale status
python3 .claude/pfsense.py bgp             # BGP summary (FRR)
python3 .claude/pfsense.py ospf            # OSPF neighbors (FRR)
```

#### Security
```bash
python3 .claude/pfsense.py snort           # Snort IDS status + recent alerts
python3 .claude/pfsense.py logs            # Last 50 firewall log entries
python3 .claude/pfsense.py logs 200        # Last 200 entries
python3 .claude/pfsense.py logs-filter "blocked"  # Search logs
```

#### Advanced
```bash
python3 .claude/pfsense.py pfctl "-sr"     # Raw pfctl command
python3 .claude/pfsense.py php "echo phpversion();"  # Run PHP on pfSense
python3 .claude/pfsense.py raw "ls /tmp"   # Run arbitrary shell command
python3 .claude/pfsense.py backup          # Dump config.xml to stdout
```

## Direct SSH Access

For tasks not covered by the script, SSH directly:
```bash
ssh admin@10.0.20.1 "<command>"
```

### Useful Direct Commands
```bash
# pfSense PHP shell (interactive config access)
ssh admin@10.0.20.1 "php -r 'require_once(\"config.inc\"); \$cfg = parse_config(true); echo json_encode(\$cfg[\"nat\"], JSON_PRETTY_PRINT);'"

# pfSsh.php playback commands
ssh admin@10.0.20.1 "pfSsh.php playback gatewaystatus"
ssh admin@10.0.20.1 "pfSsh.php playback svc restart snort"
ssh admin@10.0.20.1 "pfSsh.php playback listpkg"

# Config sections via PHP
ssh admin@10.0.20.1 "php -r 'require_once(\"config.inc\"); \$cfg = parse_config(true); print_r(\$cfg[\"filter\"][\"rule\"][0]);'"

# FRR/vtysh for routing
ssh admin@10.0.20.1 "/usr/local/bin/vtysh -c 'show ip route'"
ssh admin@10.0.20.1 "/usr/local/bin/vtysh -c 'show bgp ipv4 unicast'"
```

## REST API (pfSense-pkg-RESTAPI v2.2)

The REST API package is installed but **no API keys are configured**. To use it:
1. Create an API key in pfSense Web UI: System > REST API > Settings > Keys
2. Use Bearer token auth: `curl -sk https://10.0.20.1/api/v2/status/system -H 'Authorization: Bearer <key>'`

Until API keys are set up, use SSH for all operations.

## Key Services

| Service | Status | Notes |
|---------|--------|-------|
| FRR (BGP/OSPF) | Running | Routing daemon |
| Snort | Running | IDS/IPS |
| WireGuard | Running | VPN tunnel (10.3.2.0/24) |
| Tailscale | Running | Mesh VPN via Headscale |
| FreeRADIUS | Running | RADIUS auth |
| DHCP (Kea) | Running | kea-dhcp4 |
| SSH | Running | Admin access |
| NTP | Running | Time sync |

## Firewall Stats
- **167 firewall rules** (pfctl -sr)
- **154 NAT rules** (pfctl -sn)
- **~784 active states** (varies)
- **10 aliases** (LAN, OPT1, OPT2, WAN networks + custom)

## NFS Backup
Config backups stored at NFS: `/mnt/main/pfsense-backup`

## Troubleshooting

| Issue | Command |
|-------|---------|
| Can't reach internet from K8s | `python3 .claude/pfsense.py gateways` + `python3 .claude/pfsense.py diag 8.8.8.8` |
| K8s pod can't reach external | `python3 .claude/pfsense.py rules opt1` + check NAT |
| DHCP not working | `python3 .claude/pfsense.py dhcp-leases opt1` + `python3 .claude/pfsense.py service restart kea-dhcp4` |
| High connection count | `python3 .claude/pfsense.py states-top 20` |
| Snort blocking traffic | `python3 .claude/pfsense.py snort` + check alerts |
| DNS resolution failing | `python3 .claude/pfsense.py dns-resolve <host>` |
| BGP/OSPF routes missing | `python3 .claude/pfsense.py bgp` or `python3 .claude/pfsense.py ospf` |
| WireGuard tunnel down | `python3 .claude/pfsense.py wireguard` |

## Notes
1. **FreeBSD-based**: Commands differ from Linux (no `ip`, use `ifconfig`, `netstat`, `arp`)
2. **pfctl is the firewall**: Rules loaded from config.xml via PHP, managed by pfctl
3. **Config file**: `/cf/conf/config.xml` — all pfSense config in one XML file
4. **PHP shell**: pfSense uses PHP for all config management; `config.inc` loads the config
5. **Do NOT edit config.xml directly** — use the Web UI or PHP functions that properly reload services
6. **Logs**: Binary circular logs, read with `clog -f /var/log/<logfile>`
