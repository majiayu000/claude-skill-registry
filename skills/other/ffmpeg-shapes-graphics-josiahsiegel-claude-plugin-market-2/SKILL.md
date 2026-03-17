---
name: ffmpeg-shapes-graphics
description: Complete shape and graphics overlay system. PROACTIVELY activate for: (1) Drawing rectangles (drawbox), (2) Grid overlays (drawgrid), (3) Circles and ellipses (geq), (4) Image watermarks and logos, (5) Lower third graphics, (6) Progress bars and indicators, (7) Animated overlays, (8) Blend modes and compositing, (9) Safe area guides, (10) Generated patterns (gradients, noise, checkerboards). Provides: Filter syntax reference, position expressions, color format guide, blend mode examples, performance optimization tips. Ensures: Professional graphics overlays and visual effects on video.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

## Quick Reference

| Shape | Filter | Command Example |
|-------|--------|-----------------|
| Rectangle | `drawbox` | `-vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=fill"` |
| Grid | `drawgrid` | `-vf "drawgrid=w=iw/3:h=ih/3:t=2:color=white"` |
| Text | `drawtext` | `-vf "drawtext=text='Hello':x=10:y=10:fontsize=24"` |
| Watermark | `overlay` | `[0:v][1:v]overlay=W-w-10:10` |

| Position | Expression |
|----------|------------|
| Centered | `x=(iw-200)/2:y=(ih-150)/2` |
| Bottom-right | `x=iw-w-10:y=ih-h-10` |
| Full-width bar | `x=0:y=0:w=iw:h=80` |

## When to Use This Skill

Use for **graphics and shape overlays**:
- Drawing rectangles, boxes, borders
- Adding watermarks and logos
- Lower third graphics
- Progress bars and indicators
- Grid overlays and safe area guides

---

# FFmpeg Shapes and Graphics (2025)

Complete guide to drawing shapes, graphics overlays, and geometric patterns using FFmpeg.

## Shape Drawing Filters

### Available Drawing Filters

| Filter | Purpose | Shapes |
|--------|---------|--------|
| drawbox | Draw rectangles/boxes | Rectangles, squares |
| drawgrid | Draw grid patterns | Lines, grids |
| drawtext | Draw text | Text, numbers |
| geq | Geometric equation | Any (via expressions) |
| overlay | Composite images | Any image/shape |
| blend | Blend layers | Composite effects |

## Drawing Boxes (drawbox)

### Basic Rectangle

```bash
# Draw red box
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=3" \
  output.mp4

# Filled rectangle
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=fill" \
  output.mp4

# Semi-transparent rectangle
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red@0.5:t=fill" \
  output.mp4
```

### Position Options

```bash
# Centered box
ffmpeg -i video.mp4 \
  -vf "drawbox=x=(iw-200)/2:y=(ih-150)/2:w=200:h=150:color=blue:t=fill" \
  output.mp4

# Box at bottom right
ffmpeg -i video.mp4 \
  -vf "drawbox=x=iw-210:y=ih-160:w=200:h=150:color=green:t=3" \
  output.mp4

# Full-width bar at top
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=0:w=iw:h=80:color=black@0.7:t=fill" \
  output.mp4

# Full-width bar at bottom
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=ih-80:w=iw:h=80:color=black@0.7:t=fill" \
  output.mp4
```

### Letterbox/Pillarbox

```bash
# Add letterbox bars (16:9 to 2.35:1)
ffmpeg -i video_16x9.mp4 \
  -vf "drawbox=x=0:y=0:w=iw:h=ih*0.12:color=black:t=fill,\
       drawbox=x=0:y=ih-ih*0.12:w=iw:h=ih*0.12:color=black:t=fill" \
  letterbox.mp4

# Add pillarbox bars (4:3 in 16:9 frame)
ffmpeg -i video_4x3.mp4 \
  -vf "scale=-1:1080,pad=1920:1080:(ow-iw)/2:0:black" \
  pillarbox.mp4
```

### Animated Boxes

```bash
# Growing box
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w='min(t*50,300)':h='min(t*30,200)':color=red:t=fill" \
  growing_box.mp4

# Moving box
ffmpeg -i video.mp4 \
  -vf "drawbox=x='mod(t*100,iw)':y=100:w=100:h=100:color=blue:t=fill" \
  moving_box.mp4

# Pulsing opacity
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red@'0.3+0.3*sin(t*3)':t=fill" \
  pulsing_box.mp4

# Box appears at specific time
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=yellow:t=fill:enable='between(t,2,5)'" \
  timed_box.mp4
```

