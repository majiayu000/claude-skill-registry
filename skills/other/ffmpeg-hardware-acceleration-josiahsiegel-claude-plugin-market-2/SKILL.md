---
name: ffmpeg-hardware-acceleration
description: Complete GPU-accelerated encoding/decoding system for FFmpeg 7.1 LTS and 8.0.1 (latest stable, released 2025-11-20). PROACTIVELY activate for: (1) NVIDIA NVENC/NVDEC encoding, (2) Intel Quick Sync Video (QSV), (3) AMD AMF encoding, (4) Apple VideoToolbox, (5) Linux VAAPI setup, (6) Vulkan Video 8.0 (FFv1, AV1, VP9, ProRes RAW), (7) VVC/H.266 hardware decoding (VAAPI/QSV), (8) GPU pipeline optimization with pad_cuda, (9) Docker GPU containers, (10) Performance benchmarking. Provides: Platform-specific commands, preset comparisons, quality tuning, full GPU pipeline examples, Vulkan compute codecs, VVC decoding, troubleshooting guides. Ensures: Maximum encoding speed with optimal quality using GPU acceleration.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Platform | Encoder | Decoder | Detect Command |
|----------|---------|---------|----------------|
| NVIDIA | `h264_nvenc`, `hevc_nvenc`, `av1_nvenc` | `h264_cuvid`, `hevc_cuvid` | `ffmpeg -encoders \| grep nvenc` |
| Intel QSV | `h264_qsv`, `hevc_qsv`, `av1_qsv` | `h264_qsv`, `hevc_qsv` | `ffmpeg -encoders \| grep qsv` |
| AMD AMF | `h264_amf`, `hevc_amf`, `av1_amf` | N/A (use software) | `ffmpeg -encoders \| grep amf` |
| Apple | `h264_videotoolbox`, `hevc_videotoolbox` | `h264_videotoolbox` | macOS only |
| VAAPI | `h264_vaapi`, `hevc_vaapi`, `av1_vaapi` | with `-hwaccel vaapi` | Linux only |

## When to Use This Skill

Use when **GPU acceleration is needed**:
- Encoding speed is critical (10-30x faster than CPU)
- Processing large batches of videos
- Real-time encoding for streaming
- Server-side transcoding at scale
- Docker containers with GPU passthrough

**Key decision**: GPU encoding trades some quality for massive speed. Use `-cq` or `-qp` for quality control.

---

# FFmpeg Hardware Acceleration (2025)

Comprehensive guide to GPU-accelerated encoding and decoding with NVIDIA, Intel, AMD, Apple, and Vulkan.

**Current Latest**: FFmpeg 8.0.1 (released 2025-11-20) - Check with `ffmpeg -version`

## Hardware Acceleration Overview

Hardware acceleration uses dedicated GPU/SoC components for video processing:
- **NVENC/NVDEC** (NVIDIA): Dedicated video encode/decode engines
- **QSV** (Intel): Quick Sync Video on Intel CPUs with integrated graphics
- **AMF** (AMD): Advanced Media Framework for AMD GPUs
- **VideoToolbox** (Apple): macOS/iOS hardware acceleration
- **VAAPI** (Linux): Video Acceleration API (Intel, AMD on Linux)
- **Vulkan Video** (Cross-platform): FFmpeg 7.1+/8.0 GPU acceleration

### Performance Comparison (2025 Benchmarks)

| Method | Speed | Quality | Power | Use Case |
|--------|-------|---------|-------|----------|
| libx264 (CPU) | 1x | Best | High | Quality-critical |
| libx265 (CPU) | 0.3x | Best | Very High | Archival |
| h264_nvenc | 10-20x | Good | Low | Real-time, streaming |
| hevc_nvenc | 8-15x | Good | Low | 4K streaming |
| h264_qsv | 8-15x | Good | Very Low | Laptop, efficiency |
| h264_amf | 8-15x | Good | Low | AMD systems |

## NVIDIA NVENC/NVDEC

### Requirements
- NVIDIA GPU (GTX 600+ / Quadro K series+)
- NVIDIA drivers 450+
- FFmpeg built with `--enable-nvenc --enable-cuda --enable-cuvid`

### Check NVIDIA Support
```bash
# Check available NVIDIA codecs
ffmpeg -encoders | grep nvenc
ffmpeg -decoders | grep cuvid

# Check GPU info
nvidia-smi

# List hardware accelerators
ffmpeg -hwaccels
```

### Basic NVENC Encoding

```bash
# H.264 NVENC encoding
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -b:v 5M output.mp4

# H.265/HEVC NVENC encoding
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -b:v 4M output.mp4

# AV1 NVENC (RTX 40 series+)
ffmpeg -i input.mp4 -c:v av1_nvenc -preset p4 -b:v 3M output.mp4
```

### NVENC Presets (FFmpeg 7+)

| Preset | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| p1 | Fastest | Lowest | Real-time capture |
| p2 | Faster | Low | Screen recording |
| p3 | Fast | Medium | General streaming |
| p4 | Medium | Good | **Recommended** |
| p5 | Slow | Better | High-quality streaming |
| p6 | Slower | Best | Offline encoding |
| p7 | Slowest | Highest | Maximum quality |

### Full GPU Pipeline (Decode + Encode)

