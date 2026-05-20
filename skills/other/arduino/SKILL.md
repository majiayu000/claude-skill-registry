---
name: arduino
cluster: iot
description: "Open-source platform for Arduino microcontrollers in IoT and embedded projects"
tags: ["iot","arduino"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "arduino iot"
---

# arduino

## Purpose
This skill provides tools for programming and managing Arduino microcontrollers, focusing on IoT and embedded systems development. It leverages the Arduino ecosystem to compile, upload, and interact with sketches on hardware like Arduino Uno or ESP32 boards.

## When to Use
Use this skill when building IoT prototypes, such as sensor networks or automated devices, that require microcontroller programming. Apply it for tasks like reading data from sensors (e.g., temperature via DHT11) or controlling actuators (e.g., LEDs, motors), especially in projects involving real-time data processing or hardware integration with platforms like Raspberry Pi.

## Key Capabilities
- Compile and upload Arduino sketches to boards using CLI commands.
- Manage boards, cores, and libraries for various Arduino-compatible hardware.
- Handle serial communication for debugging or data exchange in IoT setups.
- Integrate with external sensors and actuators through standard Arduino libraries.
- Support for multiple platforms, including AVR, ARM, and ESP-based boards.

## Usage Patterns
To use this skill, invoke Arduino CLI commands from scripts or directly in AI workflows. Always ensure the Arduino CLI is installed via `curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh`. For automation, wrap commands in shell scripts or Python subprocess calls. Specify the fully qualified board name (FQBN) for all operations, e.g., "arduino:avr:uno". If integrating into a larger AI agent flow, check for board connectivity first using `arduino-cli board list`.

## Common Commands/API
Use the Arduino CLI for core operations. Key commands include:
- Install a board core: `arduino-cli core install arduino:avr`
- Compile a sketch: `arduino-cli compile --fqbn arduino:avr:uno --output-dir /tmp/build path/to/sketch.ino`
- Upload a sketch: `arduino-cli upload -b arduino:avr:uno -p /dev/ttyUSB0 path/to/sketch.ino`
- List available boards: `arduino-cli board list`
- Add a library: `arduino-cli lib install "DHT sensor library"`

Code snippets:
1. Compile and upload a basic blink sketch:
   ```cpp
   void setup() { pinMode(LED_BUILTIN, OUTPUT); }
   void loop() { digitalWrite(LED_BUILTIN, HIGH); delay(1000); digitalWrite(LED_BUILTIN, LOW); delay(1000); }
   ```
   Run: `arduino-cli compile --fqbn arduino:avr:uno blink.ino && arduino-cli upload -b arduino:avr:uno -p /dev/ttyUSB0 blink.ino`

2. Manage libraries in a script:
   ```bash
   arduino-cli lib search DHT && arduino-cli lib install "DHT sensor library"
   ```

Config formats: Use JSON for CLI config files (e.g., `arduino-cli config init` creates a directories.json). Example snippet for a config file:
```json
{
  "board_manager": {
    "additional_urls": ["https://downloads.arduino.cc/packages"]
  }
}
```
If Arduino Cloud integration is needed (e.g., for IoT services), set auth via environment variable: `export ARDUINO_API_KEY=$ARDUINO_API_KEY`.

## Integration Notes
Integrate this skill by ensuring Arduino CLI is in your PATH. For cross-platform use, detect the serial port dynamically (e.g., `/dev/ttyUSB0` on Linux or `COM3` on Windows). When combining with other IoT tools, pipe output to parsers like jq for JSON handling. For example, in a bash script: `arduino-cli board list | jq '.boards[] | select(.port == "/dev/ttyUSB0")'`. If using Arduino Cloud APIs, authenticate with `$ARDUINO_API_KEY` and make requests to endpoints like `https://api2.arduino.cc/iot/v2/things`. Always verify hardware connections before commands to avoid failures.

## Error Handling
Always check CLI exit codes; a non-zero code indicates failure (e.g., `if [ $? -ne 0 ]; then echo "Compilation failed"; fi`). Parse error output for specifics, like missing libraries: "error: 'DHT' not declared". Common issues include incorrect FQBN—verify with `arduino-cli board listall`—or port conflicts; use `ls /dev/tty*` to list ports. For upload errors, ensure the board is in bootloader mode. In scripts, wrap commands in try-catch blocks if using languages like Python: 
```python
import subprocess
try:
    subprocess.run(['arduino-cli', 'compile', '--fqbn', 'arduino:avr:uno', 'sketch.ino'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.output}")
```
Log detailed errors for debugging IoT deployments.

## Graph Relationships
- Cluster: iot (directly linked to other skills in the iot cluster)
- Tags: iot (connects to skills with iot tag, e.g., for combined IoT workflows), arduino (links to specialized embedded system skills)
- Related skills: Any with iot tag, such as those for Raspberry Pi or ESP32, for expanded IoT capabilities
