---
name: wireguard
description: WireGuard VPN configuration and management. Set up VPN servers, configure peers, manage keys, and troubleshoot connections. Use for VPN setup, secure tunneling, or network privacy. Triggers on wireguard, vpn, tunnel, secure connection, wg, peer configuration, private network.
---

# WireGuard VPN Configuration

Complete guide for WireGuard - modern, fast, and secure VPN.

## Quick Reference

### Key Commands

| Command | Purpose |
|---------|---------|
| `wg genkey` | Generate private key |
| `wg pubkey` | Derive public key |
| `wg show` | Show current config |
| `wg-quick up wg0` | Start interface |
| `wg-quick down wg0` | Stop interface |

### Config Locations

```
Linux: /etc/wireguard/wg0.conf
macOS: /usr/local/etc/wireguard/wg0.conf
Windows: C:\Program Files\WireGuard\Data\Configurations\
```

## Installation

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install wireguard

# Fedora
sudo dnf install wireguard-tools

# Arch
sudo pacman -S wireguard-tools
```

### macOS

```bash
brew install wireguard-tools
```

### Docker

```yaml
services:
  wireguard:
    image: linuxserver/wireguard
    container_name: wireguard
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - SERVERURL=vpn.example.com
      - SERVERPORT=51820
      - PEERS=5
    volumes:
      - ./config:/config
      - /lib/modules:/lib/modules
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
```

## Key Generation

### Generate Key Pair

```bash
# Generate private key
wg genkey | tee privatekey | wg pubkey > publickey

# Or step by step
wg genkey > privatekey
cat privatekey | wg pubkey > publickey

# Generate preshared key (optional, for extra security)
wg genpsk > presharedkey
```

### Secure Key Permissions

```bash
chmod 600 privatekey
chmod 644 publickey
```

## Server Configuration

### Basic Server Config

```ini
# /etc/wireguard/wg0.conf

[Interface]
# Server private key
PrivateKey = SERVER_PRIVATE_KEY
# Server VPN IP address
Address = 10.0.0.1/24
# Listening port
ListenPort = 51820
# DNS for clients (optional)
DNS = 1.1.1.1, 8.8.8.8

# Enable IP forwarding
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Client 1
PublicKey = CLIENT1_PUBLIC_KEY
# Client allowed IPs
AllowedIPs = 10.0.0.2/32
# Optional preshared key
PresharedKey = PRESHARED_KEY

[Peer]
# Client 2
PublicKey = CLIENT2_PUBLIC_KEY
AllowedIPs = 10.0.0.3/32
```

### Enable IP Forwarding

```bash
# Enable temporarily
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1

# Enable permanently
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv6.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Client Configuration

### Basic Client Config

```ini
# /etc/wireguard/wg0.conf

[Interface]
# Client private key
PrivateKey = CLIENT_PRIVATE_KEY
# Client VPN IP address
Address = 10.0.0.2/24
# DNS servers
DNS = 1.1.1.1, 8.8.8.8

[Peer]
# Server public key
PublicKey = SERVER_PUBLIC_KEY
# Optional preshared key
PresharedKey = PRESHARED_KEY
# Server endpoint
Endpoint = vpn.example.com:51820
# Route all traffic through VPN
AllowedIPs = 0.0.0.0/0, ::/0
# Keep connection alive
PersistentKeepalive = 25
```

### Split Tunnel (Specific Routes)

```ini
[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = vpn.example.com:51820
# Only route specific subnets through VPN
AllowedIPs = 10.0.0.0/24, 192.168.1.0/24
PersistentKeepalive = 25
```

## Interface Management

### Start and Stop

```bash
# Start interface
sudo wg-quick up wg0

# Stop interface
sudo wg-quick down wg0

# Restart
sudo wg-quick down wg0 && sudo wg-quick up wg0
```

### Enable at Boot

```bash
# Enable service
sudo systemctl enable wg-quick@wg0

# Start service
sudo systemctl start wg-quick@wg0

# Check status
sudo systemctl status wg-quick@wg0
```

### Show Status

```bash
# Show all interfaces
sudo wg show

# Show specific interface
sudo wg show wg0

# Show with real-time stats
watch -n 1 sudo wg show
```

## Adding Peers

### Add Peer Dynamically

```bash
# Add peer without restarting
sudo wg set wg0 peer CLIENT_PUBLIC_KEY allowed-ips 10.0.0.4/32

# With preshared key
sudo wg set wg0 peer CLIENT_PUBLIC_KEY \
  preshared-key /path/to/presharedkey \
  allowed-ips 10.0.0.4/32
```

### Remove Peer

```bash
sudo wg set wg0 peer CLIENT_PUBLIC_KEY remove
```

### Save Running Config

```bash
# Save current config to file
sudo wg-quick save wg0
```

## Site-to-Site VPN

### Site A Configuration

