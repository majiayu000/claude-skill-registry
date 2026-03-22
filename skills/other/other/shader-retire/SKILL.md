---
name: shader-retire
description: Retire a shader by moving its files to legacy/shaders_retired
user-invocable: true
disable-model-invocation: true
---

# /shader-retire — Retire a Shader

Move a shader out of the active set into `legacy/shaders_retired/` by display name, disk name, or filename.

## Invocation

- `/shader-retire Matrix Rain`
- `/shader-retire matrix_rain`
- `/shader-retire matrix_rain.json`

## Steps

### 1. Resolve the Shader

The argument can be:
- **Display name** (e.g., `Matrix Rain`) — scan `src/shaders/**/*.json` (including `mouse/` and `selection/` subdirs), match on the `"name"` field (case-insensitive)
- **Disk name** (e.g., `matrix_rain`) — look for `src/shaders/matrix_rain.json`, `src/shaders/mouse/matrix_rain.json`, or `src/shaders/selection/matrix_rain.json`
- **Filename** (e.g., `matrix_rain.json` or `matrix_rain.hlsl`) — strip extension, use as disk name

If no match found, list available shaders and stop.

### 2. Read Metadata

Read the matched `.json` file to discover iChannel texture files referenced in `"iChannels"` and the shader's directory.

### 3. Move Source Files

Create `legacy/shaders_retired/` if it doesn't exist, then move all files belonging to the shader from its directory (`src/shaders/`, `src/shaders/mouse/`, or `src/shaders/selection/`) into it:
- `{name}.glsl`
- `{name}.hlsl`
- `{name}.json`
- Any iChannel textures listed in the metadata (e.g., `{name}_i0.png`)

Only move files that exist — don't error on missing `.glsl` (some shaders may not have the original).

### 4. Regenerate Bundles

```
powershell -File tools/shader_bundle.ps1
```

This regenerates `src/gui/shader_bundle.ahk` and `src/gui/shader_resources.ahk`, and cleans stale textures from `resources/img/shaders/`.

### 5. Run Tests

```
.\tests\test.ps1
```

### 6. Report

Summarize what was retired (list each moved file).
