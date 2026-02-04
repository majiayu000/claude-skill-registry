---
name: esphome-devices
description: Create and configure ESPHome devices for DIY smart home sensors and actuators. Write YAML configurations for ESP8266/ESP32 boards, sensors, displays, and automations. Use when building custom IoT devices, flashing ESPHome firmware, or integrating with Home Assistant. (project)
---

# ESPHome Devices

Expert guidance for ESPHome DIY smart home devices.

## When to Use This Skill

- Creating custom ESP8266/ESP32 devices
- Configuring sensors (temperature, motion, etc.)
- Building smart switches and relays
- Creating LED controllers
- Setting up displays and notifications
- Integrating with Home Assistant

## Installation & Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  esphome:
    image: esphome/esphome
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
    network_mode: host
    restart: unless-stopped
```

```bash
# CLI installation
pip install esphome

# Create new device
esphome wizard my_device.yaml

# Compile and upload
esphome run my_device.yaml

# Just compile
esphome compile my_device.yaml

# OTA upload
esphome upload my_device.yaml --device 192.168.1.100

# View logs
esphome logs my_device.yaml
```

## Basic Configuration

```yaml
# my_device.yaml
esphome:
  name: my-device
  friendly_name: My Device
  platform: ESP8266  # or ESP32
  board: nodemcuv2   # or esp32dev, d1_mini, etc.

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Optional: Static IP
  manual_ip:
    static_ip: 192.168.1.100
    gateway: 192.168.1.1
    subnet: 255.255.255.0

  # Fallback AP
  ap:
    ssid: "My-Device Fallback"
    password: "fallback123"

captive_portal:

# Enable logging
logger:
  level: DEBUG

# Enable Home Assistant API
api:
  encryption:
    key: !secret api_encryption_key

# Enable OTA updates
ota:
  password: !secret ota_password

# Web server (optional)
web_server:
  port: 80
```

### Secrets File

```yaml
# secrets.yaml
wifi_ssid: "MyWiFi"
wifi_password: "password123"
api_encryption_key: "generated-key-here"
ota_password: "ota-password"
```

## Common Sensors

### Temperature & Humidity (DHT22)

```yaml
sensor:
  - platform: dht
    pin: D2
    model: DHT22
    temperature:
      name: "Temperature"
      filters:
        - offset: -0.5  # Calibration
    humidity:
      name: "Humidity"
    update_interval: 60s
```

### Temperature (Dallas DS18B20)

```yaml
dallas:
  - pin: D4

sensor:
  - platform: dallas
    address: 0x1234567890ABCDEF
    name: "Temperature"
    resolution: 12
```

### BME280 (I2C)

```yaml
i2c:
  sda: D2
  scl: D1
  scan: true

sensor:
  - platform: bme280
    temperature:
      name: "Temperature"
      oversampling: 16x
    pressure:
      name: "Pressure"
    humidity:
      name: "Humidity"
    address: 0x76
    update_interval: 60s
```

### Motion Sensor (PIR)

```yaml
binary_sensor:
  - platform: gpio
    pin: D5
    name: "Motion"
    device_class: motion
    filters:
      - delayed_off: 30s
```

### Door/Window Sensor

```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: D1
      mode: INPUT_PULLUP
      inverted: true
    name: "Door"
    device_class: door
```

### Light Sensor (BH1750)

```yaml
sensor:
  - platform: bh1750
    name: "Illuminance"
    address: 0x23
    update_interval: 60s
```

### Analog Sensor

```yaml
sensor:
  - platform: adc
    pin: A0
    name: "Soil Moisture"
    update_interval: 60s
    unit_of_measurement: "%"
    filters:
      - calibrate_linear:
          - 0.85 -> 0.0
          - 0.35 -> 100.0
```

## Switches & Relays

### Basic Relay

```yaml
switch:
  - platform: gpio
    pin: D1
    name: "Relay"
    id: relay1
    restore_mode: RESTORE_DEFAULT_OFF
```

### Button-Controlled Relay

```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: D2
      mode: INPUT_PULLUP
      inverted: true
    name: "Button"
    on_press:
      - switch.toggle: relay1

switch:
  - platform: gpio
    pin: D1
    name: "Relay"
    id: relay1
```

### Sonoff Basic

```yaml
esphome:
  name: sonoff-basic
  platform: ESP8266
  board: esp01_1m

