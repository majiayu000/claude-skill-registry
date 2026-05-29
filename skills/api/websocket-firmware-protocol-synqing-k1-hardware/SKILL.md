---
name: Websocket-Firmware-Protocol
keywords: websocket, protocol, serialization, messaging, Godot, JSON, data frame, connection state, handshake, event, command, response, real-time
---

# Websocket Firmware Protocol

## Quick Reference

Emotiscope firmware communicates with Godot web app via WebSocket. Protocol defines message format, command structure, and state synchronization.

## Core Principles

1. **JSON-based messaging**: Human-readable, easy to debug
2. **Event-driven**: Changes broadcast to client immediately
3. **Request-response**: Commands get acknowledgments
4. **Bidirectional**: Client→firmware AND firmware→client

## Connection Lifecycle

```
CLIENT              FIRMWARE
  |                   |
  |----connect------->|
  |<---identify------|  (send device info)
  |----auth--------->|  (if needed)
  |<---ready---------|
  |                   |
  | (commands/events) |
  |                   |
  |<---data stream----|  (audio, stats, status)
  |                   |
  |----disconnect---->|
  |<---goodbye--------|
```

## Message Frame Format

### Basic Structure (JSON)
```json
{
    "type": "command|event|response",
    "cmd": "command_name",
    "id": 123,
    "data": { ... }
}
```

### Message Fields
| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `type` | string | YES | "command", "event", "response", "ack" |
| `cmd` | string | YES | Command or event name |
| `id` | number | For commands | Unique ID for request/response pairing |
| `data` | object | Usually | Payload specific to command |
| `error` | string | For errors | Error message if failed |

## Command Types (Firmware → Client)

### Set Mode
```json
{
    "type": "command",
    "cmd": "set_mode",
    "id": 1,
    "data": {
        "mode": "spectrum"  // or: harmonic, wave, rhythm_breeze
    }
}
```

### Set Speed
```json
{
    "type": "command",
    "cmd": "set_speed",
    "id": 2,
    "data": {
        "speed": 1.5  // 0.5 = half speed, 2.0 = double speed
    }
}
```

### Set Brightness
```json
{
    "type": "command",
    "cmd": "set_brightness",
    "id": 3,
    "data": {
        "brightness": 255  // 0-255
    }
}
```

### Set Color Palette
```json
{
    "type": "command",
    "cmd": "set_palette",
    "id": 4,
    "data": {
        "palette_id": 5  // or palette_name
    }
}
```

### Request Current State
```json
{
    "type": "command",
    "cmd": "get_state",
    "id": 5
}
```

Response:
```json
{
    "type": "response",
    "cmd": "get_state",
    "id": 5,
    "data": {
        "mode": "spectrum",
        "speed": 1.0,
        "brightness": 200,
        "palette_id": 3,
        "uptime_ms": 123456
    }
}
```

## Event Types (Client ← Firmware)

### Status Update
```json
{
    "type": "event",
    "cmd": "status_update",
    "data": {
        "mode": "harmonic",
        "brightness": 180,
        "cpu_load": 45,
        "memory_free": 65536
    }
}
```

### Audio Level
```json
{
    "type": "event",
    "cmd": "audio_level",
    "data": {
        "rms": 15234,
        "peak": 31256,
        "frequency_bands": [100, 150, 200, 180, 120, 90, 45]
    }
}
```

### Beat Detected
```json
{
    "type": "event",
    "cmd": "beat_detected",
    "data": {
        "confidence": 0.85,
        "timestamp_ms": 123456
    }
}
```

### Tempo Updated
```json
{
    "type": "event",
    "cmd": "tempo_update",
    "data": {
        "bpm": 128,
        "confidence": 0.92
    }
}
```

### Connection Ready
```json
{
    "type": "event",
    "cmd": "ready",
    "data": {
        "device_name": "Emotiscope",
        "fw_version": "2.0.0",
        "uptime_ms": 0,
        "capabilities": ["spectrum", "harmonic", "wave", "rhythm_breeze"]
    }
}
```

## Response/Acknowledgment Format

### Command Accepted
```json
{
    "type": "response",
    "cmd": "set_mode",
    "id": 1,
    "data": {
        "success": true,
        "new_mode": "spectrum"
    }
}
```

