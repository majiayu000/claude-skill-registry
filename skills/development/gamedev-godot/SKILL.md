---
name: gamedev-godot
description: "Creates Godot games from empty project to exported build. Use when starting, building, validating, or shipping a Godot 2D/3D game or app."
compatibility: Portable core. Works on Claude Code and Codex. Godot engine facts drift between minor versions; verify volatile numbers and renamed APIs against current primary sources.
version: "1.1"
last_validated: 2026-07-11
---

# Godot Game Creation

Use this skill to take a Godot project from empty editor to a published, exported build using the engine, language, and tooling reality of **Godot 4.7** (stable, released 2026-06-18; current as of July 2026). It covers the durable build spine (prototype → first playable → content → export) and fences the volatile engine layer (renderer names, minor-version API renames, physics-engine defaults, C# and web-export caveats) so you teach what is true today, not what was true in Godot 3.

> Version note (verify): **4.7** is current stable (released 2026-06-18), on an active patch cycle — **4.7.1 was at RC2 as of 2026-07-11**, still not stable, fixing real regressions in the 4.7.0 release (editor freezes, a Jolt temp-buffer crash, Android virtual-keyboard bugs) — pin the exact patch level in CI, not just the minor, and re-check whether 4.7.1 has shipped stable before you start a new project. **4.6** (2026-01-26) made **Jolt the default 3D physics engine** — a behavior-changing default when opening a pre-4.6 3D project. **4.7** replaced the old **Asset Library** with a new **Asset Store** (in-editor, threaded browsing, reviews/ratings) — old Asset Library deep links from before 4.6 no longer resolve; point contributors at the new store. **Godot 5.0 has not shipped and has no announced date.**

This is a software/game-development domain skill. It is self-contained: pick the stage you are in, load the one reference for that stage, do the work, verify volatile claims before quoting them.

## Quick Reference

| Stage | Read or Run | Durable default (Godot 4.x, mid-2026) |
|-------|-------------|----------------------------------------|
| **Setup & project** | `references/setup-and-project.md` | One editor install per project via a version manager; commit `project.godot` + source, gitignore `.godot/`; pick **GDScript** unless you have a concrete reason for **C#** (heavier export, no web export for C# without extra setup — verify) |
| **Language & architecture** | `references/gdscript-and-architecture.md` | `class_name` + `@export` + static typing (`var x: int`); **signals up, calls down**; autoload singletons for cross-scene state; `_physics_process` for gameplay, `_process` for visuals |
| **Build the game** | `references/scenes-and-nodes.md` | Compose with **scenes as reusable prefabs**; keep the node tree shallow; instance scenes, don't deep-nest; `CharacterBody2D/3D` + `move_and_slide()`; `TileMapLayer` for 2D grids (the monolithic `TileMap` is deprecated since 4.3 — use the editor's one-click migration); **Jolt** is the default 3D physics engine since 4.6 |
| **Performance & traps** | `references/performance-and-traps.md` | Cache `get_node` results; free with `queue_free()`; use object pools for bullets/particles; profile with the built-in profiler + `--verbose`; avoid per-frame allocations in `_process` |
| **Rendering & platforms** | `references/rendering-and-export.md` | Pick the renderer per target (**Forward+** desktop, **Mobile** for phones, **Compatibility** for web/old GPUs); export needs matching **export templates**; test on-device, not just the editor |
| **Ship & polish** | `references/rendering-and-export.md#shipping` | Export presets per platform; strip debug; sign/notarize per store rules (verify per platform); one-button build via `godot --headless --export-release` in CI |

## Game Creation Workflow

The durable spine. Each step names its verification check inline — do not advance from a state you cannot describe back.

