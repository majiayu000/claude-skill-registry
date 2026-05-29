---
name: fdc-expert
description: Expert on NEC µPD765 Floppy Disk Controller for ES-1841. Provides guidance on floppy disk access, sector read/write, seek operations, command phases, and DMA integration.
---

# FDC Expert - NEC µPD765 / Intel 8272A

Expert knowledge for the ES-1841's floppy controller.

## Key Specifications

| Property    | Value                  |
| ----------- | ---------------------- |
| I/O Ports   | `3F2h`, `3F4h`, `3F5h` |
| DMA Channel | 2                      |
| IRQ         | 6                      |
| Drives      | Up to 4                |

## I/O Ports

| Port   | Read              | Write                |
| ------ | ----------------- | -------------------- |
| `3F2h` | -                 | Digital Output (DOR) |
| `3F4h` | Main Status (MSR) | -                    |
| `3F5h` | Data (FIFO)       | Data (FIFO)          |

## DOR - Digital Output (`3F2h`)

| Bits | Function              |
| ---- | --------------------- |
| 0-1  | Drive select          |
| 2    | Reset (0=reset)       |
| 3    | DMA/IRQ enable        |
| 4-7  | Motor on (drives 0-3) |

## MSR - Main Status (`3F4h`)

| Bit | Function                 |
| --- | ------------------------ |
| 7   | RQM - Ready for data     |
| 6   | DIO - Direction (1=read) |
| 4   | CB - Command busy        |

## Command Phases

1. **Command**: Write to `3F5h` (RQM=1, DIO=0)
2. **Execution**: DMA transfer
3. **Result**: Read from `3F5h` (RQM=1, DIO=1)

## Key Commands

| Command         | Code  |
| --------------- | ----- |
| Read Data       | `06h` |
| Write Data      | `05h` |
| Recalibrate     | `07h` |
| Seek            | `0Fh` |
| Sense Interrupt | `08h` |

## Drive Types

| Type     | Tracks | Sectors | Capacity |
| -------- | ------ | ------- | -------- |
| 5.25" DD | 40     | 9       | 360 KB   |
| 3.5" DD  | 80     | 9       | 720 KB   |
| 3.5" HD  | 80     | 18      | 1.44 MB  |

## References

See [references/](references/) for detailed documentation.
