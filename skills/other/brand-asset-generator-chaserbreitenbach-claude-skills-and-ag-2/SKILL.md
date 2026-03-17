---
name: brand-asset-generator
version: 1.0.0
description: |
  Generate consistent brand assets for social media, print, and digital use
  from a single brand configuration with automated sizing and formatting.
author: QuantQuiver AI R&D
license: MIT

category: domain
tags:
  - branding
  - design
  - social-media
  - assets
  - graphics
  - marketing

dependencies:
  skills:
    - branded-document-suite
  python: ">=3.9"
  packages:
    - pillow
    - svgwrite
    - pyyaml
  tools:
    - code_execution
    - bash

triggers:
  - "brand assets"
  - "social media graphics"
  - "logo variations"
  - "marketing collateral"
  - "brand kit"
  - "export assets"
---

# Brand Asset Generator

## Purpose

Generate consistent brand assets for social media, print, and digital use from a single brand configuration. Produces properly sized assets for all major platforms with consistent styling.

**Problem Space:**
- Manual asset creation is time-consuming
- Platform size requirements constantly change
- Maintaining consistency across assets is difficult
- Design tools have steep learning curves

**Solution Approach:**
- Template-based generation from brand config
- Pre-configured platform size presets
- Automated export to multiple formats
- Consistent typography and color application

## When to Use

- Setting up new brand presence
- Creating social media kits
- Generating marketing collateral
- Producing email signatures
- Creating presentation templates
- Exporting assets for different platforms

## When NOT to Use

- Complex custom illustrations
- Photography editing
- Full brand identity design (use design professionals)
- Highly custom one-off designs

---

## Core Instructions

### Platform Size Reference

```yaml
social_media_sizes:
  instagram:
    post_square: [1080, 1080]
    post_portrait: [1080, 1350]
    post_landscape: [1080, 566]
    story: [1080, 1920]
    profile: [320, 320]

  twitter_x:
    post: [1200, 675]
    header: [1500, 500]
    profile: [400, 400]

  linkedin:
    post: [1200, 1200]
    article_cover: [1200, 628]
    company_cover: [1128, 191]
    profile: [400, 400]

  facebook:
    post: [1200, 630]
    cover: [820, 312]
    profile: [170, 170]
    event_cover: [1920, 1005]

  youtube:
    thumbnail: [1280, 720]
    channel_art: [2560, 1440]

print_sizes:
  business_card:
    us: [3.5, 2, 300]  # inches, dpi
    eu: [85, 55, 300]  # mm, dpi

  letterhead:
    us: [8.5, 11, 300]
    a4: [210, 297, 300]

  flyer:
    half_letter: [5.5, 8.5, 300]
    a5: [148, 210, 300]

digital_sizes:
  email_signature: [600, 200]
  favicon: [32, 32]
  app_icon: [1024, 1024]
  og_image: [1200, 630]
```

### Standard Procedures

#### 1. Load Brand Configuration