```bash
# Keep frames in GPU memory (fastest)
ffmpeg -y -vsync 0 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i input.mp4 \
  -c:v h264_nvenc \
  -preset p4 \
  -b:v 5M \
  -c:a copy \
  output.mp4
```

### GPU Scaling and Filtering

```bash
# GPU-based scaling with scale_cuda
ffmpeg -y -vsync 0 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf scale_cuda=1280:720 \
  -c:v h264_nvenc \
  -preset p4 \
  output.mp4

# GPU overlay with overlay_cuda
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i main.mp4 \
  -hwaccel cuda -hwaccel_output_format cuda -i overlay.mp4 \
  -filter_complex "[0:v][1:v]overlay_cuda=10:10" \
  -c:v h264_nvenc output.mp4

# GPU padding with pad_cuda (FFmpeg 8.0+)
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -vf "pad_cuda=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v h264_nvenc output.mp4

# Letterbox with pad_cuda
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -vf "scale_cuda=1920:-2,pad_cuda=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v h264_nvenc output.mp4
```

### CUDA Filters Reference (FFmpeg 8.0+)

| Filter | Description | Key Parameters |
|--------|-------------|----------------|
| `scale_cuda` | GPU video scaling | `w`, `h`, `format`, `interp_algo` |
| `scale_npp` | NPP-based scaling (higher quality) | `w`, `h`, `interp_algo` |
| `overlay_cuda` | GPU overlay/compositing | `x`, `y`, `eof_action` |
| `pad_cuda` | GPU padding (8.0+) | `w`, `h`, `x`, `y`, `color` |
| `chromakey_cuda` | GPU chroma keying | `color`, `similarity`, `blend` |
| `colorspace_cuda` | Color space conversion | `all`, `space`, `trc`, `primaries` |
| `bilateral_cuda` | Bilateral filter | `sigmaS`, `sigmaR`, `window_size` |
| `bwdif_cuda` | Deinterlacing | `mode`, `parity`, `deint` |
| `hwupload_cuda` | Upload to GPU | - |
| `hwdownload` | Download from GPU | - |

### scale_npp (NVIDIA Performance Primitives)

For higher-quality scaling, use scale_npp with optimized interpolation algorithms:

```bash
# High-quality downscaling with super-sampling
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf "scale_npp=1280:720:interp_algo=super" \
  -c:v h264_nvenc output.mp4

# Lanczos interpolation for upscaling
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf "scale_npp=1920:1080:interp_algo=lanczos" \
  -c:v h264_nvenc output.mp4
```

**scale_npp Interpolation Algorithms:**

| Algorithm | Quality | Speed | Best For |
|-----------|---------|-------|----------|
| `nn` | Low | Fastest | Pixel art, nearest neighbor |
| `linear` | Medium | Fast | General use |
| `cubic` | Good | Medium | Smooth scaling |
| `lanczos` | High | Slow | High quality upscaling |
| `super` | Best | Slowest | Downscaling |

### GPU Chromakey (Green Screen)

```bash
# Green screen removal on GPU
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i greenscreen.mp4 \
  -hwaccel cuda -hwaccel_output_format cuda -i background.mp4 \
  -filter_complex "[0:v]chromakey_cuda=0x00FF00:0.3:0.1[fg];[1:v][fg]overlay_cuda" \
  -c:v h264_nvenc output.mp4
```

### Hybrid GPU + CPU Filter Pipelines

When mixing CPU and GPU filters, use `hwupload_cuda` and `hwdownload`:

```bash
# CPU decode -> CPU filter -> GPU encode
ffmpeg -i input.mp4 \
  -vf "fade=in:0:30,hwupload_cuda" \
  -c:v h264_nvenc output.mp4

# GPU decode -> CPU filter (drawtext) -> GPU encode
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf "hwdownload,format=nv12,drawtext=text='Hello':fontsize=48,hwupload_cuda" \
  -c:v h264_nvenc output.mp4

# Complete hybrid pipeline: GPU scale -> CPU text -> GPU encode
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -filter_complex "\
    [0:v]scale_cuda=1920:1080[scaled];\
    [scaled]hwdownload,format=nv12[cpu];\
    [cpu]drawtext=text='Watermark':fontsize=48:x=10:y=10[text];\
    [text]hwupload_cuda[gpu]" \
  -map "[gpu]" \
  -c:v h264_nvenc output.mp4
```

### NVENC Quality Optimization

```bash
# High quality with lookahead
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc \
  -preset p5 \
  -tune hq \
  -rc vbr \
  -cq 23 \
  -b:v 0 \
  -rc-lookahead 32 \
  -spatial-aq 1 \
  -temporal-aq 1 \
  -c:a copy \
  output.mp4

# Constant quality mode (CQP)
ffmpeg -i input.mp4 \
  -c:v h264_nvenc \
  -preset p4 \
  -rc constqp \
  -qp 23 \
  -c:a copy \
  output.mp4
```

### NVENC Two-Pass Encoding

```bash
# Two-pass for best quality (ABR)
ffmpeg -i input.mp4 \
  -c:v h264_nvenc \
  -preset p5 \
  -2pass 1 \
  -b:v 5M \
  -c:a copy \
  output.mp4
```

### NVENC B-Frames and GOP

```bash
# Enable B-frames for better compression
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc \
  -preset p4 \
  -bf 4 \
  -b_ref_mode 2 \
  -g 250 \
  -c:a copy \
  output.mp4
```

