---
name: web-cloud-designer
description: Creates realistic cloud effects for web using SVG filters (feTurbulence, feDisplacementMap), CSS animations, and layering techniques. Use for atmospheric backgrounds, weather effects, skyboxes, parallax scenes, and decorative cloud elements. Activate on "cloud effect", "SVG clouds", "realistic clouds", "atmospheric background", "sky animation", "feTurbulence", "weather effects", "parallax clouds". NOT for 3D rendering (use WebGL/Three.js skills), photo manipulation (use image editing tools), weather data APIs (use data integration skills), or simple CSS gradients without volumetric effects.
allowed-tools: Read,Write,Edit,WebFetch,Bash
category: Design & Creative
tags:
  - svg
  - css
  - animation
  - atmospheric
  - visual-effects
  - web
pairs-with:
  - skill: web-design-expert
    reason: Integrate clouds into overall web design
  - skill: physics-rendering-expert
    reason: Realistic lighting and shadow calculations
  - skill: color-theory-palette-harmony-expert
    reason: Sky gradients and atmospheric color
---

# Web Cloud Designer

Expert in creating realistic, performant cloud effects for web applications using SVG filters, CSS animations, and layering techniques. Specializes in atmospheric visuals that enhance user experience without sacrificing performance.

## When to Use This Skill

**Use for:**
- Realistic cloud backgrounds and skyboxes
- Weather-themed UI elements and transitions
- Parallax cloud scenes with depth
- Animated atmospheric effects
- Stylized/cartoon cloud designs
- Hero section backgrounds with sky themes
- Loading states with cloud animations
- Game-style cloud layers

**Do NOT use for:**
- 3D volumetric cloud rendering -> use **WebGL/Three.js**
- Photo manipulation of real clouds -> use image editing
- Weather data integration -> use weather API skills
- Simple gradient skies without cloud shapes
- Video backgrounds with clouds

## Core Techniques Reference

### SVG Filter Pipeline

The fundamental cloud effect uses this filter chain:

```
Source -> feTurbulence -> feDisplacementMap -> feGaussianBlur -> feDiffuseLighting -> Composite
```

### 1. feTurbulence - The Foundation

Generates Perlin noise that forms cloud shapes.

```xml
<feTurbulence
  type="fractalNoise"      <!-- fractalNoise for clouds (NOT turbulence) -->
  baseFrequency="0.01"     <!-- 0.005-0.02: lower = larger, rounder shapes -->
  numOctaves="4"           <!-- 3-5: detail level, >5 diminishing returns -->
  seed="42"                <!-- Change for shape variation (free!) -->
  result="noise"
/>
```

| Parameter | Range | Effect |
|-----------|-------|--------|
| `baseFrequency` | 0.005-0.02 | Scale of cloud shapes. 0.005 = giant cumulus, 0.02 = small wisps |
| `numOctaves` | 3-5 | Detail layers. 3 = smooth, 5 = detailed. Above 5 = CPU waste |
| `seed` | 0-999999 | Shape variation. Change this, NOT baseFrequency for variety |
| `type` | fractalNoise | ALWAYS use fractalNoise for clouds (turbulence = fire/water) |

### 2. feDisplacementMap - Shape Distortion

Creates organic, billowing cloud shapes from the noise.

```xml
<feDisplacementMap
  in="SourceGraphic"
  in2="noise"
  scale="80"               <!-- 20-170: distortion intensity -->
  xChannelSelector="R"
  yChannelSelector="G"
/>
```

| Scale Value | Effect |
|-------------|--------|
| 20-50 | Subtle, wispy cirrus |
| 50-100 | Balanced cumulus |
| 100-170 | Dramatic, billowing storm clouds |

### 3. feGaussianBlur - Edge Softening

**CRITICAL**: Apply BEFORE displacement for performance (per CSS-Tricks).

```xml
<feGaussianBlur
  stdDeviation="3"         <!-- 2-8 for cloud softness -->
  result="blurred"
/>
```

### 4. feDiffuseLighting - Volumetric Depth

Adds 3D-like shading to flat noise.

```xml
<feDiffuseLighting
  in="noise"
  lighting-color="white"
  surfaceScale="2"
  result="light"
>
  <feDistantLight
    azimuth="45"           <!-- Sun angle: 0-360 -->
    elevation="55"         <!-- Sun height: 0-90 -->
  />
</feDiffuseLighting>
```

## Cloud Type Recipes

### Cumulus (Puffy, Happy Clouds)

```svg
<svg width="100%" height="100%">
  <defs>
    <filter id="cumulus" x="-50%" y="-50%" width="200%" height="200%">
      <feTurbulence type="fractalNoise" baseFrequency="0.008"
                    numOctaves="4" seed="5" result="noise"/>
      <feGaussianBlur in="noise" stdDeviation="4" result="blur"/>
      <feDisplacementMap in="SourceGraphic" in2="blur" scale="60"/>
    </filter>
  </defs>
  <ellipse cx="200" cy="100" rx="150" ry="80"
           fill="white" filter="url(#cumulus)"/>
</svg>
```

