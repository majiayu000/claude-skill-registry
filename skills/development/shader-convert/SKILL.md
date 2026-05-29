---
name: shader-convert
description: Convert Shadertoy GLSL shaders to HLSL for Alt-Tabby's D3D11 pipeline
user-invocable: true
disable-model-invocation: true
---

# /shader-convert — GLSL to HLSL Shader Conversion

Convert Shadertoy GLSL shaders to the Alt-Tabby HLSL pixel shader format.

## Invocation

- `/shader-convert` — Scan `src/shaders/` (and subdirs `mouse/`, `selection/`) for any `.glsl` without matching `.hlsl`, convert all
- `/shader-convert <Shadertoy URL>` — Fetch shader from Shadertoy via Playwright, then convert
- `/shader-convert <pasted GLSL + metadata>` — Convert manually pasted shader source

**Not supported:** Multi-buffer shaders (Buffer A/B/C/D tabs). Our pipeline is single-pass only. Skip shaders that require inter-frame feedback or multi-pass rendering.

## Three Modes

### Mode A — Scan Directory (no args)

1. Scan `src/shaders/` and subdirs `src/shaders/mouse/`, `src/shaders/selection/` for any `name.glsl` that has no matching `name.hlsl`
2. For each unconverted shader: convert, create `.hlsl` (and `.json` if missing)
3. Mouse shaders go in `src/shaders/mouse/`, selection shaders in `src/shaders/selection/`, background shaders in `src/shaders/`

### Mode B — Shadertoy URL (arg matches `shadertoy.com/view/`)

Requires the Playwright MCP server. Extracts shader source, metadata, and iChannel textures automatically.

#### Step 0: Check for Playwright MCP

The Playwright MCP is **not loaded by default** — it's toggled on-demand to avoid context bloat.

Check if you have access to `mcp__playwright__browser_navigate`. If NOT available:
1. Tell the user: "Playwright MCP is not enabled. Run this to enable it, then restart Claude Code:"
   ```
   powershell -File tools/toggle-playwright-mcp.ps1 on
   ```
2. **STOP** — do not proceed until the user restarts with Playwright available.

#### Step 1: Navigate and Wait

```
browser_navigate → https://www.shadertoy.com/view/{id}
```

If Cloudflare challenge appears, wait ~10s for auto-pass. Verify the page title changes from "Shader - Shadertoy BETA" to the shader name.

#### Step 2: Extract All Data (single evaluate call)

```javascript
() => {
  const st = window.gShaderToy;
  if (!st) return { error: 'gShaderToy not found' };

  // Metadata
  const info = st.mInfo;

  // Code from each pass via CodeMirror Doc
  const passes = st.mPass.map((p, i) => {
    const code = p.mDocs && typeof p.mDocs.getValue === 'function'
      ? p.mDocs.getValue() : null;
    return { index: i, code, charCount: code ? code.length : 0 };
  });

  // Tab names → map pass index to role
  const tabNames = {};
  for (let i = 0; i < 10; i++) {
    const tab = document.getElementById('tab' + i);
    if (tab) tabNames['tab' + i] = tab.textContent.trim();
  }

  // Pass types from effect renderer (image, common, buffer, sound, cubemap)
  const passTypes = st.mEffect ? st.mEffect.mPasses.map((p, i) => ({
    index: i, type: p.mType
  })) : [];

  // iChannel inputs for the Image pass
  let iChannels = [];
  if (st.mEffect && st.mEffect.mPasses) {
    const imgPass = st.mEffect.mPasses.find(p => p.mType === 'image') || st.mEffect.mPasses[0];
    if (imgPass && imgPass.mInputs) {
      iChannels = imgPass.mInputs.map((inp, ch) => {
        if (!inp) return null;
        return JSON.parse(JSON.stringify(inp.mInfo));
      });
    }
  }

  return {
    info: { name: info.name, username: info.username, description: info.description, tags: info.tags },
    passes, tabNames, passTypes, iChannels
  };
}
```

