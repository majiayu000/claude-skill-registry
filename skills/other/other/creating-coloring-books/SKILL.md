---
name: creating-coloring-books
description: >
  End-to-end coloring book creation, packaging, pricing, and multi-storefront
  publishing pipeline. Converts a topic/trend into print-ready coloring pages,
  bundles them for sale, and posts to Etsy, Creative Market, Gumroad, Amazon KDP,
  and more. Use when: creating coloring books, coloring pages, coloring bundles,
  converting images to line art for print, packaging digital downloads, listing
  on storefronts, or when the user provides a topic and wants sellable coloring content.
  Triggers: "coloring book", "coloring pages", "coloring bundle", "line art",
  "convert to coloring", "printable coloring", "list on etsy", "sell coloring pages",
  any topic + "coloring".
---

# Creating Coloring Books

## Overview

**Input:** A topic or trend (e.g. "kpop demon hunters") + optional page count (default 10).

**Output:**

1. Workflow log in `~/d/33GOD/{YYYY-MM-DD}/DigiPopStudios/{topic-slug}/run-{RUNID}/`
2. Quality-checked coloring book pages uploaded to media.delo.sh as PNG+SVG pairs
3. Packaged bundles (PDF, ZIP) ready for sale
4. Listings posted to multiple storefronts with optimized titles, descriptions, and pricing

## Workflow — 9 Phases

Follow each phase and step **exactly**. Do not substitute, skip, or reorder.

---

### Phase 1: Research — Google Images Browse

1. Open the **openclaw browser** (`profile=openclaw`).
2. Navigate to Google Images: `https://www.google.com/search?tbm=isch&q={url-encoded topic}`.
3. Take a snapshot of the results page.
4. Identify 15–20 candidate thumbnails that have strong line-art potential:
   - Prefer: illustrations, anime/manga, vector art, bold outlines, distinct shapes.
   - Avoid: photographs, photorealistic 3D renders, blurry/low-contrast, text-heavy.
5. Log each candidate: thumbnail position, brief description, why selected.

**Hard rules:**

- Source is Google Images only. Do NOT use Pixabay, Vecteezy, or any stock API.
- Do NOT attempt to download images via curl/requests. Screenshots only (Phase 2).

---

### Phase 2: Source Capture — Screenshot & Crop

For each candidate from Phase 1:

1. Click on the thumbnail in Google Images to open the **preview panel** on the right.
2. **Screenshot the full browser window** with the preview panel visible.
3. Save screenshots to `{bundle}/research/sources/src-{NN}.png`.

**CRITICAL — Auto-crop the preview panel before conversion:**

The screenshot includes the entire Google Images page (thumbnail grid, search bar, UI chrome).
You MUST crop to extract only the preview image before feeding to Phase 3.

```python
# Crop the preview panel from each screenshot
import cv2, numpy as np
from pathlib import Path

src_dir = Path('{bundle}/research/sources')
out_dir = src_dir / 'crops'
out_dir.mkdir(exist_ok=True)

for f in sorted(src_dir.glob('src-*.png')):
    img = cv2.imread(str(f))
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    mask = np.zeros_like(th)
    mask[:, int(w * 0.45):] = th[:, int(w * 0.45):]
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    best = None
    for i in range(1, num):
        x, y, ww, hh, area = stats[i]
        if area < 8000: continue
        score = float(area)
        if hh > ww: score *= 1.3
        if x > w * 0.55: score *= 1.2
        if best is None or score > best[0]:
            best = (score, (x, y, ww, hh))
    if best:
        x, y, ww, hh = best[1]
        pad = int(min(ww, hh) * 0.12)
        crop = img[max(0,y-pad):min(h,y+hh+pad), max(0,x-pad):min(w,x+ww+pad)]
    else:
        crop = img[int(h*0.12):int(h*0.82), int(w*0.62):int(w*0.98)]
    crop = cv2.resize(crop, (1024, 1536), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(str(out_dir / f.name.replace('src-', 'crop-')), crop)
```

The **cropped images** in `sources/crops/` are what you feed to Phase 3, NOT the raw screenshots.

**The screenshot IS the source asset.** Do not attempt to download the original file.

---

### Phase 3: Convert to Coloring Pages — fal.ai Qwen Image Edit 2511

Use the bundled script on the **cropped** sources:

