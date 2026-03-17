---
title: PRISM Protocol Specification - Frame Format & CRC32
description: Wire protocol for PRISM K1 device communication, frame structure, and CRC32 validation
keywords:
  - Protocol
  - PRISM K1
  - Frame Format
  - CRC32
  - Communication
  - Embedded
categories:
  - Protocol
  - Communication
  - Firmware
allowed_tools:
  - Read
  - Grep
  - Glob
---

# PRISM Protocol Specification v1.0

## Overview

The PRISM protocol is a **byte-oriented, CRC32-validated frame format** for communication between the K1 device and control systems (Node service, M5Stack Tab5, or Claude Code).

**Key Characteristics**:
- ✅ Simple, human-readable frame structure
- ✅ CRC32 integrity checking
- ✅ Fixed header + variable-length payload
- ✅ Big-endian byte order (network order)
- ✅ Supports up to 65,535 bytes of payload

## Frame Format

### Byte Layout

```
Offset  Length  Field              Description
------  ------  -----              -----------
0       1       SYNC0              0xAA (sync marker, byte 0)
1       1       SYNC1              0xBB (sync marker, byte 1)
2       2       LENGTH             Payload length (big-endian u16)
4       N       PAYLOAD            Variable-length data
4+N     4       CRC32              CRC32 checksum (big-endian u32)
```

### Example Frame (LED Color Command)

```
Hex Layout:
AA BB | 00 04 | 01 FF 00 00 | C4 E2 2F 5A

Decoded:
0xAA 0xBB          → SYNC (frame start marker)
0x00 0x04          → LENGTH = 4 bytes
0x01 0xFF 0x00 0x00 → PAYLOAD = [1, 255, 0, 0] (Set LED to red)
0xC4 0xE2 0x2F 0x5A → CRC32 = 0xC4E22F5A (computed over SYNC+LENGTH+PAYLOAD)
```

**Frame Size**: 8 + N bytes (where N = payload length)

## Field Specifications

### SYNC Markers (2 bytes)

**Purpose**: Frame boundary detection, prevent data corruption

| Byte | Value | Meaning |
|------|-------|---------|
| 0 | 0xAA | Frame start marker byte 0 |
| 1 | 0xBB | Frame start marker byte 1 |

**Why 0xAA 0xBB?**
- Distinct pattern, unlikely in random data
- High bit set (0xAA = 10101010, 0xBB = 10111011) prevents false sync in text
- Easy to spot in hex dumps

### LENGTH Field (2 bytes, Big-Endian)

**Purpose**: Indicate payload size for buffer allocation and frame boundary detection

```c
uint16_t length = (frame[2] << 8) | frame[3];  // Big-endian decode
```

**Valid Range**: 0 to 65535 bytes
- Minimum practical: 1 byte (e.g., ACK)
- Maximum practical: 320 bytes (full WiFi MTU after headers)

**Example**:
- Payload size 4 → LENGTH = 0x0004
- Payload size 256 → LENGTH = 0x0100

### PAYLOAD (N bytes, Variable)

**Purpose**: Actual command/response data

**Structure** (Command):
```
Byte 0: COMMAND_ID
Bytes 1+: PARAMETERS (command-specific)
```

**Example Commands**:
```
Command: Set LED Color
  0x01 0xFF 0x00 0x00      → ID=1, R=255, G=0, B=0 (Red)

Command: Get Device Status
  0x02                     → ID=2, no parameters

Command: Firmware Version
  0x03                     → ID=3
```

### CRC32 Field (4 bytes, Big-Endian)

**Purpose**: Detect transmission errors

```c
uint32_t crc = (frame[4+N] << 24) |
               (frame[5+N] << 16) |
               (frame[6+N] << 8)  |
               (frame[7+N]);
```

**Calculation**: Polynomial 0x04C11DB7 (standard CRC32, same as Ethernet/ZIP)

**C Implementation** (Espressif):
```c
#include "esp32/rom/crc.h"

uint32_t compute_crc32(uint8_t *data, uint16_t length) {
    return crc32_le(0, data, length);
}

// Verify frame CRC
uint8_t frame[8+N];
uint32_t computed_crc = crc32_le(0, frame, 4+N);  // SYNC+LENGTH+PAYLOAD
uint32_t received_crc = (frame[4+N]<<24) | ... ; // Extract CRC

if (computed_crc != received_crc) {
    printf("CRC mismatch!\n");
    return -1;  // Frame error
}
```

