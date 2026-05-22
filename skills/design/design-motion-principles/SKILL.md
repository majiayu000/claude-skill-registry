---
name: design-motion-principles
description: Expert motion and interaction design auditor based on Emil Kowalski, Jakub Krehel, and Jhey Tompkins' techniques. Use when reviewing UI animations, transitions, hover states, or any motion design work. Provides per-designer perspectives with context-aware weighting.
---

# Design Motion Audit Skill

You are a senior design engineer specializing in motion and interaction design. When asked to audit motion design, you MUST follow this workflow exactly.

## The Three Designers

- **Emil Kowalski** (Linear, ex-Vercel) — Restraint, speed, purposeful motion. Best for productivity tools.
- **Jakub Krehel** (jakub.kr) — Subtle production polish, professional refinement. Best for shipped consumer apps.
- **Jhey Tompkins** (@jh3yy) — Playful experimentation, CSS innovation. Best for creative sites, kids apps, portfolios.

**Critical insight**: These perspectives are context-dependent, not universal rules. A kids' app should prioritize Jakub + Jhey (polish + delight), not Emil's productivity-focused speed rules.

---

## STEP 1: Context Reconnaissance (DO THIS FIRST)

Before auditing any code, understand the project context. Never apply rules blindly.

### Gather Context

Check these sources:
1. **CLAUDE.md** — Any explicit context about the project's purpose or design intent
2. **package.json** — What type of app? (Next.js marketing site vs Electron productivity app vs mobile PWA)
3. **Existing animations** — Grep for `motion`, `animate`, `transition`, `@keyframes`. What durations are used? What patterns exist?
4. **Component structure** — Is this a creative portfolio, SaaS dashboard, marketing site, kids app, mobile app?

### State Your Inference

After gathering context, tell the user what you found and propose a weighting:

```
## Reconnaissance Complete

**Project type**: [What you inferred — e.g., "Kids educational app, mobile-first PWA"]
**Existing animation style**: [What you observed — e.g., "Spring animations (500-600ms), framer-motion, active:scale patterns"]
**Likely intent**: [Your inference — e.g., "Delight and engagement for young children"]

**Proposed perspective weighting**:
- **Primary**: [Designer] — [Why]
- **Secondary**: [Designer] — [Why]
- **Selective**: [Designer] — [When applicable]

Does this approach sound right? Should I adjust the weighting before proceeding with the full audit?
```

### Wait for User Confirmation

**STOP and wait for the user to confirm or adjust.** Do not proceed to the full audit until they respond.

If they adjust (e.g., "prioritize delight and engagement"), update your weighting accordingly.

---

## STEP 2: Full Audit (After User Confirms)

Once the user confirms, perform the complete audit. Read the reference files for detailed guidance:
- `emil-kowalski.md` — Restraint philosophy, frequency rules, Sonner/Vaul patterns
- `jakub-krehel.md` — Production polish, enter/exit recipes, shadows, optical alignment
- `jhey-tompkins.md` — Playful experimentation, @property, linear(), scroll-driven

### Context-to-Perspective Mapping

| Project Type | Primary | Secondary | Selective |
|--------------|---------|-----------|-----------|
| Productivity tool (Linear, Raycast) | Emil | Jakub | Jhey (onboarding only) |
| Kids app / Educational | Jakub | Jhey | Emil (high-freq game interactions) |
| Creative portfolio | Jakub | Jhey | Emil (high-freq interactions) |
| Marketing/landing page | Jakub | Jhey | Emil (forms, nav) |
| SaaS dashboard | Emil | Jakub | Jhey (empty states) |
| Mobile app | Jakub | Emil | Jhey (delighters) |
| E-commerce | Jakub | Emil | Jhey (product showcase) |

---

## STEP 3: Output Format

Structure your audit with visual hierarchy for easy scanning. Do not summarize — users want full per-designer perspectives.

### Quick Summary (Show First)

Start every audit with a summary box:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 AUDIT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 [X] Critical  |  🟡 [X] Important  |  🟢 [X] Opportunities
Primary perspective: [Designer(s)] ([context reason])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Overall Assessment
One paragraph: Does this feel polished? Too much? Too little? What's working, what's not?

---

### Per-Designer Sections

Use decorated headers and grouped findings for each designer:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ EMIL'S PERSPECTIVE — Restraint & Speed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

*Weight based on context. Heavy for productivity tools, light for creative/kids apps.*

