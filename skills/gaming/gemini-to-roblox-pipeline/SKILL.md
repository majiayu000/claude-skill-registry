---
name: gemini-to-roblox-pipeline
description: End-to-end pipeline for generating Roblox games from Gemini-generated concept images. Covers map generation, model reference sheets, and building Lua code from images.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Gemini → Roblox Pipeline

Automated workflow for generating complete Roblox games:
1. **Gemini** generates conceptual images (maps, model reference sheets)
2. **Claude Code** reads images and builds Lua code

---

## Quick Start

### 1. Generate Images (TypeScript)

```typescript
// gemini-generator/src/index.ts
import { GoogleGenerativeAI } from "@google/generative-ai";

const API_KEY = process.env.GEMINI_API_KEY!;
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-3-pro-image-preview" });

async function generateImage(prompt: string, filename: string) {
    const result = await model.generateContent({
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: { responseModalities: ["image", "text"] } as any,
    });

    for (const candidate of result.response.candidates || []) {
        for (const part of candidate.content?.parts || []) {
            if ((part as any).inlineData) {
                const imageBuffer = Buffer.from((part as any).inlineData.data, "base64");
                fs.writeFileSync(path.join("output", filename), imageBuffer);
                return;
            }
        }
    }
}
```

### 2. Read Images + Build Lua (Claude Code)

```
Read output/zombiesurvival_map.png
Read output/zombiesurvival_zombie.png
Build the Lua modules from these reference images
```

---

## Map Prompts (Generate BOTH)

**IMPORTANT: Generate both views for complete map reference**

### 1. Top-Down Layout Prompt (for zone planning)

```
Create a top-down 2D concept map layout for a Roblox [GAME TYPE] game with [THEME] theme.

Map size: [X] x [Z] studs

Zones to include:
1. [Zone 1 Name] - [purpose]
2. [Zone 2 Name] - [purpose]
3. [Zone 3 Name] - [purpose]

Landmarks:
- [landmark 1]
- [landmark 2]

Borders and Environment:
- [border type: mountains, forest, walls, water, cliffs]
- [environment props: trees, rocks, bushes, flowers]

Style requirements:
- Clean, colorful, cartoon/low-poly Roblox aesthetic
- Bird's eye view / top-down perspective
- Clear zone boundaries with labels
- Paths connecting zones
- Spawn point clearly marked
- Natural borders around map edges (mountains, trees, water)
- Scale reference in studs
- White background
- Simple legend/key
```

### 2. Isometric View Prompt (for visual style)

```
Create an ISOMETRIC 3D concept art of a Roblox [GAME TYPE] game.

Show the FULL [X]x[Z] stud map with ALL these zones visible:
- [Zone 1] - [brief description with key features]
- [Zone 2] - [brief description with key features]
- [Zone 3] - [brief description with key features]

Landmarks:
- [landmark 1]
- [landmark 2]

Borders and Environment:
- Natural borders: [mountains, dense forest, water, cliffs around edges]
- Environment props: [trees, rocks, bushes scattered throughout]
- Atmosphere: [fog in distance, clouds, lighting mood]

CRITICAL - Classic Roblox Stud Style:
- ISOMETRIC 45-degree camera angle showing full map
- Visible stud bumps on ALL surfaces (ground, walls, buildings)
- Blocky rectangular shapes ONLY - no curves
- Bright saturated colors: green grass, colored walls, grey platforms
- Ground is bright green baseplate with studs
- All buildings made from stacked brick parts with visible seams
- Trees and rocks made from simple geometric shapes with studs
- Natural border (mountains/forest) visible around map edges
- LEGO/classic 2006-2010 Roblox look
- Light blue sky background
- Label each zone with text
```

**Why both views?**
- **Top-down**: Zone boundaries, paths, spatial layout planning
- **Isometric**: Visual style, stud aesthetic, 3D depth, borders, atmosphere

---

## Model Reference Sheet Template (3x3 Grid)

```
Create a 3x3 grid reference sheet for a [SUBJECT] in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 front-left | Top-down view | 3/4 front-right
- Bottom row: Close-up detail | Full model with scale reference | Part breakdown with labels

Style requirements:
- Blocky low-poly shapes (build from rectangular boxes only)
- Classic Roblox stud texture on all surfaces
- Vibrant solid colors (no gradients)
- Clean edges, no bevels or smooth curves
- Show part seams/divisions where pieces connect
- White or light gray background
- Each view clearly labeled

Subject: [DESCRIPTION]
Scale: Approximately [X] studs tall
```

---

## Building Reference Sheet Template

For detailed buildings, include architectural info:

