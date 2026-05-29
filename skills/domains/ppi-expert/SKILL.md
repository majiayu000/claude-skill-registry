---
name: ppi-expert
description: Expert on Intel 8255A Programmable Peripheral Interface for ES-1841. Provides guidance on keyboard interface, speaker control, system configuration, and port 60h-63h operations.
---

# PPI Expert - Intel 8255A / KR580VV55A

Expert knowledge for the ES-1841's peripheral interface.

## Key Specifications

| Property     | Value               |
| ------------ | ------------------- |
| Soviet Clone | KR580VV55A          |
| I/O Ports    | `60h`-`63h`         |
| Ports        | 3 × 8-bit (A, B, C) |

## I/O Port Mapping

| Port  | Direction | Function           |
| ----- | --------- | ------------------ |
| `60h` | Input     | Keyboard scan code |
| `61h` | Output    | System control     |
| `62h` | Input     | System status      |
| `63h` | Write     | Control register   |

## Port B (`61h`) - System Control

| Bit | Function                 |
| --- | ------------------------ |
| 0   | Timer 2 GATE (speaker)   |
| 1   | Speaker data enable      |
| 4   | RAM parity check enable  |
| 5   | I/O channel check enable |
| 6   | Keyboard clock low       |
| 7   | Keyboard clear/enable    |

## Port C (`62h`) - Status

| Bit | Function                   |
| --- | -------------------------- |
| 0   | Timer 2 output state       |
| 4   | RAM parity error (0=error) |
| 5   | I/O channel check          |

## Control Word (Port `63h`)

**Mode set (bit 7 = 1):**

- Bit 4: Port A direction (1=input)
- Bit 1: Port B direction (1=input)

**Bit set/reset (bit 7 = 0):**

- Bits 3-1: Bit select (PC0-PC7)
- Bit 0: Set (1) or Reset (0)

## Keyboard Interface

1. Scan code arrives at Port A
2. IRQ1 triggered
3. CPU reads port `60h`
4. Toggle Port B bit 7 to acknowledge

## References

See [references/](references/) for detailed documentation.
