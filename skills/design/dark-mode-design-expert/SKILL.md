---
name: dark-mode-design-expert
description: Master dark mode UI design with atmospheric theming, WCAG accessibility, and cross-platform best practices. Specializes in weather/sky/ocean-inspired color systems that adapt to time of day and environmental conditions.
category: Design
tags:
  - dark-mode
  - accessibility
  - theming
---

# Dark Mode Design Expert

Master dark mode UI design with atmospheric theming, WCAG accessibility, and cross-platform best practices. Specializes in weather/sky/ocean-inspired color systems that adapt to time of day and environmental conditions.

## When to Use This Skill

**Activate on:**
- "dark mode", "dark theme", "night mode"
- "theme switching", "light/dark toggle"
- "atmospheric UI", "weather theme", "sky gradient"
- "OLED optimization", "battery-friendly dark"
- "elevation in dark mode", "surface layering"
- "prefers-color-scheme", "color-scheme CSS"
- "contrast ratios dark mode", "accessibility dark theme"

**NOT for:**
- General color palette creation → `color-theory-palette-harmony-expert`
- Typography and font selection → `typography-expert`
- Component library architecture → `design-system-creator`
- Contrast auditing of specific colors → `color-contrast-auditor`

---

## The Science of Dark Mode

### Why Dark Mode Exists

| Factor | Light Mode | Dark Mode | Winner |
|--------|------------|-----------|--------|
| **OLED Battery** | 100% baseline | 39-47% savings at max brightness | Dark |
| **Low Light Comfort** | Eye strain, fatigue | Reduced glare | Dark |
| **Bright Environment** | Better readability | Washed out | Light |
| **Astigmatism Users** | Easier to read | Halation effect | Light |
| **Focus/Immersion** | Standard | Content pops forward | Dark |
| **Sleep Hygiene** | Blue light exposure | Reduced blue light | Dark |

**Key Insight:** Dark mode isn't universally better—it's contextually better. The best systems respect user preference AND adapt to environment.

### Contrast Requirements (WCAG 2.1)

| Element Type | Minimum Ratio | Target Ratio | Notes |
|--------------|---------------|--------------|-------|
| Body text | 4.5:1 | 7:1+ | AAA preferred for readability |
| Large text (≥24px) | 3:1 | 4.5:1+ | Headlines, hero text |
| UI components | 3:1 | 4.5:1+ | Borders, icons, focus rings |
| Disabled elements | None required | 2.5:1 | UX consideration |
| Decorative | None required | - | Pure aesthetic elements |

**Dark Mode Gotcha:** High contrast (21:1 pure white on black) causes more eye strain than moderate contrast (15:1). Target **12:1 to 16:1** for primary text.

---

## The Three-Tier Token Architecture

### Foundation: Primitives → Semantic → Component

