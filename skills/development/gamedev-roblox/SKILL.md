---
name: gamedev-roblox
description: "Creates Roblox experiences from empty Studio place to published world. Use when starting, building, validating, or shipping a Roblox game."
compatibility: Portable core. Works on Claude Code and Codex. Roblox platform facts are dated and drift; verify volatile numbers against current primary sources.
version: "1.1"
last_validated: 2026-07-11
---

# Roblox World Creation

Use this skill to take a Roblox experience from empty Studio place to a published, retainable world using the engine, language, and platform reality of **July 2026**. It covers the durable build spine (greybox → first playable → detail → ship) and fences the volatile platform layer (rates, limits, renamed APIs) so you teach what is true today, not what was true in 2023 — or in May 2026 (the RFY discovery algorithm, DataStore budget model, and 2D UGC publishing rules all materially changed since then; see the dated corrections in `references/discovery-economy-policy.md` and `references/luau-and-architecture.md`).

This is a software/game-development domain skill. It is self-contained: pick the stage you are in, load the one reference for that stage, do the work, verify volatile claims before quoting them.

## Quick Reference

| Stage | Read or Run | Durable default (Jul 2026) |
|-------|-------------|----------------------------|
| **Setup & toolchain** | `references/setup-and-toolchain.md` | Studio + **Rojo + Rokit + Wally** for git-native teams; **Script Sync** (Full Release since Jun 2026, Team-Create compatible) if you need Team Create; `default.project.json` defines the DataModel tree |
| **Language & architecture** | `references/luau-and-architecture.md` | `--!strict` Luau; **`task.wait/spawn/defer`** never `wait()/spawn()`; server-authoritative; RemoteEvent + `UnreliableRemoteEvent` for high-frequency; **ProfileStore** for player data |
| **Build the world** | `references/world-building.md` | Greybox in Parts first; 1 stud ≈ 0.28 m; `StreamingEnabled = true`; **Unified Lighting** `LightingStyle = Realistic` + `PrioritizeLightingQuality` (the old `Technology` enum is deprecated) |
| **Performance & traps** | `references/performance-and-traps.md` | Anchor static parts; transparency `0` or `1` only; disconnect every connection; `UpdateAsync` + session lock + `BindToClose`; `WaitForChild` in LocalScripts |
| **Discovery, economy, policy** | `references/discovery-economy-policy.md` | Design for RFY's 28-day, 3-phase retention model (Day 1 / Day 2–7 / Day 8–28; rewritten Jun 2026 — the old 7-day qPTR model is superseded); complete the **maturity questionnaire**; design sinks for every source; never trust the client for economy |
| **AI-assisted creation** | `references/setup-and-toolchain.md#ai-assisted-creation` | Studio **Assistant** (planning mode), **Material Generator** (GA), **Code Assist**, Studio **MCP server** for external LLMs — real and shipping; Texture Generator still Beta |

## World Creation Workflow

The durable spine. Each step names its verification check inline — do not advance from a state you cannot describe back.

1. **Scope the world to a testable first playable** → verify: one sentence — "a player spawns, can perform the core verb, and has a reason to return tomorrow." If you can't write it, stop and get it.
2. **Set up the toolchain and place structure** → verify: `rojo serve` (or Script Sync) round-trips an edit Studio ↔ disk; `default.project.json` maps `src/` to the right services. See `references/setup-and-toolchain.md`.
3. **Greybox the world in Parts only** — no meshes, textures, or scripts → verify: you can walk the whole space, sightlines and player flow read clearly at player scale (1 stud ≈ 0.28 m). See `references/world-building.md`.
4. **Stand up the architecture skeleton** — server-authoritative state, one RemoteEvent path, ProfileStore-backed save, CollectionService tags for repeated objects → verify: a value changed on the server replicates; a value changed only on a client does **not** (FilteringEnabled is permanently on). See `references/luau-and-architecture.md`.
5. **Reach First Playable** — working spawn/respawn, one lighting pass, the core loop is playable end to end → verify: Team Test with a second client; the loop is completable without programmer intervention.
6. **Detail pass** — modular kits replace greybox, PBR/SurfaceAppearance, atmosphere, sound zones → verify: part count and draw calls still inside budget on a real low-end Android, not just the Studio emulator. See `references/world-building.md` and `references/performance-and-traps.md`.
7. **Harden** — rate-limit and type-validate every `OnServerEvent`; serialize economy remotes; disconnect every connection; `BindToClose` save; session locking on data → verify: walk `references/performance-and-traps.md` Known Traps as a checklist; MicroProfiler shows no runaway frame peaks.
8. **Soft-launch under real concurrency** — release to a capped audience (private server, limited region, or throttled ad spend) before wide release → verify: watch real per-server-instance CPU and experience-wide DataStore budget (shared across all servers since the 2026 per-experience model) with 50–200 concurrent players, not a 2–4-client Studio Team Test — the burst-join DataStore exhaustion, physics-step cost, and remote flood only appear at real concurrency. Fix what surfaces before RFY sends volume.
9. **Ship and tune for discovery** — complete the maturity questionnaire (mandatory), set access and game settings, publish, then design the FTUE and loops around the RFY signals → verify: experience is rated (since Sep 30 2025 an **unrated experience is fully unplayable platform-wide** for users — not merely hidden; you can still playtest it unrated in Studio); first-session core-loop comprehension is real. See `references/discovery-economy-policy.md`.

