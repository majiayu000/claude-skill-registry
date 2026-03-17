---
name: ffmpeg-transitions-effects
description: Complete video transition system. PROACTIVELY activate for: (1) xfade transitions (40+ types), (2) Fade in/out effects, (3) Crossfades and dissolves, (4) Wipe transitions (directional), (5) Slide and push effects, (6) Circle/iris transitions, (7) Multi-clip transition sequences, (8) Slideshow creation, (9) Custom transition expressions, (10) Audio crossfade synchronization. Provides: Complete xfade type reference, offset calculation formulas, multi-clip examples, custom expression guide, troubleshooting for resolution/framerate mismatches. Ensures: Smooth professional transitions between video clips.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

## Quick Reference

| Transition | Command |
|------------|---------|
| Crossfade | `[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]` |
| Dissolve | `xfade=transition=dissolve:duration=1:offset=4` |
| Wipe left | `xfade=transition=wipeleft:duration=1:offset=4` |
| Circle open | `xfade=transition=circleopen:duration=1.5:offset=4` |
| Slide left | `xfade=transition=slideleft:duration=1:offset=4` |
| Fade in/out | `-vf "fade=t=in:d=1,fade=t=out:st=9:d=1"` |
| Audio crossfade | `[0:a][1:a]acrossfade=d=1[a]` |

| Offset Formula | For N clips with transition T |
|----------------|-------------------------------|
| offset1 | `clip1_duration - T` |
| offset2 | `2*duration - 2*T` |
| offsetN | `N*duration - N*T` |

## When to Use This Skill

Use for **video transition workflows**:
- Joining clips with professional transitions
- Creating slideshows from images
- Adding fade in/out effects
- Multi-clip sequence editing
- Custom transition expressions

---

# FFmpeg Transitions and Effects (2025)

Complete guide to video transitions, crossfades, and creative effects using FFmpeg.

## Transition Overview

### Available Methods

| Method | Use Case | Complexity |
|--------|----------|------------|
| xfade filter | Between two clips | Medium |
| fade filter | Single clip in/out | Simple |
| blend filter | Frame blending | Simple |
| overlay + alpha | Custom transitions | Advanced |

### xfade Transition Types

FFmpeg's xfade filter supports 40+ built-in transitions:

| Category | Transitions |
|----------|-------------|
| Fades | fade, fadeblack, fadewhite, fadegrays |
| Wipes | wipeleft, wiperight, wipeup, wipedown, wipetl, wipetr, wipebl, wipebr |
| Slides | slideleft, slideright, slideup, slidedown |
| Reveals | revealright, revealleft, revealup, revealdown |
| Pushes | horzopen, horzclose, vertopen, vertclose |
| Circles | circleopen, circleclose, circlecrop |
| Rectangles | rectcrop, hblur, radial |
| Diagonals | diagtl, diagtr, diagbl, diagbr |
| Pixel Effects | dissolve, pixelize, hlslice, hrslice, vuslice, vdslice |
| Other | zoomin, squeezeh, squeezev, hlwind, hrwind, vuwind, vdwind, coverleft, coverright, coverup, coverdown |

## Basic Fade Effects

### Fade In/Out (Single Clip)

```bash
# Fade in from black (first 2 seconds)
ffmpeg -i video.mp4 \
  -vf "fade=t=in:st=0:d=2" \
  -c:a copy \
  fade_in.mp4

# Fade out to black (last 2 seconds)
ffmpeg -i video.mp4 \
  -vf "fade=t=out:st=8:d=2" \
  -c:a copy \
  fade_out.mp4

# Both fade in and fade out
ffmpeg -i video.mp4 \
  -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" \
  -c:a copy \
  fade_both.mp4

# Fade to white instead of black
ffmpeg -i video.mp4 \
  -vf "fade=t=out:st=8:d=2:color=white" \
  -c:a copy \
  fade_white.mp4
```

### Fade with Audio

