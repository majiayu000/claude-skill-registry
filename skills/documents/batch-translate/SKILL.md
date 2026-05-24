---
name: batch-translate
description: Batch process books through the complete pipeline - generate cropped images for split pages, OCR all pages, then translate with context. Use when asked to process, OCR, translate, or batch process one or more books.
---

# Batch Book Translation Workflow

Process books through the complete pipeline: Crop → OCR → Translate

## Roadmap Reference

See `.claude/ROADMAP.md` for the translation priority list.

**Priority 1 = UNTRANSLATED** - These are highest priority for processing:
- Kircher encyclopedias (Oedipus, Musurgia, Ars Magna Lucis)
- Fludd: Utriusque Cosmi Historia
- Theatrum Chemicum, Musaeum Hermeticum
- Cardano: De Subtilitate
- Della Porta: Magia Naturalis
- Lomazzo, Poliziano, Landino

```bash
# Get roadmap with priorities
curl -s "https://sourcelibrary.org/api/books/roadmap" | jq '.books[] | select(.priority == 1) | {title, notes}'
```

Roadmap source: `src/app/api/books/roadmap/route.ts`

## Overview

This workflow handles the full processing pipeline for historical book scans:
1. **Generate Cropped Images** - For split two-page spreads, extract individual pages
2. **OCR** - Extract text from page images using Gemini vision
3. **Translate** - Translate OCR'd text with prior page context for continuity

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/books` | List all books |
| `GET /api/books/BOOK_ID` | Get book with all pages |
| `POST /api/jobs` | Create a processing job |
| `POST /api/jobs/JOB_ID/process` | Process next chunk of a job |
| `POST /api/process/batch-ocr` | OCR up to 5 pages directly |
| `POST /api/process/batch-translate` | Translate up to 10 pages directly |

## Batch Processing Options

### Option 1: Vercel Cron (Recommended for Bulk)

Two serverless functions automate the entire batch OCR pipeline:

| Endpoint | Purpose | Schedule |
|----------|---------|----------|
| `POST /api/cron/submit-ocr` | Creates batch jobs for all pages needing OCR | Daily midnight |
| `POST /api/cron/batch-processor` | Downloads results, saves to DB | Every 6 hours |

```bash
# Manual trigger - submit all pending OCR
curl -X POST https://sourcelibrary.org/api/cron/submit-ocr

# Manual trigger - process completed batches
curl -X POST https://sourcelibrary.org/api/cron/batch-processor
```

**Timeline:**
- T+0h: Submit batch jobs
- T+2-24h: Gemini processing
- T+24h: Batch processor saves results (runs every 6h)

**Critical:** Results expire after 48h - batch-processor must run at least once every 48 hours.

See `docs/BATCH-OCR-CRON-SETUP.md` for full documentation.

### Option 2: Job System (for targeted processing)

All batch jobs use **Gemini Batch API** for 50% cost savings.

| Job Type | API | Model | Cost |
|----------|-----|-------|------|
| Single page | Realtime | gemini-3-flash-preview | Full price |
| batch_ocr | Batch API | gemini-3-flash-preview | **50% off** |
| batch_translate | Batch API | gemini-3-flash-preview | **50% off** |

**IMPORTANT: Always use `gemini-3-flash-preview` for all OCR and translation tasks. Do NOT use `gemini-2.5-flash`.**

See `docs/BATCH-PROCESSING.md` for full documentation.

### How Batch Jobs Work

1. **Create job** → `use_batch_api: true` automatically set
2. **Call `/process` repeatedly** → Each call prepares 20 pages
3. **When all prepared** → Submits to Gemini Batch API
4. **Call `/process` again** → Polls for results (ready in 2-24 hours)
5. **When done** → Results saved, job complete

## OCR Output Format

OCR uses **Markdown output** with semantic tags:

### Markdown Formatting
- `# ## ###` for headings (bigger text = bigger heading)
- `**bold**`, `*italic*` for emphasis
- `->centered text<-` for centered lines (NOT for headings)
- `> blockquotes` for quotes/prayers
- `---` for dividers
- Tables only for actual tabular data

