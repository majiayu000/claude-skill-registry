---
name: web-audio
description: Production-tested patterns for fault-tolerant browser audio with zero-lag rapid-fire support. Use when implementing sound effects, background music, voice feedback, or any audio playback in web applications. Covers AudioContext singleton, preloading, cloneNode for rapid-fire, autoplay handling, and Web Audio API effects.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Web Audio Browser Patterns

Production-tested patterns for fault-tolerant browser audio with zero-lag rapid-fire support.

## Related Skills

- **`javascript`**: Async patterns, cleanup in disconnectedCallback, singleton patterns
- **`web-components`**: Integrating audio with custom elements
- **`ux-feedback-patterns`**: Audio as part of user feedback
- **`ux-accessibility`**: Respecting prefers-reduced-motion for audio

---

## Rule 1: AudioContext is Expensive — Create Once

AudioContext creation is expensive and browsers limit the number of contexts. Create one per page, reuse forever.

```javascript
// ✅ Singleton AudioContext
class AudioService {
  static #audioContext = null;

  static getContext() {
    if (!this.#audioContext) {
      this.#audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    return this.#audioContext;
  }

  // Resume context on user interaction (required by browsers)
  static async ensureResumed() {
    const ctx = this.getContext();
    if (ctx.state === 'suspended') {
      await ctx.resume();
    }
    return ctx;
  }
}

// ❌ Never create context per sound
function badPlaySound() {
  const ctx = new AudioContext(); // Creates new context every time!
  // ...
}
```

**Why:** Browsers limit AudioContext instances. Creating contexts is slow and triggers garbage collection.

---

## Rule 2: Preload All Sounds at Startup

Load audio files once at startup, play instantly during gameplay. Never load audio on hot paths.

```javascript
// ✅ Preload into cache
class AudioService {
  static #sounds = new Map();
  static #loaded = false;

  static async preload() {
    if (this.#loaded) return;

    const soundFiles = {
      sparkle: '/audio/sfx/sparkle.mp3',
      success: '/audio/sfx/success.mp3',
      phaseComplete: '/audio/sfx/phase-complete.mp3',
      wordComplete: '/audio/sfx/word-complete.mp3',
      milestone: '/audio/sfx/milestone.mp3',
      click: '/audio/sfx/click.mp3',
      error: '/audio/sfx/error.mp3'
    };

    const loadPromises = Object.entries(soundFiles).map(async ([name, path]) => {
      try {
        const audio = new Audio(path);
        audio.preload = 'auto';
        // Wait for audio to be loaded enough to play
        await new Promise((resolve, reject) => {
          audio.addEventListener('canplaythrough', resolve, { once: true });
          audio.addEventListener('error', reject, { once: true });
          audio.load();
        });
        this.#sounds.set(name, audio);
      } catch (error) {
        console.warn(`Failed to load sound: ${name}`, error);
        // Don't throw - audio is non-critical
      }
    });

    await Promise.allSettled(loadPromises);
    this.#loaded = true;
  }

  static getSound(name) {
    return this.#sounds.get(name);
  }
}
```

**Why:** Network requests during gameplay cause lag. Preloading ensures instant playback.

---

## Rule 3: cloneNode() for Rapid-Fire Sounds

For sounds that trigger rapidly (hover, clicks, typing), use `cloneNode()` to create instant playable copies without network requests.

```javascript
// ✅ Clone for overlapping/rapid plays
static playHoverSound() {
  const cached = this.#sounds.get('hover');
  if (!cached) return;

  // Cancel currently playing instance
  if (this.#currentHover && !this.#currentHover.paused) {
    this.#currentHover.pause();
    this.#currentHover.currentTime = 0;
  }

  // Clone creates instant playable copy (no network request)
  this.#currentHover = cached.cloneNode();
  this.#currentHover.volume = 0.3;

  return this.#currentHover.play().catch(() => {});
}

// ✅ Generic rapid-fire pattern
static playRapidFire(name, volume = 0.5) {
  const cached = this.#sounds.get(name);
  if (!cached) return Promise.resolve();

  const clone = cached.cloneNode();
  clone.volume = volume;
  return clone.play().catch(() => {});
}

// ❌ Never create new Audio() on hot paths
function badRapidFire(path) {
  const audio = new Audio(path); // Network request every time!
  return audio.play();
}
```

**Why:** `new Audio(path)` triggers a network request. `cloneNode()` creates an instant copy from the cached audio buffer.

---

## Rule 4: Cancel Before Play — Prevent Audio Pile-Up

For sounds that shouldn't overlap (UI feedback, voice), cancel the previous instance before starting a new one.

