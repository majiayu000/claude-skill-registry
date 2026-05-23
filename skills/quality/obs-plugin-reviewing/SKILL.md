---
name: obs-plugin-reviewing
description: Review OBS Studio plugins for correctness, memory safety, thread safety, and best practices. Audits module registration, callback implementations, resource cleanup, and common anti-patterns. Use when reviewing OBS plugin code or preparing for release.
version: 1.0.0
---

# OBS Plugin Code Review

## Purpose

Audit OBS Studio plugins for correctness, performance, memory safety, and thread safety. Covers module registration, callback implementations, resource management, and audio-specific patterns.

## When NOT to Use

- Writing new plugins → Use **obs-audio-plugin-writing**
- Getting started → Use **obs-plugin-developing**
- Need guidance on which skill → Use **obs-plugin-expert** agent

## Quick Review Checklist

Run these checks in order. Stop at first P0 issue.

### P0 - CRITICAL (Must Fix)

| Check                      | Pattern                     | Command                              |
| -------------------------- | --------------------------- | ------------------------------------ |
| Missing module macro       | No `OBS_DECLARE_MODULE()`   | `grep -r "OBS_DECLARE_MODULE" src/`  |
| Module load returns false  | `return false` in load      | `grep -A5 "obs_module_load" src/`    |
| Memory leak in destroy     | Missing `bfree()`           | Manual review of destroy callbacks   |
| Blocking in audio callback | Mutex/sleep in filter_audio | `grep -A20 "filter_audio" src/`      |
| NULL dereference           | No channel null check       | `grep -B5 -A10 "audio->data\[" src/` |

### P1 - HIGH (Should Fix)

| Check                  | Pattern                      | Command                         |
| ---------------------- | ---------------------------- | ------------------------------- | ------------- |
| Buffer overflow risk   | Ignoring audio->frames       | `grep -A15 "filter_audio" src/` |
| Global state           | Static variables             | `grep "^static.*=" src/*.c`     |
| Missing error handling | No NULL checks               | Manual review                   |
| Thread safety issues   | Shared state without atomics | `grep -E "(pthread              | mutex)" src/` |

### P2 - MEDIUM (Consider Fixing)

| Check              | Pattern                  | Command                          |
| ------------------ | ------------------------ | -------------------------------- |
| Missing defaults   | No get_defaults callback | `grep "get_defaults" src/`       |
| Hard-coded strings | No obs_module_text()     | `grep -E "\"[A-Z][a-z]" src/*.c` |
| Missing locale     | No en-US.ini             | `ls data/locale/`                |

### P3 - LOW (Nice to Have)

| Check           | Pattern                 | Command         |
| --------------- | ----------------------- | --------------- | --------------- |
| Missing logging | No blog/obs_log calls   | `grep -E "(blog | obs_log)" src/` |
| Code style      | Inconsistent formatting | Manual review   |
| Documentation   | Missing comments        | Manual review   |

---

## Module Registration Review

### Required Elements

Every OBS plugin MUST have:

```c
/* 1. Module declaration macro - REQUIRED */
OBS_DECLARE_MODULE()

/* 2. Optional but recommended: locale support */
OBS_MODULE_USE_DEFAULT_LOCALE("plugin-name", "en-US")

/* 3. Module load function - REQUIRED, must return true */
bool obs_module_load(void)
{
    /* Register all sources/outputs/encoders/services */
    obs_register_source(&my_source);
    return true;  /* MUST return true on success */
}

/* 4. Module unload - optional but recommended */
void obs_module_unload(void)
{
    /* Cleanup global resources */
}
```

### Common Module Errors

| Error                           | Impact                 | Solution                      |
| ------------------------------- | ---------------------- | ----------------------------- |
| Missing `OBS_DECLARE_MODULE()`  | Plugin won't load      | Add macro at file start       |
| `obs_module_load` returns false | Plugin fails silently  | Return true on success        |
| No unload cleanup               | Resource leak          | Implement `obs_module_unload` |
| Wrong locale path               | Strings not translated | Use `data/locale/en-US.ini`   |

### Grep Commands for Module Review

```bash
# Check for module macro
grep -l "OBS_DECLARE_MODULE" src/*.c

# Check module_load return value
grep -A10 "obs_module_load" src/*.c | grep -E "(return|false|true)"

# Check for source registration
grep "obs_register_source" src/*.c

# Check for locale setup
grep "OBS_MODULE_USE_DEFAULT_LOCALE" src/*.c
```

---

## Memory Safety Review

### Allocation/Deallocation Pattern

OBS uses custom memory functions:

| OBS Function          | Standard Equivalent  | Purpose                     |
| --------------------- | -------------------- | --------------------------- |
| `bzalloc(size)`       | `calloc(1, size)`    | Zero-initialized allocation |
| `bfree(ptr)`          | `free(ptr)`          | Free memory                 |
| `bmalloc(size)`       | `malloc(size)`       | Raw allocation              |
| `brealloc(ptr, size)` | `realloc(ptr, size)` | Resize allocation           |

