---
name: tiktok-product-analysis
description: Parallel analysis pipeline for TikTok product campaigns. Handles image analysis, video analysis, and market synthesis using Gemini async MCP. Prepares all foundation data before script generation. Designed for batch processing multiple products simultaneously.
version: 1.0.0
author: Claude
execution_agent: Gemini CLI MCP (async)
---

# TikTok Product Analysis Skill

**PURPOSE:** Prepare all analysis foundation before script generation
**EXECUTOR:** Gemini CLI MCP (async for parallelism)
**OUTPUT:** Analysis files that script generator will reference (not duplicate)

---

## Compliance & Policy Notes (DE Market) - ENHANCED

### Safety Matrix with Concrete Examples

This skill should explicitly capture policy-sensitive claims so downstream scripts stay safe.

| Risk Type | ❌ AVOID | ⚠️ USE CAREFULLY | ✅ SAFE |
|:----------|:---------|:----------------|:--------|
| **Price** | "nur €10!", "50% Rabatt" | "~€10" with disclaimer | "erschwinglich", "preiswert" |
| **Waterproof** | "100% wasserdicht", "完全防水" | "IP67" (only if sourced) | "spritzwassergeschützt" |
| **Medical** | "heilt", "Schmerzfreiheit" | "Entspannung" (no guarantees) | "angenehm", "komfortabel" |
| **Tech Specs** | "4K Support" (ambiguous) | "4K Dekodierung" (if sourced) | "HD Qualität" |

**Example format for analysis files:**
```markdown
*   **CRITICAL**: Das Produkt ist NICHT spülmaschinenfest. Darauf muss in Kommentaren hingewiesen werden.
    **关键**：该产品不可放入洗碗机。必须在评论中指出。
```

Add these as explicit DO/DON'T bullets with concrete examples in the generated `ref_video/video_synthesis.md` (section already exists in your template as "Compliance & Trust Signals").

---

## Bilingual Output Standards | 双语输出标准

MANDATORY inline Chinese translation pattern for all analysis files:

**Format for key bullets:**
```markdown
- DE: German or English description
  ZH: 中文翻译
```

**Example from gold-standard sample (image_analysis.md:93-94):**
```markdown
*   **12-Blade Power (`product_image_6.webp`):**
    *   DE: Die meisten tragbaren Mixer haben nur 4 oder 6 Klingen.
        ZH: 大多数便携式榨汁机只有4或6叶刀片。
```

**Target metrics:**
- Chinese character ratio: 15-20% of total content
- DE/ZH pairs: 30+ per analysis file
- Bilingual section headers: 10+ per file

**Quality indicators:**
- NOT literal word-for-word translation
- Cultural adaptation for Chinese-speaking German residents
- Natural idioms and expressions
- Maintain German brand names and technical terms

---

## Agent Assignment

| Task | Agent | Tool | Parallelizable |
|:-----|:------|:-----|:---------------|
| Image Analysis | Gemini | `gemini_cli_execute_async` | Yes - per product |
| Video Analysis | Gemini | `gemini_cli_execute_async` | Yes - per video |
| Video Synthesis | Gemini | `gemini_cli_execute_async` | Yes - per product (after videos) |
| Script Generation | Claude | Direct writing | No - sequential quality focus |
| Campaign Summary | Claude | Direct writing | No - needs scripts first |

---

## ⚠️ Concurrency Limits | 并发限制

**CRITICAL OPERATIONAL CONSTRAINT:**

Gemini async MCP has a **maximum safe limit of 5 concurrent tasks**.

## Model Policy (MANDATORY)

Use **Gemini 3.0** models first:
- Primary: `gemini-3-pro-preview`
- Fallback (only if capacity/quota hit): `gemini-3-flash-preview`

Avoid relying on older `2.5` models unless explicitly requested.

---

## German Market Intelligence (MANDATORY in video_synthesis.md)

**Required section in synthesis output: "## German Market Fit | 德国市场适配"**

