---
name: game-sprite-pipeline
version: 2.0.0
description: "AI sprite generation: portraits, idle loops, animated sheets via Codex/Nano Banana. Per-row generation, animation presets, video-to-sprite, identity lock. Use for generated character art."
agent: python-general-engineer
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Edit
routing:
  triggers:
    - AI sprite
    - AI character art
    - generate character
    - generate sprite
    - generate wrestler
    - generate character portrait
    - spritesheet pipeline
    - animated spritesheet
    - animated sprite
    - portrait loop
    - idle loop
    - road-to-aew sprite
    - sprite for road-to-aew
    - wrestler portrait
    - character sheet
    - fighter spritesheet
    - RPG character spritesheet
    - platformer spritesheet
    - per-row sprite generation
    - video to sprite
    - animation preset
    - deterministic idle
    - breathing loop
    - sprite QA
    - contact sheet
  complexity: Complex
  category: game
  pairs_with:
    - phaser-gamedev
    - threejs-builder
    - python-general-engineer
    - motion-pipeline
---

# Game Sprite Pipeline

Local-first AI sprite generation. One skill, four modes behind `--mode`:

- `portrait` — single full-body character PNG (road-to-aew wrestlers, card-game characters).
- `portrait-loop` — 2×2 = 4-frame subtle idle (breathing + blink) at 200ms/frame in ONE Codex call. Animated portraits without re-prompting new poses.
- `spritesheet` — animated multi-frame grid with connected-components detection, ground-line anchor alignment, and Phaser atlas output.
- `spritesheet --per-row` — row-strip generation: each animation state generated as a separate strip with layout guide grounding and identity lock, then composited into a final sheet. Eliminates cross-row contamination and reduces retry scope from whole-sheet to single-row.

