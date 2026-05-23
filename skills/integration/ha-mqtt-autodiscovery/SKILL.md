---
name: ha-mqtt-autodiscovery
description: |
  Configures and publishes MQTT auto-discovery messages to automatically register IoT devices and
  sensors with Home Assistant, defining discovery payloads with device classes, state classes, units,
  and device grouping for multi-sensor devices. Use when integrating custom IoT devices, creating
  MQTT sensors, building ESP32/ESP8266/Pi-based devices that auto-register with HA, or implementing
  resilient MQTT patterns with offline queuing and auto-reconnect.
---

Works with MQTT brokers (Mosquitto), paho-mqtt Python library, and Home Assistant MQTT integration.
# Home Assistant MQTT Auto-Discovery

Automatically register IoT devices and sensors with Home Assistant by publishing MQTT discovery configurations.

## Overview

MQTT auto-discovery allows devices to automatically appear in Home Assistant without manual YAML configuration. Publish a JSON config to the discovery topic and HA creates the entity automatically.

**Discovery Topic Pattern:**
```
homeassistant/{component}/{node_id}/{object_id}/config
```

**State Topic Pattern:**
```
{node_id}/{sensor_type}/state
```

## When to Use This Skill

Use this skill when you need to:
- Automatically register custom IoT devices with Home Assistant via MQTT
- Build ESP32/ESP8266/Raspberry Pi-based sensors that self-register
- Create multi-sensor devices grouped under a single device entry
- Implement resilient MQTT patterns with offline queuing and auto-reconnect
- Configure proper device classes and state classes for long-term statistics
- Avoid manual YAML configuration for frequently changing device deployments

Do NOT use when:
- You can use existing Home Assistant integrations (prefer official integrations)
- Building devices without MQTT broker infrastructure
- You need real-time control with minimal latency (consider direct API instead)

## Usage

Follow these steps to set up MQTT auto-discovery:

1. **Define sensor configurations** with device classes and units
2. **Publish discovery payloads** to discovery topics with retain=True
3. **Verify entities appear** in Home Assistant
4. **Publish sensor values** to state topics
5. **Implement resilient patterns** with auto-reconnect and offline queuing

## Quick Start

```python
import json
import paho.mqtt.client as mqtt

# Connect to MQTT broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("192.168.68.123", 1883, 60)

# Publish discovery config
discovery_topic = "homeassistant/sensor/enviroplus_temperature/config"
config = {
    "name": "Enviro+ Temperature",
    "unique_id": "enviroplus_temperature",
    "state_topic": "enviroplus/temperature/state",
    "device_class": "temperature",
    "unit_of_measurement": "°C",
    "state_class": "measurement",
    "device": {
        "identifiers": ["enviroplus"],
        "name": "Enviro+ Environmental Sensor",
        "manufacturer": "Pimoroni",
        "model": "Enviro+",
    },
}
client.publish(discovery_topic, json.dumps(config), qos=1, retain=True)

# Publish sensor value
client.publish("enviroplus/temperature/state", "23.5", qos=1)
```

After publishing, the sensor `sensor.enviro_temperature` appears in Home Assistant automatically.

## Discovery Payload Structure

### Required Fields

```python
{
    "name": "Friendly Name",           # Display name in HA
    "unique_id": "unique_identifier",  # Must be globally unique
    "state_topic": "device/sensor/state",  # Topic where values are published
}
```

### Recommended Fields

```python
{
    "device_class": "temperature",     # Semantic type (enables icons, units)
    "unit_of_measurement": "°C",       # Unit for display
    "state_class": "measurement",      # Enables long-term statistics
    "icon": "mdi:thermometer",         # Custom icon (optional)
}
```

### Device Information

Group sensors under a single device:

```python
{
    "device": {
        "identifiers": ["device_unique_id"],  # List of identifiers
        "name": "Device Name",
        "manufacturer": "Manufacturer",
        "model": "Model Name",
        "sw_version": "1.0.0",
    }
}
```

## Common Sensor Types

See [references/sensor_configs.md](references/sensor_configs.md) for complete sensor configuration templates.

### Environmental Sensors

```python
# Temperature
{
    "device_class": "temperature",
    "unit_of_measurement": "°C",
    "state_class": "measurement",
}

# Humidity
{
    "device_class": "humidity",
    "unit_of_measurement": "%",
    "state_class": "measurement",
}

# Pressure
{
    "device_class": "atmospheric_pressure",
    "unit_of_measurement": "hPa",
    "state_class": "measurement",
}

# Light
{
    "device_class": "illuminance",
    "unit_of_measurement": "lx",
    "state_class": "measurement",
}
```

### Air Quality Sensors

