---
name: web-weather-creator
description: Master of stylized atmospheric effects using SVG filters and CSS animations. Creates clouds, waves, lightning, rain, fog, aurora borealis, god rays, lens flares, twilight skies, and ocean spray—all with a premium aesthetic that's stylized but never cheap-looking.
category: Design
tags:
  - svg
  - animations
  - weather-effects
  - atmospheric
  - css-animations
---

# Web Weather Creator

Master of stylized atmospheric effects using SVG filters and CSS animations. Creates clouds, waves, lightning, rain, fog, aurora borealis, god rays, lens flares, twilight skies, and ocean spray—all with a premium aesthetic that's stylized but never cheap-looking.

## Activation Triggers

**Activate on:** "clouds", "waves", "weather effects", "atmospheric", "lightning", "rain", "fog", "mist", "aurora", "northern lights", "god rays", "crepuscular", "lens flare", "twilight", "sunset gradient", "golden hour", "ocean spray", "beach wash", "foam", "smoke", "parallax sky", "water ripples", "animated background"

**NOT for:**
- Photorealistic renders (use WebGL/Three.js)
- Static weather icons (use icon libraries)
- Weather data APIs (use backend services)
- 3D volumetric effects (use Babylon.js/Three.js)

---

## Philosophy: Stylized, Not Cheap

The goal is **premium stylization**—effects that feel intentional and artistic, not like stock footage or placeholder art.

### The Three Principles

1. **Layering Creates Depth** - Multiple semi-transparent layers with parallax motion
2. **Organic Motion** - Varied speeds, easing, and subtle randomization
3. **Restraint** - One hero effect, subtle supporting elements

### Quality Spectrum

```
CHEAP ──────────────────────── STYLIZED ──────────────────────── REALISTIC
CSS gradient blob         SVG filter + layered opacity        WebGL particles
Single div animation      3-5 layers with parallax            Fluid simulation
Linear easing             Cubic-bezier + varied timing        Physics engine
```

**Target Zone:** The middle—stylized enough to feel crafted, performant enough for production.

---

## Clouds Floating Through Content (Z-Index Strategy)

The most common question: *"How do I make clouds float through my content, not just behind it?"*

### The Split-Layer Solution

```html
<div class="atmosphere-container">
  <!-- BACK clouds (behind content) -->
  <div class="clouds clouds--back"></div>

  <!-- Content sits in the middle -->
  <main class="content">
    <div class="card">Your content here</div>
  </main>

  <!-- FRONT clouds (in front of content, but transparent) -->
  <div class="clouds clouds--front"></div>
</div>
```

```css
.atmosphere-container {
  position: relative;
  isolation: isolate; /* Creates stacking context */
}

.clouds {
  position: absolute;
  inset: 0;
  pointer-events: none; /* CRITICAL: Let clicks through */
  filter: url(#cloud-cumulus);
}

.clouds--back {
  z-index: -1;
  opacity: 0.3;
  transform: scale(1.5);
  animation: drift 120s linear infinite;
}

.content {
  position: relative;
  z-index: 1;
}

.clouds--front {
  z-index: 2;
  opacity: 0.12; /* LOW opacity so content is readable */
  transform: scale(0.8);
  animation: drift 50s linear infinite reverse;

  /* Optional: Mask to clear space around content */
  mask-image: linear-gradient(
    to bottom,
    black 0%,
    transparent 30%,
    transparent 70%,
    black 100%
  );
}
```

### Key Principles

1. **Split clouds into 2-3 layers** (back, mid, front)
2. **Front clouds use LOW opacity** (10-15%) so content remains visible
3. **Always use `pointer-events: none`** on cloud layers
4. **Use masks** to clear space around important content
5. **Vary animation speeds** for parallax depth (back = slow, front = fast)

### Blend Modes for Natural Integration

```css
.clouds--front {
  mix-blend-mode: soft-light; /* Blends naturally with content */
  opacity: 0.25;
}

/* Or for white clouds on dark backgrounds */
.clouds--front {
  mix-blend-mode: screen;
  opacity: 0.15;
}
```

### Content Readability

```css
/* Add subtle backdrop to cards so text is always readable */
.card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px); /* Blurs back clouds for extra depth */
}
```

→ **See `references/layering-strategies.md` for complete patterns including parallax, content-aware masking, and React components.**

---

## Core Technique: SVG Filter Chain

All atmospheric effects build on this filter architecture:

```svg
<svg width="0" height="0">
  <defs>
    <filter id="atmosphere" x="-50%" y="-50%" width="200%" height="200%">
      <!-- 1. Generate noise texture -->
      <feTurbulence
        type="fractalNoise"      <!-- or "turbulence" for water -->
        baseFrequency="0.01"     <!-- Lower = larger shapes -->
        numOctaves="4"           <!-- 3-5 for good detail -->
        seed="1"                 <!-- Change for variation -->
        result="noise"
      />

      <!-- 2. Distort the source -->
      <feDisplacementMap
        in="SourceGraphic"
        in2="noise"
        scale="30"               <!-- Distortion intensity -->
        xChannelSelector="R"
        yChannelSelector="G"
        result="displaced"
      />

      <!-- 3. Soften edges -->
      <feGaussianBlur
        in="displaced"
        stdDeviation="2"
        result="blurred"
      />

      <!-- 4. Add lighting (optional) -->
      <feDiffuseLighting
        in="noise"
        lighting-color="white"
        surfaceScale="2"
        result="lit"
      >
        <feDistantLight azimuth="45" elevation="60" />
      </feDiffuseLighting>

      <!-- 5. Composite layers -->
      <feComposite in="blurred" in2="lit" operator="multiply" />
    </filter>
  </defs>
</svg>
```

### Key Parameter Reference

