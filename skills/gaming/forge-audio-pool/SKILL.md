---
name: forge-audio-pool
description: Add fire-and-forget audio playback with a source pool and volume fading for click-free start/stop transitions.
trigger: Use when someone needs polyphonic sound effects, fire-and-forget audio, one-shot playback, or fade-in/fade-out on audio sources.
---

# forge-audio-pool

Add fire-and-forget sound effect playback using `ForgeAudioPool` and smooth
volume transitions using the fade envelope on `ForgeAudioSource`. Based on
[Audio Lesson 02](../../../lessons/audio/02-sound-effects/).

## When to use

- Playing the same sound multiple times with overlap (polyphony)
- One-shot sound effects that should auto-clean-up when finished
- Starting or stopping sounds without audible clicks (fade-in / fade-out)
- Ambient loops that toggle smoothly with a volume ramp

## Source pool pattern

```c
#include "audio/forge_audio.h"

/* In app_state */
ForgeAudioPool pool;
ForgeAudioBuffer sfx_buffer;

/* In SDL_AppInit */
forge_audio_pool_init(&pool);
forge_audio_load_wav("assets/audio/impact.wav", &sfx_buffer);

/* Fire-and-forget: each call allocates a new slot (up to 32) */
int slot = forge_audio_pool_play(&pool, &sfx_buffer, 1.0f, false);
if (slot < 0) {
    SDL_Log("Pool full — sound dropped");
}

/* In SDL_AppIterate — mix all active sources, reclaim finished slots */
SDL_memset(scratch, 0, samples * sizeof(float));
forge_audio_pool_mix(&pool, scratch, frames_needed);

/* Stop everything */
forge_audio_pool_stop_all(&pool);
```

The pool scans for the first slot with `playing == false`. Non-looping sources
auto-stop at buffer end; the slot is then reusable by the next `pool_play()`.

## Fade envelope pattern

```c
/* Fade fields on ForgeAudioSource (initialized by forge_audio_source_create):
 *   fade_volume = 1.0  (current multiplier)
 *   fade_target = 1.0  (destination)
 *   fade_rate   = 0.0  (change per second, 0 = no fade) */

/* Start a fade to any target */
forge_audio_source_fade(src, 0.5f, 2.0f);  /* fade to 50% over 2 seconds */

/* Convenience: fade in from silence (sets fade_volume=0, starts playback) */
forge_audio_source_fade_in(src, 0.5f);

/* Convenience: fade out to zero (auto-stops when complete) */
forge_audio_source_fade_out(src, 1.0f);

/* MUST call once per frame to advance the ramp */
forge_audio_source_fade_update(src, dt);
```

The fade multiplier is applied on top of `volume * pan` during
`forge_audio_source_mix()`. Default `fade_volume=1.0` means existing code
from Lesson 01 behaves identically.

## Combining pool + fade

For pool sources that need fade control, get the source pointer after play:

```c
int slot = forge_audio_pool_play(&pool, &buffer, 1.0f, true);
if (slot >= 0) {
    ForgeAudioSource *src = forge_audio_pool_get(&pool, slot);
    forge_audio_source_fade_in(src, 0.3f);
}

/* Update fades on all pool sources each frame */
for (int i = 0; i < FORGE_AUDIO_POOL_MAX_SOURCES; i++) {
    if (pool.sources[i].playing) {
        forge_audio_source_fade_update(&pool.sources[i], dt);
    }
}
```

## Ambient loop with fade toggle

For a single looping source managed outside the pool (direct fade control):

```c
/* In app_state */
ForgeAudioSource ambient;
bool ambient_active;

/* Toggle on key press */
if (ambient_active) {
    forge_audio_source_fade_out(&ambient, fade_duration);
    ambient_active = false;
} else {
    if (!ambient.playing) forge_audio_source_reset(&ambient);
    forge_audio_source_fade_in(&ambient, fade_duration);
    ambient_active = true;
}
```

## Common mistakes

- **Forgetting `fade_update`** — The fade does not advance automatically.
  Call `forge_audio_source_fade_update(src, dt)` once per frame for every
  source that might be fading.
- **Calling fade_update per mix call** — Call it per frame, not per mix
  invocation. The rate is in units per second, scaled by `dt`.
- **Not zeroing the mix buffer** — `forge_audio_pool_mix()` is additive.
  Always `memset(out, 0, ...)` before the first mix call each frame.
- **Ignoring pool_play return value** — Returns -1 when full. Decide whether
  to drop the sound or steal an existing slot.

## API reference

| Function | Purpose |
|---|---|
| `forge_audio_pool_init` | Zero all 32 slots |
| `forge_audio_pool_play` | Play buffer in first idle slot → index or -1 |
| `forge_audio_pool_get` | Get source pointer at index → `ForgeAudioSource*` or NULL |
| `forge_audio_pool_mix` | Mix active sources, reclaim finished |
| `forge_audio_pool_stop_all` | Stop everything |
| `forge_audio_pool_active_count` | Count of playing sources |
| `forge_audio_source_fade` | Start fade toward target over duration |
| `forge_audio_source_fade_in` | 0→1 fade, starts playback |
| `forge_audio_source_fade_out` | Current→0 fade, auto-stops |
| `forge_audio_source_fade_update` | Advance fade by dt seconds |
