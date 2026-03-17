---
name: audio-reactive
description: Binding audio analysis data to visual parameters including smoothing, beat detection responses, and frequency-to-visual mappings. Use when creating audio visualizers, music-reactive animations, or any visual effect driven by audio input.
---

# Audio Reactive Visuals

Connecting audio analysis to visual parameters.

## Quick Start

```javascript
import * as Tone from 'tone';

const analyser = new Tone.Analyser('fft', 256);
const player = new Tone.Player('/audio/music.mp3');
player.connect(analyser);
player.toDestination();

function animate() {
  const fft = analyser.getValue();
  const bass = (fft[2] + 100) / 100; // Normalize to 0-1

  // Apply to visual
  element.style.transform = `scale(${1 + bass * 0.2})`;

  requestAnimationFrame(animate);
}
```

## Core Patterns

### Audio-to-Visual Mapping

```javascript
class AudioReactiveMapper {
  constructor(analyser) {
    this.analyser = analyser;
    this.smoothers = {
      bass: new Smoother(0.85),
      mid: new Smoother(0.9),
      high: new Smoother(0.92)
    };
  }

  // Get values optimized for different visual properties
  getValues() {
    const fft = this.analyser.getValue();
    const len = fft.length;

    // Extract and normalize bands
    const rawBass = this.avgRange(fft, 0, len * 0.1);
    const rawMid = this.avgRange(fft, len * 0.1, len * 0.5);
    const rawHigh = this.avgRange(fft, len * 0.5, len);

    return {
      bass: this.smoothers.bass.update(this.normalize(rawBass)),
      mid: this.smoothers.mid.update(this.normalize(rawMid)),
      high: this.smoothers.high.update(this.normalize(rawHigh))
    };
  }

  avgRange(data, start, end) {
    let sum = 0;
    for (let i = Math.floor(start); i < Math.floor(end); i++) {
      sum += data[i];
    }
    return sum / (end - start);
  }

  normalize(db) {
    return Math.max(0, Math.min(1, (db + 100) / 100));
  }
}

class Smoother {
  constructor(factor = 0.9) {
    this.factor = factor;
    this.value = 0;
  }
  update(input) {
    this.value = this.factor * this.value + (1 - this.factor) * input;
    return this.value;
  }
}
```

## Visual Property Mappings

### Scale/Size

```javascript
// Pulse on bass
function updateScale(element, bass) {
  const scale = 1 + bass * 0.3; // 1.0 to 1.3
  element.style.transform = `scale(${scale})`;
}

// Three.js mesh
function updateMeshScale(mesh, bass) {
  const scale = 1 + bass * 0.5;
  mesh.scale.setScalar(scale);
}
```

### Position/Movement

```javascript
// Vibration based on high frequencies
function updatePosition(element, high) {
  const shake = high * 5; // Pixels
  const x = (Math.random() - 0.5) * shake;
  const y = (Math.random() - 0.5) * shake;
  element.style.transform = `translate(${x}px, ${y}px)`;
}

// Smooth wave motion
function updateWavePosition(mesh, mid, time) {
  mesh.position.y = Math.sin(time * 2) * mid * 2;
}
```

### Rotation

```javascript
// Continuous rotation speed based on energy
class SpinController {
  constructor() {
    this.rotation = 0;
  }

  update(energy) {
    const speed = 0.01 + energy * 0.05;
    this.rotation += speed;
    return this.rotation;
  }
}
```

### Color/Brightness

```javascript
// Brightness based on volume
function updateBrightness(element, volume) {
  const brightness = 0.5 + volume * 0.5; // 50% to 100%
  element.style.filter = `brightness(${brightness})`;
}

// Color shift based on frequency balance
function getReactiveColor(bass, mid, high) {
  // More bass = more red/magenta, more high = more cyan
  const r = Math.floor(bass * 255);
  const g = Math.floor(mid * 100);
  const b = Math.floor(high * 255);
  return `rgb(${r}, ${g}, ${b})`;
}

// Three.js emissive intensity
function updateGlow(material, bass) {
  material.emissiveIntensity = 1 + bass * 3;
}
```

### Opacity/Visibility

```javascript
// Fade based on volume
function updateOpacity(element, volume) {
  element.style.opacity = 0.3 + volume * 0.7;
}
```

## Beat Response

### Simple Beat Flash

