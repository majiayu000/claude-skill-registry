---
name: tiktok-targeted-analysis
description: Analyzes user-provided TikTok URLs to generate comprehensive video breakdowns, 1 replication script (100% structure copy), and AI video generation prompts for Veo 3.1/Sora in copy-paste ready markdown code blocks
version: 1.0.0
author: Claude Code
execution: Python scripts + gemini-cli + Claude
orchestration: Phases 1-3 use Gemini, Phases 4-5 use Gemini
output: targeted_analysis/YYYYMMDD/{video_id}/
---

# TikTok Targeted Video Analysis Skill

**PURPOSE:** Deep analysis of competitor/inspiration TikTok videos for exact structural replication

**KEY DISTINCTION:** Unlike the product-based workflow (scrape → top 5 videos → 3 different scripts), this skill analyzes specific user-provided URLs to generate 1 exact replica script with AI-ready video generation prompts.

---

## What This Skill Does

### Input
- **CSV file** with TikTok URLs or **single URL** via command line
- CSV columns: `url`, `product_name`, `campaign_id` (optional)

### Output (per video)
```
targeted_analysis/YYYYMMDD/{video_id}/
├── metadata.json                 # Creator, views, likes, duration
├── video.mp4                     # Downloaded video
├── frames/ (every 2s)            # Keyframes for analysis
├── audio.mp3                     # Extracted audio
├── transcript.json               # Hybrid transcription
├── analysis.md                   # Combined 3-part analysis
├── character_descriptions.md     # Detailed casting guide
├── replication_script.md         # Obsidian-ready script
├── ai_video_prompts.md           # Shot-by-shot Veo/Sora prompts
├── processing_status.json        # Phase completion tracking
└── analysis.log                  # Debug log
```

---

## 5-Phase Pipeline

### Phase 1: Metadata Extraction
- Extract video ID from URL (regex + yt-dlp fallback)
- Fetch metadata: creator, views, likes, duration, title
- Download video file with yt-dlp
- **Output:** `metadata.json`, `video.mp4`

### Phase 2: Frame + Audio Extraction + Transcription
- FFmpeg: Extract keyframes every **2 seconds** (vs 3s in product workflow)
- FFmpeg: Extract audio track
- **Hybrid transcription:** TikTok captions → Whisper fallback → None
- **Output:** `frames/`, `audio.mp3`, `transcript.json`

### Phase 3: Comprehensive Analysis (4 Sub-Phases)

#### 3A: Structural Analysis
- Shot-by-shot storyboard with timestamps
- Camera specs: Close-up/Medium/Wide, Static/Pan/Handheld
- Transition analysis (cuts, dissolves)
- Text overlays catalog
- Visual composition (framing, lighting, color grading)

#### 3B: Content Analysis
- Hook dissection (first 3 seconds, matches to 8 core patterns)
- Voiceover with emotion markers
- Music/audio strategy
- Product embedding timeline

#### 3C: Strategic Analysis
- Target audience (demographics + psychographics)
- Psychological triggers (FOMO, social proof, authority)
- Germany market fit score
- Replication blueprint (copy/adapt/avoid)
- Production requirements (budget, equipment, talent)

#### 3D: Character Descriptions
- Physical appearance (age, gender, hair, build)
- Clothing details
- Body language and gestures
- Vocal characteristics
- Casting notes

**Output:** `analysis.md` (combined), `character_descriptions.md`

### Phase 4: Replication Script Generation
- 100% structure/hook/timing copy
- Slightly varied dialogue (same meaning, different words)
- YAML frontmatter (Obsidian-ready)
- German VO + Chinese translation (mandatory)
- ElevenLabs v3 tone markers
- Visual strategy table
- **Output:** `replication_script.md`

### Phase 5: AI Video Prompts Generation
- Shot-by-shot prompts in markdown code blocks
- Format: ```veo-prompt for Obsidian copy-paste
- Each prompt includes: camera, subject, lighting, audio cues
- **Output:** `ai_video_prompts.md`

---

## Usage

### Prerequisites

```bash
# Ensure you're at repo root
cd /Users/lxt/Movies/TikTok/WZ/lukas_9688

# Virtual environment with dependencies
cd scripts
source venv/bin/activate

# Required tools
which yt-dlp    # Video downloading
which ffmpeg    # Frame/audio extraction
which gemini    # Analysis
python -c "from faster_whisper import WhisperModel" # Transcription
```

### Single Video Analysis

```bash
python scripts/analyze_targeted_video.py \
  --url "https://www.tiktok.com/@username/video/1234567890" \
  --product-name "Your Product Name" \
  --output-dir "targeted_analysis/20260114"
