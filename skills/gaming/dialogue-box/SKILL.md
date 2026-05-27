---
name: dialogue-box
description: Implement dialogue UI (typewriter + advance) for touch/keyboard
compatibility: opencode
---
# Skill: Dialogue Box UI

## Objective
Implement a reusable dialogue box for NPC and object interactions.

## Steps
1) Create `DialogueBox.tscn` (Control):
- panel/background
- label for text
- optional continue icon

2) Implement `DialogueBox.gd`:
- `show_text(text: String)`
- typewriter reveal with configurable speed
- confirm to: reveal instantly if mid-type; otherwise advance/close

3) Add a simple `DialogueManager`:
- queues lines
- blocks player input while visible

## Verification
- NPC interaction displays multi-line dialogue.
- Dialogue can be advanced quickly.
- Works with touch and keyboard.
