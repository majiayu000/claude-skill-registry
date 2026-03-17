---
description: Flash and test code on PrivacyLRS/ExpressLRS ESP32 hardware modules (TX/RX)
triggers:
  - test on hardware
  - flash hardware
  - upload to ESP32
  - test ESP32
  - flash TX
  - flash RX
  - test TX module
  - test RX module
  - upload firmware to hardware
  - test on real hardware
  - hardware test
---

# Test PrivacyLRS/ELRS Hardware

Flash and test firmware on ESP32-based PrivacyLRS/ExpressLRS hardware modules.

## Hardware Setup

1. **Connect Device via USB:**
   ```bash
   # Verify connection
   ls -la /dev/ttyUSB*
   pio device list
   ```

2. **Identify Device:**
   - TX modules: Transmitter/Handset
   - RX modules: Receiver
   - Note MAC address for tracking

## Building Production Firmware

```bash
cd PrivacyLRS/src
PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400" pio run -e <target> --target upload
```

Common targets: `namimnorc-tx`, `namimnorc-rx` (check platformio.ini for more)

## Creating Standalone Test Firmware

For isolated testing:

### 1. Create Test Project
```bash
mkdir -p PrivacyLRS/test_esp32_standalone/{src}
cd PrivacyLRS/test_esp32_standalone
```

### 2. Create platformio.ini
```ini
[env:esp32test]
platform = espressif32@6.4.0
board = esp32dev
framework = arduino
upload_port = /dev/ttyUSB0
monitor_port = /dev/ttyUSB0
monitor_speed = 115200
lib_deps =
    ; Add libraries as needed
```

### 3. Create src/main.cpp
```cpp
#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(2000);
    Serial.println("Test starting...");
    // Your test code
}

void loop() {
    delay(5000);
    Serial.println("Running...");
}
```

### 4. Build and Upload
```bash
pio run -e esp32test --target upload
```

## Capturing Serial Output

### Simple Capture
```bash
stty -F /dev/ttyUSB0 115200
timeout 30 cat /dev/ttyUSB0 | tee output.txt
```

### Continuous Monitor
```bash
stty -F /dev/ttyUSB0 115200
cat /dev/ttyUSB0  # Ctrl+C to stop
```

### Capture Boot Sequence
```bash
# Upload resets device automatically
pio run -e esp32test --target upload
sleep 2
timeout 10 cat /dev/ttyUSB0 > boot.txt
cat boot.txt
```

## Troubleshooting

### Device Not Found
```bash
lsusb                          # Check USB devices
ls -la /dev/ttyUSB* /dev/ttyACM*  # Check serial ports
sudo usermod -a -G dialout $USER   # Fix permissions (logout/login after)
```

### Garbled Output
```bash
# Try different baud rates
stty -F /dev/ttyUSB0 115200  # Standard
stty -F /dev/ttyUSB0 460800  # High speed
```

### Crash (Boot Loop)

Look for:
- `Guru Meditation Error` - ESP32 crash
- `panic'ed (LoadProhibited)` - Memory access error
- `EXCVADDR: 0x00000000` - Null pointer dereference
- `PC: 0x...` - Crash address

Decode crash address:
```bash
xtensa-esp32-elf-addr2line -e .pio/build/esp32test/firmware.elf <PC_address>
```

## Incremental Testing

For debugging, test incrementally:

1. Minimal - Just `Serial.println("Hello")`
2. Add includes - One header at a time
3. Create objects - Instantiate classes
4. Initialize - Call setup methods
5. Operations - Test functionality
6. Stress test - Loops and benchmarks

Stop at first failure to isolate the problem!

## Memory Check

Watch build output:
```
RAM:   [=    ]  6.6% (21552 / 327680 bytes)
Flash: [==   ] 20.2% (265285 / 1310720 bytes)
```

Safe limits: RAM < 80%, Flash < 90%

## Common Build Flags

```bash
# Required for some builds
PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400"

# Enable encryption
PLATFORMIO_BUILD_FLAGS="-DUSE_ENCRYPTION"

# Multiple flags
PLATFORMIO_BUILD_FLAGS="-DRegulatory_Domain_ISM_2400 -DUSE_ENCRYPTION"
```

## Expected Output

### Normal Boot
```
ets Jun  8 2016 00:22:57
rst:0x1 (POWERON_RESET)
...
Test starting...
Running...
```

### Crash
```
Guru Meditation Error: Core 1 panic'ed (LoadProhibited)
PC: 0x400d4314  EXCVADDR: 0x00000000
Rebooting...
```

## Best Practices

- Start with minimal test code
- Use Serial.println() for debugging
- Save all output to files
- Commit working states to git
- Document device MAC and test results

---

## Related Skills

- **privacylrs-test-runner** - Run unit tests before hardware testing
- **create-pr** - Create pull request after validating on hardware
