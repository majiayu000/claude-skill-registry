---
name: nmi-expert
description: Expert on NMI (Non-Maskable Interrupt) controller for ES-1841. Provides guidance on NMI sources, masking via port 0xA0, parity errors, I/O channel check, and coprocessor exceptions.
---

# NMI Expert - Non-Maskable Interrupt Controller

Expert knowledge for the ES-1841's NMI control logic.

## Key Specifications

| Property        | Value                                    |
| --------------- | ---------------------------------------- |
| I/O Port        | `0xA0`                                   |
| Interrupt       | Vector 2 (INT 02h)                       |
| Priority        | Higher than maskable interrupts (INTR)   |
| Masking         | Via port 0xA0 bit 7 (hardware gate only) |
| CPU IF Flag     | Has NO effect on NMI                     |

## I/O Port 0xA0

| Bit | Name       | Description                          |
| --- | ---------- | ------------------------------------ |
| 7   | NMI Enable | 1 = NMI enabled, 0 = NMI disabled    |
| 6-0 | Reserved   | System-specific, typically unused    |

## NMI Sources (ES-1841/PC XT)

| Source             | Signal Origin           | Status Location   |
| ------------------ | ----------------------- | ----------------- |
| Parity Error       | RAM parity checker      | PPI Port C bit 7  |
| I/O Channel Check  | ISA bus IOCHK# signal   | PPI Port C bit 6  |
| Coprocessor Error  | 8087 FPU INT output     | FPU Status Word   |

## NMI vs INTR Comparison

| Feature          | NMI (Vector 2)           | INTR (PIC)              |
| ---------------- | ------------------------ | ----------------------- |
| Maskable by IF   | No                       | Yes                     |
| Vector Source    | Fixed (always 2)         | PIC provides vector     |
| Edge Triggered   | Yes (in CPU)             | Configurable (edge/lvl) |
| Priority         | Highest                  | Lower than NMI          |
| Acknowledge      | Implicit                 | INTA bus cycle          |

## NMI Sequence

1. NMI source signals error condition
2. NMI controller latches the source
3. If NMI enabled (port 0xA0 bit 7 = 1):
   - NMI signal asserted to CPU
4. CPU detects rising edge on NMI pin
5. CPU pushes FLAGS, CS, IP to stack
6. CPU clears IF and TF flags
7. CPU vectors to interrupt 2
8. Handler identifies source via PPI Port C
9. Handler clears source (via PPI Port B toggles)

## Implementation Guide

The NMI controller is implemented as discrete TTL logic on the motherboard,
not as a dedicated chip. The `NmiMaskRegister` class models this logic.

### Interfaces

- **`INmiToCpuConnection`**: NMI signal to CPU (like PIC's INT signal)
- **`INmiSourceConnection`**: Sources signal NMI conditions

### Key Behaviors

- **Edge-triggered in CPU**: After servicing NMI, CPU requires LOW→HIGH
  transition to recognize next NMI
- **Source latching**: Sources are latched until explicitly cleared
- **Enable gate**: Port 0xA0 bit 7 gates NMI signal, not source latching

### Implementation Files

- `Nostalgia.Hardware/Nmi/NmiMaskRegister.cs` - Main implementation
- `Nostalgia.Hardware/Nmi/INmiToCpuConnection.cs` - CPU interface
- `Nostalgia.Hardware/Nmi/INmiSourceConnection.cs` - Source interface

## Clearing NMI Sources

Sources are cleared via PPI Port B toggles:

```text
Parity Error:    Toggle PPI Port B bit 7 (RAM parity check enable)
I/O Channel:     Toggle PPI Port B bit 6 (I/O check enable)
Coprocessor:     Clear FPU exception flags (FCLEX instruction)
```

## BIOS NMI Handler (INT 02h)

Typical BIOS NMI handler:

1. Read PPI Port C to identify source
2. Display error message
3. Clear source latch via PPI Port B
4. Halt system or attempt recovery

## References

See [references/](references/) for hardware details and programming guide.
