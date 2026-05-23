---
name: asset-placement-strategy
description: Specialized logic for strategic placement of Northcote Curio design artifacts (Seeds, Pebbles, Lenses, Stones) based on biological asymmetry and curiosity specimen aesthetics. Ensures organic balance and avoids "slop" by enforcing strict archetype constraints and structural integrity.
---

# Asset Placement Strategy Skill

This skill provides a framework for placing design "artifacts" within the Northcote Curio design system. It moves beyond standard layouts to prioritize **biological asymmetry**, **tactility**, and **curiosity-specimen** aesthetics.

## Core Principles

1. **Strategic Asymmetry**: Avoid perfect grid alignment for decorative elements. Use prime numbers and organic offsets (3px, 5px, 8px) to create a "found object" feel.
2. **Archetype Integrity**:
   - **Seeds**: Place sparingly as focal points or status indicators. Never cluster more than 3 in a horizontal line.
   - **Pebbles**: Use for secondary interactions. Root them to the bottom-right or top-left of parent containers to simulate "settling."
   - **Lenses**: Center-align for primary search or observation tasks. Surround with generous whitespace to simulate a magnifying glass view.
   - **Stones**: The structural foundation. Use variable corner radii (e.g., `rounded-[24px_32px_16px_40px]`) to simulate natural erosion.
3. **Specimen Mounting**: Treat content as if it were pinned in a curiosity cabinet. Use subtle borders (`border-leaf-base/20`) and heavy shadows on hover to simulate depth.

## Placement Workflow

### 1. Identify Anchor Points

Determine where the eye naturally rests. Place a **Seed** or **Pebble** at the end of a primary reading path (bottom-right).

### 2. Apply "Organic Drift"

Offset secondary elements by a small, non-standard amount.

- _Example_: `margin-left: 7.5%` instead of `8%`.

### 3. Layer for Depth

Use the Z-index system to stack "specimen cards" (Stones).

- **Z-0**: Background (Cloth/Linen texture)
- **Z-10**: Main Vessel
- **Z-20**: Interactive Overlays (Lenses/Seeds)

## Slop Prevention

- **NO Generic Containers**: Every `div` must have an archetype (`Stone`, `Vessel`, `Cabinet`).
- **NO Default Radii**: Avoid `rounded-xl`. Always define specific asymmetric radii.
- **NO Flat Colors**: Use the HSL-based Curio palette with alpha transparency for layering.

## Verification Checklist

- [ ] Does the layout feel "found" rather than "built"?
- [ ] Are the corner radii asymmetric and intentional?
- [ ] Is there a clear focal point (Seed/Lens)?
- [ ] Does the element respond to touch/hover with a "tactile" spring?
