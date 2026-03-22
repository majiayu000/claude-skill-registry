---
name: web-wave-designer
description: Creates realistic ocean and water wave effects for web using SVG filters (feTurbulence, feDisplacementMap), CSS animations, and layering techniques. Use for ocean backgrounds, underwater distortion, beach scenes, ripple effects, liquid glass, and water-themed UI. Activate on "ocean wave", "water effect", "SVG water", "ripple animation", "underwater distortion", "liquid glass", "wave animation", "feTurbulence water", "beach waves", "sea foam". NOT for 3D ocean simulation (use WebGL/Three.js), video water effects (use video editing), physics-based fluid simulation (use canvas/WebGL), or simple gradient backgrounds without wave motion.
allowed-tools: Read,Write,Edit,WebFetch,Bash
category: Design & Creative
tags:
  - svg
  - css
  - animation
  - water
  - ocean
  - visual-effects
  - web
pairs-with:
  - skill: web-cloud-designer
    reason: Complete atmospheric scenes with sky and water
  - skill: physics-rendering-expert
    reason: Realistic light refraction and caustics
  - skill: color-theory-palette-harmony-expert
    reason: Ocean palettes and depth gradients
  - skill: web-design-expert
    reason: Integrate water effects into overall web design
---

# Web Wave Designer

Expert in creating realistic, performant ocean and water wave effects for web applications using SVG filters, CSS animations, and layering techniques. Specializes in aquatic visuals from gentle ripples to dramatic ocean swells, with particular expertise in the physics of light refraction through water.

## When to Use This Skill

**Use for:**
- Ocean wave backgrounds and seascapes
- Underwater distortion/refraction effects
- Beach shore waves with foam
- Pond/pool ripple animations
- Liquid glass UI effects
- Water-themed loading states
- Parallax ocean layers with depth
- Stylized/cartoon water for games
- Reflection effects on water surfaces

**Do NOT use for:**
- 3D volumetric ocean rendering -> use **WebGL/Three.js/Ocean.js**
- Real-time fluid simulation -> use **canvas physics engines**
- Video effects -> use video editing software
- Simple blue gradients without motion
- Water droplet physics -> use particle systems

## Core Distinction: turbulence vs fractalNoise

**CRITICAL**: For water effects, use `type="turbulence"` (NOT fractalNoise like clouds):

| Type | Visual | Best For |
|------|--------|----------|
| `turbulence` | Continuous flow patterns, starts from transparent black | **Water, waves, liquid** |
| `fractalNoise` | Random cloudlike patches, opaque | Clouds, smoke, terrain |

```xml
<!-- WATER - use turbulence -->
<feTurbulence type="turbulence" baseFrequency="0.01 0.1" />

<!-- CLOUDS - use fractalNoise -->
<feTurbulence type="fractalNoise" baseFrequency="0.01" />
```

## SVG Filter Pipeline for Water

The fundamental water effect filter chain:

```
Source -> feTurbulence -> feDisplacementMap -> feComponentTransfer -> feComposite
            (waves)        (distortion)         (color/opacity)      (blend)
```

### 1. feTurbulence - Wave Pattern Generation

```xml
<feTurbulence
  type="turbulence"           <!-- MUST be turbulence for water -->
  baseFrequency="0.01 0.1"    <!-- TWO values: x-freq y-freq -->
  numOctaves="3"              <!-- 2-5: wave complexity -->
  seed="42"                   <!-- Variation (free performance) -->
  result="waves"
/>
```

**baseFrequency Explained (TWO Values):**

| X-Frequency | Y-Frequency | Result |
|-------------|-------------|--------|
| 0.01 | 0.1 | Long horizontal waves with vertical oscillation |
| 0.005 | 0.05 | Deep ocean swells |
| 0.02 | 0.15 | Choppy surface waves |
| 0.03 | 0.03 | Square ripples (pond) |

The ratio matters:
- **X << Y**: Stretched horizontal waves (ocean)
- **X == Y**: Circular ripples (pond, pool)
- **X >> Y**: Vertical striations (waterfall)

### 2. feDisplacementMap - Refraction Effect

Creates the bending/distortion that makes content behind water appear to ripple.

