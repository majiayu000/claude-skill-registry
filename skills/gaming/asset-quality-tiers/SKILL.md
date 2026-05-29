---
name: asset-quality-tiers
description: This skill should be used when the user asks about "asset quality tiers", "upgrade asset quality", "placeholder vs final", "hero quality", "quality improvement", "make assets better", "quality levels", "upgrade to final", "asset polish", or discusses improving existing procedural assets to higher quality levels. Provides the tier system (Placeholder → Temp → Final → Hero) and enhancement strategies for upgrading assets.
---

# Asset Quality Tiers

A four-tier quality system for procedural asset generation that enables incremental quality improvement from rapid prototyping to hero-quality assets.

## The Tier System

Assets progress through quality tiers, each appropriate for different development phases:

```
PLACEHOLDER (Tier 1) ──► TEMP (Tier 2) ──► FINAL (Tier 3) ──► HERO (Tier 4)
      │                      │                 │                  │
  Blocking              Development        Ship-ready         Showcase
  Scale testing         Testing            Production         Marketing
  Rapid iteration       Internal builds    Standard           Closeups
```

### Tier Definitions

| Tier | Name | Quality Score | Purpose | Typical Usage |
|------|------|---------------|---------|---------------|
| 1 | **Placeholder** | 30-50% | Blocking, scale testing | Level layout, gameplay testing |
| 2 | **Temp** | 50-70% | Development testing | Internal builds, playtesting |
| 3 | **Final** | 70-90% | Production quality | Shipping game assets |
| 4 | **Hero** | 90-100% | Maximum quality | Marketing, cutscenes, closeups |

### Tier Assessment Criteria

Determine asset tier by evaluating against these criteria:

**Placeholder indicators:**
- Basic primitives or box modeling
- Solid colors or single noise layer
- Missing UVs or normals
- Simple shapes without detail

**Temp indicators:**
- Basic shapes with proper UVs
- 1-2 noise layers on textures
- Meets minimum technical requirements
- Functional but lacks polish

**Final indicators:**
- Proper topology with bevels
- Multi-layer textures with detail
- Full material maps (albedo, MRE)
- Polished silhouettes

**Hero indicators:**
- Maximum detail within budget
- All material channels utilized
- Subtle variations and imperfections
- Perfect for close inspection

## Enhancement Strategies

### Mesh Enhancement by Tier

| Upgrade | Key Techniques |
|---------|----------------|
| Placeholder → Temp | Add proper UVs, calculate normals, triangulate |
| Temp → Final | Add bevels, improve silhouette, optimize topology |
| Final → Hero | Add secondary shapes, edge loops, micro-detail |

### Texture Enhancement by Tier

| Upgrade | Key Techniques |
|---------|----------------|
| Placeholder → Temp | Add noise variation, basic color palette |
| Temp → Final | Add contrast, detail layers, color richness |
| Final → Hero | Add wear maps, subtle variations, all channels |

### Audio Enhancement by Tier

| Upgrade | Key Techniques |
|---------|----------------|
| Placeholder → Temp | Add envelope shaping, basic layering |
| Temp → Final | Add multiple layers, filtering, variation |
| Final → Hero | Add subtle harmonics, pitch variations, spatial cues |

### Animation Enhancement by Tier

| Upgrade | Key Techniques |
|---------|----------------|
| Placeholder → Temp | Add proper timing, basic keyframes |
| Temp → Final | Add easing, secondary motion, proper arcs |
| Final → Hero | Add anticipation, follow-through, subtle overlap |

## Quality Score Calculation

Each asset type has weighted quality dimensions:

### Mesh Quality Score

```
Score = (UV_Coverage × 0.25) + (Silhouette_Clarity × 0.20) +
        (Topology_Quality × 0.20) + (Detail_Level × 0.20) +
        (Budget_Compliance × 0.15)
```

### Texture Quality Score

```
Score = (Contrast × 0.20) + (Color_Richness × 0.20) +
        (Detail_Layers × 0.25) + (Coherence × 0.20) +
        (Format_Compliance × 0.15)
```

### Audio Quality Score

```
Score = (Layer_Richness × 0.25) + (Envelope_Quality × 0.20) +
        (Clarity × 0.20) + (Variation × 0.20) +
        (Format_Compliance × 0.15)
```

## Tier Budget Guidelines

Each tier has different resource budgets:

### Mesh Poly Budgets

| Asset Class | Placeholder | Temp | Final | Hero |
|-------------|-------------|------|-------|------|
| Small prop | 20-50 | 50-150 | 150-300 | 300-500 |
| Medium prop | 50-100 | 100-300 | 300-500 | 500-800 |
| Character | 100-200 | 200-400 | 400-800 | 800-2000 |
| Vehicle | 100-300 | 300-600 | 600-1000 | 1000-2000 |
| Environment | 50-200 | 200-500 | 500-1500 | 1500-3000 |

### Texture Resolution Guidelines

| Tier | Typical Resolution | Channel Usage |
|------|-------------------|---------------|
| Placeholder | 32x32 - 64x64 | Albedo only |
| Temp | 64x64 - 128x128 | Albedo + basic normal |
| Final | 128x128 - 256x256 | Albedo + MRE |
| Hero | 256x256 - 512x512 | Albedo + MRE + SSE + detail |

## Using Tiers in Generation

### Specifying Target Tier

When generating assets, specify the target tier:

```
"Generate a wooden barrel at Final tier"
"Create placeholder props for layout testing"
"Upgrade these meshes to Hero quality"
```

### Style Tier Integration

Include tier specification in style recipes:

```python
{
    "asset": {
        "name": "barrel",
        "type": "prop",
        "tier": "final",  # placeholder | temp | final | hero
    },

    "generation": {
        "mesh": {
            "detail_level": 3,  # 1-4 matching tier
            "subdivision": 2,
            "bevels": True,
        },
        "texture": {
            "resolution": 256,
            "layers": 3,
            "detail_maps": True,
        },
    },
}
```

## Enhancement Workflow

### Identifying Upgrade Candidates

1. Scan project assets
2. Assess current tier of each
3. Compare to target tier
4. Prioritize by visibility/importance

### Executing Upgrades

1. Read current generation code/style spec
2. Identify specific enhancement parameters
3. Apply tier-appropriate techniques
4. Regenerate asset
5. Validate quality improvement

### Bulk Upgrades

When upgrading multiple assets:
- Process in batches by asset type
- Maintain style consistency across batch
- Verify cohesion after upgrades

## Additional Resources

### Reference Files

For enhancement techniques, use the **index files first** (lean routing), then load full references as needed:

| Asset Type | Index (load first) | Full Reference (load for code) |
|------------|-------------------|-------------------------------|
| Textures | `texture-enhancement-index.md` | `texture-enhancements.md` (1290 lines) |
| Meshes | `mesh-enhancement-index.md` | `mesh-enhancements.md` (1142 lines) |
| Audio | - | `audio-enhancements.md` |
| Animation | - | `animation-enhancements.md` |

### Related Agents

- **quality-enhancer** - Autonomous asset improvement
- **quality-analyzer** - Quality assessment and scoring
- **asset-critic** - style spec compliance checking

### Related Commands

- **/improve-assets** - Guided quality improvement workflow