Analysis files must include specific cultural context that informs creative production:

**Must document:**
1. 5+ specific cultural behaviors/preferences observed in winning videos
2. How each behavior maps to creative production choices
3. Language signals Germans respond to (formal/informal, proof > emotion)
4. Trust signals specific to German market (specs, numbers, precision)

**Example pattern from gold-standard sample:**

```markdown
## German Market Fit | 德国市场适配

**Cultural Triggers (文化触发器):**
- Germans worry portable gadgets are "weak toys" → Ice crush proof shot needed
- Germans value efficiency over entertainment → Office routine angle resonates
- Germans are price-sensitive but not cheap → Show exact ROI math (€109/month vs €10/month)
- Germans trust specs over claims → LED battery display = credibility
- Germans prefer practical over aesthetic → Function-first storyboards
```

**Implementation requirement:**
- This section must appear in `video_synthesis.md`
- Must include 5+ specific cultural insights with actionable implications
- Must show how insights translate to creative decisions

---

### The Real Bottleneck: Videos Per Product

**Each product has 5 top-performing videos** to analyze. This means:

| Task Type | Concurrency | Slots Used |
|:----------|:------------|:-----------|
| 5 videos (per product) | Parallel | **5 slots** ✅ (FULL) |
| + Image analysis | ❌ BLOCKED | Would need 6 slots |
| + Synthesis | ❌ BLOCKED | Would need 6 slots |

### Why This Matters

❌ **WRONG - Launching videos + images simultaneously:**
```python
# DANGEROUS - Exceeds 5-task limit
for product in products:
    # Launch 5 videos in parallel (5 tasks)
    for video in get_videos(product):  # 5 videos
        launch_video_analysis(product, video)

    # FAILS - trying to add 6th task while videos running
    launch_image_analysis(product)
```

✅ **CORRECT - Sequential pipeline per product:**
```python
# SAFE - Process products sequentially, pipeline within each
for product_id in products:  # Sequential across products

    # Step 1: Launch 5 video analyses in parallel (fills all 5 slots)
    video_tasks = []
    for i, video in enumerate(get_videos(product_id)):
        task = launch_video_analysis(product_id, i+1, video)
        video_tasks.append(task)

    # Wait for all 5 videos to complete
    wait_for_all(video_tasks)

    # Step 2: Launch image analysis (1 task)
    image_task = launch_image_analysis(product_id)
    wait_for_completion(image_task)

    # Step 3: Launch synthesis (1 task)
    synthesis_task = launch_synthesis(product_id)
    wait_for_completion(synthesis_task)

    print(f"✅ Product {product_id} complete")
```

### Pipeline Strategy Per Product

**Within ONE product (sequential stages):**
1. **Video Analysis Stage**: 5 videos in parallel → Wait for completion
2. **Image Analysis Stage**: 1 task → Wait for completion
3. **Synthesis Stage**: 1 task → Wait for completion

**Across multiple products:**
- Process products **sequentially** (one product pipeline at a time)
- Never try to process multiple products in parallel

### Time Impact (8 Products Example)

**Sequential processing (CORRECT):**
- Product 1: Videos (2min) + Image (1min) + Synthesis (1min) = 4 min
- Product 2: 4 min
- ...
- Product 8: 4 min
- **Total: ~32 minutes** for 8 products

**Trying to parallelize products (BROKEN):**
- Launch all 8 products' video analyses = 40 concurrent tasks
- Result: **TIMEOUT/FAILURE** ❌