```
Create a 3x3 grid reference sheet for a [BUILDING TYPE] in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 front-left | Top-down view | 3/4 front-right
- Bottom row: Close-up detail | Full model with scale reference | Part breakdown with labels

Style requirements:
- Blocky low-poly shapes (build from rectangular boxes only)
- Classic Roblox stud texture on all surfaces
- Vibrant solid colors (no gradients)
- Clean edges, no bevels or smooth curves
- Show part seams/divisions where pieces connect
- White or light gray background
- Each view clearly labeled

Subject: [BUILDING DESCRIPTION - include doors, windows, roof style, special features]
Scale: Approximately [WIDTH] studs wide, [HEIGHT] studs tall
```

---

## Zone Environment Reference Sheet Template

**CRITICAL: Generate a reference sheet for EACH zone in the game.**

```
Create a 2x2 grid environment reference sheet for the [ZONE NAME] zone in classic Roblox stud style.

Grid layout:
- Top-left: Bird's eye view of zone layout (show terrain, paths, building placements)
- Top-right: Ground-level perspective view (show atmosphere, scale, depth)
- Bottom-left: Key props and features with labels (trees, rocks, decorations specific to this zone)
- Bottom-right: Color palette swatches + terrain material samples

Zone details:
- Name: [ZONE NAME]
- Theme: [THEME - e.g., "tropical beach", "volcanic wasteland", "candy wonderland"]
- Size: [X] x [Z] studs
- Terrain type: [e.g., sand, grass, lava rock, pink candy]
- Atmosphere: [e.g., bright and cheerful, dark and dangerous, magical and sparkly]

Buildings in this zone:
- [Building 1]: [brief description]
- [Building 2]: [brief description]

Props in this zone:
- [Prop 1]: [e.g., palm trees, lava pools, lollipop trees]
- [Prop 2]: [e.g., rocks, flames, candy canes]
- [Prop 3]: [e.g., flowers, boulders, gumdrops]

Style requirements:
- Blocky low-poly Roblox aesthetic
- Classic stud texture visible on surfaces
- Vibrant solid colors matching zone theme
- Show scale reference (character silhouette or stud measurements)
- Label all key elements
- White background
```

---

## Game Config Structure (Zone-Centric)

**IMPORTANT: Organize everything by ZONE. Each zone has its own buildings and props.**

```typescript
interface ZoneConfig {
    name: string;               // "OceanParadise"
    displayName: string;        // "Ocean Paradise"
    theme: string;              // "tropical beach with palm trees and lagoons"
    size: { x: number; z: number };
    position: { x: number; z: number };  // Relative to map center
    unlockCost: number;         // 0 = free, 5000 = 5K coins
    terrain: {
        type: string;           // "sand", "grass", "lava", "candy"
        colors: string[];       // ["Brick yellow", "Bright yellow"]
    };
    buildings: Array<{
        name: string;           // "BeachShack"
        type: string;           // "Small wooden beach shop"
        description: string;    // "Weathered wood walls, thatched roof, surfboard decoration"
        position: { x: number; z: number };  // Relative to zone center
    }>;
    props: Array<{
        name: string;           // "PalmTree"
        type: string;           // "Tropical palm tree"
        description: string;    // "Curved trunk, coconuts, fan-shaped fronds"
        count: number;          // How many to scatter in zone
    }>;
    features: string[];         // ["lagoons", "waterfall", "dock", "rocks"]
}

interface GameConfig {
    name: string;
    map: {
        type: string;           // "simulator", "survival", "obby", "tycoon"
        theme: string;          // "pet collection fantasy worlds"
        size: { x: number; z: number };
        spawnZone: string;      // Which zone is the spawn hub
    };
    zones: ZoneConfig[];        // All zones with their buildings and props
    globalModels: Array<{       // Characters/pets that appear across zones
        name: string;
        type: string;
        description: string;
        category: "character" | "pet" | "npc" | "enemy";
    }>;
}
```

### Example: Pet Simulator Config