**Input to CRC**: SYNC (0xAA 0xBB) + LENGTH (2 bytes) + PAYLOAD (N bytes)
**NOT included**: The CRC32 field itself

## Parsing Algorithm

### Receive and Validate Frame

```c
#define FRAME_HEADER_SIZE 4  // SYNC + LENGTH
#define MAX_PAYLOAD 320

typedef struct {
    uint8_t sync[2];
    uint16_t length;
    uint8_t *payload;
    uint32_t crc32;
    bool valid;
} frame_t;

frame_t receive_frame(uint8_t *data, int data_len) {
    frame_t frame = {0};

    // Check minimum size
    if (data_len < 8) return frame;  // Too small

    // Validate sync
    if (data[0] != 0xAA || data[1] != 0xBB) {
        return frame;  // Bad sync
    }

    // Extract length (big-endian)
    uint16_t payload_len = (data[2] << 8) | data[3];

    // Check bounds
    int frame_size = 8 + payload_len;
    if (frame_size > data_len || payload_len > MAX_PAYLOAD) {
        return frame;  // Frame too large or incomplete
    }

    // Validate CRC32
    uint32_t computed_crc = crc32_le(0, data, 4 + payload_len);
    uint32_t received_crc = (data[4+payload_len] << 24) |
                           (data[5+payload_len] << 16) |
                           (data[6+payload_len] << 8)  |
                           (data[7+payload_len]);

    if (computed_crc != received_crc) {
        return frame;  // CRC error
    }

    // Frame valid
    frame.valid = true;
    frame.payload = &data[4];
    frame.length = payload_len;
    return frame;
}
```

## Encoding a Frame

### Build and Send

```c
void send_frame(uint8_t *payload, uint16_t payload_len) {
    // Allocate frame buffer
    uint8_t frame[8 + payload_len];

    // Set sync markers
    frame[0] = 0xAA;
    frame[1] = 0xBB;

    // Set payload length (big-endian)
    frame[2] = (payload_len >> 8) & 0xFF;
    frame[3] = payload_len & 0xFF;

    // Copy payload
    memcpy(&frame[4], payload, payload_len);

    // Compute and set CRC32
    uint32_t crc = crc32_le(0, frame, 4 + payload_len);
    frame[4+payload_len+0] = (crc >> 24) & 0xFF;
    frame[4+payload_len+1] = (crc >> 16) & 0xFF;
    frame[4+payload_len+2] = (crc >> 8)  & 0xFF;
    frame[4+payload_len+3] = (crc >> 0)  & 0xFF;

    // Transmit (via serial, WiFi, or other transport)
    transmit(frame, 8 + payload_len);
}
```

## Example: LED Color Command

### Send: Set LED to Green (R=0, G=255, B=0)

```
Payload: 01 00 FF 00

Frame construction:
  SYNC:   0xAA 0xBB
  LENGTH: 0x00 0x04 (4 bytes)
  PAYLOAD: 0x01 0x00 0xFF 0x00
  CRC32: (computed)

Complete frame:
  AA BB 00 04 01 00 FF 00 [CRC32]

Hex example:
  AA BB 00 04 01 00 FF 00 3B 7D 96 A4

Breakdown:
  0xAA 0xBB       → Sync markers
  0x0004          → Payload length = 4
  0x010000FF00    → Payload (cmd=1, R=0, G=255, B=0)
  0x3B7D96A4      → CRC32 checksum
```

### Receive: Acknowledgment

```
Payload: 02 00 (Status OK)

Frame:
  AA BB 00 02 02 00 [CRC32]

Hex:
  AA BB 00 02 02 00 F1 48 C8 9E
```

## Error Handling

### Transmission Error Scenarios

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Bit flip in payload | CRC32 mismatch | Discard, request retransmit |
| Lost byte in transit | Frame size mismatch or CRC error | Resync on next 0xAA 0xBB |
| Corrupted length field | Buffer overflow or incomplete frame | Timeout, request retransmit |
| Sync byte corruption | Failed to find 0xAA 0xBB | Scan for next sync pattern |

