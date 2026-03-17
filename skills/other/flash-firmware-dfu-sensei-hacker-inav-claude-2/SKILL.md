---
description: Flash INAV firmware to flight controllers using DFU (Device Firmware Update)
triggers:
  - flash firmware
  - flash dfu
  - dfu flash
  - flash flight controller
  - flash hex file
  - upload firmware
  - dfu-util
  - flash inav
---

# Flashing INAV Firmware via DFU

## IMPORTANT: Use the fc-flasher Agent

**When this skill is invoked, you MUST immediately use the Task tool with `subagent_type=fc-flasher`.**

The `fc-flasher` agent handles:
- Automatic settings backup and restore
- MSP reboot to DFU mode
- Hex to bin conversion
- DFU flashing
- Verification

**Example:**
```
User: "Flash inav_9.0.0_MATEKF405.hex"
Assistant: [Immediately calls Task tool with subagent_type=fc-flasher and the hex file path]
```

**Do NOT use manual DFU steps unless the fc-flasher agent fails or you're troubleshooting.**

---

# Manual DFU Flashing (Troubleshooting Only)

The information below is for troubleshooting when the automated agent doesn't work.

## Prerequisites

Install dfu-util:

```bash
# Ubuntu/Debian
sudo apt install dfu-util

# Fedora
sudo dnf install dfu-util

# Arch
sudo pacman -S dfu-util

# Or download from source
# http://sourceforge.net/p/dfu-util
```

You'll also need objcopy (part of binutils, usually pre-installed):

```bash
# If needed, install gcc-arm-none-eabi or binutils
sudo apt install binutils-arm-none-eabi  # Ubuntu/Debian
```

## Step 1: Put Flight Controller into DFU Mode

Choose **ONE** of the following methods:

### Method A: Hardware Button
Press and hold the DFU/BOOT button on the board while plugging in USB.

### Method B: Serial Command (Recommended: Use Helper Script)

**Using the helper script (RECOMMENDED):**

```bash
# Python version (requires pyserial)
.claude/skills/flash-firmware-dfu/reboot-to-dfu.py /dev/ttyACM0

# Install pyserial if needed:
pip3 install pyserial
```

**Manual method (not recommended - race condition):**

The correct sequence requires waiting for the actual CLI prompt, not just a fixed delay:

1. Send `####\r\n` to enter CLI mode
2. **Read from serial and wait for "CLI" string in response** (timeout: 2 seconds)
3. Only after receiving CLI prompt: send `dfu\r\n`
4. Disconnect

**Why simple echo + sleep doesn't work:**
```bash
# DON'T DO THIS - race condition!
echo -ne '####\r\n' > /dev/ttyACM0
sleep 0.25  # Wrong! Doesn't wait for actual CLI prompt
echo -ne 'dfu\r\n' > /dev/ttyACM0
```

This fails because:
- It blindly sleeps without checking if CLI is ready
- If the FC takes >250ms to respond, the `dfu` command is sent too early
- The helper scripts properly wait for the "CLI" prompt before sending `dfu`

### Method C: CLI Command
Connect with INAV Configurator or serial terminal and type:
```
dfu
```

### Method D: MSP Reboot Command (INAV 9.x+)

**Using MSP to reboot to DFU (most reliable programmatic method):**

```python
# Using mspapi2
from mspapi2 import MSPSerial

serial = MSPSerial("/dev/ttyACM0", 115200)
serial.open()

# Send MSP_REBOOT (68) with DFU parameter (1)
code, payload = serial.request(68, b'\x01')

serial.close()

# Wait for reboot
import time
time.sleep(2)
```

This is the most reliable programmatic method because it:
- Doesn't require CLI prompt timing
- Works through the MSP protocol
- Is supported by configurator and tools
- Provides proper backwards compatibility

**Parameter values:**
- `b'\x00'` or empty = normal reboot
- `b'\x01'` = reboot to DFU mode

## Step 2: Verify DFU Mode

Check that the device is in DFU mode:

```bash
dfu-util -l
```

You should see a device with ID `0483:df11`.

## Step 3: Convert HEX to BIN

DFU requires binary format, so convert the `.hex` file:

```bash
cd inav/build
objcopy -I ihex inav_x.y.z_TARGETNAME.hex -O binary inav_x.y.z_TARGETNAME.bin
```

Example:
```bash
objcopy -I ihex inav_8.0.0_MATEKF405.hex -O binary inav_8.0.0_MATEKF405.bin
```

## Step 4: Flash the Firmware

```bash
dfu-util -d 0483:df11 --alt 0 -s 0x08000000:force:leave -D inav_x.y.z_TARGETNAME.bin
```

Example:
```bash
dfu-util -d 0483:df11 --alt 0 -s 0x08000000:force:leave -D inav_8.0.0_MATEKF405.bin
```

### Command Breakdown:
- `-d 0483:df11` - Target device ID (STM32 DFU)
- `--alt 0` - Alternative setting (default flash memory)
- `-s 0x08000000` - Start address (STM32 flash base)
- `:force` - Force write even if non-blank
- `:leave` - Exit DFU mode and run firmware after flashing
- `-D <file>` - Binary file to flash

## Step 5: Verify

After flashing completes, the flight controller should automatically reboot and run the new firmware.

Connect with INAV Configurator to verify the version.

## Complete Example Workflow

```bash
# 1. Build the firmware
cd inav/build
make MATEKF405

# 2. Put flight controller in DFU mode
# Option A: Hardware button (press BOOT button while plugging USB)
# Option B: Serial command (use helper script)
../.claude/skills/flash-firmware-dfu/reboot-to-dfu.py /dev/ttyACM0

# 3. Verify DFU mode
dfu-util -l

# 4. Convert hex to bin
objcopy -I ihex inav_8.0.0_MATEKF405.hex -O binary inav_8.0.0_MATEKF405.bin

# 5. Flash
dfu-util -d 0483:df11 --alt 0 -s 0x08000000:force:leave -D inav_8.0.0_MATEKF405.bin
```

