---
name: building-construction
description: Provides patterns for building detailed structures programmatically using Parts and CSG. Use when creating buildings, towers, vehicles, or any brick-by-brick constructions in code.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Building & Construction Patterns

---

## MANDATORY: Stud Material Initialization

> **CRITICAL:** This code block MUST be included at the START of every building script. No exceptions. Always load stud materials BEFORE creating any parts.

```lua
--------------------------------------------------------------------------------
-- MANDATORY INITIALIZATION - COPY THIS BLOCK FIRST
--------------------------------------------------------------------------------

local Workspace = game:GetService("Workspace")
local AssetService = game:GetService("AssetService")
local MaterialService = game:GetService("MaterialService")

-- Stud material configuration
local STUD_ASSET_ID = 13719188279  -- 2022 Stud MaterialVariant
local studMaterialName = ""
local studBaseMaterial = Enum.Material.Plastic

-- Load stud materials (MUST run before creating parts)
local function loadStudMaterials()
    -- Check if already loaded in MaterialService
    for _, item in ipairs(MaterialService:GetChildren()) do
        if item:IsA("MaterialVariant") then
            studMaterialName = item.Name
            studBaseMaterial = item.BaseMaterial
            print("[Studs] Found existing: " .. studMaterialName)
            return true
        end
    end

    -- Load via AssetService
    local success, err = pcall(function()
        local asset = AssetService:LoadAssetAsync(STUD_ASSET_ID)
        if asset then
            local matVariant = asset:FindFirstChildWhichIsA("MaterialVariant", true)
            if matVariant then
                matVariant.Parent = MaterialService
                studMaterialName = matVariant.Name
                studBaseMaterial = matVariant.BaseMaterial
                print("[Studs] Loaded: " .. studMaterialName .. " (BaseMaterial: " .. tostring(studBaseMaterial) .. ")")
            end
            asset:Destroy()
        end
    end)

    if not success then
        warn("[Studs] FAILED to load: " .. tostring(err))
        return false
    end

    return studMaterialName ~= ""
end

-- EXECUTE IMMEDIATELY
local studsLoaded = loadStudMaterials()
if not studsLoaded then
    warn("[Studs] Running without stud materials - parts will be smooth plastic")
end

--------------------------------------------------------------------------------
-- STANDARD PART CREATION FUNCTION (Uses loaded stud materials)
--------------------------------------------------------------------------------

local function createPart(size, cframe, color, name, parent)
    local part = Instance.new("Part")
    part.Size = size
    part.CFrame = cframe
    part.Anchored = true
    part.BrickColor = color

    -- Apply stud material (if loaded)
    if studMaterialName ~= "" then
        part.Material = studBaseMaterial
        part.MaterialVariant = studMaterialName
    else
        part.Material = Enum.Material.Plastic
    end

    -- NEVER use legacy studs (causes Z-fighting)
    part.TopSurface = Enum.SurfaceType.Smooth
    part.BottomSurface = Enum.SurfaceType.Smooth

    part.Name = name or "Part"
    part.Parent = parent
    return part
end

--------------------------------------------------------------------------------
-- YOUR CODE STARTS HERE (use createPart function above)
--------------------------------------------------------------------------------
```

### Why This Is Mandatory

| Issue | Legacy SurfaceType.Studs | MaterialVariant (This Pattern) |
|-------|-------------------------|-------------------------------|
| Z-Fighting | YES - 3D geometry overlaps | NO - flat PBR texture |
| Performance | Worse - extra geometry | Better - texture only |
| Future-proof | NO - deprecated 2018 | YES - modern standard |
| Visual Quality | Inconsistent | High quality PBR |

### Critical Rules

1. **ALWAYS load materials BEFORE creating parts**
2. **ALWAYS use `createPart()` function, never raw Part creation**
3. **NEVER use `SurfaceType.Studs`** - causes Z-fighting
4. **ALWAYS set surfaces to `Smooth`** - MaterialVariant handles appearance
5. **part.Material MUST match studBaseMaterial** - or variant won't apply

---

## Quick Reference Links

