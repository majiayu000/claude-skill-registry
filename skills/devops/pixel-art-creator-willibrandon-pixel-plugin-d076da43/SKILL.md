---
name: pixel-art-creator
description: Create new pixel art sprites from scratch with canvas creation, layer
  management, and basic drawing primitives. Use when the user wants to create a sprite,
  draw pixel art, make a new canvas, start a n
---

---
name: Pixel Art Creator
description: Create new pixel art sprites from scratch with canvas creation, layer management, and basic drawing primitives. Use when the user wants to create a sprite, draw pixel art, make a new canvas, start a new image, begin a new project, or mentions pixel dimensions like "64x64", "32x32 sprite", "128 by 128", "16 pixel icon". Trigger on: "create", "new", "make", "draw", "sprite", "canvas", "image", "icon", "tile", "character", "background", dimensions (WxH), "from scratch", "blank canvas", "empty sprite", "Game Boy", "NES", "retro", color mode mentions ("RGB", "indexed", "grayscale"). Also use for drawing basic shapes like "circle", "rectangle", "line", "pixel", "fill", "outline".
allowed-tools: Read, Bash, mcp__aseprite__create_canvas, mcp__aseprite__add_layer, mcp__aseprite__delete_layer, mcp__aseprite__get_sprite_info, mcp__aseprite__draw_pixels, mcp__aseprite__draw_line, mcp__aseprite__draw_rectangle, mcp__aseprite__draw_circle, mcp__aseprite__draw_contour, mcp__aseprite__fill_area, mcp__aseprite__set_palette, mcp__aseprite__get_palette
---

# Pixel Art Creator

## Overview

This Skill enables creation of new pixel art sprites with full control over canvas properties, layers, and basic drawing operations. It's the foundational Skill for all pixel art workflows.

## When to Use

Use this Skill when the user:
- Wants to "create a sprite" or "make pixel art"
- Mentions sprite dimensions (e.g., "64x64", "32 by 32", "128 pixels wide")
- Asks to "draw" basic shapes (pixels, lines, rectangles, circles)
- Needs to set up a canvas or layers
- Mentions color modes (RGB, Grayscale, Indexed)

**Trigger Keywords:** create, sprite, canvas, draw, pixel art, dimensions, layer, new sprite

## Instructions

### 1. Creating a Canvas

When the user requests a sprite, create the canvas first:

**Color Modes:**
- **RGB**: Full color (24-bit), best for modern pixel art
- **Grayscale**: Shades of gray only, for monochrome art
- **Indexed**: Limited palette (1-256 colors), for retro game art

**Recommended Sizes:**
- **Icons**: 16x16, 24x24, 32x32
- **Characters**: 32x32, 48x48, 64x64
- **Tiles**: 16x16, 32x32, 64x64
- **Scenes**: 128x128, 256x256, 320x240 (retro resolution)

Use `mcp__aseprite__create_canvas` with parameters:
- `width`: 1-65535 pixels
- `height`: 1-65535 pixels
- `color_mode`: "RGB", "Grayscale", or "Indexed"

### 2. Managing Layers

**Adding Layers:**
Use `mcp__aseprite__add_layer` to organize sprite elements:
- Background layer for solid colors or backgrounds
- Character layer for main subject
- Effects layer for highlights, shadows, outlines
- Detail layer for accessories or fine details

**Layer Workflow:**
1. Create canvas
2. Add named layers (e.g., "Background", "Character", "Effects")
3. Draw on specific layers
4. Use layers for organization and editing flexibility

**Important:** Cannot delete the last layer in a sprite.

### 3. Drawing Primitives