> Verify every volatile number (part/draw budgets, DataStore limits, DevEx rates, fees, maturity ages) against current primary sources before quoting it. The platform changes these without warning. Each reference labels volatile facts `as of Jul 2026 — verify`.

## ASCII Flow

```text
Scope -> "first playable" sentence
  -> Toolchain + place structure (Rojo/Script Sync + default.project.json)
  -> Greybox in Parts (validate scale + flow)
  -> Architecture skeleton (server-authority + ProfileStore + tags)
  -> FIRST PLAYABLE (Team Test the core loop)
  -> Detail (modular kits, Unified Lighting, PBR, sound)
  -> Harden (validate + serialize remotes, disconnect leaks, BindToClose, session lock)
  -> Soft-launch (capped audience -> watch CPU + DataStore budget at real concurrency)
  -> Ship (maturity questionnaire -> publish -> FTUE + loops for RFY signals)
```

## Patterns (durable)

- **Server is the single source of truth.** Clients request; the server decides. FilteringEnabled cannot be turned off — design as if every client is hostile.
- **`task` library, always.** `task.wait/spawn/delay/defer` and `signal:Once()`. The legacy `wait()/spawn()/delay()` globals are deprecated and drift under load.
- **Set properties before parenting.** `Instance.new("Part")`, configure, then set `.Parent` last — one replication event, not several.
- **Stream the world.** `StreamingEnabled = true`; access Workspace objects from LocalScripts via `WaitForChild(name, timeout)`; keep `ReplicatedStorage`/`ReplicatedFirst` lean (they never stream).
- **Atomic, session-locked saves.** `UpdateAsync` (never `SetAsync` for shared keys) + a session lock keyed on `game.JobId` + `BindToClose` + ProfileStore. Save on cadence and on critical events, not on every stat change.
- **One script for many things.** CollectionService tags + a single manager script for repeated objects (doors, spawns, traps), not a Script per instance.
- **Client does pixels, server does truth — but "truth" means adversarial state, not everything.** Validate what a cheater profits from (currency, damage, hit-reg, item grants); leave non-adversarial state (camera shake, footstep particles, ragdoll poses) client-authoritative. Over-validating cosmetic state burns server CPU for zero security benefit. See `references/luau-and-architecture.md`.
- **Network ownership is the physics-feel lever.** `part:SetNetworkOwner(player)` makes their own vehicle/tool physics simulate locally (lag-free); `SetNetworkOwner(nil)` forces server ownership for contested/exploitable physics. This — not RemoteEvents — is why "my car lags for the driver."
- **Serialize economy remotes.** Two fires of a spend/grant remote can land in one frame before the first write commits (the dupe race). Process economy-affecting remotes through a per-player serial queue, not independent handlers.
- **Design for retention signals, not raw volume.** RFY (rewritten Jun 2026) scores Day 1, Day 2–7, and Day 8–28 separately and deliberately ignores lifetime totals — a strong new experience can outrank a large declining one, but a strong first session with no mid-game hook now shows up as a visible Day-8–28 weakness instead of being averaged away.
- **Every currency/item source needs a sink.** Before shipping a new way to earn, decide what removes it from the economy — otherwise you get inflation and an economy that only rewards early adopters. See `references/discovery-economy-policy.md#economy-design-judgment-sinks-sources-and-exploit-economics`.
- **Roblox isn't always the right call.** Sexual/gambling content, full payment-stack control, frame-perfect competitive netcode, non-Roblox-client distribution, and adult-first products fit poorly on this platform — recognize the mismatch before scoping the build. See `references/discovery-economy-policy.md#when-roblox-is-the-wrong-platform`.

## Anti-Patterns

- Changing currency, health, or inventory in a LocalScript and expecting the server (or other players) to see it.
- Trusting numeric arguments from `OnServerEvent` for economy or stat changes instead of computing on authoritative server state.
- `SetAsync` on a shared key from multiple servers (race → data loss); no `BindToClose` (lose the last autosave on shutdown).
- Partial transparency (`0.01`–`0.99`) or `RenderFidelity = Precise` on background geometry; unanchored static parts; per-instance Scripts where one tagged manager would do.
- Connecting events per-respawn without disconnecting (the most common silent memory leak); busy-wait `while ... do wait() end` loops.
- Setting the deprecated `Lighting.Technology` enum in a new project instead of `LightingStyle` + `PrioritizeLightingQuality`.
- Shipping unrated (skipping the maturity questionnaire) → **fully unplayable platform-wide** for users since Sep 30 2025 (stronger than the old "hidden from search" penalty), and absent from top charts.
- Quoting a DevEx rate, fee, part budget, or DataStore limit from memory without re-verifying — every one of these has changed and is dated in the references.

