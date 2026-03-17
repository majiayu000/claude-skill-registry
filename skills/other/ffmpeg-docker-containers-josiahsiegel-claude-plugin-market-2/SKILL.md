---
name: ffmpeg-docker-containers
description: Complete Docker FFmpeg deployment system. PROACTIVELY activate for: (1) Docker FFmpeg image selection (jrottenberg, linuxserver), (2) GPU passthrough (NVIDIA, Intel, AMD), (3) Volume mounting and permissions, (4) Docker Compose video processing, (5) Kubernetes FFmpeg jobs, (6) Custom Dockerfile builds, (7) Windows/Linux/macOS Docker usage, (8) Resource limits and optimization, (9) Watch folder automation, (10) Production container patterns. Provides: Image comparison tables, GPU Docker commands, Compose examples, K8s manifests, troubleshooting guides. Ensures: Consistent, isolated FFmpeg environments across platforms.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Image | Size | GPU | Command |
|-------|------|-----|---------|
| `jrottenberg/ffmpeg:7.1-alpine320` | ~100MB | No | `docker run --rm -v $(pwd):/data jrottenberg/ffmpeg:7.1-alpine320 -i /data/input.mp4 /data/output.mp4` |
| `jrottenberg/ffmpeg:7.1-nvidia2404` | ~1.5GB | NVIDIA | `docker run --gpus all --rm -v $(pwd):/data jrottenberg/ffmpeg:7.1-nvidia2404 ...` |
| `jrottenberg/ffmpeg:7.1-vaapi2404` | ~300MB | Intel/AMD | Add `--device /dev/dri:/dev/dri` |
| `linuxserver/ffmpeg:latest` | ~150MB | No | LinuxServer.io maintained |

## When to Use This Skill

Use for **containerized FFmpeg deployments**:
- CI/CD pipelines needing consistent FFmpeg versions
- Multi-user systems with different FFmpeg requirements
- Production transcoding services
- Kubernetes video processing jobs
- GPU passthrough configurations

---

# FFmpeg in Docker Containers (2025)

Complete guide to running FFmpeg in Docker containers with GPU support, optimization, and production patterns.

## Why Docker for FFmpeg?

### Benefits
- **Isolation**: No dependency conflicts on host system
- **Reproducibility**: Same FFmpeg version everywhere
- **Portability**: Works identically across platforms
- **Easy updates**: Switch FFmpeg versions by changing image tag
- **CI/CD integration**: Consistent builds in pipelines
- **GPU access**: NVIDIA, Intel, AMD hardware acceleration

### When to Use Docker
- Multi-user environments with different FFmpeg requirements
- CI/CD pipelines requiring specific FFmpeg builds
- Production transcoding services
- Containerized microservices architectures
- When you need specific codecs/features not in system FFmpeg

## Popular FFmpeg Docker Images

### jrottenberg/ffmpeg (Recommended)

Most popular and well-maintained FFmpeg Docker image.

**Available variants:**
| Tag | Base | Size | Use Case |
|-----|------|------|----------|
| `7.1-ubuntu2404` | Ubuntu 24.04 LTS | ~250MB | Production, full features |
| `7.1-alpine320` | Alpine 3.20 | ~100MB | Minimal, fast startup |
| `7.1-nvidia2404` | Ubuntu + CUDA | ~1.5GB | NVIDIA GPU |
| `7.1-vaapi2404` | Ubuntu + VAAPI | ~300MB | Intel/AMD GPU (Linux) |
| `7.1-scratch` | Scratch | ~80MB | Minimal, static binary |
| `8.0-ubuntu2404` | Ubuntu 24.04 LTS | ~250MB | Latest FFmpeg 8.0 |

```bash
# Pull specific version
docker pull jrottenberg/ffmpeg:7.1-ubuntu2404

# Latest (not recommended for production)
docker pull jrottenberg/ffmpeg:latest
```

### linuxserver/ffmpeg

Designed for ephemeral command-line usage.

```bash
docker pull linuxserver/ffmpeg:latest
```

### mwader/static-ffmpeg

Statically compiled FFmpeg binary.

```bash
docker pull mwader/static-ffmpeg:7.1
```

## Basic Usage

### Simple Transcode

```bash
# Mount current directory and run FFmpeg
docker run --rm \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /data/input.mp4 \
  -c:v libx264 \
  -c:a aac \
  /data/output.mp4
```

### Windows (PowerShell)

```powershell
# Windows PowerShell
docker run --rm `
  -v ${PWD}:/data `
  jrottenberg/ffmpeg:7.1-ubuntu2404 `
  -i /data/input.mp4 `
  -c:v libx264 `
  /data/output.mp4
```

### Windows (Git Bash/MINGW)

```bash
# Git Bash requires MSYS_NO_PATHCONV to prevent path conversion
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd)":/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /data/input.mp4 \
  -c:v libx264 \
  /data/output.mp4
