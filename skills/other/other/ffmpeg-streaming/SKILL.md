---
name: ffmpeg-streaming
description: Complete live streaming and protocol system for FFmpeg 7.1 LTS and 8.0.1 (latest stable, released 2025-11-20). PROACTIVELY activate for: (1) RTMP streaming to Twitch/YouTube/Facebook, (2) HLS output and adaptive bitrate (ABR), (3) DASH streaming setup, (4) Low-latency streaming (LL-HLS, LL-DASH), (5) SRT protocol configuration, (6) WebRTC/WHIP sub-second latency (FFmpeg 8.0+), (7) Protocol conversion (RTMP to HLS), (8) Multi-destination streaming, (9) nginx-rtmp integration, (10) Docker streaming services. Provides: Platform-specific stream commands, ABR ladder examples, encryption setup, latency optimization, WHIP authentication, production patterns. Ensures: Reliable live streaming with optimal quality and latency.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Protocol | Latency | Output Format | Best For |
|----------|---------|---------------|----------|
| RTMP | 2-5s | `-f flv rtmp://...` | Twitch, YouTube ingest |
| HLS | 10-30s | `-f hls output.m3u8` | Web playback, CDN |
| LL-HLS | 2-5s | `-hls_flags low_latency` | Low-latency web |
| SRT | <1s | `-f mpegts srt://...` | Reliable contribution |
| DASH | 10-30s | `-f dash output.mpd` | ABR streaming |

| Platform | Ingest URL |
|----------|------------|
| Twitch | `rtmp://live.twitch.tv/app/{key}` |
| YouTube | `rtmp://a.rtmp.youtube.com/live2/{key}` |
| Facebook | `rtmps://live-api-s.facebook.com:443/rtmp/{key}` |

## When to Use This Skill

Use for **live streaming workflows**:
- Broadcasting to Twitch, YouTube, Facebook
- Setting up HLS/DASH servers for VOD
- Building ABR encoding ladders
- Low-latency streaming requirements
- Multi-destination restreaming

---

# FFmpeg Streaming Guide (2025)

Complete guide to live streaming with FFmpeg covering RTMP, HLS, DASH, SRT, and WebRTC protocols.

**Current Latest**: FFmpeg 8.0.1 (released 2025-11-20) - Check with `ffmpeg -version`

## Streaming Protocols Overview

### Protocol Comparison (2025)

| Protocol | Latency | Compatibility | Security | Use Case |
|----------|---------|---------------|----------|----------|
| RTMP | 1-5s | Legacy, ingestion | TLS (RTMPS) | Stream ingestion |
| HLS | 6-30s | Universal | AES-128 | CDN delivery |
| DASH | 6-30s | Wide | DRM-ready | ABR streaming |
| LL-HLS | 2-4s | Apple/modern | AES-128 | Low-latency |
| LL-DASH | 2-4s | Modern browsers | DRM-ready | Low-latency |
| SRT | <1s | Growing | AES-128/256 | Contribution |
| WebRTC | <0.5s | Browsers | DTLS/SRTP | Real-time |
| WHIP | <1s | Emerging | TLS | WebRTC ingestion |

### 2025 Trends
- **SRT replacing RTMP** for contribution/ingest
- **LL-HLS** becoming default for Apple ecosystem
- **WHIP** standardizing WebRTC ingestion (FFmpeg 8.0+)
- **QUIC/HTTP3** emerging for lower latency delivery

## RTMP Streaming

### Basic RTMP Stream

```bash
# Stream to RTMP server
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k -maxrate 3000k -bufsize 6000k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key
```

### Webcam/Screen to RTMP

```bash
# Linux webcam
ffmpeg -f v4l2 -i /dev/video0 \
  -f alsa -i default \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key

# macOS webcam
ffmpeg -f avfoundation -framerate 30 -i "0:0" \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key

# Windows screen capture
ffmpeg -f gdigrab -framerate 30 -i desktop \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 3000k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key
```

### RTMP with GPU Encoding