| Parameter | Effect | Range | Notes |
|-----------|--------|-------|-------|
| `type="fractalNoise"` | Soft, cloudy | - | Clouds, smoke, fog |
| `type="turbulence"` | Wavy, liquid | - | Water, waves, ripples |
| `baseFrequency` | Shape size | 0.001-0.1 | Lower = larger shapes |
| `numOctaves` | Detail level | 1-8 | 3-5 optimal, >5 diminishing returns |
| `scale` (displacement) | Distortion | 0-100 | Start at 20-30 |
| `stdDeviation` (blur) | Softness | 0-20 | 2-5 for clouds, 0-2 for water |

---

## SECTION A: CLOUD EFFECTS

### Cloud Type Recipes

| Cloud Type | baseFrequency | numOctaves | Blur | Character |
|------------|---------------|------------|------|-----------|
| **Cumulus** (fluffy) | 0.008 | 4 | 3-5 | Puffy, cotton-like |
| **Cirrus** (wispy) | 0.003 | 5 | 1-2 | Thin, streaky |
| **Stratus** (flat) | 0.015 | 2 | 5-8 | Low, uniform |
| **Storm** (dramatic) | 0.006 | 5 | 2-3 | Dense, textured |
| **Cartoon** | 0.02 | 2 | 8-12 | Soft, simple |

### Multi-Layer Cloud System

```css
.cloud-layer {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 200% 100% at 50% 100%,
    rgba(255, 255, 255, 0.9) 0%,
    transparent 70%
  );
  filter: url(#cloud-filter);
}

/* Layer hierarchy: back → front */
.cloud-back {
  opacity: 0.3;
  transform: scale(1.5);
  animation: drift 120s linear infinite;
}

.cloud-mid {
  opacity: 0.5;
  transform: scale(1.2);
  animation: drift 80s linear infinite;
}

.cloud-front {
  opacity: 0.7;
  transform: scale(1);
  animation: drift 50s linear infinite;
}

@keyframes drift {
  from { transform: translateX(-10%); }
  to { transform: translateX(10%); }
}
```

### Cloud Color Palettes

```css
:root {
  /* Daylight clouds */
  --cloud-white: rgba(255, 255, 255, 0.9);
  --cloud-highlight: rgba(255, 250, 240, 1);
  --cloud-shadow: rgba(180, 190, 210, 0.6);

  /* Sunset clouds */
  --cloud-gold: rgba(255, 200, 100, 0.8);
  --cloud-pink: rgba(255, 150, 180, 0.7);
  --cloud-purple: rgba(180, 100, 200, 0.5);

  /* Storm clouds */
  --storm-dark: rgba(60, 70, 90, 0.9);
  --storm-purple: rgba(80, 60, 100, 0.7);
  --storm-highlight: rgba(200, 210, 230, 0.4);
}
```

---

## SECTION B: WAVE & WATER EFFECTS

### Critical Difference: Waves Use `turbulence`

```svg
<!-- WATER uses type="turbulence" NOT fractalNoise -->
<feTurbulence
  type="turbulence"
  baseFrequency="0.01 0.03"  <!-- X << Y for horizontal waves -->
  numOctaves="3"
  result="waves"
/>
```

### Wave Type Recipes

| Wave Type | baseFrequency | numOctaves | Scale | Character |
|-----------|---------------|------------|-------|-----------|
| **Ocean swell** | 0.005 0.015 | 3 | 40 | Broad, rolling |
| **Lake ripples** | 0.02 0.04 | 2 | 15 | Small, regular |
| **Beach shore** | 0.008 0.02 | 4 | 30 | Approaching, foam |
| **Pool reflection** | 0.03 0.03 | 2 | 10 | Subtle, uniform |

### Animated Wave SVG

```svg
<svg viewBox="0 0 1440 320" preserveAspectRatio="none">
  <defs>
    <filter id="wave-distort">
      <feTurbulence
        type="turbulence"
        baseFrequency="0.01 0.02"
        numOctaves="3"
        result="turbulence"
      >
        <animate
          attributeName="baseFrequency"
          dur="20s"
          values="0.01 0.02; 0.015 0.025; 0.01 0.02"
          repeatCount="indefinite"
        />
      </feTurbulence>
      <feDisplacementMap
        in="SourceGraphic"
        in2="turbulence"
        scale="20"
        xChannelSelector="R"
        yChannelSelector="G"
      />
    </filter>
  </defs>

  <path
    fill="var(--ocean-color)"
    filter="url(#wave-distort)"
    d="M0,160 C360,220 720,100 1080,180 C1260,220 1380,140 1440,160 L1440,320 L0,320 Z"
  >
    <animate
      attributeName="d"
      dur="10s"
      repeatCount="indefinite"
      values="
        M0,160 C360,220 720,100 1080,180 C1260,220 1380,140 1440,160 L1440,320 L0,320 Z;
        M0,180 C360,120 720,200 1080,140 C1260,100 1380,180 1440,140 L1440,320 L0,320 Z;
        M0,160 C360,220 720,100 1080,180 C1260,220 1380,140 1440,160 L1440,320 L0,320 Z
      "
    />
  </path>
</svg>
```

### Ocean Color Palettes

```css
:root {
  /* Deep ocean */
  --ocean-deep: #0c4a6e;
  --ocean-mid: #0369a1;
  --ocean-surface: #38bdf8;
  --ocean-foam: rgba(255, 255, 255, 0.8);

  /* Tropical */
  --tropical-deep: #047857;
  --tropical-mid: #10b981;
  --tropical-surface: #6ee7b7;

  /* Stormy */
  --stormy-deep: #1e3a5f;
  --stormy-mid: #334155;
  --stormy-surface: #64748b;

  /* Sunset reflection */
  --sunset-water: linear-gradient(
    180deg,
    rgba(251, 146, 60, 0.4) 0%,
    rgba(14, 165, 233, 0.6) 50%,
    #0c4a6e 100%
  );
}
```

---

## SECTION C: LIGHTNING EFFECTS

### SVG Stroke-Dashoffset Lightning

The most effective technique for lightning uses animated stroke-dashoffset on SVG paths:

