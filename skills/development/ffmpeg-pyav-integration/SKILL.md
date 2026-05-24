---
name: ffmpeg-pyav-integration
description: Complete PyAV (Python FFmpeg bindings) integration guide. PROACTIVELY activate for: (1) PyAV installation on Ubuntu/Windows/macOS, (2) Building PyAV against custom FFmpeg, (3) FFmpeg 7.0/8.0+ compatibility, (4) av.open() video/audio decoding, (5) VideoFrame/AudioFrame NumPy conversion, (6) Filter graph processing, (7) Video encoding with H.264/H.265/AV1, (8) Seeking and keyframe extraction, (9) RTSP/network streaming with PyAV, (10) Memory management and thread safety, (11) Error handling with FFmpegError, (12) Subtitle extraction, (13) Container manipulation and remuxing, (14) Performance optimization and threading. Provides: Complete PyAV API patterns, installation guides for all Ubuntu versions, FFmpeg 8.0+ compatibility matrix, type-safe examples, memory management best practices, filter graph examples, encoding/decoding patterns.
---

# PyAV Integration Guide (2025-2026)

Complete reference for PyAV - Pythonic bindings for FFmpeg's libraries.

## Quick Reference

| Task | PyAV Method | Notes |
|------|-------------|-------|
| Open video | `av.open('video.mp4')` | Returns Container |
| Decode frames | `container.decode(video=0)` | Yields VideoFrame |
| Frame to NumPy | `frame.to_ndarray(format='rgb24')` | RGB by default |
| NumPy to Frame | `av.VideoFrame.from_ndarray(arr, format='rgb24')` | For encoding |
| Seek | `container.seek(offset)` | Keyframe-based |
| Encode | `stream.encode(frame)` | Returns packets |
| Close | `container.close()` | ALWAYS do this |

| Version | FFmpeg Requirement | Python Requirement |
|---------|-------------------|-------------------|
| PyAV 16.1.0 (Latest) | FFmpeg 7.0+ | Python 3.10+ |
| PyAV 14.x | FFmpeg 7.0+ | Python 3.9+ |
| PyAV 12.x | FFmpeg 5.0+ | Python 3.8+ |
| PyAV 8.x-10.x | FFmpeg 4.0+ | Python 3.7+ |

---

## What is PyAV?

PyAV provides **Pythonic bindings for FFmpeg's libraries** (libavcodec, libavformat, libavfilter, etc.), offering direct access to:

- **Containers**: Media file handling (MP4, MKV, WebM, etc.)
- **Streams**: Audio, video, and subtitle tracks
- **Packets**: Compressed data units
- **Frames**: Decoded video/audio data
- **Codecs**: Encoding/decoding capabilities
- **Filters**: FFmpeg filter graph access

**Key Features:**
- Direct NumPy/Pillow integration for frame data
- Frame-level precision for seeking and manipulation
- Full codec and filter access
- Lower-level control than ffmpeg-python subprocess

**When to Use PyAV vs FFmpeg CLI:**
- Use **PyAV** when you need programmatic frame-level access
- Use **FFmpeg CLI** for simple transcoding tasks
- PyAV adds complexity - only use when CLI cannot solve your problem

---

## Installation

### Quick Install (Recommended)

Binary wheels include FFmpeg libraries - no separate FFmpeg installation needed:

```bash
pip install av
```

Or with Conda:

```bash
conda install av -c conda-forge
```

### Ubuntu Installation

#### Ubuntu 24.04 LTS (Noble)

```bash
# Option 1: pip with pre-built wheels (recommended)
pip install av

# Option 2: Build against system FFmpeg
sudo apt update
sudo apt install -y python3-dev pkg-config \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
pip install av --no-binary av
```

#### Ubuntu 22.04 LTS (Jammy)

```bash
# Option 1: pip with pre-built wheels (recommended)
pip install av

# Option 2: Build against system FFmpeg
sudo apt update
sudo apt install -y python3-dev pkg-config \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
pip install av --no-binary av
```

#### Ubuntu 20.04 LTS (Focal)

```bash
# System FFmpeg is 4.2 - too old for PyAV 14+
# Option 1: Use pip wheels (recommended)
pip install av

# Option 2: Install newer FFmpeg from PPA first
sudo add-apt-repository ppa:savoury1/ffmpeg4
sudo apt update
sudo apt install -y ffmpeg libavformat-dev libavcodec-dev \
    libavdevice-dev libavutil-dev libswscale-dev \
    libswresample-dev libavfilter-dev python3-dev pkg-config
pip install av --no-binary av
```

