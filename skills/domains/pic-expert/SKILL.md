---
name: pic-expert
description: Expert on Intel 8259A Programmable Interrupt Controller for ES-1841. Provides guidance on hardware interrupts, IRQ handling, interrupt masking, EOI commands, and priority resolution.
---

# PIC Expert - Intel 8259A / KR1810VN59

Expert knowledge for the ES-1841's interrupt controller.

## Key Specifications

| Property     | Value                      |
| ------------ | -------------------------- |
| Soviet Clone | KR1810VN59                 |
| IRQ Lines    | 8 (IR0-IR7)                |
| I/O Ports    | `20h`, `21h`               |
| Vector Base  | `08h` (IRQ0 → INT 08h)     |
| Mode         | Single PIC, edge-triggered |

## I/O Ports

| Port  | Write              | Read             |
| ----- | ------------------ | ---------------- |
| `20h` | ICW1, OCW2, OCW3   | IRR/ISR via OCW3 |
| `21h` | ICW2-4, OCW1 (IMR) | IMR              |

## Internal Registers

- **IRR** - Interrupt Request Register (pending requests)
- **ISR** - In-Service Register (currently handling)
- **IMR** - Interrupt Mask Register (1 = masked)

## IRQ Assignments (ES-1841)

| IRQ | Vector | Device       |
| --- | ------ | ------------ |
| 0   | `08h`  | System Timer |
| 1   | `09h`  | Keyboard     |
| 5   | `0Dh`  | Hard Disk    |
| 6   | `0Eh`  | Floppy Disk  |
| 7   | `0Fh`  | LPT1         |

## Initialization (ICW Sequence)

```text
ICW1 → Port 20h: 11h (edge, single, ICW4 needed)
ICW2 → Port 21h: 08h (vector base)
ICW4 → Port 21h: 01h (8086 mode)
```

## EOI Command

Non-specific EOI: Write `20h` to port `20h`

## Interrupt Sequence

1. Device asserts IRx → IRR bit set
2. INT asserted to CPU
3. CPU INTA → IRR cleared, ISR set
4. Second INTA → vector on bus
5. Handler runs, sends EOI
6. ISR bit cleared

## Implementation Guide

**[hardware-design.md](hardware-design.md)** - Complete hardware-accurate implementation reference

This comprehensive guide covers the final production design:

- **Interface Segregation**: `IPicCpuLink`, `IPicDeviceLink`, `IPeripheral`
- **Physical Hardware Mapping**: How interfaces map to real 8259A pins
- **Edge-Triggered Behavior**: IRQ line state tracking and latching
- **INTA Cycle**: Vector transfer on data bus (hardware-accurate)
- **Device Implementation**: Timer, keyboard, expansion card examples
- **CPU Implementation**: Interrupt checking and acknowledgment
- **Complete Flow**: Full interrupt sequence from device to handler

## Advanced Features (Fully Implemented)

The `Pic8259A` implementation includes all 8259A hardware features:

- ✅ **Priority Rotation**: OCW2 commands for rotating interrupt priorities
- ✅ **Special Mask Mode**: OCW3 special mask mode allowing nested interrupts
- ✅ **Polling Mode**: OCW3 poll command for reading interrupt status without INTA
- ✅ **ICW3 Support**: Cascade mode configuration (accepted but unused in single-PIC mode)
- ✅ **Auto-EOI Mode**: Automatic ISR clearing after interrupt acknowledgment
- ✅ **Specific/Non-specific EOI**: OCW2 commands for clearing ISR bits

## References

See [references/](references/) for hardware datasheets and timing diagrams.