```svg
<svg viewBox="0 0 100 200" class="lightning">
  <defs>
    <filter id="lightning-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <path
    class="bolt"
    d="M50,0 L45,40 L55,45 L40,90 L60,95 L35,150 L70,100 L50,95 L65,50 L45,45 L60,10 Z"
    fill="none"
    stroke="white"
    stroke-width="2"
    filter="url(#lightning-glow)"
  />
</svg>
```

```css
.lightning {
  position: absolute;
  pointer-events: none;
  opacity: 0;
}

.bolt {
  stroke-dasharray: 500;
  stroke-dashoffset: 500;
}

.lightning.flash {
  animation: lightning-flash 0.5s ease-out forwards;
}

.lightning.flash .bolt {
  animation: bolt-draw 0.15s ease-out forwards;
}

@keyframes lightning-flash {
  0% { opacity: 0; }
  10% { opacity: 1; }
  20% { opacity: 0.5; }
  30% { opacity: 1; }
  100% { opacity: 0; }
}

@keyframes bolt-draw {
  to { stroke-dashoffset: 0; }
}
```

### Lightning Flash Overlay

```css
.lightning-flash-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0);
  pointer-events: none;
  z-index: 1000;
}

.lightning-flash-overlay.active {
  animation: screen-flash 0.3s ease-out;
}

@keyframes screen-flash {
  0% { background: rgba(255, 255, 255, 0); }
  10% { background: rgba(200, 220, 255, 0.4); }
  20% { background: rgba(255, 255, 255, 0); }
  30% { background: rgba(200, 220, 255, 0.2); }
  100% { background: rgba(255, 255, 255, 0); }
}
```

### Branching Lightning Pattern

```javascript
function generateLightningPath(startX, startY, endY, segments = 8) {
  let path = `M${startX},${startY}`;
  let x = startX;
  let y = startY;
  const segmentHeight = (endY - startY) / segments;

  for (let i = 0; i < segments; i++) {
    const jitter = (Math.random() - 0.5) * 30;
    x += jitter;
    y += segmentHeight;
    path += ` L${x},${y}`;

    // Random branch (20% chance)
    if (Math.random() < 0.2) {
      const branchX = x + (Math.random() - 0.5) * 40;
      const branchY = y + segmentHeight * 0.5;
      path += ` M${x},${y} L${branchX},${branchY} M${x},${y}`;
    }
  }

  return path;
}
```

---

## SECTION D: RAIN EFFECTS

### CSS-Only Rain with Custom Properties

```css
.rain-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.raindrop {
  position: absolute;
  width: 2px;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(174, 194, 224, 0.5) 50%,
    rgba(174, 194, 224, 0.8) 100%
  );
  border-radius: 0 0 2px 2px;
  animation: rain-fall var(--fall-duration) linear infinite;
  animation-delay: var(--delay);
  left: var(--x);
  height: var(--length);
  opacity: var(--opacity);
}

@keyframes rain-fall {
  0% {
    transform: translateY(-100vh);
  }
  100% {
    transform: translateY(100vh);
  }
}
```

### Rain Generator (JavaScript)

```javascript
function createRain(container, dropCount = 100) {
  for (let i = 0; i < dropCount; i++) {
    const drop = document.createElement('div');
    drop.className = 'raindrop';
    drop.style.setProperty('--x', `${Math.random() * 100}%`);
    drop.style.setProperty('--delay', `${Math.random() * 2}s`);
    drop.style.setProperty('--fall-duration', `${0.5 + Math.random() * 0.5}s`);
    drop.style.setProperty('--length', `${15 + Math.random() * 20}px`);
    drop.style.setProperty('--opacity', `${0.3 + Math.random() * 0.5}`);
    container.appendChild(drop);
  }
}
```

### Rain Intensity Presets

```css
/* Light drizzle */
.rain-light {
  --drop-count: 50;
  --fall-duration-base: 1.2s;
  --drop-opacity: 0.3;
}

/* Moderate rain */
.rain-moderate {
  --drop-count: 150;
  --fall-duration-base: 0.8s;
  --drop-opacity: 0.5;
}

/* Heavy downpour */
.rain-heavy {
  --drop-count: 300;
  --fall-duration-base: 0.5s;
  --drop-opacity: 0.7;
}
```

### Rain + Wind Angle

```css
.raindrop.windy {
  animation: rain-fall-diagonal var(--fall-duration) linear infinite;
}

@keyframes rain-fall-diagonal {
  0% {
    transform: translate(-50vw, -100vh) rotate(15deg);
  }
  100% {
    transform: translate(50vw, 100vh) rotate(15deg);
  }
}
```

---

## SECTION E: FOG & MIST EFFECTS

### Multi-Layer Fog System

```css
.fog-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.fog-layer {
  position: absolute;
  width: 200%;
  height: 100%;
  background: url("data:image/svg+xml,...") repeat-x;
  opacity: 0.3;
  filter: url(#fog-filter);
}

.fog-back {
  animation: fog-drift 60s linear infinite;
  opacity: 0.2;
  transform: scale(1.5);
}

.fog-mid {
  animation: fog-drift 40s linear infinite reverse;
  opacity: 0.3;
  transform: scale(1.2);
}

.fog-front {
  animation: fog-drift 25s linear infinite;
  opacity: 0.4;
}

@keyframes fog-drift {
  from { transform: translateX(-50%); }
  to { transform: translateX(0%); }
}
```

### SVG Fog Filter

```svg
<filter id="fog-filter" x="-50%" y="-50%" width="200%" height="200%">
  <feTurbulence
    type="fractalNoise"
    baseFrequency="0.003"
    numOctaves="4"
    seed="5"
    result="noise"
  />
  <feGaussianBlur in="noise" stdDeviation="20" result="blur" />
  <feColorMatrix
    type="matrix"
    values="1 0 0 0 0
            0 1 0 0 0
            0 0 1 0 0
            0 0 0 0.5 0"
    result="faded"
  />
</filter>
```

### Fog Density Variations

