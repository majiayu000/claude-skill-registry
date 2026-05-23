---
name: tiktok-ad-analysis
description: AUTOMATIC video market analysis with hybrid transcription (TikTok captions → Whisper fallback). Auto-triggers when videos exist in ref_video/. Analyzes TikTok reference videos to extract hooks, strategies, and insights for script generation. OPTIMIZED for speed with parallel processing across products.
version: 4.4.0
author: Automated script (Python-based)
execution: Python script with FFmpeg + yt-dlp + Whisper + Gemini (AUTO-RUNS conditionally, PARALLELIZED across products)
orchestration: tiktok_product_analysis.md (for batch parallelism - 5 products max)
---

# TikTok Ad Analysis Skill (AUTOMATIC)

**WHAT THIS DOES:** Automatically analyzes TikTok reference videos with bilingual output (English + Chinese)
**WHEN IT RUNS:** AUTO-TRIGGERS after Step 1 (scraping) if `ref_video/` folder contains .mp4 files
**HOW IT WORKS:** Python script extracts frames + transcribes audio → Gemini generates analysis
**OUTPUT:** `video_N_analysis.md` for each video + `video_synthesis.md` summary (MANDATORY)

---

## Compliance & Policy Notes (DE Market)

This is an *analysis* skill, but it should proactively flag compliance-risk claims found in source videos so the script generator can avoid them.

- **Price / discount claims:** flag exact `€` amounts / “Euro” / “欧元”, hard discounts, and precise comparisons.
- **Waterproof claims:** flag absolutes like `"100% wasserdicht"`, `"komplett wasserdicht"`, `"完全防水"` unless an IP rating is visible in packaging.
- **Medical claims:** flag pain/therapy/healing language (e.g., `Schmerzfreiheit`, `Therapeut`, `Physio`, `heilt`).
- **Tech specs:** flag ambiguous claims like `"4K Support"` (often decode, not native).

When writing `video_synthesis.md`, include a small “Compliance & Trust Signals” section listing what to avoid in final scripts.

---

## Integration with Skill Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  SKILL PIPELINE                                             │
│                                                             │
│  1. tiktok_product_scraper.md → Downloads products + videos │
│                     │                                       │
│                     ▼                                       │
│  2. THIS SKILL (tiktok_ad_analysis.md)                      │
│     - Python scripts for frame extraction + transcription   │
│     - Gemini for per-video analysis                         │
│     - Output: video_N_analysis.md files                     │
│                     │                                       │
│                     ▼                                       │
│  3. tiktok_product_analysis.md (ORCHESTRATION)              │
│     - Parallel batch processing across products             │
│     - Image analysis (Gemini async MCP)                     │
│     - Video synthesis generation (Gemini async MCP)         │
│     - Output: video_synthesis.md, image_analysis.md         │
│                     │                                       │
│                     ▼                                       │
│  4. tiktok_script_generator.md                              │
│     - Script writing (Claude Code)                          │
│     - Campaign Summary (references analysis files)          │
│     - Output: Script_1/2/3.md, Campaign_Summary.md          │
└─────────────────────────────────────────────────────────────┘
```

**Agent Assignment:**
| Task | Agent | Tool |
|:-----|:------|:-----|
| Video frame extraction | Python (FFmpeg) | Local script |
| Audio transcription | Python (Whisper) | Local script |
| Per-video analysis | Gemini | gemini_cli_execute |
| Batch orchestration | Gemini | gemini_cli_execute_async |
| Video synthesis | Gemini | gemini_cli_execute_async |
| Script writing | Claude Code | Direct writing |

---

## Auto-Trigger Logic

**⚠️ CRITICAL:** This skill AUTO-RUNS conditionally. No manual invocation needed in normal workflow.

**Trigger Conditions:**
```bash
# After Step 1 (product scraping) completes:
date="YYYYMMDD"
base="product_list/$date/{product_id}"
if [ -d "$base/ref_video" ]; then
  video_count=$(find "$base/ref_video" -type f -name "*.mp4" 2>/dev/null | wc -l)
  if [ $video_count -gt 0 ]; then
    echo "✅ AUTO-TRIGGER: Found $video_count videos"
    # Automatically run video analysis
    python analyze_video_batch.py {product_id} --date "$date"
  else
    echo "⏭️ SKIP: No videos found"
  fi