### macOS Installation

```bash
# Option 1: pip wheels (recommended)
pip install av

# Option 2: Build against Homebrew FFmpeg
brew install ffmpeg pkg-config
pip install av --no-binary av
```

### Windows Installation

```bash
# Recommended: Use pip wheels
pip install av

# Building from source requires MSYS2 environment
```

### Docker Installation

```dockerfile
FROM python:3.12-slim

# Install system FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install PyAV with pre-built wheels
RUN pip install av

# Or build against system FFmpeg:
# RUN apt-get install -y python3-dev pkg-config \
#     libavformat-dev libavcodec-dev libavdevice-dev \
#     libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
# RUN pip install av --no-binary av
```

---

## Building Against Custom FFmpeg

To use PyAV with a custom FFmpeg installation (e.g., FFmpeg 8.0+):

### Step 1: Build FFmpeg

```bash
# Example: Build FFmpeg 8.0 from source
git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
git checkout n8.0

./configure \
    --prefix=/opt/ffmpeg-8.0 \
    --enable-shared \
    --enable-gpl \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libvpx \
    --enable-libopus

make -j$(nproc)
sudo make install
```

### Step 2: Set Environment Variables

```bash
# Point pkg-config to custom FFmpeg
export PKG_CONFIG_PATH=/opt/ffmpeg-8.0/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/opt/ffmpeg-8.0/lib:$LD_LIBRARY_PATH

# Verify pkg-config finds FFmpeg
pkg-config --modversion libavcodec  # Should show 61.x for FFmpeg 8.0
```

### Step 3: Install PyAV from Source

```bash
# Force source build (ignores binary wheels)
pip install av --no-binary av

# Or clone and build directly
git clone https://github.com/PyAV-Org/PyAV.git
cd PyAV
pip install .
```

### Step 4: Verify Installation

```python
import av
print(f"PyAV version: {av.__version__}")

# Check available codecs
print("H.264 available:", 'libx264' in av.codecs_available)
print("H.265 available:", 'libx265' in av.codecs_available)

# Check FFmpeg library versions
container = av.open('test.mp4')
print(f"Container format: {container.format.name}")
```

---

## FFmpeg 8.0+ Compatibility

### PyAV-FFmpeg Package Versions

The PyAV project maintains the `pyav-ffmpeg` package for bundled FFmpeg:

| pyav-ffmpeg Version | FFmpeg Version | Release Date | Notes |
|---------------------|----------------|--------------|-------|
| 8.0.1-5 | 8.0.1 | Jan 2025 | libopus 1.6.1, disabled static builds |
| 8.0.1-4 | 8.0.1 | Jan 2025 | Multi-arch support, unified build |
| 8.0.1-3 | 8.0.1 | Jan 2025 | Security fixes (libpng CVEs) |
| 8.0.1-2 | 8.0.1 | Jan 2025 | Intel QSV codec support |
| 8.0.1-1 | 8.0.1 | Dec 2024 | dav1d 1.5.2, AMD AMF, Opus 1.6 |
| 8.0-2 | 8.0 | Oct 2024 | macOS deployment target lowered |
| 8.0-1 | 8.0 | Aug 2024 | Initial FFmpeg 8.0 support |

### PyAV 16.1.0 + FFmpeg 8.0

PyAV 16.1.0 (released January 9, 2026) is compatible with FFmpeg 8.0+:

```python
# Install latest PyAV (includes FFmpeg 8.0 support in wheels)
pip install av

# Verify
import av
print(av.__version__)  # 16.1.0

# FFmpeg 8.0 features are available if using bundled FFmpeg
# or if built against FFmpeg 8.0+
```

### FFmpeg 8.0 Features Accessible via PyAV

- **Whisper AI filter** (speech recognition)
- **VVC/H.266 decoding** (libvvdec)
- **APV codec** (Samsung Advanced Professional Video)
- **Vulkan compute codecs** (AV1, VP9, ProRes RAW)
- **WHIP muxer** (WebRTC streaming)