```bash
source ~/.config/zshyzsh/secrets.zsh
~/.agents/skills/creating-coloring-books/.venv/bin/python \
  ~/.agents/skills/creating-coloring-books/scripts/coloring-convert \
  {bundle}/research/sources/crops/ \
  --output-dir {bundle}/coloring/ \
  --prompt "Convert this image into a clean black and white coloring book page. Keep only the main character(s) and scene; remove UI chrome and website elements. Thick crisp outlines, white background, no grayscale, no text, no logos."
```

The script:

- Uploads each cropped source to fal.ai storage.
- Calls `fal-ai/qwen-image-edit-2511` with the coloring conversion prompt.
- Downloads the resulting coloring page PNG.
- Proceeds to Phase 4 automatically (vectorization).
- Writes per-page metadata JSON and a manifest.

---

### Phase 4: Vectorize — fal.ai Recraft Vectorize

Handled automatically by `scripts/coloring-convert` after Phase 3.

Output pairs:

- `{bundle}/coloring/page-{NN}-coloring.png`
- `{bundle}/coloring/page-{NN}-coloring.svg`

---

### Phase 5: QA — Independent Agent Inspection

Spawn a sub-agent for QA (**use model=opus for visual accuracy**):

```
sessions_spawn(
  task="QA coloring book pages. Inspect in batches of 5 to avoid truncation.
    For each PNG in {bundle}/coloring/page-*-coloring.png:
    1. Analyze the image visually.
    2. Rate 1-5 on: line_quality, complexity_balance, colorable_regions, print_artifacts, age_appropriateness, subject_recognizability.
    3. PASS if average >= 3.5 and no category below 2. Otherwise FAIL with reason.
    4. Write results to {bundle}/qa/qa-report.json.
    5. Write summary to {bundle}/qa/qa-summary.md with ranking and Top 10.
    If a page FAILS, note which source it came from so it can be substituted.",
  mode="run",
  model="opus"
)
```

For any FAILED pages:

1. Return to Phase 1 and find a replacement source.
2. Re-run Phases 2–4 for the replacement.
3. Re-run QA on the replacement only.
4. Repeat until 10 pages pass or the candidate pool is exhausted.

---

### Phase 6: Upload to Piwigo (Asset Gallery)

Upload all passing pages (PNG + vector pairs) to `media.delo.sh` album 1.

**Auth:** username=`delorenj`, password=`Ittr5eesol`

```python
import requests
BASE = "https://media.delo.sh"
s = requests.Session()
s.headers.update({"User-Agent": "Dumply/1.0", "Referer": f"{BASE}/"})
s.post(f"{BASE}/ws.php?format=json", data={
    "method": "pwg.session.login", "username": "delorenj", "password": "Ittr5eesol"
})
# Upload each file
for file_path in files:
    with open(file_path, "rb") as f:
        s.post(f"{BASE}/ws.php?format=json",
            data={"method": "pwg.images.addSimple", "category": "1", "name": display_name},
            files={"image": (file_path.name, f, mime_type)})
```

**SVG upload caveat:** Piwigo rejects SVG. Render SVG → JPG via ImageMagick:

```bash
magick -density 300 page.svg -background white -alpha remove -alpha off -quality 95 page-vector.jpg
```

**Naming:** `{topic-slug}-page-{NN}-raster` and `{topic-slug}-page-{NN}-vector-jpg`

---

### Phase 7: Packaging & Bundling

Create sale-ready bundles in `{bundle}/packages/`:

#### 7a. Digital Download Bundle (ZIP)

```
{topic-slug}-coloring-bundle/
├── README.txt              # License, instructions, credits
├── pages/
│   ├── page-01.png         # High-res coloring pages (300 DPI)
│   ├── page-01.svg         # Vector versions
│   ├── page-02.png
│   ├── page-02.svg
│   └── ...
└── {topic-slug}-complete.pdf  # All pages in one printable PDF
```

#### 7b. Printable PDF Bundle

