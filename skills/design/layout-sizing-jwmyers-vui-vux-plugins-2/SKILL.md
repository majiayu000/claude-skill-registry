---
name: layout-sizing
description: This skill should be used when the user asks about "layout", "sizing", "coordinates", "1920x1080", "world units", "PPU", "pixels per unit", "SVG import", "texture size", "grid positioning", "screen dimensions", "camera", "orthographic size", "reserve zones", "LayoutConfig", or discusses Board display layout and sprite sizing.
version: 0.3.0
---

# Board Layout and Sizing

Expert knowledge of Board display layout, coordinate systems, SVG import settings, and sprite sizing for the 1920×1080 Board hardware.

## Display Configuration

### Target Display

| Metric | Pixels | World Units (100 PPU) |
| ------ | ------ | --------------------- |
| Width  | 1920   | 19.2                  |
| Height | 1080   | 10.8                  |

### Camera Settings

| Setting           | Value       |
| ----------------- | ----------- |
| Orthographic Size | **5.4**     |
| Position          | (0, 0, -10) |
| Aspect Ratio      | 16:9        |

**Calculation**: `Visible Height = orthoSize × 2 = 10.8 world units`

## Horizontal Layout (19.2 world units)

```text
|  Blue UI  | Blue Res | Buffer |   5×5 Grid   | Buffer | Red Res |  Red UI  |
|    2.1    |   2.0    |  0.5   |     10.0     |  0.5   |   2.0   |   2.1    |
```

### Zone Coordinates

| Zone              | Left     | Right    | Center  | Width    |
| ----------------- | -------- | -------- | ------- | -------- |
| Blue UI           | -9.6     | -7.5     | -8.55   | 2.1      |
| Blue Reserve      | -7.5     | -5.5     | -6.5    | 2.0      |
| Left Buffer       | -5.5     | -5.0     | —       | 0.5      |
| **Playable Grid** | **-5.0** | **+5.0** | **0.0** | **10.0** |
| Right Buffer      | +5.0     | +5.5     | —       | 0.5      |
| Red Reserve       | +5.5     | +7.5     | +6.5    | 2.0      |
| Red UI            | +7.5     | +9.6     | +8.55   | 2.1      |

### Reserve Pool Purpose

- Holds drawn tiles before placement (visible to both players)
- Up to **3 tiles per player** maximum
- Tiles can be **stolen** from opponent's reserve

## Vertical Layout (10.8 world units)

| Zone          | Bottom | Top  | Height |
| ------------- | ------ | ---- | ------ |
| Bottom Margin | -5.4   | -5.0 | 0.4    |
| Playable Grid | -5.0   | +5.0 | 10.0   |
| Top Margin    | +5.0   | +5.4 | 0.4    |

## LayoutConfig Reference

All layout constants centralized in `Assets/Scripts/Config/LayoutConfig.cs`:

```csharp
public static class LayoutConfig
{
    // Screen dimensions
    public const float ScreenWidth = 19.2f;
    public const float ScreenHeight = 10.8f;

    // Tile and grid
    public const float TileSize = 2.0f;
    public const int GridSize = 5;

    // Grid boundaries
    public const float GridLeft = -5.0f;
    public const float GridRight = 5.0f;
    public const float GridBottom = -5.0f;
    public const float GridTop = 5.0f;

    // Camera
    public const float CameraOrthoSize = 5.4f;

    // Reserve zones
    public const float BlueReserveCenter = -6.5f;
    public const float RedReserveCenter = 6.5f;
}
```

## Grid Positioning

### Grid to World Conversion

```csharp
// Grid (0,0) to (4,4) maps to world coordinates
float x = LayoutConfig.GridLeft + (gridX * LayoutConfig.TileSize) + (LayoutConfig.TileSize / 2f);
float y = LayoutConfig.GridBottom + (gridY * LayoutConfig.TileSize) + (LayoutConfig.TileSize / 2f);
```

### Key Grid Positions

| Grid   | World Center | Description            |
| ------ | ------------ | ---------------------- |
| (0, 0) | (-4, -4)     | Bottom-left            |
| (2, 2) | (0, 0)       | Center (starting tile) |
| (4, 4) | (4, 4)       | Top-right              |
| (0, 4) | (-4, 4)      | Top-left               |
| (4, 0) | (4, -4)      | Bottom-right           |

## SVG Import Settings

### THE GOLDEN RULE

