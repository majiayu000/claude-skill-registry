---
name: processing-video
description: "Audio and video processing with ffmpeg. Use when: user asks to convert, trim, merge, compress, or transcode video or audio files; extract audio from video; create GIFs or animated WebP from video; add subtitles or watermarks to video; change video resolution, framerate, or codec; normalize audio loudness; extract frames from video; concatenate clips; create thumbnails from video; strip or add audio tracks; convert between audio formats (MP3, AAC, FLAC, Opus, WAV); adjust volume; apply video filters; stabilize shaky video; generate waveform or spectrum visualizations; probe media file metadata. Triggers on 'ffmpeg', 'video', 'audio', 'transcode', 'MP4', 'MKV', 'WebM', 'MP3', 'AAC', 'FLAC', 'Opus', 'WAV', 'GIF from video', 'extract audio', 'add subtitles', 'video to gif', 'compress video', 'trim video', 'merge videos', 'normalize audio', 'framerate', 'resolution', 'bitrate', 'codec', 'ffprobe', 'waveform', 'spectrogram'."
metadata:
  version: 0.1.0
---

# ffmpeg Toolkit

ffmpeg 6.1.1 is pre-installed with a full-featured build. Also available: **ffprobe** (media analysis) and **ffplay** (playback, limited use in container).

Before writing custom Python for media tasks, check whether ffmpeg handles it in a single command.

## Task Reference

### Probe & Inspect Media
**ffprobe** — always start here to understand what you're working with.
```
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
ffprobe -v quiet -show_entries format=duration,bit_rate -of csv=p=0 input.mp4
ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -of csv=p=0 input.mp4
```

### Video Format Conversion
```
ffmpeg -i input.avi output.mp4                             # container swap (re-encode)
ffmpeg -i input.avi -c copy output.mp4                     # container swap (no re-encode, fast)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 output.mp4       # H.265
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 out.webm  # VP9 WebM
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 35 output.mp4     # AV1 (SVT, fastest AV1 encoder)
ffmpeg -i input.mp4 -c:v libjxl output.jxl                # JPEG XL (single frame)
```

**Encoder selection guide:**
| Goal | Encoder | Typical flags |
|---|---|---|
| Compatibility | libx264 | `-crf 23 -preset medium` |
| Better compression | libx265 | `-crf 28 -preset medium` |
| Web delivery | libvpx-vp9 | `-crf 30 -b:v 0` |
| Best compression | libsvtav1 | `-crf 35 -preset 6` |
| Lossless archival | libx264 | `-crf 0 -preset veryslow` |

Lower CRF = higher quality. x264 default 23, x265 default 28, SVT-AV1 default 35 are visually similar.

### Audio Format Conversion
```
ffmpeg -i input.wav -c:a libmp3lame -q:a 2 output.mp3     # MP3 VBR ~190kbps
ffmpeg -i input.wav -c:a libopus -b:a 128k output.opus    # Opus (best quality/size)
ffmpeg -i input.wav -c:a aac -b:a 192k output.m4a         # AAC
ffmpeg -i input.wav -c:a flac output.flac                  # FLAC lossless
ffmpeg -i input.mp3 -ar 44100 -ac 2 output.wav            # to WAV, set sample rate/channels
```

### Extract Audio from Video
```
ffmpeg -i video.mp4 -vn -c:a copy audio.aac               # extract without re-encoding
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3  # extract as MP3
ffmpeg -i video.mp4 -vn -c:a libopus -b:a 128k audio.opus
```

### Trim & Cut
```
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:00 -c copy clip.mp4        # fast, keyframe-aligned
ffmpeg -ss 00:01:30 -i input.mp4 -to 00:01:30 -c copy clip.mp4        # -ss before -i = faster seek
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:00 -c:v libx264 -c:a aac clip.mp4  # frame-accurate (re-encode)
```
`-ss` before `-i` seeks by keyframe (fast, may be imprecise). After `-i` decodes from start (slow, precise). For frame-accurate cuts, re-encode.

### Concatenate / Merge
**Demuxer method** (same codec, no re-encode):
```
# Create file list
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy merged.mp4
```
**Filter method** (different formats, re-encodes):
```
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" merged.mp4
```

### Resize & Scale
```
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4                   # exact size
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4                    # width 1280, auto height
ffmpeg -i input.mp4 -vf "scale=-1:720:flags=lanczos" output.mp4       # height 720, Lanczos
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4                  # half size
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4  # letterbox to 1080p
```

