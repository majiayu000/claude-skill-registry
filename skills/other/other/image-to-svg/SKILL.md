---
name: image-to-svg
version: 1.2.0
description: Convert raster images (photos, paintings, illustrations) into SVG vector reproductions. Use when the user uploads an image and asks to reproduce, vectorize, trace, or convert it to SVG. Also use when asked to decompose an image into shapes, create an SVG version of a picture, or faithfully reproduce artwork as vector graphics. Do NOT use for creating original SVG illustrations from text descriptions — only for converting existing raster images.
---
 
# Image to SVG Reproduction
 
Convert raster images into faithful SVG reproductions using data-driven color quantization and contour extraction. **Never hand-draw shapes from visual interpretation** — always extract geometry from the actual pixel data.
 
## Core Principle
 
**Trust the data, not your imagination.** Claude's visual interpretation of images is unreliable for precise color matching, shape positioning, and spatial relationships. Every shape, color, and position must come from computational analysis of the source pixels.
 
## Pipeline Overview
 
```
Source Image → Preprocessing → Color Quantization → Edge Map → Contour Extraction → SVG Assembly
```
 
## Step 1: Preprocessing
 
```python
import cv2
import numpy as np
 
img = cv2.imread('source.jpg')
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
# Edge-preserving blur to remove texture while keeping shape boundaries
# Bilateral filter preserves edges; Gaussian smooths remaining noise
# Use GENTLE settings — aggressive blur destroys subtle color differences
blurred = cv2.bilateralFilter(rgb, 9, 50, 50)
blurred = cv2.GaussianBlur(blurred, (3, 3), 0)
```
 
**Do NOT boost saturation during preprocessing.** This distorts colors away from the original. Color correction, if needed, should be done as a final targeted step.
 
## Step 2: Color Quantization (K-means)
 
```python
# Downscale for fast K-means, then apply centers to full resolution
small = cv2.resize(blurred, (600, 390))
pixels = small.reshape(-1, 3).astype(np.float32)
 
K = 28–36  # More K = finer color separation, but more noise
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 150, 0.1)
_, labels, centers = cv2.kmeans(pixels, K, None, criteria, 8, cv2.KMEANS_PP_CENTERS)
centers = centers.astype(np.uint8)
 
# Apply centers to full-res image
full_px = blurred.reshape(-1, 3).astype(np.float32)
dists = np.linalg.norm(full_px[:, None, :] - centers[None, :, :].astype(np.float32), axis=2)
full_labels = np.argmin(dists, axis=1)
```
 
**Save and inspect the quantized image** before proceeding. It represents the ceiling of what the SVG can achieve.
 
## Step 3: Background Detection
 
Identify background clusters by edge contact — background colors dominate image borders.
 
```python
from collections import Counter
 
label_img = full_labels.reshape(h_orig, w_orig)
counts = Counter(full_labels)
sorted_clusters = sorted(counts.items(), key=lambda x: -x[1])
 
bg_clusters = set()
bg_id = sorted_clusters[0][0]
 
for cid, cnt in sorted_clusters:
    c = centers[cid]
    pct = cnt / len(full_labels) * 100
    mask = (label_img == cid)
    edge_px = mask[0,:].sum() + mask[-1,:].sum() + mask[:,0].sum() + mask[:,-1].sum()
    edge_ratio = edge_px / (2 * (h_orig + w_orig))
    
    # High edge contact + large area = definite background
    if edge_ratio > 0.15 and pct > 3.0:
        bg_clusters.add(cid)
```
 
**Be conservative with background merging.** Only merge colors that are nearly identical to background AND heavily touch edges. Subtle features (like a gray band between two shapes) will be destroyed by aggressive merging. When in doubt, keep the color.

## Step 3b: Structural Edge Map

Use the seeing-images skill to create a reference edge map. This distinguishes real structural boundaries from gradient-transition artifacts during contour extraction.

```python
import sys
sys.path.insert(0, '/mnt/skills/user/seeing-images/scripts')
from see import edges

edge_path = edges(source_path, threshold=50)
edge_img = cv2.imread(edge_path, cv2.IMREAD_GRAYSCALE)
edge_img = cv2.resize(edge_img, (w_orig, h_orig))
```
 
