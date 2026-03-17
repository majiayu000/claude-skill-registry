---
name: ffmpeg-stabilization-360
description: Complete FFmpeg video stabilization and 360/VR video processing. PROACTIVELY activate for: (1) Video stabilization (deshake, vidstab), (2) Hardware-accelerated stabilization (deshake_opencl), (3) 360/VR video transforms (v360), (4) Perspective correction (perspective), (5) Ken Burns/zoom-pan effects (zoompan), (6) Lens distortion correction (lenscorrection, lensfun), (7) Action camera footage, (8) Drone video processing, (9) VR headset formats. Provides: Stabilization workflows, 360 projection conversions, motion effects, lens correction.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Task | Filter | Command Pattern |
|------|--------|-----------------|
| Basic stabilization | `deshake` | `-vf deshake` |
| VidStab (2-pass) | `vidstab` | See two-pass workflow |
| OpenCL stabilization | `deshake_opencl` | `-vf deshake_opencl` |
| 360 projection | `v360` | `-vf v360=e:c3x2` |
| Ken Burns effect | `zoompan` | `-vf zoompan=z='...'` |
| Lens correction | `lenscorrection` | `-vf lenscorrection=k1=...` |

## When to Use This Skill

Use for **motion correction and VR workflows**:
- Stabilizing shaky handheld footage
- Action camera (GoPro, DJI) processing
- Drone video smoothing
- 360/VR video format conversion
- Creating zoom/pan effects
- Correcting lens distortion

---

# FFmpeg Stabilization & 360 Video (2025)

Comprehensive guide to video stabilization, VR processing, and motion effects.

## Video Stabilization

### deshake - Basic Stabilization

Built-in single-pass stabilization filter.

```bash
# Basic stabilization
ffmpeg -i shaky.mp4 -vf "deshake" stable.mp4

# With custom parameters
ffmpeg -i shaky.mp4 -vf "deshake=x=-1:y=-1:w=-1:h=-1:rx=16:ry=16" stable.mp4

# Strong stabilization
ffmpeg -i shaky.mp4 -vf "deshake=rx=64:ry=64:edge=mirror" stable.mp4
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `x`, `y` | Motion search start | -1 (auto) | 0-width/height |
| `w`, `h` | Motion search size | -1 (auto) | 0-width/height |
| `rx`, `ry` | Maximum shift | 16 | 0-64 |
| `edge` | Edge handling | mirror | blank, original, clamp, mirror |
| `blocksize` | Block size for motion search | 8 | 4-128 |
| `contrast` | Contrast threshold | 125 | 1-255 |
| `search` | Search method | exhaustive | exhaustive, less |

**Edge modes:**
- `blank` - Fill edges with black
- `original` - Keep original edge pixels
- `clamp` - Clamp to edge values
- `mirror` - Mirror edge pixels (usually best)

### deshake_opencl - GPU-Accelerated Stabilization

Faster stabilization using OpenCL.

```bash
# OpenCL stabilization
ffmpeg -i shaky.mp4 \
  -vf "hwupload,deshake_opencl,hwdownload,format=yuv420p" \
  stable.mp4

# With custom parameters
ffmpeg -i shaky.mp4 \
  -vf "hwupload,deshake_opencl=tripod=0:smooth=9:adaptive_crop=1,hwdownload,format=yuv420p" \
  stable.mp4
```

### VidStab - Professional Two-Pass Stabilization

VidStab provides the highest quality stabilization using a two-pass approach.

**Pass 1: Analyze motion**
```bash
# Analyze video and save transform data
ffmpeg -i shaky.mp4 \
  -vf "vidstabdetect=stepsize=6:shakiness=8:accuracy=9:result=transforms.trf" \
  -f null -
```

**Pass 2: Apply transforms**
```bash
# Apply stabilization with transforms
ffmpeg -i shaky.mp4 \
  -vf "vidstabtransform=input=transforms.trf:zoom=1:smoothing=30" \
  stable.mp4
