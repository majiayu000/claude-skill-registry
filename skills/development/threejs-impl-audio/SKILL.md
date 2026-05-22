---
name: threejs-impl-audio
description: >
  Use when adding sound to a Three.js scene: background music, 3D
  spatial audio, or audio visualization. Prevents the common mistake
  of ignoring browser autoplay policy, not attaching AudioListener to
  camera, or wrong distance model. Covers AudioListener, Audio,
  PositionalAudio, AudioAnalyser.
  Keywords: audio, sound, AudioListener, PositionalAudio, 3D audio,
  spatial audio, music, AudioAnalyser, Web Audio API.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-audio

## Quick Reference

### Class Hierarchy

```
EventDispatcher
  └── Object3D
        ├── AudioListener    (receiver — attach to camera)
        ├── Audio            (non-positional — background music, UI sounds)
        └── PositionalAudio  (3D spatial — attached to scene objects)
```

Supporting classes:
- `AudioLoader` — loads audio files into `AudioBuffer`
- `AudioAnalyser` — real-time frequency analysis for visualization

### Architecture Overview

| Component | Role | Attach To |
|-----------|------|-----------|
| `AudioListener` | Virtual ear (Web Audio API destination) | Camera (ALWAYS) |
| `Audio` | Non-positional sound (same volume everywhere) | Any Object3D or scene |
| `PositionalAudio` | 3D spatial sound (volume depends on distance) | Mesh or Object3D in scene |
| `AudioLoader` | Async audio file loader | N/A (utility) |
| `AudioAnalyser` | FFT frequency data extractor | Wraps an Audio instance |

### Critical Warnings

**NEVER** call `sound.play()` without first ensuring the `AudioContext` is resumed after user interaction. Modern browsers ALWAYS suspend the AudioContext until a user gesture (click, tap, keypress) occurs.

**NEVER** create more than one `AudioListener` per scene. Multiple listeners produce undefined spatialization behavior.

**NEVER** set `autoplay = true` and expect playback without user interaction. The browser WILL block it silently.

**ALWAYS** attach the `AudioListener` to the camera. If attached to another object, spatial audio calculations use the wrong reference position.

**ALWAYS** call `listener.context.resume()` inside a user interaction handler before playing any audio.

**NEVER** forget to handle the `onError` callback in `AudioLoader.load()`. Missing audio files fail silently without error handling.

---

## AudioListener Setup

The `AudioListener` is the scene's virtual microphone. It wraps the Web Audio API's `AudioContext` and `AudioDestinationNode`.

```js
import * as THREE from 'three';

const listener = new THREE.AudioListener();
camera.add( listener ); // ALWAYS add to camera
```

### Master Volume Control

```js
listener.setMasterVolume( 0.8 ); // range [0, 1]
const vol = listener.getMasterVolume(); // returns 0.8
```

### Global Audio Filter

```js
const filter = listener.context.createBiquadFilter();
filter.type = 'lowpass';
filter.frequency.value = 1000;
listener.setFilter( filter );
// Later: listener.removeFilter();
```

---

## Audio (Non-Positional)

Use `Audio` for background music, ambient soundscapes, and UI feedback sounds. Volume is identical regardless of listener position.

### Loading and Playing

```js
const sound = new THREE.Audio( listener );
const audioLoader = new THREE.AudioLoader();

audioLoader.load( 'music.mp3', ( buffer ) => {
    sound.setBuffer( buffer );
    sound.setLoop( true );
    sound.setVolume( 0.5 );
    // Do NOT call sound.play() here — wait for user interaction
});
```

### Autoplay Policy Compliance (MANDATORY)

```js
document.addEventListener( 'click', () => {
    if ( listener.context.state === 'suspended' ) {
        listener.context.resume();
    }
    if ( !sound.isPlaying ) {
        sound.play();
    }
}, { once: true } );
```

### Playback Control

```js
sound.play();                    // start playback
sound.pause();                   // pause (resume with play())
sound.stop();                    // stop and reset to beginning
sound.setPlaybackRate( 1.5 );   // 1.5x speed
sound.setDetune( -100 );        // pitch down 1 semitone (100 cents)
```

### Alternative Sources

```js
// HTML5 media element (for streaming large files)
const audioEl = new Audio( 'long-track.mp3' );
sound.setMediaElementSource( audioEl );

// Microphone input
navigator.mediaDevices.getUserMedia( { audio: true } ).then( ( stream ) => {
    sound.setMediaStreamSource( stream );
});
```

