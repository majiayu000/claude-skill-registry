---
name: ui-design-patterns
description: Practical UI design patterns and principles for creating polished, professional interfaces. Based on proven techniques from Refactoring UI and Practical UI.
version: 1.1.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - ui
  - design
  - layout
  - spacing
  - typography
  - color
  - hierarchy
  - styling
  - visual
  - accessibility
  - usability
  - contrast
---

# UI Design Patterns

Practical guidelines for creating polished, professional user interfaces without relying on graphic design talent. These patterns work for any web project, including TYPO3 frontend development.

## Acknowledgements

These patterns are adapted from two excellent resources:

- **Refactoring UI** by Adam Wathan & Steve Schoger — The definitive guide to practical UI design for developers
- **Practical UI** (2nd Edition) by Adham Dannaway — Quick and practical UI design guidelines for intuitive, accessible, and beautiful interfaces

We highly recommend both works for deepening your UI design knowledge.

---

## 0. Core Principles (from Practical UI)

Before diving into specific patterns, internalize these foundational principles:

### Minimize Usability Risks

Base design decisions on risk assessment—the risk that someone could have difficulty using an interface:

- Light grey text may look sleek but risks readability issues
- Icons without labels risk confusion about meaning
- Colored heading text risks being mistaken for links

**Always consider:** people with poor eyesight, low computer literacy, reduced dexterity, and cognitive differences.

### Have a Logical Reason for Every Design Detail

Every UI element should have a rationale. "That looks nice" is not constructive feedback. Be able to articulate *why* each design decision was made.

| Element | Logical Reason |
|---------|----------------|
| Left-aligned text | Creates neat edge, improves readability |
| Descriptive headings | Scannable, works with screen readers |
| Blue underlined links | Indicates interactivity, accessible for color blind |
| Grouped spacing | Related items closer together reduce cognitive load |

### Minimize Interaction Cost

Interaction cost = physical + mental effort to complete a task. Reduce it by:

1. **Keep related actions close** (Fitts's Law—closer/larger targets are faster to click)
2. **Reduce distractions** (avoid attention-grabbing elements that pull focus)
3. **Use progressive disclosure** (reveal complexity only when needed)

### Minimize Cognitive Load

Cognitive load is the mental effort required to use an interface. Reduce it by:

- Breaking information into smaller, digestible chunks
- Using familiar patterns people already understand
- Removing unnecessary elements and decisions
- Grouping related items visually

### Design System First

Create a system of reusable guidelines before designing:

- Color palette with usage rules
- Typography scale
- Spacing system
- Component patterns
- Interaction states

This ensures consistency and speeds up decision-making.

### Accessibility is Non-Negotiable

Meet **WCAG 2.1 Level AA** at minimum:

| Requirement | Minimum Ratio |
|-------------|---------------|
| Small text (≤18px) | 4.5:1 contrast |
| Large text (>18px bold or >24px) | 3:1 contrast |
| UI elements (borders, icons) | 3:1 contrast |

**Never rely on color alone**—always pair with icons, patterns, or text for color blind users.

### Use Common Design Patterns

Per Jakob's Law, stick with patterns people already know:

- Conventional form fields (not custom/unfamiliar styles)
- Standard navigation patterns
- Expected icon meanings
- Familiar button behaviors

Save creativity for your product's unique value proposition, not basic UI conventions.

### The 80/20 Rule

Roughly 80% of users use 20% of features. Prioritize the common paths:

- Optimize for frequent tasks, not edge cases
- Focus design effort where it has the largest impact
- Don't over-engineer rarely-used features

---

## 1. Starting from Scratch

### Start with a Feature, Not a Layout

Don't begin by designing the shell (navigation, sidebar, footer). Start with actual functionality.

**Wrong approach:**
- "Should it have a top nav or sidebar?"
- "Where should the logo go?"

**Right approach:**
- Design the core feature first (search form, product card, user profile)
- The navigation will reveal itself as you design features

### Detail Comes Later

In early stages, ignore typefaces, shadows, and icons. Use thick markers or low-fidelity wireframes to explore layouts quickly.

### Hold the Color

Design in grayscale first. This forces you to use spacing, contrast, and size to create hierarchy. Color comes later as enhancement.

### Work in Cycles

1. Design a simple version of the next feature
2. Build it
3. Iterate on the working design
4. Move to the next feature

### Be a Pessimist

Design the smallest useful version first. Don't design features you can't build yet—ship what works.

---

## 2. Hierarchy is Everything

### Not All Elements Are Equal

Visual hierarchy makes interfaces feel "designed". When everything competes for attention, nothing stands out.

**The key:** Deliberately de-emphasize secondary and tertiary information while highlighting what matters most.

### Size Isn't Everything

Don't rely solely on font size for hierarchy. Use:

| Technique | Effect |
|-----------|--------|
| **Font weight** | 600-700 for emphasis, 400-500 for normal |
| **Color contrast** | Dark for primary, grey for secondary, light grey for tertiary |
| **Spacing** | More space around important elements |

**Color guidelines for text:**
- Primary content: Dark color (e.g., `slate-900`)
- Secondary content: Medium grey (e.g., `slate-600`)
- Tertiary content: Light grey (e.g., `slate-400`)

### Don't Use Grey Text on Colored Backgrounds

Grey text on colored backgrounds looks washed out. Instead, pick a color with the same hue as the background, adjusting saturation and lightness.

```css
/* Bad: Grey on blue background */
background: hsl(220, 80%, 50%);
color: #888888; /* Looks dull */

/* Good: Tinted text matching background hue */
background: hsl(220, 80%, 50%);
color: hsl(220, 60%, 85%); /* Harmonious and readable */
```

### Emphasize by De-emphasizing

If a primary element doesn't stand out, don't make it louder—make competing elements quieter.

```css
/* Instead of making active nav item bolder... */
/* ...make inactive items softer */
.nav-item { color: var(--slate-400); }
.nav-item.active { color: var(--slate-900); }
```

### Labels Are a Last Resort

Context often eliminates the need for labels:

| Instead of | Use |
|------------|-----|
| "Email: john@example.com" | john@example.com (format is obvious) |
| "In stock: 12" | "12 left in stock" |
| "Bedrooms: 3" | "3 bedrooms" |

When labels are necessary, de-emphasize them—the data is what matters.

### Balance Weight and Contrast

Heavy elements (icons, bold text) can be de-emphasized with softer colors. Light elements (thin borders) can be emphasized with increased weight.

```css
/* Icon feels too heavy? Reduce contrast */
.icon { color: var(--slate-400); } /* Instead of slate-900 */

/* Border too subtle? Increase width */
border: 2px solid hsl(210, 23%, 95%); /* Instead of 1px darker */
```

### Button Hierarchy

Design buttons based on hierarchy, not just semantics:

| Type | Style | Use for |
|------|-------|---------|
| **Primary** | Solid, high contrast | Main action on page |
| **Secondary** | Outline or lower contrast | Less important actions |
| **Tertiary** | Link style | Seldom-used actions |

**Destructive actions** aren't automatically red and bold. If "Delete" isn't the primary action, style it as secondary or tertiary, then use bold red styling in the confirmation modal.

---

## 3. Layout and Spacing

### Start with Too Much White Space

Begin with excessive space, then remove until satisfied. This ensures elements breathe properly.

### Establish a Spacing System

Use a constrained scale with meaningful jumps (~25% between values):

```
4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
```

**Base on 16px** (default browser font size, divides nicely).

### You Don't Have to Fill the Screen

If content only needs 600px, don't stretch it to 1200px. Extra space around edges never hurts.

### Shrink the Canvas

Designing for mobile first often reveals better solutions. Start with ~400px width, then expand.

### Grids Are Overrated

Not all elements should be fluid. Sidebars, icons, and avatars often work better with fixed sizes while main content flexes.

```css
/* Better than percentage-based sidebar */
.sidebar { width: 280px; flex-shrink: 0; }
.main { flex: 1; min-width: 0; }
```

### Relative Sizing Doesn't Scale

Headlines shouldn't stay proportional to body text across screen sizes. Large elements should shrink faster than small ones on mobile.

```css
/* Desktop: 45px headline, 18px body (2.5x ratio) */
/* Mobile: 24px headline, 14px body (1.7x ratio) */
```

### Avoid Ambiguous Spacing

When elements are grouped without visible separators, the spacing between groups must be greater than spacing within groups.

```css
/* Form labels should be closer to their inputs than to previous inputs */
.form-group { margin-bottom: 24px; }
.form-label { margin-bottom: 8px; }
```

---

## 4. Designing Text

### Establish a Type Scale

Hand-pick sizes rather than using mathematical ratios:

```
12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px, 48px, 60px, 72px
```

Use `px` or `rem`, not `em` (to avoid compounding issues with nesting).

### Use Good Fonts

**Safe choices:**
- System font stack for familiarity
- Fonts with 5+ weights indicate quality craftsmanship
- High x-height fonts for UI text (better legibility at small sizes)

**Filter by weight count** on Google Fonts to find quality options.

### Keep Line Length in Check

Optimal: **45-75 characters per line** (20-35em width).

```css
.prose { max-width: 65ch; } /* Character-based width */
```

### Baseline, Not Center

When mixing font sizes on one line, align by baseline, not vertical center.

```css
.header-row { align-items: baseline; } /* Not center */
```

### Line Height Is Proportional

| Font Size | Line Height |
|-----------|-------------|
| Small text (14px) | 1.5-1.75 |
| Body (16-18px) | 1.5-1.65 |
| Headlines (24px+) | 1.1-1.25 |
| Large headlines (36px+) | 1.0-1.1 |

Wider paragraphs need taller line heights.

### Not Every Link Needs a Color

In link-heavy interfaces, use subtle differentiation (font weight, darker color) instead of blue underlines everywhere. Reserve bold link styling for important navigation.

### Align with Readability in Mind

- **Left-align** most text
- **Center** only short, independent blocks (headings, CTAs)
- **Right-align** numbers in tables for easy comparison
- **Hyphenate** justified text

### Use Letter-Spacing Effectively

- **Tighten** headlines slightly: `letter-spacing: -0.02em;`
- **Widen** all-caps text: `letter-spacing: 0.05em;`
- Leave body text alone

---

## 5. Working with Color

### Ditch Hex for HSL

HSL (Hue, Saturation, Lightness) makes color relationships intuitive:

```css
/* HSL is easier to reason about */
--primary-500: hsl(220, 80%, 50%);
--primary-600: hsl(220, 80%, 40%); /* Just darken lightness */
--primary-400: hsl(220, 80%, 60%); /* Just lighten */
```

### You Need More Colors Than You Think

A complete palette includes:

| Category | Shades Needed |
|----------|---------------|
| **Greys** | 8-10 shades (true black looks unnatural) |
| **Primary** | 5-10 shades |
| **Accent colors** | 5-10 shades each (red, yellow, green, etc.) |

### Define Shades Up Front

Don't use `lighten()` or `darken()` functions. Pre-define all shades:

1. Pick your **base** color (good for button backgrounds)
2. Pick your **darkest** shade (for text on light backgrounds)
3. Pick your **lightest** shade (for tinted backgrounds)
4. Fill in 6-7 shades between them

### Don't Let Lightness Kill Saturation

As lightness approaches 0% or 100%, increase saturation to maintain vibrancy.

### Perceived Brightness Varies by Hue

Yellow appears brighter than blue at the same lightness. To make a color lighter without washing it out, rotate hue toward yellow, cyan, or magenta. To darken, rotate toward red, green, or blue.

### Greys Don't Have to Be Grey

Saturate greys slightly for personality:
- **Cool greys**: Add blue (hue ~210)
- **Warm greys**: Add yellow/orange (hue ~40)

```css
--grey-500: hsl(210, 10%, 50%); /* Cool grey */
--grey-500-warm: hsl(40, 10%, 50%); /* Warm grey */
```

### Accessible Contrast

| Text Type | Minimum Ratio |
|-----------|---------------|
| Body text (<18px) | 4.5:1 |
| Large text (18px+ bold or 24px+) | 3:1 |

**Flip the contrast** when colored backgrounds make white text too dark—use dark colored text on light colored backgrounds instead.

### Don't Rely on Color Alone

Always pair color with another indicator (icons, patterns, text) for colorblind users.

### System Colors for Status

Use traffic light colors with familiar meanings:

| Color | Usage | When to Use |
|-------|-------|-------------|
| **Red** | Error | Negative messages, failures requiring attention |
| **Amber** | Warning | Caution, potentially risky actions |
| **Green** | Success | Positive messages, completed actions |

Always pair with icons for color blind accessibility.

### APCA: The Future of Contrast Measurement

WCAG 3 introduces the **Accessible Perceptual Contrast Algorithm (APCA)**—a more accurate contrast measurement:

| APCA Value | Use For |
|------------|---------|
| ≥90 | Preferred for body text (14px+) |
| ≥75 | Minimum for body text (18px+) |
| ≥60 | Other text (24px or 16px bold+) |
| ≥45 | Large text (36px or 24px bold+), UI elements |
| ≥30 | Placeholder text, disabled buttons |
| ≥15 | Non-text decorative elements |

**Key difference:** APCA handles dark backgrounds better than WCAG 2, and swapping text/background colors affects the score.

### Transparent Colors for Flexibility

Use transparent colors (with alpha values) for:

- Hover states that work on any background
- Overlays that adapt to underlying content
- Subtle backgrounds that maintain harmony

```css
/* Transparent overlays that work on any background */
--hover-overlay: hsla(0, 0%, 0%, 0.05);
--active-overlay: hsla(0, 0%, 0%, 0.1);
--disabled-overlay: hsla(0, 0%, 100%, 0.5);
```

---

## 6. Creating Depth

### Emulate a Light Source

Light comes from above. Apply this consistently:

- **Raised elements**: Lighter top edge, shadow below
- **Inset elements**: Shadow at top, lighter bottom edge

```css
/* Raised button */
.button {
  box-shadow: 
    inset 0 1px 0 hsl(220, 80%, 70%), /* Light top edge */
    0 1px 3px hsla(0, 0%, 0%, 0.2);    /* Shadow below */
}

/* Inset input */
.input {
  box-shadow: inset 0 2px 4px hsla(0, 0%, 0%, 0.1);
}
```

### Use Shadows to Convey Elevation

| Elevation | Shadow | Use for |
|-----------|--------|---------|
| Low | `0 1px 3px rgba(0,0,0,0.12)` | Buttons, cards |
| Medium | `0 4px 6px rgba(0,0,0,0.1)` | Dropdowns, popovers |
| High | `0 15px 35px rgba(0,0,0,0.15)` | Modals, dialogs |

Define 5 shadow levels and stick to them.

### Shadows Can Have Two Parts

Combine a large soft shadow (direct light) with a small tight shadow (ambient occlusion):

```css
box-shadow: 
  0 4px 6px rgba(0, 0, 0, 0.07),   /* Large, soft */
  0 1px 3px rgba(0, 0, 0, 0.1);    /* Small, tight */
```

The tight shadow fades at higher elevations.

### Flat Designs Can Have Depth

Without shadows:
- Use **lighter colors** for raised elements
- Use **darker colors** for inset elements
- Use **solid offset shadows** (no blur) for flat aesthetic with depth

### Overlap Elements to Create Layers

Let cards cross background boundaries. Overlap images with invisible borders to prevent clashing.

---

## 7. Working with Images

### Use Good Photos

Bad photos ruin designs. Hire professionals or use quality stock (Unsplash, etc.). Don't use smartphone placeholders.

### Text on Images Needs Consistent Contrast

When placing text over images:

1. **Add overlay**: Semi-transparent black (for light text) or white (for dark text)
2. **Lower contrast**: Reduce image contrast, adjust brightness
3. **Colorize**: Desaturate + multiply blend with brand color
4. **Text shadow**: Large blur radius, no offset (glow effect)

### Everything Has an Intended Size

- **Don't scale up icons** designed for 16-24px—they look chunky
- **Don't scale down screenshots**—details become illegible
- **Redraw logos** for small sizes (favicons)

Wrap small icons in colored shapes to fill larger spaces:

```html
<div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
  <svg class="w-6 h-6 text-blue-600"><!-- Icon --></svg>
</div>
```

### User-Uploaded Content

- Force consistent aspect ratios with `object-fit: cover`
- Prevent background bleed with subtle inner shadows
- Control dimensions with fixed containers

```css
.user-image {
  object-fit: cover;
  aspect-ratio: 16/9;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);
}
```

---

## 8. Copywriting for UI

Clear interface text is as important as visual design. Poor copy creates confusion and increases cognitive load.

### Be Concise

Remove unnecessary words. Every word should earn its place.

| Verbose | Concise |
|---------|---------|
| "Click here to submit your form" | "Submit" |
| "In order to continue, please..." | "To continue..." |
| "Are you sure you want to delete?" | "Delete this item?" |

### Use Sentence Case

Sentence case is easier to read than Title Case or ALL CAPS:

- **Good:** "Create new account"
- **Avoid:** "Create New Account"
- **Never:** "CREATE NEW ACCOUNT"

### Front-Load Text

Put the most important information first. Users scan—don't bury key info.

| Back-loaded | Front-loaded |
|-------------|--------------|
| "To reset your password, click here" | "Reset password" |
| "If you need help, contact support" | "Contact support for help" |

### Use Plain Language

Write at an 8th-grade reading level. Avoid jargon and technical terms.

| Complex | Simple |
|---------|--------|
| "Authenticate your credentials" | "Sign in" |
| "Terminate session" | "Log out" |
| "Insufficient permissions" | "You don't have access" |

### Write Clear Error Messages

Good error messages:

1. **Explain what happened** (not just "Error")
2. **Suggest how to fix it** (actionable guidance)
3. **Use human language** (not error codes)

| Bad | Good |
|-----|------|
| "Error 403" | "You don't have permission to view this page" |
| "Invalid input" | "Please enter a valid email address" |
| "Request failed" | "Couldn't save changes. Check your connection and try again" |

### Consistent Vocabulary

Use the same words for the same concepts throughout:

- Pick "Sign in" or "Log in"—not both
- Pick "Settings" or "Preferences"—not both
- Pick "Delete" or "Remove"—not both

### Button Labels

Use action verbs that describe what happens:

| Vague | Specific |
|-------|----------|
| "OK" | "Save changes" |
| "Submit" | "Create account" |
| "Yes" | "Delete message" |

---

## 9. Forms and Buttons

### Button Weights

Define three distinct button styles based on importance:

| Weight | Style | Use For |
|--------|-------|---------|
| **Primary** | Solid, high contrast, brand color | Main action (one per screen) |
| **Secondary** | Outline or muted fill | Alternative actions |
| **Tertiary** | Text-only, link style | Least important actions |

### Form Field Best Practices

1. **Use conventional styles**—don't reinvent form fields
2. **Visible borders**—minimum 3:1 contrast ratio
3. **Clear focus states**—visible keyboard focus indicators
4. **Inline validation**—show errors as users type, not only on submit
5. **Helpful placeholders**—example input, not labels

### Form Layout

- **One column** for most forms (faster to complete)
- **Group related fields** with clear visual separation
- **Labels above inputs** (faster scanning than left-aligned labels)
- **Required field indicators**—mark optional fields, not required ones

### Avoid Disabled Buttons

Disabled buttons create confusion. Instead:

- Hide buttons until they're usable
- Show buttons but explain why action isn't available
- Use inline validation to guide users

```css
/* If you must use disabled buttons */
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

---

## 10. Finishing Touches

### Supercharge the Defaults

| Default | Upgrade |
|---------|---------|
| Bullet points | Custom icons (checkmarks, locks, stars) |
| Quote marks | Large, colored quote symbols |
| Links | Bold, custom underline overlapping text |
| Checkboxes | Brand-colored custom controls |

### Add Color with Accent Borders

A 4px colored border adds polish without design skills:

```css
/* Top of cards */
.card { border-top: 4px solid var(--primary-500); }

/* Side of alerts */
.alert { border-left: 4px solid var(--warning-500); }

/* Under headlines */
.headline::after { 
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: var(--primary-500);
  margin-top: 12px;
}
```

### Decorate Backgrounds

Break monotony with:
- Subtle background color changes between sections
- Gradients (keep hues within 30° of each other)
- Low-contrast repeating patterns
- Simple geometric shapes or illustrations

### Don't Overlook Empty States

Empty states are first impressions. Include:
- Illustrations or icons
- Clear call-to-action
- Hide filters/tabs until content exists

### Use Fewer Borders

Instead of borders for separation:

| Alternative | When to Use |
|-------------|-------------|
| Box shadows | Outline elements on same-color backgrounds |
| Different background colors | Adjacent sections |
| Extra spacing | Group separation |

### Think Outside the Box

Challenge assumptions about component design:
- Dropdowns can have multiple columns, icons, and descriptions
- Tables can combine columns and add hierarchy
- Radio buttons can be selectable cards
- Forms can use creative layouts

---

## 11. Leveling Up

### Look for Decisions You Wouldn't Have Made

Study designs you admire. Notice unconventional choices:
- Inverted datepicker colors
- Buttons inside inputs
- Two-color headlines

### Rebuild Favorite Interfaces

Recreate designs from scratch without inspecting code. Discovering why your version differs teaches lasting lessons.

---

## Quick Reference: System Recommendations

### Spacing Scale

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
--space-12: 48px;
--space-16: 64px;
--space-24: 96px;
--space-32: 128px;
```

### Type Scale

```css
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
--text-4xl: 36px;
--text-5xl: 48px;
--text-6xl: 60px;
```

### Shadow Scale

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
--shadow-xl: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-2xl: 0 20px 25px rgba(0, 0, 0, 0.15), 0 10px 10px rgba(0, 0, 0, 0.04);
```

### Border Radius Scale

```css
--radius-sm: 2px;
--radius-md: 4px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-2xl: 16px;
--radius-full: 9999px;
```

### Interaction States

Every interactive element needs clear state feedback:

```css
/* Button states example */
.button {
  background: var(--primary-500);
  transition: all 0.15s ease;
}
.button:hover {
  background: var(--primary-600);
}
.button:active {
  background: var(--primary-700);
  transform: translateY(1px);
}
.button:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### WCAG 2.1 AA Checklist

| Requirement | Target |
|-------------|--------|
| Text contrast (small) | 4.5:1 minimum |
| Text contrast (large) | 3:1 minimum |
| UI component contrast | 3:1 minimum |
| Focus indicators | Visible, 3:1 contrast |
| Touch targets | 44×44px minimum |
| Color independence | Never color alone |
| Text resize | Works at 200% zoom |

---

*For deeper learning, study the source materials: [Refactoring UI](https://www.refactoringui.com/) and [Practical UI](https://www.practical-ui.com/)*