```typescript
const petSimulator: GameConfig = {
    name: "PetSimulator",
    map: {
        type: "simulator",
        theme: "colorful fantasy pet worlds",
        size: { x: 500, z: 500 },
        spawnZone: "SpawnHub",
    },
    zones: [
        {
            name: "SpawnHub",
            displayName: "Spawn Hub",
            theme: "central plaza with crystal fountain and shops",
            size: { x: 100, z: 100 },
            position: { x: 0, z: 0 },
            unlockCost: 0,
            terrain: { type: "stone", colors: ["Medium stone grey", "Dark stone grey"] },
            buildings: [
                { name: "PetShop", type: "Pet store", description: "Purple walls, large windows, paw print sign, striped awning", position: { x: -30, z: -10 } },
                { name: "HatchStation", type: "Egg hatching building", description: "Dome roof, glowing eggs inside, rainbow trim", position: { x: 30, z: -5 } },
                { name: "TradingPost", type: "Trading booth", description: "Market stall with two sides, trade arrows, coin decorations", position: { x: 0, z: -35 } },
            ],
            props: [
                { name: "CrystalFountain", type: "Magical fountain", description: "Cyan crystal pillar, circular pool, glowing spikes", count: 1 },
                { name: "CoinPile", type: "Decorative coins", description: "Stack of gold coins, sparkle effect", count: 3 },
                { name: "GiantEgg", type: "Landmark statue", description: "Massive colorful egg on pedestal", count: 1 },
            ],
            features: ["spawn point", "rainbow bridges to other zones", "paths"],
        },
        {
            name: "OceanParadise",
            displayName: "Ocean Paradise",
            theme: "tropical beach with palm trees and blue lagoons",
            size: { x: 100, z: 100 },
            position: { x: -100, z: -180 },
            unlockCost: 5000,
            terrain: { type: "sand", colors: ["Brick yellow", "Bright yellow"] },
            buildings: [
                { name: "BeachShack", type: "Tropical shop", description: "Wooden walls, thatched roof, surfboard sign", position: { x: 20, z: 15 } },
            ],
            props: [
                { name: "PalmTree", type: "Tropical tree", description: "Curved trunk, coconuts, fan fronds", count: 8 },
                { name: "Lagoon", type: "Water pool", description: "Cyan water, sandy rim, deeper center", count: 3 },
                { name: "BeachRock", type: "Coastal rock", description: "Grey weathered stone", count: 6 },
                { name: "Dock", type: "Wooden pier", description: "Planks extending into water, rope ties", count: 1 },
                { name: "Waterfall", type: "Cliff waterfall", description: "Rock cliff, flowing water, splash pool", count: 1 },
            ],
            features: ["lagoons", "waterfall", "dock"],
        },
        // ... more zones
    ],
    globalModels: [
        { name: "DragonPet", type: "Dragon", description: "Purple body, orange belly, small wings, cute eyes", category: "pet" },
        { name: "UnicornPet", type: "Unicorn", description: "White body, rainbow mane, golden horn", category: "pet" },
        { name: "SlimePet", type: "Slime", description: "Green blob, big eyes, bouncy", category: "pet" },
    ],
};
```

---

## Lua Module Template

Every module MUST include stud material loading:

```lua
--[[
    [MODEL NAME] - Auto-generated from Gemini Reference Sheet

    Structure (from part breakdown):
    - [PART 1]: [description]
    - [PART 2]: [description]
]]

local Workspace = game:GetService("Workspace")
local AssetService = game:GetService("AssetService")
local MaterialService = game:GetService("MaterialService")

local ModuleName = {}

--------------------------------------------------------------------------------
-- STUD MATERIALS (MANDATORY)
--------------------------------------------------------------------------------

local studMaterialName = ""
local studBaseMaterial = Enum.Material.Plastic

pcall(function()
    for _, item in ipairs(MaterialService:GetChildren()) do
        if item:IsA("MaterialVariant") then
            studMaterialName = item.Name
            studBaseMaterial = item.BaseMaterial
            return
        end
    end
    local asset = AssetService:LoadAssetAsync(13719188279)
    if asset then
        local mv = asset:FindFirstChildWhichIsA("MaterialVariant", true)
        if mv then
            mv.Parent = MaterialService
            studMaterialName = mv.Name
            studBaseMaterial = mv.BaseMaterial
        end
        asset:Destroy()
    end
end)

--------------------------------------------------------------------------------
-- COLORS (From Reference Sheet)
--------------------------------------------------------------------------------

local C = {
    MAIN = BrickColor.new("Bright red"),
    ACCENT = BrickColor.new("Dark stone grey"),
}

--------------------------------------------------------------------------------
-- PART CREATION
--------------------------------------------------------------------------------

local function createPart(size, cframe, color, name, parent, material)
    local part = Instance.new("Part")
    part.Size = size
    part.CFrame = cframe
    part.Anchored = true
    part.BrickColor = color
    part.Material = material or Enum.Material.Plastic

    -- Apply stud material if available
    if studMaterialName ~= "" and not material then
        part.Material = studBaseMaterial
        part.MaterialVariant = studMaterialName
    end

    part.TopSurface = Enum.SurfaceType.Smooth
    part.BottomSurface = Enum.SurfaceType.Smooth
    part.Name = name or "Part"
    part.Parent = parent
    return part
end

--------------------------------------------------------------------------------
-- BUILD MODEL
--------------------------------------------------------------------------------

function ModuleName.Create(position)
    local model = Instance.new("Model")
    model.Name = "ModelName"

    local pos = position or Vector3.new(0, 0, 0)
    local baseY = pos.Y

    -- Build parts based on reference sheet...
    createPart(
        Vector3.new(width, height, depth),
        CFrame.new(pos.X, baseY + yOffset, pos.Z),
        C.MAIN, "PartName", model
    )

    model.PrimaryPart = model:FindFirstChild("MainPart")
    return model
end

function ModuleName.Spawn(position)
    local model = ModuleName.Create(position)
    model.Parent = Workspace
    return model
end

return ModuleName
```