```css
/* ══════════════════════════════════════════════════════════════════
   TIER 1: PRIMITIVES - Raw color values, never used directly
   ══════════════════════════════════════════════════════════════════ */
:root {
  /* Neutrals */
  --color-gray-50: #f8fafc;
  --color-gray-100: #f1f5f9;
  --color-gray-200: #e2e8f0;
  --color-gray-300: #cbd5e1;
  --color-gray-400: #94a3b8;
  --color-gray-500: #64748b;
  --color-gray-600: #475569;
  --color-gray-700: #334155;
  --color-gray-800: #1e293b;
  --color-gray-900: #0f172a;
  --color-gray-950: #020617;

  /* Brand Colors */
  --color-ocean-300: #7dd3fc;
  --color-ocean-400: #38bdf8;
  --color-ocean-500: #0ea5e9;
  --color-ocean-600: #0284c7;
  --color-ocean-700: #0369a1;

  /* Atmospheric Colors (for weather theming) */
  --color-twilight-deep: #0c1222;
  --color-twilight-mid: #151b2e;
  --color-twilight-surface: #1a1f3a;
  --color-dawn-warm: #fef3c7;
  --color-sunset-orange: #fb923c;
  --color-storm-gray: #374151;
}

/* ══════════════════════════════════════════════════════════════════
   TIER 2: SEMANTIC - Purpose-driven, theme-aware
   ══════════════════════════════════════════════════════════════════ */

/* Light Mode (Default) */
:root, :root.theme-light {
  /* Text */
  --color-text-primary: var(--color-gray-900);      /* 15.3:1 on white */
  --color-text-secondary: var(--color-gray-600);    /* 7.0:1 on white */
  --color-text-muted: var(--color-gray-500);        /* 4.6:1 on white */
  --color-text-inverse: var(--color-gray-50);

  /* Backgrounds */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: var(--color-gray-50);
  --color-bg-elevated: #ffffff;
  --color-bg-overlay: rgba(0, 0, 0, 0.5);

  /* Surfaces (elevation system) */
  --color-surface-base: #ffffff;
  --color-surface-raised: #ffffff;
  --color-surface-overlay: #ffffff;

  /* Borders */
  --color-border-default: var(--color-gray-200);
  --color-border-muted: var(--color-gray-100);
  --color-border-emphasis: var(--color-gray-300);

  /* Interactive */
  --color-interactive-primary: var(--color-ocean-600);
  --color-interactive-hover: var(--color-ocean-700);
  --color-interactive-focus: var(--color-ocean-500);

  /* Elevation (shadows work in light mode) */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
}

/* Dark Mode */
:root.theme-dark {
  /* Text - slightly off-white to reduce strain */
  --color-text-primary: var(--color-gray-50);       /* 15.3:1 on dark */
  --color-text-secondary: var(--color-gray-300);    /* 9.3:1 on dark */
  --color-text-muted: var(--color-gray-400);        /* 5.5:1 on dark */
  --color-text-inverse: var(--color-gray-900);

  /* Backgrounds - NOT pure black (#000) */
  --color-bg-primary: var(--color-twilight-deep);   /* #0c1222 */
  --color-bg-secondary: var(--color-twilight-mid);  /* #151b2e */
  --color-bg-elevated: var(--color-twilight-surface); /* #1a1f3a */
  --color-bg-overlay: rgba(0, 0, 0, 0.7);

  /* Surfaces - LIGHTER for elevation (key dark mode principle) */
  --color-surface-base: var(--color-twilight-deep);
  --color-surface-raised: var(--color-twilight-mid);
  --color-surface-overlay: var(--color-twilight-surface);

  /* Borders - more visible in dark mode */
  --color-border-default: rgba(255, 255, 255, 0.1);
  --color-border-muted: rgba(255, 255, 255, 0.05);
  --color-border-emphasis: rgba(255, 255, 255, 0.2);

  /* Interactive - brighter for visibility */
  --color-interactive-primary: var(--color-ocean-400);
  --color-interactive-hover: var(--color-ocean-300);
  --color-interactive-focus: var(--color-ocean-500);

  /* Elevation - GLOW replaces shadows in dark mode */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.6);

  /* Glow effects (unique to dark mode) */
  --glow-sm: 0 0 8px rgba(56, 189, 248, 0.2);
  --glow-md: 0 0 16px rgba(56, 189, 248, 0.3);
  --glow-lg: 0 0 32px rgba(56, 189, 248, 0.4);
}

/* ══════════════════════════════════════════════════════════════════
   TIER 3: COMPONENT - Specific usage, consuming semantic tokens
   ══════════════════════════════════════════════════════════════════ */
:root {
  /* Buttons */
  --button-bg: var(--color-interactive-primary);
  --button-text: var(--color-text-inverse);
  --button-border: transparent;
  --button-shadow: var(--shadow-sm);

  /* Cards */
  --card-bg: var(--color-surface-raised);
  --card-border: var(--color-border-default);
  --card-shadow: var(--shadow-md);

  /* Inputs */
  --input-bg: var(--color-bg-primary);
  --input-border: var(--color-border-default);
  --input-focus-ring: var(--color-interactive-focus);
}
```

---

## Elevation in Dark Mode: The Critical Difference

