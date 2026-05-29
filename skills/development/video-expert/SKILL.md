---
name: video-expert
description: Expert on CGA video controller for ES-1841. Provides guidance on text/graphics rendering, video RAM layout, character generation, color attributes, and display modes.
---

# Video Expert - Extended CGA

Expert knowledge for the ES-1841's video subsystem.

## Key Specifications

| Property       | Value               |
| -------------- | ------------------- |
| Video RAM      | `B8000h` - `BFFFFh` |
| Text Modes     | 40×25, 80×25        |
| Graphics Modes | 320×200, 640×200    |
| Character Size | 8×8 pixels          |

## Video Modes

| Mode | Resolution | Type     | Colors |
| ---- | ---------- | -------- | ------ |
| 0, 1 | 40×25      | Text     | 16     |
| 2, 3 | 80×25      | Text     | 16     |
| 4, 5 | 320×200    | Graphics | 4      |
| 6    | 640×200    | Graphics | 2      |

## Text Mode Memory

```text
B8000h: [Char][Attr][Char][Attr]...
```

**Attribute byte:**

- Bits 0-3: Foreground (0-15)
- Bits 4-6: Background (0-7)
- Bit 7: Blink or high-intensity

## Graphics Mode Memory

Interleaved scanlines:

- Even: `B8000h` - `B9F3Fh`
- Odd: `BA000h` - `BBF3Fh`

## CGA Palette

| Index | Colors                          |
| ----- | ------------------------------- |
| 0-7   | Dark colors (Black→Light Gray)  |
| 8-15  | Bright colors (Dark Gray→White) |

## ES-1841 Extensions

- **Downloadable fonts**: Custom character sets
- Character ROM replaceable at runtime

## Grayscale (MS 1504 LCD)

Map IRGB to 4 shades:

- `0000`: Black
- Low intensity: 33%
- High intensity: 66%
- `1111`: White

## References

- [../crtc-expert/references/implementation-guide.md](../crtc-expert/references/implementation-guide.md) - Complete CRTC/CGA implementation guide
- See [references/](references/) for detailed hardware documentation