```bash
# Video and audio fade in/out together
ffmpeg -i video.mp4 \
  -vf "fade=t=in:st=0:d=2,fade=t=out:st=8:d=2" \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=8:d=2" \
  fade_complete.mp4

# Audio crossfade between two files
ffmpeg -i audio1.mp3 -i audio2.mp3 \
  -filter_complex "[0][1]acrossfade=d=3:c1=tri:c2=tri" \
  crossfade.mp3
```

## xfade Transitions (Between Clips)

### Basic xfade Usage

```bash
# Simple crossfade between two clips
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v];\
                   [0:a][1:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" \
  output.mp4
```

**Parameters:**
- `transition`: Type of transition effect
- `duration`: Transition duration in seconds
- `offset`: When to start transition (from first clip)

### Common Transition Effects

```bash
# Dissolve (pixel-based crossfade)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=dissolve:duration=1:offset=4[v]" \
  -map "[v]" dissolve.mp4

# Wipe left to right
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=wipeleft:duration=1:offset=4[v]" \
  -map "[v]" wipe_left.mp4

# Wipe right to left
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=wiperight:duration=1:offset=4[v]" \
  -map "[v]" wipe_right.mp4

# Slide left
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=slideleft:duration=1:offset=4[v]" \
  -map "[v]" slide_left.mp4

# Circle open (iris)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=circleopen:duration=1.5:offset=4[v]" \
  -map "[v]" circle_open.mp4

# Circle close
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=circleclose:duration=1.5:offset=4[v]" \
  -map "[v]" circle_close.mp4

# Radial wipe
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=radial:duration=1.5:offset=4[v]" \
  -map "[v]" radial.mp4

# Zoom in
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=zoomin:duration=1:offset=4[v]" \
  -map "[v]" zoom_in.mp4

# Pixelize transition
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=pixelize:duration=1:offset=4[v]" \
  -map "[v]" pixelize.mp4

# Diagonal wipe (top-left to bottom-right)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=diagtl:duration=1:offset=4[v]" \
  -map "[v]" diag_tl.mp4

# Horizontal blur
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=hblur:duration=1:offset=4[v]" \
  -map "[v]" hblur.mp4
```

### All xfade Transition Types

```bash
# Fades
fade        # Standard crossfade
fadeblack   # Fade through black
fadewhite   # Fade through white
fadegrays   # Fade through gray

# Wipes
wipeleft    # Left to right wipe
wiperight   # Right to left wipe
wipeup      # Bottom to top wipe
wipedown    # Top to bottom wipe
wipetl      # Wipe from top-left corner
wipetr      # Wipe from top-right corner
wipebl      # Wipe from bottom-left corner
wipebr      # Wipe from bottom-right corner

# Slides
slideleft   # Slide new clip from right
slideright  # Slide new clip from left
slideup     # Slide new clip from bottom
slidedown   # Slide new clip from top

# Reveals
revealleft  # Reveal from right edge
revealright # Reveal from left edge
revealup    # Reveal from bottom edge
revealdown  # Reveal from top edge

# Open/Close
horzopen    # Horizontal opening (curtain)
horzclose   # Horizontal closing
vertopen    # Vertical opening
vertclose   # Vertical closing
circleopen  # Circle iris open
circleclose # Circle iris close

# Shapes
circlecrop  # Circle crop transition
rectcrop    # Rectangle crop transition
radial      # Radial/clock wipe

# Diagonals
diagtl      # Diagonal from top-left
diagtr      # Diagonal from top-right
diagbl      # Diagonal from bottom-left
diagbr      # Diagonal from bottom-right

# Pixel Effects
dissolve    # Random pixel dissolve
pixelize    # Pixelization effect
hlslice     # Horizontal left slice
hrslice     # Horizontal right slice
vuslice     # Vertical up slice
vdslice     # Vertical down slice

# Other
zoomin      # Zoom into new clip
squeezeh    # Horizontal squeeze
squeezev    # Vertical squeeze
hlwind      # Horizontal left wind
hrwind      # Horizontal right wind
vuwind      # Vertical up wind
vdwind      # Vertical down wind
coverleft   # Cover from right
coverright  # Cover from left
coverup     # Cover from bottom
coverdown   # Cover from top
```

## Multiple Clip Transitions

### Three Clips with Transitions