```

### Using Absolute Paths

```bash
# Linux/macOS
docker run --rm \
  -v /home/user/videos:/input:ro \
  -v /home/user/output:/output \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /input/video.mp4 \
  /output/converted.mp4

# Windows
docker run --rm \
  -v C:\Videos:/input:ro \
  -v C:\Output:/output \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /input/video.mp4 \
  /output/converted.mp4
```

## GPU Acceleration in Docker

### NVIDIA GPU (Docker + NVIDIA Container Toolkit)

**Requirements:**
1. NVIDIA GPU with NVENC support
2. NVIDIA drivers 450+
3. NVIDIA Container Toolkit installed

**Install NVIDIA Container Toolkit:**
```bash
# Ubuntu/Debian
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

**Run with NVIDIA GPU:**
```bash
docker run --rm --gpus all \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-nvidia2404 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i /data/input.mp4 \
  -c:v h264_nvenc \
  -preset p4 \
  /data/output.mp4
```

**Select specific GPU:**
```bash
# Use GPU 0 only
docker run --rm --gpus '"device=0"' \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-nvidia2404 \
  -hwaccel cuda -i /data/input.mp4 -c:v h264_nvenc /data/output.mp4

# Use multiple GPUs
docker run --rm --gpus '"device=0,1"' \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-nvidia2404 \
  ...
```

### Intel QSV/VAAPI (Linux)

```bash
# Intel GPU with VAAPI
docker run --rm \
  --device=/dev/dri:/dev/dri \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-vaapi2404 \
  -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i /data/input.mp4 \
  -vf 'format=nv12|vaapi,hwupload' \
  -c:v h264_vaapi \
  /data/output.mp4
```

### AMD GPU (Linux VAAPI)

```bash
docker run --rm \
  --device=/dev/dri:/dev/dri \
  --device=/dev/kfd:/dev/kfd \
  --group-add video \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-vaapi2404 \
  -hwaccel vaapi \
  -hwaccel_device /dev/dri/renderD128 \
  -i /data/input.mp4 \
  -c:v h264_vaapi \
  /data/output.mp4
```

## Building Custom FFmpeg Images

### Minimal Custom Dockerfile

```dockerfile
FROM ubuntu:24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    yasm \
    nasm \
    git \
    wget \
    libx264-dev \
    libx265-dev \
    libvpx-dev \
    libfdk-aac-dev \
    libmp3lame-dev \
    libopus-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/ffmpeg
RUN wget -O ffmpeg.tar.bz2 https://ffmpeg.org/releases/ffmpeg-7.1.tar.bz2 && \
    tar xjf ffmpeg.tar.bz2 --strip-components=1

RUN ./configure \
    --enable-gpl \
    --enable-nonfree \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libvpx \
    --enable-libfdk-aac \
    --enable-libmp3lame \
    --enable-libopus \
    --disable-doc \
    --disable-debug && \
    make -j$(nproc) && \
    make install

# Production stage
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    libx264-164 \
    libx265-209 \
    libvpx9 \
    libfdk-aac2 \
    libmp3lame0 \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/

ENTRYPOINT ["ffmpeg"]
```

### Build with NVIDIA Support

```dockerfile
FROM nvidia/cuda:12.4-devel-ubuntu24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    yasm \
    nasm \
    git \
    wget \
    libx264-dev \
    libx265-dev \
    && rm -rf /var/lib/apt/lists/*

# Install nv-codec-headers
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git && \
    cd nv-codec-headers && \
    make install

# Build FFmpeg
WORKDIR /tmp/ffmpeg
RUN wget -O ffmpeg.tar.bz2 https://ffmpeg.org/releases/ffmpeg-7.1.tar.bz2 && \
    tar xjf ffmpeg.tar.bz2 --strip-components=1

RUN ./configure \
    --enable-gpl \
    --enable-nonfree \
    --enable-cuda-nvcc \
    --enable-libnpp \
    --enable-nvenc \
    --enable-nvdec \
    --enable-cuvid \
    --enable-libx264 \
    --enable-libx265 \
    --extra-cflags=-I/usr/local/cuda/include \
    --extra-ldflags=-L/usr/local/cuda/lib64 && \
    make -j$(nproc) && \
    make install

# Production stage
FROM nvidia/cuda:12.4-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y \
    libx264-164 \
    libx265-209 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/

ENTRYPOINT ["ffmpeg"]
```

## Docker Compose Patterns

### Simple Transcoding Service

```yaml
version: '3.8'

services:
  ffmpeg:
    image: jrottenberg/ffmpeg:7.1-ubuntu2404
    volumes:
      - ./input:/input:ro
      - ./output:/output
    command: >
      -i /input/video.mp4
      -c:v libx264 -crf 23
      -c:a aac -b:a 128k
      /output/converted.mp4
```

### GPU-Accelerated Service

```yaml
version: '3.8'

services:
  ffmpeg-gpu:
    image: jrottenberg/ffmpeg:7.1-nvidia2404
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./input:/input:ro
      - ./output:/output
    command: >
      -hwaccel cuda
      -hwaccel_output_format cuda
      -i /input/video.mp4
      -c:v h264_nvenc
      /output/output.mp4
```

