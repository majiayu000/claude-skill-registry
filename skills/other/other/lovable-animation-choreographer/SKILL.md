---
name: lovable-animation-choreographer
description: "Add sophisticated, choreographed animations and micro-interactions to Lovable UIs with precise timing, sequencing, and scroll-based triggers using Framer Motion and CSS."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🎬"}}
---

# Lovable Animation Choreographer

## Purpose

Add layered, intentional animation choreography to Lovable-generated UIs. This skill defines precise entrance sequences, scroll behaviors, hover interactions, and state transitions with specific timing curves, durations, and stagger values. Use as a refinement pass after a base UI exists, or alongside any generation skill to build in motion from the start.

> **Platform context**: Lovable generates React + TypeScript + Tailwind CSS + shadcn/ui apps on Vite. Animations should use Framer Motion (already available in Lovable projects) or pure CSS transitions. Never introduce animation libraries not supported by Lovable.

## Inputs

| Parameter   | Required | Values                                          | Default |
|-------------|----------|--------------------------------------------------|---------|
| `intensity` | yes      | subtle, moderate, expressive                     | —       |
| `style`     | yes      | smooth, bouncy, snappy, cinematic                | —       |
| `trigger`   | no       | on-load, on-scroll, on-hover, mixed              | mixed   |
| `target`    | no       | hero, navigation, content, cards, cta, footer, all | all   |

## Workflow

### 1. Resolve Timing System

Based on `style`, set base timing variables to use throughout:

| Style     | Easing                                | Duration | Stagger |
|-----------|---------------------------------------|----------|---------|
| smooth    | `cubic-bezier(0.4, 0, 0.2, 1)`       | 500ms    | 80ms    |
| bouncy    | `cubic-bezier(0.34, 1.56, 0.64, 1)`  | 600ms    | 100ms   |
| snappy    | `cubic-bezier(0.25, 0.1, 0.25, 1)`   | 250ms    | 50ms    |
| cinematic | `cubic-bezier(0.16, 1, 0.3, 1)`      | 800ms    | 120ms   |

### 2. Resolve Transform Intensity

Based on `intensity`, set transform magnitudes:

| Intensity  | Translate | Scale Start | Hover Lift | Shadow   | Rotation   |
|------------|-----------|-------------|------------|----------|------------|
| subtle     | 15px      | 0.98        | 2px        | minimal  | none       |
| moderate   | 25px      | 0.96        | 4px        | medium   | none       |
| expressive | 40px      | 0.93        | 6px        | strong   | ±2° entry  |

### 3. Choreograph Section Entrances

For each section, define the animation sequence using Framer Motion `motion` components or CSS `@keyframes`:

**Hero Section** (highest priority):
- Title: Fade up from `translateY(distance)`. Duration: base × 1.2. Delay: 0ms.
- Subtitle: Same fade-up. Delay: stagger × 2.
- CTA buttons: Fade in + scale from `scale_start`. Delay: stagger × 4.
- Hero image: Fade in from right or scale from center. Delay: stagger × 3. Duration: base × 1.5.
- Background decorations: Float in from edges. Delay: stagger × 6. Duration: base × 2.

**Navigation**:
- Entire nav fades in as single unit. Duration: 200ms. Delay: 0ms.
- On scroll past hero: Add `backdrop-filter: blur(10px)` + bottom border + shadow. Transition: 300ms.

**Content Sections** (below fold):
- Trigger when 20% visible (Intersection Observer threshold 0.2, or Framer Motion `whileInView`).
- Section heading fades up from `translateY(distance ÷ 2)`. Duration: base.
- Body elements stagger after heading.

**Card Grids**:
- Stagger row-by-row, left to right within row.
- Each card: Fade up + scale from `scale_start`. Duration: base. Stagger: interval between cards.
- Cap at 12 animated cards. Remaining appear instantly.

**CTA Sections**:
- Background fades/scales in first. Duration: base × 1.5.
- Text fades up. Delay: stagger × 2.
- CTA button: Fade in + scale. Delay: stagger × 4.
- If `intensity` is expressive: subtle continuous glow pulse (2s infinite, opacity 0.8–1.0) after entrance.

**Footer**:
- Simple fade-in as single unit when scrolled into view. Duration: 400ms.

### 4. Define Hover Interactions

Apply hover to cards, buttons, nav links, image thumbnails, and clickable containers:

| Intensity  | Transform                                | Shadow                                       | Duration |
|------------|------------------------------------------|----------------------------------------------|----------|
| subtle     | `translateY(-2px)`                       | +4px blur, +2px spread                       | 200ms    |
| moderate   | `translateY(-4px)`                       | substantial increase, `brightness(1.02)`     | 250ms    |
| expressive | `translateY(-6px) scale(1.02)`           | colored shadow (accent at 0.15 opacity)      | 300ms    |

### 5. Define Scroll Behaviors

- **Parallax** (moderate/expressive only): Backgrounds at 0.5× speed, decorative elements at 0.3×.
- **Scroll progress**: 2px bar at top, brand primary color, fills left-to-right based on scroll position.
- **Section reveal**: Use `whileInView` (Framer Motion) or Intersection Observer at 0.2 threshold.
- **Nav indicators**: If page has anchor sections, dot indicators on right edge highlight current section.

### 6. Define State Transitions