## Step 4: Contour Extraction (Boundary-Aware)

The standard K-means + contour pipeline creates "woodcut" artifacts: thin dark shapes at color boundaries where gradient transitions get quantized into separate dark clusters. Two mechanisms prevent this.

For each non-background color cluster:
 
```python
DARK_LUM_THRESHOLD = 55  # Luminance below this = "dark cluster"
k_morph = np.ones((3,3), np.uint8)
k_dilate = np.ones((3,3), np.uint8)  # MUST be 3x3. 5x5 causes blotchy artifacts.

for cid, cnt in sorted_clusters:
    if cid in bg_clusters:
        continue
    
    c = centers[cid]
    lum = 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
    is_dark = lum < DARK_LUM_THRESHOLD
    
    mask = (label_img == cid).astype(np.uint8) * 255
    
    # FIX 1: Dilate non-dark regions to fill boundary gaps
    # Lighter regions grow ~1.5px, covering the dark artifact zones
    if not is_dark:
        mask = cv2.dilate(mask, k_dilate, iterations=1)
    
    # Morphological cleanup
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_morph, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k_morph, iterations=1)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 40:
            continue
        
        peri = cv2.arcLength(contour, True)
        compactness = (4 * 3.14159 * area / (peri * peri)) if peri > 0 else 1
        
        # FIX 2: Gate dark shapes — keep real features, skip boundary artifacts
        if is_dark:
            contour_mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
            cv2.drawContours(contour_mask, [contour], -1, 255, -1)
            edge_overlap = cv2.bitwise_and(edge_img, contour_mask)
            edge_density = edge_overlap.sum() / max(contour_mask.sum(), 1)
            
            # Keep if: compact (real dark area), edge-aligned, or large
            if not (compactness > 0.08 or edge_density > 0.15
                    or area > (h_orig * w_orig * 0.01)):
                continue  # Skip: thin dark boundary artifact
        
        # Simplify contour to reduce SVG path complexity
        eps = 0.002 * peri
        approx = cv2.approxPolyDP(contour, eps, True)
        
        # Convert to SVG path (simple polygon — smallest file size)
        pts = approx.reshape(-1, 2).astype(float)
        pts[:, 0] *= scale_x  # scale to SVG viewBox
        pts[:, 1] *= scale_y
        
        path_d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
        for p in pts[1:]:
            path_d += f" L {p[0]:.1f},{p[1]:.1f}"
        path_d += " Z"
```

**Why this works**: Boundary artifacts are thin (low compactness) AND don't correspond to real structural edges. Real dark features (eyes, hair, outlines in graphic art) have compact shapes or align with Sobel-detected edges.

**Tuning**:
- `DARK_LUM_THRESHOLD`: 55 works broadly; lower for dark images, higher for bright
- Dilation kernel: 3×3 is the sweet spot. **Do NOT use 5×5** — causes blotchy artifacts in hair/foliage.
- `compactness > 0.08`: Keeps all but the thinnest ribbon artifacts. Previous value of 0.15 was too aggressive — filtered real facial detail.
- `edge_density > 0.15`: Keeps shapes with even modest edge alignment. Previous value of 0.3 filtered legitimate dark features like nostrils, lip shadows, brow lines.
 
## Step 5: Z-Ordering (Painter's Algorithm)
 
Sort shapes by area descending — biggest shapes drawn first (behind), smallest last (on top):
 
```python
shapes.sort(key=lambda x: -x['area'])
```
 
This naturally handles layering: large background elements go behind small foreground details.
 
**Z-order rule for nested shapes:** If shape A contains shape B, A must be drawn BEFORE B. For ring structures (like a red ring with a black center), the order is:
1. Red ring (largest)
2. Any transition band (middle) — AFTER the ring so it paints ON TOP
3. Black center (smallest) — AFTER everything so it covers the inner area
 
## Step 6: SVG Assembly
 
