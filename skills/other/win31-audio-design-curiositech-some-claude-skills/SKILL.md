---
name: win31-audio-design
description: Expert in Windows 3.1 era sound vocabulary for modern web/mobile apps. Creates satisfying retro UI sounds using CC-licensed 8-bit audio, Web Audio API, and haptic coordination. Activate on 'win31 sounds', 'retro audio', '90s sound effects', 'chimes', 'tada', 'ding', 'satisfying UI sounds'. NOT for modern flat UI sounds, voice synthesis, or music composition.
allowed-tools: Read,Write,Edit,Bash(ffmpeg:*,node:*,npm:*),mcp__ElevenLabs__text_to_sound_effects,WebFetch
category: Design & Creative
tags:
  - audio
  - retro
  - windows
  - 90s
  - ui-sounds
pairs-with:
  - skill: windows-3-1-web-designer
    reason: Visual + audio Win31 experience
  - skill: sound-engineer
    reason: Advanced audio processing
  - skill: mobile-ux-optimizer
    reason: Mobile haptic-audio coordination
---

# Win31 Audio Design: Satisfying Retro Sound Vocabulary

Expert in creating authentic Windows 3.1 era sound experiences for modern web and mobile applications. Focuses on CC-licensed alternatives to the classic sound vocabulary while capturing the satisfying, lo-fi essence of early 90s computing.

## When to Use

**Use for:**
- Win31-themed web applications needing audio feedback
- Retro game interfaces with 90s desktop sounds
- Mobile apps wanting satisfying micro-interaction sounds
- Converting modern flat sounds to vintage 8-bit aesthetic
- Creating sound palettes that evoke early Windows nostalgia

**Do NOT use for:**
- Modern flat/material sound design → **sound-engineer**
- Voice synthesis → **voice-audio-engineer**
- Music composition → DAW tools
- Film sound design → Linear audio workflows

## Windows 3.1 Sound Vocabulary

### The Original Sounds (Copyrighted - DO NOT USE)

| File | Character | Duration | Function |
|------|-----------|----------|----------|
| CHIMES.WAV | Ethereal bells | ~1.5s | System notifications |
| CHORD.WAV | Major chord resolve | ~1.2s | Task completion |
| DING.WAV | Single bell strike | ~0.5s | Attention/alert |
| TADA.WAV | Triumphant fanfare | ~2s | Startup/major success |
| RINGIN.WAV | Rising tone | ~0.3s | Modal open |
| RINGOUT.WAV | Falling tone | ~0.2s | Modal close |

**Legal Warning**: These sounds are copyrighted by Microsoft. We create INSPIRED alternatives, never copies.

### Sound Characteristics (What Made Them Satisfying)

| Quality | Win31 Sound Profile |
|---------|---------------------|
| **Sample Rate** | 11kHz-22kHz (lo-fi charm) |
| **Bit Depth** | 8-bit (quantization warmth) |
| **Frequency Range** | 400Hz-4kHz (no sub-bass, gentle highs) |
| **Envelope** | Fast attack, medium decay, no sustain |
| **Reverb** | Dry or short room (no cathedral halls) |
| **Character** | Bright, plasticky, cheerful |

### The Win31 "Ding" Formula

```
┌─────────────────────────────────────────────────────┐
│ Attack: 5-10ms    │ Pure sine starts BRIGHT         │
│ Peak: ~880Hz (A5) │ Classic 8-bit "bleep"           │
│ Decay: 200-400ms  │ Natural damping feel            │
│ Overtones: 2nd+3rd│ Bell-like shimmer               │
│ Processing: 8-bit │ Adds warmth via quantization    │
└─────────────────────────────────────────────────────┘
```

## CC-Licensed Sound Resources

### Recommended Sources

