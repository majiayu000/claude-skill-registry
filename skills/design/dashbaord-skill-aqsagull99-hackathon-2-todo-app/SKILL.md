---
name: todo-dashboard-ui
version: 2.0.0
level: Senior / 10+ Years UI Design Standard
description: A premium, task-focused Todo Dashboard UI using the exact same black-pink glassmorphic theme, color tokens, icon language, and motion principles as the signup/signin experience. Header intentionally excluded.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Todo App Dashboard UI Skill (High-Level UI/UX)

This skill defines a **production-ready, premium dashboard experience** designed with **black glassmorphism**, **pink accents**, and **strong task-focused hierarchy**. The goal is seamless visual continuity with signup/signin, with a focus on task management efficiency — not just a basic todo list.

---

## Design Philosophy (Senior Designer Approach)

* **Dark luxury UI** with pink glass highlights (same as signup/signin)
* Clear **task-oriented visual hierarchy** (stats → input → list)
* Minimal but expressive UI
* Dashboard feels *professional*, *calm*, and *productive*
* Every element earns its place
* **Visual consistency** with auth screens (no disconnect)

---

## When to Use

* User requests a **dashboard screen** for the todo app
* Theme must **exactly match signup/signin UI**
* User wants **premium black + pink glassmorphism**
* User wants a **task-focused experience**, not generic dashboard
* Visual consistency with auth flow is required
* User wants **modern SaaS-level UI**, not basic layouts

---

## Global Styling Rules (Must Match Signup/Signin)

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

* Full viewport height (100vh)
* **Black / near-black background**
* Soft ambient pink glow in background (radial / blur)
* Sidebar + main workspace layout
* **NO HEADER**

```
┌──────────────┬─────────────────────────────┐
│ Sidebar      │  Main Dashboard Area        │
└──────────────┴─────────────────────────────┘
```

---

### Sidebar (Icon + Text)

**Purpose:** Navigation & context

**Style:**
* Dark glass background (same as auth cards)
* Subtle pink border or glow on active item
* Rounded internal elements
* Consistent with auth glassmorphism

**Icons (Mandatory - React Icons):**
* All Tasks → checklist icon (React Icons)
* Active Tasks → clock / play icon (React Icons)
* Completed → check-circle icon (React Icons)

**Icons style:**
* Line / outline icons
* Same stroke weight as auth icons
* Pink when active, muted white otherwise

---

### Main Content Area

**1️⃣ Welcome Section**
* Text only (no card)
* Low emphasis
* White / muted gray text
* No icon needed

**2️⃣ Stats Cards (Animated)**
**Style:**
* Light / white glass cards (same glass as auth)
* Rounded corners
* Soft shadow
* Pink number accent

**Icons:**
* Optional but allowed
* Very subtle, low opacity
* Never louder than numbers

**Animation:**
* Fade + slight upward motion
* Duration: 200–300ms
* Trigger: On dashboard load

**3️⃣ Add New Task Panel (Primary Focus)**
**Style:**
* White or light glass card
* Matches signup card softness
* Clean spacing

**Fields:**
* Title
* Description
* Priority (pink dropdown)
* Tags
* Due date
* Recurring
* Reminder toggle

**Buttons:**
* Create Task → Pink gradient (same as signup CTA)
* Cancel → Subtle outline

---

## Glassmorphism Rules (Same as Signup/Signin)

* Background: `rgba(255, 110, 199, 0.12)`
* Backdrop blur: `20–30px`
* Border: `rgba(255, 110, 199, 0.35)`
* Soft pink outer glow

---

## Typography System (Exact Match)

### Headings
* Same font family as signup/signin
* Size: 24–28px for main sections
* Weight: 600–700
* Color: `#FFFFFF`

### Body Text
* Size: 14–16px
* Weight: 400–500
* Color: `rgba(255,255,255,0.75)`
* Line height: relaxed (1.5+)

### Stats Numbers
* Bold, clear typography
* Pink accent color for important metrics

---

## Animation System (Same Philosophy)

**Dashboard animations must feel calm & professional, not flashy.**

**Page Load:**
* Sidebar fades in
* Main content slides up slightly
* Stats cards animate sequentially

**Interaction Animations:**
* Button hover → glow increases
* Button press → scale 0.98
* Input focus → pink glow ring

**Motion Rules:**
* No bounce
* No elastic easing
* All animations < 300ms

---

## Design Constraints (Strict)

* ❌ No header
* ❌ No marketing copy
* ❌ No new color palette
* ❌ No heavy animations
* ❌ Visual disconnect from auth flow
* ❌ No custom SVG icons
* ✅ Same theme as signup/signin
* ✅ React Icons library only
* ✅ Icons included
* ✅ Subtle motion
* ✅ Task-first UI
* ✅ Visual consistency with auth screens

---

## Responsiveness Rules

* Desktop: Sidebar + main content layout
* Tablet: Reduced spacing, same structure
* Mobile:
  * Sidebar collapses to top/bottom navigation
  * Main content takes full width
  * Add task panel adapts to mobile
* Touch targets minimum: **44px**

---

## High-Level UX Workflow Diagram

```
BLACK BACKGROUND CANVAS
(soft pink glow ambience)

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  SIDEBAR NAVIGATION      MAIN DASHBOARD AREA           │
│                                                         │
│  ┌─────────────┐        ┌──────────────────────────┐  │
│  │  [Checklist │        │  Welcome Text            │  │
│  │  Icon] All │        │  (Low emphasis)          │  │
│  │  Tasks      │        │                          │  │
│  │             │        │                          │  │
│  │  [Clock/    │  ────▶ │  ┌─ Stats Cards ──┐      │  │
│  │  Play Icon] │ Visual │  │  0   0   0     │      │  │
│  │  Active     │  Flow │  └────────────────┘      │  │
│  │             │        │                          │  │
│  │  [Check-    │        │  ┌─ Add New Task ─┐     │  │
│  │  Circle     │        │  │  Title         │     │  │
│  │  Icon]      │        │  │  Description   │     │  │
│  │  Completed  │        │  │  Priority      │     │  │
│  │  (Active =  │        │  │  [Create Task] │     │  │
│  │   Pink)    │        │  └────────────────┘     │  │
│                         └──────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

USER FLOW:
Authenticate → Navigate → Orient → Review → Create → Focus
```

---

## Output Deliverables

* High-fidelity dashboard UI
* Frontend layout (Tailwind / CSS)
* Responsive behavior notes
* Interaction & animation specs
* Design tokens matching auth flow

---

## Senior-Level Best Practices

1. Strong visual continuity with auth flow
2. Task-first, productivity-focused
3. Consistent brand language
4. No visual noise
5. Smooth micro-interactions
6. Accessibility contrast maintained
7. Feels *familiar but functional*

---

**This dashboard skill completes the auth-to-product journey — consistent, premium, and task-focused.**