### Why Shadows Fail in Dark Mode

In light mode, shadows create depth by simulating light from above. In dark mode:
- Shadows become invisible against dark backgrounds
- Pure black shadows look like "holes"
- The illusion breaks completely

### Material Design 3 Solution: Tonal Elevation

Instead of shadows, use **lighter surface colors** for elevated elements:

```css
/* Light Mode: Shadows create elevation */
.card-light {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Dark Mode: Surface color creates elevation */
.card-dark {
  background: #1e1e1e;  /* Elevated from #121212 base */
  box-shadow: none;      /* Or very subtle */
}
```

### Elevation Scale (Material Design 3)

| Level | Light Mode | Dark Mode Surface | Overlay % |
|-------|------------|-------------------|-----------|
| 0 (base) | #ffffff | #121212 | 0% |
| 1 | shadow-sm | #1e1e1e | 5% white |
| 2 | shadow-md | #232323 | 7% white |
| 3 | shadow-lg | #282828 | 8% white |
| 4 | shadow-xl | #2d2d2d | 9% white |
| 5 | shadow-2xl | #323232 | 11% white |

### Implementation Pattern

```css
:root.theme-dark {
  /* Calculate overlay colors */
  --elevation-1: color-mix(in srgb, white 5%, var(--color-bg-primary));
  --elevation-2: color-mix(in srgb, white 7%, var(--color-bg-primary));
  --elevation-3: color-mix(in srgb, white 8%, var(--color-bg-primary));
  --elevation-4: color-mix(in srgb, white 9%, var(--color-bg-primary));
  --elevation-5: color-mix(in srgb, white 11%, var(--color-bg-primary));
}

.card {
  background: var(--elevation-2);
}

.modal {
  background: var(--elevation-4);
}

.dropdown {
  background: var(--elevation-3);
}
```

---

## CSS Implementation Patterns

### Modern Approach: `prefers-color-scheme` + `light-dark()`

```css
/* 1. Set color-scheme for native element styling */
:root {
  color-scheme: light dark;
}

/* 2. Use light-dark() for inline theming (2024+ browsers) */
.card {
  background: light-dark(#ffffff, #1e1e1e);
  color: light-dark(#1f2937, #f3f4f6);
  border: 1px solid light-dark(#e5e7eb, rgba(255,255,255,0.1));
}

/* 3. Respect system preference */
@media (prefers-color-scheme: dark) {
  :root:not(.theme-light) {
    /* Dark mode tokens */
  }
}

@media (prefers-color-scheme: light) {
  :root:not(.theme-dark) {
    /* Light mode tokens */
  }
}
```

### Theme Switching with JavaScript

```typescript
// Theme manager with persistence
type Theme = 'light' | 'dark' | 'system';

function setTheme(theme: Theme) {
  const root = document.documentElement;

  // Remove existing theme classes
  root.classList.remove('theme-light', 'theme-dark');

  if (theme === 'system') {
    // Let CSS media queries handle it
    localStorage.removeItem('theme');
    return;
  }

  // Apply explicit theme
  root.classList.add(`theme-${theme}`);
  localStorage.setItem('theme', theme);
}

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

// Initialize on page load (before render to prevent flash)
function initTheme() {
  const saved = localStorage.getItem('theme') as Theme | null;
  if (saved && saved !== 'system') {
    document.documentElement.classList.add(`theme-${saved}`);
  }
}

// Listen for system changes
window.matchMedia('(prefers-color-scheme: dark)')
  .addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      // Only react if user hasn't set explicit preference
      // CSS will handle via media queries
    }
  });
```

### Preventing Flash of Wrong Theme (FOWT)

```html
<!-- In <head>, before any CSS -->
<script>
  (function() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
      document.documentElement.classList.add('theme-dark');
    } else if (theme === 'light') {
      document.documentElement.classList.add('theme-light');
    }
  })();
</script>
```

---

## Worked Example: Weather/Sky/Ocean Atmospheric UI

This is the flagship example—a complete token system for a weather-inspired UI that adapts to time of day and atmospheric conditions.

