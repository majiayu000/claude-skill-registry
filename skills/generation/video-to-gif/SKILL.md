---
name: video-to-gif
description: Convert video clips to optimized GIFs with speed control, cropping, text overlays, and file size optimization. Create perfect GIFs for social media, documentation, and presentations.
---

# Video to GIF Workshop

Transform video clips into high-quality, optimized GIFs perfect for social media, documentation, tutorials, and presentations. Features precise timing control, text overlays, effects, and intelligent file size optimization.

## Core Capabilities

- **Clip Selection**: Extract specific time ranges from videos
- **Speed Control**: Slow motion, speed up, or reverse
- **Cropping**: Resize and crop to any dimensions
- **Text Overlays**: Add captions, titles, or watermarks
- **Effects**: Filters, fades, color adjustments
- **Optimization**: Smart compression for target file size
- **Batch Processing**: Convert multiple clips at once

## Quick Start

```python
from scripts.gif_workshop import GifWorkshop

# Basic conversion
workshop = GifWorkshop("video.mp4")
workshop.to_gif("output.gif")

# With options
workshop = GifWorkshop("video.mp4")
workshop.clip(start=5, end=10)          # 5-10 seconds
workshop.resize(width=480)               # Resize to 480px wide
workshop.set_fps(15)                     # 15 frames per second
workshop.optimize(max_size_kb=500)       # Max 500KB
workshop.to_gif("output.gif")
```

## Core Workflow

### 1. Load Video

```python
from scripts.gif_workshop import GifWorkshop

# From file
workshop = GifWorkshop("video.mp4")

# With initial settings
workshop = GifWorkshop("video.mp4", fps=15, width=480)
```

### 2. Select Clip Range

```python
# By time (seconds)
workshop.clip(start=5, end=15)  # 5s to 15s

# By time string
workshop.clip(start="00:01:30", end="00:01:45")  # 1:30 to 1:45

# From start or to end
workshop.clip(start=10)  # From 10s to end
workshop.clip(end=5)     # First 5 seconds

# Multiple clips
workshop.clip_multi([
    (0, 3),
    (10, 15),
    (20, 25)
])  # Concatenates clips
```

### 3. Adjust Speed

```python
# Speed up
workshop.speed(2.0)  # 2x faster

# Slow motion
workshop.speed(0.5)  # Half speed

# Reverse
workshop.reverse()

# Boomerang effect (forward then reverse)
workshop.boomerang()
```

### 4. Resize and Crop

```python
# Resize by width (maintain aspect)
workshop.resize(width=480)

# Resize by height
workshop.resize(height=360)

# Exact dimensions
workshop.resize(width=480, height=360)

# Crop to region
workshop.crop(x=100, y=50, width=400, height=300)

# Crop to aspect ratio
workshop.crop_to_aspect(16, 9)  # 16:9
workshop.crop_to_aspect(1, 1)   # Square
```

### 5. Add Text

```python
# Simple text overlay
workshop.add_text(
    "Hello World!",
    position='bottom',
    fontsize=24,
    color='white'
)

# Text with timing
workshop.add_text(
    "Watch this!",
    position='top',
    start_time=0,
    end_time=3  # Show for first 3 seconds
)

# Multiple text overlays
workshop.add_text("Step 1", position='top-left', start_time=0, end_time=2)
workshop.add_text("Step 2", position='top-left', start_time=2, end_time=4)

# Caption bar
workshop.add_caption_bar(
    "This is a caption",
    position='bottom',
    background='black',
    padding=10
)
```

### 6. Apply Effects

```python
# Color filters
workshop.filter('grayscale')
workshop.filter('sepia')

# Adjustments
workshop.adjust(brightness=0.1, contrast=0.2)

# Fade in/out
workshop.fade_in(duration=0.5)
workshop.fade_out(duration=0.5)

# Blur
workshop.blur(intensity=2)
```

### 7. Optimize for Size

```python
# Target file size
workshop.optimize(max_size_kb=500)

# Quality settings
workshop.optimize(
    quality='medium',  # 'low', 'medium', 'high'
    colors=128         # Color palette size (2-256)
)

# Manual FPS control
workshop.set_fps(10)  # Lower FPS = smaller file

# Lossy compression
workshop.optimize(lossy=80)  # 0-100, higher = more compression
```

### 8. Export

```python
# Basic export
workshop.to_gif("output.gif")

# With options
workshop.to_gif(
    "output.gif",
    optimize=True,
    colors=256,
    loop=0  # 0 = infinite loop, 1+ = loop count
)

# Export as video (for comparison)
workshop.to_video("output.mp4")

# Export frames
workshop.export_frames("frames/", format='png')
```

