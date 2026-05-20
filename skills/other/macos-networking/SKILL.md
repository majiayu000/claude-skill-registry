---
name: macos-networking
cluster: macos
description: "WiFi/Ethernet, DNS, proxy, VPN Tailscale, airport CLI, pfctl firewall"
tags: ["networking","macos","vpn","firewall","dns"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "macos network wifi dns vpn firewall tailscale pfctl"
---

# macos-networking

## Purpose
This skill provides tools for managing macOS networking components, including WiFi, Ethernet, DNS, proxies, Tailscale VPN, and the pfctl firewall, to automate or assist in network configuration tasks.

## When to Use
Use this skill when handling macOS-specific network operations, such as troubleshooting connectivity, configuring secure VPNs, managing DNS for applications, or enforcing firewall rules in scripts or user interactions.

## Key Capabilities
- WiFi and Ethernet management via `networksetup` and `airport` CLI for connecting, scanning, or switching networks.
- DNS configuration using `networksetup` to set servers like Google DNS (e.g., 8.8.8.8).
- Proxy setup with `networksetup` for HTTP/SOCKS proxies, including authentication.
- Tailscale VPN integration for peer-to-peer networking, requiring Tailscale CLI and an auth key.
- Firewall control via `pfctl` for loading rulesets, enabling/disabling, and monitoring traffic.
- Airport CLI (part of macOS) for wireless diagnostics, like scanning networks.
- Specific tools: `networksetup` for most settings, `tailscale` for VPN, and `pfctl` for packet filtering.

## Usage Patterns
Always run commands with elevated privileges using `sudo` where needed. For scripts, check if tools like `tailscale` are installed first. Use environment variables for sensitive data, e.g., export `TAILSCALE_AUTH_KEY=$SERVICE_API_KEY` before running Tailscale commands. Integrate with AI responses by generating bash snippets that users can copy-paste.

Example 1: Switch to a specific WiFi network.
- Use this pattern: First, scan networks with `airport en0 scan`, then connect via `networksetup -setairportnetwork en0 SSID password`.

Example 2: Set up Tailscale VPN.
- Authenticate and connect: Export your auth key as `export TAILSCALE_AUTH_KEY=$SERVICE_API_KEY`, then run `tailscale up --authkey=$TAILSCALE_AUTH_KEY`.

## Common Commands/API
Use these exact commands in scripts or responses. All require macOS environment.

- WiFi: Scan networks with `/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport en0 scan`. Connect: `sudo networksetup -setairportnetwork en0 "NetworkName" "Password"`.
- Ethernet: Enable/disable: `sudo networksetup -setnetworkserviceenabled Ethernet on/off`.
- DNS: Set servers for Wi-Fi: `sudo networksetup -setdnsservers Wi-Fi 8.8.8.8 8.8.4.4`. Flush cache: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.
- Proxy: Set HTTP proxy: `sudo networksetup -setwebproxy Wi-Fi proxy.example.com 8080`. Enable with auth: `sudo networksetup -setwebproxyusername Wi-Fi username -setwebproxypassword Wi-Fi password`.
- Tailscale VPN: Install via `brew install tailscale` if needed. Authenticate: `tailscale up --authkey=$TAILSCALE_AUTH_KEY`. Status: `tailscale status --json`.
- pfctl Firewall: Load rules: `sudo pfctl -f /etc/pf.conf`. Enable: `sudo pfctl -e`. Block traffic: Add rule in /etc/pf.conf like `block in on en0 proto tcp from any to any port 80`, then reload.

Code snippet for WiFi connection:
```bash
#!/bin/bash
network=$(airport en0 scan | grep -o 'SSID: .\+' | cut -d' ' -f2-)
echo "Available networks: $network"
sudo networksetup -setairportnetwork en0 "$1" "$2"
```

Code snippet for Tailscale setup:
```bash
#!/bin/bash
export TAILSCALE_AUTH_KEY=$SERVICE_API_KEY
tailscale up --authkey=$TAILSCALE_AUTH_KEY
tailscale status
```

## Integration Notes
Integrate by wrapping commands in AI-generated scripts. For Tailscale, ensure the auth key is passed via `$TAILSCALE_AUTH_KEY` to avoid hardcoding. Check dependencies: Use `command -v tailscale >/dev/null 2>&1 || brew install tailscale`. For pfctl, edit /etc/pf.conf directly or via scripts, then reload. Avoid conflicts with system services; use `launchctl` to manage related daemons, e.g., `sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.pfctl.plist`. Test in a non-production environment first.

## Error Handling
Handle permissions with `sudo` for all root-required commands; catch failures by checking exit codes, e.g., if `$? -ne 0`, log "Command failed, check sudo access." For network errors, use `ping` to verify connectivity before proceeding. Tailscale auth failures: Check if `$TAILSCALE_AUTH_KEY` is set and valid; retry with `tailscale logout && tailscale up`. pfctl issues: If "no ALTQ support", ensure kernel extensions are loaded via `kextstat | grep pf`. Common: Interface not found errors (e.g., en0 missing)—use `ifconfig -l` to list available interfaces and adjust commands.

## Graph Relationships
- Related to cluster: "macos" (e.g., shares dependencies with macos-file-system, macos-security skills).
- Related by tags: "networking" (connects to general-networking skills), "vpn" (links to remote-access skills), "firewall" (associates with security-monitoring skills), "dns" (integrates with domain-resolution skills).
