---
title: PRISM Node K1 Light Lab API
slug: prism-node-api
description: Complete API specification for PRISM.node K1 Light Lab editor, including node system architecture, type definitions, color space transforms, WebSocket TLV protocol, and engine configuration for 320-LED addressable light patterns.
category: web
created: 2025-10-21
last_updated: 2025-10-21
source: apps/PRISM.node/src/components/k1 (shipping Phase A code)
---

# PRISM Node K1 Light Lab API

**Authoritative Source:** TypeScript source in apps/PRISM.node/src/components/k1
**Shipping Status:** Phase A (production)
**Updated:** 2025-10-21
**Technology:** Vite + React 18 (SWC compiler)

---

## 1. Project Overview

### Purpose
K1 Light Lab is a **pro-grade graph-based animation editor** for 320-LED dual-strip WS2812B RGB controllers. It runs in the browser as a visual node editor, allows real-time parameter tuning, exports patterns via WebSocket TLV, and maintains a live preview of LED output.

### Target Device
- **Pixels:** 320 RGB8 LEDs (WS2812B compatible)
- **Mapping:** Concat-2x160 (dual GPIO parallel output)
  - GPIO 9: Pixels 0–159
  - GPIO 10: Pixels 160–319
- **Preview:** Real-time canvas rendering with selectable FPS (30/60/120)
- **Export:** Binary TLV payload (max 256KB per pattern)

### Tech Stack
- **Frontend:** React 18 + TypeScript 5
- **Build:** Vite 6
- **Compiler:** SWC (super-fast Rust-based TS/JS compilation)
- **UI Framework:** Radix UI primitives + Tailwind CSS
- **Color Space:** OKLCH (perceptual color space)
- **Canvas:** 2D WebGL-backed rendering

---

## 2. Node System Architecture

### Node Types

A **node** is a graph computation unit that transforms inputs → parameters → outputs.

#### Port Types
```typescript
type PortType = 'scalar' | 'field' | 'color' | 'output';

// scalar: Single numeric value (0–1 range, normalized)
// field:  Spatial 2D field (e.g., gradient, noise)
// color:  RGB8 color value [r, g, b]
// output: Final LED frame buffer (read-only)
```

#### Node Categories
```typescript
type NodeCategory =
  | 'generator'  // Produces fields/colors (no inputs)
  | 'spatial'    // Transforms fields spatially (grid, repeat)
  | 'modifier'   // Modifies scalars/fields (ramp, smooth)
  | 'color'      // Color space transforms (hue-shift, saturate)
  | 'combine'    // Blends/mixes inputs (blend, add, multiply)
  | 'output';    // Renders to LED frame buffer
```

#### Port Color Scheme (Visual UI)
```typescript
const PORT_COLORS: Record<PortType, string> = {
  scalar: '#F59E0B',    // Amber
  field:  '#22D3EE',    // Cyan
  color:  '#F472B6',    // Pink
  output: '#34D399',    // Emerald
};

const CATEGORY_COLORS: Record<NodeCategory, string> = {
  generator: 'bg-purple-500/10 text-purple-400',
  spatial:   'bg-cyan-500/10 text-cyan-400',
  modifier:  'bg-amber-500/10 text-amber-400',
  color:     'bg-pink-500/10 text-pink-400',
  combine:   'bg-blue-500/10 text-blue-400',
  output:    'bg-green-500/10 text-green-400',
};
```

### Node Interface Definition

```typescript
interface Port {
  id: string;           // Unique within node
  label: string;        // Human-readable name
  type: PortType;       // scalar | field | color | output
}

interface NodeParameter {
  id: string;           // Unique within node
  label: string;        // Display name
  type: 'slider' | 'select' | 'number' | 'toggle';
  value: number | string | boolean;
  min?: number;         // For slider/number
  max?: number;
  step?: number;
  options?: string[];   // For select
}

interface NodeData {
  id: string;                           // Unique node ID
  title: string;                        // Node name (e.g., "Gradient")
  category: NodeCategory;
  icon: string;                         // Emoji icon
  inputs: Port[];                       // Incoming connections
  outputs: Port[];                      // Outgoing connections
  parameters?: NodeParameter[];         // Internal state
  position: { x: number; y: number };  // Canvas position
  compact?: boolean;                    // UI hint: minimize display
}
```

### Wire (Connection) Definition