---

## Zone Module Template

Each zone should be a self-contained module that builds its terrain, buildings, and props:

```lua
--[[
    [ZONE NAME] - Auto-generated from Gemini Zone Reference Sheet

    Environment (from zone sheet):
    - Terrain: [type and colors]
    - Atmosphere: [mood/lighting notes]

    Buildings:
    - [Building 1]
    - [Building 2]

    Props:
    - [Prop 1] x [count]
    - [Prop 2] x [count]
]]

local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Use shared PartUtils for stud materials
local PartUtils = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("PartUtils"))

-- Load buildings and props for this zone
local Modules = ReplicatedStorage:WaitForChild("Modules")
local Building1 = require(Modules.Buildings:WaitForChild("Building1"))
local Prop1 = require(Modules.Props:WaitForChild("Prop1"))

local ZoneName = {}

--------------------------------------------------------------------------------
-- COLORS (From Zone Reference Sheet)
--------------------------------------------------------------------------------

local C = {
    TERRAIN = BrickColor.new("Brick yellow"),
    TERRAIN_ACCENT = BrickColor.new("Bright yellow"),
    WATER = BrickColor.new("Cyan"),
}

--------------------------------------------------------------------------------
-- HELPERS
--------------------------------------------------------------------------------

local function createPart(size, cframe, color, name, parent, material, transparency)
    return PartUtils.CreatePart(size, cframe, color, name, parent, material, transparency)
end

--------------------------------------------------------------------------------
-- BUILD ZONE
--------------------------------------------------------------------------------

function ZoneName.Create(position)
    local zone = Instance.new("Model")
    zone.Name = "ZoneName"

    local pos = position or Vector3.new(0, 0, 0)
    local baseY = pos.Y

    -- TERRAIN (from zone reference sheet)
    local ground = createPart(
        Vector3.new(100, 3, 100),
        CFrame.new(pos.X, baseY - 1.5, pos.Z),
        C.TERRAIN, "Ground", zone, Enum.Material.Sand
    )

    -- TERRAIN ACCENT PATCHES (from zone reference)
    local patches = {
        {x = -25, z = 15, size = 20},
        {x = 20, z = -20, size = 18},
    }
    for i, patch in ipairs(patches) do
        createPart(
            Vector3.new(patch.size, 1, patch.size),
            CFrame.new(pos.X + patch.x, baseY + 0.1, pos.Z + patch.z),
            C.TERRAIN_ACCENT, "Patch" .. i, zone, Enum.Material.Sand
        )
    end

    -- BUILDINGS (spawn at configured positions)
    local building1 = Building1.Create(Vector3.new(pos.X + 20, baseY, pos.Z + 15))
    building1.Parent = zone

    -- PROPS (scatter according to count)
    local propPositions = {
        {x = -35, z = 25}, {x = -25, z = 35}, {x = 30, z = 20},
        {x = 40, z = -15}, {x = -40, z = -20},
    }
    for i, pp in ipairs(propPositions) do
        local prop = Prop1.Create(Vector3.new(pos.X + pp.x, baseY, pos.Z + pp.z))
        prop.Parent = zone
    end

    -- ZONE-SPECIFIC FEATURES (lagoons, lava pools, etc.)
    -- Built inline based on zone reference sheet
    createPart(
        Vector3.new(25, 1, 20),
        CFrame.new(pos.X - 20, baseY - 0.5, pos.Z + 15),
        C.WATER, "Lagoon", zone, Enum.Material.Glass, 0.3
    )

    -- ZONE LABEL
    local labelPart = createPart(
        Vector3.new(1, 1, 1),
        CFrame.new(pos.X, baseY + 20, pos.Z),
        BrickColor.new("White"), "LabelAnchor", zone
    )
    labelPart.Transparency = 1

    local billboard = Instance.new("BillboardGui")
    billboard.Size = UDim2.new(0, 300, 0, 80)
    billboard.AlwaysOnTop = true
    billboard.Parent = labelPart

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, 0, 1, 0)
    label.BackgroundColor3 = Color3.fromRGB(0, 150, 200)
    label.BackgroundTransparency = 0.3
    label.TextColor3 = Color3.new(1, 1, 1)
    label.Text = "ZONE NAME\n5K Coins"
    label.TextScaled = true
    label.Font = Enum.Font.GothamBold
    label.Parent = billboard

    zone.PrimaryPart = ground
    return zone
end

function ZoneName.Spawn(position)
    local zone = ZoneName.Create(position)
    zone.Parent = Workspace
    return zone
end

return ZoneName
```