```javascript
// ✅ Track and cancel current instance
class AudioService {
  static #currentVoice = null;

  static playVoiceFeedback(text) {
    // Cancel any currently playing voice
    if (this.#currentVoice && !this.#currentVoice.paused) {
      this.#currentVoice.pause();
      this.#currentVoice.currentTime = 0;
    }

    this.#currentVoice = this.#sounds.get('voice')?.cloneNode();
    if (!this.#currentVoice) return;

    this.#currentVoice.volume = 0.5;
    return this.#currentVoice.play().catch(() => {});
  }
}

// ✅ For overlapping sounds (celebrations), don't cancel - let them layer
static playCelebrationSound() {
  const cached = this.#sounds.get('celebration');
  if (!cached) return;

  // Clone without canceling previous - sounds can overlap
  const clone = cached.cloneNode();
  clone.volume = 0.7;
  return clone.play().catch(() => {});
}
```

**Why:** Without cancellation, rapid triggers create audio pile-up where dozens of sounds play simultaneously.

---

## Rule 5: Silent .catch() on Every .play()

Browser autoplay policies block audio until user interaction. Always catch and ignore these errors silently.

```javascript
// ✅ Silent catch - ALWAYS
audio.play().catch(() => {});

// ✅ With optional logging for development
audio.play().catch(e => {
  if (e.name !== 'NotAllowedError') {
    console.warn('Audio playback failed:', e);
  }
});

// ❌ Never leave .play() uncaught
audio.play(); // Throws on autoplay block!

// ❌ Don't let autoplay errors bubble up
async function badPlaySound() {
  await audio.play(); // Throws to caller on autoplay block
}
```

**Why:** Browsers block autoplay until user interaction. Uncaught promise rejections crash the application or flood the console.

---

## Rule 6: Window Globals for Hot-Reload Survival

For background music or persistent audio state, store singletons on `window` to survive module hot-reload during development.

```javascript
// ✅ Singleton survives hot-reload
if (typeof window.__AudioServiceClass === 'undefined') {
  window.__AudioServiceClass = class AudioService {
    #enabled = true;
    #volume = 0.5;
    #sounds = new Map();

    constructor() {
      // Restore state from previous instance
      this.#enabled = window.__audioEnabled ?? true;
      this.#volume = window.__audioVolume ?? 0.5;
    }

    setEnabled(enabled) {
      this.#enabled = enabled;
      window.__audioEnabled = enabled; // Persist across hot-reload
    }

    setVolume(volume) {
      this.#volume = volume;
      window.__audioVolume = volume;
    }
  };
}

if (!window.__audioServiceInstance) {
  window.__audioServiceInstance = new window.__AudioServiceClass();
}

export default window.__audioServiceInstance;
```

**Why:** During development, module hot-reload destroys and recreates module scope. Window globals persist, preventing audio restart.

---

## Rule 7: Volume Hierarchy by Sound Type

Different sound types serve different purposes and need different volume levels to feel balanced.

| Sound Type | Volume Range | Rationale |
|------------|--------------|-----------|
| Hover/Click | 0.2–0.3 | Subtle, frequent — shouldn't fatigue |
| Typing feedback | 0.2–0.3 | Very frequent — whisper quiet |
| Success/Error | 0.3–0.5 | Clear feedback, moderate frequency |
| Phase Complete | 0.4–0.6 | Meaningful milestone |
| Word Complete | 0.5–0.7 | Significant achievement |
| Milestone/Rank-Up | 0.7–0.8 | Big celebration moments |
| Background Music | 0.15–0.25 | Never dominate, support atmosphere |
| Warning/Alert | 0.4–0.5 | Attention-getting but not startling |

```javascript
// ✅ Volume constants
const VOLUMES = {
  MICRO: 0.25,      // sparkle, click, hover
  FEEDBACK: 0.4,    // success, error
  CELEBRATION: 0.6, // phase complete
  MAJOR: 0.75,      // word complete, milestone
  MUSIC: 0.2        // background
};

static playSparkle() {
  return this.playRapidFire('sparkle', VOLUMES.MICRO);
}

static playSuccess() {
  return this.play('success', VOLUMES.FEEDBACK);
}

static playMilestone() {
  return this.play('milestone', VOLUMES.MAJOR);
}
```

**Why:** Balanced audio creates professional feel. Loud frequent sounds cause fatigue; quiet celebrations feel anticlimactic.

---

## Rule 8: Respect prefers-reduced-motion for Audio

Users who prefer reduced motion often want reduced audio stimulation too. Check the preference and adjust.

