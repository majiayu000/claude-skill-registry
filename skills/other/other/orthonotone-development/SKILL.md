---
name: Performing Orthonotone Polychoral Instrument
description: Guides agents through launching, playing, sculpting, and capturing performances with the Orthonotone polychoral instrument MVP. Use when generating music, soundscapes, or live demos from this repository.
---

# Performing Orthonotone Polychoral Instrument

## Contents
- [Stage setup](#stage-setup)
- [Performance quickstart](#performance-quickstart)
- [Control surface map](#control-surface-map)
- [Gestural choreography](#gestural-choreography)
- [Scene design and snapshots](#scene-design-and-snapshots)
- [Tempo and groove engine](#tempo-and-groove-engine)
- [Recording and sharing takes](#recording-and-sharing-takes)
- [Troubleshooting cues](#troubleshooting-cues)
- [Reference atlas](#reference-atlas)

## Stage setup
1. **Serve the project** – run any static server from the repo root (`npx http-server .` is sufficient) and open `polychoral-instrument-mvp.html` in a Chromium-based browser for best WebAudio timing.
2. **Prime Playwright harness (optional)** – `npm install` once, then `npm run check` to ensure the QA hooks remain healthy before and after your session.
3. **Warm the audio graph** – click **Enable Audio** in either the toolbar or System section of the Controls panel. Browsers insist on a user gesture before sound.
4. **Set your monitoring level** – adjust **Master Volume** immediately; presets and snapshots respect the level currently set.

## Performance quickstart
- **Canvas focus** – keep the canvas in view (toggle Focus Mode if panels crowd the stage). The hypercube visualization reacts to the same modulation that drives the synth.
- **Baseline scene** – start from **Neutral Lattice** or **Prismatic Bloom** in *Quick Scene* to align with the sound you want. Custom tweaks always begin from the current selection.
- **Check system status** – expand the **Live State Vectors** panel for meters showing axis energy, edge resonance, and face harmonic bloom. Use these readouts to balance the mix while improvising.
- **Keep audio alive** – if silence returns after inactivity, tap **Enable Audio** again; the button mirrors the AudioContext state.

## Control surface map
### State Space
- **Quick Scene selector**: instant morph targets (Neutral, Drift, Bloom, Pulse).
- **Snapshots**: name and store mixes for instant recall mid-set.
- **Dimension / Morph / Grid / Fidelity** sliders: reshape the rendered hyper lattice and corresponding harmonic density.

### Timbre Architecture
- **Line Thickness, Shell Width, Tetra Density**: sculpt the visual-acoustic shell; thicker values emphasize lower resonances.
- **Color Shift & Glitch Intensity**: paint spectral hue and sprinkle jittered overtones.

### Rotation Velocities
- Six sliders (XY…ZW) drive base angular speed in radians/sec. Pair them with gestures for evolving drones versus rhythmic pulses.

### System Suite
- **Master Volume** controls output gain post-fader.
- **Enable Audio** toggles the synth graph.
- **Symmetry Snap** recenters rotation for crystalline chords.
- **Reset State** returns sliders to defaults while leaving audio on.
- **Freeze Rotation** halts motion for sustained pads.
- **MIDI Bridge** connects controllers, enabling external modulation.
- **Tempo Sync** buttons follow external MIDI clock or rephase the internal clock.

## Gestural choreography
- **Pointer drags**: default drags modulate XY/YZ/XZ; hold **Shift** for XW/YW, **Alt** for XZ/ZW, **Ctrl / ⌘** for fine isoclinic blends.
- **Touchscreens**: second finger emulates Shift, third finger unlocks Alt; no hardware keyboard required.
- **Motion input (beta)**: enable via Gesture panel for accelerometer blending; calibrate neutral tilt before performing.
- **Focus Mode & Hide Panels**: reclaim screen real estate mid-performance without losing panel state.

## Scene design and snapshots
1. **Choose or sculpt a starting scene** via Quick Scene.
2. **Dial lattice parameters** (Dimension/Morph/Grid/Fidelity) to set harmonic density.
3. **Shape timbre** with Shell/Line/Tetra and Color/Glitch controls.
4. **Balance rotation speeds** so Status panel meters pulse in complementary patterns (e.g., pair XY with XZ for shimmering fifths).
5. **Store the state**: enter a descriptive name and click **Save Snapshot**; it appears in the snapshot list for one-click recall.
6. **Annotate experiments** – log notable parameter sets in `audio-upgrade-turn2-core-dsp.md` or related plan docs so future performers can reproduce them.

## Tempo and groove engine
- **Clock Division & Rhythm Pattern** choose internal sequencer grids (Quarter, Eighth, Triplet, Sixteenth; Drive Pulse, Syncopated Lift, Euclidean Five, Ambient Bloom, Custom Sculpt).
- **Groove Swing** introduces humanized delay; values above 0.3 create loping polyrhythms.
- **Pattern Sculptor** appears when *Custom Sculpt* is selected—paint per-step intensities, use **Euclidise** for evenly spaced hits, **Humanise** for slight randomness, or **Clear** to reset.
- **MIDI Clock Follow** syncs modulation to external gear; monitor **Tempo Sync** and **Clock Phase** in the Status panel to verify lock.

## Recording and sharing takes
1. **Screen capture** – use system-level screen/audio recorder (e.g., QuickTime, OBS) to capture both visuals and sound; ensure desktop audio is routed from the browser.
2. **Snapshot setlists** – before recording, queue snapshots in performance order for rapid transitions.
3. **Document presets** – after recording, export slider values by copying the QA report (Status → QA Diagnostics → Copy Report) to archive performance settings.
4. **Share context** – attach relevant plan doc links or commit hashes when distributing audio/video so collaborators can align with the build you used.

## Troubleshooting cues
- **No sound after enabling**: confirm Master Volume > 0 and the Status panel shows AudioContext "Running". Reload the page if the context gets stuck in "Suspended".
- **Gestures feel unresponsive**: check if **Freeze Rotation** is active, or if axis sliders are pegged at zero. Recenter with **Reset State**.
- **Panel clutter**: toggle **Hide Panels** then reopen only what you need; Focus Mode hides panels but keeps toggles docked.
- **MIDI not detected**: ensure browser permissions allow MIDI, press **Connect MIDI** again, and verify device appears in the dropdown.

## Reference atlas
- **Instrument surface**: [`polychoral-instrument-mvp.html`](../../polychoral-instrument-mvp.html) – main performance canvas, panels, and synth wiring.
- **Render & audio theory**: [`hypercube_core_webgl_system.md`](../../hypercube_core_webgl_system.md), [`audio-synthesis-master-plan.md`](../../audio-synthesis-master-plan.md), [`audio-upgrade-turn2-core-dsp.md`](../../audio-upgrade-turn2-core-dsp.md).
- **Roadmaps**: [`mvp-roadmap.md`](../../mvp-roadmap.md), [`development-expansion-plan.md`](../../development-expansion-plan.md), [`interface-responsiveness-plan.md`](../../interface-responsiveness-plan.md).
- **QA harness**: [`check-instrument.js`](../../check-instrument.js) for Playwright-driven regression playback.
