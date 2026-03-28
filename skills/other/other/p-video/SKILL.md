---
name: p-video
description: "Generate videos with Pruna P-Video and WAN models via inference.sh CLI. Models: P-Video, WAN-T2V, WAN-I2V. Capabilities: text-to-video, image-to-video, audio support, 720p/1080p, fast inference. Pruna optimizes models for speed without quality loss. Triggers: pruna video, p-video, pruna ai video, fast video generation, optimized video, wan t2v, wan i2v, economic video generation, cheap video generation, pruna text to video, pruna image to video"
allowed-tools: Bash(infsh *)
---

# Pruna P-Video Generation

Generate videos with Pruna's optimized video models via [inference.sh](https://inference.sh) CLI.

![P-Video Generation](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kkgymcjx9g2tv51m602jssn3.jpeg)

## Quick Start

> Requires inference.sh CLI (`infsh`). Get installation instructions: `npx skills add inference-sh/skills@agent-tools`

```bash
infsh login

infsh app run pruna/p-video --input '{"prompt": "drone shot flying over a forest at sunset"}'
```


## Pruna Video Models

Pruna optimizes AI models for speed without sacrificing quality.

| Model | App ID | Best For |
|-------|--------|----------|
| P-Video | `pruna/p-video` | Text-to-video, image-to-video, with audio |
| WAN-T2V | `pruna/wan-t2v` | Text-to-video, 480p/720p |
| WAN-I2V | `pruna/wan-i2v` | Animate images, 480p/720p |

## Examples

### Text-to-Video

```bash
infsh app run pruna/p-video --input '{
  "prompt": "waves crashing on a beach at sunset",
  "duration": 5,
  "resolution": "720p"
}'
```

### Image-to-Video

```bash
infsh app run pruna/p-video --input '{
  "prompt": "gentle camera movement, clouds drifting",
  "image": "https://your-image.jpg"
}'
```

### With Audio

P-Video supports audio input that syncs with the video:

```bash
infsh app run pruna/p-video --input '{
  "prompt": "person talking in an interview setting",
  "audio": "https://your-audio.mp3"
}'
```

### WAN Text-to-Video

Fast and economical text-to-video:

```bash
infsh app run pruna/wan-t2v --input '{
  "prompt": "a cat playing with a ball of yarn",
  "resolution": "720p",
  "duration": 5
}'
```

### WAN Image-to-Video

Animate any still image:

```bash
infsh app run pruna/wan-i2v --input '{
  "prompt": "gentle movement, natural motion, subtle breathing",
  "image": "https://portrait.jpg",
  "resolution": "720p"
}'
```

### 1080p High Quality

```bash
infsh app run pruna/p-video --input '{
  "prompt": "cinematic landscape with dramatic clouds",
  "resolution": "1080p",
  "duration": 5
}'
```

### Draft Mode (Faster, Cheaper)

```bash
infsh app run pruna/p-video --input '{
  "prompt": "quick concept test video",
  "draft": true
}'
```

## Resolution Options

| Model | Resolutions | Pricing |
|-------|-------------|---------|
| P-Video | 720p, 1080p | Per second, varies by resolution/draft |
| WAN-T2V | 480p, 720p | $0.05 (480p), $0.10 (720p) per video |
| WAN-I2V | 480p, 720p | $0.05 (480p), $0.11 (720p) per video |

## Browse All Pruna Apps

```bash
infsh app list --namespace pruna
```

## Related Skills

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@agent-tools

# All video generation models
npx skills add inference-sh/skills@ai-video-generation

# Image-to-video guide
npx skills add inference-sh/skills@image-to-video

# Pruna image generation
npx skills add inference-sh/skills@p-image

# Text-to-speech (for video narration)
npx skills add inference-sh/skills@text-to-speech
```

Browse all apps: `infsh app list`

## Documentation

- [Running Apps](https://inference.sh/docs/apps/running) - How to run apps via CLI
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) - Real-time progress updates
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) - Building media workflows

