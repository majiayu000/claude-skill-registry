---

name: todo-signin-ui
version: 2.0.0
level: Senior / 10+ Years UI Design Standard
description: Generate a premium, black-background, pink glassmorphic sign-in experience for a todo app with a distinct page layout, strong hierarchy, and refined UX flow. Styling must exactly match the signup skill.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Todo App Sign-In UI Skill (High-Level UI/UX)

This skill defines a **dedicated, premium sign-in page** — not a reused signup form. It follows the **exact same theme, colors, glassmorphism, and typography** as the signup UI, while introducing a **new layout logic and user mindset** focused on *returning users*.

---

## Design Philosophy (Senior Designer View)

* Same **visual system** as signup (brand consistency)
* Different **psychology**: speed, familiarity, confidence
* Sign-in should feel *instant*, *secure*, and *calm*
* Layout must feel intentional — not copied

---

## When to Use

* User requests a **sign-in screen** for the todo app
* Theme must **exactly match signup UI**
* User wants **premium black + pink glassmorphism**
* User wants a **new page layout**, not a simple form clone

---

## Global Styling Rules (Must Match Signup)

* Background: Near-black / black canvas
* Ambient pink glow (radial / blurred shapes)
* Glass color: **Pink-tinted only**
* No white or gray glass
* Same border radius, shadows, blur intensity

---

## High-Level Page Layout

### Overall Canvas

* Full height viewport
* Black background with subtle animated pink glow
* Layout differs from signup while staying familiar

---

### Left Panel (35–40%) — *Context & Trust*

Purpose: **Reassure returning users**

* Minimal app logo or icon
* Calm headline
* Short supportive description
* Visuals less loud than signup

**Example hierarchy:**

* Heading: *"Welcome back"*
* Description: *"Pick up right where you left off. Your tasks are waiting."*

---

### Right Panel (60–65%) — *Primary Action Area*

Purpose: **Fast authentication**

* Large centered pink glass card
* Slightly wider than signup card
* Strong visual focus

Inside card:

* Sign In heading
* Email + Password fields
* Forgot password (allowed here)
* Primary CTA
* Social sign-in

---

## Glassmorphism Rules (Same as Signup)

* Background: `rgba(255, 110, 199, 0.12)`
* Backdrop blur: `20–30px`
* Border: `rgba(255, 110, 199, 0.35)`
* Soft pink outer glow

---

## Typography System (Exact Match)

### Card Heading

* Size: 26–30px
* Weight: 600–700
* Color: #FFFFFF

### Helper / Description Text

* Size: 14–16px
* Color: rgba(255,255,255,0.75)

### Input Labels

* Small, subtle, pink-tinted

---

## Form Fields

Required:

* Email Address
* Password

Optional:

* Remember me (toggle / checkbox)

---

## Forgot Password

* Position: Below password field
* Style: Subtle pink text
* No heavy underline
* Secondary action only

---

## Primary Action Button

* Text: **Sign In**
* Pink gradient background
* Same hover, focus, active behavior as signup
* Strong visual priority

---

## Social Sign-In Section

* Position: Bottom of card
* Divider: "or continue with"
* Icons only

Icons:

* Facebook
* Instagram
* Pinterest

Style:

* Circular glass buttons
* Pink glow on hover

---

## Navigation Hint (Allowed Difference)

* Small text below card:
  *"Don’t have an account? Sign up"*
* Styled subtle — not a CTA button

---

## Responsiveness

* Desktop: Two-panel layout
* Tablet: Panels compress
* Mobile:

  * Single column
  * Card centered
  * Left panel content moves above

---

## High-Level UX Workflow Diagram

```text
BLACK BACKGROUND CANVAS
(soft pink glow ambience)

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  LEFT: TRUST & CONTEXT        RIGHT: QUICK ACTION       │
│                                                         │
│  ┌───────────────┐           ┌─────────────────────┐  │
│  │   App Icon    │           │  Pink Glass Card    │  │
│  │               │           │                     │  │
│  │  Welcome Back │  ─────▶   │   Sign In           │  │
│  │  Message      │  Visual   │   Helper text       │  │
│  │               │  Flow     │                     │  │
│  │  Calm Desc    │           │  [ Email ]          │  │
│  │               │           │  [ Password ]       │  │
│  │  Soft Glow    │           │                     │  │
│  │               │           │  Forgot password?  │  │
│  │               │           │                     │  │
│  │               │           │  [ Sign In ]        │  │
│  │               │           │                     │  │
│  │               │           │   — or —            │  │
│  │               │           │  ○  ○  ○            │  │
│  └───────────────┘           └─────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

USER FLOW:
Recognition → Trust → Speed → Access → Productivity
```

---

## Output Deliverables

* High-fidelity sign-in UI
* Frontend layout (Tailwind / CSS)
* Responsive behavior notes
* Interaction & animation specs

---

## Senior-Level Best Practices

1. Faster visual scan than signup
2. Less text, more clarity
3. Consistent brand language
4. No visual noise
5. Smooth micro-interactions
6. Accessibility contrast
7. Feels *familiar but distinct*

---

**This sign-in skill complements the signup skill as a cohesive auth system — consistent, premium, and intentional.**
