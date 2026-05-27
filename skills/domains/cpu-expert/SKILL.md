---
name: cpu-expert
description: Expert on K1810VM86 (Intel 8086) CPU architecture for ES-1841. Provides guidance on registers, instruction decoding, memory segmentation, interrupts, bus cycles, and x86-16 behavior.
---

# CPU Expert - K1810VM86 / Intel 8086

Expert knowledge for the ES-1841's central processor.

## Key Specifications

| Property     | Value                               |
| ------------ | ----------------------------------- |
| Soviet Clone | K1810VM86                           |
| Architecture | x86-16, 16-bit data, 20-bit address |
| Clock        | 5 MHz (ES-1841)                     |
| Reset Vector | `FFFF:0000` → Physical `FFFF0h`     |

## Register Set

**General Purpose (16-bit, split into 8-bit):**

- AX (AH/AL) - Accumulator
- BX (BH/BL) - Base
- CX (CH/CL) - Count
- DX (DH/DL) - Data

**Index/Pointer:** SI, DI, BP, SP

**Segment:** CS, DS, SS, ES (reset: CS=`FFFFh`, others=`0000h`)

**Special:** IP, FLAGS

## Memory Segmentation

```text
Physical Address = (Segment << 4) + Offset
```

1 MB address space. Key regions:

- `00000h`-`003FFh` - IVT
- `00400h`-`004FFh` - BIOS Data Area
- `B8000h`-`BFFFFh` - Video RAM
- `F0000h`-`FFFFFh` - System BIOS

## FLAGS Register

| Bit | Flag | Function           |
| --- | ---- | ------------------ |
| 0   | CF   | Carry              |
| 2   | PF   | Parity             |
| 4   | AF   | Auxiliary Carry    |
| 6   | ZF   | Zero               |
| 7   | SF   | Sign               |
| 8   | TF   | Trap (single-step) |
| 9   | IF   | Interrupt Enable   |
| 10  | DF   | Direction          |
| 11  | OF   | Overflow           |

## Interrupt Handling

1. Complete current instruction
2. Push FLAGS, CS, IP
3. Clear IF and TF
4. Load `CS:IP` from IVT[vector × 4]

## Bus Cycles

4 clocks per memory/IO access (minimum mode):

- T1: Address, ALE high
- T2: ALE low, RD/WR asserted
- T3: Data transfer
- T4: Bus idle

## References

See [references/](references/) for detailed documentation.