```css
:root {
  /* Light haze */
  --fog-light: rgba(255, 255, 255, 0.2);
  --fog-blur-light: 10px;

  /* Morning mist */
  --fog-mist: rgba(200, 210, 230, 0.4);
  --fog-blur-mist: 20px;

  /* Dense fog */
  --fog-dense: rgba(180, 190, 210, 0.6);
  --fog-blur-dense: 40px;

  /* Eerie fog (horror) */
  --fog-eerie: rgba(100, 120, 140, 0.5);
  --fog-blur-eerie: 30px;
}
```

### Ground-Hugging Mist

```css
.ground-mist {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30%;
  background: linear-gradient(
    to top,
    rgba(255, 255, 255, 0.6) 0%,
    rgba(255, 255, 255, 0.3) 40%,
    transparent 100%
  );
  filter: url(#fog-filter);
  animation: mist-breathe 8s ease-in-out infinite;
}

@keyframes mist-breathe {
  0%, 100% {
    opacity: 0.5;
    transform: scaleY(1);
  }
  50% {
    opacity: 0.7;
    transform: scaleY(1.1);
  }
}
```

---

## SECTION F: TWILIGHT & SKY GRADIENTS

### Sky Time Progression

```css
:root {
  /* Pre-dawn (5:00-5:30) */
  --sky-predawn: linear-gradient(
    to top,
    #1a1a2e 0%,
    #16213e 30%,
    #0f3460 60%,
    #1a1a2e 100%
  );

  /* Dawn (5:30-6:30) */
  --sky-dawn: linear-gradient(
    to top,
    #ff6b6b 0%,
    #feca57 20%,
    #ff9ff3 40%,
    #54a0ff 70%,
    #1a1a2e 100%
  );

  /* Golden hour (6:30-7:30) */
  --sky-golden: linear-gradient(
    to top,
    #ff9a56 0%,
    #ffbe76 30%,
    #ffeaa7 50%,
    #74b9ff 80%,
    #0984e3 100%
  );

  /* Midday (10:00-14:00) */
  --sky-midday: linear-gradient(
    to top,
    #74b9ff 0%,
    #0984e3 50%,
    #0652dd 100%
  );

  /* Sunset (17:30-18:30) */
  --sky-sunset: linear-gradient(
    to top,
    #e17055 0%,
    #fdcb6e 20%,
    #f8a5c2 40%,
    #686de0 70%,
    #30336b 100%
  );

  /* Dusk (18:30-19:30) */
  --sky-dusk: linear-gradient(
    to top,
    #4a69bd 0%,
    #6a89cc 30%,
    #b8e994 10%,
    #e55039 5%,
    #1e3799 60%,
    #0c2461 100%
  );

  /* Night (20:00+) */
  --sky-night: linear-gradient(
    to top,
    #0c2461 0%,
    #1e3799 40%,
    #0a1931 100%
  );
}
```

### Animated Sky Transition

```css
.sky-canvas {
  background: var(--sky-midday);
  transition: background 3s ease-in-out;
}

.sky-canvas[data-time="dawn"] { background: var(--sky-dawn); }
.sky-canvas[data-time="golden"] { background: var(--sky-golden); }
.sky-canvas[data-time="midday"] { background: var(--sky-midday); }
.sky-canvas[data-time="sunset"] { background: var(--sky-sunset); }
.sky-canvas[data-time="dusk"] { background: var(--sky-dusk); }
.sky-canvas[data-time="night"] { background: var(--sky-night); }
```

### Sun/Moon Position System

```css
.celestial-body {
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  transition: all 2s cubic-bezier(0.4, 0, 0.2, 1);
}

.sun {
  background: radial-gradient(
    circle,
    #fff7e6 0%,
    #ffd93d 40%,
    #ff8c00 100%
  );
  box-shadow:
    0 0 40px 10px rgba(255, 200, 50, 0.6),
    0 0 80px 30px rgba(255, 150, 0, 0.3);
}

.moon {
  background: radial-gradient(
    circle at 30% 30%,
    #f5f5f5 0%,
    #e0e0e0 50%,
    #bdbdbd 100%
  );
  box-shadow:
    0 0 20px 5px rgba(255, 255, 255, 0.3),
    inset -10px -10px 20px rgba(0, 0, 0, 0.1);
}
```

---

## SECTION G: AURORA BOREALIS

### Stacked Gradient Aurora

```css
.aurora-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: linear-gradient(to top, #0a0a1a 0%, #1a1a3a 100%);
}

.aurora-band {
  position: absolute;
  top: 10%;
  left: -50%;
  width: 200%;
  height: 40%;
  opacity: 0.6;
  mix-blend-mode: screen;
  filter: blur(30px);
}

.aurora-green {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 255, 128, 0.4) 20%,
    rgba(0, 255, 200, 0.6) 50%,
    rgba(0, 255, 128, 0.4) 80%,
    transparent 100%
  );
  animation: aurora-wave 15s ease-in-out infinite;
}

.aurora-purple {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(138, 43, 226, 0.3) 25%,
    rgba(75, 0, 130, 0.5) 50%,
    rgba(138, 43, 226, 0.3) 75%,
    transparent 100%
  );
  animation: aurora-wave 20s ease-in-out infinite reverse;
  animation-delay: -5s;
}

.aurora-blue {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 150, 255, 0.3) 30%,
    rgba(0, 200, 255, 0.4) 50%,
    rgba(0, 150, 255, 0.3) 70%,
    transparent 100%
  );
  animation: aurora-wave 18s ease-in-out infinite;
  animation-delay: -8s;
}

@keyframes aurora-wave {
  0%, 100% {
    transform: translateX(-20%) scaleY(1) skewX(-5deg);
    opacity: 0.4;
  }
  25% {
    transform: translateX(-10%) scaleY(1.2) skewX(5deg);
    opacity: 0.7;
  }
  50% {
    transform: translateX(0%) scaleY(0.8) skewX(-3deg);
    opacity: 0.5;
  }
  75% {
    transform: translateX(10%) scaleY(1.1) skewX(3deg);
    opacity: 0.6;
  }
}
```