binary_sensor:
  - platform: gpio
    pin:
      number: GPIO0
      mode: INPUT_PULLUP
      inverted: true
    name: "Button"
    on_press:
      - switch.toggle: relay

  - platform: status
    name: "Status"

switch:
  - platform: gpio
    pin: GPIO12
    name: "Relay"
    id: relay

status_led:
  pin:
    number: GPIO13
    inverted: true
```

## Lights & LEDs

### PWM LED

```yaml
output:
  - platform: esp8266_pwm
    pin: D1
    id: led_output

light:
  - platform: monochromatic
    name: "LED"
    output: led_output
    gamma_correct: 2.8
```

### RGB LED Strip (WS2812B)

```yaml
light:
  - platform: fastled_clockless
    chipset: WS2812B
    pin: D4
    num_leds: 60
    rgb_order: GRB
    name: "LED Strip"
    effects:
      - random:
      - pulse:
      - strobe:
      - flicker:
      - addressable_rainbow:
      - addressable_color_wipe:
      - addressable_scan:
      - addressable_fireworks:
```

### RGBW LED

```yaml
output:
  - platform: esp8266_pwm
    pin: D1
    id: red
  - platform: esp8266_pwm
    pin: D2
    id: green
  - platform: esp8266_pwm
    pin: D3
    id: blue
  - platform: esp8266_pwm
    pin: D4
    id: white

light:
  - platform: rgbw
    name: "RGBW Light"
    red: red
    green: green
    blue: blue
    white: white
```

## Displays

### OLED Display (SSD1306)

```yaml
i2c:
  sda: D2
  scl: D1

font:
  - file: "fonts/arial.ttf"
    id: font1
    size: 14

display:
  - platform: ssd1306_i2c
    model: "SSD1306 128x64"
    address: 0x3C
    lambda: |-
      it.printf(0, 0, id(font1), "Temp: %.1f°C", id(temperature).state);
      it.printf(0, 20, id(font1), "Humidity: %.1f%%", id(humidity).state);
```

### E-Paper Display

```yaml
spi:
  clk_pin: D5
  mosi_pin: D7

display:
  - platform: waveshare_epaper
    cs_pin: D8
    dc_pin: D1
    busy_pin: D2
    reset_pin: D0
    model: 2.90in
    lambda: |-
      it.print(0, 0, id(font1), "Hello World!");
```

## Automations

```yaml
# Time-based automation
time:
  - platform: homeassistant
    id: homeassistant_time
    on_time:
      - seconds: 0
        minutes: 0
        hours: 7
        then:
          - light.turn_on: led

# State-based automation
binary_sensor:
  - platform: gpio
    pin: D5
    name: "Motion"
    on_press:
      then:
        - light.turn_on:
            id: led
            brightness: 100%
            transition_length: 1s
    on_release:
      then:
        - delay: 5min
        - light.turn_off:
            id: led
            transition_length: 2s

# Template automation
interval:
  - interval: 1min
    then:
      - if:
          condition:
            sensor.in_range:
              id: temperature
              above: 25
          then:
            - switch.turn_on: fan
          else:
            - switch.turn_off: fan
```

## ESP32 Bluetooth

### BLE Presence Detection

```yaml
esp32_ble_tracker:
  scan_parameters:
    interval: 1100ms
    window: 1100ms
    active: true

binary_sensor:
  - platform: ble_presence
    mac_address: AA:BB:CC:DD:EE:FF
    name: "Phone Present"
```

### Xiaomi Sensors

```yaml
esp32_ble_tracker:

sensor:
  - platform: xiaomi_lywsd03mmc
    mac_address: "A4:C1:38:XX:XX:XX"
    bindkey: "your-bind-key"
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    battery_level:
      name: "Battery"
```

## Best Practices

1. **Use secrets.yaml** for sensitive data
2. **Set static IPs** for reliability
3. **Enable fallback AP** for recovery
4. **Use meaningful names** for HA integration
5. **Add filters** for sensor smoothing
6. **Enable OTA** for remote updates
7. **Test with logs** before deploying
8. **Use restore_mode** for switches
9. **Add status LED** for debugging
10. **Document pin assignments**

## Troubleshooting

```yaml
# Enable verbose logging
logger:
  level: VERBOSE

# Check WiFi signal
sensor:
  - platform: wifi_signal
    name: "WiFi Signal"
    update_interval: 60s

# Restart button
button:
  - platform: restart
    name: "Restart"

# Safe mode
button:
  - platform: safe_mode
    name: "Safe Mode"
```
