---
name: ram-expert
description: Expert on RAM subsystem for ES-1841. Provides guidance on memory map, DRAM refresh, parity checking, conventional memory layout, and BIOS data area.
---

# RAM Expert

Expert knowledge for the ES-1841's memory subsystem.

## Key Specifications

| Property | Value                 |
| -------- | --------------------- |
| Type     | DRAM with parity      |
| Capacity | 128 KB - 640 KB       |
| Width    | 8 data + 1 parity bit |
| Refresh  | DMA Ch0 + PIT Ch1     |

## Memory Map

| Address Range     | Size    | Description       |
| ----------------- | ------- | ----------------- |
| `00000h`-`003FFh` | 1 KB    | Interrupt Vectors |
| `00400h`-`004FFh` | 256 B   | BIOS Data Area    |
| `00500h`-`9FFFFh` | ~640 KB | Conventional RAM  |
| `A0000h`-`BFFFFh` | 128 KB  | Video RAM         |
| `C0000h`-`DFFFFh` | 128 KB  | ROM Extensions    |
| `F0000h`-`FFFFFh` | 64 KB   | System BIOS       |

## BIOS Data Area (BDA)

| Offset | Size | Description        |
| ------ | ---- | ------------------ |
| `0400` | 8    | COM port addresses |
| `0408` | 8    | LPT port addresses |
| `0413` | 2    | Memory size (KB)   |
| `0417` | 2    | Keyboard flags     |
| `046C` | 4    | Timer tick count   |

## DRAM Refresh

PIT Ch1 triggers DMA Ch0 every ~15 µs:

- Prevents data loss in DRAM
- Count = 18 at 1.19 MHz ≈ 15 µs

## Parity Checking

- 9th bit per byte (odd parity)
- Error triggers NMI
- Port `61h` bit 4: Enable check
- Port `62h` bit 7: Error flag

## References

See [references/](references/) for detailed documentation.