```bash
# NVIDIA NVENC
ffmpeg -re -i input.mp4 \
  -c:v h264_nvenc -preset p3 -tune ll -zerolatency 1 -b:v 6000k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key

# Intel QSV
ffmpeg -re -init_hw_device qsv=hw -filter_hw_device hw \
  -i input.mp4 \
  -c:v h264_qsv -preset fast -b:v 6000k \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream_key
```

### RTMPS (Encrypted)

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k \
  -c:a aac -b:a 128k \
  -f flv rtmps://secure-server/live/stream_key
```

### Twitch/YouTube/Facebook

```bash
# Twitch
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 6000k -maxrate 6000k -bufsize 12000k \
  -g 60 -keyint_min 60 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv rtmp://live.twitch.tv/app/YOUR_STREAM_KEY

# YouTube
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 4500k -maxrate 4500k -bufsize 9000k \
  -g 60 -keyint_min 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY

# Facebook
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 4000k -maxrate 4000k -bufsize 8000k \
  -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv rtmps://live-api-s.facebook.com:443/rtmp/YOUR_STREAM_KEY
```

## HLS Streaming

### Basic HLS Output

```bash
# Create HLS stream
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -hls_time 6 \
  -hls_list_size 0 \
  -hls_segment_filename "segment_%03d.ts" \
  playlist.m3u8
```

### Live HLS Streaming

```bash
# Live HLS with rolling window
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k \
  -c:a aac -b:a 128k \
  -hls_time 4 \
  -hls_list_size 10 \
  -hls_flags delete_segments \
  -hls_segment_filename "live_%03d.ts" \
  live.m3u8
