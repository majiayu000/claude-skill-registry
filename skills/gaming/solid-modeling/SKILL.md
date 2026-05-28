---
name: solid-modeling
description: Teaches CSG (Constructive Solid Geometry) patterns for building complex shapes from primitives. Use when creating buildings, props, terrain features, or any geometric construction in Roblox.
allowed-tools: Read, Write, Edit, Glob, Grep
model: sonnet
---

# Solid Modeling / CSG

Constructive Solid Geometry (CSG) builds complex shapes from simple primitives using Boolean operations.

## Core Operations

```
UNION (A ∪ B)         SUBTRACT (A - B)       INTERSECT (A ∩ B)
Combines volumes      Cuts B from A          Keeps only overlap
```

| Operation | Roblox API | Use For |
|-----------|------------|---------|
| Union | `part:UnionAsync({others})` | Joining pieces |
| Subtract | `part:SubtractAsync({others})` | Holes, cutouts |
| Intersect | `part:IntersectAsync({others})` | Complex curves, clipping |

---

## Primitive Selection Guide

### Box (Most Versatile)
```
Best for:
├── Walls, floors, ceilings
├── Frames (box - smaller box)
├── Steps (stacked boxes)
├── Slots, grooves (subtract thin box)
├── Beveled edges (rotated box union)
└── Any rectangular feature
```

### Cylinder
```
Best for:
├── Holes (subtract from anything)
├── Pillars, poles, pipes
├── Rounded edges (union at corners)
├── Wheels, discs
├── Tubes (cylinder - cylinder)
└── Bolts, screws (with sphere cap)
```

### Sphere
```
Best for:
├── Domes (sphere ∩ box = hemisphere)
├── Bowls (sphere - smaller sphere)
├── Rounded corners (intersect with box)
├── Organic bulges
├── Ball joints, sockets
└── Smooth blends between shapes
```

### Wedge
```
Best for:
├── Ramps, slopes
├── Roof sections
├── Chamfered edges
├── Angular cuts
└── Triangular features
```

### Corner Wedge
```
Best for:
├── Pyramid tops
├── Corner slopes
├── Hip roof sections
└── Diagonal transitions
```

---

## Common Recipes

### Architecture

```lua
-- WINDOW: Wall with rectangular hole
local wall = createBox(10, 8, 0.5)
local windowHole = createBox(3, 4, 0.5)
windowHole.Position = Vector3.new(0, 1, 0)
local result = wall:SubtractAsync({windowHole})

-- DOOR FRAME: Box minus box
local frame = createBox(4, 8, 0.5)
local opening = createBox(3, 7, 0.5)
opening.Position = Vector3.new(0, -0.5, 0)
local result = frame:SubtractAsync({opening})

-- ARCH: Rectangle + half cylinder cutout
local wall = createBox(10, 8, 1)
local rectCut = createBox(3, 5, 1)
rectCut.Position = Vector3.new(0, -1.5, 0)
local archCut = createCylinder(1.5, 1)
archCut.CFrame = CFrame.new(0, 2.5, 0) * CFrame.Angles(math.rad(90), 0, 0)
local cutout = rectCut:UnionAsync({archCut})
local result = wall:SubtractAsync({cutout})

-- PILLAR WITH BASE: Cylinder + wider cylinder
local shaft = createCylinder(1, 10)
local base = createCylinder(1.5, 0.5)
base.Position = Vector3.new(0, -4.75, 0)
local capital = createCylinder(1.5, 0.5)
capital.Position = Vector3.new(0, 4.75, 0)
local result = shaft:UnionAsync({base, capital})
```

### Mechanical

