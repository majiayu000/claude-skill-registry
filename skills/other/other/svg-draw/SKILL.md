---
name: svg-draw
description: Create SVG images and convert them to PNG without external graphics libraries. Use when you need to generate custom illustrations, avatars, or artwork (e.g., "draw a dragon", "create an avatar", "make a logo") or convert SVG files to PNG format. This skill works by writing SVG text directly (no PIL/ImageMagick required) and uses system rsvg-convert for PNG conversion.
---

# SVG Draw

Generate vector graphics and raster images using pure SVG code and system conversion tools.

## Quick Start

**For new drawings:**
1. Write SVG code directly to a file (use templates in `assets/` as starting points)
2. Convert to PNG using the conversion script
3. Send via the appropriate channel (DingTalk, Telegram, etc.)

**For existing SVG files:**
1. Use the conversion script to convert SVG → PNG
2. Share the resulting image

## Creating SVG Images

### Basic Workflow

1. **Choose or create a template**
   - Check `assets/` for existing templates (dragon, lobster, etc.)
   - Or write SVG from scratch

2. **Write the SVG file**
   ```bash
   # Example: Write SVG to file
   write('/path/to/output.svg', svg_content)
   ```

3. **Convert to PNG**
   ```bash
   /root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh input.svg output.png 400 400
   ```

### SVG Structure Tips

**Always include:**
- `<svg>` tag with `xmlns="http://www.w3.org/2000/svg"` and `viewBox`
- Background `<rect>` (prevents transparent backgrounds)
- Appropriate `width` and `height` attributes

**Common SVG elements:**
- Shapes: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`
- Text: `<text>` with `text-anchor="middle"` for centering
- Colors: Use hex codes or named colors
- Opacity: Add `opacity` attribute for transparency effects

**Example character structure:**
```
Background → Body → Head → Face features → Limbs → Accessories → Name
```

## Converting SVG to PNG

Use the bundled conversion script:

```bash
/root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh <input.svg> <output.png> [width] [height]
```

**Parameters:**
- `input.svg`: Source SVG file path
- `output.png`: Destination PNG file path
- `width`: Output width in pixels (default: 400)
- `height`: Output height in pixels (default: 400)

**Example:**
```bash
/root/.openclaw/workspace/skills/svg-draw/scripts/svg_to_png.sh dragon.svg dragon.png 512 512
```

## Available Templates

### Dragon Template (`assets/dragon_template.svg`)
Blue dragon with:
- Serpentine body with wings
- Golden eyes with highlights
- Horns and pointed ears
- Curved tail
- Magical sparkles
- Name label: "大龙 🐉"

**Customization ideas:**
- Change `fill="#4a90d9"` for different body colors
- Adjust eye color by modifying `fill="#ffcc00"`
- Add/remove features (scales, fire, etc.)
- Change background color

### Lobster Template (`assets/lobster_template.svg`)
Red lobster with:
- Orange-red shell with segments
- Large claws (left and right)
- Eight walking legs
- Eyes on stalks
- Long antennae
- Tail fan
- Ocean bubbles background
- Name label: "大龙虾 🦞"

**Customization ideas:**
- Adjust shell color: `fill="#e85d04"` (darker red) or `fill="#f48c06"` (orange)
- Change claw size or position
- Add more bubbles
- Modify background

## Design Guidelines

### Color Palettes

**Friendly/Cute:**
- Body: `#4a90d9` (blue), `#f48c06` (orange)
- Accents: `#ffcc00` (yellow), `#ff6b6b` (coral)
- Background: `#1a1a2e` (dark blue)

**Professional:**
- Use muted tones
- Stick to 2-3 main colors
- Add subtle gradients if needed

### Character Design Principles

1. **Keep it simple** — Too many details look messy at small sizes
2. **Use contrast** — Light features on dark backgrounds
3. **Add personality** — Eyes, expressions, small details
4. **Include a label** — Add name/title at the bottom for context
5. **Test at target size** — View at 400x400 to check readability

## Common Tasks

### Creating an Avatar

1. Start with a template that matches the vibe (dragon, lobster, etc.)
2. Modify colors and features
3. Add personal touches (accessories, expressions)
4. Add name label at bottom
5. Convert and send

### Making a Logo

1. Use simple geometric shapes
2. Limit to 2-3 colors
3. Consider scalable design
4. Test at multiple sizes
5. Export at higher resolution (800x800 or 1024x1024)

### Customizing Templates

**Change colors:** Find `fill="#"` or `stroke="#"` attributes and replace the hex codes

**Resize elements:** Adjust `rx`, `ry` (ellipses) or `width`, `height` (rectangles)

**Reposition:** Modify `cx`, `cy` (circles/ellipses) or `x`, `y` (rectangles)

**Add text:**
```xml
<text x="200" y="370" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#ffcc00" text-anchor="middle">Your Text</text>
```

## Resources

### scripts/
- `svg_to_png.sh` - Convert SVG to PNG using rsvg-convert

### assets/
- `dragon_template.svg` - Friendly blue dragon
- `lobster_template.svg` - Cute red lobster

## Troubleshooting

**SVG not rendering:**
- Check for proper `<svg>` tag with `xmlns` attribute
- Ensure `viewBox` is set correctly
- Verify all tags are closed

**Conversion fails:**
- Confirm `rsvg-convert` is installed: `which rsvg-convert`
- Check file paths are correct
- Verify SVG syntax is valid

**Image looks wrong:**
- Test SVG in browser first
- Check coordinate system (viewBox vs width/height)
- Verify element stacking order (later elements draw on top)