### Metadata Tags (hidden from readers)
| Tag | Purpose |
|-----|---------|
| `<lang>X</lang>` | Detected language |
| `<page-num>N</page-num>` | Page/folio number |
| `<header>X</header>` | Running headers |
| `<sig>X</sig>` | Printer's marks (A2, B1) |
| `<meta>X</meta>` | Hidden metadata |
| `<warning>X</warning>` | Quality issues |
| `<vocab>X</vocab>` | Key terms for indexing |

### Inline Annotations (visible to readers)
| Tag | Purpose |
|-----|---------|
| `<margin>X</margin>` | Marginal notes (before paragraph) |
| `<gloss>X</gloss>` | Interlinear annotations |
| `<insert>X</insert>` | Boxed text, additions |
| `<unclear>X</unclear>` | Illegible readings |
| `<note>X</note>` | Interpretive notes |
| `<term>X</term>` | Technical vocabulary |
| `<image-desc>X</image-desc>` | Describe illustrations |

### Critical OCR Rules
1. Preserve original spelling, capitalization, punctuation
2. Page numbers/headers/signatures go in metadata tags only
3. IGNORE partial text at edges (from facing page in spread)
4. Describe images/diagrams with `<image-desc>`, never tables
5. End with `<vocab>key terms, names, concepts</vocab>`

## Step 1: Analyze Book Status

First, check what work is needed for a book:

```bash
# Get book and analyze page status
curl -s "https://sourcelibrary.org/api/books/BOOK_ID" > /tmp/book.json

# Count pages by status (IMPORTANT: check length > 0, not just existence - empty strings are truthy!)
jq '{
  title: .title,
  total_pages: (.pages | length),
  split_pages: [.pages[] | select(.crop)] | length,
  needs_crop: [.pages[] | select(.crop) | select(.cropped_photo | not)] | length,
  has_ocr: [.pages[] | select((.ocr.data // "") | length > 0)] | length,
  needs_ocr: [.pages[] | select((.ocr.data // "") | length == 0)] | length,
  has_translation: [.pages[] | select((.translation.data // "") | length > 0)] | length,
  needs_translation: [.pages[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0)] | length
}' /tmp/book.json
```

### Detecting Bad OCR

Pages that were OCR'd before cropped images were generated have incorrect OCR (contains both pages of the spread). Detect these:

```bash
# Find pages with crop data + OCR but missing cropped_photo at OCR time
# These often contain "two-page" or "spread" in the OCR text
jq '[.pages[] | select(.crop) | select(.ocr.data) |
  select(.ocr.data | test("two-page|spread"; "i"))] | length' /tmp/book.json
```

## Step 2: Generate Cropped Images

For books with split two-page spreads, generate individual page images:

```bash
# Get page IDs needing crops
CROP_IDS=$(jq '[.pages[] | select(.crop) | select(.cropped_photo | not) | .id]' /tmp/book.json)

# Create crop job
curl -s -X POST "https://sourcelibrary.org/api/jobs" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"generate_cropped_images\",
    \"book_id\": \"BOOK_ID\",
    \"book_title\": \"BOOK_TITLE\",
    \"page_ids\": $CROP_IDS
  }"
```

Process the job:

```bash
# Trigger processing (40 pages per request, auto-continues)
curl -s -X POST "https://sourcelibrary.org/api/jobs/JOB_ID/process"
```

## Step 3: OCR Pages

### Option A: Using Job System (for large batches)

```bash
# Get page IDs needing OCR (check for empty strings, not just null)
OCR_IDS=$(jq '[.pages[] | select((.ocr.data // "") | length == 0) | .id]' /tmp/book.json)

# Create OCR job
curl -s -X POST "https://sourcelibrary.org/api/jobs" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"batch_ocr\",
    \"book_id\": \"BOOK_ID\",
    \"book_title\": \"BOOK_TITLE\",
    \"model\": \"gemini-3-flash-preview\",
    \"language\": \"Latin\",
    \"page_ids\": $OCR_IDS
  }"
```

### Option B: Using Batch API Directly (for small batches or overwrites)

