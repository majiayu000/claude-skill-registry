---
name: review-shaders
description: Audit HLSL pixel shaders for GPU performance — math optimizations, ALU reduction, texture efficiency at 120-240fps
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-audit HLSL pixel shaders in `src/shaders/` for GPU performance waste — redundant math, avoidable transcendentals, suboptimal patterns. Use maximum parallelism — spawn explore agents for independent shader groups. Every optimization must be visually identical to the original.

## Context

Alt-Tabby renders background shaders at 120-240fps via D3D11 pixel shaders compiled from HLSL to DXBC. These shaders are converted from Shadertoy GLSL — many carry unoptimized patterns from their original authors or from mechanical GLSL→HLSL conversion. At 240fps on a 1440p display, every pixel shader instruction runs ~885M times/second (3840×1600×240÷2 assuming half the overlay is visible). Even saving one ALU instruction matters.

**Scope**: All `src/shaders/**/*.hlsl` files (including `mouse/` and `selection/` subdirs). Includes both pixel shader (`PSMain`) and compute shader (`CSMain`) logic — mouse shaders may contain both in a single `.hlsl` file. Does NOT cover:
- The D3D11 host-side code in `d2d_shader.ahk` (use `review-paint` for the D2D pipeline)
- The AHK-side effect chain or compositing (use `review-paint`)
- Shader compilation or bundling tooling

**Cardinal rule**: Every optimization must produce **visually identical output**. These are aesthetic shaders — if you can't prove the math is equivalent, don't suggest the change. "Close enough" is not acceptable.

## What to Look For

### 1. Redundant Transcendentals (Highest Priority)

Transcendental functions (`sin`, `cos`, `atan2`, `exp`, `log`, `pow`) are the most expensive single instructions on the GPU. Look for:

- **sin/cos of the same angle**: Replace with `sincos(angle, s, c)`. HLSL's `sincos` intrinsic computes both in one operation.
  ```hlsl
  // BEFORE — 2 transcendentals
  float s = sin(angle);
  float c = cos(angle);

  // AFTER — 1 intrinsic
  float s, c;
  sincos(angle, s, c);
  ```

- **Repeated sin/cos calls with the same argument**: Hoist to a local variable.
  ```hlsl
  // BEFORE — sin(time * 0.1) computed 3 times
  x += sin(time * 0.1) * 2.0;
  y += sin(time * 0.1) * 3.0;
  z += sin(time * 0.1);

  // AFTER — computed once
  float st = sin(time * 0.1);
  x += st * 2.0;
  y += st * 3.0;
  z += st;
  ```

- **pow(x, 2.0)**: Replace with `x * x`. `pow` is a transcendental; multiply is ALU.
- **pow(x, 0.5)**: Replace with `sqrt(x)` — dedicated hardware unit.
- **pow(x, N)** for small integer N: Expand manually (`x*x*x` for N=3).
- **exp(x * log(y))**: This is just `pow(y, x)` — but check if the original intent was simpler.

### 2. Avoidable Normalization

- **normalize(v) when length is known**: If you just constructed the vector from unit components or know its length, skip the normalize.
- **Repeated normalize of the same vector**: Hoist to a local.
- **length(v) followed by v/length(v)**: Use `normalize` once, extract length via `rsqrt` if both are needed.

### 3. Loop Optimizations

Many Shadertoy shaders use loops for FBM noise, raymarching, or iterative effects:

- **Loop-invariant expressions**: Anything computed inside the loop that doesn't depend on the loop variable should be hoisted out.
- **Unnecessary iterations**: Some shaders hardcode iteration counts higher than needed for the visual result. If reducing from 8 to 6 iterations produces identical output at the shader's typical scale, note it (but be conservative — this is the riskiest optimization).
- **Accumulator patterns**: `total += noise(p) * amp; p = mul(p, m); amp *= decay;` — ensure `mul` and noise calls can't be simplified.

### 4. Matrix and Vector Math

- **mul(v, M) vs mul(M, v)**: HLSL matrix multiplication order matters. Ensure the correct convention is used and no unnecessary transpose is happening.
- **Rotation matrices computed per-pixel**: If the rotation angle is uniform (from cbuffer `time`), the matrix is constant across all pixels — move to a static const or compute once.
  ```hlsl
  // BEFORE — per-pixel (wasteful if angle is uniform)
  float2x2 rot = float2x2(cos(a), sin(a), -sin(a), cos(a));

  // AFTER — single sincos + construction
  float s, c;
  sincos(a, s, c);
  float2x2 rot = float2x2(c, s, -s, c);
  ```
  Note: HLSL `static` local variables are computed once per draw call, not per-pixel.