```python
svg_lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}">',
    f'  <rect width="{SVG_W}" height="{SVG_H}" fill="{bg_hex}"/>',
]
for shape in shapes:
    svg_lines.append(f'  <path d="{shape["path"]}" fill="{shape["color"]}"/>')
svg_lines.append('</svg>')
```
 
## Handling Subtle Color Differences
 
When two regions have similar luminance but different hue/saturation (e.g., a gray band next to a dark background), K-means in RGB space will merge them. Use **HSV multispectral analysis**:
 
```python
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
h_ch, s_ch, v_ch = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
 
# Example: separate a gray band (low saturation) from red (high saturation)
# even though they have similar brightness
red_mask = ((h_ch < 12) | (h_ch > 168)) & (s_ch > 120) & (v_ch > 80)
gray_mask = (s_ch < 80) & (v_ch > 40) & (v_ch < 120) & spatial_constraint
```
 
**Saturation is the key discriminator** for colors that look similar in grayscale but are visually distinct to humans.
 
## Positioning Overlays
 
When adding shapes that weren't captured by quantization:
 
- **ALWAYS derive coordinates from the SVG render**, not the source image
- The extraction pipeline shifts positions due to contour simplification
- Render the SVG, detect boundaries in the render, create the overlay in render-pixel coordinates
- Verify by overlaying on the render BEFORE inserting
 
```python
# WRONG: extract from source, insert into SVG (coordinate mismatch)
# RIGHT: render SVG → detect gap in render → create shape in render coords → insert
svg_render = cv2.imread('rendered_svg.png')
# ... find boundaries in svg_render ...
# ... shapes are already in SVG pixel coordinates
```
 
## Verification Protocol
 
**After EVERY change, render and visually compare side-by-side before claiming success.** This is non-negotiable.
 
```python
# Render SVG
subprocess.run(['rsvg-convert', '-w', '1400', '-h', '940', 'output.svg', '-o', 'output.png'])
 
# Create side-by-side comparison
orig_crop = orig.crop((region))
svg_crop = svg.crop((region))
comparison = Image.new('RGB', (w1 + w2 + gap, h), bg)
comparison.paste(orig_crop, (0, 0))
comparison.paste(svg_crop, (w1 + gap, 0))
comparison.save('comparison.png')
 
# LOOK AT comparison.png BEFORE proceeding
```
 
## Anti-Patterns (What NOT to Do)
 
1. **Never hand-draw shapes** from your visual interpretation of the image. Your spatial reasoning about colors, positions, and shapes is unreliable. Use CV extraction.
 
2. **Never claim a fix works without rendering and comparing.** "Should now be filled" is not verification — a rendered comparison is.
 
3. **Never use geometric primitives (circles, rectangles) to approximate extracted contours.** The data has the actual shape; use it.
 
4. **Never extract coordinates from the source image and insert into the SVG** without verifying alignment. The contour extraction pipeline shifts positions.
 
5. **Never boost saturation globally.** This pushes colors away from the original. If colors need correction, do targeted per-color adjustments based on measured ΔE.
 
6. **Never aggressively merge near-background colors.** Subtle features live in these clusters. Only merge colors that are <10 RGB distance from background AND heavily touch image edges.
 
7. **Don't use bezier smoothing unless specifically requested.** Simple L (line-to) polygons produce smaller SVGs. Bezier C commands triple the coordinate count per segment.

8. **Don't use a dilation kernel larger than 3×3.** 5×5 was tested and causes blotchy artifacts in fine-detail areas like hair and foliage.
 
## File Size Guidelines
 
- Simple polygons (`M ... L ... L ... Z`): ~2 bytes per coordinate
- Bezier curves (`C c1x,c1y c2x,c2y x,y`): ~6 bytes per coordinate  
- Target: 500-1000 paths for a complex image, 400-900KB SVG
- Use `approxPolyDP` with epsilon ~0.002 * arc_length for good quality/size tradeoff
 
## Dependencies
 
```bash
pip install opencv-python-headless scikit-image scipy --break-system-packages
apt-get install -y librsvg2-bin  # for rsvg-convert
```

**Cross-skill dependency**: [seeing-images](/mnt/skills/user/seeing-images/SKILL.md) — the `edges()` function is used in Step 3b for structural edge detection.