### Multiple Boxes

```bash
# Border/frame effect
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=0:w=iw:h=20:color=white:t=fill,\
       drawbox=x=0:y=ih-20:w=iw:h=20:color=white:t=fill,\
       drawbox=x=0:y=0:w=20:h=ih:color=white:t=fill,\
       drawbox=x=iw-20:y=0:w=20:h=ih:color=white:t=fill" \
  bordered.mp4

# Grid of boxes
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=0:w=iw/3:h=ih/3:color=red@0.3:t=fill,\
       drawbox=x=iw/3:y=0:w=iw/3:h=ih/3:color=green@0.3:t=fill,\
       drawbox=x=2*iw/3:y=0:w=iw/3:h=ih/3:color=blue@0.3:t=fill" \
  color_grid.mp4
```

## Drawing Grids (drawgrid)

### Basic Grid

```bash
# Simple grid overlay
ffmpeg -i video.mp4 \
  -vf "drawgrid=w=100:h=100:t=1:color=white@0.5" \
  grid.mp4

# Rule of thirds grid
ffmpeg -i video.mp4 \
  -vf "drawgrid=w=iw/3:h=ih/3:t=2:color=white@0.7" \
  thirds.mp4

# Fine grid
ffmpeg -i video.mp4 \
  -vf "drawgrid=w=50:h=50:t=1:color=cyan@0.3" \
  fine_grid.mp4
```

### Crosshair/Center Marker

```bash
# Center crosshair
ffmpeg -i video.mp4 \
  -vf "drawbox=x=iw/2-1:y=0:w=2:h=ih:color=red:t=fill,\
       drawbox=x=0:y=ih/2-1:w=iw:h=2:color=red:t=fill" \
  crosshair.mp4

# Center circle marker (using multiple points)
ffmpeg -i video.mp4 \
  -vf "drawbox=x=iw/2-5:y=ih/2-5:w=10:h=10:color=red:t=2" \
  center_marker.mp4
```

## Drawing Circles and Ellipses (geq)

### Using geq Filter for Circles

```bash
# Draw circle outline
ffmpeg -i video.mp4 \
  -vf "geq=lum='if(between(sqrt(pow(X-iw/2,2)+pow(Y-ih/2,2)),100,105),255,lum(X,Y))':cb='cb(X,Y)':cr='cr(X,Y)'" \
  circle_outline.mp4

# Filled circle (white)
ffmpeg -i video.mp4 \
  -filter_complex "\
    color=c=white:s=1920x1080[c];\
    [c]geq=lum='if(lt(sqrt(pow(X-W/2,2)+pow(Y-H/2,2)),200),255,0)':cb=128:cr=128[mask];\
    [0:v][mask]overlay[v]" \
  -map "[v]" \
  filled_circle.mp4
```

### Using Overlay with Circle Images

```bash
# More practical: overlay a circle image
# First create circle image
ffmpeg -f lavfi \
  -i "color=c=red:s=200x200" \
  -vf "geq=lum='if(lt(sqrt(pow(X-100,2)+pow(Y-100,2)),100),255,0)':cb=128:cr=128,format=rgba,colorchannelmixer=aa='if(lt(sqrt(pow(X-100,2)+pow(Y-100,2)),100),1,0)'" \
  -frames:v 1 \
  circle.png

# Overlay circle on video
ffmpeg -i video.mp4 -i circle.png \
  -filter_complex "[0:v][1:v]overlay=100:100" \
  video_with_circle.mp4
```

### Generate Shape Patterns

```bash
# Radial gradient
ffmpeg -f lavfi \
  -i "color=c=black:s=500x500,geq=lum='255*sqrt(pow(X-W/2,2)+pow(Y-H/2,2))/(W/2)':cb=128:cr=128" \
  -frames:v 1 \
  radial_gradient.png

# Checkerboard pattern
ffmpeg -f lavfi \
  -i "color=c=white:s=800x800,geq=lum='if(mod(floor(X/100)+floor(Y/100),2),255,0)':cb=128:cr=128" \
  -frames:v 1 \
  checkerboard.png

# Diagonal stripes
ffmpeg -f lavfi \
  -i "color=c=black:s=800x600,geq=lum='if(mod(X+Y,100)<50,255,0)':cb=128:cr=128" \
  -frames:v 1 \
  stripes.png
```

