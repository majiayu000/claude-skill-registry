---
name: ui-ux-pro-max
description: >-
  Complete UI/UX design intelligence and implementation guidance for polished
  interfaces. Use when a user asks to improve UX, redesign an interface,
  create a design system, review UI patterns, improve user flows, design
  forms, build navigation, or make an interface more intuitive and polished.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: design
  tags: ["ui", "ux", "design-system", "user-experience", "interaction-design"]
  use-cases:
    - "Review and improve existing UI/UX with actionable recommendations"
    - "Design intuitive user flows for complex workflows"
    - "Create comprehensive design systems with reusable component patterns"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# UI/UX Pro Max

## Overview

Complete UI/UX design intelligence for building polished, intuitive interfaces. Covers interaction design, user flows, component patterns, design systems, accessibility, and micro-interactions. Provides both strategic design thinking and practical implementation guidance for production-quality interfaces.

## Instructions

When a user asks for UI/UX guidance or implementation, follow these steps:

### Step 1: Understand the design context

| Aspect | What to Identify |
|--------|-----------------|
| Users | Who are they? Technical? Non-technical? Frequency of use? |
| Task | What is the user trying to accomplish? |
| Context | Desktop, mobile, or both? Time-pressured or exploratory? |
| Complexity | How many steps? How much data? How many options? |
| Existing patterns | What conventions does the product already follow? |

### Step 2: Apply core UX principles

**Progressive disclosure:** Show only what is needed at each step. Hide complexity behind expandable sections, tooltips, or advanced settings.

**Feedback loops:** Every user action must produce visible feedback within 100ms. Clicks, submissions, errors, success — all need clear responses.

**Error prevention over error handling:** Disable invalid options, validate inline, use smart defaults. It is cheaper to prevent mistakes than to recover from them.

**Recognition over recall:** Users should see their options, not remember them. Use dropdowns instead of free text when options are known. Show recent items and suggestions.

**Consistency:** Same action, same pattern, everywhere. If clicking a row opens a detail panel on one page, it should do the same on every page.

### Step 3: Design the interaction patterns

**Navigation patterns:**
```
Top nav:        Best for < 7 primary sections, public sites
Sidebar nav:    Best for apps with deep hierarchy, frequent switching
Tab bar:        Best for mobile, 3-5 primary destinations
Breadcrumbs:    Best for deep hierarchies where users need to backtrack
Command palette: Best for power users, keyboard-driven apps
```

**Form patterns:**
```
Single column:  Best for most forms (faster completion)
Multi-column:   Only for related short fields (city/state/zip)
Stepped wizard: Best for 7+ fields or complex flows
Inline editing: Best for settings and profile pages
```

**Data display patterns:**
```
Table:          Best for comparing items with many attributes
Card grid:      Best for visual items or browsing
List:           Best for sequential or prioritized items
Detail panel:   Best for master-detail workflows
Dashboard:      Best for monitoring metrics at a glance
```

### Step 4: Implement with polish

**Loading states:**
- Skeleton screens over spinners (less jarring, feels faster)
- Show progress bars for operations over 3 seconds
- Optimistic UI for common actions (show success immediately, rollback on failure)

**Empty states:**
- Never show a blank screen. Explain what will appear here and how to get started
- Include an illustration or icon to soften the empty feeling
- Provide a primary action button ("Create your first project")

**Transitions and animation:**
```
Duration:   150-300ms for UI transitions (faster feels snappy)
Easing:     ease-out for entrances, ease-in for exits
Motion:     Fade + slight translate (8-16px) for appearing elements
Hover:      Scale 1.02-1.05 for cards, color shift for buttons
Focus:      Visible ring (2px offset) for keyboard navigation
```

**Micro-interactions that matter:**
- Button press: subtle scale down (0.97) on active
- Toggle switch: smooth slide with color transition
- Checkbox: checkmark draws in with a slight bounce
- Form submit: button shows loading state, then success checkmark
- Delete: item slides out, undo toast appears

### Step 5: Validate the design

- **5-second test:** Can a new user identify the page purpose in 5 seconds?
- **Squint test:** When you blur your eyes, does the visual hierarchy still work?
- **Tab test:** Can you navigate the entire flow with keyboard only?
- **Error test:** What happens when things go wrong? Empty data? Long text? Slow network?

