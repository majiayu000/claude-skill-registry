---
name: brand-guidelines
description: Activate for brand voice, visual identity, messaging frameworks, asset management, and brand consistency. Use when creating branded content, establishing tone of voice, managing marketing assets, validating brand compliance, or maintaining brand standards across marketing materials.
license: MIT
---

# Brand Guidelines

Brand identity, voice, messaging, asset management, and consistency frameworks.

## When to Use

- Brand voice definition
- Visual identity standards
- Messaging framework creation
- Content tone guidance
- Brand consistency review
- Style guide development
- Asset organization and naming
- Color palette management
- Typography specifications
- Logo usage validation
- Asset approval workflows

## Quick Start

**Inject brand context into prompts:**
```bash
node scripts/inject-brand-context.cjs
node scripts/inject-brand-context.cjs --json
```

**Validate an asset:**
```bash
node scripts/validate-asset.cjs <asset-path>
node scripts/validate-asset.cjs <asset-path> --json
```

**Extract/compare colors:**
```bash
node scripts/extract-colors.cjs --palette
node scripts/extract-colors.cjs <image-path>
```

## References

| Topic | File | Description |
|-------|------|-------------|
| Voice Framework | `references/voice-framework.md` | Brand voice development and testing |
| Visual Identity | `references/visual-identity.md` | Core visual elements and guidelines |
| Messaging | `references/messaging-framework.md` | Value props and messaging architecture |
| Consistency | `references/consistency-checklist.md` | Channel and material auditing |
| Guidelines Template | `references/brand-guideline-template.md` | Comprehensive template for brand docs |
| Asset Organization | `references/asset-organization.md` | Directory structure and naming |
| Color Management | `references/color-palette-management.md` | Color systems and accessibility |
| Typography | `references/typography-specifications.md` | Fonts, scales, and implementation |
| Logo Usage | `references/logo-usage-rules.md` | Logo variants and placement rules |
| Approval Checklist | `references/approval-checklist.md` | Asset review and approval process |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/inject-brand-context.cjs` | Extract brand context for prompt injection |
| `scripts/sync-brand-to-tokens.cjs` | Sync brand-guidelines.md → design-tokens.json/css |
| `scripts/validate-asset.cjs` | Validate asset naming, size, format |
| `scripts/extract-colors.cjs` | Extract and compare colors against palette |

## Brand Sync Workflow

When updating brand identity, always sync all files:

```bash
# 1. Edit docs/brand-guidelines.md (or use /brand:update command)

# 2. Sync to design tokens
node scripts/sync-brand-to-tokens.cjs

# 3. Verify
node scripts/inject-brand-context.cjs --json | head -20
```

**Files synced:**
- `docs/brand-guidelines.md` → Source of truth (human-readable)
- `assets/design-tokens.json` → Token definitions
- `assets/design-tokens.css` → CSS variables

## Templates

| Template | Purpose |
|----------|---------|
| `templates/brand-guidelines-starter.md` | Complete starter template for new brands |

## Asset Directory Structure

```
.assets/                  # Git-tracked metadata
├── manifest.json         # Central asset registry
├── tags.json            # Tagging system
├── versions/            # Version history
└── metadata/            # Type-specific metadata

assets/                   # Raw files
├── designs/             # Campaign, web, print
├── banners/             # Social, email, landing
├── logos/               # Full, icon, mono
├── videos/              # Ads, tutorials, testimonials
├── infographics/
└── generated/           # AI-generated (timestamped)
```

## Naming Convention

```
{type}_{campaign}_{description}_{timestamp}_{variant}.{ext}

Examples:
banner_claude-launch_hero-image_20251209_16-9.png
logo_brand-refresh_horizontal_20251209.svg
```

## Brand Elements

**Voice Dimensions:**
- Tone: Formal ↔ Casual
- Language: Simple ↔ Complex
- Character: Serious ↔ Playful
- Emotion: Reserved ↔ Expressive

**Visual Elements:**
- Logo (primary, secondary, icon)
- Colors (primary, secondary, accent)
- Typography (headers, body)
- Imagery style

## Workflows

### Voice Development
1. Define brand personality (3-5 traits)
2. Establish tone spectrum
3. Create do's and don'ts
4. Write example content
5. Document in style guide

### Asset Approval
1. Create asset following naming convention
2. Run `validate-asset.cjs` for compliance check
3. Extract colors, compare to palette
4. Complete approval checklist
5. Register in manifest.json

### Brand Audit
1. Collect all materials
2. Assess consistency
3. Identify gaps
4. Prioritize fixes
5. Update guidelines

## Integration

**With ai-multimodal skill:**
- Generate brand-aligned images with Imagen 4
- Analyze assets for color compliance
- Create consistent visual content

**With content-marketing skill:**
- Apply brand voice to all content
- Ensure messaging alignment
- Maintain consistency

**Primary Agents:** content-creator, social-media-manager, email-wizard, ui-ux-designer

**Skill Dependencies:** ai-multimodal, content-marketing, social-media

## Best Practices

1. Consistency > perfection
2. Voice adapts to context, personality stays same
3. Show examples, not just rules
4. Update guidelines as brand evolves
5. Audit quarterly
6. Register all assets in manifest
7. Use naming conventions strictly