- **Constructing float2x2/float3x3 from constants**: Use `static const` so the compiler knows it's constant.

### 5. Texture Sampling

For shaders with `iChannel` textures:

- **Redundant samples**: Same texture sampled at the same UV more than once — hoist to a local.
- **Sample in divergent branch**: Texture samples in dynamic branches can cause quad inefficiency. Note but don't change unless the branch is clearly avoidable.

### 6. Algebraic Simplifications

- **`x * 0.5 + 0.5`**: This is `mad(x, 0.5, 0.5)` — the compiler usually handles this, but explicit `mad()` is clearer intent.
- **`1.0 - (1.0 - x)`**: Simplifies to `x`.
- **`a / b * c`**: If `b` is constant, use `a * (c / b)` — one multiply instead of divide + multiply. Division is expensive on GPU.
- **`length(v) * length(v)`**: Use `dot(v, v)` — avoids the sqrt inside length.
- **`abs(x) * abs(x)`**: Same as `x * x`.
- **`clamp(x, 0.0, 1.0)`**: Use `saturate(x)` — free on most GPU hardware (modifier, not instruction).
- **`max(x, 0.0)`**: Could be `saturate(x)` if upper bound doesn't matter, or leave as `max`.
- **`smoothstep(0.0, 1.0, x)`**: Equivalent to `x*x*(3.0 - 2.0*x)` with `saturate`, but `smoothstep` is fine — compiler knows this.
- **Repeated subexpressions**: Factor out common terms. GPUs can't CSE across basic blocks as well as CPUs.

### 7. Conversion Artifacts

Mechanical GLSL→HLSL conversion can introduce waste:

- **`fmod` instead of `frac`**: In GLSL, `mod(x, 1.0)` is idiomatic. The converter produces `fmod(x, 1.0)` but `frac(x)` is cheaper (single instruction, no divide).
- **Unnecessary float3 → float4 → float3 conversions**: Check `.xyz` / `float4(v3, 1.0)` chains.
- **`(float3)x` broadcast**: Fine, but check if the original GLSL was doing something more specific.
- **Dead code from removed features**: iMouse handling zeroed out but code still computing with the zero. Simplify away.

### 8. Constant Folding Hints

HLSL compilers are good but not perfect. Help them:

- **`static const`** for values computed from other constants: ensures compile-time evaluation.
- **Literal precision**: `3.14159265` is fine, but `3.14159265358979323846` wastes parser time with no precision gain in `float` (only 7 significant digits). Use `3.14159265` or better yet `3.14159265f`.
- **Integer vs float constants**: `2.0` in float context is fine; `2` might cause an implicit cast in some contexts.

### 9. Any other detected optimizations.

### 10. Compute Shader Patterns

1. **Grid accumulation inner loop**: The `O(maxParticles)` loop inside each grid cell thread is the hottest compute code. Key optimizations: early-exit radius check (`if (dist > maxRadius) continue;`) before computing glow/color; skip dead particles (`if (p.life >= 1.0) continue;`) as first check; avoid redundant normalize.
2. **Grid cell packing**: Grid cells reuse the Particle struct to store RGBA (`pos.xy` = RG, `vel.xy` = BA). This is intentional for buffer reuse -- don't suggest cleanup.
3. **Dispatch thread count**: CS dispatches `ceil(totalElements / 64)` threads. The `if (idx >= total) return;` guard is necessary for non-multiple-of-64 buffer sizes -- don't flag as waste.
4. **Config-driven sizing**: Grid dimensions and particle counts are now runtime values from cbuffer (`gridW`, `gridH`, `maxParticles`), not compile-time `#define` constants. Buffer allocation comes from `_Shader_ComputeBufferLayout()` in d2d_shader.ahk.
5. **Reactivity multiplier**: All cursor forces in compute shaders are scaled by `reactivity` (cbuffer float at offset 124). Reviews should verify new shaders multiply cursor-dependent forces by this value.

## Files to Audit

All `.hlsl` files in `src/shaders/` and subdirectories (`mouse/`, `selection/`). There are 150+ shaders. Organize the audit by pattern, not by individual file — many shaders share the same noise functions, FBM loops, and rotation patterns.

**Use the `.glsl` source as reference** when verifying visual equivalence — it shows the original author intent.

## Explore Strategy

Split by optimization category (run in parallel):

