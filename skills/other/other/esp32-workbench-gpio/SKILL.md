---
name: esp32-workbench-gpio
description: GPIO pin control on the Raspberry Pi workbench for driving ESP32 boot modes and buttons. Triggers on "GPIO", "pin", "boot mode", "button", "hardware reset", "download mode".
---

# ESP32 GPIO Control

Base URL: `http://192.168.0.87:8080`

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/gpio/set` | Drive a pin: `0` (low) or `1` (high) |
| GET | `/api/gpio/status` | Read state of all driven pins |

## Allowed BCM Pins

`5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27`

## Pin Values

Only use `0` (low) and `1` (high). Release = drive HIGH (`1`).

## Pin Mapping

| Pi GPIO | ESP32 Pin | Function |
|---------|-----------|----------|
| GPIO17 | EN | **RST** — pull LOW to reset the ESP32 |
| GPIO18 | GPIO0 | **BOOT** — hold LOW during reset to enter download mode |

## Examples

```bash
# Drive GPIO18 LOW (hold BOOT button)
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' \
  -d '{"pin": 18, "value": 0}'

# Drive GPIO18 HIGH (release)
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' \
  -d '{"pin": 18, "value": 1}'

# Read all driven pin states
curl http://192.168.0.87:8080/api/gpio/status
```

## Common Workflows

1. **Enter ESP32 download mode** (hold BOOT during reset):
   ```bash
   # 1. Hold BOOT (GPIO18) LOW
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 18, "value": 0}'
   sleep 1
   # 2. Pull EN (GPIO17) LOW — assert reset
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 17, "value": 0}'
   sleep 0.2
   # 3. Release EN HIGH — ESP32 exits reset, samples BOOT=LOW → download mode
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 17, "value": 1}'
   sleep 0.5
   # 4. Release BOOT HIGH
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 18, "value": 1}'
   ```

2. **Flash after GPIO download mode:**
   ```bash
   # Wait 5s for USB re-enumeration after GPIO reset
   sleep 5
   esptool.py --port "rfc2217://192.168.0.87:<PORT>?ign_set_control" \
     --chip esp32s3 --before=no_reset write_flash 0x0 firmware.bin
   ```

3. **Normal reset** (without entering download mode):
   ```bash
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 17, "value": 0}'
   sleep 0.2
   curl -X POST http://192.168.0.87:8080/api/gpio/set \
     -H 'Content-Type: application/json' -d '{"pin": 17, "value": 1}'
   ```

4. **Simulate button press:**
   - Set pin LOW, wait, set pin HIGH (`1`) to release

## GPIO Control Probe — Auto-Detecting Board Capabilities

Not all boards have EN/BOOT pins wired to Pi GPIOs. Run this probe once per board.

### Probe Procedure

```bash
# Step 1: Try GPIO-based download mode entry
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' -d '{"pin": 18, "value": 0}'
sleep 1
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' -d '{"pin": 17, "value": 0}'
sleep 0.2
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' -d '{"pin": 17, "value": 1}'
sleep 0.5
curl -X POST http://192.168.0.87:8080/api/gpio/set \
  -H 'Content-Type: application/json' -d '{"pin": 18, "value": 1}'

# Monitor for boot output
curl -X POST http://192.168.0.87:8080/api/serial/monitor \
  -H 'Content-Type: application/json' \
  -d '{"slot": "<slot>", "pattern": "boot:", "timeout": 3}'

# Step 2: If GPIO had no effect, try USB DTR/RTS reset
curl -X POST http://192.168.0.87:8080/api/serial/reset \
  -H 'Content-Type: application/json' -d '{"slot": "<slot>"}'
```

### Interpreting Results

| GPIO probe output | USB reset output | Board type |
|-------------------|-----------------|------------|
| `boot:0x23` (DOWNLOAD) | — | **GPIO-controlled** — Pi GPIOs wired to EN/BOOT |
| No output / normal boot | Hardware reset output (`rst:0x15`) | **USB-controlled** — no GPIO wiring, use DTR/RTS |
| No output | No output | No control — check wiring or wrong slot |

### Caveats
- **Firmware crash loops** (`rst:0xc`) mask GPIO resets. Erase flash first with `esptool.py --before=usb_reset erase_flash`, then re-run the probe.
- **Dual-USB hub boards** always respond to USB DTR/RTS on the JTAG slot; GPIO probe will show no effect.
- Probe only needs to run once per physical board.

## Note: Dual-USB Hub Boards

Some ESP32-S3 dev boards have an onboard USB hub with a built-in auto-download circuit that connects GPIO0/EN to DTR/RTS on the USB-Serial/JTAG interface. For these boards, **external Pi GPIO wiring is not needed** — DTR/RTS on the JTAG slot handles reset and download mode via `POST /api/serial/reset`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "pin not in allowed set" | Use only the BCM pins listed above |
| Pin stays driven after test | Drive pins HIGH (`1`) to release |
| Pi crashes during GPIO operations | Ensure pins are driven HIGH (`1`) when not actively pulling LOW |
| GPIO reset not needed | Board may have onboard auto-download circuit (dual-USB hub board) |
| Probe shows crash loop output | Board is rebooting from firmware panic. Erase flash first for clean probe |
