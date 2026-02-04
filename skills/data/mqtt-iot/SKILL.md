---
name: mqtt-iot
description: Configure MQTT brokers (Mosquitto, EMQX) for IoT messaging, device communication, and smart home integration. Manage topics, QoS levels, authentication, and bridging. Use when setting up IoT messaging, smart home communication, or device-to-cloud connectivity. (project)
---

# MQTT IoT Messaging

Expert guidance for MQTT message broker configuration and IoT communication.

## When to Use This Skill

- Setting up MQTT brokers (Mosquitto, EMQX)
- Designing topic hierarchies
- Configuring authentication and ACLs
- Integrating with Home Assistant
- Building IoT device communication
- Bridging MQTT brokers

## Mosquitto Installation

```yaml
# docker-compose.yml
version: '3.8'
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"   # MQTT
      - "8883:8883"   # MQTT/TLS
      - "9001:9001"   # WebSocket
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    restart: unless-stopped
```

## Mosquitto Configuration

```conf
# mosquitto.conf
listener 1883
protocol mqtt

# WebSocket listener
listener 9001
protocol websockets

# TLS listener
listener 8883
protocol mqtt
cafile /mosquitto/config/certs/ca.crt
certfile /mosquitto/config/certs/server.crt
keyfile /mosquitto/config/certs/server.key
require_certificate false

# Authentication
allow_anonymous false
password_file /mosquitto/config/passwd

# ACL
acl_file /mosquitto/config/acl

# Persistence
persistence true
persistence_location /mosquitto/data/

# Logging
log_dest file /mosquitto/log/mosquitto.log
log_type all

# Connection settings
max_connections -1
max_keepalive 65535

# Message settings
message_size_limit 0
max_inflight_messages 20
max_queued_messages 1000
```

### Password File

```bash
# Create password file
mosquitto_passwd -c /mosquitto/config/passwd user1
mosquitto_passwd /mosquitto/config/passwd user2

# Or create with specific password
mosquitto_passwd -b /mosquitto/config/passwd user1 password123
```

### ACL File

```conf
# /mosquitto/config/acl

# Admin has full access
user admin
topic readwrite #

# User can publish to their own topics
user device1
topic readwrite devices/device1/#
topic read devices/broadcast/#

# Read-only user
user readonly
topic read #

# Pattern-based ACL
pattern readwrite devices/%u/#
pattern read $SYS/#

# Anonymous access (if allow_anonymous true)
topic read public/#
```

## MQTT Topics

### Topic Design Best Practices

```
# Hierarchical structure
home/
  livingroom/
    temperature
    humidity
    motion
    light/
      brightness
      state
  bedroom/
    temperature
    light/
      brightness
      state

# Device-centric
devices/
  sensor-001/
    status
    temperature
    battery
  switch-001/
    state
    command

# Command/State pattern
devices/<device_id>/state      # Device publishes state
devices/<device_id>/command    # Subscribe for commands
devices/<device_id>/config     # Configuration updates
devices/<device_id>/attributes # Device attributes

# Home Assistant compatible
homeassistant/
  sensor/
    <device_id>/
      config       # Auto-discovery
      state        # State updates
  switch/
    <device_id>/
      config
      state
      set          # Commands
```

### Wildcards

```
# Single-level wildcard (+)
home/+/temperature     # Matches home/livingroom/temperature, home/bedroom/temperature

# Multi-level wildcard (#)
home/#                 # Matches all under home/
devices/sensor-001/#   # All topics for sensor-001

# System topics
$SYS/#                 # Broker statistics
$SYS/broker/clients/connected
$SYS/broker/messages/received
```

## CLI Commands

```bash
# Subscribe
mosquitto_sub -h localhost -t "home/#" -v
mosquitto_sub -h localhost -t "devices/+/state" -u user -P password

# Publish
mosquitto_pub -h localhost -t "devices/light/command" -m "ON"
mosquitto_pub -h localhost -t "home/temperature" -m '{"value": 23.5}' -r

# With QoS
mosquitto_sub -h localhost -t "important/#" -q 2
mosquitto_pub -h localhost -t "important/data" -m "data" -q 1

# Retained messages
mosquitto_pub -h localhost -t "config/settings" -m '{"interval": 60}' -r

# Clear retained message
mosquitto_pub -h localhost -t "config/settings" -n -r

# TLS connection
mosquitto_sub -h localhost -p 8883 \
  --cafile ca.crt \
  --cert client.crt \
  --key client.key \
  -t "#"

# WebSocket
mosquitto_sub -h localhost -p 9001 --ws -t "#"
```