Backend chain (per ADR-198): Codex CLI imagegen is the default when installed and authed. When Codex is unavailable AND `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) is set, the skill falls back to Nano Banana via `nano-banana-builder`'s scripts. When neither is available, the skill fails loud with `BackendUnavailableError` listing both fix paths. Both paths use keys the user already holds — there is no third-party billing the toolkit hides. Reference implementation of the "Local-First, Deterministic Systems Over External APIs" principle in `docs/PHILOSOPHY.md` (user-owned-key clause).

## When to use

| User says | Mode | Entry script |
|-----------|------|--------------|
| "generate a wrestler portrait" | `portrait` | `portrait_pipeline.py` |
| "add a new enemy to road-to-aew" | `portrait` | `portrait_pipeline.py --target road-to-aew` |
| "animated idle portrait" / "subtle breathing loop" | `portrait-loop` | `portrait_pipeline.py --mode portrait-loop` |
| "make a walk cycle spritesheet" | `spritesheet` | `sprite_pipeline.py` |
| "4-direction character sheet" | `spritesheet` | `sprite_pipeline.py --grid 4x4` |
| "Phaser-ready texture atlas" | `spritesheet` | `sprite_pipeline.py` (emits atlas JSON) |
| "generate a fighter spritesheet" | per-row + preset | `sprite_pipeline.py --preset fighter --per-row` |
| "RPG character walk cycle" | per-row + preset | `sprite_pipeline.py --preset rpg-character --per-row` |
| "sprite from video clip" | video | `video_extract_frames.py` + `video_select_frames.py` + `video_process_frames.py` |

Portrait is the road-to-aew immediate need; spritesheet is the forward-looking capability. Both share one backbone (prompt scaffolding, backend dispatch, bg removal, validation).

## Reference Loading Table

| Signal | Load | Why |
|--------|------|-----|
| picking a style preset | `references/style-presets.md` | 9 era/hardware presets + custom slot |
| `--target road-to-aew` or `--archetype` | `references/wrestler-archetypes.md` | 9 color archetypes + 10 gimmick types + tier |
| sizing `--grid CxR` / `--cell-size` | `references/grid-shapes.md` | allowed dims, direction conventions |
| building a prompt | `references/prompt-rules.md` | ART_STYLE, CHAR_STYLE, GRID_RULES slot contents |
| picking or troubleshooting a backend | `references/backend-chain.md` | Codex CLI invocation pattern + failure modes |
| spritesheet Phase D | `references/frame-detection.md` | connected-components algorithm |
| spritesheet Phase F | `references/anchor-alignment.md` | shared-scale + bottom-anchor math |
| any bg removal phase | `references/bg-removal-local.md` | magenta chroma + rembg |
| Phase H assembly / output shape | `references/output-formats.md` | PNG / GIF / WebP / atlas JSON |
| any phase errors | `references/error-catalog.md` | failure mode → fix mapping |
| user reports clipping / blank cells / cut effects | `references/error-catalog.md` (top section) | "Codex Regeneration as a Post-Processing Fix" failure mode; debug slicer, never raw |
| asset has effects (fire, projectile trails, auras, extended limbs) | `references/error-catalog.md` + use `slice_with_content_awareness` | content extending past cell boundaries needs centroid-ownership extraction. ADR-207 RC-1: on dense grids (`cols * rows >= 16` AND both dims >= 4) `--content-aware-extraction` is silently downgraded to strict-pitch with a warning unless `--effects-asset` is also passed (orchestrator-side) or `effects_asset: True` is set (spec-side). Use `--effects-asset` only for genuine sparse-but-cross-boundary content (fire breath, plasma trails, projectile auras). |
| `--target road-to-aew` deploy | `references/road-to-aew-integration.md` | snake_case, paths, manifest regen |
| `--per-row` subagent orchestration | `references/subagent-delegation.md` | subagent boundary rules: who generates, who composes, who finalizes |
| VFX issues in per-row prompts | `references/vfx-containment.md` | full containment ruleset: allowed/forbidden effects, per-state rules |

Load greedily when a signal matches — references are only read on demand, so the cost is paid once per execution, not once per routing decision.

## Portrait-mode pipeline (5 phases)

| Phase | Script | What |
|-------|--------|------|
| A — Character generation | `sprite_prompt.py build-portrait` + `sprite_generate.py generate-portrait` | Build prompt from style+archetype+description; dispatch backend. |
| B — Background removal | `sprite_process.py remove-bg` | Magenta chroma key (two-pass); rembg fallback if installed. |
| C — Trim and center | `sprite_process.py normalize --mode portrait` | Auto-trim transparent borders; re-canvas with ~5-10% padding; bottom-anchor. |
| D — Dimension validation | `sprite_process.py validate-portrait` | Width ∈ [350, 850], height ∈ [900, 1100], aspect ∈ [1:1.5, 1:2.5]. |
| E — Project-aware deploy | `road_to_aew_integration.py deploy` | Snake_case name, path resolution; `npm run generate:sprites` if `--regen-manifest`. |

End-to-end: `python3 scripts/portrait_pipeline.py --prompt "<desc>" --style <preset> [--target road-to-aew]`.

## Portrait-loop-mode pipeline (5 phases)

| Phase | Script | What |
|-------|--------|------|
| A1 — Prompt build | `sprite_prompt.py build-portrait-loop` | Slot-structured prompt: same character, same pose, same framing, only breath + blink variation across 4 cells. |
| A2 — Backend dispatch | `sprite_generate.py generate-portrait` | Codex CLI call; produces a 1024×1024 PNG with 2×2 cells of 512×512. |
| D — Per-cell extract | inline in `portrait_pipeline.run_portrait_loop` | Naive 2×2 cell crop (cells are well-defined here). |
| E — Per-cell bg removal | `sprite_process.chroma_pass1` + `chroma_pass2_edge_flood` + `alpha_fade_magenta_fringe` + `color_despill_magenta` + `dilate_alpha_zero` | Same despill chain as portrait/spritesheet modes. |
| F — Ground-line anchor | `sprite_process.detect_ground_line` + `apply_ground_line_anchor` | Drift-free: the four near-identical bodies stay perfectly registered across the loop. |
| H — Assembly | inline | PNG sheet, animated GIF (200ms/frame, 800ms loop), animated WebP, per-frame PNGs. |

End-to-end: `python3 scripts/portrait_pipeline.py --mode portrait-loop --display-name "..." --description "..." --style <preset>`.

The loop must be SUBTLE: viewers should barely notice the animation (just feels alive). New poses defeat the purpose — that's spritesheet mode. See `references/prompt-rules.md` for the loop prompt template.

## Spritesheet-mode pipeline (8 phases)

| Phase | Script | What |
|-------|--------|------|
| A — Reference character | `sprite_prompt.py build-character` + `sprite_generate.py generate-character` | 1024x1024 magenta-bg reference PNG. |
| B — Canvas prep | `sprite_canvas.py make-template` | Pillow grid (CxR cells, magenta bg, thin borders). No LLM. |
| C — Spritesheet generation | `sprite_prompt.py build-spritesheet` + `sprite_generate.py generate-spritesheet` | Character + canvas as references; action prompt. |
| D — Frame detection | `sprite_process.py extract-frames` | Connected-components clustering (not naive grid math). See `references/frame-detection.md`. |
| E — Per-frame bg removal | `sprite_process.py remove-bg` | Same chroma engine as portrait mode, looped per frame. |
| F — Normalization & anchor | `sprite_process.py normalize --mode spritesheet` | Shared-scale rescale + bottom-anchor alignment. |
| G — Auto-curation | `sprite_process.py auto-curate` | Deterministic rank: fewest edge-touches → smallest scale variance → lowest seed. |
| H — Final assembly | `sprite_process.py assemble` | PNG sheet, GIF, WebP, per-frame PNGs, Phaser atlas JSON, per-direction strips (4xR / 8xR only). |

End-to-end: `python3 scripts/sprite_pipeline.py --prompt "<desc>" --grid <CxR> --cell-size 256`.

## Per-row generation mode (`--per-row`)

Row-strip generation eliminates the monolithic-sheet failure mode. Instead of one image-generation call for the entire sheet (where frames drift, cross-row contamination occurs, and the slicer misroutes content), each animation row is generated as a separate strip image.

**How it works:**

1. Phase A generates a canonical base character image (identity lock anchor). All subsequent rows receive this base as `--reference` with "match silhouette, face, materials, palette, props exactly" -- prevents cross-row palette shifts, proportion changes, accessory drift.
2. `sprite_canvas.py make-layout-guide` generates per-row reference PNGs (frame boundaries with numbered cells on transparent background), passed as `--reference` alongside the canonical base to prevent frame drift at generation time.
3. Each row gets its own prompt with state-specific action/pose + VFX containment rules (see `references/vfx-containment.md`).
4. Strips are composited into the final sheet after all rows pass QA.

**Retry granularity:** re-generate a single failed row, not the whole sheet. Cost drops from O(sheet) to O(row).

End-to-end: `python3 scripts/sprite_pipeline.py --prompt "<desc>" --preset fighter --per-row`.

## Animation presets (`--preset`)

Named animation presets replace raw `--grid CxR` with semantic state definitions, default frame counts, and per-frame timing.

| Preset | States | Total frames |
|--------|--------|-------------|
| `fighter` | idle(6), dash-right(8), dash-left(8), taunt(4), jump(5), hit-stun(8), charge(6), rush(6), special(6) | 57 |
| `rpg-character` | idle(4), walk-down(4), walk-up(4), walk-left(4), walk-right(4), attack(4), cast(4), hurt(2), death(4) | 34 |
| `platformer` | idle(4), run(8), jump(3), fall(2), attack(4), hurt(2), climb(4), crouch(2), slide(2) | 31 |
| `pet` | idle(6), running-right(8), running-left(8), waving(4), jumping(5), failed(8), waiting(6), running(6), review(6) | 57 |
| `custom` | user-defined via `--states` JSON | variable |

`--preset` expands to `--grid` + per-row metadata + timing arrays. Users say `--preset rpg-character` instead of computing grid dimensions manually.

## Video-to-sprite pipeline

New input modality: extract spritesheet rows from video clips when text prompting fails for complex animations (multi-hit combos, spell effects, motion-captured references).

| Script | What |
|--------|------|
| `video_extract_frames.py` | FFmpeg frame extraction from video clips at configurable FPS |
| `video_select_frames.py` | Select N frames (uniform/manual sampling), assign beat labels (anticipation, contact, follow-through, recovery) |
| `video_process_frames.py` | Background removal, resize to cell-size, ground-line anchor, composite into strip |

Wire via: `--video-rows "0:idle:/path/to/idle.mp4,4:jump:/path/to/jump.mp4"` — row index, state name, video path.

**Dependencies:** FFmpeg (already available), Pillow (already used). No new dependencies.

## Row job manifest

`row_job_status.py` tracks per-row generation status for subagent orchestration.

| Subcommand | What |
|------------|------|
| `init` | Create `row-jobs.json` manifest from preset or `--states` definition |
| `status` | Print per-row status (pending/in-progress/done/failed) |
| `mark` | Update a row's status after generation completes or fails |
| `list-pending` | List rows still needing generation (for subagent dispatch) |

**Subagent boundary rules** (see `references/subagent-delegation.md`):
- Subagent: generates one row strip image, returns path + QA assessment.
- Parent: owns manifest, identity verification, compositing, finalization, packaging.
- Subagents never edit manifests or finalize — single point of control stays with parent.

## QA artifacts (`--qa-artifacts`)

Human-inspectable QA outputs generated alongside verifier JSON when `--qa-artifacts` is passed.

| Artifact | What |
|----------|------|
| Contact sheet | All frames labeled with state names and frame numbers, saved as PNG |
| Preview GIFs | One animated GIF per animation state at intended timing |
| QA report JSON | Per-row metrics: frame count, identity match, effects compliance |

Script: `qa_artifacts.py` generates all three artifact types after assembly.

## Per-frame variable timing

Presets include per-frame millisecond timing arrays instead of uniform timing.

Example (idle): `[280, 110, 110, 140, 140, 320]` ms — longer hold on first/last frame creates natural breathing rhythm.

**Output integration:**
- GIF/WebP output uses per-frame durations via Pillow's `duration` parameter.
- Phaser atlas JSON includes `frameDurations` array and `animationTimings` map.
- Custom timing override via `--timing-json <path>` for fine-tuning.

## Backend (Codex default with Nano Banana fallback, per ADR-198)

Per generation call, evaluated in order:

1. `codex` in `PATH` and `codex --version` exits 0 → use Codex CLI imagegen. Codex CLI 0.125+ no longer exposes `--output-image`/`--aspect-ratio`/`--reference`/`--seed` as direct flags; image generation goes through the agent's internal `image_gen` tool, invoked from prompt text. Canonical invocation: `codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check [-i <ref>... --] "<wrapped prompt>"`. The wrapped prompt instructs the agent to call `image_gen` and save to an absolute path; aspect ratio, seed, and reference semantics are encoded into the prompt text. Reference list (when used) MUST be terminated with `--` before the positional prompt or it consumes the prompt as another image filename. Subprocess timeout: 360s.
2. Else if `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set → fall back to Nano Banana via `nano-banana-builder`'s scripts (`scripts/nano-banana-generate.py with-reference` for reference-guided, `batch` for multi-variant). The skill never imports the Gemini SDK directly — composition through the existing skill is the contract.
3. Else fail loudly with `BackendUnavailableError` listing BOTH fix paths:
   ```
   BackendUnavailableError: No image-generation backend available.

   Fix path 1 (Codex CLI, recommended):
     Install Codex CLI and run `codex auth` to authenticate against your existing subscription.

   Fix path 2 (Nano Banana fallback):
     Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment to enable the Nano Banana fallback.
   ```

