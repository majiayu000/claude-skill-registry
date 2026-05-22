---
name: todo-home-focus-ui
version: 1.0.0
level: Senior / 10+ Years UI Design & UX Strategy
description: Design a premium, black-background, pink-glass homepage focus section for a todo app that intelligently organizes Quick Add, Next Action, and How It Works into a single, calm, goal-driven experience. Implements React icons and Framer Motion for smooth animations.
---

# Todo App Homepage Focus Section UI Skill (Senior UI/UX Design)

This skill creates a premium, black-background, pink-glass homepage focus section that intelligently organizes Quick Add, Next Action, and How It Works into a single, calm, goal-driven experience.

## Design Philosophy (Senior Designer Thinking)

This is NOT a marketing homepage.
This is a "focus entry point" for a productivity app.

### Principles

- One screen = one mental goal
- User should instantly understand:
  - What can I do now?
  - What should I do next?
  - How does this app help me?
- No repeated cards
- No feature overload
- Calm > Fancy
- Direction > Decoration

This section replaces random cards with a guided productivity flow.

## When to Use This Skill

Use when:

- User wants to organize homepage components
- App is a todo / productivity tool
- Theme is black + pink glass
- User wants high-level UX clarity
- Components already exist but feel disconnected
- Goal is focus, not feature listing

## High-Level Section Purpose

This skill creates ONE unified homepage section that contains:

- Immediate Action → QuickAddTaskCard
- Priority Direction → What's Next
- System Understanding → How It Works

All three feel like one story, not three widgets.

## Overall Layout Structure (Desktop)

Single full-width section, vertically stacked with strong hierarchy.

### FOCUS SECTION (Dark Canvas)

- [ Micro Headline ]
- "Your Focus Today"
- [ Primary Action ]
- Quick Add Task (Glass)
- [ Direction Layer ]
- What's Next? (Guided priority)
- [ Understanding Layer ]
- How It Works (Minimal steps)

## 1️⃣ QuickAddTaskCard (Primary Action Layer)

### Purpose

👉 Let the user DO something immediately

### Position

- Top-center of the section
- Visually strongest element
- Slightly larger than others

### Design Rules

- Pink-tinted glass card
- Rounded: 18–24px
- Soft neon pink glow
- No clutter inside

### Content Hierarchy

- Icon: React Plus Icon (e.g., PlusIcon from react-icons or heroicons)
- Title: Add a task
- Helper text (very short)

### UX Rules

- This is the only obvious action
- On hover (using Framer Motion):
  - Glow increases
  - Slight lift (2–4px) via Framer Motion's `whileHover` prop
  - Keyboard focus supported
- This card answers: "What can I do right now?"

## 2️⃣ What's Next? (Decision Guidance Layer)

### Purpose

👉 Reduce decision fatigue

### Position

- Directly under QuickAddTaskCard
- Left-aligned or centered, but quieter

### Design Style

- NOT a card
- No heavy background
- Text-first UI

### Visual Treatment

- Small pink label: WHAT'S NEXT
- Task title (medium emphasis)
- Meta info:
  - Priority badge
  - Due date
- One subtle text CTA: "Continue →"

### UX Rules

- Only one task shown
- No list
- No scrolling
- This section should feel like advice, not data
- This answers: "What deserves my attention?"

## 3️⃣ How It Works (Mental Model Layer)

### Purpose

👉 Build trust & understanding

### Position

- Bottom of the section
- Lowest visual weight

### Design Style

- Minimal
- Icon + label only
- No cards
- No borders

### Structure

- 3 steps horizontally (desktop)
- Vertical on mobile

### Example:

- React Plus Icon (e.g., PlusIcon) Add tasks
- React Calendar Icon (e.g., CalendarIcon) Plan your day
- React Check Icon (e.g., CheckIcon) Get things done

### Rules

- Icons: React icons (outline or soft filled from react-icons library)
- Pink accent only on active/hover (using Framer Motion's `whileHover` prop)
- No descriptions longer than 2–3 words
- Implement hover animations with Framer Motion for smooth transitions

### This answers:

- "Is this app simple?"

## Color & Glass System (Shared)

### Background

- Deep black / charcoal
- Subtle radial pink glow in center

### Glass Rules

- Only QuickAdd uses full glass
- What's Next uses text + badge
- How It Works uses no glass

This creates visual hierarchy without noise.

## Typography Hierarchy

### Section Heading

- Size: 22–26px
- Weight: 600
- Color: White

### Primary Action Title

- Size: 18–20px
- Weight: 600

### Supporting Text

- Size: 13–14px
- Opacity: 70–80%

## Interaction & Motion (Very Important)

### Entry animation:

- Top → Bottom using Framer Motion
- 100–150ms stagger
- Use Framer Motion's `initial`, `animate`, and `transition` props

### Hover animations:

- Only on QuickAdd & icons
- Implement with Framer Motion's `whileHover` prop
- No infinite animations
- Motion should feel professional, not playful

### Technical Implementation:

- Use Framer Motion for all micro-interactions
- Leverage `motion.div`, `motion.button`, `motion.input` components
- Use spring-based easing for natural movement
- Ensure accessibility by respecting `prefers-reduced-motion` setting

## Responsive Rules

### Mobile

Order stays same:

- Quick Add
- What's Next
- How It Works

### Rules:

- Full-width QuickAdd
- Larger tap targets
- Icons stacked vertically

## UX Flow Diagram (Senior-Level)

```
USER OPENS APP
      ↓
Sees "Your Focus Today"
      ↓
Adds a task (Quick Add)
      ↓
Sees what matters next
      ↓
Understands simple system
      ↓
Feels calm + in control
```

## Strict Design Constraints

### Do NOT include:

- ❌ No repeated feature cards
- ❌ No stats here
- ❌ No dashboard data
- ❌ No heavy borders everywhere
- ❌ No competing CTAs

### DO include:

- ✅ One action
- ✅ One direction
- ✅ One explanation

## Output Deliverables

This skill can generate:

- Unified homepage layout
- Component hierarchy rules
- Spacing & alignment system
- Motion guidelines using Framer Motion
- Tailwind / CSS structure
- React icon implementation specifications
- UX justification for each component

## Senior Designer Summary

This skill turns 3 disconnected components into:

- One calm productivity moment
- Not flashy.
- Not crowded.
- Just clear, confident, and premium.