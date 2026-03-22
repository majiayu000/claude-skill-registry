---
name: review-d3d
description: Audit the D3D11 interop layer for per-frame waste — buffer allocations, redundant state calls, GPU readback efficiency
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-audit the D3D11 shader host code for per-frame waste — unnecessary allocations, redundant pipeline state calls, readback overhead. Use explore agents for independent subsystems.

## Context

Alt-Tabby renders pixel shaders via a D3D11 immediate context, then copies the result to a D2D1 bitmap for compositing. The main per-frame entry point is `Shader_PreRender()` which executes the full D3D11 pipeline: constant buffer update → compute dispatch (for compute-enabled shaders) → state setup → Draw → GPU→CPU readback → D2D bitmap write. Compute shaders write to `RWStructuredBuffer` via UAV; the same buffer is then bound as SRV at slot 4 for the pixel shader to read. Dispatch count is computed from `entry.csNumElements` (= effective particles + grid cells), which varies by `GridQuality` and `ParticleDensity` config settings. Buffer size also varies -- `_Shader_CreateComputeBuffer` allocates based on config-driven element count from `_Shader_ComputeBufferLayout()`, not the static JSON `maxParticles`. Auditing buffer size should check the allocation matches the dispatch count.

At 120-240fps, this pipeline runs every frame. Each `Buffer()` allocation, each redundant `ComCall`, and each avoidable state transition costs real time.

