---
name: ffmpeg-modal-containers
description: Complete Modal.com FFmpeg deployment system for serverless video processing. PROACTIVELY activate for: (1) Modal.com FFmpeg container setup, (2) GPU-accelerated video encoding on Modal (NVIDIA, NVENC), (3) Parallel video processing with Modal map/starmap, (4) Volume mounting for large video files, (5) CPU vs GPU container cost optimization, (6) apt_install/pip_install for FFmpeg, (7) Python subprocess FFmpeg patterns, (8) Batch video transcoding at scale, (9) Modal pricing for video workloads, (10) Audio/video processing with Whisper. Provides: Image configuration examples, GPU container patterns, parallel processing code, volume usage, cost comparisons, production-ready FFmpeg deployments. Ensures: Efficient, scalable video processing on Modal serverless infrastructure.
---

## Quick Reference

| Container Type | Image Setup | GPU | Use Case |
|---------------|-------------|-----|----------|
| CPU (debian_slim) | `.apt_install("ffmpeg")` | No | Batch processing, I/O-bound tasks |
| GPU (debian_slim) | `.apt_install("ffmpeg").pip_install("torch")` | Yes | ML inference, not NVENC |
| GPU (CUDA image) | `from_registry("nvidia/cuda:...")` | Yes | Full CUDA toolkit, NVENC possible |

| GPU Type | Price/Hour | NVENC | Best For |
|----------|-----------|-------|----------|
| T4 | ~$0.59 | Yes (Turing) | Inference + encoding |
| A10G | ~$1.10 | Yes (Ampere) | 4K encoding, ML |
| L40S | ~$1.95 | Yes (Ada) | Heavy ML + video |
| H100 | ~$4.25 | Yes (Hopper) | Training, overkill for video |

## When to Use This Skill

Use for **serverless video processing**:
- Batch transcoding that needs to scale to hundreds of containers
- Parallel video processing with Modal's map/starmap
- GPU-accelerated encoding (with limitations on NVENC)
- Cost-effective burst processing (pay only for execution time)
- Integration with ML models (Whisper, video analysis)

**Key decision**: Modal excels at parallel CPU workloads and ML inference on GPU. For pure hardware NVENC encoding, verify GPU capabilities first.

---

# FFmpeg on Modal.com (2025)

Complete guide to running FFmpeg on Modal's serverless Python platform with CPU and GPU containers.

## Overview

Modal is a serverless platform for running Python code in the cloud with:
- **Sub-second cold starts** - Containers spin up in milliseconds
- **Elastic GPU capacity** - Access T4, A10G, L40S, H100 GPUs
- **Parallel processing** - Scale to thousands of containers instantly
- **Pay-per-use** - Billed by CPU cycle, not idle time

### Modal vs Traditional Cloud

| Feature | Modal | Traditional VMs |
|---------|-------|-----------------|
| Cold start | <1 second | Minutes |
| Scaling | Automatic to 1000s | Manual setup |
| Billing | Per execution | Per hour |
| GPU access | `gpu="any"` decorator | Complex provisioning |
| Setup | Python decorators | Infrastructure as code |

## Basic FFmpeg Setup

### CPU Container (Simplest)

```python
import modal
import subprocess
from pathlib import Path

app = modal.App("ffmpeg-processor")

# Create image with FFmpeg installed
ffmpeg_image = modal.Image.debian_slim(python_version="3.12").apt_install("ffmpeg")

@app.function(image=ffmpeg_image)
def transcode_video(input_bytes: bytes, output_format: str = "mp4") -> bytes:
    """Transcode video to specified format."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input"
        output_path = Path(tmpdir) / f"output.{output_format}"

        # Write input file
        input_path.write_bytes(input_bytes)

        # Run FFmpeg
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output_path)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        return output_path.read_bytes()

@app.local_entrypoint()
def main():
    # Read local file
    video_bytes = Path("input.mp4").read_bytes()

    # Process remotely on Modal
    output_bytes = transcode_video.remote(video_bytes)

    # Save result locally
    Path("output.mp4").write_bytes(output_bytes)
    print("Transcoding complete!")
```