### Cirrus (Wispy, High Altitude)

```svg
<filter id="cirrus">
  <feTurbulence type="fractalNoise" baseFrequency="0.02 0.005"
                numOctaves="3" seed="12" result="noise"/>
  <feGaussianBlur in="noise" stdDeviation="2" result="blur"/>
  <feDisplacementMap in="SourceGraphic" in2="blur" scale="25"/>
</filter>
```

Key: Use anisotropic `baseFrequency` (two values) for stretched, directional wisps.

### Stratus (Flat Layers)

```svg
<filter id="stratus">
  <feTurbulence type="fractalNoise" baseFrequency="0.015 0.003"
                numOctaves="3" seed="8" result="noise"/>
  <feGaussianBlur stdDeviation="6" result="blur"/>
  <feDisplacementMap in="SourceGraphic" in2="blur" scale="30"/>
</filter>
```

### Cumulonimbus (Storm Clouds)

```svg
<filter id="storm">
  <feTurbulence type="fractalNoise" baseFrequency="0.006"
                numOctaves="5" seed="99" result="noise"/>
  <feGaussianBlur in="noise" stdDeviation="3" result="blur"/>
  <feDisplacementMap in="SourceGraphic" in2="blur" scale="150"/>
  <feDiffuseLighting in="blur" lighting-color="#8899aa" surfaceScale="3">
    <feDistantLight azimuth="230" elevation="25"/>
  </feDiffuseLighting>
</filter>
```

### Stylized/Cartoon Clouds

```svg
<filter id="cartoon">
  <feTurbulence type="fractalNoise" baseFrequency="0.012"
                numOctaves="2" seed="3" result="noise"/>
  <feDisplacementMap in="SourceGraphic" in2="noise" scale="40"/>
  <!-- No blur = sharper edges for cartoon look -->
</filter>
```

## Layering Strategy

Create depth with multiple cloud layers:

```html
<div class="sky">
  <div class="clouds clouds-back"></div>
  <div class="clouds clouds-mid"></div>
  <div class="clouds clouds-front"></div>
</div>
```

```css
.clouds-back {
  filter: url(#cloud-soft);
  opacity: 0.3;
  animation: drift 120s linear infinite;
  transform: scale(1.5);
}

.clouds-mid {
  filter: url(#cloud-medium);
  opacity: 0.6;
  animation: drift 80s linear infinite;
  transform: scale(1);
}

.clouds-front {
  filter: url(#cloud-sharp);
  opacity: 0.9;
  animation: drift 50s linear infinite;
  transform: scale(0.8);
}
```

### Layer Parameter Guide

| Layer | Opacity | Speed | Scale | blur stdDeviation |
|-------|---------|-------|-------|-------------------|
| Back (distant) | 0.2-0.4 | 90-120s | 1.3-1.5x | 5-8 |
| Mid | 0.5-0.7 | 50-80s | 1.0x | 3-5 |
| Front (close) | 0.8-1.0 | 30-50s | 0.7-0.9x | 1-3 |

## Animation Techniques

### CSS Keyframes (Recommended - Best Performance)

```css
@keyframes drift {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}

@keyframes morph {
  0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
}

.cloud {
  animation:
    drift 60s linear infinite,
    morph 15s ease-in-out infinite;
}
```

### SVG Animate (Use Sparingly - CPU Intensive)

```svg
<feTurbulence baseFrequency="0.01" numOctaves="4">
  <animate
    attributeName="baseFrequency"
    values="0.008;0.012;0.008"
    dur="20s"
    repeatCount="indefinite"
  />
</feTurbulence>
```

**WARNING**: Animating filter properties recalculates the entire filter. Use only for hero effects, not background loops.

### GSAP (Best Control)

```javascript
gsap.to("#cloud-filter feTurbulence", {
  attr: { baseFrequency: 0.015 },
  duration: 10,
  ease: "sine.inOut",
  yoyo: true,
  repeat: -1
});
```

### 3D Parallax (Billboard Technique)

```css
.cloud-layer {
  transform-style: preserve-3d;
  perspective: 1000px;
}

.cloud {
  transform: translateZ(-100px) scale(1.1);
  /* Further clouds appear smaller, move slower on scroll */
}
```

## Complete Implementation Templates

