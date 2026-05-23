---
name: fpu-expert
description: Expert on K1810VM87 (Intel 8087) floating-point coprocessor for ES-1841. Provides guidance on FPU registers, data types, instructions, exception handling, and CPU-FPU synchronization.
---

# FPU Expert - K1810VM87 / Intel 8087

Expert knowledge for the ES-1841's optional math coprocessor.

## Key Specifications

| Parameter  | Value                                                       |
| ---------- | ----------------------------------------------------------- |
| Chip       | K1810VM87 (Soviet 8087 clone)                               |
| Data Types | 16/32/64-bit integer, 32/64/80-bit float, 80-bit packed BCD |
| Registers  | 8 × 80-bit stack (ST0-ST7)                                  |
| Status     | Control, Status, Tag words                                  |
| I/O Ports  | `F0h`-`FFh` (escape handler)                                |
| Exception  | `IRQ 13` (via `INT 75h` on AT, varies on XT)                |

## Register Stack

```text
┌────────────────────────────────────────┐
│  ST(7)  │ 80-bit extended precision    │
├─────────┼──────────────────────────────┤
│  ST(6)  │                              │
├─────────┤                              │
│  ST(5)  │                              │
├─────────┤     Register Stack           │
│  ST(4)  │                              │
├─────────┤                              │
│  ST(3)  │                              │
├─────────┤                              │
│  ST(2)  │                              │
├─────────┤                              │
│  ST(1)  │                              │
├─────────┼──────────────────────────────┤
│  ST(0)  │ Top of Stack (TOS)           │
└─────────┴──────────────────────────────┘
```

## Data Formats

| Type          | Bits | Range                       |
| ------------- | ---- | --------------------------- |
| Word Integer  | 16   | -32768 to +32767            |
| Short Integer | 32   | -2×10⁹ to +2×10⁹            |
| Long Integer  | 64   | -9×10¹⁸ to +9×10¹⁸          |
| Short Real    | 32   | ±1.2×10⁻³⁸ to ±3.4×10³⁸     |
| Long Real     | 64   | ±2.2×10⁻³⁰⁸ to ±1.8×10³⁰⁸   |
| Temp Real     | 80   | ±3.4×10⁻⁴⁹³² to ±1.2×10⁴⁹³² |
| Packed BCD    | 80   | 18 digits                   |

## Key Instructions

| Category       | Examples                        |
| -------------- | ------------------------------- |
| Load/Store     | FLD, FST, FSTP, FILD, FIST      |
| Arithmetic     | FADD, FSUB, FMUL, FDIV, FSQRT   |
| Compare        | FCOM, FCOMP, FTST               |
| Transcendental | FSIN, FCOS, FPTAN, F2XM1, FYL2X |
| Control        | FINIT, FWAIT, FSTCW, FLDCW      |

## CPU-FPU Synchronization

```assembly
; FWAIT/WAIT required before reading FPU results
        FLD     QWORD [value]
        FSQRT
        FWAIT                   ; Wait for FPU to complete
        FST     QWORD [result]
```

## Exception Handling

8087 exceptions:

- Invalid operation
- Denormalized operand
- Zero divide
- Overflow
- Underflow
- Precision (inexact)

## ES-1841 Notes

- Optional coprocessor (not always installed)
- Software should detect presence before use
- AlphaDOS may not fully support FPU

## References

See [references/](references/) for detailed documentation.
