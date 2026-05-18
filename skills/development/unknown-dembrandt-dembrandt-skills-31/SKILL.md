---
name: visual-emphasis-and-hierarchy
description: The most important actions and content in a UI should be visually prominent — through size, colour, weight, and position. Visual hierarchy guides the user's eye to what matters most and signals which action is primary. Use when designing button groups, CTAs, dashboards, cards, or any layout where actions or content have different importance levels.
metadata:
  priority: 8
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
    - "tailwind.config.*"
  promptSignals:
    phrases:
      - "primary button"
      - "call to action"
      - "visual hierarchy"
      - "emphasis"
      - "most important"
      - "highlight"
      - "prominent"
      - "CTA"
      - "text over image"
      - "hero banner"
      - "legibility"
retrieval:
  aliases:
    - visual hierarchy
    - emphasis
    - primary action
    - CTA design
    - button hierarchy
    - content priority
  intents:
    - make the primary action stand out
    - design button hierarchy
    - guide user attention
    - emphasise key content
    - reduce visual noise
  examples:
    - make it obvious what the user should click
    - design the button group for this form
    - highlight the most important feature on this page
---

# Visual Emphasis and Hierarchy

Every screen has a most-important thing. Visual hierarchy is the design work that makes sure the user's eye finds it first — without requiring the user to read everything and decide for themselves.

Emphasis is achieved through **size**, **colour**, **weight**, **contrast**, and **position**. These tools work because they are relative: an element looks important because it differs from what surrounds it.

## The Hierarchy Ladder

Design every action group and content area with a clear hierarchy:

| Level | Role | Visual treatment |
|---|---|---|
| **Primary** | The one action the user should most likely take | Filled, brand colour, largest button in the group |
| **Secondary** | An alternative action of moderate importance | Outlined or ghost, neutral colour, same or slightly smaller size |
| **Tertiary** | Rarely needed, destructive, or low-priority | Text link or subtle ghost, smaller, visually recessive |
| **Disabled** | Unavailable | Low contrast, no hover state — signals "not yet" |

There should be **at most one primary action per view** or per logical section. Two filled buttons side by side cancel each other out — both feel equally important, so neither guides the user.

## Size as Emphasis

A larger button, heading, or element draws the eye before a smaller one. Use size deliberately:

- The primary CTA is the largest interactive element in its group
- Page headings are larger than section headings, which are larger than labels
- A featured product, plan, or option can be physically larger than its peers to signal recommendation

Size differences must be perceptible — a 2px difference reads as inconsistency, not hierarchy. Use your modular scale for type; use meaningful size steps for components.

## Colour as Emphasis

Colour is the strongest emphasis signal and therefore the most easily overused.

- **One brand colour for primary actions** — used sparingly so it retains its signal
- Secondary and tertiary actions should be neutral (grey, outlined) so the primary colour stands out
- Status colours (red, orange, green) should never appear on primary CTAs — they carry their own semantic meaning

## Brand Colour as Large Areas

Brand primary colours work well as large background regions — hero sections, feature banners, section dividers. This is different from using brand colour on interactive elements.

The rule: **pick one role and commit to it per view.**

- Brand colour as a large area → buttons and links on that section use white or a high-contrast neutral, not the brand colour again
- Brand colour on interactive elements → backgrounds stay neutral so the colour retains its signal

Used as a bold background, brand colour communicates identity and energy. Used simultaneously on both backgrounds and buttons, it loses all signal — everything blends together.

## Contrast and Whitespace as a Focal Point

Emphasis is not just about what you add (colour, size), but also what you remove (distraction).

**The "Contrast + Space" Rule:** To create a powerful focal point, combine a high-contrast element (or a bold brand colour) with generous **whitespace (negative space)** around it.
- **Isolation:** Whitespace acts as a frame, isolating the primary action or message.
- **Visual Silence:** By removing competing elements nearby, you ensure the user's eye has only one logical place to land.
- **Scale:** A small high-contrast button in a large empty field can have more "pull" than a giant button in a crowded layout.

Use whitespace deliberately to "push" the user's attention toward the primary goal.

```
✓ Dark brand-colour hero section + white CTA button
✓ White page + brand-colour primary button
✗ Brand-colour hero section + brand-colour button on top of it
```

## Weight and Contrast

