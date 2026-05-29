---
name: bios-expert
description: Expert on ROM/BIOS for ES-1841. Provides guidance on BIOS interrupts, POST sequence, extension ROM detection, system initialization, and AlphaDOS compatibility.
---

# BIOS Expert

Expert knowledge for the ES-1841's ROM/BIOS subsystem.

## Key Specifications

| Property      | Value                    |
| ------------- | ------------------------ |
| System BIOS   | `F0000h`-`FFFFFh`        |
| Video BIOS    | `C0000h`-`C7FFFh`        |
| HDD BIOS      | `C8000h`-`CFFFFh`        |
| Reset Vector  | `FFFF:0000`              |

## BIOS Interrupts

| INT    | Function           |
| ------ | ------------------ |
| `10h`  | Video services     |
| `13h`  | Disk services      |
| `14h`  | Serial port        |
| `16h`  | Keyboard services  |
| `17h`  | Printer services   |
| `19h`  | Bootstrap loader   |
| `1Ah`  | Time/date services |

## Extension ROM Detection

BIOS scans `C0000h`-`DFFFFh`:

```text
If [addr]=55h, [addr+1]=AAh:
    Size = [addr+2] × 512
    Verify checksum
    FAR CALL [addr+3]
```

## POST Sequence

1. CPU test
2. ROM checksum
3. DMA controller
4. Timer
5. Memory test
6. Keyboard init
7. Video init
8. Extension ROMs
9. Equipment check
10. Boot

> **WARNING**: ES-1841 BIOS is "extremely thorough and unforgiving"

## Critical Requirements

- V-Blank must toggle (port `3DAh` bit `3`)
- Timer interrupt at `18.2` Hz
- Keyboard must respond

## AlphaDOS

Russified MS-DOS 3.x:

- Russian commands
- `F11`/`F12` keyboard switching

## References

See [references/](references/) for detailed documentation.
