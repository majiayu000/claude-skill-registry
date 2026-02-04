---
name: hf-papers-to-video
description: Transform Hugging Face Daily Papers into professional video summaries with AI-generated narration, synchronized visuals, and smooth animations. Fully automated pipeline from paper extraction to final video export.
metadata:
  tags: video, huggingface, papers, remotion, tts, automation, content-creation
  author: clawd
  version: 1.0.0
---

# HF Papers to Video Generator

Transform Hugging Face Daily Papers into professional, shareable video summaries with synchronized narration and smooth animations.

## ✨ Features

- 📄 **Automatic Paper Extraction** - Scrape HF Daily Papers, download PDFs, extract abstracts and key insights
- 🖼️ **Smart Image Filtering** - AI-powered filtering to remove icons/headers and keep only relevant figures
- 🎙️ **Natural TTS Narration** - Professional voice synthesis using Doubao/Volcano TTS
- 🎬 **Remotion Rendering** - React-based video composition with smooth animations
- 📐 **Audio-Visual Sync** - Dynamic duration calculation based on audio length
- 📦 **Optimized Export** - Automatic compression for Telegram/Discord/Social Media

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HF PAPERS VIDEO PIPELINE                 │
├─────────────────────────────────────────────────────────────┤
│  Extract → Script → TTS → Render → Export                  │
│   (PDF)    (JSON)  (MP3)  (MP4)   (Compressed)             │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

### System Dependencies
```bash
# macOS
brew install ffmpeg node python3

# Node.js packages
npm install -g @remotion/cli remotion

# Python packages
pip install PyMuPDF Pillow beautifulsoup4 requests
```

### Environment Variables
```bash
# Doubao/Volcano TTS (required for narration)
export VOLCANO_TTS_APPID="your_app_id"
export VOLCANO_TTS_ACCESS_TOKEN="your_access_token"
export VOLCANO_TTS_SECRET_KEY="your_secret_key"
```

## 🚀 Quick Start

### 1. Extract Papers
```bash
cd skills/hf-papers-to-video
python scripts/extract_papers.py --date 2026-02-01 --limit 10
```

### 2. Filter Images
```bash
python scripts/filter_images.py --min-width 150 --min-height 100
```

### 3. Generate Script
```bash
python scripts/generate_script.py --style news-briefing
```

### 4. Create Audio
```bash
python scripts/generate_tts.py --voice zh_male_jieshuoxiaoming_moon_bigtts
```

### 5. Render Video
```bash
npm run render
```

### 6. Export
```bash
ffmpeg -i output/final.mp4 -b:v 600k -b:a 80k output/video.mp4
```

## 📁 Project Structure

```
hf-papers-to-video/
├── scripts/
│   ├── extract_papers.py      # PDF download & text extraction
│   ├── filter_images.py       # Smart image filtering
│   ├── generate_script.py     # Script generation
│   ├── generate_tts.py        # TTS audio generation
│   └── render.sh              # Render pipeline
├── src/
│   ├── components/
│   │   ├── ImageCard.tsx      # Animated image component
│   │   ├── Typography.tsx     # Text components
│   │   └── Animations.tsx     # Animation utilities
│   ├── scenes/
│   │   └── SceneTemplate.tsx  # Scene renderer
│   └── index.tsx              # Composition registry
├── scenes.json                # Scene configuration
├── audio-durations.json       # Audio sync data
└── output/                    # Generated videos
```

## ⚙️ Configuration

### Scene Types

#### Hero Scene (Intro/Outro)
```json
{
  "id": "intro",
  "variant": "hero",
  "layout": {
    "imageLayout": "background",
    "imageAnimation": "zoom"
  },
  "title": "AI Research Daily",
  "subtitle": "Latest breakthroughs in ML"
}
```

#### Content Scene (Paper Showcase)
```json
{
  "id": "paper-01",
  "variant": "content-rich",
  "layout": {
    "imageLayout": "side-right",
    "imageStyle": "card",
    "imageAnimation": "float"
  },
  "title": "Paper Title",
  "paragraphs": ["Key insight..."],
  "bulletPoints": ["Point 1", "Point 2"],
  "stat": { "value": "175%", "label": "Improvement" }
}
```

### Animation Options

