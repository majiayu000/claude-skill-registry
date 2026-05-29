---
name: mouse-expert
description: Expert on Kolobok bus mouse for ES-1841. Provides guidance on mouse input handling, quadrature decoding, button state tracking, and mouse IRQ configuration.
---

# Mouse Expert - Kolobok Bus Mouse

Expert knowledge for the ES-1841's bus mouse.

## Key Specifications

| Property  | Value                  |
| --------- | ---------------------- |
| Type      | Bus mouse (not serial) |
| I/O Ports | `23Ch`-`23Fh`          |
| IRQ       | 2, 3, 4, or 5          |
| Protocol  | MS Bus Mouse or InPort |

## I/O Ports

| Port   | Function     |
| ------ | ------------ |
| `23Ch` | Data port    |
| `23Dh` | Signature    |
| `23Eh` | Control port |

## Microsoft Bus Mouse Protocol

**Control Port:**

- Bits 0-1: Counter select
- Bit 2: IRQ enable

**Reading (4 reads for X/Y):**

```text
Select X-low  → Read nibble
Select X-high → Read nibble → Combine
Select Y-low  → Read nibble
Select Y-high → Read nibble → Combine
```

## InPort Protocol (Alternative)

Indexed access:

- Write index to `23Ch`
- Read/write data at `23Dh`

| Index | Register   |
| ----- | ---------- |
| 0     | Status     |
| 1     | X movement |
| 2     | Y movement |
| 7     | Mode       |

**Status (Index 0):**

- Bit 0: Left button (0=down)
- Bit 1: Middle button
- Bit 2: Right button
- Bit 6: Movement flag

## Implementation Notes

Limited ES-1841 documentation exists:

- Try MS Bus Mouse first
- Check MAME ec1841 for reference

## References

See [references/](references/) for detailed documentation.
