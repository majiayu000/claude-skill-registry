---
name: wireless-rf
description: Use when the target has a non-Wi-Fi radio attack surface — Bluetooth/BLE (GATT, pairing, KNOB/BIAS/BleedingTooth), Zigbee/Thread/Matter & Z-Wave mesh (Touchlink, S0 downgrade), LoRaWAN/Sub-GHz LPWAN, SDR capture/replay/rolljam, smart locks/medical/IoT radios. For Wi-Fi/WPA/evil-twin see network-attack.
metadata:
  type: offensive
  phase: exploitation
  tools: bettercap, bluetoothctl, hcitool, gatttool, bleak, crackle, Sniffle, Ubertooth, btlejack, KillerBee, zbstumbler, RfCat, HackRF, rtl_433, Universal-Radio-Hacker, gr-lora, Scapy-radio
  mitre: TA0009
kill_chain:
  phase: [recon, exploit, actions]
  step: [1, 4, 7]
  attck_tactics: [TA0043, TA0001, TA0006, TA0009, TA0040]
  attck_techniques: [T1200, T1040, T1557, T1011, T1011.001, T1592, T1602]
depends_on: [recon-osint]
feeds_into: [network-attack, mobile-pentest, reverse-engineering, exploit-development]
inputs: [rf_target_inventory, device_class, radio_captures]
outputs: [recovered_keys, replayed_commands, sniffed_traffic, device_control, firmware_pull_hints]
references:
  - references/bluetooth.md
  - references/mesh-iot-radio.md
  - references/lpwan-subghz.md
scripts:
  - scripts/rf_recon.sh
---

# Wireless / RF (non-Wi-Fi radio)

Radio attack surface **beyond Wi-Fi**: Bluetooth (BLE + Classic), 802.15.4 mesh (Zigbee/Thread/Matter),
Z-Wave, and LPWAN/Sub-GHz (LoRaWAN, ISM rolling-code / OOK-ASK). For Wi-Fi, WPA2/WPA3, evil-twin and
802.1X, use `network-attack` (`references/wireless-attacks.md`, which also now carries KRACK/FragAttacks
and WPS). Adapted in part from Claude-Red (MIT, Kai Aizen/SnailSploit) — see `THIRD-PARTY-NOTICES.md`.

## When to Activate

- Auditing a **BLE** device (smart lock, wearable, medical, tracker): GATT enumeration, unauthenticated
  characteristic R/W, pairing-mode identification, LTK recovery, sniffing, companion-app RE.
- **Bluetooth Classic** targets: encryption-key entropy downgrade (KNOB), impersonation (BIAS), BlueZ/stack
  memory-corruption (BlueBorne / BleedingTooth).
- **Zigbee / Thread / Matter / Z-Wave** home/building automation: Touchlink commissioning abuse, key
  transport in the clear, S0 key-exchange downgrade, replay/AiTM on mesh commands.
- **LoRaWAN / Sub-GHz**: join-accept / uplink replay, ABP counter & nonce reuse, and generic ISM
  capture→replay / rolljam of OOK-ASK remotes (garage, gate, some auto keyfobs).
- You have (or can request) the right radio: a dual-mode BT adapter + BLE sniffer (Sniffle/Ubertooth),
  a KillerBee-supported 802.15.4 stick, an RfCat dongle (CC1111), and/or an SDR (RTL-SDR, HackRF).
- **STOP if the RF target or its band is out of scope.** RF is trivially cross-boundary (you will hear
  neighbours). Confirm `scope.json` and the physical/RF authorization before transmitting. Jamming,
  deauth-style disruption, and replay against safety/medical systems can be illegal and dangerous —
  see OPSEC & Detection.

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| BLE GATT enum + unauth characteristic R/W | T1040 / T1592 | CWE-306 | references/bluetooth.md | scripts/rf_recon.sh |
| BLE LE-Legacy Just-Works LTK recovery (crackle) | T1557 | CWE-322 | references/bluetooth.md | - |
| BLE sniffing / active MITM (Sniffle/btlejack) | T1040 / T1557 | CWE-319 | references/bluetooth.md | scripts/rf_recon.sh |
| BT Classic key-entropy downgrade (KNOB, CVE-2019-9506) | T1557 | CWE-326 | references/bluetooth.md | - |
| BT Classic impersonation (BIAS, CVE-2020-10135) | T1557 | CWE-287 | references/bluetooth.md | - |
| BlueZ/stack RCE (BleedingTooth CVE-2020-12351/12352) | T1200 | CWE-787 | references/bluetooth.md | - |
| Bluetooth data exfiltration | T1011.001 | CWE-319 | references/bluetooth.md | - |
| Zigbee Touchlink commissioning abuse / reset | T1557 | CWE-284 | references/mesh-iot-radio.md | scripts/rf_recon.sh |
| Zigbee/ZLL key transport in clear + replay | T1040 / T1557 | CWE-319 | references/mesh-iot-radio.md | scripts/rf_recon.sh |
| Z-Wave S0 key-exchange downgrade ("Z-Shave") | T1557 | CWE-757 | references/mesh-iot-radio.md | - |
| LoRaWAN join-accept / uplink replay | T1602 | CWE-294 | references/lpwan-subghz.md | - |
| LoRaWAN ABP counter / nonce reuse | T1040 | CWE-323 | references/lpwan-subghz.md | - |
| Sub-GHz OOK-ASK capture→replay / rolljam | T1557 | CWE-294 | references/lpwan-subghz.md | scripts/rf_recon.sh |

