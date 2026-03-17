---
name: idf-flash
description: Use when the user asks to "flash", "upload", "deploy", or "program" firmware to an ESP32 using ESP-IDF (not PlatformIO). Also use for "monitor" or "serial console" with ESP-IDF projects.
---

# ESP-IDF Flash

Flash firmware to ESP32 using ESP-IDF tools.

## Flash Size and Partition Tables

> **Flash size defaults to 4MB.** Use `CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y` in
> `sdkconfig.defaults` and `--flash_size 4MB` with esptool. Only use a
> different size when the actual flash is known (e.g. `esptool.py flash_id`
> or from the datasheet).

Partition tables must fit within the flash size. The test firmware provides
two layouts:

| File | Flash size | App partition size | Use when |
|------|-----------|-------------------|----------|
| `partitions-4mb.csv` | 4MB (default) | 1216K | Unknown or 4MB flash |
| `partitions.csv` | 8MB+ | 1536K | Flash confirmed > 4MB |

Set the partition table in `sdkconfig.defaults`:
```
CONFIG_PARTITION_TABLE_CUSTOM=y
CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions-4mb.csv"
```

## Local Flash (USB)

```bash
source /opt/esp-idf/export.sh
idf.py -p /dev/ttyUSB0 flash           # Flash to specific port
idf.py -p /dev/ttyUSB0 monitor         # Open serial monitor
idf.py -p /dev/ttyUSB0 flash monitor   # Flash and monitor
```

## Remote Flash (RFC2217)

For flashing via RFC2217 serial over network, use the `esp32-workbench-serial-flashing` skill which has detailed RFC2217 instructions, device discovery, and troubleshooting.

Quick reference (check http://192.168.0.87:8080 for current slot-to-port assignments):
```bash
export ESPPORT='rfc2217://192.168.0.87:4001?ign_set_control'
source /opt/esp-idf/export.sh
idf.py flash monitor
```

## Build Commands

```bash
source /opt/esp-idf/export.sh
idf.py build                           # Build only
idf.py flash                           # Build (if needed) and flash
idf.py fullclean                       # Clean build directory
```

## Boot Mode

To put ESP32 in bootloader mode:
1. Hold **BOOT** button
2. Press **RESET** button
3. Release **RESET**, then **BOOT**

## Monitor Shortcuts

- `Ctrl+]` - Exit monitor
- `Ctrl+T` `Ctrl+H` - Show help
- `Ctrl+T` `Ctrl+R` - Reset target

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Failed to connect | Enter boot mode (BOOT+RESET sequence) |
| No serial port found | Check USB cable, `ls /dev/ttyUSB*` |
| Permission denied | `sudo usermod -aG dialout $USER`, re-login |