else
  echo "⏭️ SKIP: No ref_video folder"
fi
```

**Manual Execution (if needed):**

```bash
# Navigate to scripts directory
cd scripts

# Activate virtual environment
source venv/bin/activate

# Single product (sequential)
python analyze_video_batch.py 1729479916562717270 --date YYYYMMDD

# PARALLEL EXECUTION (v4.4.0 - RECOMMENDED for multiple products)
# Launch up to 5 products simultaneously (Gemini CLI thread limit)

# Batch 1: 5 products in parallel
for pid in 1729671956792187076 1729480049905277853 1729637085247609526 1729697087571270361 1729630936525936882; do
  python analyze_video_batch.py $pid --date YYYYMMDD &
done
wait  # Wait for all 5 to complete

# Batch 2: Remaining products in parallel
for pid in 1729607303430380470 1729607478878640746 1729489298386491816; do
  python analyze_video_batch.py $pid --date YYYYMMDD &
done
wait

# Or analyze a single video
python analyze_single_video.py 1729479916562717270 2 --date YYYYMMDD
```

**Output:**
- `product_list/YYYYMMDD/{product_id}/ref_video/video_N_analysis.md` (bilingual, per video)
- `product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md` (MANDATORY market summary)

---

## Prerequisites

✅ **Python 3.8+** with virtual environment
✅ **ffmpeg** installed (for keyframe/audio extraction)
✅ **faster-whisper** installed (`pip install faster-whisper`)
✅ **yt-dlp** installed (`pip install yt-dlp`)
✅ **gemini-cli** installed and configured
✅ **Local video files** in `product_list/YYYYMMDD/{product_id}/ref_video/`
✅ **tabcut_data.json** available (contains performance metadata)

---

## Transcription Workflow (Hybrid Approach)

```
┌─────────────────────────────┐
│  1. TikTok Captions         │ ← Fastest (yt-dlp)
│     (direct download)        │
└──────────┬──────────────────┘
           │ Not available?
           ▼
┌─────────────────────────────┐
│  2. Whisper AI              │ ← Fallback (reliable)
│     (faster-whisper)         │
└──────────┬──────────────────┘
           │ Failed?
           ▼
