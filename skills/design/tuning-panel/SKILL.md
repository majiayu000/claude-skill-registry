---
name: tuning-panel
description: Create visual parameter tuning panels for iterative adjustment of animations, layouts, colors, typography, physics, or any numeric/visual values. Use when the user asks to "create a tuning panel", "add parameter controls", "build a debug panel", "tweak parameters visually", "fine-tune values", "dial in the settings", or "adjust parameters interactively". Also triggers on mentions of "leva", "dat.GUI", or "tweakpane".
---

# Tuning Panel Skill

Create bespoke parameter tuning panels that give users visual control over values they're iterating on. These panels surface all relevant parameters for the current task, enable real-time adjustment, and export tuned values in an LLM-friendly format.

## Core Philosophy

**Err on the side of exhaustive.** When a user is tuning something, surface every parameter that could reasonably affect the outcome. Missing a parameter forces context-switching; having "too many" parameters costs only scroll distance.

**Debug-mode only.** Tuning panels should never appear in production. Use environment checks, build flags, or URL parameters.

**Export changed values only.** LLM exports should show only what was tuned, not all 100+ parameters.

## Platform Selection

| Platform | Library | Reference |
|----------|---------|-----------|
| **React** | Leva (recommended) | [references/react-leva.md](references/react-leva.md) |
| **SwiftUI** | Native controls | [references/swiftui.md](references/swiftui.md) |
| **Vanilla JS** | Tweakpane or dat.GUI | [references/vanilla-js.md](references/vanilla-js.md) |

## Implementation Workflow

### Step 1: Identify All Tunable Parameters

Analyze the code being tuned and extract every parameter that affects the output. See [references/parameter-categories.md](references/parameter-categories.md) for exhaustive lists by domain.

**Common categories:**
- **Animation**: duration, delay, easing, spring physics (stiffness, damping, mass)
- **Layout**: padding, margin, gap, width, height, position
- **Visual**: colors, opacity, shadows, borders, transforms
- **Typography**: font size, line height, letter spacing, weight

**Discovery strategies:**
1. Search for magic numbers (any hardcoded numeric value)
2. Look for style objects (CSS-in-JS, inline styles, theme values)
3. Find animation definitions (Framer Motion, CSS transitions, SwiftUI animations)
4. Identify color values (hex, RGB, HSL anywhere in the file)
5. Check component props with numeric or color defaults
6. Examine CSS custom properties (`--var-name` declarations)

### Step 2: Create Debug-Mode Panel

Wrap the tuning panel so it only appears in development:

- **React**: `process.env.NODE_ENV === 'development'`
- **SwiftUI**: `#if DEBUG`
- **Vanilla JS**: URL parameter `?debug` or environment check

See platform-specific references for code patterns.

### Step 3: Implement Controls

Follow these principles:

1. **Group related parameters** using folders/sections
2. **Use appropriate control types**: sliders for numbers, color pickers for colors, dropdowns for enums
3. **Set sensible min/max/step values** based on the parameter domain
4. **Include presets** for common configurations
5. **Add reset buttons** to return to defaults

### Step 4: Add LLM Export

**Critical requirements:**

1. **Store defaults** at initialization for comparison
2. **Use tolerance for floats** (e.g., `Math.abs(a - b) > 0.001`)
3. **Filter to changed values only** - don't show unchanged parameters
4. **Format for readability** - group by category, use human-readable names

**Export format:**

```markdown
## Tuned Parameters for [ComponentName]

### Changed Values
- Duration: 300 → 450
- Spring Damping: 0.80 → 0.65
- Corner Radius: 12 → 16

### Apply These Values
Update the component at `src/components/Card.tsx:42` with the values above.
```

**Why this matters:**
- A panel might expose 100+ parameters
- Exporting all values wastes tokens and obscures what changed
- The `default → current` format makes diffs scannable

## Additional Resources

### Reference Files
- **[references/react-leva.md](references/react-leva.md)** - Complete React/Leva implementation guide
- **[references/swiftui.md](references/swiftui.md)** - SwiftUI native controls and export patterns
- **[references/vanilla-js.md](references/vanilla-js.md)** - Tweakpane and dat.GUI for plain JS
- **[references/parameter-categories.md](references/parameter-categories.md)** - Exhaustive parameter lists by domain

### Example Files
- **[examples/react-leva-animation.tsx](examples/react-leva-animation.tsx)** - Complete animation tuning panel
- **[examples/export-format.md](examples/export-format.md)** - Full LLM export template