```javascript
// ✅ Check preference and adjust
class AudioService {
  static #enabled = true;

  static {
    // Disable by default if user prefers reduced motion
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    this.#enabled = !mediaQuery.matches;

    // Listen for changes
    mediaQuery.addEventListener('change', (e) => {
      this.#enabled = !e.matches;
    });
  }

  static play(name, volume = 0.5) {
    if (!this.#enabled) return Promise.resolve();

    const sound = this.#sounds.get(name);
    if (!sound) return Promise.resolve();

    const clone = sound.cloneNode();
    clone.volume = volume;
    return clone.play().catch(() => {});
  }

  static setEnabled(enabled) {
    this.#enabled = enabled;
  }

  static get enabled() {
    return this.#enabled;
  }
}
```

**Why:** Accessibility includes audio. Users with vestibular disorders or sensory sensitivities benefit from reduced audio.

---

## Rule 9: Web Audio API for Effects (Reverb, Ducking)

Use Web Audio API for advanced effects like reverb, ducking, and filtering. Create nodes once, reuse forever.

### Sidechain Ducking (Lower Music When SFX Play)

```javascript
// ✅ Duck background music when sound effects play
class AudioService {
  static #musicGain = null;
  static #audioContext = null;

  static initMusicWithDucking(musicElement) {
    this.#audioContext = this.getContext();

    // Create source from music element
    const source = this.#audioContext.createMediaElementSource(musicElement);

    // Create gain node for ducking
    this.#musicGain = this.#audioContext.createGain();
    this.#musicGain.gain.value = 1.0;

    // Connect: source → gain → destination
    source.connect(this.#musicGain);
    this.#musicGain.connect(this.#audioContext.destination);
  }

  static duckMusicFor(durationMs = 1500) {
    if (!this.#musicGain || !this.#audioContext) return;

    const now = this.#audioContext.currentTime;

    // Quick duck down
    this.#musicGain.gain.setValueAtTime(this.#musicGain.gain.value, now);
    this.#musicGain.gain.linearRampToValueAtTime(0.1, now + 0.1);

    // Slow release back up
    setTimeout(() => {
      const releaseTime = this.#audioContext.currentTime;
      this.#musicGain.gain.linearRampToValueAtTime(1.0, releaseTime + 0.5);
    }, durationMs);
  }

  // Call duck when playing important sounds
  static playMilestone() {
    this.duckMusicFor(2000);
    return this.play('milestone', VOLUMES.MAJOR);
  }
}
```

### Hall Reverb Effect

```javascript
// ✅ Apply reverb effect
static applyHallReverb(duration = 2.0) {
  const ctx = this.getContext();

  // Create convolver for reverb (create once, reuse)
  if (!this.#convolver) {
    this.#convolver = ctx.createConvolver();
    this.#wetGain = ctx.createGain();
    this.#dryGain = ctx.createGain();

    // Generate impulse response
    const sampleRate = ctx.sampleRate;
    const length = sampleRate * duration;
    const impulse = ctx.createBuffer(2, length, sampleRate);

    for (let ch = 0; ch < 2; ch++) {
      const data = impulse.getChannelData(ch);
      for (let i = 0; i < length; i++) {
        // Exponential decay with noise
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2);
      }
    }
    this.#convolver.buffer = impulse;

    // Initial dry/wet mix
    this.#dryGain.gain.value = 1.0;
    this.#wetGain.gain.value = 0.0;
  }

  return { convolver: this.#convolver, wetGain: this.#wetGain, dryGain: this.#dryGain };
}
```

**Why:** Web Audio API enables professional audio effects without external libraries. Create nodes once to avoid performance issues.

---

## Rule 10: Text-to-Speech Integration

Use Web Speech API for reading text aloud, with user preference persistence.

```javascript
// ✅ TTS with preference check
class TTSService {
  static #enabled = false;

  static {
    this.#enabled = localStorage.getItem('ttsEnabled') === 'true';
  }

  static speak(text, options = {}) {
    if (!this.#enabled) return;
    if (!('speechSynthesis' in window)) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = options.rate ?? 0.9;   // Slightly slower for kids
    utterance.pitch = options.pitch ?? 1.0;
    utterance.volume = options.volume ?? 0.8;

    // Cancel any current speech
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  }

  static stop() {
    speechSynthesis.cancel();
  }

  static setEnabled(enabled) {
    this.#enabled = enabled;
    localStorage.setItem('ttsEnabled', String(enabled));
  }

  static get enabled() {
    return this.#enabled;
  }

  static get supported() {
    return 'speechSynthesis' in window;
  }
}
```

**Why:** TTS helps emergent readers and improves accessibility. User preference should persist across sessions.

---

## Web Audio Node Routing Reference

