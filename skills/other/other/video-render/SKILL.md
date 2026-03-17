---
name: video-render
description: Render videos using Remotion React-based video framework
allowed-tools:
  - Bash
  - Read
  - Write
---

# Video Render Skill

Render professional videos using Remotion (React-based video framework).

## Prerequisites

- Node.js v18+ installed
- Remotion project set up in `remotion-videos/`
- ffmpeg installed for post-processing

## Available Compositions

| Composition | Duration | Description |
|-------------|----------|-------------|
| CodeExplainer | Variable | Animated code tutorials |
| GitHubRecap | 30-60s | GitHub activity summary |
| ThreadToVideo | Variable | Twitter thread as video |
| Audiogram | Variable | Audio with waveform |
| VerticalShort | 15-60s | 9:16 vertical format |
| KineticTypography | 14s | Animated text |
| CountdownTimer | 7s | 3-2-1 countdown |
| DataDashboard | 12s | Animated charts |
| AsciiArt | 10s | ASCII art animation |

## Rendering Commands

### Preview in Studio (Development)

```bash
cd remotion-videos
npm run dev
# Opens at http://localhost:3000
```

### Render Single Composition

```bash
cd remotion-videos

# Render with default settings
npx remotion render {CompositionId} output/{filename}.mp4

# Render with custom props
npx remotion render {CompositionId} output/{filename}.mp4 \
  --props='{"title": "My Video", "content": "Hello World"}'

# Render specific frame range
npx remotion render {CompositionId} output/{filename}.mp4 \
  --frames=0-150
```

### Render with Quality Settings

```bash
# High quality (slower)
npx remotion render {CompositionId} output/{filename}.mp4 \
  --codec=h264 \
  --crf=18 \
  --pixel-format=yuv420p

# Web optimized (smaller file)
npx remotion render {CompositionId} output/{filename}.mp4 \
  --codec=h264 \
  --crf=23 \
  --pixel-format=yuv420p
```

### Render Formats

| Format | Use Case | Command |
|--------|----------|---------|
| MP4 (H.264) | YouTube, general | `--codec=h264` |
| WebM (VP9) | Web embedding | `--codec=vp9` |
| ProRes | Professional editing | `--codec=prores` |
| GIF | Social previews | `--codec=gif` |
| PNG Sequence | After Effects | `--sequence` |

## Composition Props Examples

### CodeExplainer Props

```json
{
  "code": "function hello() {\n  console.log('Hello');\n}",
  "language": "javascript",
  "explanation": "This function logs a greeting",
  "title": "JavaScript Basics"
}
```

### GitHubRecap Props

```json
{
  "username": "octocat",
  "commits": 42,
  "prs": 5,
  "issues": 12,
  "repos": ["repo1", "repo2"],
  "period": "This Week"
}
```

### AsciiArt Props

```json
{
  "asciiArt": "   /\\_/\\\n  ( o.o )\n   > ^ <",
  "title": "Cat Art",
  "animationType": "typewriter",
  "backgroundColor": "#0a0e27",
  "asciiColor": "#00ff88"
}
```

## Output Specifications

| Platform | Resolution | Aspect | Duration |
|----------|------------|--------|----------|
| YouTube | 1920x1080 | 16:9 | Any |
| TikTok | 1080x1920 | 9:16 | 15-60s |
| Instagram Reels | 1080x1920 | 9:16 | 15-90s |
| YouTube Shorts | 1080x1920 | 9:16 | <60s |
| Twitter | 1280x720 | 16:9 | <140s |

## Performance Tips

1. **Use `--concurrency`**: Parallel frame rendering
   ```bash
   npx remotion render MyVideo out.mp4 --concurrency=4
   ```

2. **Use `--gl=angle`**: GPU acceleration on Windows
   ```bash
   npx remotion render MyVideo out.mp4 --gl=angle
   ```

3. **Reduce resolution for tests**:
   ```bash
   npx remotion render MyVideo out.mp4 --scale=0.5
   ```

## Output Files

- Rendered videos: `output/{composition}_{date}.mp4`
- Props files: `output/props/{composition}_props.json`
- Logs: `output/logs/render_{date}.log`
