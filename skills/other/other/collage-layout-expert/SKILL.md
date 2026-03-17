---
name: collage-layout-expert
description: "Expert in ALL computational collage composition: photo mosaics, grid layouts, scrapbook/journal styles, magazine editorial, vision boards, mood boards, social media collages, memory walls, abstract/generative arrangements, and art-historical techniques (Hockney joiners, Dadaist photomontage, Surrealist assemblage, Rauschenberg combines). Masters edge-based assembly, Poisson blending, optimal transport color harmonization, and aesthetic optimization. Activate on 'collage', 'photo mosaic', 'grid layout', 'scrapbook', 'vision board', 'mood board', 'photo wall', 'magazine layout', 'Hockney', 'joiner', 'photomontage'. NOT for simple image editing (use native-app-designer), generating new images (use Stability AI), single photo enhancement (use photo-composition-critic), or basic image similarity search (use clip-aware-embeddings)."
allowed-tools: Read,Write,Edit,Bash,mcp__stability-ai__stability-ai-generate-image,mcp__firecrawl__firecrawl_search,WebFetch
category: Design & Creative
tags:
  - collage
  - layout
  - photo-mosaic
  - composition
  - blending
pairs-with:
  - skill: color-theory-palette-harmony-expert
    reason: Harmonize colors across collage
  - skill: photo-composition-critic
    reason: Ensure aesthetic quality of result
---

# Collage & Layout Composition Expert

Expert in **ALL forms of computational collage composition** - from Instagram grids to Hockney joiners, from magazine layouts to generative art.

## When to Use This Skill

✅ **Use for:**
- **Grid Collages**: Instagram profiles, regular layouts, tiled compositions
- **Photo Mosaics**: Small images forming larger pictures
- **Hockney-Style Joiners**: Multi-perspective photographic assemblies
- **Scrapbook/Journal**: Mixed media with text, frames, embellishments
- **Magazine/Editorial**: Professional layouts with text integration
- **Vision/Mood Boards**: Inspiration collections, design references
- **Memory Walls**: Scattered Polaroid-style arrangements
- **Social Media**: Stories, carousel previews, profile grids
- **Abstract/Generative**: Algorithmic and procedural arrangements
- **Art-Historical**: Dadaist, Surrealist, Pop Art styles

❌ **Do NOT use for:**
- Simple image editing → **native-app-designer**
- Generating new images → **Stability AI**
- Single photo quality → **photo-composition-critic**
- Image similarity search → **clip-aware-embeddings**
- Color palette extraction → **color-theory-palette-harmony-expert**

## Expert vs Novice Shibboleths

| Topic | Novice | Expert |
|-------|--------|--------|
| **Layout** | "Just arrange randomly" | Visual weight, balance, golden ratio |
| **Blending** | Hard edges or simple feather | Poisson blending preserves gradients |
| **Color** | "Match colors manually" | Optimal transport; LAB space advantages |
| **Composition** | Fills all space | Negative space as design element |
| **Scale** | Same size for everything | Varies scale for hierarchy |
| **Mosaic** | "More tiles = better" | Tile size vs. recognition tradeoff |
| **Hockney** | "Stitch seamlessly" | Imperfection IS the technique |

## Decision Tree: Choosing a Style

**What's the purpose?**
- Systematic display → **Grid Collage**
- Artistic portrait from photos → **Photo Mosaic**
- Personal memories → **Scrapbook** or **Memory Wall**
- Design inspiration → **Mood Board**
- Professional/publication → **Magazine Layout**
- Social media → **Social Templates**
- Art project → **Hockney/Dadaist/Surrealist**

**What's the vibe?**
- Clean, modern → Grid with tight gutters
- Nostalgic, warm → Polaroid scatter, vintage frames
- Edgy, disruptive → Dadaist sharp cuts
- Dreamy, surreal → Seamless Poisson blending
- Cubist, intellectual → Hockney joiners

## Core Algorithms (Summary)

| Algorithm | Use Case | Performance |
|-----------|----------|-------------|
| **Edge-Based Assembly** | Hockney joiners | 0.5s for 10 photos |
| **Poisson Blending** | Seamless transitions | 20ms (512×512) |
| **Optimal Transport** | Color harmonization | Real-time w/ affine approx |
| **Force-Directed** | Organic scatter | 200ms (50 images) |
| **K-d Tree Matching** | Photo mosaic tiles | 2s for 10k tiles |

→ See `references/algorithms.md` for full implementations.

## Anti-Patterns to Avoid

### 1. Ignoring Visual Weight
**What it looks like**: All images same size, random placement
**Why it's wrong**: No focal point, viewer's eye wanders aimlessly
**Fix**: Establish 60/30/10 hierarchy with one hero image

### 2. Over-Saturating the Canvas
**What it looks like**: Every pixel filled with image content
**Why it's wrong**: Visual claustrophobia, no breathing room
**Fix**: Use negative space intentionally (20-30% white space minimum)

### 3. Linear FFT for Color Matching
**What it looks like**: Poor perceptual color matches
**Why it's wrong**: RGB is not perceptually uniform
**Fix**: Use LAB color space for matching

### 4. Seamless Hockney Joiners
**What it looks like**: Perfectly stitched panorama
**Why it's wrong**: Misses the entire point - multiple perspectives
**Fix**: Embrace ±2° rotation variance, 5-15% overlap, intentional gaps

### 5. Global Poisson Blending
**What it looks like**: Entire image becomes washed out
**Why it's wrong**: Destroys local contrast, looks fake
**Fix**: Apply locally at seams only, preserve source gradients

### 6. Reusing Mosaic Tiles
**What it looks like**: Obvious repetition patterns in mosaic
**Why it's wrong**: Human eye detects patterns immediately
**Fix**: Track tile usage, penalize reuse, use larger tile library

## MCP Integrations

| MCP | Purpose |
|-----|---------|
| **Stability AI** | Generate backgrounds, textures, missing elements |
| **Firecrawl** | Research techniques, algorithm papers, art history |
| **WebFetch** | Fetch documentation, tutorials, design references |

## Performance Targets

| Operation | Mac M2 | iPhone 15 Pro |
|-----------|--------|---------------|
| Grid layout (20 photos) | &lt;50ms | &lt;100ms |
| Photo mosaic (10k tiles) | 2s | 5s |
| Force-directed (50 images) | 200ms | 500ms |
| Poisson blending (512×512) | 20ms | 50ms |
| Hockney assembly (10 photos) | 0.5s | 2s |

## References

→ `references/collage-types.md` - Grid, mosaic, scrapbook, magazine, social templates
→ `references/art-historical-styles.md` - Hockney, Dadaist, Surrealist, Rauschenberg
→ `references/algorithms.md` - Edge assembly, Poisson, optimal transport, force-directed
→ `references/advanced-techniques.md` - Cross-photo interactions, narrative sequences
→ `references/implementation-guide.md` - Metal shaders, Core ML, performance

## Integrates With

- **photo-composition-critic** - Assess individual photos before collaging
- **color-theory-palette-harmony-expert** - Extract/match color palettes
- **clip-aware-embeddings** - Semantic grouping of images
- **native-app-designer** - Build collage creation UI
- **metal-shader-expert** - GPU-accelerated blending/effects

---

**Remember**: Great collages tell stories through arrangement. Whether grid-precise or Hockney-chaotic, the layout serves the narrative. Master both the math and the art.