**Why sequential is still fast:**
- Within each product, 5 videos analyzed in parallel (not sequential)
- If videos were sequential: 5 × 2min = 10min per product = 80min total
- With parallel videos: 2min per product = 32min total
- **Still 2.5x faster** than fully sequential

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: SEQUENTIAL PRODUCT ANALYSIS (Gemini Async MCP)    │
│  Process products one at a time, pipeline within each       │
│                                                             │
│  FOR EACH PRODUCT (sequential):                             │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Stage 1: Video Analysis (PARALLEL)                 │    │
│  │ ├─ Video 1 analysis ──┐                            │    │
│  │ ├─ Video 2 analysis ──┤                            │    │
│  │ ├─ Video 3 analysis ──┼─→ Wait for all 5 complete │    │
│  │ ├─ Video 4 analysis ──┤   (fills all 5 slots)     │    │
│  │ └─ Video 5 analysis ──┘                            │    │
│  └────────────────────────────────────────────────────┘    │
│                      ↓                                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Stage 2: Image Analysis (1 task)                   │    │
│  │ └─ Analyze all product images → Wait for complete  │    │
│  └────────────────────────────────────────────────────┘    │
│                      ↓                                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Stage 3: Video Synthesis (1 task)                  │    │
│  │ └─ Synthesize market insights → Wait for complete  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  Repeat for next product...                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  QUALITY GATE: Verify all analysis files exist              │
│  - image_analysis.md (if images exist)                      │
│  - video_N_analysis.md (for each video)                     │
│  - video_synthesis.md (MANDATORY)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: SCRIPT GENERATION (Claude Code)                   │
│  → Uses tiktok_script_generator.md skill                    │
│  → References analysis files (does NOT duplicate content)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Sequential Product Analysis Pipeline

**Process products one at a time, with pipeline stages within each product.**

### Complete Implementation

```python
PROJECT_ROOT = "/Users/lxt/Movies/TikTok/WZ/lukas_9688"

for product_id in product_ids:  # Sequential across products
    print(f"\n=== Processing Product {product_id} ===")

    # Stage 1: Launch 5 video analyses in parallel
    print(f"Stage 1: Analyzing 5 videos in parallel...")
    video_tasks = []
    videos = get_videos(product_id)  # Returns list of 5 video paths

    for i, video in enumerate(videos, 1):
        task = mcp__gemini-cli-mcp-async__gemini_cli_execute_async({
            "query": VIDEO_ANALYSIS_PROMPT.format(
                product_id=product_id,
                video_num=i,
                video_path=video
            ),
            "working_dir": PROJECT_ROOT,
            "yolo": True
        })
        video_tasks.append(task)

    # Wait for all 5 videos to complete
    for task in video_tasks:
        result = check_task_completion(task)
        while result.status == "running":
            time.sleep(5)
            result = check_task_completion(task)

    print(f"✅ Stage 1 complete: 5 videos analyzed")

    # Stage 2: Launch image analysis (1 task)
    if has_images(product_id):
        print(f"Stage 2: Analyzing product images...")
        image_task = mcp__gemini-cli-mcp-async__gemini_cli_execute_async({
            "query": IMAGE_ANALYSIS_PROMPT.format(product_id=product_id),
            "working_dir": PROJECT_ROOT,
            "yolo": True
        })

        # Wait for image analysis to complete
        result = check_task_completion(image_task)
        while result.status == "running":
            time.sleep(5)
            result = check_task_completion(image_task)

        print(f"✅ Stage 2 complete: Images analyzed")

    # Stage 3: Launch video synthesis (1 task)
    print(f"Stage 3: Creating market synthesis...")
    synthesis_task = mcp__gemini-cli-mcp-async__gemini_cli_execute_async({
        "query": SYNTHESIS_PROMPT.format(product_id=product_id),
        "working_dir": PROJECT_ROOT,
        "yolo": True
    })

    # Wait for synthesis to complete
    result = check_task_completion(synthesis_task)
    while result.status == "running":
        time.sleep(5)
        result = check_task_completion(synthesis_task)

    print(f"✅ Stage 3 complete: Synthesis created")
    print(f"✅✅✅ Product {product_id} COMPLETE\n")

print(f"\n=== ALL {len(product_ids)} PRODUCTS ANALYZED ===")
```

### Breakdown by Stage