### Command Rejected
```json
{
    "type": "response",
    "cmd": "set_brightness",
    "id": 3,
    "error": "brightness must be 0-255"
}
```

## Implementation Patterns

### Parsing Commands (Firmware)
```c
#include "cJSON.h"

void handle_websocket_message(const char *json_str) {
    cJSON *json = cJSON_Parse(json_str);
    if (!json) return;

    const char *type = cJSON_GetStringValue(cJSON_GetObjectItem(json, "type"));
    const char *cmd = cJSON_GetStringValue(cJSON_GetObjectItem(json, "cmd"));
    int id = cJSON_GetObjectItem(json, "id")->valueint;

    if (strcmp(type, "command") == 0) {
        handle_command(cmd, id, cJSON_GetObjectItem(json, "data"));
    }

    cJSON_Delete(json);
}

void handle_command(const char *cmd, int id, cJSON *data) {
    if (strcmp(cmd, "set_mode") == 0) {
        const char *mode = cJSON_GetStringValue(cJSON_GetObjectItem(data, "mode"));
        set_visualization_mode(mode);
        send_response(id, cmd, 1, NULL);
    }
    else if (strcmp(cmd, "set_brightness") == 0) {
        int brightness = cJSON_GetObjectItem(data, "brightness")->valueint;
        if (brightness >= 0 && brightness <= 255) {
            set_brightness(brightness);
            send_response(id, cmd, 1, NULL);
        } else {
            send_error(id, cmd, "brightness must be 0-255");
        }
    }
}
```

### Sending Events (Firmware)
```c
void send_event(const char *event_name, const char *json_data) {
    cJSON *msg = cJSON_CreateObject();
    cJSON_AddStringToObject(msg, "type", "event");
    cJSON_AddStringToObject(msg, "cmd", event_name);

    if (json_data) {
        cJSON *data = cJSON_Parse(json_data);
        if (data) {
            cJSON_AddItemToObject(msg, "data", data);
        }
    }

    char *str = cJSON_Print(msg);
    websocket_send(str);
    free(str);
    cJSON_Delete(msg);
}

// Usage
void notify_beat_detected(float confidence) {
    char data[100];
    snprintf(data, sizeof(data), "{\"confidence\": %.2f}", confidence);
    send_event("beat_detected", data);
}
```

### Sending Responses (Firmware)
```c
void send_response(int request_id, const char *cmd, int success, const char *json_data) {
    cJSON *msg = cJSON_CreateObject();
    cJSON_AddStringToObject(msg, "type", "response");
    cJSON_AddStringToObject(msg, "cmd", cmd);
    cJSON_AddNumberToObject(msg, "id", request_id);

    if (success) {
        cJSON *data = cJSON_CreateObject();
        if (json_data) {
            cJSON *parsed = cJSON_Parse(json_data);
            if (parsed) {
                data = parsed;
            }
        }
        cJSON_AddItemToObject(msg, "data", data);
    } else {
        cJSON_AddStringToObject(msg, "error", json_data);
    }

    char *str = cJSON_Print(msg);
    websocket_send(str);
    free(str);
    cJSON_Delete(msg);
}
```

### Receiving Events (Godot/Client)
```gdscript
# Godot GDScript example
extends WebSocketClient

func _ready():
    connect_to_host("ws://emotiscope.local:80/ws")

func _process(delta):
    poll()

func _on_message_received(message: String):
    var json = JSON.new()
    var parsed = json.parse_string(message)

    if parsed == null:
        return

    match parsed["type"]:
        "event":
            handle_event(parsed["cmd"], parsed.get("data", {}))
        "response":
            handle_response(parsed["id"], parsed)

func handle_event(event_name: String, data: Dictionary):
    match event_name:
        "beat_detected":
            flash_ui(data["confidence"])
        "tempo_update":
            update_tempo_display(data["bpm"])
        "audio_level":
            update_spectrum(data["frequency_bands"])

func send_command(cmd: String, data: Dictionary) -> int:
    var msg_id = randi()
    var msg = {
        "type": "command",
        "cmd": cmd,
        "id": msg_id,
        "data": data
    }
    send_text(JSON.stringify(msg))
    return msg_id

# Usage
send_command("set_mode", {"mode": "harmonic"})
```