### Aurora Curtain Effect

```css
.aurora-curtain {
  position: absolute;
  top: 0;
  width: 100%;
  height: 60%;
  background: repeating-linear-gradient(
    90deg,
    transparent 0px,
    rgba(0, 255, 150, 0.1) 2px,
    transparent 4px
  );
  filter: blur(2px);
  animation: curtain-shimmer 3s ease-in-out infinite;
}

@keyframes curtain-shimmer {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}
```

### Aurora Color Palettes

```css
:root {
  /* Classic green */
  --aurora-green-1: rgba(0, 255, 128, 0.6);
  --aurora-green-2: rgba(50, 255, 180, 0.4);

  /* Purple/violet */
  --aurora-purple-1: rgba(138, 43, 226, 0.5);
  --aurora-purple-2: rgba(186, 85, 211, 0.4);

  /* Blue tones */
  --aurora-blue-1: rgba(0, 191, 255, 0.4);
  --aurora-blue-2: rgba(65, 105, 225, 0.3);

  /* Rare red (high activity) */
  --aurora-red-1: rgba(255, 69, 0, 0.3);
  --aurora-red-2: rgba(255, 99, 71, 0.2);
}
```

---

## SECTION H: GOD RAYS (CREPUSCULAR RAYS)

### Conic Gradient God Rays

```css
.god-rays-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.god-rays {
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 200%;
  height: 200%;
  background: conic-gradient(
    from 180deg at 50% 0%,
    transparent 0deg,
    rgba(255, 248, 220, 0.2) 5deg,
    transparent 10deg,
    transparent 20deg,
    rgba(255, 248, 220, 0.15) 25deg,
    transparent 30deg,
    transparent 45deg,
    rgba(255, 248, 220, 0.2) 50deg,
    transparent 55deg,
    transparent 70deg,
    rgba(255, 248, 220, 0.1) 75deg,
    transparent 80deg,
    transparent 100deg,
    rgba(255, 248, 220, 0.15) 105deg,
    transparent 110deg,
    transparent 130deg,
    rgba(255, 248, 220, 0.2) 135deg,
    transparent 140deg,
    transparent 160deg,
    rgba(255, 248, 220, 0.1) 165deg,
    transparent 170deg,
    transparent 180deg
  );
  mask-image: radial-gradient(
    ellipse 100% 100% at 50% 0%,
    black 0%,
    transparent 70%
  );
  animation: rays-pulse 8s ease-in-out infinite;
}

@keyframes rays-pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 0.9; }
}
```

### Through-Window God Rays

```css
.window-rays {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    transparent 0%,
    transparent 30%,
    rgba(255, 248, 220, 0.3) 30%,
    rgba(255, 248, 220, 0.1) 35%,
    transparent 35%,
    transparent 45%,
    rgba(255, 248, 220, 0.25) 45%,
    rgba(255, 248, 220, 0.05) 52%,
    transparent 52%,
    transparent 60%,
    rgba(255, 248, 220, 0.2) 60%,
    rgba(255, 248, 220, 0.05) 68%,
    transparent 68%
  );
  filter: blur(20px);
  mix-blend-mode: overlay;
}
```

### Animated Ray Rotation

```css
.rotating-rays {
  animation: rays-rotate 120s linear infinite;
}

@keyframes rays-rotate {
  from { transform: translateX(-50%) rotate(0deg); }
  to { transform: translateX(-50%) rotate(360deg); }
}
```

---

## SECTION I: LENS FLARE & CAMERA EFFECTS

### Radial Gradient Lens Flare

```css
.lens-flare-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.flare-source {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 240, 200, 0.8) 20%,
    rgba(255, 200, 100, 0.4) 40%,
    transparent 70%
  );
  box-shadow:
    0 0 60px 30px rgba(255, 200, 100, 0.5),
    0 0 120px 60px rgba(255, 150, 50, 0.3);
}

.flare-artifact {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
}

.flare-artifact.hexagon {
  width: 40px;
  height: 40px;
  background: radial-gradient(
    circle,
    rgba(100, 200, 255, 0.4) 0%,
    rgba(100, 200, 255, 0.1) 50%,
    transparent 70%
  );
  clip-path: polygon(
    50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%
  );
}

.flare-artifact.streak {
  width: 200px;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 200, 150, 0.6) 30%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(255, 200, 150, 0.6) 70%,
    transparent 100%
  );
  transform-origin: center;
}

.flare-artifact.ring {
  width: 100px;
  height: 100px;
  border: 2px solid rgba(255, 200, 150, 0.2);
  background: transparent;
}
```

### Anamorphic Flare (Cinematic)

```css
.anamorphic-flare {
  position: absolute;
  width: 100%;
  height: 4px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(100, 180, 255, 0.3) 20%,
    rgba(255, 255, 255, 0.6) 50%,
    rgba(100, 180, 255, 0.3) 80%,
    transparent 100%
  );
  filter: blur(2px);
  animation: anamorphic-pulse 4s ease-in-out infinite;
}

@keyframes anamorphic-pulse {
  0%, 100% {
    opacity: 0.4;
    transform: translateY(-50%) scaleX(0.8);
  }
  50% {
    opacity: 0.7;
    transform: translateY(-50%) scaleX(1.2);
  }
}
```

### Dynamic Flare Following Mouse

```javascript
function createDynamicFlare(container, sourcePosition) {
  const center = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
  const direction = {
    x: center.x - sourcePosition.x,
    y: center.y - sourcePosition.y
  };

  // Create artifacts along the flare line
  const artifactCount = 5;
  for (let i = 0; i < artifactCount; i++) {
    const t = (i + 1) / (artifactCount + 1);
    const artifact = document.createElement('div');
    artifact.className = 'flare-artifact hexagon';
    artifact.style.left = `${sourcePosition.x + direction.x * t * 1.5}px`;
    artifact.style.top = `${sourcePosition.y + direction.y * t * 1.5}px`;
    artifact.style.opacity = 0.3 - (i * 0.05);
    artifact.style.transform = `scale(${1 - i * 0.15})`;
    container.appendChild(artifact);
  }
}
```