## QoS Levels

```
QoS 0 - At most once (fire and forget)
  - No acknowledgment
  - Messages may be lost
  - Use for: Telemetry where occasional loss is acceptable

QoS 1 - At least once
  - Message acknowledged
  - Messages may be duplicated
  - Use for: Most IoT applications

QoS 2 - Exactly once
  - Four-part handshake
  - Guaranteed delivery without duplicates
  - Use for: Critical operations, billing, commands
```

## Home Assistant MQTT Integration

```yaml
# configuration.yaml
mqtt:
  broker: 192.168.1.100
  port: 1883
  username: homeassistant
  password: !secret mqtt_password
  discovery: true
  discovery_prefix: homeassistant

# Manual sensor
mqtt:
  sensor:
    - name: "Living Room Temperature"
      state_topic: "home/livingroom/temperature"
      unit_of_measurement: "°C"
      value_template: "{{ value_json.value }}"
      device_class: temperature

  binary_sensor:
    - name: "Front Door"
      state_topic: "home/entrance/door"
      payload_on: "OPEN"
      payload_off: "CLOSED"
      device_class: door

  switch:
    - name: "Garden Light"
      state_topic: "devices/garden-light/state"
      command_topic: "devices/garden-light/command"
      payload_on: "ON"
      payload_off: "OFF"
      state_on: "ON"
      state_off: "OFF"

  light:
    - name: "Living Room Light"
      schema: json
      state_topic: "home/livingroom/light/state"
      command_topic: "home/livingroom/light/set"
      brightness: true
      color_mode: true
      supported_color_modes: ["brightness"]
```

### MQTT Discovery

```json
// Publish to homeassistant/sensor/temp-001/config
{
  "name": "Temperature Sensor",
  "unique_id": "temp-001",
  "state_topic": "devices/temp-001/state",
  "unit_of_measurement": "°C",
  "device_class": "temperature",
  "value_template": "{{ value_json.temperature }}",
  "device": {
    "identifiers": ["temp-001"],
    "name": "Temperature Sensor",
    "model": "DHT22",
    "manufacturer": "Generic"
  }
}
```

## Bridge Configuration

```conf
# Bridge to cloud broker
connection cloud-bridge
address cloud.example.com:8883
bridge_cafile /mosquitto/config/certs/cloud-ca.crt
bridge_certfile /mosquitto/config/certs/client.crt
bridge_keyfile /mosquitto/config/certs/client.key
remote_username bridge-user
remote_password bridge-password

# Topic mapping
topic devices/# out 1
topic commands/# in 1

# Prefix local topics when sending to remote
topic "" out 1 local/ remote/

# Bridge settings
start_type automatic
cleansession false
notifications true
notification_topic $SYS/broker/bridge/status
try_private true
```

## EMQX Configuration

```yaml
# docker-compose.yml for EMQX
services:
  emqx:
    image: emqx/emqx:5
    ports:
      - "1883:1883"
      - "8083:8083"   # WebSocket
      - "8084:8084"   # WebSocket/TLS
      - "8883:8883"   # MQTT/TLS
      - "18083:18083" # Dashboard
    environment:
      - EMQX_NAME=emqx
      - EMQX_HOST=node1.emqx.io
      - EMQX_DASHBOARD__DEFAULT_PASSWORD=admin123
    volumes:
      - emqx-data:/opt/emqx/data
      - emqx-log:/opt/emqx/log
```

## Python Client Example

```python
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("devices/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.username_pw_set("user", "password")
client.on_connect = on_connect
client.on_message = on_message

# TLS
client.tls_set(ca_certs="ca.crt")

client.connect("localhost", 8883, 60)

# Publish
client.publish("devices/sensor/temperature",
               json.dumps({"value": 23.5}),
               qos=1, retain=True)

client.loop_forever()
```

## Best Practices

1. **Design topic hierarchy** carefully before deployment
2. **Use QoS 1** for most IoT applications
3. **Implement authentication** (never allow anonymous in production)
4. **Use TLS** for encrypted communication
5. **Use retained messages** for current state
6. **Keep payloads small** for efficiency
7. **Use JSON** for structured data
8. **Implement Last Will and Testament** for device status
9. **Monitor broker metrics** ($SYS topics)
10. **Plan for scalability** with clustering/bridging
