---
name: Live Streaming
description: Real-time video broadcasting using RTMP, HLS, WebRTC protocols with streaming servers and cloud platforms for low-latency live video delivery.
---

# Live Streaming

> **Current Level:** Advanced  
> **Domain:** Video Streaming / Media

---

## Overview

Live streaming enables real-time video broadcasting. This guide covers RTMP, HLS, WebRTC, streaming servers, and cloud platforms for building scalable live streaming solutions with appropriate latency and quality.

---

---

## Core Concepts

### Live Streaming Protocols

| Protocol | Latency | Use Case | Browser Support |
|----------|---------|----------|-----------------|
| **RTMP** | 5-10s | Ingestion | No (Flash deprecated) |
| **HLS** | 10-30s | Playback | Yes (iOS native) |
| **WebRTC** | <1s | Low-latency | Yes |
| **DASH** | 10-30s | Playback | Yes (with player) |

## NGINX-RTMP Server Setup

```nginx
# nginx.conf
rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application live {
            live on;
            record off;

            # HLS
            hls on;
            hls_path /tmp/hls;
            hls_fragment 3;
            hls_playlist_length 60;

            # DASH
            dash on;
            dash_path /tmp/dash;

            # Allow publish from localhost only
            allow publish 127.0.0.1;
            deny publish all;

            # Allow play from anywhere
            allow play all;

            # Webhook on publish
            on_publish http://localhost:3000/api/stream/publish;
            on_publish_done http://localhost:3000/api/stream/done;
        }

        application recording {
            live on;
            record all;
            record_path /var/recordings;
            record_suffix -%Y-%m-%d-%H-%M-%S.flv;
        }
    }
}

http {
    server {
        listen 8080;

        location /hls {
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            root /tmp;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Origin *;
        }

        location /dash {
            root /tmp;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Origin *;
        }

        location /stat {
            rtmp_stat all;
            rtmp_stat_stylesheet stat.xsl;
        }
    }
}
```

## OBS Integration

```typescript
// services/stream-key.service.ts
export class StreamKeyService {
  async generateStreamKey(userId: string): Promise<StreamKey> {
    const key = crypto.randomBytes(16).toString('hex');

    const streamKey = await db.streamKey.create({
      data: {
        userId,
        key,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
      }
    });

    return streamKey;
  }

  async validateStreamKey(key: string): Promise<boolean> {
    const streamKey = await db.streamKey.findUnique({
      where: { key }
    });

    if (!streamKey) return false;

    if (streamKey.expiresAt < new Date()) {
      return false;
    }

    return true;
  }

  getStreamUrl(streamKey: string): StreamUrls {
    return {
      rtmpUrl: `rtmp://${process.env.STREAM_SERVER}/live`,
      streamKey,
      playbackUrl: `https://${process.env.CDN_DOMAIN}/hls/${streamKey}.m3u8`
    };
  }
}

interface StreamUrls {
  rtmpUrl: string;
  streamKey: string;
  playbackUrl: string;
}

// OBS Settings for users
const obsSettings = {
  server: 'rtmp://stream.example.com/live',
  streamKey: 'user-stream-key-here',
  encoder: 'x264',
  bitrate: 2500, // kbps
  keyframeInterval: 2,
  preset: 'veryfast',
  profile: 'main',
  tune: 'zerolatency'
};
```

## WebRTC for Low-Latency

```typescript
// services/webrtc-stream.service.ts
import { RTCPeerConnection, RTCSessionDescription } from 'wrtc';

export class WebRTCStreamService {
  private peerConnections = new Map<string, RTCPeerConnection>();

  async createOffer(streamId: string): Promise<RTCSessionDescriptionInit> {
    const pc = new RTCPeerConnection({
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        {
          urls: 'turn:turn.example.com:3478',
          username: process.env.TURN_USERNAME,
          credential: process.env.TURN_PASSWORD
        }
      ]
    });

    this.peerConnections.set(streamId, pc);

    // Add transceivers for video and audio
    pc.addTransceiver('video', { direction: 'recvonly' });
    pc.addTransceiver('audio', { direction: 'recvonly' });

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    return offer;
  }

  async handleAnswer(streamId: string, answer: RTCSessionDescriptionInit): Promise<void> {
    const pc = this.peerConnections.get(streamId);
    if (!pc) throw new Error('Peer connection not found');

    await pc.setRemoteDescription(new RTCSessionDescription(answer));
  }

  async addIceCandidate(streamId: string, candidate: RTCIceCandidateInit): Promise<void> {
    const pc = this.peerConnections.get(streamId);
    if (!pc) throw new Error('Peer connection not found');

    await pc.addIceCandidate(candidate);
  }

  closePeerConnection(streamId: string): void {
    const pc = this.peerConnections.get(streamId);
    if (pc) {
      pc.close();
      this.peerConnections.delete(streamId);
    }
  }
}

