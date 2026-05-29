---
description: Arm INAV SITL via MSP protocol for automated testing
triggers:
  - arm SITL
  - SITL arming
  - arm simulator
  - MSP arming
  - SITL MSP arm
  - run SITL armed
  - test SITL arming
  - launch and arm SITL
---

# SITL Launch and Arm Guide

This guide covers launching INAV SITL and arming it via MSP protocol for automated testing.

## Prerequisites

### Building SITL

See the **build-sitl** skill for complete build instructions. Quick reference:

```bash
cd inav
mkdir -p build_sitl && cd build_sitl
cmake -DSITL=ON ..
make -j4
```

### Python Dependencies

**Recommended: mspapi2**
```bash
cd mspapi2
pip3 install .
```

Or install directly from GitHub:
```bash
pip3 install git+https://github.com/xznhj8129/mspapi2
```

**Quick Example (mspapi2):**
```python
from mspapi2 import MSPApi

# Connect to SITL
with MSPApi(tcp_endpoint="localhost:5760") as api:
    # Get status
    info, status = api.get_nav_status()
    print(f"Nav State: {status['navState']}")

    # Set RC channels (ARM on AUX1)
    api.set_rc_channels({
        "roll": 1500,
        "pitch": 1500,
        "throttle": 1000,
        "yaw": 1500,
        4: 2000  # AUX1 for ARM
    })
```

**Documentation:**
- mspapi2 Getting Started: `mspapi2/docs/GETTING_STARTED.md`
- Flight Computer Guide: `mspapi2/docs/FLIGHT_COMPUTER.md` (autonomous navigation)
- Discovering MSP Fields: `mspapi2/docs/DISCOVERING_FIELDS.md`

**Alternative: uNAVlib (older)**
```bash
pip3 install git+https://github.com/xznhj8129/uNAVlib
```

For new projects, prefer mspapi2. Existing scripts using uNAVlib will continue to work.

## Launching SITL

```bash
cd inav/build_sitl

# Kill any existing instances
pkill -9 SITL.elf 2>/dev/null

# Remove old EEPROM for fresh config (optional)
rm -f eeprom.bin

# Launch in background
./bin/SITL.elf > /tmp/sitl.log 2>&1 &

# Wait for initialization (8-10 seconds)
sleep 10

# Verify running
pgrep -la SITL && ss -tlnp | grep 576
```

### SITL TCP Ports

- **Port 5760**: UART1 (configurator)
- **Port 5761**: UART2 (testing scripts)

## Arming SITL via MSP

### Using the Test Script

```bash
python3 claude/developer/test_tools/sitl_arm_test.py 5761
```

### Manual Arming Steps

#### 1. Set Receiver Type to MSP

MSP_SET_RX_CONFIG (code 45), set byte 23 to 2 (RX_TYPE_MSP).

#### 2. Configure ARM Mode on AUX1

MSP_SET_MODE_RANGE (code 35):
```python
# [slot, boxId, auxChannel, startStep, endStep]
payload = [0, 0, 0, 32, 48]  # ARM on AUX1, range 1700-2100
```

#### 3. Save and Reboot

```python
board.send_RAW_msg(250, data=[])  # MSP_EEPROM_WRITE
time.sleep(0.5)
board.send_RAW_msg(68, data=[])   # MSP_REBOOT
# Wait 15 seconds for restart
```

#### 4. Enable HITL Mode (Bypass Sensor Calibration)

**CRITICAL**: Standalone SITL doesn't complete sensor calibration. Use MSP_SIMULATOR:

```python
MSP_SIMULATOR = 0x201F
payload = [2, 1]  # [version, HITL_ENABLE]
board.send_RAW_msg(MSP_SIMULATOR, data=payload)
```

#### 5. Send Continuous RC Data

**CRITICAL**: MSP receiver times out after 200ms. Send at 50Hz:

```python
# AETR channel order (NOT AERT!)
# [Roll, Pitch, THROTTLE, Yaw, AUX1, ...]
channels = [1500, 1500, 1000, 1500, 2000, 1000, 1000, 1000] + [1500]*8
data = []
for ch in channels:
    data.extend([ch & 0xFF, (ch >> 8) & 0xFF])
board.send_RAW_msg(200, data=data)

# MUST consume response to prevent buffer overflow
dataHandler = board.receive_msg()
```

## Key Technical Details

### Channel Order

INAV uses rcmap `{0, 1, 3, 2}` (AETR):
- Raw 0 -> Roll
- Raw 1 -> Pitch
- Raw 2 -> **THROTTLE** (not Yaw!)
- Raw 3 -> **Yaw** (not Throttle!)

MSP_SET_RAW_RC expects: `[Roll, Pitch, Throttle, Yaw, AUX1, ...]`

### MSP Response Handling

**Always consume responses** after MSP_SET_RAW_RC to prevent socket buffer overflow and MSP parser desync.

### Arming Blockers

| Flag | Bit | Solution |
|------|-----|----------|
| RC_LINK | 18 | Send RC every 20ms, consume responses |
| THROTTLE | 19 | Use AETR order, throttle at channel 2 |
| ARM_SWITCH | 14 | Set AUX1 > 1700 |
| SENSORS_CALIBRATING | 9 | Enable HITL mode |
| ACCELEROMETER_NOT_CALIBRATED | 13 | Enable HITL mode |

### MSP Commands

| Code | Name | Purpose |
|------|------|---------|
| 35 | MSP_SET_MODE_RANGE | Configure mode activation |
| 45 | MSP_SET_RX_CONFIG | Set receiver type |
| 68 | MSP_REBOOT | Reboot FC |
| 200 | MSP_SET_RAW_RC | Send RC values |
| 250 | MSP_EEPROM_WRITE | Save config |
| 0x2000 | MSP2_INAV_STATUS | Query arming flags |
| 0x201F | MSP_SIMULATOR | Enable HITL mode |

## Files

### SITL Arming Scripts

- **Basic arm** (uNAVlib): `claude/test_tools/inav/arm_sitl.py` - Simple arming script
- **Full test** (uNAVlib): `claude/test_tools/inav/sitl/sitl_arm_test.py` - Complete test suite
- **Configure for arming** (mspapi2): `claude/test_tools/inav/gps/configure_sitl_for_arming.py` - Set up MSP receiver and ARM mode

### Project Documentation

- Project status: `claude/projects/sitl-msp-arming/status.md`

## Source Code

- rcmap: `src/main/rx/rx.c:114`
- MSP_SIMULATOR: `src/main/fc/fc_msp.c:4080-4160`
- Arming flags: `src/main/fc/runtime_config.h`

## Related Skills

- **build-sitl** - Building SITL firmware
- **test-crsf-sitl** - Testing CRSF telemetry with SITL
- **run-configurator** - Using INAV Configurator with SITL
- **msp-protocol** - MSP protocol reference (used for arming)
