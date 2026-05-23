---
name: tiktok-workflow-e2e
description: End-to-end orchestration of TikTok content creation. Single entry point for batch processing multiple products from scraping to production-ready scripts.
version: 1.4.0
author: Claude
updated: 2026-01-20 (aligned with underlying skills - corrected concurrency model)
---

# TikTok E2E Workflow

**Single command to process products from start to finish.**

---

## Quick Start

```bash
# Process single product
/workflow 1729607303430380470

# Process batch from CSV
/workflow --batch products.csv

# Resume from specific phase
/workflow --batch products.csv --start-phase analysis
```

---

## Workflow Phases

```
┌────────────────────────────────────────────────────────────────┐
│  PHASE 1: SCRAPING (Python)                                    │
│  Skill: tiktok_product_scraper.md                              │
│  Agent: Python script                                          │
│  Parallel: Yes (across products)                               │
│  Output: tabcut_data.json, product_images/, ref_video/*.mp4    │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  PHASE 2A: VIDEO ANALYSIS (Python Async)                       │
│  Skill: tiktok_ad_analysis.md                                  │
│  Agent: Python (3-phase pipeline: extract → transcribe → API)  │
│  Parallel: 5 products at once (5 Gemini CLI threads max)       │
│  Internal: Each product analyzes 5 videos in parallel          │
│  Output: video_N_analysis.md (5 files per product)             │
│  OPTIMIZED v4.4.0: 8 products in 4 min (was 16 min) - 4x faster│
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  PHASE 2B+2C: ANALYSIS + SYNTHESIS (Gemini MCP Async)          │
│  Skill: tiktok_product_analysis.md                             │
│  Agent: Gemini CLI MCP (async)                                 │
│  Parallel: SEQUENTIAL across products (5 MCP task limit)       │
│           Within each product: Videos(5) → Image(1) ∥ Synth(1) │
│  Output: image_analysis.md + video_synthesis.md                │
│  OPTIMIZED: 2B+2C run in parallel after 2A ⭐ ~3min savings    │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  QUALITY GATE                                                  │
│  Check: video_synthesis.md exists (80+ lines minimum)          │
│  Block: Cannot proceed to Phase 3 if missing                   │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  PHASE 3: SCRIPT GENERATION (Claude)                           │
│  Skill: tiktok_script_generator.md                             │
│  Agent: Claude (direct writing from synthesis)                 │
│  Parallel: Yes - batch Write calls (3 scripts + summary/product)│
│  Output: 3 scripts + Campaign_Summary.md                       │
│  OPTIMIZED v2.3.0: 2-3 min/product (was 5-8 min) - 2x faster  │
└────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Scraping

### Output Folder (Dated Batches)

This vault organizes runs under `product_list/YYYYMMDD/<product_id>/` (see existing folders like `product_list/20260103/`).

Set a date folder for the current run:

```bash
DATE=YYYYMMDD
OUT="../product_list/$DATE"
mkdir -p "$OUT"
```

**Execute:**
```bash
cd /Users/lxt/Movies/TikTok/WZ/lukas_9688/scripts
source venv/bin/activate

# Single product
python run_scraper.py --product-id {product_id} --download-videos --output-dir "$OUT"

# Batch (from products.csv)
python run_scraper.py --batch-file products.csv --download-videos --output-dir "$OUT"
```

**Output per product:**
```
product_list/YYYYMMDD/{product_id}/
├── tabcut_data.json       # Product metadata
├── tabcut_data.md         # Markdown version
├── product_images/        # 5-9 product images
│   └── *.webp
└── ref_video/             # Top 5 videos
    └── *.mp4