### Running Your First Modal App

```bash
# Install Modal
pip install modal

# Authenticate (one-time)
modal setup

# Run the app
modal run your_script.py
```

## GPU Containers

### Basic GPU Setup for ML + FFmpeg

```python
import modal

app = modal.App("ffmpeg-gpu")

# GPU image with FFmpeg and PyTorch
gpu_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg")
    .pip_install("torch", "torchaudio", "transformers")
)

@app.function(image=gpu_image, gpu="T4")
def transcribe_and_process(audio_bytes: bytes) -> dict:
    """Transcribe audio with Whisper, then process with FFmpeg."""
    import tempfile
    import torch
    from transformers import pipeline

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp3"
        input_path.write_bytes(audio_bytes)

        # GPU-accelerated transcription
        transcriber = pipeline(
            model="openai/whisper-base",
            device="cuda"
        )
        result = transcriber(str(input_path))

        # FFmpeg audio normalization (CPU-based in this setup)
        normalized_path = Path(tmpdir) / "normalized.mp3"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            str(normalized_path)
        ], check=True)

        return {
            "transcription": result["text"],
            "normalized_audio": normalized_path.read_bytes()
        }
```

### Full CUDA Toolkit for Advanced GPU Features

For NVENC or full CUDA toolkit requirements:

```python
import modal

cuda_version = "12.4.0"
flavor = "devel"  # Full toolkit
os_version = "ubuntu22.04"
tag = f"{cuda_version}-{flavor}-{os_version}"

# Full CUDA image with FFmpeg
cuda_ffmpeg_image = (
    modal.Image.from_registry(f"nvidia/cuda:{tag}", add_python="3.12")
    .entrypoint([])  # Remove base image entrypoint
    .apt_install(
        "ffmpeg",
        "git",
        "libglib2.0-0",
        "libsm6",
        "libxrender1",
        "libxext6",
        "libgl1",
    )
    .pip_install("numpy", "Pillow")
)

app = modal.App("ffmpeg-cuda")

@app.function(image=cuda_ffmpeg_image, gpu="A10G")
def gpu_transcode(input_bytes: bytes) -> bytes:
    """Transcode video with GPU acceleration if available."""
    import subprocess
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp4"
        output_path = Path(tmpdir) / "output.mp4"

        input_path.write_bytes(input_bytes)

        # Check for NVENC support
        check_result = subprocess.run(
            ["ffmpeg", "-encoders"],
            capture_output=True,
            text=True
        )

        has_nvenc = "h264_nvenc" in check_result.stdout

        if has_nvenc:
            # GPU encoding with NVENC
            cmd = [
                "ffmpeg", "-y",
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-i", str(input_path),
                "-c:v", "h264_nvenc",
                "-preset", "p4",
                "-cq", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                str(output_path)
            ]
        else:
            # Fallback to CPU encoding
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                str(output_path)
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        return output_path.read_bytes()
```

### Important Note on NVENC Support

Modal's GPU containers use NVIDIA GPUs primarily for ML inference. NVENC video encoding support depends on:

1. **FFmpeg build** - Must include `--enable-nvenc`
2. **NVIDIA drivers** - Must expose video encoding capabilities
3. **Container setup** - May require `NVIDIA_DRIVER_CAPABILITIES=compute,video,utility`

For guaranteed NVENC support, use a custom Docker image or verify with:

```python
@app.function(image=cuda_ffmpeg_image, gpu="T4")
def check_nvenc():
    """Check NVENC availability."""
    import subprocess

    # Check GPU
    gpu_result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
    print("GPU Info:", gpu_result.stdout)

    # Check FFmpeg encoders
    enc_result = subprocess.run(
        ["ffmpeg", "-encoders"],
        capture_output=True,
        text=True
    )

    nvenc_encoders = [line for line in enc_result.stdout.split('\n') if 'nvenc' in line]
    print("NVENC Encoders:", nvenc_encoders)

    return {
        "has_nvenc": len(nvenc_encoders) > 0,
        "encoders": nvenc_encoders
    }
```