1. **Scope to a testable first playable** → verify: one sentence — "a player controls something, can perform the core verb, and has a reason to keep playing." If you can't write it, stop and get it.
2. **Set up the project and repo** → verify: `project.godot` opens in a pinned editor version; `.godot/` is gitignored; a trivial scene runs with F5. See `references/setup-and-project.md`.
3. **Prototype the core verb in one scene** — placeholder art, `CharacterBody2D/3D`, input map → verify: the core verb works with keyboard/gamepad and reads clearly at real speed. See `references/scenes-and-nodes.md`.
4. **Stand up the architecture skeleton** — autoload for global state, signal wiring (signals up, calls down), a scene-per-concept layout → verify: two scenes communicate via signals/autoload without either holding a hard `get_node("../../..")` path to the other. See `references/gdscript-and-architecture.md`.
5. **Reach First Playable** — the core loop is completable end to end; scene transitions work; pause works → verify: someone else finishes the loop without you explaining the controls.
6. **Content pass** — real art/audio, reusable scene prefabs replace placeholders, `TileMapLayer`/`GridMap` for levels, particles and shaders for feel → verify: frame time stays inside budget on a real target device, not just the editor. See `references/scenes-and-nodes.md` and `references/performance-and-traps.md`.
7. **Harden** — pool spawned objects, free every instanced node, disconnect one-shot signals, validate saved data on load → verify: walk `references/performance-and-traps.md` Known Traps as a checklist; profiler shows no runaway per-frame allocation or leaked nodes.
8. **Export and ship** — set the renderer per target, install matching export templates, configure export presets, strip debug, sign per platform → verify: an exported release build launches and plays on-device; a headless CI export produces the same artifact. See `references/rendering-and-export.md`.

> Verify every volatile fact (renderer names, minor-version API renames, physics-engine defaults, C# export support, web-export threading requirements, store signing rules) against current primary sources before quoting it. Godot changes these across minor releases. Each reference labels volatile facts `as of Godot 4.7, July 2026 — verify`.

## ASCII Flow

```text
Scope -> "first playable" sentence
  -> Project + repo (pinned editor, gitignore .godot/)
  -> Prototype core verb in one scene (CharacterBody + input map)
  -> Architecture skeleton (autoload state + signals up / calls down)
  -> FIRST PLAYABLE (someone else finishes the loop)
  -> Content (scene prefabs, TileMapLayer/GridMap, shaders, audio)
  -> Harden (pool, queue_free, disconnect signals, validate saves)
  -> Export (renderer per target -> export templates -> presets -> sign)
```

## Patterns (durable)

- **Scenes are the unit of reuse.** A scene is a prefab: build a thing once (enemy, pickup, UI panel), save it as a `.tscn`, and instance it. Composition over deep inheritance.
- **Signals up, method calls down.** A parent calls methods on its children; a child emits a signal the parent connects to. This keeps children reusable and prevents fragile `get_node("../../..")` coupling.
- **Autoloads for genuinely global state only.** Singletons (game state, audio manager, scene switcher) via Project Settings → Autoload. Do not turn every manager into a global.
- **`_physics_process` for gameplay, `_process` for visuals.** Physics/movement/collision logic runs at a fixed timestep in `_physics_process(delta)`; camera smoothing and cosmetic updates run in `_process(delta)`. Multiply by `delta`.
- **`move_and_slide()` on `CharacterBody`.** Set `velocity`, call `move_and_slide()`; let the engine resolve collisions. Don't hand-roll integration unless you have a reason.
- **Static typing everywhere.** `var speed: float = 200.0`, typed `@export`, typed function signatures. Enables editor autocomplete, catches errors, and lets the compiler optimize.
- **Signals earn their cost — don't emit in hot loops.** Use signals for state-change events (`died`, `picked_up`); use a direct method call or `get_tree().call_group()` for per-frame / per-instance communication (200 collision checks/frame is not a signal's job).
- **Model pure data as a custom `Resource`, not a Node or Dictionary.** `class_name ItemData extends Resource` with typed `@export`s — inspector-editable, shareable, no scene-tree overhead. The veteran's default for item/ability/stat data.
- **Drop below Nodes when count is the bottleneck.** Nodes wrap the servers; past a few thousand identical instances use `MultiMeshInstance2D/3D` / `RenderingServer` (visuals) or `PhysicsServer` (bulk queries) — but only when the profiler says so.
- **`queue_free()`, never `free()` mid-frame.** Defer node destruction to the end of the frame so you don't invalidate iterators or signals in flight.
- **Pick the renderer for the target, not the prettiest one.** Forward+ is desktop-first; Mobile trades features for phone GPUs; Compatibility (GLES-lineage) is the safe path for web and old hardware.

## Anti-Patterns