Both paths use keys the user already holds (Codex subscription, Gemini API key). There is no third-party billing the toolkit hides. The skill never calls `api.openai.com` directly, `remove.bg`, or any service the user did not authorize. See `references/backend-chain.md` for the locked-in invocation contract and failure modes.

## --max-frames: pack the canvas

One Codex imagegen call produces ONE image. To get N frames, pack as many cells as possible into that one image rather than firing N calls.

`--max-frames` (on `sprite_canvas.py make-template` and `sprite_pipeline.py`) auto-computes the largest square grid that fits `--max-canvas` (default 1024x1024) at the given `--cell-size`:

```bash
# 4x4 = 16 frames at 256px on a 1024 canvas (default)
python3 sprite_pipeline.py --description "knight walk cycle" \
    --style snes-16bit-jrpg --cell-size 256 --max-frames --action walking

# 8x8 = 64 frames at 128px on a 1024 canvas
python3 sprite_pipeline.py --description "tiny adventurer, attack cycle" \
    --style nes-8bit --cell-size 128 --max-frames --action attack-punch

# 16x16 = 256 frames at 64px on a 1024 canvas (extreme density)
python3 sprite_pipeline.py --description "GB-era hero, 4-direction walk" \
    --style gameboy-4color --cell-size 64 --max-frames --action walking
```