## Parallel Video Processing

Modal's killer feature for video processing is parallel execution across many containers.

### Batch Processing with map()

```python
import modal
from pathlib import Path

app = modal.App("batch-transcode")

ffmpeg_image = modal.Image.debian_slim().apt_install("ffmpeg")

@app.function(image=ffmpeg_image, timeout=600)
def transcode_single(video_bytes: bytes, video_id: str) -> tuple[str, bytes]:
    """Transcode a single video."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input"
        output_path = Path(tmpdir) / "output.mp4"

        input_path.write_bytes(video_bytes)

        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            str(output_path)
        ], check=True, capture_output=True)

        return video_id, output_path.read_bytes()

@app.local_entrypoint()
def main():
    # Prepare batch of videos
    video_files = list(Path("videos").glob("*.mp4"))
    inputs = [(f.read_bytes(), f.stem) for f in video_files]

    # Process all videos in parallel (up to 100 containers)
    results = list(transcode_single.starmap(inputs))

    # Save results
    for video_id, output_bytes in results:
        Path(f"output/{video_id}.mp4").write_bytes(output_bytes)
        print(f"Processed: {video_id}")
```

### Frame-by-Frame Parallel Processing

For maximum parallelism, process frames independently:

```python
import modal
from pathlib import Path

app = modal.App("parallel-frames")

ffmpeg_image = modal.Image.debian_slim().apt_install("ffmpeg")

@app.function(image=ffmpeg_image)
def extract_frames(video_bytes: bytes, fps: int = 1) -> list[bytes]:
    """Extract frames from video."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp4"
        input_path.write_bytes(video_bytes)

        # Extract frames
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vf", f"fps={fps}",
            f"{tmpdir}/frame_%04d.png"
        ], check=True, capture_output=True)

        # Read all frames
        frames = []
        for frame_path in sorted(Path(tmpdir).glob("frame_*.png")):
            frames.append(frame_path.read_bytes())

        return frames

@app.function(image=ffmpeg_image)
def process_frame(frame_bytes: bytes, frame_id: int) -> bytes:
    """Process a single frame (add watermark, filter, etc.)."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "frame.png"
        output_path = Path(tmpdir) / "processed.png"

        input_path.write_bytes(frame_bytes)

        # Apply processing (example: add text overlay)
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vf", f"drawtext=text='Frame {frame_id}':fontsize=24:fontcolor=white:x=10:y=10",
            str(output_path)
        ], check=True, capture_output=True)

        return output_path.read_bytes()

@app.function(image=ffmpeg_image)
def combine_frames(frames: list[bytes], fps: int = 24) -> bytes:
    """Combine processed frames back into video."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Write frames
        for i, frame_bytes in enumerate(frames):
            frame_path = Path(tmpdir) / f"frame_{i:04d}.png"
            frame_path.write_bytes(frame_bytes)

        output_path = Path(tmpdir) / "output.mp4"

        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", f"{tmpdir}/frame_%04d.png",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ], check=True, capture_output=True)

        return output_path.read_bytes()

@app.local_entrypoint()
def main():
    video_bytes = Path("input.mp4").read_bytes()

    # Step 1: Extract frames (single container)
    frames = extract_frames.remote(video_bytes, fps=24)
    print(f"Extracted {len(frames)} frames")

    # Step 2: Process frames in parallel (many containers)
    args = [(frame, i) for i, frame in enumerate(frames)]
    processed_frames = list(process_frame.starmap(args))
    print(f"Processed {len(processed_frames)} frames")

    # Step 3: Combine frames (single container)
    output = combine_frames.remote(processed_frames, fps=24)

    Path("output.mp4").write_bytes(output)
    print("Video processing complete!")
```

