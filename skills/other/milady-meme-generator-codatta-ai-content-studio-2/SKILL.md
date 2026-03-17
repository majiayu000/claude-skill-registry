---
name: milady-meme-generator
description: Generate Milady NFT memes with layered composition, text overlays, and 324+ accessories. Use when creating Milady memes, adding layers like hats/glasses/earrings, working with NFT artwork, or generating custom meme images.
allowed-tools: Read, Write, Bash(python:*)
model: claude-sonnet-4-20250514
---

# Milady Meme Generator

Generate custom Milady NFT memes with advanced layering, text overlays, and 324+ accessory options.

## Overview

This Skill enables you to create Milady-themed memes using:
- **10,000 Milady NFT base images** (1000x1250 resolution)
- **324 layered accessories** across 6 categories
- **Text overlay system** with custom fonts and styles
- **Natural language parsing** for easy layer selection
- **Template-based generation** with random combinations

## Quick Start

### Basic Meme Generation

```python
from src.meme_generator_v2 import MemeGeneratorV2

# Initialize generator
generator = MemeGeneratorV2()

# Generate random Milady meme
output = generator.generate_random_meme()

# Generate specific NFT with text
output = generator.generate_meme(
    nft_id=5050,
    top_text="GM",
    bottom_text="WAGMI"
)

# Generate with custom layers
output = generator.generate_meme(
    nft_id=5050,
    layers=["Hat:Beret.png", "Glasses:Sunglasses.png"]
)
```

### Natural Language Layer Selection

```python
from src.prompt_parser import PromptParser

parser = PromptParser()

# Parse natural language to layers
result = parser.parse_prompt(
    "give her a red beret and cool sunglasses"
)
# Returns: ["Hat:Beret.png", "Glasses:Sunglasses.png"]
```

## Layer System

### Layer Categories (6 types)

| Category | Count | Z-Index | Description |
|----------|-------|---------|-------------|
| **Hat** | 89 | 60 | Headwear accessories |
| **Glasses** | 24 | 50 | Eyewear styles |
| **Earrings** | 21 | 40 | Ear accessories |
| **Necklaces** | 13 | 30 | Neck jewelry |
| **Face Decoration** | 134 | 70 | Face stickers/marks |
| **Overlay** | 43 | 80 | Special effects |

**Total:** 324 layers

### Layer Usage

```python
from src.milady_composer import MiladyComposer

composer = MiladyComposer()

# Add single layer
composer.add_layer("Hat:Cowboy.png")

# Add multiple layers
composer.add_layers([
    "Hat:Beret.png",
    "Glasses:Sunglasses.png",
    "Overlay:Heart Meme.png"
])

# Compose final image
result = composer.compose(nft_id=1234)
```

## Text Overlays

### Font Styles (4 types)

1. **Impact** - Classic meme font (bold, outlined)
2. **Angelic** - Decorative script font
3. **Chinese** - Chinese character support
4. **Glow** - Neon glow effect

```python
from src.caption_meme import CaptionMeme

captioner = CaptionMeme()

# Add text with Impact font (classic meme style)
captioner.add_caption(
    image=img,
    top_text="GM",
    bottom_text="WAGMI",
    font_style="impact"
)

# Custom positioning and styling
captioner.add_caption(
    image=img,
    top_text="Good Morning",
    bottom_text="Let's Go",
    font_style="glow",
    font_size=60,
    text_color="white"
)
```

## NFT Metadata

Each NFT (0-9999) has metadata including:
- **Attributes**: Background, Skin, Eyes, Hair, Shirt, etc.
- **Rarity scores**: For each trait
- **Image path**: Direct link to PNG file

```python
# Access NFT metadata
metadata = composer.get_nft_metadata(nft_id=5050)

# Returns:
{
    "id": 5050,
    "attributes": {
        "Background": "Baby Pink",
        "Skin": "Peach",
        "Eyes": "Brown",
        "Hair": "Long Black",
        "Shirt": "White Tee"
    },
    "rarity": {...}
}
```

## Common Use Cases

### 1. Generate Random GM Post

```python
generator = MemeGeneratorV2()

output = generator.generate_gm_meme()
# Returns random NFT with "GM" text and random accessories
```

### 2. Create Themed Meme

```python
# Crypto-themed
output = generator.generate_themed_meme(theme="crypto")

# Milady culture
output = generator.generate_themed_meme(theme="milady")
```

### 3. Custom Composition

```python
composer = MiladyComposer()

# Start with specific NFT
composer.set_base(nft_id=1234)

# Add accessories
composer.add_layer("Hat:Beret.png")
composer.add_layer("Glasses:Heart Shaped.png")

# Add overlay effect
composer.add_layer("Overlay:Sparkles.png")

# Compose and save
result = composer.compose()
result.save("output/my_meme.png")
```

## File Locations

- **NFT Images**: `assets/milady_nfts/images/` (10,000 PNGs)
- **Layers**: `assets/milady_layers/` (6 subdirectories)
- **Metadata**: `assets/milady_nfts/metadata.json`
- **Output**: `output/` directory

## Installation

### 1. Download NFT Assets

```bash
# Download all 10,000 NFTs (requires ~500MB)
python scripts/download_nfts.py

# Download all 324 layers
python scripts/download_layers.py

# Check for missing assets
python scripts/check_missing.py
```

### 2. Install Dependencies

```bash
pip install pillow requests
```

## Advanced Features

### Template System

Pre-defined text templates for quick generation:

```python
# GM templates (30+ variations)
generator.generate_from_template("gm")

# Crypto templates (40+ variations)
generator.generate_from_template("crypto")

# Milady culture templates (25+ variations)
generator.generate_from_template("milady")

# Motivational templates (15+ variations)
generator.generate_from_template("motivational")
```

### Batch Generation

```python
# Generate multiple random memes
outputs = generator.batch_generate(count=10)

# Generate series with same base, different accessories
outputs = generator.generate_series(
    nft_id=5050,
    variations=5
)
```

## Layer Reference

For complete layer listings and examples, see:
- [LAYER_REFERENCE.md](LAYER_REFERENCE.md) - All 324 layers with previews
- [NFT_METADATA.md](NFT_METADATA.md) - NFT attributes and rarity
- [EXAMPLES.md](EXAMPLES.md) - Example generations with code

## Tips & Best Practices

1. **Layer Order Matters**: Overlays appear on top, Necklaces on bottom
2. **Not All Combinations Work**: Some layers may clash visually
3. **Use Natural Language**: PromptParser handles "cool sunglasses" → layer mapping
4. **Check Asset Availability**: Run `check_missing.py` if layers don't load
5. **Output Resolution**: Final images are 1000x1250 (Milady standard)

## Troubleshooting

**Missing NFT images?**
```bash
python scripts/download_nfts.py
```

**Layer not found?**
```bash
# Check available layers
ls assets/milady_layers/Hat/

# Download missing layers
python scripts/download_layers.py
```

**Text not rendering?**
- Ensure font files are in `assets/fonts/`
- Use fallback font: `font_style="impact"`

## Cost

All generation is **FREE** - runs locally with Pillow (no API calls).

---

**Related Skills:**
- [ai-image-effects](../ai-image-effects/SKILL.md) - Add AI effects (Illusion, FLUX)
- [lark-bot-integration](../lark-bot-integration/SKILL.md) - Deploy as Lark bot