## Image Overlays

### Basic Overlay

```bash
# Overlay logo at top-right corner
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[0:v][1:v]overlay=W-w-10:10" \
  watermarked.mp4

# Overlay at bottom-left
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[0:v][1:v]overlay=10:H-h-10" \
  watermarked.mp4

# Centered overlay
ffmpeg -i video.mp4 -i overlay.png \
  -filter_complex "[0:v][1:v]overlay=(W-w)/2:(H-h)/2" \
  centered.mp4
```

### Overlay with Transparency

```bash
# Scale and position logo with transparency
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [1:v]format=rgba,colorchannelmixer=aa=0.5[logo];\
    [0:v][logo]overlay=W-w-20:H-h-20" \
  watermark_50.mp4

# Fade in logo
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [1:v]format=rgba,fade=t=in:st=0:d=1:alpha=1[logo];\
    [0:v][logo]overlay=W-w-10:10:enable='gte(t,1)'" \
  fade_logo.mp4
```

### Animated Overlays

```bash
# Moving logo across screen
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [0:v][1:v]overlay=x='mod(t*100,W+w)-w':y=10" \
  scrolling_logo.mp4

# Bouncing logo
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [0:v][1:v]overlay=x='abs(mod(t*100,2*(W-w))-(W-w))':y='abs(mod(t*80,2*(H-h))-(H-h))'" \
  bouncing_logo.mp4

# Rotating overlay (using rotate filter)
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [1:v]rotate=t*PI/4:c=none:ow=200:oh=200[rot];\
    [0:v][rot]overlay=(W-200)/2:(H-200)/2" \
  rotating_logo.mp4
```

### Multiple Overlays

```bash
# Multiple logos/watermarks
ffmpeg -i video.mp4 -i logo1.png -i logo2.png \
  -filter_complex "\
    [0:v][1:v]overlay=10:10[tmp];\
    [tmp][2:v]overlay=W-w-10:10" \
  multi_logo.mp4

# Grid of thumbnails
ffmpeg -i main.mp4 -i thumb1.png -i thumb2.png -i thumb3.png -i thumb4.png \
  -filter_complex "\
    [1:v]scale=200:150[t1];[2:v]scale=200:150[t2];\
    [3:v]scale=200:150[t3];[4:v]scale=200:150[t4];\
    [0:v][t1]overlay=10:10[a];\
    [a][t2]overlay=220:10[b];\
    [b][t3]overlay=10:170[c];\
    [c][t4]overlay=220:170" \
  thumbnail_grid.mp4
```

## Text Graphics (drawtext)

### Styled Text

```bash
# Text with background box
ffmpeg -i video.mp4 \
  -vf "drawtext=text='LIVE':x=10:y=10:fontsize=36:fontcolor=white:\
       box=1:boxcolor=red:boxborderw=10" \
  live_badge.mp4

# Text with shadow
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Title':x=(w-tw)/2:y=50:fontsize=72:fontcolor=white:\
       shadowcolor=black:shadowx=3:shadowy=3" \
  title.mp4

# Text with outline
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Outlined':x=100:y=100:fontsize=64:fontcolor=yellow:\
       borderw=3:bordercolor=black" \
  outlined.mp4
```

### Lower Thirds

```bash
# Professional lower third
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=ih-120:w=400:h=100:color=0x1a1a2e@0.9:t=fill,\
       drawbox=x=0:y=ih-120:w=5:h=100:color=0x00ff88:t=fill,\
       drawtext=text='John Smith':x=20:y=ih-110:fontsize=32:fontcolor=white,\
       drawtext=text='Senior Developer':x=20:y=ih-70:fontsize=24:fontcolor=0xaaaaaa" \
  lower_third.mp4

# Animated lower third (slide in)
ffmpeg -i video.mp4 \
  -vf "drawbox=x='if(lt(t,1),-400+t*400,0)':y=ih-120:w=400:h=100:color=blue@0.8:t=fill:\
       enable='gte(t,0.5)',\
       drawtext=text='Guest Speaker':x='if(lt(t,1.2),-400+t*333,20)':y=ih-100:\
       fontsize=28:fontcolor=white:enable='gte(t,0.7)'" \
  animated_lower.mp4
```

### Timecode Display

