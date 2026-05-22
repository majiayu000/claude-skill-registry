---
name: e2e-tests-gut
description: End-to-end tests in Godot using GUT (Godot 4.5)
compatibility: opencode
---
# Skill: Add headless tests (GUT)

## Objective
Add automated tests that validate the playable slice without manual play.

## Recommended tests
- Smoke: boot `Main.tscn` and assert no errors
- Scene routing: load an area, transition through a door, assert spawn works
- Battle: start a battle, select a command, assert HP changes

## CLI
`godot --headless --path . --script res://addons/gut/gut_cmdln.gd -gconfig=.gutconfig.json`
