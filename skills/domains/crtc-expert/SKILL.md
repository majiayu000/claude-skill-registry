---
name: crtc-expert
description: Expert on MC6845 CRTC for ES-1841 video timing. Provides guidance on video timing, cursor control, display addressing, V-Blank detection, and CGA register programming.
---

# CRTC Expert - MC6845 / KR1810VG85

Expert knowledge for the ES-1841's CRT controller.

## Key Specifications

| Property     | Value                      |
| ------------ | -------------------------- |
| Soviet Clone | KR1810VG85                 |
| I/O Ports    | `3D4h`/`3D5h` (index/data) |
| Registers    | R0-R17                     |
| Video RAM    | `B8000h`                   |

## I/O Ports

| Port   | Function            |
| ------ | ------------------- |
| `3D4h` | Index register (W)  |
| `3D5h` | Data register (R/W) |
| `3D8h` | Mode Control (W)    |
| `3D9h` | Color Select (W)    |
| `3DAh` | Status Register (R) |

## Key Registers

| Reg    | Name                 | 80×25 Value    |
| ------ | -------------------- | -------------- |
| R0     | Horizontal Total     | `71h`          |
| R1     | Horizontal Displayed | `50h`          |
| R4     | Vertical Total       | `1Fh`          |
| R6     | Vertical Displayed   | `19h`          |
| R9     | Max Scan Line        | `07h`          |
| R12-13 | Start Address        | Display offset |
| R14-15 | Cursor Address       | Cursor pos     |

## Status Register (`3DAh`)

| Bit | Function                      |
| --- | ----------------------------- |
| 0   | Display enable (1=retrace)    |
| 3   | **Vertical Sync** (1=V-Blank) |

> **CRITICAL**: ES-1841 BIOS hangs if V-Blank (bit 3) doesn't toggle correctly!

## V-Blank Timing

```text
V-Blank Start = R6 × (R9 + 1)
V-Blank End   = (R4 + 1) × (R9 + 1)
```

Status must update on **every read**.

## Mode Control (`3D8h`)

| Bit | Function                   |
| --- | -------------------------- |
| 0   | 80-column (1) / 40-col (0) |
| 1   | Graphics (1) / Text (0)    |
| 3   | Video enable               |
| 4   | Hi-res 640×200             |
| 5   | Blink enable               |

## References

- [references/implementation-guide.md](references/implementation-guide.md) - Complete CRTC/CGA implementation guide with code examples
- See [references/](references/) for detailed hardware documentation
