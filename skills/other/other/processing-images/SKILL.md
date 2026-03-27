---
name: processing-images
description: "Image processing toolkit awareness. Use when: user uploads images for manipulation, requests format conversion, batch processing, compositing, resizing, optimization, analysis, effects, metadata inspection, montages, animated GIFs, color correction, or any image-related task. Also use when working with screenshots, photos, diagrams, icons, or visual assets. Triggers on 'resize', 'crop', 'convert', 'compress', 'optimize', 'thumbnail', 'watermark', 'montage', 'collage', 'gif', 'sprite sheet', 'color space', 'metadata', 'EXIF', 'compare images', 'diff', 'overlay', 'composite', 'batch process', 'image analysis', 'histogram', 'blur', 'sharpen', 'rotate', 'flip', 'border', 'shadow', 'round corners', 'favicon', 'icon set'."
metadata:
  version: 0.1.0
---

# Image Processing Tools

This container has a rich image processing toolkit. Before writing any image code, scan this inventory to pick the best tool for the job — don't default to Pillow for everything.

## Tool Selection by Task

### Format Conversion & Batch Operations
**ImageMagick `convert`** is the default choice. Handles 260+ formats, single command, no code needed.
```
convert input.png output.webp
convert input.png -quality 85 output.jpg
mogrify -format webp *.png          # batch in-place
```
For animated formats (GIF↔WebP↔APNG, video↔frames), prefer **ffmpeg**.

### Resize, Crop, Thumbnails
**ImageMagick** for CLI one-liners. **Pillow** when already in Python pipeline.
```
convert input.jpg -resize 800x600 output.jpg          # fit within box
convert input.jpg -resize 800x600^ -gravity center -extent 800x600 output.jpg  # fill+crop
convert input.jpg -thumbnail 200x200^ -gravity center -extent 200x200 thumb.jpg
```
IM supports 30+ resize filters: `-filter Lanczos` (sharp downscale), `-filter Mitchell` (balanced), `-filter Point` (nearest-neighbor/pixel art).

### Compositing & Overlays
**ImageMagick `composite`** or `convert` with `-composite`. Supports all Porter-Duff modes.
```
composite -gravity southeast watermark.png photo.jpg output.jpg
convert base.png overlay.png -gravity center -composite result.png
```
For complex multi-layer work or programmatic positioning, use **Pillow** (`Image.paste`, `Image.alpha_composite`).

### Montages, Collages, Contact Sheets
**ImageMagick `montage`** — purpose-built for grid layouts.
```
montage *.jpg -geometry 200x200+5+5 -tile 4x3 sheet.jpg
montage *.png -label '%f' -geometry +4+4 catalog.png
```

### Animated GIFs & Frame Sequences
**ImageMagick** for simple GIF assembly. **ffmpeg** for anything involving timing control, video sources, or optimization.
```
convert -delay 10 -loop 0 frame_*.png animation.gif        # IM
ffmpeg -framerate 10 -i frame_%03d.png -vf palettegen palette.png && \
ffmpeg -framerate 10 -i frame_%03d.png -i palette.png -lavfi paletteuse output.gif  # optimized
```
**imageio** is convenient for frame-sequence GIFs from Python arrays.

### Image Analysis & Measurement
**`identify`** for quick metadata and stats. **OpenCV** for structural analysis. **scikit-image** for scientific measurement.
```
identify -verbose image.png          # full metadata dump
identify -format '%wx%h %[colorspace] %[depth]bit' image.png   # targeted
```
- **OpenCV** (`cv2`): histograms, contour detection, template matching, edge detection, color distribution
- **scikit-image** (`skimage`): region properties, morphology, thresholding (Otsu, adaptive), feature detection (SIFT via OpenCV, ORB), SSIM comparison
- **scipy.ndimage**: convolution, interpolation, labeling connected components

### Image Comparison & Diffing
**ImageMagick `compare`** produces visual diffs directly.
```
compare image1.png image2.png diff.png
compare -metric RMSE image1.png image2.png null: 2>&1   # numeric similarity
```
For structural similarity: `skimage.metrics.structural_similarity` (SSIM).