```

### Adaptive Bitrate HLS (ABR)

```bash
# Multi-bitrate HLS
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split=3[v1][v2][v3]; \
    [v1]scale=1920:1080[v1out]; \
    [v2]scale=1280:720[v2out]; \
    [v3]scale=854:480[v3out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 5000k -maxrate:v:0 5350k -bufsize:v:0 7500k \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 2800k -maxrate:v:1 2996k -bufsize:v:1 4200k \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1400k -maxrate:v:2 1498k -bufsize:v:2 2100k \
  -map a:0 -c:a:0 aac -b:a:0 192k \
  -map a:0 -c:a:1 aac -b:a:1 128k \
  -map a:0 -c:a:2 aac -b:a:2 96k \
  -f hls \
  -hls_time 6 \
  -hls_list_size 0 \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
  -master_pl_name master.m3u8 \
  -hls_segment_filename "stream_%v/segment_%03d.ts" \
  stream_%v/playlist.m3u8
```

### HLS with AES Encryption

```bash
# Generate encryption key
openssl rand 16 > enc.key
echo "http://example.com/enc.key" > enc.keyinfo
echo "enc.key" >> enc.keyinfo
openssl rand -hex 16 >> enc.keyinfo

# Encrypted HLS
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -hls_time 6 \
  -hls_key_info_file enc.keyinfo \
  -hls_segment_filename "encrypted_%03d.ts" \
  encrypted.m3u8
```

### Low-Latency HLS (LL-HLS)

```bash
# LL-HLS with partial segments
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -tune zerolatency \
  -c:a aac \
  -hls_time 4 \
  -hls_list_size 6 \
  -hls_flags independent_segments+delete_segments \
  -hls_segment_type fmp4 \
  -hls_fmp4_init_filename init.mp4 \
  -hls_segment_filename "ll_%03d.m4s" \
  ll_playlist.m3u8
```

## DASH Streaming

### Basic DASH Output

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -f dash \
  -seg_duration 4 \
  -use_timeline 1 \
  -use_template 1 \
  output.mpd
```

### Adaptive DASH

```bash
ffmpeg -i input.mp4 \
  -map 0:v -map 0:v -map 0:v -map 0:a \
  -c:v libx264 -c:a aac \
  -b:v:0 5M -s:v:0 1920x1080 \
  -b:v:1 3M -s:v:1 1280x720 \
  -b:v:2 1M -s:v:2 640x360 \
  -b:a 128k \
  -f dash \
  -seg_duration 4 \
  -adaptation_sets "id=0,streams=v id=1,streams=a" \
  manifest.mpd
```

### Low-Latency DASH (LL-DASH)

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -c:a aac \
  -f dash \
  -seg_duration 1 \
  -frag_duration 0.1 \
  -streaming 1 \
  -ldash 1 \
  -use_timeline 0 \
  -use_template 1 \
  -remove_at_exit 1 \
  -window_size 5 \
  ll_manifest.mpd
```

## SRT Streaming (FFmpeg 4.0+)

### SRT Listener (Server Mode)

```bash
# FFmpeg as SRT server
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k \
  -c:a aac -b:a 128k \
  -f mpegts "srt://0.0.0.0:9000?mode=listener"
```

### SRT Caller (Client Mode)

```bash
# Send to SRT server
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k \
  -c:a aac -b:a 128k \
  -f mpegts "srt://server:9000?mode=caller"
```

### SRT with Encryption

```bash
# AES-128 encrypted SRT
ffmpeg -re -i input.mp4 \
  -c:v libx264 -c:a aac \
  -f mpegts "srt://server:9000?passphrase=mySecretKey123&pbkeylen=16"
```

### Receive SRT Stream

```bash
# Receive and save
ffmpeg -i "srt://0.0.0.0:9000?mode=listener" \
  -c copy output.mp4

# Receive and transcode
ffmpeg -i "srt://server:9000?mode=caller" \
  -c:v libx264 -c:a aac \
  output.mp4
```

## WebRTC/WHIP (FFmpeg 8.0+)

### Overview
FFmpeg 8.0 introduces the WHIP (WebRTC-HTTP Ingestion Protocol) muxer, enabling sub-second latency streaming to WebRTC endpoints. WHIP is becoming the standard for WebRTC ingestion, replacing proprietary solutions.

### WHIP Output

```bash
# Stream to WHIP endpoint
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -c:a libopus \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"

# Low-latency webcam to WHIP (Linux)
ffmpeg -f v4l2 -i /dev/video0 \
  -f pulse -i default \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k \
  -c:a libopus -b:a 64k \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"

# Low-latency webcam to WHIP (macOS)
ffmpeg -f avfoundation -framerate 30 -i "0:0" \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k \
  -c:a libopus -b:a 64k \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"

# Low-latency screen capture to WHIP (Windows)
ffmpeg -f gdigrab -framerate 30 -i desktop \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 3000k \
  -c:a libopus -b:a 64k \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"
```

### WHIP with Hardware Encoding

```bash
# NVIDIA NVENC WHIP streaming
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -c:v h264_nvenc -preset p3 -tune ll -zerolatency 1 -b:v 3000k \
  -c:a libopus -b:a 64k \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"

# Intel QSV WHIP streaming
ffmpeg -init_hw_device qsv=hw -filter_hw_device hw \
  -i input.mp4 \
  -c:v h264_qsv -preset fast -b:v 3000k \
  -c:a libopus -b:a 64k \
  -f whip \
  "https://whip-server.example.com/publish/stream_id"
```

### WHIP Authentication

```bash
# With bearer token authentication
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -c:a libopus \
  -f whip \
  -headers "Authorization: Bearer YOUR_TOKEN" \
  "https://whip-server.example.com/publish/stream_id"
```

### WHIP Servers/Platforms
- **Cloudflare Stream** - WebRTC ingest via WHIP
- **Dolby.io** - Interactive streaming
- **Janus** - Open-source WebRTC gateway
- **mediasoup** - Open-source SFU with WHIP support
- **LiveKit** - WebRTC platform with WHIP ingestion

## Multicast Streaming

### UDP Multicast

```bash
# Send multicast
ffmpeg -re -i input.mp4 \
  -c:v libx264 -c:a aac \
  -f mpegts "udp://239.0.0.1:1234?pkt_size=1316"

# Receive multicast
ffmpeg -i "udp://239.0.0.1:1234" -c copy output.mp4
```

## Re-streaming (Protocol Conversion)

### RTMP to HLS

```bash
# Receive RTMP, output HLS
ffmpeg -i rtmp://source/live/stream \
  -c:v libx264 -preset veryfast \
  -c:a aac \
  -hls_time 4 \
  -hls_list_size 10 \
  -hls_flags delete_segments \
  /var/www/html/hls/stream.m3u8
```

### SRT to RTMP

```bash
ffmpeg -i "srt://0.0.0.0:9000?mode=listener" \
  -c copy \
  -f flv rtmp://destination/live/stream
```

### RTMP to Multiple Destinations

```bash
ffmpeg -i rtmp://source/live/stream \
  -c copy -f flv rtmp://youtube/live/key1 \
  -c copy -f flv rtmp://twitch/app/key2 \
  -c copy -f flv rtmp://facebook/rtmp/key3
```

## Production Patterns

### nginx-rtmp Integration

```nginx
# nginx.conf
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            exec_push ffmpeg -i rtmp://localhost/live/$name
                -c:v libx264 -preset veryfast -b:v 3000k
                -c:a aac -b:a 128k
                -hls_time 4
                -hls_list_size 10
                -hls_flags delete_segments
                /var/www/html/hls/$name.m3u8;
        }
    }
}
```

### Docker Streaming Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  rtmp:
    image: tiangolo/nginx-rtmp
    ports:
      - "1935:1935"
      - "8080:8080"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

  transcoder:
    image: jrottenberg/ffmpeg:7.1-ubuntu2404
    depends_on:
      - rtmp
    command: >
      -i rtmp://rtmp:1935/live/stream
      -c:v libx264 -preset veryfast
      -c:a aac
      -hls_time 4
      -f hls /output/stream.m3u8
    volumes:
      - ./output:/output
```