---

## Game Runner Template

```lua
--[[
    [GAME NAME] - Full Game Runner
    Auto-generated from Gemini Reference Images
]]

local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lighting = game:GetService("Lighting")

--------------------------------------------------------------------------------
-- LOAD MODULES
--------------------------------------------------------------------------------

local Modules = ReplicatedStorage:WaitForChild("Modules")

local Model1 = require(Modules:WaitForChild("Model1"))
local Model2 = require(Modules:WaitForChild("Model2"))
-- ... more modules

--------------------------------------------------------------------------------
-- COLORS
--------------------------------------------------------------------------------

local C = {
    GROUND = BrickColor.new("Dark stone grey"),
    ROAD = BrickColor.new("Really black"),
    GRASS = BrickColor.new("Bright green"),
}

--------------------------------------------------------------------------------
-- HELPERS
--------------------------------------------------------------------------------

local function createPart(size, position, color, name, parent, material)
    local part = Instance.new("Part")
    part.Size = size
    part.Position = position
    part.Anchored = true
    part.BrickColor = color
    part.Material = material or Enum.Material.Concrete
    part.TopSurface = Enum.SurfaceType.Smooth
    part.BottomSurface = Enum.SurfaceType.Smooth
    part.Name = name or "Part"
    part.Parent = parent
    return part
end

--------------------------------------------------------------------------------
-- BUILD WORLD
--------------------------------------------------------------------------------

local function buildGameWorld()
    if Workspace:FindFirstChild("GameWorld") then
        Workspace.GameWorld:Destroy()
    end

    local world = Instance.new("Model")
    world.Name = "GameWorld"

    -- BASEPLATE
    local baseplate = createPart(
        Vector3.new(400, 1, 400),
        Vector3.new(0, -0.5, 0),
        C.GROUND, "Baseplate", world
    )

    -- SPAWN BUILDINGS
    local building1 = Model1.Create(Vector3.new(x, 0, z))
    building1.Parent = world

    -- LIGHTING (BRIGHT)
    Lighting.TimeOfDay = "14:00:00"
    Lighting.Ambient = Color3.fromRGB(150, 150, 150)
    Lighting.OutdoorAmbient = Color3.fromRGB(180, 180, 180)
    Lighting.Brightness = 2
    Lighting.FogEnd = 10000

    world.PrimaryPart = baseplate
    world.Parent = Workspace

    return world
end

buildGameWorld()
```

---

## Lighting Presets

### Bright Daytime (DEFAULT - Use this!)
```lua
Lighting.TimeOfDay = "14:00:00"
Lighting.Ambient = Color3.fromRGB(150, 150, 150)
Lighting.OutdoorAmbient = Color3.fromRGB(180, 180, 180)
Lighting.Brightness = 2
Lighting.FogEnd = 10000
```

### Sunset/Dusk
```lua
Lighting.TimeOfDay = "18:30:00"
Lighting.Ambient = Color3.fromRGB(120, 100, 100)
Lighting.OutdoorAmbient = Color3.fromRGB(150, 120, 100)
Lighting.Brightness = 1.8
```

### Night (Use sparingly)
```lua
Lighting.TimeOfDay = "00:00:00"
Lighting.Ambient = Color3.fromRGB(50, 50, 70)
Lighting.OutdoorAmbient = Color3.fromRGB(70, 70, 90)
Lighting.Brightness = 0.5
```

---

## File Structure (Zone-Centric)

