---
name: audio-playback
description: Audio playback using Tone.js including players, transport, scheduling, and loading audio. Use when implementing background music, sound effects, audio synchronization, or timed audio events. Essential for any audio-enabled web application.
---

# Audio Playback

Audio playback and scheduling with Tone.js.

## Quick Start

```bash
npm install tone
```

```javascript
import * as Tone from 'tone';

// Simple playback
const player = new Tone.Player('/audio/music.mp3').toDestination();

// Must start audio context after user interaction
document.addEventListener('click', async () => {
  await Tone.start();
  player.start();
});
```

## Core Concepts

### Audio Context Initialization

```javascript
import * as Tone from 'tone';

// Audio context requires user gesture to start
async function initAudio() {
  await Tone.start();
  console.log('Audio context started');
}

// Common pattern: init on first click
document.addEventListener('click', initAudio, { once: true });
```

### Player Basics

```javascript
// Create player
const player = new Tone.Player({
  url: '/audio/track.mp3',
  loop: true,
  autostart: false,
  onload: () => console.log('Loaded')
}).toDestination();

// Control
player.start();
player.stop();
player.seek(10); // Seek to 10 seconds
player.volume.value = -6; // Volume in dB

// Properties
player.state;      // 'started' | 'stopped'
player.loaded;     // boolean
player.duration;   // in seconds
```

### Loading Audio

```javascript
// Single file
const player = new Tone.Player('/audio/music.mp3');
await player.load('/audio/music.mp3');

// Multiple files with Players
const players = new Tone.Players({
  kick: '/audio/kick.mp3',
  snare: '/audio/snare.mp3',
  hihat: '/audio/hihat.mp3'
}).toDestination();

// Access individual player
players.player('kick').start();

// Buffer for programmatic access
const buffer = new Tone.Buffer('/audio/sample.mp3', () => {
  console.log('Buffer loaded, duration:', buffer.duration);
});
```

## Transport

### Basic Transport Control

```javascript
// Global transport (master clock)
Tone.Transport.start();
Tone.Transport.stop();
Tone.Transport.pause();

// Position
Tone.Transport.position = '0:0:0'; // bars:beats:sixteenths
Tone.Transport.seconds = 10;        // in seconds

// Tempo
Tone.Transport.bpm.value = 120;

// Time signature
Tone.Transport.timeSignature = [4, 4];
```

### Scheduling Events

```javascript
// Schedule at specific time
Tone.Transport.schedule((time) => {
  player.start(time);
}, '0:0:0');

// Schedule repeating
Tone.Transport.scheduleRepeat((time) => {
  synth.triggerAttackRelease('C4', '8n', time);
}, '4n'); // Every quarter note

// Schedule once
Tone.Transport.scheduleOnce((time) => {
  console.log('One time event at', time);
}, '4:0:0'); // At bar 4
```

### Time Notation

| Format | Description | Example |
|--------|-------------|---------|
| `'4n'` | Quarter note | One beat at 4/4 |
| `'8n'` | Eighth note | Half a beat |
| `'16n'` | Sixteenth note | Quarter beat |
| `'1m'` | One measure | Full bar |
| `'2:0:0'` | Bars:beats:16ths | Start of bar 2 |
| `'+0.5'` | Relative seconds | 0.5s from now |
| `0.5` | Absolute seconds | At 0.5 seconds |

## Effects Chain

### Basic Signal Flow

```javascript
// Source → Effects → Destination
const player = new Tone.Player('/audio/track.mp3');
const reverb = new Tone.Reverb(2);
const volume = new Tone.Volume(-6);

player.chain(reverb, volume, Tone.Destination);
```

### Common Effects

```javascript
// Reverb
const reverb = new Tone.Reverb({
  decay: 2.5,
  wet: 0.4
});

// Delay
const delay = new Tone.FeedbackDelay({
  delayTime: '8n',
  feedback: 0.3,
  wet: 0.25
});

// Filter
const filter = new Tone.Filter({
  frequency: 1000,
  type: 'lowpass',
  Q: 2
});

// Compressor
const compressor = new Tone.Compressor({
  threshold: -24,
  ratio: 4,
  attack: 0.003,
  release: 0.25
});

// Volume/Gain
const volume = new Tone.Volume(-12);
const gain = new Tone.Gain(0.5);
```

### Effect Wet/Dry Mix

```javascript
const reverb = new Tone.Reverb(2);
reverb.wet.value = 0.5; // 50% wet, 50% dry

// Automate wet mix
reverb.wet.rampTo(1, 2); // Ramp to 100% wet over 2 seconds
```

## Playback Patterns

### Music Player

```javascript
class MusicPlayer {
  constructor() {
    this.player = new Tone.Player().toDestination();
    this.isPlaying = false;
  }

  async load(url) {
    await this.player.load(url);
  }

  async play() {
    await Tone.start();
    this.player.start();
    this.isPlaying = true;
  }

  pause() {
    this.player.stop();
    this.isPlaying = false;
  }

  setVolume(db) {
    this.player.volume.value = db;
  }

  seek(seconds) {
    const wasPlaying = this.isPlaying;
    this.player.stop();
    this.player.seek(seconds);
    if (wasPlaying) this.player.start();
  }

  get duration() {
    return this.player.buffer?.duration || 0;
  }

  get currentTime() {
    return this.player.immediate();
  }
}
```

### Sound Effects Manager

