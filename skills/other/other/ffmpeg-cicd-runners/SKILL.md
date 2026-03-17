---
name: ffmpeg-cicd-runners
description: Complete CI/CD video processing system. PROACTIVELY activate for: (1) GitHub Actions FFmpeg setup, (2) GitLab CI video pipelines, (3) Jenkins declarative pipelines, (4) FFmpeg caching strategies, (5) Windows runner workarounds, (6) GPU-enabled self-hosted runners, (7) Matrix builds for multi-format, (8) Artifact upload/download, (9) Video validation workflows, (10) BtbN/FFmpeg-Builds integration. Provides: YAML workflow examples, Docker container patterns, caching configuration, platform-specific solutions, debugging guides. Ensures: Fast, reliable video processing in CI/CD pipelines.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Platform | Install Method | Example |
|----------|---------------|---------|
| GitHub Actions | `apt-get` or action | `uses: FedericoCarboni/setup-ffmpeg@v3` |
| GitLab CI | Docker image | `image: jrottenberg/ffmpeg:7.1-ubuntu2404` |
| Jenkins | Docker container | `docker { image 'jrottenberg/ffmpeg:7.1' }` |

| Task | YAML Snippet |
|------|--------------|
| Cache FFmpeg | `uses: actions/cache@v4` with `path: /usr/local/bin/ffmpeg` |
| Upload artifact | `uses: actions/upload-artifact@v4` |
| Matrix build | `strategy: { matrix: { format: [mp4, webm, mkv] } }` |

## When to Use This Skill

Use for **CI/CD video processing pipelines**:
- GitHub Actions FFmpeg workflows
- GitLab CI/CD video transcoding
- Jenkins video processing jobs
- Caching FFmpeg for faster builds
- Windows runner workarounds

---

# FFmpeg in CI/CD Pipelines (2025)

Comprehensive guide to using FFmpeg in GitHub Actions, GitLab CI, Jenkins, and other CI/CD systems.

## Overview

### Common CI/CD Use Cases
- **Video validation**: Check uploaded videos meet requirements
- **Transcoding**: Convert videos to multiple formats/resolutions
- **Thumbnail generation**: Create preview images
- **Audio extraction**: Process audio tracks
- **Quality checks**: Validate encoding parameters
- **Testing**: Test video processing pipelines

### Key Considerations
- **Build time**: FFmpeg compilation takes 20-40+ minutes
- **Runner resources**: CPU/memory limits affect processing
- **Caching**: Cache FFmpeg builds for faster runs
- **Platform differences**: Windows runners have unique issues
- **Dependencies**: Codec libraries may need installation

## GitHub Actions

### Install FFmpeg (Quick)

