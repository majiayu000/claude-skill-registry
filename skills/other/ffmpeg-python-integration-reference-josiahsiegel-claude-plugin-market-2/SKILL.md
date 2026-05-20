---
name: ffmpeg-python-integration-reference
description: Authoritative Python-FFmpeg parameter integration reference ensuring type safety, accurate parameter mappings, and proper unit conversions. PROACTIVELY activate for: (1) ffmpeg-python library usage, (2) Python subprocess FFmpeg calls, (3) Caption/subtitle parameter mapping (drawtext, ASS), (4) Color format conversions (BGR, RGB, ABGR, ASS &HAABBGGRR), (5) Time unit conversions (seconds, centiseconds, milliseconds), (6) Type safety validation (int, float, string), (7) Coordinate systems, (8) Parameter range enforcement, (9) Frame pipe handling, (10) Error detection for type mismatches. Provides: Complete parameter type reference, color format conversion tables, time unit conversion formulas, validation patterns, working Python examples with proper typing.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

# Python-FFmpeg Integration Reference (2025-2026)

Complete type-safe parameter mapping reference for integrating FFmpeg with Python.

## Quick Reference

| FFmpeg Parameter | Python Type | Range/Format | Common Mistake |
|------------------|-------------|--------------|----------------|
| `-crf` | `int` or `str` | 0-51 (H.264/H.265) | Using float: `crf=18.5` ❌ |
| `-b:v` | `str` | "5M", "1000k" | Using int: `b:v=5000000` ❌ |
| `fontsize` | `int` | 1-999 | Using str: `fontsize="24"` ❌ |
| `fontcolor` | `str` | "white", "#FFFFFF", "0xFFFFFF" | Wrong format: `fontcolor="255,255,255"` ❌ |
| ASS PrimaryColour | `str` | "&HAABBGGRR" | Using RGB: `&H00FFFFFF` ❌ (should be BGR) |
| `alpha` | `str` (expression) | "0.5", "min(1,t/2)" | Using float: `alpha=0.5` ❌ |
| `x`, `y` | `str` or `int` | "100", "(w-tw)/2" | Forgetting quotes on expressions ❌ |

---

# Section 1: Color Format Conversions

## Critical: FFmpeg Color Format Landscape

| Context | Format | Byte Order | Example | Python Type |
|---------|--------|------------|---------|-------------|
| **FFmpeg drawtext** | Named/Hex | RGB | "white", "#FFFFFF", "0xFFFFFF" | `str` |
| **ASS PrimaryColour** | &HAABBGGRR | ABGR | `&H00FFFFFF` (white) | `str` |
| **ASS OutlineColour** | &HAABBGGRR | ABGR | `&H00000000` (black) | `str` |
| **OpenCV cv2** | Array | BGR | `[255, 255, 255]` | `np.ndarray` |
| **PIL/Pillow** | Tuple/Hex | RGB | `(255, 255, 255)`, "#FFFFFF" | `tuple` or `str` |
| **NumPy** | Array | RGB or BGR | Depends on source | `np.ndarray` |

## Color Conversion Functions (Python)

```python
from typing import Tuple

def rgb_to_bgr_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB (0-255) to BGR hex string.
    Used for OpenCV color specifications.

    Args:
        r, g, b: Red, Green, Blue (0-255)

    Returns:
        Hex string in BGR order: "0xBBGGRR"
    """
    return f"0x{b:02X}{g:02X}{r:02X}"

def rgb_to_ass_color(r: int, g: int, b: int, alpha: int = 0) -> str:
    """
    Convert RGB to ASS/SSA color format (&HAABBGGRR).

    CRITICAL: ASS uses BGR order, not RGB!

    Args:
        r, g, b: Red, Green, Blue (0-255)
        alpha: Alpha channel (0=opaque, 255=transparent)

    Returns:
        ASS color string: "&HAABBGGRR"

    Examples:
        >>> rgb_to_ass_color(255, 255, 255)  # White
        '&H00FFFFFF'
        >>> rgb_to_ass_color(255, 0, 0)      # Red
        '&H000000FF'
        >>> rgb_to_ass_color(0, 255, 0)      # Green
        '&H0000FF00'
        >>> rgb_to_ass_color(0, 0, 255)      # Blue
        '&H00FF0000'
    """
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"

def ass_color_to_rgb(ass_color: str) -> Tuple[int, int, int, int]:
    """
    Parse ASS color format (&HAABBGGRR) to RGBA.

    Args:
        ass_color: ASS color string like "&H00FFFFFF"

    Returns:
        Tuple (r, g, b, alpha)
    """
    # Remove &H prefix
    hex_val = ass_color.replace("&H", "").replace("&h", "")

    # Pad to 8 characters if needed (some formats omit alpha)
    hex_val = hex_val.zfill(8)

    # Extract AABBGGRR
    alpha = int(hex_val[0:2], 16)
    blue = int(hex_val[2:4], 16)
    green = int(hex_val[4:6], 16)
    red = int(hex_val[6:8], 16)

    return (red, green, blue, alpha)

def ffmpeg_color_to_rgb(color: str) -> Tuple[int, int, int]:
    """
    Parse FFmpeg named or hex color to RGB.

    Args:
        color: Named color ("white") or hex ("#FFFFFF", "0xFFFFFF")

    Returns:
        Tuple (r, g, b)
    """
    # Named colors (subset)
    named_colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
    }

    if color.lower() in named_colors:
        return named_colors[color.lower()]

    # Parse hex
    hex_val = color.replace("#", "").replace("0x", "")
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)

    return (r, g, b)

# Common color presets (ASS format)
ASS_COLORS = {
    "white": "&H00FFFFFF",
    "black": "&H00000000",
    "red": "&H000000FF",
    "green": "&H0000FF00",
    "blue": "&H00FF0000",
    "yellow": "&H0000FFFF",
    "cyan": "&H00FFFF00",
    "magenta": "&H00FF00FF",
    "orange": "&H0000A5FF",  # RGB(255, 165, 0)
    "purple": "&H00800080",  # RGB(128, 0, 128)
}

# Transparency examples (ASS alpha channel)
ASS_ALPHA = {
    "opaque": 0x00,        # Fully opaque (0%)
    "transparent_10": 0x1A,  # 10% transparent
    "transparent_25": 0x40,  # 25% transparent
    "transparent_50": 0x80,  # 50% transparent (common for shadows)
    "transparent_75": 0xBF,  # 75% transparent
    "invisible": 0xFF,     # Fully transparent (100%)
}
```