### Design Philosophy

The ocean and sky share a visual language:
- **Dawn/Dusk**: Warm gradients, soft transitions
- **Midday**: Bright, high contrast, clear
- **Night**: Deep blues, subtle glows, stars
- **Storm**: Dramatic grays, electric highlights
- **Underwater**: Teal depths, bioluminescent accents

### Complete Token System

```css
/* ══════════════════════════════════════════════════════════════════
   OCEAN MODERN: ATMOSPHERIC UI TOKEN SYSTEM
   A weather/sky/ocean-inspired design system with time-of-day awareness
   ══════════════════════════════════════════════════════════════════ */

:root {
  /* ────────────────────────────────────────────────────────────────
     PRIMITIVES: Atmospheric Color Palette
     ──────────────────────────────────────────────────────────────── */

  /* Ocean Depths */
  --ocean-surface: #38bdf8;      /* Sunlit surface */
  --ocean-shallow: #0ea5e9;      /* Clear shallows */
  --ocean-mid: #0284c7;          /* Mid-depth */
  --ocean-deep: #0369a1;         /* Deep water */
  --ocean-abyss: #075985;        /* Abyssal zone */
  --ocean-trench: #0c4a6e;       /* Hadal zone */

  /* Sky States */
  --sky-dawn: #fef3c7;           /* Golden hour */
  --sky-morning: #bae6fd;        /* Clear morning */
  --sky-midday: #7dd3fc;         /* Bright day */
  --sky-golden: #fcd34d;         /* Golden hour */
  --sky-sunset: #fb923c;         /* Sunset orange */
  --sky-dusk: #a78bfa;           /* Purple dusk */
  --sky-twilight: #6366f1;       /* Civil twilight */
  --sky-night: #1e1b4b;          /* Night sky */

  /* Atmospheric Effects */
  --atmosphere-haze: rgba(186, 230, 253, 0.3);
  --atmosphere-fog: rgba(241, 245, 249, 0.6);
  --atmosphere-mist: rgba(148, 163, 184, 0.4);

  /* Storm System */
  --storm-light: #9ca3af;
  --storm-mid: #6b7280;
  --storm-dark: #4b5563;
  --storm-thunder: #374151;
  --storm-lightning: #fbbf24;

  /* Bioluminescence (dark mode accents) */
  --bio-cyan: #22d3ee;
  --bio-teal: #2dd4bf;
  --bio-blue: #60a5fa;
  --bio-purple: #a78bfa;
  --bio-glow: rgba(34, 211, 238, 0.4);

  /* Sand & Beach */
  --sand-light: #fef3c7;
  --sand-warm: #fde68a;
  --sand-golden: #fcd34d;
  --sand-wet: #d4a574;

  /* Coral & Life */
  --coral-pink: #fb7185;
  --coral-orange: #fb923c;
  --kelp-green: #22c55e;
  --algae-teal: #14b8a6;
}

/* ════════════════════════════════════════════════════════════════════
   SEMANTIC: Time-of-Day Themes
   ════════════════════════════════════════════════════════════════════ */

/* DAWN THEME (5am - 8am) - Warm, hopeful, transitional */
:root.atmosphere-dawn {
  --color-text-primary: #1e293b;
  --color-text-secondary: #475569;
  --color-bg-primary: var(--sky-dawn);
  --color-bg-secondary: #fef9e7;
  --color-accent: var(--sky-golden);
  --gradient-sky: linear-gradient(
    180deg,
    var(--sky-night) 0%,
    var(--sky-dusk) 20%,
    var(--sky-sunset) 40%,
    var(--sky-golden) 70%,
    var(--sky-dawn) 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    var(--ocean-deep) 0%,
    var(--ocean-mid) 50%,
    var(--ocean-surface) 100%
  );
}

/* DAYLIGHT THEME (8am - 5pm) - Bright, clear, energetic */
:root.atmosphere-day, :root.theme-light {
  --color-text-primary: #0f172a;
  --color-text-secondary: #334155;
  --color-text-muted: #64748b;
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f8fafc;
  --color-bg-elevated: #ffffff;
  --color-accent: var(--ocean-shallow);
  --color-accent-hover: var(--ocean-mid);
  --gradient-sky: linear-gradient(
    180deg,
    var(--sky-midday) 0%,
    var(--sky-morning) 50%,
    #ffffff 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    var(--ocean-abyss) 0%,
    var(--ocean-deep) 30%,
    var(--ocean-mid) 60%,
    var(--ocean-shallow) 100%
  );
  /* Daylight uses shadows for elevation */
  --elevation-method: shadow;
}

/* GOLDEN HOUR THEME (5pm - 7pm) - Warm, dramatic, nostalgic */
:root.atmosphere-golden {
  --color-text-primary: #1c1917;
  --color-text-secondary: #44403c;
  --color-bg-primary: #fffbeb;
  --color-bg-secondary: #fef3c7;
  --color-accent: var(--sky-sunset);
  --gradient-sky: linear-gradient(
    180deg,
    var(--sky-midday) 0%,
    var(--sky-golden) 40%,
    var(--sky-sunset) 70%,
    var(--coral-pink) 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    var(--ocean-deep) 0%,
    #0891b2 50%,
    #fcd34d 100%
  );
}

/* TWILIGHT THEME (7pm - 9pm) - Transitional, mysterious */
:root.atmosphere-twilight {
  --color-text-primary: #e2e8f0;
  --color-text-secondary: #94a3b8;
  --color-bg-primary: #0f172a;
  --color-bg-secondary: #1e293b;
  --color-bg-elevated: #334155;
  --color-accent: var(--sky-twilight);
  --gradient-sky: linear-gradient(
    180deg,
    var(--sky-night) 0%,
    var(--sky-twilight) 30%,
    var(--sky-dusk) 60%,
    var(--sky-sunset) 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    var(--ocean-trench) 0%,
    var(--ocean-abyss) 50%,
    var(--ocean-deep) 100%
  );
}

/* NIGHT THEME (9pm - 5am) - Deep, calm, bioluminescent */
:root.atmosphere-night, :root.theme-dark {
  --color-text-primary: #f1f5f9;        /* 15.3:1 ✓ AAA */
  --color-text-secondary: #cbd5e1;      /* 9.3:1 ✓ AAA */
  --color-text-muted: #94a3b8;          /* 5.5:1 ✓ AA */
  --color-bg-primary: #0c1222;          /* Deep twilight navy */
  --color-bg-secondary: #151b2e;
  --color-bg-elevated: #1a1f3a;
  --color-accent: var(--bio-cyan);
  --color-accent-hover: var(--bio-teal);
  --gradient-sky: linear-gradient(
    180deg,
    #020617 0%,
    var(--sky-night) 50%,
    #1e1b4b 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    #020617 0%,
    var(--ocean-trench) 50%,
    var(--ocean-abyss) 100%
  );
  /* Night uses lighter surfaces for elevation */
  --elevation-method: surface;

  /* Bioluminescent glow effects */
  --glow-accent: 0 0 20px var(--bio-glow);
  --glow-subtle: 0 0 10px rgba(34, 211, 238, 0.2);

  /* Surface elevation scale */
  --surface-base: #0c1222;
  --surface-1: #111827;
  --surface-2: #1f2937;
  --surface-3: #374151;
  --surface-4: #4b5563;
}

/* STORM THEME - Dramatic, intense, electric */
:root.atmosphere-storm {
  --color-text-primary: #f3f4f6;
  --color-text-secondary: #d1d5db;
  --color-bg-primary: var(--storm-thunder);
  --color-bg-secondary: var(--storm-dark);
  --color-bg-elevated: var(--storm-mid);
  --color-accent: var(--storm-lightning);
  --gradient-sky: linear-gradient(
    180deg,
    var(--storm-thunder) 0%,
    var(--storm-dark) 30%,
    var(--storm-mid) 60%,
    var(--storm-light) 100%
  );
  --gradient-ocean: linear-gradient(
    180deg,
    #1f2937 0%,
    #374151 40%,
    #6b7280 80%,
    #9ca3af 100%
  );
  /* Lightning flash animation */
  --flash-color: rgba(251, 191, 36, 0.3);
}

/* ════════════════════════════════════════════════════════════════════
   COMPONENT: Atmospheric UI Elements
   ════════════════════════════════════════════════════════════════════ */

/* Glass Card - works in all atmospheres */
.glass-card {
  background: var(--glass-bg, rgba(255, 255, 255, 0.1));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.2));
  border-radius: 16px;
}

:root.theme-light .glass-card,
:root.atmosphere-day .glass-card,
:root.atmosphere-dawn .glass-card {
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-border: rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
}

:root.theme-dark .glass-card,
:root.atmosphere-night .glass-card,
:root.atmosphere-twilight .glass-card {
  --glass-bg: rgba(15, 23, 42, 0.6);
  --glass-border: rgba(255, 255, 255, 0.1);
  box-shadow: var(--glow-subtle);
}

/* Wave Animation */
.wave-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: var(--wave-height, 100px);
  background: var(--wave-color);
  animation: wave var(--wave-duration, 8s) ease-in-out infinite;
  opacity: var(--wave-opacity, 0.6);
}

@keyframes wave {
  0%, 100% { transform: translateX(0) translateY(0); }
  50% { transform: translateX(-25%) translateY(-10px); }
}

/* Bioluminescent Glow (dark mode only) */
:root.theme-dark .glow-element,
:root.atmosphere-night .glow-element {
  box-shadow: var(--glow-accent);
  transition: box-shadow 0.3s ease;
}

:root.theme-dark .glow-element:hover,
:root.atmosphere-night .glow-element:hover {
  box-shadow: 0 0 30px var(--bio-glow), 0 0 60px rgba(34, 211, 238, 0.2);
}

/* Cloud Layer */
.cloud-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: var(--cloud-pattern);
  opacity: var(--cloud-opacity, 0.5);
  animation: drift var(--cloud-speed, 60s) linear infinite;
}

@keyframes drift {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
```