```bash
# OCR with overwrite (for fixing bad OCR)
curl -s -X POST "https://sourcelibrary.org/api/process/batch-ocr" \
  -H "Content-Type: application/json" \
  -d '{
    "pages": [
      {"pageId": "PAGE_ID_1", "imageUrl": "", "pageNumber": 0},
      {"pageId": "PAGE_ID_2", "imageUrl": "", "pageNumber": 0}
    ],
    "language": "Latin",
    "model": "gemini-3-flash-preview",
    "overwrite": true
  }'
```

The batch-ocr API automatically uses `cropped_photo` when available.

## Step 4: Translate Pages

### Option A: Using Job System

```bash
# Get page IDs needing translation (must have OCR content, check for empty strings)
TRANS_IDS=$(jq '[.pages[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0) | .id]' /tmp/book.json)

# Create translation job
curl -s -X POST "https://sourcelibrary.org/api/jobs" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"batch_translate\",
    \"book_id\": \"BOOK_ID\",
    \"book_title\": \"BOOK_TITLE\",
    \"model\": \"gemini-3-flash-preview\",
    \"language\": \"Latin\",
    \"page_ids\": $TRANS_IDS
  }"
```

### Option B: Using Batch API with Context

For better continuity, translate with previous page context:

```bash
# Get pages sorted by page number with OCR text (check for empty strings)
PAGES=$(jq '[.pages | sort_by(.page_number) | .[] |
  select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0) |
  {pageId: .id, ocrText: .ocr.data, pageNumber: .page_number}]' /tmp/book.json)

# Translate with context (process in batches of 5-10)
curl -s -X POST "https://sourcelibrary.org/api/process/batch-translate" \
  -H "Content-Type: application/json" \
  -d "{
    \"pages\": $BATCH,
    \"model\": \"gemini-3-flash-preview\",
    \"sourceLanguage\": \"Latin\",
    \"targetLanguage\": \"English\",
    \"previousContext\": \"PREVIOUS_PAGE_TRANSLATION_TEXT\"
  }"
```

## Complete Book Processing Script

Process a single book through the full pipeline:

```bash
#!/bin/bash
BOOK_ID="YOUR_BOOK_ID"
MODEL="gemini-3-flash-preview"
BASE_URL="https://sourcelibrary.org"

# 1. Fetch book data
echo "Fetching book..."
BOOK=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
TITLE=$(echo "$BOOK" | jq -r '.title[0:40]')
echo "Processing: $TITLE"

# 2. Generate missing crops
NEEDS_CROP=$(echo "$BOOK" | jq '[.pages[] | select(.crop) | select(.cropped_photo | not)] | length')
if [ "$NEEDS_CROP" != "0" ]; then
  echo "Generating $NEEDS_CROP cropped images..."
  CROP_IDS=$(echo "$BOOK" | jq '[.pages[] | select(.crop) | select(.cropped_photo | not) | .id]')
  JOB=$(curl -s -X POST "$BASE_URL/api/jobs" -H "Content-Type: application/json" \
    -d "{\"type\":\"generate_cropped_images\",\"book_id\":\"$BOOK_ID\",\"page_ids\":$CROP_IDS}")
  JOB_ID=$(echo "$JOB" | jq -r '.job.id')

  while true; do
    RESULT=$(curl -s -X POST "$BASE_URL/api/jobs/$JOB_ID/process")
    [ "$(echo "$RESULT" | jq -r '.done')" = "true" ] && break
    sleep 2
  done
  echo "Crops complete!"
  BOOK=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
fi

# 3. OCR missing pages (check for empty strings, not just null)
NEEDS_OCR=$(echo "$BOOK" | jq '[.pages[] | select((.ocr.data // "") | length == 0)] | length')
if [ "$NEEDS_OCR" != "0" ]; then
  echo "OCRing $NEEDS_OCR pages..."
  OCR_IDS=$(echo "$BOOK" | jq '[.pages[] | select((.ocr.data // "") | length == 0) | .id]')

  TOTAL=$(echo "$OCR_IDS" | jq 'length')
  for ((i=0; i<TOTAL; i+=5)); do
    BATCH=$(echo "$OCR_IDS" | jq ".[$i:$((i+5))] | [.[] | {pageId: ., imageUrl: \"\", pageNumber: 0}]")
    curl -s -X POST "$BASE_URL/api/process/batch-ocr" -H "Content-Type: application/json" \
      -d "{\"pages\":$BATCH,\"model\":\"$MODEL\"}" > /dev/null
    echo -n "."
  done
  echo " OCR complete!"
  BOOK=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
fi

# 4. Translate with context (check for empty strings)
NEEDS_TRANS=$(echo "$BOOK" | jq '[.pages[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0)] | length')
if [ "$NEEDS_TRANS" != "0" ]; then
  echo "Translating $NEEDS_TRANS pages..."
  PAGES=$(echo "$BOOK" | jq '[.pages | sort_by(.page_number) | .[] |
    select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0) |
    {pageId: .id, ocrText: .ocr.data, pageNumber: .page_number}]')

  TOTAL=$(echo "$PAGES" | jq 'length')
  PREV_CONTEXT=""

  for ((i=0; i<TOTAL; i+=5)); do
    BATCH=$(echo "$PAGES" | jq ".[$i:$((i+5))]")

    if [ -n "$PREV_CONTEXT" ]; then
      RESP=$(curl -s -X POST "$BASE_URL/api/process/batch-translate" -H "Content-Type: application/json" \
        -d "{\"pages\":$BATCH,\"model\":\"$MODEL\",\"previousContext\":$(echo "$PREV_CONTEXT" | jq -Rs .)}")
    else
      RESP=$(curl -s -X POST "$BASE_URL/api/process/batch-translate" -H "Content-Type: application/json" \
        -d "{\"pages\":$BATCH,\"model\":\"$MODEL\"}")
    fi

    # Get last translation for context
    LAST_ID=$(echo "$BATCH" | jq -r '.[-1].pageId')
    PREV_CONTEXT=$(echo "$RESP" | jq -r ".translations[\"$LAST_ID\"] // \"\"" | head -c 1500)
    echo -n "."
  done
  echo " Translation complete!"
fi

echo "Book processing complete!"
```