## Color Format Comparison Chart

| Color | RGB | Hex (RGB) | ASS (&HAABBGGRR) | OpenCV BGR Array |
|-------|-----|-----------|------------------|------------------|
| White | (255,255,255) | #FFFFFF | &H00FFFFFF | [255,255,255] |
| Black | (0,0,0) | #000000 | &H00000000 | [0,0,0] |
| Red | (255,0,0) | #FF0000 | &H000000FF | [0,0,255] |
| Green | (0,255,0) | #00FF00 | &H0000FF00 | [0,255,0] |
| Blue | (0,0,255) | #0000FF | &H00FF0000 | [255,0,0] |
| Yellow | (255,255,0) | #FFFF00 | &H0000FFFF | [0,255,255] |
| Cyan | (0,255,255) | #00FFFF | &H00FFFF00 | [255,255,0] |
| Magenta | (255,0,255) | #FF00FF | &H00FF00FF | [255,0,255] |
| Orange | (255,165,0) | #FFA500 | &H0000A5FF | [0,165,255] |

---

# Section 2: Time Unit Conversions

## Critical: Three Different Time Systems

| Context | Unit | Python Type | Conversion Formula | Example |
|---------|------|-------------|-------------------|---------|
| **FFmpeg filters** (fade, xfade) | Seconds | `float` or `int` | N/A | `duration=1.5` |
| **ASS karaoke** (\k, \kf, \ko) | Centiseconds | `int` | `cs = seconds * 100` | `{\k50}` = 0.5s |
| **ASS animation** (\t, \fad, \move) | Milliseconds | `int` | `ms = seconds * 1000` | `\t(0,500,...)` = 0.5s |

## Time Conversion Functions

```python
from typing import Union

def seconds_to_centiseconds(seconds: float) -> int:
    """
    Convert seconds to centiseconds for ASS karaoke tags.

    Args:
        seconds: Time in seconds

    Returns:
        Centiseconds (1/100 second)

    Examples:
        >>> seconds_to_centiseconds(0.5)
        50
        >>> seconds_to_centiseconds(1.0)
        100
        >>> seconds_to_centiseconds(2.5)
        250
    """
    return int(seconds * 100)

def seconds_to_milliseconds(seconds: float) -> int:
    """
    Convert seconds to milliseconds for ASS animation tags.

    Args:
        seconds: Time in seconds

    Returns:
        Milliseconds (1/1000 second)

    Examples:
        >>> seconds_to_milliseconds(0.5)
        500
        >>> seconds_to_milliseconds(1.0)
        1000
        >>> seconds_to_milliseconds(0.2)
        200
    """
    return int(seconds * 1000)

def centiseconds_to_seconds(centiseconds: int) -> float:
    """
    Convert ASS karaoke centiseconds to seconds.

    Args:
        centiseconds: Duration in centiseconds

    Returns:
        Seconds
    """
    return centiseconds / 100.0

def milliseconds_to_seconds(milliseconds: int) -> float:
    """
    Convert ASS animation milliseconds to seconds.

    Args:
        milliseconds: Duration in milliseconds

    Returns:
        Seconds
    """
    return milliseconds / 1000.0

def format_ass_timestamp(seconds: float) -> str:
    """
    Format seconds as ASS timestamp (H:MM:SS.CC).

    Args:
        seconds: Time in seconds

    Returns:
        ASS timestamp string

    Examples:
        >>> format_ass_timestamp(1.5)
        '0:00:01.50'
        >>> format_ass_timestamp(65.25)
        '0:01:05.25'
        >>> format_ass_timestamp(3661.0)
        '1:01:01.00'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int((seconds % 1) * 100)

    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

def parse_ass_timestamp(timestamp: str) -> float:
    """
    Parse ASS timestamp to seconds.

    Args:
        timestamp: ASS timestamp like "0:00:05.50"

    Returns:
        Time in seconds

    Examples:
        >>> parse_ass_timestamp("0:00:01.50")
        1.5
        >>> parse_ass_timestamp("0:01:05.25")
        65.25
    """
    parts = timestamp.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    sec_parts = parts[2].split(".")
    seconds = int(sec_parts[0])
    centiseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0

    total = hours * 3600 + minutes * 60 + seconds + centiseconds / 100.0
    return total

# Quick conversion constants
SECOND_TO_CS = 100      # Centiseconds per second
SECOND_TO_MS = 1000     # Milliseconds per second
CS_TO_MS = 10           # Milliseconds per centisecond
```

## Common Duration Mappings

| Human Readable | Seconds | Centiseconds (ASS \k) | Milliseconds (ASS \t) |
|----------------|---------|----------------------|----------------------|
| 100ms (flash) | 0.1 | 10 | 100 |
| 250ms (quick) | 0.25 | 25 | 250 |
| 500ms (half second) | 0.5 | 50 | 500 |
| 1 second | 1.0 | 100 | 1000 |
| 1.5 seconds | 1.5 | 150 | 1500 |
| 2 seconds | 2.0 | 200 | 2000 |

---

# Section 3: FFmpeg drawtext Parameters

## Complete Parameter Type Reference

### Text Content

| Parameter | Python Type | Description | Example |
|-----------|-------------|-------------|---------|
| `text` | `str` | Text to display | `text='Hello World'` |
| `textfile` | `str` (path) | Path to text file | `textfile='/path/to/text.txt'` |

### Font Parameters

| Parameter | Python Type | Range/Format | Validation | Example |
|-----------|-------------|--------------|------------|---------|
| `fontfile` | `str` (path) | Absolute path to .ttf/.otf | File exists | `fontfile='/fonts/Arial.ttf'` |
| `fontsize` | `int` | 1-999 (practical: 12-200) | `1 <= size <= 999` | `fontsize=48` |
| `fontcolor` | `str` | Named or hex RGB | Valid color | `fontcolor='white'` |
| `fontcolor_expr` | `str` (expression) | Dynamic color expression | Valid FFmpeg expr | `fontcolor_expr='0xFFFFFF'` |