#### Step 3: Validate Compatibility

Check `passTypes` — if any pass has `type` of `"buffer"`, `"sound"`, or `"cubemap"`:
- `"buffer"` → **STOP**: Multi-buffer shader, not supported. Tell user.
- `"sound"` → **STOP**: Audio-output shader, not supported.
- `"cubemap"` → **STOP**: Cubemap pass, not supported.
- Only `"image"` and `"common"` are valid.

Check `iChannels` for audio inputs:
- If any channel has `mType` !== `"texture"` (e.g., `"music"`, `"musicstream"`, `"webcam"`, `"video"`, `"keyboard"`), note it. Audio channels will need synthetic beat replacement (see §7). Webcam/video/keyboard → skip the shader.

#### Step 4: Save GLSL Source

Combine passes into a single `.glsl` file:
- If a `"common"` tab exists: put Common code first, then `// --- Image ---` separator, then Image code
- If only Image: save directly
- Derive `name` from `info.name` → snake_case (e.g., "Power (Chainsaw Man)" → `power_chain_saw_man`)

#### Step 5: Download iChannel Textures

For each non-null iChannel with `mType === "texture"`:

```javascript
// In browser_run_code (needs Playwright page object for download API)
// NOTE: page.evaluate only accepts one arg — wrap multiple values in an object
async (page) => {
  const textures = [
    { url: 'https://www.shadertoy.com' + mSrc0, file: 'name_i0.png' },
    { url: 'https://www.shadertoy.com' + mSrc1, file: 'name_i1.png' }
  ];
  const results = [];
  for (const tex of textures) {
    const downloadPromise = page.waitForEvent('download', { timeout: 15000 });
    await page.evaluate(({url, filename}) => {
      return fetch(url).then(r => r.blob()).then(blob => {
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(blobUrl);
      });
    }, {url: tex.url, filename: tex.file});
    const download = await downloadPromise;
    await download.saveAs('src/shaders/' + tex.file);
    results.push(tex.file);
  }
  return results;
}
```

- Full URL: `https://www.shadertoy.com` + `mInfo.mSrc` (e.g., `/media/a/...png`)
- Save as: `src/shaders/{name}_i{channel}.png`
- **curl won't work** — Shadertoy returns 403 for direct requests (requires cookies/origin)

#### Step 6: Create .json Metadata

Populate from extracted `info`:
- `name` → `info.name`
- `shadertoyId` → the ID from the URL
- `author` → `info.username`
- `license` → `"CC BY-NC-SA 3.0"` (Shadertoy default)
- `iChannels` → from downloaded textures, include `filter`/`wrap` from `mSampler`

#### Step 7: Close Browser & Convert

**Close the browser (`browser_close`) immediately** — before writing any files or starting HLSL conversion. The Playwright MCP server is a shared resource; holding it open blocks other agents. Extract all data into local variables in Steps 2-5, then close the browser as the very first action in this step.

Proceed to HLSL conversion (same as Mode C).

#### Step 8: Remind User to Disable Playwright MCP

After Mode B is fully complete (conversion, bundle, compile, tests), remind the user:

"Playwright MCP is still enabled and consuming context. To disable it for future sessions, run:"
```
powershell -File tools/toggle-playwright-mcp.ps1 off
```

### Mode C — Paste GLSL (with non-URL args)

1. Ask for a shader name if not obvious from the source
2. Write `src/shaders/name.glsl` with the pasted source
3. Create `src/shaders/name.json` with metadata (prompt for Shadertoy URL/author if not provided)
4. Convert to `src/shaders/name.hlsl`

## Conversion Steps (all modes)

### 1. Mechanical Type Conversions