// Client-side WebRTC player
async function playWebRTCStream(streamId: string) {
  const pc = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
  });

  pc.ontrack = (event) => {
    const video = document.getElementById('video') as HTMLVideoElement;
    video.srcObject = event.streams[0];
  };

  // Get offer from server
  const response = await fetch(`/api/stream/${streamId}/offer`, {
    method: 'POST'
  });
  const { offer } = await response.json();

  await pc.setRemoteDescription(offer);
  const answer = await pc.createAnswer();
  await pc.setLocalDescription(answer);

  // Send answer to server
  await fetch(`/api/stream/${streamId}/answer`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer })
  });
}
```

## Chat Integration

```typescript
// services/stream-chat.service.ts
import { Server as SocketIOServer } from 'socket.io';

export class StreamChatService {
  private io: SocketIOServer;

  constructor(io: SocketIOServer) {
    this.io = io;
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', (socket) => {
      socket.on('join-stream', async (streamId: string) => {
        socket.join(`stream:${streamId}`);

        // Increment viewer count
        await this.incrementViewerCount(streamId);

        // Broadcast viewer count
        this.broadcastViewerCount(streamId);
      });

      socket.on('leave-stream', async (streamId: string) => {
        socket.leave(`stream:${streamId}`);

        await this.decrementViewerCount(streamId);
        this.broadcastViewerCount(streamId);
      });

      socket.on('chat-message', async (data: ChatMessage) => {
        // Save message
        await db.chatMessage.create({
          data: {
            streamId: data.streamId,
            userId: data.userId,
            message: data.message
          }
        });

        // Broadcast to all viewers
        this.io.to(`stream:${data.streamId}`).emit('chat-message', {
          username: data.username,
          message: data.message,
          timestamp: Date.now()
        });
      });

      socket.on('disconnect', () => {
        // Handle disconnect
      });
    });
  }

  private async incrementViewerCount(streamId: string): Promise<void> {
    await db.stream.update({
      where: { id: streamId },
      data: { viewerCount: { increment: 1 } }
    });
  }

  private async decrementViewerCount(streamId: string): Promise<void> {
    await db.stream.update({
      where: { id: streamId },
      data: { viewerCount: { decrement: 1 } }
    });
  }

  private async broadcastViewerCount(streamId: string): Promise<void> {
    const stream = await db.stream.findUnique({ where: { id: streamId } });
    
    this.io.to(`stream:${streamId}`).emit('viewer-count', {
      count: stream?.viewerCount || 0
    });
  }
}

interface ChatMessage {
  streamId: string;
  userId: string;
  username: string;
  message: string;
}
```

## Recording Live Streams

```typescript
// services/stream-recording.service.ts
import ffmpeg from 'fluent-ffmpeg';

export class StreamRecordingService {
  async startRecording(streamId: string, hlsUrl: string): Promise<void> {
    const outputPath = `/recordings/${streamId}-${Date.now()}.mp4`;

    ffmpeg(hlsUrl)
      .outputOptions([
        '-c copy',
        '-bsf:a aac_adtstoasc'
      ])
      .output(outputPath)
      .on('start', () => {
        console.log('Recording started:', streamId);
      })
      .on('end', async () => {
        console.log('Recording ended:', streamId);
        await this.uploadRecording(streamId, outputPath);
      })
      .on('error', (err) => {
        console.error('Recording error:', err);
      })
      .run();

    await db.stream.update({
      where: { id: streamId },
      data: { recording: true }
    });
  }

  private async uploadRecording(streamId: string, filePath: string): Promise<void> {
    // Upload to S3
    const s3Key = `recordings/${streamId}.mp4`;
    await uploadToS3(filePath, s3Key, 'video/mp4');

    // Save to database
    await db.recording.create({
      data: {
        streamId,
        s3Key,
        url: `${process.env.CDN_URL}/${s3Key}`
      }
    });
  }
}
```

## AWS IVS (Interactive Video Service)

```typescript
// services/aws-ivs.service.ts
import { IVSClient, CreateChannelCommand, GetStreamCommand } from '@aws-sdk/client-ivs';

export class AWSIVSService {
  private client: IVSClient;

  constructor() {
    this.client = new IVSClient({ region: process.env.AWS_REGION! });
  }

  async createChannel(name: string): Promise<IVSChannel> {
    const command = new CreateChannelCommand({
      name,
      latencyMode: 'LOW', // or 'NORMAL'
      type: 'STANDARD',
      authorized: true
    });

    const response = await this.client.send(command);

    return {
      arn: response.channel?.arn!,
      ingestEndpoint: response.channel?.ingestEndpoint!,
      playbackUrl: response.channel?.playbackUrl!,
      streamKey: response.streamKey?.value!
    };
  }