---

## PositionalAudio (3D Spatial)

Use `PositionalAudio` for sounds that exist at a location in the scene. Volume and stereo panning change based on the listener's distance and orientation.

### Basic Setup

```js
const positionalSound = new THREE.PositionalAudio( listener );

audioLoader.load( 'engine.ogg', ( buffer ) => {
    positionalSound.setBuffer( buffer );
    positionalSound.setRefDistance( 20 );
    positionalSound.setRolloffFactor( 1 );
    positionalSound.setDistanceModel( 'inverse' );
    positionalSound.setLoop( true );
    positionalSound.setVolume( 0.5 );
});

mesh.add( positionalSound ); // sound position follows the mesh
```

### Distance Model Decision Tree

| Model | When to Use | Behavior |
|-------|-------------|----------|
| `'inverse'` (default) | Realistic environments | Gradual rolloff; NEVER reaches zero |
| `'linear'` | Controlled radius (e.g., room-based) | Volume drops to zero at `maxDistance` |
| `'exponential'` | Dramatic close/far contrast | Steep falloff curve |

**Choosing parameters:**

- **`refDistance`** — Distance at which volume is 100%. Set to the "comfortable listening range" in scene units. Typical: `1` to `20`.
- **`maxDistance`** — ONLY matters for `'linear'` model. Ignored by `'inverse'` and `'exponential'`.
- **`rolloffFactor`** — Speed of volume decrease. For `'inverse'`: `1` = realistic. For `'linear'`: `1` = full range. Higher values = faster rolloff.

### Directional Audio Cone

```js
positionalSound.setDirectionalCone( 180, 360, 0.1 );
// coneInnerAngle: 180° — full volume zone
// coneOuterAngle: 360° — transition zone
// coneOuterGain: 0.1  — volume outside outer cone (10%)
```

---

## AudioLoader

ALWAYS use `AudioLoader` to load audio files. It returns an `AudioBuffer` via callback.

```js
const loader = new THREE.AudioLoader();

loader.load(
    'sound.ogg',
    ( buffer ) => { sound.setBuffer( buffer ); },   // onLoad
    ( xhr ) => { console.log( (xhr.loaded / xhr.total * 100) + '% loaded' ); }, // onProgress
    ( err ) => { console.error( 'Audio load failed:', err ); }  // onError — ALWAYS handle
);
```

**Supported formats:** MP3, OGG, WAV, AAC. OGG has the best compression-to-quality ratio but is NOT supported in Safari. ALWAYS provide MP3 as a fallback for cross-browser compatibility.

---

## AudioAnalyser

Wraps the Web Audio API's `AnalyserNode` for real-time frequency visualization.

```js
const analyser = new THREE.AudioAnalyser( sound, 256 );
// fftSize MUST be a power of 2: 32, 64, 128, 256, 512, 1024, 2048

function animate() {
    requestAnimationFrame( animate );

    const data = analyser.getFrequencyData();    // Uint8Array, length = fftSize / 2
    const avg = analyser.getAverageFrequency();  // number (0-255)

    // Drive visuals from audio data
    mesh.scale.y = 1 + avg / 128;
    renderer.render( scene, camera );
}
```

### Frequency Data Details

- `getFrequencyData()` returns a `Uint8Array` with `fftSize / 2` elements
- Each element ranges from `0` to `255` (decibel magnitude)
- Index `0` = lowest frequency, last index = highest frequency
- `getAverageFrequency()` returns the arithmetic mean of all bins

---

## Integration Checklist

1. Create ONE `AudioListener` and add it to the camera
2. Create `Audio` or `PositionalAudio` with the listener
3. Load audio with `AudioLoader`
4. Set buffer, volume, loop, and distance properties
5. Add user interaction handler to resume `AudioContext`
6. Call `play()` ONLY after user interaction
7. For spatial audio: add `PositionalAudio` as child of the target mesh

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for AudioListener, Audio, PositionalAudio, AudioLoader, AudioAnalyser
- [references/examples.md](references/examples.md) -- Working code examples for common audio scenarios
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with Three.js audio

### Official Sources

- https://threejs.org/docs/#api/en/audio/AudioListener
- https://threejs.org/docs/#api/en/audio/Audio
- https://threejs.org/docs/#api/en/audio/PositionalAudio
- https://threejs.org/docs/#api/en/audio/AudioAnalyser
- https://threejs.org/docs/#api/en/loaders/AudioLoader