```yaml
name: Video Processing

on: [push, pull_request]

jobs:
  process:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install FFmpeg
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg

      - name: Check FFmpeg version
        run: ffmpeg -version

      - name: Process video
        run: |
          ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Install Specific FFmpeg Version

```yaml
jobs:
  process:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install FFmpeg 7.1
        run: |
          wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz
          tar xf ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz
          sudo cp ffmpeg-n7.1-latest-linux64-gpl-7.1/bin/* /usr/local/bin/
          ffmpeg -version
```

### Use FedericoCarboni/setup-ffmpeg Action

```yaml
jobs:
  process:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup FFmpeg
        uses: FedericoCarboni/setup-ffmpeg@v3
        with:
          ffmpeg-version: release
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Process video
        run: ffmpeg -i input.mp4 output.webm
```

### Docker-Based FFmpeg

```yaml
jobs:
  process:
    runs-on: ubuntu-latest
    container:
      image: jrottenberg/ffmpeg:7.1-ubuntu2404

    steps:
      - uses: actions/checkout@v4

      - name: Process video
        run: |
          ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Caching FFmpeg Build

```yaml
jobs:
  build-ffmpeg:
    runs-on: ubuntu-latest

    steps:
      - name: Cache FFmpeg
        id: cache-ffmpeg
        uses: actions/cache@v4
        with:
          path: /usr/local/bin/ffmpeg
          key: ffmpeg-7.1-linux-${{ runner.arch }}

      - name: Build FFmpeg (if not cached)
        if: steps.cache-ffmpeg.outputs.cache-hit != 'true'
        run: |
          wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz
          tar xf ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz
          sudo cp ffmpeg-n7.1-latest-linux64-gpl-7.1/bin/ffmpeg /usr/local/bin/
```

### Matrix Build (Multiple Platforms)

```yaml
jobs:
  process:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup FFmpeg
        uses: FedericoCarboni/setup-ffmpeg@v3

      - name: Process video
        run: ffmpeg -i input.mp4 -c:v libx264 output_${{ matrix.os }}.mp4
        shell: bash
```

### Windows Runner (Known Issues)

**Issue**: Windows runners take significantly longer (up to 4 hours for vcpkg FFmpeg builds)

**Solutions**:

```yaml
jobs:
  windows-ffmpeg:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v4

      # Option 1: Use pre-built binaries (recommended)
      - name: Download FFmpeg
        run: |
          Invoke-WebRequest -Uri "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-win64-gpl-7.1.zip" -OutFile ffmpeg.zip
          Expand-Archive ffmpeg.zip -DestinationPath .
          $env:PATH = "$PWD\ffmpeg-n7.1-latest-win64-gpl-7.1\bin;$env:PATH"
          ffmpeg -version

      # Option 2: Use setup-ffmpeg action
      - name: Setup FFmpeg
        uses: FedericoCarboni/setup-ffmpeg@v3

      - name: Process video
        run: ffmpeg -i input.mp4 output.mp4
```

### GPU-Enabled Runners

```yaml
jobs:
  gpu-process:
    runs-on: [self-hosted, gpu, linux]

    steps:
      - uses: actions/checkout@v4

      - name: Process with NVIDIA GPU
        run: |
          ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
            -i input.mp4 \
            -c:v h264_nvenc \
            -preset p4 \
            output.mp4
```

### Artifact Upload

```yaml
jobs:
  process:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install FFmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg

      - name: Generate outputs
        run: |
          mkdir -p outputs
          ffmpeg -i input.mp4 -vf scale=1920:1080 outputs/1080p.mp4
          ffmpeg -i input.mp4 -vf scale=1280:720 outputs/720p.mp4
          ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 outputs/thumbnail.jpg

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: video-outputs
          path: outputs/
          retention-days: 7
```

### Video Validation Workflow

```yaml
name: Validate Videos

on:
  pull_request:
    paths:
      - '**.mp4'
      - '**.webm'
      - '**.mov'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install FFmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg

      - name: Validate videos
        run: |
          for video in $(find . -name "*.mp4" -o -name "*.webm" -o -name "*.mov"); do
            echo "Validating: $video"

            # Check if valid
            if ! ffprobe -v error "$video"; then
              echo "Invalid video: $video"
              exit 1
            fi

            # Get info
            duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video")
            resolution=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$video")

            echo "Duration: ${duration}s"
            echo "Resolution: $resolution"

            # Validate constraints
            if (( $(echo "$duration > 300" | bc -l) )); then
              echo "Video too long: $video ($duration seconds)"
              exit 1
            fi
          done
```

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml

stages:
  - process

video-process:
  stage: process
  image: jrottenberg/ffmpeg:7.1-ubuntu2404
  script:
    - ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
  artifacts:
    paths:
      - output.mp4
    expire_in: 1 week
```

### Multi-Format Transcoding

```yaml
transcode:
  stage: process
  image: jrottenberg/ffmpeg:7.1-ubuntu2404
  script:
    - mkdir -p outputs
    - ffmpeg -i input.mp4 -c:v libx264 -crf 23 outputs/h264.mp4
    - ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 outputs/vp9.webm
    - ffmpeg -i input.mp4 -vf scale=1280:720 outputs/720p.mp4
  artifacts:
    paths:
      - outputs/
```

### Parallel Processing

```yaml
.process-template: &process-template
  stage: process
  image: jrottenberg/ffmpeg:7.1-ubuntu2404

process-1080p:
  <<: *process-template
  script:
    - ffmpeg -i input.mp4 -vf scale=1920:1080 output_1080p.mp4
  artifacts:
    paths:
      - output_1080p.mp4

process-720p:
  <<: *process-template
  script:
    - ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4
  artifacts:
    paths:
      - output_720p.mp4

process-480p:
  <<: *process-template
  script:
    - ffmpeg -i input.mp4 -vf scale=854:480 output_480p.mp4
  artifacts:
    paths:
      - output_480p.mp4
```

### GPU Runner (GitLab)

```yaml
gpu-transcode:
  stage: process
  tags:
    - gpu
    - linux
  image: jrottenberg/ffmpeg:7.1-nvidia2404
  script:
    - ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

## Jenkins

### Declarative Pipeline

```groovy
pipeline {
    agent {
        docker {
            image 'jrottenberg/ffmpeg:7.1-ubuntu2404'
            args '-v /data/videos:/videos'
        }
    }

    stages {
        stage('Process') {
            steps {
                sh '''
                    ffmpeg -i /videos/input.mp4 \
                           -c:v libx264 -crf 23 \
                           -c:a aac -b:a 128k \
                           /videos/output.mp4
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '/videos/output.mp4'
        }
    }
}
```

### Parallel Transcoding

```groovy
pipeline {
    agent any

    stages {
        stage('Transcode') {
            parallel {
                stage('1080p') {
                    agent {
                        docker { image 'jrottenberg/ffmpeg:7.1-ubuntu2404' }
                    }
                    steps {
                        sh 'ffmpeg -i input.mp4 -vf scale=1920:1080 output_1080p.mp4'
                    }
                }
                stage('720p') {
                    agent {
                        docker { image 'jrottenberg/ffmpeg:7.1-ubuntu2404' }
                    }
                    steps {
                        sh 'ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4'
                    }
                }
            }
        }
    }
}
```

## BtbN/FFmpeg-Builds

### Overview

BtbN/FFmpeg-Builds is the most popular automated FFmpeg build system, providing pre-built static binaries for multiple platforms.

### Build Matrix

| Target | Variants | Features |
|--------|----------|----------|
| win64 | gpl, lgpl, gpl-shared, lgpl-shared | Full Windows 64-bit |
| winarm64 | gpl, lgpl | Windows ARM64 |
| linux64 | gpl, lgpl, gpl-shared, lgpl-shared | Full Linux 64-bit |
| linuxarm64 | gpl, lgpl | Linux ARM64 |

### Download in CI

```yaml
- name: Download FFmpeg
  run: |
    # Latest release
    wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz

    # Specific version
    wget https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2025-01-15-12-50/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz
```

## Performance Optimization

### Parallel Processing

```yaml
# Process multiple files in parallel
jobs:
  process:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        video: [video1.mp4, video2.mp4, video3.mp4]
      max-parallel: 3

    steps:
      - name: Process ${{ matrix.video }}
        run: ffmpeg -i ${{ matrix.video }} -c:v libx264 output_${{ matrix.video }}
```

### Resource-Optimized Encoding

```yaml
- name: Optimized encoding
  run: |
    # Use appropriate threads for runner
    THREADS=$(nproc)

    ffmpeg -i input.mp4 \
      -threads $THREADS \
      -c:v libx264 \
      -preset fast \
      -crf 23 \
      output.mp4
```

### Caching Dependencies

```yaml
- name: Cache FFmpeg and libraries
  uses: actions/cache@v4
  with:
    path: |
      ~/.local/bin/ffmpeg
      ~/.local/lib/
    key: ffmpeg-${{ runner.os }}-${{ hashFiles('ffmpeg-version.txt') }}
```

## Troubleshooting

### Common Issues

**"ffmpeg: command not found"**
```yaml
# Ensure FFmpeg is in PATH
- name: Add FFmpeg to PATH
  run: echo "/path/to/ffmpeg/bin" >> $GITHUB_PATH
```

**"Cannot allocate memory"**
```yaml
# Reduce memory usage
- name: Process with low memory
  run: |
    ffmpeg -i input.mp4 \
      -threads 2 \
      -preset ultrafast \
      -vf scale=1280:720 \
      output.mp4
```

**Windows path issues**
```yaml
# Use forward slashes on Windows
- name: Process on Windows
  run: ffmpeg -i "./input.mp4" "./output.mp4"
  shell: bash
```

### Debugging

```yaml
- name: Debug FFmpeg
  run: |
    # Check FFmpeg capabilities
    ffmpeg -version
    ffmpeg -encoders
    ffmpeg -decoders
    ffmpeg -formats

    # Verbose processing
    ffmpeg -v verbose -i input.mp4 -c:v libx264 output.mp4 2>&1 | tee ffmpeg.log

- name: Upload logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: ffmpeg-logs
    path: ffmpeg.log
```

## Best Practices

1. **Use pre-built binaries** - Avoid compiling FFmpeg in CI (slow)
2. **Cache FFmpeg installation** - Reduce setup time
3. **Use Docker containers** - Consistent FFmpeg environment
4. **Optimize for runner resources** - Match threads/preset to available CPU
5. **Validate inputs** - Check video files before processing
6. **Upload artifacts** - Store outputs for review
7. **Use matrix builds** - Parallelize multi-format transcoding
8. **Monitor build times** - Windows runners are slower
9. **Pin versions** - Avoid `latest` for reproducibility
10. **Use `-preset fast/ultrafast`** - Faster encoding for CI

This guide covers CI/CD FFmpeg patterns. For hardware acceleration in CI, consider self-hosted GPU runners.
