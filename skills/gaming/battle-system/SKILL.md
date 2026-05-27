---
name: battle-system
description: Implement classic turn-based battle scene (top HUD + bottom commands)
compatibility: opencode
---
# Skill: Turn-based battle system

## Objective
Implement a minimal but correct classic JRPG battle loop:
- show battle scene with pre-rendered background
- show party/enemy status in a top HUD
- allow selecting a command for the current actor
- execute a single turn and advance

## Steps

1) Create battle scene
- `game/scenes/battle/BattleScene.tscn`
  - background renderer
  - battler sprite anchors (party and enemy)
  - BattleHUD (top)
  - CommandMenu (bottom)

2) Implement battle state machine
- `game/scripts/battle/battle_controller.gd`
  - states: Start, CommandSelect, ResolveTurn, End

3) Data models (minimal)
- CharacterData, EnemyData, SkillData, ItemData

4) Integration
- Exploration encounter triggers transition to BattleScene
- On battle end, return to exploration at a defined spawn

## Verification
- Can win a battle and return to exploration
- UI updates HP correctly
- Deterministic outcomes when seeded