```
roblox-auto-builder/
├── default.project.json          # Rojo project
├── gemini-generator/
│   ├── src/
│   │   ├── index.ts              # Simple image generator
│   │   ├── game-config.ts        # Game configurations (zone-centric)
│   │   └── generate-game.ts      # Full game generator
│   └── output/
│       ├── gamename_map.png              # Overall map layout
│       ├── gamename_zone_SpawnHub.png    # Zone environment sheet
│       ├── gamename_zone_OceanParadise.png
│       ├── gamename_zone_VolcanoIsland.png
│       ├── gamename_building_PetShop.png  # Building reference sheets
│       ├── gamename_building_BeachShack.png
│       ├── gamename_prop_PalmTree.png     # Prop reference sheets
│       ├── gamename_prop_Lagoon.png
│       ├── gamename_pet_DragonPet.png     # Global model sheets
│       └── gamename_manifest.json
└── src/
    ├── ReplicatedStorage/
    │   └── Modules/
    │       ├── PartUtils.lua             # Shared stud material utility
    │       ├── Zones/
    │       │   ├── SpawnHub.lua          # Zone modules (terrain + props)
    │       │   ├── OceanParadise.lua
    │       │   └── VolcanoIsland.lua
    │       ├── Buildings/
    │       │   ├── PetShop.lua
    │       │   └── BeachShack.lua
    │       ├── Props/
    │       │   ├── PalmTree.lua
    │       │   └── Lagoon.lua
    │       └── Pets/
    │           ├── DragonPet.lua
    │           └── UnicornPet.lua
    └── ServerScriptService/
        └── GameRunner.server.lua
```

---

## Workflow Checklist

### 1. Image Generation (Zone-Centric)

**Overall Map:**
- [ ] Generate top-down map showing all zones and connections

**For EACH Zone:**
- [ ] Generate zone environment reference sheet (terrain, layout, atmosphere)
- [ ] Generate reference sheets for each BUILDING in that zone
- [ ] Generate reference sheets for each PROP type in that zone

**Global Models:**
- [ ] Generate reference sheets for pets/characters that appear across zones

### 2. Building Lua (Zone-First Approach)

**Shared Utilities:**
- [ ] Create PartUtils.lua for stud material handling

**For EACH Zone:**
- [ ] Read zone environment reference image
- [ ] Create Zone module (terrain, ground, atmosphere)
- [ ] Read each building reference for that zone → create Building module
- [ ] Read each prop reference for that zone → create Prop module
- [ ] Zone module should spawn its own buildings and props

**Global Models:**
- [ ] Create Pet/Character modules from reference sheets

### 3. Zone Module Structure

Each zone module should:
- [ ] Create terrain/ground with correct colors
- [ ] Spawn all buildings at configured positions
- [ ] Scatter props according to count
- [ ] Add zone-specific features (lagoons, lava pools, etc.)
- [ ] Include zone label (BillboardGui)

### 4. Game Runner

- [ ] Load stud materials at startup (MANDATORY)
- [ ] Load all zone modules
- [ ] Spawn each zone at its configured position
- [ ] Create paths/bridges connecting zones
- [ ] Set BRIGHT lighting (TimeOfDay = "14:00:00")
- [ ] Test with `rojo serve`

---

## Layer System (Prevent Z-Fighting)

**CRITICAL: Never place parts with surfaces at exactly the same Y position.**

```lua
-- Define layer heights (build from bottom up)
local LAYERS = {
    GROUND = 0,           -- Ground centered here, top surface at Y=1
    GROUND_TOP = 1,       -- Top of ground surface (objects sit HERE)
    PLATFORM = 2,         -- Platforms ON TOP of ground (not overlapping)
    BUILDING = 1,         -- Buildings bottom at GROUND_TOP
    SPAWN = 1.5,          -- Spawn pads slightly above ground
}

-- Ground: 2 thick, centered at Y=0 → bottom at -1, top at +1
local ground = createPart(
    Vector3.new(MAP_SIZE, 2, MAP_SIZE),
    CFrame.new(0, LAYERS.GROUND, 0),
    COLORS.Ground, arena
)

-- Platform: 2 thick, bottom at GROUND_TOP (Y=1), center at Y=2
local platformY = LAYERS.GROUND_TOP + 1
createPart(
    Vector3.new(60, 2, 60),
    CFrame.new(0, platformY, 0),
    COLORS.Grey, arena
)

-- Objects on ground: position Y = GROUND_TOP (1)
HealthPack.create(Vector3.new(50, LAYERS.GROUND_TOP, 0))

-- Buildings: bottom at GROUND_TOP, so center = GROUND_TOP + height/2
local buildingHeight = 15
createBuilding(
    Vector3.new(50, buildingHeight, 25),
    CFrame.new(x, LAYERS.GROUND_TOP + buildingHeight/2, z),
    COLORS.Red, arena
)
```