┌─────────────────────────────┐
│  3. No transcript           │ ← Music/silent
│     (mark as unavailable)    │
└─────────────────────────────┘
```

**Benefits:**
- **Speed:** TikTok captions are instant when available
- **Accuracy:** Whisper handles videos without captions
- **Coverage:** Graceful fallback for music-only content

---

## Script Files

### `analyze_video_batch.py` - Batch Processing

**Usage:**
```bash
python analyze_video_batch.py <product_id>
```

**What it does:**
1. For each video in `ref_video/`:
   - FFmpeg extracts keyframes (every 3 seconds) + audio
   - Tries TikTok captions via yt-dlp (fast)
   - Falls back to Whisper transcription if needed
   - Passes frames + transcript to Gemini
   - Writes `video_N_analysis.md`

2. After all videos: Creates `video_synthesis.md` (market-level insights)

**Output files:**
```
product_list/YYYYMMDD/{product_id}/ref_video/
├── video_1_analysis.md    # Individual analysis (bilingual)
├── video_2_analysis.md
├── video_3_analysis.md
├── video_4_analysis.md
├── video_5_analysis.md
└── video_synthesis.md     # Market summary (all videos)
```

### `analyze_single_video.py` - Single Video

**Usage:**
```bash
python analyze_single_video.py <product_id> <video_number>
```

**Example:**
```bash
python analyze_single_video.py 1729479916562717270 2
```

**What it does:** Same workflow as batch, but for a single video

---

## Analysis Output Format

Each `video_N_analysis.md` contains:

### 1. Video Metadata | 视频元数据
- Creator, followers, rank, sales, views, duration

### 2. Voiceover/Dialogue Transcript | 旁白/对话文本
- **Language Detected:** German/English/Russian/etc.
- **Original Transcript:** With timestamps [MM:SS]
- **中文翻译:** Chinese translation line by line

---

## Chinese Translation Philosophy | 中文翻译哲学

**CRITICAL: Not literal word-for-word translation**

Translate for Chinese-speaking German residents, not Mainland China audience.

**Translation principles:**
- Use natural idioms, NOT literal word-for-word
- Expand if German idiom has no Chinese equivalent
- Match emotional tone (frustrated → 沮丧, amused → 好笑)
- Keep brand names and German terms original

**Examples from gold-standard sample scripts:**

| German | ❌ Literal Translation | ✅ Cultural Adaptation |
|:-------|:---------------------|:----------------------|
| "Gönn dir was Gutes" | "请自己享受好东西" (awkward) | "对自己好一点" (natural) |
| "Das läppert sich" | "那累积起来" (loses meaning) | "一个月下来可是一大笔" (captures impact) |
| "Ich bin mal skeptisch" | "我是怀疑的" (unnatural) | "我本来还挺怀疑" (conversational) |

**Quality indicators:**
- Sounds natural when read aloud in Chinese
- Preserves emotional arc and tone of original
- Uses appropriate register (casual vs. formal)
- Maintains cultural context of German market

---

### 3. Hook/Opening Strategy | 开场策略
- Hook Type (Problem-Solution, Pricing-FOMO, etc.)
- Hook Description
- Visual + Audio Combination
- Effectiveness Rating

### 4. Shot-by-Shot Storyboard | 分镜脚本
- Frame-by-frame analysis
- Visual action descriptions
- Voiceover alignment
- Shot purpose (Hook, Product Reveal, CTA, etc.)

### 5. Visual Elements Catalog | 视觉元素目录
- Graphics/Text Overlays
- Product Showcase
- Transitions
- Color Grading
- Lighting

### 6. Music/Audio Analysis | 音乐/音频分析
- Genre, Mood, Audio Quality
- Voice type (Human/TTS)
- Sync analysis

### 7. Key Selling Points | 核心卖点
- Feature emphasis with time allocation

### 8. Creative Strategy & Execution | 创意策略与执行
- Production Style (UGC/Professional)
- Germany Market Fit
- Authenticity Level
- Viral Elements

### 9. Call-to-Action Analysis | 行动号召分析
- CTA Type, Timing, Strength Rating

### 10. Target Audience Inference | 目标受众推断
- Demographics, Psychographics, Language Signals

### 11. Effectiveness Rating (7-Dimension) | 有效性评分
- Hook Strength, Pacing, Visual Quality, Trust Signals
- Value Clarity, CTA Effectiveness, Overall Score

### 12. Replication Insights | 复制要点
- Production Budget
- Equipment Needed
- Key Success Factor
- Reproduducible Elements

### 13. Recommendations (DO/DON'T/OPPORTUNITY) | 建议
- Specific actionable recommendations
- Mistakes to avoid
- Untapped opportunities

---

## Language Support

**Transcription supports:**
- German (de) - Primary market
- English (en)
- Russian (ru) - Diaspora targeting
- Spanish (es), French (fr), Japanese (ja), Korean (ko), Portuguese (pt)
- Chinese Simplified (zh-Hans), Chinese Traditional (zh-Hant)

**Auto-detection:** Both yt-dlp captions and Whisper auto-detect language

---

## Performance Notes

| Method | Speed | Accuracy | When Used |
|:-------|:------|:---------|:----------|
| TikTok captions (yt-dlp) | ~2-5s | High (creator's own) | When creator adds captions |
| Whisper transcription (tiny) | ~8-15s | High | When no captions available |
| No transcript | Instant | N/A | Music-only or unintelligible |

**Typical batch time (5 videos per product) - OPTIMIZED:**
- All have TikTok captions: ~20-30 seconds (was ~30s)
- All need Whisper: ~80-120 seconds (was ~4-5 minutes) **↓ 3-5x faster**
- Mixed: ~40-60 seconds (was ~1-2 minutes) **↓ 2-3x faster**

**Multi-product performance (v4.4.0 - PARALLELIZED):**
- **Sequential (old):** 8 products × 2 min = 16 min
- **Parallel (new):** Batch1(5 products) + Batch2(3 products) = 4 min ⭐ **4x faster**
- **Key:** Launch up to 5 products in parallel using bash background jobs (`&` + `wait`)

**Optimization Highlights (v4.4.0):**
- ✅ **CROSS-PRODUCT PARALLELISM:** Up to 5 products simultaneously (Gemini CLI limit)
- ✅ Whisper model caching (load once per batch, not per video)
- ✅ Parallel frame/audio extraction (ThreadPoolExecutor, 5 workers)
- ✅ Async Gemini analysis (max 5 concurrent API calls per product)
- ✅ Optimized FFmpeg (640px frames, lower quality, sufficient for analysis)
- ✅ Tiny Whisper model (4x faster than base, minimal accuracy loss)
- ✅ 3-phase pipeline architecture (extract → transcribe → analyze)

---

## Error Handling

### No TikTok captions available
```
  ├─ Fetching captions from TikTok (yt-dlp)...
  ├─ No captions found on TikTok
  ├─ Falling back to Whisper transcription...
