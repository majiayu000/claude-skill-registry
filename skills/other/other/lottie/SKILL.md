---
name: lottie
description: Add and manage Lottie animations in the website using LottieFiles. Auto-activates when user asks about animations, lottie, motion graphics, or animated icons. Trigger words: "lottie", "animation", "animated icon", "motion graphic", "add animation", "lottiefiles"
allowed-tools: Bash, Read, Write, Edit
---

# Lottie Animation Skill

Add lightweight, scalable Lottie animations to the Mediar website using LottieFiles.

## Current Animation Setup

The project currently uses **Framer Motion** (`framer-motion@11.0.14`) for animations. Lottie can be added alongside Framer Motion for more complex pre-made animations.

---

## Installation

### Install LottieFiles React Package

```bash
npm install @lottiefiles/dotlottie-react
```

This is the official LottieFiles package that supports both `.json` and `.lottie` (optimized) formats.

---

## Basic Usage

### Simple Lottie Component

Create a reusable Lottie component at `components/lottie-animation.tsx`:

```tsx
"use client";

import { DotLottieReact } from "@lottiefiles/dotlottie-react";

interface LottieAnimationProps {
  src: string;
  loop?: boolean;
  autoplay?: boolean;
  className?: string;
  speed?: number;
}

export function LottieAnimation({
  src,
  loop = true,
  autoplay = true,
  className = "",
  speed = 1,
}: LottieAnimationProps) {
  return (
    <DotLottieReact
      src={src}
      loop={loop}
      autoplay={autoplay}
      className={className}
      speed={speed}
    />
  );
}
```

### Usage Example

```tsx
import { LottieAnimation } from "@/components/lottie-animation";

export function MyComponent() {
  return (
    <LottieAnimation
      src="https://lottie.host/xxx/animation.lottie"
      className="w-64 h-64"
    />
  );
}
```

---

## Integration with Framer Motion

Combine Lottie with Framer Motion for scroll-triggered animations:

```tsx
"use client";

import { motion, useInView } from "framer-motion";
import { useRef, useState, useEffect } from "react";
import { DotLottieReact, DotLottie } from "@lottiefiles/dotlottie-react";

interface AnimatedLottieProps {
  src: string;
  className?: string;
  playOnView?: boolean;
}

export function AnimatedLottie({
  src,
  className = "",
  playOnView = true,
}: AnimatedLottieProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });
  const [dotLottie, setDotLottie] = useState<DotLottie | null>(null);

  useEffect(() => {
    if (playOnView && dotLottie) {
      if (isInView) {
        dotLottie.play();
      } else {
        dotLottie.pause();
      }
    }
  }, [isInView, dotLottie, playOnView]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6 }}
      className={className}
    >
      <DotLottieReact
        src={src}
        loop
        autoplay={!playOnView}
        dotLottieRefCallback={setDotLottie}
      />
    </motion.div>
  );
}
```

---

## Local Animation Files

### Storing Animations

Store Lottie files in `public/animations/`:

```
public/
  animations/
    loading.lottie
    success.lottie
    workflow.json
```

### Using Local Files

```tsx
<LottieAnimation src="/animations/loading.lottie" />
```

---

## Controlled Playback

### Play/Pause/Stop Controls

```tsx
"use client";

import { useState, useCallback } from "react";
import { DotLottieReact, DotLottie } from "@lottiefiles/dotlottie-react";

export function ControlledLottie({ src }: { src: string }) {
  const [dotLottie, setDotLottie] = useState<DotLottie | null>(null);

  const play = useCallback(() => dotLottie?.play(), [dotLottie]);
  const pause = useCallback(() => dotLottie?.pause(), [dotLottie]);
  const stop = useCallback(() => dotLottie?.stop(), [dotLottie]);

  return (
    <div>
      <DotLottieReact
        src={src}
        loop
        autoplay={false}
        dotLottieRefCallback={setDotLottie}
      />
      <div className="flex gap-2 mt-4">
        <button onClick={play}>Play</button>
        <button onClick={pause}>Pause</button>
        <button onClick={stop}>Stop</button>
      </div>
    </div>
  );
}
```

### Segment Playback (Play Specific Frames)

```tsx
const playSegment = useCallback(() => {
  if (dotLottie) {
    dotLottie.setSegment(0, 30); // Play frames 0-30
    dotLottie.play();
  }
}, [dotLottie]);
```

---

## Event Handlers

```tsx
<DotLottieReact
  src={src}
  loop
  autoplay
  dotLottieRefCallback={setDotLottie}
  onComplete={() => console.log("Animation complete")}
  onLoad={() => console.log("Animation loaded")}
  onPlay={() => console.log("Playing")}
  onPause={() => console.log("Paused")}
  onStop={() => console.log("Stopped")}
  onFrame={(frame) => console.log("Frame:", frame)}
/>
```

---

## Common Animation Sources

### LottieFiles Free Animations

Browse free animations at: https://lottiefiles.com/free-animations

Popular categories for business/SaaS:
- **Loading/Processing**: https://lottiefiles.com/search?q=loading
- **Success/Checkmark**: https://lottiefiles.com/search?q=success
- **Workflow/Process**: https://lottiefiles.com/search?q=workflow
- **Robot/AI**: https://lottiefiles.com/search?q=robot
- **Data/Analytics**: https://lottiefiles.com/search?q=analytics
- **Document/File**: https://lottiefiles.com/search?q=document

### Using LottieFiles CDN

Copy the CDN URL from any animation on LottieFiles:

```tsx
<LottieAnimation
  src="https://lottie.host/embedded/your-animation-id.lottie"
/>
```