## Presets

```python
# Social media presets
workshop.preset('twitter')     # 512px wide, 5MB max
workshop.preset('discord')     # 256px, 8MB max
workshop.preset('slack')       # 480px, 5MB max
workshop.preset('reddit')      # 720px, optimized

# Quality presets
workshop.preset('high')        # High quality, larger file
workshop.preset('medium')      # Balanced
workshop.preset('low')         # Small file, lower quality

# Special presets
workshop.preset('thumbnail')   # Small preview GIF
workshop.preset('reaction')    # Reaction GIF (small, fast)
```

## Text Position Options

| Position | Description |
|----------|-------------|
| `'top'` | Top center |
| `'bottom'` | Bottom center |
| `'center'` | Center of frame |
| `'top-left'` | Top left corner |
| `'top-right'` | Top right corner |
| `'bottom-left'` | Bottom left corner |
| `'bottom-right'` | Bottom right corner |

## Advanced Features

### Frame Extraction

```python
# Get best frame (thumbnail)
best_frame = workshop.get_best_frame()
best_frame.save("thumbnail.png")

# Extract frame at time
frame = workshop.get_frame_at(5.5)  # Frame at 5.5 seconds
frame.save("frame.png")

# Extract all frames
workshop.export_frames("frames/", format='png')
```

### Video Information

```python
info = workshop.get_info()
print(f"Duration: {info['duration']} seconds")
print(f"Size: {info['width']}x{info['height']}")
print(f"FPS: {info['fps']}")
print(f"Frames: {info['frame_count']}")
```

### Custom Filters

```python
# Apply custom function to each frame
def custom_filter(frame):
    # frame is a PIL Image
    return frame.rotate(5)

workshop.apply_filter(custom_filter)
```

### Concatenate Videos

```python
# Join multiple clips
workshop.concat([
    "intro.mp4",
    "main.mp4",
    "outro.mp4"
])
```

## CLI Usage

```bash
# Basic conversion
python gif_workshop.py video.mp4 -o output.gif

# With clip selection
python gif_workshop.py video.mp4 -o output.gif --start 5 --end 15

# With options
python gif_workshop.py video.mp4 -o output.gif \
    --width 480 \
    --fps 15 \
    --speed 1.5 \
    --max-size 500

# With text
python gif_workshop.py video.mp4 -o output.gif \
    --text "Hello World" \
    --text-position bottom

# Apply preset
python gif_workshop.py video.mp4 -o output.gif --preset twitter
```

## Optimization Tips

### File Size Reduction

1. **Reduce dimensions**: Smaller = much smaller file
2. **Lower FPS**: 10-15 FPS is usually sufficient
3. **Limit colors**: 64-128 colors often looks fine
4. **Shorter duration**: Each second adds significant size
5. **Use lossy compression**: Small quality loss, big size reduction

### Quality Improvement

1. **Start with high-quality source**: Better input = better output
2. **Use 256 colors**: Maximum palette
3. **Higher FPS**: 24-30 FPS for smooth motion
4. **Avoid heavy compression**: Keep lossy above 90

### Size vs Quality Presets

| Preset | Width | FPS | Colors | Use Case |
|--------|-------|-----|--------|----------|
| `reaction` | 256px | 10 | 64 | Quick reactions |
| `low` | 320px | 12 | 128 | Basic sharing |
| `medium` | 480px | 15 | 256 | General use |
| `high` | 640px | 20 | 256 | High quality |
| `max` | Original | 24 | 256 | Best quality |

## Error Handling

```python
from scripts.gif_workshop import GifWorkshop, GifError

try:
    workshop = GifWorkshop("video.mp4")
    workshop.clip(start=0, end=100)  # May exceed video length
    workshop.to_gif("output.gif")
except GifError as e:
    print(f"Error: {e}")
except FileNotFoundError:
    print("Video file not found")
```

## Supported Formats

### Input (Video)
- MP4, MOV, AVI, MKV, WebM, FLV, WMV

### Output
- GIF (animated)
- MP4 (for comparison)
- PNG/JPEG (frames)

## Dependencies

```
moviepy>=1.0.3
Pillow>=10.0.0
imageio>=2.31.0
numpy>=1.24.0
```

## Limitations

- Maximum practical GIF size: ~20-30MB
- Very long GIFs become unwieldy
- Complex scenes may have color banding
- No audio support in GIF format