**CRITICAL:** `fontsize` MUST be `int`, not `str`. Common error:
```python
# ❌ WRONG:
drawtext(fontsize="24")

# ✅ CORRECT:
drawtext(fontsize=24)
```

### Position Parameters

| Parameter | Python Type | Format | Example |
|-----------|-------------|--------|---------|
| `x` | `str` or `int` | Pixel value or expression | `x=10` or `x='(w-tw)/2'` |
| `y` | `str` or `int` | Pixel value or expression | `y=50` or `y='h-th-20'` |

**Position Expression Variables:**
- `w`: Video width (pixels)
- `h`: Video height (pixels)
- `tw`: Text width (pixels)
- `th`: Text height (pixels)
- `t`: Time in seconds

```python
# Static position (int)
x=100, y=50

# Dynamic position (str expression)
x='(w-tw)/2'  # Centered horizontally
y='h-th-20'   # 20px from bottom

# Time-based animation (str expression)
x='w-mod(t*100,w+tw)'  # Scrolling ticker
```

### Styling Parameters

| Parameter | Python Type | Range | Example |
|-----------|-------------|-------|---------|
| `borderw` | `int` | 0-20 (practical) | `borderw=3` |
| `bordercolor` | `str` | Named or hex RGB | `bordercolor='black'` |
| `shadowx` | `int` | -50 to 50 (practical) | `shadowx=2` |
| `shadowy` | `int` | -50 to 50 (practical) | `shadowy=2` |
| `shadowcolor` | `str` | Named or hex RGB | `shadowcolor='black'` |
| `box` | `int` | 0 (off) or 1 (on) | `box=1` |
| `boxcolor` | `str` | Named/hex + alpha | `boxcolor='black@0.5'` |
| `boxborderw` | `int` | 0-50 | `boxborderw=5` |

**Alpha Transparency in Colors:**
```python
# Format: "color@opacity"
# opacity: 0.0 (transparent) to 1.0 (opaque)

boxcolor='black@0.5'      # 50% transparent black
shadowcolor='red@0.3'     # 30% opaque red
fontcolor='white@0.8'     # 80% opaque white
```

### Timing Parameters

| Parameter | Python Type | Format | Example |
|-----------|-------------|--------|---------|
| `enable` | `str` (expression) | Boolean expression | `enable='gte(t,2)'` |
| `alpha` | `str` (expression) | 0.0-1.0 | `alpha='min(1,t/2)'` |

**Timing Expressions:**
```python
# Show after 2 seconds
enable='gte(t,2)'

# Show between 2-5 seconds
enable='between(t,2,5)'

# Fade in over 1 second
alpha='min(1,t)'

# Fade out over last 2 seconds (10s video)
alpha='if(gt(t,8),1-(t-8)/2,1)'
```

---

# Section 4: ASS/SSA Subtitle Parameters

## ASS Style Definition

```python
from typing import NamedTuple

class ASSStyle(NamedTuple):
    """Type-safe ASS style definition."""
    name: str
    fontname: str
    fontsize: int
    primary_colour: str      # &HAABBGGRR format
    secondary_colour: str    # &HAABBGGRR format
    outline_colour: str      # &HAABBGGRR format
    back_colour: str         # &HAABBGGRR format (shadow)
    bold: int                # 0 or -1 (FFmpeg quirk: -1 for bold)
    italic: int              # 0 or 1
    underline: int           # 0 or 1
    strikeout: int           # 0 or 1
    scale_x: int             # Percentage (100 = normal)
    scale_y: int             # Percentage (100 = normal)
    spacing: int             # Letter spacing in pixels
    angle: float             # Rotation angle in degrees
    border_style: int        # 1 (outline) or 3 (opaque box)
    outline: float           # Outline width (0.0-4.0)
    shadow: float            # Shadow distance (0.0-4.0)
    alignment: int           # Numpad alignment (1-9)
    margin_l: int            # Left margin (pixels)
    margin_r: int            # Right margin (pixels)
    margin_v: int            # Vertical margin (pixels)
    encoding: int            # Character encoding (1=UTF-8)

def ass_style_to_string(style: ASSStyle) -> str:
    """
    Convert ASSStyle to ASS format string.

    Returns:
        ASS Style line
    """
    return (
        f"Style: {style.name},"
        f"{style.fontname},{style.fontsize},"
        f"{style.primary_colour},{style.secondary_colour},"
        f"{style.outline_colour},{style.back_colour},"
        f"{style.bold},{style.italic},{style.underline},{style.strikeout},"
        f"{style.scale_x},{style.scale_y},{style.spacing},{style.angle},"
        f"{style.border_style},{style.outline},{style.shadow},"
        f"{style.alignment},"
        f"{style.margin_l},{style.margin_r},{style.margin_v},"
        f"{style.encoding}"
    )

# Example usage
karaoke_style = ASSStyle(
    name="Karaoke",
    fontname="Arial Black",
    fontsize=72,
    primary_colour="&H00FFFFFF",  # White text (unhighlighted)
    secondary_colour="&H000000FF",  # Red text (highlighted)
    outline_colour="&H00000000",  # Black outline
    back_colour="&H80000000",     # 50% transparent black shadow
    bold=-1,                      # Bold (FFmpeg uses -1)
    italic=0,
    underline=0,
    strikeout=0,
    scale_x=100,
    scale_y=100,
    spacing=0,
    angle=0.0,
    border_style=1,               # Outline + shadow
    outline=3.0,                  # 3px outline
    shadow=2.0,                   # 2px shadow
    alignment=2,                  # Bottom center
    margin_l=10,
    margin_r=10,
    margin_v=50,                  # 50px from bottom
    encoding=1                    # UTF-8
)

print(ass_style_to_string(karaoke_style))
```

## ASS Parameter Ranges and Types

