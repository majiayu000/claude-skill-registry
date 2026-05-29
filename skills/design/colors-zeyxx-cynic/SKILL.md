---
name: colors
description: Preview CYNIC's color system with semantic colors, health indicators, progress bars, and Dog colors (Sefirot). Use when testing terminal colors or wanting to see the visual theme.
user-invocable: true
---

# /colors - CYNIC Color System Preview

*"Les couleurs révèlent la vérité"* - κυνικός

## Execution

Run the color preview script:

```bash
node scripts/lib/colors.cjs
```

Display the output directly to the user.

## What It Shows

1. **Semantic Colors**: Success, warning, error, info, muted
2. **Health Indicators**: φ-aligned thresholds (61.8%, 38.2%)
3. **Progress Bars**: Normal and inverse (for heat/frustration)
4. **Dog Colors**: All 11 Sefirot with their assigned colors
5. **Dashboard Themes**: Color schemes for /psy, /health, /dogs, etc.

## φ-Aligned Thresholds

| Threshold | Meaning | Color |
|-----------|---------|-------|
| >61.8% | Healthy | Green |
| 38.2%-61.8% | Caution | Yellow |
| <38.2% | Critical | Red |

These thresholds are derived from the golden ratio (φ = 1.618).

## Using Colors in Scripts

```javascript
const { ANSI, c, progressBar, DOG_COLORS } = require('./scripts/lib/colors.cjs');

// Colorize text
console.log(c(ANSI.brightGreen, 'Success!'));

// Progress bar with φ thresholds
console.log(`Health: [${progressBar(0.75)}]`);

// Dog color
console.log(c(DOG_COLORS.SCOUT, '🔍 Scout'));
```

## See Also

- `/psy` - Human psychology (uses magenta theme)
- `/health` - System health (uses cyan theme)
- `/dogs` - Collective Dogs (uses cyan/yellow theme)
- `/status` - Self-status (uses cyan theme)
