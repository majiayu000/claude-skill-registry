---
name: algorithmic-color-palette
description: Derive a full UI colour palette algorithmically from one or two brand colours. Darker and lighter variants for interactive states, desaturated greys from the brand hue for borders and backgrounds, and semantic colours that feel coherent with the brand rather than generic. Use when building a colour system from scratch or expanding a limited brand palette for UI use.
metadata:
  priority: 8
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/tokens/**"
    - "**/theme/**"
    - "tailwind.config.*"
    - "design-system/**"
  promptSignals:
    phrases:
      - "colour palette"
      - "color palette"
      - "brand colours"
      - "derive colours"
      - "colour tokens"
      - "hover colour"
      - "shade"
      - "tint"
      - "colour system"
  retrieval:
    aliases:
      - colour system
      - algorithmic colours
      - brand colour palette
      - derive shades
      - colour tokens
    intents:
      - generate a colour palette from brand colours
      - derive hover and active colours
      - create grey palette from brand
      - build a full colour system
      - extend a limited brand palette
    examples:
      - generate a full colour palette from this brand blue
      - what colour should the hover state be
      - create a grey palette that fits this brand
      - derive semantic colours from the brand primary
---

# Algorithmic Colour Palette

A brand palette of 2–3 colours is not enough for a UI. You need shades for states (hover, active, disabled), neutrals for backgrounds and borders, and semantic colours for status. Deriving these algorithmically from the brand colours produces a palette that feels coherent — everything is visually related to the brand rather than pulled from a generic grey or a stock colour library.

## Deriving Interactive State Colours

From each brand colour, generate at minimum three variants: base, darker (hover/active), lighter (tint/background).

### Method: HSL adjustment

```
base:    hsl(H, S%, L%)
hover:   hsl(H, S%, L% - 8%)     ← darken by reducing lightness
active:  hsl(H, S%, L% - 14%)    ← darken further
tint:    hsl(H, S%, L% + 40%)    ← lighten significantly for backgrounds
subtle:  hsl(H, S% * 0.3, L% + 45%)  ← heavily desaturated, near-white
```

### Example: brand primary `#133174` (hsl 224, 70%, 27%)

```css
--color-primary-subtle:  hsl(224, 21%, 94%);  /* background tint */
--color-primary-tint:    hsl(224, 70%, 67%);  /* light variant */
--color-primary:         hsl(224, 70%, 27%);  /* base */
--color-primary-hover:   hsl(224, 70%, 19%);  /* hover: -8% lightness */
--color-primary-active:  hsl(224, 70%, 13%);  /* active: -14% lightness */
```

### Example: success green derived from a teal brand colour

If the brand has a green or teal, shift it toward a clearer success green:

```css
--color-success-subtle:  hsl(142, 20%, 94%);
--color-success:         hsl(142, 60%, 35%);
--color-success-hover:   hsl(142, 60%, 27%);
```

## Deriving Brand-Tinted Greys

Generic greys (`#666`, `#999`, `#eee`) feel disconnected from the brand. Desaturating the brand hue produces greys that are subtly tinted — warm, cool, or neutral depending on the brand — and feel like they belong to the same palette.

### Optical Comfort: Avoiding Pure Black on White
Extreme contrast (pure black `#000000` on pure white `#FFFFFF`) can cause "halation" and eye strain. To create a more comfortable reading experience:
- **Use "Near-Black" for text:** Use a very dark grey (e.g., `#222222` or your `grey-900` token) instead of pure black.
- **Use "Off-White" for backgrounds:** A slightly muted white (e.g., `#EEEEEE` or your `grey-50` token) is softer on the eyes than pure `#FFFFFF`.

This "softened contrast" remains highly accessible (passing WCAG AA/AAA) but feels more professional and less harsh.

### Method: desaturate + adjust lightness

