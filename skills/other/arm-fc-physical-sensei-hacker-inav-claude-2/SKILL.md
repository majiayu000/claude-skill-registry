---
description: Arm physical flight controller via MSP and download blackbox logs
triggers:
  - arm fc
  - arm physical fc
  - download blackbox
  - blackbox from fc
---

# arm-fc-physical

**Arm a physical flight controller via MSP and download blackbox logs for analysis**

---

## When to Use This Skill

- Generate blackbox logs from physical FC for debugging
- Test firmware behavior without actual flight
- Capture sensor data for analysis
- Validate blackbox logging is working correctly

---

## Quick Start

### 1. Configure FC (One-Time Setup)

```bash
# Check FC status
~/.claude/skills/flash-firmware-dfu/fc-cli.py status /dev/ttyACM0

# Configure MSP receiver and arming
cd claude/developer/scripts/testing/inav/gps
python3 configure_fc_for_msp_arming.py /dev/ttyACM0
python3 configure_fc_blackbox.py /dev/ttyACM0

# Calibrate accelerometer via INAV Configurator (if needed)
```

### 2. Generate Blackbox Log

**SAFETY: Remove propellers before arming!**

```bash
cd claude/developer/scripts/testing/inav/gps

# Arm for 30 seconds (default)
python3 continuous_msp_rc_sender.py /dev/ttyACM0

# Arm for custom duration
python3 continuous_msp_rc_sender.py /dev/ttyACM0 --duration 60
```

### 3. Download Log

```bash
cd claude/developer/scripts/testing/inav/gps

# Download to default filename
python3 download_blackbox_from_fc.py /dev/ttyACM0

# Download to specific file
python3 download_blackbox_from_fc.py /dev/ttyACM0 test_log.TXT
```

### 4. Decode and Analyze

```bash
# Decode log to CSV
blackbox_decode test_log.TXT

# Creates: test_log.01.csv, test_log.01.gps.csv
# View data
head -50 test_log.01.csv
```

---

## Prerequisites

**Hardware:**
- Flight controller with USB connection
- FC appears as `/dev/ttyACM0` (or similar)
- **Propellers removed!**

**Software:**
```bash
pip3 install pyserial
pip3 install git+https://github.com/xznhj8129/mspapi2
```

**FC Configuration:**
1. Accelerometer calibrated (via Configurator)
2. MSP receiver configured (`rx_spi_protocol = MSP`)
3. ARM mode on AUX1 (range 1700-2100)
4. Blackbox enabled (`blackbox_device = SPIFLASH`)

---

## Common Issues

### FC Won't Arm

Check arming flags:
```bash
~/.claude/skills/flash-firmware-dfu/fc-cli.py status /dev/ttyACM0
```

Common blockers:
- **ACC** - Calibrate accelerometer via Configurator
- **CAL** - Wait 5+ seconds after boot
- **ANGLE** - Level FC or disable small_angle check
- **SETTINGFAIL** - Fix RX settings with configure script

### No Blackbox Data (0 bytes)

1. **HITL mode was used** - Use `continuous_msp_rc_sender.py` instead
2. **FC not armed** - Check arming flags
3. **Blackbox not configured** - Run `configure_fc_blackbox.py`
4. **Flash full** - Erase via Configurator

### Serial Port Permission Denied

```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

---

## Key Scripts

All located in: `claude/developer/scripts/testing/inav/gps/`

- **continuous_msp_rc_sender.py** - Arm FC and send RC frames
- **download_blackbox_from_fc.py** - Download log via MSP
- **configure_fc_for_msp_arming.py** - Configure MSP receiver
- **configure_fc_blackbox.py** - Configure blackbox settings

---

## Technical Details

**RC Frame Rate:** 50 Hz (matches CRSF standard)
**Download Speed:** ~2.5 KB/s (~20s for 50KB log)
**MSP Commands Used:**
- MSP_SET_RAW_RC (200) - Send RC channels
- MSP_DATAFLASH_SUMMARY (70) - Query flash status
- MSP_DATAFLASH_READ (71) - Download data

**RC Channel Mapping (AETR):**
- Channel 3: Throttle (1000=low, 1600=mid)
- Channel 5: AUX1 ARM (1000=disarm, 1800=arm)

---

## See Also

- **Detailed Guide:** `.claude/skills/arm-fc-physical/REFERENCE.md`
- **Flash Firmware:** `/flash-firmware-dfu`
- **Build Firmware:** `/build-inav-target`
- **Arm SITL:** `/sitl-arm`
- **MSP Protocol:** `/msp-protocol`
