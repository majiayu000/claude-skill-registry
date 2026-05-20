---
name: mqtt
cluster: iot
description: "Lightweight pub/sub protocol for efficient IoT communication and telemetry"
tags: ["iot","mqtt"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "mqtt iot"
---

# mqtt

## Purpose
This skill allows the AI to interact with MQTT, a lightweight pub/sub protocol, for efficient IoT communication. Use it to publish telemetry data or subscribe to device updates, enabling real-time interactions in constrained environments.

## When to Use
Use this skill for scenarios requiring low-bandwidth, real-time messaging, such as sending sensor data from IoT devices, remote device control, or telemetry monitoring. Avoid it for high-throughput needs like file transfers, where HTTP is more suitable.

## Key Capabilities
- Publish messages to topics with configurable Quality of Service (QoS) levels (0, 1, or 2).
- Subscribe to topics and handle incoming messages asynchronously.
- Support for retained messages, last will and testament, and wildcard subscriptions (e.g., "#" for all subtopics).
- Secure connections via TLS and authentication methods like username/password.

## Usage Patterns
To use MQTT, first connect to a broker using a client library. Establish a connection with credentials, then publish or subscribe. For example, in a loop: connect, subscribe, process messages, and disconnect. Use environment variables for sensitive data, like `$MQTT_BROKER_URL` for the broker address. Always handle reconnections for unstable networks.

## Common Commands/API
Use the Paho MQTT library for Python interactions. Import it as follows:

```python
import paho.mqtt.client as mqtt
```

To connect to a broker:
- Command: `client.connect(broker_address, port=1883)`
- Example with auth: `client.username_pw_set(username='$MQTT_USERNAME', password='$MQTT_PASSWORD')`

To publish a message:
- API: `client.publish(topic, payload, qos=1)`
- Example: `client.publish('sensors/temp', '22.5', qos=1)`

To subscribe:
- API: `client.subscribe(topic, qos=1)`
- Example: `client.subscribe('commands/device1', qos=1)`

Config format: Use a JSON file for settings, e.g., `{"broker": "$MQTT_BROKER_URL", "topic": "sensors/temp"}`. CLI tools like `mosquitto_pub` can be invoked via subprocess: `subprocess.run(['mosquitto_pub', '-h', '$MQTT_BROKER_URL', '-t', 'sensors/temp', '-m', '22.5'])`.

## Integration Notes
Integrate MQTT by wrapping it in your AI agent's code. Set environment variables for keys, e.g., export `$MQTT_API_KEY` for token-based auth. For multi-service setups, use a broker like HiveMQ or Mosquitto; connect via `client.connect('$MQTT_BROKER_URL')`. Ensure TLS for secure endpoints (e.g., `client.tls_set()`). If combining with other skills, like a database, publish data on success: e.g., after inserting into a DB, run `client.publish('db/updates', json.dumps(data))`.

## Error Handling
Handle common errors explicitly. For connection issues, catch `ConnectionRefusedError` and retry with exponential backoff: e.g., `time.sleep(5)`. For publish failures, check return codes (e.g., if `client.publish()` returns >0, log and retry). Subscription errors might involve invalid topics; validate with `if '/' not in topic: raise ValueError('Invalid topic')`. Use callbacks for message errors, like in `on_message` handler: `if error: print('Error: ', error)`. Always clean up with `client.disconnect()` in a finally block.

## Concrete Usage Examples
**Example 1: Publish sensor data**
To publish a temperature reading to an MQTT topic, first set env vars: `export MQTT_BROKER_URL='broker.example.com'`. Then, in code:
```python
client = mqtt.Client()
client.connect(os.environ['MQTT_BROKER_URL'])
client.publish('sensors/temperature', '25.0', qos=1)
client.disconnect()
```
This sends a message to the broker for IoT dashboard updates.

**Example 2: Subscribe to device commands**
To subscribe and react to commands, use:
```python
def on_message(client, userdata, message):
    print(f"Received: {message.payload.decode()}")
client = mqtt.Client()
client.on_message = on_message
client.connect(os.environ['MQTT_BROKER_URL'])
client.subscribe('commands/device1', qos=1)
client.loop_forever()
```
This keeps the client listening for commands to control an IoT device.

## Graph Relationships
- Related to cluster: iot
- Related to tags: iot, mqtt
- Connections: Can integrate with other iot skills, such as for data processing or device management.