```lua
-- PIPE: Cylinder minus cylinder
local outer = createCylinder(2, 10)
local inner = createCylinder(1.5, 10)
local pipe = outer:SubtractAsync({inner})

-- FLANGE: Pipe + wider disc
local flange = createCylinder(3, 0.5)
flange.Position = Vector3.new(0, 5, 0)
local result = pipe:UnionAsync({flange})

-- BOLT HOLES: Subtract cylinders in circle
local plate = createBox(10, 10, 1)
local holes = {}
for i = 0, 5 do
    local angle = i * (math.pi * 2 / 6)
    local hole = createCylinder(0.5, 1)
    hole.Position = Vector3.new(math.cos(angle) * 3, 0, math.sin(angle) * 3)
    table.insert(holes, hole)
end
local result = plate:SubtractAsync(holes)

-- GEAR TOOTH: Wedge shapes around cylinder
local disc = createCylinder(5, 1)
local teeth = {}
for i = 0, 11 do
    local angle = i * (math.pi * 2 / 12)
    local tooth = createWedge(1, 1, 0.5)
    tooth.CFrame = CFrame.new(math.cos(angle) * 5.5, 0, math.sin(angle) * 5.5)
                 * CFrame.Angles(0, -angle, 0)
    table.insert(teeth, tooth)
end
local result = disc:UnionAsync(teeth)
```

### Organic / Curved

```lua
-- ROUNDED BOX: Box intersect sphere
local box = createBox(4, 4, 4)
local sphere = createSphere(3.2)  -- Slightly larger than box diagonal / 2
local rounded = box:IntersectAsync({sphere})

-- DOME: Sphere intersect box (top half)
local sphere = createSphere(5)
local cutter = createBox(10, 5, 10)
cutter.Position = Vector3.new(0, 2.5, 0)
local dome = sphere:IntersectAsync({cutter})

-- BOWL: Sphere minus smaller sphere
local outer = createSphere(5)
local inner = createSphere(4)
inner.Position = Vector3.new(0, 1, 0)  -- Offset up for bowl shape
local bowl = outer:SubtractAsync({inner})

-- TORUS (Donut): Revolve circle (approximate with unions)
local segments = {}
for i = 0, 23 do
    local angle = i * (math.pi * 2 / 24)
    local ring = createSphere(1)
    ring.Position = Vector3.new(math.cos(angle) * 4, 0, math.sin(angle) * 4)
    table.insert(segments, ring)
end
local torus = segments[1]:UnionAsync({unpack(segments, 2)})
```

### Terrain / Environment

```lua
-- CAVE ENTRANCE: Hill minus stretched sphere
local hill = createSphere(20)
hill.Size = Vector3.new(40, 20, 30)  -- Flatten
local caveCut = createSphere(8)
caveCut.Position = Vector3.new(0, -5, -15)  -- Position at front
local result = hill:SubtractAsync({caveCut})

-- CLIFF LEDGE: Box with angular cut
local cliff = createBox(20, 15, 10)
local cut = createWedge(20, 10, 10)
cut.CFrame = CFrame.new(0, 7.5, 5) * CFrame.Angles(0, 0, math.rad(180))
local result = cliff:SubtractAsync({cut})

-- ROCK: Multiple spheres unioned
local spheres = {}
for i = 1, 8 do
    local s = createSphere(math.random(2, 4))
    s.Position = Vector3.new(
        math.random(-3, 3),
        math.random(-2, 2),
        math.random(-3, 3)
    )
    table.insert(spheres, s)
end
local rock = spheres[1]:UnionAsync({unpack(spheres, 2)})
```

---

## Operation Order Strategy

### Principle: Minimize Operations

```lua
-- BAD: Many sequential operations
local result = a:UnionAsync({b})
result = result:UnionAsync({c})
result = result:UnionAsync({d})
result = result:SubtractAsync({e})
result = result:SubtractAsync({f})

-- GOOD: Batch similar operations
local additions = a:UnionAsync({b, c, d})
local result = additions:SubtractAsync({e, f})
```

### Principle: Subtract Last

```lua
-- GOOD: Build up, then cut
local solid = base:UnionAsync({extensions})
local final = solid:SubtractAsync({allHoles})

-- BAD: Alternating (more mesh complexity)
local step1 = base:SubtractAsync({hole1})
local step2 = step1:UnionAsync({ext1})
local step3 = step2:SubtractAsync({hole2})
```

### Principle: Hierarchical Assembly