```
brand hue H
grey-900: hsl(H, 12%, 10%)   ← near-black, text
grey-700: hsl(H, 10%, 30%)   ← dark text, icons
grey-500: hsl(H,  8%, 50%)   ← secondary text, placeholders
grey-300: hsl(H,  6%, 70%)   ← disabled text, subtle labels
grey-200: hsl(H,  5%, 82%)   ← borders, dividers
grey-100: hsl(H,  4%, 92%)   ← input backgrounds, table stripes
grey-50:  hsl(H,  3%, 96%)   ← page background, subtle fills
```

### Example: brand primary `#133174` (H = 224, blue-tinted)

```css
--color-grey-900: hsl(224, 12%, 10%);  /* #16171f — slightly blue-black */
--color-grey-500: hsl(224,  8%, 50%);  /* #7b7e8a — cool grey */
--color-grey-200: hsl(224,  5%, 82%);  /* #cfd0d5 — cool light border */
--color-grey-50:  hsl(224,  3%, 96%);  /* #f4f4f6 — near-white with a hint of blue */
```

Compare to generic `#f5f5f5` (no hue) — the brand-tinted version is subtly different but feels intentional.

## Semantic Colour Derivation

Status colours (error, warning, success, info) should feel harmonious with the brand. To achieve cohesion, align their **Saturation** and **Lightness** to create a consistent "visual weight" across the status set.

### Method: Aligned visual weight

1. **Pick the Hues:** Use standard semantic hues (0 for Error, 38 for Warning, 142 for Success).
2. **Align S & L:** Use the saturation and lightness of your Brand Primary as a starting point.
3. **Adjust for Perceived Brightness:** Hues like Yellow/Orange (Warning) feel brighter than Blue/Red. Reduce the lightness of Warning by 5–10% compared to Success or Error to ensure they feel equally "heavy" on the page.

| Semantic | Hue (H) | Saturation (S) | Lightness (L) |
|---|---|---|---|
| **Error** | 0–10 | Match Primary | Match Primary |
| **Warning** | 35–45 | Match Primary | Primary L - 10% |
| **Success** | 140–160 | Match Primary | Match Primary |
| **Info** | 210–230 | Match Primary | Match Primary |

**The "Vibrancy" Rule:** If the brand is muted (low saturation), the semantic colours should also be slightly muted. If the brand is neon/vibrant, the semantics should follow suit. Cohesion comes from shared intensity.

## Functional and Interactive Colours

Standard UI elements require dedicated functional tokens beyond basic brand and semantic colours.

### Focus States
Focus indicators are critical for accessibility. Use a high-visibility colour that works on all backgrounds.
- **Default:** Brand Primary (if contrast is high enough).
- **Fallback:** A dedicated high-contrast blue `hsl(215, 95%, 50%)`.
- **Token:** `--color-focus`.

### Selection and Highlights
Text selection and list item highlights should be subtle and non-distracting.
- **Method:** Use the primary hue with very high lightness (90%+) and moderate saturation.
- **Token:** `--color-selection`.

### Overlays and Modals
Backdrops for modals or drawers need a neutral, semi-transparent colour.
- **Method:** Use your `grey-900` hue with an alpha channel.
- **Token:** `--color-overlay: hsla(H, 12%, 10%, 0.5);`

### Skeleton and Loading
Loading states should be neutral and recessive.
- **Method:** Use `grey-200` as the base and `grey-100` as the shimmer highlight.
- **Token:** `--color-skeleton`.

### Disabled States
Disabled elements must communicate unreachability.
- **Method:** Use `grey-500` for text and `grey-200` for backgrounds/borders.
- **Rule:** Avoid using brand tints for disabled backgrounds to prevent "pseudo-active" confusion.

### Brand-Tinted Shadows
Premium UIs avoid pure black shadows. Use a very dark, desaturated brand hue.
- **Method:** `hsla(H, 15%, 5%, alpha)` where H is the brand hue.
- **Token:** `--color-shadow-base`.