## Examples

### Example 1: Improve a settings page UX

**User request:** "Our settings page is confusing, help me redesign it"

**Analysis and output:**
```markdown
## Current Issues
1. All settings on one long page — overwhelming
2. No grouping — unrelated settings mixed together
3. Save button only at the bottom — easy to miss
4. No indication of which settings were changed

## Recommended Design

### Structure
- Group settings into logical sections with a left sidebar:
  - General, Notifications, Security, Billing, Integrations
- Each section loads as its own panel on the right

### Interaction
- Auto-save with a subtle "Saved" toast (no save button needed)
- Or: floating save bar that appears only when changes are detected
- Show changed fields with a subtle highlight
- Add "Reset to default" per field, not per page

### Component Pattern
[Sidebar] → [Section Header + Description] → [Setting Group]

Each setting:
  Label (bold) + Description (gray, smaller)
  Input/Toggle/Select aligned to the right
  Divider between settings
```

### Example 2: Design a user onboarding flow

**User request:** "Design an onboarding flow for our project management app"

**Output:**
```markdown
## Onboarding Flow (4 steps)

### Step 1: Welcome + Name (10 sec)
- "Welcome to [App]! Let's get you set up."
- Single field: "What should we call you?"
- Skip button visible but de-emphasized
- Progress: ████░░░░ 1/4

### Step 2: Create First Project (20 sec)
- "Create your first project"
- Project name field (pre-filled with "My First Project")
- Template picker: 3 visual cards (Blank, Marketing, Engineering)
- Progress: █████░░░ 2/4

### Step 3: Invite Team (optional) (15 sec)
- "Work better together"
- Email input with "Add another" button
- "I'll do this later" link prominent
- Progress: ███████░ 3/4

### Step 4: Quick Tour (30 sec)
- 3-step spotlight tour of key features
- Highlight: sidebar nav, create button, notification bell
- "Got it" button on each, skip link visible
- Progress: ████████ Done!

### Design Principles Applied
- Each step has ONE primary action
- Never more than 2 fields per step
- Always show progress and allow skipping
- Pre-fill smart defaults to reduce effort
- Total time: under 90 seconds
```

### Example 3: Design system component audit

**User request:** "Help me create consistent button styles for our app"

**Output:**
```markdown
## Button System

### Hierarchy (use exactly these 4 variants)
| Variant | Use Case | Example |
|---------|----------|---------|
| Primary | Main CTA, 1 per screen | "Save", "Submit", "Create" |
| Secondary | Supporting actions | "Cancel", "Back", "Export" |
| Ghost | Tertiary actions | "Learn more", "View all" |
| Destructive | Irreversible actions | "Delete", "Remove" |

### Sizes
| Size | Height | Padding | Font | Use Case |
|------|--------|---------|------|----------|
| sm | 32px | 12px 16px | 13px | Tables, dense UI |
| md | 40px | 12px 20px | 14px | Default, forms |
| lg | 48px | 14px 24px | 16px | Hero CTAs, landing |

### States (every button needs all of these)
- Default → Hover (darken 10%) → Active (darken 15%, scale 0.98)
- Focus (visible ring, 2px offset)
- Disabled (50% opacity, no pointer events)
- Loading (spinner replaces text, same width to prevent layout shift)

### Rules
- Max 1 primary button per visible area
- Destructive buttons require a confirmation step
- Icon-only buttons need a tooltip and aria-label
- Button text: verb + noun ("Create project" not just "Create")
```

## Guidelines

- Design for the 80% case. Optimize the common path. Edge cases go behind menus and advanced options.
- Every screen should have one obvious next action. If users hesitate, the design has failed.
- White space is not wasted space. Cramming more elements in does not make the interface more useful.
- Copy is part of UX. "Something went wrong" is bad. "We couldn't save your changes. Check your connection and try again." is good.
- Test with real data. A card that looks great with 3 words breaks with 30. Design for the worst case.
- Performance is UX. A beautiful interface that takes 4 seconds to respond feels broken.
- Accessibility is UX for everyone. Keyboard navigation, screen readers, color contrast, and motion preferences all matter.
- When in doubt, look at what works. Study interfaces people already use and love. Do not reinvent patterns without good reason.