### Memory Safety Checklist

```
□ Every bzalloc/bmalloc has matching bfree in destroy callback
□ Context struct freed in destroy callback
□ No memory allocation in audio/video callbacks
□ Pre-allocated buffers for real-time processing
□ Reference counting handled correctly (obs_source_addref/release)
```

### Common Memory Errors

```c
/* BAD: Memory leak - no bfree in destroy */
static void *my_create(obs_data_t *settings, obs_source_t *source)
{
    struct my_data *ctx = bzalloc(sizeof(*ctx));
    ctx->buffer = bmalloc(4096);  /* Also needs freeing! */
    return ctx;
}

static void my_destroy(void *data)
{
    /* WRONG: Missing bfree calls! */
}

/* GOOD: Proper cleanup */
static void my_destroy(void *data)
{
    struct my_data *ctx = data;
    if (ctx) {
        bfree(ctx->buffer);  /* Free nested allocations first */
        bfree(ctx);          /* Free context last */
    }
}
```

### Grep Commands for Memory Review

```bash
# Find all allocations
grep -n "bzalloc\|bmalloc\|brealloc" src/*.c

# Find all deallocations
grep -n "bfree" src/*.c

# Check destroy callbacks
grep -A20 "_destroy\|\.destroy" src/*.c

# Find potential leaks (alloc without corresponding free)
# Manual comparison of above results
```

---

## Thread Safety Review

### OBS Threading Model

| Thread           | Callbacks                                             | Rules                          |
| ---------------- | ----------------------------------------------------- | ------------------------------ |
| **Main Thread**  | create, destroy, update, get_properties, get_defaults | Safe to block, allocate memory |
| **Audio Thread** | filter_audio                                          | NEVER block, no allocations    |
| **Video Thread** | video_render, video_tick                              | Minimize blocking              |

### Audio Thread Rules (CRITICAL)

The `filter_audio` callback runs on the audio thread:

```c
/* FORBIDDEN in filter_audio: */
pthread_mutex_lock(&mutex);  /* NEVER: Can cause audio glitches */
sleep(1);                    /* NEVER: Blocks audio processing */
bmalloc(size);              /* NEVER: Allocation can block */
obs_data_get_*();           /* NEVER: Settings access can lock */
fopen();                    /* NEVER: I/O blocks */

/* ALLOWED in filter_audio: */
atomic_load(&value);         /* OK: Lock-free */
ctx->cached_value;           /* OK: Pre-computed in update() */
math operations;             /* OK: CPU-bound is fine */
```

### Safe Configuration Updates

```c
/* Pattern: Update on main thread, read atomically on audio thread */
#include <stdatomic.h>

struct filter_data {
    atomic_int gain_scaled;  /* Atomic for thread-safe reads */
};

/* Main thread: update callback */
static void filter_update(void *data, obs_data_t *settings)
{
    struct filter_data *ctx = data;
    double db = obs_data_get_double(settings, "gain_db");
    int scaled = (int)(db_to_mul((float)db) * 1000);
    atomic_store(&ctx->gain_scaled, scaled);
}

/* Audio thread: filter_audio callback */
static struct obs_audio_data *filter_audio(void *data,
                                           struct obs_audio_data *audio)
{
    struct filter_data *ctx = data;
    float gain = atomic_load(&ctx->gain_scaled) / 1000.0f;
    /* ... process with gain ... */
    return audio;
}
```

### Grep Commands for Thread Safety

```bash
# Find mutex usage in audio callbacks
grep -B5 -A20 "filter_audio" src/*.c | grep -E "(mutex|lock|pthread)"

# Find memory allocation in audio callbacks
grep -B5 -A20 "filter_audio" src/*.c | grep -E "(malloc|alloc|bfree)"

# Find I/O in audio callbacks
grep -B5 -A20 "filter_audio" src/*.c | grep -E "(fopen|fread|fwrite)"

# Check for atomic usage
grep -n "atomic\|_Atomic" src/*.c
```

---

## Callback Correctness Review

### Required Callbacks

| Callback          | Required?         | Purpose                  |
| ----------------- | ----------------- | ------------------------ |
| `.id`             | YES               | Unique identifier string |
| `.type`           | YES               | Source type enum         |
| `.output_flags`   | YES               | Capability flags         |
| `.get_name`       | YES               | Display name function    |
| `.create`         | YES               | Instance creation        |
| `.destroy`        | YES               | Instance cleanup         |
| `.update`         | Recommended       | Settings application     |
| `.get_defaults`   | Recommended       | Default values           |
| `.get_properties` | Recommended       | UI generation            |
| `.filter_audio`   | For audio filters | Audio processing         |

### Audio Filter Callback Review

```c
/* Review this pattern in filter_audio: */
static struct obs_audio_data *filter_audio(void *data,
                                           struct obs_audio_data *audio)
{
    struct filter_data *ctx = data;
    float **adata = (float **)audio->data;

    /* CHECK 1: Are all channels processed? */
    for (size_t c = 0; c < ctx->channels; c++) {
        /* CHECK 2: Is NULL channel check present? */
        if (!audio->data[c])  /* REQUIRED: Some channels may be NULL */
            continue;

        /* CHECK 3: Is frames count used correctly? */
        for (size_t i = 0; i < audio->frames; i++) {
            adata[c][i] *= ctx->gain;
        }
    }

    /* CHECK 4: Is audio returned (not NULL)? */
    return audio;
}
```

