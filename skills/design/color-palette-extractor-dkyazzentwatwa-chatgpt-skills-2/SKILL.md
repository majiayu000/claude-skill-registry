---
name: color-palette-extractor
description: Extract dominant colors from images, generate color palettes, and export as CSS, JSON, or ASE with K-means clustering.
---

# Color Palette Extractor

Extract dominant colors from images and generate color palettes with multiple export formats.

## Features

- **Dominant Colors**: Extract N most dominant colors using K-means
- **Color Schemes**: Generate complementary, analogous, triadic schemes
- **Multiple Formats**: Export as CSS, JSON, ASE (Adobe Swatch), ACO (Photoshop)
- **Color Analysis**: RGB, HEX, HSL, HSV values
- **Visualization**: Palette swatches, color distribution charts
- **Batch Processing**: Extract palettes from multiple images
- **Similarity Matching**: Find similar colors across palettes

## Quick Start

```python
from color_palette_extractor import ColorPaletteExtractor

extractor = ColorPaletteExtractor()

# Extract colors
extractor.load('image.jpg')
palette = extractor.extract_colors(n_colors=5)

# Export
extractor.export_css('palette.css')
extractor.export_json('palette.json')
extractor.save_swatch('swatch.png')
```

## CLI Usage

```bash
# Extract 5 colors
python color_palette_extractor.py --input image.jpg --colors 5 --output palette.json

# With CSS export
python color_palette_extractor.py --input image.jpg --colors 8 --css palette.css --swatch swatch.png

# Batch mode
python color_palette_extractor.py --batch images/ --colors 5 --output palettes/
```

## Dependencies

- pillow>=10.0.0
- scikit-learn>=1.3.0
- numpy>=1.24.0
- matplotlib>=3.7.0