```

### Whisper transcription succeeds
```
  ├─ Transcribing audio with faster-whisper...
  ├─ Detected language: de (confidence: 1.00)
  ├─ Transcript length: 9 segments
  └─ Transcript: whisper_transcription - de with 9 segments
```

### Both methods fail
```
  ├─ No transcript available - marking as music/silent
  └─ Transcript: none - unknown with 0 segments
```

---

## Installation

```bash
# Create virtual environment
cd scripts
python3 -m venv venv

# Activate
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install faster-whisper yt-dlp

# Verify ffmpeg is installed
ffmpeg -version

# Verify yt-dlp works
yt-dlp --version

# Test Whisper
python -c "from faster_whisper import WhisperModel; print('OK')"
```

---

## Configuration

### Whisper Model Options

Edit `analyze_single_video.py` or `analyze_video_batch.py`:

```python
# Current (fast, good accuracy) - OPTIMIZED v4.3.0
model = WhisperModel("tiny", device="cpu", compute_type="int8")
# With caching: model loads once per batch, not per video

# For better accuracy (slower)
model = WhisperModel("small", device="cpu", compute_type="int8")

# For best accuracy (slowest)
model = WhisperModel("medium", device="cpu", compute_type="int8")
```

**Note:** The batch script uses a singleton pattern to cache the model across all videos in a batch, eliminating redundant model loading overhead.

### yt-dlp Language Priority

Current priority order:
```python
"--sub-lang", "en,de,ru,es,fr,ja,ko,pt,zh-Hans,zh-Hant"
```

Add/remove languages as needed for your market.

---

## Troubleshooting

### Issue: yt-dlp can't access TikTok

**Error:** `HTTP Error 429: Too Many Requests`

**Solution:** TikTok rate limiting - wait a few minutes and retry, or rely on Whisper fallback

### Issue: Whisper slow transcription

**Solution:** Use smaller model (`base` instead of `small`/`medium`)

### Issue: Gemini quota exhausted

**Error:** `API Error: You have exhausted your capacity`

**Solution:** Wait for quota reset (~4-6 hours) or switch Google account

### Issue: No audio in transcript

**Check:**
```bash
# Verify audio file was extracted
ls -lh product_list/YYYYMMDD/{product_id}/ref_video/video_N_analysis_temp/audio.mp3

# Play audio to verify
ffplay product_list/YYYYMMDD/{product_id}/ref_video/video_N_analysis_temp/audio.mp3
```

---

## File Structure After Analysis

```
product_list/YYYYMMDD/{product_id}/
├── tabcut_data.json           # Source metadata
├── ref_video/
│   ├── video_1_{creator}.mp4
│   ├── video_1_analysis_temp/  # Temp (can be deleted)
│   │   ├── frames/            # Extracted keyframes
│   │   │   ├── frame_001.jpg
│   │   │   ├── frame_002.jpg
│   │   │   └── ...
│   │   └── audio.mp3          # Extracted audio
│   ├── video_1_analysis.md    # ← Generated analysis
│   ├── video_2_{creator}.mp4
│   ├── video_2_analysis_temp/
│   ├── video_2_analysis.md
│   └── ...
└── script/                    # Scripts use analysis (new workflow)
    ├── Product_Model_Angle1.md
    ├── Product_Model_Angle2.md
    └── Product_Model_Angle3.md
