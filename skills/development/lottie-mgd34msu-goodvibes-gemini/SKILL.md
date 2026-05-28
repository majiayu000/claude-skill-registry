---
name: lottie
description: Renders After Effects animations as lightweight JSON on web and mobile using lottie-web. Use when adding vector animations, loading indicators, or complex motion graphics without video files.
---

# Lottie Web Animation

Render After Effects animations natively with lightweight JSON. Vector-based, scalable, and performant.

## Quick Start

```bash
npm install lottie-web
```

```javascript
import lottie from 'lottie-web';

const animation = lottie.loadAnimation({
  container: document.getElementById('lottie-container'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: '/animations/loading.json'  // or animationData: jsonObject
});
```

## loadAnimation Options

```javascript
const animation = lottie.loadAnimation({
  // Required
  container: document.getElementById('container'),  // DOM element

  // Animation source (use one)
  path: '/animation.json',           // URL to JSON file
  animationData: importedJSON,       // or imported JSON object

  // Renderer
  renderer: 'svg',                   // 'svg' | 'canvas' | 'html'

  // Playback
  loop: true,                        // boolean or number of loops
  autoplay: true,                    // start immediately
  name: 'myAnimation',               // reference name

  // Performance
  rendererSettings: {
    preserveAspectRatio: 'xMidYMid slice',
    progressiveLoad: true,           // improve initial load
    hideOnTransparent: true,         // hide elements with 0 opacity
    className: 'lottie-svg'          // class for SVG element
  }
});
```

## Animation Control Methods

```javascript
// Playback
animation.play();
animation.pause();
animation.stop();                    // stop and go to first frame

// Speed & Direction
animation.setSpeed(2);               // 2x speed
animation.setSpeed(0.5);             // half speed
animation.setDirection(1);           // forward
animation.setDirection(-1);          // reverse

// Seek
animation.goToAndPlay(30, true);     // frame 30, play
animation.goToAndStop(2, false);     // 2 seconds, stop
// Second param: true = frames, false = seconds

// Segments
animation.playSegments([0, 30], true);    // play frames 0-30
animation.playSegments([[0, 10], [20, 30]], false);  // multiple segments

// Info
animation.getDuration();             // in seconds
animation.getDuration(true);         // in frames
animation.totalFrames;
animation.currentFrame;
animation.isPaused;

// Cleanup
animation.destroy();
```

## Events

```javascript
// Event listener style
animation.addEventListener('complete', () => {
  console.log('Animation completed');
});

animation.addEventListener('loopComplete', () => {
  console.log('Loop finished');
});

animation.addEventListener('enterFrame', (e) => {
  console.log('Current frame:', e.currentTime);
});

// All events
'complete'          // non-looping animation finished
'loopComplete'      // loop cycle finished
'enterFrame'        // each frame (use sparingly)
'segmentStart'      // segment started playing
'config_ready'      // initial config loaded
'data_ready'        // animation data loaded
'data_failed'       // failed to load data
'DOMLoaded'         // elements added to DOM
'destroy'           // animation destroyed
```

## Global Lottie Methods

```javascript
import lottie from 'lottie-web';

// Control all animations
lottie.play();                       // play all
lottie.play('myAnimation');          // play by name
lottie.stop();
lottie.pause();

// Settings
lottie.setSpeed(1.5);                // all animations
lottie.setDirection(-1);

// State
lottie.freeze();                     // suspend all animations
lottie.unfreeze();                   // resume

// Responsive
lottie.resize();                     // recalculate sizes

// Quality (canvas renderer)
lottie.setQuality('high');           // 'high' | 'medium' | 'low'
lottie.setQuality(2);                // or number (1-10)

// Auto-discover
lottie.searchAnimations();           // find elements with class "lottie"

// Cleanup
lottie.destroy('myAnimation');       // by name
lottie.destroy();                    // all
```

## React Integration

### Using lottie-react

```bash
npm install lottie-react
```

```jsx
import Lottie from 'lottie-react';
import animationData from './animation.json';

function MyAnimation() {
  return (
    <Lottie
      animationData={animationData}
      loop={true}
      autoplay={true}
      style={{ width: 300, height: 300 }}
    />
  );
}
```

### With Ref Control

```jsx
import { useRef } from 'react';
import Lottie from 'lottie-react';
import animationData from './animation.json';

function ControlledAnimation() {
  const lottieRef = useRef();

  const handlePlay = () => lottieRef.current?.play();
  const handlePause = () => lottieRef.current?.pause();
  const handleStop = () => lottieRef.current?.stop();

  return (
    <>
      <Lottie
        lottieRef={lottieRef}
        animationData={animationData}
        autoplay={false}
      />
      <button onClick={handlePlay}>Play</button>
      <button onClick={handlePause}>Pause</button>
      <button onClick={handleStop}>Stop</button>
    </>
  );
}
```

