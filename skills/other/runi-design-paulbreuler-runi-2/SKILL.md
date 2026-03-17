---
name: runi-design
description: Build UI components and pages following the runi design system. Use this skill when creating React components for runi—the HTTP client that catches spec drift, verifies AI-generated code, and reveals cross-API relationships. Design language reflects runi's German Shepherd nature: vigilant, protective, with ambient intelligence through subtle signal dots that demand investigation.
---

# runi Design System (Zen & Ryo Lu Principles)

This skill guides creation of UI components and pages following runi's "Zen" design system and Ryo Lu's (Cursor)
design principles for high-performance developer tools.

**Brand:** runi is vigilant, protective, and minimalist. The interface should feel like a "dark room" where content
is the only light.

**Philosophy:** "Collapse uncertainty into truth" through clarity and deliberate focus.

## Core Visual Logic (The Tokens)

1. **Zen "Ink" Surface Palette:**
   - **App Background:** `#080809` (Deep Ink)
   - **Surface:** `#111113` (Standard cards/sections)
   - **Raised:** `#1a1a1d` (Hover states/elevated UI)
   - **Border Subtle:** `oklch(0.2 0.01 240 / 0.4)` (Precision 1px strokes)
   - **The "Dark Room" Effect:** Use depth through surface shifts rather than shadows.

2. **Zen-Signal Mapping (Low-Chroma OKLCH):**
   - **Success (Green):** `oklch(0.75 0.1 150)` — Verified, spec-compliant.
   - **Warning (Amber):** `oklch(0.8 0.1 75)` — Drift detected, deprecations.
   - **AI (Purple):** `oklch(0.65 0.1 300)` — Generated content, suspect.
   - **Error (Red):** `oklch(0.65 0.12 25)` — Failures, critical debt.
   - **Accent (Blue):** `oklch(0.7 0.1 230)` — Brand actions (CTAs), focus.

3. **Zen Inactive State (Window Blur):**
   - When the window is blurred (`.window-blur`), significantly dim all elements.
   - Borders should drop to very low opacity: `oklch(... / 0.1)`.
   - Signals should lose chroma and brightness: `oklch(0.4 0.02 ...)`.
   - This maintains the "Dark Room" feel by letting content recede entirely when not in use.

4. **The "Signal" Rule:**
   - UI should be **90% Grayscale** (using the Ink palette).
   - **10% Signal:** Reserve color strictly for semantic meaning.
   - Eliminate "AI slop"—no massive shadows or unnecessary gradients.

5. **Typography:**
   - **UI:** Inter (system sans-serif) for all interface elements.
   - **Code/Specs:** JetBrains Mono for all data, JSON, and specifications.
   - Maintain a clear hierarchy with minimal visual noise.

6. **Animations:**
   - Animations must be "deliberate and calm".
   - Use **linear easing**.
   - Durations: **0.2s–0.4s**.

## Ryo Lu’s Feedback & "Zen" Application

1. **Clean Basics (No AI Slop):**
   - Eliminate unnecessary visual distractions.
   - No massive shadows, no decorative purple gradients.
   - No "mystery meat" buttons—icons should have clear tooltips or labels.

2. **Clarity over Jargon:**
   - Don't just show technical shorthand (e.g., "DCFs", "400").
   - Show the actual problem: "Field 'user_id' is missing from spec" or "Status code differs from OpenAPI definition".

3. **State Transparency (Vigilance Monitor):**
   - Every background state must be visible.
   - When AI verification or a background check is running, use a **"Vigilance Monitor"** progress bar that explicitly
     explains what is being checked (e.g., "Verifying request against user.yaml...").

4. **Progressive Discovery (Avoid Template-itis):**
   - Reduce initial visual complexity.
   - Hide advanced "Building" level tools (AI mapping, semantic search) until the user is deep in a "Room"
     (a specific spec/request).
   - Only show what is necessary for the current context.

## Feature-Specific Polish

1. **The Request Builder (The Door):**
   - Lighter than Postman. Focus on raw HTTP method and URL.
   - Minimize chrome and UI panels.

2. **Drift Sniffer (The Room):**
   - When a request drifts from the spec, highlight the specific line in the JSON body with a subtle
     **amber glow** (`--color-signal-warning-rgba-15`).
   - Avoid jarring error modals; use in-context visual indicators.

3. **AI Verification (The Building):**
   - AI-suggested requests/content must be wrapped in a **purple border** (`--color-signal-ai-rgba-35`).
   - This signifies "Draft" status until explicitly verified or accepted.

## Tech Stack

| Component | Technology                |
| --------- | ------------------------- |
| Runtime   | Tauri v2.9.x              |
| Backend   | Rust 1.80+                |
| Frontend  | React 19 + TypeScript 5.9 |
| Editor    | CodeMirror (Migrating)    |
| Styling   | Tailwind CSS 4.x          |
| Animation | Motion 12.x               |

## State Transparency (The Vigilance Monitor)

1. **Never Surface Errors Silently:** Always display Rust/Backend errors in the UI with correlation IDs.
2. **Visible Background States:** If a background process is running (AI verification, spec sync, request execution),
   it must be visible.
3. **The Vigilance Monitor:**
   - Use the `VigilanceMonitor` component for long-running or background tasks.
   - Provide clear, non-jargon labels (e.g., "Verifying response against spec..." instead of "Running DCF check").
   - The monitor should use the `vigilance-progress` animation for a calm, flowing feel.

## Implementation Checklist

1. **90% Grayscale (Ink)** - Most UI is monochrome deep ink.
2. **10% Signal (Zen-Signal)** - Color strictly for Amber/Green/Purple/Blue signals.
3. **Calm Motion** - Linear easing, 0.2s-0.4s.
4. **No Decoration** - Eliminate shadows and gradients that aren't functional.
5. **Contextual Depth** - Use surface shifts (`bg-surface` -> `bg-raised`) for hover/active states.
6. **Progressive Discovery** - Reveal advanced tools only when deep in a specific context.
