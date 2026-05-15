# Glass Hero Palette

CSS token preset for the kaolti glass-hero aesthetic. Apply these overrides to `:root` alongside the default `--grn-*` tokens to re-theme any grainient mode in the Glass Hero dark palette.

## Token Override Block

```css
:root {
  /* Glass Hero palette — overrides default grainient tokens */

  /* Background scale */
  --grn-bg: #0a0a0c;
  --grn-surface: #161616;      /* rgb(22, 22, 22) — panel bg */
  --grn-elevated: #1c1c1e;
  --grn-card: #2a2a2e;

  /* Accent — mint green (replaces lime) */
  --grn-accent: #57FFA8;
  --grn-accent-40: rgba(87, 255, 168, 0.4);
  --grn-accent-20: rgba(87, 255, 168, 0.2);

  /* Secondary accent — violet */
  --grn-glass-hero-secondary: #A78BFA;
  --grn-glass-hero-secondary-40: rgba(167, 139, 250, 0.4);
  --grn-glass-hero-secondary-20: rgba(167, 139, 250, 0.2);

  /* Warm accent — orange (for UI highlights) */
  --grn-glass-hero-warm: rgb(254, 128, 64);

  /* Text */
  --grn-text: #FFFFFF;
  --grn-text-70: rgba(255, 255, 255, 0.7);   /* banner text */
  --grn-text-40: rgba(255, 255, 255, 0.4);
  --grn-text-20: rgba(255, 255, 255, 0.2);
  --grn-text-10: rgba(255, 255, 255, 0.1);
  --grn-glass-hero-text-90: rgba(255, 255, 255, 0.9);  /* code text */
  --grn-glass-hero-text-60: rgba(255, 255, 255, 0.6);  /* body text */

  /* Borders — glass-edge style */
  --grn-border: rgba(255, 255, 255, 0.11);        /* glass edge light */
  --grn-border-subtle: rgba(255, 255, 255, 0.06);
  --grn-glass-hero-border-bright: rgba(255, 255, 255, 0.9); /* glass edge highlight */

  /* Blur tiers (unchanged — grainient defaults work) */
  /* --grn-blur-light: blur(5px);   */
  /* --grn-blur-medium: blur(10px); */
  /* --grn-blur-heavy: blur(20px);  */

  /* Typography — Geist replaces Inter */
  --grn-font: 'Geist', 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  --grn-glass-hero-font-mono: 'Geist Mono', 'IBM Plex Mono', monospace;
  --grn-glass-hero-font-display: 'Space Grotesk', 'Inter', sans-serif;
  --grn-hero-size: clamp(24px, 3vw + 0.5rem, 28px);
  --grn-body-size: clamp(14px, 0.8vw + 0.5rem, 15px);
}
```

## Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500&display=swap" rel="stylesheet">
```

Geist is not on Google Fonts — load via `https://cdn.jsdelivr.net/npm/geist@1.3.1/dist/fonts/geist-sans/` or fall back to Inter (the grainient default). The palette works with either; Geist adds tighter tracking and a more technical feel.

## Typography Scale

| Role | Token / Size | Tracking | Weight |
|------|-------------|----------|--------|
| Display heading | `var(--grn-hero-size)` | -0.02em | 600 |
| Body | `var(--grn-body-size)` | -0.005em | 400 |
| Banner / small | 12px | normal | 400 |
| Nav labels | 10–11px | normal | 400 |
| Code inline | `var(--grn-glass-hero-font-mono)` | normal | 400 |

Line height: 1.6 for body.

## Glassmorphism Recipe (Glass Hero style)

```css
.glass-hero-panel {
  backdrop-filter: var(--grn-blur-medium);
  background: rgba(10, 10, 12, 0.6);
  border: 1px solid var(--grn-border);
  border-radius: 8px;
}

.glass-hero-banner {
  backdrop-filter: var(--grn-blur-light);
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: var(--grn-text-70);
  font-size: 12px;
  padding: 8px 12px;
}

.glass-hero-nav {
  backdrop-filter: var(--grn-blur-heavy);
  background: rgba(10, 10, 12, 0.8);
  border-bottom: 1px solid var(--grn-border);
  height: 40px;
}
```

## Color Palette Visual Map

```
Base         #0a0a0c  ████████  Near-black with blue undertone
Surface      #161616  ████████  Panel/sidebar background
Elevated     #1c1c1e  ████████  Card elevation
Card         #2a2a2e  ████████  Highest elevation

Accent       #57FFA8  ████████  Mint green — CTA, links
Secondary    #A78BFA  ████████  Violet — secondary actions
Warm         FE8040   ████████  Orange — UI highlights

Glass edges  white/11 ░░░░░░░░  Subtle glass border
Glass bright white/90 ████████  Strong glass highlight
```

## Differences from Default Grainient

| Property | Default Grainient | Glass Hero Override |
|----------|-------------------|---------------------|
| `--grn-bg` | `#000000` | `#0a0a0c` (blue-tinted) |
| `--grn-accent` | `#C2F13C` (lime) | `#57FFA8` (mint) |
| `--grn-border` | `white/20` | `white/11` (subtler) |
| `--grn-font` | Inter | Geist (tighter tracking) |
| Body text opacity | `white/70` | `white/60` (more subtle) |
| Has secondary accent | No | Yes (`#A78BFA` violet) |

## Cross-Skill Reference

For the full 3D glass experience with MeshPhysicalMaterial refraction, dispersion, and iridescence, use threejs-particle-canvas Mode 6 (glass-hero). This palette provides the flat CSS equivalent for grainient's glassmorphism effect (#8 in the effects catalog).

## Attribution

Palette extracted from [Glass Hero](https://experiments.thisiswhitespace.com/glass-hero) by kaolti (thisiswhitespace.com), May 2026.
