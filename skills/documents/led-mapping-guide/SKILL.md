---
name: led-mapping-guide
description: Visual guide for APC Mini MK2 LED and button mapping. Use when user needs to know "which button", "pad location", "LED position", "coordinate to note", "note to coordinate", or wants to understand the physical layout of the controller.
---

# APC Mini MK2 LED Mapping Guide

Visual reference for button positions. For complete details, see [reference.md](reference.md).

## Physical Layout

```
┌─────────────────────────────────────────────┐
│  [SHIFT]                        [SCENE 1-8] │
│                                   112-119   │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐  ┌───┐  │
│  │56 │57 │58 │59 │60 │61 │62 │63 │  │112│  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤  ├───┤  │
│  │...│   │   │   │   │   │   │...│  │...│  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤  ├───┤  │
│  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │  │119│  │
│  └───┴───┴───┴───┴───┴───┴───┴───┘  └───┘  │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐         │
│  │100│101│102│103│104│105│106│107│ TRACK   │
│  └───┴───┴───┴───┴───┴───┴───┴───┘         │
│  ═══════════════════════════════  FADERS   │
│  CC48-55                          CC56     │
└─────────────────────────────────────────────┘
```

## Coordinate Conversion

```typescript
// (row, col) to note (1-indexed)
const coordToNote = (row: number, col: number): number =>
  (row - 1) * 8 + (col - 1);

// note to (row, col)
const noteToCoord = (note: number) => ({
  row: Math.floor(note / 8) + 1,
  col: (note % 8) + 1
} as const);

// (x, y) to note (0-indexed)
const xyToNote = (x: number, y: number): number => y * 8 + x;
```

## LED Types

| Region | Notes | LED Type | States |
|--------|-------|----------|--------|
| Pads | 0-63 | RGB | 128 colors + custom RGB |
| Track | 100-107 | Red | 0=off, 1=on, 2=blink |
| Scene | 112-119 | Green | 0=off, 1=on, 2=blink |
