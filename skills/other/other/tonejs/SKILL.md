---
name: tonejs
description: Web Audio framework for creating interactive music in browsers. Use when building audio applications, synthesizers, musical instruments, effects processors, audio visualizations, DAWs, step sequencers, or any browser-based sound generation. Handles synthesis, scheduling, sample playback, effects, and audio routing.
license: MIT
metadata:
    author: Yotam Mann
    version: "15.4.0"
    repository: https://github.com/Tonejs/Tone.js
---

# Tone.js Skill

Build interactive music applications in the browser using the Web Audio API through Tone.js's high-level abstractions.

## When to Use This Skill

Use Tone.js when:

- Creating synthesizers, samplers, or musical instruments
- Building step sequencers, drum machines, or DAWs
- Adding sound effects or music to games
- Implementing audio visualizations synchronized to sound
- Processing audio in real-time with effects
- Scheduling musical events with precise timing
- Working with musical concepts (notes, tempo, measures)

## Core Concepts

### 1. Context and Initialization

The AudioContext must be started from a user interaction (browser requirement):

```javascript
import * as Tone from "tone";

// ALWAYS call Tone.start() from user interaction
document.querySelector("button").addEventListener("click", async () => {
	await Tone.start();
	console.log("Audio context ready");
	// Now safe to play audio
});
```

### 2. Audio Graph and Routing

All audio nodes connect in a graph leading to `Tone.Destination` (the speakers):

```javascript
// Basic connection
const synth = new Tone.Synth().toDestination();

// Chain through effects
const synth = new Tone.Synth();
const filter = new Tone.Filter(400, "lowpass");
const delay = new Tone.FeedbackDelay(0.125, 0.5);
synth.chain(filter, delay, Tone.Destination);

// Parallel routing (split signal)
const reverb = new Tone.Reverb().toDestination();
const delay = new Tone.Delay(0.2).toDestination();
synth.connect(reverb);
synth.connect(delay);
```

### 3. Time and Scheduling

Tone.js abstracts time in musical notation:

- `"4n"` = quarter note
- `"8n"` = eighth note
- `"2m"` = two measures
- `"8t"` = eighth note triplet
- Numbers = seconds

**CRITICAL**: Always use the `time` parameter passed to callbacks:

```javascript
// CORRECT - sample-accurate timing
const loop = new Tone.Loop((time) => {
	synth.triggerAttackRelease("C4", "8n", time);
}, "4n");

// WRONG - JavaScript timing is imprecise
const loop = new Tone.Loop(() => {
	synth.triggerAttackRelease("C4", "8n"); // Will drift
}, "4n");
```

### 4. Transport System

The global timekeeper for synchronized events:

```javascript
// Schedule events on the Transport
const loop = new Tone.Loop((time) => {
	synth.triggerAttackRelease("C4", "8n", time);
}, "4n").start(0);

// Control the Transport
Tone.Transport.start();
Tone.Transport.stop();
Tone.Transport.pause();
Tone.Transport.bpm.value = 120; // Set tempo
```

## Step-by-Step Instructions

### Task 1: Create a Basic Synthesizer

1. Import Tone.js
2. Create a synth and connect to output
3. Wait for user interaction to start audio
4. Play notes using `triggerAttackRelease`

```javascript
import * as Tone from "tone";

const synth = new Tone.Synth().toDestination();

button.addEventListener("click", async () => {
	await Tone.start();
	// Play C4 for an eighth note
	synth.triggerAttackRelease("C4", "8n");
});
```

### Task 2: Create a Polyphonic Instrument

1. Use `PolySynth` to wrap a monophonic synth
2. Pass multiple notes to play chords
3. Release specific notes when needed

```javascript
const polySynth = new Tone.PolySynth(Tone.Synth).toDestination();

// Play a chord
polySynth.triggerAttack(["C4", "E4", "G4"]);

// Release specific notes
polySynth.triggerRelease(["E4"], "+1");
```

### Task 3: Load and Play Audio Files