### Template 1: Simple Sky Background

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .sky {
      position: relative;
      width: 100%;
      height: 100vh;
      background: linear-gradient(180deg, #87CEEB 0%, #E0F6FF 100%);
      overflow: hidden;
    }

    .cloud {
      position: absolute;
      background: white;
      border-radius: 50%;
      filter: url(#cloudFilter);
      animation: float linear infinite;
    }

    .cloud-1 { width: 300px; height: 150px; top: 10%; animation-duration: 80s; }
    .cloud-2 { width: 400px; height: 180px; top: 30%; animation-duration: 100s; animation-delay: -30s; }
    .cloud-3 { width: 250px; height: 120px; top: 50%; animation-duration: 70s; animation-delay: -50s; }

    @keyframes float {
      from { transform: translateX(-120%); }
      to { transform: translateX(120vw); }
    }
  </style>
</head>
<body>
  <svg style="position:absolute;width:0;height:0">
    <defs>
      <filter id="cloudFilter" x="-50%" y="-50%" width="200%" height="200%">
        <feTurbulence type="fractalNoise" baseFrequency="0.01" numOctaves="4" seed="5"/>
        <feGaussianBlur stdDeviation="4"/>
        <feDisplacementMap in="SourceGraphic" scale="50"/>
      </filter>
    </defs>
  </svg>

  <div class="sky">
    <div class="cloud cloud-1"></div>
    <div class="cloud cloud-2"></div>
    <div class="cloud cloud-3"></div>
  </div>
</body>
</html>
```

### Template 2: Layered Parallax Clouds

```html
<style>
  .parallax-sky {
    position: relative;
    height: 100vh;
    background: linear-gradient(to bottom,
      #1e3c72 0%,
      #2a5298 30%,
      #f5af19 90%,
      #f12711 100%
    );
    overflow: hidden;
  }

  .cloud-layer {
    position: absolute;
    width: 200%;
    height: 100%;
    background-repeat: repeat-x;
  }

  .layer-back {
    opacity: 0.3;
    filter: url(#cloudBack) blur(2px);
    animation: scroll 120s linear infinite;
  }

  .layer-mid {
    opacity: 0.5;
    filter: url(#cloudMid);
    animation: scroll 80s linear infinite;
  }

  .layer-front {
    opacity: 0.8;
    filter: url(#cloudFront);
    animation: scroll 45s linear infinite;
  }

  @keyframes scroll {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
  }
</style>

<svg style="display:none">
  <defs>
    <filter id="cloudBack">
      <feTurbulence type="fractalNoise" baseFrequency="0.005" numOctaves="3" seed="1"/>
      <feDisplacementMap in="SourceGraphic" scale="40"/>
    </filter>
    <filter id="cloudMid">
      <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="4" seed="2"/>
      <feDisplacementMap in="SourceGraphic" scale="60"/>
    </filter>
    <filter id="cloudFront">
      <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="3"/>
      <feDisplacementMap in="SourceGraphic" scale="80"/>
    </filter>
  </defs>
</svg>
```

### Template 3: React Component

```tsx
import React, { useMemo } from 'react';

interface CloudProps {
  type?: 'cumulus' | 'cirrus' | 'stratus' | 'storm';
  seed?: number;
  className?: string;
}

const CLOUD_CONFIGS = {
  cumulus: { baseFrequency: '0.008', numOctaves: 4, scale: 60, blur: 4 },
  cirrus: { baseFrequency: '0.02 0.005', numOctaves: 3, scale: 25, blur: 2 },
  stratus: { baseFrequency: '0.015 0.003', numOctaves: 3, scale: 30, blur: 6 },
  storm: { baseFrequency: '0.006', numOctaves: 5, scale: 150, blur: 3 },
};

export const Cloud: React.FC<CloudProps> = ({
  type = 'cumulus',
  seed = Math.floor(Math.random() * 1000),
  className
}) => {
  const filterId = useMemo(() => `cloud-${type}-${seed}`, [type, seed]);
  const config = CLOUD_CONFIGS[type];

  return (
    <>
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <filter id={filterId} x="-50%" y="-50%" width="200%" height="200%">
            <feTurbulence
              type="fractalNoise"
              baseFrequency={config.baseFrequency}
              numOctaves={config.numOctaves}
              seed={seed}
              result="noise"
            />
            <feGaussianBlur in="noise" stdDeviation={config.blur} result="blur"/>
            <feDisplacementMap in="SourceGraphic" in2="blur" scale={config.scale}/>
          </filter>
        </defs>
      </svg>
      <div
        className={className}
        style={{ filter: `url(#${filterId})` }}
      />
    </>
  );
};

// Usage:
// <Cloud type="cumulus" seed={42} className="cloud-shape" />
```

### Template 4: CSS-Only Box-Shadow Clouds

For simpler, more performant clouds without SVG filters:

```css
.cloud-simple {
  width: 200px;
  height: 60px;
  background: white;
  border-radius: 100px;
  position: relative;
  box-shadow:
    /* Main body shadows for volume */
    inset -10px -10px 30px rgba(0,0,0,0.05),
    inset 10px 10px 30px rgba(255,255,255,0.8),
    /* Outer glow */
    0 10px 40px rgba(0,0,0,0.1);
}

.cloud-simple::before,
.cloud-simple::after {
  content: '';
  position: absolute;
  background: white;
  border-radius: 50%;
}

.cloud-simple::before {
  width: 100px;
  height: 100px;
  top: -50px;
  left: 30px;
}

.cloud-simple::after {
  width: 70px;
  height: 70px;
  top: -30px;
  left: 100px;
}
```

## Performance Optimization

### Critical Rules

1. **numOctaves <= 5** - Above 5 provides diminishing visual returns with exponential CPU cost
2. **Blur BEFORE displacement** - 40% more efficient than blur after
3. **Avoid animating filter properties** - Use CSS transforms instead
4. **Use `seed` for variation** - Free performance vs. changing baseFrequency
5. **`will-change: transform`** - Only on animated elements, remove when static
6. **Batch filter definitions** - One `<defs>` block, reference by ID

### Performance Tiers

| Tier | Technique | FPS Target | Use Case |
|------|-----------|------------|----------|
| Ultra | CSS box-shadow only | 60fps | Mobile, low-end |
| High | SVG filter, no animation | 60fps | Static backgrounds |
| Medium | SVG filter + CSS transform animation | 45-60fps | Subtle movement |
| Low | SVG filter + `<animate>` | 30fps | Hero sections only |

### Mobile Considerations

```css
@media (prefers-reduced-motion: reduce) {
  .cloud {
    animation: none;
  }
}

@media (max-width: 768px) {
  .cloud-layer {
    /* Reduce to 2 layers on mobile */
  }

  .cloud {
    filter: url(#cloudSimple); /* Fewer octaves */
  }
}
```

### Performance Detection

```javascript
// Detect if device can handle filter animations
const canHandleFilters = () => {
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl');
  if (!gl) return false;

  const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
  const renderer = debugInfo
    ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
    : '';

  // Reduce effects on integrated graphics
  return !renderer.includes('Intel');
};
```

## Framework Integration

### Next.js / React

```tsx
// components/CloudBackground.tsx
'use client';

import { useEffect, useState } from 'react';

export function CloudBackground() {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mq.matches);
    mq.addEventListener('change', (e) => setReducedMotion(e.matches));
  }, []);

  return (
    <div className="cloud-container">
      {/* SVG defs in portal to document head */}
      {/* Cloud layers */}
    </div>
  );
}
```

### Vue 3

```vue
<template>
  <div class="sky-background">
    <CloudFilter />
    <div
      v-for="cloud in clouds"
      :key="cloud.id"
      class="cloud"
      :style="cloud.style"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import CloudFilter from './CloudFilter.vue';

const clouds = computed(() =>
  Array.from({ length: 5 }, (_, i) => ({
    id: i,
    style: {
      animationDuration: `${60 + i * 20}s`,
      animationDelay: `${-i * 15}s`,
      top: `${10 + i * 15}%`,
    }
  }))
);
</script>
```

### Tailwind CSS

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'cloud-drift': 'drift 80s linear infinite',
        'cloud-morph': 'morph 15s ease-in-out infinite',
      },
      keyframes: {
        drift: {
          from: { transform: 'translateX(-100%)' },
          to: { transform: 'translateX(100vw)' },
        },
        morph: {
          '0%, 100%': { borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%' },
          '50%': { borderRadius: '30% 60% 70% 40% / 50% 60% 30% 60%' },
        },
      },
    },
  },
};
```

## Debugging Tips

### Visualize Filter Steps

```xml
<!-- Output each filter step to see what's happening -->
<filter id="debug">
  <feTurbulence result="step1"/>
  <feGaussianBlur in="step1" result="step2"/>
  <feDisplacementMap in="SourceGraphic" in2="step2" result="step3"/>

  <!-- Tile outputs to see each step -->
  <feTile in="step1" result="tile1"/>
  <feOffset in="tile1" dx="0" dy="0"/>
</filter>
```

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Clouds cut off | Filter region too small | Add `x="-50%" y="-50%" width="200%" height="200%"` |
| Jagged edges | Missing blur | Add `feGaussianBlur` before displacement |
| No variation | Same seed | Use different `seed` values |
| Performance issues | Too many octaves | Reduce `numOctaves` to 3-4 |
| Animation stuttering | Animating filter attrs | Use CSS transform animations instead |

## Reference Sources

- CSS-Tricks: "Drawing Realistic Clouds with SVG and CSS"
- LogRocket: "Animated Cloud Generator with SVG CSS"
- Codrops: "SVG Filter Effects with feTurbulence"
- Click to Release: "CSS 3D Clouds" (billboard technique)
- Nephele Cloud Generator tool
- MDN: SVG Filter Primitives documentation

---

*Clouds are nature's way of reminding us that even the sky has texture.*