| GLSL | HLSL |
|------|------|
| `vec2`, `vec3`, `vec4` | `float2`, `float3`, `float4` |
| `ivec2`, `ivec3`, `ivec4` | `int2`, `int3`, `int4` |
| `mat2`, `mat3`, `mat4` | `float2x2`, `float3x3`, `float4x4` |
| `fract()` | `frac()` |
| `mod(a, b)` | `fmod(a, b)` |
| `mix(a, b, t)` | `lerp(a, b, t)` |
| `texture(sampler, uv)` | `tex.Sample(samplerState, uv)` |
| `texelFetch(sampler, coord, lod)` | `tex.Load(int3(coord, lod))` |
| `atan(y, x)` | `atan2(y, x)` |
| `dFdx()`, `dFdy()` | `ddx()`, `ddy()` |

### 2. Constructor Broadcasts

GLSL allows `vec3(x)` as shorthand for `vec3(x, x, x)`. HLSL does too with `float3(x, x, x)` or `(float3)x`.

### 3. Replace Shadertoy Uniforms

| Shadertoy | HLSL cbuffer |
|-----------|-------------|
| `iTime` | `time` |
| `iResolution.xy` | `resolution` |
| `iResolution` (vec3) | `float3(resolution, 1.0)` |
| `iTimeDelta` | `timeDelta` |
| `iFrame` | `frame` |
| `fragCoord` | `input.pos.xy` (from SV_Position) |
| `fragColor` | return value of PSMain |

### 4. Entry Point Wrapper

Replace `void mainImage(out vec4 fragColor, in vec2 fragCoord)` with:

```hlsl
// PSInput and cbuffer are provided by alt_tabby_common.hlsl (prepended automatically)

float4 PSMain(PSInput input) : SV_Target {
    float2 fragCoord = input.pos.xy;
    // ... converted body ...
    return AT_PostProcess(color);  // instead of manual post-processing
}
```

**Y-axis flip:** Shadertoy's `fragCoord.y = 0` is at the **bottom** of the screen; `SV_Position.y = 0` is at the **top**. For shaders with gravity, falling particles, directional motion, or any up/down asymmetry, flip Y at the start:

```hlsl
float2 fragCoord = float2(input.pos.x, resolution.y - input.pos.y);
```

Symmetric shaders (noise fields, clouds, fractals) usually don't need the flip.

### 5. Constant Buffer Header

