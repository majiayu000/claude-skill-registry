---
name: image-filter-lab
description: Apply artistic filters to images including vintage, sepia, B&W, blur, sharpen, vignette, and color adjustments. Create custom filter presets.
---

# Image Filter Lab

Apply professional filters and effects to images.

## Features

- **Color Filters**: Sepia, B&W, color tint, saturation
- **Blur Effects**: Gaussian, motion, radial blur
- **Artistic Filters**: Vintage, film grain, vignette
- **Enhancements**: Sharpen, contrast, brightness
- **Custom Presets**: Save and apply filter combinations
- **Batch Processing**: Apply filters to multiple images

## Quick Start

```python
from image_filter import ImageFilterLab

lab = ImageFilterLab()
lab.load("photo.jpg")

# Apply vintage filter
lab.vintage()
lab.save("photo_vintage.jpg")

# Chain multiple effects
lab.load("photo.jpg")
lab.brightness(1.2).contrast(1.1).saturation(0.8).vignette()
lab.save("photo_edited.jpg")
```

## CLI Usage

```bash
# Apply single filter
python image_filter.py --input photo.jpg --filter vintage --output result.jpg

# Apply multiple filters
python image_filter.py -i photo.jpg --sepia --vignette --sharpen -o result.jpg

# Adjust parameters
python image_filter.py -i photo.jpg --brightness 1.2 --contrast 1.1 -o result.jpg

# Batch process
python image_filter.py --batch photos/ --filter vintage --output-dir filtered/
```

## API Reference

### ImageFilterLab Class

```python
class ImageFilterLab:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'ImageFilterLab'

    # Color Filters
    def grayscale(self) -> 'ImageFilterLab'
    def sepia(self, intensity: float = 1.0) -> 'ImageFilterLab'
    def negative(self) -> 'ImageFilterLab'
    def tint(self, color: Tuple, intensity: float = 0.3) -> 'ImageFilterLab'

    # Adjustments
    def brightness(self, factor: float) -> 'ImageFilterLab'
    def contrast(self, factor: float) -> 'ImageFilterLab'
    def saturation(self, factor: float) -> 'ImageFilterLab'
    def hue(self, shift: int) -> 'ImageFilterLab'
    def temperature(self, value: int) -> 'ImageFilterLab'

    # Blur Effects
    def blur(self, radius: int = 5) -> 'ImageFilterLab'
    def motion_blur(self, size: int = 15, angle: int = 0) -> 'ImageFilterLab'
    def radial_blur(self, amount: int = 10) -> 'ImageFilterLab'

    # Sharpen
    def sharpen(self, factor: float = 1.0) -> 'ImageFilterLab'
    def unsharp_mask(self, radius: int = 2, percent: int = 150) -> 'ImageFilterLab'

    # Artistic
    def vintage(self) -> 'ImageFilterLab'
    def film_grain(self, amount: int = 25) -> 'ImageFilterLab'
    def vignette(self, radius: float = 0.8, intensity: float = 0.5) -> 'ImageFilterLab'
    def posterize(self, levels: int = 4) -> 'ImageFilterLab'
    def solarize(self, threshold: int = 128) -> 'ImageFilterLab'

    # Presets
    def apply_preset(self, preset: str) -> 'ImageFilterLab'
    def save_preset(self, name: str, operations: List) -> None

    # Output
    def save(self, filepath: str, quality: int = 95) -> str
    def reset(self) -> 'ImageFilterLab'

    # Batch
    def batch_process(self, input_dir: str, output_dir: str,
                     filter_func: callable) -> List[str]
```

## Built-in Presets

- **vintage**: Sepia tint, reduced saturation, vignette
- **film**: Slight desaturation, grain, crushed blacks
- **instagram**: High contrast, warm tint, vignette
- **noir**: High contrast B&W, strong vignette
- **warm**: Warm color temperature, increased saturation
- **cool**: Cool color temperature, slightly desaturated
- **dramatic**: High contrast, deep shadows
- **dreamy**: Soft blur, bright highlights, low contrast

## Dependencies

- pillow>=10.0.0
- opencv-python>=4.8.0
- numpy>=1.24.0