| Parameter | Python Type | Range | Unit | Notes |
|-----------|-------------|-------|------|-------|
| `fontsize` | `int` | 1-999 | Points | Screen-relative |
| `primary_colour` | `str` | &H00000000 - &HFFFFFFFF | ABGR hex | Text color |
| `secondary_colour` | `str` | &H00000000 - &HFFFFFFFF | ABGR hex | Karaoke fill |
| `outline_colour` | `str` | &H00000000 - &HFFFFFFFF | ABGR hex | Border color |
| `back_colour` | `str` | &H00000000 - &HFFFFFFFF | ABGR hex | Shadow color |
| `bold` | `int` | -1 (on), 0 (off) | Boolean | FFmpeg quirk: -1 for bold |
| `italic` | `int` | 0, 1 | Boolean | Standard |
| `scale_x`, `scale_y` | `int` | 1-1000 | Percentage | 100 = normal |
| `outline` | `float` | 0.0-4.0 | Pixels | Border width |
| `shadow` | `float` | 0.0-4.0 | Pixels | Shadow offset |
| `alignment` | `int` | 1-9 | Numpad | See alignment chart |

## ASS Alignment (Numpad Layout)

```
7 (top-left)      8 (top-center)      9 (top-right)
4 (middle-left)   5 (middle-center)   6 (middle-right)
1 (bottom-left)   2 (bottom-center)   3 (bottom-right)
```

```python
ASS_ALIGNMENT = {
    "bottom_left": 1,
    "bottom_center": 2,
    "bottom_right": 3,
    "middle_left": 4,
    "middle_center": 5,
    "middle_right": 6,
    "top_left": 7,
    "top_center": 8,
    "top_right": 9,
}
```

---

# Section 5: ASS Karaoke Tags

## Karaoke Tag Reference

| Tag | Name | Unit | Python Type | Range | Effect |
|-----|------|------|-------------|-------|--------|
| `\k` | Karaoke | Centiseconds | `int` | 0-9999 | Instant highlight |
| `\kf` / `\K` | Karaoke Fill | Centiseconds | `int` | 0-9999 | Progressive fill |
| `\ko` | Karaoke Outline | Centiseconds | `int` | 0-9999 | Outline sweep |

```python
def generate_karaoke_line(
    words: list[str],
    durations: list[float],  # In SECONDS
    style: str = "Karaoke"
) -> str:
    """
    Generate ASS karaoke dialogue line.

    Args:
        words: List of words/syllables
        durations: Duration for each word IN SECONDS
        style: ASS style name

    Returns:
        ASS dialogue line with karaoke tags

    Example:
        >>> generate_karaoke_line(
        ...     ["Hello", "world"],
        ...     [0.5, 0.6]
        ... )
        '{\\k50}Hello {\\k60}world'
    """
    # Convert seconds to centiseconds
    karaoke_tags = []
    for word, duration_sec in zip(words, durations):
        cs = int(duration_sec * 100)  # Centiseconds
        karaoke_tags.append(f"{{\\k{cs}}}{word}")

    return " ".join(karaoke_tags)

# Example usage
words = ["Never", "gonna", "give", "you", "up"]
durations = [0.8, 0.6, 0.6, 0.5, 0.7]  # seconds

karaoke_text = generate_karaoke_line(words, durations)
print(karaoke_text)
# Output: {\k80}Never {\k60}gonna {\k60}give {\k50}you {\k70}up
```

---

# Section 6: ASS Animation Tags

## Animation Tag Reference

| Tag | Format | Unit | Example | Description |
|-----|--------|------|---------|-------------|
| `\t` | `\t(t1,t2,tags)` | Milliseconds | `\t(0,500,\fscx120)` | Animate over time |
| `\fad` | `\fad(in,out)` | Milliseconds | `\fad(300,200)` | Fade in/out |
| `\move` | `\move(x1,y1,x2,y2,t1,t2)` | Milliseconds | `\move(0,0,100,100,0,1000)` | Move position |
| `\fscx`, `\fscy` | `\fscxN`, `\fscyN` | Percentage | `\fscx120\fscy120` | Scale X/Y |
| `\frz` | `\frzN` | Degrees | `\frz45` | Rotate (Z-axis) |
| `\c`, `\1c` | `\c&HBBGGRR&` | ABGR hex | `\c&HFF0000&` | Primary color |
| `\3c` | `\3c&HBBGGRR&` | ABGR hex | `\3c&H000000&` | Outline color |
| `\4c` | `\4c&HBBGGRR&` | ABGR hex | `\4c&H808080&` | Shadow color |

