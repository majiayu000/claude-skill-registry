---
name: YouTube Packaging
tier: 3
load_policy: task-specific
description: Prepare complete YouTube upload package with metadata
version: 1.0.0
parent_skill: production-operations
---

# YouTube Packaging Skill

> **The Final Mile to Publication**

This skill handles preparing the complete YouTube upload package with video, thumbnail, metadata, and subtitles.

---

## Purpose

Create a professional, SEO-optimized YouTube package ready for upload.

---

## Package Contents

| File | Purpose | Required |
|------|---------|----------|
| `final_video.mp4` | Upload video | Yes |
| `thumbnail.png` | Custom thumbnail | Yes |
| `metadata.yaml` | Title, description, tags | Yes |
| `subtitles.vtt` | Closed captions | Yes |
| `chapters.txt` | Chapter markers | Recommended |

---

## Command

```bash
python3 scripts/core/package_youtube.py sessions/{session}/
```

---

## Output Location

```
sessions/{session}/output/youtube_package/
├── final_video.mp4
├── thumbnail.png
├── metadata.yaml
├── subtitles.vtt
└── chapters.txt
```

---

## Thumbnail Generation

```bash
python3 scripts/core/generate_thumbnail.py sessions/{session}/
```

### Thumbnail Specifications

| Property | Requirement |
|----------|-------------|
| Resolution | 1280x720 pixels |
| Aspect Ratio | 16:9 |
| Format | PNG or JPEG |
| File Size | Under 2MB |
| Title Font | 80-120px, bold, white with glow |

### Template Selection

| Template | Best For |
|----------|----------|
| `portal_gateway` | Eden pathworkings, cosmic journeys |
| `sacred_symbol` | Tree of Life, chakras, geometry |
| `journey_scene` | Gardens, temples, vistas |
| `abstract_energy` | Neural themes, brainwaves |

### Color Palettes

| Palette | Colors | Best For |
|---------|--------|----------|
| `sacred_light` | Gold, Cream, Cosmic | Divine, spiritual |
| `cosmic_journey` | Purple, Blue, Space | Cosmic, astral |
| `garden_eden` | Emerald, Gold, Forest | Nature, Eden |
| `ancient_temple` | Antique Gold, Bronze | Historical, temple |

---

## Metadata Structure

```yaml
# metadata.yaml
title: "EDEN GATEWAY | Deep Hypnotic Journey to Paradise"
description: |
  Embark on a profound journey into the Garden of Eden...

  What you'll experience:
  - Progressive relaxation and gentle induction
  - Guided visualization through paradise
  - Connection with divine presence
  - Peaceful emergence and integration

  ⚠️ Safety Note:
  Listen only when safely relaxed. Not for driving or operating machinery.

  🎧 For best experience, use headphones with binaural-capable audio.

  #hypnosis #meditation #guidedmeditation #eden #spiritualjourney

tags:
  - hypnosis
  - guided meditation
  - deep relaxation
  - binaural beats
  - eden garden
  - spiritual journey
  - theta waves
  - christian meditation

category: "People & Blogs"
visibility: "public"
made_for_kids: false
```

---

## Title Optimization

### High-CTR Title Patterns

| Pattern | Example |
|---------|---------|
| Outcome + Method | "Deep Sleep in 10 Minutes | Guided Hypnosis" |
| Destination + Experience | "EDEN GATEWAY | Hypnotic Journey to Paradise" |
| Problem + Solution | "Anxiety Relief | Theta Wave Meditation" |

### Title Guidelines

- **Length**: 50-70 characters optimal
- **CAPS**: Use for key words (EDEN, DEEP, SACRED)
- **Pipe separator**: Divides title from descriptor
- **No clickbait**: Honest representation of content

---

## Description Template

```markdown
[Opening hook - 1-2 sentences about the journey]

[What the listener will experience - 3-5 bullet points]

[Timestamps/Chapters if applicable]

⚠️ IMPORTANT: [Safety disclaimer]

🎧 BEST EXPERIENCE: [Headphone recommendation]

═══════════════════════════════════════

📿 About This Journey
[2-3 sentences about the spiritual/therapeutic intention]

✨ Benefits
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

═══════════════════════════════════════

🔔 Subscribe for more transformative journeys
👍 Like if this helped you
💬 Share your experience in the comments

#[tag1] #[tag2] #[tag3] #[tag4] #[tag5]
```

---

## Chapter Markers

Format for YouTube chapters:

```txt
0:00 Introduction
0:45 Safety & Preparation
3:00 Progressive Relaxation
7:00 Deepening Into Trance
12:00 The Garden Gateway
18:00 Divine Presence
24:00 Integration & Gifts
27:00 Gentle Awakening
```

**Requirements**:
- First chapter must be at 0:00
- Minimum 3 chapters
- Each chapter minimum 10 seconds

---

## Tag Strategy

### Primary Tags (5-8)
- Core topic: `hypnosis`, `guided meditation`
- Brainwave: `theta waves`, `binaural beats`
- Theme: `eden garden`, `spiritual journey`
- Outcome: `deep relaxation`, `inner peace`

### Secondary Tags (5-7)
- Related topics: `christian meditation`, `visualization`
- Long-tail: `guided meditation for sleep`, `deep theta meditation`

### Tag Guidelines
- Total tags: 10-15
- Mix broad and specific
- Include relevant LSI terms
- No misleading tags

---

## Pre-Upload Checklist

### Video File
- [ ] Resolution: 1920x1080
- [ ] Duration matches expected
- [ ] Audio/video sync verified
- [ ] No artifacts or glitches

### Thumbnail
- [ ] 1280x720 resolution
- [ ] Under 2MB file size
- [ ] Text readable at small size
- [ ] Compelling and honest

### Metadata
- [ ] Title under 100 characters
- [ ] Description complete with sections
- [ ] 10-15 relevant tags
- [ ] Chapters formatted correctly

### Subtitles
- [ ] VTT format valid
- [ ] Timing synced to audio
- [ ] All text included
- [ ] No formatting errors

---

## YouTube Studio Settings

When uploading:

| Setting | Value |
|---------|-------|
| Visibility | Public (or Unlisted for testing) |
| Category | People & Blogs |
| Made for Kids | No |
| Age Restriction | No |
| Comments | On, held for review |
| Subtitles | Upload VTT file |

---

## Website Upload (Optional)

After YouTube, optionally upload to salars.net:

```bash
python3 scripts/core/upload_to_website.py --session sessions/{session}/
```

---

## Related Resources

- **Skill**: `tier3-production/video-assembly/` (input)
- **Doc**: `docs/YOUTUBE_PACKAGING_SOP.md`
- **Doc**: `docs/THUMBNAIL_DESIGN_GUIDE.md`
- **Doc**: `docs/YOUTUBE_TITLE_GUIDE.md`
- **Script**: `scripts/core/package_youtube.py`