```xml
<feDisplacementMap
  in="SourceGraphic"          <!-- What gets distorted -->
  in2="waves"                 <!-- Distortion pattern (from turbulence) -->
  scale="20"                  <!-- 10-40 for realistic refraction -->
  xChannelSelector="R"        <!-- Which color channel drives X displacement -->
  yChannelSelector="G"        <!-- Which color channel drives Y displacement -->
  result="refracted"
/>
```

| Scale Value | Effect |
|-------------|--------|
| 10-15 | Gentle pool ripples |
| 15-25 | Standard water refraction |
| 25-40 | Strong wave distortion |
| 40+ | Psychedelic (unrealistic) |

### 3. feComponentTransfer - Water Color

Transform noise into water-like colors by manipulating channels.

```xml
<feComponentTransfer in="waves" result="waterColor">
  <feFuncR type="linear" slope="0.3" intercept="0"/>     <!-- Reduce red -->
  <feFuncG type="linear" slope="0.7" intercept="0.2"/>   <!-- Boost green -->
  <feFuncB type="linear" slope="1.2" intercept="0.3"/>   <!-- Strong blue -->
  <feFuncA type="linear" slope="0.6" intercept="0.3"/>   <!-- Water opacity -->
</feComponentTransfer>
```

### 4. feGaussianBlur - Caustics (Underwater Light)

```xml
<feGaussianBlur
  in="waves"
  stdDeviation="2"            <!-- 1-5 for soft caustic patterns -->
  result="caustics"
/>
```

### 5. Compositing - Layer Assembly

```xml
<feFlood flood-color="#0077be" flood-opacity="0.4" result="baseWater"/>
<feBlend in="caustics" in2="baseWater" mode="screen" result="waterLayer"/>
<feComposite in="waterLayer" in2="SourceGraphic" operator="over"/>
```

## Wave Type Recipes

### Ocean Surface Waves

```svg
<svg width="100%" height="300">
  <defs>
    <filter id="oceanWaves" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="turbulence"
                    baseFrequency="0.005 0.05"
                    numOctaves="4"
                    seed="1"
                    result="waves">
        <animate attributeName="baseFrequency"
                 dur="60s"
                 values="0.005 0.05;0.007 0.06;0.005 0.05"
                 repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" in2="waves" scale="25"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="url(#oceanGradient)" filter="url(#oceanWaves)"/>
</svg>
```

### Pond Ripples (Circular)

```svg
<filter id="pondRipples">
  <feTurbulence type="turbulence"
                baseFrequency="0.02 0.02"  <!-- Equal = circular -->
                numOctaves="2"
                seed="10"
                result="ripples"/>
  <feDisplacementMap in="SourceGraphic" in2="ripples" scale="12"/>
</filter>
```

### Beach Shore Waves (Breaking)

```svg
<filter id="shoreWaves">
  <feTurbulence type="turbulence"
                baseFrequency="0.008 0.12"  <!-- Strong vertical motion -->
                numOctaves="3"
                seed="5"
                result="waves"/>
  <feGaussianBlur in="waves" stdDeviation="1.5" result="softWaves"/>
  <feDisplacementMap in="SourceGraphic" in2="softWaves" scale="30"/>
  <!-- Add foam layer -->
  <feTurbulence type="fractalNoise"
                baseFrequency="0.03"
                numOctaves="5"
                result="foam"/>
  <feColorMatrix in="foam" type="matrix"
                 values="1 0 0 0 0.9
                         1 0 0 0 0.95
                         1 0 0 0 1
                         0 0 0 0.3 0"/>
</filter>
```

### Underwater Distortion (Looking Through Water)

```svg
<filter id="underwater" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="turbulence"
                baseFrequency="0.015 0.08"
                numOctaves="3"
                result="distort">
    <animate attributeName="baseFrequency"
             dur="8s"
             values="0.015 0.08;0.018 0.09;0.015 0.08"
             repeatCount="indefinite"/>
  </feTurbulence>
  <feDisplacementMap in="SourceGraphic" in2="distort"
                     scale="20"
                     xChannelSelector="R"
                     yChannelSelector="B"/>
  <!-- Slight blue tint -->
  <feColorMatrix type="matrix"
                 values="0.9 0 0 0 0
                         0 0.95 0 0 0.02
                         0 0 1.1 0 0.05
                         0 0 0 1 0"/>
</filter>
```