```python
import av

# Check for VVC decoder
if 'vvc' in [c.name for c in av.codecs_available]:
    print("VVC decoder available")

# Check for Whisper filter (FFmpeg 8.0+)
try:
    graph = av.filter.Graph()
    graph.add('whisper')
    print("Whisper filter available")
except av.FFmpegError:
    print("Whisper filter not available")
```

---

## Core Usage Patterns

### Opening and Decoding Video

```python
import av
import numpy as np

# Open video file
container = av.open('video.mp4')

# Access video stream
video_stream = container.streams.video[0]
print(f"Resolution: {video_stream.width}x{video_stream.height}")
print(f"FPS: {video_stream.average_rate}")
print(f"Duration: {container.duration / av.time_base} seconds")

# Decode frames
for frame in container.decode(video=0):
    # frame is a VideoFrame object
    print(f"Frame {frame.index}: pts={frame.pts}, time={frame.time}")

    # Convert to NumPy array (RGB format)
    array = frame.to_ndarray(format='rgb24')
    print(f"Array shape: {array.shape}")  # (height, width, 3)

    # For OpenCV (BGR format)
    import cv2
    bgr_array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

container.close()
```

### Context Manager Pattern (Recommended)

```python
import av

# Automatic cleanup with context manager
with av.open('video.mp4') as container:
    for frame in container.decode(video=0):
        array = frame.to_ndarray(format='rgb24')
        # Process frame...
# Container automatically closed
```

### Performance: Multi-threaded Decoding

```python
import av

container = av.open('video.mp4')

# Enable multi-threaded decoding (5x faster!)
container.streams.video[0].thread_type = 'AUTO'

for frame in container.decode(video=0):
    array = frame.to_ndarray(format='rgb24')
    # Process...

container.close()
```

**Thread Types:**
- `'SLICE'`: Default, threads cooperate on single frame
- `'FRAME'`: Threads decode independent frames
- `'AUTO'`: Best of both (recommended)

Note: `FRAME` threading increases decode delay by one frame per thread.

### Keyframe-Only Decoding

```python
import av

container = av.open('video.mp4')
stream = container.streams.video[0]

# Skip non-keyframes (much faster for thumbnails)
stream.codec_context.skip_frame = 'NONKEY'

for frame in container.decode(stream):
    # Only keyframes are decoded
    array = frame.to_ndarray(format='rgb24')
    print(f"Keyframe at {frame.time} seconds")

container.close()
```

---

## NumPy Integration

### Video Frame to NumPy

```python
import av
import numpy as np

container = av.open('video.mp4')
container.streams.video[0].thread_type = 'AUTO'

for frame in container.decode(video=0):
    # RGB24 format (most common)
    rgb_array = frame.to_ndarray(format='rgb24')
    # Shape: (height, width, 3), dtype: uint8

    # BGR24 for OpenCV
    bgr_array = frame.to_ndarray(format='bgr24')

    # Grayscale
    gray_array = frame.to_ndarray(format='gray')
    # Shape: (height, width), dtype: uint8

    # YUV420P (native format, more efficient)
    yuv_array = frame.to_ndarray(format='yuv420p')
    # Shape varies, contains Y, U, V planes

container.close()
```

### NumPy to Video Frame

```python
import av
import numpy as np

# Create RGB array
rgb_array = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

# Convert to VideoFrame
frame = av.VideoFrame.from_ndarray(rgb_array, format='rgb24')
print(f"Frame size: {frame.width}x{frame.height}")
```

### Complete Video Generation Example

```python
import av
import numpy as np

def generate_test_video(output_path: str, duration: float = 5.0, fps: int = 30):
    """Generate video from NumPy arrays."""

    container = av.open(output_path, mode='w')

    # Add video stream
    stream = container.add_stream('libx264', rate=fps)
    stream.width = 1920
    stream.height = 1080
    stream.pix_fmt = 'yuv420p'
    stream.options = {'crf': '23', 'preset': 'fast'}

    total_frames = int(duration * fps)

    for i in range(total_frames):
        # Generate gradient frame
        t = i / total_frames
        r = int(255 * t)
        g = int(255 * (1 - t))
        b = 128

        frame_rgb = np.full((1080, 1920, 3), [r, g, b], dtype=np.uint8)

        # Convert to VideoFrame
        frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')

        # Encode and mux
        for packet in stream.encode(frame):
            container.mux(packet)

    # Flush encoder
    for packet in stream.encode():
        container.mux(packet)

    container.close()
    print(f"Generated {output_path}")

generate_test_video('test_output.mp4')
```

