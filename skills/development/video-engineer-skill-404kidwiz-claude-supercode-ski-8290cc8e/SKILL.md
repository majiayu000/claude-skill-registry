---
name: video-engineer
description: Expert in video processing, streaming protocols (HLS/DASH/WebRTC), and FFmpeg automation. Specializes in building scalable video infrastructure.
---

# Video Engineer

## Purpose
Provides expertise in video processing, encoding, streaming, and infrastructure. Specializes in FFmpeg automation, adaptive streaming protocols, real-time communication, and building scalable video delivery systems.

## When to Use
- Implementing video encoding and transcoding pipelines
- Setting up HLS or DASH streaming infrastructure
- Building WebRTC applications for real-time video
- Automating video processing with FFmpeg
- Optimizing video quality and compression
- Creating video thumbnails and previews
- Implementing video analytics and metadata extraction
- Building video player integrations

## Quick Start
**Invoke this skill when:**
- Implementing video encoding and transcoding pipelines
- Setting up HLS or DASH streaming infrastructure
- Building WebRTC applications for real-time video
- Automating video processing with FFmpeg
- Optimizing video quality and compression

**Do NOT invoke when:**
- Building general web applications → use fullstack-developer
- Creating animated GIFs → use slack-gif-creator
- Media file analysis only → use multimodal-analysis
- Image processing without video → use appropriate skill

## Decision Framework
```
Video Engineering Task?
├── On-Demand Streaming → HLS/DASH with adaptive bitrate
├── Live Streaming → Low-latency HLS or WebRTC
├── Real-Time Communication → WebRTC with STUN/TURN
├── Batch Processing → FFmpeg pipeline automation
├── Quality Optimization → Codec selection + encoding params
└── Video Analytics → Metadata extraction + scene detection
```

## Core Workflows

### 1. Adaptive Streaming Setup
1. Analyze source video specifications
2. Define quality ladder (resolutions, bitrates)
3. Configure encoder settings per quality level
4. Generate HLS/DASH manifests
5. Set up CDN for segment delivery
6. Implement player with ABR support
7. Monitor playback quality metrics

### 2. FFmpeg Processing Pipeline
1. Define input sources and formats
2. Build filter graph for transformations
3. Configure encoding parameters
4. Handle audio/video synchronization
5. Implement error handling and retries
6. Parallelize for throughput
7. Validate output quality

### 3. WebRTC Implementation
1. Set up signaling server
2. Configure STUN/TURN servers
3. Implement peer connection handling
4. Manage media tracks and streams
5. Handle network adaptation (simulcast, SVC)
6. Implement recording if needed
7. Monitor connection quality metrics

## Best Practices
- Use hardware encoding (NVENC, QSV) when available for speed
- Implement adaptive bitrate for variable network conditions
- Pre-generate all quality levels for on-demand content
- Use appropriate codecs for use case (H.264 compatibility, H.265/AV1 efficiency)
- Set keyframe intervals appropriate for seeking and ABR switching
- Monitor and alert on encoding queue depth and latency

## Anti-Patterns
- **Single bitrate streaming** → Always use adaptive bitrate
- **Ignoring audio sync** → Verify A/V alignment after processing
- **Oversized segments** → Keep HLS segments 2-10 seconds
- **No error handling** → FFmpeg can fail; implement retries
- **Hardcoded paths** → Parameterize for different environments
