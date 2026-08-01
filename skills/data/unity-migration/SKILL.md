---
name: unity-migration
description: 'Migrate a browser-based JavaScript/Canvas game to Unity (C#). Use for
  Shelter 2250 (or similar) when you need: (1) Unity project setup decisions (2D/URP/input/UI),
  (2) mapping existing JS classes/syst'
---

---
name: unity-migration
description: Migrate a browser-based JavaScript/Canvas game to Unity (C#). Use for Shelter 2250 (or similar) when you need: (1) Unity project setup decisions (2D/URP/input/UI), (2) mapping existing JS classes/systems to Unity architecture, (3) porting core simulation loops (time/resources/rooms/dwellers/save), and (4) planning incremental milestones with parity checks.
---

# Unity Migration (Shelter 2250)

## 0) Inputs to confirm (ask if missing)

- Target Unity version (recommend latest LTS)
- Render/UI approach: `UGUI` (Canvas) vs `UI Toolkit` (or hybrid)
- 2D pipeline: built-in 2D vs `URP 2D`
- Target platforms: WebGL/PC/Mobile
- Parity target: “feature parity first” vs “re-architecture first”

## 1) Migration strategy (keep risk low)

1. Create a new Unity project and commit it early.
2. Port **data + simulation** first (no fancy visuals): resources, time, room placement rules, dwellers, save/load.
3. Add a minimal debug UI (text HUD + simple buttons).
4. Only then port visuals (room rendering, animations, VFX).
5. Keep a running parity checklist (JS build vs Unity build).

## 2) Mapping guide (read only if needed)

- For a concrete mapping of the current JS codebase to Unity scripts/components, read `references/js-to-unity-map.md`.

## 3) Unity architecture (recommended baseline)

- **Scene**: `Boot` (init, load/save), `Game` (world), `UI` (HUD/menus) or single `Game` scene + additive `UI`.
- **Game loop**:
  - Render: per-frame (`Update`)
  - Simulation tick: fixed step (e.g., 1 sec real-time) using a `GameTickService`
  - “Game time” scale: multiplier (1/2/6x) applied consistently to tick + clock
- **Data**:
  - Room types / costs: `ScriptableObject` (`RoomTypeDefinition`)
  - Traits: `ScriptableObject` (`TraitDefinition`)
  - Country bonuses: `ScriptableObject` (`CountryDefinition`)
- **State**:
  - `GameState` plain C# object (serializable)
  - `SaveService` writes JSON to disk (PC) and PlayerPrefs/WebGL fallback

## 4) Incremental milestones (suggested)

1. “Simulation only”: tick + resources + rooms + dwellers + save/load (no graphics)
2. “Build mode”: placement preview + validation + costs + upgrade
3. “UI parity”: resource bars + dwellers panel + room modal
4. “Visual parity”: 2D cutaway rendering, lighting, animations
5. “Content”: events, exploration, country-specific flavor

## 5) Parity checks (fast)

- Room placement rule tests: given grid + rooms, validate allowed positions
- Tick consistency: at 1x/2x/6x, 60 seconds real-time should advance:
  - 1x: 1 in-game hour
  - 2x: 2 in-game hours
  - 6x: 6 in-game hours
- Save/load: load legacy saves (if required) and new saves