---

## SECTION J: OCEAN SPRAY & SPLASH

### Particle-Based Spray

```css
.spray-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%;
  overflow: hidden;
  pointer-events: none;
}

.spray-particle {
  position: absolute;
  width: var(--size, 4px);
  height: var(--size, 4px);
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(200, 230, 255, 0.6) 50%,
    transparent 100%
  );
  animation: spray-rise var(--duration, 1s) ease-out forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes spray-rise {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0.8;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) translateX(var(--drift, 20px)) scale(0.3);
    opacity: 0;
  }
}
```

### Spray Generator

```javascript
function createSpray(container, intensity = 'medium') {
  const config = {
    light: { count: 20, maxSize: 6, maxDuration: 1.2 },
    medium: { count: 50, maxSize: 10, maxDuration: 1.5 },
    heavy: { count: 100, maxSize: 15, maxDuration: 2 }
  }[intensity];

  for (let i = 0; i < config.count; i++) {
    const particle = document.createElement('div');
    particle.className = 'spray-particle';
    particle.style.setProperty('--size', `${2 + Math.random() * config.maxSize}px`);
    particle.style.setProperty('--duration', `${0.5 + Math.random() * config.maxDuration}s`);
    particle.style.setProperty('--delay', `${Math.random() * 0.5}s`);
    particle.style.setProperty('--drift', `${(Math.random() - 0.5) * 60}px`);
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.bottom = '0';
    container.appendChild(particle);

    // Remove after animation
    setTimeout(() => particle.remove(), (0.5 + config.maxDuration) * 1000 + 500);
  }
}
```

### Impact Splash Ring

```css
.splash-ring {
  position: absolute;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.6);
  background: transparent;
  animation: splash-expand 0.8s ease-out forwards;
}

@keyframes splash-expand {
  0% {
    width: 10px;
    height: 10px;
    opacity: 1;
    transform: translate(-50%, -50%) rotateX(70deg);
  }
  100% {
    width: 150px;
    height: 150px;
    opacity: 0;
    transform: translate(-50%, -50%) rotateX(70deg);
  }
}
```

---

## SECTION K: BEACH WASH & FOAM

### Shore Wash Animation

```svg
<svg class="beach-wave" viewBox="0 0 1440 200" preserveAspectRatio="none">
  <defs>
    <linearGradient id="foam-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(255,255,255,0.9)" />
      <stop offset="30%" stop-color="rgba(200,230,255,0.6)" />
      <stop offset="100%" stop-color="rgba(56,189,248,0.4)" />
    </linearGradient>

    <filter id="foam-texture">
      <feTurbulence type="turbulence" baseFrequency="0.02 0.05" numOctaves="3" />
      <feDisplacementMap in="SourceGraphic" scale="5" />
    </filter>
  </defs>

  <path
    class="wave-foam"
    fill="url(#foam-gradient)"
    filter="url(#foam-texture)"
  >
    <animate
      attributeName="d"
      dur="4s"
      repeatCount="indefinite"
      values="
        M0,100 Q360,50 720,100 T1440,100 L1440,200 L0,200 Z;
        M0,80 Q360,130 720,80 T1440,80 L1440,200 L0,200 Z;
        M0,100 Q360,50 720,100 T1440,100 L1440,200 L0,200 Z
      "
    />
  </path>
</svg>
```

```css
.beach-container {
  position: relative;
  height: 300px;
  overflow: hidden;
}

.wet-sand {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(
    to top,
    #c2b280 0%,
    #d4c896 50%,
    #e6dbb0 100%
  );
}

.wet-sand::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(56, 189, 248, 0.2);
  animation: wet-recede 4s ease-in-out infinite;
}

@keyframes wet-recede {
  0%, 100% {
    clip-path: polygon(0 0, 100% 0, 100% 80%, 0 60%);
  }
  50% {
    clip-path: polygon(0 30%, 100% 50%, 100% 100%, 0 100%);
  }
}
```

### Foam Bubble Details

```css
.foam-bubbles {
  position: absolute;
  width: 100%;
  height: 30px;
  bottom: 60px;
}

.foam-bubble {
  position: absolute;
  width: var(--size, 8px);
  height: var(--size, 8px);
  border-radius: 50%;
  background: radial-gradient(
    circle at 30% 30%,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(200, 230, 255, 0.5) 50%,
    transparent 100%
  );
  animation: bubble-pop var(--duration, 2s) ease-out infinite;
  animation-delay: var(--delay, 0s);
}

@keyframes bubble-pop {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  80% {
    transform: scale(1.1);
    opacity: 0.6;
  }
  100% {
    transform: scale(0);
    opacity: 0;
  }
}
```

### Receding Wave Trail

```css
.wave-trail {
  position: absolute;
  bottom: 60px;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.6) 10%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(255, 255, 255, 0.6) 90%,
    transparent 100%
  );
  animation: trail-recede 4s ease-in-out infinite;
}

@keyframes trail-recede {
  0% {
    transform: translateY(0) scaleX(1);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-30px) scaleX(0.95);
    opacity: 0.4;
  }
  100% {
    transform: translateY(0) scaleX(1);
    opacity: 0.8;
  }
}
```

---

## SECTION L: PERFORMANCE OPTIMIZATION

### Performance Tiers

```css
/* Tier 1: Ultra Performance (CSS-only) */
@media (prefers-reduced-motion: reduce) {
  .weather-effect {
    animation: none !important;
    filter: none !important;
  }
}

/* Tier 2: High Performance (static filters) */
.weather-effect--performance {
  filter: url(#static-filter);
  animation-play-state: paused;
}

/* Tier 3: Full Effects */
.weather-effect--full {
  filter: url(#animated-filter);
  animation-play-state: running;
}
```

### GPU Acceleration

