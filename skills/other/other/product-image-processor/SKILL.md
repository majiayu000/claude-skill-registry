---
name: product-image-processor
description: Download, resize, and remove backgrounds from product images at scale
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - WebFetch
  - AskUserQuestion
  - mcp__google__sheets_values_get
  - mcp__google__sheets_spreadsheet_get
---

# /product-image-processor — Product Image Processor

Download product images from a Google Sheet, normalize sizing, and remove backgrounds. Saves output at each processing stage.

Works with the **master Google Sheet** — the 33-column schema defined in `../../schema/product-schema.md`. Image URLs are in column AC, product names in column C. Read `../../schema/sheet-conventions.md` for CRUD patterns with MCP tools.

## Step 1: Get Input

If no arguments provided, ask the user:
1. **Spreadsheet ID** — the Google Sheets ID (from the URL: `docs.google.com/spreadsheets/d/{ID}/...`). This is typically the same master sheet used by Norma Jean.
2. **Image URL column** — which column contains image URLs (default: `AC` in the master schema, or the user can specify)
3. **Name column** (optional) — which column has product names for file naming (default: `C` in the master schema). If not provided, derive names from the image URL/filename.
4. **Output location** — where to save the images. Suggest `~/Documents/Work-Docs/product-images-YYYY-MM-DD/` as default but let the user pick any path.
5. **Header row** — whether row 1 is a header (default: yes, row 2 in master schema)

## Step 2: Read URLs from Google Sheet

Use `mcp__google__sheets_spreadsheet_get` to inspect the sheet, then `mcp__google__sheets_values_get` to read the image URL column and optional name column.

Build a list of `{ index, url, name }` entries. Skip empty rows.

## Step 3: Create Output Folders

Create the output directory at the user's chosen path with 3 subfolders:

```
<output-path>/
├── originals/     # Raw downloads
├── resized/       # Normalized sizing
└── nobg/          # Background removed
```

If the folder already exists, append a suffix: `-2`, `-3`, etc.

## Step 4: Download Images

Download each image using `curl` in Bash:

```bash
curl -L -o "<output-path>" "<url>"
```

**IMPORTANT:** Use `curl`, NOT WebFetch. WebFetch processes content through an AI model which corrupts binary image data.

Name files as: `001-product-name.png`, `002-product-name.png`, etc.
- Slugify the product name: lowercase, replace spaces/special chars with hyphens, strip consecutive hyphens
- If no name column, extract a name from the URL filename (strip extension and query params)
- If the URL gives no usable name, use `001-image.png`, `002-image.png`, etc.

If the downloaded file is not a PNG (check extension or content type), convert it to PNG during the resize step.

## Step 5: Resize Images

Run a Python script to resize all images in `originals/` → `resized/`:

```python
from PIL import Image
import os, sys

input_dir = sys.argv[1]   # originals/
output_dir = sys.argv[2]  # resized/
max_edge = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

for fname in sorted(os.listdir(input_dir)):
    if not fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff')):
        continue
    try:
        img = Image.open(os.path.join(input_dir, fname))
        img = img.convert("RGBA")
        w, h = img.size
        longest = max(w, h)
        if longest > max_edge:
            scale = max_edge / longest
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        out_name = os.path.splitext(fname)[0] + ".png"
        img.save(os.path.join(output_dir, out_name), "PNG")
        print(f"OK: {fname} → {out_name} ({img.size[0]}x{img.size[1]})")
    except Exception as e:
        print(f"FAIL: {fname} — {e}")
```

Rules:
- Max **2000px** on the longest edge (configurable if user requests)
- Preserve aspect ratio
- Do NOT upscale — if already smaller than max, keep original dimensions
- Convert everything to PNG (RGBA mode for transparency support)

## Step 6: Remove Backgrounds

Check if `rembg` is installed. If not, install it:

```bash
pip3 install rembg onnxruntime
```

Then run background removal on all resized images → `nobg/`:

```python
from rembg import remove
from PIL import Image
import os, sys, io

input_dir = sys.argv[1]   # resized/
output_dir = sys.argv[2]  # nobg/

for fname in sorted(os.listdir(input_dir)):
    if not fname.lower().endswith('.png'):
        continue
    try:
        input_path = os.path.join(input_dir, fname)
        with open(input_path, 'rb') as f:
            input_data = f.read()
        output_data = remove(input_data)
        img = Image.open(io.BytesIO(output_data))
        img.save(os.path.join(output_dir, fname), "PNG")
        print(f"OK: {fname}")
    except Exception as e:
        print(f"FAIL: {fname} — {e}")
```

**Note:** The first run of rembg downloads the u2net model (~170MB). Warn the user this may take a minute.

## Step 7: Report Results

After processing, print a summary:

```
## Product Image Processing Complete

📁 Output: ~/Documents/Work-Docs/product-images-YYYY-MM-DD/

| Stage        | Success | Failed |
|-------------|---------|--------|
| Downloaded  | 12      | 1      |
| Resized     | 12      | 0      |
| BG Removed  | 12      | 0      |

### Failures
- 003-chair-arm.png: Download failed (404 Not Found)
```

Include the full path to the output folder so the user can open it.

## Error Handling

- **Download failures:** Log and continue. Don't block the pipeline for one bad URL.
- **Resize failures:** Log and continue. Skip that image in the bg-removal step.
- **rembg failures:** Log and continue. Some images (vectors, icons) may not process well.
- **Sheet read errors:** Stop and report. Ask the user to verify the spreadsheet ID and column.

## Notes

- Process images sequentially (not parallel) to avoid overwhelming the network or CPU
- For large batches (50+ images), print progress every 10 images
- The rembg model download only happens once — subsequent runs reuse the cached model