---

## Encoding Video

### H.264 Encoding

```python
import av
import numpy as np

def encode_h264(frames: list[np.ndarray], output_path: str, fps: float = 30.0):
    """Encode NumPy frames to H.264 video."""

    height, width = frames[0].shape[:2]

    container = av.open(output_path, mode='w')

    # Try libx264, fall back to other H.264 encoders
    try:
        stream = container.add_stream('libx264', rate=fps)
    except av.FFmpegError:
        # Fall back to hardware encoder if available
        stream = container.add_stream('h264_videotoolbox', rate=fps)

    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.options = {
        'crf': '23',
        'preset': 'medium',
        'profile': 'high',
    }

    for frame_rgb in frames:
        frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')
        for packet in stream.encode(frame):
            container.mux(packet)

    # Flush
    for packet in stream.encode():
        container.mux(packet)

    container.close()
```

### H.265/HEVC Encoding

```python
import av

def encode_h265(frames: list, output_path: str, fps: float = 30.0):
    """Encode frames to H.265/HEVC."""

    height, width = frames[0].shape[:2]

    container = av.open(output_path, mode='w')
    stream = container.add_stream('libx265', rate=fps)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.options = {
        'crf': '28',
        'preset': 'medium',
    }

    for frame_rgb in frames:
        frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')
        for packet in stream.encode(frame):
            container.mux(packet)

    for packet in stream.encode():
        container.mux(packet)

    container.close()
```

### Codec Availability Check

```python
import av

def get_available_encoder(codec_list: list[str]) -> str:
    """Find first available encoder from list."""
    for codec_name in codec_list:
        try:
            codec = av.Codec(codec_name, 'w')
            return codec.name
        except av.FFmpegError:
            continue
    raise RuntimeError(f"No encoder available from: {codec_list}")

# Usage
h264_encoder = get_available_encoder(['libx264', 'h264_nvenc', 'h264_videotoolbox'])
h265_encoder = get_available_encoder(['libx265', 'hevc_nvenc', 'hevc_videotoolbox'])
print(f"H.264: {h264_encoder}, H.265: {h265_encoder}")
```

---

## Audio Processing

### Decoding Audio

```python
import av
import numpy as np

container = av.open('audio.mp3')

for frame in container.decode(audio=0):
    # Get audio samples as NumPy array
    # Shape: (channels, samples) for planar formats
    # Shape: (samples, channels) for interleaved formats
    array = frame.to_ndarray()

    print(f"Sample rate: {frame.sample_rate}")
    print(f"Channels: {frame.layout.channels}")
    print(f"Samples: {frame.samples}")
    print(f"Format: {frame.format.name}")
    print(f"Array shape: {array.shape}")

container.close()
```

### Encoding Audio (AAC)

```python
import av
import numpy as np

def encode_audio_aac(audio_data: np.ndarray, output_path: str, sample_rate: int = 44100):
    """Encode NumPy audio array to AAC."""

    container = av.open(output_path, mode='w')
    stream = container.add_stream('aac', rate=sample_rate)
    stream.layout = 'stereo'
    stream.format = 'fltp'  # Float planar

    # Ensure correct shape: (channels, samples)
    if audio_data.ndim == 1:
        audio_data = np.stack([audio_data, audio_data])  # Mono to stereo

    # Create AudioFrame
    frame = av.AudioFrame.from_ndarray(audio_data.astype(np.float32), format='fltp', layout='stereo')
    frame.sample_rate = sample_rate

    for packet in stream.encode(frame):
        container.mux(packet)

    for packet in stream.encode():
        container.mux(packet)

    container.close()
```

### Audio Resampling

```python
import av

container = av.open('input.mp3')
audio_stream = container.streams.audio[0]

# Create resampler
resampler = av.AudioResampler(
    format='s16',      # 16-bit signed integer
    layout='stereo',   # Stereo output
    rate=48000         # 48kHz sample rate
)

for frame in container.decode(audio_stream):
    # Resample frame
    resampled_frames = resampler.resample(frame)
    for resampled in resampled_frames:
        array = resampled.to_ndarray()
        # Process resampled audio...

container.close()
```

---

## Filter Graphs

### Basic Video Filter

