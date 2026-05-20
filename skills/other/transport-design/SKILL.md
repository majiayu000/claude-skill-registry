---
name: transport-design
description: Extract transportation entities from narrative text. Use when analyzing mounts, vehicles, portals, teleporters, airships, spaceships, fast travel systems, and familiars.
---
# transport-design

Domain skill for Transportation Engineer. Specific extraction rules and expertise.

## Domain Expertise

- **Mounts**: Horses, flying mounts, magical creatures, rideable beasts
- **Vehicles**: Cars, ships, aircraft, spacecraft
- **Teleportation**: Portals, teleporters, fast travel systems
- **Mount equipment**: Saddles, armor, gear for mounts
- **Familiars**: Magical companions, summonable creatures
- **Travel mechanics**: Movement speeds, travel time, logistics

## Entity Types (9 total)

- **mount** - Mounts and rideable creatures
- **familiar** - Familiars and summoned companions
- **mount_equipment** - Mount equipment and gear
- **vehicle** - Vehicles and transport technology
- **airship** - Airships
- **spaceship** - Spaceships
- **portal** - Portals and dimensional gates
- **teleporter** - Teleporters and magical transport
- **fast_travel_point** - Fast travel waypoints

## Processing Guidelines

When extracting transportation entities from chapter text:

1. **Identify transportation elements**:
   - Mounts or rideable creatures
   - Vehicles or transport technology
   - Portals, teleporters, or magical gates
   - Fast travel points or waypoints
   - Mount equipment or gear mentioned
   - Familiars or summoned companions

2. **Extract transportation details**:
   - Mount types, speeds, abilities
   - Vehicle types, capacities, fuel/power
   - Portal types and destinations
   - Teleporter locations and costs
   - Mount equipment and upgrades
   - Familiar types and abilities

3. **Analyze transportation context**:
   - Tech level of transportation
   - Magical vs mechanical systems
   - Travel infrastructure quality
   - Accessibility and costs

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Technology level**: Transportation reflects world advancement
- **Magical vs mechanical**: Different systems may coexist
- **Travel time**: Distances and speeds should feel realistic
- **Cost and accessibility**: Not all transport is available to everyone
- **Mount welfare**: Mounts may have care needs