Generate a print-ready PDF (8.5×11" letter, portrait):

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

c = canvas.Canvas(output_pdf, pagesize=letter)
w, h = letter  # 612 x 792 points

# Cover page
c.setFont("Helvetica-Bold", 36)
c.drawCentredString(w/2, h*0.6, title)
c.setFont("Helvetica", 18)
c.drawCentredString(w/2, h*0.5, f"{page_count} Coloring Pages")
c.drawCentredString(w/2, h*0.35, "DigiPop Studios")
c.showPage()

# Coloring pages (one per page, centered with margins)
for png in sorted_pages:
    c.drawImage(png, 0.5*inch, 0.5*inch, w - 1*inch, h - 1*inch,
                preserveAspectRatio=True, anchor='c')
    c.showPage()

c.save()
```

#### 7c. Amazon KDP Interior (if 24+ pages)

KDP requires minimum 24 interior pages. For a 10-page bundle:

- Add a title page, copyright page, "how to use" page, and back-of-page blanks
- Total: title + copyright + howto + (10 × 2 sides) + closing = 24 pages minimum
- Format: PDF, 8.5×11" (or 8.25×11.25" with bleed), 300 DPI
- Generate cover separately: front + spine + back as a single PDF spread

#### 7d. Preview/Mockup Images

Generate 3-5 preview images for storefront listings:

1. **Hero image**: 2-3 best pages fanned out on a wooden table mockup
2. **Grid preview**: 2×5 grid showing all 10 pages as thumbnails
3. **Single page zoom**: Close-up of the highest-rated page
4. **Device mockup**: Pages shown on a tablet screen

Use the `fal-text-to-image` skill or browser-based mockup generators.

#### 7e. ZIP the bundle

```bash
cd {bundle}/packages
zip -r {topic-slug}-coloring-bundle.zip {topic-slug}-coloring-bundle/
```

---

### Phase 8: Pricing Strategy

#### Base pricing tiers (10-page digital bundle)

| Storefront               | Price                           | Rationale                                                          |
| ------------------------ | ------------------------------- | ------------------------------------------------------------------ |
| **Etsy**                 | $3.99–$5.99                     | Sweet spot for digital coloring bundles; under $5 impulse buy zone |
| **Creative Market**      | $7.00–$12.00                    | Premium positioning, designer audience expects higher quality      |
| **Gumroad**              | $4.99 (pay-what-you-want floor) | PWYW boosts conversions; avg payment typically 1.5x floor          |
| **Amazon KDP** (print)   | $6.99–$8.99                     | Physical book, KDP takes ~60% for expanded distribution            |
| **Amazon KDP** (digital) | $2.99                           | Low price, 70% royalty tier                                        |
| **Payhip**               | $4.99                           | Zero transaction fees on paid plan                                 |
| **Ko-fi Shop**           | $3.99                           | Creator-friendly audience, tips common                             |

#### Pricing rules

- **10-page bundles**: $3.99–$5.99 (digital), $6.99–$8.99 (print)
- **20-page bundles**: $5.99–$8.99 (digital), $9.99–$12.99 (print)
- **50+ page mega bundles**: $9.99–$14.99 (digital)
- **Individual pages**: $0.99–$1.49 each (upsell to bundle)
- **Launch discount**: 20-30% off first week (creates urgency)
- **Bundle discount**: Always price bundle < sum of individual pages

#### Fee structure to track

| Platform        | Listing Fee   | Transaction Fee              | Payment Processing |
| --------------- | ------------- | ---------------------------- | ------------------ |
| Etsy            | $0.20/listing | 6.5%                         | 3% + $0.25         |
| Creative Market | Free          | 50% commission (standard)    | Included           |
| Gumroad         | Free          | 10%                          | Included           |
| Amazon KDP      | Free          | 30-65% (varies)              | Included           |
| Payhip          | Free          | 5% (free plan) / 0% ($99/yr) | Included           |
| Ko-fi           | Free          | 0% (Gold: $6/mo)             | PayPal/Stripe fees |

---

### Phase 9: Storefront Publishing

Post listings to each storefront. Prioritize by traffic and margin.

#### 9a. Etsy (highest traffic for coloring pages)

Use the openclaw browser (`profile=openclaw`) to:

1. Navigate to `https://www.etsy.com/your/shops/me/tools/listings/create`
2. Fill listing form:
   - **Title**: `{Topic} Coloring Pages Bundle | {N} Printable Pages | Digital Download | Kids & Adults`
   - **Description**: (see template below)
   - **Category**: Art & Collectibles > Drawing & Illustration > Digital
   - **Type**: Digital download
   - **Price**: Per pricing strategy above
   - **Tags** (13 max): `coloring pages, coloring book, printable, digital download, {topic keywords}, kids coloring, adult coloring, line art, instant download`
   - **Files**: Upload ZIP bundle
   - **Images**: Upload preview mockups (first image = hero)
3. Publish listing

#### 9b. Creative Market

1. Navigate to `https://creativemarket.com/sell`
2. Create product:
   - **Title**: `{Topic} Coloring Book Bundle – {N} Printable Pages`
   - **Category**: Graphics > Illustrations
   - **Price**: Premium tier from pricing strategy
   - **Files**: Upload ZIP
   - **Preview images**: Upload mockups
3. Submit for review

#### 9c. Gumroad

1. Navigate to `https://app.gumroad.com/products/new`
2. Create product:
   - **Name**: `{Topic} Coloring Pages – {N} Page Bundle`
   - **Price**: Set minimum (PWYW)
   - **Files**: Upload ZIP + PDF
   - **Cover**: Upload hero mockup
   - **Description**: From template
3. Publish

#### 9d. Amazon KDP (if 24+ pages available)

1. Navigate to `https://kdp.amazon.com/en_US/bookshelf`
2. Create new paperback:
   - **Title**: `{Topic} Coloring Book: {N} Pages for Kids and Adults`
   - **Interior**: Upload KDP-formatted PDF
   - **Cover**: Upload KDP cover PDF
   - **Trim size**: 8.5×11"
   - **Paper**: White, no bleed
   - **Price**: Per pricing strategy
3. Also create Kindle ebook version with the digital PDF

#### 9e. Payhip (zero fees)

1. Navigate to `https://payhip.com/dashboard/products/new`
2. Upload ZIP + fill product details
3. Publish

#### 9f. Ko-fi Shop

1. Navigate to `https://ko-fi.com/manage/shop`
2. Add shop item with ZIP download
3. Publish

#### Listing Description Template

```
✨ {TOPIC} Coloring Pages Bundle ✨

{N} beautiful, hand-curated coloring pages featuring {topic description}.
Perfect for kids, teens, and adults who love {related interests}!

📦 WHAT'S INCLUDED:
• {N} high-resolution coloring pages (PNG, 300 DPI)
• {N} vector versions (SVG) for crisp printing at any size
• 1 printable PDF with all pages (8.5×11" letter size)
• Instant digital download

🖍️ FEATURES:
• Clean, bold outlines perfect for coloring
• Mix of simple and detailed designs
• Suitable for all ages (5+)
• Print as many copies as you like for personal use

🖨️ HOW TO USE:
1. Download the ZIP file after purchase
2. Print pages on standard letter paper (8.5×11")
3. Use crayons, colored pencils, markers, or gel pens
4. Frame your favorites!

📋 LICENSE:
• Personal use and classroom use permitted
• Not for resale or redistribution
• Commercial use available — contact us

💝 From DigiPop Studios with love!
```

---

## Observability Log Structure

All run artifacts go in the daily ephemeral doc vault:

```
~/d/33GOD/{YYYY-MM-DD}/{topic-slug}/run-{YYYYMMDD-HHMMSS}/
├── README.md
├── events.jsonl
├── asset-ledger.csv
├── phases/
│   ├── phase-1-research.md
│   ├── phase-2-capture.md
│   ├── phase-3-coloring.md
│   ├── phase-4-vectorize.md
│   ├── phase-5-qa.md
│   ├── phase-6-upload.md
│   ├── phase-7-packaging.md
│   ├── phase-8-pricing.md
│   └── phase-9-publishing.md
├── upload-report.json
└── publishing-report.json     # Links to all storefront listings
```

---

## Prerequisites

- `FAL_KEY` environment variable — sourced from `~/.config/zshyzsh/secrets.zsh`

  ```bash
  source ~/.config/zshyzsh/secrets.zsh
  ```

- Python venv with deps:

  ```bash
  cd ~/.agents/skills/creating-coloring-books && uv venv .venv && uv pip install fal-client requests reportlab
  ```

- Run the conversion script with the skill's venv Python:

  ```bash
  source ~/.config/zshyzsh/secrets.zsh
  ~/.agents/skills/creating-coloring-books/.venv/bin/python \
    ~/.agents/skills/creating-coloring-books/scripts/coloring-convert ...
  ```

- OpenClaw browser available (`profile=openclaw`)
- ImageMagick (`magick`) for SVG→JPG fallback
- Piwigo credentials: `delorenj` / `Ittr5eesol`
- Storefront accounts (Etsy, Creative Market, Gumroad, etc.) — logged in via openclaw browser

---

## Key Constraints

- **No Pixabay.** No stock site APIs. Source is Google Images search only.
- **No image downloads.** Capture sources via browser screenshot only.
- **Crop preview panels** before conversion. Never feed raw full-page screenshots to Qwen.
- **Follow phases in order.** Do not skip or combine.
- **QA is mandatory.** Failed pages must be replaced, not shipped.
- **Every asset tracked.** If it was used or created, it appears in the log.
- **Pricing is per strategy.** Don't underprice. Don't overprice. Follow the tiers.
- **All storefronts get listings.** Cast a wide net. Revenue compounds across channels.