- Hard-coding node paths across scene boundaries (`get_node("../../Player")`) instead of signals, exported node references, or an autoload — the top cause of scenes that break when moved.
- Running movement, collision, or timers in `_process` instead of `_physics_process` — behavior then varies with frame rate.
- Forgetting `* delta` on per-frame movement, so speed scales with the player's monitor refresh rate.
- Calling `free()` on a node during signal handling or iteration instead of `queue_free()` — use-after-free crashes.
- Instancing objects every frame (bullets, particles, damage numbers) without pooling — GC/allocation spikes and frame stutter.
- Never disconnecting one-shot or per-instance signal connections — silent leaks as the leftover connection keeps a freed context referenced.
- Assuming C# and GDScript have identical export support — as of Godot 4.7 (July 2026) **C# has no web/WASM export in stable** (a prototype was demoed but not shipped). For any web target, use GDScript. Re-verify, but do not promise a C# web build.
- Shipping without matching **export templates** installed for the editor version → export fails or produces a broken binary.
- Shipping **`CSGShape` geometry** as final level meshes — CSG is documented as prototyping-only; bake to static meshes before release.
- Quoting a renderer name, API signature, physics default, or export caveat from Godot 3 or an older 4.x minor without re-verifying — several were renamed or re-defaulted across 4.x (e.g. Jolt became the default 3D physics engine in 4.6).

## Known Traps

- **Frame-rate-dependent logic** — anything in `_process` that moves or times gameplay drifts across machines; use `_physics_process` and always multiply by `delta`.
- **`TileMap` → `TileMapLayer` migration** — the monolithic `TileMap` node was **deprecated in 4.3** (present but frozen — no new features) in favor of per-layer `TileMapLayer` nodes; code and scenes from older tutorials will not match. Use the editor's one-click conversion tool rather than hand-porting.
- **Jolt-as-default silent change** — since **4.6** new 3D projects use **Jolt** physics by default; a pre-4.6 project upgraded in place can behave differently with no code change. Re-test physics after an upgrade, or pin the engine explicitly.
- **`@onready` ordering** — `@onready var x = $Child` resolves when the node enters the tree (after `_init()`, before `_ready()`); referencing it in `_init()` returns null.
- **C# / web export** — as of 4.7 (July 2026) C# web export is **not supported in stable**; do not promise a web build for a C# game. Re-verify per release, but treat GDScript as the web path.
- **Export templates version-lock** — templates must match the exact editor version **including patch level** (4.7 is on an active patch cycle); a mismatch fails silently or ships a broken build. Pin the exact patch in CI and reinstall templates on every upgrade.
- **Shader compilation stutter** — Godot compiles shader variants lazily on first use, so effects hitch the first time they appear (worst on Android). Pre-warm materials on a loading screen (hidden `SubViewport`), persist the shader cache, and test on the real target where the editor's pre-cache doesn't hide it. See `references/rendering-and-shaders.md`.
- **`.res`/`ResourceSaver` save-file RCE** — loading a user-modifiable `.tres`/`.res` can execute arbitrary GDScript via resource deserialization. Use `FileAccess` + JSON (or `ConfigFile`) for save data, never `ResourceSaver` for user-shared files. See `references/rendering-and-export.md`.
- **Editor ≠ device** — the editor runs on your desktop GPU with the editor renderer, often with shaders pre-cached; a phone or web target has different capabilities. Test an actual exported build on the real target before shipping.
- **`.godot/` in git** — committing the generated `.godot/` cache causes churn and merge pain; gitignore it and commit only `project.godot` + source + assets.

## Frameworks & tooling (Godot 4.7, July 2026 status — verify before adopting)

| Need | Pick | Status |
|------|------|--------|
| Primary language | **GDScript** (typed) | First-class, fastest iteration, full web export; typed Dictionaries (`Dictionary[K,V]`) since 4.4 |
| Performance-critical / .NET ecosystem | **C#** (.NET) | First-class but heavier; **no web export in stable** as of 4.7 — GDScript for web targets |
| Native performance modules | **GDExtension** (C/C++/Rust via godot-cpp / gdext) | Stable ABI for compiled extensions; verify binding maturity |
| 3D physics | **Jolt** (built-in) | **Default for new 3D projects since 4.6**; Godot Physics still selectable |
| 2D tilemaps | **TileMapLayer** (per-layer) | Current node; the monolithic `TileMap` is deprecated since 4.3 |
| Dependency/asset sharing | **Asset Store** (renamed from Asset Library in 4.7) + git submodules | In-editor store with reviews/versioning; vet third-party addons for version fit |
| Console export | **Third-party middleware only** (e.g. W4 Games) | Godot has no official console export — MIT/open-source licensing conflicts with console NDAs; budget for a middleware partner and its own cert timeline if a console SKU is planned |
| CI export | **`godot --headless --export-release`** | Scriptable headless export; needs version-matched templates on the runner |

## When Godot Is the Wrong Choice