### Time-Based Theme Switching

```typescript
type Atmosphere = 'dawn' | 'day' | 'golden' | 'twilight' | 'night' | 'storm';

function getAtmosphereFromTime(hour: number): Atmosphere {
  if (hour >= 5 && hour < 8) return 'dawn';
  if (hour >= 8 && hour < 17) return 'day';
  if (hour >= 17 && hour < 19) return 'golden';
  if (hour >= 19 && hour < 21) return 'twilight';
  return 'night';
}

function setAtmosphere(atmosphere: Atmosphere) {
  const root = document.documentElement;

  // Remove all atmosphere classes
  root.classList.remove(
    'atmosphere-dawn', 'atmosphere-day', 'atmosphere-golden',
    'atmosphere-twilight', 'atmosphere-night', 'atmosphere-storm',
    'theme-light', 'theme-dark'
  );

  // Add new atmosphere
  root.classList.add(`atmosphere-${atmosphere}`);

  // Also set base theme for compatibility
  const isDark = ['twilight', 'night', 'storm'].includes(atmosphere);
  root.classList.add(isDark ? 'theme-dark' : 'theme-light');
}

// Auto-update based on time
function initAtmosphericUI() {
  const updateAtmosphere = () => {
    const hour = new Date().getHours();
    setAtmosphere(getAtmosphereFromTime(hour));
  };

  updateAtmosphere();
  // Update every 15 minutes
  setInterval(updateAtmosphere, 15 * 60 * 1000);
}
```

