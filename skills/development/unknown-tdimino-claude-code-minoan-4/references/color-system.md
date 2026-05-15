# Color System

## Full Token Set

```css
:root {
    /* Background scale (dark-on-dark elevation) */
    --grn-bg: #000000;          /* Body */
    --grn-surface: #141414;     /* Section backgrounds, vignette target */
    --grn-elevated: #1A1A1A;    /* Elevated cards, panels */
    --grn-card: #2B2B2B;        /* Interactive card surfaces */

    /* Accent */
    --grn-accent: #C2F13C;           /* Primary lime green */
    --grn-accent-40: rgba(194, 241, 60, 0.4);  /* Overlays */
    --grn-accent-20: rgba(194, 241, 60, 0.2);  /* Grid, glow */

    /* Text */
    --grn-text: #FFFFFF;
    --grn-text-70: rgba(255, 255, 255, 0.7);   /* Secondary */
    --grn-text-40: rgba(255, 255, 255, 0.4);   /* Muted */
    --grn-text-20: rgba(255, 255, 255, 0.2);   /* Subtle */
    --grn-text-10: rgba(255, 255, 255, 0.1);   /* Ghost */

    /* Borders */
    --grn-border: rgba(255, 255, 255, 0.2);
    --grn-border-subtle: rgba(255, 255, 255, 0.1);
}
```

## Dark-on-Dark Elevation

`#000` → `#141414` → `#1A1A1A` → `#2B2B2B`

Each step: 20-30 lightness units apart. Subtle but perceptible.

On dark backgrounds, shadows are invisible unless colored — use lime or white glow for elevation.

Borders provide primary visual separation, not shadows.

## Re-Theming

Override all `--grn-*` at `:root`:

```css
:root {
    --grn-accent: #FF6B35;  /* Orange */
    --grn-accent-40: rgba(255, 107, 53, 0.4);
    --grn-accent-20: rgba(255, 107, 53, 0.2);
}
```

Accent should always be saturated + high-lightness for glow visibility.

For warm themes, shift surface scale to warm grays: `#181614`, `#1E1A16`.