```javascript
class BeatFlash {
  constructor(decayRate = 0.95) {
    this.intensity = 0;
    this.decayRate = decayRate;
  }

  trigger() {
    this.intensity = 1;
  }

  update() {
    this.intensity *= this.decayRate;
    return this.intensity;
  }
}

// Usage
const flash = new BeatFlash();

function animate() {
  if (beatDetector.detect(analyser)) {
    flash.trigger();
  }

  const intensity = flash.update();
  element.style.backgroundColor = `rgba(0, 245, 255, ${intensity})`;

  requestAnimationFrame(animate);
}
```

### Beat Scale Pop

```javascript
class BeatPop {
  constructor(popScale = 1.3, decayRate = 0.9) {
    this.scale = 1;
    this.targetScale = 1;
    this.popScale = popScale;
    this.decayRate = decayRate;
  }

  trigger() {
    this.targetScale = this.popScale;
  }

  update() {
    // Lerp toward target, then decay target back to 1
    this.scale += (this.targetScale - this.scale) * 0.3;
    this.targetScale = 1 + (this.targetScale - 1) * this.decayRate;
    return this.scale;
  }
}
```

### Beat Spawn

```javascript
class BeatSpawner {
  constructor(onSpawn) {
    this.onSpawn = onSpawn;
    this.cooldown = 0;
    this.minInterval = 200; // ms
  }

  check(isBeat) {
    if (isBeat && this.cooldown <= 0) {
      this.onSpawn();
      this.cooldown = this.minInterval;
    }
    this.cooldown -= 16; // Assuming 60fps
  }
}

// Usage: spawn particles on beat
const spawner = new BeatSpawner(() => {
  particleSystem.emit(10);
});
```

## React Three Fiber Integration

### Audio Reactive Component

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