```ini
# /etc/wireguard/wg0.conf on Site A

[Interface]
PrivateKey = SITE_A_PRIVATE_KEY
Address = 10.0.0.1/24
ListenPort = 51820

PostUp = iptables -A FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -i %i -j ACCEPT

[Peer]
# Site B
PublicKey = SITE_B_PUBLIC_KEY
Endpoint = site-b.example.com:51820
# Site B's VPN IP and LAN subnet
AllowedIPs = 10.0.0.2/32, 192.168.2.0/24
PersistentKeepalive = 25
```

### Site B Configuration

```ini
# /etc/wireguard/wg0.conf on Site B

[Interface]
PrivateKey = SITE_B_PRIVATE_KEY
Address = 10.0.0.2/24
ListenPort = 51820

PostUp = iptables -A FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -i %i -j ACCEPT

[Peer]
# Site A
PublicKey = SITE_A_PUBLIC_KEY
Endpoint = site-a.example.com:51820
# Site A's VPN IP and LAN subnet
AllowedIPs = 10.0.0.1/32, 192.168.1.0/24
PersistentKeepalive = 25
```

## Firewall Configuration

### UFW

```bash
# Allow WireGuard port
sudo ufw allow 51820/udp

# Allow forwarding
sudo ufw route allow in on wg0 out on eth0
```

### iptables

```bash
# Allow WireGuard traffic
iptables -A INPUT -p udp --dport 51820 -j ACCEPT

# Allow forwarding
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A FORWARD -o wg0 -j ACCEPT

# NAT for internet access
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### firewalld

```bash
# Add WireGuard port
firewall-cmd --permanent --add-port=51820/udp

# Enable masquerade
firewall-cmd --permanent --add-masquerade

# Reload
firewall-cmd --reload
```

## QR Code Generation

### Generate QR for Mobile

```bash
# Install qrencode
sudo apt install qrencode

# Generate QR code
qrencode -t ansiutf8 < client.conf

# Save as image
qrencode -o client-qr.png < client.conf
```

## Troubleshooting

### Debug Mode

```bash
# Enable debug logging
echo 'module wireguard +p' | sudo tee /sys/kernel/debug/dynamic_debug/control

# View logs
sudo dmesg | grep wireguard
sudo journalctl -u wg-quick@wg0
```

### Common Issues

**No connection:**
```bash
# Check interface is up
ip link show wg0

# Check endpoint reachability
ping vpn.example.com

# Verify port is open
nc -zvu vpn.example.com 51820
```

**Handshake not completing:**
```bash
# Check keys match
# Client's public key should match server's Peer PublicKey
# Server's public key should match client's Peer PublicKey

# Check firewall
sudo iptables -L -n | grep 51820
```

**No internet through VPN:**
```bash
# Check IP forwarding
sysctl net.ipv4.ip_forward

# Check NAT rules
sudo iptables -t nat -L -n

# Check DNS resolution
nslookup google.com
```

### Verify Configuration

```bash
# Test config syntax
sudo wg-quick strip wg0

# Check current config
sudo wg showconf wg0
```

## Automation Scripts

### Add New Peer Script

```bash
#!/bin/bash
# add-peer.sh

CLIENT_NAME=$1
SERVER_PUBLIC_KEY="YOUR_SERVER_PUBLIC_KEY"
SERVER_ENDPOINT="vpn.example.com:51820"

# Generate keys
CLIENT_PRIVATE_KEY=$(wg genkey)
CLIENT_PUBLIC_KEY=$(echo "$CLIENT_PRIVATE_KEY" | wg pubkey)

# Find next available IP
NEXT_IP=10.0.0.$(( $(sudo wg show wg0 | grep -c 'peer:') + 2 ))

# Add to server
sudo wg set wg0 peer "$CLIENT_PUBLIC_KEY" allowed-ips "$NEXT_IP/32"

# Generate client config
cat > "${CLIENT_NAME}.conf" << EOF
[Interface]
PrivateKey = $CLIENT_PRIVATE_KEY
Address = $NEXT_IP/24
DNS = 1.1.1.1

[Peer]
PublicKey = $SERVER_PUBLIC_KEY
Endpoint = $SERVER_ENDPOINT
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

echo "Client config saved to ${CLIENT_NAME}.conf"
qrencode -t ansiutf8 < "${CLIENT_NAME}.conf"
```

## Best Practices

1. **Secure keys** - Never share private keys
2. **Use preshared keys** - Additional security layer
3. **Rotate keys** - Change keys periodically
4. **Limit AllowedIPs** - Only allow needed ranges
5. **Enable keepalive** - For NAT traversal
6. **Firewall rules** - Restrict access appropriately
7. **Monitor connections** - Watch for anomalies
8. **Backup configs** - Keep secure backups
9. **Document peers** - Track who has access
10. **Update regularly** - Keep WireGuard updated

## When to Use This Skill

- Setting up VPN servers
- Configuring client connections
- Creating site-to-site tunnels
- Troubleshooting VPN issues
- Automating peer management
- Securing network communications
