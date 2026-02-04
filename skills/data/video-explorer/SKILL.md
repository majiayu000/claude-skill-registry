---
name: video-explorer
description: This skill should be used when analyzing video files. Claude cannot process video directly, so this skill extracts frames hierarchically - starting with a quick overview, then zooming into regions of interest with higher resolution and temporal density. Use when asked to watch, analyze, review, or understand video content.
---

# Video Explorer

Analyze video content through hierarchical frame extraction. Start wide, identify interesting regions, zoom in.

## Workflow

### 1. Overview First

Extract quick thumbnails to see the video timeline:

```bash
./skills/video-explorer/scripts/videx overview <video>
```

This creates small frames (320px) at 10-second intervals in `./videx-out/<name>/overview/`.

Read all overview frames to understand video structure:
```bash
ls ./videx-out/<name>/overview/
```

Then use the Read tool on the jpg files to see them.

### 2. Identify Regions of Interest

After viewing overview frames, identify timestamps where:
- Something interesting is happening
- More detail is needed
- Action is occurring that requires temporal resolution

### 3. Zoom In

**For a time range** (more frames, higher resolution):
```bash
./skills/video-explorer/scripts/videx range <video> <start>-<end>
# Example: videx range talk.mp4 5:30-6:00
```

**For higher temporal resolution** (catch fast action):
```bash
./skills/video-explorer/scripts/videx range <video> <start>-<end> --fps=10
```

**For a single frame at full detail**:
```bash
./skills/video-explorer/scripts/videx zoom <video> <time>
# Example: videx zoom talk.mp4 5:45
```

### 4. Iterate

Repeat zoom operations as needed until the question is answered.

## Commands Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `videx overview <video>` | Quick timeline scan | 320px frames @ 10s intervals |
| `videx overview <video> 5 480` | Denser timeline | 480px frames @ 5s intervals |
| `videx range <video> <start>-<end>` | Extract segment | 1280px frames @ 2fps |
| `videx range <video> <start>-<end> --fps=10` | Fast action | 1280px frames @ 10fps |
| `videx zoom <video> <time>` | Single frame detail | 1920px single frame |
| `videx zoom <video> <time> --hd` | Maximum detail | Full resolution frame |

## Time Formats

All commands accept these time formats:
- `1:30` = 1 minute 30 seconds
- `01:30:00` = 1 hour 30 minutes
- `90` = 90 seconds
- `1:30.5` = 1 minute 30.5 seconds

## Output Structure

Frames are saved with timestamps in filenames for easy reference:

```
./videx-out/
└── video-name/
    ├── overview/
    │   ├── t_00-00-00.00.jpg
    │   ├── t_00-00-10.00.jpg
    │   └── ...
    ├── range_5-30_6-00/
    │   ├── t_00-05-30.00.jpg
    │   └── ...
    └── zoom/
        └── t_00-05-45.00.jpg
```

## Example Session

User asks: "What happens in this lecture video around the 10 minute mark?"

1. Run overview to understand video structure
2. View overview frames, note that slides change around 9:30-11:00
3. Extract that range: `videx range lecture.mp4 9:30-11:00`
4. View range frames, find the specific slide transition at 10:15
5. Zoom for detail: `videx zoom lecture.mp4 10:15`
6. Report findings with specific timestamps