```python
from typing import List, Tuple

def create_scale_animation(
    duration_ms: int,
    start_scale: int = 80,
    peak_scale: int = 120,
    end_scale: int = 100
) -> str:
    """
    Create bounce scale animation (pop effect).

    Args:
        duration_ms: Total animation duration in MILLISECONDS
        start_scale: Initial scale percentage
        peak_scale: Peak scale (overshoot)
        end_scale: Final settled scale

    Returns:
        ASS animation tags

    Example:
        >>> create_scale_animation(400)
        '\\fscx80\\fscy80\\t(0,150,\\fscx120\\fscy120)\\t(150,300,\\fscx95\\fscy95)\\t(300,400,\\fscx100\\fscy100)'
    """
    t1 = int(duration_ms * 0.375)  # 37.5% to peak
    t2 = int(duration_ms * 0.75)   # 75% to settle
    t3 = duration_ms

    mid_scale = int((peak_scale + end_scale) / 2) - 5

    return (
        f"\\fscx{start_scale}\\fscy{start_scale}"
        f"\\t(0,{t1},\\fscx{peak_scale}\\fscy{peak_scale})"
        f"\\t({t1},{t2},\\fscx{mid_scale}\\fscy{mid_scale})"
        f"\\t({t2},{t3},\\fscx{end_scale}\\fscy{end_scale})"
    )

def create_fade_animation(
    fade_in_ms: int,
    fade_out_ms: int = 0
) -> str:
    """
    Create fade in/out animation.

    Args:
        fade_in_ms: Fade in duration in MILLISECONDS
        fade_out_ms: Fade out duration in MILLISECONDS (0 = no fade out)

    Returns:
        ASS fade tag

    Example:
        >>> create_fade_animation(300, 200)
        '\\fad(300,200)'
    """
    return f"\\fad({fade_in_ms},{fade_out_ms})"

def create_color_transition(
    start_color_rgb: Tuple[int, int, int],
    end_color_rgb: Tuple[int, int, int],
    duration_ms: int
) -> str:
    """
    Create smooth color transition animation.

    Args:
        start_color_rgb: Starting RGB color
        end_color_rgb: Ending RGB color
        duration_ms: Transition duration in MILLISECONDS

    Returns:
        ASS animation tags

    Example:
        >>> create_color_transition((255,255,255), (255,0,0), 1000)
        '\\c&H00FFFFFF&\\t(0,1000,\\c&H000000FF&)'
    """
    start_ass = rgb_to_ass_color(*start_color_rgb)[:-2] + "&"  # Remove last 2 chars, add &
    end_ass = rgb_to_ass_color(*end_color_rgb)[:-2] + "&"

    return f"\\c{start_ass}\\t(0,{duration_ms},\\c{end_ass})"

# Example: Complete animated karaoke line
def create_animated_karaoke_word(
    word: str,
    karaoke_duration_sec: float,
    pop_animation: bool = True
) -> str:
    """
    Create word with karaoke + pop animation.

    Args:
        word: Word text
        karaoke_duration_sec: Karaoke fill duration in SECONDS
        pop_animation: Add scale pop effect

    Returns:
        ASS karaoke word with animations
    """
    karaoke_cs = int(karaoke_duration_sec * 100)  # Centiseconds
    karaoke_ms = int(karaoke_duration_sec * 1000)  # Milliseconds

    if pop_animation:
        pop = create_scale_animation(karaoke_ms, 90, 115, 100)
        return f"{{\\k{karaoke_cs}{pop}}}{word}"
    else:
        return f"{{\\k{karaoke_cs}}}{word}"

# Usage
animated_line = " ".join([
    create_animated_karaoke_word("Never", 0.8, True),
    create_animated_karaoke_word("gonna", 0.6, True),
    create_animated_karaoke_word("give", 0.6, True),
    create_animated_karaoke_word("you", 0.5, True),
    create_animated_karaoke_word("up", 0.7, True),
])
```

---

# Section 7: ffmpeg-python Library Integration

## Type-Safe Filter Application

```python
import ffmpeg
from typing import Optional, Union

def apply_drawtext_filter(
    input_stream,
    text: str,
    fontsize: int,
    fontcolor: str = "white",
    x: Union[str, int] = 10,
    y: Union[str, int] = 10,
    fontfile: Optional[str] = None,
    borderw: int = 0,
    bordercolor: str = "black",
    shadowx: int = 0,
    shadowy: int = 0,
    shadowcolor: str = "black",
    box: int = 0,
    boxcolor: str = "black@0.5",
    boxborderw: int = 0,
    enable: Optional[str] = None,
    alpha: Optional[str] = None
):
    """
    Apply drawtext filter with type safety.

    Args:
        input_stream: ffmpeg input stream
        text: Text to display
        fontsize: Font size in points (int, 1-999)
        fontcolor: Color name or hex string
        x: X position (int or expression string)
        y: Y position (int or expression string)
        fontfile: Path to font file (optional)
        borderw: Border width (int, 0-20)
        bordercolor: Border color
        shadowx: Shadow X offset (int)
        shadowy: Shadow Y offset (int)
        shadowcolor: Shadow color
        box: Enable background box (0 or 1)
        boxcolor: Box color with alpha (e.g., "black@0.5")
        boxborderw: Box border width
        enable: Enable expression (e.g., "gte(t,2)")
        alpha: Alpha expression (e.g., "min(1,t)")

    Returns:
        ffmpeg stream with drawtext filter applied

    Raises:
        TypeError: If parameters have incorrect types
        ValueError: If parameters are out of valid range
    """
    # Type validation
    if not isinstance(fontsize, int):
        raise TypeError(f"fontsize must be int, got {type(fontsize).__name__}")

    if not (1 <= fontsize <= 999):
        raise ValueError(f"fontsize must be 1-999, got {fontsize}")

    if not isinstance(borderw, int) or borderw < 0:
        raise ValueError(f"borderw must be non-negative int, got {borderw}")

    if not isinstance(box, int) or box not in (0, 1):
        raise ValueError(f"box must be 0 or 1, got {box}")

    # Build filter parameters
    params = {
        "text": text,
        "fontsize": fontsize,
        "fontcolor": fontcolor,
        "x": x,
        "y": y,
        "borderw": borderw,
        "bordercolor": bordercolor,
        "box": box,
    }

    # Optional parameters
    if fontfile:
        params["fontfile"] = fontfile

    if shadowx != 0:
        params["shadowx"] = shadowx

    if shadowy != 0:
        params["shadowy"] = shadowy
        params["shadowcolor"] = shadowcolor

    if box == 1:
        params["boxcolor"] = boxcolor
        if boxborderw > 0:
            params["boxborderw"] = boxborderw

    if enable:
        params["enable"] = enable

    if alpha:
        params["alpha"] = alpha

    return input_stream.drawtext(**params)

# Example usage
input_file = ffmpeg.input("input.mp4")
output = apply_drawtext_filter(
    input_file,
    text="Hello World",
    fontsize=48,
    fontcolor="white",
    x="(w-tw)/2",
    y="(h-th)/2",
    borderw=2,
    bordercolor="black",
    shadowx=2,
    shadowy=2,
    enable="between(t,1,5)"
)
output = ffmpeg.output(output, "output.mp4")
ffmpeg.run(output)
```

## Complete Audio/Video Filter Example