```typescript
interface Wire {
  id: string;                    // Unique wire ID
  from: {
    nodeId: string;
    portId: string;
  };
  to: {
    nodeId: string;
    portId: string;
  };
  type: PortType;                // scalar | field | color | output
}
```

---

## 3. Built-in Node Library

### Generator Nodes (No Inputs)

#### Gradient
- **Purpose:** Create linear color gradients
- **Outputs:** `field` (0–1 range)
- **Parameters:**
  - `start` (slider, 0–100): Starting position
  - `end` (slider, 0–100): Ending position
  - `startColor` (select): Color at start
  - `endColor` (select): Color at end

#### Noise
- **Purpose:** Perlin/Simplex noise for organic patterns
- **Outputs:** `field` (0–1 range)
- **Parameters:**
  - `scale` (slider, 1–100): Noise frequency
  - `speed` (slider, 0–10): Animation speed
  - `octaves` (number, 1–8): Noise complexity

### Spatial Nodes

#### Grid
- **Purpose:** Convert linear position to 2D grid
- **Inputs:** `field`
- **Outputs:** `field`
- **Parameters:**
  - `cols` (number): Grid width
  - `rows` (number): Grid height

#### Repeat
- **Purpose:** Repeat pattern N times
- **Inputs:** `field`
- **Outputs:** `field`
- **Parameters:**
  - `count` (number, 1–50): Repetitions
  - `offset` (slider): Phase offset between repeats

### Modifier Nodes

#### Ramp
- **Purpose:** Smooth transitions between values
- **Inputs:** `scalar`
- **Outputs:** `scalar`
- **Parameters:**
  - `easing` (select): Ease function (linear/ease-in/ease-out/ease-in-out)
  - `sharpness` (slider, 0–100): Curve steepness

#### Smooth
- **Purpose:** Gaussian blur on field
- **Inputs:** `field`
- **Outputs:** `field`
- **Parameters:**
  - `radius` (slider, 0.5–50): Blur radius in pixels
  - `iterations` (number, 1–5): Blur passes

### Color Nodes

#### Hue Shift
- **Purpose:** Rotate color around hue wheel
- **Inputs:** `color`, `scalar` (amount)
- **Outputs:** `color`
- **Parameters:**
  - `hue` (slider, -180–180): Hue rotation in degrees

#### Saturate
- **Purpose:** Increase/decrease color saturation
- **Inputs:** `color`, `scalar` (amount)
- **Outputs:** `color`
- **Parameters:**
  - `saturation` (slider, 0–200): Saturation multiplier

### Combine Nodes

#### Blend
- **Purpose:** Mix two colors
- **Inputs:** `color` (A), `color` (B), `scalar` (mix amount)
- **Outputs:** `color`
- **Parameters:**
  - `blend` (slider, 0–100): Mix ratio
  - `mode` (select): Blend mode (mix/add/multiply/screen)

#### Add
- **Purpose:** Additive color mixing
- **Inputs:** `color` (A), `color` (B)
- **Outputs:** `color`

### Output Node

#### K1 Output
- **Purpose:** Render computed color field to LED frame buffer
- **Inputs:** `color` (primary), `scalar` (brightness, optional)
- **Outputs:** None (terminal node)
- **Parameters:** None
- **Behavior:** Produces 320 × 3 bytes RGB8 frame

---

## 4. Engine Configuration

### Preview Specification
```typescript
const PREVIEW_SPEC = {
  length: 320,      // 320 pixels
  fps: 120 as Fps,  // Default FPS
};

type Fps = 120 | 60 | 30;  // Selectable options
```

### Engine Configuration
```typescript
const ENGINE_CONFIG = {
  pixelCount: 320,
  colorFormat: 'RGB8' as const,
  mapping: 'concat-2x160',
  channels: [
    { gpio: 9, count: 160, start: 0, end: 159 },
    { gpio: 10, count: 160, start: 160, end: 319 },
  ],
  map: Array.from({ length: 320 }, (_, i) => i),  // Identity map
};
```

### Frame Data Structure
```typescript
type RGB8 = [number, number, number];  // 8-bit R, G, B
type Frame = RGB8[];                   // 320 pixels
type FrameBuffer = Uint8Array;         // 960 bytes (320 × 3)
```

---

## 5. Color Space Transforms

### sRGB ↔ Linear (Gamma Correction)
```typescript
export function srgb8ToLinear(c: number): number {
  const v = c / 255;
  return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
}

export function linearToSrgb8(v: number): number {
  const s = v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
  return Math.round(clamp01(s) * 255);
}
```

