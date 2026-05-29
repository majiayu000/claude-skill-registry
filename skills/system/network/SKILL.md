---
name: network
description: |
  Network configuration for Bazzite. iwd WiFi backend, Wake-on-LAN, and Tailscale VPN.
  Use when users need to configure network services. For SSH, see bazzite-ai:config.
---

# Network - Bazzite Network Configuration

## Overview

Bazzite network configuration including alternative WiFi backends, Wake-on-LAN for remote power control, and Tailscale for VPN/mesh networking.

## Quick Reference

| Command | Description |
|---------|-------------|
| `ujust toggle-iwd` | Enable/disable iwd as WiFi backend |
| `ujust toggle-wol` | Toggle Wake-on-LAN |
| `ujust enable-tailscale` | Enable Tailscale service |

## WiFi Backend

### Toggle iwd

```bash
# Switch between iwd and wpa_supplicant
ujust toggle-iwd
```

**iwd (Intel Wireless Daemon):**
- Faster connection times
- Lower resource usage
- Better power efficiency
- Modern replacement for wpa_supplicant

**wpa_supplicant:**
- Default on most systems
- Broader compatibility
- Required for some enterprise networks

**After switching:** Reconnect to WiFi networks.

## Wake-on-LAN

### Toggle WOL

```bash
# Interactive WOL toggle
ujust toggle-wol

# Non-interactive
ujust toggle-wol enable
ujust toggle-wol disable
ujust toggle-wol force-enable
```

**Options:**
- `enable` - Enable WOL
- `disable` - Disable WOL
- `force-enable` - Force enable (overrides power settings)

### Using WOL

**On target machine:**

```bash
# Get MAC address
ip link show | grep ether
```

**From remote machine:**

```bash
# Wake the target
wakeonlan <MAC_ADDRESS>
# or
wol <MAC_ADDRESS>
```

**Requirements:**
- Wired Ethernet connection
- BIOS WOL support enabled
- Both machines on same network (or port forwarding)

## Tailscale VPN

### Enable Tailscale

```bash
# Enable Tailscale service
ujust enable-tailscale
```

**After enabling:**

```bash
# Authenticate
tailscale up

# Check status
tailscale status

# Get IP
tailscale ip
```

**Features:**
- Zero-config VPN
- Mesh networking
- Access machines anywhere
- MagicDNS for hostnames

### Tailscale Usage

```bash
# Connect to Tailscale network
tailscale up

# Exit node (route all traffic)
tailscale up --exit-node=<node>

# Disconnect
tailscale down

# Status
tailscale status
```

## Common Workflows

### Remote Access Setup

```bash
# Enable Tailscale
ujust enable-tailscale
tailscale up

# Enable Wake-on-LAN for remote power
ujust toggle-wol enable

# Enable SSH (via bazzite-ai)
ujust config sshd enable
```

### Better WiFi Performance

```bash
# Switch to iwd
ujust toggle-iwd

# Reconnect to WiFi
nmcli device wifi list
nmcli device wifi connect "<SSID>" password "<password>"
```

### Home Server Access

```bash
# On server: Enable Tailscale
ujust enable-tailscale
tailscale up

# On client: Connect
tailscale up

# Access server via Tailscale IP or MagicDNS name
ssh user@<server-tailscale-ip>
ssh user@<server-name>  # with MagicDNS
```

## Network Troubleshooting

### Check Network Status

```bash
# NetworkManager status
nmcli general status

# List connections
nmcli connection show

# Current IP
ip addr show

# WiFi networks
nmcli device wifi list
```

### WiFi Issues

**Reconnect:**

```bash
nmcli device wifi connect "<SSID>" password "<password>"
```

**Forget and reconnect:**

```bash
nmcli connection delete "<SSID>"
nmcli device wifi connect "<SSID>" password "<password>"
```

### Tailscale Issues

**Check service:**

```bash
systemctl status tailscaled
```

**Re-authenticate:**

```bash
tailscale logout
tailscale up
```

**Check connectivity:**

```bash
tailscale netcheck
tailscale ping <node>
```

### WOL Not Working

**Check BIOS:**
- Enable "Wake on LAN" in BIOS/UEFI

**Check interface:**

```bash
# Verify WOL enabled
ethtool <interface> | grep Wake-on
# Should show: Wake-on: g
```

**Enable manually:**

```bash
sudo ethtool -s <interface> wol g
```

## Cross-References

- **bazzite-ai:configure** - SSH server configuration
- **bazzite:security** - VPN security considerations
- **bazzite:system** - Network diagnostics

## When to Use This Skill

Use when the user asks about:
- "iwd", "wpa_supplicant", "WiFi backend", "faster WiFi"
- "Wake on LAN", "WOL", "remote power on", "wake computer"
- "Tailscale", "VPN", "mesh network", "remote access"
- "WiFi not connecting", "network issues"

**For SSH configuration, use:** `/bazzite-ai:configure`