```css
.weather-layer {
  /* Force GPU compositing */
  will-change: transform, opacity;
  transform: translateZ(0);
  backface-visibility: hidden;

  /* Avoid triggering repaints */
  contain: layout paint;
}

/* Avoid animating these properties */
.weather-layer {
  /* BAD: causes repaints */
  /* animation: filter-change 10s; */

  /* GOOD: GPU-accelerated */
  animation: transform-change 10s;
}
```

### Intersection Observer for Off-Screen

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const effect = entry.target;
    if (entry.isIntersecting) {
      effect.classList.add('weather-effect--active');
    } else {
      effect.classList.remove('weather-effect--active');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.weather-effect').forEach(el => observer.observe(el));
```

### Mobile Optimization

```css
@media (max-width: 768px) {
  /* Reduce layer count on mobile */
  .cloud-back,
  .fog-back {
    display: none;
  }

  /* Simplify filters */
  .weather-filter {
    filter: blur(var(--blur)) opacity(0.5);
  }

  /* Reduce particle count */
  .rain-container {
    --drop-count: 50;
  }
}
```

---

## SECTION M: REACT INTEGRATION

### Weather Effect Provider

```tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

type WeatherType =
  | 'clear'
  | 'cloudy'
  | 'rainy'
  | 'stormy'
  | 'foggy'
  | 'snowy'
  | 'aurora';

type TimeOfDay = 'dawn' | 'morning' | 'noon' | 'afternoon' | 'dusk' | 'night';

interface WeatherContextType {
  weather: WeatherType;
  timeOfDay: TimeOfDay;
  intensity: number; // 0-1
  setWeather: (w: WeatherType) => void;
  setTimeOfDay: (t: TimeOfDay) => void;
  setIntensity: (i: number) => void;
}

const WeatherContext = createContext<WeatherContextType | null>(null);

export function WeatherProvider({ children }: { children: React.ReactNode }) {
  const [weather, setWeather] = useState<WeatherType>('clear');
  const [timeOfDay, setTimeOfDay] = useState<TimeOfDay>('noon');
  const [intensity, setIntensity] = useState(0.5);

  // Auto-detect time of day
  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 7) setTimeOfDay('dawn');
    else if (hour >= 7 && hour < 12) setTimeOfDay('morning');
    else if (hour >= 12 && hour < 14) setTimeOfDay('noon');
    else if (hour >= 14 && hour < 17) setTimeOfDay('afternoon');
    else if (hour >= 17 && hour < 20) setTimeOfDay('dusk');
    else setTimeOfDay('night');
  }, []);

  return (
    <WeatherContext.Provider value={{
      weather, timeOfDay, intensity,
      setWeather, setTimeOfDay, setIntensity
    }}>
      {children}
    </WeatherContext.Provider>
  );
}

export const useWeather = () => {
  const context = useContext(WeatherContext);
  if (!context) throw new Error('useWeather must be used within WeatherProvider');
  return context;
};
```

### Atmospheric Canvas Component

```tsx
import React from 'react';
import { useWeather } from './WeatherProvider';
import { CloudLayer } from './CloudLayer';
import { RainEffect } from './RainEffect';
import { LightningEffect } from './LightningEffect';
import { FogLayer } from './FogLayer';
import { AuroraEffect } from './AuroraEffect';
import { SkyGradient } from './SkyGradient';

export function AtmosphericCanvas() {
  const { weather, timeOfDay, intensity } = useWeather();

  return (
    <div className="atmospheric-canvas">
      {/* SVG Filters */}
      <svg width="0" height="0" aria-hidden="true">
        <defs>
          <filter id="cloud-filter">...</filter>
          <filter id="fog-filter">...</filter>
          <filter id="wave-filter">...</filter>
        </defs>
      </svg>

      {/* Sky base */}
      <SkyGradient timeOfDay={timeOfDay} />

      {/* Weather layers */}
      {(weather === 'cloudy' || weather === 'rainy' || weather === 'stormy') && (
        <CloudLayer variant={weather === 'stormy' ? 'storm' : 'cumulus'} />
      )}

      {weather === 'foggy' && <FogLayer intensity={intensity} />}

      {weather === 'aurora' && <AuroraEffect intensity={intensity} />}

      {(weather === 'rainy' || weather === 'stormy') && (
        <RainEffect intensity={weather === 'stormy' ? 1 : intensity} />
      )}

      {weather === 'stormy' && <LightningEffect frequency={intensity} />}
    </div>
  );
}
```

### Individual Effect Components

```tsx
// CloudLayer.tsx
interface CloudLayerProps {
  variant: 'cumulus' | 'cirrus' | 'stratus' | 'storm';
  opacity?: number;
}

