---
name: interior-design-expert
description: Expert interior designer with deep knowledge of space planning, color theory (Munsell, NCS), lighting design (IES standards), furniture proportions, and AI-assisted visualization. Use for room layout optimization, lighting calculations, color palette selection for interiors, furniture placement, style consultation. Activate on "interior design", "room layout", "lighting design", "furniture placement", "space planning", "Munsell color". NOT for exterior/landscape design, architectural structure, web/UI design (use web-design-expert), brand color theory (use color-theory-palette-harmony-expert), or building codes/permits.
allowed-tools: Read,Write,Edit,mcp__stability-ai__stability-ai-generate-image
category: Design & Creative
tags:
  - interior
  - lighting
  - furniture
  - space-planning
  - color
pairs-with:
  - skill: color-theory-palette-harmony-expert
    reason: Color decisions for interiors
  - skill: fancy-yard-landscaper
    reason: Indoor-outdoor cohesion
---

# Interior Design Expert

Expert interior designer combining classical training with computational design tools and AI-assisted visualization.

## When to Use This Skill

✅ **Use for:**
- Room layout optimization and furniture placement
- Lighting design calculations (IES standards)
- Color palette selection using Munsell/NCS systems
- Space planning with anthropometric considerations
- Style consultation (Mid-Century, Scandinavian, Japandi, etc.)
- AI-assisted room visualization with Stability AI/Ideogram
- Furniture proportion and scale analysis
- Circulation path planning

❌ **Do NOT use for:**
- Exterior/landscape design → different domain
- Architectural structural changes → requires licensed architect
- Web/UI color design → use **web-design-expert**
- Brand/marketing color theory → use **color-theory-palette-harmony-expert**
- Building codes/permits → consult local regulations
- Kitchen/bath detailed cabinetry → specialized trades
- 3D modeling implementation → use SketchUp directly

## MCP Integrations

### Available MCPs

| MCP | Purpose |
|-----|---------|
| **Stability AI** | Generate photorealistic room renders |
| **Ideogram** | Create room visualizations with text control |
| **SketchUp MCP** (if configured) | Direct 3D modeling control |

### Room Visualization Workflow
```
1. Establish room parameters (dimensions, style, colors)
2. Use mcp__stability-ai__stability-ai-generate-image for renders
3. Or use mcp__ideogram__generate_image for concept exploration
4. Iterate based on feedback
```

## Common Anti-Patterns

### Anti-Pattern: Ignoring Traffic Flow
**What it looks like**: Furniture blocking natural pathways, awkward circulation
**Why it's wrong**: Rooms feel cramped, daily use becomes frustrating
**What to do instead**: Map circulation paths first, then place furniture. Primary paths: 900-1200mm. Secondary: 600-900mm.

### Anti-Pattern: Single Light Source
**What it looks like**: One overhead light illuminating entire room
**Why it's wrong**: Creates harsh shadows, unflattering light, no ambiance
**What to do instead**: Layer lighting: ambient + task + accent. See `/references/lighting-design.md`.

### Anti-Pattern: Scale Mismatch
**What it looks like**: Oversized sectional in small room, tiny rug under large furniture
**Why it's wrong**: Proportions feel "off," space reads awkwardly
**What to do instead**: Measure room, calculate proportions. Rugs should extend under front legs of furniture at minimum.

### Anti-Pattern: Paint Color from Memory
**What it looks like**: Selecting paint without testing in actual lighting conditions
**Why it's wrong**: Metamerism - colors shift dramatically under different light sources
**What to do instead**: Always test paint samples in YOUR lighting, at different times of day.

## Core Knowledge Areas

### Color Science (Munsell System)

Interior design uses **Munsell notation**: Hue Value/Chroma (e.g., 5R 5/14)
- **Hue**: 10 major hues in a circle (R, YR, Y, GY, G, BG, B, PB, P, RP)
- **Value**: Lightness 0-10 (black to white)
- **Chroma**: Saturation 0-max (gray to vivid)

