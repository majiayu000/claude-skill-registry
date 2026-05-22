---
name: iot-developer
description: Expert in IoT development, microcontrollers, sensors, and MQTT protocols
version: 1.0.0
tags: [iot, mqtt, arduino, raspberry-pi, sensors, esp32]
---

# IoT Developer Skill

I help you build IoT applications, connect sensors and devices, and create smart home/industrial IoT solutions.

## What I Do

**Device Integration:**

- Microcontroller programming (Arduino, ESP32)
- Sensor reading and data collection
- Actuator control (motors, LEDs, relays)
- Hardware interfacing

**Communication:**

- MQTT messaging
- WebSocket connections
- REST API integration
- Bluetooth/WiFi connectivity

**IoT Platforms:**

- Real-time dashboards
- Device management
- Data logging
- Alerts and automation

## MQTT Basics (Web Client)

```bash
npm install mqtt
```

```typescript
// lib/mqtt-client.ts
import mqtt from 'mqtt'

export class MQTTClient {
  private client: mqtt.MqttClient

  constructor(brokerUrl: string) {
    this.client = mqtt.connect(brokerUrl, {
      clientId: `web_${Math.random().toString(16).slice(3)}`,
      clean: true,
      connectTimeout: 4000
    })

    this.client.on('connect', () => {
      console.log('MQTT connected')
    })

    this.client.on('error', error => {
      console.error('MQTT error:', error)
    })
  }

  subscribe(topic: string, callback: (message: string) => void) {
    this.client.subscribe(topic, err => {
      if (err) console.error('Subscribe error:', err)
    })

    this.client.on('message', (receivedTopic, message) => {
      if (receivedTopic === topic) {
        callback(message.toString())
      }
    })
  }

  publish(topic: string, message: string) {
    this.client.publish(topic, message)
  }

  disconnect() {
    this.client.end()
  }
}
```

**Usage:**

```typescript
'use client'
import { useEffect, useState } from 'react'
import { MQTTClient } from '@/lib/mqtt-client'

export function TemperatureDashboard() {
  const [temperature, setTemperature] = useState(0)
  const [humidity, setHumidity] = useState(0)

  useEffect(() => {
    const mqtt = new MQTTClient('ws://broker.hivemq.com:8000/mqtt')

    mqtt.subscribe('home/temperature', (msg) => {
      setTemperature(parseFloat(msg))
    })

    mqtt.subscribe('home/humidity', (msg) => {
      setHumidity(parseFloat(msg))
    })

    return () => mqtt.disconnect()
  }, [])

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="p-6 bg-white rounded-lg shadow">
        <h3 className="text-gray-600">Temperature</h3>
        <p className="text-4xl font-bold">{temperature}°C</p>
      </div>

      <div className="p-6 bg-white rounded-lg shadow">
        <h3 className="text-gray-600">Humidity</h3>
        <p className="text-4xl font-bold">{humidity}%</p>
      </div>
    </div>
  )
}
```

---

## Arduino/ESP32 Code

### Temperature Sensor (DHT22)

```cpp
// ESP32 + DHT22 Temperature/Humidity Sensor
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Connect to MQTT
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Publish to MQTT
  if (!isnan(temperature)) {
    client.publish("home/temperature", String(temperature).c_str());
  }

  if (!isnan(humidity)) {
    client.publish("home/humidity", String(humidity).c_str());
  }

  delay(5000); // Publish every 5 seconds
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      Serial.println("MQTT connected");
    } else {
      delay(5000);
    }
  }
}
```

---

## Smart Home Dashboard

```typescript
'use client'
import { useEffect, useState } from 'react'
import { MQTTClient } from '@/lib/mqtt-client'

interface Device {
  id: string
  name: string
  type: 'light' | 'sensor' | 'thermostat'
  status: string | number
}

export function SmartHomeDashboard() {
  const [devices, setDevices] = useState<Device[]>([
    { id: '1', name: 'Living Room Light', type: 'light', status: 'off' },
    { id: '2', name: 'Temperature', type: 'sensor', status: 22 },
    { id: '3', name: 'Thermostat', type: 'thermostat', status: 20 }
  ])

  const [mqtt, setMqtt] = useState<MQTTClient | null>(null)

  useEffect(() => {
    const client = new MQTTClient('ws://broker.hivemq.com:8000/mqtt')

    // Subscribe to device topics
    client.subscribe('home/light/1', (msg) => {
      updateDevice('1', msg)
    })

    client.subscribe('home/temperature', (msg) => {
      updateDevice('2', parseFloat(msg))
    })

    setMqtt(client)

    return () => client.disconnect()
  }, [])

  const updateDevice = (id: string, status: string | number) => {
    setDevices(prev => prev.map(device =>
      device.id === id ? { ...device, status } : device
    ))
  }

  const toggleLight = (id: string) => {
    const device = devices.find(d => d.id === id)
    if (device && mqtt) {
      const newStatus = device.status === 'on' ? 'off' : 'on'
      mqtt.publish(`home/light/${id}`, newStatus)
      updateDevice(id, newStatus)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Smart Home</h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {devices.map((device) => (
          <div key={device.id} className="p-6 bg-white rounded-lg shadow">
            <h3 className="font-semibold mb-2">{device.name}</h3>

            {device.type === 'light' && (
              <button
                onClick={() => toggleLight(device.id)}
                className={`px-4 py-2 rounded ${
                  device.status === 'on'
                    ? 'bg-yellow-400 text-black'
                    : 'bg-gray-300'
                }`}
              >
                {device.status === 'on' ? '💡 ON' : '🌑 OFF'}
              </button>
            )}

            {device.type === 'sensor' && (
              <p className="text-2xl font-bold">{device.status}°C</p>
            )}

            {device.type === 'thermostat' && (
              <div>
                <p className="text-xl">Target: {device.status}°C</p>
                <div className="flex gap-2 mt-2">
                  <button className="px-3 py-1 bg-blue-600 text-white rounded">
                    -
                  </button>
                  <button className="px-3 py-1 bg-blue-600 text-white rounded">
                    +
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## WebSocket Real-Time Sensor Data

```typescript
// app/api/sensor-stream/route.ts
export async function GET(req: Request) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    start(controller) {
      const interval = setInterval(async () => {
        // Simulate sensor data (or read from actual IoT device)
        const temperature = 20 + Math.random() * 10
        const humidity = 40 + Math.random() * 20

        const data = `data: ${JSON.stringify({
          temperature,
          humidity,
          timestamp: new Date().toISOString()
        })}\n\n`

        controller.enqueue(encoder.encode(data))
      }, 1000)

      req.signal.addEventListener('abort', () => {
        clearInterval(interval)
        controller.close()
      })
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive'
    }
  })
}
```

---

## When to Use Me

**Perfect for:**

- Building smart home systems
- Creating industrial IoT solutions
- Implementing sensor networks
- Developing device dashboards
- Automating physical processes

**I'll help you:**

- Connect IoT devices
- Implement MQTT protocols
- Read sensor data
- Build real-time dashboards
- Control actuators

## What I'll Create

```
🌡️ Sensor Integration
💡 Smart Device Control
📊 IoT Dashboards
📡 MQTT Communication
🏠 Smart Home Systems
🏭 Industrial IoT
```

Let's connect the physical and digital worlds!