1. Create a `Player` or `Sampler`
2. Wait for `Tone.loaded()` promise
3. Start playback

```javascript
const player = new Tone.Player("https://example.com/audio.mp3").toDestination();

await Tone.loaded();
player.start();

// For multi-sample instruments
const sampler = new Tone.Sampler({
	urls: {
		C4: "C4.mp3",
		"D#4": "Ds4.mp3",
		"F#4": "Fs4.mp3",
	},
	baseUrl: "https://example.com/samples/",
}).toDestination();

await Tone.loaded();
sampler.triggerAttackRelease(["C4", "E4"], 1);
```

### Task 4: Create a Looping Pattern

1. Use `Tone.Loop` or `Tone.Sequence` for patterns
2. Pass the time parameter to instrument triggers
3. Start the loop and the Transport

```javascript
const synth = new Tone.Synth().toDestination();

const loop = new Tone.Loop((time) => {
	synth.triggerAttackRelease("C4", "8n", time);
}, "4n").start(0);

await Tone.start();
Tone.Transport.start();
```

### Task 5: Add Effects Processing

1. Create effect instances
2. Connect in desired order (serial or parallel)
3. Adjust wet/dry mix if needed

```javascript
const synth = new Tone.Synth();
const distortion = new Tone.Distortion(0.4);
const reverb = new Tone.Reverb({
	decay: 2.5,
	wet: 0.5, // 50% effect, 50% dry
});

synth.chain(distortion, reverb, Tone.Destination);
```

### Task 6: Automate Parameters

1. Access parameter via property (e.g., `frequency`, `volume`)
2. Use methods like `rampTo`, `linearRampTo`, `exponentialRampTo`
3. Schedule changes with time parameter

```javascript
const osc = new Tone.Oscillator(440, "sine").toDestination();

osc.start();

// Ramp frequency to 880 Hz over 2 seconds
osc.frequency.rampTo(880, 2);

// Set value at specific time
osc.frequency.setValueAtTime(440, "+4");

// Exponential ramp (better for frequency)
osc.frequency.exponentialRampTo(220, 1, "+4");
```

### Task 7: Synchronize Visuals with Audio

1. Use `Tone.Draw.schedule()` for visual updates
2. Schedule in the same callback as audio events
3. Visual updates happen just before audio plays

```javascript
const loop = new Tone.Loop((time) => {
	synth.triggerAttackRelease("C4", "8n", time);

	// Schedule visual update
	Tone.Draw.schedule(() => {
		element.classList.add("active");
	}, time);
}, "4n");
```

## Common Patterns

### Pattern: Step Sequencer

```javascript
const synth = new Tone.Synth().toDestination();
const notes = ["C4", "D4", "E4", "G4"];

const seq = new Tone.Sequence(
	(time, note) => {
		synth.triggerAttackRelease(note, "8n", time);
	},
	notes,
	"8n"
).start(0);

Tone.Transport.start();
```

### Pattern: Probabilistic Playback

```javascript
const loop = new Tone.Loop((time) => {
	if (Math.random() > 0.5) {
		synth.triggerAttackRelease("C4", "8n", time);
	}
}, "8n");
```

### Pattern: Dynamic Effect Parameters

```javascript
const filter = new Tone.Filter(1000, "lowpass").toDestination();
const lfo = new Tone.LFO(4, 200, 2000); // 4Hz, 200-2000Hz range

lfo.connect(filter.frequency);
lfo.start();
```

## Sound Design Principles

### Core Insights

**Auditory processing is 10x faster than visual** (~25ms vs ~250ms). Sound provides immediate feedback that makes interactions feel responsive. A button that clicks *feels* faster than one that doesn't, even with identical visual feedback.

**Sound communicates emotion instantly.** A single tone conveys success, error, or tension better than visual choreography. When audio and visuals tell the same story together, the experience is stronger than either alone.

**Less is more.** Most interactions should be silent. Reserve sound for moments that matter: confirmations for major actions, errors that can't be overlooked, state transitions, and notifications. Always pair sound with visuals for accessibility - sound enhances, never replaces. Study games for reference - they've perfected informative, emotional, non-intrusive audio feedback.

