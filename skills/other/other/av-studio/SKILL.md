---
name: av-studio
description: Audio/video studio production — multi-track editing, color grading, motion graphics, compositing, live streaming, screen recording, YouTube publishing.
activationKeywords:
  - video editing
  - color grading
  - color correction
  - motion graphics
  - compositing
  - green screen
  - chroma key
  - screen recording
  - screencast
  - OBS
  - streaming
  - live stream
  - YouTube upload
  - YouTube publish
  - render
  - timeline
  - keyframe
  - transition
  - fade
  - crossfade
  - title card
  - lower third
  - intro
  - outro
  - B-roll
  - cutaway
  - jump cut
  - montage
  - timelapse
  - slow motion
  - stabilization
  - aspect ratio
  - letterbox
  - pip
  - picture in picture
type: skill
category: media
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/media/av-studio/SKILL.md
superseded_by: null
---
# AV Studio Production Skill

*Combines ffmpeg-media (codecs/formats), audio-engineering (mastering/mixing), and gource-visualizer (repo visualization) into a unified production toolkit for video content creation, live streaming, and multimedia publishing.*

## Production Templates

### YouTube Video Pipeline
```bash
# 1. Screen recording (with audio)
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :0.0 \
  -f pulse -i default \
  -c:v libx264 -preset ultrafast -crf 18 \
  -c:a aac -b:a 192k \
  raw_recording.mkv

# 2. Trim to content
ffmpeg -ss 00:00:05 -i raw_recording.mkv -to 00:45:00 -c copy trimmed.mkv

# 3. Add intro + outro
cat > concat.txt << EOF
file 'intro.mp4'
file 'trimmed.mkv'
file 'outro.mp4'
EOF
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -c:a aac assembled.mp4

# 4. Color grade + normalize audio
ffmpeg -i assembled.mp4 \
  -vf "eq=brightness=0.04:contrast=1.1:saturation=1.15,unsharp=5:5:0.5" \
  -af "loudnorm=I=-14:TP=-1:LRA=11" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  final.mp4

# 5. Generate thumbnail
ffmpeg -i final.mp4 -ss 00:00:30 -frames:v 1 \
  -vf "scale=1280:720" thumbnail.jpg
```

### Presentation Recording
```bash
# Record screen + webcam PiP
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :0.0 \
  -f v4l2 -video_size 320x240 -framerate 30 -i /dev/video0 \
  -f pulse -i default \
  -filter_complex "[0:v][1:v]overlay=W-w-20:H-h-20[out]" \
  -map "[out]" -map 2:a \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 128k \
  presentation.mp4
```

### Tutorial / Screencast
```bash
# Record with mouse cursor highlight
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 \
  -draw_mouse 1 -i :0.0 \
  -f pulse -i default \
  -c:v libx264 -preset fast -crf 20 \
  -c:a aac -b:a 128k \
  tutorial.mp4

# Add chapter markers (for YouTube)
ffmpeg -i tutorial.mp4 -c copy \
  -metadata:c:0 title="Introduction" \
  -metadata:c:0 timebase=1/1000 \
  chaptered.mp4
```

## Color Grading

### LUT Application
```bash
# Apply a 3D LUT (cube format)
ffmpeg -i input.mp4 -vf "lut3d=cinematic.cube" graded.mp4

# Apply with blend (50% strength)
ffmpeg -i input.mp4 -vf "split[a][b];[b]lut3d=cinematic.cube[c];[a][c]blend=all_opacity=0.5" graded.mp4
```

### Manual Color Correction
```bash
# Lift/Gamma/Gain (shadows/midtones/highlights)
ffmpeg -i input.mp4 -vf "\
  colorbalance=rs=0.1:gs=-0.05:bs=0.15:\
  rm=0:gm=0:bm=0:\
  rh=-0.05:gh=0:bh=0.05" \
  corrected.mp4

# White balance correction (warm up)
ffmpeg -i input.mp4 -vf "colortemperature=temperature=6500" warm.mp4

# Curves (S-curve for contrast)
ffmpeg -i input.mp4 -vf "curves=master='0/0 0.25/0.15 0.5/0.5 0.75/0.85 1/1'" contrast.mp4
```

## Motion Graphics

### Text Animations
```bash
# Fade-in title card (2 seconds)
ffmpeg -i input.mp4 -vf "\
  drawtext=text='Episode Title':\
  fontsize=72:fontcolor=white@0.0:\
  x=(w-text_w)/2:y=(h-text_h)/2:\
  alpha='if(lt(t,1),t,if(lt(t,3),1,if(lt(t,4),4-t,0)))'" \
  titled.mp4

# Lower third (name + title)
ffmpeg -i input.mp4 -vf "\
  drawbox=x=0:y=ih-120:w=500:h=120:color=black@0.7:t=fill,\
  drawtext=text='Jane Doe':fontsize=36:fontcolor=white:x=20:y=ih-110,\
  drawtext=text='Software Engineer':fontsize=24:fontcolor=0xcccccc:x=20:y=ih-65" \
  lower_third.mp4
```

### Transitions
```bash
# Crossfade between two clips (1 second overlap)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
  [0:v]trim=0:10,setpts=PTS-STARTPTS[v0];\
  [1:v]trim=0:10,setpts=PTS-STARTPTS[v1];\
  [v0][v1]xfade=transition=fade:duration=1:offset=9[vout];\
  [0:a]atrim=0:10,asetpts=PTS-STARTPTS[a0];\
  [1:a]atrim=0:10,asetpts=PTS-STARTPTS[a1];\
  [a0][a1]acrossfade=d=1[aout]" \
  -map "[vout]" -map "[aout]" crossfade.mp4

# Available xfade transitions:
# fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright,
# slideup, slidedown, circlecrop, circleopen, circleclose, dissolve,
# pixelize, diagtl, diagtr, diagbl, diagbr, hlslice, hrslice,
# vuslice, vdslice, hblur, fadegrays, squeezeh, squeezev
```