```bash
# Calculate offsets: clip1=5s, clip2=5s, clip3=5s, transition=1s
# offset1 = clip1_duration - transition = 5-1 = 4
# offset2 = clip1_duration + clip2_duration - 2*transition = 5+5-2 = 8

ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=4[v1];\
    [v1][2:v]xfade=transition=fade:duration=1:offset=8[v];\
    [0:a][1:a]acrossfade=d=1[a1];\
    [a1][2:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" \
  three_clips.mp4
```

### Slideshow with Transitions

```bash
#!/bin/bash
# slideshow.sh - Create slideshow from images with transitions

DURATION=3      # Each image duration
TRANSITION=1    # Transition duration
FPS=30

# Generate input commands
inputs=""
for img in *.jpg; do
    inputs="$inputs -loop 1 -t $DURATION -i $img"
done

# Calculate filter for 4 images
# Adjust offsets based on image count
ffmpeg $inputs \
  -filter_complex "\
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=$FPS[v0];\
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=$FPS[v1];\
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=$FPS[v2];\
    [3:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=$FPS[v3];\
    [v0][v1]xfade=transition=fade:duration=$TRANSITION:offset=$((DURATION-TRANSITION))[x1];\
    [x1][v2]xfade=transition=wipeleft:duration=$TRANSITION:offset=$((2*DURATION-2*TRANSITION))[x2];\
    [x2][v3]xfade=transition=circleopen:duration=$TRANSITION:offset=$((3*DURATION-3*TRANSITION))[v]" \
  -map "[v]" -c:v libx264 -pix_fmt yuv420p \
  slideshow.mp4
```

### Different Transitions per Cut

```bash
# Use different transitions between each clip
ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 -i clip4.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=4[x1];\
    [x1][2:v]xfade=transition=wipeleft:duration=1:offset=8[x2];\
    [x2][3:v]xfade=transition=circleopen:duration=1.5:offset=12[v]" \
  -map "[v]" \
  varied_transitions.mp4
```

## Custom Transitions with Expressions

### Custom xfade Expression

```bash
# Custom diagonal wipe with easing
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=custom:duration=1:offset=4:\
    expr='if(gt(X+Y,W+H*P),B,A)'[v]" \
  -map "[v]" custom_diag.mp4

# Smooth custom fade
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=custom:duration=1:offset=4:\
    expr='A*(1-P)+B*P'[v]" \
  -map "[v]" smooth_fade.mp4

# Circular reveal with custom center
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=custom:duration=1.5:offset=4:\
    expr='if(gt(sqrt(pow(X-W/2,2)+pow(Y-H/2,2)),P*sqrt(pow(W/2,2)+pow(H/2,2))),A,B)'[v]" \
  -map "[v]" circle_reveal.mp4
```

### Expression Variables

| Variable | Description |
|----------|-------------|
| X | Current pixel X coordinate |
| Y | Current pixel Y coordinate |
| W | Frame width |
| H | Frame height |
| P | Progress (0 to 1) |
| A | First clip pixel value |
| B | Second clip pixel value |

## Advanced Transition Techniques

### Luma/Alpha Matte Transitions

```bash
# Using a gradient image as transition mask
ffmpeg -i clip1.mp4 -i clip2.mp4 -loop 1 -i gradient.png \
  -filter_complex "\
    [0:v]format=rgba[a];\
    [1:v]format=rgba[b];\
    [2:v]format=gray,scale=1920:1080[mask];\
    [a][b][mask]maskedmerge[v]" \
  -map "[v]" -t 5 \
  luma_transition.mp4
```

### Motion Blur Transition

```bash
# Add motion blur during transition
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]split[a1][a2];\
    [1:v]split[b1][b2];\
    [a1][b1]xfade=transition=fade:duration=1:offset=4[fade];\
    [fade]tblend=all_mode=average:all_opacity=0.5[v]" \
  -map "[v]" \
  blur_transition.mp4
```

### Push/Reveal Transition