### Liquid Glass Effect (Modern UI)

```svg
<filter id="liquidGlass" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="turbulence"
                baseFrequency="0.01 0.05"
                numOctaves="2"
                seed="99"
                result="ripple">
    <animate attributeName="seed"
             dur="4s"
             values="99;100;101;100;99"
             repeatCount="indefinite"/>
  </feTurbulence>
  <feDisplacementMap in="SourceGraphic" in2="ripple" scale="8"/>
  <!-- Frosted glass blur -->
  <feGaussianBlur stdDeviation="0.5"/>
</filter>
```

### Stylized/Cartoon Waves

```svg
<filter id="cartoonWater">
  <feTurbulence type="turbulence"
                baseFrequency="0.02 0.08"
                numOctaves="1"  <!-- Low octaves = bold shapes -->
                result="waves"/>
  <feDisplacementMap in="SourceGraphic" in2="waves" scale="15"/>
  <!-- Sharp edges, no blur -->
</filter>
```

## Animation Techniques

### JavaScript requestAnimationFrame (Smoothest)

```javascript
const turbulence = document.querySelector('#seaFilter feTurbulence');
let frame = 0;

function animateWaves() {
  frame += 0.003;

  // Gentle breathing motion
  const xFreq = 0.006 + Math.sin(frame) * 0.002;
  const yFreq = 0.05 + Math.sin(frame * 0.7) * 0.01;

  turbulence.setAttribute('baseFrequency', `${xFreq} ${yFreq}`);
  requestAnimationFrame(animateWaves);
}

animateWaves();
```

### SVG animate (Declarative, CPU-Heavy)

```xml
<feTurbulence baseFrequency="0.01 0.1" numOctaves="3">
  <animate
    attributeName="baseFrequency"
    dur="60s"
    keyTimes="0;0.5;1"
    values="0.008 0.08;0.012 0.12;0.008 0.08"
    repeatCount="indefinite"
  />
</feTurbulence>
```

**WARNING**: SVG animate on filter attributes forces full filter recalculation every frame. Use sparingly.

### CSS Transform Animation (Best Performance)

Move the water element, not the filter:

```css
.wave-layer {
  animation: wave-drift 20s linear infinite;
}

@keyframes wave-drift {
  from { transform: translateX(0) translateY(0); }
  to { transform: translateX(-50%) translateY(5px); }
}
```

### Seed Animation (Morphing Waves)

Animate seed for shape variation without baseFrequency cost:

```xml
<feTurbulence baseFrequency="0.01 0.1">
  <animate
    attributeName="seed"
    dur="20s"
    values="1;50;100;50;1"
    repeatCount="indefinite"
  />
</feTurbulence>
```

## Layering Strategy

### Multi-Layer Ocean

```html
<div class="ocean">
  <div class="wave wave-back"></div>
  <div class="wave wave-mid"></div>
  <div class="wave wave-front"></div>
  <div class="foam-layer"></div>
</div>
```

```css
.ocean {
  position: relative;
  height: 100vh;
  background: linear-gradient(180deg,
    #0c4a6e 0%,
    #0369a1 40%,
    #0ea5e9 100%
  );
  overflow: hidden;
}

.wave {
  position: absolute;
  width: 200%;
  height: 100%;
  background: rgba(255,255,255,0.1);
}

.wave-back {
  filter: url(#waveBack);
  opacity: 0.3;
  animation: drift 90s linear infinite;
  bottom: 0;
}

.wave-mid {
  filter: url(#waveMid);
  opacity: 0.5;
  animation: drift 60s linear infinite;
  bottom: -5%;
}

.wave-front {
  filter: url(#waveFront);
  opacity: 0.7;
  animation: drift 35s linear infinite;
  bottom: -10%;
}

.foam-layer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 20%;
  background: linear-gradient(to top,
    rgba(255,255,255,0.8) 0%,
    transparent 100%
  );
  filter: url(#foamFilter);
}

@keyframes drift {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
```

### Layer Parameter Guide

| Layer | Opacity | Speed | Filter Scale | baseFrequency |
|-------|---------|-------|--------------|---------------|
| Back (deep) | 0.2-0.4 | 80-100s | 15 | 0.004 0.04 |
| Mid | 0.4-0.6 | 50-70s | 20 | 0.006 0.06 |
| Front (surface) | 0.6-0.8 | 30-45s | 25 | 0.01 0.1 |
| Foam | 0.7-0.9 | 25-35s | 10 | 0.02 0.02 |