## GPU Memory Management

### Critical Concepts

PCIe transfers between CPU and GPU memory are the primary bottleneck. Keeping frames in GPU memory throughout the pipeline is critical for performance.

**Memory Flow Patterns:**

```
Pattern 1: Full GPU Pipeline (OPTIMAL)
Input File -> GPU Decode -> GPU Filter -> GPU Encode -> Output File
                    |          |           |
                    v          v           v
                  [GPU Memory - No PCIe Transfer]

Pattern 2: CPU Filter Insertion (SUBOPTIMAL)
Input -> GPU Decode -> hwdownload -> CPU Filter -> hwupload -> GPU Encode -> Output
                           |                           |
                           v                           v
                     [PCIe Transfer]             [PCIe Transfer]

Pattern 3: Software Decode + GPU Encode
Input -> CPU Decode -> hwupload -> GPU Encode -> Output
                          |
                          v
                    [PCIe Transfer]
```

### Command Patterns Comparison

```bash
# OPTIMAL: Full GPU pipeline - no CPU-GPU transfers
ffmpeg -y -vsync 0 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf scale_cuda=1280:720 \
  -c:v h264_nvenc \
  output.mp4

# SUBOPTIMAL: GPU decode, CPU filter, GPU encode - 2 transfers
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -vf "hwdownload,format=nv12,drawtext=text='Hello',hwupload_cuda" \
  -c:v h264_nvenc output.mp4

# AVOID: Missing -hwaccel_output_format - frame copies to CPU after decode
ffmpeg -hwaccel cuda -i input.mp4 \
  -vf scale=1280:720 \
  -c:v h264_nvenc output.mp4
```

**Why `-hwaccel_output_format cuda` matters:** Without it, decoded frames transfer from GPU to CPU via PCIe, get processed, then transfer back to GPU for encoding. This can reduce throughput by up to 50%.

### Memory Monitoring

```bash
# NVIDIA GPU memory and utilization
nvidia-smi dmon -s m

# Watch GPU utilization in real-time
watch -n 1 nvidia-smi

# Intel GPU monitoring
intel_gpu_top
```

### Best Practices

1. **Use `-hwaccel_output_format`** to keep decoded frames in GPU memory
2. **Use GPU filters when available** (scale_cuda, overlay_cuda, pad_cuda)
3. **Batch similar operations** to minimize filter graph complexity
4. **Monitor GPU memory** for high-resolution content
5. **Use `-vsync 0`** to prevent frame duplication overhead

## Multi-GPU Encoding

### NVIDIA Multi-GPU

```bash
# Specify GPU by index (parallel processing on different GPUs)
ffmpeg -hwaccel cuda \
  -hwaccel_device 0 \
  -hwaccel_output_format cuda \
  -i input1.mp4 \
  -c:v h264_nvenc output1.mp4 &

ffmpeg -hwaccel cuda \
  -hwaccel_device 1 \
  -hwaccel_output_format cuda \
  -i input2.mp4 \
  -c:v h264_nvenc output2.mp4 &

wait

# Initialize specific CUDA device for filters
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -init_hw_device cuda=gpu1:1 \
  -filter_complex "[0:v]scale_cuda=1280:720[scaled]" \
  -map "[scaled]" \
  -c:v h264_nvenc output.mp4
```

### 1:N Encoding (Single Input, Multiple Outputs)

More efficient than separate processes - shares CUDA context:

```bash
# Single input to multiple resolutions (ABR ladder)
ffmpeg -y -vsync 0 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i input.mp4 \
  -filter_complex "[0:v]split=3[v1][v2][v3];\
    [v1]scale_cuda=1920:1080[hd];\
    [v2]scale_cuda=1280:720[sd];\
    [v3]scale_cuda=640:360[mobile]" \
  -map "[hd]" -c:v h264_nvenc -b:v 5M output_1080p.mp4 \
  -map "[sd]" -c:v h264_nvenc -b:v 2M output_720p.mp4 \
  -map "[mobile]" -c:v h264_nvenc -b:v 500k output_360p.mp4
```

### Parallel Encoding Strategy

For maximum throughput:
1. Run 4+ parallel FFmpeg sessions
2. Use inputs with 15+ seconds to amortize initialization
3. Measure aggregate FPS across all sessions

```bash
# Environment variables for faster initialization
export CUDA_VISIBLE_DEVICES=0
export CUDA_DEVICE_MAX_CONNECTIONS=2

# Parallel encoding script
for i in {1..4}; do
  ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
    -i input_$i.mp4 \
    -c:v h264_nvenc \
    output_$i.mp4 &
done
wait
```

## Intel Quick Sync Video (QSV)

### Requirements
- Intel CPU with integrated graphics (Sandy Bridge+)
- Intel Media SDK or oneVPL
- FFmpeg built with `--enable-libmfx` or `--enable-libvpl`

### Check QSV Support
```bash
# Check available QSV codecs
ffmpeg -encoders | grep qsv
ffmpeg -decoders | grep qsv

# Verify Intel GPU access (Linux)
ls /dev/dri/
vainfo  # Check VAAPI support
```

### Basic QSV Encoding

