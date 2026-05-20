---
name: 2000s-visualization-expert
description: Expert in 2000s-era music visualization (Milkdrop, AVS, Geiss) and modern WebGL implementations. Specializes in Butterchurn integration, Web Audio API AnalyserNode FFT data, GLSL shaders for audio-reactive visuals, and psychedelic generative art. Activate on "Milkdrop", "music visualization", "WebGL visualizer", "Butterchurn", "audio reactive", "FFT visualization", "spectrum analyzer". NOT for simple bar charts/waveforms (use basic canvas), video editing, or non-audio visuals.
allowed-tools: Read,Write,Edit,Bash,WebFetch
category: Design & Creative
tags:
  - audio
  - webgl
  - visualization
  - shaders
  - music
pairs-with:
  - skill: sound-engineer
    reason: Audio processing feeds the visualizations
  - skill: metal-shader-expert
    reason: Advanced GPU shader techniques
---

# 2000s Music Visualization Expert

Expert in recreating the legendary 2000s music visualization era - Milkdrop, AVS, Geiss - using modern WebGL and Web Audio APIs.

## When to Use

✅ **Use for:**
- Implementing Milkdrop-style psychedelic visualizations
- Butterchurn library integration (WebGL Milkdrop)
- Web Audio API AnalyserNode FFT/waveform extraction
- GLSL fragment shaders for audio-reactive effects
- Full-screen immersive music experiences
- Real-time beat detection and audio analysis
- Preset systems and visualization transitions

❌ **NOT for:**
- Simple spectrum bar charts (use Canvas 2D)
- Static audio waveform displays
- Video editing or processing
- Non-audio generative art
- Audio playback/streaming issues (use audio-engineer skills)

## The Golden Era (Summary)

| Era | Key Software | Innovation |
|-----|--------------|------------|
| **1998-2000** | Geiss | Simple plasma effects, DirectX |
| **2001-2007** | Milkdrop 1 & 2 | Per-pixel equations, preset system |
| **2007-2015** | Decline | Streaming services rise |
| **2018-Present** | Butterchurn | WebGL renaissance |

**Milkdrop's magic**: Layering simple effects - blur, zoom, rotation, color shift - with audio-reactive parameters.

→ See `references/butterchurn-guide.md` for full history and integration.

## Core Technologies

### Butterchurn (WebGL Milkdrop)
- 1.7k GitHub stars, MIT licensed
- Full preset compatibility with original Milkdrop
- npm: `butterchurn`, `butterchurn-presets`

```typescript
import butterchurn from 'butterchurn';
const visualizer = butterchurn.createVisualizer(audioContext, canvas, {
  width: window.innerWidth,
  height: window.innerHeight,
  pixelRatio: window.devicePixelRatio || 1,
});
visualizer.connectAudio(audioNode);
visualizer.loadPreset(preset, 2.0);  // 2s blend
```

### Web Audio API FFT
```typescript
const analyser = audioContext.createAnalyser();
analyser.fftSize = 2048;
analyser.smoothingTimeConstant = 0.8;
const frequencyData = new Uint8Array(analyser.frequencyBinCount);
analyser.getByteFrequencyData(frequencyData);
```

**Critical**: FFT bins are linear but hearing is logarithmic! Use logarithmic mapping.

→ See `references/web-audio-fft.md` for frequency band extraction.

### GLSL Shaders
Pass audio data as 1D texture, use uniforms for bass/mid/treble:

```glsl
uniform float u_bass;
float glow = smoothstep(0.5 - u_bass * 0.3, 0.0, dist);
```

→ See `references/glsl-shaders.md` for complete patterns.

## Anti-Patterns to Avoid

### 1. Ignoring AudioContext State
**What it looks like**: Visualization silently fails
**Why it's wrong**: AudioContext starts suspended, needs user interaction
**Fix**: Resume on click: `await audioContext.resume()`

### 2. Linear Frequency Display
**What it looks like**: Bass dominates, treble invisible
**Why it's wrong**: FFT bins are linear; first 100 bins might be 0-2kHz
**Fix**: Use logarithmic bin mapping (code in references)

### 3. No Smoothing
**What it looks like**: Jittery, seizure-inducing visuals
**Why it's wrong**: Raw FFT data is noisy frame-to-frame
**Fix**: `analyserNode.smoothingTimeConstant = 0.7`

### 4. requestAnimationFrame Without Cleanup
**What it looks like**: Memory leaks, multiple render loops
**Fix**: Store animation ID, call `cancelAnimationFrame` on unmount

### 5. Hardcoded Canvas Size
**What it looks like**: Blurry on retina, wrong aspect ratio
**Fix**: Multiply by `devicePixelRatio`, handle resize events

### 6. Blocking Main Thread
**What it looks like**: Choppy audio, dropped frames
**Why it's wrong**: Heavy shader compilation on UI thread
**Fix**: Compile shaders during loading, not during playback

## Preset Recommendations

**Psychedelic/Trippy:**
- `Flexi, martin + geiss - dedicated to the sherwin maxawow`
- `Rovastar - Fractopia`

**Smooth/Chill:**
- `Flexi - predator-prey-spirals`
- `Geiss - Cosmic Strings 2`

**High Energy:**
- `Flexi + Martin - disconnected`
- `shifter - tumbling cubes`

## Integration Checklist

- [ ] AudioContext created and resumed on user interaction
- [ ] AnalyserNode connected to audio source
- [ ] Canvas sized correctly (account for devicePixelRatio)
- [ ] Render loop with requestAnimationFrame
- [ ] Cleanup on unmount (cancelAnimationFrame)
- [ ] Preset loading with blend time
- [ ] Resize handling
- [ ] Full-screen support with ESC to exit
- [ ] Track info overlay (z-index above canvas)
- [ ] Cursor hiding after inactivity

## Performance Tips

1. **Lower texture ratio** for older GPUs: `textureRatio: 0.5`
2. **Reduce fftSize** if not needed: 512 or 1024 vs 2048
3. **Use `will-change: transform`** on canvas
4. **Avoid DOM updates** during render loop
5. **Profile with Chrome DevTools** GPU timeline

## References

→ `references/butterchurn-guide.md` - Complete Butterchurn integration
→ `references/web-audio-fft.md` - FFT extraction and frequency analysis
→ `references/glsl-shaders.md` - Audio-reactive shader patterns

---

**This skill covers**: Butterchurn/Milkdrop | Web Audio FFT | GLSL shaders | Full-screen visualization | Audio-reactive art