### Links
- **Base:** Brand Primary or a dedicated high-visibility blue.
- **Visited:** Shift primary hue toward purple (+20) and reduce saturation.
- **Token:** `--color-link`, `--color-link-visited`.

### Input and Validation
- **Method:** Use semantic base colours for borders and text in error/success states.
- **Inactive Border:** `grey-200`.
- **Active/Focus Border:** Brand Primary.

## Full Token Output Example

```css
:root {
  /* Primary — derived from brand #133174 */
  --color-primary-subtle:  hsl(224, 21%, 94%);
  --color-primary-tint:    hsl(224, 70%, 67%);
  --color-primary:         hsl(224, 70%, 27%);
  --color-primary-hover:   hsl(224, 70%, 19%);
  --color-primary-active:  hsl(224, 70%, 13%);

  /* Brand-tinted neutrals */
  --color-grey-900: hsl(224, 12%, 10%);
  --color-grey-700: hsl(224, 10%, 30%);
  --color-grey-500: hsl(224,  8%, 50%);
  --color-grey-300: hsl(224,  6%, 70%);
  --color-grey-200: hsl(224,  5%, 82%);
  --color-grey-100: hsl(224,  4%, 92%);
  --color-grey-50:  hsl(224,  3%, 96%);

  /* Semantic */
  --color-error:   hsl(4,  72%, 44%);
  --color-warning: hsl(38, 80%, 44%);
  --color-success: hsl(142, 58%, 35%);
  --color-info:    hsl(224, 70%, 27%); /* = primary */

  /* Semantic subtle backgrounds */
  --color-error-subtle:   hsl(4,  50%, 95%);
  --color-warning-subtle: hsl(38, 60%, 95%);
  --color-success-subtle: hsl(142, 40%, 95%);

  /* Functional */
  --color-focus:     var(--color-primary);
  --color-selection: hsl(224, 70%, 90%);
  --color-overlay:   hsla(224, 12%, 10%, 0.5);
  --color-skeleton:  var(--color-grey-200);
  --color-shadow:    hsla(224, 15%, 5%, 0.1);

  /* Links */
  --color-link:         var(--color-primary);
  --color-link-visited: hsl(244, 40%, 35%);
}
```

## Review Checklist

- [ ] Are hover and active colours derived from the base by lightness adjustment, not chosen independently?
- [ ] Are neutral greys tinted with the brand hue rather than using generic `#666` / `#eee`?
- [ ] Is saturation reduced progressively as lightness increases in the grey scale?
- [ ] Is pure black (#000000) on pure white (#FFFFFF) avoided in favor of near-blacks (e.g., #222) and off-whites (e.g., #EEE)?
- [ ] Are status colours (Success, Warning, Error) visually weighted to match the brand primary?
- [ ] If the brand primary is orange or amber, is warning colour clearly distinct from it?
- [ ] Does each brand colour have at minimum: subtle, base, hover, active variants?
- [ ] Are semantic colours aligned in Saturation and Lightness to create a cohesive visual weight?
- [ ] Is there a dedicated `--color-focus` token that meets accessibility contrast requirements?
- [ ] Are selection, overlay, and shadow colours derived from the brand hue rather than generic black/grey?
- [ ] Are disabled states neutral (greys) to avoid confusion with interactive brand colours?
- [ ] Does the link colour have a distinct `visited` state derived algorithmically?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| **Pure black on pure white** | High visual strain, "halation" | Use near-black (#222) and off-white (#EEE) |
| **Grey borders next to colourful areas** | Looks cheap and disconnected | Remove border or use a tinted/darker version of the adjacent colour |
| **Randomly picked "Warning/Error" colours** | Palette feels uncoordinated | Derive from brand HSL with visual weight alignment |
| **Generic grey palette (#666, #999)** | Lacks brand identity | Tint neutrals with a low-saturation version of the brand hue |
