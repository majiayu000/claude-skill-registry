---
description: Replay blackbox sensor data to flight controller (SITL or HITL)
triggers:
  - replay blackbox
  - replay blackbox log
  - blackbox replay
  - hitl replay
---

# replay-blackbox

**Replay blackbox sensor data to flight controller (SITL or HITL)**

---

## ⚠️ FIRMWARE MODIFICATION REQUIRED

**This skill sends real GPS EPH and EPV values from blackbox logs.**

Stock INAV hardcodes EPH=100cm and EPV=100cm. You must use **modified INAV firmware** that reads EPH/EPV from MSP_SIMULATOR packets.

**Modified file:** `inav/src/main/fc/fc_msp.c` (lines 4233-4260)

**Rebuild SITL after modification:**
```bash
cd ~/Documents/planes/inavflight/inav/build_sitl && cmake -DSITL=ON .. && make
```

---

## Description

Replays GPS, accelerometer, gyro, barometer, and magnetometer data from a decoded blackbox log to a flight controller using MSP_SIMULATOR (HITL mode). This allows you to reproduce flight conditions in a controlled environment for debugging and testing.

---

## Use Cases

- **Debug navigation issues** - Replay problematic flight data to reproduce bugs
- **Test position estimator** - Validate EPH calculations with real sensor data
- **Validate firmware changes** - Ensure fixes work with real flight conditions
- **Reproduce oscillations** - Debug GPS/EPH oscillation issues (Issue #11202)

---

## How It Works

1. Loads decoded blackbox CSV data:
   - Main CSV (`.01.csv`): IMU, baro, mag at high rate (~100-1000 Hz)
   - GPS CSV (`.01.gps.csv`): GPS data at real update rate (~10 Hz)
2. Connects to FC via TCP (SITL) or serial (HITL)
3. Enables HITL mode via MSP_SIMULATOR
4. Replays sensor data at original timing (or faster/slower)
   - GPS preserved at real rate (not artificially repeated)
5. FC processes data as if sensors were real

---

## Parameters

- **Required:**
  - `--csv` - Path to decoded blackbox CSV file

- **Optional:**
  - `--port` - Port to connect to (default: tcp:localhost:5761)
    - SITL: `tcp:localhost:5761`
    - HITL: `/dev/ttyACM0` or `/dev/ttyUSB0`
  - `--start-time` - Start time in seconds (default: 0.0)
  - `--duration` - Duration in seconds (default: entire log)
  - `--speed` - Playback speed multiplier (default: 1.0)

---

## Examples

### Replay to SITL (Software In The Loop)

```bash
# Replay entire log
/replay-blackbox --csv blackbox.01.csv

# Replay specific time range
/replay-blackbox --csv blackbox.01.csv --start-time 10.0 --duration 30.0

# Replay at 2x speed
/replay-blackbox --csv blackbox.01.csv --speed 2.0
```

### Replay to Physical FC (Hardware In The Loop)

```bash
# Replay to FC on /dev/ttyACM0
/replay-blackbox --csv blackbox.01.csv --port /dev/ttyACM0

# Replay specific section at half speed
/replay-blackbox --csv blackbox.01.csv --port /dev/ttyACM0 \
    --start-time 20.0 --duration 10.0 --speed 0.5
```

---

## Workflow

### 1. Prepare Blackbox Data

First, decode your blackbox log to CSV:

```bash
~/Documents/planes/inavflight/blackbox-tools/obj/blackbox_decode flight.TXT
# Creates: flight.01.csv (main sensor data)
#          flight.01.gps.csv (GPS data at ~10 Hz)
```

### 2. Start Target (SITL or HITL)

**For SITL:**
```bash
cd ~/Documents/planes/inavflight/inav/build_sitl
./bin/SITL.elf &
sleep 3  # Wait for SITL to start
```

**For HITL:**
- Connect FC via USB
- Ensure FC is in normal mode (not CLI)
- FC will enter HITL mode automatically when receiving MSP_SIMULATOR

### 3. Replay Data

```bash
/replay-blackbox --csv flight.01.csv --port tcp:localhost:5761
```

### 4. Capture Results

**For SITL:**
```bash
# Download blackbox from SITL
ls -lt ~/*.TXT | head -1  # Find latest blackbox

# Decode it
blackbox_decode <sitl_log>.TXT

# Compare with original
# Check if issue reproduced
```

**For HITL:**
```bash
# Download blackbox via MSP
python3 claude/developer/scripts/testing/inav/gps/download_blackbox_from_fc.py --port /dev/ttyACM0

# Decode and analyze
```

---

## Requirements

- **mspapi2** - `pip install mspapi2` or install from `mspapi2/` directory
- **Decoded blackbox CSV** - Use `blackbox_decode` to create from .TXT

---

## Troubleshooting

### "Serial port is not open"
- For SITL: Ensure SITL is running on tcp:localhost:5761
- For HITL: Check serial port permissions and correct device name

### "Could not enable HITL mode"
- Wait a few seconds after starting SITL
- For HITL: Ensure FC is not in CLI mode
- Check connection with: `netstat -an | grep 5761` (SITL)

### No GPS data in replay
- GPS data loaded from `.gps.csv` file (created by blackbox_decode)
- Check if file exists: `ls flight.01.gps.csv`
- Verify GPS data: `head -5 flight.01.gps.csv`
- Ensure GPS had fix during original flight
- Use `--start-time` to skip pre-GPS-lock period
- GPS sent at real rate (~10 Hz), not repeated at IMU rate

### Replay too fast/slow
- Adjust with `--speed` parameter
- 1.0 = real-time, 2.0 = 2x speed, 0.5 = half speed

---

## Technical Details

### MSP_SIMULATOR Format

Uses MSP command 0x201F (MSP_SIMULATOR) with HITL mode flags:
- `0x0001` - HITL_ENABLE
- `0x0002` - HITL_HAS_NEW_GPS_DATA

Sends all sensor data:
- GPS: position, velocity, EPH, satellites, HDOP
  - Loaded from `.gps.csv` at real update rate (~10 Hz)
  - Not artificially repeated - preserves GPS timing
- IMU: accelerometer (milli-G), gyro (deg/s × 16)
- Baro: pressure (Pa)
- Mag: magnetometer (firmware divides by 20)

See: `inav/src/main/fc/fc_msp.c:4160-4290`

### Field Conversions

| Blackbox Field | MSP Format | Conversion |
|----------------|------------|------------|
| `accSmooth[0-2]` | milli-G (int16) | `accSmooth / 512.0 * 1000.0` |
| `gyroADC[0-2]` | deg/s × 16 (int16) | Already correct format |
| `magADC[0-2]` | Scaled (int16) | `magADC * 20` |
| `BaroAlt (cm)` | Pressure (uint32 Pa) | `101325 - (alt_m * 12)` |
| `GPS_coord[0]` | int32 × 10^7 | `lat * 1e7` |

---

## See Also

- **Tool:** `claude/developer/scripts/testing/inav/blackbox/analysis/replay_blackbox_to_fc.py`
- **Investigation:** `claude/developer/investigations/gps-fluctuation-issue-11202/`
- **HITL docs:** INAV wiki - MSP_SIMULATOR
- **Related:** `/build-sitl` - Build SITL for testing

---

## Notes

- FC attitude (roll/pitch/yaw) set to 0 to let FC calculate from IMU
- Sample rate preserved from original blackbox (typically 100-1000 Hz)
- GPS rate preserved at real update rate (~10 Hz from .gps.csv)
- Works with any blackbox log that has IMU data
- GPS data optional (will replay IMU-only if no .gps.csv file)