Typography weight communicates importance within text and aids scannability.

- **Bold for meaning, not just emphasis.** Avoid bolding individual words in isolation. Instead, bold the meaningful parts of a sentence or a complete phrase that carries the key information. This allows users to scan and understand the core message without reading the whole block.
- **Bold headings and labels.** Use weight to distinguish the structure of the information from the information itself.
- **Regular weight for supporting content.** Keep descriptions and secondary info in regular weight to provide a "rest area" for the eye.
- **Light or muted colour for metadata.** Use low contrast for timestamps, secondary labels, or "fine print".

In data-heavy UIs (tables, dashboards), bold the **primary metric or the row's identifying name**. The eye should be able to jump from one bold anchor to the next to quickly locate data.

## Text Over Imagery

Text legibility is often compromised when placed directly over photographs or complex patterns. To maintain hierarchy and credibility:

- **Subtle Text Shadow:** Use a soft, high-blur text-shadow (e.g. `0 2px 4px rgba(0,0,0,0.2)`) to lift text off the background. It should be felt rather than seen — if the shadow is obvious, it's too heavy.
- **Image Tints & Gradients:** Apply a subtle dark tint or a linear gradient (e.g. from transparent to 40% black) over the image to increase contrast behind the text.
- **Selective Backgrounds:** When selecting stock footage, look for images with "negative space" or solid color areas (e.g. a clear sky, a plain wall) where text can sit naturally.
- **Scrims:** Use a "scrim" (a semi-transparent gradient overlay) specifically in the area where text sits to preserve the image's vibrant colours while ensuring text is readable.

## Position as Emphasis

Users in left-to-right reading cultures scan top-left first. Position reinforces hierarchy:

- Primary action: bottom-right of a form or dialog (natural end of the reading flow), or top-right of a page header
- Most important content: top of the page, above the fold
- Warnings and critical status: top of the affected section, not buried at the bottom
- Destructive actions (Delete, Remove): visually separated from constructive actions, often at the end of an action group

## One Primary Action Per View

The biggest hierarchy mistake is giving everything equal emphasis. When every button is filled, every heading is bold, and every card is highlighted, the user has no signal about where to start.

**Rule:** In any view, ask "what is the single most likely next action for most users?" Make that one thing visually dominant. Everything else recedes.

## Cursor

Every clickable or interactive element must use `cursor: pointer`. Users rely on the cursor changing to confirm that an element is actionable — without it, buttons and links feel broken or unresponsive.

```css
button, a, [role="button"], [onclick], label { cursor: pointer; }
```

Never leave interactive elements on the default `cursor: auto`. The one exception is text inputs, which correctly use `cursor: text`.

## Review Checklist

- [ ] Is there at most one primary (filled, brand-coloured) button per section?
- [ ] Is the primary action framed by enough whitespace to stand out from surrounding content?
- [ ] Are secondary and tertiary actions visually recessive compared to the primary?
- [ ] Is the most important content positioned highest and/or largest?
- [ ] Are size differences between hierarchy levels perceptible, not just 1–2px?
- [ ] Is brand colour used sparingly enough that it retains its emphasis signal?
- [ ] Are destructive actions visually distinct and separated from constructive actions?
- [ ] Do all buttons, links, and interactive elements use `cursor: pointer`?
- [ ] Does bold text appear only on genuinely important labels, values, or meaningful phrases?
- [ ] Is text overlaid on images easily legible (using shadows, tints, or smart image selection)?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Two or more filled primary buttons side by side | Both feel equally important — no guidance | One primary, one secondary (outlined) |
| Brand colour used on backgrounds, headers, AND buttons | Colour loses emphasis signal | Reserve brand colour for one role |
| All text the same weight on a data-heavy screen | No visual entry point for the eye | Bold the key metric or label per group |
| "Cancel" and "Confirm" buttons the same size and colour | User must read to distinguish | Primary = filled, Cancel = ghost or text link |
| White text over a bright or busy image | Text is illegible or "vibrates" | Add a subtle text-shadow, image tint, or select images with solid-color areas |
| Important warnings placed below the fold | Users miss them | Surface critical status at the top of the affected section |
| Buttons changing size or shifting on interaction | Feels unstable and unpolished ("squishy" UI) | Maintain rock-solid layout; use color and internal feedback only |
