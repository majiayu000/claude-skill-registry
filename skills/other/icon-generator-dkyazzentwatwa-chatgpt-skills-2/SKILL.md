---
name: icon-generator
description: Generate app icons and favicons in multiple sizes from a single source image. Support for iOS, Android, web favicon, and social media formats.
---

# Icon Generator

Generate app icons in all required sizes from a single image.

## Features

- **Multi-Platform**: iOS, Android, Web, macOS, Windows
- **Batch Generation**: All sizes from one source
- **Smart Scaling**: Maintain quality at all sizes
- **Format Support**: PNG, ICO, ICNS
- **Presets**: Platform-specific size sets
- **Rounding Options**: Square or rounded corners

## Quick Start

```python
from icon_generator import IconGenerator

gen = IconGenerator()

# Generate all iOS icons
gen.load("logo.png")
gen.generate_ios("ios_icons/")

# Generate all favicon sizes
gen.load("logo.png")
gen.generate_favicon("favicon/")

# Generate specific sizes
gen.load("logo.png")
gen.generate_sizes([16, 32, 64, 128, 256, 512], "icons/")
```

## CLI Usage

```bash
# Generate iOS icons
python icon_generator.py --input logo.png --preset ios --output-dir ios_icons/

# Generate Android icons
python icon_generator.py --input logo.png --preset android --output-dir android_icons/

# Generate favicons
python icon_generator.py --input logo.png --preset favicon --output-dir favicon/

# Custom sizes
python icon_generator.py --input logo.png --sizes 16 32 64 128 256 -o icons/

# Generate all platforms
python icon_generator.py --input logo.png --preset all --output-dir app_icons/
```

## API Reference

### IconGenerator Class

```python
class IconGenerator:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'IconGenerator'

    # Generation
    def generate_ios(self, output_dir: str) -> List[str]
    def generate_android(self, output_dir: str) -> List[str]
    def generate_favicon(self, output_dir: str) -> List[str]
    def generate_macos(self, output_dir: str) -> List[str]
    def generate_windows(self, output_dir: str) -> List[str]
    def generate_pwa(self, output_dir: str) -> List[str]
    def generate_all(self, output_dir: str) -> Dict[str, List[str]]

    # Custom
    def generate_sizes(self, sizes: List[int], output_dir: str,
                      prefix: str = "icon") -> List[str]
    def generate_single(self, size: int, output: str) -> str

    # Options
    def set_rounding(self, radius_percent: float) -> 'IconGenerator'
    def set_padding(self, padding_percent: float) -> 'IconGenerator'
    def set_background(self, color: Tuple) -> 'IconGenerator'
```

## Platform Sizes

### iOS (App Store)
- 20x20, 29x29, 40x40, 60x60, 76x76, 83.5x83.5
- 1024x1024 (App Store)
- @2x and @3x variants

### Android
- mdpi: 48x48
- hdpi: 72x72
- xhdpi: 96x96
- xxhdpi: 144x144
- xxxhdpi: 192x192
- Play Store: 512x512

### Favicon
- 16x16, 32x32, 48x48
- 180x180 (Apple Touch)
- 192x192, 512x512 (PWA)

### Windows
- 16x16, 32x32, 48x48
- 256x256 (ICO)

## Dependencies

- pillow>=10.0.0
