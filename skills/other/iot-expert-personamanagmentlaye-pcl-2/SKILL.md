---
name: iot-expert
version: 1.0.0
description: Expert-level IoT systems, embedded devices, edge computing, and IoT protocols
category: domains
tags: [iot, embedded, edge-computing, mqtt, sensors, firmware]
allowed-tools:
  - Read
  - Write
  - Edit
---

# IoT Expert

Expert guidance for IoT systems, embedded devices, edge computing, sensor networks, and IoT protocols.

## Core Concepts

### IoT Architecture
- Device layer (sensors, actuators)
- Edge computing layer
- Network layer (connectivity)
- Cloud/platform layer
- Application layer
- Security across all layers

### IoT Protocols
- MQTT (Message Queuing Telemetry Transport)
- CoAP (Constrained Application Protocol)
- HTTP/REST for IoT
- WebSocket for real-time
- LoRaWAN for long-range
- Zigbee, Z-Wave for home automation

### Embedded Systems
- Microcontroller programming
- Real-time operating systems (RTOS)
- Power management
- Firmware updates (OTA)
- Hardware interfaces (I2C, SPI, UART)
- Memory constraints

## MQTT Implementation

```python
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from typing import Callable, Dict

class MQTTClient:
    def __init__(self, broker: str, port: int = 1883, client_id: str = "iot_device"):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id)
        self.subscriptions: Dict[str, Callable] = {}

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
            # Resubscribe to topics on reconnect
            for topic in self.subscriptions.keys():
                self.client.subscribe(topic)
        else:
            print(f"Connection failed with code {rc}")

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic in self.subscriptions:
            try:
                data = json.loads(payload)
                self.subscriptions[topic](data)
            except json.JSONDecodeError:
                self.subscriptions[topic](payload)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"Unexpected disconnect. Reconnecting...")

    def connect(self, username: str = None, password: str = None):
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def publish(self, topic: str, payload: Dict, qos: int = 1, retain: bool = False):
        """Publish message to MQTT topic"""
        message = json.dumps(payload)
        result = self.client.publish(topic, message, qos=qos, retain=retain)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def subscribe(self, topic: str, callback: Callable, qos: int = 1):
        """Subscribe to MQTT topic with callback"""
        self.subscriptions[topic] = callback
        self.client.subscribe(topic, qos=qos)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

# IoT Device Example
class TemperatureSensor:
    def __init__(self, device_id: str, mqtt_client: MQTTClient):
        self.device_id = device_id
        self.mqtt = mqtt_client
        self.topic = f"sensors/temperature/{device_id}"

    def read_temperature(self) -> float:
        # In real device, read from actual sensor
        import random
        return round(random.uniform(20.0, 30.0), 2)

    def publish_reading(self):
        temperature = self.read_temperature()

        payload = {
            "device_id": self.device_id,
            "temperature": temperature,
            "unit": "celsius",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.mqtt.publish(self.topic, payload)
        return payload
```

## Embedded C for Microcontroller

```c
// Arduino/ESP32 Example
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22

const char* ssid = "YourWiFiSSID";
const char* password = "YourPassword";
const char* mqtt_server = "broker.example.com";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
    delay(10);
    Serial.println("Connecting to WiFi...");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");

    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");

        if (client.connect("ESP32Client")) {
            Serial.println("connected");
            client.subscribe("device/control");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    dht.begin();
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    // Read sensor every 10 seconds
    static unsigned long lastRead = 0;
    if (millis() - lastRead > 10000) {
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        if (!isnan(humidity) && !isnan(temperature)) {
            char msg[100];
            snprintf(msg, sizeof(msg),
                    "{\"temperature\":%.2f,\"humidity\":%.2f}",
                    temperature, humidity);

            client.publish("sensors/data", msg);
            Serial.println(msg);
        }

        lastRead = millis();
    }
}
```

## Edge Computing