```bash
# Initialize QSV device
ffmpeg -init_hw_device qsv=hw \
  -filter_hw_device hw \
  -i input.mp4 \
  -c:v h264_qsv \
  -preset medium \
  -b:v 5M \
  output.mp4

# H.265/HEVC QSV
ffmpeg -init_hw_device qsv=hw \
  -filter_hw_device hw \
  -i input.mp4 \
  -c:v hevc_qsv \
  -preset medium \
  -b:v 4M \
  output.mp4

# AV1 QSV (Intel Arc, 12th gen+)
ffmpeg -init_hw_device qsv=hw \
  -filter_hw_device hw \
  -i input.mp4 \
  -c:v av1_qsv \
  -preset medium \
  -b:v 3M \
  output.mp4
```

### Full QSV Pipeline

```bash
# Decode and encode on GPU
ffmpeg -hwaccel qsv \
  -hwaccel_output_format qsv \
  -i input.mp4 \
  -c:v h264_qsv \
  -preset medium \
  -b:v 5M \
  output.mp4
```

### QSV Quality Settings

```bash
# Constant quality (recommended)
ffmpeg -hwaccel qsv -hwaccel_output_format qsv \
  -i input.mp4 \
  -c:v hevc_qsv \
  -preset slow \
  -global_quality 22 \
  -look_ahead 1 \
  output.mp4

# VBR with lookahead
ffmpeg -hwaccel qsv -hwaccel_output_format qsv \
  -i input.mp4 \
  -c:v h264_qsv \
  -preset medium \
  -b:v 5M \
  -maxrate 7M \
  -bufsize 10M \
  -look_ahead 1 \
  -look_ahead_depth 40 \
  output.mp4
```

**QSV Quality Parameters:**

| Parameter | Description | Range |
|-----------|-------------|-------|
| `-global_quality` | Quality level (like CRF) | 1-51 (lower = better) |
| `-preset` | Encoding speed/quality | `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow` |
| `-look_ahead` | Enable lookahead | 0 or 1 |
| `-look_ahead_depth` | Lookahead frames | 10-100 |

### Multi-GPU QSV (Linux)

```bash
# Select specific GPU by render device
ffmpeg -init_hw_device qsv=hw:/dev/dri/renderD129 \
  -filter_hw_device hw \
  -i input.mp4 \
  -c:v h264_qsv output.mp4
```

### QSV with Scaling

```bash
# GPU scaling with vpp_qsv
ffmpeg -hwaccel qsv \
  -hwaccel_output_format qsv \
  -i input.mp4 \
  -vf "vpp_qsv=w=1280:h=720" \
  -c:v h264_qsv \
  -preset medium \
  output.mp4
```

### VVC/H.266 QSV Decoding (FFmpeg 7.1+)

```bash
# Hardware VVC decoding
ffmpeg -hwaccel qsv \
  -hwaccel_output_format qsv \
  -c:v vvc_qsv \
  -i input.vvc \
  -c:v h264_qsv \
  output.mp4
```

## AMD AMF

### Requirements
- AMD GPU (GCN or newer)
- AMD drivers with AMF support
- FFmpeg built with `--enable-amf`

### Check AMF Support
```bash
ffmpeg -encoders | grep amf
```

### Basic AMF Encoding

```bash
# H.264 AMF
ffmpeg -i input.mp4 \
  -c:v h264_amf \
  -quality balanced \
  -b:v 5M \
  output.mp4

# H.265/HEVC AMF
ffmpeg -i input.mp4 \
  -c:v hevc_amf \
  -quality balanced \
  -b:v 4M \
  output.mp4

# AV1 AMF (RDNA3+)
ffmpeg -i input.mp4 \
  -c:v av1_amf \
  -quality balanced \
  -b:v 3M \
  output.mp4
```

### AMF Quality Presets

| Preset | Description |
|--------|-------------|
| speed | Fastest encoding |
| balanced | **Recommended** |
| quality | Best quality |

### AMD Hardware Upscaling (FFmpeg 8.0+)

```bash
# Super resolution upscaling
ffmpeg -i input.mp4 \
  -vf "sr_amf=4096:2160:algorithm=sr1-1" \
  -c:v hevc_amf \
  output.mp4
```

## VAAPI (Linux)

### Requirements
- Intel, AMD, or NVIDIA GPU on Linux
- VAAPI drivers (intel-media-driver, mesa-va-drivers)
- FFmpeg built with `--enable-vaapi`

### Check VAAPI Support
```bash
# Check VAAPI info
vainfo

# List VAAPI codecs
ffmpeg -encoders | grep vaapi
ffmpeg -decoders | grep vaapi
```

### Basic VAAPI Encoding

```bash
# H.264 VAAPI
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -i input.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi \
  -b:v 5M \
  output.mp4

# H.265/HEVC VAAPI
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -i input.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v hevc_vaapi \
  -b:v 4M \
  output.mp4
```

### Full VAAPI Pipeline

```bash
# Decode and encode on GPU
ffmpeg -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i input.mp4 \
  -c:v h264_vaapi \
  -b:v 5M \
  output.mp4
```

### VAAPI Scaling

```bash
ffmpeg -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i input.mp4 \
  -vf 'scale_vaapi=w=1280:h=720' \
  -c:v h264_vaapi \
  output.mp4
```

### VVC VAAPI Decoding (FFmpeg 8.0+)

FFmpeg 8.0 adds VVC/H.266 hardware decoding on Intel and AMD GPUs via VAAPI.

