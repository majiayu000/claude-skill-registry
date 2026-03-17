---
name: pio-build
description: Use when the user asks to "build", "compile", "make", or test changes in a PlatformIO project, or after making code changes when the user wants to verify they work.
---

# PlatformIO Build

When building a PlatformIO project:

1. Run `pio run` to build the project
2. If there are compilation errors:
   - Parse the error messages
   - Show which files and lines have errors
   - Suggest fixes if possible
3. If build succeeds, show the firmware size (RAM/Flash usage)

If there are multiple environments in `platformio.ini`, ask which one to build or build all.

## Common Build Commands

```bash
pio run                    # Build default environment
pio run -e esp32dev        # Build specific environment
pio run -t clean           # Clean build
```

## RFC2217 Configuration

For remote upload/monitor via Serial Pi (RFC2217), add to `platformio.ini`:

```ini
upload_port = rfc2217://192.168.0.87:4001?ign_set_control
monitor_port = rfc2217://192.168.0.87:4001?ign_set_control
```

Check http://192.168.0.87:8080 for device port assignments.

## Error Handling

- Parse compiler errors and map to source files
- Check for missing libraries in `platformio.ini`
- Verify `lib_deps` are correctly specified
