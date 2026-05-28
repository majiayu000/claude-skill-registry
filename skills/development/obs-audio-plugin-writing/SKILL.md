---
name: obs-audio-plugin-writing
description: Create OBS Studio audio plugins including audio sources, audio filters, and real-time audio processing. Covers obs_source_info for audio, filter_audio callback, audio data structures, settings API, and properties UI. Use when developing audio plugins for OBS.
version: 1.0.0
---

# OBS Audio Plugin Development

## Purpose

Develop OBS Studio audio plugins including audio sources (generators, capture) and audio filters (gain, EQ, compression). Covers real-time audio processing patterns, the filter_audio callback, and audio-specific settings.

## When NOT to Use

- Video plugins → Use **obs-plugin-developing** (future skills)
- Output/encoder plugins → Use **obs-plugin-developing**
- Code review → Use **obs-plugin-reviewing**

## Quick Start: Audio Filter in 5 Steps

### Step 1: Create Plugin Structure

```c
#include <obs-module.h>
#include <media-io/audio-math.h>  /* For db_to_mul, mul_to_db */

OBS_DECLARE_MODULE()
OBS_MODULE_USE_DEFAULT_LOCALE("my-audio-filter", "en-US")

/* Forward declaration */
extern struct obs_source_info my_audio_filter;

bool obs_module_load(void)
{
    obs_register_source(&my_audio_filter);
    return true;
}
```

### Step 2: Define Context Structure

```c
struct filter_data {
    obs_source_t *context;    /* Required: Reference to this filter */
    size_t channels;          /* Number of audio channels */
    float gain;               /* Gain multiplier (linear, not dB) */
};
```

### Step 3: Implement Core Callbacks

```c
static const char *filter_name(void *unused)
{
    UNUSED_PARAMETER(unused);
    return obs_module_text("MyAudioFilter");
}

static void *filter_create(obs_data_t *settings, obs_source_t *filter)
{
    struct filter_data *ctx = bzalloc(sizeof(*ctx));
    ctx->context = filter;
    filter_update(ctx, settings);  /* Apply initial settings */
    return ctx;
}

static void filter_destroy(void *data)
{
    struct filter_data *ctx = data;
    bfree(ctx);  /* CRITICAL: Always free allocated memory */
}

static void filter_update(void *data, obs_data_t *settings)
{
    struct filter_data *ctx = data;
    double db = obs_data_get_double(settings, "gain_db");
    ctx->gain = db_to_mul((float)db);
    ctx->channels = audio_output_get_channels(obs_get_audio());
}
```

### Step 4: Implement filter_audio Callback

```c
static struct obs_audio_data *filter_audio(void *data,
                                           struct obs_audio_data *audio)
{
    struct filter_data *ctx = data;
    float **adata = (float **)audio->data;

    for (size_t c = 0; c < ctx->channels; c++) {
        if (audio->data[c]) {  /* CRITICAL: Check channel exists */
            for (size_t i = 0; i < audio->frames; i++) {
                adata[c][i] *= ctx->gain;
            }
        }
    }
    return audio;
}
```

### Step 5: Define Settings & Properties

```c
static void filter_defaults(obs_data_t *settings)
{
    obs_data_set_default_double(settings, "gain_db", 0.0);
}

static obs_properties_t *filter_properties(void *data)
{
    UNUSED_PARAMETER(data);
    obs_properties_t *props = obs_properties_create();

    obs_property_t *p = obs_properties_add_float_slider(
        props, "gain_db", obs_module_text("Gain"),
        -30.0, 30.0, 0.1);
    obs_property_float_set_suffix(p, " dB");

    return props;
}
```

### Step 6: Register the Filter

```c
struct obs_source_info my_audio_filter = {
    .id = "my_audio_filter",
    .type = OBS_SOURCE_TYPE_FILTER,
    .output_flags = OBS_SOURCE_AUDIO,
    .get_name = filter_name,
    .create = filter_create,
    .destroy = filter_destroy,
    .update = filter_update,
    .filter_audio = filter_audio,
    .get_defaults = filter_defaults,
    .get_properties = filter_properties,
};
```

## Audio Source Development

Audio sources generate or capture audio and push it to OBS.

### Audio Source Structure

