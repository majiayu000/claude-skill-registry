---
name: esp32-workbench-logging
description: Serial monitor and UDP debug log retrieval from ESP32 devices. Covers pattern matching, boot capture, crash output, and runtime logging. Triggers on "serial monitor", "log", "debug log", "UDP log", "boot output", "crash", "monitor", "pattern".
---

# ESP32 Debug Logging

Base URL: `http://192.168.0.87:8080`

Two logging methods are available. Choose based on your situation:

| | Serial Monitor | UDP Logs |
|---|---|---|
| **Works without WiFi** | Yes | No |
| **Boot/crash output** | Yes | No |
| **Pattern matching** | Built-in (regex + timeout) | Manual (poll + grep) |
| **Blocks serial port** | Yes (one session per slot) | No |
| **Multiple devices** | One slot at a time | All devices simultaneously |
| **Long-running** | Limited by timeout | Continuous (buffer persists) |

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/serial/monitor` | Read serial output with optional pattern matching |
| POST | `/api/serial/reset` | Hardware reset via DTR/RTS, returns boot output |
| GET | `/api/udplog` | Retrieve UDP log lines (filter by source, since, limit) |
| DELETE | `/api/udplog` | Clear the UDP log buffer |
| GET | `/api/log` | Workbench activity log (portal actions, not device logs) |

## Serial Monitor

Reads serial output via RFC2217 proxy. Optionally waits for a regex pattern.

```bash
# Wait up to 10s for a pattern match
curl -X POST http://192.168.0.87:8080/api/serial/monitor \
  -H 'Content-Type: application/json' \
  -d '{"slot": "slot-1", "pattern": "WiFi connected", "timeout": 10}'

# Just capture output for 5s (no pattern)
curl -X POST http://192.168.0.87:8080/api/serial/monitor \
  -H 'Content-Type: application/json' \
  -d '{"slot": "slot-1", "timeout": 5}'
```

Response: `{"ok": true, "matched": true, "line": "WiFi connected to MyAP", "output": [...]}`

### Use serial monitor when:
- You need **boot messages** (before WiFi is up)
- You need to **wait for a specific log line** (pattern matching with timeout)
- Device has **no WiFi** or UDP logging is not compiled in
- You want **crash/panic output** from the UART

### Dual-USB hub boards
- **Reset** via the JTAG slot (triggers DTR/RTS auto-download circuit)
- **Monitor** via the UART slot (where ESP_LOGI output appears)
- Boot output on the JTAG slot will be empty or minimal — the actual boot log appears on the UART slot

```bash
# Reset via JTAG slot
curl -X POST http://192.168.0.87:8080/api/serial/reset \
  -H 'Content-Type: application/json' \
  -d '{"slot": "<JTAG-slot>"}'

# Capture boot output from UART slot
curl -X POST http://192.168.0.87:8080/api/serial/monitor \
  -H 'Content-Type: application/json' \
  -d '{"slot": "<UART-slot>", "timeout": 10}'
```

## UDP Logs

ESP32 firmware sends debug logs as UDP datagrams to the workbench on port 5555. The workbench buffers up to 2000 lines.

```bash
# Get recent UDP logs (default limit: 200)
curl -s http://192.168.0.87:8080/api/udplog | jq .

# Filter by source device IP
curl -s "http://192.168.0.87:8080/api/udplog?source=192.168.4.2" | jq .

# Get logs since a timestamp, limited to 50 lines
curl -s "http://192.168.0.87:8080/api/udplog?since=1700000000.0&limit=50" | jq .

# Clear the buffer before starting a test
curl -X DELETE http://192.168.0.87:8080/api/udplog
```

Response format: `{"ok": true, "lines": [{"ts": 1700000001.23, "source": "192.168.4.2", "line": "OTA progress: 45%"}, ...]}`

### Use UDP logs when:
- Device is **on WiFi** and firmware sends UDP log packets
- You want **non-blocking** log collection (doesn't tie up the serial port)
- You're monitoring **multiple devices** simultaneously (filter by source IP)
- You need logs during **OTA updates** (serial may be unavailable)

### Do NOT use UDP logs when:
- Device has **no WiFi** yet (pre-provisioning, boot phase) — use serial monitor
- Firmware **doesn't include UDP logging** — use serial monitor
- You need **boot/crash output** — only serial captures UART output from early boot
- You need to **wait for a specific pattern** with a timeout — serial monitor has built-in pattern matching

## How ESP32 Sends UDP Logs

The workbench listens on UDP port **5555**. ESP32 firmware sends plain text lines:

```c
struct sockaddr_in workbench = { .sin_family = AF_INET, .sin_port = htons(5555) };
inet_aton("192.168.0.87", &workbench.sin_addr);
sendto(sock, msg, strlen(msg), 0, (struct sockaddr *)&workbench, sizeof(workbench));
```

## Activity Log

The activity log tracks workbench actions (resets, WiFi changes, firmware uploads) — not device output.

```bash
curl -s http://192.168.0.87:8080/api/log | jq .
curl -s "http://192.168.0.87:8080/api/log?since=2025-01-01T00:00:00Z" | jq .
```

## Common Workflows

1. **Verify boot after flash:**
   - `POST /api/serial/reset` — returns boot output
   - Check for expected boot messages (e.g., `boot:0x28`, firmware version)

2. **Wait for WiFi connection:**
   - `POST /api/serial/monitor` with `pattern: "WiFi connected"` and `timeout: 15`

3. **Monitor OTA progress:**
   - `DELETE /api/udplog` — clear buffer
   - Trigger OTA (see esp32-workbench-ota)
   - Poll: `GET /api/udplog?since=<last_ts>&limit=50`

4. **Debug a running device:**
   - `GET /api/udplog?source=<device_ip>` — see what it's logging
   - If empty, device may not have UDP logging — fall back to serial monitor

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Monitor timeout, no output | Baud rate is fixed at 115200; ensure device matches. For dual-USB boards: make sure you're monitoring the UART slot, not the JTAG slot |
| No UDP logs appearing | Ensure firmware sends UDP to workbench IP:5555; check WiFi connectivity |
| Logs from wrong device | Use `source` query param to filter by IP |
| Old/stale logs | Clear with `DELETE /api/udplog` before starting a test |
| Need boot output | UDP logs don't capture boot — use serial monitor. For dual-USB boards, monitor the UART slot |
| Slot shows `monitoring` | Another monitor session is active — wait for it to finish |