### Framerate
```
ffmpeg -i input.mp4 -r 30 output.mp4                       # simple (drops/dupes frames)
ffmpeg -i input.mp4 -vf "fps=24" output.mp4                # filter-based
ffmpeg -i input.mp4 -vf "minterpolate=fps=60" output.mp4   # motion interpolation (slow)
```

### Animated GIF from Video
Use the two-pass palette method for quality:
```
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -i palette.png -lavfi "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```
Single-pass (simpler, lower quality):
```
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif
```

### Animated WebP from Video
```
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1" -c:v libwebp -lossless 0 -q:v 75 -loop 0 output.webp
```

### Extract Frames
```
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png             # 1 frame/second
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframe_%04d.png  # keyframes only
ffmpeg -i input.mp4 -vf "thumbnail=300" -frames:v 1 thumb.png   # best thumbnail from first 300 frames
ffmpeg -ss 00:00:05 -i input.mp4 -frames:v 1 screenshot.png     # single frame at timestamp
```

### Subtitles
```
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4           # burn in SRT
ffmpeg -i input.mp4 -vf "ass=subs.ass" output.mp4                 # burn in ASS (styled)
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s mov_text output.mp4  # soft subs in MP4
```
Subtitle rendering uses **libass** (full ASS/SSA styling support).

### Text & Watermark Overlays
```
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':fontsize=48:fontcolor=white:x=10:y=10" output.mp4
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4
ffmpeg -i input.mp4 -vf "drawtext=text='%{pts\:hms}':fontsize=24:fontcolor=white:x=10:y=H-30" output.mp4  # timestamp
```

### Audio Processing
```
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4                    # volume boost
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp4  # EBU R128 normalization
ffmpeg -i input.mp4 -af "afade=t=in:d=2,afade=t=out:st=58:d=2" output.mp4  # fade in/out
ffmpeg -i input.mp4 -af "highpass=f=200,lowpass=f=3000" output.mp4  # bandpass
ffmpeg -i input.mp4 -an output_silent.mp4                           # strip audio
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -map 0:v -map 1:a output.mp4  # replace audio track
```

### Video Stabilization (libvidstab, two-pass)
```
ffmpeg -i shaky.mp4 -vf "vidstabdetect=shakiness=5:accuracy=15" -f null -
ffmpeg -i shaky.mp4 -vf "vidstabtransform=smoothing=10:input=transforms.trf" stabilized.mp4
```

### Crossfade & Transitions
```
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "xfade=transition=fade:duration=1:offset=4" output.mp4
```
Transition types: fade, wipeleft, wiperight, slideup, slidedown, circlecrop, dissolve, and ~40 more.

### Waveform & Spectrum Visualization
```
ffmpeg -i audio.mp3 -filter_complex "showwavespic=s=1280x240:colors=0x1e90ff" -frames:v 1 waveform.png
ffmpeg -i audio.mp3 -filter_complex "showspectrumpic=s=1280x720" -frames:v 1 spectrum.png
```

### Compress / Reduce File Size
```
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset faster -c:a aac -b:a 128k smaller.mp4
ffmpeg -i input.mp4 -c:v libx265 -crf 32 -preset medium -c:a libopus -b:a 96k smallest.mp4
```
CRF is the primary quality knob. Preset trades encoding speed for compression efficiency.

## Available Codecs & Libraries Summary

**Video encoders:** libx264, libx265, libvpx (VP8), libvpx-vp9, libsvtav1, librav1e, libaom-av1, libjxl (JPEG XL), gif, png, apng, libwebp
**Audio encoders:** aac, libmp3lame, libopus, libvorbis, flac, ac3, pcm_s16le
**Subtitle:** ASS/SSA (libass), SRT, DVB, DVD, MOV text
**426 formats**, **562 filters**, hardware accel stubs (vaapi, vulkan, opencl — limited use in container)

## Key Constraints

- **No GPU acceleration** — CUDA device count is 0; vaapi/vulkan/opencl listed but no hardware available. All encoding is CPU-only.
- **Container is ephemeral** — long encodes on large files are feasible but the container resets between tasks. Work in `/home/claude/`, deliver to `/mnt/user-data/outputs/`.
- **4 CPU cores, 9 GB RAM** — encoding is parallel but constrained. Use `-preset faster` or `-preset veryfast` for large files to avoid timeouts.
- **ffplay** exists but display is unavailable — use for probing only, not playback.
- **No GPU-accelerated filters** — stick to CPU filter variants.