---

## Replacing Framer Motion Animations

### Before (Framer Motion custom animation)

```tsx
<motion.div
  className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
  animate={{ scale: [1, 1.2, 1] }}
  transition={{ duration: 1.5, repeat: Infinity }}
/>
```

### After (Lottie)

```tsx
<LottieAnimation
  src="/animations/pulse.lottie"
  className="w-8 h-8"
/>
```

---

## Performance Tips

1. **Use .lottie format** - Up to 80% smaller than .json
2. **Lazy load** - Only load animations when needed
3. **Pause offscreen** - Use `useInView` to pause animations not in viewport
4. **Limit concurrent** - Don't run too many animations simultaneously
5. **Optimize size** - Use LottieFiles editor to reduce complexity

### Lazy Loading Example

```tsx
import dynamic from "next/dynamic";

const LottieAnimation = dynamic(
  () => import("@/components/lottie-animation").then((mod) => mod.LottieAnimation),
  { ssr: false, loading: () => <div className="w-64 h-64 bg-muted animate-pulse" /> }
);
```

---

## Workflow Animation Example

Replace custom step animations with Lottie:

```tsx
"use client";

import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import { DotLottieReact } from "@lottiefiles/dotlottie-react";

const STEP_ANIMATIONS = {
  document: "https://lottie.host/xxx/document.lottie",
  ai: "https://lottie.host/xxx/ai-brain.lottie",
  typing: "https://lottie.host/xxx/typing.lottie",
  success: "https://lottie.host/xxx/checkmark.lottie",
};

interface WorkflowStep {
  animation: keyof typeof STEP_ANIMATIONS;
  label: string;
  description: string;
}

export function LottieWorkflowAnimation() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  const steps: WorkflowStep[] = [
    { animation: "document", label: "PDF Arrives", description: "Invoice received" },
    { animation: "ai", label: "AI Reads", description: "Extracts data" },
    { animation: "typing", label: "Enters Data", description: "Types into SAP" },
    { animation: "success", label: "Done", description: "Ready for review" },
  ];

  return (
    <div ref={ref} className="flex justify-between">
      {steps.map((step, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: index * 0.2 }}
          className="flex flex-col items-center"
        >
          <div className="w-24 h-24">
            <DotLottieReact
              src={STEP_ANIMATIONS[step.animation]}
              loop
              autoplay={isInView}
            />
          </div>
          <p className="font-semibold mt-4">{step.label}</p>
          <p className="text-sm text-muted-foreground">{step.description}</p>
        </motion.div>
      ))}
    </div>
  );
}
```

---

## Icon Animations

Use Lottie for animated icons:

```tsx
"use client";

import { DotLottieReact } from "@lottiefiles/dotlottie-react";

const ANIMATED_ICONS = {
  check: "https://lottie.host/xxx/check.lottie",
  loading: "https://lottie.host/xxx/loading.lottie",
  error: "https://lottie.host/xxx/error.lottie",
  arrow: "https://lottie.host/xxx/arrow.lottie",
};

interface AnimatedIconProps {
  icon: keyof typeof ANIMATED_ICONS;
  size?: number;
  loop?: boolean;
}

export function AnimatedIcon({ icon, size = 24, loop = false }: AnimatedIconProps) {
  return (
    <DotLottieReact
      src={ANIMATED_ICONS[icon]}
      loop={loop}
      autoplay
      style={{ width: size, height: size }}
    />
  );
}
```

---

## Creating Custom Animations

### Option 1: LottieFiles Creator (Browser-based)
https://lottiefiles.com/lottie-creator

### Option 2: Figma + LottieFiles Plugin
1. Design in Figma
2. Use LottieFiles Figma plugin to export

### Option 3: Adobe After Effects + Bodymovin
1. Create animation in After Effects
2. Export with Bodymovin extension

---

## Troubleshooting

### Animation Not Playing
- Check if `autoplay` is set to `true`
- Verify the src URL is correct and accessible
- Check browser console for errors

### Animation Too Large
- Use `.lottie` format instead of `.json`
- Optimize using LottieFiles editor
- Reduce animation complexity

### Flash of Unstyled Content
- Add a placeholder/skeleton while loading
- Use dynamic import with loading state

### SSR Issues
- Use `dynamic` import with `ssr: false`
- Or conditionally render based on client-side check

---

## API Reference

### DotLottieReact Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| src | string | required | URL or path to animation |
| autoplay | boolean | false | Auto-start animation |
| loop | boolean | false | Loop animation |
| speed | number | 1 | Playback speed (0.5 = half, 2 = double) |
| direction | 1 \| -1 | 1 | Playback direction |
| mode | string | "forward" | "forward", "reverse", "bounce", "reverse-bounce" |
| segment | [number, number] | - | Frame segment to play |
| backgroundColor | string | - | Background color |

### DotLottie Instance Methods

| Method | Description |
|--------|-------------|
| play() | Start animation |
| pause() | Pause animation |
| stop() | Stop and reset |
| setSpeed(speed) | Set playback speed |
| setDirection(dir) | Set direction (1 or -1) |
| setSegment(start, end) | Set frame range |
| goToAndPlay(frame) | Jump to frame and play |
| goToAndStop(frame) | Jump to frame and stop |

---

## Resources

- **LottieFiles**: https://lottiefiles.com
- **Free Animations**: https://lottiefiles.com/free-animations
- **Documentation**: https://developers.lottiefiles.com/docs/dotlottie-player/dotlottie-react
- **Lottie Creator**: https://lottiefiles.com/lottie-creator
- **Figma Plugin**: https://www.figma.com/community/plugin/809860933081065308