```python
import yaml
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class BrandAssetGenerator:
    def __init__(self, brand_config_path: str):
        with open(brand_config_path) as f:
            self.config = yaml.safe_load(f)

        self.colors = self.config['colors']
        self.typography = self.config['typography']
        self.assets = self.config.get('assets', {})

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

#### 2. Generate Social Media Assets

```python
def generate_social_kit(self, output_dir: str, platforms: list = None):
    """
    Generate complete social media asset kit.

    Args:
        output_dir: Directory to save assets
        platforms: List of platforms (default: all)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    platforms = platforms or ['instagram', 'twitter_x', 'linkedin', 'facebook']

    for platform in platforms:
        platform_path = output_path / platform
        platform_path.mkdir(exist_ok=True)

        if platform == 'instagram':
            self._generate_instagram_assets(platform_path)
        elif platform == 'twitter_x':
            self._generate_twitter_assets(platform_path)
        # ... other platforms

def _generate_instagram_assets(self, output_path: Path):
    """Generate Instagram asset variants."""
    sizes = {
        'post_square': (1080, 1080),
        'post_portrait': (1080, 1350),
        'story': (1080, 1920),
        'profile': (320, 320),
    }

    for name, size in sizes.items():
        # Create base image with brand background
        img = self._create_branded_background(size)

        # Add logo centered
        img = self._add_centered_logo(img)

        # Save
        img.save(output_path / f'{name}.png', 'PNG')

        # Also save as template (with guides)
        template = self._add_safe_zone_guides(img.copy())
        template.save(output_path / f'{name}_template.png', 'PNG')

def _create_branded_background(self, size: tuple, style: str = 'gradient') -> Image:
    """Create branded background image."""
    width, height = size

    if style == 'solid':
        img = Image.new('RGB', size, self.hex_to_rgb(self.colors['primary']))
    elif style == 'gradient':
        img = self._create_gradient(size,
            self.hex_to_rgb(self.colors['primary']),
            self.hex_to_rgb(self.colors['primary_dark']))
    elif style == 'secondary':
        img = Image.new('RGB', size, self.hex_to_rgb(self.colors['secondary']))

    return img

def _create_gradient(self, size: tuple, color1: tuple, color2: tuple) -> Image:
    """Create vertical gradient image."""
    width, height = size
    img = Image.new('RGB', size)

    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

        for x in range(width):
            img.putpixel((x, y), (r, g, b))

    return img
```

#### 3. Generate Logo Variations

```python
def generate_logo_variations(self, output_dir: str):
    """
    Generate logo in multiple formats and color variations.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    variations = [
        ('primary', self.colors['primary'], '#FFFFFF'),
        ('white', '#FFFFFF', self.colors['secondary']),
        ('dark', self.colors['secondary'], '#FFFFFF'),
        ('monochrome', '#000000', '#FFFFFF'),
    ]

    sizes = [
        ('small', 100),
        ('medium', 250),
        ('large', 500),
        ('xlarge', 1000),
    ]

    for var_name, fg_color, bg_color in variations:
        var_path = output_path / var_name
        var_path.mkdir(exist_ok=True)

        for size_name, size in sizes:
            # Generate PNG with background
            img = self._generate_logo_image(size, fg_color, bg_color)
            img.save(var_path / f'logo_{size_name}.png', 'PNG')

            # Generate PNG with transparency
            img_transparent = self._generate_logo_image(size, fg_color, None)
            img_transparent.save(var_path / f'logo_{size_name}_transparent.png', 'PNG')
```

#### 4. Generate Print Assets

```python
def generate_business_card(self, output_dir: str,
                          name: str, title: str,
                          email: str, phone: str = None):
    """
    Generate business card design.
    """
    # US standard size at 300 DPI
    width = int(3.5 * 300)  # 1050px
    height = int(2 * 300)   # 600px

    # Create front
    front = Image.new('RGB', (width, height),
                     self.hex_to_rgb(self.colors['surface_primary']))
    draw = ImageDraw.Draw(front)

    # Add logo (top left)
    logo_size = 150
    # ... add logo

    # Add contact info
    font_name = ImageFont.truetype('fonts/Inter-SemiBold.ttf', 48)
    font_title = ImageFont.truetype('fonts/Inter-Regular.ttf', 36)
    font_contact = ImageFont.truetype('fonts/Inter-Regular.ttf', 30)

    y_offset = 200
    draw.text((100, y_offset), name,
             fill=self.hex_to_rgb(self.colors['text_primary']),
             font=font_name)

    y_offset += 60
    draw.text((100, y_offset), title,
             fill=self.hex_to_rgb(self.colors['text_secondary']),
             font=font_title)

    y_offset += 80
    draw.text((100, y_offset), email,
             fill=self.hex_to_rgb(self.colors['text_secondary']),
             font=font_contact)

    if phone:
        y_offset += 45
        draw.text((100, y_offset), phone,
                 fill=self.hex_to_rgb(self.colors['text_secondary']),
                 font=font_contact)

    # Add brand accent line
    draw.rectangle([0, height - 20, width, height],
                  fill=self.hex_to_rgb(self.colors['primary']))

    # Save with bleed
    front.save(Path(output_dir) / 'business_card_front.png', 'PNG')

    # Create back (simple brand design)
    back = Image.new('RGB', (width, height),
                    self.hex_to_rgb(self.colors['secondary']))
    # ... add centered logo
    back.save(Path(output_dir) / 'business_card_back.png', 'PNG')
