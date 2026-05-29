---
name: hdd-expert
description: Expert on ST-506/MFM Hard Disk Controller for ES-1841. Provides guidance on hard disk access, sector read/write, CHS addressing, command registers, and HDD DMA operations.
---

# HDD Expert - ST-506/MFM

Expert knowledge for the ES-1841's hard disk controller.

## Key Specifications

| Property    | Value                    |
| ----------- | ------------------------ |
| I/O Ports   | `320h`-`327h`            |
| DMA Channel | 3                        |
| IRQ         | 5                        |
| Addressing  | CHS                      |

## I/O Ports

| Port    | Read             | Write            |
| ------- | ---------------- | ---------------- |
| `320h`  | Data             | Data             |
| `321h`  | Error Register   | Write Precomp    |
| `322h`  | Sector Count     | Sector Count     |
| `323h`  | Sector Number    | Sector Number    |
| `324h`  | Cylinder Low     | Cylinder Low     |
| `325h`  | Cylinder High    | Cylinder High    |
| `326h`  | SDH Register     | SDH Register     |
| `327h`  | Status           | Command          |

## Status Register (`327h`)

| Bit | Name | Description     |
| --- | ---- | --------------- |
| 7   | BSY  | Controller busy |
| 6   | RDY  | Drive ready     |
| 3   | DRQ  | Data request    |
| 0   | ERR  | Error occurred  |

## SDH Register (`326h`)

```text
Bit 7: 1 (always)
Bit 6: LBA mode (0=CHS)
Bit 5: 1 (always)
Bit 4: Drive select
Bits 0-3: Head number
```

## Commands

| Command      | Code   |
| ------------ | ------ |
| Recalibrate  | `10h`  |
| Read Sector  | `20h`  |
| Write Sector | `30h`  |
| Seek         | `70h`  |

## Command Sequence

1. Wait BSY=0, RDY=1
2. Write parameters (`322h`-`326h`)
3. Write command (`327h`)
4. Wait for IRQ or poll DRQ
5. Transfer data
6. Read status

## References

See [references/](references/) for detailed documentation.
