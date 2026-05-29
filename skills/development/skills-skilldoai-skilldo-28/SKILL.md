---
name: pillow
description: Python Imaging Library fork for image processing, format conversion, and manipulation.
version: 12.1.1
ecosystem: python
license: MIT-CMU
generated_with: gpt-4.1
---

## Imports

```python
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageCms
from PIL import ExifTags
```

## Core Patterns

### Opening and Saving Images

```python
from PIL import Image

img = Image.open("input.png")
print(img.size, img.mode, img.format)

img.save("output.jpg", quality=95)
img.save("output.webp", lossless=True)
```

### Resizing and Thumbnails

```python
from PIL import Image

img = Image.open("photo.jpg")

resized = img.resize((800, 600), Image.Resampling.LANCZOS)

thumbnail = img.copy()
thumbnail.thumbnail((200, 200))
thumbnail.save("thumb.jpg")
```

### Color Mode Conversion

```python
from PIL import Image

img = Image.open("photo.jpg")

grayscale = img.convert("L")
rgba = img.convert("RGBA")
```

### Cropping and Rotating

```python
from PIL import Image

img = Image.open("photo.jpg")

cropped = img.crop((left, upper, right, lower))

rotated = img.rotate(45, expand=True, fillcolor=(255, 255, 255))

flipped = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
```

### Drawing on Images

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (400, 300), color="white")
draw = ImageDraw.Draw(img)

draw.rectangle([10, 10, 390, 290], outline="black", width=2)
draw.ellipse([50, 50, 200, 200], fill="blue")
draw.text((210, 100), "Hello", fill="black")

img.save("drawn.png")
```

### Applying Filters

```python
from PIL import Image, ImageFilter

img = Image.open("photo.jpg")

blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
sharpened = img.filter(ImageFilter.SHARPEN)
edges = img.filter(ImageFilter.FIND_EDGES)
```

### ICC Color Management

```python
from PIL import ImageCms

srgb_profile = ImageCms.createProfile("sRGB")
transform = ImageCms.buildTransform(
    "input.icc", "output.icc", "RGB", "RGB"
)
corrected = ImageCms.applyTransform(img, transform)
```

## Configuration

```python
from PIL import Image

Image.MAX_IMAGE_PIXELS = 200_000_000

Image.warnings.simplefilter("error", Image.DecompressionBombWarning)
```

## Pitfalls

### Wrong: Not closing file handles

```python
img = Image.open("large.tiff")
data = img.load()
```

### Right: Use context manager or explicit close

```python
with Image.open("large.tiff") as img:
    data = img.load()
    img.save("output.tiff")
```

### Wrong: Using deprecated resampling constants

```python
resized = img.resize((100, 100), Image.ANTIALIAS)
```

### Right: Use Image.Resampling enum

```python
resized = img.resize((100, 100), Image.Resampling.LANCZOS)
```

### Wrong: Saving RGBA as JPEG

```python
rgba_img = Image.open("logo.png")
rgba_img.save("logo.jpg")
```

### Right: Convert to RGB first

```python
rgba_img = Image.open("logo.png")
rgb_img = rgba_img.convert("RGB")
rgb_img.save("logo.jpg")
```

## References

- [Documentation](https://pillow.readthedocs.io/en/stable/)
- [Source](https://github.com/python-pillow/Pillow)
- [Changelog](https://pillow.readthedocs.io/en/stable/releasenotes/)
- [PyPI](https://pypi.org/project/pillow/)