`--max-frames` overrides `--grid`; the chosen grid is logged to stderr. See `references/grid-shapes.md` for the cell-size → max-grid → total-frames table at canvas sizes 1024, 1536, and 2048.

## Dimension and cell policy

**Portrait mode** — variable output, validated after trim:
- width 350-850, height 900-1100, aspect 1:1.5 to 1:2.5 (h:w).
- `--force-dimensions` skips the gate (emergency only; logged loudly).

**Spritesheet mode** — fixed cells:
- cell-size in {64, 128, 192, 256, 384, 512}; default 256.
- grid `CxR` via `--grid`; total canvas <= 2048x2048.
- `--grid 4xR` or `--grid 8xR` triggers per-direction strip output.

See `references/grid-shapes.md` for direction-to-row conventions.

## Auto-curation (deterministic)

Default. Applied when `--variants N` > 1.

1. Fewest edge-touch frames wins (sprite touching canvas edge = clipping).
2. Tiebreak: smallest shared-scale variance (visually consistent height across frames).
3. Tiebreak: lowest seed number (reproducible tie resolution).

`--curate` writes a contact sheet and opens a manual review gate. Off by default; interactive gates block automation.

## Shared constraints

- **User-owned keys only.** Codex CLI (default) and Nano Banana via `GEMINI_API_KEY`/`GOOGLE_API_KEY` (fallback) are the two authorized backends — both billed under the user's existing accounts. The skill never calls `api.openai.com` directly, `remove.bg`, or any service the user did not authorize. See ADR-198 and the user-owned-key clause in `docs/PHILOSOPHY.md`.
- **Magenta background (`#FF00FF`)** is the chroma-key default because it never appears in realistic character skin or wrestling gear. Backend prompts include explicit "solid magenta background" instruction; post-processing validates the dominant corner color.
- **Fixed seed per run** for reproducibility. Re-running with the same `--seed` should produce identical output given identical backend output (best-effort: Codex CLI does not currently expose a public seed flag, so the seed travels in the prompt body as a comment).