function AudioReactiveSphere({ audioData }) {
  const meshRef = useRef();
  const materialRef = useRef();

  useFrame(() => {
    if (!audioData || !meshRef.current) return;

    const { bass, mid, high, isBeat } = audioData;

    // Scale on bass
    const scale = 1 + bass * 0.5;
    meshRef.current.scale.setScalar(scale);

    // Rotation speed on mid
    meshRef.current.rotation.y += 0.01 + mid * 0.03;

    // Emissive on high
    if (materialRef.current) {
      materialRef.current.emissiveIntensity = 1 + high * 2;
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial
        ref={materialRef}
        color="#111"
        emissive="#00F5FF"
        emissiveIntensity={1}
      />
    </mesh>
  );
}
```

### Audio Context Hook

```tsx
function useAudioAnalysis(playerRef) {
  const [data, setData] = useState(null);
  const analyserRef = useRef(null);
  const mapperRef = useRef(null);

  useEffect(() => {
    analyserRef.current = new Tone.Analyser('fft', 256);
    mapperRef.current = new AudioReactiveMapper(analyserRef.current);

    if (playerRef.current) {
      playerRef.current.connect(analyserRef.current);
    }

    return () => analyserRef.current?.dispose();
  }, []);

  useFrame(() => {
    if (mapperRef.current) {
      setData(mapperRef.current.getValues());
    }
  });

  return data;
}
```

## Post-Processing Integration

### Audio-Reactive Bloom

```tsx
function AudioReactiveBloom({ audioData }) {
  const bloomRef = useRef();

  useFrame(() => {
    if (bloomRef.current && audioData) {
      // Bass drives bloom intensity
      bloomRef.current.intensity = 1 + audioData.bass * 2;

      // High frequencies lower threshold (more bloom)
      bloomRef.current.luminanceThreshold = 0.3 - audioData.high * 0.2;
    }
  });

  return (
    <EffectComposer>
      <Bloom ref={bloomRef} luminanceThreshold={0.2} intensity={1} />
    </EffectComposer>
  );
}
```

### Audio-Reactive Chromatic Aberration

```tsx
function AudioReactiveChroma({ audioData }) {
  const chromaRef = useRef();

  useFrame(() => {
    if (chromaRef.current && audioData) {
      // High frequencies drive aberration
      const offset = 0.001 + audioData.high * 0.005;
      chromaRef.current.offset.set(offset, offset * 0.5);
    }
  });

  return <ChromaticAberration ref={chromaRef} offset={[0.002, 0.001]} />;
}
```

## GSAP Integration

### Audio-Driven Timeline

```javascript
class AudioTimeline {
  constructor() {
    this.timeline = gsap.timeline({ paused: true });
    this.progress = 0;
  }

  build(duration) {
    this.timeline
      .to('.element', { scale: 1.5 }, 0)
      .to('.element', { rotation: 360 }, duration * 0.5)
      .to('.element', { scale: 1 }, duration);
  }

  updateWithAudio(bass) {
    // Map bass to timeline progress
    const targetProgress = this.progress + bass * 0.02;
    this.progress = Math.min(1, targetProgress);
    this.timeline.progress(this.progress);
  }
}
```

### Beat-Triggered GSAP

```javascript
function createBeatAnimation(element) {
  return gsap.timeline({ paused: true })
    .to(element, {
      scale: 1.2,
      duration: 0.1,
      ease: 'power2.out'
    })
    .to(element, {
      scale: 1,
      duration: 0.3,
      ease: 'power2.out'
    });
}

// On beat
if (isBeat) {
  beatAnimation.restart();
}
```

## Complete System Example

```javascript
class AudioVisualSystem {
  constructor(player, visualElements) {
    this.player = player;
    this.elements = visualElements;

    // Analysis
    this.analyser = new Tone.Analyser('fft', 256);
    this.mapper = new AudioReactiveMapper(this.analyser);
    this.beatDetector = new BeatDetector();

    // Reactive controllers
    this.beatFlash = new BeatFlash();
    this.beatPop = new BeatPop();

    // Connect
    this.player.connect(this.analyser);
    this.player.toDestination();
  }

  update() {
    const values = this.mapper.getValues();
    const isBeat = this.beatDetector.detect(this.analyser);

    if (isBeat) {
      this.beatFlash.trigger();
      this.beatPop.trigger();
    }

    const flashIntensity = this.beatFlash.update();
    const popScale = this.beatPop.update();

    // Apply to visuals
    this.elements.background.style.opacity = 0.5 + values.bass * 0.5;
    this.elements.circle.style.transform = `scale(${popScale})`;
    this.elements.glow.style.boxShadow =
      `0 0 ${flashIntensity * 50}px rgba(0, 245, 255, ${flashIntensity})`;
  }

  start() {
    const animate = () => {
      this.update();
      requestAnimationFrame(animate);
    };
    animate();
  }
}
```

## Temporal Collapse Integration

```javascript
const TEMPORAL_MAPPINGS = {
  // Digit glow intensity
  digitGlow: (bass, mid) => 1 + bass * 2 + mid,

  // Particle emission rate
  particleRate: (bass, isBeat) => isBeat ? 50 : bass * 20,

  // Background pulse
  backgroundBrightness: (bass) => 1 + bass * 0.3,

  // Time dilation visual (warp effect)
  warpIntensity: (high) => high * 0.5,

  // Vignette darkness (close in on beat)
  vignetteDarkness: (isBeat, current) => isBeat ? 0.7 : current * 0.95,

  // Chromatic aberration (glitch on high)
  chromaticOffset: (high) => 0.001 + high * 0.004
};

function applyTemporalMappings(audioData, visuals) {
  const { bass, mid, high, isBeat } = audioData;

  visuals.digitMaterial.emissiveIntensity =
    TEMPORAL_MAPPINGS.digitGlow(bass, mid);

  visuals.particles.emissionRate =
    TEMPORAL_MAPPINGS.particleRate(bass, isBeat);

  visuals.background.brightness =
    TEMPORAL_MAPPINGS.backgroundBrightness(bass);

  visuals.bloom.intensity =
    1.5 + bass * 1.5;

  visuals.chromatic.offset =
    TEMPORAL_MAPPINGS.chromaticOffset(high);
}
```

## Performance Tips

```javascript
// 1. Update at lower frequency if possible
let frameCount = 0;
function animate() {
  if (frameCount % 2 === 0) {
    updateAudioData();
  }
  applyVisuals();
  frameCount++;
}

// 2. Use smoothing to hide skipped frames
const smoother = new Smoother(0.95); // Higher = more smoothing

// 3. Batch DOM updates
function applyAllStyles(elements, values) {
  // Single reflow
  requestAnimationFrame(() => {
    elements.forEach((el, i) => {
      el.style.transform = `scale(${values[i]})`;
    });
  });
}

// 4. Use CSS variables for multiple elements
document.documentElement.style.setProperty('--audio-bass', bass);
// CSS: transform: scale(calc(1 + var(--audio-bass) * 0.2));
```

## Reference

- See `audio-playback` for audio loading and transport
- See `audio-analysis` for FFT and beat detection
- See `audio-router` for audio domain routing
