---
name: image
description: ImageAgent - Generate EVOLEA Brand Images with Reinforcement Learning
---

# EVOLEA Image Generation with Reinforcement Learning

> **Invoke with**: `/image` or use automatically when generating images for the website
> **Last Updated**: 2025-12-27

This skill provides an intelligent image generation system that learns from user feedback to produce increasingly better, brand-consistent images for EVOLEA.

---

## MCP Server (Claude Desktop / Claude App)

The image generation system is available as an MCP server for use with Claude Desktop and Claude App.

### Available Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Generate a single image with EVOLEA branding |
| `generate_ab_comparison` | Generate A/B comparison for training (2 options + grid) |
| `list_generated_images` | List recent generated images by category |
| `get_brand_prompt_template` | Get prompt templates for specific image types |
| `publish_image` | Publish image to GitHub for public URL access |
| `get_training_guide` | Get the full training guide documentation |

### Setup (Claude Desktop)

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "evolea-images": {
      "command": "python",
      "args": ["C:/Users/christoph/evolea-website/scripts/mcp_image_server.py"],
      "env": {
        "GOOGLE_API_KEY": "your-gemini-api-key"
      }
    }
  }
}
```

### Quick Commands in Claude Desktop

```
"Generate an image of children doing art together"
"Create an A/B comparison for Mini Projekte hero"
"Show me recent training images"
"Publish the image to GitHub so I can see it on my phone"
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. LOAD LEARNINGS from LEARNINGS.md                        │
│     - Apply positive patterns (+3, +1 boosts)               │
│     - Include negative patterns in exclusions (-1, -3)      │
├─────────────────────────────────────────────────────────────┤
│  2. GENERATE OPTIONS (A and B)                              │
│     - Option A: Base prompt with current learnings          │
│     - Option B: Base + additional style modifiers           │
│     - Save to: public/images/generated/training/            │
├─────────────────────────────────────────────────────────────┤
│  3. CREATE COMPARISON GRID                                  │
│     - Side-by-side A|B image for easy comparison            │
├─────────────────────────────────────────────────────────────┤
│  4. USER SELECTS                                            │
│     - A, B, or Neither with feedback                        │
├─────────────────────────────────────────────────────────────┤
│  5. UPDATE LEARNINGS                                        │
│     - Boost winning patterns                                │
│     - Record negative patterns from feedback                │
│     - Persist to LEARNINGS.md                               │
├─────────────────────────────────────────────────────────────┤
│  6. PUBLISH (optional)                                      │
│     - Push to GitHub → Cloudflare Pages                     │
│     - Get public URL for mobile access                      │
├─────────────────────────────────────────────────────────────┤
│  7. ITERATE until satisfied                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Command Line Usage

### Generate with Training Loop

```bash
# Start a training session for a specific image
python scripts/generate_image.py "children ages 5-8 creating art" \
  --name mini-projekte-hero \
  --category programs \
  --training
```

### Manual A/B Generation

```bash
# Generate 2 options with comparison grid
python scripts/generate_image.py "your prompt" \
  --name image-name \
  --count 2 \
  --comparison-grid
```

### Fully Automated (with Claude selection)

```bash
python scripts/generate_image.py "your prompt" \
  --name image-name \
  --auto-select
```

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/mcp_image_server.py` | MCP server for Claude Desktop |
| `scripts/generate_image.py` | Core image generation script |
| `LEARNINGS.md` | Persistent style preferences with scores |
| `TRAINING-GUIDE.md` | User guide for iterative training |
| `training-log.json` | Full history of all training sessions |
| `style-profiles/*.md` | Pre-defined style templates |

---

## EVOLEA Style Guidelines

### Central European Children (Ages 5-8)
- **Skin tones**: Light/fair with warm undertones
- **Hair colors**: Blonde, light brown, auburn, brown
- **Features**: Soft, rounded, friendly expressions
- **NO**: Religious symbols, American cultural elements

### Whimsical Style (User's Preferred)
- Soft dreamy watercolor textures
- Floating, layered clouds in spectrum colors
- Ethereal, magical atmosphere
- Delicate butterflies or unicorns
- Pastel gradient backgrounds (lavender, mint, coral, cream)

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Magenta | #DD48E0 | Primary accents |
| Mint | #7BEDD5 | Fresh, nature |
| Lavender | #CD87F8 | Calm, creative |
| Coral | #FF7E5D | Energy, warmth |
| Cream | #FFFBF7 | Backgrounds |

### NEVER Include
- Puzzle piece symbols
- Clinical/medical settings
- Religious symbols on children
- American cultural elements (yellow school buses)
- Photorealistic style
- Dark or muted colors

---

## Teacher Illustrations

Based on EVOLEA team members:

| Name | Description |
|------|-------------|
| Gianna Spiess | Female, professional, warm, M.Sc. BCBA |
| Annemarie Elias | Female, friendly, approachable, M.Sc. BCBA |
| Christoph Jenny | Male, supportive, engaged |
| Alexandra Aleksic | Female, young, energetic, B.Sc. |

---

## Prompt Templates

### Program Hero
```
Children aged [AGE] [ACTIVITY] in [SETTING].
Swiss/Central European children with light skin and varied natural hair colors.
[SPECIFIC DETAILS].
Mood: [EMOTION]. Dominant colors: [COLORS].
Soft watercolor children's book illustration style with delicate butterflies.
```

### Abstract/Decorative
```
Soft dreamy [SUBJECT] in whimsical watercolor style.
Layered colorful clouds in lavender, mint, coral, and cream.
Ethereal atmosphere with gentle sparkles.
Delicate butterflies floating softly.
Dominant colors: [COLORS]. Mood: magical, warm, inviting.
```

---

## Backend Configuration

The image generation always uses **Gemini 3 Pro**:

| Model | ID |
|-------|-----|
| Gemini 3 Pro | `gemini-3-pro-image-preview` |

This is configured in `scripts/generate_image.py` via `CONFIG.gemini_model`.

Replicate (Flux) is available as a fallback if Gemini is unavailable in your region.

---

## Related Files

- `TRAINING-GUIDE.md` - Detailed training workflow guide
- `LEARNINGS.md` - Current learned preferences
- `style-profiles/` - Style profile templates
- `.claude/skills/Design skills/illustrations.md` - Illustration guidelines