```python
import av

container = av.open('input.mp4')
stream = container.streams.video[0]

# Create filter graph
graph = av.filter.Graph()

# Add buffer source (input)
buffer = graph.add_buffer(template=stream)

# Add scale filter
scale = graph.add('scale', 'w=1280:h=720')

# Add buffer sink (output)
buffersink = graph.add('buffersink')

# Link filters: buffer -> scale -> buffersink
buffer.link_to(scale)
scale.link_to(buffersink)

# Configure graph
graph.configure()

# Process frames
for frame in container.decode(stream):
    graph.push(frame)
    filtered_frame = graph.pull()

    # filtered_frame is now 1280x720
    array = filtered_frame.to_ndarray(format='rgb24')

container.close()
```

### Audio Filter (atempo - Speed Change)

```python
import av

def change_audio_speed(input_path: str, output_path: str, speed: float = 2.0):
    """Change audio playback speed using atempo filter."""

    input_container = av.open(input_path)
    output_container = av.open(output_path, mode='w')

    input_stream = input_container.streams.audio[0]
    output_stream = output_container.add_stream('aac')

    # Create filter graph
    graph = av.filter.Graph()

    # Add audio buffer (input)
    abuffer = graph.add_abuffer(
        template=input_stream,
    )

    # Add atempo filter
    atempo = graph.add('atempo', f'{speed}')

    # Add abuffersink (output)
    abuffersink = graph.add('abuffersink')

    # Link: abuffer -> atempo -> abuffersink
    abuffer.link_to(atempo)
    atempo.link_to(abuffersink)

    graph.configure()

    for frame in input_container.decode(input_stream):
        graph.push(frame)

        while True:
            try:
                filtered = graph.pull()
                for packet in output_stream.encode(filtered):
                    output_container.mux(packet)
            except av.error.BlockingIOError:
                break

    # Flush
    for packet in output_stream.encode():
        output_container.mux(packet)

    input_container.close()
    output_container.close()

change_audio_speed('input.mp3', 'output_2x.mp3', speed=2.0)
```

---

## Seeking

### Basic Seeking

```python
import av

container = av.open('video.mp4')
stream = container.streams.video[0]

# Seek to 10 seconds
# Note: offset is in stream time_base units
target_time = 10.0
target_pts = int(target_time / stream.time_base)

container.seek(target_pts, stream=stream)

# Decode frame at (approximately) 10 seconds
for frame in container.decode(stream):
    print(f"Frame at {frame.time} seconds")
    break

container.close()
```

### Accurate Frame Seeking

```python
import av

def get_frame_at_time(path: str, target_time: float):
    """Get frame at specific timestamp (accurate)."""

    container = av.open(path)
    stream = container.streams.video[0]

    # Seek to keyframe before target
    container.seek(int(target_time * av.time_base), backward=True)

    # Decode until we reach target time
    for frame in container.decode(stream):
        if frame.time >= target_time:
            array = frame.to_ndarray(format='rgb24')
            container.close()
            return array

    container.close()
    return None

frame = get_frame_at_time('video.mp4', 30.5)  # Frame at 30.5 seconds
```

### Seek Parameters

```python
import av

container = av.open('video.mp4')

# backward=True (default): Seek to keyframe at or before offset
# backward=False: Seek to keyframe at or after offset
container.seek(offset, backward=True)

# any_frame=True: Seek to any frame, not just keyframes
# Warning: May cause decoding artifacts
container.seek(offset, any_frame=True)

# stream: Specify which stream's time_base to use
container.seek(offset, stream=container.streams.video[0])
```

---

## Container Manipulation

### Remuxing (Copy Without Transcoding)

```python
import av

def remux_video(input_path: str, output_path: str):
    """Copy video to new container without transcoding."""

    input_container = av.open(input_path)
    output_container = av.open(output_path, mode='w')

    # Copy stream configurations
    for stream in input_container.streams:
        output_container.add_stream_from_template(stream)

    # Copy packets (no decoding/encoding)
    for packet in input_container.demux():
        if packet.dts is not None:
            output_container.mux(packet)

    input_container.close()
    output_container.close()

remux_video('input.mkv', 'output.mp4')
```

### Extract Video Segment