```

**vidstabdetect Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `stepsize` | Step size for motion estimation | 6 | 1-32 |
| `shakiness` | Shakiness amount (higher = more analysis) | 5 | 1-10 |
| `accuracy` | Detection accuracy | 15 | 1-15 |
| `result` | Output transform file | transforms.trf | filename |
| `show` | Visualize detection | 0 | 0-2 |

**vidstabtransform Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `input` | Transform file | transforms.trf | filename |
| `smoothing` | Smoothing frames (higher = smoother) | 10 | 0-100 |
| `zoom` | Zoom percentage | 0 | -100 to 100 |
| `optzoom` | Optimal zoom calculation | 1 | 0-2 |
| `zoomspeed` | Max zoom change per frame | 0.25 | 0-5 |
| `crop` | Cropping mode | keep | keep, black |
| `relative` | Transform type | 1 | 0-1 |
| `tripod` | Tripod mode (fixed position) | 0 | 0-1 |

**Complete VidStab workflow:**
```bash
#!/bin/bash
# Professional stabilization workflow

INPUT="$1"
OUTPUT="${1%.*}_stabilized.mp4"

echo "Pass 1: Analyzing motion..."
ffmpeg -i "$INPUT" \
  -vf "vidstabdetect=stepsize=6:shakiness=8:accuracy=15:result=transforms.trf" \
  -f null -

echo "Pass 2: Applying stabilization..."
ffmpeg -i "$INPUT" \
  -vf "vidstabtransform=input=transforms.trf:smoothing=30:zoom=2:optzoom=1" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy \
  "$OUTPUT"

rm transforms.trf
echo "Stabilized: $OUTPUT"
```

### Stabilization Comparison

| Method | Quality | Speed | GPU | Use Case |
|--------|---------|-------|-----|----------|
| `deshake` | Good | Fast | No | Quick fixes |
| `deshake_opencl` | Good | Very Fast | Yes | Quick fixes with GPU |
| `vidstab` (2-pass) | Best | Slow | No | Professional work |

---

## 360/VR Video Processing

### v360 - 360 Video Projection Conversion

Converts between various 360 video projections.

```bash
# Equirectangular to Cubemap 3x2
ffmpeg -i equirect.mp4 -vf "v360=e:c3x2" cubemap.mp4

# Equirectangular to Cubemap 6x1
ffmpeg -i equirect.mp4 -vf "v360=e:c6x1" cubemap_6x1.mp4

# Cubemap to Equirectangular
ffmpeg -i cubemap.mp4 -vf "v360=c3x2:e" equirect.mp4

# Equirectangular to EAC (YouTube format)
ffmpeg -i equirect.mp4 -vf "v360=e:eac" youtube_360.mp4

# Dual fisheye to Equirectangular
ffmpeg -i dual_fisheye.mp4 -vf "v360=dfisheye:e:ih_fov=190:iv_fov=190" equirect.mp4
```

**Input/Output Projections:**
| Code | Projection | Description |
|------|------------|-------------|
| `e` | Equirectangular | Standard 360 format (2:1 ratio) |
| `c3x2` | Cubemap 3x2 | 3 faces wide, 2 high |
| `c6x1` | Cubemap 6x1 | 6 faces in a row |
| `c1x6` | Cubemap 1x6 | 6 faces in a column |
| `eac` | Equi-Angular Cubemap | YouTube 360 format |
| `dfisheye` | Dual Fisheye | Two circular fisheye images |
| `sg` | Stereographic | Low distortion projection |
| `flat` | Flat/Rectilinear | Normal perspective view |
| `barrel` | Barrel | Barrel split |
| `fb` | Facebook | Facebook 360 format |

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `id_fov` | Input diagonal FOV | `id_fov=195` |
| `ih_fov`, `iv_fov` | Input H/V FOV | `ih_fov=190:iv_fov=190` |
| `yaw`, `pitch`, `roll` | Rotation angles | `yaw=90:pitch=0` |
| `w`, `h` | Output size | `w=4096:h=2048` |
| `interp` | Interpolation | `nearest`, `linear`, `cubic`, `lanczos` |

### 360 Video Rotation and Reframing

```bash
# Rotate 360 video 90 degrees
ffmpeg -i input_360.mp4 -vf "v360=e:e:yaw=90" rotated.mp4

