---
name: esp32-workbench-mqtt
description: MQTT broker control on the Universal ESP32 Workbench. Start and stop the broker for testing ESP32 MQTT clients. Triggers on "MQTT", "broker", "mosquitto", "pub", "sub", "publish", "subscribe".
---

# ESP32 MQTT Broker

Base URL: `http://192.168.0.87:8080`

The workbench can run an MQTT broker (mosquitto) for testing ESP32 devices that use MQTT for communication. The broker is accessible to devices connected to the workbench's WiFi AP.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/mqtt/start` | Start the MQTT broker |
| POST | `/api/mqtt/stop` | Stop the MQTT broker |
| GET | `/api/mqtt/status` | Check broker status |

## Examples

```bash
# Start the MQTT broker
curl -X POST http://192.168.0.87:8080/api/mqtt/start

# Check broker status
curl http://192.168.0.87:8080/api/mqtt/status

# Stop the MQTT broker
curl -X POST http://192.168.0.87:8080/api/mqtt/stop
```

## MQTT Broker Details

| Property | Value |
|----------|-------|
| Broker IP | `192.168.0.87` (from LAN) or `192.168.4.1` (from workbench AP) |
| Default port | `1883` |
| Authentication | None (open broker for testing) |

## Common Workflows

1. **Test ESP32 MQTT client:**
   - Ensure device is on workbench WiFi (see esp32-workbench-wifi)
   - `POST /api/mqtt/start` — start broker
   - Device connects to `192.168.4.1:1883`
   - Monitor device behavior via serial or UDP logs (see esp32-workbench-logging)
   - `POST /api/mqtt/stop` — stop broker when done

2. **Test MQTT disconnect/reconnect:**
   - Start broker, let device connect
   - `POST /api/mqtt/stop` — device loses MQTT
   - Monitor device's reconnection behavior
   - `POST /api/mqtt/start` — device should reconnect

3. **Test MQTT + WiFi together:**
   - Start AP + broker
   - `POST /api/wifi/ap_stop` — device loses both WiFi and MQTT
   - `POST /api/wifi/ap_start` + `POST /api/mqtt/start` — restore both
   - Verify device recovers

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Broker won't start | Check if mosquitto is installed on the workbench Pi |
| Device can't connect | Ensure device is on workbench WiFi; use broker IP `192.168.4.1` from AP clients |
| Broker status shows stopped | Start it with `POST /api/mqtt/start` |
