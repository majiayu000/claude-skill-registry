---
description: Test CRSF telemetry changes using INAV SITL simulation
triggers:
  - test crsf
  - test crsf sitl
  - crsf telemetry test
---

# test-crsf-sitl

**Complete workflow for testing CRSF telemetry changes using INAV SITL**

---

## When to Use This Skill

Use this skill when testing Pull Requests that modify CRSF telemetry:
- New telemetry frame types
- Changes to existing CRSF frames
- CRSF protocol updates
- Telemetry scheduling changes

**Example PRs:**
- PR #11025: Add AIRSPEED, RPM, TEMPERATURE frames
- PR #11100: BAROMETER altitude frame variations

---

## Prerequisites

### Required Tools

1. **INAV Source Code** - Checked out to PR branch
2. **INAV Configurator** - Built and ready (`npm install` completed)
3. **Python 3** - For testing scripts
4. **MSP Library** - mspapi2 (recommended) or uNAVlib (older alternative)
   - **mspapi2:** `$HOME/inavflight/mspapi2` (https://github.com/xznhj8129/mspapi2)
     - Install: `cd mspapi2 && pip install .`
     - Docs: `mspapi2/docs/GETTING_STARTED.md`
   - **uNAVlib:** `$HOME/inavflight/uNAVlib` (https://github.com/xznhj8129/uNAVlib)
     - Use for legacy scripts only, prefer mspapi2 for new work

### Testing Scripts

**Location:** `claude/developer/scripts/testing/inav/crsf/`

**Key Scripts:**

1. **crsf_rc_sender.py** - Bidirectional RC/Telemetry Handler with Error Detection
   - Sends CRSF RC frames to SITL at configurable rate (default 50Hz)
   - **Receives and displays telemetry** on same connection (bidirectional)
   - **EdgeTX-compatible error detection** - validates all frames (CRC, length, framing)
   - Use `--show-telemetry` flag for verbose output (errors, warnings, frame dumps)
   - **IMPORTANT:** This is the ONLY script you need - it handles both RC and telemetry!
   - **Detects:** CRC errors, framing errors, buffer overflows, sync loss
   - **Reports:** Stream health indicator (EXCELLENT/GOOD/FAIR/POOR)

2. **configure_crsf_proper_sequence.py** - MSP-based CRSF configuration
   - Configures UART2 for CRSF RX in correct sequence
   - Sets receiver type, protocol, and enables telemetry feature
   - Located in `inav/` directory

3. **TCP_CONNECTION_LIMITATION.md** - Important Documentation
   - Explains why separate RC sender and telemetry reader won't work
   - Documents TCP port constraints and bidirectional solution
   - Located in `claude/developer/scripts/testing/inav/docs/`

---

## Complete Testing Workflow

### Step 1: Enable CRSF Telemetry in SITL (**CRITICAL!**)

**⚠️ IMPORTANT:** SITL disables CRSF telemetry at TWO levels - both MUST be enabled!

#### Part A: Compile-Time Enable (Required Before Build)

Before building, you MUST enable CRSF telemetry compilation:

```bash
cd $HOME/inavflight/inav

# Edit src/main/target/SITL/target.h
# Find line ~97: #undef USE_TELEMETRY_CRSF
# Comment it out:
// #undef USE_TELEMETRY_CRSF  // ENABLED FOR TESTING PR #XXXXX
```

**Why this is needed:**
- SITL `target.h` explicitly disables CRSF telemetry compilation (line 97)
- Without this, `initCrsfTelemetry()` is never compiled into the binary
- Verify after build: `nm bin/SITL.elf | grep initCrsfTelemetry` should show the symbol

#### Part B: Runtime Enable (Required After Build)

After building and starting SITL, you MUST also enable the TELEMETRY feature flag:

**Using Python Script (Recommended):**
```bash
cd $HOME/inavflight/inav
python3 enable_telemetry_feature.py
```

**Manual Method (Configurator):**
1. Start SITL
2. Connect with Configurator (TCP:5760)
3. Go to **Configuration** tab
4. Enable **TELEMETRY** checkbox in features list
5. Click **Save and Reboot**

**Why this is needed:**
- File: `src/main/fc/fc_init.c:608`
- Code: `if (feature(FEATURE_TELEMETRY)) { telemetryInit(); }`
- By default, SITL does NOT enable the TELEMETRY feature (bit 10 = 0x400)
- Without this runtime flag, `telemetryInit()` is NEVER called even though it's compiled
- CRSF RX will work, but telemetry initialization is completely skipped

**Verification:**
After both steps, SITL logs should show:
```
[CRSF INIT] SUCCESS: Serial port opened
[TELEMETRY] telemetryInit() called
[CRSF TELEM] initCrsfTelemetry: enabled=1
[CRSF TELEM] Calling crsfRxSendTelemetryData
```

### Step 2: Build SITL for Target PR

```bash
cd $HOME/inavflight/inav

# Fetch PR (example: PR #11025)
git fetch origin pull/11025/head:pr-11025-crsf-telem
git checkout pr-11025-crsf-telem

# IMPORTANT: Enable CRSF telemetry in target.h (see Step 1)

# Create separate build directory
mkdir build_sitl_pr11025
cd build_sitl_pr11025

# Configure and build
cmake -DSITL=ON ..
make -j4

# Verify binary
file bin/SITL.elf
# Expected: ELF 64-bit LSB pie executable, x86-64
```

**Build Time:** ~2 minutes on 4 cores

**Known Issue:** If linker fails with `--no-warn-rwx-segments` error:
```bash
# Edit cmake/sitl.cmake, comment out lines 67-70
# OR use build-sitl skill for automatic fix
```

### Step 2: Configure CRSF (Use Configurator - Most Reliable)

**Important:** MSP configuration script has limitations. Use Configurator GUI for reliable setup.

```bash
# Start Configurator
cd $HOME/inavflight/inav-configurator
npm start
```

**In Configurator:**

1. **Start SITL first:**
   ```bash
   cd $HOME/inavflight/inav/build_sitl_pr11025
   ./bin/SITL.elf &
   ```

2. **Connect:**
   - Connection: `TCP`
   - Port: `5760`
   - Click "Connect"

3. **Configure Receiver:**
   - Go to **Receiver** tab
   - Receiver Type → **Serial Based Receiver**
   - Serial Receiver Provider → **CRSF**

4. **Save and Reboot:**
   - Click **Save and Reboot**
   - Wait 15 seconds for SITL to restart

5. **Verify Configuration:**
   ```bash
   # Check that UART2 is now listening
   ss -tlnp | grep 5761
   # Expected: LISTEN ... *:5761 ... SITL.elf

   # Check eeprom.bin was created
   ls -lh eeprom.bin
   # Expected: 32K file
   ```

### Step 3: Test CRSF RC and Telemetry (Bidirectional)

**IMPORTANT:** Use the bidirectional RC sender that handles both RC transmission and telemetry reception!

```bash
cd $HOME/inavflight/claude/developer/scripts/testing/inav/crsf

# Test for 30 seconds with telemetry display
python3 crsf_rc_sender.py 2 --rate 50 --duration 30 --show-telemetry

# Or run without telemetry display (cleaner output, shows summary only)
python3 crsf_rc_sender.py 2 --rate 50 --duration 30
```

**Script Options:**
- `2` - UART number (UART2 = port 5761)
- `--rate 50` - Frame rate in Hz (50Hz = CRSF standard)
- `--duration N` - Stop after N seconds (omit for continuous)
- `--show-telemetry` - Display each telemetry frame on STDOUT

**Why Bidirectional?**
- TCP ports accept only ONE client connection
- CRSF is bidirectional on same wire (matches real hardware)
- Single script sends RC frames AND reads telemetry responses
- See `TCP_CONNECTION_LIMITATION.md` for detailed explanation

### Step 4: Verify Telemetry Output

**Expected Output (with --show-telemetry):**
```
=== CRSF RC Frame Sender ===
Connecting to SITL UART2 on port 5761...
✓ Connected to 127.0.0.1:5761 (after 0 retries)

Sending RC frames at 50Hz...
Channels: All at 1500us (midpoint)
Telemetry display: ENABLED

[TELEM] ATTITUDE     (10 bytes): C8 08 1E 00 00 00 00 00 00 30
[TELEM] BATTERY      (12 bytes): C8 0A 08 00 00 00 00 00 00 00 00 6D
[TELEM] FLIGHT_MODE  ( 9 bytes): C8 07 21 21 45 52 52 00 31
[TELEM] VARIO        ( 6 bytes): C8 04 07 00 00 23
...

Sent 500 frames (50.1 Hz) | Received 534 telemetry frames
```

**Expected Summary (without --show-telemetry):**
```
======================================================================
SUMMARY
======================================================================
RC Frames Sent: 500 in 10.0 seconds (50.0 Hz avg)
Telemetry Received: 534 frames

Telemetry Frame Breakdown:
  ATTITUDE       :   90 frames
  BATTERY        :   89 frames
  FLIGHT_MODE    :   89 frames
  VARIO          :   89 frames
  UNKNOWN_0x09   :   88 frames
  UNKNOWN_0x0D   :   89 frames
======================================================================
```

### Step 5: Validate Results

**Frame Integrity Checks:**
- ✅ All frames have valid CRC8
- ✅ No "CRC FAIL" messages
- ✅ No "Invalid address" warnings
- ✅ Frame boundaries intact

**New Frame Detection (PR #11025):**
- ✅ AIRSPEED (0x0A) appears when pitot configured
- ✅ RPM (0x0C) appears when ESC telemetry active
- ✅ TEMPERATURE (0x0D) appears when temp sensors present
- ✅ BAROMETER (0x09) appears when baro active

**Test Missing Sensors:**
1. Disable pitot sensor in Configurator
2. Restart SITL
3. Verify AIRSPEED frame absent
4. Verify other frames still valid

---

## ✅ BREAKTHROUGH: CRSF Telemetry Works in SITL!

**Status:** CRSF telemetry is FULLY FUNCTIONAL in SITL without a simulator!

### Critical Discovery: RC Frames Must Be Sent FIRST

**The Issue:** CRSF telemetry appears broken until you understand the trigger mechanism.

**The Solution:** CRSF telemetry only transmits AFTER receiving RC frames!

**Why This Happens:**
- File: `src/main/rx/crsf.c:295-318` (`crsfRxSendTelemetryData`)
- CRSF is bidirectional on a single wire - telemetry timing is synchronized with RC reception
- Code waits for `crsfFrameStartAt` timing window between RC frames
- Without incoming RC frames, `crsfFrameStartAt` is never set
- Result: `telemetryBufLen` is written but never transmitted

**Correct Workflow:**
```bash
# Terminal 1 - Start SITL
./bin/SITL.elf

# Terminal 2 - Start RC sender FIRST (this is critical!)
python3 crsf_rc_sender.py 2 --rate 50

# Terminal 3 - NOW capture telemetry (works immediately!)
python3 capture_frames.py
```

**Test Results (PR #11025):**
```
✅ 200 frames captured successfully
✅ 0x07 VARIO - 40 frames
✅ 0x08 BATTERY - 40 frames
✅ 0x09 BAROMETER - 40 frames (PR #11025 VALIDATED!)
✅ 0x1E ATTITUDE - 40 frames
✅ 0x21 FLIGHT_MODE - 40 frames
```

### Sensors and Frame Generation

**Frame Schedule Logic:**
- File: `src/main/telemetry/crsf.c:668-697`
- Frames are conditionally generated based on `sensors()` function
- Missing frames = sensors not active (correct behavior!)

**PR #11025 Frames:**
- ✅ `0x09 BAROMETER` - Appears when `sensors(SENSOR_BARO)` true
- ⏸️ `0x0A AIRSPEED` - Needs `sensors(SENSOR_PITOT)` true
- ⏸️ `0x0C RPM` - Needs ESC telemetry active
- ⏸️ `0x0D TEMPERATURE` - Needs temp sensors configured

**To Test All Frames:** Need to enable fake sensors (see "Advanced Testing" below)

### Debug Logging with SD() Macro

Use `SD()` macro for SITL-only debug output:

```c
#include "build/debug.h"

SD(fprintf(stderr, "[DEBUG] Your message here\n"));
```

**Example** (from testing):
```c
// src/main/rx/crsf.c
SD(debugCallCount < 3 ? fprintf(stderr, "[CRSF TX] Sending %d bytes\n", telemetryBufLen) : 0);
```

This only compiles in SITL builds and outputs to stderr.

### Advanced Testing: Enabling Missing Sensors

**Current Status:** Working on fake sensor implementations

To test AIRSPEED, RPM, and TEMPERATURE frames:

**Option 1: Use External Simulator (X-Plane/RealFlight)**
```bash
./bin/SITL.elf --sim=xp  # X-Plane provides airspeed
```

**Option 2: Fake Sensor Injection (In Development)**
- Creating `fakeEscSetData()` for RPM testing
- Creating `fakeTempSetValue()` for temperature testing
- Already exists: `fakePitotSetAirspeed()` for airspeed

**Option 3: MSP Sensor Data (Limited)**
- `MSP2_SENSOR_AIRSPEED` (0x1F06) - ✅ Supported
- ESC/Temperature - ❌ No incoming MSP messages

---

## Configuration Details

### MSP Configuration Requirements

CRSF requires **three separate settings**:

1. **Receiver Type** (MSP_SET_RX_CONFIG byte 23):
   ```python
   RX_TYPE_SERIAL = 1
   ```

2. **Serial RX Provider** (MSP_SET_RX_CONFIG byte 0):
   ```python
   SERIALRX_CRSF = 6
   ```

3. **UART Function** (MSP2_COMMON_SET_SERIAL_CONFIG):
   ```python
   FUNCTION_RX_SERIAL = 0x40  # Bit 6
   ```

### EEPROM Persistence Sequence

**Critical:** MSP_REBOOT required after MSP_EEPROM_WRITE!

```python
# 1. Send configuration
board.send_RAW_msg(MSPCodes['MSP_SET_RX_CONFIG'], data=rx_config)
board.send_RAW_msg(MSPCodes['MSP2_COMMON_SET_SERIAL_CONFIG'], data=serial_config)

# 2. Save to EEPROM
board.send_RAW_msg(MSPCodes['MSP_EEPROM_WRITE'], data=[])
time.sleep(0.5)

# 3. REBOOT (creates eeprom.bin file)
board.send_RAW_msg(MSPCodes['MSP_REBOOT'], data=[])
time.sleep(15)  # Wait for SITL restart + EEPROM init
```

Without MSP_REBOOT, `eeprom.bin` file is not created.

---

## Troubleshooting

### Problem: SITL Won't Build

**Error:** `unrecognized option '--no-warn-rwx-segments'`

**Solution:**
```bash
# Edit cmake/sitl.cmake, comment lines 67-70
# OR use build-sitl skill
```

### Problem: Port 5761 Not Listening

**Possible Causes:**
1. CRSF not configured → Use Configurator GUI
2. SITL not restarted → Kill and restart SITL
3. Configuration not saved → Check eeprom.bin exists

**Check:**
```bash
ss -tlnp | grep 576
# Should see both 5760 (UART1/MSP) and 5761 (UART2/CRSF)
```

### Problem: No Telemetry Frames

**Causes:**
1. Not using bidirectional script → Use updated `crsf_rc_sender.py`
2. CRSF RX not initialized → Check SITL logs for `[CRSF TELEM] enabled=1`
3. Wrong port → Verify connecting to port 5761 (UART2)

**Debug:**
```bash
# Check SITL telemetry initialization
grep "CRSF TELEM" /tmp/sitl_bidirectional_test.log
# Expected: [CRSF TELEM] initCrsfTelemetry called, crsfRxIsActive=1, enabled=1

# Run with --show-telemetry to see frames in real-time
cd claude/developer/scripts/testing/inav/crsf
python3 crsf_rc_sender.py 2 --rate 50 --duration 10 --show-telemetry

# Check ports
ss -tlnp | grep 5761
# Expected: LISTEN on port 5761
```

### Problem: "Connection Refused" When Running Telemetry Reader

**Cause:** Trying to run separate RC sender and telemetry reader scripts

**Solution:**
- TCP ports accept only ONE client connection
- Use the bidirectional `crsf_rc_sender.py` (handles both RC and telemetry)
- See `TCP_CONNECTION_LIMITATION.md` for detailed explanation

### Problem: CRC Errors in Parser

**Cause:** Frame corruption or incorrect CRC implementation

**Validation:**
```bash
# CRC8 implementation validated against:
# - INAV src/main/common/crc.c:57-68
# - TBS CRSF specification
# - Multiple reference implementations
```

If seeing CRC errors, check for:
- Baud rate mismatches
- Buffer overflow in sender
- Network packet fragmentation

---

## Frame Reference

### CRSF RC Frame Structure

```
[Address: 0xC8] - Flight Controller
[Length: 24]    - Type(1) + Payload(22) + CRC(1)
[Type: 0x16]    - RC_CHANNELS_PACKED
[Payload: 22]   - 16 channels × 11 bits
[CRC8]          - DVB-S2 over Type + Payload
```

**Channel Encoding:**
- 11-bit range: 172-1811
- Midpoint (1500us): 992
- Formula: `value = (us - 1000) * 1.639 + 172`

### CRSF Telemetry Frames

**Baseline Frames (Always Present):**
- `0x02` GPS (15 bytes)
- `0x07` VARIO (2 bytes)
- `0x08` BATTERY (8 bytes)
- `0x1E` ATTITUDE (6 bytes)

**Conditional Frames (PR #11025):**
- `0x09` BAROMETER (2 bytes) - When baro sensor active
- `0x0A` AIRSPEED (2 bytes) - When pitot sensor active
- `0x0C` RPM (variable) - When ESC telemetry active
- `0x0D` TEMPERATURE (variable) - When temp sensors present

---

## File Locations

### Testing Scripts

**Current Location:**
```
$HOME/inavflight/claude/developer/scripts/testing/inav/crsf/
├── crsf_rc_sender.py              # Bidirectional RC sender + telemetry reader
├── crsf_stream_parser.py          # Telemetry frame parser and analyzer
├── configure_sitl_crsf.py         # MSP configuration for CRSF
├── test_crsf_telemetry.sh         # Automated comprehensive test
├── quick_test_crsf.sh             # Quick build-test cycle
├── analyze_frame_0x09.py          # Altitude/vario frame analyzer
└── test_telemetry_simple.py       # Simple telemetry test

$HOME/inavflight/claude/developer/scripts/testing/inav/docs/
└── TCP_CONNECTION_LIMITATION.md   # Important documentation about TCP constraints
```

### Build Artifacts

```
$HOME/inavflight/inav/build_sitl_pr11025/
├── bin/SITL.elf               # SITL binary
└── eeprom.bin                 # Configuration (32KB, created after config)
```

### Documentation

```
$HOME/inavflight/claude/developer/
└── crsf-sitl-testing-findings.md  # Detailed findings and lessons learned
```

---

## Related Skills

- **build-sitl** - Building SITL with troubleshooting
- **sitl-arm** - MSP-based SITL control and arming
- **run-configurator** - Starting INAV Configurator

---

## Quick Reference Commands

```bash
# Build SITL for PR
cd ~/Documents/planes/inavflight/inav
git fetch origin pull/XXXXX/head:pr-XXXXX-description
git checkout pr-XXXXX-description
mkdir build_sitl_prXXXXX && cd build_sitl_prXXXXX
cmake -DSITL=ON .. && make -j4

# Start SITL
./bin/SITL.elf 2>&1 | tee /tmp/sitl.log &
sleep 5

# Configure CRSF via MSP (automated)
cd ~/Documents/planes/inavflight/inav
python3 configure_crsf_proper_sequence.py 5760
sleep 10  # Wait for SITL reboot

# Test telemetry (bidirectional - sends RC, receives telemetry)
cd ~/Documents/planes/inavflight/claude/developer/scripts/testing/inav/crsf
python3 crsf_rc_sender.py 2 --rate 50 --duration 30 --show-telemetry

# Or without telemetry display (just summary)
python3 crsf_rc_sender.py 2 --rate 50 --duration 30
```

---

## References

- [TBS CRSF Specification](https://github.com/tbs-fpv/tbs-crsf-spec)
- [INAV SITL Documentation](https://github.com/iNavFlight/inav/blob/master/docs/SITL/SITL.md)
- INAV Source: `src/main/telemetry/crsf.c`
- INAV Source: `src/main/rx/crsf.c`