```c
struct source_data {
    obs_source_t *source;
    pthread_t thread;
    os_event_t *event;
    bool active;
    uint64_t timestamp;
};
```

### Audio Source Registration

```c
struct obs_source_info my_audio_source = {
    .id = "my_audio_source",
    .type = OBS_SOURCE_TYPE_INPUT,
    .output_flags = OBS_SOURCE_AUDIO,
    .get_name = source_name,
    .create = source_create,
    .destroy = source_destroy,
    /* Audio sources typically don't need filter_audio */
    /* Instead, they push audio via obs_source_output_audio() */
};
```

### Pushing Audio Data

```c
static void push_audio(struct source_data *ctx, uint8_t *buffer, size_t frames)
{
    struct obs_source_audio audio = {
        .data[0] = buffer,
        .frames = frames,
        .speakers = SPEAKERS_MONO,        /* Or SPEAKERS_STEREO, etc. */
        .samples_per_sec = 48000,
        .timestamp = ctx->timestamp,
        .format = AUDIO_FORMAT_FLOAT_PLANAR,
    };

    obs_source_output_audio(ctx->source, &audio);
    ctx->timestamp += (uint64_t)frames * 1000000000ULL / 48000;
}
```

## Audio Data Structures

### obs_audio_data (Filter Input)

```c
struct obs_audio_data {
    uint8_t *data[MAX_AV_PLANES];  /* Audio channel data */
    uint32_t frames;               /* Number of audio frames */
    uint64_t timestamp;            /* Timestamp in nanoseconds */
};
```

### obs_source_audio (Source Output)

```c
struct obs_source_audio {
    const uint8_t *data[MAX_AV_PLANES];
    uint32_t frames;
    enum speaker_layout speakers;
    enum audio_format format;
    uint32_t samples_per_sec;
    uint64_t timestamp;
};
```

### Speaker Layouts

| Constant           | Channels | Description                  |
| ------------------ | -------- | ---------------------------- |
| `SPEAKERS_MONO`    | 1        | Single channel               |
| `SPEAKERS_STEREO`  | 2        | Left, Right                  |
| `SPEAKERS_2POINT1` | 3        | L, R, LFE                    |
| `SPEAKERS_4POINT0` | 4        | L, R, C, S                   |
| `SPEAKERS_4POINT1` | 5        | L, R, C, LFE, S              |
| `SPEAKERS_5POINT1` | 6        | L, R, C, LFE, SL, SR         |
| `SPEAKERS_7POINT1` | 8        | L, R, C, LFE, SL, SR, BL, BR |

### Audio Formats

| Constant                    | Type    | Description              |
| --------------------------- | ------- | ------------------------ |
| `AUDIO_FORMAT_U8BIT`        | uint8_t | Unsigned 8-bit           |
| `AUDIO_FORMAT_16BIT`        | int16_t | Signed 16-bit            |
| `AUDIO_FORMAT_32BIT`        | int32_t | Signed 32-bit            |
| `AUDIO_FORMAT_FLOAT`        | float   | 32-bit float interleaved |
| `AUDIO_FORMAT_FLOAT_PLANAR` | float   | 32-bit float planar      |

## Audio Math Functions

Include `<media-io/audio-math.h>` for these utilities:

```c
/* Convert decibels to linear multiplier */
float db_to_mul(float db);
/* Example: db_to_mul(-6.0) ≈ 0.5 (half volume) */

/* Convert linear multiplier to decibels */
float mul_to_db(float mul);
/* Example: mul_to_db(0.5) ≈ -6.0 dB */
```

## Audio Properties UI

### Gain Slider (dB)

```c
obs_property_t *p = obs_properties_add_float_slider(
    props, "gain_db", "Gain", -30.0, 30.0, 0.1);
obs_property_float_set_suffix(p, " dB");
```

### Channel Selector

```c
obs_property_t *ch = obs_properties_add_list(
    props, "channel", "Channel",
    OBS_COMBO_TYPE_LIST, OBS_COMBO_FORMAT_INT);
obs_property_list_add_int(ch, "All", -1);
obs_property_list_add_int(ch, "Left", 0);
obs_property_list_add_int(ch, "Right", 1);
```

### Frequency Selector

```c
obs_property_t *freq = obs_properties_add_int_slider(
    props, "frequency", "Frequency (Hz)", 20, 20000, 1);
obs_property_int_set_suffix(freq, " Hz");
```

