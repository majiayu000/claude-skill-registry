---
name: gpio-config
description: Assigns, validates, and generates code for GPIO pin configurations on Raspberry Pi and ESP32 embedded projects. Activates for queries about GPIO pins, wiring, pin mapping, pin conflicts, I2C, SPI, UART, PWM, 1-Wire, CAN, ADC configuration, device tree overlays, config.txt, sdkconfig, strapping pins, boot pins, flash voltage, or connecting sensors, displays, and modules such as BME280, SSD1306, DHT22, LoRa, GPS, MCP2515, and NeoPixels. Covers Pi 3, Pi 4, Pi 5, Zero 2W, ESP32, ESP32-S2, ESP32-S3, ESP32-C3, and ESP32-C6. Produces platform-specific config files and initialization code for Python gpiozero, RPi.GPIO, Arduino, and ESP-IDF frameworks. Also activates when a device and board are named without mentioning GPIO, e.g. 'BME280 on a Pi 4' or 'connect a GPS to my ESP32', or when pin selection or pin safety questions arise.
license: MIT. See LICENSE in repository root.
---

## 1 · Platform Detection

### Explicit Detection

| Keywords/Patterns | Platform |
|---|---|
| Raspberry Pi, RPi, BCM2835, BCM2711, BCM2712, config.txt, dtoverlay, gpiozero, RPi.GPIO, pigpio, /boot/firmware/ | RPi |
| ESP32, ESP-IDF, WROOM, WROVER, menuconfig, sdkconfig, Arduino (with ESP context), esp_err_t, gpio_config(), ESP32-S2, S3, C3, C6 | ESP32 |

### Model/Variant Detection

**RPi Variants:**

| Identifier | Models Covered | Key Differences |
|---|---|---|
| rpi3 | Pi 3B/3B+ | UART/BT conflict on mini-UART, 2× PWM channels, config at /boot/config.txt |
| rpi4 | Pi 4B | 4× PWM channels, dual SPI, config at /boot/firmware/config.txt |
| rpi5 | Pi 5 | RP1 southbridge (different peripheral base), 4× PWM, config at /boot/firmware/config.txt |
| rpi_zero2w | Zero 2W | Same SoC as Pi 3, UART/BT conflict, limited current budget |

**ESP32 Variants:**

| Identifier | Key Differences |
|---|---|
| esp32 | 34 GPIO, dual-core, ADC2 conflicts with WiFi, Hall sensor on GPIO36/39 |
| esp32s2 | 43 GPIO, single-core, no Bluetooth, native USB, no ADC2/WiFi conflict |
| esp32s3 | 45 GPIO, dual-core, BLE5, native USB, no ADC2/WiFi conflict |
| esp32c3 | 22 GPIO, single-core RISC-V, BLE5 only, no ADC2/WiFi conflict |
| esp32c6 | 30 GPIO, RISC-V, WiFi 6, 802.15.4, no ADC2/WiFi conflict |

**ESP32 Modules:**

| Module | Additional Reserved Pins |
|---|---|
| WROOM | GPIO6–11 (flash SPI) |
| WROVER | GPIO6–11 (flash SPI) + GPIO16–17 (PSRAM) |

### Ambiguity Rules

1. If platform cannot be determined from context: ask the user. NEVER silently default to a platform.
2. If platform is detected but variant is unknown: ask the user for model/variant. Default to most conservative variant if user declines (rpi3 for RPi, esp32 + WROOM for ESP32).
3. Unsupported platforms (RP2040/Pico, STM32, Arduino AVR, BeagleBone): state that the platform is not yet supported, list supported platforms, offer to help if user switches.

## 2 · Reference Loading

ALWAYS load the platform pin database. Load other files only when their trigger condition is met.

| File | Trigger |
|---|---|
| references/platforms/rpi-pins.md | Platform is RPi (any variant) |
| references/platforms/esp32-pins.md | Platform is ESP32 (any variant) |
| references/platforms/esp32-specifics.md | ESP32 detected AND any of: strapping pins mentioned, deep sleep, flash/PSRAM, ADC2, boot issues |
| references/platforms/rpi-overlays.md | RPi detected AND any of: device tree, dtoverlay, overlay, kernel module, /boot/ config |
| references/protocol-quick-ref.md | Any protocol mentioned: I2C, SPI, UART, PWM, 1-Wire, CAN, Modbus, ADC, DAC |
| references/electrical-constraints.md | Current limits, voltage levels, pull-ups/pull-downs, power supply, level shifting mentioned |
| references/common-devices.md | Specific sensor, module, display, or breakout board mentioned by name or part number |