```bash
# Hardware VVC/H.266 decoding
ffmpeg -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i input.vvc \
  -c:v h264_vaapi \
  output.mp4

# VVC decode + transcode to H.265
ffmpeg -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i input.mkv \
  -c:v hevc_vaapi \
  -b:v 4M \
  output.mp4

# VVC with Screen Content Coding (SCC) support
# FFmpeg 8.0 adds full SCC support including:
# - IBC (Inter Block Copy)
# - Palette Mode
# - ACT (Adaptive Color Transform)
ffmpeg -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -i screen_recording.vvc \
  output.mp4
```

**VVC VAAPI Requirements:**
- Intel Xe2 graphics (Lunar Lake) or newer for full VVC support
- FFmpeg 8.0 or later
- Intel media driver with VVC support

## Apple VideoToolbox

### Requirements
- macOS 10.8+ or iOS 8+
- FFmpeg built with `--enable-videotoolbox`

### Check VideoToolbox Support
```bash
ffmpeg -encoders | grep videotoolbox
ffmpeg -decoders | grep videotoolbox
```

### Basic VideoToolbox Encoding

```bash
# H.264 VideoToolbox
ffmpeg -i input.mp4 \
  -c:v h264_videotoolbox \
  -b:v 5M \
  output.mp4

# H.265/HEVC VideoToolbox
ffmpeg -i input.mp4 \
  -c:v hevc_videotoolbox \
  -b:v 4M \
  -tag:v hvc1 \
  output.mp4

# ProRes VideoToolbox
ffmpeg -i input.mp4 \
  -c:v prores_videotoolbox \
  -profile:v 3 \
  output.mov
```

### VideoToolbox Quality Settings

```bash
# Quality-based encoding
ffmpeg -i input.mp4 \
  -c:v h264_videotoolbox \
  -q:v 65 \
  output.mp4

# Hardware accelerated decode + encode
ffmpeg -hwaccel videotoolbox \
  -i input.mp4 \
  -c:v h264_videotoolbox \
  -b:v 5M \
  output.mp4
```

## Vulkan Video (FFmpeg 7.1+/8.0)

### Overview
Vulkan Video provides cross-platform GPU acceleration using Vulkan compute shaders. Unlike proprietary hardware accelerators, Vulkan codecs are based on compute shaders and work on any implementation of Vulkan 1.3.

### FFmpeg 7.1 Vulkan Features
- H.264 Vulkan encoding
- H.265/HEVC Vulkan encoding

### FFmpeg 8.0 Vulkan Features (New)
- **AV1 Vulkan encoding** - GPU-accelerated AV1 via compute shaders
- **VP9 Vulkan decoding** - Hardware-accelerated VP9 decode
- **FFv1 Vulkan encode/decode** - Lossless codec for archival/capture
- **ProRes RAW Vulkan decode** - Apple ProRes RAW hardware decode

**Benefits of Vulkan Compute Codecs:**
- Cross-platform: Same code works on AMD, Intel, and NVIDIA
- No vendor lock-in: Works with any Vulkan 1.3 driver
- Ideal for: Lossless screen capture, high-throughput archival, professional workflows

### Basic Vulkan Encoding

```bash
# H.264 Vulkan
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -c:v h264_vulkan \
  -b:v 5M \
  output.mp4

# H.265/HEVC Vulkan
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -c:v hevc_vulkan \
  -b:v 4M \
  output.mp4

# AV1 Vulkan (FFmpeg 8.0+)
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -c:v av1_vulkan \
  -b:v 3M \
  output.mp4

# FFv1 Vulkan Lossless (FFmpeg 8.0+)
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -c:v ffv1_vulkan \
  output.mkv
```

### Full Vulkan Pipeline

```bash
# Complete Vulkan decode-filter-encode
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -hwaccel vulkan \
  -hwaccel_output_format vulkan \
  -i input.mp4 \
  -vf "scale_vulkan=1280:720" \
  -c:v h264_vulkan \
  output.mp4
```

### VP9 Vulkan Decoding (FFmpeg 8.0+)

```bash
# Hardware decode VP9 with Vulkan
ffmpeg -init_hw_device vulkan \
  -hwaccel vulkan \
  -hwaccel_output_format vulkan \
  -i input.webm \
  -c:v h264_vulkan \
  output.mp4
```

### ProRes RAW Vulkan Decoding (FFmpeg 8.0+)

```bash
# Hardware decode ProRes RAW with Vulkan
ffmpeg -init_hw_device vulkan \
  -hwaccel vulkan \
  -i input.mov \
  -c:v libx264 \
  output.mp4
```

### Lossless Screen Capture with FFv1 Vulkan

```bash
# High-throughput lossless capture (Linux X11)
ffmpeg -init_hw_device vulkan \
  -f x11grab -framerate 60 -i :0.0 \
  -c:v ffv1_vulkan \
  screen_capture.mkv

# Lossless screen recording (Windows)
ffmpeg -init_hw_device vulkan \
  -f gdigrab -framerate 60 -i desktop \
  -c:v ffv1_vulkan \
  screen_capture.mkv
```

### Upcoming Vulkan Codecs
The next minor update will add:
- ProRes (encode and decode)
- VC-2 (encode and decode)

## Vulkan Filters (FFmpeg 8.0+)

Vulkan filters provide cross-platform GPU acceleration for video processing.

### Vulkan Filter Reference

