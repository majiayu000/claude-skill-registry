---
name: midi-protocol-lookup
description: Look up APC Mini MK2 MIDI protocol details including note numbers, MIDI channels, velocity values, and SysEx format. Use when user asks about "MIDI note", "channel", "velocity", "status byte", "SysEx", "protocol", or needs to understand how MIDI messages control the APC Mini MK2.
---

# APC Mini MK2 MIDI Protocol Reference

Quick reference for MIDI protocol. For complete details, see [reference.md](reference.md).

## MIDI Message Structure

- **Note On**: `[0x9n, note, velocity]` (n = channel 0-15)
- **Note Off**: `[0x8n, note, velocity]`
- **Control Change**: `[0xBn, cc, value]`

## Note Mapping

| Region | Notes | Purpose |
|--------|-------|---------|
| Pad Grid | 0-63 | 8x8 RGB pads (row * 8 + col) |
| Track Buttons | 100-107 | Red LEDs |
| Scene Buttons | 112-119 | Green LEDs |
| Shift | 122 | No LED |
| Faders (CC) | 48-56 | CC 48-55 + Master 56 |

## MIDI Channel Effects

| Channel | Effect |
|---------|--------|
| 0-6 | Brightness 10%-100% |
| 7-10 | Pulse animation |
| 11-15 | Blink animation |

**Use channel 6 (0x96) for full brightness.**

## SysEx Custom RGB

```
F0 47 7F 4F 24 00 08 [pad] [pad] [R-MSB] [R-LSB] [G-MSB] [G-LSB] [B-MSB] [B-LSB] F7
```

RGB encoding:
```typescript
const encodeRGB = (value: number): readonly [number, number] =>
  [(value >> 7) & 0x01, value & 0x7F] as const;
```