```

**Time:** ~5-10 minutes per video
**Cost:** ~$0.30-0.60 (Gemini API)

### Batch Processing

**1. Create CSV file:**

```csv
url,product_name,campaign_id
https://www.tiktok.com/@user1/video/111,Product A,winter_2026
https://www.tiktok.com/@user2/video/222,Product B,
https://www.tiktok.com/@user3/video/333,Product C,spring_2026
```

**2. Run batch:**

```bash
python scripts/analyze_targeted_batch.py \
  --csv targeted_videos.csv \
  --output-dir "targeted_analysis/20260114" \
  --max-workers 3
```

**Time:** 10 videos ÷ 3 workers × 8 min ≈ 27 minutes
**Cost:** ~$3-6 for 10 videos

### Skip Phases (Resume from Checkpoint)

If a phase fails or you want to regenerate later phases:

```bash
python scripts/analyze_targeted_video.py \
  --url "..." \
  --product-name "..." \
  --output-dir "..." \
  --skip-phases "1,2"  # Skip metadata and extraction, use existing data
```

Useful for:
- Regenerating scripts without re-analyzing
- Testing prompts without re-downloading

---

## Quality Gates

### Phase 1 Success
- ✅ `metadata.json` exists with creator, views, duration
- ✅ `video.mp4` exists (size > 100KB)

### Phase 2 Success
- ✅ Frame count = (duration / 2) ±1
- ✅ `audio.mp3` exists OR marked "silent"
- ✅ `transcript.json` exists (source: tiktok_captions, whisper_transcription, or none)

### Phase 3 Success
- ✅ `analysis.md` has all 3 parts (structural, content, strategic)
- ✅ Shot table has ≥ (frame_count / 2) shots
- ✅ Hook analysis references Tiktok_Golden_3_seconds.md patterns
- ✅ `character_descriptions.md` has ≥ 1 character
- ✅ No meta-text pollution ("I will...", "Loaded credentials...")
- ✅ Minimum 1500 lines combined

### Phase 4 Success
- ✅ `replication_script.md` has valid YAML frontmatter
- ✅ Contains: Structure, Visual Strategy, German VO, Chinese translation
- ✅ Duration matches original ±5s

### Phase 5 Success
- ✅ One ```veo-prompt per shot
- ✅ Each block has: camera, subject, lighting, audio
- ✅ No generic prompts

---

## Integration with Existing Workflow

**Comparison:**

| Aspect | Product Workflow | Targeted Analysis (NEW) |
|:-------|:----------------|:------------------------|
| **Input** | Product ID (scraper) | TikTok URL (user-provided) |
| **Videos** | Top 5 performing | Specific competitor video |
| **Analysis** | Market synthesis | Deep single-video replication |
| **Scripts** | 3 different angles | 1 exact replica (100% structure) |
| **Output** | `product_list/YYYYMMDD/{product_id}/` | `targeted_analysis/YYYYMMDD/{video_id}/` |
| **Use Case** | New product launch | Clone proven video |

**No conflicts** - separate directories and workflows.

---

## Key Technical Decisions

### 1. Frame Interval: 2s vs 3s
**Why 2s:** TikTok videos are short (30-60s). More frames = better shot detection for precise replication. Trade-off: +50% cost (~$0.10 more) but critical for accuracy.

### 2. Three-Phase Gemini Analysis
**Why separate:** Focused prompts (structural → content → strategic) produce better results than one mega-prompt.

### 3. AI Prompt Format
**Why code blocks:** User requested copy-paste functionality in Obsidian. Visual separation, easy to copy entire block for Veo/Sora.

### 4. Character Descriptions Separation
**Why separate file:** Too detailed for main analysis, critical for casting. Enables precise replication.

### 5. 1 Script (not 3)
**Why:** User requirement - 100% exact structure replication for same product, slightly varied dialogue only.

---

## Error Handling

### Download Failures
- **Symptom:** `yt-dlp` timeout or rate limit
- **Solution:** Uses `--cookies-from-browser chrome` flag, 3 retries with exponential backoff
- **Fallback:** Manual download (provide local file path)

### Transcription Failures
- **Symptom:** No TikTok captions + Whisper fails
- **Solution:** Graceful fallback to `source: none` (music-only video)
- **Impact:** Analysis still proceeds with visual-only context

