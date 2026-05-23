---
description: Profile INAV firmware performance by measuring CPU usage at specific code points
triggers:
  - profile fc
  - profile performance
  - measure cpu usage
---

# Profile Flight Controller Performance

**Purpose:** Profile INAV firmware performance by measuring CPU usage at specific code points.

**Method:** Early return profiling - insert `return` statements at key points and measure task execution times.

---

## Overview

This skill helps profile where CPU time is being spent in INAV firmware by:
1. Adding `return;` statements at specific profiling points in the code
2. Building and flashing modified firmware
3. Running the `tasks` CLI command to capture CPU usage
4. Comparing results across different profiling points

---

## Prerequisites

- Flight controller connected via USB
- Access to `/dev/ttyACM0` (or appropriate serial port)
- `fc-cli.py` script available at `.claude/skills/flash-firmware-dfu/fc-cli.py`
- `arm-none-eabi-objcopy` and `dfu-util` installed

---

## Basic Profiling Workflow

### Step 1: Identify Profiling Points

Choose where to insert profiling returns. Common locations:

**Main PID Loop** (`src/main/fc/fc_core.c::taskMainPidLoop`):
- After `gyroFilter()` - ~line 937
- After `imuUpdateAccelerometer()` - ~line 941
- After `imuUpdateAttitude()` - ~line 944
- After `updatePositionEstimator()` - ~line 972

**Position Estimator** (`src/main/navigation/navigation_pos_estimator.c::updateEstimatedTopic`):
- After `estimationCalculateAGL()` - ~line 750
- After `estimationPredict()` - ~line 754
- After `estimationCalculateCorrection_Z()` - ~line 758
- After `estimationCalculateCorrection_XY_GPS()` - ~line 766

### Step 2: Add Profiling Return

**CRITICAL:** Comment out any `return` statements BEFORE your profiling point!

```c
// Example: Profile after imuUpdateAttitude()

gyroFilter();
// return;  // ← MUST comment out earlier returns!

imuUpdateAccelerometer();
// return;  // ← MUST comment out earlier returns!

imuUpdateAttitude(currentTimeUs);
return;  // ← Your profiling point

updatePositionEstimator();
// ... rest of function won't execute
```

**Common Pitfall:** Forgetting to comment out earlier returns will cause profiling to exit too early, showing unexpectedly low CPU usage.

### Step 3: Build Firmware

```bash
cd $HOME/inavflight/inav/build
make TARGETNAME  # e.g., make JHEMCUF435
```

Build time: ~30-60 seconds for incremental builds.

### Step 4: Convert Hex to Bin

DFU-util requires `.bin` format, but make produces `.hex`:

```bash
cd $HOME/inavflight/inav
HEX=$(ls build/inav_*TARGETNAME*.hex | head -1)
BIN="${HEX%.hex}.bin"
arm-none-eabi-objcopy -I ihex -O binary "$HEX" "$BIN"
```

### Step 5: Reboot FC to DFU Mode

```bash
$HOME/inavflight/.claude/skills/flash-firmware-dfu/fc-cli.py dfu /dev/ttyACM0
```

**Wait 2-3 seconds** for FC to enter DFU mode before flashing.

**Note:** The script may show "⚠ WARNING: DFU device not detected" but DFU often works anyway. Verify with `dfu-util -l`.

### Step 6: Flash Firmware

```bash
cd /home/raymoris/Documents/planes/inavflight/inav/build
dfu-util -d 2e3c:df11 --alt 0 -s 0x08000000:force:leave -D inav_VERSION_TARGETNAME.bin
```

Look for: "Download done."

Flash time: ~10-15 seconds.

### Step 7: Capture Tasks Output

**Wait 5 seconds** for FC to reboot, then:

```bash
$HOME/inavflight/.claude/skills/flash-firmware-dfu/fc-cli.py tasks /dev/ttyACM0
```

### Step 8: Record Results

Look for the **PID task** line:

```
 1 -          PID    1968      36      13    7.5%    3.0%       664
                              ↑       ↑      ↑       ↑
                           max/us  avg/us  maxload avgload
```

Record: `maxload%` and `avgload%`

Example: "After imuUpdateAttitude(): 42.3% max, 15.5% avg"

---

## Full Profiling Cycle Script

Save this as `profile-one-point.sh`:

```bash
#!/bin/bash
# Usage: ./profile-one-point.sh TARGETNAME "Description of profiling point"

TARGET="$1"
DESCRIPTION="$2"

if [ -z "$TARGET" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 TARGETNAME \"Description\""
    exit 1
fi

INAV_ROOT="$HOME/inavflight/inav"
FC_CLI="$HOME/inavflight/.claude/skills/flash-firmware-dfu/fc-cli.py"

echo "=== Profiling: $DESCRIPTION ==="
echo ""

# Build
echo "Building $TARGET..."
cd "$INAV_ROOT/build" || exit 1
make "$TARGET" || exit 1

# Convert
echo "Converting hex to bin..."
cd "$INAV_ROOT" || exit 1
HEX=$(ls build/inav_*${TARGET}*.hex | grep -v "AIO\|noAF" | head -1)
BIN="${HEX%.hex}.bin"
arm-none-eabi-objcopy -I ihex -O binary "$HEX" "$BIN"

# Reboot to DFU
echo "Rebooting to DFU..."
"$FC_CLI" dfu /dev/ttyACM0 > /dev/null 2>&1
sleep 3

# Flash
echo "Flashing firmware..."
cd "$INAV_ROOT/build" || exit 1
dfu-util -d 2e3c:df11 --alt 0 -s 0x08000000:force:leave -D "$(basename $BIN)" 2>&1 | grep -E "Download done"

# Wait and run tasks
echo "Waiting for reboot..."
sleep 5
echo ""
echo "=== TASKS OUTPUT ==="
"$FC_CLI" tasks /dev/ttyACM0

echo ""
echo "=== Profiling Point: $DESCRIPTION ==="
echo "Record the PID task maxload% and avgload% values above"
```