```lua
-- Build sub-assemblies, then combine
local leftWing = buildWing(params)
local rightWing = buildWing(params):Clone()
rightWing.CFrame = mirrorCFrame

local fuselage = buildFuselage(params)
local tail = buildTail(params)

local aircraft = fuselage:UnionAsync({leftWing, rightWing, tail})
```

---

## Roblox CSG API

### Basic Usage

```lua
-- Union: Combine parts
local union = mainPart:UnionAsync(otherParts)
union.Parent = workspace

-- Subtract: Cut away
local result = mainPart:SubtractAsync(cutParts)

-- Intersect: Keep overlap
local result = mainPart:IntersectAsync(clipParts)
```

### With Options

```lua
local result = mainPart:UnionAsync(others, {
    CollisionFidelity = Enum.CollisionFidelity.Hull,
    RenderFidelity = Enum.RenderFidelity.Automatic
})
```

### Collision Fidelity

| Setting | Use When |
|---------|----------|
| `Box` | Background props, fastest |
| `Hull` | Convex shapes, good balance |
| `Default` | Precise collision needed |
| `PreciseConvexDecomposition` | Most accurate, slowest |

### Property Inheritance

The **calling part's** properties transfer to result:
- Color, Material, Transparency
- Anchored, CanCollide
- Physical properties (Density, Friction, etc.)

```lua
-- mainPart's properties will be on result
local result = mainPart:SubtractAsync({cutPart})
```

### UsePartColor

```lua
-- true: Each original part keeps its color
-- false: Result uses single color
result.UsePartColor = true
```

---

## Performance Guidelines

### Triangle Count

```
Each operation can multiply triangles:
- Simple box: 12 triangles
- Box + Cylinder: ~50 triangles
- Complex union: 100s-1000s

Monitor with: result:GetTrianglesCount() -- in Studio
```

### Avoid These

```lua
-- BAD: Tiny cuts (creates many small faces)
for i = 1, 100 do
    local tinyHole = createCylinder(0.1, 1)
    result = result:SubtractAsync({tinyHole})
end

-- BAD: Near-coplanar faces (z-fighting, artifacts)
local cut = createBox(10, 10, 0.001)  -- Too thin!

-- BAD: Many sequential single operations
for _, part in pairs(parts) do
    result = result:UnionAsync({part})  -- Slow!
end
```

### Do These Instead

```lua
-- GOOD: Batch operations
local allCuts = {}
for i = 1, 20 do
    table.insert(allCuts, createHole(positions[i]))
end
result = base:SubtractAsync(allCuts)

-- GOOD: Reasonable cut sizes
local cut = createBox(10, 10, 0.5)  -- Visible thickness

-- GOOD: Use CollisionFidelity.Box for non-gameplay parts
result.CollisionFidelity = Enum.CollisionFidelity.Box
```

### Async Considerations

```lua
-- Operations yield - don't spam
-- BAD:
for i = 1, 100 do
    result = result:UnionAsync({parts[i]})  -- 100 yields!
end

-- GOOD:
result = base:UnionAsync(parts)  -- Single yield
```

---

## Debugging CSG

### Visual Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Holes in mesh | Coplanar faces | Offset by 0.01+ |
| Z-fighting | Overlapping faces | Extend cuts through |
| Inside-out faces | Bad operation order | Check normals |
| Missing parts | Didn't intersect | Ensure overlap |

### Collision Issues

```lua
-- Show collision geometry in Studio:
-- View > Show > Decomposition Geometry

-- Or at runtime:
workspace:SetAttribute("ShowDecompositionGeometry", true)
```

### Fixing Bad Unions

```lua
-- If union has artifacts, try:
-- 1. Scale up parts slightly before operation
-- 2. Use SeparateAsync and re-union
-- 3. Recreate with offset positions
```

---

## Complete Example: Building Generator