```

### Decision Framework

**Asset Format Selection:**

| Use Case | Format | Why |
|----------|--------|-----|
| Web graphics | PNG | Lossless, transparency |
| Photos | JPEG | Smaller file size |
| Scalable logos | SVG | Resolution independent |
| Print | PDF/TIFF | High quality, CMYK |
| Icons | ICO/PNG | Platform requirements |

**Color Space:**
- Digital: RGB/sRGB
- Print: CMYK
- Web: Hex colors

---

## Templates

### Brand Asset Manifest

```yaml
# brand-assets.yaml
brand:
  name: "Company Name"
  tagline: "Your tagline"

assets:
  social_media:
    instagram:
      - post_square
      - post_portrait
      - story
      - profile
    twitter:
      - post
      - header
      - profile
    linkedin:
      - post
      - cover
      - profile

  logo_variations:
    colors:
      - primary
      - white
      - dark
      - monochrome
    sizes:
      - small: 100
      - medium: 250
      - large: 500

  print:
    - business_card
    - letterhead

  digital:
    - email_signature
    - favicon
    - og_image

output:
  directory: "./brand-assets"
  formats:
    images: ["png", "jpg"]
    vectors: ["svg"]
```

### Export Script

```python
#!/usr/bin/env python3
"""
Brand Asset Export Script

Usage:
    python export_assets.py --config brand-config.yaml --output ./assets
"""

import argparse
from brand_asset_generator import BrandAssetGenerator

def main():
    parser = argparse.ArgumentParser(description='Export brand assets')
    parser.add_argument('--config', required=True, help='Brand config YAML')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--platforms', nargs='+', help='Specific platforms')
    args = parser.parse_args()

    generator = BrandAssetGenerator(args.config)

    # Generate all assets
    print("Generating social media kit...")
    generator.generate_social_kit(
        f"{args.output}/social",
        platforms=args.platforms
    )

    print("Generating logo variations...")
    generator.generate_logo_variations(f"{args.output}/logos")

    print("Generating favicons...")
    generator.generate_favicon_set(f"{args.output}/favicons")

    print(f"Assets exported to {args.output}")

if __name__ == "__main__":
    main()
```

---

## Examples

### Example 1: Social Media Launch Kit

**Input**: "Create all social media assets for our brand launch"

**Output**:
```
brand-assets/
├── instagram/
│   ├── post_square.png
│   ├── post_square_template.png
│   ├── story.png
│   └── profile.png
├── twitter/
│   ├── post.png
│   ├── header.png
│   └── profile.png
├── linkedin/
│   ├── post.png
│   ├── cover.png
│   └── profile.png
└── facebook/
    ├── post.png
    ├── cover.png
    └── profile.png
```

### Example 2: Business Card Generation

**Input**: "Generate business cards for John Smith, CTO"

**Output**: Front and back PNG files with:
- Logo placement
- Contact information
- Brand colors
- Print-ready resolution (300 DPI)

---

## Validation Checklist

Before exporting assets:

- [ ] Brand config file validated
- [ ] Logo files accessible
- [ ] Fonts available (or fallbacks specified)
- [ ] Output directory writable
- [ ] Color values valid hex
- [ ] Sizes correct for intended platforms
- [ ] Transparency preserved where needed
- [ ] Resolution appropriate for use case

---

## Related Resources

- Skill: `branded-document-suite` - Document generation
- Skill: `technical-documentation-generator` - Style consistency
- Platform guidelines: Each platform's official size specs
- Color tools: Coolors, Adobe Color

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Social media asset generation
- Logo variation export
- Business card templates
- Favicon generation