### Weather API Integration

```typescript
interface WeatherCondition {
  main: 'Clear' | 'Clouds' | 'Rain' | 'Thunderstorm' | 'Snow' | 'Mist';
  description: string;
}

function getAtmosphereFromWeather(
  weather: WeatherCondition,
  hour: number
): Atmosphere {
  // Storm conditions override time
  if (weather.main === 'Thunderstorm') return 'storm';

  // Heavy overcast dims everything
  if (weather.main === 'Clouds' && weather.description.includes('overcast')) {
    return hour >= 19 || hour < 6 ? 'night' : 'twilight';
  }

  // Default to time-based
  return getAtmosphereFromTime(hour);
}
```

---

## Anti-Patterns to Avoid

### 1. Pure Black Background (#000000)

**Problem:** Causes eye strain, harsh contrast, OLED "smearing" on scroll
**Solution:** Use near-black like #0c1222, #121212, or #1a1a2e

### 2. Pure White Text (#FFFFFF) on Dark

**Problem:** Too harsh, causes halation for astigmatism users
**Solution:** Use off-white like #f1f5f9, #e2e8f0

### 3. Same Colors for Both Themes

**Problem:** Teal that looks great on white becomes invisible on dark
**Solution:** Use brighter variants in dark mode (ocean-400 instead of ocean-600)