### Picture-in-Picture
```bash
# Webcam overlay (bottom right, 25% size)
ffmpeg -i screen.mp4 -i webcam.mp4 \
  -filter_complex "\
  [1:v]scale=iw/4:ih/4[pip];\
  [0:v][pip]overlay=W-w-20:H-h-20" \
  -c:v libx264 -crf 22 -c:a aac pip.mp4

# Animated PiP (slides in from right)
ffmpeg -i screen.mp4 -i webcam.mp4 \
  -filter_complex "\
  [1:v]scale=320:240[pip];\
  [0:v][pip]overlay=x='if(lt(t,1),W,W-w-20)':y=H-h-20" \
  animated_pip.mp4
```

## Video Stabilization
```bash
# Two-pass stabilization with vidstab
# Pass 1: analyze
ffmpeg -i shaky.mp4 -vf vidstabdetect=shakiness=5:accuracy=15 -f null -
# Pass 2: apply
ffmpeg -i shaky.mp4 -vf vidstabtransform=smoothing=10:input=transforms.trf stabilized.mp4
```

## Timelapse / Slow Motion
```bash
# Timelapse from photos (one frame per image)
ffmpeg -framerate 30 -pattern_type glob -i 'photos/*.jpg' \
  -c:v libx264 -crf 18 -pix_fmt yuv420p timelapse.mp4

# Speed ramp (normal → 4x → normal)
ffmpeg -i input.mp4 -filter_complex "\
  [0:v]trim=0:10,setpts=PTS-STARTPTS[v1];\
  [0:v]trim=10:30,setpts=0.25*(PTS-STARTPTS)[v2];\
  [0:v]trim=30:40,setpts=PTS-STARTPTS[v3];\
  [v1][v2][v3]concat=n=3:v=1:a=0[out]" \
  -map "[out]" speed_ramp.mp4

# Smooth slow motion (frame interpolation with minterpolate)
ffmpeg -i input.mp4 -vf "minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:vsbmc=1" \
  -r 30 slowmo.mp4
```

## Live Streaming
```bash
# Stream to YouTube via RTMP
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :0.0 \
  -f pulse -i default \
  -c:v libx264 -preset veryfast -maxrate 4500k -bufsize 9000k \
  -pix_fmt yuv420p -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"

# Stream to Twitch
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :0.0 \
  -f pulse -i default \
  -c:v libx264 -preset veryfast -maxrate 6000k -bufsize 12000k \
  -pix_fmt yuv420p -g 60 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv "rtmp://live.twitch.tv/app/YOUR_STREAM_KEY"
```

## Aspect Ratios

| Format | Ratio | Resolution | Use |
|--------|-------|-----------|-----|
| Widescreen | 16:9 | 1920x1080 | YouTube, presentations |
| Vertical | 9:16 | 1080x1920 | TikTok, Reels, Shorts |
| Square | 1:1 | 1080x1080 | Instagram feed |
| Ultrawide | 21:9 | 2560x1080 | Cinematic |
| Classic | 4:3 | 1440x1080 | Legacy, some webcams |
| Cinema | 2.39:1 | 2048x858 | Film standard |

### Letterboxing / Pillarboxing
```bash
# Add letterbox (16:9 → 21:9 cinematic bars)
ffmpeg -i input.mp4 -vf "pad=iw:iw*9/21:(ow-iw)/2:(oh-ih)/2:black" cinematic.mp4

# Convert vertical to horizontal (blur background)
ffmpeg -i vertical.mp4 -filter_complex "\
  [0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=20[bg];\
  [0:v]scale=-1:1080[fg];\
  [bg][fg]overlay=(W-w)/2:0" \
  horizontal_blurbg.mp4
```

## YouTube Publishing Checklist

1. **Video specs:** H.264, 1080p+, -14 LUFS audio, thumbnail 1280x720
2. **faststart:** `-movflags +faststart` for progressive download
3. **Pixel format:** `-pix_fmt yuv420p` for compatibility
4. **Chapters:** Include in description (00:00 Intro, 01:30 Topic, etc.)
5. **Thumbnail:** High-contrast, readable text at small sizes, faces perform well
6. **Subtitles:** SRT file or burn-in with `drawtext` filter
7. **End screen:** Last 20 seconds reserved for cards/end screen elements

## Related Skills & Agents

| Asset | Role |
|-------|------|
| `ffmpeg-media` skill | Codec/format foundation |
| `audio-engineering` skill | Audio mastering/mixing |
| `ffmpeg-processor` agent | Format conversion |
| `audio-engineer` agent | Audio mastering |
| `podcast-producer` agent | Podcast pipeline |
| `music-analyzer` agent | Audio analysis |
| `gource-visualizer` skill | Repository visualization → video |

## When This Skill Activates

- Video editing, trimming, concatenation with transitions
- Color grading and correction
- Motion graphics, titles, lower thirds
- Screen recording and screencasts
- Live streaming (YouTube, Twitch)
- Picture-in-picture compositing
- Video stabilization
- Timelapse and slow motion
- Aspect ratio conversion
- YouTube video publishing workflow