## Verification

Before shipping any change to this skill, run:

```bash
cd /home/feedgen/vexjoy-agent
python3 scripts/generate-skill-index.py
python3 scripts/validate-references.py --check-do-framing
ruff check . --config pyproject.toml
ruff format --check . --config pyproject.toml
```

Plus the two smoke tests:

```bash
# Portrait (no backend required in dry-run)
python3 skills/game/game-sprite-pipeline/scripts/portrait_pipeline.py \
    --prompt "veteran wrestler, indie circuit, 35yo, scarred face, leather jacket" \
    --style slay-the-spire-painted --target road-to-aew --dry-run

# Spritesheet (no backend required in dry-run; --allow-frame-duplication
# because the synthetic fixture has 4 near-identical figures that trip the
# verify_frames_distinct gate by construction at the new 70% threshold;
# see "Verifier gates" below). Default-on verify; exits 0 on success,
# 2 on gate failure, 3 on --no-verify (ADR-207 Rule 4).
python3 skills/game/game-sprite-pipeline/scripts/sprite_pipeline.py \
    --prompt "wrestler walk cycle, 4 frames" \
    --grid 4x1 --cell-size 256 --dry-run --allow-frame-duplication
```

Both dry-run modes skip the backend call, generate a synthetic fixture, and exercise every post-processing phase. Pass criteria: exit 0, expected output files present, dimension gates satisfied.

## Verifier gates (default-on, ADR-199)

Both pipelines run a verifier suite as the LAST step (after assemble). Default-on; opt out with `--no-verify`.

| Flag | Default | Effect |
|------|---------|--------|
| `--verify` | ON | Run the applicable verifier gate suite after assembly. Print structured JSON to stdout; exit 2 on any failure. |
| `--no-verify` | — | Skip all gates. Logs `WARNING: --no-verify opted out; output not validated` to stderr so silent skips remain visible. **Spritesheet mode (ADR-207 Rule 4)**: returns exit code 3 (`VERIFIER_SKIPPED_EXIT_CODE`) instead of 0 so orchestrators cannot silently mask spritesheet failures with the same exit status as success. **Portrait + portrait-loop modes**: retain exit 0 because their verifier surface is small enough (`verify_no_magenta` only) that an explicit skip is plausibly intentional. |
| `--allow-frame-duplication` | OFF | Relax `verify_frames_distinct` from 70% to 100% duplicate-pct (ADR-208 RC-3). Use for spec-known sheets with legitimate frame repetition: idle loops where 8 frames repeat to fill 64 cells, taunt poses where the character holds a stance, or any animation where >70% duplicate-pct is the artist's intent. Without this flag the gate fires at 70% to catch the layout-drift signature where centroid mis-routing lands most cells on a few near-identical poses. |
| `--effects-asset` | OFF | Opt INTO content-aware routing on a DENSE grid (>= 4x4 with >= 16 cells). Use ONLY for sparse-but-cross-boundary content: fire breath, plasma trails, projectile auras. Keep dense character grids on strict-pitch slicing because content-aware routing can drop cells via centroid drift (ADR-207 RC-1). |