### Custom Hook

```jsx
import { useEffect, useRef, useState } from 'react';
import lottie from 'lottie-web';

function useLottie(options) {
  const containerRef = useRef(null);
  const animationRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    animationRef.current = lottie.loadAnimation({
      container: containerRef.current,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      ...options
    });

    animationRef.current.addEventListener('DOMLoaded', () => {
      setIsLoaded(true);
    });

    return () => {
      animationRef.current?.destroy();
    };
  }, [options.path || options.animationData]);

  return {
    containerRef,
    animation: animationRef.current,
    isLoaded
  };
}

// Usage
function MyComponent() {
  const { containerRef, animation } = useLottie({
    path: '/animation.json'
  });

  return <div ref={containerRef} style={{ width: 200, height: 200 }} />;
}
```

## Vue Integration

```vue
<template>
  <div ref="container" class="lottie-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import lottie from 'lottie-web';

const container = ref(null);
let animation = null;

onMounted(() => {
  animation = lottie.loadAnimation({
    container: container.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/animation.json'
  });
});

onUnmounted(() => {
  animation?.destroy();
});
</script>
```

## Renderer Comparison

| Renderer | Pros | Cons |
|----------|------|------|
| `svg` | Best quality, DOM access, smaller file | Slower with complex animations |
| `canvas` | Best performance, consistent | No DOM access, larger memory |
| `html` | DOM access | Limited feature support |

```javascript
// SVG (default, recommended)
{ renderer: 'svg' }

// Canvas (performance-critical)
{
  renderer: 'canvas',
  rendererSettings: {
    context: canvasContext,  // optional: provide 2d context
    clearCanvas: true
  }
}
```

## dotLottie Format

Smaller file size using `.lottie` container format.

```bash
npm install @dotlottie/player-component
```

```html
<script src="https://unpkg.com/@dotlottie/player-component"></script>

<dotlottie-player
  src="/animation.lottie"
  autoplay
  loop
  style="width: 300px; height: 300px"
></dotlottie-player>
```

## Performance Tips

1. **Use SVG renderer** for most cases
2. **Use canvas** for complex animations or many instances
3. **Reduce frame rate** if not needed:
   ```javascript
   animation.setSubframe(false);  // disable subframe rendering
   ```
4. **Progressive load** for large files:
   ```javascript
   rendererSettings: { progressiveLoad: true }
   ```
5. **Destroy when not visible**:
   ```javascript
   // In viewport observer
   if (!isVisible) animation.destroy();
   ```
6. **Lazy load** animations not immediately visible

## Common Patterns

### Loading Spinner
```jsx
function LoadingSpinner({ isLoading }) {
  if (!isLoading) return null;

  return (
    <Lottie
      animationData={spinnerAnimation}
      loop={true}
      style={{ width: 48, height: 48 }}
    />
  );
}
```

### Interactive Animation
```jsx
function InteractiveAnimation() {
  const [isHovered, setIsHovered] = useState(false);
  const lottieRef = useRef();

  useEffect(() => {
    if (isHovered) {
      lottieRef.current?.play();
    } else {
      lottieRef.current?.stop();
    }
  }, [isHovered]);

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Lottie
        lottieRef={lottieRef}
        animationData={hoverAnimation}
        autoplay={false}
        loop={false}
      />
    </div>
  );
}
```

### Scroll-Triggered Animation
```jsx
function ScrollAnimation() {
  const containerRef = useRef();
  const animationRef = useRef();

  useEffect(() => {
    const animation = lottie.loadAnimation({
      container: containerRef.current,
      path: '/scroll-animation.json',
      autoplay: false
    });
    animationRef.current = animation;

    const handleScroll = () => {
      const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);
      const frame = scrollPercent * animation.totalFrames;
      animation.goToAndStop(frame, true);
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      animation.destroy();
    };
  }, []);

  return <div ref={containerRef} />;
}
```

## Finding Animations

- **LottieFiles**: https://lottiefiles.com - Free and premium animations
- **IconScout**: https://iconscout.com/lottie-animations
- **LordIcon**: https://lordicon.com - Animated icons

## After Effects Export

Use **LottieFiles plugin** or **Bodymovin** to export from After Effects.

### Supported Features
- Shapes, masks, trim paths
- Parenting, opacity, transforms
- Text (convert to shapes for best results)
- Image sequences (embedded as base64)

### Not Supported
- Video/audio
- 3D layers
- Expressions (limited support)
- Effects like blur, glow
- Very complex masks

## Reference Files

- [references/react-patterns.md](references/react-patterns.md) - React integration patterns
