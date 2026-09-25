---
name: riso-score
description: Scores a riso film or reworks its score. Designs the cue list from the film's FILM.md events, builds a deterministic renderAudio() from the sound kit in studies/sound.html, iterates with tools/audio.mjs, gates determinism, length, loudness and sync, and records measured results in FILM.md. Use for "score this film", "add sound/music", "the climax is too loud", "fix the handoff at 16 s", "check the mix", sound effects, foley or a soundtrack on a riso film. Not for drawing or motion (riso-film) or changing tools/.
---

# Riso score

Produce the `renderAudio()` half of `films/<name>/index.html`: a deterministic stereo score exactly
the film's duration at 48 kHz, scaled once to −16 LUFS under a −1 dBTP ceiling, with a measured
sheet and a full muxed MP4 reviewed with the picture. Commands run in `tools/`.
[examples.md](examples.md) shows eight finished scores: sampled piano (`films/window-seat`),
recorded strings timed from the picture (`films/roost`), found CC0 instruments (`films/held`),
sampled handpan with edge-timed swells (`films/nonpareil`), a CC0 trio sharing the picture's
clock (`films/eclosion`), procedural (`films/lumen`), procedural from the kit alone with a note
per drawn mark (`films/passenger`) and two switchable candidates (`films/emergence`).

## Before writing a note

1. Read the film's `FILM.md` for sound direction and timed events, and `docs/sound.md` for the
   kit, sync, transitions, mix and how to read the sheet.
2. Spot the film: list every boundary and visible event with its time and decide whether the
   music notices it or rides through. Pick three to five true sync points. Choose tempo, mode and
   one motif from the subject; the project mandates no BPM, key or chord.
3. Find the film's event data (cue arrays, reveal starts, contact times). The score reads those,
   never copied numbers, so retiming the picture retimes the sound.

## Stages

Each stage ends with `audio.mjs` output (seconds to run), not with reasoning about code.

1. **Kit and skeleton.** Copy the `── sound kit ──` block from `studies/sound.html` after the
   film's motion kit; its header lists the names it declares, so rename collisions. Write
   `buildScore()`: `Score({ duration: DUR, key: '<name>' })`, `air` across the film, `return
   s.render()`. Cache the promise so the player and `renderAudio()` share one render;
   `renderAudio()` returns `wavBase64(buffer)`. Publish sync points as `window.__riso.marks`.
   `node audio.mjs ../films/<name>/index.html --twice` must show matching length and two equal
   renders before anything else.
2. **Bed and transitions.** Place sustained layers (`pad`, `organ`, `wind`, `rain`, `air`)
   passage to passage. Bridge each cut on purpose: pre-lap, post-lap, pedal, pivot or texture
   handoff. Run with `--marks` on the boundaries; a 200 ms hole 10 dB under its surroundings at a
   cut is the fade-to-silence failure. Fix it before adding foreground.
3. **Foreground and sync.** Put `hit`s on the true sync points so swells peak on the visible
   arrival; let the rest breathe. `--around <t> --window 1` per point: onset within ~40 ms after
   the mark, never more than 20 ms before. Pick material timbres (`contact`, `paper`, `drop`) from
   what is on screen.
4. **Climax and ending.** Prepare the climax with a riser, a low body and staggered accents, not
   the same voices louder. Decide button, tail or hard out. Check the lift into the climax in the
   short-term curve.
5. **Mix.** Balance voices, pan by screen `x`, keep bass centred; `render` sets the level. If the
   true-peak ceiling pulled the mix under target, fix the peak, not the target. Nothing above
   4 kHz in the band percentages means no air.

## Gates

After every stage, and once more in Firefox before delivery:

```
node audio.mjs ../films/<name>/index.html --twice --marks <sync points>
node audio.mjs ../films/<name>/index.html --engine firefox --ffmpeg
```

`FAIL` breaks the contract: no `renderAudio()`, wrong length, clipped samples, or two renders
differing beyond 16-bit jitter (Chromium jitters a step or two; Firefox is byte-identical).
`WARN` is a judgement to resolve or record: level more than 1 LU off −16 LUFS, true peak above
−1 dBTP, a rate other than 48 kHz, an opening or ending above −40 dBFS in its first or last
10 ms. Discontinuities are bugs at note starts and expected at designed ticks. Then read
`out/<name>/_audio.png`: waveform lanes, log spectrogram, loudness against the target band with
valleys marked, and the per-mark table.

## Delivery

```
node render.mjs ../films/<name>/index.html --fps 30 --size 1080 --engine firefox
```

Only the full export carries the score; `render.mjs` prints the muxed loudness and true peak.
When only the score changed, remux instead of re-rendering every frame: take the Firefox WAV that
`audio.mjs --engine firefox` writes to `out/<name>.wav`, then

```
ffmpeg -i ../out/<name>.mp4 -i ../out/<name>.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart ../out/<name>-rescored.mp4
ffmpeg -i ../out/<name>-rescored.mp4 -af ebur128=peak=true -f null -
```

and read the true peak from the second command, as `render.mjs` would. Listen through quiet
passages, every handoff and the climax with the picture. If you cannot listen, say so, leave
perceptual quality unclaimed and name three to five times for the user to hear: passing meters did
not stop a modal piano sounding like MIDI to a human listener.

Record under `## Score` in `FILM.md`: direction, tempo/grid and mode, each sync event and what
sounds on it, deliberate silences, the measured line (`I −16.0 LUFS, LRA 3.7 LU, TP −2.0 dBTP,
clipped 0, firefox byte-identical`), the marks table, and what was heard or that nothing was.
Recorded samples need a license that permits redistribution, pinned sources and attribution
beside the film (see `films/window-seat/AUDIO-SOURCES.md`, CC BY, and
`films/roost/AUDIO-SOURCES.md`, CC0). Libraries disagree on octave numbering (VSCO 2's cello,
bass, clarinet and horn and VCSL's vibraphone name middle C C3; VSCO 2's violin C4), so check each
root against the recorded partials. A soft low note can lack its fundamental (VSCO horn C1: 0.00
at f, 0.71 at 4f), and a partial scorer then takes the second harmonic: pin such roots from the
harmonic spacing and measure only tuning (`films/eclosion/build-sample-bank.py`).

## Player audio and rework

The export never plays in the page. For the in-page player, wire the cached buffer to a live
`AudioContext` that starts from the scrubbed time, stops on pause and seek, and starts muted;
examples.md names the functions that do this in each film.

When reworking, read `FILM.md` first, edit the authoritative `index.html`, and measure before
changing anything so the revision has a baseline. Fix continuity before adding notes. Local fixes
preserve approved pacing, sync points and dynamics.