```python
import ffmpeg
from pathlib import Path

def add_subtitles_with_audio(
    input_video: str,
    output_video: str,
    subtitle_text: str,
    fontsize: int = 48,
    crf: int = 18,
    audio_codec: str = "aac",
    audio_bitrate: str = "192k"
):
    """
    Add burned-in subtitles while preserving audio.

    CRITICAL: Always explicitly handle audio stream to prevent loss.

    Args:
        input_video: Input video path
        output_video: Output video path
        subtitle_text: Text to display
        fontsize: Font size (int)
        crf: Constant Rate Factor for H.264 (int, 0-51)
        audio_codec: Audio codec (default: "aac")
        audio_bitrate: Audio bitrate (default: "192k")
    """
    # Input
    input_file = ffmpeg.input(input_video)

    # Video processing
    video = input_file.video.drawtext(
        text=subtitle_text,
        fontsize=fontsize,
        fontcolor="white",
        x="(w-tw)/2",
        y="h-th-50",
        borderw=2,
        bordercolor="black"
    )

    # Audio passthrough (CRITICAL)
    audio = input_file.audio

    # Output with both streams
    output = ffmpeg.output(
        video,
        audio,
        output_video,
        vcodec="libx264",
        crf=crf,
        acodec=audio_codec,
        audio_bitrate=audio_bitrate
    )

    # Run
    output = output.overwrite_output()
    ffmpeg.run(output)
```

---

# Section 8: Subprocess Pattern with Pipes

## Frame-by-Frame Processing

```python
import subprocess
import numpy as np
from typing import Generator, Tuple

def read_video_frames(
    input_path: str,
    width: int,
    height: int,
    pix_fmt: str = "rgb24"
) -> Generator[np.ndarray, None, None]:
    """
    Read video frames using FFmpeg subprocess.

    Args:
        input_path: Input video file path
        width: Frame width
        height: Frame height
        pix_fmt: Pixel format ("rgb24" or "bgr24")

    Yields:
        NumPy array frames (height, width, 3)

    Example:
        >>> for frame in read_video_frames("input.mp4", 1920, 1080):
        ...     # Process frame (RGB format)
        ...     processed = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    """
    # FFmpeg command
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-f", "rawvideo",
        "-pix_fmt", pix_fmt,
        "-"  # Output to stdout
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=10**8
    )

    frame_size = width * height * 3

    try:
        while True:
            raw_frame = process.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                break

            # Convert to NumPy array
            frame = np.frombuffer(raw_frame, dtype=np.uint8)
            frame = frame.reshape((height, width, 3))

            yield frame
    finally:
        process.stdout.close()
        process.wait()

def write_video_frames(
    output_path: str,
    width: int,
    height: int,
    fps: float = 30.0,
    pix_fmt: str = "rgb24",
    crf: int = 18
) -> subprocess.Popen:
    """
    Create FFmpeg process for writing frames.

    Args:
        output_path: Output video file path
        width: Frame width
        height: Frame height
        fps: Frames per second
        pix_fmt: Pixel format ("rgb24" or "bgr24")
        crf: Constant Rate Factor (0-51)

    Returns:
        subprocess.Popen instance (write frames to .stdin)

    Example:
        >>> writer = write_video_frames("output.mp4", 1920, 1080, 30)
        >>> for frame in frames:
        ...     writer.stdin.write(frame.tobytes())
        >>> writer.stdin.close()
        >>> writer.wait()
    """
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", pix_fmt,
        "-r", str(fps),
        "-i", "-",  # Read from stdin
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        output_path
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    return process

# Complete pipeline example
def process_video_frames(
    input_path: str,
    output_path: str,
    process_fn: callable
):
    """
    Read, process, and write video frames.

    Args:
        input_path: Input video
        output_path: Output video
        process_fn: Function to process each frame
    """
    # Get video dimensions
    import cv2
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # Create writer
    writer = write_video_frames(output_path, width, height, fps)

    try:
        # Process frames
        for frame in read_video_frames(input_path, width, height):
            processed = process_fn(frame)
            writer.stdin.write(processed.tobytes())
    finally:
        writer.stdin.close()
        writer.wait()
```

---

# Section 9: Common Pitfalls and Solutions

## Pitfall 1: String vs Int for Numeric Parameters

```python
# ❌ WRONG - passing string for int parameter
import ffmpeg
ffmpeg.input("input.mp4").drawtext(
    text="Hello",
    fontsize="24"  # ❌ Should be int
).output("output.mp4")

# ✅ CORRECT
ffmpeg.input("input.mp4").drawtext(
    text="Hello",
    fontsize=24  # ✅ int
).output("output.mp4")
```

## Pitfall 2: RGB vs BGR Color Order

```python
# ❌ WRONG - using RGB for ASS color
def wrong_ass_color(r: int, g: int, b: int) -> str:
    return f"&H00{r:02X}{g:02X}{b:02X}"  # ❌ RGB order

# ✅ CORRECT - BGR order for ASS
def correct_ass_color(r: int, g: int, b: int) -> str:
    return f"&H00{b:02X}{g:02X}{r:02X}"  # ✅ BGR order

# Example: Pure red
print(wrong_ass_color(255, 0, 0))   # ❌ "&H00FF0000" = Blue in ASS!
print(correct_ass_color(255, 0, 0))  # ✅ "&H000000FF" = Red in ASS
```

## Pitfall 3: Centiseconds vs Milliseconds Confusion

```python
# ❌ WRONG - mixing units
def wrong_karaoke_timing():
    # Karaoke tag uses centiseconds
    # Animation uses milliseconds - DIFFERENT!
    return r"{\k100\t(0,100,\fscx120)}Word"  # ❌ Mismatch!
    # \k100 = 1 second
    # \t(0,100,...) = 0.1 seconds (100ms)

# ✅ CORRECT - consistent timing
def correct_karaoke_timing(duration_sec: float):
    cs = int(duration_sec * 100)   # Karaoke: centiseconds
    ms = int(duration_sec * 1000)  # Animation: milliseconds
    return rf"{{\k{cs}\t(0,{ms},\fscx120)}}Word"

print(correct_karaoke_timing(1.0))
# Output: {\k100\t(0,1000,\fscx120)}Word
# Both tags now represent 1 second ✅
```

## Pitfall 4: Forgetting Quotes on Expressions

```python
# ❌ WRONG - expression without quotes
import ffmpeg
ffmpeg.input("input.mp4").drawtext(
    text="Hello",
    x=(w-tw)/2  # ❌ Python evaluates this, causes NameError
)

# ✅ CORRECT - expression as string
ffmpeg.input("input.mp4").drawtext(
    text="Hello",
    x="(w-tw)/2"  # ✅ FFmpeg evaluates this at runtime
)
```