## Automated Script

For repeated flashing during development:

```bash
#!/bin/bash
# flash-firmware.sh

TARGET="MATEKF405"
SERIAL_PORT="/dev/ttyACM0"
HEX_FILE="inav_*.${TARGET}.hex"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Put FC into DFU mode using helper script
echo "Entering DFU mode..."
if ! $SCRIPT_DIR/.claude/skills/flash-firmware-dfu/reboot-to-dfu.py $SERIAL_PORT; then
    echo "ERROR: Failed to enter DFU mode!"
    exit 1
fi

# Note: Helper script already waits and verifies DFU mode

# Convert to bin
echo "Converting hex to bin..."
objcopy -I ihex $HEX_FILE -O binary ${HEX_FILE%.hex}.bin

# Flash
echo "Flashing firmware..."
dfu-util -d 0483:df11 --alt 0 -s 0x08000000:force:leave -D ${HEX_FILE%.hex}.bin

echo "Flash complete!"
```

Usage:
```bash
chmod +x flash-firmware.sh
./flash-firmware.sh
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No DFU capable USB device found` | Ensure board is in DFU mode, try different USB cable/port |
| `Permission denied` | Add udev rules or use `sudo` |
| `Cannot open DFU device` | Check that no other program is accessing the device |
| Flash succeeds but board doesn't boot | Wrong target or corrupted file - reflash |
| Hardware doesn't work after flashing (gyro not detected, etc.) | May be target configuration issue - use **target-developer** agent |

### udev Rules (Avoid sudo)

Create `/etc/udev/rules.d/45-stm32dfu.rules`:

```
# STM32 DFU Bootloader
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0664", GROUP="plugdev"
```

Then reload:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Add your user to the plugdev group:
```bash
sudo usermod -a -G plugdev $USER
```

Log out and back in for group changes to take effect.

## Alternative Methods

### INAV Configurator (GUI)
1. Open INAV Configurator
2. Click "Firmware Flasher"
3. Select "Load Firmware [Local]"
4. Browse to your `.hex` file
5. Click "Flash Firmware"

### msp-tool (Command Line)
```bash
# Install msp-tool
go install github.com/fiam/msp-tool@latest

# Flash
msp-tool flash --port /dev/ttyACM0 inav_x.y.z_TARGETNAME.hex
```

### flash.sh
See [mwptools documentation](https://github.com/stronnag/mwptools/blob/master/docs/MiscTools.asciidoc#flashsh)

## Safety Notes

- **ALWAYS** verify you're flashing the correct target for your hardware
- **Backup** your settings using CLI `dump` command before flashing
- **Double-check** file paths and target names
- Keep a known-good firmware hex file as backup

## CLI Command Tools

This skill includes Python scripts for sending commands to the flight controller via CLI:

### fc-cli.py - Modular CLI Command Tool

Send any CLI command to the flight controller:

```bash
# Show task execution times (useful for performance analysis)
.claude/skills/flash-firmware-dfu/fc-cli.py tasks

# Show firmware version
.claude/skills/flash-firmware-dfu/fc-cli.py version

# Show flight controller status
.claude/skills/flash-firmware-dfu/fc-cli.py status

# Reboot to DFU mode
.claude/skills/flash-firmware-dfu/fc-cli.py dfu

# Send any custom CLI command
.claude/skills/flash-firmware-dfu/fc-cli.py "get gyro_lpf1_static_hz"

# Specify custom serial port
.claude/skills/flash-firmware-dfu/fc-cli.py tasks /dev/ttyUSB0
```

**Available built-in commands:**
- `dfu` - Reboot to DFU bootloader mode
- `tasks` - Show task execution times
- `status` - Show flight controller status
- `version` - Show firmware version
- Any other CLI command - just pass it as an argument

**How it works:**
1. Opens serial connection to flight controller
2. Enters CLI mode by sending `####\r\n`
3. Waits for "CLI" prompt (with timeout)
4. Sends your command
5. Reads and displays the response (except for `dfu` which disconnects)

**Adding new commands:**
Edit `fc-cli.py` and add to the `COMMANDS` dictionary:

```python
COMMANDS = {
    'mycommand': {
        'handler': lambda cli: cmd_generic(cli, 'mycommand'),
        'description': 'Description of my command',
        'read_response': True,
    },
}
```

### reboot-to-dfu.py - Simple DFU Reboot

Simple standalone script that only reboots to DFU mode (equivalent to `fc-cli.py dfu`):

```bash
.claude/skills/flash-firmware-dfu/reboot-to-dfu.py [port]
```

Use `fc-cli.py` for new work - it's more flexible.

## USB Debugging

When USB MSC (mass storage) or CDC (serial) modes have issues, see:
`claude/developer/docs/debugging/usb-msc-debugging.md`

Quick commands:
```bash
lsusb -v | grep -A20 "STM"
dmesg | tail -50
cat /sys/bus/usb/devices/*/product
```

## Related Skills and Agents

**Skills:**
- **build-inav-target** - Build firmware before flashing
- **build-sitl** - Test changes in SITL before flashing hardware
- **msp-protocol** - MSP protocol reference

**Agents:**
- **fc-flasher** - Automated flashing with settings preservation (RECOMMENDED)
- **inav-builder** - Build firmware for targets
- **target-developer** - Fix target configuration issues if hardware doesn't work after flashing

## References

- Full documentation: `inav/docs/development/Building in Linux.md`
- USB debugging: `claude/developer/docs/debugging/usb-msc-debugging.md`
