---
name: dsp-runtime
description: Use when working on the DSP engine, biquad cascade, kernel math, interpolation, minifloat codec, coefficient ramping, AGC, DF2T render, control blocks, or any code in trench-core/ or the audio path of trench-plugin/
---

Before writing any code, read these files:
- `docs/context/runtime-pipeline.md` — proven CPhantomRTFilter pipeline, memory layout, bilinear interpolation, minifloat codec
- `docs/context/q-law.md` — Q architecture, SINC table correction

Key constraints:
- Plugin runtime is 44100 Hz. Never 39062.5 in audio path.
- Interpolate kernel-form [c0..c4] only. Never raw biquad [b0,b1,b2,a1,a2].
- Interpolation order: Q first, then morph.
- 32-sample control blocks, per-sample ramping.
- No allocations on audio thread. The commit-guard hook will catch this but don't rely on it.
- Read `trench-core/CLAUDE.md` for kernel form, AGC table, stability rules