```

**Gate:** Check all products have `tabcut_data.json`

---

## Phase 2: Analysis

**⚠️ IMPORTANT:** Video analysis now runs with **cross-product parallelism** (up to 5 products simultaneously via Gemini CLI background tasks).

### Concurrency Model (v4.4.0 Optimized)

**Video Analysis (Python async - PARALLELIZED):**
- Uses `gemini_cli_execute_async` to launch up to **5 products in parallel**
- Each product uses Python's internal pipeline:
  - `asyncio` with `Semaphore(5)` for 5 concurrent Gemini API calls
  - `ThreadPoolExecutor(5)` for parallel FFmpeg frame extraction
  - Cached Whisper model (loads once per product)
- **Execution:** Launch 5 async tasks → wait → launch next batch
- **Result:** 8 products analyzed in ~4 minutes (was 16 min sequential)

**Image + Synthesis (Gemini MCP async):**
- **⚠️ CRITICAL:** 5 MCP task limit (per tiktok_product_analysis.md)
- Process products **SEQUENTIALLY** (one at a time)
- Within each product: Stage 1 (5 videos parallel) → Stage 2 (image) → Stage 3 (synthesis)
- **Never** try to parallelize multiple products for image+synthesis

### Model Policy (MANDATORY)

Run analysis prompts with:
- Primary: `-m gemini-3-pro-preview`
- Fallback (only if capacity/quota hit): `-m gemini-3-flash-preview`

### 2A: Video Analysis (Python - PARALLEL v4.4.0)

**Execute with parallelism (up to 5 products at once):**
```bash
cd scripts
source venv/bin/activate

# Launch 5 products in parallel using Gemini CLI async
# Product IDs: 1729671956792187076, 1729480049905277853, 1729637085247609526, etc.

# Example: Batch 1 (5 products in parallel)
for pid in 1729671956792187076 1729480049905277853 1729637085247609526 1729697087571270361 1729630936525936882; do
  python analyze_video_batch.py $pid --date YYYYMMDD &
done
wait

# Batch 2 (remaining 3 products)
for pid in 1729607303430380470 1729607478878640746 1729489298386491816; do
  python analyze_video_batch.py $pid --date YYYYMMDD &
done
wait
```

**What happens per product (3-phase pipeline):**
```
📦 PHASE 1: Parallel frame extraction (ThreadPoolExecutor, 5 workers)
  → All 5 videos extract frames simultaneously (~10-15s)

🎤 PHASE 2: Sequential transcription (cached Whisper model)
  → Model loads once, transcribes all 5 videos (~30-50s)

🤖 PHASE 3: Parallel Gemini analysis (asyncio.Semaphore(5))
  → 5 async subprocess calls to gemini-cli (~60-120s)

Total per product: ~80-120s (was ~4-5 min)
```

**Performance (v4.4.0 - PARALLELIZED):**
- **Single product (5 videos):** 80-120 seconds
- **8 products sequentially:** 16 minutes
- **8 products in 2 batches (5+3):** ~4 minutes ⭐ **4x faster**
- **Key:** Gemini CLI limit = 5 concurrent threads max

**Output:** `ref_video/video_N_analysis.md` (bilingual, per video)

### 2B+2C: Image Analysis + Video Synthesis (Gemini MCP Async - PARALLEL ⭐)

**✅ OPTIMIZED MODEL (v1.5.0):**

Uses **Gemini CLI MCP async** (NOT Claude). Process products **SEQUENTIALLY**, but **2B and 2C run in parallel** after 2A completes.

**Pipeline per product (2 stages: sequential 2A, then parallel 2B+2C):**
```
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: Video Analysis (5 tasks in parallel - fills limit) │
│ └─ video_1..5_analysis.md → Wait for all 5                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ Stage 2: Image Analysis (1)  │ │ Stage 3: Synthesis (1)       │
│ └─ image_analysis.md         │ │ └─ video_synthesis.md        │
└──────────────────────────────┘ └──────────────────────────────┘
              ↓                               ↓
              └───────────────┬───────────────┘
                              ↓ wait for both