**Stage 1: Video Analysis (Parallel within product)**
- Launch 5 video analyses simultaneously
- Uses all 5 available Gemini async slots
- Wait for all to complete before proceeding

**Stage 2: Image Analysis (Single task)**
- Launch 1 image analysis task
- Wait for completion before proceeding
- Skipped if product has no images

**Stage 3: Video Synthesis (Single task)**
- Launch 1 synthesis task
- Requires Stage 1 video analyses to exist
- Wait for completion before moving to next product

---

## Quality Gate: Analysis Verification

**Run BEFORE proceeding to script generation:**

```bash
#!/bin/bash
# verify_analysis.sh

product_id=$1
date="YYYYMMDD"
base="product_list/$date/$product_id"
status="PASS"

echo "=== Analysis Verification: $product_id ==="

# Check 1: Image analysis (if images exist)
if [ -d "$base/product_images" ]; then
    img_count=$(find "$base/product_images" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.webp" \) 2>/dev/null | wc -l | tr -d ' ')
    if [ "$img_count" -gt 0 ]; then
        if [ -f "$base/product_images/image_analysis.md" ]; then
            lines=$(wc -l < "$base/product_images/image_analysis.md" | tr -d ' ')
            if [ "$lines" -ge 200 ]; then
                echo "✅ Image analysis: $lines lines"
            else
                echo "⚠️ Image analysis incomplete: $lines lines (need 200+)"
                status="WARN"
            fi
        else
            echo "❌ Image analysis MISSING (found $img_count images)"
            status="FAIL"
        fi
    fi
fi

# Check 2: Video synthesis (MANDATORY if videos exist)
if [ -d "$base/ref_video" ]; then
    video_count=$(find "$base/ref_video" -type f -name "*.mp4" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$video_count" -gt 0 ]; then
        if [ -f "$base/ref_video/video_synthesis.md" ]; then
            lines=$(wc -l < "$base/ref_video/video_synthesis.md" | tr -d ' ')
            if [ "$lines" -ge 150 ]; then
                echo "✅ Video synthesis: $lines lines"
            else
                echo "⚠️ Video synthesis incomplete: $lines lines (need 150+)"
                status="WARN"
            fi
        else
            echo "❌ Video synthesis MISSING (found $video_count videos)"
            status="FAIL"
        fi

        # Check individual video analyses
        analysis_count=$(find "$base/ref_video" -type f -name "video_*_analysis.md" 2>/dev/null | wc -l | tr -d ' ')
        echo "   Video analyses: $analysis_count/$video_count"
        
        # CRITICAL: Verify compliance risks are properly flagged in synthesis
        echo "   Checking compliance flagging..."
        if [ -f "$base/ref_video/video_synthesis.md" ]; then
            if python3 scripts/validate_compliance_flags.py "$base/ref_video/video_synthesis.md" >/dev/null 2>&1; then
                echo "   ✅ Compliance risks properly flagged"
            else
                echo "   ⚠️ WARNING: Unflagged compliance risks detected"
                echo "      Run: python3 scripts/validate_compliance_flags.py \"$base/ref_video/video_synthesis.md\""
                echo "      Ensure 'Compliance & Trust Signals' section documents all risks"
                status="WARN"
            fi
        fi
    fi
fi

echo ""
echo "Status: $status"
[ "$status" = "FAIL" ] && exit 1
exit 0
```

### Recommended (Repo Verifier)

Prefer the repo verifier script so the gate is consistent across runs:

```bash
# Analysis-only gate for a date batch folder
bash scripts/verify_gate.sh --date YYYYMMDD --csv scripts/products.csv --phase analysis
```

### Retry / Stop Criteria (MANDATORY)

- If `image_analysis.md` fails gate checks (missing / too short / meta preamble), rerun image analysis **once** with the strict output contract.
- If `video_synthesis.md` fails gate checks (missing / too short / meta preamble), rerun synthesis **once** with the strict output contract.
- If it still fails after one retry: mark the product as **analysis_incomplete** and **do not proceed** to script generation for that product.