```

**Cleanup:** `*_analysis_temp/` directories can be deleted after successful analysis

---

## Next Step: Script Generation

After video analysis is complete:

1. **Check the analyses:**
   ```bash
   ls -lh product_list/YYYYMMDD/{product_id}/ref_video/video_*_analysis.md
   ```

2. **Verify bilingual format:**
   - Check section headers have `English | 中文`
   - Check transcripts have Chinese translations

3. **Run script generation:**
   - Use `tiktok_script_generator.md` skill
   - Claude will read `video_*_analysis.md` files
   - Generate 3 production-ready scripts

**Workflow:**
```
[Hybrid Analysis] → video_N_analysis.md (bilingual)
                        ↓
            [Script Generator Skill] → 3 Scripts (German + Chinese)
```

---

## Version History

**v4.4.0** (2026-01-18) - **CROSS-PRODUCT PARALLELISM**
- **MAJOR IMPROVEMENT:** 4x faster multi-product processing via parallel execution
- **NEW:** Support for up to 5 products running simultaneously (Gemini CLI thread limit)
- **NEW:** Bash background job orchestration (`&` + `wait` for batching)
- **PERFORMANCE:** 8 products: ~4 min (was 16 min) ⭐ **4x faster**
- **EXECUTION:** Batch1(5 products in parallel) + Batch2(3 products in parallel)
- **WHY:** User feedback - can parallelize across products, not just within products
- **COMPATIBILITY:** Fully backward compatible with single-product execution

**v4.3.0** (2026-01-07) - **PERFORMANCE OPTIMIZATION**
- **MAJOR IMPROVEMENT:** 3-5x faster batch processing through parallelization
- **NEW:** Whisper model caching (singleton pattern - load once per batch)
- **NEW:** Parallel frame/audio extraction (ThreadPoolExecutor, 5 workers)
- **NEW:** Async Gemini analysis (max 5 concurrent API calls with semaphore)
- **NEW:** 3-phase pipeline architecture (extract → transcribe → analyze)
- **OPTIMIZED:** FFmpeg frame extraction (640px, q:v 8 - smaller, faster, sufficient quality)
- **OPTIMIZED:** Whisper params (tiny model, beam_size=1, no word_timestamps)
- **OPTIMIZED:** Graceful error handling (continue on failure, report at end)
- **PERFORMANCE:** 5-video batch: ~80-120s (was ~4-5 min) when using Whisper
- **PERFORMANCE:** 5-video batch: ~20-30s (was ~30s) when using TikTok captions
- **WHY:** User feedback on slow video analysis due to sequential processing

**v4.1.0** (2026-01-01) - **AUTOMATIC EXECUTION**
- **MAJOR CHANGE:** Skill now AUTO-RUNS conditionally (no longer manual/optional)
- **Auto-trigger logic:** Checks if `ref_video/` has .mp4 files after Step 1 → runs automatically
- **Updated description:** Changed from "Automated" to "AUTOMATIC" (clarifies it's conditional, not manual)
- **Added trigger conditions:** Documented when skill runs vs when it skips
- **Output requirement:** `video_synthesis.md` is now MANDATORY (not optional)
- **Why this matters:** Ensures video analysis never gets skipped when videos exist
- **Integration:** Part of automated workflow, not a standalone manual tool

**v4.0.0** (2025-12-29)
- **NEW:** Hybrid transcription workflow (TikTok captions → Whisper fallback)
- **NEW:** Bilingual output format (English + Chinese)
- **NEW:** Language detection and confidence scores
- **NEW:** Graceful handling of music-only content
- **Improved:** Python-based automated processing
- **Removed:** Manual gemini-cli prompts (now automated)

**v3.0.0** (Previous)
- Manual gemini-cli usage by user

**v2.0.0** (Previous)
- Four-tier system (failed due to MCP limitations)