## Color Palettes

### Deep Ocean

```css
.deep-ocean {
  background: linear-gradient(180deg,
    #0c4a6e 0%,    /* Deep blue */
    #075985 30%,
    #0369a1 60%,
    #0284c7 100%   /* Surface shimmer */
  );
}
```
- Primary: `#0369a1`
- Deep: `#0c4a6e`
- Highlight: `#38bdf8`

### Tropical/Caribbean

```css
.tropical {
  background: linear-gradient(180deg,
    #06b6d4 0%,    /* Cyan surface */
    #22d3ee 40%,
    #67e8f9 70%,
    #a5f3fc 100%   /* Shallow sand reflection */
  );
}
```
- Primary: `#06b6d4`
- Shallow: `#67e8f9`
- Foam: `#ecfeff`

### Stormy Sea

```css
.stormy {
  background: linear-gradient(180deg,
    #1e293b 0%,    /* Dark clouds */
    #334155 30%,
    #475569 60%,
    #64748b 100%   /* Whitecaps */
  );
}
```
- Primary: `#475569`
- Depth: `#1e293b`
- Whitecap: `#cbd5e1`

### Sunset Reflection

```css
.sunset-water {
  background: linear-gradient(180deg,
    #831843 0%,    /* Pink sky */
    #9d174d 20%,
    #be185d 40%,
    #0369a1 60%,   /* Water starts */
    #0c4a6e 100%
  );
}
```

## Complete Implementation Templates

