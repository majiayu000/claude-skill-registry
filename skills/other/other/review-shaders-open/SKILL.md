---
name: review-shaders-open
description: Audit HLSL pixel shaders for GPU performance — math optimizations, ALU reduction, texture efficiency at 120-240fps
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-audit HLSL pixel shaders in src/shaders/ for GPU performance waste — redundant math, avoidable transcendentals, suboptimal patterns. Use maximum parallelism — spawn explore agents for independent shader groups. Every optimization must be visually identical to the original.

Context
Alt-Tabby renders background shaders at 120-240fps via D3D11 pixel shaders compiled from HLSL to DXBC. These shaders are converted from Shadertoy GLSL — many carry unoptimized patterns from their original authors or from mechanical GLSL→HLSL conversion. At 240fps on a 1440p display, every pixel shader instruction runs ~885M times/second (3840×1600×240÷2 assuming half the overlay is visible). Even saving one ALU instruction matters.

Scope: All src/shaders/**/*.hlsl files (including mouse/ and selection/ subdirs). Includes both pixel shader (PSMain) and compute shader (CSMain) logic — mouse shaders may contain both in a single .hlsl file. Does NOT cover:

The D3D11 host-side code in d2d_shader.ahk (use review-paint for the D2D pipeline)
The AHK-side effect chain or compositing (use review-paint)
Shader compilation or bundling tooling
Cardinal rule: Every optimization must produce visually identical output. These are aesthetic shaders — if you can't prove the math is equivalent, don't suggest the change. "Close enough" is not acceptable.

What to Look For
Any other detected optimizations. In the past I've directed you - this time, lets see what you do on your own.

Files to Audit
All .hlsl files in src/shaders/ and subdirectories (mouse/, selection/). There are 150+ shaders. Organize the audit by pattern, not by individual file — many shaders share the same noise functions, FBM loops, and rotation patterns.

Use the .glsl source as reference when verifying visual equivalence — it shows the original author intent.

Explore Strategy
Do not filter. A single saved transcendental ×885M pixels/sec = real watts and real frame time. List everything.

Validation
Prove equivalence: For every suggested change, show the mathematical equivalence. If equivalence requires assumptions (e.g., "x is non-negative"), state the assumption and verify it holds in context.

Check the GLSL original: If the HLSL already differs from the GLSL in a way that suggests intentional optimization during conversion, don't flag it again.

Don't break visual output: If unsure whether a simplification is visually identical, err on the side of not suggesting it. Mark uncertain cases as "needs visual verification."

Respect author intent: Some "inefficiencies" are intentional artistic choices (e.g., a specific pow curve for color grading). Don't optimize these away.

Plan Format
Section 1 — Transcendental Optimizations:

Pattern	Affected Shaders	Per-Pixel Cost Saved	Complexity	Fix
Section 2 — Loop Optimizations:

Pattern	Affected Shaders	Per-Pixel Cost Saved	Complexity	Fix
Section 3 — Algebraic Simplifications:

Pattern	Affected Shaders	Per-Pixel Cost Saved	Complexity	Fix
Section 4 — Conversion Artifacts:

Pattern	Affected Shaders	Per-Pixel Cost Saved	Complexity	Fix
Order within each section by total impact (per-pixel savings × number of affected shaders, highest first).

Ignore any existing plans — create a fresh one.

## MANDATORY: Post-Implementation Verification

After implementing any shader changes, you MUST:

1. **Run the full `--live` test suite** — `powershell -File tests/test.ps1 --live`. This compiles the exe (which compiles HLSL→DXBC) and validates everything end-to-end.
2. **Check `git status`** for changed `.bin` files in `resources/shaders/`. HLSL source changes produce new compiled DXBC binaries — these MUST be committed alongside the `.hlsl` changes.
3. **Do not ship** until both the test suite passes and all compiled bins are staged.

Shader changes without compiled bins are broken — the compiled exe embeds the `.bin` files, not the `.hlsl` source.
