---
name: interaction-design
description: Design intuitive, meaningful interactions grounded in user goals and cognitive principles. Use when designing component behaviors, user flows, feedback systems, error handling, loading states, transitions, accessibility, keyboard navigation, touch/gesture interactions, or when evaluating interaction quality. Also use for modal vs modeless decisions, direct manipulation patterns, input device considerations, emotional/dramatic aspects of UX, or when asked about making interfaces feel responsive, humane, and goal-directed.
---

# Interaction Design

Design interactions that help real people accomplish real goals with minimum friction and maximum meaning.

## The Fundamental Question

Before any pattern or timing value, ask: **What is the user trying to accomplish, and how does this interaction help or hinder that goal?**

Interaction design is not about mechanisms. It is about helping specific people achieve specific purposes while respecting their time, attention, and humanity.

## Output Contracts

### Interaction Specification

```markdown
## Interaction Spec: [Component Name]

### User Goal
What is the user trying to accomplish? What are the stakes?

### Conceptual Model
How should users understand this interaction? What mental model should they form?

### States & Transitions
| State | Appearance | Transition | Emotional Tone |
|-------|------------|------------|----------------|
| Default | [appearance] | — | [calm/ready/inviting] |
| Hover | [changes] | 150ms ease-out | [responsive/acknowledged] |
| Active | [pressed] | 50ms | [committed/engaged] |
| Loading | [feedback] | — | [progressing/patient] |
| Success | [confirmation] | 200ms | [accomplished/closure] |
| Error | [clear indication] | — | [recoverable/guided] |

### Keyboard & Input
- Tab: [focus behavior]
- Enter/Space: [activation]
- Escape: [reversal/dismissal]
- Touch: [gesture, target size]

### Error Prevention & Recovery
- How does design prevent errors?
- What happens when errors occur?
- How does user recover?

### Accessibility
- Screen reader announcement
- Focus management
- Reduced motion behavior
```

### Flow Analysis

```markdown
## Flow Analysis: [Journey Name]

### User Goal & Stakes
What does success mean? What does failure cost?

### Dramatic Arc
- Setup: How does user enter this flow?
- Rising action: What builds toward the goal?
- Climax: The moment of commitment/completion
- Resolution: Confirmation and next steps

### Steps
1. [Step] → [Interaction] → [User feeling]

### Friction Analysis
- Necessary friction (builds engagement/prevents errors)
- Excise to eliminate (work that doesn't serve the goal)

### Error Paths
- [Error scenario]: [Prevention] → [Recovery]
```

## Core Principles

### 1. Goal-Directed Design

Users are not "operators" triggering state changes. They are people with purposes.

