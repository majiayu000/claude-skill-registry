---
name: video-delivery-coach
description: "Analyze YOUR video recordings before publishing. Evaluates voice (pace, pitch, volume), facial expressions (emotions, eye contact, smiles), and content (filler words, structure). Helps improve your Hinglish YouTube delivery over time."
---
# Video Delivery Coach

**Get better at video, video by video.** This skill analyzes your recordings before you publish, identifying areas for improvement.

---

## WHAT IT DOES

| Analysis Type | Metrics | Tool Used |
|---------------|---------|-----------|
| **Voice** | Speech rate (WPM), pitch variation, volume consistency | Librosa + Whisper |
| **Facial** | Emotion timeline, eye contact frequency, smile frequency | OpenCV + DeepFace + Mediapipe |
| **Content** | Transcription, filler words, structure | Faster-Whisper + Claude |
| **Overall** | 5-dimension score (1-5 each, max 25) | Claude analysis |

---

## SCORING RUBRIC

| Dimension | Score 1 | Score 5 |
|-----------|---------|---------|
| **Content & Organization** | Disorganized, unclear | Logical, well-structured |
| **Delivery & Vocal Quality** | Monotone, many fillers | Clear, varied, engaging |
| **Body Language & Eye Contact** | No eye contact, stiff | Direct gaze, natural movement |
| **Audience Engagement** | Boring, loses attention | Captivating, maintains interest |
| **Language & Clarity** | Grammar issues, unclear | Clear, impactful, professional |

**Total Score Interpretation:**
- 5-9: Needs significant improvement
- 10-14: Developing skills
- 15-18: Competent speaker
- 19-22: Proficient speaker
- 23-25: Outstanding speaker

---

## TRIGGERS

Use this skill when you say:
- "Analyze my video recording"
- "How was my delivery?"
- "Review my video before upload"
- "Check my presentation"
- "Coach my speaking"

---

## USAGE

### In Claude Code (Recommended)

```
"Analyze my video at /path/to/recording.mp4"

"Coach my delivery on the latest YouTube recording"

"What can I improve in this video?"
```

### CLI Mode

```bash
# Basic analysis
python scripts/analyze_video.py --video "/path/to/video.mp4"

# Full analysis with all features
python scripts/analyze_video.py --video "/path/to/video.mp4" --full

# Voice only (faster)
python scripts/analyze_video.py --video "/path/to/video.mp4" --voice-only

# Save report
python scripts/analyze_video.py --video "/path/to/video.mp4" --output ~/reports/
```

---

## OUTPUT FORMAT

### Quick Summary
```
┌────────────────────────────────────────┐
│     VIDEO DELIVERY ANALYSIS            │
│     recording_2025_01_15.mp4           │
├────────────────────────────────────────┤
│  OVERALL SCORE: 18/25 (Competent)      │
│                                        │
│  Content & Organization:    4/5        │
│  Delivery & Vocal Quality:  3/5        │
│  Body Language & Eye Contact: 4/5      │
│  Audience Engagement:       4/5        │
│  Language & Clarity:        3/5        │
└────────────────────────────────────────┘
```

### Detailed Report
```markdown
# Video Delivery Analysis

**File:** recording_2025_01_15.mp4
**Duration:** 12:34
**Date:** 2025-01-15

---

## VOICE ANALYSIS

| Metric | Value | Target | Assessment |
|--------|-------|--------|------------|
| Speech Rate | 145 WPM | 120-160 | ✅ Good |
| Pitch Variation | 42.3 Hz | >30 Hz | ✅ Engaging |
| Volume Consistency | 0.08 | <0.15 | ✅ Steady |

**Filler Words Detected:**
- "um" - 8 times
- "you know" - 5 times
- "basically" - 3 times

**Recommendation:** Reduce "um" usage. Try pausing instead.

---

## FACIAL ANALYSIS

| Metric | Value | Assessment |
|--------|-------|------------|
| Eye Contact Frequency | 72% | ✅ Good |
| Smile Frequency | 35% | ⚠️ Could increase |

**Emotion Timeline:**
- 0:00-2:00: Neutral (intro)
- 2:00-8:00: Happy/Engaged (main content)
- 8:00-10:00: Serious (data presentation)
- 10:00-12:34: Happy (conclusion)

**Recommendation:** More smiles during technical sections.

---

## CONTENT ANALYSIS

**Strengths:**
- Clear opening hook
- Good use of clinical examples
- Strong call-to-action

**Areas for Improvement:**
- Could use more pauses after key points
- Consider adding more Hinglish transitions
- Section on side effects could be more structured

---

## OVERALL FEEDBACK

**What You Did Well:**
1. Excellent pace - not too fast, not too slow
2. Good eye contact with camera
3. Clinical examples were relatable

**What to Improve:**
1. Reduce filler words (especially "um")
2. Add more smiles during technical explanations
3. Pause after key statistics for emphasis

**Score: 18/25 - Competent Speaker**
You're delivering solid content with room for refinement.
```

