---
name: Adaptive Bitrate Streaming
description: Automatically adjusting video quality based on network conditions using HLS, DASH protocols and player implementation for smooth playback and optimal user experience.
---

# Adaptive Bitrate Streaming

> **Current Level:** Advanced  
> **Domain:** Video Streaming / Media

---

## Overview

Adaptive Bitrate (ABR) streaming automatically adjusts video quality based on network conditions. This guide covers HLS, DASH, and player implementation for building video streaming solutions that provide smooth playback across varying network conditions.

---

## ABR Concepts

```
Network Speed Detection → Quality Selection → Seamless Switching
```

**Benefits:**
- Smooth playback
- Reduced buffering
- Optimal quality
- Better user experience

## HLS (HTTP Live Streaming)

### Master Playlist

```m3u8
#EXTM3U
#EXT-X-VERSION:3

#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
1080p/playlist.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
720p/playlist.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=854x480,CODECS="avc1.64001e,mp4a.40.2"
480p/playlist.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360,CODECS="avc1.64001e,mp4a.40.2"
360p/playlist.m3u8
```

### Media Playlist

```m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0

#EXTINF:10.0,
segment_0000.ts
#EXTINF:10.0,
segment_0001.ts
#EXTINF:10.0,
segment_0002.ts
#EXTINF:10.0,
segment_0003.ts

#EXT-X-ENDLIST
```

## Creating ABR Streams with FFmpeg

```bash
# Create HLS with multiple bitrates
ffmpeg -i input.mp4 \
  -filter_complex \
  "[0:v]split=4[v1][v2][v3][v4]; \
   [v1]scale=w=1920:h=1080[v1out]; \
   [v2]scale=w=1280:h=720[v2out]; \
   [v3]scale=w=854:h=480[v3out]; \
   [v4]scale=w=640:h=360[v4out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 5M -maxrate:v:0 5M -bufsize:v:0 10M \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 3M -maxrate:v:1 3M -bufsize:v:1 6M \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1.5M -maxrate:v:2 1.5M -bufsize:v:2 3M \
  -map "[v4out]" -c:v:3 libx264 -b:v:3 800k -maxrate:v:3 800k -bufsize:v:3 1.6M \
  -map a:0 -c:a:0 aac -b:a:0 128k \
  -map a:0 -c:a:1 aac -b:a:1 128k \
  -map a:0 -c:a:2 aac -b:a:2 96k \
  -map a:0 -c:a:3 aac -b:a:3 64k \
  -f hls \
  -hls_time 6 \
  -hls_playlist_type vod \
  -hls_flags independent_segments \
  -hls_segment_type mpegts \
  -hls_segment_filename "stream_%v/data%03d.ts" \
  -master_pl_name master.m3u8 \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3" \
  stream_%v.m3u8
```

## DASH (MPEG-DASH)

### MPD Manifest

```xml
<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" type="static">
  <Period>
    <AdaptationSet mimeType="video/mp4" codecs="avc1.64001f">
      <Representation id="1080p" bandwidth="5000000" width="1920" height="1080">
        <BaseURL>1080p/</BaseURL>
        <SegmentTemplate media="segment_$Number$.m4s" initialization="init.mp4" startNumber="1" duration="6000" timescale="1000"/>
      </Representation>
      <Representation id="720p" bandwidth="3000000" width="1280" height="720">
        <BaseURL>720p/</BaseURL>
        <SegmentTemplate media="segment_$Number$.m4s" initialization="init.mp4" startNumber="1" duration="6000" timescale="1000"/>
      </Representation>
    </AdaptationSet>
    <AdaptationSet mimeType="audio/mp4" codecs="mp4a.40.2">
      <Representation id="audio" bandwidth="128000">
        <BaseURL>audio/</BaseURL>
        <SegmentTemplate media="segment_$Number$.m4s" initialization="init.mp4" startNumber="1" duration="6000" timescale="1000"/>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

### Creating DASH with FFmpeg

```bash
ffmpeg -i input.mp4 \
  -map 0:v -map 0:a \
  -c:v libx264 -c:a aac \
  -b:v:0 5M -s:v:0 1920x1080 \
  -b:v:1 3M -s:v:1 1280x720 \
  -b:v:2 1.5M -s:v:2 854x480 \
  -b:a 128k \
  -f dash \
  -seg_duration 6 \
  -use_template 1 \
  -use_timeline 1 \
  -init_seg_name 'init-$RepresentationID$.m4s' \
  -media_seg_name 'chunk-$RepresentationID$-$Number%05d$.m4s' \
  manifest.mpd