```lua
local function createBuilding(config)
    local width = config.width or 20
    local height = config.height or 15
    local depth = config.depth or 20
    local windowSize = config.windowSize or Vector3.new(3, 4, 1)
    local windowSpacing = config.windowSpacing or 5
    local doorSize = config.doorSize or Vector3.new(4, 7, 1)

    -- Main structure
    local shell = Instance.new("Part")
    shell.Size = Vector3.new(width, height, depth)
    shell.Position = Vector3.new(0, height/2, 0)
    shell.Anchored = true

    -- Hollow interior
    local interior = Instance.new("Part")
    interior.Size = Vector3.new(width - 1, height - 1, depth - 1)
    interior.Position = shell.Position

    local building = shell:SubtractAsync({interior})

    -- Windows
    local windows = {}
    local windowY = 5
    while windowY < height - 3 do
        local windowX = -width/2 + windowSpacing
        while windowX < width/2 - windowSpacing do
            -- Front windows
            local w = Instance.new("Part")
            w.Size = windowSize
            w.Position = Vector3.new(windowX, windowY, -depth/2)
            table.insert(windows, w)

            -- Back windows
            local w2 = w:Clone()
            w2.Position = Vector3.new(windowX, windowY, depth/2)
            table.insert(windows, w2)

            windowX = windowX + windowSpacing
        end
        windowY = windowY + windowSpacing
    end

    if #windows > 0 then
        building = building:SubtractAsync(windows)
    end

    -- Door
    local door = Instance.new("Part")
    door.Size = doorSize
    door.Position = Vector3.new(0, doorSize.Y/2, -depth/2)

    building = building:SubtractAsync({door})

    -- Properties
    building.Anchored = true
    building.Material = Enum.Material.Concrete
    building.Color = Color3.fromRGB(200, 200, 200)
    building.CollisionFidelity = Enum.CollisionFidelity.Hull
    building.Parent = workspace

    return building
end

-- Usage
local office = createBuilding({
    width = 30,
    height = 20,
    depth = 25,
    windowSpacing = 6
})
```

---

## Quick Reference

### What To Build With CSG

| Object | Approach |
|--------|----------|
| Building | Box shell - interior - windows - door |
| Pipe | Cylinder - cylinder |
| Wheel | Cylinder - center hole - spoke holes |
| Bridge | Box deck ∪ supports - arch cutouts |
| Tunnel | Box - stretched cylinder |
| Stairs | Union stacked boxes |
| Ramp | Box ∪ wedge |
| Dome | Sphere ∩ box |
| Arch | Box - (box ∪ half-cylinder) |
| Frame | Box - box |
| Gear | Cylinder ∪ teeth - center hole |

### What NOT To Build With CSG

| Object | Why Not | Use Instead |
|--------|---------|-------------|
| Characters | Organic, needs animation | MeshPart + rig |
| Trees/plants | Organic, many polys | MeshPart |
| Cloth | Needs simulation | MeshPart |
| High detail | Polygon explosion | MeshPart |
| Smooth curves | Faceted result | MeshPart |

---

## CSG Thinking: Mental Models

Beyond recipes, here's how to **think** about solid modeling.

### Positive vs Negative Space

Every object is:
- **Positive space**: Material that exists
- **Negative space**: Voids, holes, cavities

```
A coffee mug:
├── Positive: Cylinder (body), Torus (handle)
└── Negative: Cylinder (cavity inside)

A window:
├── Positive: Wall exists
└── Negative: Rectangle removed
```

**Key insight**: Think "What's THERE vs what's MISSING" - expert modelers often think subtractive first.

### Silhouette Analysis

Look at object from 3 orthogonal axes:

```
        TOP (Y)
          │
          ▼
    ┌─────────┐
    │  Plan   │
    │  View   │
    └─────────┘

FRONT (Z)      SIDE (X)
    │              │
    ▼              ▼
┌───────┐    ┌───────┐
│ Front │    │ Side  │
│ View  │    │ View  │
└───────┘    └───────┘
```

Each silhouette suggests extrusions:
- Front silhouette → extrude along Z
- Side silhouette → extrude along X
- Top silhouette → extrude along Y

**Intersect all three = approximation of complex object**

---

## Decomposition Strategies

### Strategy A: Outside-In (Subtractive)

```
Start: Bounding box that contains entire object
Process: Carve away material until shape emerges

Best for:
├── Objects that fit in a box
├── Objects with holes/cavities
├── Architecture (walls with openings)
└── Sculpture-like objects

Mental model: Carving marble
```