### Watch Folder Processing

```yaml
version: '3.8'

services:
  ffmpeg-watcher:
    image: jrottenberg/ffmpeg:7.1-ubuntu2404
    volumes:
      - ./watch:/watch
      - ./done:/done
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        while true; do
          for f in /watch/*.mp4; do
            [ -e "$$f" ] || continue
            filename=$$(basename "$$f")
            ffmpeg -i "$$f" -c:v libx264 -crf 23 "/done/$$filename"
            rm "$$f"
          done
          sleep 5
        done
    restart: unless-stopped
```

## Kubernetes Deployment

### FFmpeg Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ffmpeg-transcode
spec:
  template:
    spec:
      containers:
        - name: ffmpeg
          image: jrottenberg/ffmpeg:7.1-ubuntu2404
          command:
            - ffmpeg
            - -i
            - /input/video.mp4
            - -c:v
            - libx264
            - /output/output.mp4
          volumeMounts:
            - name: input
              mountPath: /input
              readOnly: true
            - name: output
              mountPath: /output
      volumes:
        - name: input
          persistentVolumeClaim:
            claimName: input-pvc
        - name: output
          persistentVolumeClaim:
            claimName: output-pvc
      restartPolicy: Never
```

### GPU-Enabled Pod (NVIDIA)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ffmpeg-gpu
spec:
  containers:
    - name: ffmpeg
      image: jrottenberg/ffmpeg:7.1-nvidia2404
      resources:
        limits:
          nvidia.com/gpu: 1
      command:
        - ffmpeg
        - -hwaccel
        - cuda
        - -i
        - /input/video.mp4
        - -c:v
        - h264_nvenc
        - /output/output.mp4
      volumeMounts:
        - name: input
          mountPath: /input
        - name: output
          mountPath: /output
  volumes:
    - name: input
      hostPath:
        path: /data/input
    - name: output
      hostPath:
        path: /data/output
```

## Performance Optimization

### Volume Mount Best Practices

```bash
# Read-only input for security
docker run --rm \
  -v $(pwd)/input:/input:ro \
  -v $(pwd)/output:/output \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /input/video.mp4 /output/output.mp4

# Use tmpfs for temp files
docker run --rm \
  --tmpfs /tmp:size=1G \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /data/input.mp4 /data/output.mp4
```

### Resource Limits

```bash
# Limit CPU and memory
docker run --rm \
  --cpus="4" \
  --memory="4g" \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -threads 4 \
  -i /data/input.mp4 /data/output.mp4
```

### Parallel Processing

```bash
# Process multiple files in parallel
for f in *.mp4; do
  docker run --rm -d \
    --cpus="2" \
    -v $(pwd):/data \
    jrottenberg/ffmpeg:7.1-ubuntu2404 \
    -i "/data/$f" "/data/converted_$f"
done
```

## Troubleshooting

### Common Issues

**Permission denied on output:**
```bash
# Check file ownership
ls -la output/

# Run with current user
docker run --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /data/input.mp4 /data/output.mp4
```

**GPU not detected:**
```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.4-base-ubuntu24.04 nvidia-smi

# Check Docker GPU support
docker info | grep -i gpu
```

**Path conversion issues (Git Bash):**
```bash
# Set MSYS_NO_PATHCONV
MSYS_NO_PATHCONV=1 docker run ...

# Or add to ~/.bashrc
export MSYS_NO_PATHCONV=1
```

**Out of memory:**
```bash
# Increase memory limit
docker run --rm --memory="8g" --memory-swap="8g" ...

# Use streaming mode
docker run --rm \
  -v $(pwd):/data \
  jrottenberg/ffmpeg:7.1-ubuntu2404 \
  -i /data/input.mp4 \
  -f segment -segment_time 60 \
  /data/output_%03d.mp4
```

### Debug Commands

```bash
# Enter container shell
docker run --rm -it \
  --entrypoint /bin/bash \
  jrottenberg/ffmpeg:7.1-ubuntu2404

# Check FFmpeg version and capabilities
docker run --rm jrottenberg/ffmpeg:7.1-ubuntu2404 -version
docker run --rm jrottenberg/ffmpeg:7.1-ubuntu2404 -encoders
docker run --rm jrottenberg/ffmpeg:7.1-ubuntu2404 -hwaccels
```

## Best Practices

1. **Pin image versions** - Use specific tags, not `latest`
2. **Use read-only mounts** for input files
3. **Limit resources** to prevent host exhaustion
4. **Use multi-stage builds** for custom images
5. **Log to stdout/stderr** for container logging
6. **Health checks** for long-running services
7. **Clean up** containers with `--rm` flag
8. **Security** - Run as non-root when possible

This guide covers Docker FFmpeg patterns. For hardware acceleration specifics, see the hardware acceleration skill.