**Official Documentation:**
- [Parts Overview](https://create.roblox.com/docs/parts)
- [MaterialVariant API](https://create.roblox.com/docs/reference/engine/classes/MaterialVariant)
- [MaterialService API](https://create.roblox.com/docs/reference/engine/classes/MaterialService)
- [AssetService API](https://create.roblox.com/docs/reference/engine/classes/AssetService)
- [Part API](https://create.roblox.com/docs/reference/engine/classes/Part)
- [CFrame API](https://create.roblox.com/docs/reference/engine/datatypes/CFrame)

**Community Resources:**
- Asset ID `13719188279` - 2022 Stud MaterialVariant (RECOMMENDED)
- Asset ID `18987102498` - Full 2008-2024 Studs pack
- [Resurface Plugin](https://create.roblox.com/store/asset/5765511674) - For existing builds

---

## Performance Optimization (Community Consensus)

### Part Count Guidelines
- **Optimal**: Under 5,000 parts in render distance
- **Per Building**: 100-600 parts (no interior)
- **Warning**: 9,000+ parts = noticeable fps drops

### Critical Rules
- **ALWAYS anchor static parts** - moving parts = lag
- **Disable CanCollide + CanTouch** on decorative parts
- **Avoid Unions** - bad topology, breaks instancing
- **Reuse designs** - vary with scale/color/rotation instead of unique parts
- **Enable Streaming** in Workspace for large maps

### MeshPart Settings (If Using Meshes)
| RenderFidelity | Use For |
|----------------|---------|
| Performance | Decorative, distant objects |
| Automatic | Interactive items |
| Precise | Major landmarks only |

| CollisionFidelity | Use For |
|-------------------|---------|
| Box | Walkthrough objects, tiny items |
| Hull | Trees, varied shapes |
| Default | Terrain, complex structures |

---

## Layer System (Avoid Z-Fighting)

> **IMPORTANT:** Never place parts with surfaces at exactly the same Y position. Use a layer system.

```lua
-- Define layer heights (build from bottom up)
local LAYERS = {
    GROUND = 0,           -- Base ground level
    PLATFORM = 2,         -- Platforms ON TOP of ground (not overlapping)
    SPAWN = 4,            -- Spawn platforms above main platforms
    DECORATION = 5,       -- Decorations on platforms
}

-- Ground: 2 thick centered at Y=0, top surface at Y=1
local GROUND_TOP = LAYERS.GROUND + 1

-- Platforms sit ON TOP of ground (bottom at Y=1, not Y=0)
createPart(Vector3.new(80, 3, 80), CFrame.new(0, GROUND_TOP + 1.5, 0), color, "Platform", parent)
```

---

## Natural Map Borders (Community Best Practice)

> **DO NOT** use plain walls. Use mountains + forest + invisible collision.

```lua
--------------------------------------------------------------------------------
-- NATURAL BORDER PATTERN
--------------------------------------------------------------------------------

local borderFolder = Instance.new("Folder")
borderFolder.Name = "MapBorder"
borderFolder.Parent = workspace

-- Low-poly mountain
local function createMountain(position, baseSize, height, color)
    local mountain = Instance.new("Model")
    mountain.Name = "Mountain"

    -- Base (wide)
    createPart(Vector3.new(baseSize, height * 0.4, baseSize),
        CFrame.new(position + Vector3.new(0, height * 0.2, 0)),
        color, "Base", mountain)

    -- Middle (narrower)
    createPart(Vector3.new(baseSize * 0.7, height * 0.35, baseSize * 0.7),
        CFrame.new(position + Vector3.new(0, height * 0.55, 0)),
        color, "Mid", mountain)

    -- Peak with snow cap
    createPart(Vector3.new(baseSize * 0.35, height * 0.3, baseSize * 0.35),
        CFrame.new(position + Vector3.new(0, height * 0.85, 0)),
        BrickColor.new("Institutional white"), "Peak", mountain)

    mountain.Parent = borderFolder
    return mountain
end

-- Dense forest cluster
local function createForestCluster(centerX, centerZ, groundY, radius, density)
    for i = 1, density do
        local angle = math.random() * math.pi * 2
        local dist = math.random() * radius
        local x = centerX + math.cos(angle) * dist
        local z = centerZ + math.sin(angle) * dist
        local height = math.random(6, 14)
        createTree(Vector3.new(x, groundY, z), height, borderFolder)
    end
end

-- Invisible collision wall
local function createInvisibleWall(size, cframe)
    local wall = Instance.new("Part")
    wall.Size = size
    wall.CFrame = cframe
    wall.Anchored = true
    wall.Transparency = 1
    wall.CanCollide = true
    wall.Name = "InvisibleBarrier"
    wall.Parent = borderFolder
    return wall
end

-- Add atmosphere fog
local atmosphere = Instance.new("Atmosphere")
atmosphere.Density = 0.3
atmosphere.Haze = 1
atmosphere.Parent = game:GetService("Lighting")
```

### Border Placement Pattern
1. **Mountains** - Far outside map edge (50+ studs beyond)
2. **Forest** - Dense trees inside map edge
3. **Invisible Wall** - At exact map boundary
4. **Atmosphere** - Fog to obscure distant edges

---

## Building Patterns

### Simple Tree

```lua
local function createTree(position, height, parent)
    local tree = Instance.new("Model")
    tree.Name = "Tree"

    -- Trunk
    createPart(Vector3.new(2, height, 2),
        CFrame.new(position + Vector3.new(0, height / 2, 0)),
        BrickColor.new("Reddish brown"), "Trunk", tree)

    -- Leaves (stacked, tapering)
    local leafSizes = {8, 6, 4}
    for i, size in ipairs(leafSizes) do
        createPart(Vector3.new(size, 3, size),
            CFrame.new(position + Vector3.new(0, height + i * 3 - 1, 0)),
            BrickColor.new("Bright green"), "Leaves" .. i, tree)
    end

    tree.Parent = parent
    return tree
end
```

### Castle Components

```lua
-- Foundation (widest, ground level)
createPart(Vector3.new(40, 2, 40), CFrame.new(0, 1, 0), BrickColor.new("Dark stone grey"), "Foundation", castle)

-- Walls
createPart(Vector3.new(wallLength, wallHeight, wallThickness), wallCFrame, BrickColor.new("Medium stone grey"), "Wall", castle)

-- Crenellations (on top of walls)
for i = -n, n do
    createPart(Vector3.new(1.5, 2, 1.5), CFrame.new(i * spacing, wallTop + 1, wallZ), BrickColor.new("Medium stone grey"), "Crenel", castle)
end

-- Corner towers (taller than walls)
createPart(Vector3.new(towerSize, towerHeight, towerSize), cornerCFrame, BrickColor.new("Medium stone grey"), "Tower", castle)

-- Tower roofs (stacked, tapering)
for i, size in ipairs({4, 3, 2}) do
    createPart(Vector3.new(size, 1, size), CFrame.new(roofX, roofY + i - 1, roofZ), BrickColor.new("Bright red"), "Roof" .. i, castle)
end
```

### Dragon/Creature (Static Decoration)

```lua
-- For STATIC decorations: keep all parts Anchored
-- DO NOT use WeldConstraint for static models

local function createDragon(position, color, scale, parent)
    local dragon = Instance.new("Model")
    dragon.Name = "Dragon"
    local s = scale or 1

    -- Body (main mass)
    createPart(Vector3.new(6*s, 4*s, 10*s), CFrame.new(position), color, "Body", dragon)

    -- Head
    createPart(Vector3.new(3*s, 3*s, 4*s), CFrame.new(position + Vector3.new(0, 1*s, -6*s)), color, "Head", dragon)

    -- Snout
    createPart(Vector3.new(2*s, 1.5*s, 2*s), CFrame.new(position + Vector3.new(0, 0.5*s, -8.5*s)), color, "Snout", dragon)

    -- Neck
    createPart(Vector3.new(2*s, 3*s, 2*s), CFrame.new(position + Vector3.new(0, 2*s, -4*s)) * CFrame.Angles(math.rad(-30), 0, 0), color, "Neck", dragon)

    -- Tail segments
    local tailPos = position + Vector3.new(0, 0, 5*s)
    for i = 1, 4 do
        local tailSize = (5 - i) * s
        createPart(Vector3.new(tailSize, tailSize, 3*s), CFrame.new(tailPos + Vector3.new(0, 0, i * 3*s)), color, "Tail" .. i, dragon)
    end

    -- Wings
    for side = -1, 1, 2 do
        createPart(Vector3.new(8*s, 0.5*s, 6*s),
            CFrame.new(position + Vector3.new(side * 6*s, 2*s, 0)) * CFrame.Angles(0, 0, math.rad(side * 20)),
            color, (side == 1 and "RWing" or "LWing"), dragon)
    end

    -- Legs
    for _, offset in ipairs({{-2, -3}, {2, -3}, {-2, 3}, {2, 3}}) do
        createPart(Vector3.new(1.5*s, 3*s, 1.5*s),
            CFrame.new(position + Vector3.new(offset[1]*s, -2*s, offset[2]*s)),
            color, "Leg", dragon)
    end

    dragon.Parent = parent
    return dragon
end
```

---

## Model Organization

```
Workspace/
  MapName/
    Terrain/          -- Ground, borders, natural features
      MainGround
      MapBorder/
        Mountains/
        Trees/
        InvisibleWalls/
    HubArea/          -- Spawn, shops, etc
    ObbyCourse/       -- Stages
    WinnerArea/       -- Victory zone
```

### Rules
- Use **Folders** for organization (not Models)
- Use **Models** only for geometric objects that move together
- Set **PrimaryPart** only for physics-joined models
- **Anchor all static parts**

---

## Color Palette (Classic Style)

| Color | BrickColor Name | Use For |
|-------|-----------------|---------|
| Grey | "Medium stone grey" | Neutral, backgrounds, stone |
| Dark Grey | "Dark stone grey" | Shadows, metal, dark accents |
| Brown | "Reddish brown" | Wood, doors, trunks |
| Green | "Bright green" | Grass, leaves, nature |
| Red | "Bright red" | Lava, danger, accents |
| Blue | "Bright blue" | Water, ice, sky elements |
| Yellow | "Bright yellow" | Gold, highlights, rewards |
| White | "Institutional white" | Snow, clean surfaces |

---

## Checklist Before Building

- [ ] Stud materials loaded at script start?
- [ ] Using `createPart()` function (not raw Instance.new)?
- [ ] All surfaces set to Smooth?
- [ ] Layer system defined to avoid Z-fighting?
- [ ] All static parts anchored?
- [ ] Map border uses mountains + forest (not plain walls)?
- [ ] Part count reasonable (<5000 in view)?
