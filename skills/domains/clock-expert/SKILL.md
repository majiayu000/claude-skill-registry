---
name: clock-expert
description: Expert on Intel 8284A Clock Generator for ES-1841. Provides guidance on system timing, CPU clock generation, peripheral clock, reset circuit, and wait state synchronization.
---

# Clock Expert - Intel 8284A / KR1810GF84

Expert knowledge for the ES-1841's clock generator.

## Key Specifications

| Property     | Value                    |
| ------------ | ------------------------ |
| Soviet Clone | KR1810GF84               |
| Crystal      | 14.31818 MHz             |
| CPU Clock    | 4.77 MHz (÷3)            |
| PCLK         | 2.39 MHz (÷6)            |

## Clock Outputs

| Output | Frequency    | Duty | Use              |
| ------ | ------------ | ---- | ---------------- |
| CLK    | 4.77 MHz     | 33%  | CPU clock        |
| PCLK   | 2.39 MHz     | 50%  | Peripheral clock |
| OSC    | 14.31818 MHz | -    | Color burst      |

## Clock Derivation

```text
Crystal: 14.31818 MHz
   ÷3  → CLK:  4.77272 MHz (CPU)
   ÷6  → PCLK: 2.38636 MHz (peripherals)
   ÷12 → PIT:  1.19318 MHz (timer)
```

## Reset Circuit

- **RES** input: Schmitt trigger
- **RESET** output: Synchronized to CLK, active HIGH
- Hold ≥4 CLK cycles after RES inactive

## Ready Synchronization

```text
READY = (RDY1 OR AEN1) AND (RDY2 OR AEN2)
```

Used for wait state insertion with slow devices.

## Wait States

```text
Normal:     T1 → T2 → T3 → T4
With waits: T1 → T2 → T3 → Tw... → T4
```

## Emulation Notes

For most emulation purposes:

- Use fixed frequency values
- Generate reset pulse on startup
- Wait states often abstracted

## References

See [references/](references/) for detailed documentation.
