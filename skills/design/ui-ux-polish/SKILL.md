---
name: ui-ux-polish
description: "Iterative UI/UX polishing workflow for web applications. The exact prompt and methodology for achieving Stripe-level visual polish through multiple passes."
---

# UI/UX Polish — Iterative Enhancement Workflow

> **When to Use:** This is for when your site/app already works and looks decent and you want to improve it. There's a different approach when it looks bad and needs a complete overhaul.
>
> **Key Insight:** Something about asking for agreement from the model ("don't you agree?") somehow motivates it to polish things up better. Also, instructing it to separately think through desktop vs mobile leads to much better outcomes.

---

## The Workflow

### Overview

1. App already works and looks decent
2. Run the polish prompt
3. Agent makes incremental improvements
4. Repeat many times (10+ iterations)
5. Each pass adds small improvements that compound

### Why Multiple Passes Work

- Each time, it tries to make some incremental improvement, even if it's minor
- These really add up after 10 iterations!
- Multiple agents can work on this simultaneously
- Cumulative effect is dramatic

---

## THE EXACT PROMPT — UI/UX Polish

This prompt is used so frequently it's worth putting on a Stream Deck button:

```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

---

## Why This Prompt Works

### 1. Asks for Agreement

The phrase "don't you agree?" engages the model's reasoning about whether improvements are possible, rather than just executing instructions.

### 2. Separates Desktop and Mobile

```
"carefully consider desktop UI/UX and mobile UI/UX separately...
hyper-optimize for both separately to play to the specifics of each modality"
```

This prevents the model from making compromises that work "okay" on both but great on neither.

### 3. Sets High Standards

References:
- "world class"
- "best practices like those used by Stripe"
- "makes people gasp at how stunning and perfect it is"

These anchors push the model toward higher quality than generic "make it better" instructions.

### 4. Uses Ultrathink

Extended thinking allows the model to:
- Analyze the current state thoroughly
- Consider multiple improvement options
- Choose the highest-impact changes
- Think through edge cases

---

## Best Models for This Task

| Model | Effectiveness |
|-------|---------------|
| **Claude Code + Opus 4.5** | Excellent |
| **Codex + GPT 5.2** (High/Extra-High reasoning) | Excellent |
| **Gemini CLI** | Good |

---

## Tech Stack Compatibility

This prompt works with:
- Next.js 16 + React 19 + Tailwind 4
- Any modern web framework
- Applications using Framer Motion or similar animation libraries
- Pretty much anything—it's generic enough to adapt

---

## Iteration Protocol

### Single Agent

```
# First pass
[Run the UI/UX polish prompt]

# Review changes
[Agent makes improvements]

# Second pass
[Run the same prompt again]

# Repeat 10+ times until changes become minimal
```

### Multiple Agents

You can have more than one agent working on UI/UX polish simultaneously:
- They'll focus on different areas
- Use file reservations to avoid conflicts
- Compound improvements faster

---

## When to Use vs. When NOT to Use

### USE This Prompt When:

- App works correctly
- Basic styling is in place
- You want to elevate from "decent" to "world-class"
- Ready for iterative refinement
- Want to optimize for both desktop and mobile

### DON'T Use This Prompt When:

- App is broken or buggy (fix bugs first)
- Styling is fundamentally wrong (need complete overhaul)
- No basic design system in place
- Starting from scratch

For complete overhauls, use a different approach focused on establishing a design system and component library first.

---

## What the Model Typically Improves

### Visual Polish
- Spacing and padding consistency
- Typography hierarchy
- Color contrast and accessibility
- Shadow and depth effects
- Border radius consistency
- Hover/focus states

### Interaction Design
- Button feedback
- Loading states
- Transitions and animations
- Error state handling
- Empty state design

### Mobile Optimization
- Touch target sizes
- Responsive breakpoints
- Mobile-specific navigation
- Gesture support
- Performance on mobile devices

### Desktop Optimization
- Keyboard navigation
- Hover states
- Multi-column layouts
- Sidebar navigation
- Power user shortcuts

---

## Tracking Progress

After each iteration, you might notice:
- Subtle shadow improvements
- Better spacing rhythm
- More consistent typography
- Smoother animations
- Better responsive behavior

These small changes compound. An app after 10 passes looks dramatically better than after 1 pass.

---

## Integration with Beads

For systematic UI/UX work, create beads:

```bash
bd create "Polish homepage UI/UX for desktop" -t enhancement -p 2
bd create "Polish homepage UI/UX for mobile" -t enhancement -p 2
bd create "Polish dashboard UI/UX for desktop" -t enhancement -p 2
bd create "Polish dashboard UI/UX for mobile" -t enhancement -p 2
```

This lets agents work on UI/UX polish as part of the normal bead workflow.

---

## Complete Prompt Reference

### Main Polish Prompt
```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

### Alternative: General Scrutiny (from agent-swarm-workflow)
```
Great, now I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high quality, like Stripe-level apps.
```

---

## Tips

1. **Don't skip iterations** — Even when changes seem small, keep going
2. **Review changes** — Make sure the model isn't breaking things
3. **Test on real devices** — Desktop browser != mobile experience
4. **Consider accessibility** — WCAG compliance matters
5. **Keep performance in mind** — Pretty but slow is bad UX