```bash
# Timecode overlay
ffmpeg -i video.mp4 \
  -vf "drawtext=timecode='00\:00\:00\:00':rate=30:x=10:y=10:\
       fontsize=32:fontcolor=white:box=1:boxcolor=black@0.6" \
  with_timecode.mp4

# Frame counter
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Frame\: %{frame_num}':x=10:y=10:fontsize=24:fontcolor=white:\
       box=1:boxcolor=black@0.5" \
  frame_counter.mp4
```

## Progress Bars and Indicators

### Progress Bar

```bash
# Horizontal progress bar
ffmpeg -i video.mp4 \
  -vf "drawbox=x=50:y=ih-30:w=iw-100:h=10:color=gray@0.5:t=fill,\
       drawbox=x=50:y=ih-30:w='(iw-100)*t/10':h=10:color=red:t=fill" \
  progress_bar.mp4

# Circular progress (approximate with boxes)
# Note: True circular progress requires more complex expressions
```

### Loading Spinner (Approximation)

```bash
# Rotating indicator using drawbox
ffmpeg -i video.mp4 \
  -vf "drawbox=x='iw/2+50*cos(t*3)':y='ih/2+50*sin(t*3)':w=10:h=10:color=white:t=fill" \
  spinner.mp4
```

## Color Correction Overlays

### Vignette Effect

```bash
# Dark vignette
ffmpeg -i video.mp4 \
  -vf "vignette=PI/4" \
  vignette.mp4

# Custom vignette intensity
ffmpeg -i video.mp4 \
  -vf "vignette=angle=PI/4:mode=backward" \
  soft_vignette.mp4
```

### Color Tint Overlay

```bash
# Warm tint using blend
ffmpeg -i video.mp4 \
  -f lavfi -i "color=c=0xFF8800:s=1920x1080" \
  -filter_complex "[0:v][1:v]blend=all_mode=softlight:all_opacity=0.3" \
  warm_tint.mp4

# Cool tint
ffmpeg -i video.mp4 \
  -f lavfi -i "color=c=0x0088FF:s=1920x1080" \
  -filter_complex "[0:v][1:v]blend=all_mode=softlight:all_opacity=0.2" \
  cool_tint.mp4
```

## Blend Modes

### Available Blend Modes

| Mode | Effect |
|------|--------|
| addition | Add pixel values |
| multiply | Multiply (darken) |
| screen | Screen (lighten) |
| overlay | Overlay blend |
| softlight | Soft light |
| hardlight | Hard light |
| difference | Difference |
| exclusion | Exclusion |
| darken | Darken only |
| lighten | Lighten only |

### Blend Mode Examples

```bash
# Multiply blend (darken)
ffmpeg -i video.mp4 -i texture.png \
  -filter_complex "[0:v][1:v]blend=all_mode=multiply" \
  multiply.mp4

# Screen blend (lighten)
ffmpeg -i video.mp4 -i light_leak.png \
  -filter_complex "[0:v][1:v]blend=all_mode=screen" \
  light_leak.mp4

# Overlay blend
ffmpeg -i video.mp4 -i texture.png \
  -filter_complex "[0:v][1:v]blend=all_mode=overlay:all_opacity=0.5" \
  textured.mp4
```

## Safe Areas and Guides

### Broadcast Safe Areas

```bash
# Title safe (90%) and action safe (80%) guides
ffmpeg -i video.mp4 \
  -vf "drawbox=x=iw*0.05:y=ih*0.05:w=iw*0.9:h=ih*0.9:color=red:t=1,\
       drawbox=x=iw*0.1:y=ih*0.1:w=iw*0.8:h=ih*0.8:color=yellow:t=1" \
  safe_areas.mp4
```

### Aspect Ratio Guides

```bash
# 16:9 guide on 4:3 content
ffmpeg -i video_4x3.mp4 \
  -vf "drawbox=x=(iw-iw*0.75)/2:y=0:w=iw*0.75:h=ih:color=green:t=1" \
  aspect_guide.mp4

# 2.35:1 cinematic guide
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=ih*0.12:w=iw:h=ih*0.76:color=red:t=1" \
  cinematic_guide.mp4
```

## Masking

### Rectangle Mask

```bash
# Blur outside rectangle
ffmpeg -i video.mp4 \
  -filter_complex "\
    [0:v]split[a][b];\
    [a]boxblur=20[blur];\
    [b]crop=400:300:100:100[crop];\
    [blur][crop]overlay=100:100" \
  spotlight.mp4
```

### Using Alpha Mask

