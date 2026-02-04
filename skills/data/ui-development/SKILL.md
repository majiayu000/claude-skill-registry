<!--
  This skill integrates patterns from:
  - Original source: https://github.com/Dammyjay93/interface-design
  - Author: Dammyjay93
  - License: MIT
  - Integrated into claude-code-quickstart SDK by Sandhya Simhan
-->

---
name: ui-development
description: Build premium, crafted interfaces with audience alignment and design system memory. Automatically invoked by workflows for UI/frontend work.
---

# UI Development & Premium Aesthetics

## Scope

**Use for:** All web interfaces, dashboards, apps, tools, admin panels, landing pages, marketing sites.

**Not for:** Backend services, APIs, data processing.

## When This Skill Triggers

This skill is automatically invoked by workflows when:
- `/brainstorm` detects UI/frontend work
- `/design` creates implementation plans for UI features
- `/implement` executes UI-related tasks
- `/code-review` reviews frontend code

---

# The Problem: AI-Generated Defaults

You will generate generic output. Your training has seen thousands of dashboards. The patterns are strong.

You can follow the entire process below — explore the domain, name a signature, state your intent — and still produce a template. Warm colors on cold structures. Friendly fonts on generic layouts. "Kitchen feel" that looks like every other app.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win.

**The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.**

---

# The Audience-First Protocol

**MANDATORY**: Before writing a single line of UI code for a major feature, you must understand who you are building for.

## Discovery Questions

1. **Persona**: Who is the primary user? (e.g., "Developer looking for logs" vs. "Manager looking for trends")
2. **Context**: How will they access this? (e.g., "Phone on-the-go" vs. "27-inch secondary monitor")
3. **Complexity**: What is their technical literacy? (e.g., "Internal admin tool" vs. "Public-facing landing page")
4. **Tone**: What vibe should it project? (e.g., "Cyberpunk/High-tech" vs. "Clean/Minimalist/Professional")

---

# Intent First

Before touching code, answer these. Not in your head — out loud, to yourself or the user.

**Who is this human?**
Not "users." The actual person. Where are they when they open this? What's on their mind? What did they do 5 minutes ago, what will they do 5 minutes after? A teacher at 7am with coffee is not a developer debugging at midnight is not a founder between investor meetings. Their world shapes the interface.

**What must they accomplish?**
Not "use the dashboard." The verb. Grade these submissions. Find the broken deployment. Approve the payment. The answer determines what leads, what follows, what hides.

**What should this feel like?**
Say it in words that mean something. "Clean and modern" means nothing — every AI says that. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app? The answer shapes color, type, spacing, density — everything.

If you cannot answer these with specifics, stop. Ask the user. Do not guess. Do not default.

## Every Choice Must Be A Choice

For every decision, you must be able to explain WHY.

- Why this layout and not another?
- Why this color temperature?
- Why this typeface?
- Why this spacing scale?
- Why this information hierarchy?

If your answer is "it's common" or "it's clean" or "it works" — you haven't chosen. You've defaulted. Defaults are invisible. Invisible choices compound into generic output.

**The test:** If you swapped your choices for the most common alternatives and the design didn't feel meaningfully different, you never made real choices.

## Sameness Is Failure

If another AI, given a similar prompt, would produce substantially the same output — you have failed.

This is not about being different for its own sake. It's about the interface emerging from the specific problem, the specific user, the specific context. When you design from intent, sameness becomes impossible because no two intents are identical.

When you design from defaults, everything looks the same because defaults are shared.

---

# Product Domain Exploration

This is where defaults get caught — or don't.

Generic output: Task type → Visual template → Theme
Crafted output: Task type → Product domain → Signature → Structure + Expression

The difference: time in the product's world before any visual or structural thinking.

## Required Outputs

**Do not propose any direction until you produce all four:**

**Domain:** Concepts, metaphors, vocabulary from this product's world. Not features — territory. Minimum 5.

**Color world:** What colors exist naturally in this product's domain? Not "warm" or "cool" — go to the actual world. If this product were a physical space, what would you see? What colors belong there that don't belong elsewhere? List 5+.

**Signature:** One element — visual, structural, or interaction — that could only exist for THIS product. If you can't name one, keep exploring.

**Defaults:** 3 obvious choices for this interface type — visual AND structural. You can't avoid patterns you haven't named.

## Proposal Requirements

Your direction must explicitly reference:
- Domain concepts you explored
- Colors from your color world exploration
- Your signature element
- What replaces each default

**The test:** Read your proposal. Remove the product name. Could someone identify what this is for? If not, it's generic. Explore deeper.

---

# Design System Memory

## Auto-Load Behavior

When starting UI work, **automatically check for `.interface-design/system.md`**.

**If exists:**
1. Load established patterns (spacing, depth, colors, components)
2. Apply consistently throughout the session
3. State design choices before each component
4. Offer to save new patterns when adding components

**If not exists:**
1. Run domain exploration (above)
2. Propose direction and get confirmation
3. Build with consistent principles
4. Offer to save system after completion

