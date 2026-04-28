---
name: frontend-design
description: Use when user asks to build a web component, page, or application, or when the task involves frontend design, HTML/CSS generation, or UI layout. Applies specific rules for typography, OKLCH color, layout, motion, interaction, and UX writing to produce distinctive, production-grade interfaces that avoid generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design without project context produces generic output. Before designing anything:

1. **Check for existing context**: If your loaded instructions contain a **Design Context** section, use it.
2. **Ask if missing**: You need at minimum — *target audience*, *use cases*, *brand personality/tone*. Code tells you what was built, not who it's for or what it should feel like. Ask before generating.

## The AI Slop Test

Before shipping: "If someone saw this and said 'AI made this,' would they believe it immediately?"

If yes — fix it. The fingerprints of AI-generated work from 2024–2025:
- Inter font, Roboto, Open Sans, Arial, or system defaults
- Purple-to-blue gradients; cyan-on-dark; neon accents on dark backgrounds
- Gray text on colored backgrounds
- Glassmorphism used decoratively (blur cards, glow borders)
- Pure black (#000) or pure white (#fff) anywhere
- Everything wrapped in cards; cards nested inside cards; identical card grids
- Everything centered; same spacing everywhere
- Hero metric layout (big number, small label, supporting stats, gradient accent)
- Dark mode as the default aesthetic (looks cool without requiring actual design decisions)
- Gradient text for "impact" — decorative, not meaningful
- Large rounded icons above every heading
- Bounce / elastic easing
- Sparklines as decoration
- Rounded rectangles with generic drop shadows
- `ease` as the default easing function

A distinctive interface makes someone ask "how was this made?" not "which AI made this?"

## Design Direction

Commit to a **bold, specific aesthetic direction** before touching code:
- **Tone**: Pick an extreme — brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. There are endless flavors. Design one true to the context, not a safe middle ground.
- **Differentiation**: What's the one thing someone will remember?

Bold maximalism and refined minimalism both work. The key is intentionality, not intensity.

---

## Typography

**Font selection — avoid the invisible defaults:**

| Instead of | Use |
|-----------|-----|
| Inter | Instrument Sans, Plus Jakarta Sans, Outfit |
| Roboto | Onest, Figtree, Urbanist |
| Open Sans | Source Sans 3, DM Sans |
| Anything generic | Fraunces / Newsreader / Lora (editorial/premium) |
| Any above | `-apple-system, BlinkMacSystemFont, system-ui` (native feel, zero cost) |

You often don't need a second font. One family in multiple weights creates cleaner hierarchy than two competing typefaces. When pairing, contrast on multiple axes: serif + sans, geometric + humanist, condensed display + wide body. Never pair two fonts that are similar but not identical.

**Modular scale**: Use fewer sizes with more contrast. A 5-step system covers everything: xs (0.75rem) / sm (0.875rem) / base (1rem) / lg (1.25–1.5rem) / xl+ (2–4rem). Common ratios: 1.25, 1.333, 1.5. Pick one and commit.

**Fluid type**: Use `clamp(min, preferred, max)`. Don't use on button text, labels, or UI elements.

**Line-height is the base unit** for ALL vertical spacing. If body text is 16px at 1.5 line-height = 24px, spacing values should be multiples of 24px. Creates subconscious mathematical harmony.

**Readable measure**: `max-width: 65ch` on paragraphs. Light text on dark: add 0.05–0.1 to line-height.

**OpenType features** (most devs forget these):
```css
.data-table { font-variant-numeric: tabular-nums; }    /* aligned numbers */
abbr { font-variant-caps: all-small-caps; }
code { font-variant-ligatures: none; }
```

**Prevent font layout shift** — define fallback font metrics:
```css
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
}
body { font-family: 'CustomFont', 'CustomFont-Fallback', sans-serif; }
```

**Rules**: Never px for body text (use rem/em). Never disable zoom. Minimum 16px body. 44px+ touch targets for text links.

---

## Color

**Use OKLCH, not HSL.** HSL is not perceptually uniform — 50% lightness in yellow looks bright, in blue looks dark. OKLCH equal steps look equal.

```css
--color-primary: oklch(60% 0.15 250);
--color-primary-light: oklch(85% 0.08 250);  /* reduce chroma at extremes */
--color-primary-dark: oklch(35% 0.12 250);
```

**Always tint neutrals toward brand hue** — pure gray doesn't exist in nature:
```css
--gray-100: oklch(95% 0.01 250);  /* chroma 0.01 — tiny but creates cohesion */
--gray-900: oklch(15% 0.01 250);
```

**Palette structure**: Primary (1 color, 3–5 shades) + Neutral (9–11 shades) + Semantic (success/error/warning/info) + Surface (2–3 elevation levels). Skip secondary/tertiary unless genuinely needed.

**60-30-10 rule**: 60% neutral backgrounds / 30% secondary (text, borders, inactive states) / 10% accent (CTAs, focus states). Accent colors work *because* they're rare. Overuse kills the power.

**Contrast minimums**: Body text 4.5:1 (AA). Large text (18px+) 3:1. UI components 3:1. Placeholder text still needs 4.5:1 — that common light gray placeholder almost always fails.

**Gray on color always fails** — never use gray text on a colored background. Use a darker shade of the background color instead.

**Dark mode is NOT inverted light mode:**
```css
:root[data-theme="dark"] {
  --surface-1: oklch(15% 0.01 250);
  --surface-2: oklch(20% 0.01 250);  /* lighter surface = higher elevation */
  --surface-3: oklch(25% 0.01 250);
  --body-weight: 350;  /* perceived weight is lighter on dark — reduce slightly */
}
```
No pure black backgrounds (use oklch 12–18%). No shadows for elevation — use lighter surface colors. Desaturate accents slightly. Never `#000` or `#fff` anywhere.

**Token hierarchy**: Primitive (`--blue-500`) + semantic (`--color-primary: var(--blue-500)`). Dark mode only redefines the semantic layer.

**Heavy use of alpha (rgba) is a design smell** — usually means an incomplete palette. Define explicit colors per context instead.

---

## Layout & Space

**4pt base spacing** (4, 8, 12, 16, 24, 32, 48, 64, 96px) — 8pt is too coarse. Name tokens by relationship: `--space-sm`, `--space-lg` (not `--spacing-8`). Use `gap` instead of margins for siblings.

**The Squint Test**: Blur your eyes. Can you identify the most important element? Second most? Clear groupings? If everything looks the same weight blurred — hierarchy problem.

**Hierarchy uses multiple dimensions simultaneously**:

| Dimension | Strong | Weak |
|-----------|--------|------|
| Size | 3:1+ ratio | <2:1 |
| Weight | Bold vs Regular | Medium vs Regular |
| Color | High contrast | Similar tones |
| Position | Top/left | Bottom/right |
| Space | Surrounded by whitespace | Crowded |

A heading that's larger AND bolder AND has more space above it is strong hierarchy. One dimension alone is weak.

**Cards are not required.** Spacing + alignment create visual grouping naturally. Use cards only when content needs explicit comparison, discrete actionability, or clear interaction boundaries. Never nest cards inside cards — use spacing, typography, and subtle dividers for within-card hierarchy.

**Asymmetry feels designed** — left-aligned text with asymmetric layouts beats everything centered. Create visual rhythm through varied spacing (tight groupings, generous separations), not the same padding everywhere. Break the grid intentionally for emphasis.

**Container queries for components, not viewport queries:**
```css
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { grid-template-columns: 120px 1fr; }
}
```

A card in a narrow sidebar stays compact; in main content it expands — automatically, without viewport hacks.

**Self-adjusting grid** (no breakpoints needed):
```css
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
```

**Touch targets** — visual size ≠ tap target (44px minimum):
```css
.icon-button { width: 24px; height: 24px; position: relative; }
.icon-button::before { content: ''; position: absolute; inset: -10px; }
```

**Optical alignment**: Text at `margin-left: 0` looks slightly indented — use `margin-left: -0.05em` to optically align.

---

## Motion

**Duration rule (100 / 300 / 500)**:

| Duration | Use |
|----------|-----|
| 100–150ms | Button press, toggle, color change |
| 200–300ms | Menu open, tooltip, hover state |
| 300–500ms | Accordion, modal, drawer |
| 500–800ms | Page load, hero reveals |

Exit animations at ~75% of enter duration.

**Easing — never use the `ease` keyword** (it's a compromise):
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* elements entering */
--ease-in: cubic-bezier(0.7, 0, 0.84, 0);        /* elements leaving */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);   /* state toggles */

/* Default for micro-interactions — natural deceleration */
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
```

**Only animate `transform` and `opacity`** — everything else causes layout recalculation.

For height animations: `grid-template-rows: 0fr → 1fr` instead of animating `height`.

**Perceived performance**: Our brains buffer ~80ms of sensory input — anything under feels instant. Optimistic UI (update immediately, sync later) applies for low-stakes actions (likes, follows). Never for payments or destructive operations.

**Reduced motion is not optional** — 35% of adults 40+ have vestibular disorders:
```css
@media (prefers-reduced-motion: reduce) {
  .card { animation: fade-in 200ms ease-out; }  /* crossfade, not motion */
}
```

---

## Interaction Design

**Every interactive element needs all 8 states**: Default, Hover, Focus, Active, Disabled, Loading, Error, Success. Common miss: designing hover without focus. Keyboard users never see hover states.

**Focus rings — never `outline: none` without replacement:**
```css
button:focus { outline: none; }
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

**Loading**: Skeleton screens beat spinners — they preview content shape and feel faster. Optimistic updates for low-stakes actions. Specific copy: "Saving your draft..." not "Loading..."

**Modals**: Use native `<dialog>` (automatic focus trap + Escape). Use them sparingly — modals are almost always the lazy choice. The `popover` API handles tooltips/dropdowns/non-modal overlays without z-index wars.

**Destructive actions**: Undo > confirmation dialogs. Users click through confirmations mindlessly. Remove → show undo toast → delete after toast expires.

**Forms**: Placeholders are not labels. Validate on blur, not every keystroke. Errors below fields with `aria-describedby`.

---

## Responsive Design

**Mobile-first**: Start with mobile base styles, layer with `min-width` queries. Desktop-first (`max-width`) makes mobile load unnecessary styles.

**Detect input method, not just screen size** — a laptop can have a touchscreen; a tablet can have a keyboard:
```css
@media (pointer: coarse) { .button { padding: 12px 20px; } }  /* touch */
@media (hover: none) { .card { /* no hover states */ } }       /* touch devices */
```

**Handle the notch**:
```css
body { padding-bottom: max(1rem, env(safe-area-inset-bottom)); }
```
Enable: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`

**Test on real devices** — DevTools emulation misses actual touch interactions, CPU/memory constraints, font rendering differences, and browser chrome. At minimum: one real iPhone, one real Android.

---

## UX Writing

**Button labels — never "OK", "Submit", "Yes/No"** — use specific verb + object:

| Bad | Good |
|-----|------|
| OK | Save changes |
| Submit | Create account |
| Yes | Delete message |
| Cancel | Keep editing |

For destructive: name the destruction — "Delete 5 items" not "Delete selected".

**Error message formula**: What happened + Why + How to fix. Never blame the user.
> "Email address isn't valid. Please include an @ symbol." not "Invalid input."

**Empty states are onboarding moments**: Acknowledge + explain value + provide action.
> "No projects yet. Create your first one to get started." not "No items."

**Consistency**: One term per concept. Build a glossary. (Delete, not Delete/Remove/Trash.)

**Never humor for errors** — users are already frustrated. Be helpful, not cute.

---

## Implementation

Match complexity to vision. Maximalist designs need elaborate code with extensive animations. Minimalist designs need restraint, precision, and careful attention to spacing and subtle details. Elegance comes from executing the vision well, not from adding effects.

Make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.
