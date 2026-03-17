---
name: pio-upload
description: Use when the user asks to "upload", "flash", "deploy", or "program" firmware to an ESP32 or other microcontroller in a PlatformIO project.
---

# PlatformIO Upload

When uploading firmware to a device:

1. First check for connected devices:
   - Local: `pio device list`
   - Remote (RFC2217): Check web portal at http://192.168.0.87:8080
2. If no device found, inform user and suggest checking USB connection or RFC2217 portal
3. Run `pio run -t upload`
4. If upload fails:
   - Check if the correct port is configured in `platformio.ini`
   - Suggest putting ESP32 in bootloader mode (hold BOOT, press RESET)
   - Check permissions on the serial port
5. If upload succeeds, optionally start the serial monitor

## RFC2217 Remote Upload (Preferred)

For remote serial access via the Serial Pi (192.168.0.87), use RFC2217:

```ini
# platformio.ini
upload_port = rfc2217://192.168.0.87:4000?ign_set_control
monitor_port = rfc2217://192.168.0.87:4000?ign_set_control
```

Or via command line:
```bash
pio run -t upload --upload-port 'rfc2217://192.168.0.87:4000?ign_set_control'
pio device monitor --port 'rfc2217://192.168.0.87:4000?ign_set_control'
```

**Port Assignment:**
- Port 4000: First RFC2217 device
- Port 4001: Second RFC2217 device
- Check http://192.168.0.87:8080 for current port assignments

## Local Upload Commands

```bash
pio run -t upload              # Upload to default environment
pio run -e esp32dev -t upload  # Upload to specific environment
pio device monitor             # Open serial monitor after upload
pio run -t upload && pio device monitor  # Upload and monitor
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No device found | USB not connected | Check USB cable, try different port |
| Permission denied | Missing dialout group | `sudo usermod -a -G dialout $USER` |
| Upload timeout | Not in bootloader mode | Hold BOOT while pressing RESET, retry |
| Connection refused (RFC2217) | Server not running | Check portal; verify device in RFC2217 mode |
| Timeout during flash (RFC2217) | Network latency | Use `--no-stub` flag; check network |
| Port busy (RFC2217) | Another connection active | Close other terminal/tool |