```python
# PM2.5
{
    "device_class": "pm25",
    "unit_of_measurement": "µg/m³",
    "state_class": "measurement",
}

# PM10
{
    "device_class": "pm10",
    "unit_of_measurement": "µg/m³",
    "state_class": "measurement",
}
```

### Energy Monitoring

```python
# Power
{
    "device_class": "power",
    "unit_of_measurement": "W",
    "state_class": "measurement",
}

# Energy (cumulative)
{
    "device_class": "energy",
    "unit_of_measurement": "kWh",
    "state_class": "total_increasing",
}
```

## State Classes

| State Class | Purpose | Resets? | Statistics? |
|-------------|---------|---------|-------------|
| `measurement` | Current value (temp, power) | No | Yes (mean, min, max) |
| `total` | Monotonically increasing (odometer) | No | Yes (rate of change) |
| `total_increasing` | Cumulative with resets (daily energy) | Yes | Yes (rate of change) |

## Complete Example: Multi-Sensor Device

```python
import json
import paho.mqtt.client as mqtt

DEVICE_ID = "enviroplus"
BROKER = "192.168.68.123"

# Sensor definitions
SENSORS = {
    "temperature": {
        "name": "Temperature",
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "state_class": "measurement",
    },
    "humidity": {
        "name": "Humidity",
        "device_class": "humidity",
        "unit_of_measurement": "%",
        "state_class": "measurement",
    },
    "pressure": {
        "name": "Pressure",
        "device_class": "atmospheric_pressure",
        "unit_of_measurement": "hPa",
        "state_class": "measurement",
    },
    "pm2_5": {
        "name": "PM2.5",
        "device_class": "pm25",
        "unit_of_measurement": "µg/m³",
        "state_class": "measurement",
    },
}

def publish_discovery(client):
    """Publish discovery configs for all sensors."""
    for sensor_key, config in SENSORS.items():
        unique_id = f"{DEVICE_ID}_{sensor_key}"
        discovery_topic = f"homeassistant/sensor/{unique_id}/config"

        payload = {
            "name": config["name"],
            "unique_id": unique_id,
            "state_topic": f"{DEVICE_ID}/{sensor_key}/state",
            "device_class": config["device_class"],
            "unit_of_measurement": config["unit_of_measurement"],
            "state_class": config["state_class"],
            "device": {
                "identifiers": [DEVICE_ID],
                "name": "Enviro+ Sensor",
                "manufacturer": "Pimoroni",
                "model": "Enviro+",
            },
        }

        client.publish(discovery_topic, json.dumps(payload), qos=1, retain=True)
        print(f"Published discovery for {config['name']}")

# Connect and publish
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, 1883, 60)
publish_discovery(client)

# Publish sample values
client.publish(f"{DEVICE_ID}/temperature/state", "23.5", qos=1)
client.publish(f"{DEVICE_ID}/humidity/state", "65", qos=1)
client.publish(f"{DEVICE_ID}/pressure/state", "1013.25", qos=1)
client.publish(f"{DEVICE_ID}/pm2_5/state", "12.3", qos=1)

client.disconnect()
```

## Resilient MQTT Pattern

For production devices, use auto-reconnect and offline queuing:

```python
from collections import deque
import paho.mqtt.client as mqtt


class ResilientMQTT:
    """MQTT client with offline queuing and auto-reconnect."""

    def __init__(self, broker: str, port: int = 1883):
        self.broker = broker
        self.port = port
        self.connected = False
        self._message_queue = deque(maxlen=1000)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def connect(self):
        """Connect with auto-reconnect enabled."""
        self.client.reconnect_delay_set(min_delay=1, max_delay=60)
        self.client.connect_async(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.connected = True
            self._publish_discovery()  # Re-publish on reconnect
            self._flush_queue()

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        self.connected = False

    def publish(self, topic: str, payload: str, qos: int = 1):
        """Publish with offline queuing."""
        if self.connected:
            self.client.publish(topic, payload, qos=qos)
        else:
            self._message_queue.append({"topic": topic, "payload": payload})

    def _flush_queue(self):
        """Publish queued messages on reconnect."""
        while self._message_queue and self.connected:
            msg = self._message_queue.popleft()
            self.client.publish(msg["topic"], msg["payload"], qos=1)

    def _publish_discovery(self):
        """Re-publish discovery configs on reconnect."""
        # Implement your discovery publishing logic here
        pass
```

See `references/sensor_configs.md` for complete sensor configuration templates, best practices, testing commands, and entity removal procedures.

## Resources

- [references/sensor_configs.md](references/sensor_configs.md) - Complete sensor configuration templates
- [scripts/mqtt_discovery.py](scripts/mqtt_discovery.py) - Multi-sensor discovery publisher