```bash
# Apply effect only to masked area
ffmpeg -i video.mp4 -i mask.png \
  -filter_complex "\
    [0:v]split[a][b];\
    [a]curves=preset=lighter[light];\
    [1:v]format=gray[mask];\
    [light][b][mask]maskedmerge" \
  masked_effect.mp4
```

## Generating Graphics Programmatically

### Color Bars and Test Patterns

```bash
# SMPTE color bars
ffmpeg -f lavfi -i "smptebars=size=1920x1080:duration=10" \
  -c:v libx264 -pix_fmt yuv420p \
  colorbars.mp4

# Test pattern with grid
ffmpeg -f lavfi -i "testsrc=size=1920x1080:duration=10" \
  -c:v libx264 -pix_fmt yuv420p \
  testpattern.mp4

# Solid color
ffmpeg -f lavfi -i "color=c=red:s=1920x1080:d=5" \
  -c:v libx264 -pix_fmt yuv420p \
  red.mp4
```

### Gradient Backgrounds

```bash
# Horizontal gradient
ffmpeg -f lavfi -i "gradients=s=1920x1080:c0=0x000033:c1=0x003366:duration=5" \
  -c:v libx264 -pix_fmt yuv420p \
  gradient.mp4

# Radial gradient (using geq)
ffmpeg -f lavfi \
  -i "color=c=black:s=1920x1080:d=5,geq=lum='255-255*sqrt(pow(X-W/2,2)+pow(Y-H/2,2))/sqrt(pow(W/2,2)+pow(H/2,2))':cb=128:cr=128" \
  -c:v libx264 -pix_fmt yuv420p \
  radial.mp4
```

### Noise and Texture

```bash
# Noise overlay
ffmpeg -f lavfi -i "nullsrc=size=1920x1080:duration=5,geq=lum='random(1)*255':cb=128:cr=128" \
  -c:v libx264 -pix_fmt yuv420p \
  noise.mp4

# Film grain effect
ffmpeg -i video.mp4 -f lavfi -i "nullsrc=size=1920x1080,geq=lum='random(1)*20+lum(X,Y)':cb=128:cr=128" \
  -filter_complex "[0:v][1:v]blend=all_mode=addition:all_opacity=0.1" \
  grainy.mp4
```

## Performance Tips

### Optimize Drawing Operations

```bash
# Use enable parameter to limit processing
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=fill:enable='between(t,5,10)'" \
  optimized.mp4

# Pre-render static graphics
# Instead of complex real-time drawing, overlay pre-made images
ffmpeg -i video.mp4 -i prerendered_graphic.png \
  -filter_complex "[0:v][1:v]overlay=10:10" \
  faster.mp4
```

### Hardware Acceleration

```bash
# Use hardware encoding for graphics-heavy output
ffmpeg -i video.mp4 \
  -vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=fill" \
  -c:v h264_nvenc -preset fast \
  output.mp4
```

## Troubleshooting

### Common Issues

**"Expression syntax error"**
```bash
# Escape special characters properly
# Use single quotes around expression values
ffmpeg -i video.mp4 \
  -vf "drawbox=x='iw/2':y='ih/2':w=100:h=100:color=red:t=fill" \
  output.mp4
```

**Overlay not visible**
```bash
# Check PNG has alpha channel
ffprobe -v error -select_streams v -show_entries stream=pix_fmt overlay.png

# Convert to RGBA if needed
ffmpeg -i overlay.png -pix_fmt rgba overlay_rgba.png
```

**Text not rendering**
```bash
# Specify font file explicitly
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Hello':fontfile=/path/to/font.ttf:fontsize=24:fontcolor=white" \
  output.mp4

# List available fonts
fc-list : family | sort | uniq
```

**Performance issues with complex filters**
```bash
# Reduce filter chain complexity
# Pre-render graphics
# Use lower resolution for preview
ffmpeg -i video.mp4 \
  -vf "scale=640:360,drawbox=..." \
  -preset ultrafast \
  preview.mp4
```

## Best Practices

### Design
1. Use transparency (RGBA) for overlays
2. Match overlay resolution to video
3. Use appropriate colors for visibility
4. Test on various backgrounds

### Performance
1. Pre-render complex graphics as images
2. Use enable parameter for timed effects
3. Limit filter chain length
4. Use hardware encoding for final output

### Accessibility
1. Ensure sufficient contrast for text
2. Avoid flashing/blinking elements
3. Keep important content within safe areas
4. Test at multiple resolutions

This guide covers FFmpeg shape and graphics operations. For subtitle and caption overlays, see the captions-subtitles skill.