Recommending Godot by default is itself a judgment call, not a rule — push back when the project profile doesn't fit:

- **A console SKU is the primary target, not a stretch goal.** Godot has no official console export (open-source licensing conflicts with console NDAs); you're committing to a third-party middleware vendor (e.g. W4 Games) as a second dependency with its own pricing, support SLA, and version lag behind Godot's own releases. If PS5/Xbox/Switch is launch-day, weigh that against Unity's or Unreal's direct console pipelines before committing.
- **The team already has deep Unity or Unreal expertise and no Godot experience**, and the timeline doesn't afford a learning-curve tax — re-platforming mid-project is expensive; the switching cost usually isn't worth it for its own sake.
- **AAA-fidelity 3D rendering is the product** (film-quality GI, Nanite-style virtualized geometry, large open-world streaming). Godot's renderer is credible for stylized and mid-scope 3D, but it doesn't have Unreal's Lumen/Nanite-class pipeline; don't promise that fidelity on Godot.
- **The genre leans on a mature, licensed middleware ecosystem** (large-scale multiplayer backends, advanced physics/destruction, certain anti-cheat or ad-mediation SDKs) that ships Unity/Unreal plugins first and Godot support late or not at all — check the specific vendor before assuming parity.
- **The team needs a large in-house animation/rigging pipeline** matching Unity's Mecanim or Unreal's Control Rig maturity — Godot's `AnimationTree`/`AnimationPlayer` cover most 2D/indie-3D needs but are thinner for complex character-animation production pipelines.
- Godot remains a strong default for 2D, stylized/mid-scope 3D, rapid prototyping, jam games, and teams that value an open-source, royalty-free engine with fast iteration — the above are reasons to *check* fit, not a blanket "avoid Godot."

## Navigation

Resources:

- [references/setup-and-project.md](references/setup-and-project.md) — Editor versioning, project structure, repo hygiene, input maps, and GDScript-vs-C# choice
- [references/gdscript-and-architecture.md](references/gdscript-and-architecture.md) — Typed GDScript, signals (and when direct calls / `call_group` beat them), autoloads, `_process` vs `_physics_process`, custom `Resource` data modeling, `@tool`, `_notification` lifecycle, and node-communication patterns
- [references/scenes-and-nodes.md](references/scenes-and-nodes.md) — Scene composition vs inheritance, node tree design, `CharacterBody`, Jolt physics default, TileMapLayer/GridMap, and instancing
- [references/performance-and-traps.md](references/performance-and-traps.md) — CPU/GPU profiling, the drop-below-Nodes escape hatch (`MultiMesh`/servers), object pooling, node/signal lifecycle, and the full Known Traps catalog with fixes
- [references/rendering-and-shaders.md](references/rendering-and-shaders.md) — Shader compilation stutter and mitigation, lighting/GI strategy (LightmapGI/SDFGI/VoxelGI), `WorldEnvironment`, and `SubViewport` techniques
- [references/rendering-and-export.md](references/rendering-and-export.md) — Renderer choice, export templates and gotchas, save systems (and the `.res` security trap), high-level multiplayer, per-platform presets, and shipping/signing
- [data/sources.json](data/sources.json) — Primary sources to verify volatile facts against

Related skills (same family only):

- [../software-mobile/SKILL.md](../software-mobile/SKILL.md) — Mobile-platform constraints and store flows
- [../software-performance/SKILL.md](../software-performance/SKILL.md) — General performance profiling discipline
- [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) — Onboarding and flow design that transfers to game UX
- [../gamedev-roblox/SKILL.md](../gamedev-roblox/SKILL.md) — Sibling game-creation skill for the Roblox platform

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

## Fact-Checking

- Godot 4.x engine facts drift between **minor versions**. Treat renderer names, node renames (e.g. `TileMap` → `TileMapLayer`), API signatures, C# export support, and web-export requirements as volatile and verify against current primary sources (docs.godotengine.org, godotengine.org/blog, the GitHub release notes) before quoting.
- The references separate **DURABLE** principles (scene composition, signals up / calls down, physics-vs-process, typed GDScript) from **VOLATILE** facts (renderer names, renamed nodes, export caveats) and date the volatile ones `as of mid-2026`.
- Features announced on the roadmap but not confirmed shipped (verify against the milestone) are marked as such — confirm shipping status before depending on them.
- If web access is unavailable, state the limitation and mark any volatile engine claim as unverified rather than asserting it as current.