| Filter | Description | Key Parameters |
|--------|-------------|----------------|
| `scale_vulkan` | GPU scaling | `w`, `h`, `scaler` |
| `overlay_vulkan` | Compositing | `x`, `y` |
| `transpose_vulkan` | Rotate/transpose | `dir`, `passthrough` |
| `flip_vulkan` | Horizontal flip | - |
| `avgblur_vulkan` | Box blur | `sizeX`, `sizeY` |
| `gblur_vulkan` | Gaussian blur | `sigma`, `sigmaV`, `planes` |
| `chromaber_vulkan` | Chromatic aberration | `dist_x`, `dist_y` |
| `nlmeans_vulkan` | NLMeans denoising | `s`, `p`, `r` |
| `bwdif_vulkan` | Deinterlacing | `mode`, `parity`, `deint` |
| `xfade_vulkan` | Transitions | `transition`, `duration`, `offset` |
| `libplacebo` | Libplacebo processing | `w`, `h`, `colorspace` |

### Vulkan Scaling

```bash
# Basic Vulkan scaling
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -i input.mp4 \
  -vf "hwupload,scale_vulkan=1920:1080,hwdownload,format=yuv420p" \
  output.mp4

# Full Vulkan pipeline with scaling
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -hwaccel vulkan -hwaccel_output_format vulkan \
  -i input.mp4 \
  -vf "scale_vulkan=1280:720" \
  -c:v h264_vulkan output.mp4

# Vulkan scaling with specific scaler
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,scale_vulkan=w=1920:h=1080:scaler=lanczos,hwdownload,format=yuv420p" \
  output.mp4
```

### Vulkan Compositing (overlay_vulkan)

```bash
# Picture-in-picture with Vulkan
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -i main.mp4 -i overlay.mp4 \
  -filter_complex "\
    [0:v]hwupload[main];\
    [1:v]hwupload,scale_vulkan=320:180[pip];\
    [main][pip]overlay_vulkan=x=10:y=10[out];\
    [out]hwdownload,format=yuv420p" \
  -map "[out]" output.mp4

# Full Vulkan overlay pipeline
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -hwaccel vulkan -hwaccel_output_format vulkan -i main.mp4 \
  -hwaccel vulkan -hwaccel_output_format vulkan -i overlay.mp4 \
  -filter_complex "[0:v][1:v]overlay_vulkan=x=W-w-10:y=10" \
  -c:v h264_vulkan output.mp4
```

### Vulkan Rotation and Transpose

```bash
# Transpose (rotate 90° clockwise)
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,transpose_vulkan=dir=clock,hwdownload,format=yuv420p" \
  output.mp4

# Horizontal flip
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,flip_vulkan,hwdownload,format=yuv420p" \
  output.mp4
```

**transpose_vulkan directions:**
| dir | Rotation |
|-----|----------|
| `cclock_flip` | 90° counter-clockwise + vertical flip |
| `clock` | 90° clockwise |
| `cclock` | 90° counter-clockwise |
| `clock_flip` | 90° clockwise + vertical flip |

### Vulkan Blur Effects

```bash
# Gaussian blur
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,gblur_vulkan=sigma=5,hwdownload,format=yuv420p" \
  output.mp4

# Box blur (averaging)
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,avgblur_vulkan=sizeX=5:sizeY=5,hwdownload,format=yuv420p" \
  output.mp4
```

### Vulkan Chromatic Aberration

```bash
# Add chromatic aberration effect
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,chromaber_vulkan=dist_x=-0.002:dist_y=0.002,hwdownload,format=yuv420p" \
  output.mp4
```

### Vulkan Denoising (nlmeans_vulkan)

```bash
# Non-local means denoising on GPU
ffmpeg -init_hw_device vulkan \
  -i noisy.mp4 \
  -vf "hwupload,nlmeans_vulkan=s=3:p=7:r=15,hwdownload,format=yuv420p" \
  output.mp4

# Full Vulkan denoising pipeline
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -hwaccel vulkan -hwaccel_output_format vulkan \
  -i noisy.mp4 \
  -vf "nlmeans_vulkan=s=4" \
  -c:v h264_vulkan output.mp4
```

### Vulkan Deinterlacing (bwdif_vulkan)

```bash
# Bob-Weaver deinterlacing
ffmpeg -init_hw_device vulkan \
  -i interlaced.mp4 \
  -vf "hwupload,bwdif_vulkan=mode=send_frame,hwdownload,format=yuv420p" \
  output.mp4

# Full Vulkan deinterlace pipeline
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -hwaccel vulkan -hwaccel_output_format vulkan \
  -i interlaced.mp4 \
  -vf "bwdif_vulkan=1" \
  -c:v h264_vulkan output.mp4
```

### Vulkan Transitions (xfade_vulkan)

```bash
# GPU-accelerated crossfade between two clips
ffmpeg -init_hw_device vulkan=vk \
  -filter_hw_device vk \
  -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "\
    [0:v]hwupload[v1];\
    [1:v]hwupload[v2];\
    [v1][v2]xfade_vulkan=transition=fade:duration=1:offset=4[out];\
    [out]hwdownload,format=yuv420p" \
  -map "[out]" output.mp4
```

**xfade_vulkan transitions:** `fade`, `dissolve`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `slideleft`, `slideright`, `slideup`, `slidedown`, and more.

