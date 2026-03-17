---
name: extract-images
description: Extract and catalog illustrations from historical books using AI vision. Generates rich metadata (subjects, figures, symbols, style, technique) and museum-style descriptions. Use when asked to extract images, run image detection, or process book illustrations.
---

# Image Extraction Skill

Extract illustrations from historical book scans using Gemini vision AI. Creates a curated gallery with rich metadata for each image.

## Invocation

```
/extract-images                      # Show extraction status across library
/extract-images BOOK_ID              # Extract images from specific book
/extract-images --all                # Extract from all books missing images
/extract-images --priority           # Extract from high-priority books first
```

## What Gets Extracted

For each illustration found:
- **Bounding box** - Precise crop coordinates
- **Type classification** - emblem, woodcut, engraving, portrait, frontispiece, musical_score, diagram, symbol, decorative, map
- **Gallery quality score** - 0.0-1.0 rating for curation
- **Museum description** - 2-3 sentence scholarly label
- **Structured metadata**:
  - `subjects` - Topics (alchemy, transformation, mythology)
  - `figures` - People/beings depicted (Mercury, serpent, old man)
  - `symbols` - Symbolic elements (ouroboros, athanor, philosophical egg)
  - `style` - Art historical style (Northern European Renaissance)
  - `technique` - Production method (woodcut, engraving)

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /api/extract-images` | Extract images from pages |
| `GET /api/gallery` | List extracted images |
| `GET /api/gallery/image/[id]` | Get single image with metadata |
| `PATCH /api/gallery/image/[id]` | Update metadata/quality |

## Check Extraction Status

```bash
# Get books with extraction counts
curl -s "https://sourcelibrary.org/api/books" | jq '[.[] | {
  id,
  title: .title[0:40],
  pages: .pages_count,
  images: (.detected_images_count // 0)
}] | sort_by(-.pages)'

# Find books needing extraction (no detected_images)
curl -s "https://sourcelibrary.org/api/books" | jq '[.[] |
  select((.detected_images_count // 0) == 0) |
  {id, title: .title[0:40], pages: .pages_count}
] | sort_by(-.pages)'
```

## Extract Images from a Book

### Smart Extraction (Recommended)

Uses OCR `<image-desc>` tags to find pages with images, ranks them with AI, and only extracts the best 15-20:

```bash
# Extract top 20 images from a book
node scripts/smart-extract.mjs BOOK_ID --limit=20

# Extract top 15 images
node scripts/smart-extract.mjs BOOK_ID --limit=15
```

**How it works:**
1. Finds pages with `<image-desc>` tags in OCR (from previous OCR pass)
2. Uses AI to rank descriptions and pick the most interesting
3. Only extracts those specific pages
4. ~30 seconds for 20 images instead of scanning all pages

### Full Extraction (All Pages)

For comprehensive extraction of every page (slow, use sparingly):

```bash
node scripts/evaluate-extraction.mjs BOOK_ID --clear
```

### Via API (Individual Pages)

```bash
curl -s -X POST "https://sourcelibrary.org/api/extract-images" \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": "BOOK_ID",
    "pageIds": ["PAGE_ID_1", "PAGE_ID_2"],
    "overwrite": false
  }'
```

### Books with OCR Image Descriptions

Check which books have `<image-desc>` tags (best for smart extraction):

```bash
# Find books with image descriptions in OCR
node -e "
const { MongoClient } = require('mongodb');
require('dotenv').config({ path: '.env.local' });
// ... aggregation to find books with <image-desc> tags
"
```

## Output Quality

### Gallery Quality Scoring (0.0-1.0)

| Score | Description | Examples |
|-------|-------------|----------|
| 0.9-1.0 | Exceptional | Striking emblems, allegorical scenes with figures |
| 0.8-0.9 | High | Images featuring people, well-composed scenes |
| 0.6-0.8 | Good | Illustrations without people, interesting diagrams |
| 0.4-0.6 | Moderate | Musical scores, simple diagrams |
| 0.2-0.4 | Low | Page ornaments, generic borders |
| 0.0-0.2 | Minimal | Marbled papers, blank frames |

**Key Rule**: Images with people/figures always score 0.8+

### Image Types

| Type | Description |
|------|-------------|
| `emblem` | Symbolic/allegorical with motto |
| `woodcut` | Bold relief print lines |
| `engraving` | Fine detailed lines, crosshatching |
| `portrait` | Depiction of a person |
| `frontispiece` | Decorative title page |
| `musical_score` | Sheet music, notation |
| `diagram` | Technical/scientific illustration |
| `symbol` | Alchemical, astrological symbols |
| `decorative` | Ornaments, borders, initials |
| `map` | Geographic representation |

## Viewing Results

### Gallery Page
```
https://sourcelibrary.org/gallery?bookId=BOOK_ID
```

### Book Guide Page (high-quality images only)
```
https://sourcelibrary.org/book/BOOK_ID/guide
```

### Individual Image Detail
```
https://sourcelibrary.org/gallery/image/PAGE_ID:INDEX
```

## Cost Estimation

Using Gemini 2.5 Flash:

| Metric | Cost |
|--------|------|
| Per page | ~$0.0004 |
| Per high-quality image | ~$0.0012 |
| 100-page book | ~$0.04 |
| 500-page book | ~$0.20 |

## Monitoring Extraction

```bash
# Check extraction results for a book
curl -s "https://sourcelibrary.org/api/gallery?bookId=BOOK_ID" | jq '{
  total: .total,
  high_quality: [.images[] | select(.galleryQuality >= 0.75)] | length,
  types: [.images[].type] | group_by(.) | map({type: .[0], count: length})
}'

# Sample image metadata
curl -s "https://sourcelibrary.org/api/gallery/image/PAGE_ID:0" | jq '{
  type,
  galleryQuality,
  museumDescription,
  metadata
}'
```

## Troubleshooting

### Rate Limiting
The evaluation script has built-in 500ms delays. For higher throughput:
- Use multiple API keys (rotate on 429)
- Reduce delay for paid tiers

### Missing Images
If extraction finds fewer images than expected:
- Check page image quality (blurry scans)
- Verify pages have `cropped_photo` or `photo_original` URLs
- Re-run with `--clear` to retry

### Wrong Classifications
If images are misclassified:
- Edit via gallery UI at `/gallery/image/PAGE_ID:INDEX`
- Use PATCH endpoint to update type/metadata
