---
name: mqtt-diagnosis
description: Diagnose MQTT publishing issues between CaptureLora.py and mqtt_grid_web.py. Check topic distribution, connection stability, and cross-reference with web app logs. Use when messages aren't reaching the web interface.
---

# MQTT Diagnosis

Investigate why MQTT messages may not be reaching the web interface.

## Step 1: MQTT Publish Success Rate

Count in `logs/IQRight_Daemon.debug`:
- Pattern `MQTT-TX.*SUCCESS` = successful publishes
- Pattern `MQTT-TX.*FAILED` = failed publishes

Calculate success rate. Baseline: >95% is healthy.

## Step 2: Topic Distribution

Search for all `Topic=` values in MQTT-TX lines. Extract and count unique topics.

**Correct topics**:
- `Class{number}` (e.g., `Class96`, `Class89`) = student data routed to teacher's class
- `IQRSend` = commands (break/release/cleanup)

**Malformed topics (known bugs)**:
- `Class['cmd', 'ack', 'break']` = BUG-001, command list stringified as topic suffix (FIXED Feb 2026)
- `Classcmd|ack|cleanup}` = raw payload leaking into topic name (FIXED Feb 2026)

If malformed topics found: the server code needs updating to the latest version.

## Step 3: Connection Stability

Search for `Connected to MQTT` and `Disconnected from MQTT` patterns.

Analyze:
- Connect/disconnect ratio (healthy: few disconnects)
- Clustering (many rapid reconnects = broker unstable)
- Gaps between disconnect and reconnect (long gaps = extended outage)

## Step 4: MQTT Error Codes

Search for `MQTT-TX.*FAILED` and extract `Status=` values.
- **Status 7** = `MQTT_ERR_CONN_LOST` (most common, broker connection dropped)
- Check if retries succeeded (same payload, later SUCCESS)

## Step 5: Cross-Reference with Web App Logs

If server-side MQTT publishing looks healthy, the problem is downstream. Check:

1. Does `logs/IQRight_FE_WEB.debug` exist?
2. Search for `[MQTT-RX]` = messages received by web app
3. Search for `[MQTT-SUB]` = subscription confirmations
4. Search for `[SOCKETIO-TX]` = data emitted to browser
5. Search for `[MQTT-CONN]` = web app MQTT connection status

**Key question**: Is the web app subscribed to the same topics the server publishes to?
- Server publishes to: `Class{hierarchyID}` (e.g., `Class96`)
- Web app subscribes to: `{TOPIC_PREFIX}{classCode}` (e.g., `Class96`)
- These MUST match for data to flow through

## Diagnosis Flow

```
Server MQTT-TX SUCCESS > 95%?
  NO  -> Broker connection issue
         Check: mosquitto service running?
         Check: reconnection pattern in logs
  YES -> Topics correct? (Class{NN}, IQRSend)
           NO  -> Malformed topic bug (update code)
           YES -> Check web app logs (Step 5)
                    Web MQTT-RX present?
                      NO  -> Web app not subscribing / not connected
                      YES -> Check SOCKETIO-TX
                               NO  -> SocketIO emit bug
                               YES -> Check browser console for JS errors
```

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` section 2 (Stage 4) and section 5 (BUG-001).