Per-mode gate selection:

| Mode | Entry | Gates |
|------|-------|-------|
| spritesheet | `sprite_pipeline.py run_pipeline` | `verify_no_magenta`, `verify_grid_alignment`, `verify_anchor_consistency`, `verify_frames_have_content`, `verify_frames_distinct`, `verify_pixel_preservation` (when `{name}_sheet_raw.png` is present), `verify_raw_vs_final_cell_parity` (ADR-207 Rule 3 — same precondition as `verify_pixel_preservation`) |
| portrait | `portrait_pipeline.py run_pipeline` (mode=portrait) | `verify_no_magenta` (single-image mode; per-cell gates do not apply) |
| portrait-loop | `portrait_pipeline.py run_portrait_loop` | `verify_no_magenta`, `verify_frames_have_content`, `verify_frames_distinct`, `verify_anchor_consistency` |

Output JSON shape on stdout (last thing the pipeline prints before exit):

```json
{
  "passed": false,
  "verifier_verdict": "FAIL",
  "gates_run": ["verify_no_magenta", "verify_grid_alignment", ...],
  "failures": [{"check": "verify_no_magenta", "file": "...", "details": {...}}],
  "backends_available": {"codex": true, "nano_banana": true},
  "elapsed_seconds": 0.21
}
```

`verifier_verdict` (ADR-207 Rule 2) is the contracted consumer-facing field. Manifest writers, orchestrators, and downstream classifiers MUST derive their own status fields from this string; the toolkit's `write_manifest_record` writer asserts at write time that `verifier_verdict == "PASS"` implies an empty `verifier_failures` list (and vice versa).

Exit codes:
- 0: `passed: true` (or `--no-verify` for portrait / portrait-loop modes).
- 2: at least one gate failed (distinct from generic pipeline error rc=1 so CI can branch on "verifier said no" vs "the pipeline blew up").
- 3: `--no-verify` was passed in spritesheet mode (ADR-207 Rule 4 — `VERIFIER_SKIPPED_EXIT_CODE`). Orchestrators that explicitly want to skip spritesheet verification must explicitly accept exit code 3.

## Logging (ADR-202)

Both pipelines emit diagnostic logs via stdlib `logging` on stderr. Verifier JSON and other structured machine-readable output stays on stdout. Logger name pattern: `sprite-pipeline.<module>` (e.g., `sprite-pipeline.sprite_pipeline`, `sprite-pipeline.sprite_bg`). Default level: INFO.

| Flag | Default | Effect |
|------|---------|--------|
| (none) | — | INFO level. Phase boundaries, backend selection, asset paths, per-phase status. |
| `--quiet` / `-q` | — | WARNING level. Suppresses INFO chatter; only fallback warnings + errors reach stderr. Mutually exclusive with `--verbose`. |
| `--verbose` / `-v` | — | DEBUG level. Adds detailed parameter dumps and intermediate counters. Mutually exclusive with `--quiet`. |

Stream contract: stdout carries structured output (verifier JSON, generated paths); stderr carries diagnostic logs. Redirect them independently (e.g., `python3 sprite_pipeline.py ... 1>out.json 2>logs.txt`).

## Error handling

**Error: "BackendUnavailableError: No image-generation backend available"**
- Cause: Neither `codex` CLI nor `GEMINI_API_KEY`/`GOOGLE_API_KEY` is available.
- Solution: Install Codex CLI (`npm install -g @openai/codex` or per-OS) and run `codex auth`, OR set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in your environment to use the Nano Banana fallback. Both paths use keys the user already holds; pick whichever is available. Never set `OPENAI_API_KEY` for this skill — direct OpenAI calls are not an authorized path.

**Error: "Aspect ratio X outside allowed range [1:1.5, 1:2.5]"**
- Cause: Character rendered too wide (crouched pose) or too tall (full-extension jump pose).
- Solution: Re-generate with a neutral standing prompt. If the character must have an atypical pose, add `--force-dimensions` (logs loudly, should not become routine).