## Fixing Bad OCR

When pages were OCR'd before cropped images existed, they contain text from both pages. Fix with:

```bash
# 1. Generate cropped images first (Step 2 above)

# 2. Find pages with bad OCR
BAD_OCR_IDS=$(jq '[.pages[] | select(.crop) | select(.ocr.data) |
  select(.ocr.data | test("two-page|spread"; "i")) | .id]' /tmp/book.json)

# 3. Re-OCR with overwrite
TOTAL=$(echo "$BAD_OCR_IDS" | jq 'length')
for ((i=0; i<TOTAL; i+=5)); do
  BATCH=$(echo "$BAD_OCR_IDS" | jq ".[$i:$((i+5))] | [.[] | {pageId: ., imageUrl: \"\", pageNumber: 0}]")
  curl -s -X POST "https://sourcelibrary.org/api/process/batch-ocr" \
    -H "Content-Type: application/json" \
    -d "{\"pages\":$BATCH,\"model\":\"gemini-3-flash-preview\",\"overwrite\":true}"
done
```

## Processing All Books

### Optimized Batch Script (Tier 1)

This script processes all books with proper rate limiting:

```bash
#!/bin/bash
# Optimized for Tier 1 (300 RPM) - adjust SLEEP_TIME for other tiers

BASE_URL="https://sourcelibrary.org"
# IMPORTANT: Always use gemini-3-flash-preview, NOT gemini-2.5-flash
MODEL="gemini-3-flash-preview"
BATCH_SIZE=5
SLEEP_TIME=0.4  # Tier 1: 0.4s, Tier 2: 0.12s, Tier 3: 0.06s

process_book() {
  BOOK_ID="$1"
  BOOK_DATA=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
  TITLE=$(echo "$BOOK_DATA" | jq -r '.title[0:30]')

  # Check what's needed (IMPORTANT: empty string detection)
  NEEDS_CROP=$(echo "$BOOK_DATA" | jq '[.pages[] | select(.crop) | select(.cropped_photo | not)] | length')
  NEEDS_OCR=$(echo "$BOOK_DATA" | jq '[.pages[] | select((.ocr.data // "") | length == 0)] | length')
  NEEDS_TRANSLATE=$(echo "$BOOK_DATA" | jq '[.pages[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0)] | length')

  if [ "$NEEDS_CROP" = "0" ] && [ "$NEEDS_OCR" = "0" ] && [ "$NEEDS_TRANSLATE" = "0" ]; then
    echo "SKIP: $TITLE"
    return
  fi

  echo "START: $TITLE [crop:$NEEDS_CROP ocr:$NEEDS_OCR trans:$NEEDS_TRANSLATE]"

  # Step 1: Crops
  if [ "$NEEDS_CROP" != "0" ]; then
    CROP_IDS=$(echo "$BOOK_DATA" | jq '[.pages[] | select(.crop) | select(.cropped_photo | not) | .id]')
    JOB_RESP=$(curl -s -X POST "$BASE_URL/api/jobs" \
      -H 'Content-Type: application/json' \
      -d "{\"type\": \"generate_cropped_images\", \"book_id\": \"$BOOK_ID\", \"page_ids\": $CROP_IDS}")
    JOB_ID=$(echo "$JOB_RESP" | jq -r '.job.id')

    if [ "$JOB_ID" != "null" ]; then
      while true; do
        RESULT=$(curl -s -X POST "$BASE_URL/api/jobs/$JOB_ID/process")
        [ "$(echo "$RESULT" | jq -r '.done')" = "true" ] && break
        sleep 1
      done
    fi
    BOOK_DATA=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
  fi

  # Step 2: OCR
  NEEDS_OCR=$(echo "$BOOK_DATA" | jq '[.pages[] | select((.ocr.data // "") | length == 0)] | length')
  if [ "$NEEDS_OCR" != "0" ]; then
    OCR_IDS=$(echo "$BOOK_DATA" | jq '[.pages[] | select((.ocr.data // "") | length == 0) | .id]')
    TOTAL_OCR=$(echo "$OCR_IDS" | jq 'length')

    for ((i=0; i<TOTAL_OCR; i+=BATCH_SIZE)); do
      BATCH=$(echo "$OCR_IDS" | jq ".[$i:$((i+BATCH_SIZE))]")
      PAGES=$(echo "$BATCH" | jq '[.[] | {pageId: ., imageUrl: "", pageNumber: 0}]')

      RESP=$(curl -s -X POST "$BASE_URL/api/process/batch-ocr" \
        -H 'Content-Type: application/json' \
        -d "{\"pages\": $PAGES, \"model\": \"$MODEL\"}")

      if echo "$RESP" | grep -q "429\|rate"; then
        echo "RATE_LIMIT: $TITLE - backing off 10s"
        sleep 10
        i=$((i-BATCH_SIZE))  # Retry this batch
      fi
      sleep $SLEEP_TIME
    done
    echo "OCR_DONE: $TITLE"
    BOOK_DATA=$(curl -s "$BASE_URL/api/books/$BOOK_ID")
  fi

  # Step 3: Translate with context
  NEEDS_TRANSLATE=$(echo "$BOOK_DATA" | jq '[.pages[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0)] | length')
  if [ "$NEEDS_TRANSLATE" != "0" ]; then
    TRANSLATE_PAGES=$(echo "$BOOK_DATA" | jq '[.pages | sort_by(.page_number) | .[] | select((.ocr.data // "") | length > 0) | select((.translation.data // "") | length == 0) | {pageId: .id, ocrText: .ocr.data, pageNumber: .page_number}]')
    TOTAL_TRANS=$(echo "$TRANSLATE_PAGES" | jq 'length')
    PREV_CONTEXT=""

    for ((i=0; i<TOTAL_TRANS; i+=BATCH_SIZE)); do
      BATCH=$(echo "$TRANSLATE_PAGES" | jq ".[$i:$((i+BATCH_SIZE))]")

      if [ -n "$PREV_CONTEXT" ]; then
        RESP=$(curl -s -X POST "$BASE_URL/api/process/batch-translate" \
          -H 'Content-Type: application/json' \
          -d "{\"pages\": $BATCH, \"model\": \"$MODEL\", \"previousContext\": \"$PREV_CONTEXT\"}")
      else
        RESP=$(curl -s -X POST "$BASE_URL/api/process/batch-translate" \
          -H 'Content-Type: application/json' \
          -d "{\"pages\": $BATCH, \"model\": \"$MODEL\"}")
      fi

      if echo "$RESP" | grep -q "429\|rate"; then
        echo "RATE_LIMIT: $TITLE - backing off 10s"
        sleep 10
        i=$((i-BATCH_SIZE))  # Retry this batch
      else
        LAST_ID=$(echo "$BATCH" | jq -r '.[-1].pageId')
        PREV_CONTEXT=$(echo "$RESP" | jq -r ".translations[\"$LAST_ID\"] // \"\"" | head -c 1500)
      fi
      sleep $SLEEP_TIME
    done
    echo "TRANS_DONE: $TITLE"
  fi

  echo "COMPLETE: $TITLE"
}

export -f process_book
export BASE_URL MODEL BATCH_SIZE SLEEP_TIME

echo "=== BATCH PROCESSING ==="
echo "Batch: $BATCH_SIZE | Sleep: ${SLEEP_TIME}s"

curl -s "$BASE_URL/api/books" | jq -r '.[] | .id' > /tmp/book_ids.txt
TOTAL=$(wc -l < /tmp/book_ids.txt | tr -d ' ')
echo "Processing $TOTAL books..."

cat /tmp/book_ids.txt | xargs -P 1 -I {} bash -c 'process_book "$@"' _ {}

echo "=== ALL DONE ==="
```

