---
name: background-remover
description: Remove backgrounds from images using segmentation. Support for color-based, edge detection, and AI-assisted removal methods. Batch processing available.
---

# Background Remover

Remove backgrounds from images using multiple detection methods.

## Features

- **Color-Based Removal**: Remove solid color backgrounds
- **Edge Detection**: Detect subject edges for removal
- **GrabCut Algorithm**: Interactive foreground extraction
- **Batch Processing**: Process multiple images
- **Transparency Output**: Export with alpha channel
- **Background Replacement**: Replace with color or image

## Quick Start

```python
from background_remover import BackgroundRemover

remover = BackgroundRemover()

# Simple removal
remover.load("photo.jpg")
remover.remove_background()
remover.save("photo_transparent.png")

# Remove specific color
remover.load("product.jpg")
remover.remove_color((255, 255, 255), tolerance=30)  # Remove white
remover.save("product_clean.png")

# Replace background
remover.load("portrait.jpg")
remover.remove_background()
remover.replace_background(color=(0, 120, 255))  # Blue background
remover.save("portrait_blue.png")
```

## CLI Usage

```bash
# Remove background (auto-detect)
python background_remover.py --input photo.jpg --output result.png

# Remove specific color
python background_remover.py --input image.jpg --color "255,255,255" --tolerance 30 -o clean.png

# Use GrabCut method
python background_remover.py --input photo.jpg --method grabcut -o result.png

# Replace background with color
python background_remover.py --input photo.jpg --replace-color "0,120,255" -o result.png

# Replace background with image
python background_remover.py --input photo.jpg --replace-image bg.jpg -o result.png

# Batch process
python background_remover.py --batch input_folder/ --output-dir output/ --method edge
```

## API Reference

### BackgroundRemover Class

```python
class BackgroundRemover:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'BackgroundRemover'
    def load_array(self, array: np.ndarray) -> 'BackgroundRemover'

    # Removal Methods
    def remove_background(self, method: str = "auto") -> 'BackgroundRemover'
    def remove_color(self, color: Tuple, tolerance: int = 20) -> 'BackgroundRemover'
    def remove_edges(self, threshold: int = 50) -> 'BackgroundRemover'
    def grabcut(self, rect: Tuple = None, iterations: int = 5) -> 'BackgroundRemover'

    # Background Operations
    def replace_background(self, color: Tuple = None, image: str = None) -> 'BackgroundRemover'
    def add_shadow(self, offset: Tuple = (5, 5), blur: int = 10) -> 'BackgroundRemover'

    # Refinement
    def refine_edges(self, feather: int = 2) -> 'BackgroundRemover'
    def expand_mask(self, pixels: int = 2) -> 'BackgroundRemover'
    def contract_mask(self, pixels: int = 2) -> 'BackgroundRemover'

    # Output
    def save(self, filepath: str, quality: int = 95) -> str
    def get_image(self) -> Image
    def get_mask(self) -> Image

    # Batch Processing
    def batch_process(self, input_dir: str, output_dir: str,
                     method: str = "auto") -> List[str]
```

## Removal Methods

### Auto Detection
```python
# Automatically choose best method
remover.remove_background(method="auto")
```

### Color-Based Removal
```python
# Remove white background
remover.remove_color((255, 255, 255), tolerance=30)

# Remove green screen
remover.remove_color((0, 255, 0), tolerance=50)

# Remove any solid color
remover.remove_color((200, 200, 200), tolerance=40)
```

### Edge Detection
```python
# Use edge detection to find subject
remover.remove_edges(threshold=50)
```

### GrabCut (OpenCV)
```python
# Full image GrabCut
remover.grabcut(iterations=5)

# With bounding rectangle hint
remover.grabcut(rect=(50, 50, 400, 300), iterations=10)
```

## Background Replacement

### Solid Color
```python
remover.remove_background()
remover.replace_background(color=(255, 255, 255))  # White
remover.replace_background(color=(0, 0, 0))        # Black
remover.replace_background(color=(135, 206, 235))  # Sky blue
```

### Image Background
```python
remover.remove_background()
remover.replace_background(image="office_bg.jpg")
```

### Transparent (Default)
```python
remover.remove_background()
remover.save("transparent.png")  # PNG preserves alpha
```

## Edge Refinement

```python
# Soften edges with feathering
remover.refine_edges(feather=3)

# Expand mask to include more area
remover.expand_mask(pixels=2)

# Contract mask for tighter crop
remover.contract_mask(pixels=2)
```

## Example Workflows

### Product Photography
```python
remover = BackgroundRemover()

# Remove white studio background
remover.load("product_photo.jpg")
remover.remove_color((255, 255, 255), tolerance=25)
remover.refine_edges(feather=2)
remover.save("product_transparent.png")
```

### Portrait Editing
```python
remover = BackgroundRemover()

# Remove background from portrait
remover.load("portrait.jpg")
remover.grabcut(iterations=8)
remover.refine_edges(feather=3)

# Add professional background
remover.replace_background(color=(220, 220, 220))
remover.add_shadow(offset=(5, 5), blur=15)
remover.save("portrait_professional.jpg")
```

### Green Screen Removal
```python
remover = BackgroundRemover()

remover.load("greenscreen_video_frame.jpg")
remover.remove_color((0, 255, 0), tolerance=60)
remover.replace_background(image="virtual_bg.jpg")
remover.save("composited.jpg")
```

### Batch Processing
```python
remover = BackgroundRemover()

processed = remover.batch_process(
    input_dir="product_photos/",
    output_dir="processed/",
    method="color",
    color=(255, 255, 255),
    tolerance=30
)

print(f"Processed {len(processed)} images")
```

## Output Formats

- **PNG**: Preserves transparency (recommended)
- **WEBP**: Smaller file, supports alpha
- **JPEG**: No transparency (use with replace_background)

## Tips for Best Results

1. **White/Solid Backgrounds**: Use `remove_color()` method
2. **Complex Backgrounds**: Use `grabcut()` method
3. **High Contrast Subjects**: Edge detection works well
4. **Portraits**: GrabCut with edge refinement
5. **Product Photos**: Color removal with feathering

## Limitations

- Best results with high contrast between subject and background
- Complex hair/fur edges may need manual touch-up
- Transparent or semi-transparent subjects are challenging
- Very busy backgrounds may require manual assistance

## Dependencies

- pillow>=10.0.0
- opencv-python>=4.8.0
- numpy>=1.24.0
- scikit-image>=0.21.0