```

## Player Implementation

### Video.js

```typescript
// components/VideoPlayer.tsx
import { useEffect, useRef } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

export function VideoPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<any>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    const player = videojs(videoRef.current, {
      controls: true,
      autoplay: false,
      preload: 'auto',
      fluid: true,
      sources: [{
        src,
        type: 'application/x-mpegURL' // HLS
      }]
    });

    playerRef.current = player;

    // Quality selection
    player.on('loadedmetadata', () => {
      const qualityLevels = player.qualityLevels();
      
      qualityLevels.on('addqualitylevel', (event: any) => {
        console.log('Quality level added:', event.qualityLevel);
      });

      qualityLevels.on('change', () => {
        console.log('Quality changed to:', qualityLevels[qualityLevels.selectedIndex]);
      });
    });

    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
      }
    };
  }, [src]);

  return (
    <div data-vjs-player>
      <video ref={videoRef} className="video-js vjs-big-play-centered" />
    </div>
  );
}
```

### hls.js

```typescript
// components/HLSPlayer.tsx
import { useEffect, useRef } from 'react';
import Hls from 'hls.js';

export function HLSPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    if (Hls.isSupported()) {
      const hls = new Hls({
        enableWorker: true,
        lowLatencyMode: true,
        backBufferLength: 90
      });

      hls.loadSource(src);
      hls.attachMedia(videoRef.current);

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        console.log('Manifest loaded, levels:', hls.levels);
      });

      hls.on(Hls.Events.LEVEL_SWITCHED, (event, data) => {
        console.log('Level switched to:', data.level);
      });

      hls.on(Hls.Events.ERROR, (event, data) => {
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              console.error('Network error');
              hls.startLoad();
              break;
            case Hls.ErrorTypes.MEDIA_ERROR:
              console.error('Media error');
              hls.recoverMediaError();
              break;
            default:
              hls.destroy();
              break;
          }
        }
      });

      hlsRef.current = hls;
    } else if (videoRef.current.canPlayType('application/vnd.apple.mpegurl')) {
      // Native HLS support (Safari)
      videoRef.current.src = src;
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
      }
    };
  }, [src]);

  return (
    <video
      ref={videoRef}
      controls
      style={{ width: '100%', maxWidth: '800px' }}
    />
  );
}
```

### Shaka Player (DASH)

```typescript
// components/DASHPlayer.tsx
import { useEffect, useRef } from 'react';
import shaka from 'shaka-player';

export function DASHPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<shaka.Player | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    const player = new shaka.Player(videoRef.current);

    player.configure({
      abr: {
        enabled: true,
        defaultBandwidthEstimate: 1000000
      },
      streaming: {
        bufferingGoal: 30,
        rebufferingGoal: 2
      }
    });

    player.load(src).then(() => {
      console.log('Video loaded successfully');
    }).catch((error) => {
      console.error('Error loading video:', error);
    });

    player.addEventListener('adaptation', () => {
      const tracks = player.getVariantTracks();
      const activeTrack = tracks.find(t => t.active);
      console.log('Adapted to:', activeTrack?.height + 'p');
    });

    playerRef.current = player;

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, [src]);

  return (
    <video
      ref={videoRef}
      controls
      style={{ width: '100%', maxWidth: '800px' }}
    />
  );
}
```

## Quality Selection

```typescript
// Manual quality selection
export function QualitySelector({ player }: { player: any }) {
  const [qualities, setQualities] = useState<Quality[]>([]);
  const [currentQuality, setCurrentQuality] = useState<number>(-1);

  useEffect(() => {
    if (!player) return;

    const qualityLevels = player.qualityLevels();
    
    const levels: Quality[] = [];
    for (let i = 0; i < qualityLevels.length; i++) {
      levels.push({
        index: i,
        height: qualityLevels[i].height,
        bitrate: qualityLevels[i].bitrate,
        label: `${qualityLevels[i].height}p`
      });
    }

    setQualities(levels);

    qualityLevels.on('change', () => {
      setCurrentQuality(qualityLevels.selectedIndex);
    });
  }, [player]);

  const selectQuality = (index: number) => {
    const qualityLevels = player.qualityLevels();
    
    // Disable all levels
    for (let i = 0; i < qualityLevels.length; i++) {
      qualityLevels[i].enabled = false;
    }

    // Enable selected level
    if (index === -1) {
      // Auto mode
      for (let i = 0; i < qualityLevels.length; i++) {
        qualityLevels[i].enabled = true;
      }
    } else {
      qualityLevels[index].enabled = true;
    }
  };

  return (
    <select value={currentQuality} onChange={(e) => selectQuality(parseInt(e.target.value))}>
      <option value={-1}>Auto</option>
      {qualities.map((q) => (
        <option key={q.index} value={q.index}>
          {q.label}
        </option>
      ))}
    </select>
  );
}

