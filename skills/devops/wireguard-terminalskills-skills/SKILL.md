---
name: wireguard
description: >-
  Deploy and manage WireGuard VPN tunnels. Use when a user asks to set up a
  WireGuard server, create peer configurations, build mesh networks, configure
  split tunneling, set up site-to-site links, automate peer provisioning,
  integrate with DNS (Pi-hole/AdGuard), manage keys, monitor connections, or
  build WireGuard-based overlay networks. Covers server setup, peer management,
  routing, DNS integration, and production deployment patterns.
license: Apache-2.0
compatibility: 'Linux kernel 5.6+ (built-in), or wireguard-tools on older kernels'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - wireguard
    - vpn
    - networking
    - tunneling
    - security
---

# WireGuard

## Overview

Deploy WireGuard — the modern, high-performance VPN protocol built into the Linux kernel. Simpler than OpenVPN, faster than IPsec, with a minimal attack surface (~4,000 lines of code). This skill covers server setup, peer management, split tunneling, site-to-site links, mesh topologies, DNS integration (Pi-hole/AdGuard), automated provisioning with QR codes, and monitoring.

## Instructions

### Step 1: Installation & Key Generation

```bash
# Ubuntu/Debian (kernel 5.6+ has WireGuard built-in)
apt update && apt install -y wireguard wireguard-tools qrencode

# Generate server keys
umask 077
wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key

# Generate peer keys (+ optional preshared key for post-quantum resistance)
wg genkey | tee client1_private.key | wg pubkey > client1_public.key
wg genpsk > client1_preshared.key
```

### Step 2: Server Configuration

**`/etc/wireguard/wg0.conf`:**
```ini
[Interface]
Address = 10.10.0.1/24
ListenPort = 51820
PrivateKey = SERVER_PRIVATE_KEY
SaveConfig = false

PostUp = iptables -t nat -A POSTROUTING -s 10.10.0.0/24 -o eth0 -j MASQUERADE; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -s 10.10.0.0/24 -o eth0 -j MASQUERADE; iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT

[Peer]
PublicKey = ALICE_PUBLIC_KEY
PresharedKey = ALICE_PRESHARED_KEY
AllowedIPs = 10.10.0.2/32
```

**Replace `eth0` with your actual interface and start:**
```bash
IFACE=$(ip route get 1.1.1.1 | awk '{print $5; exit}')
sed -i "s/eth0/$IFACE/g" /etc/wireguard/wg0.conf

echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf && sysctl -p
systemctl enable --now wg-quick@wg0
ufw allow 51820/udp
```

### Step 3: Client/Peer Configuration

**Full tunnel** (all traffic through VPN):
```ini
[Interface]
PrivateKey = CLIENT_PRIVATE_KEY
Address = 10.10.0.2/32
DNS = 1.1.1.1, 1.0.0.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
PresharedKey = PRESHARED_KEY
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

**Split tunnel** (only specific networks): change `AllowedIPs` to `10.10.0.0/24, 10.0.0.0/8, 192.168.0.0/16`

**QR code for mobile:** `qrencode -t ansiutf8 < client1.conf`

### Step 4: Automated Peer Provisioning

```bash
#!/bin/bash
# add-peer.sh — generate keys, add to server, create client config + QR
set -e
PEER_NAME=$1; SERVER_IP="your.server.ip"; SERVER_PORT=51820
SERVER_PUBKEY=$(cat /etc/wireguard/server_public.key)
WG_SUBNET="10.10.0"

LAST_IP=$(grep -oP 'AllowedIPs = 10\.10\.0\.\K\d+' /etc/wireguard/wg0.conf | sort -n | tail -1)
NEXT_IP=$((${LAST_IP:-1} + 1))

PRIV=$(wg genkey); PUB=$(echo "$PRIV" | wg pubkey); PSK=$(wg genpsk)

# Add peer live + to config
wg set wg0 peer "$PUB" preshared-key <(echo "$PSK") allowed-ips "${WG_SUBNET}.${NEXT_IP}/32"
cat >> /etc/wireguard/wg0.conf <<EOF

# ${PEER_NAME}
[Peer]
PublicKey = ${PUB}
PresharedKey = ${PSK}
AllowedIPs = ${WG_SUBNET}.${NEXT_IP}/32
EOF

