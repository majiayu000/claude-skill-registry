---
name: image-analysis
description: GLM-4.6v image analysis subagent for game screenshot and sprite quality assessment
---

# Image Analysis Skill

**Purpose:** Delegate image analysis tasks to GLM-4.6v subagent for visual quality assessment of game screenshots and sprites.

## When to Use

Invoke this skill when:
- New sprites are generated (via glm-image-gen)
- Screenshots captured during playtesting
- Visual quality validation needed before commits
- Checking for blocky backgrounds or transparency issues
- Comparing assets against Harvest Moon SNES style

## Direct vs Delegated Analysis

**Claude Opus can analyze images directly** via the Read tool. Choose the right approach:

| Scenario | Approach | Why |
|----------|----------|-----|
| 1-3 images | Claude Direct | No overhead, faster |
| Quick quality check | Claude Direct | Immediate feedback |
| Batch analysis (10+) | MiniMax Parallel | Token efficiency |
| Extensive visual QA | MiniMax Parallel | 50x cheaper |

### Claude Direct Pattern
```
Read image file → Analyze in-context → Continue workflow
```

### MiniMax/GLM Delegation Pattern (for batches)
```
Spawn parallel agents → Each analyzes subset → Aggregate results
```

**Default:** Use Claude Direct for small tasks, delegate batches to save tokens.

## Quick Start

### Analyze Screenshot
```bash
mcp__4_5v_mcp__analyze_image \
  --imageSource "temp/screenshots/[filename].png" \
  --prompt "Analyze this game screenshot for visual quality. Check for: blocky backgrounds, tiling seams, sprite transparency issues, pixel art scaling problems, overall Harvest Moon SNES readability. Provide specific, actionable feedback."
```

### Analyze Sprite Asset
```bash
mcp__4_5v_mcp__analyze_image \
  --imageSource "assets/sprites/placeholders/[filename].png" \
  --prompt "Analyze this pixel art sprite for Harvest Moon SNES style quality. Check: transparency (clean edges), silhouette (strong/readable), proportions (compact not stretched), color palette (dusk-friendly), pixel detail (minimal noise). Reference: assets/sprites/PLACEHOLDER_ASSET_SPEC.txt"
```

### Analyze NPC Sprite
```bash
mcp__4_5v_mcp__analyze_image \
  --imageSource "assets/sprites/placeholders/npc_[name].png" \
  --prompt "Analyze this 64x64 NPC sprite. Target proportions: ~48h x 32w centered. Check: strong silhouette, Mediterranean theme alignment, clean transparency, no elongation. Harvest Moon SNES style reference."
```

## Standard Prompts

### Full Quality Assessment
```
Analyze this image for Circe's Garden game quality standards:

Visual Style:
- Harvest Moon SNES readability (clean pixel art, strong silhouettes)
- Stardew Valley influence (but more mythic/moody)
- Mediterranean ancient Greek island theme
- Dusk-friendly palette (muted, not oversaturated)
- 32px tiles, 2x camera zoom

Check For:
1. Background issues: blocky patterns, tiling seams, color banding
2. Transparency: clean edges (no halos), proper alpha channel
3. Pixel art: minimal noise, clear details, proper scaling
4. Proportions: compact bodies, not stretched/elongated
5. Colors: natural earth tones, muted jewel accents
6. Lighting: soft ambient, no harsh specular
7. Silhouette: strong, recognizable at small size

Provide specific feedback: what works, what needs fixing, file references.
```

### Transparency Check (Focused)
```
Check this sprite for transparency issues:
- Halo effect (light/dark ring around edges)
- Color bleeding (background showing through)
- Harsh edges (no smooth curves on diagonals)
- Partial transparency (should be opaque or transparent, not in-between)

Report specific pixel locations and severity.
```

### Style Comparison
```
Compare this asset to Harvest Moon SNES style:
- Clean pixel art with minimal noise
- Strong silhouette (recognizable at 32x32)
- Soft, natural color palette
- Proper alpha blending
- No anti-aliasing on edges
- Cozy, approachable aesthetic

Report what matches style and what deviates.
```

## Output Format

Expected response should include:

```markdown
## Analysis Summary
[One-line assessment: PASS / NEEDS WORK / FAIL]

### Issues Found
**Critical (P0):**
- [Specific issue with location]

**Important (P1):**
- [Issue description]

**Minor (P2):**
- [Minor detail]

### What Works
- [Positive aspects to preserve]

### Recommendations
1. [Actionable fix 1]
2. [Actionable fix 2]
```

## Common Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Blocky background | Visible pixel grid, tiling patterns | Regenerate with better seam handling |
| Halo effect | Light/dark ring around sprite | Fix alpha channel, clean edges |
| Color bleeding | Background color in transparent pixels | Re-export with proper transparency |
| Stretched proportions | Elongated body/limbs | Regenerate with compact proportions |
| Oversaturated colors | Too bright/vibrant | Adjust palette to dusk-friendly tones |
| Poor silhouette | Not recognizable at small size | Strengthen outline, simplify details |

## File Locations

**Input:**
- Screenshots: `temp/screenshots/`
- Sprites: `assets/sprites/`
- Placeholders: `assets/sprites/placeholders/`

**Reference:**
- Asset specs: `assets/sprites/PLACEHOLDER_ASSET_SPEC.txt`
- Style guide: `assets/sprites/PLACEHOLDER_README.md`

## Integration

### With glm-image-gen
```bash
# After generating new sprite
./generate-image.sh '{"subject":"..."}' 1024x1024 standard
./process-image.sh "$TEMP" "32x32" "assets/sprites/output.png"

# Then analyze quality
mcp__4_5v_mcp__analyze_image --imageSource "assets/sprites/output.png" --prompt "[standard prompt]"
```

### With HPV (Playtesting)
```bash
# During screenshot review
ls temp/screenshots/
mcp__4_5v_mcp__analyze_image --imageSource "temp/screenshots/world_map.png" --prompt "[screenshot prompt]"
```

### Pre-commit Check
```bash
# Before committing asset changes
git status
mcp__4_5v_mcp__analyze_image --imageSource "assets/sprites/new_asset.png" --prompt "[validation prompt]"
```

## Subagent Role

Full subagent configuration: `.claude/roles/image-analysis-subagent.md`

**Model:** GLM-4.6v (vision-capable)
**Tool:** `mcp__4_5v_mcp__analyze_image`
**Purpose:** Specialized visual quality assessment

## Success Criteria

Analysis is effective when:
- Issues match human findings (80%+ accuracy)
- False positives < 20%
- Actionable feedback provided
- Response time < 30 seconds
- Consistent report format

---

**Related:**
- `.claude/skills/glm-image-gen/SKILL.md` (sprite generation)
- `assets/sprites/PLACEHOLDER_ASSET_SPEC.txt` (asset specifications)
- `.claude/roles/image-analysis-subagent.md` (full subagent docs)

[Kimi Code CLI - 2026-01-26]