```
Simple Playback:
  Source ──────────────────────────────► Destination

With Volume Control:
  Source ──► GainNode ─────────────────► Destination

Wet/Dry Effects (Reverb):
  Source ─┬─► DryGain ─────────────────┬► Destination
          └─► Effect ──► WetGain ──────┘

Sidechain Ducking:
  Music ──► MusicGain ─────────────────► Destination
  SFX ────► SFXGain ───────────────────► Destination
            (MusicGain.gain reduced when SFX plays)
```

### Common Web Audio Nodes

| Node | Purpose |
|------|---------|
| `GainNode` | Volume control |
| `ConvolverNode` | Reverb, room simulation |
| `DelayNode` | Echo, delay effects |
| `BiquadFilterNode` | EQ, low/high pass |
| `DynamicsCompressorNode` | Limiting, compression |
| `AnalyserNode` | Visualization data |

---

## Complete AudioService Implementation

```javascript
/**
 * AudioService - Centralized audio management
 *
 * Skills applied:
 * - web-audio: All 10 rules
 * - javascript: Singleton, cleanup, error handling
 * - ux-accessibility: prefers-reduced-motion
 */
class AudioService {
  static #sounds = new Map();
  static #enabled = true;
  static #volume = 0.5;
  static #currentByCategory = new Map();
  static #audioContext = null;
  static #loaded = false;

  // Volume hierarchy
  static VOLUMES = {
    MICRO: 0.25,
    FEEDBACK: 0.4,
    CELEBRATION: 0.6,
    MAJOR: 0.75,
    MUSIC: 0.2
  };

  static {
    // Respect reduced motion preference
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    this.#enabled = !mq.matches;
    mq.addEventListener('change', (e) => { this.#enabled = !e.matches; });
  }

  static async preload() {
    if (this.#loaded) return;

    const files = {
      sparkle: '/audio/sfx/sparkle.mp3',
      success: '/audio/sfx/success.mp3',
      phaseComplete: '/audio/sfx/phase-complete.mp3',
      wordComplete: '/audio/sfx/word-complete.mp3',
      milestone: '/audio/sfx/milestone.mp3',
      click: '/audio/sfx/click.mp3',
      error: '/audio/sfx/error.mp3'
    };

    await Promise.allSettled(
      Object.entries(files).map(async ([name, path]) => {
        try {
          const audio = new Audio(path);
          audio.preload = 'auto';
          this.#sounds.set(name, audio);
        } catch (e) {
          console.warn(`Audio load failed: ${name}`, e);
        }
      })
    );

    this.#loaded = true;
  }

  static play(name, volume = 0.5, category = null) {
    if (!this.#enabled) return Promise.resolve();

    const cached = this.#sounds.get(name);
    if (!cached) return Promise.resolve();

    // Cancel previous in same category
    if (category) {
      const prev = this.#currentByCategory.get(category);
      if (prev && !prev.paused) {
        prev.pause();
        prev.currentTime = 0;
      }
    }

    const clone = cached.cloneNode();
    clone.volume = Math.min(1, volume * this.#volume);

    if (category) {
      this.#currentByCategory.set(category, clone);
    }

    return clone.play().catch(() => {});
  }

  // Convenience methods
  static playSparkle() { return this.play('sparkle', this.VOLUMES.MICRO); }
  static playSuccess() { return this.play('success', this.VOLUMES.FEEDBACK, 'feedback'); }
  static playError() { return this.play('error', this.VOLUMES.FEEDBACK, 'feedback'); }
  static playPhaseComplete() { return this.play('phaseComplete', this.VOLUMES.CELEBRATION); }
  static playWordComplete() { return this.play('wordComplete', this.VOLUMES.MAJOR); }
  static playMilestone() { return this.play('milestone', this.VOLUMES.MAJOR); }
  static playClick() { return this.play('click', this.VOLUMES.MICRO, 'ui'); }

  static setEnabled(enabled) { this.#enabled = enabled; }
  static setVolume(v) { this.#volume = Math.max(0, Math.min(1, v)); }
  static get enabled() { return this.#enabled; }
  static get volume() { return this.#volume; }
}

export { AudioService };
export const audioService = AudioService;
```

---

## Checklist

- [ ] AudioContext created once per page
- [ ] All sounds preloaded at startup
- [ ] `cloneNode()` used for rapid-fire sounds
- [ ] Previous sound canceled before playing (where appropriate)
- [ ] Silent `.catch(() => {})` on every `.play()`
- [ ] Window globals for hot-reload survival (if needed)
- [ ] Volume hierarchy applied by sound type
- [ ] `prefers-reduced-motion` respected
- [ ] Web Audio nodes created once, reused
- [ ] TTS preference persisted to localStorage
