---
name: pit-expert
description: Expert on Intel 8253/8254 Programmable Interval Timer for ES-1841. Provides guidance on system timer, DRAM refresh, PC speaker tone generation, and timer interrupt timing.
---

# PIT Expert - Intel 8253 / KR580VI53

Expert knowledge for the ES-1841's timer subsystem.

## Key Specifications

| Property     | Value                |
| ------------ | -------------------- |
| Soviet Clone | KR580VI53            |
| Counters     | 3 independent 16-bit |
| I/O Ports    | `40h`-`43h`          |
| Clock Input  | 1.193182 MHz         |

## I/O Ports

| Port  | Description    |
| ----- | -------------- |
| `40h` | Counter 0 data |
| `41h` | Counter 1 data |
| `42h` | Counter 2 data |
| `43h` | Control Word   |

## Control Word Format

```text
Bits 7-6: Counter select (00/01/10 = C0/C1/C2)
Bits 5-4: R/W (01=LSB, 10=MSB, 11=LSB+MSB)
Bits 3-1: Mode (0-5)
Bit 0:    BCD (0=binary)
```

## Channel Assignments

| Ch  | Function     | Mode | Typical Count  |
| --- | ------------ | ---- | -------------- |
| 0   | System Timer | 3    | 65536 (18.2Hz) |
| 1   | DRAM Refresh | 2    | 18 (~66kHz)    |
| 2   | PC Speaker   | 3    | Variable       |

## Operating Modes

- **Mode 0**: Interrupt on terminal count
- **Mode 2**: Rate generator (periodic pulse)
- **Mode 3**: Square wave generator (50% duty)

## Timer Frequency Calculations

```text
Output Frequency = 1193182 / Count
18.2 Hz = 1193182 / 65536
```

## Speaker Control (Port `61h`)

- Bit 0: Timer 2 GATE enable
- Bit 1: Speaker output enable

## References

See [references/](references/) for detailed documentation.
