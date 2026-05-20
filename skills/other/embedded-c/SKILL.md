---
name: embedded-c
cluster: iot
description: "C/C++ for embedded systems: microcontrollers, IoT, resource optimization"
tags: ["iot","embedded"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "embedded-c iot"
---

# embedded-c

## Purpose
This skill provides expertise in C/C++ programming for embedded systems, focusing on microcontrollers (e.g., Arduino, STM32) and IoT devices, emphasizing resource optimization like low memory usage and power efficiency.

## When to Use
Use this skill for developing firmware, handling hardware interactions (e.g., sensors, actuators), or optimizing code for constrained environments. Apply it when building IoT prototypes, debugging real-time systems, or integrating with hardware like ESP8266 for wireless connectivity.

## Key Capabilities
- Generate C/C++ code for GPIO control, timers, and interrupts, e.g., setting up a PWM signal on a microcontroller.
- Optimize code for resource constraints, such as reducing stack usage or minimizing flash memory footprint.
- Handle communication protocols like I2C, SPI, or UART in embedded contexts.
- Provide best practices for error-free coding in low-level environments, including volatile keyword usage for hardware registers.

## Usage Patterns
Prompt the AI with specific, actionable requests: "Write a C function to read temperature from an LM35 sensor on an AVR microcontroller." Structure prompts to include hardware details, e.g., "For ESP32, generate code to connect to WiFi and send HTTP requests." Always specify optimization goals, like "Ensure the code uses less than 1KB of RAM." Chain prompts for iterative development: first, generate code; then, refine for bugs.

## Common Commands/API
Use GCC for compilation with flags like `-Os` for optimization and `-mmcu=atmega328p` for AVR targets. For API examples:
- Include headers: `#include <avr/io.h>` for AVR microcontrollers.
- Code snippet for blinking an LED:
  ```
  DDRB |= (1 << PB5);  // Set PB5 as output
  while(1) { PORTB ^= (1 << PB5); _delay_ms(1000); }
  ```
- For IoT, use ESP-IDF API: `esp_wifi_init(&config);` to initialize Wi-Fi.
- Config formats: JSON for IoT device configs, e.g., `{"ssid": "myNetwork", "password": "$WIFI_PASSWORD"}`, loaded via `nvs_set_str()` in ESP32 code.
- If API keys are needed (e.g., for cloud services), set env vars like `$AWS_IOT_KEY` and access via `getenv("AWS_IOT_KEY")` in code.

## Integration Notes
Integrate this skill with development tools by setting up environments: Install GCC and tools like avrdude for flashing. For IoT, use PlatformIO or Arduino IDE. Authenticate with services using env vars, e.g., export `$AZURE_IOT_HUB_KEY` for Azure integration. Link code with libraries via `#pragma once` guards or CMake for cross-compilation. Test on emulators like QEMU for ARM before hardware deployment. Ensure compatibility by specifying board types in prompts, e.g., "Adapt this code for STM32F4."

## Error Handling
Always check return values in embedded code, e.g., if (`i2c_read() != 0`) { handle_error(); }. Use asserts for debugging: `#include <assert.h>` and `assert(pin >= 0);`. For C++, catch exceptions in main loops: try { setup_hardware(); } catch (...) { reset_device(); }. Handle hardware failures by implementing watchdogs, e.g., `wdt_enable(WDTO_8S);` in AVR. Log errors via UART: printf("Error: Sensor timeout\n"); and use finite state machines to recover from faults.

## Concrete Usage Examples
1. Example: Write code for an Arduino Uno to read a button and toggle an LED. Prompt: "Generate C++ code for Arduino Uno: Read digital input on pin 2 and toggle pin 13 LED." Result: Use `pinMode(2, INPUT);` and in loop: `if (digitalRead(2) == HIGH) { digitalWrite(13, !digitalRead(13)); delay(50); }`.
2. Example: Optimize IoT code for ESP32 to send sensor data to a server. Prompt: "Write efficient C code for ESP32 to read DHT11 sensor and POST data to http://example.com via WiFi, using less than 10KB RAM." Result: Include `dht.h`; use `esp_http_client_init()`; snippet: `float temp = dht_readTemperature(); http_post_data(temp);`.

## Graph Relationships
- Related to cluster: iot
- Shares tags: iot, embedded
- Connected skills: potentially other iot cluster skills like "wireless-protocols" or "sensor-integration" based on common tags
