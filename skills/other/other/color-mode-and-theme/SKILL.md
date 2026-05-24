---
name: color-mode-and-theme
description: Choose light, dark, or combined color mode deliberately based on brand tone and user context. Offer a theme selector only when user control genuinely matters — enterprise tools, data-heavy UIs, or extended-use applications. Use when defining the base color palette, designing a design system, or deciding whether to build dark mode support.
metadata:
  priority: 7
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/tokens/**"
    - "**/theme/**"
    - "tailwind.config.*"
    - "design-system/**"
  promptSignals:
    phrases:
      - "dark mode"
      - "light mode"
      - "theme"
      - "color mode"
      - "dark design"
      - "white design"
      - "theme selector"
      - "brand tone"
retrieval:
  aliases:
    - dark mode
    - light mode
    - theme selector
    - color scheme
    - brand tone
    - white design
    - dark design
  intents:
    - choose between dark and light mode
    - decide if dark mode is needed
    - build a theme selector
    - match brand tone in color palette
    - design for enterprise tools
  examples:
    - should this app be dark or light
    - when should I add a theme toggle
    - design a dark mode for this dashboard
    - this is a trading platform, what color mode fits
---

# Color Mode and Theme

## The Decision: Light, Dark, or Both

Color mode is a brand and context decision, not a personal preference. Make it deliberately.

### Light (white design)
**Tone:** Open, trustworthy, content-forward, accessible, professional  
**Fits:** Marketing sites, e-commerce, editorial, SaaS with mixed audiences, consumer products, B2B tools where the content is the focus

Light mode is the safer default for most products. It performs better in bright environments and has broader accessibility coverage out of the box.

### Dark (dark design)
**Tone:** Premium, focused, immersive, technical, high-contrast data  
**Fits:** Trading platforms, developer tools, creative tools (video/audio editors), data dashboards with dense visualisations, entertainment, gaming

Dark mode reduces eye strain during extended use in low-light environments. It also makes colourful data visualisations (charts, heatmaps) pop more clearly against a dark surface.

**Caution:** Dark mode is harder to get right. Low-contrast text, over-saturated brand colours, and insufficient surface differentiation are common failures. If the team cannot maintain it properly, light mode is better than a broken dark mode.

### Combined (system-default + manual override)
Respect `prefers-color-scheme` and let the OS set the default. Offer a toggle for users who want to override. This is the modern standard for most products with a returning user base.

```css
@media (prefers-color-scheme: dark) {
  :root { /* dark tokens */ }
}
@media (prefers-color-scheme: light) {
  :root { /* light tokens */ }
}
[data-theme="dark"] { /* manual override */ }
[data-theme="light"] { /* manual override */ }
```

---

## When to Build a Theme Selector in the UI

A theme selector is a UI control — it takes space and adds complexity. Only build it when user control genuinely matters.

| Situation | Theme selector? |
|---|---|
| Marketing site, landing page | No — pick one mode, commit to it |
| Consumer SaaS, general audience | Combined (system-default + toggle) |
| Developer tool, technical product | Yes — developers expect it |
| Trading platform, financial dashboard | Yes — extended use, low-light sessions common |
| B2B enterprise tool (ERP, analytics) | Yes — power users, long sessions, personal preference varies |
| E-commerce storefront | Usually no — light default, possibly system-default |
| Creative tool (design, video, audio) | Yes — dark is often preferred, toggle still expected |

**Rule:** if the user will spend hours per day in the tool, give them control. If it's a transactional or occasional-use product, pick the mode that fits the brand and move on.

Place the theme toggle in the header (top-right, near account) or in user settings — not in primary navigation.

---

## Brand Tone and Color Mode

The brand's existing visual identity should inform the default mode.

| Brand tone | Default mode |
|---|---|
| Clean, minimal, trustworthy, open | Light |
| Premium, exclusive, bold, immersive | Dark |
| Technical, data-heavy, precise | Dark |
| Playful, colourful, energetic | Light (dark mode harder to maintain with vivid brand colours) |
| Neutral, enterprise, functional | Light, with system-default toggle |

If the brand uses a very dark primary colour (navy, deep green, near-black), a dark mode surfaces it naturally. If the brand is built around a bright, vivid primary, light mode lets it breathe.

---

## Dark Mode Token Principles

Dark mode is not just inverting colours. Common mistakes:

- **Do not use pure black (#000000) as the base surface** — use a very dark neutral (#0A0A0F, #111827) for depth
- **Surface hierarchy in dark mode uses lightness, not shadows** — base, +1, +2 surfaces get progressively lighter, not more shadowed
- **Reduce brand colour saturation slightly** — vivid colours on dark backgrounds can be visually aggressive; a 10–15% desaturation keeps them readable
- **Increase font weight for reversed text** — light text on a dark background often appears "thinner" than the same weight in light mode. Increase the weight by one step (e.g., from Regular to Medium, or Medium to Semibold) to maintain legibility.
- **Text contrast needs active verification** — light text on dark surfaces is not automatically WCAG-compliant; check all combinations

```css
/* Dark mode surface scale */
--color-surface:         #0A0A0F;  /* base */
--color-surface-raised:  #141419;  /* cards */
--color-surface-overlay: #1E1E26;  /* modals, popovers */
--color-border:          rgba(255,255,255,0.08);
--color-text:            #F0F0F5;
--color-text-secondary:  #8A8F98;
```

---

## Review Checklist

- [ ] Is the color mode choice deliberate and based on brand tone and use context?
- [ ] If combined mode: does `prefers-color-scheme` set the default?
- [ ] If a theme selector is built: is it placed in a low-profile but accessible location?
- [ ] In dark mode: are surfaces differentiated by lightness steps, not just shadows?
- [ ] In dark mode: is brand colour slightly desaturated to avoid visual aggression?
- [ ] Are all text/background contrast ratios verified in both modes (WCAG 2.2 AA)?
- [ ] Is font weight increased by one step for reversed text (light-on-dark) to maintain optical legibility?
- [ ] Is pure black (#000000) avoided as a dark mode base surface?
