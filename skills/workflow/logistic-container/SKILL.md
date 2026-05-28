---
name: logistic-container
description: "Factorio-style logistics — items flow automatically between containers"
license: MIT
tier: 2
allowed-tools: [read_file, write_file]
protocol: LOGISTIC-CONTAINER
related: [room, container, prototype]
tags: [moollm, logistics, inventory, automation, factorio, containers]
---

# Logistic Container Skill

> "The factory grows. Items flow. The world runs itself."

## Overview

The Logistic Container skill brings Factorio-style logistics to MOOLLM adventures. Containers participate in a network where items flow automatically between providers and requesters.

## The Five Box Types

Like Factorio's colored logistic chests:

| Mode | Color | Emoji | Behavior |
|------|-------|-------|----------|
| **passive-provider** | Yellow | 📦🟡 | "Take from me if you need" |
| **active-provider** | Red | 📦🔴 | "I'm pushing these OUT" |
| **requester** | Blue | 📦🔵 | "I WANT these items" |
| **storage** | White | 📦⬜ | "General overflow" |
| **buffer** | Green | 📦🟢 | "Hold until condition met" |

## Grid Storage

Containers can manage grids of cells, each holding one item type:

```
warehouse/
  LOGISTIC-CONTAINER.yml    # The config
  iron-ore/                 # Auto-created
    CELL.yml                # count: 2500
  copper-ore/
    CELL.yml                # count: 1800
  magic-sword/
    CELL.yml                # instances: [{...}, {...}]
```

### Auto-Creation

When you toss a new item type into a grid container, a new cell directory is created automatically. Like `mkdir -p` for items!

```yaml
grid:
  enabled: true
  auto_create_cells: true
  cell_naming: item-id        # iron-ore/ from iron-ore item
```

## Fungible vs Instance Items

### Fungible (Just Count)

Identical items — store as a count:

```yaml
# 500 iron ore, all the same
{ item: "iron-ore", count: 500 }
```

Tags that trigger fungible mode:
- `raw-material`, `currency`, `ammo`, `commodity`, `stackable`

### Instance (Keep State)

Items with individual properties — store as array:

```yaml
# 3 swords, each different
{ item: "magic-sword", count: 3, instances: [
    { id: "sword-001", durability: 85, enchant: "fire" },
    { id: "sword-002", durability: 100, enchant: null },
    { id: "sword-003", durability: 50, enchant: "ice" }
]}
```

Tags that trigger instance mode:
- `unique`, `named`, `enchanted`, `damaged`, `configured`

## Examples

### Pantry (Passive Provider)

```yaml
logistic-container:
  id: pantry
  name: "Kitchen Pantry"
  mode: passive-provider
  
  provides:
    - tags: ["food", "ingredient"]
    
  reserve: 1    # Always keep 1 of each
  
  filters:
    allow: [{ tags: ["food"] }]
```

### Factory Output (Active Provider)

```yaml
logistic-container:
  id: assembly-output
  name: "Assembly Line Output"
  mode: active-provider
  
  push_to:
    - match: { tags: ["finished"] }
      destination: "../warehouse/"
    - match: { tags: ["scrap"] }
      destination: "../recycling/"
    - default: "../overflow/"
```

### Workbench (Requester)

```yaml
logistic-container:
  id: workbench
  name: "Crafting Workbench"
  mode: requester
  
  request_list:
    - item: "iron-plate"
      count: 20
      min: 5          # Request more when below 5
    - tags: ["fuel"]
      count: 10
```

### Warehouse (Grid + Provider)

```yaml
logistic-container:
  id: main-warehouse
  name: "Central Warehouse"
  mode: passive-provider
  
  grid:
    enabled: true
    auto_create_cells: true
    stack_limit: 10000
    navigable: true       # Players can walk between cells
    
  item_handling:
    default_mode: auto
    fungible_tags: ["ore", "ingot", "plate"]
    instance_tags: ["weapon", "armor"]
```

### Loading Dock (Buffer)

```yaml
logistic-container:
  id: dock
  name: "Ship Loading Dock"
  mode: buffer
  
  buffer_for:
    - destination: "../ship/cargo/"
      when: "world.ship.docked == true"
```

## Network Participation

Containers only exchange items with others in the same network:

```yaml
network: factory-a        # Only connects to factory-a

# Or multiple networks:
network: [factory, emergency]
```

## Signals (Circuit Network)

Emit signals about contents for automation:

```yaml
signals:
  enabled: true
  emit:
    - signal: "iron-count"
      value: "count of iron-plate"
    - signal: "is-full"
      value: "total_items >= capacity"
```

Other objects can read these signals:

```yaml
# Door that only opens when warehouse has iron
exit:
  signal_control:
    open_when:
      signal: "iron-count"
      operator: ">"
      value: 100
```

## Logistics Bots

Characters with `behavior.type: logistic-bot` move items between containers:

```yaml
character:
  id: courier-kitten
  behavior:
    type: logistic-bot
    roboport: warehouse/#charging-station
    cargo_slots: 5
    range: 10
```

Bots:
1. Find active providers or pending requests
2. Pick up items
3. Deliver to requesters or push destinations
4. Return to roboport when idle

## Integration with Exits

Exits can have flow for automatic item transport:

```yaml
exit:
  direction: EAST
  destination: ../warehouse/
  flow:
    enabled: true
    allow: [{ tags: ["finished"] }]
```

This creates a "conveyor belt" between rooms!

## Related Skills

- **container** — Simpler container without logistics
- **exit** — Exits with flow behavior
- **character** — Logistic bot characters
- **object** — Inserters and assemblers
- **postal** — Message-based logistics

## Design Document

See [factorio-logistics-protocol.md](../../designs/factorio-logistics-protocol.md) for the full design.
