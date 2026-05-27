---
name: cloverhollow-town
description: Build Cloverhollow town exterior + key building entrances (3D low-poly)
compatibility: opencode
---
# Skill: Build Cloverhollow Town (3D)

## Objective
Create a small, readable 3D town area that supports:
- exploration
- multiple building entrances
- early NPC interactions
- at least one visible enemy encounter for battle testing

## Minimum structures
- Fae's House entrance
- School entrance
- Arcade entrance
- Park landmark

## Steps
1) Create `game/scenes/areas/cloverhollow/Area_Cloverhollow_Town.tscn`
- Low-poly ground + a few buildings (placeholders ok)
- Collisions on walls/props
- Navigation surface (NavMesh) suitable for deterministic movement

2) Place interactables
- 2 NPCs
- 1 sign
- 1 container

3) Place at least one visible enemy actor
- Put it in a predictable location to support Scenario Runner tests

## Verification
- Player can traverse without getting stuck
- Doors route to target interior scenes with correct spawn markers
- Interactions and battle trigger are reachable and deterministic
