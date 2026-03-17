---
name: visual-designing
description: 视觉设计工具箱 - Canvas / Themes / Design System / Artifacts。The unified Visual Design Engine for Antigravity.
---

# Visual Design System
*Unified Design Engine v1.0*

## Purpose
A single source of truth for all UI/UX design tasks. This skill intelligently switches between "Production Efficiency" (Standard) and "Wow Factor" (Premium) based on user intent.

## 🧭 Design Modes

| Mode | Trigger | Focus | Style Traits |
| :--- | :--- | :--- | :--- |
| **Standard (Production)** | "create a dashboard", "login form", "settings page" | Usability, Speed, Accessibility | Tailwind utility-first, clean whites/darks, standard shadcn/ui components. |
| **Premium (Aesthetic)** | "premium", "glassmorphism", "wow me", "landing page" | Visual Impact, Emotion, Brand | Glass effects, Aurora gradients, Micro-interactions, custom CSS variables. |

## 🛠️ Execution Protocol

1.  **Analyze Aesthetic Intent**: Does the user want a solid tool (Standard) or a piece of art (Premium)?
2.  **Load Resources (Premium Only)**:
    - If Premium/Glass/Motion is requested, you **MUST** read:
        - `resources/glass-components.md` (for glass CSS)
        - `resources/premium-palettes.md` (for gradients/colors)
        - `resources/micro-interactions.md` (for animations)
3.  **Generate CSS/Tailwind**:
    - **Standard**: Use standard Tailwind (`bg-white`, `text-slate-900`, `rounded-lg`).
    - **Premium**: Use `backdrop-filter`, `bg-white/10`, `border-white/20`, and custom animations.

## 📐 Core Principles (All Modes)
1.  **Mobile First**: Always responsive.
2.  **Dark Mode Ready**: All specific colors must have dark mode equivalents.
3.  **Accessibility**: No ultra-low contrast text, even in "Premium" mode.

## 🚫 Anti-Patterns
- **Mixing Metaphors**: Don't put a hyper-realistic glass card inside a flat material design dashboard. Commit to one style.
- **Over-Animation**: Motion should facilitate understanding, not distract.