**Draw Individual Pixels:**
Use `mcp__aseprite__draw_pixels` for precise pixel placement:
- Supports batch operations (multiple pixels at once)
- Accepts colors in hex format (#RRGGBB) or palette indices
- Can snap to nearest palette color (for Indexed mode)

Example:
```
Draw pixels at coordinates:
- (10, 10) in red (#FF0000)
- (11, 10) in red (#FF0000)
- (12, 10) in red (#FF0000)
```

**Draw Lines:**
Use `mcp__aseprite__draw_line`:
- Straight lines between two points
- Useful for outlines, edges, connecting points

**Draw Rectangles:**
Use `mcp__aseprite__draw_rectangle`:
- Filled or outline mode
- Perfect for backgrounds, UI elements, platforms

**Draw Circles/Ellipses:**
Use `mcp__aseprite__draw_circle`:
- Filled or outline mode
- For round objects, planets, effects

**Draw Contours (Polylines/Polygons):**
Use `mcp__aseprite__draw_contour`:
- Connect multiple points
- Useful for complex shapes, terrain, irregular outlines

**Flood Fill:**
Use `mcp__aseprite__fill_area`:
- Fill connected pixels of the same color
- Like a paint bucket tool
- Great for filling large areas quickly

### 4. Working with Colors

**Setting Colors:**
- **Hex Format**: #RRGGBB (e.g., #FF0000 for red)
- **RGB**: Specify red, green, blue values (0-255)
- **Palette Index**: For Indexed mode (0-255)

**Common Colors:**
- Red: #FF0000
- Green: #00FF00
- Blue: #0000FF
- Yellow: #FFFF00
- Cyan: #00FFFF
- Magenta: #FF00FF
- Black: #000000
- White: #FFFFFF

**Color Palettes:**
For Indexed color mode, set the palette first:
- Use `mcp__aseprite__set_palette` with array of hex colors
- Example: ["#000000", "#FFFFFF", "#FF0000", "#00FF00"]

### 5. Workflow Best Practices

**Typical Creation Workflow:**
1. **Understand Requirements**
   - What size sprite?
   - What color mode?
   - What style (modern vs retro)?

2. **Create Canvas**
   - Choose appropriate dimensions
   - Select color mode (RGB for modern, Indexed for retro)

3. **Set Up Layers** (optional but recommended)
   - Add layers for organization
   - Name layers descriptively

4. **Set Palette** (for Indexed mode)
   - Define limited color palette
   - Use retro-appropriate palettes (NES: 16 colors, Game Boy: 4 colors)

5. **Draw Basic Shapes**
   - Start with outline
   - Fill with colors
   - Add details

6. **Verify Result**
   - Use `mcp__aseprite__get_sprite_info` to check properties
   - Describe what was created to user

7. **Prepare for Export** (if requested)
   - Hand off to pixel-art-exporter Skill

## Examples

### Example 1: Simple Sprite

**User Request:** "Create a 32x32 sprite with a red circle"

**Approach:**
1. Create 32x32 RGB canvas
2. Draw filled circle in center (radius 12) in red
3. Confirm creation

### Example 2: Layered Sprite

**User Request:** "Make a 64x64 sprite with a blue background and a yellow character"

**Approach:**
1. Create 64x64 RGB canvas
2. Add layer "Background"
3. Fill entire canvas with blue (#0000FF) on Background layer
4. Add layer "Character"
5. Draw yellow (#FFFF00) rectangle or shape on Character layer
6. Confirm layers and contents

### Example 3: Indexed Color Sprite

**User Request:** "Create a 48x48 Game Boy style sprite"

**Approach:**
1. Create 48x48 Indexed canvas
2. Set Game Boy palette: ["#0F380F", "#306230", "#8BAC0F", "#9BBC0F"]
3. Draw using 4-color palette
4. Use pixel-perfect drawing

### Example 4: Complex Shape

**User Request:** "Draw a pixelated tree on a 64x64 canvas"

**Approach:**
1. Create 64x64 RGB canvas
2. Draw brown (#8B4513) rectangle for trunk (using draw_rectangle)
3. Draw green (#228B22) irregular shape for foliage (using draw_contour or multiple rectangles)
4. Add details with individual pixels
5. Describe the tree to user

## Technical Details

### Canvas Properties
- **Width/Height**: 1-65535 pixels (practical limit usually <1024)
- **Color Modes**:
  - RGB: 24-bit color (16.7 million colors)
  - Grayscale: 8-bit (256 shades of gray)
  - Indexed: 1-256 colors from palette

### Drawing Coordinates
- Origin (0, 0) is top-left corner
- X increases rightward
- Y increases downward

### Performance
- Batch pixel operations when possible
- Drawing operations complete in <100ms typically
- Large canvases (>512x512) may take slightly longer

### Limitations
- Cannot create canvas smaller than 1x1
- Cannot create canvas larger than 65535x65535 (practical limit much lower)
- Cannot delete last layer
- Indexed mode palette limited to 256 colors maximum

## Common Patterns

### Pattern: Quick Sprite
For simple requests like "create a sprite":
- Default to 64x64 RGB canvas
- Add basic shape or placeholder
- Ask user for refinements

### Pattern: Retro Game Sprite
For retro-style requests:
- Use Indexed color mode
- Set appropriate palette (NES, Game Boy, C64, etc.)
- Use limited colors and pixel-perfect drawing

### Pattern: Icon Creation
For icon requests:
- Use 16x16, 24x24, or 32x32 dimensions
- RGB mode for modern icons
- Simple, recognizable shapes
- High contrast colors

## Integration with Other Skills

- **Hand off to pixel-art-animator** when user mentions "animation", "frames", or "movement"
- **Hand off to pixel-art-professional** when user asks for "dithering", "shading", or "palette refinement"
- **Hand off to pixel-art-exporter** when user asks to "export", "save", or mentions file formats

## Error Handling

**If canvas creation fails:**
- Check dimensions are valid (1-65535)
- Verify color mode is spelled correctly
- Suggest alternative dimensions if too large

**If drawing fails:**
- Verify coordinates are within canvas bounds
- Check color format is valid hex (#RRGGBB)
- For Indexed mode, ensure palette is set first

**If layer operations fail:**
- Cannot delete last layer (inform user)
- Layer names should be descriptive strings

## Success Indicators

You've successfully used this Skill when:
- Canvas created with correct dimensions and color mode
- Drawing operations complete without errors
- User can see or understand what was created
- Sprite is ready for next steps (animation, export, refinement)