### Design Philosophy

Good sound design transforms user experience across all platforms - web apps, mobile apps, desktop applications, and games. These principles apply universally whether creating notification sounds, UI feedback, or musical interactions.

Sound uses a universal language understood by everyone. When designing audio:

**Ask foundational questions:**
- What is the essence of what this app/feature is about?
- What emotion do you want to evoke?
- How does it match the app's visual aesthetics?
- How would users understand this interaction without looking at the screen?

**Consider context:**
- Where will users hear this? (Pocket, desk, busy street, quiet room)
- What will they be doing? (Working, commuting, gaming)
- How often will they hear it? (Once per day vs hundreds of times)

### Notification Sound Design

Effective notification sounds have these characteristics:

**1. Distinguishable**
- Create a unique sonic signature that identifies the app
- Use characteristic timbres or melodic patterns
- Layer simple elements to build recognition
- Don't mimic system defaults or other common sounds

**2. Conveys meaning**
- The sound should connect to the message (not literal, but suggestive)
- Liquid qualities for water/weather, metallic for alerts, warm tones for success
- Use timbre and envelope to suggest the content
- Abstract representation, not sound effects

**3. Friendly and appropriate**
- Match urgency to message importance
- Gentle sounds: Soft attacks (50ms+), smooth timbres (sine, triangle)
- Urgent sounds: Fast attacks (<5ms), brighter timbres (square, FM synthesis)
- Volume and brightness indicate priority

**4. Simple and clean**
- Avoid complex layering or dense harmonic content
- One or two-note patterns work better than melodies
- Pleasant timbres remain tolerable when heard repeatedly
- Clarity over cleverness

**5. Unobtrusive and repeatable**
- Duration: 0.3-0.8 seconds maximum for notifications
- Use softer timbres (sine, triangle) for frequent sounds
- Avoid harsh, complex, or extremely bright timbres
- Should remain pleasant when heard 50+ times per day

**6. Cuts through noise, not abrasive**
- Mid-range frequencies (300-3000Hz) are most effective
- Avoid extreme highs (>8kHz) and lows (<80Hz)
- Design for noisy environments without being harsh
- Triangle and sine waves are gentler than square waves

### UI Sound Design

For buttons, interactions, and transitions:

**1. Use sparingly**
- Add sound only to significant state changes or confirmations
- Silence is often the best choice
- Don't sonify every hover, mouseover, or minor interaction
- Reserve audio feedback for meaningful moments

**2. Volume relative to purpose**
- UI sounds: Much quieter than notifications (-20 to -30dB)
- Users have device in hand, subtlety works
- Notifications: Louder to cut through ambient noise (-10 to -15dB)

**3. Synchronization matters**
- Audio and visual updates must occur simultaneously (< 10ms tolerance)
- Misalignment feels laggy and unprofessional
- Use precise scheduling, not approximate timing

**4. Match interaction character**
- Quick taps: Short duration (<50ms), higher frequencies
- Heavy presses: Longer duration (100-200ms), lower frequencies
- Drag operations: Continuous feedback or silence
- Successful actions: Rising pitch or bright timbre
- Failed actions: Falling pitch or dull timbre

**5. Convey depth and movement**
- Forward movement: Rising pitch over time
- Backward movement: Falling pitch over time
- Opening: Expanding envelope (fade in)
- Closing: Contracting envelope (fade out)
- Envelope shape suggests physical metaphor

### Creative Process

**1. Start with a sound palette**
- Explore different synthesis types (sine, triangle, square, FM, AM, noise)
- Record or synthesize sounds related to the concept
- Physical objects, everyday sounds, and traditional instruments all work
- Build a library of 5-10 candidate sounds

**2. Match sound to purpose**
- Each UI element gets ONE sound that fits its specific purpose
- Button click: Quick and responsive (high pitch, fast decay)
- Toggle switch: Two distinct sounds for on/off states
- Notification: Longer and more distinctive
- No need to provide multiple options - choose the best fit