| Source | License | Best For |
|--------|---------|----------|
| [Dominik Braun's 107 Retro Sounds](https://dominik-braun.net/retro-sounds/) | CC BY 4.0 | UI blips, beeps, positive feedback |
| [LittleRobotSoundFactory (Freesound)](https://freesound.org/people/LittleRobotSoundFactory/packs/16681/) | CC0/CC BY | 8-bit game sounds |
| [OpenGameArt 512 SFX](https://opengameart.org/content/512-sound-effects-8-bit-style) | CC0 | Comprehensive retro library |
| [Gritty Retro UI (Exechamp)](https://freesound.org/people/Exechamp/packs/28921/) | CC0 | UI-specific clicks and tones |

### Attribution Template

```
Audio: [Sound Name] by [Creator] from [Source]
Licensed under [CC BY 4.0 / CC0]
https://[source-url]
```

## Sound Palette for Win31 Apps

### Interaction Sounds

| Action | Sound Character | Duration | Frequency |
|--------|-----------------|----------|-----------|
| **Button click** | Soft plastic "tik" | 20-40ms | 800-1200Hz |
| **Button release** | Subtle "tok" | 15-30ms | 600-900Hz |
| **Toggle on** | Rising chirp | 80-120ms | 600→1200Hz |
| **Toggle off** | Falling chirp | 80-120ms | 1200→600Hz |
| **Window open** | Ascending arpeggio | 150-250ms | C4-E4-G4 |
| **Window close** | Descending arpeggio | 100-200ms | G4-E4-C4 |
| **Error** | Low buzz + descending | 300-500ms | 200-400Hz |
| **Success** | Bright ding + shimmer | 200-400ms | 880Hz + harmonics |
| **Notification** | Double chime | 400-600ms | 660Hz, 880Hz |

### System Sounds

| Event | Sound Character | Duration |
|-------|-----------------|----------|
| **Startup** | Triumphant chord resolve | 1.5-2.5s |
| **Shutdown** | Gentle descending phrase | 1-2s |
| **Critical error** | Harsh double-buzz | 400-600ms |
| **Task complete** | Satisfying "da-ding!" | 300-500ms |
| **Navigation** | Soft whoosh + settle | 100-200ms |

## Web Audio Implementation

### Basic Sound Player

```typescript
// Win31-style sound manager for web
class Win31SoundManager {
  private audioContext: AudioContext | null = null;
  private sounds: Map<string, AudioBuffer> = new Map();

  constructor() {
    // Lazy init on first user interaction (browser policy)
  }

  private getContext(): AudioContext {
    if (!this.audioContext) {
      this.audioContext = new AudioContext({ sampleRate: 22050 }); // Lo-fi!
    }
    return this.audioContext;
  }

  async loadSound(name: string, url: string) {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    const audioBuffer = await this.getContext().decodeAudioData(arrayBuffer);
    this.sounds.set(name, audioBuffer);
  }

  play(name: string, volume = 0.5) {
    const buffer = this.sounds.get(name);
    if (!buffer) return;

    const ctx = this.getContext();
    const source = ctx.createBufferSource();
    const gain = ctx.createGain();

    source.buffer = buffer;
    gain.gain.value = volume;

    source.connect(gain);
    gain.connect(ctx.destination);
    source.start(0);
  }

  // Procedural 8-bit "ding"
  playDing(frequency = 880) {
    const ctx = this.getContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'triangle'; // Softer than sine, more 8-bit
    osc.frequency.setValueAtTime(frequency, ctx.currentTime);

    // Fast attack, medium decay
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.4);
  }
}

export const win31Sounds = new Win31SoundManager();
```

### Synthesized Retro Sounds

```typescript
// Generate Win31-style sounds procedurally
function createChime(ctx: AudioContext, baseFreq = 660): AudioBufferSourceNode {
  const duration = 1.5;
  const sampleRate = ctx.sampleRate;
  const buffer = ctx.createBuffer(1, duration * sampleRate, sampleRate);
  const data = buffer.getChannelData(0);

  // Two-tone chime (like CHIMES.WAV character)
  for (let i = 0; i < data.length; i++) {
    const t = i / sampleRate;
    const env = Math.exp(-t * 3); // Decay envelope

    // Two harmonically related tones
    const tone1 = Math.sin(2 * Math.PI * baseFreq * t);
    const tone2 = Math.sin(2 * Math.PI * baseFreq * 1.5 * t) * 0.5;

    data[i] = (tone1 + tone2) * env * 0.3;
  }

  // 8-bit quantization for authentic lo-fi
  for (let i = 0; i < data.length; i++) {
    data[i] = Math.round(data[i] * 127) / 127;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;
  return source;
}
```

## Mobile Haptic Coordination

### iOS Haptic-Sound Pairing

| Sound Event | Haptic Type | Intensity |
|-------------|-------------|-----------|
| Button click | `.light` | 0.5 |
| Toggle switch | `.medium` | 0.6 |
| Error buzz | `.heavy` | 0.9 |
| Success ding | `.selection` | 0.4 |
| Window open | `.soft` | 0.3 |

### React Native Implementation

```typescript
import * as Haptics from 'expo-haptics';

async function playWithHaptic(soundName: string, hapticType: Haptics.ImpactFeedbackStyle) {
  // Fire both simultaneously
  await Promise.all([
    win31Sounds.play(soundName),
    Haptics.impactAsync(hapticType),
  ]);
}

// Usage
await playWithHaptic('click', Haptics.ImpactFeedbackStyle.Light);
await playWithHaptic('error', Haptics.ImpactFeedbackStyle.Heavy);
```

## Anti-Patterns

### Anti-Pattern: High-Fidelity Samples
**What it looks like**: 48kHz, 24-bit crystal-clear audio
**Why wrong**: Sounds too modern, loses retro charm
**Instead**: Downsample to 22kHz, apply 8-bit quantization

### Anti-Pattern: Long Reverb Tails
**What it looks like**: Sounds echoing in a cathedral
**Why wrong**: Win31 sounds were DRY or short room
**Instead**: No reverb or <100ms decay

### Anti-Pattern: Sub-Bass
**What it looks like**: Deep rumbling under 100Hz
**Why wrong**: 90s PC speakers couldn't reproduce sub-bass
**Instead**: Cut everything below 200Hz

### Anti-Pattern: Copying Microsoft Sounds
**What it looks like**: Using actual CHIMES.WAV or TADA.WAV
**Why wrong**: Copyright infringement
**Instead**: Create inspired alternatives with CC-licensed sources

### Anti-Pattern: Too Many Sounds
**What it looks like**: Every micro-interaction makes noise
**Why wrong**: Becomes annoying, fatiguing
**Instead**: Sounds for primary actions only, user toggle for audio

## Sound Level Guidelines

| Category | Level | Notes |
|----------|-------|-------|
| UI feedback | -24 to -18 dB | Subtle, never intrusive |
| Notifications | -18 to -12 dB | Attention-getting but not loud |
| Errors | -15 to -9 dB | Noticeable but not jarring |
| System sounds | -12 to -6 dB | Major events (startup/shutdown) |

**Always provide:**
1. Global sound toggle (on/off)
2. Volume slider (0-100%)
3. Respect system silent mode

## Quick Implementation Checklist

- [ ] Create Win31SoundManager class
- [ ] Load CC-licensed base sounds
- [ ] Add procedural fallbacks (ding, chime)
- [ ] Implement haptic pairing for mobile
- [ ] Add global sound toggle
- [ ] Test with Win31 visual theme
- [ ] Add attribution for CC sounds
- [ ] Verify sample rates (22kHz max)

## Integrates With

- **windows-3-1-web-designer** - Visual + audio Win31 experience
- **sound-engineer** - Advanced spatial audio if needed
- **mobile-ux-optimizer** - Touch + haptic + audio coordination
- **pwa-expert** - Offline sound caching

---

**Core insight**: Win31 sounds were satisfying because they were SIMPLE—short, bright, lo-fi tones that gave immediate feedback without being distracting. The 8-bit quantization and limited frequency response added warmth, not harshness. Capture that spirit with CC-licensed alternatives, never copies.

**Remember**: Always include a sound toggle. Never play sounds without user consent. Pair audio with haptics on mobile for maximum satisfaction.