### Linear ↔ OKLab (Perceptual)
```typescript
// OKLab: Perceptually uniform color space
// Better for animation because distances = perceived differences

interface OKLab {
  L: number;  // Lightness (0–1)
  a: number;  // Green-Red axis
  b: number;  // Blue-Yellow axis
}

function oklabFromLinear([r, g, b]): [number, number, number]
function linearFromOklab([L, a, b]): [number, number, number]
```

### OKLab ↔ OKLCH (Hue-Saturation-Lightness)
```typescript
// OKLCH: Cylindrical representation of OKLab
// Separates hue from saturation, easier for rotations

interface OKLCH {
  L: number;       // Lightness (0–1)
  C: number;       // Chroma (saturation-like, 0–0.4)
  H: number;       // Hue (0–360 degrees)
}
```

### Usage Pattern
```typescript
// Example: Rotate hue while preserving brightness
const rgb8: RGB8 = [255, 128, 0];  // Orange

// 1. Convert to linear
const linear = rgb8ToLinear(rgb8);  // [1, 0.5, 0]

// 2. Convert to OKLCH
const oklch = rgbToOklch(linear);   // { L: 0.6, C: 0.2, H: 45 }

// 3. Modify hue
oklch.H = (oklch.H + 120) % 360;   // +120° → green

// 4. Convert back to RGB8
const result = oklchToRgb8(oklch);  // [0, 255, 128]
```

---

## 6. WebSocket Transport (TLV Protocol)

### Connection Setup
```typescript
const ws = new WebSocket('ws://device-ip:8080');
ws.binaryType = 'arraybuffer';
```

### TLV Message Format

**Type-Length-Value serialization:**
- **Type:** 1 byte (0x01/0x02/0x03)
- **Length:** 2 bytes (little-endian uint16)
- **Value:** N bytes (raw payload)

```typescript
enum TLVType {
  PUT_BEGIN = 0x01,  // Payload size header
  PUT_DATA = 0x02,   // Data chunk
  PUT_END = 0x03,    // CRC32 checksum
}

interface TLV {
  type: TLVType;
  length: number;
  value: Uint8Array;
}
```

### TLV Message Types

#### PUT_BEGIN (0x01)
- **Value:** 4 bytes (uint32-LE total payload size)
- **Purpose:** Signal incoming pattern, total size
- **Example:** Pattern 256KB → value = 262144 (0x0004_0000 in little-endian)

#### PUT_DATA (0x02)
- **Value:** 4089 bytes max (4 byte offset LE + 4085 bytes data)
- **Structure:**
  - Bytes 0–3: Offset in payload (uint32-LE)
  - Bytes 4–4088: Pattern data chunk
- **Count:** Total payload / 4085, rounded up
- **Example:** 256KB payload = 63 PUT_DATA messages

#### PUT_END (0x03)
- **Value:** 4 bytes (uint32-LE CRC32 checksum)
- **Purpose:** Validate pattern integrity
- **CRC32 Polynomial:** 0xEDB88320 (standard)

### Transaction Example

```
Client → Device PUT_BEGIN(262144)     // 256KB pattern
Client → Device PUT_DATA(0, 4085B)    // Bytes 0–4084
Client → Device PUT_DATA(4085, 4085B) // Bytes 4085–8169
... (61 more PUT_DATA chunks)
Client → Device PUT_END(0x12345678)   // CRC32 checksum

Device: Validates CRC32
Device: Stores pattern to /littlefs
Device: Sends ACK (firmware-dependent)
```

### Helper Functions

```typescript
export const PAYLOAD_MAX = 262_144;     // 256KB max pattern
export const PUT_DATA_MAX = 4_089;      // Per chunk

export function makePutPlan(bytes: Uint8Array): {
  tlvs: TLV[];
  total: number;
  crc: number;
}

export function serializePlan(plan): Uint8Array {
  // Combines all TLV messages into single byte array
}

export function dryRunReport(plan): string {
  // Returns debug info: "TLV plan: totalBytes=262144 | chunks=63 | CRC32=0x..."
}

export async function sendPlanOverWs(url: string, plan): Promise<void> {
  // Opens WebSocket, sends all TLV messages, closes
}
```

---

## 7. App Component Structure

