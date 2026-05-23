---
name: asset-packager
description: Automated asset packaging—converts validated PNG + IDF JSON into complete production bundle (context.md, tokens.json, usage.md). Eliminates 30 manual file generations across 10 assets.
---

# Asset-Packager Skill

## Purpose

Automates asset packaging after validation. Input: validated PNG + IDF. Output: complete directory with context/tokens/usage files + production file copy + git commit. Replaces 15 min manual work with 2 min automated execution.

## Input Requirements

```json
{
  "asset_id": "ASSET-3",
  "asset_name": "Nocturnal Canopy Pattern",
  "validated_png": "/downloads/asset-3-validated.png",
  "compliance_score": 92,
  "idf_data": {
    "colors": {"background": "#1A1714", "wattle_gold": "#D4A84B"},
    "specimens": ["Eucalyptus", "Wattle", "Banksia"],
    "dimensions": {"width": 512, "height": 512},
    "mode": "Gallery",
    "purpose": "Seamless background pattern"
  }
}
```

## Generated Files

### 1. context.md
Narrative philosophy explaining specimen choices, geometric principles, mode context.

**Template:**
```markdown
# Asset [N]: [Name]

## Narrative

[Victorian naturalist discovery story based on specimens]

## Specimens

[List with taxonomic significance]

## Mode Context

Gallery: [Warm/theatrical interpretation]
Laboratory: [Clinical/analytical interpretation]

## Purpose

[UI placement and compositional role]
```

### 2. tokens.json
Machine-readable design specifications.

**Structure:**
```json
{
  "asset_id": "ASSET-3",
  "background": "#1A1714",
  "palette": {
    "primary": ["#C45C4B", "#D4A84B"],
    "accents": ["#7A9E82", "#D4885C"]
  },
  "dimensions": {"width": 512, "height": 512, "format": "PNG"},
  "density_zones": {
    "upper_left": {"coverage": "18%"},
    "central": {"coverage": "65%"}
  },
  "specimens": [...],
  "mode": "Gallery",
  "compliance_score": 92
}
```

### 3. usage.md
CSS implementation with responsive behavior, opacity ranges, placement guidelines.

**Template:**
```markdown
# Usage Guidelines

## CSS Implementation

\`\`\`css
.asset-[name] {
  background-image: url('/assets/[path]');
  background-size: [cover|contain|repeat];
  background-position: center;
}

/* Opacity by context */
.gallery-hero { opacity: 0.85; }
.gallery-content { opacity: 0.70; }
.dashboard { opacity: 0.60; }
\`\`\`

## Responsive Behavior

- Desktop: Full resolution
- Tablet: Scale proportionally
- Mobile: [Specific guidance]

## Component Integration

Recommended for: [Components list]
Avoid for: [Contexts where inappropriate]
```

## Automation Steps

1. **Create Directory**
   ```bash
   mkdir -p /assets/ASSET-[N]-[slug]/
   ```

2. **Generate context.md**
   - Extract specimens from IDF
   - Build narrative using specimen → taxonomic significance mapping
   - Insert mode context (Gallery/Laboratory)

3. **Generate tokens.json**
   - Convert IDF to structured JSON
   - Add compliance metadata
   - Format for machine parsing

4. **Generate usage.md**
   - Build CSS template with asset path
   - Add opacity recommendations based on mode
   - List component integration targets

5. **Copy Production File**
   ```bash
   cp [validated_png] /frontend/public/assets/[category]/[filename]
   ```
   Categories: wallpapers, patterns, specimens, icons

6. **Git Commit**
   ```bash
   git add /assets/ASSET-[N]-* /frontend/public/assets/[category]/
   git commit -m "feat(assets): Add Asset [N] [name] - [score]/100"
   ```

## Integration Points

**Flash-Sidekick:**
- Call `generate_idf` on validated PNG → extract design tokens
- Call `quick_summarize` on specimen list → generate narrative

**Auto-Validator:**
- Trigger: score ≥90 → auto-package
- Input: validation JSON + PNG path

**Claude Code:**
- Delegates file operations and git commits
- Verifies directory structure creation

## Usage Example

```python
# After auto-validation passes
packager_result = asset_packager.run(
    asset_id="ASSET-3",
    validation_result=auto_validator_output,
    png_path="/downloads/asset-3-validated.png"
)

# Output:
# Created: /assets/ASSET-3-nocturnal-canopy/{context,tokens,usage}
# Copied: /frontend/public/assets/patterns/nocturnal-canopy-tile-512.png
# Committed: feat(assets): Add Asset 3 Nocturnal Canopy - 92/100
```

## Efficiency Gain

**Before:** 15 min per asset × 10 assets = 150 min
**After:** 2 min per asset × 10 assets = 20 min
**Savings:** 130 min (87% time reduction)

## File Naming Convention

**Assets Directory:** `ASSET-[N]-[kebab-case-name]/`
**Production Files:**
- Wallpapers: `texture-[mode]-[name]-[width].png`
- Patterns: `[name]-tile-[size].png`
- Specimens: `specimen-[name]-[style]-[size].png`
- Icons: `[name]-[purpose]-[size].png`

---

*Eliminates repetitive packaging work. Validated asset → production bundle in 2 minutes.*