## Pitfall 5: Audio Stream Loss

```python
# ❌ WRONG - audio is silently dropped
import ffmpeg
input_file = ffmpeg.input("input.mp4")
(
    input_file
    .filter("scale", 1280, 720)  # ❌ Only video stream
    .output("output.mp4")
    .run()
)

# ✅ CORRECT - explicitly handle audio
input_file = ffmpeg.input("input.mp4")
video = input_file.video.filter("scale", 1280, 720)
audio = input_file.audio  # ✅ Preserve audio
ffmpeg.output(video, audio, "output.mp4").run()
```

## Pitfall 6: Incorrect ASS Bold Value

```python
# ❌ WRONG - using 1 for bold (works in some renderers, not all)
ass_style = f"Style: Default,Arial,48,&H00FFFFFF,...,1,..."  # ❌ May not work

# ✅ CORRECT - FFmpeg expects -1 for bold
ass_style = f"Style: Default,Arial,48,&H00FFFFFF,...,-1,..."  # ✅ Proper bold
```

---

# Section 10: Validation Helpers

```python
from typing import Union
import re

def validate_fontsize(size: int) -> int:
    """Validate fontsize parameter."""
    if not isinstance(size, int):
        raise TypeError(f"fontsize must be int, got {type(size).__name__}")
    if not (1 <= size <= 999):
        raise ValueError(f"fontsize must be 1-999, got {size}")
    return size

def validate_crf(crf: int, codec: str = "h264") -> int:
    """Validate CRF parameter."""
    if not isinstance(crf, int):
        raise TypeError(f"crf must be int, got {type(crf).__name__}")

    ranges = {
        "h264": (0, 51),
        "h265": (0, 51),
        "hevc": (0, 51),
        "vp9": (0, 63),
        "av1": (0, 63),
    }

    min_crf, max_crf = ranges.get(codec, (0, 51))
    if not (min_crf <= crf <= max_crf):
        raise ValueError(f"crf for {codec} must be {min_crf}-{max_crf}, got {crf}")

    return crf

def validate_ass_color(color: str) -> str:
    """Validate ASS color format."""
    pattern = r"^&H[0-9A-Fa-f]{8}$"
    if not re.match(pattern, color):
        raise ValueError(f"Invalid ASS color format: {color} (expected &HAABBGGRR)")
    return color

def validate_alignment(alignment: int) -> int:
    """Validate ASS alignment (1-9 numpad)."""
    if not isinstance(alignment, int):
        raise TypeError(f"alignment must be int, got {type(alignment).__name__}")
    if not (1 <= alignment <= 9):
        raise ValueError(f"alignment must be 1-9, got {alignment}")
    return alignment

def validate_ffmpeg_color(color: str) -> str:
    """Validate FFmpeg color (named or hex)."""
    named_colors = {
        "white", "black", "red", "green", "blue",
        "yellow", "cyan", "magenta", "orange", "purple"
    }

    if color.lower() in named_colors:
        return color

    # Validate hex format
    hex_pattern = r"^(#|0x)?[0-9A-Fa-f]{6}$"
    if re.match(hex_pattern, color):
        return color

    raise ValueError(f"Invalid FFmpeg color: {color}")

def validate_time_expression(expr: str) -> str:
    """Validate FFmpeg time expression syntax."""
    # Basic validation - check for common mistakes
    if not isinstance(expr, str):
        raise TypeError(f"Time expression must be str, got {type(expr).__name__}")

    # Check for unquoted expressions in Python (common mistake)
    if "w" in expr or "h" in expr or "tw" in expr or "th" in expr:
        # Likely an expression - ensure it's a string
        if not isinstance(expr, str):
            raise TypeError("FFmpeg expressions must be strings")

    return expr
```

---

# Section 11: Complete Working Examples

## Example 1: Type-Safe Karaoke Generator

```python
import ffmpeg
from typing import List, Tuple
from pathlib import Path

class KaraokeGenerator:
    """Type-safe karaoke subtitle generator."""

    def __init__(
        self,
        video_path: str,
        output_path: str,
        font_size: int = 72,
        font_name: str = "Arial Black",
        text_color_rgb: Tuple[int, int, int] = (255, 255, 255),
        highlight_color_rgb: Tuple[int, int, int] = (255, 0, 0)
    ):
        self.video_path = video_path
        self.output_path = output_path
        self.font_size = validate_fontsize(font_size)
        self.font_name = font_name
        self.text_color = rgb_to_ass_color(*text_color_rgb)
        self.highlight_color = rgb_to_ass_color(*highlight_color_rgb)

        self.lyrics: List[Tuple[float, List[Tuple[str, float]]]] = []

    def add_line(
        self,
        start_time: float,
        words: List[str],
        durations: List[float]
    ):
        """
        Add karaoke line.

        Args:
            start_time: Line start time in SECONDS
            words: List of words
            durations: Duration for each word in SECONDS
        """
        if len(words) != len(durations):
            raise ValueError("words and durations must have same length")

        self.lyrics.append((start_time, list(zip(words, durations))))

    def generate_ass(self) -> str:
        """Generate complete ASS subtitle file."""
        lines = [
            "[Script Info]",
            "Title: Karaoke Subtitles",
            "ScriptType: v4.00+",
            "PlayResX: 1920",
            "PlayResY: 1080",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding",
            (
                f"Style: Karaoke,{self.font_name},{self.font_size},"
                f"{self.text_color},{self.highlight_color},"
                "&H00000000,&H80000000,"
                "-1,0,0,0,100,100,0,0,1,3,2,2,10,10,50,1"
            ),
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]

        # Generate dialogue lines
        for start_time, word_durations in self.lyrics:
            # Calculate end time
            total_duration = sum(dur for _, dur in word_durations)
            end_time = start_time + total_duration

            # Generate karaoke tags (centiseconds)
            karaoke_text = ""
            for word, duration_sec in word_durations:
                cs = seconds_to_centiseconds(duration_sec)
                karaoke_text += f"{{\\k{cs}}}{word} "

            karaoke_text = karaoke_text.strip()

            # Format timestamps
            start_str = format_ass_timestamp(start_time)
            end_str = format_ass_timestamp(end_time)

            dialogue = f"Dialogue: 0,{start_str},{end_str},Karaoke,,0,0,0,,{karaoke_text}"
            lines.append(dialogue)

        return "\n".join(lines)

    def render(self, crf: int = 18):
        """Render video with karaoke subtitles."""
        # Generate ASS file
        ass_content = self.generate_ass()
        ass_path = Path(self.output_path).with_suffix(".ass")
        ass_path.write_text(ass_content, encoding="utf-8")

        # Apply subtitles with ffmpeg-python
        input_file = ffmpeg.input(self.video_path)
        video = input_file.video.filter("ass", str(ass_path))
        audio = input_file.audio

        output = ffmpeg.output(
            video,
            audio,
            self.output_path,
            vcodec="libx264",
            crf=validate_crf(crf),
            acodec="aac"
        )

        ffmpeg.run(output.overwrite_output())

        print(f"✅ Karaoke video saved: {self.output_path}")

# Usage example
karaoke = KaraokeGenerator(
    "input.mp4",
    "karaoke_output.mp4",
    font_size=80,
    text_color_rgb=(255, 255, 255),  # White
    highlight_color_rgb=(255, 0, 0)   # Red
)

# Add lyrics
karaoke.add_line(
    start_time=1.0,
    words=["Never", "gonna", "give", "you", "up"],
    durations=[0.8, 0.6, 0.6, 0.5, 0.7]
)

karaoke.add_line(
    start_time=4.3,
    words=["Never", "gonna", "let", "you", "down"],
    durations=[0.8, 0.6, 0.6, 0.5, 0.7]
)

# Render
karaoke.render(crf=18)
```