---

## Prompt Templates

### Strict Output Contract (MANDATORY)

When generating analysis files, the model must output clean Markdown only. Add these constraints to every Gemini prompt:

- Output **ONLY** Markdown content (no preamble like “I will…” and no tool/system chatter)
- Do **not** claim you saved/wrote files
- Do **not** describe tool usage
- If uncertain, label uncertainty explicitly

### Image Analysis Prompt (Bilingual)

```
Analyze all product images in product_list/YYYYMMDD/{product_id}/product_images/

Create a BILINGUAL product analysis for TikTok script writing.

MANDATORY: Include inline Chinese translations throughout (not just headers).
- Every key bullet should include Chinese in parentheses: `English text (中文翻译)`

**OUTPUT FILE:** Save as product_list/YYYYMMDD/{product_id}/product_images/image_analysis.md

STRICT OUTPUT:
- Output ONLY Markdown (no preamble, no meta text)
- Do NOT mention tools/filesystem, do NOT say you saved files

**FORMAT:**
- Bilingual headers: ## Section | 中文标题
- Inline Chinese translations on the same line for key bullets: `English text (中文翻译)`
- 10+ sections, 200+ lines minimum

**REQUIRED SECTIONS:**
1. Product Design & Aesthetics | 产品设计与美学
2. Key Features | 核心功能
3. Size & Specifications | 尺寸与规格
4. Text & Labels (German) | 文字与标签
5. Quality Signals | 质量信号
6. Color/Variant Options | 颜色/变体选项
7. Key Differentiators | 关键差异化
8. Usage Context | 使用场景
9. Packaging | 包装展示
10. Visual Hooks for Scripts | 脚本视觉钩子

**CRITICAL - Section 10 Must Include:**
- 5+ specific visual hook ideas
- Filming instructions for each
- German hook lines for scripts
- Priority ranking for script angles
```

### Video Analysis Prompt (Per Video)

```
Analyze video: product_list/YYYYMMDD/{product_id}/ref_video/video_{video_num}_*.mp4

**OUTPUT FILE:** Save as product_list/YYYYMMDD/{product_id}/ref_video/video_{video_num}_analysis.md

**REQUIRED SECTIONS:**
1. Video Metadata (duration, creator, views)
2. Hook Analysis (first 3 seconds)
3. Voiceover/Dialogue Transcript (German + Chinese translation)
4. Visual Storyboard (shot-by-shot)
5. Key Selling Points (ranked)
6. Music/Audio Analysis
7. CTA Analysis
8. Target Audience Inference
9. Effectiveness Rating (1-10)
10. Replication Insights

**FORMAT:**
- Bilingual: German/English content with Chinese translations
- Specific timestamps for each section
- Actionable insights for script writers
```

### Video Synthesis Prompt (Market Summary)