### Libplacebo Processing (Advanced)

Libplacebo provides advanced color management and processing:

```bash
# HDR tonemapping with libplacebo
ffmpeg -init_hw_device vulkan \
  -i hdr_input.mp4 \
  -vf "hwupload,libplacebo=tonemapping=hable:colorspace=bt709:color_primaries=bt709:color_trc=bt709,hwdownload,format=yuv420p" \
  sdr_output.mp4

# Scaling with libplacebo (high quality)
ffmpeg -init_hw_device vulkan \
  -i input.mp4 \
  -vf "hwupload,libplacebo=w=3840:h=2160:upscaler=ewa_lanczos,hwdownload,format=yuv420p10le" \
  output.mp4
```

## OpenCL Filters

OpenCL provides GPU acceleration that works across vendors (NVIDIA, AMD, Intel).

### OpenCL Filter Reference

| Filter | Description | Key Parameters |
|--------|-------------|----------------|
| `scale_opencl` | GPU scaling | `w`, `h` |
| `overlay_opencl` | Compositing | `x`, `y` |
| `pad_opencl` | Padding | `w`, `h`, `x`, `y`, `color` |
| `colorkey_opencl` | Chroma keying | `color`, `similarity`, `blend` |
| `unsharp_opencl` | Sharpening | `lx`, `ly`, `la`, `cx`, `cy`, `ca` |
| `nlmeans_opencl` | NLMeans denoising | `s`, `p`, `r` |
| `deshake_opencl` | Stabilization | `tripod`, `smooth`, `filename` |
| `tonemap_opencl` | HDR tonemapping | `tonemap`, `transfer`, `matrix` |
| `avgblur_opencl` | Box blur | `sizeX`, `sizeY` |
| `convolution_opencl` | Custom kernel | `0m`, `1m`, etc. |

### OpenCL Initialization

```bash
# List OpenCL devices
ffmpeg -init_hw_device opencl=gpu:0.0 -filter_hw_device gpu -f lavfi -i nullsrc -vf "hwupload,avgblur_opencl=2" -t 1 -f null -

# Basic OpenCL filter pattern
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,<filter_opencl>,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL Scaling

```bash
# GPU scaling with OpenCL
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,scale_opencl=1920:1080,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL Compositing

```bash
# Picture-in-picture with OpenCL
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i main.mp4 -i overlay.mp4 \
  -filter_complex "\
    [0:v]hwupload[main];\
    [1:v]hwupload,scale_opencl=320:180[pip];\
    [main][pip]overlay_opencl=x=10:y=10[out];\
    [out]hwdownload,format=yuv420p" \
  -map "[out]" output.mp4
```

### OpenCL Chroma Keying (colorkey_opencl)

```bash
# Green screen removal with OpenCL
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i greenscreen.mp4 -i background.mp4 \
  -filter_complex "\
    [0:v]hwupload,colorkey_opencl=0x00FF00:0.3:0.1[fg];\
    [1:v]hwupload[bg];\
    [bg][fg]overlay_opencl[out];\
    [out]hwdownload,format=yuv420p" \
  -map "[out]" output.mp4
```

### OpenCL Denoising (nlmeans_opencl)

```bash
# Non-local means denoising on GPU
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i noisy.mp4 \
  -vf "hwupload,nlmeans_opencl=s=3:p=7:r=15,hwdownload,format=yuv420p" \
  output.mp4

# Strong denoising
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i noisy.mp4 \
  -vf "hwupload,nlmeans_opencl=s=5:p=7:r=21,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL Stabilization (deshake_opencl)

```bash
# GPU-accelerated video stabilization
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i shaky.mp4 \
  -vf "hwupload,deshake_opencl,hwdownload,format=yuv420p" \
  output.mp4

# Tripod mode (camera stays in one place)
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i shaky.mp4 \
  -vf "hwupload,deshake_opencl=tripod=1,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL Sharpening (unsharp_opencl)

```bash
# Basic sharpening
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,unsharp_opencl=lx=5:ly=5:la=1.0,hwdownload,format=yuv420p" \
  output.mp4

# Subtle sharpening for HD video
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,unsharp_opencl=lx=3:ly=3:la=0.5,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL HDR Tonemapping (tonemap_opencl)

```bash
# HDR to SDR conversion with GPU
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i hdr_input.mp4 \
  -vf "hwupload,tonemap_opencl=tonemap=hable:transfer=bt709:matrix=bt709:primaries=bt709,hwdownload,format=yuv420p" \
  sdr_output.mp4

# Reinhard tonemapping
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i hdr_input.mp4 \
  -vf "hwupload,tonemap_opencl=tonemap=reinhard:param=0.5,hwdownload,format=yuv420p" \
  sdr_output.mp4
```

**tonemap_opencl algorithms:**
| Algorithm | Description |
|-----------|-------------|
| `none` | No tonemapping |
| `clip` | Simple clipping |
| `linear` | Linear scaling |
| `gamma` | Gamma-based |
| `reinhard` | Reinhard operator |
| `hable` | Hable/Filmic (most popular) |
| `mobius` | Mobius (preserves blacks) |
| `bt2390` | ITU-R BT.2390 (broadcast standard) |

### OpenCL Blur

```bash
# Box blur
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,avgblur_opencl=sizeX=5:sizeY=5,hwdownload,format=yuv420p" \
  output.mp4