```javascript
class SFXManager {
  constructor() {
    this.sounds = {};
  }

  async load(name, url) {
    const player = new Tone.Player(url).toDestination();
    await player.load(url);
    this.sounds[name] = player;
  }

  play(name) {
    const sound = this.sounds[name];
    if (sound) {
      sound.stop();  // Stop if already playing
      sound.start();
    }
  }

  setVolume(name, db) {
    if (this.sounds[name]) {
      this.sounds[name].volume.value = db;
    }
  }

  setMasterVolume(db) {
    Tone.Destination.volume.value = db;
  }
}

// Usage
const sfx = new SFXManager();
await sfx.load('click', '/audio/click.mp3');
await sfx.load('success', '/audio/success.mp3');
sfx.play('click');
```

### Looping Ambient Layer

```javascript
class AmbientLayer {
  constructor(url) {
    this.player = new Tone.Player({
      url,
      loop: true,
      fadeIn: 2,
      fadeOut: 2
    });

    this.volume = new Tone.Volume(-12);
    this.reverb = new Tone.Reverb(4);

    this.player.chain(this.reverb, this.volume, Tone.Destination);
  }

  async start() {
    await Tone.start();
    this.player.start();
  }

  stop() {
    this.player.stop();
  }

  setIntensity(value) {
    // 0-1 range
    this.volume.volume.value = -24 + (value * 18); // -24dB to -6dB
    this.reverb.wet.value = 0.3 + (value * 0.4);   // 30% to 70% wet
  }
}
```

## Crossfading

```javascript
class CrossfadePlayer {
  constructor() {
    this.playerA = new Tone.Player();
    this.playerB = new Tone.Player();
    this.crossfade = new Tone.CrossFade();

    this.playerA.connect(this.crossfade.a);
    this.playerB.connect(this.crossfade.b);
    this.crossfade.toDestination();

    this.current = 'a';
  }

  async loadAndCrossfade(url, duration = 2) {
    const nextPlayer = this.current === 'a' ? this.playerB : this.playerA;
    const targetFade = this.current === 'a' ? 1 : 0;

    await nextPlayer.load(url);
    nextPlayer.start();

    this.crossfade.fade.rampTo(targetFade, duration);

    // Stop old player after crossfade
    setTimeout(() => {
      const oldPlayer = this.current === 'a' ? this.playerA : this.playerB;
      oldPlayer.stop();
    }, duration * 1000);

    this.current = this.current === 'a' ? 'b' : 'a';
  }
}
```

## Synced Playback

### Sync to Transport

```javascript
// Player synced to transport
const player = new Tone.Player('/audio/track.mp3');
player.sync().start(0).toDestination();

// Now transport controls playback
Tone.Transport.start();
Tone.Transport.pause();
Tone.Transport.stop();
```

### Multiple Synced Players

```javascript
const drums = new Tone.Player('/audio/drums.mp3').toDestination();
const bass = new Tone.Player('/audio/bass.mp3').toDestination();
const melody = new Tone.Player('/audio/melody.mp3').toDestination();

// Sync all to transport
drums.sync().start(0);
bass.sync().start(0);
melody.sync().start(0);

// Set tempo
Tone.Transport.bpm.value = 120;

// Control all with transport
Tone.Transport.start();
```

## Temporal Collapse Patterns

### Countdown Audio Manager

```javascript
class CountdownAudio {
  constructor() {
    this.ambient = new Tone.Player({ loop: true });
    this.tickSound = new Tone.Player();
    this.finalTicks = new Tone.Player();
    this.celebration = new Tone.Player();

    // Effects
    this.filter = new Tone.Filter(2000, 'lowpass');
    this.reverb = new Tone.Reverb(3);

    // Routing
    this.ambient.chain(this.filter, this.reverb, Tone.Destination);
    this.tickSound.toDestination();
    this.finalTicks.toDestination();
    this.celebration.toDestination();
  }

  async loadAll() {
    await Promise.all([
      this.ambient.load('/audio/cosmic-ambient.mp3'),
      this.tickSound.load('/audio/tick.mp3'),
      this.finalTicks.load('/audio/final-tick.mp3'),
      this.celebration.load('/audio/celebration.mp3')
    ]);
  }

  async start() {
    await Tone.start();
    this.ambient.start();
  }

  tick(secondsRemaining) {
    if (secondsRemaining <= 10) {
      // Intense ticks for final 10 seconds
      this.finalTicks.start();
    } else {
      this.tickSound.start();
    }
  }

  setIntensity(value) {
    // 0-1, increases as countdown nears zero
    this.filter.frequency.value = 500 + (value * 3500);
    this.ambient.volume.value = -12 + (value * 6);
  }

  celebrate() {
    this.ambient.stop();
    this.celebration.start();
  }
}
```

### Time-Synced Audio Events

```javascript
function scheduleCountdownAudio(targetDate) {
  const checkInterval = setInterval(() => {
    const now = Date.now();
    const remaining = targetDate - now;
    const seconds = Math.floor(remaining / 1000);

    if (seconds <= 0) {
      clearInterval(checkInterval);
      audio.celebrate();
      return;
    }

    // Tick every second
    audio.tick(seconds);

    // Increase intensity as countdown progresses
    const intensity = Math.max(0, 1 - (seconds / 3600)); // Over 1 hour
    audio.setIntensity(intensity);

  }, 1000);
}
```

## Performance Tips

```javascript
// 1. Preload audio before needed
await player.load(url);

// 2. Reuse players instead of creating new ones
player.stop();
player.start(); // Reuse same player

// 3. Dispose when done
player.dispose();

// 4. Use buffer for frequently played sounds
const buffer = new Tone.Buffer(url);
// Create players from buffer
const player = new Tone.Player(buffer);

// 5. Limit concurrent sounds
const limiter = new Tone.Limiter(-3).toDestination();
players.forEach(p => p.connect(limiter));
```

## Reference

- See `audio-analysis` for FFT and frequency extraction
- See `audio-reactive` for visual-audio binding
- See `audio-router` for audio domain routing
