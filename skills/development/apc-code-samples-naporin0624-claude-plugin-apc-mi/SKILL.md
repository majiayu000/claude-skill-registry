---
name: apc-code-samples
description: TypeScript and Node.js code samples for APC Mini MK2 development. Use when user needs "code example", "implementation", "easymidi", "@julusian/midi", "sample code", "how to implement", or wants working code for LED control, button handling, or MIDI communication.
---

# APC Mini MK2 Code Samples

Quick start examples. For complete implementation details, see [reference.md](reference.md).

## Library Setup

```bash
# Rapid development
npm install easymidi && npm install -D @types/easymidi

# Production
npm install @julusian/midi
```

## Basic Connection

```typescript
import easymidi from 'easymidi';

const createConnection = () => ({
  output: new easymidi.Output('APC mini mk2'),
  input: new easymidi.Input('APC mini mk2')
} as const);
```

## Set Pad Color

```typescript
// Red at full brightness (channel 6)
const setPad = (output: Output, note: number, velocity: number, channel = 6): void =>
  output.send('noteon', { note, velocity, channel });

// Turn off
const setPadOff = (output: Output, note: number): void =>
  output.send('noteon', { note, velocity: 0, channel: 0 });
```

## Handle Button Press

```typescript
const onPadPress = (input: Input, callback: (pad: number) => void): void =>
  input.on('noteon', (msg) => {
    if (msg.note < 64 && msg.velocity > 0) callback(msg.note);
  });

const onTrackButton = (input: Input, callback: (track: number) => void): void =>
  input.on('noteon', (msg) => {
    if (msg.note >= 100 && msg.note <= 107) callback(msg.note - 99);
  });

const onSceneButton = (input: Input, callback: (scene: number) => void): void =>
  input.on('noteon', (msg) => {
    if (msg.note >= 112 && msg.note <= 119) callback(msg.note - 111);
  });
```

## Handle Fader

```typescript
const onFader = (input: Input, callback: (fader: number, value: number) => void): void =>
  input.on('cc', (msg) => {
    if (msg.controller >= 48 && msg.controller <= 56) {
      callback(msg.controller - 47, msg.value);
    }
  });
```

## Custom RGB

```typescript
const encodeRGB = (v: number): readonly [number, number] =>
  [(v >> 7) & 0x01, v & 0x7F] as const;

const setRGB = (output: Output, pad: number, r: number, g: number, b: number): void =>
  output.send('sysex', [
    0xF0, 0x47, 0x7F, 0x4F, 0x24, 0x00, 0x08,
    pad, pad, ...encodeRGB(r), ...encodeRGB(g), ...encodeRGB(b),
    0xF7
  ]);
```

## Color Constants

```typescript
const Colors = {
  OFF: 0, WHITE: 3, RED: 5, ORANGE: 9, YELLOW: 13,
  GREEN: 21, CYAN: 33, BLUE: 45, PURPLE: 49, MAGENTA: 53
} as const;
```