**Multi-shader-per-frame reality (post-#177):** `Shader_PreRender` is no longer called once per frame — it runs once per active shader layer (up to 4 background + 1 mouse + 1 selection + 1 hover = 7 invocations). Each invocation is the full D3D11 pipeline. Per-call waste multiplied by 7 is the actual per-frame cost. Additionally, compute-enabled shaders (mouse effects) run both a CS dispatch AND a PS draw per invocation.

**Scope**: Only `src/gui/d2d_shader.ahk` — the D3D11 host-side interop code. Does NOT cover:
- HLSL shader source optimization (use `review-shaders` for that)
- The D2D paint pipeline that consumes the shader output (use `review-paint` for that)
- Shader compilation or bundling tooling

## What to Look For

### 1. Per-Frame Buffer Allocations (Highest Priority)

`Shader_PreRender()` allocates multiple marshaling Buffers every frame for D3D11 API calls. These are AHK heap allocations created, filled via NumPut, passed to ComCall, then discarded.

Known allocation sites per frame:
- `mapped` buffer (16 bytes) — for `Map`/`Unmap` of constant buffer AND staging texture (allocated twice)
- `rtvBuf` (8 bytes) — holds single RTV pointer for `OMSetRenderTargets`
- `vp` (24 bytes) — viewport struct for `RSSetViewports`
- `cbBuf` (8 bytes) — holds cbuffer pointer for `PSSetConstantBuffers`
- `srvBuf` (8×N bytes) — SRV pointer array for `PSSetShaderResources` (when iChannels present)
- `sampBuf` (8×N bytes) — sampler pointer array for `PSSetSamplers`
- `nullSrvBuf` (8×N bytes) — null SRV array for unbinding (when iChannels present)

**The fix pattern** (from `ahk-patterns.md`):
```ahk
; WRONG — allocates every call
Shader_PreRender(...) {
    mapped := Buffer(16, 0)
    NumPut("Ptr", dataPtr, mapped, 0)
    ComCall(14, ctx, ..., "Ptr", mapped, ...)
}

; CORRECT — static buffer, repopulated (ONLY if function is not reachable during STA pump)
Shader_PreRender(...) {
    static mapped := Buffer(16, 0)
    NumPut("Ptr", dataPtr, mapped, 0)
    ComCall(14, ctx, ..., "Ptr", mapped, ...)
}
```

Check: Are any buffers reusable as `static`? Verify no STA pump reentrancy — `Critical "On"` does NOT prevent reentrancy from COM calls (BeginDraw, EndDraw, DrawBitmap, DwmFlush all pump the STA message loop). If the function is reachable during a COM call's STA pump, static buffers are unsafe. Also verify no size variance between calls.

### 2. Redundant D3D11 State Calls

The D3D11 immediate context is a state machine. Once state is set, it persists until changed. Check whether `Shader_PreRender` sets state that hasn't changed since the previous frame:

- **`IASetPrimitiveTopology(TRIANGLELIST)`** — topology never changes (always fullscreen triangle). Could be set once in `Shader_Init()`.
- **`VSSetShader(gShader_VS)`** — vertex shader never changes. Could be set once.
- **`PSSetConstantBuffers(0, 1, cbBuf)`** — same cbuffer every frame. Could be set once.
- **`PSSetSamplers(...)`** — same sampler every frame if shader hasn't changed. Could be set once per shader switch.
- **`PSSetShader`** — only needs to change when shader switches, not every frame.

**Caveat**: D2D's `BeginDraw`/`EndDraw` may dirty the D3D11 state between frames. If D2D touches the immediate context, we may need to re-set state. Verify whether D2D actually dirties these specific state slots.

### 3. Double Allocations

Look for cases where the same logical buffer is allocated more than once per frame:
- `mapped` buffer used for both cbuffer Map AND staging texture Map — could be a single `static` reused
- `srvBuf` for binding and `nullSrvBuf` for unbinding — same size, could reuse one buffer (zero it out for unbind)

### 4. GPU→CPU Readback Path

Every frame executes: `CopyResource(staging, rt)` → `Map(staging)` → pixel memcpy → `Unmap(staging)`. This is the most expensive per-frame operation (GPU stall + memory copy). Check:

- **Is the staging texture created with optimal usage flags?** (`D3D11_USAGE_STAGING` + `CPU_ACCESS_READ`)
- **Is there a GPU pipeline stall?** `Map` with `D3D11_MAP_READ` blocks until the GPU finishes. Could a double-buffered staging approach reduce stalls?
- **Is the CopyResource necessary every frame?** If the shader output hasn't changed (e.g., paused time), could we skip the copy?
- **Is `CopyFromMemory` on the D2D bitmap the most efficient transfer?** Could we use a shared DXGI surface instead of staging→CPU→D2D?

Note: Shared DXGI surfaces (DXGI_RESOURCE_MISC_SHARED_KEYED_MUTEX) would eliminate the CPU readback entirely — the D2D bitmap would reference the same GPU memory as the D3D11 render target. This is an architectural change but potentially the highest-impact optimization.

### 5. Render Target Lifecycle

- **Lazy creation**: RT created on first PreRender, resized on dimension change. Verify resize detection is correct (no unnecessary recreate when dimensions match).
- **Shader switching**: Previous shader's RT released, new one created. If the user rapidly cycles shaders, this could cause allocation churn. Check if RT dimensions match and could be reused.
- **Device loss recovery**: How does the code handle D3D11 device removal? Does it recreate cleanly?

### 6. Constant Buffer Update Efficiency

- `Map`/`Unmap` with `D3D11_MAP_WRITE_DISCARD` is the correct pattern for dynamic cbuffers.
- Check: Is the cbuffer size optimal? (144 bytes currently, 9 × 16-byte rows)
- Check: Could we skip the cbuffer update if no values changed? (Unlikely — `time` changes every frame, but `darken`/`desaturate` don't.)

### 7. Compute Dispatch Path Efficiency

Compute-enabled shaders (mouse effects) run a CS5.0 dispatch before the pixel shader draw. The dispatch sequence includes: unbind PS SRV at slot 4 → bind UAV at u0 → CSSetShader → Dispatch → unbind UAV → rebind as SRV for PS. Check:

- **Is the UAV bind/unbind necessary every frame?** If the same compute shader runs consecutive frames, the UAV binding persists. Only need to rebind on shader switch.
- **Dispatch group count**: Computed from `entry.csNumElements` via `Ceil(N / 256)`. Verify the thread group size (256) matches the HLSL `[numthreads]` declaration.
- **CS→PS resource hazard**: The unbind-rebind cycle (UAV → SRV) ensures the GPU finishes compute before pixel shader reads. Verify this is done correctly — missing the unbind causes undefined behavior. But also check: is the null-bind necessary, or does the PS bind implicitly resolve the hazard?

### 8. ComCall Exception Guarding

The code wraps ComCall in `try` blocks. Check:
- Are try/catch blocks used per-call or per-block? Per-call try/catch has higher overhead.
- Could error checking use HRESULT return values instead of exceptions?
- Is the exception guarding actually needed for all calls, or only for specific failure-prone ones?

### 9. Any other detected optimizations.

## Files to Audit

Primary:
- `src/gui/d2d_shader.ahk` — the entire D3D11 interop layer

Supporting (for understanding the call pattern):
- `src/gui/gui_effects.ahk` — where `FX_PreRenderShaderLayers` loops active layers calling `Shader_PreRender`, plus mouse/selection/hover pre-render. Also manages shader init/dispose and layer registration
- `src/gui/gui_paint.ahk` — where `FX_DrawShaderLayers` calls `Shader_GetBitmap` + `DrawImage` per layer
- `src/gui/gui_interceptor.ahk` — where shader switching happens (V key toggle)

## Explore Strategy

Split by concern (run in parallel):

- **Allocation agent**: Read `Shader_PreRender()` line by line. Map every `Buffer(` allocation — size, purpose, whether it varies between calls, whether it could be `static`. Also check `Shader_Init`, `Shader_Register*` for any per-call waste.
- **State redundancy agent**: Read `Shader_PreRender()` and list every `ComCall` that sets D3D11 pipeline state. For each, determine: does this state change between frames? Could it be set once in init or on shader switch? Cross-reference with D2D's `BeginDraw`/`EndDraw` to check if D2D dirties the state.
- **Readback agent**: Focus on the GPU→CPU→D2D path (CopyResource → Map → CopyFromMemory). Research whether AHK's D2D wrapper supports shared DXGI surfaces. Check if the current staging texture approach can be optimized (double buffering, skip-if-unchanged).

### Tools

- `query_function.ps1 Shader_PreRender` — extract the full per-frame function body (if query_function.ps1 can't parse it, read `src/gui/d2d_shader.ahk` directly at line ~1055)
- `query_function.ps1 Shader_Init` — extract init code
- `query_interface.ps1 d2d_shader` — shader globals and public API

## Assessment Format

For each finding:

| Finding | File:Lines | Per-Call Cost | Calls/Frame | Per-Frame Cost | Complexity | Fix |
|---------|-----------|--------------|-------------|----------------|------------|-----|
| `mapped` Buffer(16) allocated twice | `d2d_shader.ahk:759,848` | ~2μs | 2 | ~4μs | One-line static | `static mapped := Buffer(16, 0)` |

**Columns:**
- **Per-Call Cost**: Estimated cost per invocation (allocation, ComCall overhead, GPU stall)
- **Calls/Frame**: How many times per frame
- **Per-Frame Cost**: Per-Call × Calls/Frame
- **Complexity**: One-line / small refactor / medium refactor / architectural
- **Fix**: Concrete description

**Do not filter.** At 240fps, 4μs/frame = ~1ms/s. Every ComCall avoided, every Buffer reused, matters. List everything, ordered by per-frame cost (highest first).

**Separate architectural findings** (like shared DXGI surfaces) into their own section with honest complexity/risk assessment.

## Validation

1. **Trace the actual call path**: Confirm each finding is in the per-frame path, not init-time. `Shader_Init` runs once; `Shader_PreRender` runs every frame.
2. **Check D2D state dirtying**: Before claiming a D3D11 state call is redundant, verify D2D's `BeginDraw`/`EndDraw` doesn't reset it. If uncertain, note the uncertainty.
3. **Verify static safety**: `static` buffers in AHK persist across calls. `Critical "On"` prevents timer/hotkey interruption but does NOT prevent STA pump reentrancy — any COM call (ComCall) can dispatch callbacks that re-enter the same function. Only use `static` buffers when the buffer is fully consumed (NumGet'd into locals) before any COM call, or when the function is provably unreachable from STA pump paths.
4. **Preserve Float() on GPU buffers**: Never remove `Float()` wrappers from `NumPut("float", ...)` calls that feed D3D11/D2D buffers (cbuffers, viewports, rects). These ensure IEEE 754 bit patterns — AHK v2 integer-to-float coercion in NumPut is not guaranteed safe. Removing them is not an optimization.
5. **Check existing optimizations**: The code already has some optimization (lazy RT creation, shared cbuffer). Don't re-flag what's already handled.

## Plan Format

**Section 1 — Per-Frame Allocations:**

| Finding | File:Lines | Per-Call Cost | Calls/Frame | Per-Frame Cost | Complexity | Fix |
|---------|-----------|--------------|-------------|----------------|------------|-----|

**Section 2 — Redundant State Calls:**

| Finding | File:Lines | Per-Call Cost | Calls/Frame | Per-Frame Cost | Complexity | Fix |
|---------|-----------|--------------|-------------|----------------|------------|-----|

**Section 3 — Readback Path:**

| Finding | File:Lines | Per-Call Cost | Calls/Frame | Per-Frame Cost | Complexity | Fix |
|---------|-----------|--------------|-------------|----------------|------------|-----|

**Section 4 — Architectural Opportunities:**

| Finding | Current Cost | Potential Savings | Complexity | Risk | Description |
|---------|-------------|-------------------|------------|------|-------------|

Order within each section by per-frame cost (highest first). Architectural opportunities ordered by potential savings.

Ignore any existing plans — create a fresh one.