### Main Entry Point
- **File:** `src/main.tsx`
- **Bootstrap:** React 18 root render

### Core Components

#### LightLab (`LightLab.tsx`)
**Purpose:** Master workspace controller, state management
- **Responsibilities:**
  - Manage nodes & wires state
  - Export payload generation
  - Real-time preview update loop
  - WebSocket connection management
- **State:** `nodes[]`, `wires[]`, `selectedNode`, `previewFps`

#### K1Toolbar (`K1Toolbar.tsx`)
**Purpose:** Top toolbar, export & FPS controls
- **Features:**
  - Export button (downloads binary or sends via WS)
  - FPS selector dropdown (120/60/30)
  - Undo/redo
  - File load/save

#### NodeCanvas (`NodeCanvas.tsx`)
**Purpose:** Visual graph editor with node connections
- **Features:**
  - Drag nodes to reposition
  - Click & drag to create wires
  - Right-click context menu (delete, inspect)
  - Pan & zoom
  - Minimap

#### Node (`Node.tsx`)
**Purpose:** Individual node card UI
- **Features:**
  - Title & category color
  - Input/output port circles
  - Parameter sliders/selects
  - Compactness toggle

#### NodeInspector (`NodeInspector.tsx`)
**Purpose:** Right-side detail panel
- **Shows:** Selected node properties, parameters, connections
- **Allows:** Edit parameters, view data flow

#### NodeLibrary (`NodeLibrary.tsx`)
**Purpose:** Left sidebar, node catalog
- **Features:**
  - Filterable by category
  - Drag-to-canvas node creation
  - Search by name

### Engine (`engine.ts`)
**Purpose:** Color space math & frame rendering
- **Exports:**
  - `stubTick()` - Debug frame generator
  - `applyFrameCapRGB8()` - Brightness capping
  - Color transform functions
  - OKLCH conversion utilities

### Transport (`transport/wsTlv.ts`)
**Purpose:** WebSocket TLV serialization & sending
- **Exports:**
  - `makePutPlan()` - Create TLV message plan
  - `sendPlanOverWs()` - Send to device
  - `dryRunReport()` - Debug info

---

## 8. Data Flow & Export Pipeline

### Editor → Device Export Pipeline

```
User clicks "Export" in toolbar
       ↓
LightLab.tsx collects:
  - All nodes & wires
  - Parameter values
  - Preview settings (FPS)
       ↓
engine.ts runs graph:
  - Evaluates all nodes
  - Computes 320 RGB8 colors
  - Returns Uint8Array(960)
       ↓
transport/wsTlv.ts packages:
  - makePutPlan(960 bytes)
  - Creates TLV messages
  - Calculates CRC32
       ↓
sendPlanOverWs() transmits:
  - Opens WebSocket
  - Sends PUT_BEGIN
  - Chunks into PUT_DATA (4089 bytes each)
  - Sends PUT_END with CRC32
  - Closes WebSocket
       ↓
Firmware receives:
  - Validates CRC32
  - Stores pattern to /littlefs
  - Playback task reads next frame
  - LEDs render 320-pixel pattern at 120 FPS
```

---

## 9. Real-Time Preview

### Canvas Preview Rendering
- **Canvas size:** 320 pixels wide × variable height
- **Pixel format:** RGB8 (3 bytes per pixel)
- **Rendering:** Immediate (no debounce)
- **FPS options:** 30, 60, 120 (matches device capability)

### Frame Update Loop
```typescript
// Pseudocode from LightLab.tsx
setInterval(() => {
  const frame = engine.evaluate(nodes, wires);  // 960 bytes
  setPreview(frame);
  canvas.drawPixels(frame);
}, 1000 / previewFps);
```

---

## 10. Quick Integration Examples

### Creating a Custom Node

```typescript
const customNode: NodeData = {
  id: "mynode-1",
  title: "My Custom Effect",
  category: "modifier",
  icon: "✨",
  inputs: [
    { id: "field", label: "Input Field", type: "field" },
  ],
  outputs: [
    { id: "output", label: "Output", type: "field" },
  ],
  parameters: [
    { id: "intensity", label: "Intensity", type: "slider", value: 50, min: 0, max: 100, step: 1 },
  ],
  position: { x: 100, y: 100 },
};
```

### Sending Pattern to Device

