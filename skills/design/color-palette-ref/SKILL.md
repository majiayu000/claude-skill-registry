---
name: color-palette-ref
description: APC Mini MK2 color palette reference with velocity values and custom RGB via SysEx. Use when user asks about "color", "velocity value", "RGB", "palette", "brightness", "LED color", or needs to set specific colors on the APC Mini MK2.
---

# APC Mini MK2 Color Palette Reference

Color reference for velocity values. For complete details, see [reference.md](reference.md).

## Primary Colors

| Color | Velocity | Hex |
|-------|----------|-----|
| Off | 0 | 0x00 |
| White | 3 | 0x03 |
| Red | 5 | 0x05 |
| Orange | 9 | 0x09 |
| Yellow | 13 | 0x0D |
| Green | 21 | 0x15 |
| Cyan | 33 | 0x21 |
| Blue | 45 | 0x2D |
| Purple | 49 | 0x31 |
| Magenta | 53 | 0x35 |
| Pink | 57 | 0x39 |

## Brightness (MIDI Channel)

| Channel | Brightness |
|---------|------------|
| 0-6 | 10%-100% solid |
| 7-10 | Pulse animation |
| 11-15 | Blink animation |

## Custom RGB via SysEx

```typescript
type RGBPair = readonly [number, number];

const encodeRGB = (value: number): RGBPair =>
  [(value >> 7) & 0x01, value & 0x7F] as const;

const setCustomRGB = (output: Output, pad: number, r: number, g: number, b: number): void => {
  const [rMSB, rLSB] = encodeRGB(r);
  const [gMSB, gLSB] = encodeRGB(g);
  const [bMSB, bLSB] = encodeRGB(b);

  output.send('sysex', [
    0xF0, 0x47, 0x7F, 0x4F, 0x24, 0x00, 0x08,
    pad, pad, rMSB, rLSB, gMSB, gLSB, bMSB, bLSB,
    0xF7
  ]);
};
```

## Peripheral Buttons

| Type | LED Color | On | Blink |
|------|-----------|-------|-------|
| Track 1-8 | Red | velocity=1 | velocity=2 |
| Scene 1-8 | Green | velocity=1 | velocity=2 |
