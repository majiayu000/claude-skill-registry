---
name: esp32-workbench-serial-flashing
description: Device discovery, slot management, dual-USB hub boards, remote flashing via RFC2217, GPIO download mode, crash-loop recovery, and flapping. Triggers on "flash", "esptool", "device", "slot", "erase", "download mode", "crash loop", "flapping", "bricked".
---

# ESP32 Serial Flashing

Base URL: `http://192.168.0.87:8080`

## When to Use Serial Flashing

- Device has **no firmware** (blank/bricked/first flash)
- Firmware **lacks OTA support**
- You need to **erase NVS** or flash a **bootloader/partition table**
- Device has **no WiFi connectivity**
- **Alternative:** if device already runs OTA-capable firmware and is on WiFi, use OTA instead (see esp32-workbench-ota) — it's faster and doesn't block serial

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/devices` | List all slots with state, device node, RFC2217 URL |
| GET | `/api/info` | System info (host IP, hostname, slot counts) |
| POST | `/api/serial/reset` | Hardware reset via DTR/RTS pulse, returns boot output |
| POST | `/api/serial/recover` | Manual flap recovery trigger `{"slot": "SLOT1"}` |
| POST | `/api/serial/release` | Release GPIO after flashing, reboot into firmware `{"slot": "SLOT1"}` |

## Step 1: Discover Devices and Determine Board Type

Always start here.

```bash
curl -s http://192.168.0.87:8080/api/devices | jq .
```

Response fields per slot: `label`, `state`, `url` (RFC2217), `present`, `running`.

### Board type detection

| Present slots | Board type | How to identify |
|---------------|------------|-----------------|
| 1 slot | **Single-USB** | One `ttyACM`/`ttyUSB` device; same slot for flash + monitor |
| 2 slots (same hub parent) | **Dual-USB hub board** | Two `ttyACM` devices under a common USB hub path |

**For dual-USB boards**, identify which slot is which:

```bash
ssh pi@192.168.0.87 "udevadm info -q property /dev/ttyACM0 | grep ID_SERIAL"
# Contains "Espressif" → JTAG slot (flash + reset here)
# Contains "1a86", "CH340", "CP210x" → UART slot (serial console here)
```

### Slot roles

| Operation | Single-USB board | Dual-USB board |
|-----------|-----------------|----------------|
| **Flash (esptool)** | The one slot | JTAG slot |
| **Reset (DTR/RTS)** | The one slot (or Pi GPIO) | JTAG slot (auto-download circuit) |
| **GPIO control needed?** | Run GPIO probe (see esp32-workbench-gpio) | No (handled by JTAG DTR/RTS) |

## Step 2: Flash via RFC2217

Each slot exposes an RFC2217 URL from `/api/devices`. Use it with esptool.

> **Flash size and partition layout:** see the `idf-flash` skill for the
> authoritative flash size rule (default 4MB) and partition table selection.

**Baud rate:** Native USB devices (ESP32-S3/C3 `ttyACM`) ignore the baud rate — data transfers at USB speed regardless. The effective throughput is limited by the RFC2217 TCP proxy (~300 kbit/s). UART-bridge devices (`ttyUSB`) respect the baud rate. Use `-b 921600` as a sensible default for both cases.

```bash
# Get the RFC2217 URL
SLOT_URL=$(curl -s http://192.168.0.87:8080/api/devices | jq -r '.slots[0].url')

# Flash firmware using build-generated flash_args (recommended)
cd build && esptool.py --port "${SLOT_URL}?ign_set_control" \
  --chip esp32s3 -b 921600 write_flash @flash_args

# Erase NVS partition
esptool.py --port "${SLOT_URL}?ign_set_control" --chip esp32s3 erase_region 0x9000 0x6000
```

### esptool flags by device type

| Device | `--before` | `--after` |
|--------|-----------|----------|
| ESP32-S3 (ttyACM, native USB) | `usb_reset` | `hard_reset` |
| ESP32-C3 (ttyACM, native USB) | `usb_reset` | `watchdog_reset` |
| ESP32 (ttyUSB, UART bridge) | `default_reset` | `hard_reset` |

**For dual-USB boards:** always flash via the **JTAG slot** (not the UART slot).

## GPIO Download Mode

When DTR/RTS reset doesn't work (no auto-download circuit), use GPIO to enter download mode. See esp32-workbench-gpio for the full sequence.

After entering download mode via GPIO, flash with `--before=no_reset` (device is already in download mode):

```bash
# Wait 5s for USB re-enumeration after GPIO reset
sleep 5

esptool.py --port "rfc2217://192.168.0.87:<PORT>?ign_set_control" \
  --chip esp32s3 --before=no_reset write_flash 0x0 firmware.bin
```

## Crash-Loop Recovery

When firmware crashes on boot, the ESP32 enters a rapid panic→reboot cycle. Serial monitor shows repeated `rst:0xc (RTC_SW_CPU_RST)` with crash backtraces.

**For native USB devices (ESP32-S3/C3):** `esptool --before=usb_reset` can connect even during a crash loop — it catches the device during the brief USB re-enumeration between reboots.

```bash
esptool.py --port "rfc2217://192.168.0.87:<PORT>?ign_set_control" \
  --chip esp32s3 --before=usb_reset erase_flash
```

After erasing, the device boots to empty flash and stops looping. Verify with serial reset — should show `rst:0x15 (USB_UART_CHIP_RESET)` and `boot:0x28 (SPI_FAST_FLASH_BOOT)`.

## Flapping & Automatic Recovery

Empty or corrupt flash can cause USB connection cycling (`flapping` state — add/remove every ~3s). The portal now **actively recovers** by unbinding USB at the kernel level to stop the event storm, then recovering the device.

### How it works

1. **Detection:** 6+ hotplug events in 30s → `flapping` state
2. **USB unbind:** portal writes to `/sys/bus/usb/drivers/usb/unbind` → storm stops immediately, Pi stays reachable
3. **Recovery dispatch** (background thread):
   - **GPIO path** (slots with `gpio_boot`/`gpio_en` in slots.json): hold BOOT LOW → pulse EN → rebind USB → device enumerates in **download mode** (stable)
   - **No-GPIO path**: fixed cooldown (10s), rebind and retry up to 2 times
4. **Result:** slot enters `download_mode` (GPIO) or retries until stable / flags manual intervention (no-GPIO)

### Recovery with GPIO (automatic)

```
State flow: flapping → recovering → download_mode → (flash firmware) → idle
```

After the portal reaches `download_mode`, upload build artifacts to the Pi and flash (use flash size matching the board — see `idf-flash` skill):

```bash
scp build/bootloader/bootloader.bin build/partition_table/partition-table.bin \
    build/ota_data_initial.bin build/wb-test-firmware.bin pi@192.168.0.87:/tmp/
ssh pi@192.168.0.87 "python3 -m esptool --chip esp32s3 --port /dev/ttyACM1 \
  write_flash --flash_mode dio --flash_size 4MB \
  0x0 /tmp/bootloader.bin 0x8000 /tmp/partition-table.bin \
  0xf000 /tmp/ota_data_initial.bin 0x20000 /tmp/wb-test-firmware.bin"
```

Then release GPIO and reboot into firmware:

```bash
curl -X POST http://192.168.0.87:8080/api/serial/release \
  -H 'Content-Type: application/json' -d '{"slot": "SLOT1"}'
```

### Recovery without GPIO (backoff + retry)

```
State flow: flapping → recovering → idle (if stable) or flapping (retry, up to 2x)
```

After 2 failed attempts, the slot shows "needs manual intervention". Upload build artifacts and flash directly on the Pi:

```bash
ssh pi@192.168.0.87 "python3 -m esptool --chip esp32s3 --port /dev/ttyACM0 \
  --before=usb_reset --after=hard_reset write_flash \
  --flash_mode dio --flash_size 4MB \
  0x0 /tmp/bootloader.bin 0x8000 /tmp/partition-table.bin \
  0xf000 /tmp/ota_data_initial.bin 0x20000 /tmp/wb-test-firmware.bin"
```

Once the device boots stable firmware, the flapping flag auto-clears on the next poll (within 5s).

### Manual recovery trigger

```bash
curl -X POST http://192.168.0.87:8080/api/serial/recover \
  -H 'Content-Type: application/json' -d '{"slot": "SLOT1"}'
```

Resets retry counter and starts a fresh recovery cycle. Works even when not currently flapping.

### `/api/devices` recovery fields

| Field | Type | Description |
|-------|------|-------------|
| `recovering` | bool | USB unbound, recovery in progress |
| `recover_retries` | int | No-GPIO retry counter (0-2) |
| `has_gpio` | bool | Slot has `gpio_boot` configured |
| `gpio_boot` | int/null | Pi BCM pin wired to ESP32 BOOT/GPIO0 |
| `gpio_en` | int/null | Pi BCM pin wired to ESP32 EN/RST |

### GPIO pin configuration (slots.json)

```json
{"label": "SLOT1", "slot_key": "...", "tcp_port": 4001, "gpio_boot": 18, "gpio_en": 17}
```

Slots without `gpio_boot`/`gpio_en` use the no-GPIO backoff path.

## Slot States

| State | Meaning | Can flash? |
|-------|---------|------------|
| `absent` | No USB device | No |
| `idle` | Ready | Yes (via RFC2217) |
| `resetting` | Reset in progress | No |
| `monitoring` | Monitor active | No |
| `flapping` | USB storm, recovery failed or pending | No |
| `recovering` | USB unbound, recovery in progress | No |
| `download_mode` | GPIO holding BOOT LOW, device stable in bootloader | Yes (direct serial on Pi) |

## Serial Reset

Sends DTR/RTS pulse, captures boot output (up to 5s), restarts proxy automatically.

```bash
curl -X POST http://192.168.0.87:8080/api/serial/reset \
  -H 'Content-Type: application/json' \
  -d '{"slot": "slot-1"}'
```

Response: `{"ok": true, "output": ["line1", "line2", ...]}`

## Common Workflows

1. **Flash a blank device:** `GET /api/devices` to find slot URL → `esptool.py --port <url> write_flash ...`
2. **Flash via GPIO download mode:** enter download mode (see esp32-workbench-gpio) → wait 5s → `esptool.py --before=no_reset write_flash ...`
3. **Recover crash-looping device:** `esptool.py --before=usb_reset erase_flash` → then flash working firmware
4. **Recover flapping device (GPIO):** wait for `download_mode` state → flash on Pi → `POST /api/serial/release`
5. **Recover flapping device (no GPIO):** wait for backoff to stabilize, or `POST /api/serial/recover` to retry
6. **Manual recovery trigger:** `POST /api/serial/recover {"slot": "SLOT1"}` — works anytime

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Slot shows `absent` | Check USB cable, re-seat device |
| "proxy not running" | Device may be flapping — check `state` field |
| `flapping` state | Recovery should start automatically; if stuck, `POST /api/serial/recover` |
| `recovering` state | USB unbound, recovery in progress — wait for `download_mode` or `idle` |
| `download_mode` state | Flash firmware on the Pi, then `POST /api/serial/release` |
| "needs manual intervention" | No-GPIO recovery exhausted 2 retries — flash directly on Pi with `esptool --before=usb_reset` |
| esptool can't connect | Ensure slot is `idle`; for native USB use `--before=usb_reset` |
| esptool fails after GPIO download mode | Wait 5s for USB re-enumeration before connecting; use `--before=no_reset` |
| Device crash-looping (`rst:0xc` repeated) | Erase flash with `esptool.py --before=usb_reset erase_flash` |
| Board occupies two slots | Onboard USB hub — identify JTAG vs UART via `udevadm info` (see above) |