**3. Use any sound source**
- Traditional instruments: Kalimba, bells, piano, marimba
- Physical materials: Metal, glass, wood, plastic
- Synthesized: Pure tones, FM synthesis, filtered noise
- Unconventional: Toasters, doors, mechanical sounds
- The source matters less than the final character

**4. Layer for richness**
- Combine 2-3 simple elements rather than one complex sound
- Base tone + harmonic layer + texture
- Each layer serves a purpose (body, brightness, character)
- Keep total duration brief even with layers

### Technical Considerations

**1. Clean audio**
- Fade in/out to prevent clicks (10-50ms)
- Remove DC offset
- Normalize levels consistently
- Avoid truncation or abrupt endings

**2. Frequency filtering**
- High-pass filter at 80Hz (removes sub-bass)
- Small speakers can't reproduce low frequencies
- Low-pass filter at 8kHz if needed (removes harsh highs)
- Focus energy in 300-3000Hz for maximum effectiveness

**3. Cross-platform design**
- Design for the worst speaker system (phone, laptop)
- Headphones reveal more detail, but optimize for speakers
- Avoid sub-bass (<80Hz) entirely
- Mid-range frequencies work everywhere

**4. Duration guidelines**
- Notifications: 0.3-0.8 seconds
- Button clicks: 0.05-0.1 seconds
- Toggles: 0.05-0.15 seconds
- Transitions: 0.1-0.3 seconds
- Keep all UI sounds brief to respect user attention

**5. User control**
- Always provide settings to disable sounds
- Volume control separate from system volume
- Per-sound-type toggles (notifications vs UI feedback)
- Respect system-wide mute switches

**6. Synchronization precision**
- Schedule audio at exact same moment as visuals
- 10-20ms latency is perceptible and feels wrong
- Use precise timing APIs, not setTimeout/setInterval
- Audio-visual sync is critical for perceived responsiveness

### Design Checklist

Implementation considerations when designing sounds:

- **Distinguishable**: Unique waveform/envelope that doesn't mimic system defaults
- **Repeatable**: Simple, pleasant timbres (sine, triangle) rather than complex or harsh
- **Cross-platform**: Frequencies between 300-3000Hz, high-pass filtered at 80Hz
- **Audible but not harsh**: Mid-range frequencies, avoid extreme highs (>8kHz) and lows (<80Hz)
- **Short duration**: 0.3-0.8 seconds for notifications, <0.1 seconds for UI feedback
- **Synchronized**: Audio triggers scheduled at same time as visual updates (< 10ms tolerance)
- **User control**: Settings option to disable sounds and adjust volume
- **Appropriate character**: Envelope matches interaction (quick tap = short decay, heavy press = longer decay)
- **Clean audio**: Fade in/out to prevent clicks, filtered to remove unused frequencies
- **Meaningful**: Timbre/pitch suggests the message (liquid for rain, metallic for alerts, warm for success)

## Important Edge Cases and Gotchas

### 1. Browser Autoplay Policy

**MUST** call `Tone.start()` from user interaction. Without this, no audio will play.

```javascript
// WRONG - will fail silently
Tone.Transport.start();

// CORRECT
button.addEventListener("click", async () => {
	await Tone.start();
	Tone.Transport.start();
});
```

### 2. Memory Management

Always dispose of nodes when done:

```javascript
const synth = new Tone.Synth().toDestination();

// When finished
synth.dispose();

// For arrays of instruments
players.forEach((player) => player.dispose());
```

### 3. Timing Precision

JavaScript callbacks are NOT precise. Always use the time parameter:

```javascript
// WRONG - will drift out of sync
setInterval(() => {
	synth.triggerAttackRelease("C4", "8n");
}, 250);

// CORRECT - sample-accurate
new Tone.Loop((time) => {
	synth.triggerAttackRelease("C4", "8n", time);
}, "4n").start(0);
```

### 4. Loading Samples

Wait for samples to load before playing:

```javascript
const sampler = new Tone.Sampler({
	urls: { C4: "piano.mp3" },
	baseUrl: "/audio/",
}).toDestination();

// WRONG - may not be loaded yet
sampler.triggerAttack("C4");

// CORRECT
await Tone.loaded();
sampler.triggerAttack("C4");
```

### 5. Monophonic vs Polyphonic

Basic synths are monophonic (one note at a time):

```javascript
// Only plays one note
const mono = new Tone.Synth().toDestination();
mono.triggerAttack(["C4", "E4", "G4"]); // Only C4 plays

// Plays all notes
const poly = new Tone.PolySynth(Tone.Synth).toDestination();
poly.triggerAttack(["C4", "E4", "G4"]); // All play
```

### 6. Note Format

Notes can be specified multiple ways:

```javascript
synth.triggerAttackRelease("C4", "8n"); // Pitch-octave notation
synth.triggerAttackRelease(440, "8n"); // Frequency in Hz
synth.triggerAttackRelease("A4", "8n"); // A4 = 440Hz
```

### 7. Transport Time vs Audio Context Time

Two timing systems exist:

```javascript
Tone.now(); // AudioContext time (always running)
Tone.Transport.seconds; // Transport time (starts at 0)

// Schedule on AudioContext
synth.triggerAttackRelease("C4", "8n", Tone.now() + 1);

// Schedule on Transport
Tone.Transport.schedule((time) => {
	synth.triggerAttackRelease("C4", "8n", time);
}, "1m");
```

## Architecture Overview

```
ToneAudioNode (base class)
├── Source (audio generators)
│   ├── Oscillator, Player, Noise
│   └── Instrument
│       ├── Synth, FMSynth, AMSynth
│       ├── Sampler
│       └── PolySynth
├── Effect (audio processors)
│   ├── Filter, Delay, Reverb
│   ├── Distortion, Chorus, Phaser
│   └── PitchShift, FrequencyShifter
├── Component (building blocks)
│   ├── Envelope, Filter, LFO
│   └── Channel, Volume, Panner
└── Signal (parameter automation)
    ├── Signal, Add, Multiply
    └── Scale, WaveShaper
```

## Quick Reference

### Instrument Types

- `Tone.Synth` - Basic single-oscillator synth
- `Tone.FMSynth` - Frequency modulation synthesis
- `Tone.AMSynth` - Amplitude modulation synthesis
- `Tone.MonoSynth` - Monophonic with filter and envelope
- `Tone.DuoSynth` - Two-voice synth
- `Tone.MembraneSynth` - Percussive synth
- `Tone.MetalSynth` - Metallic sounds
- `Tone.NoiseSynth` - Noise-based synthesis
- `Tone.PluckSynth` - Plucked string model
- `Tone.PolySynth` - Polyphonic wrapper
- `Tone.Sampler` - Multi-sample instrument

### Common Effects

- `Tone.Filter` - Lowpass, highpass, bandpass, etc.
- `Tone.Reverb` - Convolution reverb
- `Tone.Delay` / `Tone.FeedbackDelay` - Echo effects
- `Tone.Distortion` - Waveshaping distortion
- `Tone.Chorus` - Chorus effect
- `Tone.Phaser` - Phaser effect
- `Tone.PitchShift` - Real-time pitch shifting
- `Tone.Compressor` - Dynamic range compression
- `Tone.Limiter` - Brick wall limiter

### Time Notation

- `"4n"` - Quarter note
- `"8n"` - Eighth note
- `"16n"` - Sixteenth note
- `"2m"` - Two measures
- `"8t"` - Eighth note triplet
- `"1:0:0"` - Bars:Beats:Sixteenths
- `0.5` - Seconds (number)

## Resources

- [Official API Documentation](https://tonejs.github.io/docs/)
- [Interactive Examples](https://tonejs.github.io/examples/)
- [GitHub Repository](https://github.com/Tonejs/Tone.js)
- [Performance Best Practices](https://github.com/Tonejs/Tone.js/wiki/Performance)