interface Quality {
  index: number;
  height: number;
  bitrate: number;
  label: string;
}
```

## DRM Integration

```typescript
// DRM configuration for Shaka Player
const drmConfig = {
  drm: {
    servers: {
      'com.widevine.alpha': 'https://widevine-proxy.example.com/proxy',
      'com.microsoft.playready': 'https://playready.example.com/rightsmanager.asmx'
    }
  }
};

player.configure(drmConfig);

// FairPlay for Safari
if (shaka.Player.isBrowserSupported() && 
    navigator.requestMediaKeySystemAccess) {
  // Configure FairPlay
}
```

---

## Quick Start

### HLS Manifest Generation

```bash
# Generate HLS with multiple bitrates
ffmpeg -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v:0 3000k -s:v:0 1920x1080 \
  -c:v libx264 -preset veryfast -b:v:1 1500k -s:v:1 1280x720 \
  -c:v libx264 -preset veryfast -b:v:2 800k -s:v:2 854x480 \
  -c:a aac -b:a 128k \
  -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0" \
  -master_pl_name master.m3u8 \
  -f hls -hls_time 6 -hls_list_size 0 \
  stream_%v/playlist.m3u8
```

### HLS.js Player

```javascript
import Hls from 'hls.js'

const video = document.getElementById('video')
const hls = new Hls()

hls.loadSource('https://server/master.m3u8')
hls.attachMedia(video)

// Monitor quality changes
hls.on(Hls.Events.LEVEL_SWITCHED, (event, data) => {
  console.log('Switched to quality:', data.level)
})
```

---

## Production Checklist

- [ ] **Multiple Qualities**: Provide 3-5 quality levels
- [ ] **Segment Duration**: Use 6-10 second segments
- [ ] **Buffer Management**: Configure appropriate buffers
- [ ] **Error Handling**: Handle network errors gracefully
- [ ] **CDN**: Use CDN for global distribution
- [ ] **Monitoring**: Monitor playback quality and buffering
- [ ] **Testing**: Test on various network conditions
- [ ] **Fallback**: Fallback to lower quality on errors
- [ ] **Analytics**: Track quality switches and buffering
- [ ] **Documentation**: Document quality levels
- [ ] **Optimization**: Optimize encoding settings
- [ ] **Compatibility**: Test across browsers and devices

---

## Anti-patterns

### ❌ Don't: Single Quality

```bash
# ❌ Bad - One quality only
ffmpeg -i input.mp4 -b:v 3000k output.m3u8
```

```bash
# ✅ Good - Multiple qualities
ffmpeg -i input.mp4 \
  -b:v:0 3000k -b:v:1 1500k -b:v:2 800k \
  -var_stream_map "v:0 v:1 v:2" \
  master.m3u8
```

### ❌ Don't: Long Segments

```bash
# ❌ Bad - Long segments
-hls_time 30  # 30 seconds - slow adaptation
```

```bash
# ✅ Good - Shorter segments
-hls_time 6  # 6 seconds - faster adaptation
```

---

## Integration Points

- **Live Streaming** (`37-video-streaming/live-streaming/`) - Live ABR
- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - CDN setup
- **Video Analytics** (`37-video-streaming/video-analytics/`) - Quality metrics

---

## Further Reading

- [HLS Specification](https://developer.apple.com/streaming/)
- [DASH Specification](https://dashif.org/)
- [HLS.js Documentation](https://github.com/video-dev/hls.js/)
5. **Quality Selection** - Allow manual quality override
6. **Analytics** - Track quality switches
7. **CDN** - Use CDN for delivery
8. **Testing** - Test on various network conditions
9. **Fallback** - Provide progressive download fallback
10. **DRM** - Implement DRM when needed

## Resources

- [HLS Specification](https://datatracker.ietf.org/doc/html/rfc8216)
- [DASH Specification](https://dashif.org/)
- [Video.js](https://videojs.com/)
- [hls.js](https://github.com/video-dev/hls.js/)
- [Shaka Player](https://github.com/shaka-project/shaka-player)