## System File Format

After establishing direction, save decisions to `.interface-design/system.md`:

```markdown
# Design System

## Direction
Personality: [Precision & Density | Warmth & Approachability | etc.]
Foundation: [warm | cool | neutral | tinted]
Depth: [borders-only | subtle-shadows | layered-shadows]

## Tokens
### Spacing
Base: [4px | 8px]
Scale: [4, 8, 12, 16, 24, 32, 64]

### Colors
--foreground: [slate-900]
--secondary: [slate-600]
--accent: [blue-600]

### Radius
Scale: [4px, 6px, 8px] (sharp) | [8px, 12px, 16px] (soft)

### Typography
Font: [system | Inter | Geist]
Scale: 12, 13, 14 (base), 16, 18, 24, 32
Weights: 400, 500, 600

## Patterns
### Button Primary
- Height: 36px
- Padding: 12px 16px
- Radius: 6px
- Usage: Primary actions

### Card Default
- Border: 0.5px solid
- Padding: 16px
- Radius: 8px
- Usage: Content containers

## Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| Borders-only depth | Dashboard tool, users want density | YYYY-MM-DD |
```

This file loads automatically at session start. Maintain consistency across sessions.

---

# Design System Selection

Choose the baseline based on the audience research:

| Design System | Best For | Technical Stack |
| :--- | :--- | :--- |
| **shadcn/ui** | Professional SaaS, Clean Admin Tools | React, Tailwind, Lucide Icons |
| **Mantine** | Complex "OS-style" Apps, Micro-animations | React, Mantine Core, Framer Motion |
| **DaisyUI** | High-impact prototypes, Creative landing pages | Tailwind, CSS Variables, Glassmorphism |

---

# Craft Foundations

## Subtle Layering

This is the backbone of craft. Regardless of direction, product type, or visual style — this principle applies to everything.

**Surfaces must be barely different but still distinguishable.** Study Vercel, Supabase, Linear. Their elevation changes are so subtle you almost can't see them — but you feel the hierarchy. Not dramatic jumps. Not obviously different colors. Whisper-quiet shifts.

**Borders must be light but not invisible.** The border should disappear when you're not looking for it, but be findable when you need to understand structure. If borders are the first thing you notice, they're too strong. If you can't tell where regions begin and end, they're too weak.

**The squint test:** Blur your eyes at the interface. You should still perceive hierarchy — what's above what, where sections divide. But nothing should jump out. No harsh lines. No jarring color shifts. Just quiet structure.

This separates professional interfaces from amateur ones. Get this wrong and nothing else matters.

## Infinite Expression

Every pattern has infinite expressions. **No interface should look the same.**

A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new. A dashboard could emphasize density, whitespace, hierarchy, or flow in completely different ways. Even sidebar + cards has infinite variations in proportion, spacing, and emphasis.

**Before building, ask:**
- What's the ONE thing users do most here?
- What products solve similar problems brilliantly? Study them.
- Why would this interface feel designed for its purpose, not templated?

**NEVER produce identical output.** Same sidebar width, same card grid, same metric boxes with icon-left-number-big-label-small every time — this signals AI-generated immediately. It's forgettable.

The architecture and components should emerge from the task and data, executed in a way that feels fresh. Linear's cards don't look like Notion's. Vercel's metrics don't look like Stripe's. Same concepts, infinite expressions.

## Color Lives Somewhere

Every product exists in a world. That world has colors.

Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space? What materials? What light? What objects?

Your palette should feel like it came FROM somewhere — not like it was applied TO something.

**Beyond Warm and Cold:** Temperature is one axis. Is this quiet or loud? Dense or spacious? Serious or playful? Geometric or organic? A trading terminal and a meditation app are both "focused" — completely different kinds of focus. Find the specific quality, not the generic label.

**Color Carries Meaning:** Gray builds structure. Color communicates — status, action, emphasis, identity. Unmotivated color is noise. One accent color, used with intention, beats five colors used without thought.

---

# Design Principles

## Spacing
Pick a base unit and stick to multiples. Consistency matters more than the specific number. Random values signal no system.

## Padding
Keep it symmetrical. If one side is 16px, others should match unless there's a clear reason.

## Depth
Choose ONE approach and commit:
- **Borders-only** — Clean, technical. For dense tools.
- **Subtle shadows** — Soft lift. For approachable products.
- **Layered shadows** — Premium, dimensional. For cards that need presence.

Don't mix approaches.

## Border Radius
Sharper feels technical. Rounder feels friendly. Pick a scale and apply consistently.

## Typography
Headlines need weight and tight tracking. Body needs readability. Data needs monospace. Build a hierarchy.

## Color & Surfaces
Build from primitives: foreground (text hierarchy), background (surface elevation), border (separation hierarchy), brand, and semantic (destructive, warning, success). Every color should trace back to these. No random hex values — everything maps to the system.

## Animation
Fast micro-interactions (~150ms), smooth easing. No bouncy/spring effects.