### Template 1: Full Ocean Scene

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .ocean-scene {
      position: relative;
      width: 100%;
      height: 100vh;
      background: linear-gradient(180deg,
        #87CEEB 0%,    /* Sky */
        #87CEEB 40%,
        #0369a1 40%,   /* Horizon */
        #0c4a6e 100%   /* Deep */
      );
      overflow: hidden;
    }

    .horizon-line {
      position: absolute;
      top: 40%;
      left: 0;
      right: 0;
      height: 2px;
      background: rgba(255,255,255,0.3);
    }

    .wave {
      position: absolute;
      width: 200%;
      height: 60%;
      bottom: 0;
      background: rgba(255,255,255,0.15);
    }

    .wave-1 {
      filter: url(#wave1);
      animation: drift 80s linear infinite;
      opacity: 0.4;
    }

    .wave-2 {
      filter: url(#wave2);
      animation: drift 55s linear infinite;
      animation-delay: -20s;
      opacity: 0.6;
    }

    .wave-3 {
      filter: url(#wave3);
      animation: drift 35s linear infinite;
      animation-delay: -10s;
      opacity: 0.8;
    }

    @keyframes drift {
      from { transform: translateX(0); }
      to { transform: translateX(-50%); }
    }
  </style>
</head>
<body>
  <svg style="position:absolute;width:0;height:0">
    <defs>
      <filter id="wave1" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="turbulence" baseFrequency="0.004 0.04" numOctaves="3" seed="1"/>
        <feDisplacementMap in="SourceGraphic" scale="15"/>
      </filter>
      <filter id="wave2" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="turbulence" baseFrequency="0.006 0.06" numOctaves="3" seed="2"/>
        <feDisplacementMap in="SourceGraphic" scale="20"/>
      </filter>
      <filter id="wave3" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="turbulence" baseFrequency="0.01 0.1" numOctaves="4" seed="3"/>
        <feDisplacementMap in="SourceGraphic" scale="25"/>
      </filter>
    </defs>
  </svg>

  <div class="ocean-scene">
    <div class="horizon-line"></div>
    <div class="wave wave-1"></div>
    <div class="wave wave-2"></div>
    <div class="wave wave-3"></div>
  </div>
</body>
</html>
```

### Template 2: Underwater View (Content Behind Water)

```html
<style>
  .underwater-container {
    position: relative;
    width: 100%;
    overflow: hidden;
  }

  .content-behind-water {
    /* Your actual content */
  }

  .water-overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    filter: url(#underwaterDistort);
  }

  .caustics {
    position: absolute;
    inset: 0;
    background: url('data:image/svg+xml,...') repeat;
    opacity: 0.3;
    mix-blend-mode: overlay;
    animation: caustic-shift 10s linear infinite;
  }

  @keyframes caustic-shift {
    from { background-position: 0 0; }
    to { background-position: 100px 50px; }
  }
</style>

<svg style="display:none">
  <defs>
    <filter id="underwaterDistort" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence id="underwaterTurb" type="turbulence"
                    baseFrequency="0.015 0.08" numOctaves="3"/>
      <feDisplacementMap in="SourceGraphic" scale="20"
                         xChannelSelector="R" yChannelSelector="B"/>
      <feColorMatrix type="matrix"
                     values="0.85 0 0 0 0
                             0 0.9 0 0 0.02
                             0 0 1.1 0 0.08
                             0 0 0 1 0"/>
    </filter>
  </defs>
</svg>

<script>
  // Animate underwater distortion
  const turb = document.getElementById('underwaterTurb');
  let frame = 0;

  function animate() {
    frame += 0.005;
    const xFreq = 0.015 + Math.sin(frame) * 0.003;
    const yFreq = 0.08 + Math.sin(frame * 0.7) * 0.01;
    turb.setAttribute('baseFrequency', `${xFreq} ${yFreq}`);
    requestAnimationFrame(animate);
  }
  animate();
</script>
```

### Template 3: React Water Component

```tsx
import React, { useEffect, useRef, useMemo } from 'react';

interface WaterEffectProps {
  type?: 'ocean' | 'pool' | 'stream' | 'glass';
  intensity?: 'subtle' | 'medium' | 'strong';
  animate?: boolean;
  className?: string;
  children?: React.ReactNode;
}

const WATER_CONFIGS = {
  ocean: { baseFreq: [0.008, 0.08], octaves: 4, scale: 25 },
  pool: { baseFreq: [0.02, 0.02], octaves: 2, scale: 12 },
  stream: { baseFreq: [0.01, 0.15], octaves: 3, scale: 20 },
  glass: { baseFreq: [0.01, 0.05], octaves: 2, scale: 8 },
};

const INTENSITY_MULTIPLIERS = {
  subtle: 0.5,
  medium: 1.0,
  strong: 1.5,
};

export const WaterEffect: React.FC<WaterEffectProps> = ({
  type = 'ocean',
  intensity = 'medium',
  animate = true,
  className,
  children
}) => {
  const turbRef = useRef<SVGFETurbulenceElement>(null);
  const frameRef = useRef(0);
  const config = WATER_CONFIGS[type];
  const mult = INTENSITY_MULTIPLIERS[intensity];

  const filterId = useMemo(() =>
    `water-${type}-${Date.now()}`, [type]
  );

  useEffect(() => {
    if (!animate || !turbRef.current) return;

    let animationId: number;

    const animateWater = () => {
      frameRef.current += 0.004;
      const frame = frameRef.current;

      const xFreq = config.baseFreq[0] + Math.sin(frame) * 0.002;
      const yFreq = config.baseFreq[1] + Math.sin(frame * 0.7) * 0.01;

      turbRef.current?.setAttribute('baseFrequency', `${xFreq} ${yFreq}`);
      animationId = requestAnimationFrame(animateWater);
    };

    animateWater();
    return () => cancelAnimationFrame(animationId);
  }, [animate, config]);

  return (
    <>
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <filter id={filterId} x="-10%" y="-10%" width="120%" height="120%">
            <feTurbulence
              ref={turbRef}
              type="turbulence"
              baseFrequency={config.baseFreq.join(' ')}
              numOctaves={config.octaves}
              result="waves"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="waves"
              scale={config.scale * mult}
              xChannelSelector="R"
              yChannelSelector="G"
            />
          </filter>
        </defs>
      </svg>
      <div className={className} style={{ filter: `url(#${filterId})` }}>
        {children}
      </div>
    </>
  );
};

// Usage:
// <WaterEffect type="ocean" intensity="medium" animate>
//   <img src="underwater-scene.jpg" />
// </WaterEffect>
```

### Template 4: CSS-Only Waves (No SVG)

For simple, high-performance waves without SVG filters:

```css
.css-waves {
  position: relative;
  height: 300px;
  background: linear-gradient(180deg, #0369a1 0%, #0c4a6e 100%);
  overflow: hidden;
}

.css-wave {
  position: absolute;
  width: 200%;
  height: 100%;
  bottom: 0;
  left: -50%;
  background:
    radial-gradient(ellipse 100% 50% at 50% 100%,
      rgba(255,255,255,0.3) 0%,
      transparent 60%
    );
  animation: css-wave-move 8s ease-in-out infinite;
  transform-origin: center bottom;
}

.css-wave:nth-child(1) {
  animation-duration: 7s;
  opacity: 0.5;
}

.css-wave:nth-child(2) {
  animation-duration: 10s;
  animation-delay: -3s;
  opacity: 0.3;
}

.css-wave:nth-child(3) {
  animation-duration: 13s;
  animation-delay: -5s;
  opacity: 0.2;
}

@keyframes css-wave-move {
  0%, 100% {
    transform: translateX(0) scaleY(1);
  }
  50% {
    transform: translateX(25%) scaleY(1.1);
  }
}
```

## Performance Optimization

### Critical Rules

1. **Use `type="turbulence"`** - Correct type for water (not fractalNoise)
2. **numOctaves <= 4** - Above 4 minimal visual gain, exponential CPU cost
3. **Scale 10-30** - Above 40 becomes unrealistic and slower
4. **Avoid animating baseFrequency** - Use CSS transforms or seed animation instead
5. **GPU hints** - Add `will-change: transform` on animated layers
6. **Batch SVG defs** - One `<defs>` block, multiple filters

### Performance Tiers

| Tier | Technique | FPS Target | Use Case |
|------|-----------|------------|----------|
| Ultra | CSS radial gradients only | 60fps | Mobile, low-end |
| High | SVG filter, CSS transform animation | 60fps | Background waves |
| Medium | SVG filter + seed animation | 45-60fps | Interactive water |
| Low | SVG filter + baseFrequency animation | 30-40fps | Hero sections only |

### Mobile Optimization

```css
@media (prefers-reduced-motion: reduce) {
  .wave {
    animation: none !important;
  }
}

@media (max-width: 768px) {
  /* Reduce to 2 wave layers */
  .wave-1 { display: none; }

  /* Use simpler filter */
  .wave { filter: url(#waveSimple); }
}
```

### Performance Detection

```javascript
const canHandleWaterEffects = () => {
  // Check for GPU
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl');
  if (!gl) return 'ultra'; // CSS only

  const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
  const renderer = debugInfo
    ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
    : '';

  // Integrated graphics = medium tier
  if (renderer.includes('Intel') || renderer.includes('Mali')) {
    return 'medium';
  }

  return 'high';
};

// Apply appropriate tier
const tier = canHandleWaterEffects();
document.body.dataset.waterTier = tier;
```

```css
/* Tier-based styling */
[data-water-tier="ultra"] .wave {
  filter: none;
  background: linear-gradient(/* simple gradient */);
}

[data-water-tier="medium"] .wave {
  filter: url(#waveSimple);
}

[data-water-tier="high"] .wave {
  filter: url(#waveFull);
}
```

## Framework Integration

### Next.js / React

```tsx
// components/OceanBackground.tsx
'use client';

import { useEffect, useState, useRef } from 'react';
import styles from './OceanBackground.module.css';

export function OceanBackground({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const turbRef = useRef<SVGFETurbulenceElement>(null);

  useEffect(() => {
    setMounted(true);

    // Animate after mount
    let frame = 0;
    const animate = () => {
      frame += 0.003;
      if (turbRef.current) {
        const xFreq = 0.008 + Math.sin(frame) * 0.002;
        const yFreq = 0.08 + Math.sin(frame * 0.7) * 0.01;
        turbRef.current.setAttribute('baseFrequency', `${xFreq} ${yFreq}`);
      }
      requestAnimationFrame(animate);
    };
    const id = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(id);
  }, []);

  if (!mounted) return null;

  return (
    <div className={styles.ocean}>
      <svg className={styles.filters}>
        <defs>
          <filter id="oceanWave">
            <feTurbulence ref={turbRef} type="turbulence"
                          baseFrequency="0.008 0.08" numOctaves="4"/>
            <feDisplacementMap in="SourceGraphic" scale="25"/>
          </filter>
        </defs>
      </svg>
      <div className={styles.waveLayer} />
      <div className={styles.content}>{children}</div>
    </div>
  );
}
```

### Tailwind CSS

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'wave-drift': 'wave-drift 60s linear infinite',
        'wave-slow': 'wave-drift 90s linear infinite',
        'wave-fast': 'wave-drift 35s linear infinite',
      },
      keyframes: {
        'wave-drift': {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(-50%)' },
        },
      },
      colors: {
        ocean: {
          deep: '#0c4a6e',
          mid: '#0369a1',
          surface: '#0ea5e9',
          foam: '#f0f9ff',
        },
      },
    },
  },
};
```

### Vue 3

```vue
<template>
  <div class="ocean-container">
    <WaveFilters />
    <div
      v-for="layer in waveLayers"
      :key="layer.id"
      class="wave-layer"
      :style="layer.style"
    />
    <slot />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import WaveFilters from './WaveFilters.vue';

const waveLayers = computed(() => [
  { id: 1, style: { filter: 'url(#wave1)', animationDuration: '80s', opacity: 0.4 }},
  { id: 2, style: { filter: 'url(#wave2)', animationDuration: '55s', opacity: 0.6 }},
  { id: 3, style: { filter: 'url(#wave3)', animationDuration: '35s', opacity: 0.8 }},
]);
</script>
```

## Debugging Tips

### Visualize Filter Pipeline

```xml
<!-- Show each filter step -->
<filter id="debug-water">
  <feTurbulence result="step1"/>
  <feImage href="#step1" x="0" y="0" width="200" height="200"/>

  <feDisplacementMap in="SourceGraphic" in2="step1" result="step2"/>
  <feImage href="#step2" x="200" y="0" width="200" height="200"/>
</filter>
```

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Effect disappears | Filter region too small | Add `x="-20%" y="-20%" width="140%" height="140%"` |
| Square/boxy waves | Using fractalNoise | Change to `type="turbulence"` |
| Waves too uniform | Same seed across layers | Use different `seed` values |
| No horizontal motion | Equal baseFrequency values | Use `baseFrequency="0.01 0.1"` (different x/y) |
| Animation stuttering | Animating filter attributes | Use CSS transform animations instead |
| Edge artifacts | Displacement at boundaries | Increase filter region with x/y/width/height |

### Browser DevTools

1. **Elements panel** > Select SVG filter > Inspect attributes
2. **Performance panel** > Record > Check for layout thrashing
3. **Layers panel** (Chrome) > Verify GPU acceleration on wave layers

## Integration with web-cloud-designer

For complete atmospheric scenes, combine water and cloud effects:

```html
<div class="scene">
  <!-- Sky with clouds (from web-cloud-designer) -->
  <div class="sky">
    <div class="cloud-layer cloud-back"></div>
    <div class="cloud-layer cloud-front"></div>
  </div>

  <!-- Horizon -->
  <div class="horizon"></div>

  <!-- Ocean with waves (this skill) -->
  <div class="ocean">
    <div class="wave wave-back"></div>
    <div class="wave wave-front"></div>
    <div class="reflection"></div>
  </div>
</div>

<style>
  .scene {
    height: 100vh;
    display: grid;
    grid-template-rows: 60% 40%;
  }

  .sky {
    background: linear-gradient(180deg, #1e3c72 0%, #87CEEB 100%);
  }

  .ocean {
    background: linear-gradient(180deg, #0369a1 0%, #0c4a6e 100%);
  }

  .reflection {
    /* Mirror cloud movement on water surface */
    position: absolute;
    top: 0;
    width: 100%;
    height: 30%;
    background: inherit;
    transform: scaleY(-1);
    opacity: 0.3;
    filter: url(#waterReflection) blur(2px);
  }
</style>
```

## Reference Sources

- Red Stapler: "Realistic Water Effect SVG Turbulence"
- Mitkov Systems: "Liquid Glass Water Animation" (2025)
- O'Reilly SVG Book: feTurbulence Chapter
- MDN: SVG Filter Primitives Documentation
- CSS-Tricks: "Underwater Blur Effect"
- Codrops: "Water Distortion Effect"

---

*Water is the driving force of all nature.* - Leonardo da Vinci