**Ask first:**
- Who is using this? (Not abstract "users"—specific archetypes)
- What are they trying to accomplish?
- What excise can we eliminate? (Work that doesn't serve their goal)
- How should they feel during and after?

**The perpetual intermediate:** Most users are neither novices learning nor experts optimizing. They learned enough to work and won't learn more. Design for them—make the common path fast while keeping advanced options discoverable but unobtrusive.

### 2. Conceptual Models

Users must form accurate mental models of how the system works. The gap between the designer's model and the user's model is where confusion lives.

**The system image** (what users see and interact with) must accurately convey the designer's model. When users are confused, the system image has failed—not the user.

**Signifiers** communicate where action is possible and how to perform it. A drag handle icon is a signifier; the ability to drag is the affordance. Design signifiers that make affordances discoverable.

### 3. Direct Manipulation

Make the computer disappear so users concentrate on their task.

**Core properties:**
- Visible objects of interest, always accessible
- Rapid, incremental, reversible actions
- Immediate feedback—action and result visibly connected
- Operations in the problem domain, not command syntax

**The syntactic/semantic insight:** Direct manipulation works because it operates at the semantic level (the problem domain) rather than requiring translation into syntactic commands. This reduces cognitive load by eliminating the translation step.

**When direct manipulation is inappropriate:**
- Precise specification (typing "24pt" may be better than dragging)
- Batch operations across many objects
- Abstract operations without spatial metaphor
- Expert users who prefer keyboard efficiency

### 4. Reversibility Enables Exploration

Reversibility is not a feature—it is a psychological safety mechanism that transforms a system from intimidating to inviting.

- **Undo depth:** Support multi-step undo, not just single-step
- **Congruent inverses:** If Cmd+B bolds, Cmd+B unbolds (same action reverses)
- **State visibility:** Show that undo is available
- **Graceful degradation:** When true undo isn't possible, confirm before destructive actions

### 5. Error Prevention Over Error Handling

Errors are usually design failures, not user failures.

**Slips** (execution errors): User intends correctly but acts wrong
- Prevent with constraints, defaults, confirmation for destructive actions

**Mistakes** (intention errors): User forms wrong goal or plan
- Prevent with clear conceptual models, visible system state

**Design forcing functions:**
- Interlocks: Require prerequisite actions
- Lockins: Prevent stopping mid-action when dangerous
- Lockouts: Prevent entering dangerous states

See [references/cognitive-foundations.md](references/cognitive-foundations.md) for error psychology and prevention patterns.

### 6. Feedback & System Status

Every action deserves acknowledgment. Users should never wonder "Did that work?"

| Response Time | Perception | Design Response |
|---------------|------------|-----------------|
| <100ms | Instant | Direct result, no indicator |
| 100ms–1s | Brief delay | Subtle state change (cursor, opacity) |
| 1–10s | Noticeable wait | Spinner or determinate progress |
| >10s | Long operation | Progress bar, estimate, allow cancel |

**Optimistic UI:** Update immediately, reconcile errors gracefully. But be honest—don't show success before confirming it for important actions.

### 7. Modality: A Necessary Evil

Modes cause errors when users forget which mode they're in. But modes also isolate cognitive scope and can reduce errors when users would otherwise forget context.

**Use modeless design** (inspectors, inline editing) when:
- User needs to see results while adjusting
- Trial-and-error is expected
- Context switching is frequent

**Accept modality** when:
- Isolating scope reduces errors (complex multi-step wizards)
- Action is destructive and confirmation prevents accidents
- System needs exclusive attention (authentication)

**If you must use modes:**
- Make current mode highly visible (not just status bar)
- Ensure mode indicators are near the locus of attention
- Provide quick escape (Escape key, clear exit path)

### 8. Meaning and Emotional Design

Interactions are not just efficient or inefficient—they carry meaning.

**Visceral level:** Immediate emotional response to appearance
**Behavioral level:** Pleasure or frustration from use
**Reflective level:** What the experience means, how it's remembered

A loading state that builds anticipation differs from one that frustrates—same mechanism, different meaning. Consider:
- What should the user feel during this interaction?
- What story does this interaction tell?
- How does completing this action transform the user's situation?

See [references/goals-and-context.md](references/goals-and-context.md) for dramatic structure and emotional design.

## Decision Frameworks

### Activation Type

| Use Frequency | Recommended Activation | Rationale |
|---------------|------------------------|-----------|
| Constant | Always visible (spatial) | Zero activation cost |
| Frequent | Keyboard shortcut + visible control | Fast for regulars, discoverable for others |
| Occasional | Menu or command palette | Saves space, still findable |
| Rare/Dangerous | Menu only, possibly nested | Prevents accidents |

### When to Animate

Animation serves purposes—it is not decoration.

**Animate when:**
- Maintaining object constancy during transitions
- Communicating causality (this caused that)
- Reducing change blindness
- Conveying emotional tone appropriate to context

**Don't animate when:**
- User performs action habitually (animation becomes excise)
- Speed is critical (expert workflows)
- User has indicated reduced motion preference
- Animation would obscure rather than clarify

See [references/animation-timing.md](references/animation-timing.md) for timing, curves, and emotional qualities.

### Friction: Eliminate or Leverage?

Not all friction is bad. Distinguish:

**Excise (eliminate):** Work that doesn't serve user's goal
- Navigating to buried menus
- Re-entering information the system knows
- Waiting for unnecessary animations
- Confirming non-destructive actions

**Productive friction (consider keeping):**
- Confirmation before irreversible actions
- Deliberate pacing that prevents rushed errors
- Moments that build anticipation or mark significance
- Resistance that indicates "this matters"

## Input & Physicality

The device shapes the interaction. A finger on glass is not a stylus is not a mouse.

### Touch Targets
| Platform | Minimum | Comfortable |
|----------|---------|-------------|
| iOS | 44×44pt | 48pt+ |
| Android | 48×48dp | 56dp+ |
| Web (touch) | 44×44px | 48px+ |

### Gesture Vocabulary
| Gesture | Use | Considerations |
|---------|-----|----------------|
| Tap | Primary action | Clear affordance required |
| Long-press | Secondary/context | Needs discoverability hint |
| Swipe | Reveal, delete, navigate | Always provide undo; don't hide primary actions |
| Pinch | Zoom | Maintain focus under fingers |

### Two-Handed Interaction

When designing for tablets or considering desktop power users:
- Non-dominant hand: coarse positioning, context setting
- Dominant hand: fine manipulation, action
- Consider: Can both hands be usefully engaged?

See [references/input-and-physicality.md](references/input-and-physicality.md) for device-specific patterns and haptics.

## Platform Considerations

### Web
- Focus management in SPAs (trap in modals, restore on close)
- Respect `prefers-reduced-motion`
- Design for touch AND mouse—avoid hover-only interactions
- Keyboard navigation for all interactive elements

### iOS
- Respect system gestures and scroll physics
- Support Dynamic Type (test at largest sizes)
- Haptic feedback for significant moments
- VoiceOver with proper traits

### Android
- Material motion principles
- Predictive back gesture (Android 14+)
- Edge-to-edge with proper insets
- TalkBack support

### Desktop
- Keyboard shortcuts with discoverability
- Multi-window state management
- Trackpad gestures where appropriate
- High information density options for power users

## Anti-Patterns

### Breaking Direct Manipulation
❌ Modal dialog with Preview button
✓ Live preview as user adjusts

❌ Must click Apply to see changes
✓ Changes visible immediately, undo available

### Hidden State
❌ Current mode only in status bar
✓ Mode visible at locus of attention

❌ Unsaved changes with no indicator
✓ Clear dirty state (title, dot, changed button)

### Excise Accumulation
❌ Confirmation for every action
✓ Undo support; confirm only destructive/irreversible

❌ Animation that user must wait through
✓ Animation user can interrupt or that doesn't block

### Cognitive Overload
❌ All options visible at once
✓ Progressive disclosure based on task stage

❌ Error messages that blame user
✓ Clear explanation + recovery path

## Reference Files

Load these as needed for detailed guidance:

- **[references/goals-and-context.md](references/goals-and-context.md)** — User goals, personas, dramatic structure, emotional design
- **[references/cognitive-foundations.md](references/cognitive-foundations.md)** — Mental models, error psychology, measurement approaches
- **[references/input-and-physicality.md](references/input-and-physicality.md)** — Input devices, haptics, two-handed interaction, sketching
- **[references/component-patterns.md](references/component-patterns.md)** — Detailed patterns for forms, modals, menus, etc.
- **[references/animation-timing.md](references/animation-timing.md)** — Timing, easing, springs, emotional qualities
- **[references/accessibility-patterns.md](references/accessibility-patterns.md)** — ARIA, focus management, screen readers

## Theoretical Foundations

- **Direct Manipulation** (Shneiderman): Visibility, reversibility, immediate feedback. See [references/direct-manipulation.md](references/direct-manipulation.md)
- **Instrumental Interaction** (Beaudouin-Lafon): Tools mediating user-object relationship; degrees of indirection, integration, compatibility. See [references/instrumental-interaction.md](references/instrumental-interaction.md)
- **Goal-Directed Design** (Cooper): Personas, perpetual intermediates, eliminating excise
- **Emotional Design** (Norman): Visceral, behavioral, reflective levels
- **Computers as Theatre** (Laurel): Dramatic structure, meaning, engagement