**Key Rules:**
1. Ground top surface at Y=1 (size 2, centered at Y=0)
2. All objects placed at Y ≥ 1 (never Y=0)
3. Platforms sit ON TOP of ground (bottom at Y=1)
4. No surfaces at exactly the same Y position

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Can't see anything | Set Lighting.TimeOfDay = "14:00:00", Brightness = 2 |
| Z-fighting/flickering | Use Layer system - ground top at Y=1, objects at Y≥1 |
| No studs | Check studMaterialName loaded, Material = studBaseMaterial |
| Parts floating | Check baseY calculation, use CFrame |
| Module not found | Ensure file is in ReplicatedStorage/Modules |

---

## Image Generation Order

**Generate images in this order for best results:**

```
1. OVERALL MAP
   └── gamename_map.png (top-down layout of all zones)

2. FOR EACH ZONE (repeat for every zone):
   ├── gamename_zone_ZoneName.png (zone environment sheet)
   ├── gamename_building_BuildingName.png (for each building in zone)
   └── gamename_prop_PropName.png (for each unique prop type in zone)

3. GLOBAL MODELS (pets, characters, enemies):
   └── gamename_pet_PetName.png (reference sheet for each)
```

### Example: Pet Simulator Images to Generate

```
1. petsimulator_map.png                    # Overall map

2. Spawn Hub Zone:
   - petsimulator_zone_SpawnHub.png        # Zone environment
   - petsimulator_building_PetShop.png     # Building in this zone
   - petsimulator_building_HatchStation.png
   - petsimulator_building_TradingPost.png
   - petsimulator_prop_CrystalFountain.png # Props in this zone
   - petsimulator_prop_CoinPile.png
   - petsimulator_prop_GiantEgg.png

3. Ocean Paradise Zone:
   - petsimulator_zone_OceanParadise.png   # Zone environment
   - petsimulator_building_BeachShack.png  # Building in this zone
   - petsimulator_prop_PalmTree.png        # Props in this zone
   - petsimulator_prop_Lagoon.png
   - petsimulator_prop_BeachRock.png
   - petsimulator_prop_Dock.png
   - petsimulator_prop_Waterfall.png

4. Volcano Island Zone:
   - petsimulator_zone_VolcanoIsland.png
   - petsimulator_prop_Volcano.png
   - petsimulator_prop_LavaPool.png
   - petsimulator_prop_LavaRiver.png
   - petsimulator_prop_Flame.png
   - petsimulator_prop_Boulder.png

5. (Repeat for Candy Kingdom, Cloud Temple, etc.)

6. Global Pets:
   - petsimulator_pet_DragonPet.png
   - petsimulator_pet_UnicornPet.png
   - petsimulator_pet_SlimePet.png
```

**Total images for a 6-zone game: ~40-60 images**

---

## Running the Pipeline

```bash
# 1. Generate images (zone by zone)
cd gemini-generator
npx tsx src/generate-game.ts petsimulator

# 2. Build Lua (Claude Code reads images, builds code)
#    - Read zone images first, build zone modules
#    - Read building/prop images, build their modules
#    - Read pet images, build pet modules

# 3. Serve with Rojo
cd ..
rojo serve

# 4. Connect in Roblox Studio and Play
```

---

## Roblox Open Cloud Asset Upload

Upload generated images (icons, textures) to Roblox using the Open Cloud API.

### API Key Setup