export function CloudLayer({ variant, opacity = 0.7 }: CloudLayerProps) {
  const configs = {
    cumulus: { baseFrequency: 0.008, blur: 4, layers: 3 },
    cirrus: { baseFrequency: 0.003, blur: 2, layers: 2 },
    stratus: { baseFrequency: 0.015, blur: 6, layers: 2 },
    storm: { baseFrequency: 0.006, blur: 3, layers: 4 }
  };

  const config = configs[variant];

  return (
    <div className="cloud-system" style={{ '--opacity': opacity } as React.CSSProperties}>
      {Array.from({ length: config.layers }, (_, i) => (
        <div
          key={i}
          className={`cloud-layer cloud-layer-${i}`}
          style={{
            '--layer-index': i,
            '--animation-duration': `${50 + i * 30}s`
          } as React.CSSProperties}
        />
      ))}
    </div>
  );
}
```

---

## SECTION N: TAILWIND INTEGRATION

### Custom Tailwind Utilities

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'drift': 'drift 60s linear infinite',
        'drift-slow': 'drift 120s linear infinite',
        'drift-fast': 'drift 30s linear infinite',
        'wave': 'wave 10s ease-in-out infinite',
        'rain-fall': 'rain-fall 0.8s linear infinite',
        'lightning': 'lightning-flash 0.5s ease-out',
        'aurora': 'aurora-wave 15s ease-in-out infinite',
        'fog-breathe': 'fog-breathe 8s ease-in-out infinite',
      },
      keyframes: {
        drift: {
          '0%': { transform: 'translateX(-10%)' },
          '100%': { transform: 'translateX(10%)' },
        },
        wave: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'rain-fall': {
          '0%': { transform: 'translateY(-100vh)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        'lightning-flash': {
          '0%': { opacity: '0' },
          '10%': { opacity: '1' },
          '20%': { opacity: '0.5' },
          '30%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        'aurora-wave': {
          '0%, 100%': { transform: 'translateX(-20%) skewX(-5deg)', opacity: '0.4' },
          '50%': { transform: 'translateX(0%) skewX(5deg)', opacity: '0.7' },
        },
        'fog-breathe': {
          '0%, 100%': { opacity: '0.5', transform: 'scaleY(1)' },
          '50%': { opacity: '0.7', transform: 'scaleY(1.1)' },
        },
      },
      backdropBlur: {
        'fog': '20px',
        'mist': '10px',
      },
    },
  },
  plugins: [
    function({ addUtilities }) {
      addUtilities({
        '.filter-cloud': {
          filter: 'url(#cloud-filter)',
        },
        '.filter-fog': {
          filter: 'url(#fog-filter)',
        },
        '.filter-wave': {
          filter: 'url(#wave-filter)',
        },
        '.mix-screen': {
          mixBlendMode: 'screen',
        },
        '.mix-overlay': {
          mixBlendMode: 'overlay',
        },
      });
    },
  ],
};
```

### Tailwind Component Classes

```html
<!-- Cloud layer -->
<div class="absolute inset-0 opacity-50 filter-cloud animate-drift-slow"></div>

<!-- Rain container -->
<div class="absolute inset-0 overflow-hidden pointer-events-none">
  <div class="w-0.5 h-5 bg-gradient-to-b from-transparent via-sky-200/50 to-sky-300/80 rounded-b animate-rain-fall"></div>
</div>

<!-- Fog overlay -->
<div class="absolute inset-0 bg-white/30 backdrop-blur-fog filter-fog animate-fog-breathe"></div>

<!-- Aurora band -->
<div class="absolute top-1/4 -left-1/2 w-[200%] h-2/5 opacity-60 mix-screen blur-3xl animate-aurora bg-gradient-to-r from-transparent via-emerald-400/40 to-transparent"></div>
```

---

## Quick Reference Card

### Effect Selection Matrix

| Effect | Best For | Complexity | Performance |
|--------|----------|------------|-------------|
| **Clouds** | Hero sections, headers | Medium | High |
| **Waves** | Footers, section dividers | Medium | High |
| **Lightning** | Dramatic moments, gaming | Low | Very High |
| **Rain** | Mood, atmosphere | Medium | Medium |
| **Fog** | Mystery, depth | Low | High |
| **Aurora** | Night scenes, magical | High | Medium |
| **God rays** | Divine, cinematic | Low | High |
| **Lens flare** | Realistic, photography | Medium | High |
| **Ocean spray** | Beach, action | High | Low |
| **Beach wash** | Coastal, calm | Medium | Medium |
| **Twilight sky** | Time indication | Low | Very High |

### Common Combinations

| Scene | Effects | Notes |
|-------|---------|-------|
| **Dramatic storm** | Storm clouds + Rain + Lightning | Stagger lightning timing |
| **Peaceful beach** | Light clouds + Beach wash + God rays | Slow animations |
| **Foggy morning** | Fog + Ground mist + Soft clouds | Reduce saturation |
| **Northern night** | Aurora + Stars + Light fog | Dark background essential |
| **Cinematic moment** | God rays + Lens flare + Light haze | Don't overdo flares |

### Performance Budget

| Device | Max Layers | Max Particles | Filter Complexity |
|--------|------------|---------------|-------------------|
| Desktop | 5-7 | 200 | Full |
| Tablet | 3-5 | 100 | Simplified |
| Mobile | 2-3 | 50 | Minimal |

---

## Resources & References

### Tutorials Referenced
- [CSS-Tricks: Lens Flare](https://css-tricks.com/add-a-css-lens-flare-to-photos-for-a-bright-touch/)
- [Red Stapler: SVG Water Turbulence](https://redstapler.co/realistic-water-effect-svg-turbulence-filter/)
- [CSS In Real Life: Animated Sun with God Rays](https://css-irl.info/heatwave-animated-sun-illustration/)
- [Pyxofy: Sunset Animation](https://www.pyxofy.com/css-art-how-to-make-a-sunset-scene/)
- [Medium: God Rays with Sass](https://medium.com/@rcbat73/how-to-create-god-rays-effect-with-html-and-css-sass-65af0c436788)

### Tools
- [Magic Pattern: God Rays Generator](https://www.magicpattern.design/tools/god-rays-generator)
- [UI Surgeon: CSS Wave Generator](https://uisurgeon.com/tools/css-wave-generator)
- [uiGradients: Sky Gradients](https://uigradients.com/)
- [iColorPalette: Sunset Gradients](https://icolorpalette.com/gradients/sunset-gradients)

### Code Collections
- [CodePen: Fog Tag](https://codepen.io/tag/fog)
- [FreeFrontend: CSS Water Effects](https://freefrontend.com/css-water-effects/)
- [DevSnap: CSS Water Effects](https://devsnap.me/css-water-effects)
- [GitHub: CSS FOG ANIMATION](https://github.com/danielstuart14/CSS_FOG_ANIMATION)

---

## Version History

- **v1.0.0** (2026-01-25): Merged from web-cloud-designer + web-wave-designer, added lightning, rain, fog, twilight, aurora, god rays, lens flare, ocean spray, beach wash effects

---

*Remember: Stylized weather effects are about **restraint and layering**. One well-crafted effect beats five mediocre ones. When in doubt, reduce intensity and increase subtlety.*