**Error: "Frame count mismatch: detected 6 components, grid expected 8"**
- Cause: Connected-components merged neighboring frames, or small fragments were filtered.
- Solution: Increase cell-size (gives more separation gap), re-generate, or use `--chroma-threshold` to tighten the bg mask. See `references/frame-detection.md`.

**Error: "Codex CLI grid-template input not supported"**
- Cause: Codex imagegen may not consume a magenta grid canvas as a structural input.
- Solution: Skill auto-falls-back to per-frame generation + Pillow compositing. Slower but deterministic.

**Error: "rembg not installed"**
- Cause: `--bg-mode rembg` requested without the opt-in dependency.
- Solution: `pip install rembg onnxruntime` (~200MB ONNX model). Or re-run with default magenta chroma key.

**Error: "road-to-aew directory not found at ~/road-to-aew"**
- Cause: `--target road-to-aew` resolves to a path that does not exist.
- Solution: Pass `--target-dir <explicit-path>` or clone the repo to `~/road-to-aew`. The deploy step refuses to guess.

<!-- no-pair-required: section header; pairs live in subsections -->
## Failure Patterns

### Failure mode: Codex regeneration as a post-processing fix

**What it looks like:** A verifier flags a blank cell, clipped fire, missing silhouette, or any other final-asset defect. The reflex is to re-run `codex exec` to redraw the raw with a different prompt or seed. STOP.

**Why wrong:** Codex generation is treated as ground truth. The raw PNG in `<your-output-dir>/raw/<slug>.png` is what Codex painted, and it is almost always correct. If the final-sheet shows blank cells, clipped effects, or missing silhouettes, the bug is in one of the post-processing steps:
- `slice_grid_cells` derived the wrong pitch (raw_size / grid math) and cut the cell at the wrong place
- `slice_with_content_awareness` claimed a component to the wrong cell (centroid mapping bug)
- The despill chain (`chroma_pass2_edge_flood`, `kill_pink_fringe`, `neutralize_interior_magenta_spill`) ate the silhouette
- The mass-centroid anchor pinned the wrong body part to the ground line
- The LANCZOS resize between magenta padding and content created pink fringe

The user's framing: "the codex generation has never failed, it is working perfectly, the rest has failed."

**Do instead:** Open the raw and the final side-by-side. Confirm the raw has the content (it almost always does). Trace which post-processing step lost it. Specifically for boundary clipping (asset 27 dragon flame, asset 30 plasma trail): set `has_effects: True` and/or `content_aware_extraction: True` in the spec to use `slice_with_content_awareness`, which expands cell windows to recover content extending past conceptual cell boundaries.

