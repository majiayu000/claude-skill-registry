---
name: todo-homepage-ui
version: 2.0.0
level: Senior / 10+ Years UI Design Standard
description: A premium, minimal, animated Todo App homepage with a strong hero message, refined typography, floating icons, and a single focused CTA — visually aligned with black-pink glassmorphism used across auth and dashboard.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Todo App Homepage UI Skill (High-Level UI/UX)

This skill defines a **premium, focused landing page** designed with **black glassmorphism**, **pink accents**, and **calm, confident messaging**. The goal is to create immediate clarity and confidence — not marketing noise. The homepage must feel calm, focused, and premium while maintaining visual consistency with the auth and dashboard screens.

---

## Design Philosophy (Senior Designer Approach)

* **Calm, confident messaging** with pink glass highlights (same as auth/dashboard)
* **Single purpose**: Focus user's attention on the core value proposition
* **Premium feel** without marketing noise
* **Immediate clarity** in under 5 seconds
* **Visual consistency** with the broader app ecosystem
* **Motion supports message**, not distracts

---

## When to Use

* User requests a **homepage/landing page** for the todo app
* Theme must **exactly match signup/signin/dashboard UI**
* User wants **premium black + pink glassmorphism**
* User wants a **conversion-focused page**, not marketing clutter
* Need a **single CTA** focused landing experience
* User wants **modern SaaS-grade UI**, not basic layouts

---

## Global Styling Rules (Must Match Auth/Dashboard)

* Background: Near-black / black canvas
* Ambient pink glow (radial / blurred shapes)
* Glass color: **Pink-tinted only**
* No white or gray glass
* Same border radius, shadows, blur intensity
* Same typography system
* Same animation philosophy

---

## High-Level Layout Structure

### Overall Canvas

* Full viewport: 100vh × 100vw
* **Centered layout** (both axes)
* No scroll on initial view
* **Black / near-black background**
* Subtle pink ambient glow
* Single centered column layout

```
┌──────────────────────────────────────────────┐
│                                              │
│        One Task at a Time                    │
│                                              │
│  A focused Todo app designed to help you     │
│  move forward without distractions.          │
│                                              │
│           [ Get Started ]                    │
│                                              │
│   (Floating pink glass icons drifting)       │
│                                              │
└──────────────────────────────────────────────┘
```

---

### Hero Section (Primary Focus)

**Purpose:** Immediate clarity in <5 seconds

**Layout:**
* Single centered column
* Vertical rhythm: Title → Description → CTA

**Headline (Locked):**
* Main Title (Required): "One Task at a Time"
* Rules:
  - Large
  - Bold
  - Calm
  - Confident
* This text is the visual anchor of the entire page.

**Description Text:**
* 1–2 lines only
* Explains value without buzzwords
* Example: "A focused Todo app designed to help you move forward without distractions."
* Style:
  - Soft white
  - High readability
  - Relaxed line height

---

### Typography System (Premium)

**Font Style:**
* Use same family as signup/dashboard:
  - Inter / Poppins / Satoshi / SF Pro

**Hierarchy:**
* Headline: 48–64px (desktop)
* Description: 16–18px
* Button text: 14–16px, medium weight
* No font mixing.

---

### Get Started Button (Single CTA)

**Position:** Centered below description

**Style:**
* Rounded (pill or 14–16px radius)
* Pink gradient background
* Soft glow
* Clean label: Get Started

**Interaction:**
* Hover → glow intensifies
* Active → scale 0.97
* Focus → subtle pink ring

---

### Icons & Floating Elements (Depth & Mood)

**Purpose:** Visual interest without distraction

**Style:**
* 3D-like or soft glass icons
* Cards / task icons / check marks
* Pink-tinted glass
* Soft blur + shadow

**Placement:**
* Around hero text
* Never overlapping text
* Asymmetric but balanced

**Motion:**
* Slow floating / drift
* Slight parallax
* Continuous but subtle

---

## Glassmorphism Rules (Same as Auth/Dashboard)

* Background: `rgba(255, 110, 199, 0.12)`
* Backdrop blur: `20–30px`
* Border: `rgba(255, 110, 199, 0.35)`
* Soft pink outer glow
* Very light application
* Only pink-tinted glass
* No noisy borders
* Glass should feel soft and expensive, not flashy

---

## Animation System (Page Load & Text)

**Animation must trigger every time homepage enters viewport**

**Animation Sequence:**
1️⃣ **Headline**
* Opacity: 0 → 1
* Y: +20px → 0
* Duration: 500–600ms
* Ease: ease-out

2️⃣ **Description**
* Delay: 80–120ms
* Same fade + move

3️⃣ **Get Started Button**
* Scale: 0.96 → 1
* Soft glow pulse (once)

**Re-Entry Rule:**
* Animation replays on revisit
* No stacking
* No jitter

**Motion Discipline (Senior Rule):**
* No bounce
* No elastic easing
* Total sequence < 1.2s
* Respect reduced-motion preference

---

## Design Constraints (Strict)

* ❌ No header
* ❌ No footer
* ❌ No sidebar
* ❌ No extra CTAs
* ❌ No marketing sections
* ❌ No white/gray glass panels
* ❌ No marketing noise
* ✅ One message
* ✅ One button
* ✅ One emotion: focus
* ✅ Same theme as auth/dashboard
* ✅ Visual consistency across app
* ✅ Calm, not salesy
* ✅ Premium feel (not flashy)

---

## Responsiveness Rules

* Desktop: Centered layout with proper spacing
* Tablet: Reduced font sizes, same structure
* Mobile:
  * Single column
  * Text sizes adjusted for readability
  * Button touch targets: minimum 44px
  * Floating elements adapt to smaller screens

---

## High-Level UX Workflow Diagram

```
USER OPENS APP
        ↓
HOMEPAGE ENTERS VIEWPORT
        ↓
TEXT ANIMATION PLAYS
        ↓
ATTENTION → MESSAGE → CTA

┌──────────────────────────────────────────────┐
│                                              │
│        One Task at a Time                    │
│                                              │
│  A focused Todo app designed to help you     │
│  move forward without distractions.          │
│                                              │
│           [ Get Started ]                    │
│                                              │
│   (Floating pink glass icons drifting)       │
│                                              │
└──────────────────────────────────────────────┘

FLOW:
Calm → Clarity → Motivation → Action
```

---

## Output Deliverables

* High-fidelity homepage UI
* Frontend layout (Tailwind / CSS)
* Animation specs (Framer Motion)
* Responsive behavior notes
* Interaction & animation specs
* Design tokens matching auth/dashboard flow

---

## Senior-Level Best Practices

1. Less content, more clarity
2. Motion supports message, not distracts
3. CTA visible within 3 seconds
4. Visual consistency across app
5. Homepage feels calm, not salesy
6. Premium ≠ flashy
7. Focus is the brand
8. Accessibility contrast maintained

---

**This homepage skill creates a focused, premium landing experience — calm, clear, and conversion-focused.**