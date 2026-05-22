---
name: playtesting
description: Headed playtesting workflow for Godot projects, focused on HPV runs with MCP, runtime eval teleporting, and efficient logging. Use when you need to validate quest flow, UI playability, or record HPV findings in PLAYTESTING_ROADMAP.md.
---

# Playtesting HPV Skill

Use this skill to run headed playability validation (HPV) quickly with MCP while keeping calls and tokens low. Teleport-assisted flow is the default unless a full walk is requested.

## Minimal Workflow
1. Run project headed (MCP).
2. Get runtime scene structure once.
3. Identify the active scene root (world or location).
4. Teleport to target, interact, and advance dialogue with batched inputs.
5. Verify state (DialogueBox text, marker visibility, flags).
6. Log findings in PLAYTESTING_ROADMAP.md.

## Efficiency Rules (Core)
- Batch inputs with 400-800 ms waits, then verify once.
- Cache node paths early; avoid repeated scene tree dumps.
- Gate actions on state checks (DialogueBox visible, marker visible, flags).
 - Prefer teleporting to targets unless a full walk is required.

## Teleport Pattern (Expression-Only)
Use method calls in eval (no var or assignment). Examples:

- Find world by name when available:
  get_tree().root.find_child("World", true, false)

- Teleport the player (replace WORLD_INDEX if needed):
  get_tree().root.get_child(WORLD_INDEX).get_node("Player").set_global_position(Vector2(384, 64))

- Trigger a quest area:
  get_tree().root.get_child(WORLD_INDEX).get_node("QuestTriggers/Quest10")._on_body_entered(get_tree().root.get_child(WORLD_INDEX).get_node("Player"))

- Read dialogue text:
  get_tree().root.get_child(WORLD_INDEX).get_node("UI/DialogueBox/Panel/Text").text

## Logging Checklist
- Scope (quest range, shortcuts used, minigames skipped or not)
- What worked and what failed
- Any blockers and repro steps
- Next steps for the next playtester

## In This Repo
- Log in docs/playtesting/PLAYTESTING_ROADMAP.md
- HPV uses MCP or manual playthrough; avoid headless tests for playability
- Minigames are typically skipped unless explicitly requested