## FORBIDDEN Patterns

### Critical Violations

| Pattern                                 | Problem               | Solution                 |
| --------------------------------------- | --------------------- | ------------------------ |
| Missing `OBS_DECLARE_MODULE()`          | Plugin won't load     | Add macro at file start  |
| `return false` from `obs_module_load()` | Plugin fails silently | Return `true` on success |
| Missing `bfree()` in destroy            | Memory leak           | Always free context      |
| Global state                            | Thread safety issues  | Use context struct       |
| Blocking in `filter_audio`              | Audio glitches        | Never block/wait         |
| Ignoring NULL channels                  | Crash                 | Check `audio->data[c]`   |
| Ignoring `audio->frames`                | Buffer overflow       | Always use frame count   |
| Malloc in `filter_audio`                | Performance issues    | Pre-allocate buffers     |

### Anti-Pattern Examples

```c
/* BAD: Global state */
static float g_gain = 1.0;  /* WRONG - not thread safe */

/* GOOD: Context structure */
struct filter_data {
    float gain;  /* Per-instance state */
};

/* BAD: Ignoring NULL channels */
for (size_t c = 0; c < channels; c++) {
    adata[c][i] *= gain;  /* CRASH if channel doesn't exist */
}

/* GOOD: Check channel exists */
for (size_t c = 0; c < channels; c++) {
    if (audio->data[c]) {  /* Check first */
        adata[c][i] *= gain;
    }
}

/* BAD: Blocking in audio callback */
static struct obs_audio_data *filter_audio(void *data, struct obs_audio_data *audio)
{
    pthread_mutex_lock(&mutex);  /* WRONG - can cause glitches */
    /* ... */
}

/* GOOD: Use atomic operations or lock-free structures */
```

## Common Pitfalls

| Problem            | Cause                           | Solution                          |
| ------------------ | ------------------------------- | --------------------------------- |
| No audio output    | Wrong `output_flags`            | Use `OBS_SOURCE_AUDIO`            |
| Filter not applied | Missing `filter_audio` callback | Implement callback                |
| Crackles/pops      | Blocking in audio thread        | Never block                       |
| Volume too loud    | Using dB directly               | Convert with `db_to_mul()`        |
| Mono only          | Hardcoded channel count         | Use `audio_output_get_channels()` |
| Settings not saved | Missing `get_defaults`          | Implement defaults callback       |

## Thread Safety

The `filter_audio` callback runs on the audio thread, separate from the main thread.

**Rules:**

1. Never block (no mutexes, no I/O, no allocations)
2. Use atomic operations for shared state
3. Pre-allocate all buffers in `create` callback
4. Configuration changes happen in `update` (main thread)

```c
/* Safe pattern: atomic gain update */
#include <stdatomic.h>

struct filter_data {
    atomic_int gain_int;  /* Store gain * 1000 as int */
};

static void filter_update(void *data, obs_data_t *settings)
{
    struct filter_data *ctx = data;
    double db = obs_data_get_double(settings, "gain_db");
    int gain_scaled = (int)(db_to_mul((float)db) * 1000);
    atomic_store(&ctx->gain_int, gain_scaled);
}

static struct obs_audio_data *filter_audio(void *data, struct obs_audio_data *audio)
{
    struct filter_data *ctx = data;
    float gain = atomic_load(&ctx->gain_int) / 1000.0f;
    /* ... process audio ... */
}
```

## External Documentation

### Context7 (Real-time docs)

```
mcp__context7__get-library-docs
context7CompatibleLibraryID: "/obsproject/obs-studio"
topic: "audio filter plugin filter_audio"
```

### Official References

- **Source Reference**: https://docs.obsproject.com/reference-sources
- **Settings Reference**: https://docs.obsproject.com/reference-settings
- **Properties Reference**: https://docs.obsproject.com/reference-properties
- **Gain Filter Example**: https://github.com/obsproject/obs-studio/blob/master/plugins/obs-filters/gain-filter.c

## Related Files

- **REFERENCE.md** - Complete API documentation
- **TEMPLATES.md** - Ready-to-use code templates

## Related Skills

- **obs-plugin-developing** - Plugin types overview, build system
- **obs-plugin-reviewing** - Code review checklist