```python
import av

def extract_segment(input_path: str, output_path: str, start: float, end: float):
    """Extract video segment between start and end times."""

    input_container = av.open(input_path)
    output_container = av.open(output_path, mode='w')

    # Add streams
    video_in = input_container.streams.video[0]
    audio_in = input_container.streams.audio[0] if input_container.streams.audio else None

    video_out = output_container.add_stream('libx264', rate=video_in.average_rate)
    video_out.width = video_in.width
    video_out.height = video_in.height
    video_out.pix_fmt = 'yuv420p'

    if audio_in:
        audio_out = output_container.add_stream('aac', rate=audio_in.rate)

    # Seek to start
    input_container.seek(int(start * av.time_base))

    for frame in input_container.decode(video=0):
        if frame.time < start:
            continue
        if frame.time > end:
            break

        for packet in video_out.encode(frame):
            output_container.mux(packet)

    # Flush
    for packet in video_out.encode():
        output_container.mux(packet)

    input_container.close()
    output_container.close()

extract_segment('input.mp4', 'clip.mp4', start=10.0, end=20.0)
```

---

## Subtitles

### Reading Subtitles

```python
import av

container = av.open('video_with_subs.mkv')

# Check for subtitle streams
for i, stream in enumerate(container.streams.subtitle):
    print(f"Subtitle stream {i}: {stream.codec_context.name}")

# Decode subtitles
for packet in container.demux(container.streams.subtitle[0]):
    for subtitle in packet.decode():
        # subtitle is a SubtitleSet
        for rect in subtitle.rects:
            if hasattr(rect, 'ass'):
                # Text subtitle (ASS/SSA format)
                print(f"ASS: {rect.ass}")
                print(f"Dialogue: {rect.dialogue}")  # Without ASS formatting
            elif hasattr(rect, 'planes'):
                # Bitmap subtitle (DVD, Blu-ray)
                print(f"Bitmap: {rect.width}x{rect.height}")

container.close()
```

### SubtitleSet Properties

```python
import av

# When decoding subtitles:
# - subtitle.pts: Presentation timestamp
# - subtitle.start_display_time: When to show (relative to pts)
# - subtitle.end_display_time: When to hide
# - subtitle.format: 0=graphics, 1=text
# - subtitle.rects: List of Subtitle objects

# AssSubtitle properties:
# - rect.ass: Full ASS format string
# - rect.dialogue: Plain text (stripped of formatting)
# - rect.text: Rarely used
```

**Note:** Subtitle transcoding in PyAV is limited. For complex subtitle operations, consider using FFmpeg CLI directly.

---

## RTSP/Network Streaming

### Reading RTSP Stream

```python
import av

def read_rtsp_stream(url: str, timeout: int = 10):
    """Read frames from RTSP stream."""

    options = {
        'rtsp_transport': 'tcp',      # Use TCP (more reliable)
        'stimeout': str(timeout * 1000000),  # Timeout in microseconds
        'max_delay': '5000000',       # Max delay in microseconds
    }

    try:
        container = av.open(url, options=options, timeout=timeout)

        for frame in container.decode(video=0):
            array = frame.to_ndarray(format='rgb24')
            yield array

    except av.FFmpegError as e:
        print(f"Stream error: {e}")
    finally:
        if 'container' in locals():
            container.close()

# Usage
for frame in read_rtsp_stream('rtsp://192.168.1.100:554/stream'):
    # Process frame...
    pass
```

### RTSP with Reconnection

```python
import av
import time

def robust_rtsp_reader(url: str, max_retries: int = 5):
    """RTSP reader with automatic reconnection."""

    retries = 0

    while retries < max_retries:
        try:
            options = {
                'rtsp_transport': 'tcp',
                'stimeout': '5000000',
            }

            container = av.open(url, options=options)
            container.streams.video[0].thread_type = 'AUTO'

            for frame in container.decode(video=0):
                retries = 0  # Reset on successful frame
                yield frame.to_ndarray(format='rgb24')

        except av.FFmpegError as e:
            print(f"Connection error: {e}")
            retries += 1
            time.sleep(1)  # Wait before retry

        finally:
            if 'container' in locals():
                container.close()

    raise RuntimeError(f"Failed to connect after {max_retries} retries")
```

---

## Error Handling

### FFmpegError Exception

