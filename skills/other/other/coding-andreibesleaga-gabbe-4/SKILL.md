---
name: vibe-coding
description: Translates high-level aesthetic or behavioral "vibe" requests (e.g., "Make it feel like 90s cyberpunk", "Apple-style minimalism") into concrete code changes (CSS, Animation, Copy).
triggers: [vibe, aesthetic, style, feel, atmosphere, theme, mood, redesign, make it pop]
context_cost: medium
---

# Vibe Coding Skill

## Goal
Translate abstract user intents ("Vibes") into concrete implementation details (Design Tokens, CSS, Animation, Tone of Voice).

## Flow

### 1. Vibe Analysis
**Input**: User Request (e.g., "Make the dashboard feel like a spaceship HUD")
**Action**: Decompose "The Vibe" into technical primitives.
*   **Color Palette**: High contrast? Neons? Pastels? Dark mode?
*   **Typography**: Monospace? Serif? Sans-Serif? Size/Weight?
*   **Motion**: Snappy? Float? ease-in-out? Glitch effects?
*   **Border/Shape**: Rounded? Sharp? Glassmorphism? Brutalist?

### 2. The "Vibe Translator" Persona
Adopt the `design-sys-arch` persona temporarily.
*   **Step 1**: Consult `design-tokens.json` or CSS variables.
*   **Step 2**: Propose a "Vibe Drift" (e.g., changing `--primary-color` from `#007bff` to `#00ffcc`).
*   **Step 3**: Generate a quick prototype of the change.

### 3. Implementation Patterns

#### A. Cyberpunk / Sci-Fi / HUD
*   **CSS**: `border: 1px solid var(--neon); box-shadow: 0 0 10px var(--neon);`
*   **Font**: Monospace (e.g., Fira Code, JetBrains Mono).
*   **Motion**: Glitch effects, scanning lines.

#### B. Clean / Minimal / "Apple"
*   **CSS**: `backdrop-filter: blur(20px); border-radius: 20px; box-shadow: 0 4px 24px rgba(0,0,0,0.05);`
*   **Font**: Systematic Sans-Serif (Inter, SF Pro).
*   **Motion**: Spring physics, subtle scales.

#### C. Brutalist / Retro
*   **CSS**: `border: 3px solid black; box-shadow: 4px 4px 0 black;`
*   **Font**: Bold headers, distinct serifs.
*   **Motion**: No easing, hard cuts.

### 4. Verification
*   ASK USER: "Does this match the vibe you were looking for?"
*   If NO -> Adjuest **Intensity** (e.g., "More neon", "Less blur").