```text
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   WORLD SIZE = TEXTURE SIZE ÷ PIXELS PER UNIT                 ║
║                                                               ║
║   ALWAYS use PPU = 100. Adjust Texture Size for world size.   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Formula**: `Texture Size = Desired World Size × 100`

### Standard Settings

| Asset      | Desired World Size | Texture Size | PPU |
| ---------- | ------------------ | ------------ | --- |
| **Tiles**  | 2.0                | **200**      | 100 |
| **Tokens** | 0.4 (20% of tile)  | **40**       | 100 |

### Import Steps

1. Select SVG file(s) in Project window
2. In Inspector:
   - Generated Asset Type: **Texture2D**
   - Texture Size: **(calculated value)**
   - Pixels Per Unit: **100**
3. Click **Apply**

### Common Mistakes

| Mistake                    | Consequence          | Solution                        |
| -------------------------- | -------------------- | ------------------------------- |
| Changing PPU               | Inconsistent sizing  | Always PPU = 100                |
| Default Texture Size (256) | Wrong world size     | Calculate: WorldSize × 100      |
| Matching viewBox           | Irrelevant to sizing | Set based on desired world size |

## Rendering Order

Higher sorting order = renders in front.

| Layer         | Sorting Order | Content                     |
| ------------- | ------------- | --------------------------- |
| Background    | -10           | Solid color (#0D0F14)       |
| Tiles         | 0             | TileView sprites            |
| Grid Glow     | 1             | Wide semi-transparent lines |
| Grid Core     | 2             | Thin bright lines           |
| Reserve Lines | 1             | Zone boundaries             |
| Tokens        | 10            | TokenView sprites           |

### Grid Visibility

Grid MUST have higher sorting order than tiles (1-2 vs 0) to appear above them.

## Player Orientation

Players sit facing each other:

- **Blue player**: Views from LEFT side (x < 0)
- **Red player**: Views from RIGHT side (x > 0)

UI text rotation:

- Blue UI: Normal rotation (readable from left)
- Red UI: Rotated 180° (readable from right)

## Edge Node Positions

Each tile has 4 edge nodes at side midpoints:

| Node   | Offset from Tile Center |
| ------ | ----------------------- |
| Top    | (0, +1.0)               |
| Right  | (+1.0, 0)               |
| Bottom | (0, -1.0)               |
| Left   | (-1.0, 0)               |

### Token Snapping

- `NodeSnapDistance = 0.5` world units (appropriate for TokenSize = 0.4)
- Tokens snap to the nearest edge node within snap distance

### EdgeNode and Tile Rotation

EdgeNode values (`Top`, `Right`, `Bottom`, `Left`) are **tile-local coordinates** that rotate with the tile:

```csharp
// Rotate edge node by rotation steps (each step = 90 degrees clockwise)
public static EdgeNode RotateEdge(EdgeNode node, int rotationSteps)
{
    return (EdgeNode)(((int)node + rotationSteps) % 4);
}

// Example: A path from Left to Top on an unrotated tile
// After 1 rotation step (90 CW): becomes Bottom to Right
```

**Center Tile Special Case:**

- Center tile (game-tile-13) is the ONLY tile that cannot rotate
- Blue Attack starts on Left node, Red Attack starts on Right node
- These starting positions are fixed and hardcoded per game rules

## Coordinate System Summary

```text
                    World Y
                       ↑
                       |  +5.4 (screen top)
                       |  +5.0 (grid top)
                       |
-9.6 ←─────────────────┼─────────────────→ +9.6  World X
                       |
                       |  -5.0 (grid bottom)
                       |  -5.4 (screen bottom)
                       ↓
```

## Troubleshooting

### Camera not showing full screen

**Cause**: Wrong orthographic size
**Solution**: Set `Camera → Orthographic Size = 5.4`

### Tiles too large/small

**Cause**: Wrong SVG Texture Size
**Solution**: `Texture Size = World Size × 100`

- Tiles: 200 (2.0 × 100)
- Tokens: 40 (0.4 × 100)

### Grid lines hidden behind tiles

**Cause**: Sorting order wrong
**Solution**: Grid sorting order (1-2) must be higher than tiles (0)

### Sprites not aligning

**Cause**: Not using LayoutConfig
**Solution**: Always use `LayoutConfig` constants for positioning

## Why 5×5 Grid?

- **Balanced gameplay**: Enough space for strategy, small enough for quick games
- **Fits display**: 10.0 world units fills the 1920×1080 display with room for UI
- **Network aesthetic**: 5×5 creates interconnected network paths matching cybersecurity theme

## Reference Files

This skill's `references/` folder contains:

| File                     | Contains                                | Read When                          |
| ------------------------ | --------------------------------------- | ---------------------------------- |
| `coordinate-systems.md`  | Grid, World, Screen conversion formulas | Implementing coordinate transforms |
| `layout-config.md`       | All LayoutConfig constants and values   | Need exact constant values         |
| `svg-import-settings.md` | PPU=100 rule, Texture Size formula      | Importing new SVG assets           |
| `player-zones.md`        | Reserve pools, hand areas, stealing     | Implementing reserve functionality |

## Key Source Files

| File                                    | Purpose              |
| --------------------------------------- | -------------------- |
| `Assets/Scripts/Config/LayoutConfig.cs` | All layout constants |

## Quick Reference

```text
PPU = 100 (ALWAYS)
Texture Size = World Size × 100
NodeSnapDistance = 0.5 world units

Tiles:  2.0 world units → Texture Size = 200
Tokens: 0.4 world units → Texture Size = 40
```
