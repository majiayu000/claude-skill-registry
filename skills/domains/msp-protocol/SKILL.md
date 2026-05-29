---
description: Look up MSP protocol commands, packet formats, and implementations
triggers:
  - msp protocol
  - msp command
  - lookup msp
  - what is MSP_
  - find msp command
  - msp packet format
  - search msp
  - msp definition
---

# MSP Protocol Reference

Look up MultiWii Serial Protocol (MSP) command definitions, packet structures, and implementations in INAV.

## MSP Packet Structure

All MSP packets follow this format:

```
Header: '$' 'M' '<'/'>'  (3 bytes)
Size:   payload length   (1 byte)
Command: MSP command ID  (1 byte)
Data:   command payload  (0-255 bytes)
CRC:    checksum         (1 byte)
```

**Direction indicators:**
- `$M<` - Request (to flight controller)
- `$M>` - Response (from flight controller)

**Minimum packet size:** 6 bytes (for commands with no data payload)

## Finding MSP Commands

### In Firmware (C code)

MSP commands are defined in:
- **Command IDs:** `inav/src/main/msp/msp_protocol.h`
- **Command handlers:** `inav/src/main/msp/msp.c`
- **Serial processing:** `inav/src/main/msp/msp_serial.c`

**Search for command definitions:**
```bash
grep "MSP_COMMAND_NAME" inav/src/main/msp/msp_protocol.h
```

**Search for command handlers:**
```bash
grep -r "MSP_COMMAND_NAME" inav/src/main/msp/
```

### In Configurator (JavaScript)

MSP commands are used in:
- **MSP client:** `inav-configurator/src/js/msp/`
- **MSP definitions:** `inav-configurator/src/js/msp.js` or similar
- **Tab implementations:** `inav-configurator/src/js/tabs/`

**Search for MSP usage:**
```bash
grep -r "MSP_COMMAND_NAME" inav-configurator/src/js/
```

### Python MSP Libraries

**RECOMMENDED: mspapi2**

The **mspapi2** library is the recommended Python MSP implementation for testing and automation.

**Location:** `mspapi2/` (or install from GitHub)
**GitHub:** https://github.com/xznhj8129/mspapi2

**Key features:**
- Clean separation: codec, transport, API, multi-client TCP server
- MSP packet encoding/decoding with strict validation
- Serial and TCP communication with robust error handling
- High-level API with typed getters/setters
- INAV enums for type-safe mission scripting
- Introspection tools for discovering message structure
- Useful for testing, scripting, automation, and multi-client scenarios
- Can communicate with both real hardware and SITL

**Installation:**
```bash
cd mspapi2
pip install .
# or editable install for development
pip install -e .
```

**Basic usage:**
```python
from mspapi2 import MSPApi

with MSPApi(port="/dev/ttyACM0", baudrate=115200) as api:
    info, version = api.get_api_version()
    print(f"API Version: {version['apiVersionMajor']}.{version['apiVersionMinor']}")
```

**Discovering message fields:**
```python
from examples.introspection import print_message_info
from mspapi2 import InavMSP

# Find out what fields a message has
print_message_info(InavMSP.MSP_ATTITUDE)
```

**Using messages without convenience methods:**
```python
from mspapi2 import MSPApi, InavMSP

with MSPApi(port="/dev/ttyACM0") as api:
    # Pack request
    request = api._pack_request(
        InavMSP.MSP2_INAV_LOGIC_CONDITIONS_SINGLE,
        {"conditionIndex": 0}
    )

    # Send and get reply
    info, reply = api._request(InavMSP.MSP2_INAV_LOGIC_CONDITIONS_SINGLE, request)
    print(f"Enabled: {reply['enabled']}")
```

**Documentation:**
- Getting Started: `mspapi2/docs/GETTING_STARTED.md`
- Flight Computer Guide: `mspapi2/docs/FLIGHT_COMPUTER.md`
- Discovering Fields: `mspapi2/docs/DISCOVERING_FIELDS.md`
- TCP Server: `mspapi2/docs/SERVER.md`
- Examples: `mspapi2/examples/`

**Contributing:**
If you encounter issues or see improvements needed in mspapi2, PRs are welcome at the GitHub repository!

**Alternative: uNAVlib (older)**

The **uNAVlib** library is the older Python MSP implementation, still available for backward compatibility.

**Location:** `uNAVlib/`
**GitHub:** https://github.com/xznhj8129/uNAVlib

Use this if you have existing scripts or need asyncio-based functionality. For new projects, prefer mspapi2.

See `claude/test_tools/inav/` for example scripts (some may use uNAVlib, consider updating to mspapi2).

## Common MSP Commands

| Command | ID | Purpose | Data Size |
|---------|-----|---------|-----------|
| MSP_IDENT | 100 | Board identification | 0 (request), 7 (response) |
| MSP_STATUS | 101 | Flight status | 0 (request), 11 (response) |
| MSP_ATTITUDE | 108 | Roll/pitch/yaw angles | 0 (request), 6 (response) |
| MSP_ALTITUDE | 109 | Altitude data | 0 (request), 10 (response) |
| MSP_ANALOG | 110 | Battery/current | 0 (request), 7 (response) |

## MSP Response Sizes

When investigating MSP issues, note that:
- Commands with `size=0` return no data payload (6-byte packet total)
- Most commands return small payloads (6-20 bytes typical)
- Large commands (settings, waypoints) can be 100+ bytes

## Debugging MSP

**Enable MSP debug logging in firmware:**

Edit `inav/src/main/msp/msp_serial.c` and add debug prints:
```c
fprintf(stderr, "[MSP_DEBUG] Command: %d, Size: %d\n", command, dataLen);
```

**Test MSP communication:**

Use the benchmark tools in `claude/test_tools/inav/`:
- `msp_benchmark_serial.py` - Test serial MSP
- `msp_benchmark_improved.py` - Test with detailed logging

Or use **mspapi2** for interactive testing and automation (recommended), or **uNAVlib** for legacy scripts.

## MSP Protocol Versions

- **MSP v1:** Original protocol (most common)
- **MSP v2:** Extended protocol with larger payloads and CRC32
- Check `msp_protocol.h` for version-specific commands

## Resources

- **Firmware MSP handlers:** `inav/src/main/msp/msp.c`
- **Protocol definitions:** `inav/src/main/msp/msp_protocol.h`
- **mspapi2 Python library (recommended):** `mspapi2/` - https://github.com/xznhj8129/mspapi2
- **uNAVlib Python library (older alternative):** `uNAVlib/` - https://github.com/xznhj8129/uNAVlib
- **Investigation notes:** `claude/msp_investigation_facts.md`
- **Test tools:** `claude/test_tools/inav/`

---

## Related Skills

- **sitl-arm** - Arm SITL using MSP protocol
- **build-sitl** - Build SITL firmware for MSP testing
- **find-symbol** - Find MSP command handlers and definitions in code