The cbuffer and PSInput struct are provided by `alt_tabby_common.hlsl`, which is prepended automatically before compilation. **Do NOT include them in the `.hlsl` file.** The common header provides:
- `cbuffer Constants : register(b0)` with all uniforms (144 bytes, 9 × 16-byte rows):
  - **Core**: `time` (float), `resolution` (float2), `timeDelta` (float), `frame` (uint), `darken` (float), `desaturate` (float), `opacity` (float)
  - **Mouse**: `iMouse` (float2, cursor px), `iMouseVel` (float2, velocity px/sec), `iMouseSpeed` (float, magnitude of velocity)
  - **Grid/Compute**: `gridW` (uint, grid width, 0 = no grid), `gridH` (uint, grid height, 0 = no grid), `maxParticles` (uint, particle slots excluding grid cells), `reactivity` (float, cursor force multiplier)
  - **Selection**: `selRect` (float4, x/y/w/h), `selColor` (float4, premul RGBA), `borderColor` (float4, premul RGBA), `borderWidth` (float), `isHovered` (float, intensity: 1.0 = full selected, <1.0 = dimmed for hover), `entranceT` (float), `selGlow` (float, outer glow radius multiplier), `selIntensity` (float, effect blend strength), `rowRadius` (float, user's RowRadius in pixels, 0 = shader decides)
- `struct PSInput` with `SV_Position` and `TEXCOORD0`
- `AT_PostProcess(float3 col)` and `AT_PostProcess(float3 col, float customAlpha)` functions

All fields are populated every frame for all shader categories. Background shaders typically use only core fields. Mouse shaders use core + mouse fields. Selection shaders use core + selection fields.

Compute-enabled mouse shaders access the same cbuffer via `register(b0)` in both `CSMain` and `PSMain`. The common header is prepended for both entry points during compilation.

iChannel `Texture2D`/`SamplerState` declarations still go in the individual `.hlsl` file (they vary per shader and are NOT in the common header).

### 6. Alpha Handling

**Standard shaders** (alpha from brightness): End PSMain with `return AT_PostProcess(color);`

**Shaders with custom alpha** (transparency masks, particle alpha, etc.): End PSMain with `return AT_PostProcess(color, customAlpha);`

`AT_PostProcess` handles darken, desaturate, opacity multiplication, and premultiplied alpha output. Do NOT write these manually.

### 7. Audio Channels

Shadertoy shaders may use `iChannel0..3` for audio input (spectrum/waveform) or produce audio output via a "Sound" tab.

- **Audio input** (e.g., `texture(iChannel0, vec2(freq, 0.0)).r` for spectrum): Replace with a gentle time-based pulse so the shader retains dynamic variation without requiring audio hardware:
  ```hlsl
  float getBeat() {
      return smoothstep(0.6, 0.9, pow(sin(time * 1.5) * 0.5 + 0.5, 4.0)) * 0.3;
  }
  ```
  Adjust frequency/amplitude to match how the original used the audio data (subtle background pulse vs heavy bass reactivity).

- **Audio output** ("Sound" tab shaders): Remove entirely. Alt-Tabby is visual only.

### 8. Mouse Input (iMouse)

Shadertoy provides `iMouse` (pixel coordinates, click state). Alt-Tabby provides mouse data via cbuffer:
- `iMouse` (float2): cursor position in physical pixels
- `iMouseVel` (float2): cursor velocity in pixels/second (smoothed, CPU-computed)
- `iMouseSpeed` (float): magnitude of `iMouseVel` (convenience scalar)

**For background shaders** (no mouse interaction): Zero out or ignore `iMouse`. Set any derived mouse variables to `(float2)0` and simplify away dead code. If mouse is the sole camera control, replace with a time-based sweep:
  ```hlsl
  float2 fakeMouse = float2(
      sin(time * 0.1) * 0.3,
      cos(time * 0.07) * 0.2
  );
  ```

**For mouse-category shaders**: Use `iMouse` for cursor position, `iMouseVel` for direction-dependent effects (particles trailing behind cursor), and `iMouseSpeed` for motion gating (e.g., `if (iMouseSpeed < threshold) return zero`). Speed-gated effects should use `smoothstep()` for gradual activation rather than hard cutoffs.

### 9. iChannel Textures

If the shader uses `iChannel0..3`:

1. Save texture PNGs as `src/shaders/name_i0.png`, `name_i1.png`, etc.
2. Add entries to the `.json` metadata:
   ```json
   "iChannels": [{"index": 0, "file": "name_i0.png", "filter": "linear", "wrap": "repeat"}]
   ```
3. In HLSL, declare textures:
   ```hlsl
   Texture2D iChannel0 : register(t0);
   SamplerState samp0 : register(s0);
   ```
4. Replace `texture(iChannelN, uv)` with `iChannelN.Sample(sampN, uv)`

## Final Steps (always, after all conversions)

10. Run the bundle script:
    ```
    powershell -File tools/shader_bundle.ps1
    ```

11. Compile shaders to DXBC:
    ```
    powershell -File tools/shader_compile.ps1
    ```

12. Run tests:
    ```
    .\tests\test.ps1
    ```

## .json Metadata Format

```json
{
  "name": "Display Name",
  "shadertoyId": "XXXXXX",
  "author": "Author Name",
  "license": "CC BY-NC-SA 3.0",
  "opacity": 0.50,
  "iChannels": [],
  "timeOffsetMin": 40,
  "timeOffsetMax": 120,
  "timeAccumulate": true
}
```

- `opacity`: Default layer opacity when compositing (0.0-1.0)
- `iChannels`: Array of texture references (empty if no textures needed)
- `timeOffsetMin`: (optional) Minimum random time offset in seconds. Skips the shader's warmup period so it looks interesting immediately. Falls back to config `ShaderTimeOffsetMin` (default 30) if omitted.
- `timeOffsetMax`: (optional) Maximum random time offset in seconds. Falls back to config `ShaderTimeOffsetMax` (default 90) if omitted. Set higher for shaders with long warmup (e.g., volumetric fog needs 40-120s).
- `timeAccumulate`: (optional) When true, shader time persists across overlay show/hide so it picks up where it left off. Falls back to config `ShaderTimeAccumulate` (default true) if omitted. Set false for shaders with a deliberate intro animation you want to see each time.
- `category`: (optional) `"mouse"` or `"selection"` for shaders in subdirectories. Background shaders (root dir) omit this field.
- `compute`: (optional) `{ "maxParticles": N, "particleStride": 32, "baseParticles": M }`. When present, the shader is compiled as a compute+pixel pair. CS entry point is `CSMain` (compiled with `cs_5_0`), PS entry point is `PSMain` (compiled with `ps_5_0`), both in the same `.hlsl` file. The compute shader writes to `RWStructuredBuffer` via UAV; the pixel shader reads the same buffer as `StructuredBuffer` at `register(t4)`. Only used for mouse-category shaders that need persistent GPU-side state (particles, waves).
  - `baseParticles` is the shader's intrinsic particle count (0 for pure-grid fluids, 128/384 for particle+grid). `maxParticles` in the JSON is the default total (= baseParticles + gridW * gridH at high quality). At runtime, actual buffer size is computed from `baseParticles * ParticleDensity + gridW * gridH` where grid dimensions come from `GridQuality` config.

Add time fields when the shader has a notable warmup period or deliberate intro. Omit them for shaders that look good immediately at any time value.

**Note on shader models:** Compute shaders require `cs_5_0` profile (DX11 feature level 11_0). Compute-paired pixel shaders use `ps_5_0`. Background and selection shaders remain `ps_4_0` for maximum compatibility.

### Compute Shader Architectures

Compute-enabled mouse shaders follow one of three buffer layout patterns:

- **Particle + Grid** (ember_trail, ember_trail_long, campfire_embers, smoke_trail, fireflies, scatter, gravity_well, neon_trail): Buffer = `[particles 0..N-1] [grid cells N..N+W*H-1]`. CS particle threads do physics, CS grid threads accumulate nearby particles. PS bilinear-samples the grid. Grid cells reuse the Particle struct: `pos.xy` = accumulated RG, `vel.xy` = accumulated BA.
- **Pure Grid / Fluid** (fluid_aquarium, fluid_calm, fluid_emit, water_surface): Buffer = `[grid cells 0..W*H-1]`. CS runs wave/fluid equations. PS samples the grid.
- **No Grid** (ripple): Buffer = `[slots 0..N-1]`. CS manages slot lifecycle. PS loops over all slots.

### Shader Categories

Shaders are organized into three categories by directory:
- **Background shaders** (`src/shaders/`): Composited as stackable layers behind the window list. Up to 4 layers.
- **Mouse shaders** (`src/shaders/mouse/`): Single-slot effect receiving cursor data: `iMouse` (position), `iMouseVel` (velocity px/sec), `iMouseSpeed` (speed magnitude). Add `"category": "mouse"` to JSON.
- **Selection shaders** (`src/shaders/selection/`): Single-slot effect for row selection highlight. Receives `selRect`, `selColor`, `borderColor`, `borderWidth`, `isHovered`, `entranceT`, `selGlow`, `selIntensity`, `rowRadius` via cbuffer. `isHovered` is an intensity multiplier (1.0 = full selected, <1.0 = dimmed for hover reuse) — use it directly as `float intensity = isHovered;`. Do NOT hardcode hover dimming (e.g., `lerp(1.0, 0.45, isHovered)` is wrong). For corner radius, use `rowRadius > 0.0 ? rowRadius : min(hs.x, hs.y) * 0.15` so the shader respects the user's RowRadius setting while falling back to 15% of the smaller half-dimension. Add `"category": "selection"` to JSON.
