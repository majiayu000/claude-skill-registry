---
name: sprite-sheet-generator
description: Combine multiple images into sprite sheets with customizable grid layouts and generate CSS sprite maps for web development.
---

# Sprite Sheet Generator

Combine multiple images into optimized sprite sheets with CSS generation.

## Features

- **Grid Layouts**: Auto or custom grid arrangements
- **Smart Packing**: Optimize sprite placement
- **CSS Generation**: Auto-generate sprite CSS classes
- **Transparent Backgrounds**: Preserve alpha channels
- **Padding/Margins**: Control spacing between sprites
- **Batch Processing**: Process multiple sprite sets

## Quick Start

```python
from sprite_sheet_generator import SpriteSheetGenerator

gen = SpriteSheetGenerator()
gen.add_images_from_dir('icons/')
gen.generate(output='sprites.png', grid=(4, 4))
gen.generate_css('sprites.css', class_prefix='icon')
```

## CLI Usage

```bash
python sprite_sheet_generator.py --input icons/ --output sprites.png --grid 4x4 --css sprites.css
```

## Dependencies

- pillow>=10.0.0
