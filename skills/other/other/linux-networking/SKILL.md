---
name: linux-networking
cluster: linux
description: "netplan/ip, ufw/nftables firewall, DNS, VPN Wireguard/Tailscale, inter-instance routing System76"
tags: ["networking","linux","firewall","vpn","tailscale"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "linux network firewall ufw ip routing vpn tailscale dns"
---

# linux-networking

## Purpose
This skill handles Linux networking tasks, including IP configuration with Netplan, firewall management via UFW or Nftables, DNS setup, VPN configuration for Wireguard or Tailscale, and inter-instance routing on systems like System76.

## When to Use
Use this skill for server setup on Ubuntu/Debian systems, securing applications with firewalls, establishing secure remote access via VPN, resolving DNS issues in containerized environments, or optimizing routing between networked instances in data centers or edge devices.

## Key Capabilities
- Configure static/dynamic IP addresses using Netplan YAML files (e.g., set interface to DHCP or static IP).
- Manage firewalls with UFW for simple rules (e.g., allow/deny ports) or Nftables for advanced packet filtering via tables and chains.
- Handle DNS resolution with tools like systemd-resolved or /etc/resolv.conf edits.
- Set up VPNs: Wireguard for peer-to-peer tunnels using wg-quick, or Tailscale for automatic mesh networks with key authentication.
- Implement inter-instance routing on System76 hardware, such as setting up OSPF or static routes for multi-device communication.

## Usage Patterns
Always run commands with sudo for root privileges. For scripts, check if services like NetworkManager or systemd-networkd are active. Use environment variables for sensitive data, e.g., export TAILSCALE_API_KEY=$SERVICE_API_KEY before Tailscale operations. In AI responses, structure tasks as sequential commands: first validate config files, then apply changes, and finally verify with diagnostic tools. For automation, wrap commands in bash scripts with error checks, e.g., use `set -e` to exit on failure.

## Common Commands/API
- Netplan configuration: Edit /etc/netplan/01-netcfg.yaml with content like `network: version: 2 renderer: networkd ethernets: eno1: dhcp4: true`, then run `sudo netplan apply`.
- UFW firewall: Enable with `sudo ufw enable`, add rules like `sudo ufw allow 22/tcp`, and check status with `sudo ufw status verbose`.
- Nftables firewall: Load rules from /etc/nftables.conf (e.g., `table ip filter { chain input { type filter hook input priority 0; policy accept; } }`), then apply with `sudo nft -f /etc/nftables.conf`.
- DNS management: Edit /etc/resolv.conf (e.g., add `nameserver 8.8.8.8`), or use `systemd-resolve --set-dns=8.8.8.8 eth0`.
- Wireguard VPN: Generate keys with `wg genkey | tee privatekey | wg pubkey > publickey`, configure /etc/wireguard/wg0.conf with `[Interface] PrivateKey = <key> Address = 10.0.0.1/24`, and start with `sudo wg-quick up wg0`.
- Tailscale VPN: Authenticate with `tailscale up --authkey $TAILSCALE_API_KEY`, then manage peers via Tailscale API (e.g., GET https://api.tailscale.com/api/v2/devices).
- Inter-instance routing: Add static routes with `sudo ip route add 192.168.1.0/24 via 10.0.0.1`, or configure OSPF on System76 using `quagga` with commands like `router ospf` in vtysh.

## Integration Notes
Integrate with orchestration tools like Ansible by using modules such as `ansible.builtin.shell` for running Netplan commands, or `community.general.ufw` for firewall rules. For Tailscale, pass API keys via environment variables (e.g., $TAILSCALE_API_KEY) and use their HTTP API for device management. Wireguard integrates with systemd by enabling services via `sudo systemctl enable wg-quick@wg0`. Ensure compatibility with NetworkManager by disabling it for Netplan (e.g., `sudo systemctl stop NetworkManager`). For DNS, link with systemd-resolved in containers by mounting /etc/resolv.conf. Always validate configs with tools like `nmcli` or `ip a` before applying changes.

## Error Handling
Check for permission errors by prefixing commands with sudo; if `netplan apply` fails with "Invalid YAML", validate the file with `yamllint /etc/netplan/01-netcfg.yaml`. For UFW/Nftables, use `sudo ufw status` or `sudo nft list ruleset` to debug rules; common issues include port conflicts—resolve by checking with `ss -tuln`. VPN errors: If Wireguard fails to start, verify keys with `wg show` and check logs with `journalctl -u wg-quick@wg0`; for Tailscale, handle authentication failures by re-exporting $TAILSCALE_API_KEY and retrying. Routing problems: Use `ip route show` to diagnose; if routes don't propagate, restart networking with `sudo systemctl restart networking`. Always log outputs in scripts using `>> error.log 2>&1`.

## Concrete Usage Examples
1. Set up a basic firewall on Ubuntu: First, enable UFW with `sudo ufw enable`. Then, allow SSH: `sudo ufw allow 22`. Verify: `sudo ufw status`. This secures the server while permitting remote access.
2. Configure a Wireguard VPN tunnel: Create a config file at /etc/wireguard/wg0.conf with ` [Interface] Address = 10.0.0.1/24 PrivateKey = <generated_key> `. Start it: `sudo wg-quick up wg0`. Test connectivity: `ping 10.0.0.2`. This establishes a secure link between instances.

## Graph Relationships
- Related to cluster: linux
- Connected via tags: networking (direct link), linux (cluster parent), firewall (sub-skill), vpn (dependency), tailscale (specific tool)
- Outgoing edges: integrates with linux-security for broader protection, links to linux-storage for network-mounted volumes
- Incoming edges: depends on linux-basics for core OS commands, referenced by devops-tools for automation workflows