| Animation | Description | Use Case |
|-----------|-------------|----------|
| `zoom` | Slow scale 1.0→1.1 | Background images |
| `float` | Smooth sine wave ±8px | Side panel images |
| `fade` | Opacity 0→1 | Inline images |
| `slide` | Horizontal entrance | Transitions |

## 🔧 Image Filtering Algorithm

The skill uses multi-stage filtering to remove irrelevant images:

```python
def is_likely_figure(img):
    # Size filtering
    if width < 150 or height < 100: return False  # Icons
    if width > 2000 or height > 1500: return False  # Anomalies
    
    # Content analysis
    content_ratio = non_blank_pixels / total_pixels
    if content_ratio < 0.05: return False  # Blank images
    
    # Color diversity (filter monochrome headers)
    color_ratio = unique_colors / total_pixels
    if color_ratio < 0.05: return False
    
    return True
```

## 🎙️ TTS Configuration

### Recommended Voices

| Voice | Type | Use Case |
|-------|------|----------|
| `zh_male_jieshuoxiaoming_moon_bigtts` | News anchor | Professional briefings |
| `zh_female_cancan_mars_bigtts` | Cheerful | Casual content |
| `en_male_mars_bigtts` | English male | International audiences |

### Audio Sync

Duration is dynamically calculated:
```typescript
const FPS = 30;
const audioDuration = getAudioDuration(scene.id); // seconds
const frames = Math.ceil(audioDuration * FPS);
```

## 🐛 Troubleshooting

### Issue: Image shaking/jittering
**Cause**: Using `extrapolateRight: 'repeat'` for float animation
**Fix**: Use sine wave instead:
```typescript
const floatY = Math.sin((frame % 120) / 120 * Math.PI * 2) * 8;
```

### Issue: Transform conflicts
**Cause**: Layout transform + animation transform string concatenation
**Fix**: Separate concerns:
```typescript
// Layout transform (static)
<div style={{ transform: 'translateY(-50%)' }}>
  {/* Animation transform (dynamic) */}
  <Img style={{ transform: animTransform }} />
</div>
```

### Issue: Video too large for Telegram
**Solution**: Two-pass compression
```bash
# Pass 1: Moderate compression
ffmpeg -i input.mp4 -b:v 1.5M output.mp4  # ~20MB

# Pass 2: Aggressive compression
ffmpeg -i output.mp4 -b:v 600k -b:a 80k final.mp4  # ~15MB
```

### Issue: TTS "resource not granted" error
**Cause**: Missing Volcano Engine permissions
**Fix**: 
1. Check console.volcengine.com for TTS service activation
2. Verify API credentials
3. Ensure quota available

## 📊 Performance Metrics

| Step | Duration | Output Size |
|------|----------|-------------|
| Paper extraction | ~2 min | ~50MB (PDFs) |
| Image filtering | ~30 sec | ~25 images |
| TTS generation | ~3 min | ~5MB (audio) |
| Video rendering | ~15 min | ~60MB |
| Compression | ~15 sec | ~15MB |

**Total pipeline time**: ~20 minutes for 10 papers

## 🎯 Customization

### Custom Scene Layout
Edit `scenes.json`:
```json
{
  "layout": {
    "imageLayout": "side-left",
    "imageStyle": "polaroid",
    "accentColor": "#3b82f6"
  }
}
```

### Custom Animation Speed
Edit `ImageCard.tsx`:
```typescript
// Slower animation (240 frames = 8 seconds)
const floatProgress = (frame % 240) / 240;

// Larger amplitude (±15px)
const floatY = Math.sin(floatProgress * Math.PI * 2) * 15;
```

### Custom Video Length
Adjust scene count in `generate_script.py`:
```python
MAX_PAPERS = 5  # Shorter video
SCENE_DURATION = 15  # Seconds per scene
```

## 🔗 Integration Examples

### With nano-banana-pro
```bash
# 1. Extract papers
python extract_papers.py

# 2. Generate thumbnail with AI
python /skills/nano-banana-pro/scripts/generate.py \
  --prompt "AI research visualization, futuristic, clean"

# 3. Include in video
```

### With x-trends
```bash
# 1. Get trending AI topics
python /skills/x-trends/scripts/trends.py --query "AI papers"

# 2. Filter papers by trending keywords
python extract_papers.py --filter-trending
```

## 📜 License

MIT - Free for personal and commercial use.

## 🙏 Credits

- Remotion for video rendering engine
- Doubao/Volcano for TTS
- Hugging Face for Daily Papers