**Why Munsell for interiors**: Perceptually uniform, paint companies use it, predicts color interactions.

**Key concept**: Metamerism - colors match under one light but differ under another. Always test in YOUR lighting.

→ See `/references/color-science.md` for harmony calculations, palette examples

### Lighting Design (IES Standards)

**Layer lighting for success:**
1. **Ambient** (60-70%): Overall illumination - recessed, chandeliers
2. **Task** (2-3x ambient): Specific activities - desk lamps, under-cabinet
3. **Accent** (3-5x ambient): Drama - track, picture lights
4. **Natural**: Free daylight - control glare with shades

**Key illuminance levels:**
- Living general: 150-300 lux
- Reading/detail: 300-500 lux
- Kitchen counters: 300-750 lux
- Bedroom general: 50-150 lux

**Color temperature by time:**
- Morning: 5000-6500K (alertness)
- Midday: 4000-5000K (productivity)
- Evening: 2700-3000K (relaxation)
- Night: 2200-2700K (melatonin)

→ See `/references/lighting-design.md` for IES tables, CCT programming

### Space Planning

**Circulation minimums:**
- Primary paths: 900-1200mm (main halls, living paths)
- Secondary: 600-900mm (between furniture)
- Squeeze points: 450mm minimum (not regular use)

**Furniture clearances:**
- Sofa to coffee table: 450-500mm
- Dining chair push-back: 900mm
- Bed side clearance: 600mm minimum

**Proportion systems:**
- Golden ratio (φ = 1.618): Room proportions, art placement
- Root rectangles: √2 (1:1.414) common in floor plans
- Double square (1:2): Classic rug proportions

→ See `/references/space-planning.md` for anthropometrics, constraint solver code

### Style Reference

**Major styles:**
- **Mid-Century Modern** (1945-70): Organic curves, tapered legs, mustard/teal/walnut
- **Scandinavian**: Light wood, hygge, white/gray/blonde, maximize natural light
- **Japandi**: Wabi-sabi meets hygge, low furniture, earth tones, negative space
- **Maximalist**: Curated abundance, bold colors, pattern mixing

→ See `/references/style-guide.md` for full style DNA breakdowns

## AI Visualization Prompts

### Room Render Structure
```
[Style] [room type] interior, [key features],
[color palette], [lighting quality],
[materials/textures], [mood/atmosphere],
[photography style], [technical specs]
```

### Example - Scandinavian Living Room
```
Scandinavian modern living room interior,
large floor-to-ceiling windows with sheer curtains,
white walls with warm oak wood accents,
gray boucle sofa with sheepskin throws,
natural daylight streaming in, soft shadows,
matte plaster walls, natural linen textiles,
cozy hygge atmosphere,
architectural photography, wide angle lens,
8k resolution, photorealistic
```

### Negative Prompts
```
cluttered, messy, dark, oversaturated,
cartoon, illustration, low quality, watermark
```

## Essential Reading

- Ching, F. (2014). *Interior Design Illustrated*
- Pile, J. (2013). *A History of Interior Design*
- IES (2021). *The Lighting Handbook* (11th ed.)
- Munsell, A. (1905). *A Color Notation*

## Tools & Resources

- **Munsell Color Charts** (physical) - essential for palette work
- **Benjamin Moore Color Portfolio** - ties to Munsell
- **DIALux** - lighting calculation software (free)
- **SketchUp + V-Ray** - visualization
- **Planner 5D / RoomGPT** - AI-assisted quick concepts

---

**Technical references for deep dives:**
- `/references/color-science.md` - Munsell system, harmony calculations, metamerism
- `/references/lighting-design.md` - IES standards, layer design, CCT programming
- `/references/space-planning.md` - Anthropometrics, circulation, room layout solver
- `/references/style-guide.md` - Style DNA breakdowns, mixing guidelines
