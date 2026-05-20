---
name: photo-collage-maker
description: Create photo collages with grid layouts, custom arrangements, borders, and backgrounds. Combine multiple images into single compositions.
---

# Photo Collage Maker

Create beautiful photo collages from multiple images.

## Features

- **Grid Layouts**: 2x2, 3x3, custom grids
- **Custom Arrangements**: Free-form positioning
- **Borders**: Add spacing and frames
- **Backgrounds**: Solid colors, gradients, images
- **Image Fitting**: Fit, fill, stretch options
- **Text Labels**: Add captions to images
- **Templates**: Pre-built collage templates

## Quick Start

```python
from collage_maker import CollageMaker

collage = CollageMaker()

# Simple 2x2 grid
collage.grid(2, 2, gap=10)
collage.add_images(["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"])
collage.save("collage.jpg")

# Custom layout
collage.canvas(1200, 800)
collage.add_image("main.jpg", x=0, y=0, width=800, height=800)
collage.add_image("side1.jpg", x=800, y=0, width=400, height=400)
collage.add_image("side2.jpg", x=800, y=400, width=400, height=400)
collage.save("custom_collage.jpg")
```

## CLI Usage

```bash
# 2x2 grid collage
python collage_maker.py --grid 2x2 --images img1.jpg img2.jpg img3.jpg img4.jpg -o collage.jpg

# 3x3 grid with gap
python collage_maker.py --grid 3x3 --gap 10 --images photos/*.jpg -o grid.jpg

# With background color
python collage_maker.py --grid 2x3 --bg-color "255,255,255" --images *.jpg -o collage.jpg

# Template layout
python collage_maker.py --template magazine --images *.jpg -o magazine.jpg
```

## API Reference

### CollageMaker Class

```python
class CollageMaker:
    def __init__(self)

    # Canvas Setup
    def canvas(self, width: int, height: int, bg_color: Tuple = (255,255,255)) -> 'CollageMaker'
    def grid(self, rows: int, cols: int, gap: int = 0) -> 'CollageMaker'
    def template(self, name: str) -> 'CollageMaker'

    # Adding Images
    def add_images(self, image_paths: List[str], fit: str = "fill") -> 'CollageMaker'
    def add_image(self, path: str, x: int, y: int, width: int, height: int,
                 fit: str = "fill") -> 'CollageMaker'

    # Styling
    def set_background(self, color: Tuple = None, image: str = None) -> 'CollageMaker'
    def set_border(self, width: int, color: Tuple = (255,255,255)) -> 'CollageMaker'
    def set_gap(self, gap: int) -> 'CollageMaker'
    def rounded_corners(self, radius: int) -> 'CollageMaker'

    # Text
    def add_text(self, text: str, x: int, y: int, font_size: int = 24,
                color: Tuple = (0,0,0)) -> 'CollageMaker'

    # Output
    def save(self, filepath: str, quality: int = 95) -> str
    def get_image(self) -> Image
```

## Templates

- **grid_2x2**: Simple 2x2 grid
- **grid_3x3**: 3x3 grid layout
- **magazine**: Large image with smaller thumbnails
- **pinterest**: Masonry-style vertical layout
- **polaroid**: Images with white borders and captions
- **story**: Vertical mobile-style collage

## Dependencies

- pillow>=10.0.0
- numpy>=1.24.0