## Modal Volumes for Large Files

For video files too large to pass as function arguments, use Modal Volumes:

### Volume Setup and Usage

```python
import modal
from pathlib import Path

app = modal.App("video-volume")

# Create persistent volume for video storage
video_volume = modal.Volume.from_name("video-storage", create_if_missing=True)

ffmpeg_image = modal.Image.debian_slim().apt_install("ffmpeg")

@app.function(
    image=ffmpeg_image,
    volumes={"/data": video_volume},
    timeout=1800  # 30 minutes for large files
)
def transcode_from_volume(input_filename: str, output_filename: str):
    """Transcode video from volume to volume."""
    import subprocess

    input_path = Path("/data") / input_filename
    output_path = Path("/data") / output_filename

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_path)
    ], check=True, capture_output=True)

    # Commit changes to volume (important!)
    video_volume.commit()

    return f"Transcoded: {output_filename}"

@app.function(volumes={"/data": video_volume})
def list_videos():
    """List all videos in the volume."""
    videos = list(Path("/data").glob("*.mp4"))
    return [v.name for v in videos]

@app.local_entrypoint()
def main():
    # Upload a file to the volume first
    # modal volume put video-storage local_video.mp4 video.mp4

    # Then transcode
    result = transcode_from_volume.remote("video.mp4", "video_transcoded.mp4")
    print(result)

    # List files
    files = list_videos.remote()
    print("Files in volume:", files)
```

### Uploading to Volumes

```bash
# Upload file to volume
modal volume put video-storage local_video.mp4 video.mp4

# Download file from volume
modal volume get video-storage video_transcoded.mp4 local_output.mp4

# List volume contents
modal volume ls video-storage
```

### Volume Best Practices

```python
@app.function(
    volumes={"/data": video_volume},
    ephemeral_disk=50 * 1024  # 50 GB ephemeral disk for temp files
)
def process_large_video(input_filename: str):
    """Process large video with ephemeral disk for temp storage."""
    import subprocess
    import shutil

    # Copy from volume to ephemeral disk for faster I/O
    input_volume_path = Path("/data") / input_filename
    temp_input = Path("/tmp") / input_filename
    shutil.copy(input_volume_path, temp_input)

    temp_output = Path("/tmp") / "output.mp4"

    # Process on fast ephemeral disk
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(temp_input),
        "-c:v", "libx264",
        "-preset", "slow",  # Higher quality, more processing
        "-crf", "18",
        str(temp_output)
    ], check=True, capture_output=True)

    # Copy result back to volume
    output_volume_path = Path("/data") / f"processed_{input_filename}"
    shutil.copy(temp_output, output_volume_path)

    # Commit to persist
    video_volume.commit()

    return str(output_volume_path)
```

## Cost Optimization

### CPU vs GPU Pricing

```python
# Modal pricing (approximate, 2025):
# - CPU: ~$0.000024/vCPU-second
# - Memory: ~$0.0000025/GiB-second
# - T4 GPU: ~$0.000164/second ($0.59/hour)
# - A10G GPU: ~$0.000306/second ($1.10/hour)
# - L40S GPU: ~$0.000542/second ($1.95/hour)

# For a 10-second video transcode:
# - CPU (4 cores, 10 seconds): ~$0.001
# - GPU (T4, 2 seconds): ~$0.0003

# For 1000 videos:
# - CPU: ~$1.00, parallelized across 100 containers = ~10 seconds wall time
# - GPU: ~$0.30, but harder to parallelize

# Recommendation: Use CPU for transcoding, GPU for ML inference
```

### Resource Configuration