```typescript
import { makePutPlan, sendPlanOverWs } from './transport/wsTlv';

const patternBytes = new Uint8Array(/* 960 bytes of RGB8 data */);
const plan = makePutPlan(patternBytes);
console.log(dryRunReport(plan));  // Debug: "TLV plan: ..."
await sendPlanOverWs('ws://192.168.1.100:8080', plan);
```

### Accessing Engine Config in Code

```typescript
import { ENGINE_CONFIG, PREVIEW_SPEC } from './engine';

console.log(ENGINE_CONFIG.pixelCount);   // 320
console.log(ENGINE_CONFIG.mapping);      // "concat-2x160"
console.log(ENGINE_CONFIG.channels);     // GPIO 9 & 10 info
console.log(PREVIEW_SPEC.fps);           // 120 (default)
```

---

## 11. Type Reference

### All Exported Types

```typescript
// Core types
export type PortType = 'scalar' | 'field' | 'color' | 'output';
export type NodeCategory = 'generator' | 'spatial' | 'modifier' | 'color' | 'combine' | 'output';
export type Fps = 120 | 60 | 30;
export type RGB8 = [number, number, number];

// Interfaces
export interface Port { id: string; label: string; type: PortType; }
export interface NodeParameter { id: string; label: string; type: 'slider' | 'select' | 'number' | 'toggle'; value: any; min?: number; max?: number; step?: number; options?: string[]; }
export interface NodeData { id: string; title: string; category: NodeCategory; icon: string; inputs: Port[]; outputs: Port[]; parameters?: NodeParameter[]; position: { x: number; y: number }; compact?: boolean; }
export interface Wire { id: string; from: { nodeId: string; portId: string }; to: { nodeId: string; portId: string }; type: PortType; }

// TLV types
export enum TLVType { PUT_BEGIN = 0x01, PUT_DATA = 0x02, PUT_END = 0x03 }
export interface TLV { type: TLVType; length: number; value: Uint8Array; }
```

---

## 12. Configuration & Constants

### Device Configuration
- **Pixel count:** 320 (from CANON.md)
- **Color format:** RGB8 (3 bytes per pixel)
- **Mapping:** Concat-2x160 (GPIO 9+10 parallel)
- **Max pattern size:** 256KB (262,144 bytes)
- **WebSocket timeout:** 5 seconds
- **WebSocket buffer:** 4096 bytes

### UI Colors
- **Scalar port:** Amber (#F59E0B)
- **Field port:** Cyan (#22D3EE)
- **Color port:** Pink (#F472B6)
- **Output port:** Emerald (#34D399)

---

## 13. Performance Optimization Tips

### Tips for Smooth Editing
1. **Preview FPS:** Set to 30 if graph has 20+ nodes
2. **Node count:** Keep under 50 for real-time feedback
3. **WebSocket chunks:** Max 4089 bytes per message (auto-handled)
4. **CRC32:** Calculated client-side, doesn't block export

### Debugging
- **Browser DevTools:** F12 → Network tab → WS messages
- **Firmware logs:** UART 115200 baud (see PRISM.k1 Firmware Skill)
- **Export dry-run:** Call `dryRunReport(plan)` before sending

---

## 14. External API Contracts

### Firmware Expects (from PRISM.k1 Firmware Skill)
- **WebSocket at:** `ws://device:8080` (default, configurable)
- **TLV format:** Exactly as specified (PUT_BEGIN → PUT_DATA* → PUT_END)
- **CRC32:** Must validate; firmware rejects mismatches
- **Pattern max:** 256KB (enforced)

### Device Provides (to PRISM.node)
- **WebSocket endpoint:** Opens after boot
- **Pattern storage:** LittleFS at `/littlefs`
- **LED output:** 120 FPS refresh (CANON.md ADR-008)
- **Acknowledgment:** Optional (depends on firmware implementation)

---

## 15. Testing Checklist

- [ ] Canvas renders 320 pixels?
- [ ] Nodes connect with colored wires (port type matches)?
- [ ] Parameters update preview in real-time?
- [ ] Export button generates TLV messages?
- [ ] CRC32 calculates correctly?
- [ ] WebSocket connects to device?
- [ ] Pattern appears on LEDs after send?
- [ ] FPS selector updates preview rate?
- [ ] Undo/redo works?

---

**This specification reflects shipping Phase A code. Updates to types.ts, engine.ts, or transport/wsTlv.ts require version bump and regeneration of this skill.**

*Last updated: 2025-10-21 by Claude Code Captain*
