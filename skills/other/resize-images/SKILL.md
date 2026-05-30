---
name: resize-images
description: Batch-resize images for web (WebP at 1920/1200/400px), social (center-cropped WebP at Instagram square/portrait, Twitter/X, LinkedIn), slides (center-cropped JPEG at 1024×768 and 1920×1080), and print (300 DPI JPEG at ARCH A 9×12, ARCH B 12×18, ARCH C 18×24). Asks user for source folder, outputs resized copies into subfolders within that folder.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# /resize-images — Image Resizer for Web, Social, and Print

Resize project photos and renders for web publishing, social media, and print layouts. Always asks the user for the source folder before doing anything. Outputs resized copies into clearly named subfolders — originals are never modified.

## Step 1: Ask for the source folder

Before doing anything else, ask:

> "Which folder contains the images you'd like to resize?"

Wait for the user's response. Accept any valid path — absolute, relative, or with `~`. Expand `~` to the user's home directory.

Then ask:

> "Which outputs do you need? (choose one or more)
> - **Web** — WebP at 1920px (hero), 1200px (standard), 400px (thumb)
> - **Social** — center-cropped WebP: Instagram square (1080×1080), Instagram portrait (1080×1350), Twitter/X (1200×675), LinkedIn (1200×627)
> - **Slides** — center-cropped JPEG: standard 4:3 (1024×768), widescreen 16:9 (1920×1080)
> - **Print** — 300 DPI JPEG at ARCH A (9×12), ARCH B (12×18), ARCH C (18×24)
> - **All**"

## Step 2: Scan the folder

List all image files in the folder (non-recursive). Supported formats: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.webp`.

```python
import os, sys

folder = sys.argv[1]
exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp'}
images = [f for f in os.listdir(folder) if os.path.splitext(f.lower())[1] in exts]
images.sort()
for img in images:
    print(img)
```

Report the count: `"Found N image(s) in [folder]. Ready to resize."`

If the folder is empty or contains no supported images, tell the user and stop.

## Step 3: Check for Pillow

Run this to confirm Pillow is available:

```bash
python3 -c "import PIL; print('ok')" 2>/dev/null || echo "missing"
```

If missing, tell the user:

> "Pillow isn't installed. Run `pip install Pillow` then try again."

Stop if Pillow is unavailable.

## Step 4: Create output folders

Inside the source folder, create one subfolder per requested mode:

- `resized-web/` — if web sizes were requested
- `resized-social/` — if social sizes were requested
- `resized-slides/` — if slides sizes were requested
- `resized-print/` — if print sizes were requested

```python
import os, sys
folder = sys.argv[1]
modes = sys.argv[2:]  # 'web', 'social', 'slides', and/or 'print'
for mode in modes:
    os.makedirs(os.path.join(folder, f"resized-{mode}"), exist_ok=True)
```

## Step 5: Resize images

Run this Python script via Bash, passing the folder path and modes as arguments:

```python
import sys
import os
from PIL import Image

folder = sys.argv[1]
modes = sys.argv[2:]  # 'web', 'social', and/or 'print'

exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp'}
images = [f for f in os.listdir(folder) if os.path.splitext(f.lower())[1] in exts]

WEB_SIZES = [
    ("hero",     1920),
    ("standard", 1200),
    ("thumb",    400),
]

# Social: exact crop dimensions (width, height)
SOCIAL_SIZES = [
    ("social-square",    (1080, 1080)),
    ("social-portrait",  (1080, 1350)),
    ("social-landscape", (1200, 675)),
    ("social-linkedin",  (1200, 627)),
]

# Slides: center-crop to fill slide canvas
SLIDES_SIZES = [
    ("slides-standard", (1024, 768)),   # 4:3
    ("slides-wide",     (1920, 1080)),  # 16:9
]

# ARCH sizes in pixels at 300 DPI: inches × 300
PRINT_SIZES = [
    ("arch-a", (9 * 300,  12 * 300)),   # 2700 × 3600
    ("arch-b", (12 * 300, 18 * 300)),   # 3600 × 5400
    ("arch-c", (18 * 300, 24 * 300)),   # 5400 × 7200
]