- **Tab/toggle**: Active indicator slides to new position (250ms ease-out). Content crossfades (150ms out, 200ms in).
- **Accordion**: Height animates with `AnimatePresence` + `motion.div`. Content fades in 100ms after height completes.
- **Modal/dialog**: Backdrop fades in (200ms). Modal scales from 0.95 + fades in (300ms). Close reverses at 0.7× duration.
- **Toast**: Slides in from top-right (300ms ease-out). Auto-dismiss slides out after 5s. Progress bar shrinks over 5s.
- **Page transitions**: Use `AnimatePresence` with `mode="wait"`. Fade out (150ms) → fade in (300ms) with subtle `translateY(-10px)`.

## Output Format

A complete animation specification formatted as Lovable prompt instructions. Includes Framer Motion component patterns, CSS transition properties, Intersection Observer configuration, and interaction states for every targeted section. Ready to paste into a Lovable chat prompt.

## Guardrails

- Never animate more than 3 CSS properties simultaneously per element. Prefer `transform` + `opacity` for GPU acceleration.
- Never animate `width`, `height`, `top`, `left`, `margin`, or `padding` directly. Use `transform: translate/scale` instead.
- All animations MUST respect `prefers-reduced-motion: reduce`. When reduced motion is active, resolve instantly (duration: 0ms) or use opacity only.
- Hero entrance must complete within 1500ms of page load.
- Hover animations must not exceed 300ms.
- No infinite animations except: loading indicators, ambient decorative floats, and CTA attention pulses (expressive only). All must be subtle.
- Maximum stagger count: 12 elements. Beyond 12, remaining appear instantly.
- Scroll-triggered animations fire once only (no re-trigger on scroll-up) unless user explicitly requests otherwise.
- Use Framer Motion `motion` components or CSS `@keyframes` — do not introduce GSAP, Anime.js, or other external animation libraries.

## Failure Handling

| Problem | Follow-up Prompt |
|---------|-----------------|
| All elements appear simultaneously | "Stagger entrance animations. Title first (delay 0ms), subtitle follows (delay {stagger×2}ms), CTA last (delay {stagger×4}ms). Use {style_easing}. Cards stagger row-by-row at {stagger}ms intervals." |
| Janky animations / layout shift | "Change all animated properties to transform and opacity only. Remove width/height/margin animations. Add will-change: transform, opacity. Ensure animated elements have explicit dimensions." |
| Too aggressive / distracting | "Reduce intensity: translate 15px, scale 0.98, hover lift 2px. Shorten durations by 40%. Remove parallax and continuous pulse." |
| No reduced-motion support | "Wrap animations in @media (prefers-reduced-motion: no-preference). Add fallback setting all transition-duration and animation-duration to 0.01ms." |
| Framer Motion not working | "Import { motion, AnimatePresence } from 'framer-motion'. Ensure framer-motion is in package.json dependencies. Use motion.div with initial, animate, and transition props." |

## Examples

### Example 1: Subtle Smooth Landing Page

**Input**: `intensity=subtle`, `style=smooth`, `trigger=mixed`, `target=all`

**Prompt to Lovable**:
```
Add subtle, smooth animations to the entire page:

Hero section: Title fades up from 15px below over 600ms with ease-out (cubic-bezier(0.4,0,0.2,1)), delay 0ms. Subtitle fades up with 160ms delay. CTA button fades in and scales from 0.98 with 320ms delay. Hero image fades in from right with 240ms delay over 750ms.

Navigation: Fades in over 200ms on load. On scroll past hero, add backdrop-filter blur(10px) and subtle bottom border with 300ms transition.

Below-fold sections: Each section animates when 20% visible. Heading fades up from 8px. Body elements stagger at 80ms intervals after heading.

Cards: Stagger row-by-row at 80ms per card. Each fades up from 15px and scales from 0.98. Max 12 cards animated.

Hover on cards and buttons: translateY(-2px) with slight shadow increase, 200ms ease-out.

Add prefers-reduced-motion support — disable all animations when reduced motion is preferred.
```

### Example 2: Expressive Cinematic Product Page

**Input**: `intensity=expressive`, `style=cinematic`, `trigger=on-scroll`, `target=hero,cards,cta`

**Prompt to Lovable**:
```
Add expressive cinematic animations to hero, cards, and CTA sections:

Hero: Title fades up from 40px below over 960ms with cinematic easing (cubic-bezier(0.16,1,0.3,1)), slight 2° rotation settling to 0°. Subtitle follows at 240ms delay. Hero image scales from 0.93 to 1 over 1200ms with 360ms delay. Background decorations float in from edges over 1600ms.

Cards: Trigger when 20% visible (use Framer Motion whileInView). Each card fades up from 40px, scales from 0.93, with optional ±2° rotation. Stagger at 120ms. Cap at 12 animated cards.

CTA section: Background scales in first (1200ms). Text fades up at 240ms delay. CTA button fades and scales in at 480ms delay. After entrance, add subtle glow pulse (2s infinite, opacity 0.8-1.0).

Hover: translateY(-6px) scale(1.02) with colored accent shadow at 0.15 opacity, 300ms ease-out.

Wrap all animations in prefers-reduced-motion: no-preference media query.
```

## Security & Privacy

This skill generates text prompts only. It does not access external endpoints, transmit data, or execute code. All output is prompt text intended for the Lovable.dev platform.

## Trust Statement

This skill contains no executable scripts. It produces Lovable-compatible prompt instructions that guide UI animation generation. It does not access the filesystem, network, or any external service.