# Tilt view up
ffmpeg -i input_360.mp4 -vf "v360=e:e:pitch=-30" tilted.mp4

# Extract flat view from 360
ffmpeg -i 360_video.mp4 \
  -vf "v360=e:flat:h_fov=120:v_fov=90:yaw=45:pitch=-10:w=1920:h=1080" \
  flat_extract.mp4
```

### Stereoscopic 360 Processing

```bash
# Split top-bottom stereo to left eye only
ffmpeg -i stereo_tb.mp4 -vf "v360=e:e:in_stereo=tb:out_stereo=2d" left_eye.mp4

# Convert side-by-side to top-bottom
ffmpeg -i stereo_sbs.mp4 -vf "v360=e:e:in_stereo=sbs:out_stereo=tb" stereo_tb.mp4
```

---

## Ken Burns and Zoom Effects

### zoompan - Pan and Zoom Animation

Creates Ken Burns style effects on still images or video.

```bash
# Basic zoom in on center
ffmpeg -loop 1 -i image.jpg -t 5 \
  -vf "zoompan=z='min(zoom+0.001,1.5)':d=125" \
  -c:v libx264 zoom_in.mp4

# Zoom in from top-left to center
ffmpeg -loop 1 -i image.jpg -t 5 \
  -vf "zoompan=z='min(zoom+0.001,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080" \
  ken_burns.mp4

# Pan across image
ffmpeg -loop 1 -i image.jpg -t 10 \
  -vf "zoompan=z=1.3:x='if(gte(x,iw-iw/zoom),0,x+1)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080" \
  pan.mp4

# Zoom out
ffmpeg -loop 1 -i image.jpg -t 5 \
  -vf "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.002))':d=125:s=1920x1080" \
  zoom_out.mp4
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `z` | Zoom factor expression | `z='min(zoom+0.001,1.5)'` |
| `x`, `y` | Pan position expression | `x='iw/2'` |
| `d` | Duration per image (frames) | `d=125` |
| `s` | Output size | `s=1920x1080` |
| `fps` | Output frame rate | `fps=30` |

**Useful expressions:**
- `zoom` - Current zoom value
- `pzoom` - Previous zoom value
- `iw`, `ih` - Input width/height
- `on` - Output frame number

### Animated Slideshow Example

```bash
# Create slideshow with Ken Burns
ffmpeg -loop 1 -t 5 -i img1.jpg \
       -loop 1 -t 5 -i img2.jpg \
       -loop 1 -t 5 -i img3.jpg \
  -filter_complex "\
    [0:v]zoompan=z='min(zoom+0.001,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30[v0];\
    [1:v]zoompan=z=1.3:x='if(gte(x,iw-iw/zoom),0,x+2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30[v1];\
    [2:v]zoompan=z='1.3-0.002*on':d=150:s=1920x1080:fps=30[v2];\
    [v0][v1]xfade=transition=fade:duration=1:offset=4[x1];\
    [x1][v2]xfade=transition=fade:duration=1:offset=8[out]" \
  -map "[out]" slideshow.mp4
```

---

## Lens Correction

### lenscorrection - Barrel/Pincushion Correction

Corrects lens distortion mathematically.