```python
import av

try:
    container = av.open('nonexistent.mp4')
except av.FFmpegError as e:
    print(f"FFmpeg error: {e}")
    print(f"Errno: {e.errno}")
    print(f"Message: {e.strerror}")
    print(f"Filename: {e.filename}")
    print(f"Log: {e.log}")  # Last FFmpeg log message

# Specific exception types
try:
    # ... operations
    pass
except av.error.InvalidDataError:
    print("Invalid or corrupt media data")
except av.error.FileNotFoundError:
    print("File not found")
except av.error.PermissionError:
    print("Permission denied")
except av.error.EOFError:
    print("End of file reached")
except av.FFmpegError as e:
    print(f"Other FFmpeg error: {e}")
```

### PyAV 14+ vs Earlier Versions

```python
# Handle exception name change in PyAV 14
try:
    FFmpegError = av.FFmpegError  # PyAV 14+
except AttributeError:
    FFmpegError = av.AVError      # PyAV < 14

try:
    container = av.open('video.mp4')
except FFmpegError as e:
    print(f"Error: {e}")
```

### Enable Logging for Debugging

```python
import av.logging

# Enable verbose logging (helpful for debugging)
av.logging.set_level(av.logging.VERBOSE)

# Now FFmpegError will include detailed log messages
try:
    container = av.open('corrupted.mp4')
except av.FFmpegError as e:
    print(f"Error with log: {e.log}")
```

---

## Memory Management Best Practices

### 1. Always Close Containers

```python
import av

# BAD: Container may not be closed promptly
container = av.open('video.mp4')
for frame in container.decode(video=0):
    pass
# Container eventually closed by GC, but timing is unpredictable

# GOOD: Use context manager
with av.open('video.mp4') as container:
    for frame in container.decode(video=0):
        pass
# Container closed immediately

# GOOD: Explicit close
container = av.open('video.mp4')
try:
    for frame in container.decode(video=0):
        pass
finally:
    container.close()
```

### 2. Reference Cycles

PyAV has reference cycles that can delay garbage collection. In tight loops, explicitly close containers:

```python
import av

# Processing many files
for path in file_list:
    container = av.open(path)
    try:
        # Process...
        pass
    finally:
        container.close()  # Critical in loops!
```

### 3. Frame Memory

VideoFrame and AudioFrame objects hold references to underlying buffers:

```python
import av
import numpy as np

container = av.open('video.mp4')

# Frames reference internal buffers - make copies if keeping data
stored_arrays = []
for frame in container.decode(video=0):
    # BAD: May reference freed memory after container closes
    # stored_arrays.append(frame.to_ndarray())

    # GOOD: Make explicit copy
    array = frame.to_ndarray(format='rgb24').copy()
    stored_arrays.append(array)

container.close()
# stored_arrays now contains independent copies
```

---

## Thread Safety

### Known Threading Issues

1. **Sub-interpreter incompatibility**: PyAV may cause lockups in WSGI applications
2. **Python file objects**: Passing file-like objects to `av.open()` can cause issues with threads
3. **Logging**: Multi-threaded encoding/decoding with logging enabled can cause lockups

### Safe Threading Practices

```python
import av
import av.logging

# Disable logging in multi-threaded applications
av.logging.set_level(av.logging.PANIC)

# Use file paths instead of file objects
# BAD: File object with threads
# container = av.open(file_object)

# GOOD: File path with threads
container = av.open('/path/to/video.mp4')

# Enable threading within single container (safe)
container.streams.video[0].thread_type = 'AUTO'
```

### Processing Multiple Files in Parallel

```python
import av
import av.logging
from concurrent.futures import ThreadPoolExecutor

# Disable logging for thread safety
av.logging.set_level(av.logging.PANIC)

def process_video(path: str) -> dict:
    """Process single video file."""
    with av.open(path) as container:
        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'

        frame_count = 0
        for frame in container.decode(stream):
            frame_count += 1

        return {'path': path, 'frames': frame_count}

# Process multiple files in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_video, video_paths))
```

---

## Performance Optimization

### Benchmarks

PyAV is generally faster than ffmpeg-python subprocess for frame-level operations:

| Operation | PyAV | ffmpeg subprocess | OpenCV |
|-----------|------|-------------------|--------|
| Decode 1080p | ~120 fps | ~100 fps | ~150 fps |
| Decode with thread_type=AUTO | ~500 fps | N/A | N/A |
| Frame to NumPy | ~200 fps | ~50 fps (pipe) | Direct |

### Optimization Tips

