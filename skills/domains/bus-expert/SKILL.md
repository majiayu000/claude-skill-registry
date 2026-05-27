---
name: bus-expert
description: Expert on ISA system bus for ES-1841. Provides guidance on bus timing, I/O port addressing, memory mapping, bus signals, and expansion card interface.
---

# Bus Expert - ISA Compatible

Expert knowledge for the ES-1841's system bus.

## Key Specifications

| Property     | Value                    |
| ------------ | ------------------------ |
| Type         | 8-bit ISA (XT bus)       |
| Clock        | 4.77 MHz                 |
| Address      | 20 lines (A0-A19)        |
| Data         | 8 lines (D0-D7)          |
| ES-1841      | 135-pin connector        |

## Bus Signals

### Control

| Signal  | Description            |
| ------- | ---------------------- |
| ALE     | Address Latch Enable   |
| /IOR    | I/O Read               |
| /IOW    | I/O Write              |
| /MEMR   | Memory Read            |
| /MEMW   | Memory Write           |

### Interrupt/DMA

- IRQ0-IRQ7: Interrupt requests
- DRQ0-DRQ3: DMA requests
- DACK0-DACK3: DMA acknowledges

## Bus Cycle Timing

4 clocks = 838 ns:

```text
T1: Address, ALE high
T2: ALE low, /RD or /WR
T3: Data transfer
T4: Deassert control
```

## I/O Port Map

| Range         | Device           |
| ------------- | ---------------- |
| `000h`-`00Fh` | DMA Controller   |
| `020h`-`021h` | PIC              |
| `040h`-`043h` | PIT              |
| `060h`-`063h` | PPI              |
| `3D0h`-`3DFh` | CGA Video        |
| `3F0h`-`3F7h` | Floppy           |
| `320h`-`327h` | Hard Disk        |

## Memory Regions

| Range             | Type   |
| ----------------- | ------ |
| `00000h`-`9FFFFh` | RAM    |
| `A0000h`-`BFFFFh` | Video  |
| `C0000h`-`DFFFFh` | ROM    |
| `F0000h`-`FFFFFh` | BIOS   |

## Wait States

Slow peripherals insert wait states (Tw) by controlling the RDY signal.

### Peripheral Interfaces

**IPeripheral** - Fast devices (RAM, ROM):

```csharp
byte Read(uint offset);
void Write(uint offset, byte value);
```

**IBusAwarePeripheral** - Slow devices (FDC, HDD, DMA):

```csharp
void Initialize(IClock clock);
void BeginBusCycle(uint offset, bool isWrite);  // Called at T1
void OnWaitState();                              // Called each Tw
```

### Wait State Pattern

```csharp
public void BeginBusCycle(uint offset, bool isWrite)
{
    _clock.SetReady(false);  // Pull RDY LOW
    _readyAtCycle = _clock.TotalCycles + 3 + waitStates;
}

public void OnWaitState()
{
    if (_clock.TotalCycles >= _readyAtCycle)
        _clock.SetReady(true);  // Release RDY HIGH
}
```

**Formula**: `readyAtCycle = current + 3 + waitStates`

- BeginBusCycle at T1 (cycle 0)
- +1: T1→T2
- +2: T2→T3  
- +3: T3→Tw (first wait state)
- +N: Additional wait states

## References

See [references/](references/) for detailed ISA bus documentation.