```bash
# Correct barrel distortion
ffmpeg -i distorted.mp4 -vf "lenscorrection=k1=-0.2:k2=-0.05" corrected.mp4

# Correct pincushion distortion
ffmpeg -i distorted.mp4 -vf "lenscorrection=k1=0.2:k2=0.05" corrected.mp4

# With center offset
ffmpeg -i distorted.mp4 -vf "lenscorrection=cx=0.5:cy=0.5:k1=-0.2:k2=-0.05" corrected.mp4
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `cx`, `cy` | Center position | 0.5 | 0-1 |
| `k1` | Primary coefficient | 0 | -1 to 1 |
| `k2` | Secondary coefficient | 0 | -1 to 1 |
| `i` | Interpolation | bilinear | nearest, bilinear |

**Tips for finding coefficients:**
- Barrel distortion (fisheye): negative k1 (-0.1 to -0.5)
- Pincushion distortion: positive k1 (0.1 to 0.5)
- Start with k2=0, adjust k1 first

### lensfun - Database-Driven Lens Correction

Uses the lensfun database for automatic lens correction.

```bash
# Auto-detect lens from metadata
ffmpeg -i photo.jpg -vf "lensfun=make=Canon:model=EOS 5D Mark II:lens_model=Canon EF 24-70mm" corrected.jpg

# With specific parameters
ffmpeg -i video.mp4 -vf "lensfun=make=GoPro:model=HERO10:mode=geometry" corrected.mp4
```

**Requires**: lensfun library and database installed

### perspective - Perspective Correction

Corrects keystone/perspective distortion.

```bash
# Correct perspective with four corner points
# Map corners: (x0,y0)-(x1,y1)-(x2,y2)-(x3,y3) to rectangle
ffmpeg -i skewed.mp4 \
  -vf "perspective=x0=100:y0=50:x1=1820:y1=80:x2=0:y2=1030:x3=1920:y3=1000:interpolation=linear" \
  corrected.mp4

# Interactive: find coordinates with test overlay first
ffmpeg -i skewed.mp4 -vf "drawgrid=w=100:h=100:c=red" grid_overlay.mp4
```

---

## Common Workflows

### Action Camera Processing

```bash
# GoPro footage: stabilize + lens correct + encode
ffmpeg -i GOPR0001.MP4 \
  -vf "lenscorrection=k1=-0.2:k2=-0.05,vidstabdetect=shakiness=8:result=gopro.trf" \
  -f null -

ffmpeg -i GOPR0001.MP4 \
  -vf "lenscorrection=k1=-0.2:k2=-0.05,vidstabtransform=input=gopro.trf:smoothing=20:zoom=5" \
  -c:v libx264 -crf 18 \
  gopro_processed.mp4
```

### Drone Footage Processing

```bash
# DJI footage: stabilize and enhance
ffmpeg -i DJI_0001.MP4 \
  -vf "vidstabdetect=shakiness=5:stepsize=6:result=drone.trf" -f null -

ffmpeg -i DJI_0001.MP4 \
  -vf "vidstabtransform=input=drone.trf:smoothing=40:zoom=2,eq=contrast=1.1:saturation=1.2" \
  -c:v libx264 -crf 18 -preset slow \
  drone_processed.mp4
```

### 360 Camera to Flat Video

```bash
# Extract interesting view from 360 footage
ffmpeg -i insta360.mp4 \
  -vf "v360=e:flat:h_fov=110:v_fov=70:yaw=45:pitch=-15:w=1920:h=1080,deshake" \
  flat_view.mp4
```

---

## Best Practices

1. **VidStab for quality** - Two-pass is slower but much better than deshake
2. **Allow zoom headroom** - Stabilization needs room to crop
3. **Match frame rates** - Ensure consistent fps before and after
4. **GPU when available** - Use deshake_opencl for speed
5. **Test coefficients** - Lens correction needs experimentation
6. **Preserve 360 metadata** - Use `-map_metadata 0` for VR videos

This guide covers stabilization and 360 processing for 2025. For hardware acceleration, see `ffmpeg-hardware-acceleration`. For filters and effects, see `ffmpeg-filter-complex-patterns`.