### Running the Script
```bash
# Save to file and run
chmod +x batch_process.sh
./batch_process.sh 2>&1 | tee batch.log

# Or run in background
nohup ./batch_process.sh > batch.log 2>&1 &
```

## Monitoring Progress

Check overall library status:

```bash
curl -s "https://sourcelibrary.org/api/books" | jq '[.[] | {
  title: .title[0:30],
  pages: .pages_count,
  ocr: .ocr_count,
  translated: .translation_count
}] | sort_by(-.pages)'
```

## Troubleshooting

### Empty Strings vs Null (CRITICAL)
In jq, empty strings `""` are truthy! This means:
- `select(.ocr.data)` matches pages with `""` (WRONG)
- `select(.ocr.data | not)` does NOT match pages with `""` (WRONG)
- Use `select((.ocr.data // "") | length == 0)` to find missing/empty OCR
- Use `select((.ocr.data // "") | length > 0)` to find pages WITH OCR content

### Rate Limits (429 errors)

#### Gemini API Tiers
| Tier | RPM | How to Qualify |
|------|-----|----------------|
| Free | 15 | Default |
| Tier 1 | 300 | Enable billing + $50 spend |
| Tier 2 | 1000 | $250 spend |
| Tier 3 | 2000 | $1000 spend |

#### Optimal Sleep Times by Tier
| Tier | Max RPM | Safe Sleep Time | Effective Rate |
|------|---------|-----------------|----------------|
| Free | 15 | 4.0s | ~15/min |
| Tier 1 | 300 | 0.4s | ~150/min |
| Tier 2 | 1000 | 0.12s | ~500/min |
| Tier 3 | 2000 | 0.06s | ~1000/min |

**Note:** Use ~50% of max rate to leave headroom for bursts.

#### API Key Rotation
The system supports multiple API keys for higher throughput:
- Set `GEMINI_API_KEY` (primary)
- Set `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`, ... up to `GEMINI_API_KEY_10`
- Keys rotate automatically with 60s cooldown after rate limit

With N keys at Tier 1, you get N × 300 RPM = N × 150 safe req/min

### Function Timeouts
- Jobs have `maxDuration=300s` for Vercel Pro
- If hitting timeouts, reduce `CROP_CHUNK_SIZE` in job processing

### Missing Cropped Photos
- Check if crop job completed successfully
- Verify page has `crop` data with `xStart` and `xEnd`
- Re-run crop generation for specific pages

### Bad OCR Detection
Look for these patterns in OCR text indicating wrong image was used:
- "two-page spread"
- "left page" / "right page" descriptions
- Duplicate text blocks
- References to facing pages