**Caveat (ADR-207 RC-1, dense-grid downgrade):** on dense grids (`cols * rows >= 16` AND both dims >= 4 — i.e. 4x4 and denser), the slicer dispatch in `sprite_pipeline.py` and `cmd_extract_frames` silently downgrades `--content-aware-extraction` (and the spec's `content_aware_extraction` / `has_effects` slicer leg) to strict-pitch with a WARNING log because content-aware routing on Codex's fractional-pitch raws drops cells via centroid drift. To opt INTO content-aware on a dense grid for genuine sparse effects assets, also pass `--effects-asset` (orchestrator-side) or set `effects_asset: True` (spec-side). Character grids with arms touching cell edges should stay on the strict slicer and rely on `verify_raw_vs_final_cell_parity` to flag genuine slicing bugs.

See `references/error-catalog.md` for the full diagnostic procedure.

### Failure mode: Calling a third-party paid API the user did not authorize

**What it looks like:** Adding a try/except that falls back from Codex CLI → `api.openai.com` direct / `remove.bg` / any service whose billing relationship the user did not establish.

**Why wrong:** The user-owned-key clause (PHILOSOPHY.md, ADR-198) authorizes fallbacks gated on environment variables the user explicitly set — Codex's auth and `GEMINI_API_KEY`/`GOOGLE_API_KEY` for Nano Banana qualify because the user holds the keys. A fallback that hits a service the toolkit pays for, or that silently charges a card the user never connected, does not. That's the failure mode the Local-First principle exists to prevent.

**Do instead**: Stop at the two authorized backends (Codex CLI, then Nano Banana via user-set Gemini key). When neither is available, raise `BackendUnavailableError` with both fix paths in the message. Adding a third backend requires a new env-var-gated path AND an ADR amendment — never a silent runtime fallback.

### Failure mode: Naive grid-math frame cropping

**What it looks like:** `frame = sheet.crop((col*CELL, row*CELL, (col+1)*CELL, (row+1)*CELL))` for every cell.

**Why wrong:** Generated frames drift within their cells (the model does not respect grid boundaries precisely). Naive cropping captures neighbor-cell pixels and truncates the current sprite.

**Do instead**: Use connected-components clustering (flood-fill from non-magenta pixels, bound each cluster by its actual pixel extent). See `references/frame-detection.md`.

### Failure mode: Trusting the backend's alpha channel

**What it looks like:** Prompting "transparent background" and consuming the output PNG directly.

**Why wrong:** Both Codex CLI and Nano Banana produce backgrounds that are nominally transparent but often have magenta/white/gray fringing, full-opacity backgrounds, or inconsistent alpha. Downstream consumers get dirty assets.

**Do instead**: Always post-process: prompt for a known chroma color (magenta `#FF00FF`), then run local bg removal. Two-pass flood fill handles feathering. `references/bg-removal-local.md` has the algorithm.

### Failure mode: Interactive curation as the default

**What it looks like:** Every pipeline run opens a contact-sheet viewer and waits for user confirmation.

**Why wrong:** Blocks automation (batch generation of 50 wrestlers), adds cognitive load, and prevents reproducibility. The user is not always at the keyboard.

**Do instead**: Deterministic auto-curation is the default (rank by edge-touches → scale variance → seed). Expose `--curate` for cases where the automated pick is visibly wrong. Reproducibility matters more than picking the single prettiest variant.

## Reference files

- `references/style-presets.md` — full catalog of 9 era/hardware presets, prompt fragments, `--style custom` slot.
- `references/wrestler-archetypes.md` — 9 color archetypes, 10 gimmick types, tier modifiers (Act 1/2/3).
- `references/grid-shapes.md` — cell-size table, grid validation, direction-to-row mapping.
- `references/prompt-rules.md` — ART_STYLE, CHAR_STYLE, GRID_RULES slot content; negative prompts.
- `references/backend-chain.md` — Codex CLI invocation pattern, auth checks, failure modes.
- `references/frame-detection.md` — connected-components algorithm, minimum-separation gap, component filter.
- `references/anchor-alignment.md` — shared-scale percentile, bottom-anchor math, horizontal centering.
- `references/bg-removal-local.md` — two-pass chroma, rembg opt-in, failure modes.
- `references/output-formats.md` — PNG / GIF / WebP / atlas JSON / strips matrix per mode.
- `references/error-catalog.md` — error message → cause → fix, per phase.
- `references/road-to-aew-integration.md` — snake_case naming, deploy paths, manifest regen.
- `references/subagent-delegation.md` — subagent boundary rules: who generates, who composes, who finalizes.
- `references/vfx-containment.md` — VFX containment ruleset: allowed/forbidden effects, per-state rules.

## Demo idempotency

Demo orchestrators (e.g. `<your-output-dir>/generate.py`) should be idempotent: running them again on a partial output skips assets whose `assets/<slug>/final.png` (or `final-sheet.png`) AND `meta.json` already exist. This saves ~30-60s per asset of Codex CLI time when iterating. The pattern:

```python
def _is_done(asset_dir: Path) -> bool:
    if not (asset_dir / "meta.json").exists():
        return False
    if (asset_dir / "final.png").exists() or (asset_dir / "final-sheet.png").exists():
        return True
    return False

def run_one(spec, force=False):
    if not force and _is_done(asset_dir):
        return existing_meta  # log "skipping" + return
    ...
```

Provide `--force` to override (re-run all) and `--force-slug <prefix>` to re-run a specific asset. Document the behavior in the orchestrator's docstring so future maintainers don't accidentally regenerate everything.

## Related skills

- `phaser-gamedev` — downstream consumer of spritesheet output (atlas JSON with `frameDurations` and `animationTimings`).
- `threejs-builder` — may consume portrait output for 3D card framing.
- `game-asset-generator` — sibling umbrella for 3D models / textures / matrix-driven pixel art. Its `references/pixel-art-sprites.md` redirects AI-driven sprite work here.
- `game-pipeline` — parent lifecycle orchestrator; slot this skill under its ASSETS phase when building a new game.
- `motion-pipeline` — CPU-only motion data processing; can provide BVH-derived reference frames for video-to-sprite extraction.