```bash
# Push left (new clip pushes old off screen)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]fps=30[a];\
    [1:v]fps=30[b];\
    [a][b]xfade=transition=slideleft:duration=0.5:offset=4.5[v]" \
  -map "[v]" \
  push_left.mp4

# Cover transition (new clip covers old)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=coverright:duration=0.75:offset=4.25[v]" \
  -map "[v]" \
  cover_right.mp4
```

### Zoom with Ken Burns Effect

```bash
# Zoom transition with motion
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]scale=2*iw:-1,zoompan=z='min(zoom+0.0015,1.5)':d=150:s=1920x1080[a];\
    [1:v][a]xfade=transition=zoomin:duration=1:offset=4[v]" \
  -map "[v]" -t 6 \
  zoom_transition.mp4
```

## Transition with Text/Graphics

### Title Card Transition

```bash
# Fade to title card, then fade to next clip
ffmpeg -i clip1.mp4 \
  -f lavfi -i "color=c=black:s=1920x1080:d=3" \
  -i clip2.mp4 \
  -filter_complex "\
    [1:v]drawtext=text='Chapter 2':fontsize=72:fontcolor=white:x=(w-tw)/2:y=(h-th)/2[title];\
    [0:v][title]xfade=transition=fadeblack:duration=1:offset=4[x1];\
    [x1][2:v]xfade=transition=fadeblack:duration=1:offset=6[v]" \
  -map "[v]" \
  title_transition.mp4
```

### Lower Third Transition

```bash
# Animate lower third with clip transition
ffmpeg -i clip1.mp4 -i clip2.mp4 -i lower_third.png \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=4[bg];\
    [2:v]format=rgba[lt];\
    [bg][lt]overlay=x=50:y=H-h-50:enable='between(t,1,4)'[v]" \
  -map "[v]" \
  lower_third_trans.mp4
```

## Performance Optimization

### Hardware-Accelerated Transitions

```bash
# Use NVENC for faster encoding after transition
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" \
  -c:v h264_nvenc -preset fast \
  output.mp4

# Hardware decode + CPU transition + hardware encode
ffmpeg -hwaccel cuda -i clip1.mp4 -hwaccel cuda -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=dissolve:duration=1:offset=4[v]" \
  -map "[v]" \
  -c:v h264_nvenc \
  output.mp4
```

### Optimize for Preview

```bash
# Lower resolution preview
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]scale=640:360[a];\
    [1:v]scale=640:360[b];\
    [a][b]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" \
  -c:v libx264 -preset ultrafast \
  preview.mp4
```

## Troubleshooting

### Common Issues

**"Discordant resolution" error**
```bash
# Ensure both clips have same resolution
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[a];\
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[b];\
    [a][b]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" output.mp4
```

**"Input streams have different frame rates" warning**
```bash
# Normalize frame rates
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]fps=30[a];\
    [1:v]fps=30[b];\
    [a][b]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" output.mp4
```

**Offset calculation for multiple clips**
```
For clips of duration D with transition T:
- offset1 = D - T
- offset2 = 2D - 2T
- offset3 = 3D - 3T
- offsetN = N*D - N*T
```

**Audio doesn't match video transition**
```bash
# Sync audio crossfade with video xfade
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=4[v];\
    [0:a][1:a]acrossfade=d=1:c1=tri:c2=tri[a]" \
  -map "[v]" -map "[a]" \
  output.mp4
```

### Verification Commands

```bash
# Check clip durations before creating transitions
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 clip1.mp4

# Check frame rate
ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 clip1.mp4

# Check resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 clip1.mp4
```

## Best Practices

### Timing
1. Standard transition duration: 0.5-1.5 seconds
2. Match transition style to content mood
3. Use consistent transitions within a sequence
4. Avoid overly long transitions (>2 seconds)

### Quality
1. Normalize resolution and frame rate before transitions
2. Use high-quality presets for final render
3. Test transitions at full resolution before batch processing
4. Consider color matching between clips

### Style Guidelines
1. Fade/dissolve: Universal, professional
2. Wipes: Energetic, action content
3. Slides/pushes: Modern, dynamic
4. Circle/iris: Dramatic, theatrical
5. Pixelize/blur: Creative, artistic

This guide covers FFmpeg transitions. For drawing shapes and graphics, see the shapes-graphics skill.
