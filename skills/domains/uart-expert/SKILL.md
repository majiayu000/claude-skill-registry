---
name: uart-expert
description: Expert on Intel 8250 UART for ES-1841 serial ports. Provides guidance on COM ports, serial communication, baud rate configuration, and modem control. Note: ES-1841 serial is incompatible with standard PC.
---

# UART Expert - Intel 8250

Expert knowledge for serial communication (with ES-1841 caveats).

> **WARNING**: ES-1841's serial port is "completely incompatible" with standard
> IBM PC.

## Key Specifications

| Property  | Value                        |
| --------- | ---------------------------- |
| I/O Ports | `3F8h` (COM1), `2F8h` (COM2) |
| IRQ       | COM1=`IRQ4`, COM2=`IRQ3`     |
| Clock     | 1.8432 MHz                   |

## Register Map (Base + Offset)

| Offset | DLAB=0 Read | DLAB=0 Write | DLAB=1 |
| ------ | ----------- | ------------ | ------ |
| +0     | RBR         | THR          | DLL    |
| +1     | IER         | IER          | DLM    |
| +3     | LCR         | LCR          | -      |
| +4     | MCR         | MCR          | -      |
| +5     | LSR         | -            | -      |
| +6     | MSR         | -            | -      |

## Key Registers

**LCR (Base+3):** Word length, stop bits, parity, DLAB

**LSR (Base+5):**

- Bit 0: Data Ready
- Bit 5: THR Empty

**MCR (Base+4):**

- Bit 0: DTR
- Bit 1: RTS
- Bit 3: OUT2 (IRQ enable)

## Baud Rate

```text
Divisor = 1843200 / (16 × Baud)
```

| Baud | Divisor |
| ---- | ------- |
| 9600 | 12      |
| 4800 | 24      |

## ES-1841 Notes

Consider minimal/stub implementation due to incompatibility.

## References

See [references/](references/) for detailed documentation.
