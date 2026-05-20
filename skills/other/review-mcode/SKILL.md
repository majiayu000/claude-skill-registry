---
name: review-mcode
description: Scan for hot loops over raw buffers that would benefit from MCode (native C) optimization
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Scan the codebase for MCode optimization opportunities. Use parallelism where possible.

MCode replaces AHK-interpreted tight loops with native C machine code embedded as base64. The project already has an MCode pipeline (`tools/native_benchmark/native_src/`) and a working example (`src/gui/icon_alpha.ahk`). Adding a new function to an existing MCode module is low cost — the infrastructure exists.

## What Qualifies

All four must be true:

1. **Hot path** — called frequently OR scales with data (per-window, per-pixel, per-byte). Use `query_function_visibility.ps1` to check call frequency — a loop called 1x/session vs 100x/sec changes the MCode ROI. Use `query_callchain.ps1 <funcName> -Reverse` to trace all invocation contexts. Use `query_timers.ps1` to check if the candidate is inside a timer callback (hot path signal).
2. **Pure buffer computation** — operates on `Buffer` / `NumGet` / `NumPut`, not AHK objects
3. **Interpreter-bound** — the bottleneck is AHK loop overhead, not an underlying Win32/native call
4. **Measurable** — worst-case cost exceeds ~100μs (below that, DllCall overhead eats the savings)

## What Does NOT Qualify

- **AHK built-ins that already call native C** — `StrPut`, `InStr`, `SubStr`, `Sort`, `RegExMatch` etc.
- **Loops over AHK objects/Maps/Arrays** — MCode can't read AHK objects without COM interop
- **Functions where the expensive part is a DllCall** — GDI+, Win32 API calls. The loop around them is not the bottleneck.
- **Anything under ~100μs worst case** — DllCall marshaling overhead cancels the gain

## What to Look For

- `NumGet` / `NumPut` inside loops (pixel processing, binary protocol parsing, buffer scanning)
- Byte-by-byte or word-by-word buffer iteration
- Math-heavy loops with no AHK object interaction
- Any loop where removing the body makes it instant (= per-iteration AHK overhead dominates)

## Reference

- `src/gui/icon_alpha.ahk` — template for MCode embedding (base64 → CryptStringToBinary → VirtualProtect)
- `tools/native_benchmark/native_src/icon_alpha.c` — reference C source (no CRT, no imports, pure computation)
- `tools/native_benchmark/` — benchmark harness and native build pipeline

## Explore Strategy

Focus on files with buffer/binary operations:

- `src/gui/gui_paint.ahk` — rendering, pixel manipulation
- `src/core/` — icon extraction, process info, any binary data handling
- `src/shared/ipc_pipe.ahk` — binary pipe protocol parsing
- `src/pump/` — icon resolution, bitmap processing
- Any file with `NumGet` or `NumPut` usage

## Plan Format

For each candidate:

| File | Function | Loop Description | Est. Worst Case | Qualifies? | Why |
|------|----------|-----------------|----------------|-----------|-----|
| `foo.ahk:42` | `ScanBuffer()` | NumGet loop over 256KB icon bitmap, ~65k iterations | ~65ms | Yes | Pure buffer, no AHK objects, scales with icon count |
| `bar.ahk:100` | `ParseWindows()` | Loop over window array calling WinGetTitle | ~2ms | No | Bottleneck is Win32 calls, not AHK loop |

For qualifying candidates, additionally note:
- Whether it fits into an existing MCode module (e.g., `icon_alpha`) or needs a new one
- The C function signature it would need
- Any complication (pointer to AHK string, callback needed, etc.)

Ignore any existing plans — create a fresh one.