---

## HINGLISH-SPECIFIC ANALYSIS

This skill is calibrated for Hinglish content:

| Feature | What It Checks |
|---------|----------------|
| Code-switching | Natural Hindi ↔ English transitions |
| Pace adjustment | Slower for English technical terms |
| Cultural markers | Use of "ji", "beta", "aapko bata doon" |
| Engagement phrases | "Dekho", "Suniye", "Samjhe?" |

---

## COMPARING OVER TIME

Track your improvement across recordings:

```
┌─────────────────────────────────────────────────────┐
│  PROGRESS TRACKER (Last 5 Videos)                   │
├─────────────────────────────────────────────────────┤
│  Video           │ Score │ Main Improvement         │
│  ─────────────────────────────────────────────────  │
│  Jan 10          │ 15/25 │ Baseline                 │
│  Jan 15          │ 18/25 │ Better eye contact       │
│  Jan 20          │ 17/25 │ Fewer filler words       │
│  Jan 25          │ 19/25 │ More varied pace         │
│  Jan 30          │ 21/25 │ Natural Hinglish flow    │
└─────────────────────────────────────────────────────┘
```

---

## INTEGRATION

### With Your Workflow
```
Record Video → Analyze with video-delivery-coach → Fix issues → Re-record (optional) → Publish
```

### Feeds Into:
- `youtube-script-master` - Script adjustments based on delivery feedback
- Personal improvement tracking

---

## DEPENDENCIES

```bash
# Core (required)
pip install anthropic python-dotenv rich

# Voice analysis
pip install librosa moviepy faster-whisper

# Facial analysis (optional - for full analysis)
pip install opencv-python mediapipe deepface tf-keras

# Note: tf-keras is heavy (~500MB). Skip for voice-only mode.
```

---

## API KEYS NEEDED

| Key | Purpose | Status |
|-----|---------|--------|
| ANTHROPIC_API_KEY | Final analysis and coaching | Already have |

---

## MODES

### Voice-Only Mode (Lightweight)
```bash
python scripts/analyze_video.py --video file.mp4 --voice-only
```
- Requires: librosa, moviepy, faster-whisper
- Analyzes: Speech rate, pitch, volume, transcription, filler words
- Skip: Facial analysis (faster, lighter)

### Full Mode (Comprehensive)
```bash
python scripts/analyze_video.py --video file.mp4 --full
```
- Requires: All dependencies including OpenCV, DeepFace, Mediapipe
- Analyzes: Everything including facial expressions
- Slower but complete

---

## HOW CLAUDE SHOULD USE THIS SKILL

When user asks to analyze a video:

### Step 1: Check if video file exists
```python
import os
if not os.path.exists(video_path):
    print("Video file not found")
    return
```

### Step 2: Run analysis
```bash
python scripts/analyze_video.py --video "/path/to/video.mp4"
```

### Step 3: Present results
- Show quick summary first
- Offer detailed breakdown if requested
- Provide actionable recommendations

### Step 4: Track progress
- Compare with previous analyses
- Note improvements
- Identify persistent issues

---

## SAMPLE OUTPUT

```
=== VIDEO DELIVERY ANALYSIS ===
File: hinglish_statin_video.mp4
Duration: 15:23

VOICE METRICS:
├── Speech Rate: 138 WPM (Target: 120-160) ✅
├── Pitch Variation: 38.5 Hz ✅ Natural variation
└── Volume: Consistent ✅

FILLER WORDS:
├── "um": 12 occurrences
├── "basically": 8 occurrences
└── "you know": 5 occurrences

FACIAL METRICS:
├── Eye Contact: 68% ✅ Good
├── Smiles: 28% ⚠️ Below target (40%)
└── Dominant Emotion: Engaged

CONTENT SCORE:
├── Content & Organization: 4/5
├── Delivery & Vocal Quality: 3/5
├── Body Language: 4/5
├── Engagement: 4/5
└── Language & Clarity: 4/5

TOTAL: 19/25 (Proficient Speaker)

TOP 3 IMPROVEMENTS:
1. Replace "um" with pauses
2. Smile more during technical explanations
3. Slow down slightly when explaining statistics

HINGLISH NOTES:
✅ Natural code-switching
✅ Good use of "aapko batata hoon"
⚠️ Consider more "samjhe?" checks for engagement
```

---

## NOTES

- **Privacy**: All analysis is local, video never uploaded anywhere
- **Speed**: Voice-only takes ~1 min, full analysis takes ~3-5 min
- **File types**: Supports MP4, MOV, AVI, MKV
- **Duration**: Works best with 5-30 minute videos

---

*This skill helps you improve your delivery over time - not by judging, but by giving you objective data to work with.*