Then proceed to next product...
```

**Key Optimization:** Image analysis and synthesis have **no dependency** on each other:
- Image reads: `product_images/*.webp`
- Synthesis reads: `ref_video/video_*_analysis.md` (from Stage 1)
- Can safely run in parallel using only 2 of 5 available MCP slots

**Execution:**
```bash
# Process products sequentially with optimized pipeline
for product_id in $products; do
  # Stage 1: Launch 5 video analyses (parallel, fills 5 MCP slots)
  python analyze_video_batch.py $product_id --date YYYYMMDD &
  wait  # Wait for video analysis to complete
  
  # Stage 2+3: Launch image + synthesis in parallel (uses 2 slots)
  python analyze_product_images.py $product_id --date YYYYMMDD &
  python create_video_synthesis.py $product_id --date YYYYMMDD &
  wait  # Wait for both to complete
done
```

**Performance (8 products):**
- Per product: Videos (2min) + max(Image 3min, Synthesis 3min) = ~5 min
- 8 products sequential: ~40 min
- **Old model:** Videos (2min) + Image (3min) + Synthesis (3min) = ~8 min → ~64 min total
- **Savings:** ~24 minutes for 8 products ⭐ **~3 min per product**

**Output per product:**
- `product_images/image_analysis.md`
- `ref_video/video_synthesis.md` (CRITICAL)

---

## Quality Gate - ENHANCED

**Before Phase 3, verify analysis quality and compliance:**

### Option 1: Enhanced Quality Gate (Recommended)

Use the updated verify_gate.sh script with integrated quality validators:

```bash
# Comprehensive gate: file existence + bilingual coverage + compliance + ElevenLabs cues
bash scripts/verify_gate.sh --date YYYYMMDD --csv scripts/products.csv --phase all
```

The enhanced gate now validates:
- **Phase 1: File Existence** (existing checks)
  - `tabcut_data.json/md` presence
  - `image_analysis.md` (200+ lines, no meta preamble)
  - `video_synthesis.md` (150+ lines, no meta preamble)
  - Video analysis files count
  - Script files count (4+)

- **Phase 2: Quality Standards** (NEW)
  - **Bilingual Coverage**: DE/ZH pairs (30+), bilingual headers (10+), Chinese ratio (8-25%)
  - **Compliance Flags**: Risky claims properly flagged in analysis, absent from scripts
  - **ElevenLabs Cues**: Density (≥0.3), variety (≥8 unique), valid cues only

### Option 2: Manual Verification (Basic)

If you need a quick check without quality validators:

```bash
#!/bin/bash
# verify_ready_for_scripts.sh

date="YYYYMMDD"
products="1729607303430380470 1729607478878640746 ..."  # Your product IDs

for pid in $products; do
  echo "=== $pid ==="

  # MANDATORY: Synthesis must exist
  if [ ! -f "product_list/$date/$pid/ref_video/video_synthesis.md" ]; then
    echo "❌ BLOCKED: video_synthesis.md missing"
    exit 1
  fi

  lines=$(wc -l < "product_list/$date/$pid/ref_video/video_synthesis.md" | tr -d ' ')
  if [ "$lines" -lt 150 ]; then
    echo "❌ BLOCKED: synthesis only $lines lines (need 150+)"
    exit 1
  fi

  # NEW: Quality validators (optional but recommended)
  echo "Checking quality standards..."
  python3 scripts/validate_bilingual_coverage.py "product_list/$date/$pid/ref_video/video_synthesis.md" || echo "⚠️ Bilingual coverage below standards"
  python3 scripts/validate_compliance_flags.py "product_list/$date/$pid/ref_video/video_synthesis.md" || echo "⚠️ Compliance issues found"

  echo "✅ Ready for scripts"
done

echo ""
echo "=== ALL PRODUCTS READY FOR PHASE 3 ==="
```

### Individual Validator Usage

Run validators individually for debugging:

```bash
# Bilingual coverage
python3 scripts/validate_bilingual_coverage.py product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md

# Compliance flags
python3 scripts/validate_compliance_flags.py product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md

# ElevenLabs cues (for scripts)
python3 scripts/validate_elevenlabs_cues.py product_list/YYYYMMDD/{product_id}/scripts/Script_Name.md
```

---

## Phase 3: Script Generation (BATCHED v2.3.0)

⚠️ **CRITICAL FORMAT REQUIREMENT - ElevenLabs v3 Inline Cues:**
- **MANDATORY:** Emotion cues MUST be inline: `[emotion] Text here.`
- **FORBIDDEN:** Broken lines format with cue on separate line from text
- **WRONG:** `[frustrated]` followed by `Du kennst das?` on next line ❌
- **CORRECT:** `[frustrated] Du kennst das?` on same line ✅
- See `tiktok_script_generator.md` lines 285-311 for full format specification

**Execute (Claude Code with batch Write calls):**

For each product, Claude reads analysis files and writes **ALL 4 FILES IN ONE MESSAGE**:
1. `Script_1_[Angle].md` - Hook/Challenge angle
2. `Script_2_[Angle].md` - Feature Demo angle
3. `Script_3_[Angle].md` - Social Proof angle
4. `Campaign_Summary.md` - Executive summary

**CRITICAL OPTIMIZATION:** Use 4 parallel Write tool calls in a single message:
```
[Read synthesis, image analysis, tabcut data]
[Generate all 3 scripts + Campaign Summary]
[Call Write tool 4 times in parallel in single message]
```

**Performance:**
- **Old (sequential):** 5-8 min per product (read → write → read → write → ...)
- **New (batched):** 2-3 min per product (read all → write all) ⭐ **2x faster**
- **8 products:** 16-24 min (was 40-50 min)

**Output location:** `product_list/YYYYMMDD/{product_id}/scripts/`

**Key rules:**
- Claude writes ALL scripts (not Gemini)
- Read ALL analysis files in parallel (5+ Read calls at once)
- Write ALL 4 files in parallel (4 Write calls in one message)
- Campaign Summary references files (no duplication)

### Retry / Stop Rules

- If the gate fails (missing files or below line thresholds), retry the failed stage **once** with the strict output contract prompts.
- If it fails again, mark that product as **BLOCKED** and continue to the next product (do not generate scripts with incomplete analysis).

---

## Autonomous Batch Execution

**To run the full workflow autonomously:**

```
User prompt to Claude:

"Run the e2e workflow for these products autonomously:
- products.csv contains 8 product IDs
- Don't pause for approval between phases
- If something fails, retry once then skip and continue
- Report failures at the end"
```

**Claude will:**
1. Run Phase 1 (scraping) - wait for completion
2. Run Phase 2A (video analysis) - parallel via Python (bash bg, 5 products max)
3. Run Phase 2B+2C (image + synthesis) - **SEQUENTIAL** via Gemini MCP (per tiktok_product_analysis.md)
4. Verify quality gate
5. Run Phase 3 (scripts) - sequential with batched writes
6. Report completion status

---

## Time Estimates

**Updated for v4.4.0 parallel video analysis + v2.3.0 batched scripts**

| Phase | Single Product | 8 Products | Scaling Notes |
|:------|:---------------|:-----------|:--------------|
| 1. Scraping | 2-3 min | 5 min | Parallel across products |
| 2A. Video Analysis | **1.5-2 min** | **4 min** | **v4.4.0: 5 products parallel (bash bg)** ⭐ |
| 2B+2C. Image+Synthesis | **~3 min** | **~24 min** | **PARALLEL 2B∥2C** (v1.5.0 optimized) ⭐ |
|  - Image (Gemini MCP) | 3 min | - | Parallel with Synthesis ∥ |
|  - Synthesis (Gemini MCP) | 3 min | - | Parallel with Image ∥ |
| 3. Scripts | **2-3 min** | **16-24 min** | **Batched Write calls** ⭐ |
| **Total** | **~8-10 min** | **~49-57 min** | Optimized model |

### Performance Notes

**Phase 2A Video Analysis (8 products) - PARALLELIZED:**
- **Old (v4.3.0 sequential):** 8 × 2 min = 16 min
- **New (v4.4.0 parallel):** Batch1(5): 2min + Batch2(3): 2min = 4 min
- **Savings:** ~12 minutes ⭐ **4x faster**

**Phase 2B+2C Image+Synthesis (8 products) - PARALLEL WITHIN PRODUCT ⭐:**
- **Optimized v1.5.0:** Image and Synthesis run in parallel after videos complete
- **Why it works:** No dependency between image analysis and synthesis
- **Time:** 8 × max(3min, 3min) = ~24 min (was ~32 min sequential)
- **Savings:** ~8 minutes for 8 products (~1 min per product)

**Phase 3 Scripts (8 products) - BATCHED:**
- **Old (sequential writes):** 8 × 5 min = 40 min
- **New (batched writes):** 8 × 2.5 min = 20 min
- **Savings:** ~20 minutes ⭐ **2x faster**

**Total Workflow (Optimized v1.5.0):**
- **Phase 1:** 5 min
- **Phase 2A:** 4 min (parallel video analysis)
- **Phase 2B+2C:** 24 min (parallel image + synthesis per product) ⭐
- **Phase 3:** 20 min (batched script writes)
- **Total:** ~53 min for 8 products (was ~61 min)

### Pipeline Strategy (8 Products - PARALLELIZED)

**Phase 2A: Video Analysis (Parallel batches of 5):**

```
┌─────────────────────────────────────────────────────────────┐
│ BATCH 1 (5 products in parallel) - 2 minutes               │
├─────────────────────────────────────────────────────────────┤
│ Product 1: [Videos: 5 parallel Gemini calls] → 2 min       │
│ Product 2: [Videos: 5 parallel Gemini calls] → 2 min       │
│ Product 3: [Videos: 5 parallel Gemini calls] → 2 min       │ All running
│ Product 4: [Videos: 5 parallel Gemini calls] → 2 min       │ simultaneously
│ Product 5: [Videos: 5 parallel Gemini calls] → 2 min       │ (max 5 threads)
└─────────────────────────────────────────────────────────────┘
                              ↓ wait for completion
┌─────────────────────────────────────────────────────────────┐
│ BATCH 2 (3 products in parallel) - 2 minutes               │
├─────────────────────────────────────────────────────────────┤
│ Product 6: [Videos: 5 parallel Gemini calls] → 2 min       │
│ Product 7: [Videos: 5 parallel Gemini calls] → 2 min       │ Running
│ Product 8: [Videos: 5 parallel Gemini calls] → 2 min       │ simultaneously
└─────────────────────────────────────────────────────────────┘

Total: ~4 min (was 16 min sequential) ⭐ 4x faster
```

**Phase 2B+2C: Image + Synthesis (PARALLEL WITHIN PRODUCT ⭐ v1.5.0):**
```
✅ OPTIMIZED: 2B and 2C run in parallel after 2A completes

Product 1: [Videos: 5 parallel] → [Image ∥ Synthesis] → ~5 min
Product 2: [Videos: 5 parallel] → [Image ∥ Synthesis] → ~5 min
Product 3: [Videos: 5 parallel] → [Image ∥ Synthesis] → ~5 min
...
Product 8: [Videos: 5 parallel] → [Image ∥ Synthesis] → ~5 min

Total: ~40 min (was ~64 min sequential 2B→2C) ⭐ ~3 min savings per product
```

**Why parallel 2B+2C works:**
- Image analysis reads: `product_images/*.webp`
- Synthesis reads: `ref_video/video_*_analysis.md` (from 2A)
- **No dependency** between them → safe to run concurrently
- Uses only 2 of 5 available MCP slots (well within limits)

**Phase 3: Scripts (Batched Write calls per product):**
```
Product 1: [Read all files parallel] → [Write 4 files parallel] → 2.5 min
Product 2: [Read all files parallel] → [Write 4 files parallel] → 2.5 min
...
Product 8: [Read all files parallel] → [Write 4 files parallel] → 2.5 min
Total: ~20 min (was 40 min) ⭐ 2x faster
```

---

## Error Handling

| Error | Action |
|:------|:-------|
| Scraping fails | Retry once, then skip product |
| No videos downloaded | Skip video analysis, continue with images |
| Video analysis fails | Retry with single video, mark incomplete |
| Image analysis fails | Continue without (not mandatory) |
| Synthesis fails | BLOCK - retry until success or manual intervention |
| Script generation fails | Retry, check for generic placeholders |

---

## Resume Points

**If workflow interrupted:**

```bash
# Check current state
./check_workflow_status.sh products.csv

# Resume from Phase 2
/workflow --batch products.csv --start-phase analysis

# Resume from Phase 3 only
/workflow --batch products.csv --start-phase scripts
```

---

## Skill Dependency Map

```
tiktok_product_scraper.md (v2.0.0)
│  Agent: Python script
│  Output: tabcut_data.json, product_images/, ref_video/*.mp4
│
├──────────────────────────────────────────────────┐
│                                                  │
▼                                                  ▼
tiktok_ad_analysis.md (v4.4.0)        tiktok_product_analysis.md (v1.0.0)
│  Agent: Python + Gemini CLI          │  Agent: Gemini MCP async
│  Parallel: 5 products via bash bg    │  Sequential: 1 product at a time
│  Output: video_N_analysis.md         │  Output: image_analysis.md
│                                      │
└──────────────┬───────────────────────┘
               │
               ▼
    tiktok_product_analysis.md (v1.0.0)
    │  Agent: Gemini MCP async
    │  Output: video_synthesis.md (CRITICAL)
    │
    ▼
    tiktok_script_generator.md (v2.3.0)
    │  Agent: Claude Code
    │  Batched: 4 Write calls per product
    │  Output: Script_1/2/3.md + Campaign_Summary.md
```

**Agent Assignment Summary:**
| Phase | Agent | Why |
|:------|:------|:----|
| 1. Scraping | Python | Playwright automation |
| 2A. Video Analysis | Python + Gemini CLI | Bash background parallelism |
| 2B. Image Analysis | Gemini MCP async | Sequential, 5 task limit |
| 2C. Synthesis | Gemini MCP async | Sequential, 5 task limit |
| 3. Scripts | Claude Code | Better creative quality |

---

## Example: Full Batch Run

```
User: Run e2e workflow for products.csv autonomously

Claude:
1. Starting Phase 1: Scraping 8 products...
   ✅ 8/8 products scraped (5 min)

2. Starting Phase 2: Analysis (PARALLELIZED v4.4.0)...

   === Phase 2A: Video Analysis (Batch 1 - 5 products in parallel) ===
   🚀 Launching 5 parallel video analysis tasks...
   - Product 1: [Videos: 5 parallel Gemini calls]
   - Product 2: [Videos: 5 parallel Gemini calls]
   - Product 3: [Videos: 5 parallel Gemini calls]
   - Product 4: [Videos: 5 parallel Gemini calls]
   - Product 5: [Videos: 5 parallel Gemini calls]
   ⏳ Waiting for batch completion...
   ✅ Batch 1 complete (2 min)

   === Phase 2A: Video Analysis (Batch 2 - 3 products in parallel) ===
   🚀 Launching 3 parallel video analysis tasks...
   - Product 6: [Videos: 5 parallel Gemini calls]
   - Product 7: [Videos: 5 parallel Gemini calls]
   - Product 8: [Videos: 5 parallel Gemini calls]
   ⏳ Waiting for batch completion...
   ✅ Batch 2 complete (2 min)

   ✅ All 8 products - videos analyzed (4 min total, was 16 min) ⭐ 4x faster

   === Phase 2B+2C: Image Analysis + Synthesis (PARALLEL 2B∥2C - v1.5.0) ===
   📦 Product 1: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 2: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 3: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 4: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 5: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 6: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 7: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   📦 Product 8: [Videos 5∥] → [Image ∥ Synthesis] ✅ (5 min)
   ✅ All 8 products analyzed (40 min total - 2B+2C parallel per product) ⭐

3. Quality Gate...
   ✅ 8/8 products have valid synthesis files

4. Starting Phase 3: Script Generation (BATCHED v2.3.0)...
   - Product 1/8: [Read all] → [Write 4 files in parallel] ✅ (2.5 min)
   - Product 2/8: [Read all] → [Write 4 files in parallel] ✅ (2 min)
   - Product 3/8: [Read all] → [Write 4 files in parallel] ✅ (2.5 min)
   - Product 4/8: [Read all] → [Write 4 files in parallel] ✅ (3 min)
   - Product 5/8: [Read all] → [Write 4 files in parallel] ✅ (2 min)
   - Product 6/8: [Read all] → [Write 4 files in parallel] ✅ (2.5 min)
   - Product 7/8: [Read all] → [Write 4 files in parallel] ✅ (3 min)
   - Product 8/8: [Read all] → [Write 4 files in parallel] ✅ (2.5 min)
   ✅ All scripts generated (20 min, was 40 min) ⭐ 2x faster

=== WORKFLOW COMPLETE ===
Total time: ~61 minutes (corrected model per tiktok_product_analysis.md)
Products processed: 8/8
Scripts generated: 24 (3 per product)
Campaign summaries: 8

Performance Breakdown:
- Phase 1 (Scraping): 5 min
- Phase 2A (Videos): 4 min ⭐ (was 16 min - 4x faster via bash parallel batches)
- Phase 2B+2C (Image+Synthesis): 24 min ⭐ (was 32 min - parallel 2B∥2C optimization)
- Phase 3 (Scripts): 20 min ⭐ (was 40 min - 2x faster via batched writes)

Ready for video production!
```

---

**Version:** 1.5.0
**Last Updated:** 2026-01-21
**Changelog:**
- v1.5.0 (2026-01-21): **OPTIMIZED PHASE 2B+2C PARALLEL EXECUTION** ⭐
  - **NEW:** Image analysis and synthesis run in parallel after video analysis
  - **Why:** No dependency between 2B (images) and 2C (synthesis from videos)
  - **Execution:** `python analyze_product_images.py $pid & python create_video_synthesis.py $pid & wait`
  - **Performance:** ~3 min savings per product (5 min vs 8 min)
  - **8 products:** ~53 min (was ~61 min) - saves ~8 minutes total
  - Updated all workflow diagrams, time tables, and execution examples
  - MCP slot usage: Only 2 of 5 slots for 2B+2C (safe and efficient)
- v1.4.0 (2026-01-20): **ALIGNED WITH UNDERLYING SKILLS**
  - **CORRECTED:** Phase 2B+2C uses Gemini MCP async (NOT Claude)
  - Aligned with tiktok_product_analysis.md v1.0.0 concurrency constraints
  - Phase 2A (videos): Parallel via bash bg
  - Updated pipeline diagrams to show correct execution model
- v1.3.0 (2026-01-18): Parallel video analysis + batched scripts
  - Parallel video analysis across products (5 Gemini CLI threads max)
  - Batched script generation (4 Write calls per product in one message)
  - Phase 2A: 4 min (was 16 min) via parallel batches of 5 products
  - Phase 3: 20 min (was 40 min) via batched Write tool calls
- v1.2.0 (2026-01-07): Parallel image+synthesis execution (NOTE: was incorrect)
- v1.1.0 (2026-01-07): Updated for v4.3.0 video analysis optimizations
  - 3-5x faster video analysis (Python async + ThreadPoolExecutor)
  - Clarified that video analysis uses Python async, not MCP slots
- v1.0.0 (2026-01-01): Initial e2e workflow documentation