### Color Operations
**ImageMagick** handles color space conversion, channel manipulation, color quantization.
```
convert input.jpg -colorspace Gray output.jpg
convert input.png -colors 16 reduced.png           # quantize
convert input.jpg -modulate 110,130,100 output.jpg  # brightness,saturation,hue
convert input.png -channel R -separate red_channel.png
```
For programmatic color analysis (dominant colors, palettes): **OpenCV** k-means on pixel arrays, or **Pillow** `getcolors()`.

### Effects & Filters
**ImageMagick** has extensive built-in effects:
```
convert in.png -blur 0x3 out.png              # Gaussian blur
convert in.png -sharpen 0x1 out.png
convert in.png -shadow 60x4+2+2 out.png       # drop shadow
convert in.png -vignette 0x40 out.png
convert in.png -sketch 0x10+120 out.png
convert in.png -charcoal 2 out.png
convert in.png -edge 1 out.png
convert in.png -emboss 1 out.png
convert in.png \( +clone -background black -shadow 60x4+0+0 \) +swap -background none -layers merge +repage rounded.png
```
For advanced/custom convolution kernels: **scipy.ndimage** or **OpenCV**.

### Metadata & EXIF
**`identify -verbose`** reads all metadata. **Pillow** reads/writes EXIF programmatically.
```
identify -verbose image.jpg | grep -A20 'Properties:'
```
```python
from PIL import Image
img = Image.open("photo.jpg")
exif = img.getexif()  # dict-like access to EXIF tags
```
Note: no `exiftool` in this container. Use `identify` or Pillow for metadata tasks.

### Icons, Favicons, App Icons
**ImageMagick** generates multi-size ICO files directly.
```
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 favicon.ico
```
For icon sets (iOS/Android), batch-resize with `convert` or `mogrify` to each required size.

### PDF & EPS (limited)
ImageMagick can read/write PDF and EPS but **Ghostscript is not installed** — complex PDF rasterization may fail. For PDF-to-image, prefer **Pillow** (for simple cases), **pdfplumber** (text/table extraction), or the **pdf skill** (for full PDF manipulation). IM's built-in PDF delegate handles basic operations.

### Seam Carving (Content-Aware Resize)
ImageMagick has **Liquid Rescale** (LQR) built in:
```
convert input.jpg -liquid-rescale 80x100%! output.jpg   # shrink width 20%, preserve content
```

### SVG Handling
ImageMagick rasterizes SVG via its built-in delegate. For SVG→PNG at specific sizes:
```
convert -density 300 input.svg -resize 800x output.png
```
No Inkscape or rsvg-convert available. For SVG manipulation, work with the XML directly or use Python's `lxml`.

## Complete Tool Inventory

| Tool | Type | Key Strength |
|---|---|---|
| **ImageMagick 6.9** | CLI suite | 260 formats, effects, compositing, batch ops |
| **ffmpeg** | CLI | Video/animation, frame extraction, optimized GIFs |
| **Graphviz** | CLI | Diagram→image rendering (dot, neato, etc.) |
| **LibreOffice** | CLI | Document→image conversion |
| **Pillow 12.1** | Python | General-purpose, EXIF, drawing, WebP/AVIF, freetype |
| **OpenCV 4.13** | Python | Computer vision, histograms, contours, morphology |
| **scikit-image 0.26** | Python | Scientific analysis, SSIM, segmentation, features |
| **Wand 0.6** | Python | Full ImageMagick API from Python |
| **imageio 2.37** | Python | Unified I/O, GIF frame sequences |
| **scipy.ndimage** | Python | Convolution, interpolation, labeling |
| **numpy** | Python | Raw pixel array math |
| **reportlab** | Python | PDF generation with embedded images |

## Key Constraints

- **No Ghostscript** — PDF/EPS rasterization is limited to IM's built-in delegate
- **No potrace/autotrace** — bitmap-to-vector tracing unavailable
- **No standalone optimizers** — no optipng, pngquant, jpegoptim, gifsicle (use IM quality settings or ffmpeg instead)
- **No exiftool** — use `identify` or Pillow for metadata
- **No Inkscape** — SVG manipulation is XML-level only
- **HEIC/AVIF read-only** in ImageMagick; Pillow supports AVIF read/write
- **ImageMagick is v6** — use `convert`/`identify` commands, not `magick` (v7 syntax)