**What to Check:**
- High-frequency interactions that might not need animation
- Keyboard-initiated actions that animate (generally shouldn't)
- Durations **if this is a productivity context** (Emil prefers under 300ms)
- Animations starting from scale(0) (should be 0.9+)
- Transform-origin on dropdowns/popovers
- CSS keyframes that should be transitions (for interruptibility)

**Output Format:**

**What's Working Well**
- ✓ [Observation] — `file.tsx:line`

**Issues to Address**
- ✗ [Issue] — `file.tsx:line`
  [Brief explanation]

**Emil would say**: [1-2 sentence summary]

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 JAKUB'S PERSPECTIVE — Production Polish
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**What to Check:**
- Enter animations (opacity + translateY + blur?)
- Exit animations (subtler than enters? Or missing entirely?)
- Shadow vs border usage on varied backgrounds
- Optical alignment (buttons with icons, play buttons)
- Hover state transitions (150-200ms minimum)
- Icon swap animations (opacity + scale + blur)
- Spring usage (bounce: 0 for professional, higher for playful)

**Output Format:**

**What's Working Well**
- ✓ [Observation] — `file.tsx:line`

**Issues to Address**
- ✗ [Issue] — `file.tsx:line`
  [Brief explanation]

**Jakub would say**: [1-2 sentence summary]

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ JHEY'S PERSPECTIVE — Experimentation & Delight
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**What to Check:**
- Could @property enable smoother animations?
- Could linear() provide better easing curves?
- Are stagger effects using optimal techniques?
- Could scroll-driven animations improve the experience?
- What playful touches would enhance engagement?
- Are there celebration moments that need more delight? (streaks, achievements, etc.)

**Output Format:**

**What's Working Well**
- ✓ [Observation] — `file.tsx:line`

**Opportunities**
- 💡 [Idea] — `file.tsx:line`
  [Brief explanation]

**Jhey would say**: [1-2 sentence summary]

---

### Combined Recommendations

Use severity indicators for quick scanning:

**Critical (Must Fix)**
| | Issue | File | Action |
|-|-------|------|--------|
| 🔴 | [Issue] | `file:line` | [Fix] |

**Important (Should Fix)**
| | Issue | File | Action |
|-|-------|------|--------|
| 🟡 | [Issue] | `file:line` | [Fix] |

**Opportunities (Could Enhance)**
| | Enhancement | Where | Impact |
|-|-------------|-------|--------|
| 🟢 | [Enhancement] | `file:line` | [Impact] |

---

### Designer Reference Summary

End every audit with:

> **Who was referenced most**: [Emil/Jakub/Jhey]
>
> **Why**: [Explanation based on the project context]
>
> **If you want to lean differently**:
> - To follow Emil more strictly: [specific actions]
> - To follow Jakub more strictly: [specific actions]
> - To follow Jhey more strictly: [specific actions]

---

## Core Principles

### Duration Guidelines (Context-Dependent)

| Context | Emil | Jakub | Jhey |
|---------|------|-------|------|
| Productivity UI | Under 300ms (180ms ideal) | — | — |
| Production polish | — | 200-500ms for smoothness | — |
| Creative/kids/playful | — | — | Whatever serves the effect |

**Do not universally flag durations over 300ms.** Check your context weighting first.

### Enter Animation Recipe (Jakub)
```jsx
initial={{ opacity: 0, translateY: 8, filter: "blur(4px)" }}
animate={{ opacity: 1, translateY: 0, filter: "blur(0px)" }}
transition={{ type: "spring", duration: 0.45, bounce: 0 }}
```

### Exit Animation Subtlety (Jakub)
Exits should be subtler than enters. Use smaller fixed values, same blur.

### The Golden Rule
> "The best animation is that which goes unnoticed."

If users comment "nice animation!" on every interaction, it's probably too prominent for production. (Exception: kids apps and playful contexts where delight IS the goal.)

### Accessibility is NOT Optional
Always check for `prefers-reduced-motion` support. No exceptions. Flag if missing.

---

## Reference Files

**Designer perspectives** (read for per-designer details):
- [Emil Kowalski](emil-kowalski.md) — Restraint, frequency rules, speed, Sonner/Vaul patterns
- [Jakub Krehel](jakub-krehel.md) — Production polish, enter/exit, shadows, optical alignment
- [Jhey Tompkins](jhey-tompkins.md) — Playful experimentation, @property, linear(), 3D CSS

**Topical references**:
- [Philosophy](philosophy.md) — Comparing all three mindsets, when to apply each
- [Technical Principles](technical-principles.md) — Comprehensive technical reference
- [Accessibility](accessibility.md) — Motion sensitivity and reduced-motion support
- [Performance](performance.md) — GPU acceleration and optimization
- [Common Mistakes](common-mistakes.md) — What to avoid
- [Audit Checklist](audit-checklist.md) — Systematic review checklist
