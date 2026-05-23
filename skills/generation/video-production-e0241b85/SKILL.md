---
name: video-production
description: Technical video production including tutorials, live streams, and YouTube content
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 03-content-creator
bond_type: SECONDARY_BOND
---

# Video Production for DevRel

Create **engaging technical videos** from tutorials to live coding sessions.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - video_type: enum[short, tutorial, deep_dive, livestream]
    - topic: string
  optional:
    - duration_target: duration
    - platform: enum[youtube, tiktok, linkedin, twitch]
```

### Output
```yaml
output:
  video:
    script_outline: markdown
    equipment_checklist: array[string]
    post_production_notes: array[string]
```

## Video Types

| Type | Length | Purpose |
|------|--------|---------|
| Short-form | 1-3 min | Quick tips, TikTok/Reels |
| Tutorial | 5-20 min | Step-by-step learning |
| Deep dive | 20-45 min | Comprehensive coverage |
| Live stream | 30-120 min | Real-time engagement |

## Production Workflow

```
Script → Record → Edit → Review → Publish → Promote
   ↓        ↓        ↓       ↓         ↓         ↓
Outline  Capture   Cut    QA check  Upload    Social
         Video    Polish  Feedback  Optimize  Share
```

## Equipment Setup

### Minimum Viable (~$500)
- Webcam (Logitech C920/C922)
- USB microphone (Blue Yeti/AT2020)
- Ring light
- OBS Studio (free)

### Professional (~$2000+)
- DSLR/mirrorless camera
- XLR microphone + interface
- Key + fill lighting
- Stream deck

## Recording Tips

### Screen Recording
- 1080p minimum, 4K preferred
- Clean desktop (hide icons)
- Increase font sizes (140%)
- Record in segments

### On-Camera
- Eye level with camera
- Well-lit face (no shadows)
- Neutral background
- Look at camera (not screen)

## Editing Workflow

1. **Rough cut**: Remove mistakes, dead air
2. **Fine cut**: Tighten pacing
3. **Polish**: Add B-roll, graphics
4. **Audio**: Level, noise reduction
5. **Export**: Platform-optimized settings

## YouTube Optimization

| Element | Best Practice |
|---------|---------------|
| Title | Keyword + benefit, <60 chars |
| Thumbnail | Bold text, faces, contrast |
| Description | Links, timestamps, keywords |
| Tags | 5-10 relevant keywords |

## Retry Logic

```yaml
retry_patterns:
  poor_audio:
    strategy: "Re-record with better mic placement"

  low_engagement:
    strategy: "Improve thumbnail and title"

  tech_issues_during_record:
    strategy: "Record in segments, have backup"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Audio issues | Bad sound | Re-record or AI cleanup |
| Poor lighting | Dark footage | Add post-processing |
| Low views | <10% click rate | Update thumbnail |

## Debug Checklist

```
□ Script/outline ready?
□ Equipment tested?
□ Background clean?
□ Audio levels checked?
□ Recording software set up?
□ Backup storage available?
```

## Test Template

```yaml
test_video_production:
  unit_tests:
    - test_audio_quality:
        assert: "Clear, no background noise"
    - test_video_quality:
        assert: "1080p minimum"

  integration_tests:
    - test_full_workflow:
        assert: "Script to publish complete"
```

## Observability

```yaml
metrics:
  - video_length: duration
  - views: integer
  - watch_time_avg: duration
  - click_through_rate: float
```

See `assets/` for production checklists.