### Monitoring & Logging

```bash
# Enable detailed logging
ffmpeg -report -i input.mp4 -f flv rtmp://server/live/stream

# Real-time stats
ffmpeg -re -i input.mp4 \
  -progress pipe:1 \
  -c:v libx264 -c:a aac \
  -f flv rtmp://server/live/stream

# Write stats to file
ffmpeg -re -i input.mp4 \
  -progress stats.txt \
  -c:v libx264 -c:a aac \
  -f flv rtmp://server/live/stream
```

## Troubleshooting

### Common Issues

**"Connection refused"**
```bash
# Check server is reachable
nc -zv server 1935

# Test with simple stream
ffmpeg -re -f lavfi -i testsrc=size=1280x720:rate=30 \
  -f flv rtmp://server/live/test
```

**Buffer underrun/overrun**
```bash
# Increase buffer size
ffmpeg -re -i input.mp4 \
  -b:v 3000k -maxrate 3000k -bufsize 6000k \
  -f flv rtmp://server/live/stream
```

**High latency**
```bash
# Reduce latency settings
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -g 30 -keyint_min 30 \
  -f flv rtmp://server/live/stream
```

**Packet drops**
```bash
# Increase receive buffer (SRT)
ffmpeg -i "srt://server:9000?rcvbuf=8192000" -c copy output.mp4

# Increase buffer for UDP
ffmpeg -buffer_size 8192000 -i udp://239.0.0.1:1234 -c copy output.mp4
```

## Best Practices

1. **Use appropriate keyframe interval** - 2 seconds for live streaming
2. **Match bitrate to bandwidth** - Leave 20% headroom
3. **Use CBR for streaming** - Consistent bandwidth
4. **Enable faststart for VOD** - `-movflags +faststart`
5. **Monitor stream health** - Check for drops/errors
6. **Use hardware encoding** - NVENC/QSV for GPU offload
7. **Implement ABR** - Multiple quality levels
8. **Secure your streams** - Use RTMPS/encryption
9. **Test failover** - Backup ingest points
10. **Log everything** - Use `-report` for debugging

This guide covers FFmpeg streaming fundamentals. For hardware acceleration, see the hardware acceleration skill.
