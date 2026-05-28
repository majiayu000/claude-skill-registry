---
name: ffmpeg-media
description: FFmpeg media processing. Video/audio transcoding, stream manipulation, and filter graphs.
version: 1.0.0
---


# FFmpeg Media Skill

**Trit**: +1 (PLUS - generative media transformation)  
**Foundation**: FFmpeg + libav + filter system  

## Core Concept

FFmpeg transforms media through:
- Container/codec transcoding
- Stream extraction and muxing
- Complex filter graphs
- Hardware acceleration

## Common Commands

```bash
# Transcode video
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -c:a aac output.m4a

# Convert to GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif

# Cut segment
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c copy segment.mp4

# Concat files
ffmpeg -f concat -i list.txt -c copy output.mp4
```

## Filter Graphs

```bash
# Scale and add text
ffmpeg -i input.mp4 \
  -vf "scale=1280:720,drawtext=text='Title':fontsize=24:x=10:y=10" \
  output.mp4

# Color adjustment
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:saturation=1.2" output.mp4
```

## GF(3) Integration

```python
def trit_from_media_op(op: str) -> int:
    """Map FFmpeg operations to GF(3) trits."""
    if op in ["probe", "analyze", "check"]:
        return -1  # MINUS: verification
    elif op in ["copy", "remux", "extract"]:
        return 0   # ERGODIC: preservation
    else:
        return 1   # PLUS: transformation
```

## Canonical Triads

```
spi-parallel-verify (-1) ⊗ video-downloader (0) ⊗ ffmpeg-media (+1) = 0 ✓
mathpix-ocr (-1) ⊗ image-enhancer (0) ⊗ ffmpeg-media (+1) = 0 ✓
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.