```
Create a COMPREHENSIVE market synthesis from all video analyses in:
product_list/YYYYMMDD/{product_id}/ref_video/video_*_analysis.md

**OUTPUT FILE:** Save as product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md

STRICT OUTPUT:
- Output ONLY Markdown (no preamble, no meta text)
- Do NOT mention tools/filesystem, do NOT say you saved files

**REQUIRED SECTIONS (14 minimum):**
1. Executive Summary | 执行摘要
2. Common Winning Patterns | 共同获胜模式
   - Hook Types (ranked by effectiveness)
   - Visual Strategy
   - Key Selling Points (ranked by emphasis)
3. Duration Sweet Spot | 时长最佳点
4. Language & Voice Strategy | 语言与声音策略
5. Target Audience Profile | 目标受众画像
6. Creative Production Patterns | 创意制作模式
7. Seasonal Context | 季节性背景
8. Compliance & Trust Signals | 合规与信任信号
   - Price: avoid exact € in scripts (use relative wording)
   - Waterproof: only claim if IP rating sourced
   - Medical: avoid therapy/healing promises
   - Tech specs: avoid ambiguous claims (e.g. 4K decode vs native)
9. Competitive Differentiation | 竞争差异化
10. Replication Strategy | 复制策略
    - 3+ specific script angles with estimated effectiveness
11. Performance Predictions | 效果预测
12. Recommendations (DO's and DON'Ts) | 建议
13. Source Materials | 源材料

**CRITICAL - Depth Requirements:**

Section 2 (Winning Patterns) must include:
- **Hook Library Table** with 25+ patterns:
  | Pattern | German Example | When to Use | Risk Level |
  (Reference sample: video_synthesis.md contains 25+ concrete hook examples)

Section 5 (Creative Production) must include:
- **German Copy Bank** with 80+ production-ready lines:
  - Hooks (Problem/Attention) - 20 lines
  - Features & Benefits - 20 lines
  - CTAs - 20 lines
  - Objection Handling - 20 lines
  (Each with Chinese translation)

**Example quality benchmark from sample:**
1. Hör auf, überteuerte Smoothies zu kaufen! (Stop buying overpriced smoothies!)
2. Dein neuer bester Freund im Büro. (Your new best friend at the office.)
3. Das läppert sich, oder? (That adds up, doesn't it?)

**CRITICAL FORMAT - Bilingual Structure:**

⚠️ **MANDATORY Bilingual Format:**
- **Bilingual headers:** Section | 章节
- **Key points MUST use nested DE:/ZH: format:**
  ```markdown
  *   **Key Point Name:**
      *   DE: Full German explanation text here.
      *   ZH: Full Chinese translation here.
  ```
- **NEVER parenthetical:** Do NOT use `German text (中文翻译)` format
- **Tables in Hook Library:** Each cell must have `DE: ... ZH: ...` format

**Example CORRECT format:**
*   **The "Chaos Reality" Hook:**
    *   DE: Visual clutter creates tension. Filters target audience instantly.
    *   ZH: 视觉混乱制造紧张感。瞬间筛选目标受众。

**Example WRONG format (DO NOT USE):**
*   ❌ Visual clutter creates tension (视觉混乱制造紧张感)
*   ❌ German text (Chinese translation in parentheses)

**Minimum 150+ lines** with comprehensive bilingual coverage for all key insights.
```

### Post-Run Validation (Quick Sanity Checks)

After writing an analysis file, do not proceed if it contains meta chatter. Examples of invalid first lines:
- "I will…"
- "Loaded cached credentials…"

#### Automated Compliance Validation (RECOMMENDED)

Use the compliance validator to automatically check all generated content:

```bash
# Validate synthesis for properly flagged risks
python3 scripts/validate_compliance_flags.py product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md

# Validate all scripts (analysis phase should flag risks, scripts should have none)
for script in product_list/YYYYMMDD/{product_id}/scripts/*.md; do
  [[ "$(basename "$script")" == "Campaign_Summary.md" ]] && continue
  python3 scripts/validate_compliance_flags.py "$script"
done
```

#### Manual Compliance Scans (Optional)

For targeted checks, use these ripgrep commands:

```bash
scripts_dir="product_list/YYYYMMDD/{product_id}/scripts"
# Price bait patterns
rg -n "€|\\bEuro\\b|欧元|nur\\s+\\d|statt\\s+\\d" "$scripts_dir" --glob '!Campaign_Summary.md' || true
# Absolute claims
rg -n "100% wasserdicht|komplett wasserdicht|100%防水|完全防水|genauso\\s+gut|besser\\s+als|perfekt" "$scripts_dir" --glob '!Campaign_Summary.md' || true
# Medical claims
rg -n "Schmerz|Physio|Therapeut|Tiefengewebe|heilt|behandelt" "$scripts_dir" --glob '!Campaign_Summary.md' || true
# Exaggerated promotions
rg -n "unbezahlbar|genial|unglaublich|bevor\\s+es|letzte\\s+Chance" "$scripts_dir" --glob '!Campaign_Summary.md' || true
```