def center_crop(img, target_w, target_h):
    """Scale to fill target dimensions, then center-crop."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    scaled_w = int(src_w * scale)
    scaled_h = int(src_h * scale)
    img = img.resize((scaled_w, scaled_h), Image.LANCZOS)
    left = (scaled_w - target_w) // 2
    top  = (scaled_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))

for filename in images:
    stem = os.path.splitext(filename)[0]
    src_path = os.path.join(folder, filename)

    try:
        img = Image.open(src_path)
        # Convert to RGB if needed (handles RGBA, palette, etc.)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        print(f"Processing: {filename} ({img.width}×{img.height})")

        if "web" in modes:
            web_dir = os.path.join(folder, "resized-web")
            for label, max_width in WEB_SIZES:
                out_img = img.copy()
                if out_img.width > max_width:
                    ratio = max_width / out_img.width
                    new_size = (max_width, int(out_img.height * ratio))
                    out_img = out_img.resize(new_size, Image.LANCZOS)
                out_path = os.path.join(web_dir, f"{stem}-{label}.webp")
                out_img.save(out_path, "WEBP", quality=82)
                size_kb = os.path.getsize(out_path) // 1024
                print(f"  {stem}-{label}.webp  ({out_img.width}×{out_img.height})  {size_kb} KB")

        if "social" in modes:
            social_dir = os.path.join(folder, "resized-social")
            for label, (tw, th) in SOCIAL_SIZES:
                out_img = center_crop(img.copy(), tw, th)
                out_path = os.path.join(social_dir, f"{stem}-{label}.webp")
                out_img.save(out_path, "WEBP", quality=85)
                size_kb = os.path.getsize(out_path) // 1024
                print(f"  {stem}-{label}.webp  ({out_img.width}×{out_img.height})  {size_kb} KB")

        if "slides" in modes:
            slides_dir = os.path.join(folder, "resized-slides")
            for label, (tw, th) in SLIDES_SIZES:
                out_img = center_crop(img.copy(), tw, th)
                out_path = os.path.join(slides_dir, f"{stem}-{label}.jpg")
                out_img.save(out_path, "JPEG", quality=92)
                size_kb = os.path.getsize(out_path) // 1024
                print(f"  {stem}-{label}.jpg  ({out_img.width}×{out_img.height})  {size_kb} KB")

        if "print" in modes:
            print_dir = os.path.join(folder, "resized-print")
            for label, (pw, ph) in PRINT_SIZES:
                out_img = img.copy()
                # Fit within the target box, preserving aspect ratio
                out_img.thumbnail((pw, ph), Image.LANCZOS)
                out_path = os.path.join(print_dir, f"{stem}-{label}.jpg")
                out_img.save(out_path, "JPEG", quality=95, dpi=(300, 300))
                size_kb = os.path.getsize(out_path) // 1024
                print(f"  {stem}-{label}.jpg  ({out_img.width}×{out_img.height})  {size_kb} KB")

    except Exception as e:
        print(f"ERROR: {filename} — {e}")

print("\nDone.")
```

Give a progress update for each file as it completes.

## Step 6: Report results

After all files are processed, show a summary:

```
Resized N image(s) → [folder]/resized-web/, resized-social/, resized-print/

Web (resized-web/):
  project-photo-hero.webp          (1920×1385)   138 KB
  project-photo-standard.webp      (1200×866)     62 KB
  project-photo-thumb.webp         (400×288)      11 KB

Social (resized-social/):
  project-photo-social-square.webp    (1080×1080)   74 KB
  project-photo-social-portrait.webp  (1080×1350)   91 KB
  project-photo-social-landscape.webp (1200×675)    65 KB
  project-photo-social-linkedin.webp  (1200×627)    63 KB

Print (resized-print/):
  project-photo-arch-a.jpg         (2700×1949)   959 KB
  project-photo-arch-b.jpg         (3600×2599)  1698 KB
  project-photo-arch-c.jpg         (5019×3623)  3470 KB
```

If any files failed, list them with their error messages.

## Edge Cases

- **Social and slides crops** — center crop always; if a subject is off-center, the user should crop manually before running the skill
- **Portrait images (web/print)** — aspect ratio is always preserved; the image fits within the target dimensions, so a portrait image will be narrower than the target width
- **Images already smaller than the target** — web sizes: skip upscaling, save as-is with the size label; print sizes: save at original resolution with 300 DPI tag; social: upscale to fill (center crop still applies)
- **RGBA / PNG with transparency** — convert to RGB before saving (JPEG and most social WebP don't support alpha)
- **Duplicate filenames** — if two source files share a stem after stripping extension, the second will overwrite the first; warn the user if this happens
- **Read errors** — catch and report per-file, continue processing the rest