## Example 2: Dynamic Text Overlay with Type Safety

```python
import ffmpeg
from typing import Optional

class TextOverlay:
    """Type-safe text overlay builder."""

    def __init__(self, text: str):
        self.text = text
        self.fontsize: int = 48
        self.fontcolor: str = "white"
        self.x: str = "10"
        self.y: str = "10"
        self.borderw: int = 0
        self.bordercolor: str = "black"
        self.shadowx: int = 0
        self.shadowy: int = 0
        self.enable: Optional[str] = None
        self.alpha: Optional[str] = None

    def set_size(self, size: int) -> 'TextOverlay':
        """Set font size (fluent API)."""
        self.fontsize = validate_fontsize(size)
        return self

    def set_color(self, color: str) -> 'TextOverlay':
        """Set font color (fluent API)."""
        self.fontcolor = validate_ffmpeg_color(color)
        return self

    def center(self) -> 'TextOverlay':
        """Center text horizontally and vertically."""
        self.x = "(w-tw)/2"
        self.y = "(h-th)/2"
        return self

    def set_border(self, width: int, color: str = "black") -> 'TextOverlay':
        """Add text border."""
        if not isinstance(width, int) or width < 0:
            raise ValueError(f"Border width must be non-negative int")
        self.borderw = width
        self.bordercolor = validate_ffmpeg_color(color)
        return self

    def set_shadow(self, x: int, y: int, color: str = "black") -> 'TextOverlay':
        """Add text shadow."""
        self.shadowx = x
        self.shadowy = y
        return self

    def fade_in(self, duration: float) -> 'TextOverlay':
        """Add fade-in effect."""
        self.alpha = f"min(1,t/{duration})"
        return self

    def show_between(self, start: float, end: float) -> 'TextOverlay':
        """Show text between specific times."""
        self.enable = f"between(t,{start},{end})"
        return self

    def apply(self, stream) -> ffmpeg.Stream:
        """Apply text overlay to ffmpeg stream."""
        params = {
            "text": self.text,
            "fontsize": self.fontsize,
            "fontcolor": self.fontcolor,
            "x": self.x,
            "y": self.y,
        }

        if self.borderw > 0:
            params["borderw"] = self.borderw
            params["bordercolor"] = self.bordercolor

        if self.shadowx != 0 or self.shadowy != 0:
            params["shadowx"] = self.shadowx
            params["shadowy"] = self.shadowy

        if self.enable:
            params["enable"] = self.enable

        if self.alpha:
            params["alpha"] = self.alpha

        return stream.drawtext(**params)

# Usage with fluent API
input_file = ffmpeg.input("input.mp4")

overlay = (
    TextOverlay("Hello World")
    .set_size(72)
    .set_color("white")
    .center()
    .set_border(3, "black")
    .set_shadow(2, 2, "black")
    .fade_in(1.0)
    .show_between(1.0, 5.0)
)

output = overlay.apply(input_file)
output = ffmpeg.output(output, "output.mp4", vcodec="libx264", crf=18)
ffmpeg.run(output.overwrite_output())
```

---

# Summary: Type Safety Checklist

When integrating FFmpeg with Python:

## ✅ Always Use Correct Types

- [ ] `fontsize` → `int` (not `str`)
- [ ] `crf` → `int` (not `float`)
- [ ] `b:v`, `audio_bitrate` → `str` with unit ("5M", "192k")
- [ ] Color values → `str` (named or hex)
- [ ] Position expressions → `str` (quoted)
- [ ] Time values → `float` for seconds, `int` for frames

## ✅ Verify Unit Conversions

- [ ] ASS karaoke tags: seconds × 100 = centiseconds
- [ ] ASS animation tags: seconds × 1000 = milliseconds
- [ ] FFmpeg filters: use seconds directly

## ✅ Check Color Format

- [ ] FFmpeg drawtext: RGB hex or named
- [ ] ASS colors: BGR format (&HAABBGGRR)
- [ ] OpenCV: BGR array order

## ✅ Handle Audio Streams

- [ ] Always explicitly preserve audio with `.audio`
- [ ] Don't rely on automatic passthrough

## ✅ Validate Ranges

- [ ] CRF: 0-51 (H.264/H.265), 0-63 (VP9/AV1)
- [ ] Fontsize: 1-999 (practical: 12-200)
- [ ] Alignment: 1-9 (numpad layout)

---

This reference ensures type-safe, bug-free Python-FFmpeg integration with accurate parameter mappings and proper unit conversions.