## Streaming Data (High Frequency Updates)

### Compact Format for Audio Stream
Instead of full JSON for every audio sample, use compact binary or reduced JSON:

```json
{
    "type": "stream",
    "cmd": "audio",
    "data": [100, 150, 200, 180, 120, 90, 45]
}
```

Or base64-encoded binary:
```c
void send_audio_stream(const int16_t *samples, size_t count) {
    // Convert to base64 for compact transmission
    size_t encoded_size = ((count * 2) * 4) / 3 + 4;
    char *encoded = malloc(encoded_size);

    mbedtls_base64_encode((unsigned char *)encoded, encoded_size,
                          &encoded_size,
                          (unsigned char *)samples, count * 2);

    cJSON *msg = cJSON_CreateObject();
    cJSON_AddStringToObject(msg, "type", "stream");
    cJSON_AddStringToObject(msg, "cmd", "audio");
    cJSON_AddStringToObject(msg, "data", encoded);

    char *str = cJSON_Print(msg);
    websocket_send(str);
    free(str);
    cJSON_Delete(msg);
    free(encoded);
}
```

## Error Handling

### Graceful Degradation
```c
void websocket_error_handler(const char *error_msg) {
    ESP_LOGI(TAG, "WebSocket error: %s", error_msg);
    // Firmware continues operating normally
    // Client reconnects automatically
}
```

### Connection Lost Detection
```c
void check_connection_timeout(void) {
    static uint32_t last_heartbeat = 0;

    if (millis() - last_heartbeat > 30000) {  // 30s timeout
        // Connection likely lost
        reconnect_websocket();
        last_heartbeat = millis();
    }
}

void send_heartbeat(void) {
    cJSON *msg = cJSON_CreateObject();
    cJSON_AddStringToObject(msg, "type", "event");
    cJSON_AddStringToObject(msg, "cmd", "heartbeat");

    char *str = cJSON_Print(msg);
    websocket_send(str);
    free(str);
    cJSON_Delete(msg);
}
```

## Performance Considerations

| Aspect | Target | Notes |
|---|---|---|
| Command latency | <50ms | Should respond immediately |
| Event frequency | 10-30Hz | Audio/tempo updates |
| Message size | <1KB | Keep JSON compact |
| Bandwidth | <1Mbps | WiFi easily handles this |
| Queue depth | 50-100 | Buffer for bursty traffic |

## Anti-Patterns

### ❌ WRONG: Blocking WebSocket send
```c
void bad_send(const char *msg) {
    websocket_send_blocking(msg);  // ← Blocks choreography!
}
```

### ✅ CORRECT: Non-blocking queue
```c
void good_send(const char *msg) {
    enqueue_websocket_message(msg);  // ← Returns immediately
}
```

### ❌ WRONG: Parsing without bounds checking
```c
void bad_parse(const char *json) {
    cJSON *data = cJSON_GetObjectItem(root, "data");
    int value = data->valueint;  // ← Crashes if null!
}
```

### ✅ CORRECT: Validate all fields
```c
void good_parse(const char *json) {
    cJSON *data = cJSON_GetObjectItem(root, "data");
    if (!data || data->type != cJSON_Number) return;
    int value = data->valueint;
}
```

## Message Sequence Examples

### User Changes Mode
```
Client                          Firmware
  |                               |
  |--set_mode(spectrum)---------->|
  |                            (process)
  |<--response(success)-----------|
  |                               |
  |<--status_update(spectrum)-----|
```

### Audio Reactive Update
```
Firmware                        Client
  |                               |
  |--beat_detected(0.9)---------->|
  |                            (flash UI)
  |--tempo_update(128 BPM)------->|
  |                            (update BPM)
  |--audio_level([...])---------->|
  |                            (display spectrum)
```

## References

- JSON specification: https://www.json.org/
- WebSocket protocol (RFC 6455): https://datatracker.ietf.org/doc/html/rfc6455
- cJSON library: https://github.com/DaveGamble/cJSON
- Godot WebSocket: https://docs.godotengine.org/en/stable/tutorials/networking/websocket.html