### Strategy B: Inside-Out (Additive)

```
Start: Nothing
Process: Add pieces until complete

Best for:
├── Assemblies of distinct parts
├── Objects with protruding features
├── Mechanical systems
└── Modular constructions

Mental model: Building with Lego
```

### Strategy C: Skeleton-Based

```
Start: Central axis or spine
Process: Build volume around skeleton

Best for:
├── Elongated objects (pipes, beams, limbs)
├── Symmetric objects
├── Branching structures
└── Objects with clear "core"

Mental model: Adding flesh to bones
```

### Strategy D: Slice-Based

```
Start: 2D cross-section profile
Process: Extrude, sweep, or revolve the profile

Best for:
├── Objects with consistent cross-section
├── Revolution solids (vases, bowls, spindles)
├── Extruded profiles (beams, moldings)
└── Swept paths (curved pipes)

Mental model: Lathe or extrusion
```

---

## Operation Selection Logic

```
DECISION TREE:

Need to combine separate volumes?
└── YES → UNION

Need to remove material / make holes?
└── YES → SUBTRACT

Need only the overlapping region?
└── YES → INTERSECT

But also ask:
├── Can I avoid an operation entirely?
│   └── Repositioning primitives may achieve same result
├── Can I batch multiple operations?
│   └── Union all additions THEN subtract all cuts
└── Will this create valid geometry?
    └── Check for manifold issues
```

---

## Why Operations Fail: Topology

### Manifold vs Non-Manifold

```
MANIFOLD (valid):
├── Every edge shared by exactly 2 faces
├── Clear inside/outside distinction
├── Watertight surface
└── CSG operations work correctly

NON-MANIFOLD (problematic):
├── Edge shared by 0, 1, or 3+ faces
├── Ambiguous inside/outside
├── Has holes, dangling geometry
└── CSG operations may fail or produce artifacts
```

### Operations That Create Non-Manifold

```
TANGENT TOUCHING (edges align exactly)
    ┌───┐
    │   ├───┐     ← Edges touch but don't overlap
┌───┤   │   │       Result: ambiguous
│   │   │   │
└───┴───┴───┘

FIX: Ensure overlap, not just touching
    ┌───┐
    │ ┌─┼─┐       ← Volumes actually intersect
┌───┼─┼─┼─│       Result: clean boolean
│   │ │ │ │
└───┴─┴─┴─┘

COPLANAR FACES (same plane)
    ┌───────┐
    │       │     ← Cut stops exactly at surface
    │   ┌───┤       Result: z-fighting, holes
    │   │   │
    └───┴───┘

FIX: Extend cuts THROUGH the object
    ┌───────┐
    │       │
    │ ┌─────┼──   ← Cut extends beyond surface
    │ │     │       Result: clean cut
    └─┴─────┘
```

### The Golden Rule

**Always extend subtractive geometry through and beyond the target surface.**

---

## Level of Detail Decisions

```
QUESTION: How much detail does this object need?

FACTORS:

1. View Distance
   ├── Far (>100 studs): Only silhouette matters
   ├── Medium (20-100): Major features visible
   └── Close (<20): Fine details matter

2. Purpose
   ├── Visual only: Can be complex
   ├── Collision: Should be simplified
   └── Both: Balance needed

3. Quantity
   ├── Unique hero prop: High detail OK
   └── Repeated 100+ times: Minimize polys

4. Generation Time
   ├── Pre-built in Studio: Complex OK
   └── Runtime generated: Keep simple

DECISION:

                    High Detail
                         │
    Hero prop ───────────┼─────────── Background prop
    Close-up             │             Distant
    Unique               │             Repeated
    Pre-built            │             Runtime
                         │
                    Low Detail
```

---

## Parametric Thinking

Don't hardcode dimensions - use configuration:

```lua
-- BAD: Magic numbers everywhere
local hole = createCylinder(2.5, 10)
hole.Position = Vector3.new(3.7, 0, 4.2)

-- GOOD: Parametric and reusable
local function createBoltPattern(config)
    local boltRadius = config.boltRadius or 0.5
    local boltCount = config.boltCount or 6
    local patternRadius = config.patternRadius or 3
    local plateThickness = config.plateThickness or 1

    local holes = {}
    for i = 0, boltCount - 1 do
        local angle = i * (math.pi * 2 / boltCount)
        local hole = createCylinder(boltRadius, plateThickness * 1.1)
        hole.Position = Vector3.new(
            math.cos(angle) * patternRadius,
            0,
            math.sin(angle) * patternRadius
        )
        table.insert(holes, hole)
    end
    return holes
end

-- Now reusable with different configs
local smallPattern = createBoltPattern({boltCount = 4, patternRadius = 2})
local largePattern = createBoltPattern({boltCount = 8, patternRadius = 5})
```

**Benefits:**
- Reusable across projects
- Easy to adjust and iterate
- Self-documenting (config keys explain purpose)
- Testable with different inputs

---

## Reference Analysis Workflow

When asked to "build X", follow this process:

### 1. OBSERVE

```
├── What are the major volumes?
│   └── Break down into largest recognizable shapes
├── What are the negative spaces?
│   └── Identify all holes, cavities, cutouts
├── What symmetry exists?
│   └── Can I build half and mirror?
└── What's the simplest bounding shape?
    └── Box? Cylinder? Sphere?
```

### 2. DECOMPOSE

```
├── Map each feature to a primitive
│   └── "This curved part = sphere intersection"
├── Identify operation types
│   └── "These holes = subtracts, this extension = union"
├── Determine dependencies
│   └── "Must create body before cutting windows"
└── Group related operations
    └── "All bolt holes can be one subtract"
```

### 3. SIMPLIFY

```
├── Can two operations become one?
│   └── Batch unions, batch subtracts
├── Can detail be omitted?
│   └── Will anyone notice from gameplay distance?
├── Can a complex shape approximate?
│   └── Cylinder instead of 12-sided polygon
└── Is CSG even the right approach?
    └── Maybe MeshPart for this one
```

### 4. IMPLEMENT

```
├── Build sub-assemblies first
│   └── Test each component independently
├── Batch similar operations
│   └── All unions, then all subtracts
├── Apply materials/colors appropriately
│   └── Set on main part before operations
└── Verify collision and visuals
    └── Test in context
```

---

## Example: Analyzing a Chair

```
OBSERVATION:
├── Seat: Flat rectangular volume
├── Back: Flat rectangular volume, angled
├── Legs: 4 vertical cylinders (or boxes)
└── Negative: Open space under seat, between legs

DECOMPOSITION OPTIONS:

Option A: Pure Additive
    seat ∪ back ∪ leg1 ∪ leg2 ∪ leg3 ∪ leg4

    Pros: Simple, clear
    Cons: Many operations (6 parts)

Option B: Subtractive from Block
    solidBlock - underSeatVoid - behindBackVoid - legGaps

    Pros: Might be fewer operations
    Cons: Complex void shapes, more triangles

Option C: Hybrid
    (seat ∪ back) as one L-shaped piece
    then ∪ legs

    Pros: Reduces operations
    Cons: L-shape might need subtract anyway

DECISION FACTORS:
├── Chair style: Modern (boxy) vs Classic (curved)
├── Leg shape: Round legs = cylinders, Square = boxes
├── Detail level: Cushion? Armrests? Carved details?
└── Quantity: One chair or 50 chairs?

LIKELY BEST: Option A for simple chair
    - Clear and maintainable
    - Each part can have different material
    - Easy to adjust proportions
```

---

## The Fundamental Trade-off

```
ACCURACY ◄────────────────────────────► PERFORMANCE

More operations                         Fewer operations
More primitives                         Simpler shapes
Precise collision                       Box collision
Higher triangle count                   Lower triangle count
Longer generation time                  Faster generation

     │                                        │
     ▼                                        ▼
Hero props                              Background/repeated
Close-up items                          Distant items
Gameplay-critical collision             Visual-only props
Design-time generation                  Runtime generation
```

**There is no "correct" answer - only appropriate trade-offs for your context.**
