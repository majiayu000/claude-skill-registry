---
name: esp32-workbench-ota
description: OTA firmware upload, listing, deletion, and over-the-air update for the Universal ESP32 Workbench. Triggers on "OTA", "firmware", "update", "upload", "binary", "over-the-air".
---

# ESP32 OTA & Firmware Repository

Base URL: `http://192.168.0.87:8080`

## When to Use OTA (vs Serial Flashing)

### Use OTA when:
- Device **already runs firmware** with an OTA HTTP endpoint
- Device is **on the WiFi network** (connected to workbench's AP or same LAN)
- You want to update firmware **without blocking the serial port**
- You're doing **iterative development** (build → upload → trigger → monitor cycle)

### Do NOT use OTA when:
- Device is **blank/bricked** — use serial flashing (see esp32-workbench-serial-flashing)
- Device firmware **has no OTA support** — use serial flashing
- Device has **no WiFi connectivity** — use serial flashing
- You need to flash a **bootloader or partition table** — only esptool can do this

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/firmware/upload` | Upload firmware binary (multipart/form-data) |
| GET | `/api/firmware/list` | List all uploaded firmware files |
| DELETE | `/api/firmware/delete` | Delete a firmware file |
| GET | `/firmware/<project>/<file>` | Download URL (ESP32 fetches from here during OTA) |

## End-to-End OTA Workflow

### Step 1: Upload firmware to workbench

```bash
curl -X POST http://192.168.0.87:8080/api/firmware/upload \
  -F "project=my-project" \
  -F "file=@build/firmware.bin"
```

Response: `{"ok": true, "project": "my-project", "filename": "firmware.bin", "size": 456789}`

### Step 2: Verify upload

```bash
curl -s http://192.168.0.87:8080/api/firmware/list | jq .
```

### Step 3: Ensure device is on the network

The device must be able to reach `http://192.168.0.87:8080`. Use enter-portal to provision if needed (see esp32-workbench-wifi).

### Step 4: Clear UDP log buffer (for clean monitoring)

```bash
curl -X DELETE http://192.168.0.87:8080/api/udplog
```

### Step 5: Trigger OTA on the ESP32 via HTTP relay

```bash
OTA_BODY=$(echo -n '{"url":"http://192.168.0.87:8080/firmware/my-project/firmware.bin"}' | base64)

curl -X POST http://192.168.0.87:8080/api/wifi/http \
  -H 'Content-Type: application/json' \
  -d "{\"method\": \"POST\", \"url\": \"http://192.168.4.2/ota\", \"headers\": {\"Content-Type\": \"application/json\"}, \"body\": \"$OTA_BODY\", \"timeout\": 30}"
```

### Step 6: Monitor OTA progress

```bash
# Via UDP logs (preferred — non-blocking)
curl "http://192.168.0.87:8080/api/udplog?limit=50"

# Or via serial monitor (see esp32-workbench-logging)
curl -X POST http://192.168.0.87:8080/api/serial/monitor \
  -H 'Content-Type: application/json' \
  -d '{"slot": "slot-1", "pattern": "OTA.*complete", "timeout": 60}'
```

## Managing Firmware Files

```bash
# List all uploaded firmware
curl http://192.168.0.87:8080/api/firmware/list

# Delete a firmware file
curl -X DELETE http://192.168.0.87:8080/api/firmware/delete \
  -H 'Content-Type: application/json' \
  -d '{"project": "my-project", "filename": "firmware.bin"}'

# The download URL for ESP32 to fetch:
# http://192.168.0.87:8080/firmware/<project>/<filename>
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Upload returns "expected multipart/form-data" | Use `-F` flags (not `-d`) for multipart upload |
| File not in list after upload | Check project/filename; `..` and `/` are rejected |
| ESP32 can't download firmware | Device must reach workbench at 192.168.0.87:8080; check WiFi |
| OTA trigger times out | Check device's OTA endpoint URL; increase HTTP relay timeout |
| No progress in UDP logs | Device may not send UDP logs — check serial monitor instead (see esp32-workbench-logging) |
| OTA trigger returns error | Verify device firmware has OTA endpoint; check relay response body |
