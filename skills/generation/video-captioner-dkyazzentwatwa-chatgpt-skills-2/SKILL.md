---
name: video-captioner
description: Use when asked to add text overlays, subtitles, or captions to videos with customizable positioning, styling, and timing.
---

# Video Captioner

Add text overlays, subtitles, and captions to videos with full control over positioning, styling, timing, and animation.

## Purpose

Video captioning and text overlays for:
- Social media videos (Instagram, TikTok, YouTube)
- Educational content and tutorials
- Subtitle generation and translation
- Branding and watermarks
- Accessibility compliance

## Features

- **Text Overlays**: Add static or timed text to videos
- **Subtitle Tracks**: Import SRT files or create programmatically
- **Custom Styling**: Font, size, color, background, outline
- **Positioning**: Top, middle, bottom, custom coordinates
- **Animations**: Fade in/out, typewriter effect
- **Batch Captions**: Apply same style to multiple videos
- **Preview**: Generate preview frames before rendering

## Quick Start

```python
from video_captioner import VideoCaptioner

# Add simple text overlay
captioner = VideoCaptioner()
captioner.load('video.mp4')
captioner.add_text(
    text="Hello World!",
    position='bottom',
    font_size=48,
    color='white'
)
captioner.save('captioned.mp4')

# Add timed captions
captioner.add_caption(
    text="First caption",
    start=0.0,
    end=3.0,
    position='bottom'
)
captioner.add_caption(
    text="Second caption",
    start=3.0,
    end=6.0,
    position='bottom'
)
captioner.save('with_captions.mp4')

# Import SRT subtitles
captioner.import_srt('subtitles.srt')
captioner.save('subtitled.mp4')
```

## CLI Usage

```bash
# Simple text overlay
python video_captioner.py input.mp4 --text "Subscribe!" --position bottom --output captioned.mp4

# Add SRT subtitles
python video_captioner.py input.mp4 --srt subtitles.srt --output subtitled.mp4

# Custom styling
python video_captioner.py input.mp4 --text "Sale!" --font-size 72 --color red --bg-color black --position center --output promo.mp4

# Timed text (JSON format)
python video_captioner.py input.mp4 --captions captions.json --output video_with_captions.mp4
```

## API Reference

### VideoCaptioner

```python
class VideoCaptioner:
    def load(self, filepath: str) -> 'VideoCaptioner'
    def add_text(self, text: str, position: str = 'bottom',
                font: str = 'Arial', font_size: int = 48,
                color: str = 'white', bg_color: str = None,
                outline: bool = True) -> 'VideoCaptioner'
    def add_caption(self, text: str, start: float, end: float,
                   **style_kwargs) -> 'VideoCaptioner'
    def import_srt(self, srt_filepath: str, **style_kwargs) -> 'VideoCaptioner'
    def import_captions_json(self, json_filepath: str) -> 'VideoCaptioner'
    def style_preset(self, preset: str) -> 'VideoCaptioner'
    def preview_frame(self, time: float, output: str) -> str
    def save(self, output: str, codec: str = 'libx264') -> str
    def clear_captions(self) -> 'VideoCaptioner'
```

## Text Positioning

Available positions:
- `'top'`: Top center
- `'bottom'`: Bottom center (default)
- `'center'`: Middle center
- `'top-left'`: Top left corner
- `'top-right'`: Top right corner
- `'bottom-left'`: Bottom left corner
- `'bottom-right'`: Bottom right corner
- `(x, y)`: Custom pixel coordinates (tuple)

## Style Presets

**Instagram Story:**
```python
captioner.style_preset('instagram-story')
# White text, large font, top position, strong outline
```

**YouTube Subtitle:**
```python
captioner.style_preset('youtube')
# Yellow text, medium font, bottom position, black background
```

**Minimal:**
```python
captioner.style_preset('minimal')
# White text, no background, subtle shadow
```

**Bold:**
```python
captioner.style_preset('bold')
# Large white text, black background box
```

## SRT Format

Create SRT subtitle files:
```srt
1
00:00:00,000 --> 00:00:03,000
First subtitle text

2
00:00:03,000 --> 00:00:06,000
Second subtitle text
```

## JSON Captions Format

```json
{
  "captions": [
    {
      "text": "First caption",
      "start": 0.0,
      "end": 3.0,
      "position": "bottom",
      "font_size": 48,
      "color": "white"
    },
    {
      "text": "Second caption",
      "start": 3.0,
      "end": 6.0,
      "position": "center",
      "font_size": 60,
      "color": "yellow"
    }
  ]
}
```

## Advanced Styling

**Text with Background Box:**
```python
captioner.add_text(
    text="Important!",
    color='white',
    bg_color='black',
    font_size=60
)
```

**Text with Outline:**
```python
captioner.add_text(
    text="Subscribe",
    color='yellow',
    outline=True,
    outline_color='black',
    outline_width=2
)
```

**Semi-transparent Background:**
```python
captioner.add_text(
    text="Overlay text",
    bg_color='rgba(0,0,0,128)',  # Black, 50% opacity
    font_size=48
)
```

## Use Cases

**Social Media Videos:**
```python
# Instagram reel with centered text
captioner.style_preset('instagram-story')
captioner.add_text("Check this out!", position='top')
```

**Tutorial Videos:**
```python
# Add step-by-step instructions
captioner.add_caption("Step 1: Open the app", 0, 5)
captioner.add_caption("Step 2: Click settings", 5, 10)
captioner.add_caption("Step 3: Enable feature", 10, 15)
```

**Accessibility:**
```python
# Add full subtitles from SRT
captioner.import_srt('subtitles.srt')
captioner.style_preset('youtube')  # High contrast for readability
```

**Branding:**
```python
# Add persistent watermark
captioner.add_text(
    "@username",
    position='bottom-right',
    font_size=24,
    color='white',
    outline=True
)
```

## Performance Tips

- Pre-render preview frames to test styling
- Use h264 codec for faster encoding
- Keep caption duration >2 seconds for readability
- Use high contrast colors for accessibility
- Test on mobile screens for social media

## Limitations

- Text rendering performance depends on video length
- Complex animations may increase render time
- Very long text may overflow screen bounds
- Emoji support depends on installed fonts
- Cannot edit burned-in existing captions (requires original)