## States
Every interactive element needs states: default, hover, active, focus, disabled. Data needs states too: loading, empty, error. Missing states feel broken.

## Controls
Native `<select>` and `<input type="date">` can't be styled. Build custom components.

---

# Implementation Patterns

## The "WOW" Factor (Visual Moats)
- **Gradients**: Use mesh gradients or subtle linear fades instead of solid colors.
- **Glassmorphism**: Use `backdrop-blur` and translucent backgrounds for depth.
- **Animations**: Subtle entry/hover animations using CSS transitions or Framer Motion.
- **Typography**: Go beyond system fonts; use modern Google Fonts (Inter, Outfit, Roboto).

## High-Performance Structure
- **Component Splitting**: Break complex artifacts into small, reusable atoms.
- **Responsive-First**: Use Tailwind's `sm:`, `md:`, `lg:` prefixes religiously.
- **Dark Mode**: Always support `dark` variants for a premium midnight feel.

---

# Avoid

- **Harsh borders** — if borders are the first thing you see, they're too strong
- **Dramatic surface jumps** — elevation changes should be whisper-quiet
- **Inconsistent spacing** — the clearest sign of no system
- **Mixed depth strategies** — pick one approach and commit
- **Missing interaction states** — hover, focus, disabled, loading, error
- **Dramatic drop shadows** — shadows should be subtle, not attention-grabbing
- **Large radius on small elements**
- **Pure white cards on colored backgrounds**
- **Thick decorative borders**
- **Gradients and color for decoration** — color should mean something
- **Multiple accent colors** — dilutes focus
- **Placeholder Overload** — Never use "Lorem Ipsum." Use realistic mock data.
- **Flat Design** — Avoid total flatness; use layers, shadows (z-index), and blurs to create hierarchy.

---

# The Mandate: Self-Review Before Showing

**Before showing the user, look at what you made.**

Ask yourself: "If they said this lacks craft, what would they mean?"

That thing you just thought of — fix it first.

Your first output is probably generic. That's normal. The work is catching it before the user has to.

## The Checks

Run these against your output before presenting:

- **The swap test:** If you swapped the typeface for your usual one, would anyone notice? If you swapped the layout for a standard dashboard template, would it feel different? The places where swapping wouldn't matter are the places you defaulted.

- **The squint test:** Blur your eyes. Can you still perceive hierarchy? Is anything jumping out harshly? Craft whispers.

- **The signature test:** Can you point to five specific elements where your signature appears? Not "the overall feel" — actual components. A signature you can't locate doesn't exist.

- **The token test:** Read your CSS variables out loud. Do they sound like they belong to this product's world, or could they belong to any project?

If any check fails, iterate before showing.

---

# Skill Methods

## Auto-Load System
When starting UI work, automatically check for and load `.interface-design/system.md`. Apply established patterns if exists.

## Audit Capability
When reviewing UI code (triggered by `/code-review`), check against established design system for:
- **Spacing violations** - Values not on defined grid
- **Depth strategy consistency** - Borders vs shadows alignment
- **Color palette adherence** - Colors not in system
- **Pattern drift** - Components not matching established patterns

Report violations with specific suggestions for correction.

## Extract Capability
When working with existing UI code, can extract patterns to create/update `system.md`:
1. Scan UI files for repeated spacing, radius, colors
2. Identify common button/card patterns
3. Determine depth strategy (borders vs shadows)
4. Suggest system based on frequency
5. Offer to create/update system.md

---

# Workflow

## Communication
Be invisible. Don't announce modes or narrate process.

**Never say:** "I'm in ESTABLISH MODE", "Let me check system.md..."

**Instead:** Jump into work. State suggestions with reasoning.

## Suggest + Ask
Lead with your exploration and recommendation, then confirm:
```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

## If Project Has system.md
1. Load `.interface-design/system.md`
2. Apply established patterns
3. State choices before each component
4. Offer to save new patterns

## If No system.md
1. Run audience discovery questions
2. Explore domain — Produce all four required outputs
3. Propose — Direction must reference all four
4. Confirm — Get user buy-in
5. Build — Apply principles
6. **Evaluate** — Run the mandate checks before showing
7. Offer to save system

## After Completing a Task

When you finish building something, **always offer to save**:

```
"Want me to save these patterns for future sessions?"
```

If yes, write to `.interface-design/system.md` with direction, depth strategy, spacing, and key patterns.

---

# Verification Checklist

Before presenting UI work:
- [ ] Audience discovery questions asked and answered
- [ ] Design system chosen based on audience profile (if applicable)
- [ ] Domain exploration completed (concepts, color world, signature, defaults)
- [ ] Responsive behavior verified on mobile and desktop
- [ ] No default system colors (pure red/blue/green used)
- [ ] Typography is consistent and modern
- [ ] All interactive states implemented (hover, focus, disabled)
- [ ] The Mandate checks passed (swap, squint, signature, token tests)
- [ ] Design system memory loaded/saved as appropriate