Make it executable:
```bash
chmod +x profile-one-point.sh
```

Usage:
```bash
./profile-one-point.sh JHEMCUF435 "After imuUpdateAttitude()"
```

---

## Timing Recommendations

Based on empirical testing:

| Operation | Recommended Wait Time |
|-----------|----------------------|
| After `fc-cli.py dfu` | 2-3 seconds |
| After `dfu-util` flash | 5 seconds |
| Before running `tasks` | FC must be fully booted |

**Tip:** If `tasks` command fails with serial port error, wait 2 more seconds and try again.

---

## Common Pitfalls

### 1. Early Return Not Commented Out ⚠️

**Symptom:** Unexpectedly low CPU usage (e.g., 7.5% when expecting 40%+)

**Cause:** An earlier `return;` statement is still active, causing profiling to exit before reaching your intended point.

**Solution:** Carefully review ALL code between function start and your profiling point. Comment out any `return;` statements.

**Example of the problem:**
```c
void taskMainPidLoop() {
    gyroFilter();
    return;  // ← This is still active!

    // Your code never reaches here...
    imuUpdateAttitude();
    return;  // ← Your intended profiling point never executes
}
```

### 2. Wrong Target Built

**Symptom:** Firmware flashes but doesn't boot, or shows unexpected behavior.

**Cause:** Built wrong target (e.g., built JHEMCUF435 but Blueberry FC is connected).

**Solution:** Always verify target name matches connected FC.

### 3. FC Not in DFU Mode

**Symptom:** `dfu-util` reports "No DFU capable USB device available"

**Cause:** FC didn't enter DFU mode, or exited DFU mode.

**Solution:**
- Run `fc-cli.py dfu` again
- Wait 2-3 seconds
- Verify with `dfu-util -l` before flashing

### 4. Profiling Function That's Not Called

**Symptom:** No change in CPU usage when profiling point is moved.

**Cause:** The function containing the profiling return might not be called (e.g., no GPS → GPS correction functions don't run).

**Solution:** Check if the function is actually executing. Add debug output or check sensor state.

---

## Profiling Results Template

Use this template to record results:

```markdown
# Profiling Results: [TARGET] - [Date]

## Configuration
- Target: TARGETNAME
- Profiling area: [e.g., "Position Estimator"]
- File: [e.g., "navigation_pos_estimator.c"]
- Function: [e.g., "updateEstimatedTopic()"]

## Results

| Profiling Point | Max CPU | Avg CPU | Notes |
|----------------|---------|---------|-------|
| After [function1] | XX.X% | XX.X% | [Any observations] |
| After [function2] | XX.X% | XX.X% | |
| After [function3] | XX.X% | XX.X% | |

## Analysis

[What you learned from these measurements]

## Next Steps

[What to profile next]
```

---

## Comparing Multiple FCs

When comparing performance between FCs:

1. **Use identical profiling points** (same line numbers, same functions)
2. **Document GPS state** (locked vs no signal)
3. **Document sensor state** (baro detected, mag detected, etc.)
4. **Record both max and avg** CPU percentages
5. **Note environmental differences** (indoor vs outdoor, moving vs stationary)

---

## Example: Comparing JHEMCU vs Blueberry

See `claude/developer/profiling-comparison-granular.md` for a complete example of:
- Multiple profiling points
- Side-by-side comparison
- Analysis of differences
- Next steps based on findings

---

## Files Referenced

- **fc-cli.py:** `.claude/skills/flash-firmware-dfu/fc-cli.py`
- **Example comparisons:** `claude/developer/profiling-comparison-granular.md`
- **Evidence log:** `claude/developer/hardware-comparison-evidence.md`
- **Investigation summary:** `claude/developer/investigation-summary.md`

---

## Cleanup After Profiling

**IMPORTANT:** Remember to remove or comment out profiling returns before committing code!

```bash
# Check for profiling returns in tracked files
cd inav
git diff | grep -n "return;.*Profile point"
```

---

## Advanced: Profiling Interrupt Handlers

**Limitation:** Early return profiling doesn't work well for interrupt handlers or interrupt service routines (ISRs).

**Reasons:**
1. ISRs must complete their critical work (acknowledge interrupts, clear flags, etc.)
2. Early returns would prevent cleanup code from running, potentially breaking the system
3. ISRs need to be kept minimal anyway - use hardware timers for ISR profiling instead

**For ISR profiling:** Use GPIO toggles + logic analyzer, or DWT cycle counter measurements.
