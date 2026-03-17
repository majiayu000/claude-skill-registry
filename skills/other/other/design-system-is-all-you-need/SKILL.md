---
name: design-system-is-all-you-need
description: This skill provides a curated set of cross-platform design guideline prompts for building consistent, high-quality UIs. Each guideline defines common rules, component-specific guides, and an auto-derived token system — all driven by minimal user inputs.
---

## When to Use
Activate this skill whenever the user requests UI/UX design work, frontend implementation, component creation, or any visual design task — including but not limited to:
- Creating web pages, apps, dashboards, or landing pages
- Building UI components (buttons, cards, forms, modals, etc.)
- Designing or prototyping interfaces
- Generating frontend code (HTML/CSS, React, SwiftUI, Jetpack Compose, etc.)

---

## CRITICAL: Mandatory Design Guideline Selection Flow

**You MUST follow the three-step flow below IN ORDER before producing any design or code output.
Do NOT skip any step. Do NOT assume defaults. Do NOT proceed until each step is confirmed by the user.**

### Step 1 — Select a Design Guideline

If the user has NOT already specified which design style to use, you MUST stop and ask them to choose from the available guidelines:

**Available Design Guidelines:**
| # | Style | File | Description |
|---|-------|------|-------------|
| 1 | **Neumorphism** (Soft UI) | `references/neumorphism.md` | Extruded/pressed soft surfaces with dual-directional shadows on a matte background |
| 2 | **Glassmorphism** (Frosted Glass UI) | `references/glassmorphism.md` | Translucent frosted glass panels layered over rich, vibrant backgrounds |
| 3 | **Brutalism** (Raw UI)| `references/brutalism.md` | Exposed structural elements with thick borders, hard-edge shadows, and aggressive typography on flat surfaces |
| 4 | **Skeuomorphism** (Realistic UI) | `references/skeuomorphism.md` | Tangible, material-driven surfaces with realistic gradients, textures, highlights, and physically weighted interactions |
| 5 | **Material Design** (Material You / M3) | `references/material-design.md` | Layered adaptive surfaces with tonal color palettes, systematic elevation, and physically informed motion |
| 6 | **Pnalism** (Two-Tone Minimal, Pnal's UI) | `references/pnalism.md` | Disciplined two-tone color system with zero shadows, relying solely on typography, whitespace, and precise accent placement |
| 7 | **Neon** (Glow UI) | `references/neon.md` | Dark-first luminous interfaces with multi-layer colored glow effects simulating electric neon tube signage |
| 8 | **Heritage** (Warm Editorial UI) | `references/heritage.md` | Warm earthy tonal surfaces with serif/script typography, organic image shapes, and editorial asymmetric layouts |


Present these options clearly and wait for the user's choice. If the user describes a style that clearly maps to one of the above (e.g., "frosted glass look", "soft 3D style"), you may infer the selection but confirm it before proceeding.

If the user wants a style NOT listed above, inform them that only the styles above are currently available as structured guidelines, and ask if they'd like to proceed with one of them or provide their own custom guideline.

### Step 2 — Read the Selected Guideline

Once the user has chosen a guideline, immediately read the corresponding file from the `references/` folder:

- Neumorphism → Read `references/neumorphism.md`
- Glassmorphism → Read `references/glassmorphism.md`
- Brutalism → Read `references/brutalism.md`
- Skeuomorphism → Read `references/skeuomorphism.md`
- Meterial Design → Read `references/meterial-design.md`
- Pnalism → Read `references/pnalism.md`
- Neon → Read `references/neon.md`
- Heritage → Read `references/heritage.md`

Internalize ALL rules from the selected guideline — both common rules and component-specific guides. These rules govern every design decision from this point forward.

### Step 3 — Collect Required User Inputs

Each guideline requires exactly **two user inputs**. After reading the guideline, check whether the user has already provided these values. If ANY value is missing, you MUST ask for it before producing any output.

**For Neumorphism:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #6C63FF)
2. **Shadow Intensity** (`--shadow-intensity`): `subtle` | `medium` | `strong`

**For Glassmorphism:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #6C63FF)
2. **Blur Intensity** (`--blur-intensity`): `light` | `medium` | `heavy`

**For Brutalism:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #FF5733)
2. **Rawness Level** (`--rawness`): `moderate` | `raw` | `extreme`

**For Skeuomorphism:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #3A7BD5)
2. **Realism Depth** (`--realism`): `refined` | `classic` | `rich`

**For Material Design:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #6750A4)
2. **Elevation Style** (`--elevation-style`): `flat` | `tonal` | `shadow`

**For Pnalism:**
1. **Theme Color** (`--theme-color`): A hex color code (e.g., #4A7DFF)
2. **Density** (`--density`): `compact` | `comfortable` | `spacious`

**For Neon**:
1. Theme Color (`--theme-color`): A hex color code (e.g., #FF00FF)
2. Glow Intensity (`--glow-intensity`): `dim` | `standard` | `vivid`

**For Heritage:**
1. Theme Color (`--theme-color`): A hex color code (e.g., #C4A882)
2. Warmth Level (`--warmth`): `subtle` | `classic` | `rich`

When asking, provide brief descriptions and examples so the user can make an informed choice. Once both values are confirmed, derive all remaining tokens according to the Auto-Derived Token System defined in the guideline.

---

## After the Flow is Complete

Once all three steps are done, you have:
- A selected design guideline (fully read and internalized)
- Two confirmed user inputs
- A complete set of auto-derived design tokens

From this point, apply the guideline strictly to ALL design and code output. Specifically:
- Follow every rule in the **Common Rules** section without exception.
- Apply the **Component-Specific Guides** whenever creating or modifying the relevant component.
- Use the **Final Checklist** at the end of the guideline to verify every deliverable before presenting it to the user.

## Important Notes
- If the user changes the theme color or intensity mid-conversation, recalculate ALL derived tokens before producing new output.
- If the user requests a component not covered in the component-specific guides, apply the common rules and extrapolate the closest matching component's guide.
- The guideline is platform-agnostic. Apply the same visual rules whether outputting HTML/CSS, React, Swift, Kotlin, Flutter, or design specifications.
- Always prioritize accessibility requirements defined in the guideline (WCAG AA contrast, touch targets, focus indicators).