### Callback Review Checklist

```
□ filter_audio checks audio->data[c] for NULL before access
□ filter_audio uses audio->frames for loop bounds (not hardcoded)
□ filter_audio returns the audio pointer
□ update callback converts dB to linear (if applicable)
□ destroy callback frees all allocated memory
□ create callback initializes all context fields
□ get_properties creates all needed UI elements
□ get_defaults sets sensible default values
```

---

## Settings Validation Review

### Settings API Patterns

```c
/* GOOD: Proper settings handling */
static void filter_update(void *data, obs_data_t *settings)
{
    struct filter_data *ctx = data;

    /* Get values with type checking */
    double gain_db = obs_data_get_double(settings, "gain_db");
    bool enabled = obs_data_get_bool(settings, "enabled");

    /* Validate ranges */
    if (gain_db < -60.0) gain_db = -60.0;
    if (gain_db > 30.0) gain_db = 30.0;

    /* Convert and store */
    ctx->gain = db_to_mul((float)gain_db);
    ctx->enabled = enabled;
}

/* GOOD: Proper defaults */
static void filter_defaults(obs_data_t *settings)
{
    obs_data_set_default_double(settings, "gain_db", 0.0);
    obs_data_set_default_bool(settings, "enabled", true);
}
```

### Common Settings Errors

| Error               | Problem                | Solution                           |
| ------------------- | ---------------------- | ---------------------------------- |
| No range validation | Values out of bounds   | Check min/max in update            |
| Wrong type function | Data corruption        | Match obs*data_get*\* to data type |
| No defaults         | Unpredictable behavior | Implement get_defaults             |
| Hardcoded defaults  | Maintenance burden     | Use get_defaults callback          |

---

## Build System Review

### Required Build Files

```
project/
├── CMakeLists.txt      # Build configuration
├── buildspec.json      # Plugin metadata
├── src/
│   ├── plugin-main.c   # Module entry point
│   └── *.c             # Source files
└── data/
    └── locale/
        └── en-US.ini   # Localization strings
```

### CMakeLists.txt Review

```cmake
# Required: Minimum CMake version
cmake_minimum_required(VERSION 3.28...3.30)

# Required: Project name and version
project(my-plugin VERSION 1.0.0)

# Required: Create module library
add_library(${CMAKE_PROJECT_NAME} MODULE)

# Required: Link libobs
find_package(libobs REQUIRED)
target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE OBS::libobs)

# Required: Add source files
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    src/plugin-main.c
    src/my-filter.c
)
```

### Build Review Checklist

```
□ CMakeLists.txt uses cmake_minimum_required(VERSION 3.28)
□ add_library uses MODULE keyword
□ find_package(libobs REQUIRED) is present
□ target_link_libraries links OBS::libobs
□ All source files are listed in target_sources
□ buildspec.json has valid name and version
□ data/locale/en-US.ini exists with all strings
```

---

## Automated Audit Script

Run this script to check for common issues:

```bash
#!/bin/bash
# obs-plugin-audit.sh

echo "=== OBS Plugin Audit ==="
echo ""

# P0: Critical checks
echo "P0 - CRITICAL:"
echo "  Module macro:"
grep -l "OBS_DECLARE_MODULE" src/*.c || echo "    MISSING: OBS_DECLARE_MODULE not found!"

echo "  Module load:"
grep -A5 "obs_module_load" src/*.c | grep -q "return true" && echo "    OK" || echo "    WARNING: Check return value"

echo "  Destroy callbacks:"
grep -l "bfree" src/*.c || echo "    WARNING: No bfree calls found"

# P1: High priority
echo ""
echo "P1 - HIGH:"
echo "  Static variables:"
grep -c "^static.*=" src/*.c | while read line; do echo "    $line"; done

echo "  Audio thread safety:"
grep -A20 "filter_audio" src/*.c | grep -E "(mutex|lock|malloc)" && echo "    WARNING: Potential blocking in audio thread"

# P2: Medium priority
echo ""
echo "P2 - MEDIUM:"
echo "  Localization:"
ls data/locale/*.ini 2>/dev/null || echo "    WARNING: No locale files found"

echo "  Defaults callback:"
grep -l "get_defaults" src/*.c || echo "    WARNING: No get_defaults found"

echo ""
echo "=== Audit Complete ==="
```

---

## Related Files

- **CHECKLIST.md** - Quick reference review checklist

## Related Skills

- **obs-plugin-developing** - Entry point and overview
- **obs-audio-plugin-writing** - Audio plugin development patterns

## Related Agent

Use **obs-plugin-expert** agent for:

- Coordinated development and review guidance
- Choosing between skills based on task
- Complex plugin development workflows