```python
@app.function(
    image=ffmpeg_image,
    cpu=4,          # 4 CPU cores
    memory=8192,    # 8 GB RAM
    timeout=300,    # 5 minute timeout
)
def optimized_transcode(video_bytes: bytes) -> bytes:
    """Transcode with optimized resource allocation."""
    # Use all available CPU cores
    subprocess.run([
        "ffmpeg", "-y",
        "-threads", "4",  # Match CPU allocation
        "-i", "input.mp4",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "output.mp4"
    ], check=True)
```

### When to Use GPU

| Task | Recommendation | Reason |
|------|---------------|--------|
| Transcoding only | CPU | libx264 is fast, parallelizes well |
| Whisper transcription | GPU | ML inference, 10x+ faster |
| Video analysis (YOLO) | GPU | ML inference required |
| Thumbnail generation | CPU | Simple extraction |
| Audio normalization | CPU | No GPU benefit |
| NVENC encoding | GPU (verify) | May not be available |

## Production Patterns

### Error Handling and Retries

```python
import modal
from modal import Retries

app = modal.App("production-ffmpeg")

ffmpeg_image = modal.Image.debian_slim().apt_install("ffmpeg")

@app.function(
    image=ffmpeg_image,
    retries=Retries(
        max_retries=3,
        initial_delay=1.0,
        backoff_coefficient=2.0,
    ),
    timeout=600,
)
def reliable_transcode(video_bytes: bytes) -> bytes:
    """Transcode with automatic retries."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input"
        output_path = Path(tmpdir) / "output.mp4"

        input_path.write_bytes(video_bytes)

        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            str(output_path)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            # Log error for debugging
            print(f"FFmpeg stderr: {result.stderr}")
            raise RuntimeError(f"FFmpeg failed: {result.returncode}")

        return output_path.read_bytes()
```

### Webhook Integration

```python
import modal

app = modal.App("ffmpeg-webhook")

ffmpeg_image = modal.Image.debian_slim().apt_install("ffmpeg", "curl")

@app.function(image=ffmpeg_image)
def transcode_with_webhook(
    video_bytes: bytes,
    webhook_url: str,
    job_id: str
) -> str:
    """Transcode and notify webhook on completion."""
    import subprocess
    import tempfile
    import json

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input"
        output_path = Path(tmpdir) / "output.mp4"

        input_path.write_bytes(video_bytes)

        try:
            subprocess.run([
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                str(output_path)
            ], check=True, capture_output=True)

            status = "success"
            output_size = output_path.stat().st_size

        except subprocess.CalledProcessError as e:
            status = "failed"
            output_size = 0

        # Notify webhook
        payload = json.dumps({
            "job_id": job_id,
            "status": status,
            "output_size": output_size
        })

        subprocess.run([
            "curl", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", payload,
            webhook_url
        ], check=True)

        return status
```

### Web Endpoint

```python
import modal
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse
import io

app = modal.App("ffmpeg-api")

ffmpeg_image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg")
    .pip_install("fastapi[standard]", "python-multipart")
)

web_app = FastAPI()

@web_app.post("/transcode")
async def transcode_endpoint(file: UploadFile):
    """HTTP endpoint for video transcoding."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input"
        output_path = Path(tmpdir) / "output.mp4"

        # Save uploaded file
        content = await file.read()
        input_path.write_bytes(content)

        # Transcode
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "28",
            str(output_path)
        ], check=True, capture_output=True)

        # Stream response
        output_bytes = output_path.read_bytes()
        return StreamingResponse(
            io.BytesIO(output_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=output.mp4"}
        )

@app.function(image=ffmpeg_image)
@modal.asgi_app()
def fastapi_app():
    return web_app
```

## Audio Processing with Whisper

Complete pattern for audio transcription and processing:

```python
import modal

app = modal.App("whisper-ffmpeg")

# Image with FFmpeg and Whisper dependencies
whisper_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg")
    .pip_install(
        "transformers[torch]",
        "accelerate",
        "torch",
        "torchaudio",
    )
)

@app.function(image=whisper_image, gpu="T4", timeout=600)
def transcribe_video(video_bytes: bytes) -> dict:
    """Extract audio from video and transcribe with Whisper."""
    import subprocess
    import tempfile
    from transformers import pipeline

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = Path(tmpdir) / "video.mp4"
        audio_path = Path(tmpdir) / "audio.wav"

        video_path.write_bytes(video_bytes)

        # Extract audio with FFmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vn",                    # No video
            "-acodec", "pcm_s16le",   # WAV format
            "-ar", "16000",           # 16kHz for Whisper
            "-ac", "1",               # Mono
            str(audio_path)
        ], check=True, capture_output=True)

        # Transcribe with Whisper
        transcriber = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
            device="cuda"
        )

        result = transcriber(str(audio_path))

        return {
            "text": result["text"],
            "audio_duration": get_duration(str(audio_path))
        }

def get_duration(audio_path: str) -> float:
    """Get audio duration using FFprobe."""
    import subprocess
    import json

    result = subprocess.run([
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        audio_path
    ], capture_output=True, text=True)

    data = json.loads(result.stdout)
    return float(data["format"]["duration"])
```

## Troubleshooting

### Common Issues

**FFmpeg not found:**
```python
# Verify FFmpeg is installed in your image
@app.function(image=ffmpeg_image)
def check_ffmpeg():
    import subprocess
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0
```

**Out of memory:**
```python
# Increase memory allocation
@app.function(image=ffmpeg_image, memory=16384)  # 16 GB
def process_large_video(video_bytes: bytes):
    pass
```

**Timeout errors:**
```python
# Increase timeout for long operations
@app.function(image=ffmpeg_image, timeout=3600)  # 1 hour
def transcode_4k_video(video_bytes: bytes):
    pass
```

**Volume not persisting:**
```python
# Always call commit() after writing to volume
@app.function(volumes={"/data": video_volume})
def write_to_volume():
    Path("/data/output.mp4").write_bytes(data)
    video_volume.commit()  # Critical!
```

### Debugging FFmpeg Commands

```python
@app.function(image=ffmpeg_image)
def debug_transcode(video_bytes: bytes):
    """Transcode with full debugging output."""
    import subprocess

    result = subprocess.run([
        "ffmpeg", "-y",
        "-v", "verbose",  # Verbose logging
        "-i", "input.mp4",
        "-c:v", "libx264",
        "output.mp4"
    ], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)

    return result.returncode == 0
```

## Best Practices

1. **Use CPU for transcoding** - GPU is overkill for most encoding
2. **Parallelize with map/starmap** - Process many files simultaneously
3. **Use Volumes for large files** - Avoid passing large data as arguments
4. **Set appropriate timeouts** - Video processing can be slow
5. **Commit Volume changes** - Always call `commit()` after writes
6. **Use ephemeral disk** - For temp files during processing
7. **Monitor costs** - Track execution time and resource usage
8. **Handle errors gracefully** - FFmpeg can fail on corrupt inputs
9. **Use fast presets for testing** - Switch to slower for production
10. **Verify GPU capabilities** - NVENC may not be available

## Related Skills

- **ffmpeg-opencv-integration** - For FFmpeg + OpenCV combined pipelines, including:
  - BGR/RGB color format conversion (OpenCV=BGR, FFmpeg=RGB)
  - Frame coordinate gotchas (img[y,x] not img[x,y])
  - ffmpegcv for GPU-accelerated video I/O (NVDEC/NVENC)
  - VidGear for multi-threaded streaming
  - Decord for ML batch video loading (2x faster than OpenCV)
  - PyAV for frame-level precision
  - Parallel frame processing patterns with Modal map()

## References

- [Modal Documentation](https://modal.com/docs)
- [Modal Examples - Blender Video](https://modal.com/docs/examples/blender_video)
- [Modal CUDA Guide](https://modal.com/docs/guide/cuda)
- [Modal Volumes](https://modal.com/docs/guide/volumes)
- [Modal Pricing](https://modal.com/pricing)