```python
import asyncio
from typing import Dict, List
import numpy as np

class EdgeProcessor:
    """Process data at edge before sending to cloud"""

    def __init__(self, buffer_size: int = 100):
        self.buffer: List[Dict] = []
        self.buffer_size = buffer_size

    def add_reading(self, reading: Dict):
        """Add sensor reading to buffer"""
        self.buffer.append(reading)

        if len(self.buffer) >= self.buffer_size:
            self.process_buffer()

    def process_buffer(self) -> Dict:
        """Process buffered data at edge"""
        if not self.buffer:
            return {}

        # Extract temperature values
        temperatures = [r['temperature'] for r in self.buffer]

        # Compute statistics at edge
        summary = {
            "count": len(temperatures),
            "mean": np.mean(temperatures),
            "std": np.std(temperatures),
            "min": np.min(temperatures),
            "max": np.max(temperatures),
            "anomalies": self.detect_anomalies(temperatures)
        }

        # Clear buffer
        self.buffer = []

        return summary

    def detect_anomalies(self, values: List[float]) -> List[int]:
        """Detect anomalies using simple threshold"""
        mean = np.mean(values)
        std = np.std(values)
        threshold = 2.5

        anomalies = []
        for i, v in enumerate(values):
            if abs(v - mean) > threshold * std:
                anomalies.append(i)

        return anomalies

class IoTPipeline:
    """Complete IoT data pipeline"""

    def __init__(self, mqtt_client: MQTTClient):
        self.mqtt = mqtt_client
        self.edge_processor = EdgeProcessor()
        self.devices: Dict[str, TemperatureSensor] = {}

    def register_device(self, device: TemperatureSensor):
        """Register IoT device"""
        self.devices[device.device_id] = device

        # Subscribe to device topic
        topic = f"sensors/temperature/{device.device_id}"
        self.mqtt.subscribe(topic, self.handle_device_data)

    def handle_device_data(self, data: Dict):
        """Handle incoming device data"""
        # Process at edge
        self.edge_processor.add_reading(data)

    async def collect_data_loop(self, interval: int = 5):
        """Continuous data collection from devices"""
        while True:
            for device in self.devices.values():
                reading = device.publish_reading()
                print(f"Device {device.device_id}: {reading['temperature']}°C")

            await asyncio.sleep(interval)
```

## Device Management

```python
from datetime import datetime
from enum import Enum

class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class IoTDevice:
    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type
        self.status = DeviceStatus.OFFLINE
        self.last_seen = None
        self.firmware_version = "1.0.0"
        self.metadata = {}

    def update_status(self, status: DeviceStatus):
        self.status = status
        self.last_seen = datetime.utcnow()

    def needs_firmware_update(self, latest_version: str) -> bool:
        return self.firmware_version < latest_version

class DeviceManager:
    def __init__(self):
        self.devices: Dict[str, IoTDevice] = {}

    def register_device(self, device: IoTDevice):
        """Register new device"""
        self.devices[device.device_id] = device

    def update_device_heartbeat(self, device_id: str):
        """Update device last seen timestamp"""
        if device_id in self.devices:
            self.devices[device_id].update_status(DeviceStatus.ONLINE)

    def get_offline_devices(self, timeout_seconds: int = 300) -> List[IoTDevice]:
        """Get devices that haven't reported recently"""
        offline = []
        now = datetime.utcnow()

        for device in self.devices.values():
            if device.last_seen:
                elapsed = (now - device.last_seen).total_seconds()
                if elapsed > timeout_seconds:
                    offline.append(device)

        return offline

    def schedule_firmware_update(self, device_id: str, new_version: str):
        """Schedule OTA firmware update"""
        if device_id in self.devices:
            # Send update command via MQTT
            payload = {
                "command": "firmware_update",
                "version": new_version,
                "url": f"https://updates.example.com/{new_version}.bin"
            }
            return payload
```

## Best Practices

### Device Design
- Implement power management for battery devices
- Use deep sleep modes when idle
- Handle network disconnections gracefully
- Implement watchdog timers
- Design for remote diagnostics
- Plan for firmware updates (OTA)

### Security
- Use TLS/SSL for MQTT connections
- Implement device authentication
- Encrypt sensitive data
- Secure firmware updates
- Regular security patches
- Network segmentation

### Data Management
- Process data at edge when possible
- Implement data buffering for offline scenarios
- Use efficient data formats (e.g., Protocol Buffers)
- Compress data before transmission
- Handle time synchronization
- Implement data retention policies

## Anti-Patterns

❌ No power management strategy
❌ Unencrypted communications
❌ No error handling for network failures
❌ Sending all raw data to cloud
❌ No device authentication
❌ Hard-coded credentials in firmware
❌ No OTA update mechanism

## Resources

- MQTT: https://mqtt.org/
- ESP32 Documentation: https://docs.espressif.com/
- Arduino: https://www.arduino.cc/
- AWS IoT: https://aws.amazon.com/iot/
- Azure IoT: https://azure.microsoft.com/en-us/overview/iot/
