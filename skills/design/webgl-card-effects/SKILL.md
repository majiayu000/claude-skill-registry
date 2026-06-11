---
name: webgl-card-effects
description: "Standalone WebGL fragment shaders for card visual effects: holographic foil, shimmer, rarity glow."
agent: typescript-frontend-engineer
user-invocable: false
command: /card-effects
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - card effects
    - holographic
    - foil effect
    - card shimmer
    - card glow
    - shader card
    - WebGL card
    - rarity effects
    - Balatro effect
    - card visual effects
  pairs_with:
    - typescript-frontend-engineer
    - ui-design-engineer
  complexity: Medium
  category: frontend
---

# WebGL Card Effects Skill

## Overview

This skill adds GPU-accelerated visual effects to React card components using standalone WebGL2 fragment shaders — no Three.js, no R3F, no external library required. It targets deckbuilder games and card UIs where rarity tiers should feel visually distinct, not just differentiated by a CSS `box-shadow` value.

**Scope**: Holographic foil overlays, metallic shimmer bands, rarity-driven energy pulses, and interactive tilt-shine effects mounted directly on React card components. The canonical target is `FramedCard.tsx` in a React 19 / Vite / Tailwind project with a rarity system (starter → common → uncommon → rare → legendary).

**Not in scope**: 3D transformations, texture loading, post-processing pipelines, or any Three.js scene management. For those, use `threejs-builder`.

**Key constraint**: Browsers cap WebGL contexts at roughly 8–16 total per page. This skill uses a single shared WebGL2 context with blit-to-2D-canvas output per card, avoiding the per-card context problem entirely. See `references/shader-integration-react.md` for the full singleton pattern.

---

## Instructions

### Phase 1: ASSESS

**Goal**: Understand which effects are needed and confirm the card component structure before writing any code.

**Step 1: Read the card component**

Read these files before writing anything:
- `src/components/cards/FramedCard.tsx` — component structure, hover state, rarity prop flow
- `src/components/cards/cardStyles.ts` — `CARD_SIZE_CONFIG` for pixel dimensions, rarity string values

Confirm:
- How rarity reaches the component (prop name, TypeScript type, exact string values)
- Whether `isHovered` state already exists in the component
- Which sizes are rendered in contexts that justify shader cost (xl/lg only — xs/sm are too small)
- Whether `showShine` / `card-shine` CSS exists and needs coordination

**Step 2: Select effect tier per rarity**

| Rarity | WebGL? | Effect |
|--------|--------|--------|
| starter / common | No | CSS shimmer only — no WebGL overhead |
| uncommon | Yes (subtle) | Metallic band shimmer, very low opacity |
| rare | Yes (medium) | Moving shimmer + blue hue shift + edge pulse |
| legendary | Yes (full) | Rainbow holographic foil, mouse-reactive tilt |

**Step 3: Confirm React version**

Check `package.json` for the React version. This skill assumes React 19 (ref as prop, no forwardRef). If the project uses React 18, canvas refs require `useRef` + standard ref passing.

**Gate**: Rarity values confirmed, CARD_SIZE_CONFIG read, effect tiers decided. Proceed only when this gate passes.

---

### Phase 2: BUILD

**Goal**: Write working GLSL shaders and the WebGL initialization harness.

Load `references/card-shader-patterns.md` now.

**Step 1: Create the shader strings module**

Create `src/components/cards/effects/cardShaders.ts`. This file holds:
- The shared vertex shader (passthrough UV coordinates)
- Three fragment shader strings: `SHIMMER_FRAG`, `RARE_FRAG`, `LEGENDARY_FRAG`
- A `rarityToUniform(rarity: string): number` mapping function

Every shader must expose this exact uniform interface:

```glsl
uniform float u_time;        // seconds elapsed, JS wraps at 1000.0
uniform float u_rarity;      // 0.0=starter/common, 0.25=uncommon, 0.5=rare, 1.0=legendary
uniform float u_hover;       // 0.0 to 1.0, lerped by JavaScript each frame
uniform vec2  u_mouse;       // normalized card-space [0,1] mouse position
uniform vec2  u_resolution;  // canvas pixel dimensions (width, height)
uniform float u_upgraded;    // 0.0 or 1.0 — upgraded cards get slightly more intense effect
```

**Step 2: Create the WebGL harness hook**

Create `src/components/cards/effects/useCardShader.ts`.

Load `references/shader-integration-react.md` for the full hook source. The hook must:
- Use the shared WebGL2 context singleton (not create a new context per card)
- Accept `{ rarity, isHovered, isUpgraded, enabled }` as input
- Return a `RefObject<HTMLCanvasElement>` that the component attaches to the canvas element
- Pause the animation loop when the card is off-screen (IntersectionObserver)
- Run at 30fps maximum via delta-time throttle
- Clean up the RAF loop and observer on unmount

**Step 3: Shader construction for each tier**

Load `references/balatro-shader-breakdown.md` for the legendary holographic shader GLSL source.

For rare: use the shimmer band + hue shift layer from the breakdown, omit the rainbow foil layer.

For uncommon: use only the metallic band pass (single moving highlight), opacity 0.3 maximum.

**Gate**: Run `npx tsc --noEmit`. Zero TypeScript errors. Open browser console and verify `gl.getShaderInfoLog()` returns empty string for all shaders.

---

### Phase 3: INTEGRATE

**Goal**: Mount the canvas overlay on `FramedCard.tsx` and wire rarity/hover state into the shader uniforms.

**Step 1: Derive render decision**

Inside `FramedCard`, after the existing `const shouldShine` line:

```tsx
const shouldRenderShader =
  ['uncommon', 'rare', 'legendary'].includes(rarity) &&
  size !== 'xs' &&
  size !== 'sm';
```