### Gemini Capacity Errors
- **Symptom:** "You have exhausted your capacity"
- **Solution:** Automatic fallback to `gemini-3-flash-preview`
- **Retry:** Uses exponential backoff

### Character Detection Issues
- **Symptom:** Gemini misses subtle casting details
- **Solution:** Export character reference frames to `frames/characters/`
- **Manual review:** Human can refine descriptions post-analysis

---

## Performance & Costs

### Single Video
| Phase | Time | Cost |
|:------|:-----|:-----|
| 1: Metadata | 15-40s | Free |
| 2: Extraction | 17-45s | Free |
| 3A: Structural | 60-120s | ~$0.10 |
| 3B: Content | 60-120s | ~$0.10 |
| 3C: Strategic | 60-120s | ~$0.05 |
| 3D: Character | 30-60s | ~$0.05 |
| 4: Script | 30-60s | ~$0.05 |
| 5: AI Prompts | 20-40s | ~$0.05 |
| **TOTAL** | **5-10 min** | **~$0.40** |

### Batch (10 videos, 3 concurrent)
- **Time:** ~27 minutes
- **Cost:** ~$4.00

---

## Common Issues & Solutions

### Issue: "Invalid TikTok URL format"
**Cause:** Unsupported URL structure
**Solution:** Ensure URL format matches:
- `https://www.tiktok.com/@user/video/123456`
- `https://vm.tiktok.com/ABCDEF` (short URL)

### Issue: "No frames found"
**Cause:** FFmpeg extraction failed
**Solution:** Check video file integrity, ensure ffmpeg installed

### Issue: "Replication script missing frontmatter"
**Cause:** Gemini output formatting issue
**Solution:** Re-run Phase 4 with `--skip-phases 1,2,3`

### Issue: "Analysis too generic"
**Cause:** Insufficient frame granularity
**Solution:** Default 2s interval should be sufficient; check frame count matches (duration / 2) ±1

---

## Copyright & Legal Considerations

⚠️ **IMPORTANT DISCLAIMER:**

This skill generates **replication scripts** based on competitor videos. Key points:

1. **100% structure copy + varied dialogue** is a legal gray area
2. **User is responsible** for final usage and copyright compliance
3. **Recommendation:** Use as "inspiration" not "copy"
4. **High-risk videos:** Viral/professional productions may be closely monitored
5. **Best practice:** Significant dialogue variation + unique visual styling

**Generated `replication_script.md` includes prominent disclaimer.**

---

## File Structure After Completion

```
targeted_analysis/
└── 20260114/                         # Batch date
    ├── 1234567890/                   # Video ID 1
    │   ├── metadata.json
    │   ├── video.mp4
    │   ├── frames/
    │   │   ├── frame_001.jpg
    │   │   ├── frame_002.jpg
    │   │   └── ...
    │   ├── audio.mp3
    │   ├── transcript.json
    │   ├── analysis.md               # Combined 3-part analysis
    │   ├── character_descriptions.md
    │   ├── replication_script.md     # Obsidian-ready
    │   ├── ai_video_prompts.md       # Copy-paste ready
    │   ├── processing_status.json
    │   └── analysis.log
    ├── 2345678901/                   # Video ID 2
    │   └── ...
    └── 3456789012/                   # Video ID 3
        └── ...
```

---

## Next Steps After Analysis

1. **Review Analysis:** Read `analysis.md` to understand video strategy
2. **Check Character Casting:** Use `character_descriptions.md` for talent selection
3. **Adapt Script:** Review `replication_script.md`, adjust dialogue as needed
4. **Generate Video:** Copy prompts from `ai_video_prompts.md` to Veo 3.1/Sora
5. **Quality Check:** Ensure generated shots match analysis specifications
6. **Final Assembly:** Edit shots together, add VO, music, text overlays

---

## Version History

**v1.0.0** (2026-01-14)
- Initial release
- 5-phase pipeline (metadata → extraction → analysis → script → prompts)
- 2-second frame intervals for precise shot detection
- Hybrid transcription (TikTok → Whisper → None)
- 4-part analysis (structural, content, strategic, character)
- 1 exact replica script with varied dialogue
- AI video prompts in markdown code blocks
- Batch processing with 3 concurrent workers
- Comprehensive error handling and fallbacks

---

**Generated by:** Claude Code
**Repository:** /Users/lxt/Movies/TikTok/WZ/lukas_9688
**Related Skills:** tiktok_product_scraper.md, tiktok_ad_analysis.md, tiktok_script_generator.md