## Quick Start

```bash
# 0. AUTHORIZATION FIRST — confirm the RF target/band is in scope (RF crosses walls).
python3 ../coding-mastery/scripts/_lib/scope_guard.py --target "<device-id-or-mac>" || exit 3

# 1. BLE recon: discover, enumerate GATT, flag unauthenticated writable characteristics
sudo bash scripts/rf_recon.sh ble-scan
sudo bash scripts/rf_recon.sh ble-enum <BD_ADDR>      # services/characteristics + R/W perms

# 2. BLE pairing/crypto: identify pairing method; LE-Legacy Just Works -> crackle recovers LTK
#    (capture pairing with Sniffle/Ubertooth to a pcap, then:)
crackle -i pairing.pcap                                # LTK/STK if LE Legacy

# 3. 802.15.4 mesh recon (KillerBee): find Zigbee networks + channel
sudo bash scripts/rf_recon.sh zb-scan                  # zbstumbler across channels 11-26

# 4. Sub-GHz capture -> analyze -> replay (RfCat / SDR). rtl_433 first to fingerprint.
sudo bash scripts/rf_recon.sh subghz-id                 # rtl_433 protocol/mod fingerprint
#    then capture+replay in Universal Radio Hacker (URH), watching for rolling codes.
```

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection | OPSEC / legal note |
|-----------|-----------------|-----------|--------------------|
| BLE scan/enum | connectable advertising probes; repeated GATT connects | BLE WIDS (rare); app-side connection anomaly | passive `hcitool lescan`/Sniffle is quiet; enumeration is a normal client action |
| BLE MITM / LTK recovery | cloned advertiser; a 2nd device holding the connection | duplicate BD_ADDR; RSSI/2-radio anomaly | LE Legacy Just Works is the weak path; LE Secure Connections (ECDH) defeats crackle |
| KNOB / BIAS (Classic) | renegotiated low-entropy key; unexpected re-pair | patched stacks reject 1-byte entropy / require MITM-protection | needs proximity + a window; patched hosts (post-2019/2020) mitigate |
| BleedingTooth / BlueBorne | target BlueZ/stack crash or reboot | crash telemetry; kernel/stack patch level | memory-corruption = crash/DoS risk; lab-validate, get written sign-off |
| Zigbee Touchlink / key-in-clear | Touchlink scan/identify; devices leaving/rejoining | 802.15.4 IDS (rare); coordinator join logs | Touchlink range abuse can factory-reset lights building-wide — scope tight |
| Z-Wave S0 downgrade | S0 key-exchange when S2 expected | controller S2 bootstrap logs | needs presence during (re)pairing; S2 defeats it |
| LoRaWAN replay | duplicate frame counters at the NS; join floods | NS frame-counter monitoring; join-nonce checks | 1.0.x is weaker than 1.1; downlink replay can toggle actuators |
| Sub-GHz replay / rolljam | jamming energy in-band + delayed replay | RF spectrum monitoring (rare on ISM) | **jamming is illegal in most jurisdictions**; rolljam defeats rolling codes but needs jam+capture — explicit authorization only |

## Deep Dives

- **references/bluetooth.md** — BLE (GATT enumeration & unauth R/W, pairing-method identification, LE-Legacy
  Just-Works LTK recovery with crackle, Sniffle/btlejack sniffing & active MITM, companion-app RE, device-class
  playbooks for locks/medical/wearables) and Bluetooth Classic (KNOB CVE-2019-9506, BIAS CVE-2020-10135,
  BlueBorne, BleedingTooth CVE-2020-12351/12352/24490, BLESA, SweynTooth). Detection + OPSEC per technique.
- **references/mesh-iot-radio.md** — 802.15.4 mesh: Zigbee (Touchlink/ZLL commissioning abuse & master-key
  leak, key transport in the clear, NWK/APS replay, KillerBee/zbstumbler/zbdump), Thread/Matter (commissioning,
  OpenThread lab), and Z-Wave (S0 key-exchange downgrade "Z-Shave", S2 bootstrap, Scapy-radio/EZ-Wave, RfCat).
- **references/lpwan-subghz.md** — LoRaWAN (1.0.x vs 1.1 root/session keys, join-accept & uplink replay, ABP
  counter/nonce reuse, gr-lora/ChirpStack lab) and generic Sub-GHz/ISM (rtl_433 fingerprinting, RfCat CC1111,
  HackRF + Universal Radio Hacker capture→replay, OOK-ASK rolling-code vs fixed-code, rolljam theory & legality).

## Cross-references

- **Wi-Fi / WPA2 / WPA3 / evil-twin / 802.1X / KRACK / WPS →** `network-attack` (`references/wireless-attacks.md`).
- **Companion-app / firmware reversing →** `reverse-engineering`; **mobile app pairing logic →** `mobile-pentest`.
- **REQUIRED:** `scope-discipline` before transmitting; `finding-discipline` before any `[CONFIRMED]`
  (an advertised characteristic is not impact — you must read/write it or recover the key). Authorized only (`TERMS.md`).