- **Transcendentals agent**: Scan ALL `.hlsl` files for `sin(`, `cos(`, `pow(`, `exp(`, `atan2(`. Find paired sin/cos, repeated calls, pow with integer/simple exponents. Count frequency per file.
- **Loop agent**: Find all `for` loops in `.hlsl` files. Check for loop-invariant hoisting opportunities, unnecessary iterations, per-pixel matrix construction inside loops.
- **Algebraic agent**: Scan for `fmod(.*1.0)`, `length(.*length(`, `clamp(.*0.0.*1.0)`, division by constants, `1.0 - (1.0 -`, and other algebraic simplification opportunities.
- **Conversion artifact agent**: Compare `.hlsl` against `.glsl` for each shader. Find dead iMouse code, unnecessary type conversions, `fmod` that should be `frac`.

### Tools

- Grep for pattern scanning across all HLSL files
- Read for examining specific shaders in detail
- The `.glsl` file next to each `.hlsl` is the original Shadertoy source for reference
- `query_interface.ps1 <file>` — understand the public surface of D3D11 infrastructure files (`d2d_shader.ahk`, `gui_effects.ahk`) when tracing how shaders are loaded and composed

## Assessment Format

Group findings by **pattern**, not by individual file. Many shaders will share the same issue.

For each pattern:

| Pattern | Affected Shaders | Per-Pixel Cost Saved | Complexity | Fix |
|---------|-----------------|---------------------|------------|-----|
| Paired sin/cos → sincos | `fire.hlsl:45`, `accretion.hlsl:23`, +12 more | ~1 transcendental/pixel | One-line per site | `sincos(angle, s, c)` |

**Columns:**
- **Pattern**: The optimization pattern being applied
- **Affected Shaders**: List files:lines (show first 3, then "+N more" if widespread)
- **Per-Pixel Cost Saved**: Estimated ALU/transcendental savings per pixel
- **Complexity**: How mechanical is the fix? "Find-replace" / "Simple refactor" / "Needs visual verification"
- **Fix**: Concrete transformation

Then for each affected file, list the specific locations as a sub-table or bullet list so implementation can be done methodically.

**Do not filter.** A single saved transcendental ×885M pixels/sec = real watts and real frame time. List everything.

## Validation

1. **Prove equivalence**: For every suggested change, show the mathematical equivalence. `sincos(a, s, c)` produces exactly `s=sin(a), c=cos(a)` — trivially equivalent. `x*x` vs `pow(x, 2.0)` — equivalent for all finite float values. If equivalence requires assumptions (e.g., "x is non-negative"), state the assumption and verify it holds in context.

2. **Check the GLSL original**: If the HLSL already differs from the GLSL in a way that suggests intentional optimization during conversion, don't flag it again.

3. **Don't break visual output**: If unsure whether a simplification is visually identical, err on the side of not suggesting it. Mark uncertain cases as "needs visual verification."

4. **Respect author intent**: Some "inefficiencies" are intentional artistic choices (e.g., a specific pow curve for color grading). Don't optimize these away.

## Plan Format

**Section 1 — Transcendental Optimizations:**

| Pattern | Affected Shaders | Per-Pixel Cost Saved | Complexity | Fix |
|---------|-----------------|---------------------|------------|-----|

**Section 2 — Loop Optimizations:**

| Pattern | Affected Shaders | Per-Pixel Cost Saved | Complexity | Fix |
|---------|-----------------|---------------------|------------|-----|

**Section 3 — Algebraic Simplifications:**

| Pattern | Affected Shaders | Per-Pixel Cost Saved | Complexity | Fix |
|---------|-----------------|---------------------|------------|-----|

**Section 4 — Conversion Artifacts:**

| Pattern | Affected Shaders | Per-Pixel Cost Saved | Complexity | Fix |
|---------|-----------------|---------------------|------------|-----|

Order within each section by total impact (per-pixel savings × number of affected shaders, highest first).

Ignore any existing plans — create a fresh one.

## MANDATORY: Post-Implementation Verification

After implementing any shader changes, you MUST:

1. **Run the full `--live` test suite** — `powershell -File tests/test.ps1 --live`. This compiles the exe (which compiles HLSL→DXBC) and validates everything end-to-end.
2. **Check `git status`** for changed `.bin` files in `resources/shaders/`. HLSL source changes produce new compiled DXBC binaries — these MUST be committed alongside the `.hlsl` changes.
3. **Do not ship** until both the test suite passes and all compiled bins are staged.

Shader changes without compiled bins are broken — the compiled exe embeds the `.bin` files, not the `.hlsl` source.