## Known Traps

- **`wait()` drift** — legacy scheduler resumes on ~1/30s minimum and accumulates drift; use `task.wait`.
- **Replication timing** — a Workspace object that exists on the server may not have replicated/streamed to a given client yet; LocalScripts must `WaitForChild` with a timeout.
- **Humanoid race** — `Humanoid`/`HumanoidRootPart` are not all present the instant `CharacterAdded` fires; `:WaitForChild` them.
- **DataStore throttling** — request/storage budget is now per-*experience* (2026 change), shared across every running server, not per-server; a burst on one server can starve all of them. Wrap in `pcall` + logging; use ProfileStore.
- **`RemoteFunction:InvokeClient()` from the server** — a malicious client can yield forever and hang the thread; never call it.
- **Emulator ≠ device** — Studio's device emulator tests layout only, not CPU/GPU; most players are mobile, so test on a real 3–4 year old Android before shipping.
- **New Type Solver footguns (2026)** — the current type solver has open issues (as of mid-2026 — verify fixed): stale `Parent`/`Model` type narrowing after reparenting or reassignment, and high Studio memory use. If strict-typed code reports impossible type errors after moving instances, suspect the solver, not your code.
- **Script Sync edge cases (2026)** — even post-full-release, Script Sync has reported "ghost instances" in Team Create and silently skips scripts nested under non-Folder/non-Script ancestors. Confirm every script actually round-trips; don't assume a clean sync.

## Frameworks (Jul 2026 status — verify before adopting)

| Need | Pick | Status |
|------|------|--------|
| Player data persistence | **ProfileStore** | Active community standard; successor to ProfileService (deprecated) |
| Tag/component architecture | **CollectionService** (optionally **Stamp** wrapper) | Built-in; idiomatic |
| Typed networking | **Jolt** (community) or **ByteNet** | Emerging community options; no official typed networking API yet; verify package activity before adopting |
| ECS | **Matter** (`matter-ecs`) | **Dormant** — no confirmed 2026 activity on the canonical or community-fork repos; do not adopt for new production ECS without independent confirmation of maintenance |
| Module framework | Modular OOP, or ECS if needed | **Knit is no longer maintained** — do not start new projects on it |
| Build automation / CI | **Lune** + **Wally** + **Rokit** | Git-native production stack |

## Navigation

Resources:

- [references/setup-and-toolchain.md](references/setup-and-toolchain.md) — Studio, Rojo/Script Sync/Azul, Rokit/Wally/Lune, project structure, and AI-assisted creation
- [references/luau-and-architecture.md](references/luau-and-architecture.md) — Luau 2026 (strict types, task, native, buffer), client-server model, network ownership, client-vs-server authority judgment, remotes + anti-exploit (dupe races, speed hacks), data persistence (ProfileStore lease traps, DataStore budget bursts, schema migration), Parallel Luau/Actors, MessagingService, module patterns
- [references/world-building.md](references/world-building.md) — Scale, greyboxing, modular kits, Unified Lighting, terrain/mesh/PBR, sound, streaming, publishing and testing
- [references/performance-and-traps.md](references/performance-and-traps.md) — Performance budgets, profiling, memory-leak patterns, and the full Known Traps catalog with fixes
- [references/discovery-economy-policy.md](references/discovery-economy-policy.md) — RFY discovery signals, monetization mix, retention/FTUE design, content maturity and safety policy, UGC economy
- [data/sources.json](data/sources.json) — Primary sources to verify volatile facts against

Related skills (same family only):

- [../software-mobile/SKILL.md](../software-mobile/SKILL.md) — Mobile-platform constraints and store flows
- [../software-performance/SKILL.md](../software-performance/SKILL.md) — General performance profiling discipline
- [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) — Onboarding and flow design that transfers to FTUE

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

## Fact-Checking

- Roblox platform facts are **high-drift**. Treat every rate, fee, percentage, numeric limit, maturity age, and recently renamed API as volatile and verify against current primary sources (create.roblox.com, devforum.roblox.com, luau.org, about.roblox.com) before quoting.
- The references separate **DURABLE** principles (build order, server authority, save discipline) from **VOLATILE** facts (budgets, rates, API names) and date the volatile ones `as of Jul 2026`.
- Items announced on the roadmap but not confirmed shipped (e.g. CSG-on-meshes, enhanced voxel terrain, Android native codegen) are marked as such — confirm shipping status before depending on them.
- If web access is unavailable, state the limitation and mark any volatile platform claim as unverified rather than asserting it as current.