**Step 2: Call the hook**

```tsx
const shaderCanvasRef = useCardShader({
  rarity,
  isHovered,
  isUpgraded,
  enabled: shouldRenderShader,
});
```

**Step 3: Add the canvas overlay to JSX**

Inside the `motion.div` return, immediately after the frame `<img>` element (after z-10):

```tsx
{shouldRenderShader && (
  <canvas
    ref={shaderCanvasRef}
    className="absolute inset-0 w-full h-full pointer-events-none rounded-lg"
    style={{ zIndex: 15, mixBlendMode: 'screen' }}
  />
)}
```

`mix-blend-mode: screen` makes the shader's black background transparent while letting bright holographic colors add onto the card surface.

**Step 4: Coordinate with existing CSS shine**

The existing `card-shine` CSS class creates a gradient sweep on hover. It will double-shimmer with the WebGL effect. Suppress it for rarities that have the WebGL shader:

```tsx
const shineClass =
  showShine && shouldShine && !shouldRenderShader
    ? `card-shine ${...}`
    : '';
```

**Step 5: Verify z-layer stack**

From bottom to top inside the card:
- `z-0` — artwork container
- `z-10` — frame PNG image
- `z-15` — shader canvas (new)
- `z-20` — text elements (energy orb, name, description, type strip)
- Tooltip renders outside via `AnimatePresence` portal

Tailwind does not generate `z-15` by default. Either add it to `tailwind.config` or use `style={{ zIndex: 15 }}` inline (already shown above).

**Gate**: Cards render correctly at all sizes. Shader canvas is visible on uncommon/rare/legendary. No z-fighting between shader layer and frame image. TypeScript clean.

---

### Phase 4: POLISH

**Goal**: Performance verification, visual tuning, mobile fallback confirmation.

**Step 1: Performance audit**

Open Chrome DevTools → Performance tab. Record 5 seconds while hovering over a legendary card.

Targets:
- GPU usage: < 5% for a single legendary card
- Frame time: shader must not push game loop below 60fps
- No memory growth across multiple mount/unmount cycles (check Heap in Memory tab)

**Step 2: Mobile fallback verification**

```typescript
// In useCardShader.ts — call this once at module load
function supportsWebGL2(): boolean {
  try {
    const canvas = document.createElement('canvas');
    return !!canvas.getContext('webgl2');
  } catch {
    return false;
  }
}
```

On devices where `supportsWebGL2()` returns false, the hook returns a null ref and `shouldRenderShader` must evaluate to false. The existing `card-shine` CSS handles the fallback. Verify this works by temporarily forcing the function to return false.

**Step 3: Visual calibration**

- **Legendary**: Rainbow visible but not garish. Effective opacity 0.65–0.75 over the card. Animation speed: `u_time` advances at 0.5× real-time (not 1:1 — too fast feels cheap).
- **Rare**: Blue hue shift + shimmer. Feels premium, not like a cursor glow effect.
- **Uncommon**: Barely perceptible silver shimmer. If you notice it immediately on a static card, the opacity is too high.
- **Mouse tilt**: The holographic angle shift should feel like physically tilting a card under light, not like a flashlight following the cursor. Limit the angular response to ±15 degrees of apparent rotation.

**Step 4: Test across all rendered sizes**

| Size | Width | Shader? | Note |
|------|-------|---------|------|
| xs | 80px | No | Too small — no overhead |
| sm | 110px | No | Too small — no overhead |
| md | 140px | Optional | Test legibility first |
| lg | 170px | Yes | Minimum size for full effect |
| xl | 200px | Yes | Primary target — should look best |

**Gate**: All DevTools performance targets met. Mobile fallback verified. Visual quality approved at lg and xl sizes across all three shader tiers.

---

## Error Handling

### "WebGL: INVALID_OPERATION: useProgram: program not valid"
Shader compilation failed silently. Call `gl.getShaderInfoLog(shader)` immediately after `gl.compileShader(shader)`. Common causes: GLSL syntax error, wrong `#version 300 es` directive missing, or a uniform declared but never referenced (GLSL compilers strip unused uniforms — reference them or remove the declaration).

### Canvas present but effect invisible
Check `mixBlendMode`. On very dark card backgrounds, `screen` blend mode makes dark shader output invisible. For debugging, switch to `normal` blend mode to see the raw shader output. Also verify the canvas `zIndex` is above the frame PNG (15 > 10).

### Browser console: "Too many active WebGL contexts"
The shared context singleton in `useCardShader` is not being used — individual hook calls are each creating a new context. Verify the module-level singleton is initialized once and reused. See the singleton pattern in `references/shader-integration-react.md`.

### Canvas appears stretched or distorted on high-DPI displays
Canvas `width` / `height` attributes must match physical pixel dimensions, not CSS dimensions. CSS `w-full h-full` sets display size only. Use a `ResizeObserver` on the canvas element: `canvas.width = entry.contentRect.width * devicePixelRatio`.

### TypeScript error: "Property 'ref' does not exist on 'HTMLCanvasElement'"
React 19 passes ref as a prop. The canvas element should be `<canvas ref={shaderCanvasRef} ... />` — no forwardRef needed. Ensure the ref type matches: `useRef<HTMLCanvasElement>(null)`.

---

## Reference Loading Table

| Task | Reference File |
|------|---------------|
| Fragment shader GLSL source | `references/card-shader-patterns.md` |
| React 19 WebGL hook + context pool | `references/shader-integration-react.md` |
| Balatro holographic foil breakdown | `references/balatro-shader-breakdown.md` |

Load only the reference needed for the current phase. All three together is ~1,400 lines — only load all three if implementing everything in one pass.
