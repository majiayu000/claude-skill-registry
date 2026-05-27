---
name: dma-expert
description: Expert on Intel 8237A DMA Controller for ES-1841. Provides guidance on DMA transfers, floppy/HDD data transfer, DRAM refresh, page registers, and channel configuration.
---

# DMA Expert - Intel 8237A / KR580VT57

Expert knowledge for the ES-1841's DMA controller.

## Key Specifications

| Property     | Value                      |
| ------------ | -------------------------- |
| Soviet Clone | KR580VT57 / KR1810VT37     |
| Channels     | 4 independent              |
| I/O Ports    | `00h`-`0Fh`                |
| Page Regs    | `81h`, `82h`, `83h`, `87h` |

## I/O Ports

| Port        | Read               | Write                |
| ----------- | ------------------ | -------------------- |
| `00h`-`07h` | Current addr/count | Base addr/count      |
| `08h`       | Status Register    | Command Register     |
| `0Ah`       | -                  | Single Mask Register |
| `0Bh`       | -                  | Mode Register        |
| `0Ch`       | -                  | Clear Flip-Flop      |
| `0Dh`       | Temp Register      | Master Clear         |

## Page Registers (Upper 4 Address Bits)

| Port  | Channel |
| ----- | ------- |
| `87h` | Ch0     |
| `83h` | Ch1     |
| `81h` | Ch2     |
| `82h` | Ch3     |

## Channel Assignments

| Channel | Usage        |
| ------- | ------------ |
| 0       | DRAM Refresh |
| 2       | Floppy Disk  |
| 3       | Hard Disk    |

## Mode Register (Port `0Bh`)

```text
Bits 7-6: Mode (00=demand, 01=single, 10=block)
Bit 5:    Decrement/Increment
Bit 4:    Auto-init
Bits 3-2: Transfer type (01=write, 10=read)
Bits 1-0: Channel select
```

## Programming Sequence

1. Mask channel
2. Clear flip-flop
3. Write address LSB/MSB
4. Write page register
5. Clear flip-flop
6. Write count LSB/MSB (bytes - 1)
7. Set mode
8. Unmask channel

## References

See [references/](references/) for detailed documentation.