```python
import av
import numpy as np

# 1. Enable multi-threaded decoding
container = av.open('video.mp4')
container.streams.video[0].thread_type = 'AUTO'

# 2. Skip non-keyframes when extracting thumbnails
stream = container.streams.video[0]
stream.codec_context.skip_frame = 'NONKEY'

# 3. Use frombuffer instead of copy for large data
for frame in container.decode(video=0):
    # Efficient: shares memory when possible
    array = frame.to_ndarray(format='rgb24')
    # Make copy only if needed for storage
    if storing:
        array = array.copy()

# 4. Decode specific streams only
for frame in container.decode(video=0):  # Video only
    pass
# vs
for frame in container.decode():  # All streams (slower)
    pass

# 5. Use batch reading with Decord for ML workloads
# PyAV doesn't support batch operations - consider Decord instead
```

---

## Hardware Acceleration (Limited)

### Status

PyAV's hardware acceleration support is **limited** because:
1. FFmpeg wheels don't include CUDA/hardware codecs
2. GPU-to-CPU memory copies often negate performance gains
3. PyAV maintainers consider it low priority

### Checking Hardware Codec Availability

```python
import av

# Check if hardware codecs are available
hardware_codecs = {
    'h264_nvenc': 'NVIDIA H.264 encoder',
    'hevc_nvenc': 'NVIDIA H.265 encoder',
    'h264_cuvid': 'NVIDIA H.264 decoder',
    'h264_qsv': 'Intel QuickSync H.264',
    'h264_videotoolbox': 'Apple VideoToolbox H.264',
}

for codec, description in hardware_codecs.items():
    try:
        av.Codec(codec, 'w' if 'enc' in codec else 'r')
        print(f"{codec}: Available ({description})")
    except av.FFmpegError:
        print(f"{codec}: Not available")
```

### Alternative: Use avcuda or ffmpegcv

For GPU-accelerated video processing, consider:
- **avcuda**: PyAV extension with CUDA support
- **ffmpegcv**: OpenCV-compatible API with NVDEC/NVENC
- **Decord**: Batch GPU decoding for ML

See the `ffmpeg-opencv-integration` skill for GPU-accelerated alternatives.

---

## Common Patterns Summary

### Frame Iterator Pattern

```python
import av
from typing import Generator
import numpy as np

def frame_iterator(path: str, format: str = 'rgb24') -> Generator[np.ndarray, None, None]:
    """Memory-efficient frame iterator."""
    with av.open(path) as container:
        container.streams.video[0].thread_type = 'AUTO'
        for frame in container.decode(video=0):
            yield frame.to_ndarray(format=format)
```

### Video Info Pattern

```python
import av

def get_video_info(path: str) -> dict:
    """Get video metadata."""
    with av.open(path) as container:
        stream = container.streams.video[0]
        return {
            'width': stream.width,
            'height': stream.height,
            'fps': float(stream.average_rate),
            'duration': float(container.duration) / av.time_base if container.duration else None,
            'codec': stream.codec_context.name,
            'frames': stream.frames,
        }
```

### Transcode Pattern

```python
import av

def transcode_video(
    input_path: str,
    output_path: str,
    codec: str = 'libx264',
    crf: int = 23
):
    """Transcode video to new codec."""

    with av.open(input_path) as input_container:
        with av.open(output_path, mode='w') as output_container:
            in_stream = input_container.streams.video[0]

            out_stream = output_container.add_stream(codec, rate=in_stream.average_rate)
            out_stream.width = in_stream.width
            out_stream.height = in_stream.height
            out_stream.pix_fmt = 'yuv420p'
            out_stream.options = {'crf': str(crf)}

            for frame in input_container.decode(in_stream):
                for packet in out_stream.encode(frame):
                    output_container.mux(packet)

            for packet in out_stream.encode():
                output_container.mux(packet)
```

---

## References

- [PyAV Documentation](https://pyav.basswood-io.com/docs/stable/index.html)
- [PyAV GitHub Repository](https://github.com/PyAV-Org/PyAV)
- [PyAV-FFmpeg Releases](https://github.com/PyAV-Org/pyav-ffmpeg/releases)
- [PyPI Package](https://pypi.org/project/av/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

## Related Skills

- **ffmpeg-python-integration-reference** - Type-safe parameter mappings, color conversions
- **ffmpeg-opencv-integration** - FFmpeg + OpenCV pipelines, GPU alternatives
- **ffmpeg-fundamentals-2025** - Core FFmpeg operations
