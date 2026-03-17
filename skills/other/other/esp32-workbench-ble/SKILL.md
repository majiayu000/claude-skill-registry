---
name: esp32-workbench-ble
description: Bluetooth LE scanning, connecting, and GATT writes via the Universal ESP32 Workbench. Triggers on "BLE", "bluetooth", "GATT", "NUS", "Nordic UART".
---

# ESP32 Bluetooth LE Proxy

Base URL: `http://192.168.0.87:8080`

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/ble/scan` | Scan for BLE devices (optional name filter) |
| POST | `/api/ble/connect` | Connect to a device by MAC address |
| POST | `/api/ble/write` | Write hex data to a GATT characteristic |
| POST | `/api/ble/disconnect` | Disconnect current device |
| GET | `/api/ble/status` | Connection state and device info |

One BLE connection at a time.

## Examples

```bash
# Scan for BLE devices (5s timeout)
curl -X POST http://192.168.0.87:8080/api/ble/scan \
  -H 'Content-Type: application/json' \
  -d '{"timeout": 5}'

# Scan with name filter
curl -X POST http://192.168.0.87:8080/api/ble/scan \
  -H 'Content-Type: application/json' \
  -d '{"timeout": 5, "name_filter": "iOS-Keyboard"}'

# Connect by MAC address
curl -X POST http://192.168.0.87:8080/api/ble/connect \
  -H 'Content-Type: application/json' \
  -d '{"address": "AA:BB:CC:DD:EE:FF"}'

# Write hex data to a GATT characteristic
curl -X POST http://192.168.0.87:8080/api/ble/write \
  -H 'Content-Type: application/json' \
  -d '{"characteristic": "6e400002-b5a3-f393-e0a9-e50e24dcca9e", "data": "48656c6c6f", "response": true}'

# Check connection status
curl http://192.168.0.87:8080/api/ble/status

# Disconnect
curl -X POST http://192.168.0.87:8080/api/ble/disconnect
```

## Nordic UART Service (NUS) UUIDs

| UUID | Role |
|------|------|
| `6e400001-b5a3-f393-e0a9-e50e24dcca9e` | NUS Service |
| `6e400002-b5a3-f393-e0a9-e50e24dcca9e` | RX Characteristic (write to this) |
| `6e400003-b5a3-f393-e0a9-e50e24dcca9e` | TX Characteristic (notifications from device) |

## Common Workflows

1. **Send a command via NUS:**
   - `POST /api/ble/scan` with `name_filter` to find device
   - `POST /api/ble/connect` with the MAC address from scan results
   - `POST /api/ble/write` with NUS RX UUID and hex-encoded command
   - `POST /api/ble/disconnect` when done

2. **Check if device is advertising:**
   - `POST /api/ble/scan` with short timeout and name filter
   - Check `devices` array in response

3. **Send binary command protocol:**
   - Connect to device
   - Encode command bytes as hex (e.g., `0x02` + "Hello" = `0248656c6c6f`)
   - Write to NUS RX characteristic
   - Monitor device response via serial or UDP logs (see esp32-workbench-logging)

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "BLE not available" | `bleak` not installed on workbench Pi |
| Scan returns empty | Increase timeout; check device is advertising |
| Connect fails (409) | Already connected — disconnect first |
| Write fails "invalid hex data" | Data must be hex string (e.g., `"48656c6c6f"` for "Hello") |
| Device not found by name | Check exact advertised name; BLE names are case-sensitive |
