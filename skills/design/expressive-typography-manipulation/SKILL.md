---
description: Technical implementation guide for Maximum Expressive M3 Typography. Contains code patterns for Variable Font axis manipulation (`GRAD`, `WONK`, `wdth`), COLRv1 palette switching, and Framer Motion typographic animations.
name: expressive-typography-manipulation
---

# Expressive Typography Manipulation

**Purpose**: Provide copy-pasteable strategies for implementing "Extreme Variability" in React.
**Target Audience**: AI Agents & Frontend Engineers.

## 1. The Variable Font Token System

Define these CSS Variables to control axes globally.

```css
:root {
  /* --- The Workhorse (Lora/Serif) --- */
  --font-body: "Lora Variable", serif;
  /* Hover State: Grade Axis */
  --type-action-grade-rest: 0;
  --type-action-grade-hover: 150;

  /* --- The Expressive (Fraunces) --- */
  --font-display: "Fraunces Variable", serif;
  /* Personality Axes */
  --type-wonk-regular: 0;
  --type-wonk-hand: 1;
  --type-soft-sharp: 0;
  --type-soft-inky: 50;

  /* --- The Accent (Script/Color) --- */
  --font-flourish: "Birthstone Bounce", cursive;
  --font-cyberpunk: "Nabla", display;
}
```

## 2. "Layout-Safe" Interactions (The API)

Use this pattern to create interactive text that **does not reflow the page**.

### CSS Module / Styled Component

```tsx
import styled from "styled-components";

export const BreathingLabel = styled.span`
  font-family: var(--font-body);
  font-weight: 500;
  font-variation-settings: "GRAD" var(--type-action-grade-rest);
  transition: font-variation-settings 0.2s cubic-bezier(0.2, 0, 0, 1);

  &:hover {
    font-variation-settings: "GRAD" var(--type-action-grade-hover);
    cursor: pointer;
  }
`;
```

## 3. Motion-Driven Axis Animation (React)

Use `framer-motion` to map user inputs (Scroll, Mouse) to Font Axes.

### The "Scroll-Breathing" Header

_Header expands (Width) and gets wonkier (Wonk) as you scroll._

```tsx
import { motion, useScroll, useTransform } from "framer-motion";

export const LivingHeader = () => {
  const { scrollYProgress } = useScroll();

  // Transform scroll (0-1) to Axis Values
  const width = useTransform(scrollYProgress, [0, 1], [100, 50]); // Compresses on scroll
  const wonk = useTransform(scrollYProgress, [0, 0.5], [0, 1]); // Gets irregular

  return (
    <motion.h1
      style={{
        fontFamily: "var(--font-display)",
        // Map MotionValues directly to variation settings string
        fontVariationSettings: `"wdth" ${width}, "WONK" ${wonk}, "SOFT" 50`,
      }}
    >
      Northcote Curio
    </motion.h1>
  );
};
```

## 4. COLRv1 Palette Switching

Switch color themes programmatically without changing classes.

### Global CSS Setup

```css
/* Define Palettes */
@font-palette-values --palette-sepia {
  font-family: "Nabla";
  base-palette: 0;
}

@font-palette-values --palette-neon {
  font-family: "Nabla";
  base-palette: 1;
  override-colors: 0 #00ff00; /* Matrix Green Override */
}
```

### React Implementation

```tsx
export const CyberpunkText = ({ mode }: { mode: "day" | "night" }) => (
  <h1
    style={{
      fontFamily: "var(--font-cyberpunk)",
      fontPalette: mode === "day" ? "--palette-sepia" : "--palette-neon",
      transition: "font-palette 0.5s ease",
    }}
  >
    SYSTEM.INIT
  </h1>
);
```

## 5. The "Cursive Juxtaposition" Component

Pattern for mixing Clean + Handwritten.

```tsx
<div style={{ display: "grid", gridTemplateColumns: "1fr auto" }}>
  <h2 style={{ fontFamily: "var(--font-body)", fontWeight: 300 }}>Verified Compliance Audit</h2>

  {/* The "Human" Annotation */}
  <aside
    style={{
      fontFamily: "var(--font-flourish)",
      transform: "rotate(-5deg)",
      color: "var(--sys-color-tertiary)",
      fontSize: "1.5em",
    }}
  >
    (signed by Admin)
  </aside>
</div>
```

## 6. Actionable Implementation Checklist for Agents

When implementing typography:

1.  **Check for `font-weight: bold` on hover**:
    - ❌ **DENIED**.
    - ✅ **RESTRUCTURE** to use `'GRAD' 150` variation.

2.  **Check for Static Imports**:
    - ❌ `import './Lora-Bold.ttf'`
    - ✅ `import './Lora-Variable.ttf'`

3.  **Check for "Boring" Headers**:
    - If Header is > 32px and STATIC, **PROPOSE** adding `useScroll` motion to specific axes (`wdth`, `opsz`).

4.  **Optical Sizing**:
    - Ensure `font-optical-sizing: auto` is on the root element.

5.  **Cursive Usage**:
    - Only use Cursive for "Human" metadata or "Interrupting" thoughts. Never for structural navigation.