```

### OpenCL Custom Convolution

```bash
# Edge detection kernel
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,convolution_opencl=0m='-1 -1 -1 -1 8 -1 -1 -1 -1':0rdiv=1:0bias=128,hwdownload,format=yuv420p" \
  output.mp4

# Sharpen kernel
ffmpeg -init_hw_device opencl=gpu \
  -filter_hw_device gpu \
  -i input.mp4 \
  -vf "hwupload,convolution_opencl=0m='0 -1 0 -1 5 -1 0 -1 0':0rdiv=1:0bias=0,hwdownload,format=yuv420p" \
  output.mp4
```

## GPU Filter Comparison

### Cross-Platform Filter Availability

| Filter Type | CUDA | Vulkan | OpenCL | VAAPI | QSV |
|-------------|------|--------|--------|-------|-----|
| Scaling | ✅ `scale_cuda` | ✅ `scale_vulkan` | ✅ `scale_opencl` | ✅ `scale_vaapi` | ✅ `vpp_qsv` |
| Overlay | ✅ `overlay_cuda` | ✅ `overlay_vulkan` | ✅ `overlay_opencl` | - | - |
| Denoising | ✅ `bilateral_cuda` | ✅ `nlmeans_vulkan` | ✅ `nlmeans_opencl` | - | - |
| Deinterlace | ✅ `bwdif_cuda` | ✅ `bwdif_vulkan` | - | ✅ `deinterlace_vaapi` | ✅ `vpp_qsv` |
| Chromakey | ✅ `chromakey_cuda` | - | ✅ `colorkey_opencl` | - | - |
| Tonemapping | - | ✅ `libplacebo` | ✅ `tonemap_opencl` | ✅ `tonemap_vaapi` | - |
| Stabilization | - | - | ✅ `deshake_opencl` | - | - |
| Padding | ✅ `pad_cuda` | - | ✅ `pad_opencl` | - | - |

### Performance Comparison

| API | Platform Support | Filter Variety | Performance |
|-----|------------------|----------------|-------------|
| CUDA | NVIDIA only | Excellent | Best on NVIDIA |
| Vulkan | Cross-platform | Good (growing) | Very good |
| OpenCL | Cross-platform | Good | Good |
| VAAPI | Linux only | Limited | Good on Linux |
| QSV | Intel only | Limited | Good on Intel |

## Docker with Hardware Acceleration

### NVIDIA GPU in Docker

```bash
# Run with NVIDIA GPU support
docker run --gpus all \
  --rm \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:nvidia \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i /data/input.mp4 \
  -c:v h264_nvenc \
  /data/output.mp4
```

### Intel QSV in Docker

```bash
# Run with Intel GPU access
docker run --rm \
  --device=/dev/dri:/dev/dri \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:vaapi \
  -hwaccel qsv \
  -i /data/input.mp4 \
  -c:v h264_qsv \
  /data/output.mp4
```

## Troubleshooting

### Common Issues

**"No NVENC capable devices found"**
```bash
# Check GPU support
nvidia-smi
# Verify driver version
nvidia-smi --query-gpu=driver_version --format=csv
# Check CUDA version
nvcc --version
```

**"Cannot load libcuda.so"**
```bash
# Set library path (Linux)
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

**QSV "Unsupported format"**
```bash
# Force pixel format conversion
ffmpeg -i input.mp4 \
  -vf "format=nv12" \
  -c:v h264_qsv \
  output.mp4
```

**VAAPI permission denied**
```bash
# Add user to video/render group
sudo usermod -aG video $USER
sudo usermod -aG render $USER
# Re-login or use newgrp
```

### Performance Debugging

```bash
# Benchmark encode speed
ffmpeg -benchmark -i input.mp4 -c:v h264_nvenc -f null -

# Show hardware decode stats
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -benchmark -i input.mp4 -f null -

# Monitor GPU usage (NVIDIA)
nvidia-smi dmon -s u

# Monitor GPU usage (Intel)
intel_gpu_top
```

## Best Practices

1. **Use full GPU pipelines** when possible to avoid CPU-GPU memory transfers
2. **Match decode and encode hardware** for best performance
3. **Use appropriate presets** - faster isn't always better for quality
4. **Enable lookahead and AQ** for quality-critical encodes
5. **Test on target hardware** - quality varies by GPU generation
6. **Monitor GPU memory** for high-resolution content
7. **Consider power efficiency** for laptops and servers
8. **Update drivers regularly** for performance and feature improvements

## Recommended Settings by Use Case

### Live Streaming
```bash
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input \
  -c:v h264_nvenc -preset p3 -tune ll -zerolatency 1 -b:v 6M \
  -f flv rtmp://server/live/stream
```

### VOD Encoding (Quality)
```bash
ffmpeg -i input.mp4 \
  -c:v hevc_nvenc -preset p6 -tune hq \
  -rc vbr -cq 22 -b:v 0 \
  -rc-lookahead 32 -spatial-aq 1 \
  output.mp4
```

### Batch Processing
```bash
# Multiple parallel streams on one GPU
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input1.mp4 -c:v h264_nvenc output1.mp4 &
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input2.mp4 -c:v h264_nvenc output2.mp4 &
wait
```

This guide covers hardware acceleration fundamentals. For specific platform optimizations and advanced configurations, consult the respective vendor documentation.