Use the repo verifier to enforce analysis-output formatting consistently:

```bash
bash scripts/verify_gate.sh --date YYYYMMDD --csv scripts/products.csv --phase analysis
```

---

## Batch Processing Example

**For 8 products with 5 videos each:**

```python
# Time comparison:
# Fully sequential: 8 products × (5 videos × 2min each) = 8 × 10min = 80min (videos alone)
# Pipeline approach: 8 products × (5 videos in parallel: 2min + image: 1min + synthesis: 1min) = 8 × 4min = 32min
# Speed improvement: 2.5x faster

# Process products sequentially with pipeline stages
completed_products = []
failed_products = []

for product_id in products:  # Sequential across products
    print(f"\n=== Product {product_id} ===")

    try:
        # Stage 1: Video analyses (5 tasks in parallel)
        print(f"Launching 5 video analyses...")
        video_tasks = []
        for i in range(1, 6):
            task = launch_video_analysis(product_id, i)
            video_tasks.append(task)

        # Wait for all 5 videos
        wait_for_all(video_tasks)
        print(f"✅ Videos analyzed")

        # Stage 2: Image analysis (1 task)
        if has_images(product_id):
            print(f"Analyzing images...")
            image_task = launch_image_analysis(product_id)
            wait_for_completion(image_task)
            print(f"✅ Images analyzed")

        # Stage 3: Synthesis (1 task)
        print(f"Creating synthesis...")
        synthesis_task = launch_synthesis(product_id)
        wait_for_completion(synthesis_task)
        print(f"✅ Synthesis complete")

        # Quality gate verification
        verify_analysis(product_id)
        completed_products.append(product_id)

    except Exception as e:
        print(f"❌ Failed: {e}")
        failed_products.append(product_id)
        continue  # Continue with next product

# Summary
print(f"\n=== BATCH COMPLETE ===")
print(f"Completed: {len(completed_products)}/{len(products)}")
if failed_products:
    print(f"Failed: {failed_products}")

# Now proceed to script generation (Claude Code)
print("\n✅ Ready for script generation phase")
```

---

## Handoff to Script Generator

**After Phase 1 completes, the following files exist:**

```
product_list/YYYYMMDD/{product_id}/
├── tabcut_data.json           # Product metadata (from scraper)
├── product_images/
│   ├── *.webp                 # Product images
│   └── image_analysis.md      # Gemini analysis (bilingual)
└── ref_video/
    ├── video_1_*.mp4          # Reference videos
    ├── video_1_analysis.md    # Per-video analysis
    ├── video_2_analysis.md
    ├── ...
    └── video_synthesis.md     # Market summary (CRITICAL)
```

**Script generator (Claude Code) will:**
1. Read these files (not regenerate them)
2. Extract key insights for scripts
3. Reference files in Campaign Summary (not duplicate content)

---

## Error Handling

**If analysis fails:**

1. **Retry once** with same prompt
2. **If retry fails:** Mark product as "analysis_incomplete"
3. **Continue with other products** (don't block batch)
4. **Report failures** at end for manual review

```python
# Error handling pattern
try:
    result = await check_task(task_id)
    if result.status == "failed":
        # Retry once
        retry_task = launch_retry(product_id, task_type)
        result = await check_task(retry_task)
        if result.status == "failed":
            failed_products.append(product_id)
            continue
except TimeoutError:
    failed_products.append(product_id)
    continue

# At end of batch
if failed_products:
    print(f"⚠️ Failed products: {failed_products}")
    print("Run manually or skip for now")
```

---

## Integration with Existing Skills

**This skill replaces image analysis from `tiktok_script_generator.md`**

**Workflow order:**
1. `tiktok_product_scraper.md` → Downloads product data + videos
2. `tiktok_product_analysis.md` → Analyzes images + videos (THIS SKILL)
3. `tiktok_script_generator.md` → Generates scripts using analysis files

---

**Version:** 1.0.0
**Last Updated:** 2026-01-01