1. Go to [Roblox Creator Dashboard](https://create.roblox.com/credentials)
2. Create an API Key with **Asset** permissions
3. Store in `.env` file:

```
ROBLOX_API_KEY=your_api_key_here
ROBLOX_CREATOR_ID=your_user_id
```

### CRITICAL: Image vs Decal Asset Types

**Use `"Image"` NOT `"Decal"` for ImageLabel/ImageButton assets!**

| Asset Type | Use For | ImageLabel Works? |
|------------|---------|-------------------|
| `Image` | UI icons, textures for ImageLabel/ImageButton | ✅ YES |
| `Decal` | Placing on 3D surfaces (SurfaceGui, Part faces) | ❌ NO - fails silently |

If your `ImageLabel.Image = "rbxassetid://..."` shows nothing, the asset was likely uploaded as Decal instead of Image.

### Upload Script (Python)

```python
#!/usr/bin/env python3
"""Upload images to Roblox using Open Cloud API"""

import os
import requests
import json
import time
from pathlib import Path

API_KEY = os.environ.get("ROBLOX_API_KEY")
CREATOR_ID = os.environ.get("ROBLOX_CREATOR_ID")  # Your Roblox user ID

def upload_image(filepath: Path) -> dict:
    """Upload a single image to Roblox"""

    # Step 1: Create the asset
    create_url = "https://apis.roblox.com/assets/v1/assets"

    request_data = {
        "assetType": "Image",  # CRITICAL: Use "Image" not "Decal"!
        "displayName": filepath.stem,
        "description": f"Game icon: {filepath.stem}",
        "creationContext": {
            "creator": {
                "userId": CREATOR_ID
            }
        }
    }

    with open(filepath, "rb") as f:
        files = {
            "request": (None, json.dumps(request_data), "application/json"),
            "fileContent": (filepath.name, f, "image/png")
        }

        headers = {"x-api-key": API_KEY}
        response = requests.post(create_url, headers=headers, files=files)

    if response.status_code not in [200, 202]:
        print(f"Error uploading {filepath.name}: {response.status_code}")
        print(response.text)
        return None

    result = response.json()
    operation_path = result.get("path")

    if not operation_path:
        # Asset created immediately
        asset_id = result.get("assetId")
        return {"name": filepath.stem, "assetId": asset_id}

    # Step 2: Poll for operation completion
    operation_url = f"https://apis.roblox.com/assets/v1/{operation_path}"

    for _ in range(30):  # Try for up to 30 seconds
        time.sleep(1)
        poll_response = requests.get(operation_url, headers={"x-api-key": API_KEY})

        if poll_response.status_code == 200:
            poll_result = poll_response.json()
            if poll_result.get("done"):
                asset_id = poll_result.get("response", {}).get("assetId")
                return {"name": filepath.stem, "assetId": asset_id}

    return None

def upload_all_icons(icons_dir: str = "icons"):
    """Upload all PNG icons from a directory"""

    icons_path = Path(icons_dir)
    results = {}

    for icon_file in sorted(icons_path.glob("*.png")):
        print(f"Uploading: {icon_file.name}")
        result = upload_image(icon_file)

        if result:
            results[result["name"]] = result["assetId"]
            print(f"  ✓ Asset ID: {result['assetId']}")
        else:
            print(f"  ✗ Failed")

        time.sleep(0.5)  # Rate limiting

    # Output Lua table format
    print("\n-- Lua ImageIds table:")
    print("local ImageIds = {")
    for name, asset_id in results.items():
        print(f'    {name} = {asset_id},')
    print("}")

    return results

if __name__ == "__main__":
    upload_all_icons()
```

### Usage in Lua

```lua
-- Asset IDs from upload script
local ImageIds = {
    cart = 90283386707571,
    user = 72853438280365,
    gift = 77873200486139,
    star = 116490617957644,
    settings = 74083320393999,
    lightning = 81822478326252,
    coin = 110273009388007,
    gem = 73443096543152,
    close = 113514151215598,
    lock = 96486895661754,
    snowflake = 131525484032997,
    wings = 73570345607333,
    heart = 73938811915569,
    thumbsup = 80642926508347,
    crown = 109249962609144,
    trophy = 92957897014777,
}

-- Preload assets for smooth loading
local ContentProvider = game:GetService("ContentProvider")

local function preloadIcons()
    local assets = {}
    for name, id in pairs(ImageIds) do
        table.insert(assets, "rbxassetid://" .. id)
    end
    ContentProvider:PreloadAsync(assets)
end

-- Use in ImageLabel
local icon = Instance.new("ImageLabel")
icon.Image = "rbxassetid://" .. ImageIds.coin  -- Works!
```

### Troubleshooting Upload Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| ImageLabel shows nothing | Asset uploaded as "Decal" | Re-upload with `assetType: "Image"` |
| 403 Forbidden | API key lacks permissions | Add Asset permissions in Creator Dashboard |
| 400 Bad Request | Invalid creator ID | Use your Roblox user ID as CREATOR_ID |
| Asset stuck "processing" | Large file or server busy | Wait and poll, or retry |
| Rate limited | Too many requests | Add `time.sleep(0.5)` between uploads |

### Full Pipeline: Generate → Upload → Use

```bash
# 1. Generate icon grid with Gemini
python generate_icons.py

# 2. Upload to Roblox
python upload_icons.py

# 3. Copy the Lua ImageIds table to your game script

# 4. Use in Roblox Studio
```

### Directory Structure for Asset Pipeline

```
project/
├── .env                    # API keys (gitignored!)
├── generate_icons.py       # Gemini icon grid generation
├── upload_icons.py         # Roblox Open Cloud upload
├── icon_grid.png           # Generated 4x4 grid
├── icons/                  # Cropped individual icons
│   ├── cart.png
│   ├── user.png
│   ├── gift.png
│   └── ...
└── src/
    └── ObbyUI_Show.lua     # Game script using uploaded assets
```