### 4. Shadows in Dark Mode

**Problem:** Shadows disappear against dark backgrounds
**Solution:** Use lighter surface colors for elevation instead

### 5. Inverted Light Mode Colors

**Problem:** Simply inverting creates jarring, unnatural results
**Solution:** Design dark mode as its own coherent system

### 6. Ignoring System Preference

**Problem:** Forcing dark mode ignores user's system-wide preference
**Solution:** Default to `prefers-color-scheme`, allow override

### 7. Flash of Wrong Theme

**Problem:** Page loads light, then flashes to dark
**Solution:** Inline script in `<head>` before CSS loads

---

## Testing Checklist

### Visual Testing

- [ ] Primary text readable on all backgrounds (4.5:1+)
- [ ] Secondary text readable (4.5:1+)
- [ ] Muted text acceptable (3:1+ for large, 4.5:1+ for normal)
- [ ] Interactive elements distinguishable
- [ ] Focus states clearly visible
- [ ] Disabled states identifiable (but not required contrast)
- [ ] Elevation hierarchy clear without shadows
- [ ] No harsh white/black combinations

### Functional Testing

- [ ] Theme toggle works correctly
- [ ] System preference respected on first load
- [ ] Theme persists across page reloads
- [ ] No flash of wrong theme
- [ ] Images adapt appropriately
- [ ] Code blocks readable
- [ ] Charts/graphs remain legible
- [ ] Form elements properly styled

### Device Testing

- [ ] OLED screens (check for smearing on scroll)
- [ ] LCD screens (check for backlight bleed visibility)
- [ ] High brightness outdoor use
- [ ] Low brightness night use
- [ ] Color blindness simulation

---

## Industry References

### Material Design 3
- Base dark surface: #121212
- Tonal elevation with white overlay (5-11%)
- Primary colors at 80% lightness for dark mode
- 15.8:1 target contrast for elevated surfaces

### Apple Human Interface Guidelines
- Respect system appearance setting
- Semantic colors that adapt automatically
- Increased vibrancy in dark mode
- Base system background: dynamic (not static black)

### Figma
- Background: #2c2c2c (base), #383838 (elevated)
- Text: #ffffff (primary), #b3b3b3 (secondary)
- Accent: #0d99ff (brand blue, brightened for dark)

### Discord
- Background: #36393f (main), #2f3136 (sidebar)
- Text: #dcddde (primary), #72767d (muted)
- Accent: #5865f2 (blurple, same in both modes)

### Slack
- Background: #1a1d21 (base), #222529 (elevated)
- Uses colored sidebars in dark mode
- Maintains brand identity while adapting

---

## Companion Skills

| Skill | Handoff Point |
|-------|---------------|
| `color-contrast-auditor` | After designing tokens, audit specific pairs |
| `design-system-creator` | Integrate dark mode into broader design system |
| `web-design-expert` | Overall visual direction and brand alignment |
| `color-theory-palette-harmony-expert` | Generating initial color palettes |

---

*Remember: Dark mode isn't the absence of light—it's the careful orchestration of luminance to guide attention, reduce strain, and create atmosphere.*