## 3 · Core Workflow

### Step 1 — Parse

Extract from the user's request:
- Target platform and variant (or flag as unknown)
- Required protocols and their quantities (e.g., "2× I2C", "1× SPI")
- Named devices/modules (e.g., "BME280", "SSD1306", "NeoPixel")
- Existing pin commitments ("I'm already using GPIO17 for...")
- Special requirements (deep sleep wake, interrupt-capable, analog input, high-speed)
- Framework preference (gpiozero, RPi.GPIO, Arduino, ESP-IDF) or "not specified"

### Step 2 — Detect

Apply Section 1 rules. Result: confirmed platform + variant + module type, OR ask the user.

### Step 3 — Load

Apply Section 2 table. Load all triggered reference files before proceeding.

### Step 4 — Gather

If any critical information is missing (platform, protocol count, or device identity), ask ONE concise follow-up question covering all gaps. If information is merely ambiguous but reasonable defaults exist, proceed and list assumptions in the output. Never ask more than one follow-up message.

### Step 5 — Generate

Assign pins using platform-specific strategy:

**RPi strategy:**
1. Assign hardware-native pins first (I2C → GPIO2/3, SPI0 → GPIO7–11, UART → GPIO14/15)
2. Prefer GPIO12/13 for hardware PWM
3. Never assign GPIO0 or GPIO1 (I2C EEPROM reserved)
4. Use clean GPIOs for general digital I/O: 5, 6, 16, 17, 22, 23, 24, 25, 26, 27
5. Note all pins that pull high/low at boot
6. Track cumulative current draw against 50mA GPIO budget

**ESP32 strategy:**
1. Never assign flash SPI pins (GPIO6–11; also GPIO16–17 on WROVER)
2. Warn if assigning strapping pins (GPIO0, 2, 5, 12, 15) — add boot-state note for each
3. Elevate GPIO12 (MTDI) to a stronger warning: wrong state at boot can set flash voltage to 1.8V and brick the module
4. Use conventional I2C pins (GPIO21 SDA, GPIO22 SCL) unless conflict exists
5. Use native SPI pins: VSPI (GPIO5/18/19/23) or HSPI (GPIO12/13/14/15) — note strapping overlap on HSPI
6. If WiFi is enabled, avoid ADC2 channels entirely (esp32 variant only)
7. Assign input-only pins (GPIO34–39) only for inputs, never outputs or bidirectional
8. Prefer RTC-capable GPIOs for deep-sleep wake sources
9. Reserve GPIO1/3 (UART0 TX/RX) for debug serial unless user explicitly reassigns
10. Note that any output-capable GPIO supports PWM via LEDC — no dedicated PWM pins needed

### Step 6 — Validate

Invoke the validation script:

```bash
python scripts/validate_pinmap.py --format json <<'EOF'
<input JSON>
EOF
```

If validation returns errors: reassign conflicting pins and re-validate. Loop a maximum of 3 times. If still failing after 3 attempts, present the best result with remaining warnings explained.

If validation returns warnings only: include warnings in output, proceed.

### Step 7 — Output

Generate the response using Section 4 format. Then invoke the generation script:

```bash
python scripts/generate_config.py --format json --framework <framework> <<'EOF'
<input JSON>
EOF
```

Include all script outputs in the structured response.

## 4 · Output Format

### Pin Assignment Table

- RPi columns: Function | GPIO (BCM) | Physical Pin | Alt Mode | Notes
- ESP32 columns: Function | GPIO | Notes | Strapping? | RTC Channel?
- Sort by function group (I2C, SPI, UART, PWM, digital I/O, analog)

### Configuration

- RPi: config.txt lines (dtoverlay, dtparam, gpio= directives). Note correct path for variant.
- ESP32: menuconfig/sdkconfig.defaults lines (if Arduino: note that most config is in code)