# Generate client config
mkdir -p ~/wg-clients
cat > ~/wg-clients/${PEER_NAME}.conf <<EOF
[Interface]
PrivateKey = ${PRIV}
Address = ${WG_SUBNET}.${NEXT_IP}/32
DNS = 1.1.1.1, 1.0.0.1

[Peer]
PublicKey = ${SERVER_PUBKEY}
PresharedKey = ${PSK}
Endpoint = ${SERVER_IP}:${SERVER_PORT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

qrencode -t ansiutf8 < ~/wg-clients/${PEER_NAME}.conf
echo "Peer added: ${PEER_NAME} (${WG_SUBNET}.${NEXT_IP})"
```

**Remove a peer:** `wg set wg0 peer "$PEER_PUB" remove` and edit `wg0.conf` to remove the block.

### Step 5: Site-to-Site VPN

**Office A** (LAN: 192.168.1.0/24):
```ini
[Interface]
Address = 10.10.0.1/24
ListenPort = 51820
PrivateKey = OFFICE_A_PRIVATE
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT

[Peer]
PublicKey = OFFICE_B_PUBLIC
Endpoint = office-b.example.com:51820
AllowedIPs = 10.10.0.2/32, 192.168.2.0/24
PersistentKeepalive = 25
```

Office B mirrors this with its own private key, Office A's public key, and `AllowedIPs = 10.10.0.1/32, 192.168.1.0/24`. Both need IP forwarding enabled.

### Step 6: DNS Integration & Monitoring

**Pi-hole on WireGuard server:**
```bash
curl -sSL https://install.pi-hole.net | bash
pihole -a -i wg0
# Set client DNS to 10.10.0.1
```

**Monitoring:**
```bash
wg show          # Active peers, endpoints, transfer stats, last handshake
wg show wg0 dump # Machine-readable output for scripting
```

**Performance tuning:**
```bash
sysctl -w net.core.rmem_max=2500000
sysctl -w net.core.wmem_max=2500000
# In [Interface]: MTU = 1380 (for networks with extra encapsulation)
```

## Examples

### Example 1: Deploy a WireGuard server and provision 5 team members
**User prompt:** "Set up WireGuard on our Ubuntu 22.04 server at 203.0.113.10. Create peers for alice, bob, carol, dave, and eve with full tunnel configs and generate QR codes for mobile setup."

The agent will install wireguard and qrencode, generate server keys, create `/etc/wireguard/wg0.conf` with the server interface on 10.10.0.1/24 and NAT masquerading, enable IP forwarding, write an `add-peer.sh` script, run it for each of the five team members to generate key pairs, append peer blocks to the server config, create individual `.conf` files with full tunnel routing (AllowedIPs 0.0.0.0/0), display QR codes for each, and start the wg-quick service.

### Example 2: Connect two office networks over a site-to-site WireGuard tunnel
**User prompt:** "Office A is at 198.51.100.5 with LAN 192.168.1.0/24 and Office B is at 203.0.113.20 with LAN 192.168.2.0/24. Set up a WireGuard site-to-site tunnel so both LANs can reach each other."

The agent will generate key pairs on both servers, create `wg0.conf` on Office A with a peer block for Office B listing `AllowedIPs = 10.10.0.2/32, 192.168.2.0/24`, create the mirror config on Office B with `AllowedIPs = 10.10.0.1/32, 192.168.1.0/24`, enable IP forwarding and iptables FORWARD rules on both machines, open UDP port 51820 in the firewall, and start `wg-quick@wg0` on each side.

## Guidelines

- Always use `umask 077` before generating keys so private keys are readable only by root
- Enable preshared keys (`wg genpsk`) on all peers for defense-in-depth against future quantum computing attacks
- WireGuard has no built-in user authentication; access is controlled entirely by key pairs, so treat private keys like passwords and revoke peers by removing their public key from the server
- Set `PersistentKeepalive = 25` for peers behind NAT to keep the UDP session alive; omit it for server-to-server links where both sides have public IPs
- The `AllowedIPs` field serves as both a routing table and an ACL; it controls which IPs a peer can send traffic from and which destination IPs get routed to that peer
- Back up `/etc/wireguard/wg0.conf` before adding peers since `wg-quick` will refuse to start if the config has syntax errors