  async getStreamStatus(channelArn: string): Promise<StreamStatus> {
    const command = new GetStreamCommand({
      channelArn
    });

    const response = await this.client.send(command);

    return {
      state: response.stream?.state!,
      health: response.stream?.health!,
      viewerCount: response.stream?.viewerCount || 0
    };
  }
}

interface IVSChannel {
  arn: string;
  ingestEndpoint: string;
  playbackUrl: string;
  streamKey: string;
}

interface StreamStatus {
  state: string;
  health: string;
  viewerCount: number;
}
```

## Adaptive Streaming

```bash
# FFmpeg command for adaptive streaming
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -b:v:0 5000k -s:v:0 1920x1080 -profile:v:0 high \
  -b:v:1 3000k -s:v:1 1280x720 -profile:v:1 main \
  -b:v:2 1500k -s:v:2 854x480 -profile:v:2 main \
  -b:v:3 800k -s:v:3 640x360 -profile:v:3 baseline \
  -b:a 128k \
  -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0 v:3,a:0" \
  -master_pl_name master.m3u8 \
  -f hls -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "stream_%v/segment_%03d.ts" \
  stream_%v/playlist.m3u8
```

## Best Practices

1. **Low Latency** - Use WebRTC for <1s latency
2. **Scalability** - Use CDN for distribution
3. **Recording** - Record all streams
4. **Chat** - Integrate real-time chat
5. **Monitoring** - Monitor stream health
6. **Authentication** - Secure stream keys
7. **Adaptive** - Support adaptive bitrate
8. **Backup** - Have failover streams
9. **Analytics** - Track viewer metrics
10. **Compliance** - Follow content policies

---

## Quick Start

### Basic RTMP Stream

```bash
# Stream to RTMP server
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -maxrate 3000k \
  -bufsize 6000k -pix_fmt yuv420p -g 50 \
  -c:a aac -b:a 160k -ac 2 -ar 44100 \
  -f flv rtmp://server/live/stream_key
```

### HLS Playback

```html
<!-- HLS.js for browser playback -->
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<video id="video"></video>

<script>
  const video = document.getElementById('video')
  const hls = new Hls()
  hls.loadSource('https://server/stream.m3u8')
  hls.attachMedia(video)
</script>
```

---

## Production Checklist

- [ ] **Streaming Protocol**: Choose protocol (RTMP, HLS, WebRTC)
- [ ] **Streaming Server**: Set up streaming server (NGINX-RTMP, Wowza)
- [ ] **CDN**: Use CDN for global distribution
- [ ] **Adaptive Bitrate**: Implement adaptive bitrate streaming
- [ ] **Authentication**: Secure stream keys
- [ ] **Monitoring**: Monitor stream health and viewer metrics
- [ ] **Backup**: Failover streams for reliability
- [ ] **Analytics**: Track viewer metrics
- [ ] **Compliance**: Follow content policies
- [ ] **Testing**: Test with various devices and networks
- [ ] **Error Handling**: Handle stream failures gracefully
- [ ] **Documentation**: Document streaming setup

---

## Anti-patterns

### ❌ Don't: No Authentication

```bash
# ❌ Bad - Public stream key
rtmp://server/live/public_key  # Anyone can stream!
```

```bash
# ✅ Good - Secure stream key
rtmp://server/live/secure-random-key-12345
# Rotate keys regularly
```

### ❌ Don't: Single Bitrate

```bash
# ❌ Bad - One quality only
ffmpeg -i input.mp4 -b:v 3000k output.m3u8
```

```bash
# ✅ Good - Adaptive bitrate
ffmpeg -i input.mp4 \
  -b:v:0 3000k -b:v:1 1500k -b:v:2 800k \
  -var_stream_map "v:0 v:1 v:2" \
  output.m3u8
```

### ❌ Don't: No Monitoring

```javascript
// ❌ Bad - No stream health checks
stream.on('data', (chunk) => {
  // No monitoring!
})
```

```javascript
// ✅ Good - Monitor stream health
stream.on('data', (chunk) => {
  metrics.increment('stream.bytes')
  metrics.gauge('stream.bitrate', calculateBitrate(chunk))
})

// Alert on issues
if (bitrate < threshold) {
  alert('Low bitrate detected')
}
```

---

## Integration Points

- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - CDN setup
- **Adaptive Bitrate** (`37-video-streaming/adaptive-bitrate/`) - ABR streaming
- **Video Analytics** (`37-video-streaming/video-analytics/`) - Viewer metrics

---

## Further Reading

- [NGINX-RTMP](https://github.com/arut/nginx-rtmp-module)
- [AWS IVS](https://aws.amazon.com/ivs/)
- [HLS.js](https://github.com/video-dev/hls.js/)
- [WebRTC](https://webrtc.org/)
- [Mux](https://mux.com/)
- [WebRTC](https://webrtc.org/)
- [OBS Studio](https://obsproject.com/)