### Initialization Code

- RPi: provide both gpiozero and RPi.GPIO versions unless user specified one
- ESP32: provide both Arduino and ESP-IDF versions unless user specified one
- Always include: pin mode setup, pull-up/pull-down config, protocol init with correct pins, brief comments

### Wiring Notes

- Human-readable wiring instructions using physical pin numbers AND GPIO numbers
- Include: pull-up resistor values for I2C/1-Wire, power rail connections, level shifter notes if mixing voltages, decoupling caps for sensitive devices

### Warnings

- Pin conflicts detected during validation
- Strapping pin usage (ESP32)
- Current budget concerns
- UART/Bluetooth conflicts (RPi 3/4/Zero2W)
- PWM/audio conflicts (RPi)
- ADC2/WiFi conflicts (ESP32)
- Deprecated library warnings (e.g., RPi.GPIO on Pi 5)

### Alternatives

- For every conflict that was auto-resolved, explain: original pin → replacement pin and why
- If multiple valid assignments exist, briefly note the top alternative

## 5 · Critical Rules

### Universal

1. Always present GPIO numbers prominently — never reference physical pin numbers only
2. Never silently assign a reserved or restricted pin — always warn
3. Check I2C device address collisions when multiple I2C devices share a bus
4. Include pull-up/pull-down notes for every protocol that requires them
5. Respect per-platform current limits and warn when cumulative draw approaches budget
6. Warn about deprecated libraries (RPi.GPIO on Pi 5 has limited support; suggest gpiozero or lgpio)
7. If the user's request exceeds available pins, say so and suggest multiplexing (I2C expander, SPI daisy-chain)

### RPi-Specific

1. Use BCM numbering by default. If user requests BOARD numbering, provide both.
2. Never assign GPIO0 or GPIO1 — reserved for HAT EEPROM I2C
3. On Pi 3/4/Zero 2W: UART0 (GPIO14/15) is linked to Bluetooth by default. Warn and explain dtoverlay=miniuart-bt or dtoverlay=disable-bt
4. Prefer GPIO12/13 for hardware PWM (PWM0/PWM1). GPIO18 is PWM-capable but conflicts with PCM/audio.
5. PWM on GPIO18 + audio output = conflict. Warn if both are needed.
6. Total GPIO current budget: 50mA across all pins. Track and warn.
7. SPI0 claims GPIO7–11 (CE1, CE0, MISO, MOSI, SCLK). Do not assign these for other use when SPI0 is active.
8. Config.txt path: /boot/config.txt on Pi 3 and older, /boot/firmware/config.txt on Pi 4/5 with Bookworm+

### ESP32-Specific

1. Flash SPI pins (GPIO6–11) are never available. On WROVER modules, GPIO16–17 are also reserved (PSRAM).
2. Strapping pins (GPIO0, 2, 5, 12, 15): warn on every use with the required boot state for each.
3. GPIO12 (MTDI) gets an elevated warning: if pulled high at boot, flash voltage switches to 1.8V — can brick 3.3V flash modules. Advise efuse or boot-fix if user must use it.
4. ADC2 (GPIO0, 2, 4, 12–15, 25–27) is unavailable when WiFi is active — this applies to the original ESP32 variant only, not S2/S3/C3/C6.
5. GPIO34–39 are input-only: no internal pull-ups, no output mode. Assign only for input signals.
6. For deep-sleep wake: use RTC GPIOs only (GPIO0–21, 25–27 on ESP32). Check per-variant RTC GPIO list.
7. UART0 (GPIO1 TX, GPIO3 RX) is the default debug/programming port. Do not reassign without explicit user intent.
8. Any output-capable GPIO can generate PWM via LEDC peripheral — no special pin selection needed.
9. Maximum source current per pin: 40mA (recommended 20mA). Total chip limit varies by variant.

## 6 · Script Interface

### validate_pinmap.py

Location: scripts/validate_pinmap.py

CLI usage:

```bash
python scripts/validate_pinmap.py --format json [--verbose] < input.json
python scripts/validate_pinmap.py --help
```

Input JSON schema:

```json
{
  "platform": "rpi | esp32",
  "variant": "rpi3 | rpi4 | rpi5 | rpi_zero2w | esp32 | esp32s2 | esp32s3 | esp32c3 | esp32c6",
  "module": "WROOM | WROVER | null",
  "wifi_enabled": true,
  "pins": [
    {
      "gpio": 17,
      "function": "I2C_SDA | I2C_SCL | SPI_MOSI | SPI_MISO | SPI_SCLK | SPI_CS | UART_TX | UART_RX | PWM | DIGITAL_IN | DIGITAL_OUT | ANALOG_IN | 1WIRE | CAN_TX | CAN_RX",
      "protocol_bus": 0,
      "device": "BME280",
      "pull": "up | down | none",
      "notes": ""
    }
  ]
}
```

Output JSON schema:

```json
{
  "valid": true,
  "errors": [
    {
      "gpio": 6,
      "code": "RESERVED_PIN | CONFLICT | INPUT_ONLY_AS_OUTPUT | STRAPPING_UNACKNOWLEDGED | ADC2_WIFI | CURRENT_EXCEEDED",
      "message": "Human-readable error",
      "severity": "error"
    }
  ],
  "warnings": [
    {
      "gpio": 12,
      "code": "STRAPPING_PIN | UART_BT_CONFLICT | PWM_AUDIO_CONFLICT | DEPRECATED_LIB | CURRENT_WARNING | BOOT_STATE",
      "message": "Human-readable warning",
      "severity": "warning"
    }
  ],
  "summary": {
    "total_pins": 8,
    "errors": 0,
    "warnings": 2,
    "current_draw_ma": 32
  }
}
```

Exit codes: 0 = valid (warnings ok), 1 = errors found, 2 = invalid input

### generate_config.py

Location: scripts/generate_config.py

CLI usage:

```bash
python scripts/generate_config.py --format json --framework arduino|espidf|gpiozero|rpigpio [--verbose] < input.json
python scripts/generate_config.py --help
```

Input JSON schema: same as validate_pinmap.py input, plus:

```json
{
  "platform": "rpi | esp32",
  "variant": "rpi3 | rpi4 | rpi5 | rpi_zero2w | esp32 | esp32s2 | esp32s3 | esp32c3 | esp32c6",
  "module": "WROOM | WROVER | null",
  "wifi_enabled": true,
  "pins": [],
  "framework": "arduino | espidf | gpiozero | rpigpio"
}
```

Output JSON schema:

```json
{
  "config_lines": ["dtoverlay=i2c1", "dtparam=spi=on"],
  "init_code": "# Full initialization code as a single string with newlines",
  "wiring_notes": [
    "Connect BME280 SDA to GPIO2 (physical pin 3). Add 4.7kΩ pull-up to 3.3V."
  ],
  "warnings": ["GPIO12 is a strapping pin — see boot state notes"],
  "alternatives": [
    {
      "original_gpio": 12,
      "alternative_gpio": 17,
      "reason": "Avoids MTDI strapping pin risk"
    }
  ]
}
```

Exit codes: 0 = success, 1 = generation error, 2 = invalid input

## 7 · Requirements

- Python 3.9+ (standard library only — no pip packages required)

## 8 · Example

**User request:** "Set up a weather station with BME280 temperature sensor and SSD1306 OLED display on Raspberry Pi 4"

**Generated pinmap (excerpt):**

```json
{
  "platform": "rpi",
  "variant": "rpi4",
  "pins": [
    {"gpio": 2, "function": "I2C_SDA", "protocol_bus": 1, "device": "BME280+SSD1306", "pull": "external_up"},
    {"gpio": 3, "function": "I2C_SCL", "protocol_bus": 1, "device": "BME280+SSD1306", "pull": "external_up"},
    {"gpio": 17, "function": "DIGITAL_OUT", "device": "Status LED", "pull": "none"}
  ]
}
```

**Generated initialization code (gpiozero, excerpt):**

```python
from gpiozero import LED
import smbus2

bus = smbus2.SMBus(1)  # I2C bus 1: SDA=GPIO2, SCL=GPIO3
# BME280 at 0x76, SSD1306 at 0x3C — shared I2C bus, no conflict

status_led = LED(17)
```