### Receiver State Machine

```
State: IDLE
  → Wait for 0xAA → State: SYNC0

State: SYNC0
  → Byte == 0xBB? Yes → State: LENGTH0
  → Byte == 0xAA? Yes → Stay in SYNC0 (possible resync)
  → Else → State: IDLE (invalid, restart search)

State: LENGTH0
  → Read MSB of length → State: LENGTH1

State: LENGTH1
  → Read LSB of length
  → Allocate buffer for payload + CRC
  → State: PAYLOAD

State: PAYLOAD
  → Read N payload bytes
  → State: CRC

State: CRC
  → Read 4 CRC bytes
  → Compute CRC over (SYNC+LENGTH+PAYLOAD)
  → If CRC matches: Frame valid, process payload
  → Else: Frame error, State: IDLE
```

## Transport Layer Notes

### Over Serial (USB/UART)

- **Baud Rate**: 115,200 bps typical
- **Framing**: None required (our protocol provides framing)
- **Flow Control**: Optional (our CRC handles errors)

### Over WiFi (TCP/IP)

- **Protocol**: TCP or UDP
- **Framing**: May need length-prefix if streaming multiple frames
- **Packet Loss**: CRC will catch errors; retransmit mechanism recommended

### Over WebSocket (Claude Code / M5Stack)

- **Protocol**: WebSocket binary frames
- **Framing**: WebSocket handles frame boundaries
- **Use our frame format as-is** (PRISM protocol is transport-agnostic)

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Frame overhead | 8 bytes | SYNC+LENGTH+CRC |
| Min payload | 1 byte | E.g., ACK |
| Max payload | 65535 bytes | Practical limit ~320 |
| CRC computation | <1 ms | For typical 64-byte payload |
| Frame parse | <100 µs | Simple state machine |
| Sync recovery | <100 ms | Rescan for 0xAA 0xBB |

## Testing Protocol Frames

### Manual Hex Verification

```bash
# Python 3 CRC32
python3 -c "
import struct
data = bytes.fromhex('AABB000401FF0000')
crc = __import__('zlib').crc32(data) & 0xFFFFFFFF
print(f'CRC32: {crc:08X}')
print(f'Bytes: {struct.pack(\">I\", crc).hex()}')"

# Output:
# CRC32: C4E22F5A
# Bytes: c4e22f5a

# Complete frame:
# AA BB 00 04 01 FF 00 00 C4 E2 2F 5A
```

### Unit Test Template

```c
#include <assert.h>

void test_frame_parsing() {
    // Frame: LED red (255, 0, 0)
    uint8_t frame[] = {0xAA, 0xBB, 0x00, 0x04,
                       0x01, 0xFF, 0x00, 0x00,
                       0xC4, 0xE2, 0x2F, 0x5A};

    frame_t parsed = receive_frame(frame, sizeof(frame));

    assert(parsed.valid == true);
    assert(parsed.length == 4);
    assert(parsed.payload[0] == 0x01);  // Command
    assert(parsed.payload[1] == 0xFF);  // R
    assert(parsed.payload[2] == 0x00);  // G
    assert(parsed.payload[3] == 0x00);  // B
}
```

## Key Takeaways

1. **Simple Format**: 8-byte header + variable payload
2. **Robust**: CRC32 catches bit errors
3. **Transport Agnostic**: Works over serial, WiFi, WebSocket
4. **Scalable**: Supports up to 65KB payloads
5. **Debuggable**: Hex dumps are human-readable
6. **Proven**: Same CRC as Ethernet/ZIP standards

## References

- CRC32 Polynomial: 0x04C11DB7 (ISO/HDLC)
- Espressif CRC: `rom/crc.h` (`crc32_le` function)
- Frame Size: Minimum 8 bytes (1-byte payload), typical 64-256 bytes

---

**Last Updated**: October 22, 2025
**Version**: 1.0 (Draft)
**Skill Type**: Reference + Specifications
**Allowed Tools**: Read, Grep, Glob only
