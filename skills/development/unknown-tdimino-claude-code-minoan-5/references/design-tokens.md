# Conductor Motion Design Tokens

Complete token reference for the `--cm-*` CSS custom property system.

## Dark Scheme (Default)

```css
:root {
  /* Background */
  --cm-bg: #0B0F1A;
  --cm-surface: #141824;
  --cm-elevated: #1C2133;
  --cm-card: #242A3D;

  /* Brand */
  --cm-brand: #4F7BF7;
  --cm-brand-text: #0B0F1A;
  --cm-brand-40: rgba(79, 123, 247, 0.4);
  --cm-brand-20: rgba(79, 123, 247, 0.2);

  /* Text */
  --cm-text: #E8ECF4;
  --cm-text-70: rgba(232, 236, 244, 0.7);
  --cm-text-40: rgba(232, 236, 244, 0.4);
  --cm-text-20: rgba(232, 236, 244, 0.2);

  /* Status */
  --cm-success: #34D399;
  --cm-warning: #FBBF24;
  --cm-processing: #4F7BF7;
  --cm-error: #F87171;

  /* Borders */
  --cm-border: rgba(232, 236, 244, 0.15);
  --cm-border-subtle: rgba(232, 236, 244, 0.08);

  /* Motion */
  --cm-ease-out-cubic: cubic-bezier(0.33, 1, 0.68, 1);
  --cm-ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --cm-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  /* Timing */
  --cm-stagger: 200ms;
  --cm-reveal-duration: 420ms;
  --cm-typing-speed: 45ms;
  --cm-hero-transition: 1300ms;

  /* Typography */
  --cm-font: 'Geist', 'Inter', system-ui, sans-serif;
  --cm-font-mono: 'Geist Mono', 'SF Mono', 'Consolas', monospace;
  --cm-hero-size: clamp(2rem, 4vw + 1rem, 4.5rem);
  --cm-body-size: clamp(0.875rem, 0.5vw + 0.75rem, 1rem);
  --cm-mono-size: clamp(0.75rem, 0.4vw + 0.65rem, 0.875rem);
}
```

## Light Scheme

```css
:root {
  --cm-bg: #FFFFFF;
  --cm-surface: #F8F9FB;
  --cm-elevated: #F1F3F7;
  --cm-card: #E8ECF4;
  --cm-text: #0B0F1A;
  --cm-text-70: rgba(11, 15, 26, 0.7);
  --cm-text-40: rgba(11, 15, 26, 0.4);
  --cm-border: rgba(11, 15, 26, 0.12);
  --cm-border-subtle: rgba(11, 15, 26, 0.06);
}
```

## Easing Functions

```javascript
const EASING = {
  easeOutCubic: t => 1 - Math.pow(1 - t, 3),
  easeOutQuart: t => 1 - Math.pow(1 - t, 4),
  easeOutExpo:  t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
  linear:       t => t
};
```

## Timing Constants (medium pacing)

```
Typewriter:
  TYPE_SPEED       = 45ms base + 18ms variance (per char)
  DELETE_SPEED     = 24ms (per char)
  HOLD_FULL        = 1100ms (before deleting)
  HOLD_EMPTY       = 180ms (between words)

Progress:
  TOTAL_DURATION   = 6000ms
  START_PERCENT    = 5
  END_PERCENT      = 100
  ROW_STAGGER      = 900ms (between row reveals)
  ROW_TRANSITION   = 420ms (opacity + translateY)
  DOTS_CYCLE       = 420ms (PROCESSING... dots)

Stagger Reveal:
  STAGGER_DELAY    = 200ms (per element)
  TRANSITION       = 1300ms ease-in-out (opacity + transform)
  TRANSLATE_Y      = 10px (initial offset)
  TRIGGER          = double rAF + class toggle

File Review:
  PROCESS_DURATION = 2000ms (per file)
  STAGGER          = 800ms (between files starting)
  STATE_TRANSITION = 300ms (fade between states)
```

## Pacing Multiplier

| Pacing | Multiplier | Effect |
|--------|-----------|--------|
| `slow` | 1.5× | Deliberate, dramatic reveals |
| `medium` | 1.0× | Professional, ConductorAI default |
| `fast` | 0.6× | Urgent, high-energy |

Applied to all duration constants. Stagger delays scale at 0.8× the multiplier to prevent long sequences from feeling glacial at slow pacing.
