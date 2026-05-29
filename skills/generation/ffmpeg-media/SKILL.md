---
name: media
description: Media processing = ffmpeg + imagemagick + sox.
version: 1.0.0
---


# media

Media processing = ffmpeg + imagemagick + sox.

## Atomic Skills

| Skill | Domain |
|-------|--------|
| ffmpeg | Video/audio |
| imagemagick | Images |
| sox | Audio |

## Video

```bash
# Convert
ffmpeg -i in.mov -c:v libx264 out.mp4

# Resize
ffmpeg -i in.mp4 -vf scale=1280:-1 out.mp4

# GIF
ffmpeg -i in.mp4 -vf "fps=10,scale=320:-1" out.gif
```

## Audio

```bash
# Extract
ffmpeg -i video.mp4 -vn -c:a aac audio.m4a

# Convert
sox in.wav -r 44100 out.wav
```

## Image

```bash
# Resize
convert in.png -resize 800x600 out.png

# Format
convert in.png out.jpg
```

## Pipeline

```bash
ffmpeg -i in.mp4 -f image2pipe - | convert - -resize 50% out.gif
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