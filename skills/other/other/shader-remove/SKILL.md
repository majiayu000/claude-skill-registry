---
name: shader-remove
description: Remove a shader and all its associated files from the project
user-invocable: true
disable-model-invocation: true
---

# /shader-remove — Remove a Shader

Remove a shader by display name, disk name, or filename.

## Invocation

- `/shader-remove Matrix Rain`
- `/shader-remove matrix_rain`
- `/shader-remove matrix_rain.json`

## Steps

### 1. Resolve the Shader

The argument can be:
- **Display name** (e.g., `Matrix Rain`) — scan `src/shaders/**/*.json` (including `mouse/` and `selection/` subdirs), match on the `"name"` field (case-insensitive)
- **Disk name** (e.g., `matrix_rain`) — look for `src/shaders/matrix_rain.json`, `src/shaders/mouse/matrix_rain.json`, or `src/shaders/selection/matrix_rain.json`
- **Filename** (e.g., `matrix_rain.json` or `matrix_rain.hlsl`) — strip extension, use as disk name

If no match found, list available shaders and stop.

### 2. Read Metadata

Read the matched `.json` file to discover iChannel texture files referenced in `"iChannels"` and the shader's directory.

### 3. Delete Source Files

Remove all files belonging to the shader from its directory (`src/shaders/`, `src/shaders/mouse/`, or `src/shaders/selection/`):
- `{name}.glsl`
- `{name}.hlsl`
- `{name}.json`
- Any iChannel textures listed in the metadata (e.g., `{name}_i0.png`)

Only delete files that exist — don't error on missing `.glsl` (some shaders may not have the original).

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

Summarize what was removed (list each deleted file).
