---
name: technical-systems
description: Safety-net catch-all for extracting technical game entities not covered by other skills. Covers 193 entity types across achievements, inventory, audio, visual, cinematic, events, progression, research, media, secrets, art, and transport systems.
---
# technical-systems

Domain skill for Technical Director. Specific extraction rules and expertise.

## Domain Expertise

- **Achievement systems**: Unlockables, progression rewards
- **Inventory/item systems**: Items, crafting, equipment
- **Audio/visual**: Music, effects, shaders, lighting
- **Cinematics**: Cutscenes, camera work, transitions
- **Transportation**: Mounts, vehicles, fast travel
- **Legendary items**: Rare, powerful, cursed equipment
- **Biology & astronomy**: Life cycles, celestial bodies
- **Architecture**: City layouts, districts
- **Player analytics**: Metrics, heatmaps, data tracking

## Entity Types (193 total)

Catch-all for all remaining technical entities including:

- **Achievement Systems**: achievement, trophy, badge, title, rank, leaderboard
- **Inventory & Items**: item, inventory, crafting_recipe, material, component, blueprint
- **Content Organization**: map, image, tag, template
- **Creative Tools**: inspiration, note
- **Interactive Systems**: choice, flowchart, handout, tokenboard
- **Audio Systems**: music_track, music_theme, motif, score, sound_effect, ambient
- **Visual Systems**: visual_effect, particle, shader, lighting, color_palette
- **Cinematic Systems**: cutscene, cinematic, camera_path, transition, fade
- **Events & Disasters**: world_event, seasonal_event, invasion, plague, famine, war
- **Progression & Save**: fast_travel_point, waypoint, save_point, checkpoint
- **Research & Education**: research, academy, university, school, library
- **Media & Communication**: newspaper, radio, television, internet, social_media, propaganda
- **Secrets & Puzzles**: secret_area, hidden_path, easter_egg, puzzle, trap
- **Art & Culture**: festival, celebration, ceremony, concert, exhibition
- **Transport & Travel**: mount, familiar, mount_equipment, vehicle, spaceship, portal

## Processing Guidelines

When extracting technical entities from chapter text:

1. **Identify all remaining entity types**:
   - Items mentioned (weapons, armor, consumables)
   - Achievements or rewards referenced
   - Audio/visual cues (music, lighting, effects)
   - Transportation (mounts, vehicles, travel points)
   - Legendary items or artifacts
   - Technical systems (UI, save points, checkpoints)

2. **Extract all remaining details**:
   - Item stats, crafting recipes, enchantments
   - Achievement criteria, rewards
   - Audio tracks, visual effects, shaders
   - Cinematic moments, camera movements
   - Transportation types and abilities
   - Legendary item properties and legends

3. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Completeness**: You are safety net—don't miss entities
- **Consistency**: Maintain schema consistency with other subagents
- **Quality**: Even technical entities need rich details
- **Integration**: Technical entities link to narrative/gameplay elements
