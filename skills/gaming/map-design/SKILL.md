---
name: map-design
description: Roblox map design patterns for different game genres including simulators, tycoons, obbies, tower defense, and open world. Covers hub/lobby design, terrain, paths, areas, and visual flow.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Map Design Patterns

## Quick Reference Links

**Official Documentation:**
- [Parts Overview](https://create.roblox.com/docs/parts) - Basic building blocks
- [Terrain](https://create.roblox.com/docs/environment/terrain) - Terrain editor
- [Lighting](https://create.roblox.com/docs/environment/lighting) - Atmosphere

**DevForum Tutorials:**
- [Ruski's Tutorial #1 - Map Layout Design](https://devforum.roblox.com/t/ruskis-tutorial-1-how-to-design-a-map-layout/277853)
- [Ruski's Tutorial #5 - Open World Maps](https://devforum.roblox.com/t/ruskis-tutorial-5-how-to-design-an-open-world-map/3554962)
- [How to Make a Simulator Map](https://devforum.roblox.com/t/how-to-make-a-simulator-map-part-1/1343396)

**Creator Store Resources:**
- [Tycoon Layout](https://create.roblox.com/store/asset/518672699/Tycoon-Layout-Updated)
- [Tycoon Map](https://create.roblox.com/store/asset/12061074643/Tycoon-Map)

---

## Pre-Design Planning

Before opening Studio, answer these questions:

| Question | Impact |
|----------|--------|
| **Genre** | Determines flow - FPS needs fluidity, simulators need areas, obbies need progression |
| **Theme** | Setting, time period, colors, materials |
| **Player Count** | Scale and density - 6v6 is compact, 32+ needs large maps |
| **Detail Level** | Low-poly vs realistic, color palette, lighting |
| **Shape** | Avoid boxy - use curves, horseshoes, organic layouts |

**Real-World Inspiration:** Go outside and observe how roads curve, trees cluster, buildings have wear, nothing is perfectly uniform.

---

## Map Layout Principles

### Visual Flow
- **Players should ALWAYS see something interesting** - never empty walls or dead space
- Use landmarks for navigation (tall buildings, unique structures, colored areas)
- Create sight lines that guide players toward objectives

### Risk & Reward
- Dead ends offer safety but vulnerability to ambush
- Open areas are dangerous but fast to traverse
- Elevated positions offer advantage but exposure

### Organization
- Group elements systematically (Terrain, Buildings, Props, NPCs)
- Name parts descriptively
- Use folders for areas (Spawn, Shop, Arena)

---

## Genre-Specific Patterns

### Why Lobbies Exist

| Purpose | Description |
|---------|-------------|
| **Waiting Room** | Round-based games need a place for players while match runs |
| **Teleportation Hub** | Central point with portals to different game areas/places |
| **Social & Trading** | Low-stress area to show off, trade, chat without danger |
| **Monetization** | Primary location for shops, crate openings, leaderboards |

### Standard Lobby Features

**Players expect these specific features:**

1. **Lobby Obby** - Simple obstacle course in corner to entertain waiting players
2. **Voting Pads** - Colored floor squares to vote for next map (3-4 options)
3. **Global Leaderboards** - Boards showing top players (Most Wins, Most Cash)
4. **Daily Reward Chest** - Physical chest/circle for daily login bonus
5. **Shop/Crates** - Purchase area with spinning/opening animations
6. **Spawn Platform** - Clear central spawn point

### Simulator Hub/Lobby

The central spawn area where players access shops, collections, and features.

**Layout Structure:**
```
+------------------+
|     TERRAIN      |  <- Hills, trees (background)
|  +----+  +----+  |
|  |SHOP|  |SHOP|  |  <- Shop stalls
|  +----+  +----+  |
|                  |
|    [DISPLAYS]    |  <- Pet/item displays
|                  |
|  +----+  +----+  |
|  |AREA|  |AREA|  |  <- Feature areas
|  +----+  +----+  |
|     [SPAWN]      |  <- Center spawn
+------------------+
```

**Key Elements:**
- Central spawn platform (highlighted, often stone/marble)
- Shop stalls with striped awnings (red/white, blue/white)
- Display pedestals for pets/items
- Clear paths (different color/material than grass)
- Surrounding hills with trees (visual boundary)
- Multiple NPC vendors
- Sign posts (SALE!, NEW!, etc.)

**Color Zones:**
- Spawn area: Stone/marble (neutral)
- Grass areas: Bright green, lime green
- Paths: Brown/nougat (dirt)
- Borders: Orange, different material
- Shops: Colored awnings for identification

**Stud Style (Classic Roblox):**
```lua
-- All parts get studs
part.Material = Enum.Material.Plastic
part.TopSurface = Enum.SurfaceType.Studs
part.BottomSurface = Enum.SurfaceType.Inlet
part.FrontSurface = Enum.SurfaceType.Studs
part.BackSurface = Enum.SurfaceType.Studs
part.LeftSurface = Enum.SurfaceType.Studs
part.RightSurface = Enum.SurfaceType.Studs
```

### Tycoon Layout

Individual player plots with droppers, conveyors, and collectors.

**Standard Flow:**
```
[DROPPER] -> [CONVEYOR] -> [UPGRADER] -> [CONVEYOR] -> [COLLECTOR]
     |                                                      |
     v                                                      v
  Spawns                                               Converts
  "bricks"                                            to money
```

**Plot Layout:**
```
+----------------------------------+
|  [BUY BUTTONS]                   |
|      |                           |
|  [DROPPER 1] -> [CONV] -> [UPG]  |
|  [DROPPER 2] -> [CONV] ->        |
|  [DROPPER 3] -> [CONV] ----+     |
|                            |     |
|             [COLLECTOR] <--+     |
|                                  |
|  [EXPANSION AREA...]             |
+----------------------------------+
```

**Key Components:**
- Buy buttons (color-coded, tiered pricing)
- Droppers (spawn parts)
- Conveyors (transport parts)
- Upgraders (multiply part value)
- Collectors (convert to currency)
- Clear boundaries between plots
- Expansion areas for progression

**Production Line Design:**
Example: Donut Tycoon
1. Dropper: Spawns dough
2. Upgrader 1: Shapes into donut
3. Upgrader 2: Cooks/fries
4. Upgrader 3: Adds sprinkles
5. Collector: Sells completed donut

### Obby Layout

Linear or tower progression with checkpoints.

**Linear Obby:**
```
[SPAWN] -> [STAGE 1] -> [CHECKPOINT] -> [STAGE 2] -> ... -> [WIN]
```

**Tower Obby:**
```
    [WIN]
      |
  [STAGE 10]
      |
  [STAGE 9]
      |
    ...
      |
  [STAGE 1]
      |
   [SPAWN]
```

**Design Principles:**
- Clear start and end points
- Checkpoints every 3-5 stages
- Difficulty curve (easy -> hard)
- Visual variety (don't repeat same obstacle)
- Safe zones between challenges
- Kill bricks clearly colored (red, lava material)

**Obstacle Variety:**
- Platform jumps (varying distances)
- Moving platforms
- Spinning obstacles
- Thin balance beams
- Disappearing platforms
- Wall jumps
- Trampolines/launchers

**Tower of Hell Style:**
- Randomly generated stages
- Each stage is a Model with set dimensions
- Stages stack vertically
- Rising lava for tension
- Time limit per tower

### Themed Obby with Hub

Complete obby games combine a hub/lobby area with the obby course. This pattern is common for dragon obbies, adventure obbies, and similar games.

**Full Layout:**
```
+------------------------------------------+
|                  HUB AREA                |
|  +------+  +------+  +------+  +------+  |
|  |SHOP 1|  |SHOP 2|  |SHOP 3|  |SHOP 4|  |
|  +------+  +------+  +------+  +------+  |
|                                          |
|  [DISPLAYS]    [SPAWN]    [LEADERBOARD]  |
|                                          |
|  [LOBBY OBBY]         [DAILY CHEST]      |
|                                          |
|  [VOTING PADS]        [STATUE/DECOR]     |
|                                          |
|            +----------+                  |
|            |   GATE   |                  |
|            +----------+                  |
+------------------------------------------+
              |
              v
+------------------------------------------+
|               OBBY COURSE                |
|  [STAGE 1] -> [STAGE 2] -> ... -> [WIN]  |
+------------------------------------------+
```

**Gate/Transition Pattern:**
```lua
local function createGate(position, name, parent)
    local gate = Instance.new("Model")
    gate.Name = name

    -- Gate posts
    createPart(Vector3.new(3, 15, 3), CFrame.new(position + Vector3.new(-8, 7.5, 0)),
        BrickColor.new("Dark stone grey"), "PostL", gate)
    createPart(Vector3.new(3, 15, 3), CFrame.new(position + Vector3.new(8, 7.5, 0)),
        BrickColor.new("Dark stone grey"), "PostR", gate)

    -- Gate arch
    createPart(Vector3.new(19, 3, 3), CFrame.new(position + Vector3.new(0, 16.5, 0)),
        BrickColor.new("Dark stone grey"), "Arch", gate)

    -- Decorative caps
    createPart(Vector3.new(4, 2, 4), CFrame.new(position + Vector3.new(-8, 15.5, 0)),
        BrickColor.new("Medium stone grey"), "CapL", gate)
    createPart(Vector3.new(4, 2, 4), CFrame.new(position + Vector3.new(8, 15.5, 0)),
        BrickColor.new("Medium stone grey"), "CapR", gate)

    gate.Parent = parent
    return gate
end
```

**Winner Area Pattern:**
The final area rewards players who complete the obby with visual celebration.

```lua
local function createWinnerArea(position, theme, parent)
    local area = Instance.new("Model")
    area.Name = "WinnerArea"

    -- Victory platform (larger, special material)
    createPart(Vector3.new(30, 2, 30), CFrame.new(position + Vector3.new(0, 1, 0)),
        BrickColor.new("Bright yellow"), "VictoryPlatform", area)

    -- Treasure displays
    for i = 1, 4 do
        local angle = (i / 4) * math.pi * 2
        local treasurePos = position + Vector3.new(math.cos(angle) * 10, 2, math.sin(angle) * 10)
        createPedestal(treasurePos, area)

        -- Gold pile on pedestal
        createPart(Vector3.new(2, 1, 2), CFrame.new(treasurePos + Vector3.new(0, 3.5, 0)),
            BrickColor.new("Bright yellow"), "Treasure" .. i, area)
    end

    -- Central victory statue/decoration
    -- (Theme-specific: dragon, trophy, etc.)

    area.Parent = parent
    return area
end
```

**Themed Decorations (Dragon Example):**
```lua
-- Dragon eggs on pedestals
local function createDragonEgg(position, color, parent)
    local egg = Instance.new("Part")
    egg.Shape = Enum.PartType.Ball
    egg.Size = Vector3.new(2, 3, 2)
    egg.CFrame = CFrame.new(position)
    egg.Anchored = true
    egg.BrickColor = color
    egg.Material = Enum.Material.Plastic
    -- Apply studs to egg
    egg.TopSurface = Enum.SurfaceType.Studs
    egg.BottomSurface = Enum.SurfaceType.Inlet
    egg.Parent = parent
    return egg
end

-- Treasure piles
local function createTreasure(position, parent)
    local treasure = Instance.new("Model")
    treasure.Name = "Treasure"

    -- Gold bars (stacked)
    for y = 0, 2 do
        for x = -1, 1 do
            createPart(Vector3.new(1, 0.5, 2),
                CFrame.new(position + Vector3.new(x * 1.2, y * 0.5 + 0.25, 0)),
                BrickColor.new("Bright yellow"), "Gold", treasure)
        end
    end

    -- Gems scattered on top
    local gemColors = {"Bright red", "Bright blue", "Bright green", "Bright violet"}
    for i = 1, 4 do
        createPart(Vector3.new(0.5, 0.5, 0.5),
            CFrame.new(position + Vector3.new((math.random() - 0.5) * 2, 1.5, (math.random() - 0.5) * 2)),
            BrickColor.new(gemColors[i]), "Gem" .. i, treasure)
    end

    treasure.Parent = parent
    return treasure
end
```

### Tower Defense Layout

Enemy paths with tower placement zones.

**Path Design:**
```
[SPAWN] --+
          |
    +-----+-----+
    |     |     |
    +--+  |  +--+    <- Winding path
       |  |  |
    +--+--+--+--+
    |           |
    +-----+-----+
          |
       [EXIT]
```

**Key Elements:**
- Clear enemy path (highlighted material)
- Tower placement zones (grid squares, off-path)
- Multiple spawn points (later waves)
- Path intersections (strategic chokepoints)
- Visual lane indicators
- Upgrade stations/shops

**Placement Grid:**
```lua
-- Tower placement uses grid system
local GRID_SIZE = 4  -- 4x4 studs per cell
local function snapToGrid(position)
    return Vector3.new(
        math.round(position.X / GRID_SIZE) * GRID_SIZE,
        position.Y,
        math.round(position.Z / GRID_SIZE) * GRID_SIZE
    )
end
```

### Open World Map

Non-linear exploration with landmarks and regions.

**Region Layout:**
```
+--------+--------+--------+
| FOREST | PLAINS | DESERT |
+--------+--------+--------+
| SWAMP  | [HUB]  | BEACH  |
+--------+--------+--------+
| CAVES  | RIVER  | MOUNT  |
+--------+--------+--------+
```

**Design Principles:**
- Distinct biomes/regions
- Landmarks visible from distance
- Paths connect regions (natural flow)
- Points of interest in each area
- Central hub for fast travel
- Difficulty zones (easier near spawn)

**Navigation Aids:**
- Tall landmarks (towers, mountains, trees)
- Unique color palettes per region
- Map/minimap UI
- Path markers
- NPC guides

---

## Terrain Building

### Layered Hills (Stud Style)
```lua
local function createHill(position, baseSize, height, parent)
    local layers = math.ceil(height / 3)
    for i = 1, layers do
        local size = baseSize - (i - 1) * 4
        if size > 2 then
            createPart(
                Vector3.new(size, 3, size),
                CFrame.new(position + Vector3.new(0, (i-1) * 3 + 1.5, 0)),
                i % 2 == 1 and BrickColor.new("Bright green") or BrickColor.new("Lime green"),
                "HillLayer" .. i,
                parent
            )
        end
    end
end
```

### Trees (Stacked Blocks)
```lua
local function createTree(position, height, parent)
    -- Trunk
    createPart(
        Vector3.new(2, height, 2),
        CFrame.new(position + Vector3.new(0, height/2, 0)),
        BrickColor.new("Reddish brown"),
        "Trunk",
        parent
    )
    -- Leaves (stacked, shrinking)
    local leafY = height
    for i, size in ipairs({8, 6, 4}) do
        createPart(
            Vector3.new(size, 3, size),
            CFrame.new(position + Vector3.new(0, leafY + i * 3, 0)),
            BrickColor.new("Bright green"),
            "Leaves" .. i,
            parent
        )
    end
end
```

### Paths
```lua
local function createPath(startPos, endPos, width, parent)
    local direction = endPos - startPos
    local length = direction.Magnitude
    local midPoint = startPos + direction / 2
    local angle = math.atan2(direction.X, direction.Z)

    createPart(
        Vector3.new(width, 0.5, length),
        CFrame.new(midPoint) * CFrame.Angles(0, angle, 0),
        BrickColor.new("Nougat"),
        "Path",
        parent
    )
end
```

---

## Shop Stalls

### Striped Awning Shop
```lua
local function createShop(position, name, color1, color2, parent)
    local shop = Instance.new("Model")
    shop.Name = name

    -- Counter
    createPart(Vector3.new(10, 4, 6), CFrame.new(position + Vector3.new(0, 2, 0)),
        BrickColor.new("Brown"), "Counter", shop)

    -- Back wall
    createPart(Vector3.new(10, 8, 1), CFrame.new(position + Vector3.new(0, 6, 3)),
        BrickColor.new("Bright orange"), "Wall", shop)

    -- Pillars
    createPart(Vector3.new(1, 10, 1), CFrame.new(position + Vector3.new(-5, 5, -2)),
        BrickColor.new("Medium stone grey"), "PillarL", shop)
    createPart(Vector3.new(1, 10, 1), CFrame.new(position + Vector3.new(5, 5, -2)),
        BrickColor.new("Medium stone grey"), "PillarR", shop)

    -- Striped awning
    for i = 0, 4 do
        createPart(
            Vector3.new(2, 0.5, 5),
            CFrame.new(position + Vector3.new(-4 + i*2, 10, 0)) * CFrame.Angles(math.rad(-15), 0, 0),
            i % 2 == 0 and color1 or color2,
            "Awning" .. i,
            shop
        )
    end

    shop.Parent = parent
    return shop
end
```

---

## Display Pedestals

```lua
local function createPedestal(position, parent)
    local pedestal = Instance.new("Model")
    pedestal.Name = "Pedestal"

    -- Tiered base
    createPart(Vector3.new(5, 1, 5), CFrame.new(position + Vector3.new(0, 0.5, 0)),
        BrickColor.new("Medium stone grey"), "Base1", pedestal)
    createPart(Vector3.new(4, 1, 4), CFrame.new(position + Vector3.new(0, 1.5, 0)),
        BrickColor.new("Dark stone grey"), "Base2", pedestal)
    createPart(Vector3.new(3, 1, 3), CFrame.new(position + Vector3.new(0, 2.5, 0)),
        BrickColor.new("Medium stone grey"), "Base3", pedestal)

    pedestal.Parent = parent
    return pedestal
end
```

---

## Color Palettes by Theme

### Simulator/Pet Game
| Element | Color |
|---------|-------|
| Grass | Bright green, Lime green |
| Paths | Nougat, Brown |
| Shops | Bright orange, Deep orange |
| Stone | Medium stone grey |
| Accents | Bright red, Bright blue |

### Tycoon
| Element | Color |
|---------|-------|
| Plot floor | Bright green |
| Conveyors | Black, Dark grey |
| Buy buttons | Bright green (cheap), Bright yellow (mid), Bright red (expensive) |
| Droppers | Material-specific |

### Fantasy/Dragon
| Element | Color |
|---------|-------|
| Grass | Earth green, Forest green |
| Stone | Dark stone grey |
| Dragon scales | Bright red, Bright blue, Bright violet |
| Gold/Treasure | Bright yellow |
| Fire | Bright orange, Bright red |

### Ice/Winter
| Element | Color |
|---------|-------|
| Ground | White, Institutional white |
| Ice | Cyan, Medium blue |
| Accents | Bright blue |
| Trees | White (snow-covered) |

---

## Checklist for Map Design

**Pre-Build:**
- [ ] Defined genre and theme
- [ ] Sketched layout (paper or digital)
- [ ] Identified key areas/zones
- [ ] Planned player flow

**Hub/Lobby:**
- [ ] Clear spawn point
- [ ] Visible shop stalls
- [ ] Display areas for collectibles
- [ ] Paths connecting areas
- [ ] Visual boundaries (hills, fences)
- [ ] NPC vendors placed

**Visual Polish:**
- [ ] No empty walls or dead space
- [ ] Landmarks for navigation
- [ ] Consistent color palette
- [ ] Lighting appropriate to theme
- [ ] Studs on all surfaces (if classic style)

**Gameplay:**
- [ ] Player can easily find objectives
- [ ] Risk/reward areas
- [ ] Clear boundaries
- [ ] Playtested for flow

---

## Hub Building Order

1. **Ground** - Base terrain, color zones
2. **Paths** - Connect areas, define flow
3. **Major structures** - Shops, buildings
4. **Terrain features** - Hills, water
5. **Trees/vegetation** - Background fill
6. **Props** - Pedestals, fences, signs
7. **NPCs** - Vendors, guides
8. **Displays** - Pets, items on pedestals
9. **Lighting** - PointLights, atmosphere
10. **Polish** - Signs, details, particles
