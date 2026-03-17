---
name: podcast-production-guide
description: Эксперт podcast production. Используй для создания подкастов, audio editing и distribution.
---

# Podcast Production Guide

Expert in podcast creation, production, distribution, and growth strategies.

## Pre-Production Planning

### Format Selection

```yaml
podcast_formats:
  interview:
    description: "Host interviews guests"
    pros: ["Fresh perspectives", "Built-in networking", "Easier content"]
    cons: ["Scheduling complexity", "Variable audio quality"]
    best_for: "Thought leadership, industry insights"

  solo:
    description: "Single host commentary"
    pros: ["Complete control", "Flexible scheduling"]
    cons: ["All content burden on host"]
    best_for: "Education, personal brand"

  co_hosted:
    description: "Two or more regular hosts"
    pros: ["Dynamic conversation", "Shared workload"]
    best_for: "Discussion, commentary"

  narrative:
    description: "Scripted, story-driven"
    pros: ["High production value", "Bingeable"]
    cons: ["Time-intensive production"]
    best_for: "Documentary, true crime, fiction"
```

### Episode Structure

```yaml
episode_structure:
  intro:
    duration: "30-90 seconds"
    elements:
      - "Theme music / audio branding"
      - "Show introduction"
      - "Episode teaser"
      - "Sponsor message (if applicable)"

  main_content:
    duration: "20-45 minutes"
    elements:
      - "Topic introduction"
      - "Core content segments"
      - "Guest interview (if applicable)"

  outro:
    duration: "60-120 seconds"
    elements:
      - "Summary of key points"
      - "Call to action"
      - "Next episode teaser"
      - "Credits and thanks"
```

## Recording Best Practices

### Audio Quality Standards

```yaml
audio_specifications:
  recording:
    format: "WAV or AIFF"
    sample_rate: "48kHz"
    bit_depth: "24-bit"
    channels: "Mono per speaker"

  microphone:
    distance: "6-8 inches from mouth"
    positioning: "Slightly off-axis to reduce plosives"

  gain_staging:
    target_level: "-18dB to -12dB peaks"
    headroom: "6dB minimum"
    clipping: "Never clip - cannot be fixed"

  environment_checklist:
    - "[ ] Phone on silent"
    - "[ ] Computer notifications off"
    - "[ ] Levels checked"
    - "[ ] Headphones connected"
```

## Post-Production Workflow

### Audio Processing Chain

```yaml
editing_workflow:
  stage_1_cleanup:
    - action: "High-pass filter"
      setting: "80-100Hz to remove rumble"
    - action: "Noise reduction"
      setting: "Light touch, preserve naturalness"
    - action: "De-essing"
      setting: "Reduce harsh sibilance"

  stage_2_dynamics:
    - action: "Compression"
      setting: "4:1 ratio, -18dB threshold"
    - action: "Limiting"
      setting: "-1dB ceiling"

  stage_3_mastering:
    - action: "Loudness normalization"
      target: "-16 LUFS (podcast standard)"
    - action: "True peak limiting"
      setting: "-1.5dB true peak"
```

## Distribution

### Export Settings

```yaml
export_specifications:
  audio:
    format: "MP3"
    bit_rate: "128kbps CBR (stereo) or 64kbps (mono)"
    sample_rate: "44.1kHz"

  artwork:
    dimensions: "3000x3000 pixels"
    format: "JPEG or PNG"
    file_size: "Under 512KB"
```

### Platforms

```yaml
distribution:
  primary:
    - "Apple Podcasts"
    - "Spotify"
    - "Google Podcasts"

  hosting:
    - name: "Transistor"
      features: "Analytics, multiple shows"
    - name: "Buzzsprout"
      features: "Easy setup, promotional tools"
    - name: "Anchor"
      features: "Free, Spotify integration"
```

## Monetization

```yaml
monetization:
  advertising:
    pre_roll: "$15-25 CPM"
    mid_roll: "$20-35 CPM"
    post_roll: "$10-15 CPM"
    note: "Host-read ads perform 3x better"

  premium_content:
    platforms: ["Patreon", "Apple Subscriptions", "Supercast"]
    offerings:
      - "Ad-free episodes"
      - "Bonus content"
      - "Early access"

  affiliate:
    - "Product recommendations"
    - "Trackable links"
    - "Promo codes"
```

## Лучшие практики

1. **Consistency** — придерживайтесь регулярного графика
2. **Audio quality** — инвестируйте в хорошее оборудование
3. **Show notes SEO** — оптимизируйте описания для поиска
4. **Engage audience** — отвечайте на отзывы
5. **Promote actively** — каждый эпизод требует продвижения
6. **Measure and iterate** — анализируйте метрики
