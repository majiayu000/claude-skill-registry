---
name: ffmpeg-webassembly-workers
description: Complete browser-based FFmpeg system. PROACTIVELY activate for: (1) ffmpeg.wasm setup and loading, (2) Browser video transcoding, (3) React/Vue/Next.js integration, (4) SharedArrayBuffer and COOP/COEP headers, (5) Multi-threaded ffmpeg-core-mt, (6) Cloudflare Workers limitations, (7) Custom ffmpeg.wasm builds, (8) Memory management and cleanup, (9) Progress tracking and UI, (10) IndexedDB core caching. Provides: Framework-specific examples, header configuration, common operation recipes, performance optimization, troubleshooting guides. Ensures: Client-side video processing without server dependencies.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Package | Size | Threading | Install |
|---------|------|-----------|---------|
| `@ffmpeg/core` | ~31MB | Single | `npm install @ffmpeg/ffmpeg @ffmpeg/util` |
| `@ffmpeg/core-mt` | ~31MB | Multi | Requires COOP/COEP headers |

| Header | Value | Purpose |
|--------|-------|---------|
| Cross-Origin-Embedder-Policy | `require-corp` | SharedArrayBuffer |
| Cross-Origin-Opener-Policy | `same-origin` | Multi-threading |

| Operation | Command |
|-----------|---------|
| Convert WebM→MP4 | `await ffmpeg.exec(['-i', 'input.webm', 'output.mp4'])` |
| Extract frame | `await ffmpeg.exec(['-i', 'video.mp4', '-ss', '5', '-vframes', '1', 'thumb.jpg'])` |

## When to Use This Skill

Use for **browser-based video processing**:
- Client-side transcoding without server
- React/Vue/Next.js FFmpeg integration
- Setting up COOP/COEP headers
- Cloudflare Workers FFmpeg limitations
- Memory management and cleanup

---

# FFmpeg WebAssembly & Cloudflare Workers (2025)

Guide to running FFmpeg in browsers and edge environments using WebAssembly.

## ffmpeg.wasm Overview

**ffmpeg.wasm** is a pure WebAssembly/JavaScript port of FFmpeg that runs directly in browsers without server-side processing.

### Key Features
- **Browser-based**: No server required for video processing
- **Cross-platform**: Works on any modern browser
- **Single-thread**: @ffmpeg/core (~31MB)
- **Multi-thread**: @ffmpeg/core-mt (requires SharedArrayBuffer)
- **Customizable**: Build your own core with specific codecs

### Limitations
- **Performance**: ~10-100x slower than native FFmpeg
- **Memory**: Limited by browser memory constraints
- **File size**: Core is ~31MB (can be reduced with custom builds)
- **Threading**: Multi-thread requires specific headers (COOP/COEP)
- **Codecs**: Not all codecs available (licensing restrictions)

## Installation

### npm
```bash
npm install @ffmpeg/ffmpeg @ffmpeg/util
```

### CDN
```html
<script src="https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.10/dist/umd/ffmpeg.min.js"></script>
```

## Basic Usage

### Single-Thread (Browser)

```javascript
import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile, toBlobURL } from '@ffmpeg/util';

const ffmpeg = new FFmpeg();

// Load FFmpeg core
const baseURL = 'https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.10/dist/umd';
await ffmpeg.load({
  coreURL: await toBlobURL(`${baseURL}/ffmpeg-core.js`, 'text/javascript'),
  wasmURL: await toBlobURL(`${baseURL}/ffmpeg-core.wasm`, 'application/wasm'),
});

// Transcode video
await ffmpeg.writeFile('input.webm', await fetchFile(videoFile));
await ffmpeg.exec(['-i', 'input.webm', 'output.mp4']);
const data = await ffmpeg.readFile('output.mp4');

// Create blob URL for playback
const videoURL = URL.createObjectURL(
  new Blob([data.buffer], { type: 'video/mp4' })
);
```

### Multi-Thread (Requires COOP/COEP Headers)

```javascript
import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile, toBlobURL } from '@ffmpeg/util';

const ffmpeg = new FFmpeg();

// Load multi-threaded core
const baseURL = 'https://cdn.jsdelivr.net/npm/@ffmpeg/core-mt@0.12.10/dist/umd';
await ffmpeg.load({
  coreURL: await toBlobURL(`${baseURL}/ffmpeg-core.js`, 'text/javascript'),
  wasmURL: await toBlobURL(`${baseURL}/ffmpeg-core.wasm`, 'application/wasm'),
  workerURL: await toBlobURL(`${baseURL}/ffmpeg-core.worker.js`, 'text/javascript'),
});

// Use multi-threaded encoding
await ffmpeg.exec(['-i', 'input.webm', '-threads', '4', 'output.mp4']);
```

## Cross-Origin Isolation (SharedArrayBuffer)

Multi-threaded ffmpeg.wasm requires SharedArrayBuffer, which needs Cross-Origin Isolation headers.

### Vite Configuration

```javascript
// vite.config.js
export default {
  server: {
    headers: {
      "Cross-Origin-Embedder-Policy": "require-corp",
      "Cross-Origin-Opener-Policy": "same-origin",
    },
  },
  optimizeDeps: {
    exclude: ["@ffmpeg/ffmpeg", "@ffmpeg/util"],
  },
};
```

### Next.js Configuration

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Cross-Origin-Embedder-Policy", value: "require-corp" },
          { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
        ],
      },
    ];
  },
};
```

### Express.js Middleware

```javascript
import express from 'express';

const app = express();

app.use((req, res, next) => {
  res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
  res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
  res.setHeader("Cross-Origin-Resource-Policy", "cross-origin");
  next();
});

app.use(express.static('public'));
app.listen(3000);
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl;

    add_header Cross-Origin-Embedder-Policy "require-corp" always;
    add_header Cross-Origin-Opener-Policy "same-origin" always;

    location / {
        root /var/www/html;
    }
}
```

## React Integration

### React Component

```jsx
import { useState, useRef } from 'react';
import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile, toBlobURL } from '@ffmpeg/util';

function VideoTranscoder() {
  const [loaded, setLoaded] = useState(false);
  const [progress, setProgress] = useState(0);
  const [outputURL, setOutputURL] = useState(null);
  const ffmpegRef = useRef(new FFmpeg());

  const load = async () => {
    const ffmpeg = ffmpegRef.current;

    // Progress handler
    ffmpeg.on('progress', ({ progress }) => {
      setProgress(Math.round(progress * 100));
    });

    const baseURL = 'https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.10/dist/umd';
    await ffmpeg.load({
      coreURL: await toBlobURL(`${baseURL}/ffmpeg-core.js`, 'text/javascript'),
      wasmURL: await toBlobURL(`${baseURL}/ffmpeg-core.wasm`, 'application/wasm'),
    });

    setLoaded(true);
  };

  const transcode = async (file) => {
    const ffmpeg = ffmpegRef.current;

    await ffmpeg.writeFile('input.webm', await fetchFile(file));
    await ffmpeg.exec([
      '-i', 'input.webm',
      '-c:v', 'libx264',
      '-preset', 'ultrafast',
      '-c:a', 'aac',
      'output.mp4'
    ]);

    const data = await ffmpeg.readFile('output.mp4');
    const url = URL.createObjectURL(
      new Blob([data.buffer], { type: 'video/mp4' })
    );
    setOutputURL(url);
  };

  return (
    <div>
      {!loaded ? (
        <button onClick={load}>Load FFmpeg (~31MB)</button>
      ) : (
        <>
          <input
            type="file"
            accept="video/*"
            onChange={(e) => transcode(e.target.files[0])}
          />
          <p>Progress: {progress}%</p>
          {outputURL && <video src={outputURL} controls />}
        </>
      )}
    </div>
  );
}
```

## Common Operations

### Convert WebM to MP4
```javascript
await ffmpeg.exec(['-i', 'input.webm', '-c:v', 'libx264', 'output.mp4']);
```

### Extract Audio
```javascript
await ffmpeg.exec(['-i', 'video.mp4', '-vn', '-c:a', 'libmp3lame', 'audio.mp3']);
```

### Create Thumbnail
```javascript
await ffmpeg.exec(['-i', 'video.mp4', '-ss', '00:00:05', '-vframes', '1', 'thumb.jpg']);
```

### Trim Video
```javascript
await ffmpeg.exec([
  '-i', 'input.mp4',
  '-ss', '00:00:10',
  '-t', '00:00:30',
  '-c', 'copy',
  'output.mp4'
]);
```

### Add Watermark
```javascript
await ffmpeg.writeFile('logo.png', await fetchFile(logoFile));
await ffmpeg.exec([
  '-i', 'input.mp4',
  '-i', 'logo.png',
  '-filter_complex', 'overlay=10:10',
  'output.mp4'
]);
```

### Scale Video
```javascript
await ffmpeg.exec([
  '-i', 'input.mp4',
  '-vf', 'scale=1280:720',
  '-c:a', 'copy',
  'output.mp4'
]);
```

## Cloudflare Workers

### Current Limitations (December 2025)

Running ffmpeg.wasm on Cloudflare Workers faces significant challenges:

1. **Size limit**: Workers have a 10MB compressed limit (paid plan)
2. **No Web Workers**: Cannot spawn workers from within a CF Worker
3. **SharedArrayBuffer**: Not available in Workers environment
4. **Environment detection**: ffmpeg.wasm environment checks may fail

### Workarounds

#### 1. Use External FFmpeg Service
```javascript
// Cloudflare Worker calling external FFmpeg API
export default {
  async fetch(request) {
    const formData = await request.formData();
    const video = formData.get('video');

    // Send to external FFmpeg service
    const response = await fetch('https://your-ffmpeg-api.com/transcode', {
      method: 'POST',
      body: video,
    });

    return response;
  },
};
```

#### 2. Use Durable Objects with R2 Storage
```javascript
// Store video in R2, process with external service
export default {
  async fetch(request, env) {
    const video = await request.arrayBuffer();

    // Store in R2
    await env.BUCKET.put('input.mp4', video);

    // Trigger external processing
    await env.QUEUE.send({
      bucket: 'BUCKET',
      key: 'input.mp4',
    });

    return new Response('Processing started');
  },
};
```

#### 3. Custom ffmpeg.wasm Build (Experimental)

For simple operations, a minimal custom build may fit within limits:

```bash
# Build minimal ffmpeg.wasm (~8MB compressed)
# Only include essential codecs
git clone https://github.com/ffmpegwasm/ffmpeg.wasm
cd ffmpeg.wasm
# Modify build scripts to include only needed codecs
npm run build:core -- --disable-all --enable-libx264
```

### Alternative: Cloudflare Stream

For video processing in Cloudflare ecosystem, consider Cloudflare Stream:

```javascript
// Upload to Cloudflare Stream for processing
export default {
  async fetch(request, env) {
    const formData = new FormData();
    formData.append('file', await request.arrayBuffer());

    const response = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.API_TOKEN}`,
        },
        body: formData,
      }
    );

    return response;
  },
};
```

## Building Custom ffmpeg.wasm Core

### Reduce Core Size

```dockerfile
# Custom Dockerfile for minimal build
FROM emscripten/emsdk:3.1.50

WORKDIR /src

# Clone FFmpeg
RUN git clone https://github.com/FFmpeg/FFmpeg.git ffmpeg

WORKDIR /src/ffmpeg

# Configure with minimal codecs
RUN emconfigure ./configure \
  --target-os=none \
  --arch=x86_32 \
  --enable-cross-compile \
  --disable-x86asm \
  --disable-inline-asm \
  --disable-stripping \
  --disable-programs \
  --disable-doc \
  --disable-debug \
  --disable-runtime-cpudetect \
  --disable-autodetect \
  --enable-small \
  --enable-gpl \
  --enable-libx264 \
  --extra-cflags="-O3 -s USE_PTHREADS=1" \
  --extra-ldflags="-O3 -s USE_PTHREADS=1"

RUN emmake make -j$(nproc)
```

### Build Script

```bash
#!/bin/bash
# build-minimal.sh

# Configure build
./configure \
  --disable-all \
  --enable-avcodec \
  --enable-avformat \
  --enable-avutil \
  --enable-swresample \
  --enable-swscale \
  --enable-decoder=h264 \
  --enable-decoder=aac \
  --enable-encoder=libx264 \
  --enable-encoder=aac \
  --enable-muxer=mp4 \
  --enable-demuxer=mov \
  --enable-protocol=file \
  --enable-gpl \
  --enable-libx264

make -j$(nproc)
```

## Performance Optimization

### Browser Best Practices

1. **Load core lazily** - Don't load until needed
2. **Use Web Workers** - Keep main thread responsive
3. **Stream processing** - Process chunks for large files
4. **Cache core** - Store in IndexedDB or Cache API
5. **Show progress** - Use progress events for UX

### Caching ffmpeg-core

```javascript
// Cache ffmpeg core in IndexedDB
async function loadCachedFFmpeg() {
  const cacheKey = 'ffmpeg-core-0.12.10';

  // Check cache
  const cached = await getCachedCore(cacheKey);
  if (cached) {
    await ffmpeg.load({
      coreURL: URL.createObjectURL(cached.core),
      wasmURL: URL.createObjectURL(cached.wasm),
    });
    return;
  }

  // Download and cache
  const baseURL = 'https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.10/dist/umd';
  const [core, wasm] = await Promise.all([
    fetch(`${baseURL}/ffmpeg-core.js`).then(r => r.blob()),
    fetch(`${baseURL}/ffmpeg-core.wasm`).then(r => r.blob()),
  ]);

  await cacheCore(cacheKey, { core, wasm });

  await ffmpeg.load({
    coreURL: URL.createObjectURL(core),
    wasmURL: URL.createObjectURL(wasm),
  });
}
```

### Memory Management

```javascript
// Clean up after processing
async function processAndCleanup(inputFile) {
  const ffmpeg = new FFmpeg();
  await ffmpeg.load({ ... });

  try {
    await ffmpeg.writeFile('input.mp4', await fetchFile(inputFile));
    await ffmpeg.exec(['-i', 'input.mp4', 'output.mp4']);
    const data = await ffmpeg.readFile('output.mp4');

    // Clean up virtual filesystem
    await ffmpeg.deleteFile('input.mp4');
    await ffmpeg.deleteFile('output.mp4');

    return data;
  } finally {
    // Terminate FFmpeg to free memory
    ffmpeg.terminate();
  }
}
```

## Troubleshooting

### "SharedArrayBuffer is not defined"

**Cause**: Missing Cross-Origin Isolation headers

**Solution**: Add COOP/COEP headers to server configuration

### "Worker is not defined" (Cloudflare Workers)

**Cause**: ffmpeg.wasm tries to spawn Web Workers, unavailable in CF Workers

**Solution**: Use single-thread core or external FFmpeg service

### Out of memory

**Cause**: Large video files exhaust browser memory

**Solutions**:
1. Process in chunks
2. Use lower resolution/quality
3. Use multi-thread core (more efficient)
4. Implement streaming processing

### Slow encoding

**Cause**: WebAssembly is slower than native

**Solutions**:
1. Use `-preset ultrafast`
2. Reduce resolution before encoding
3. Use hardware acceleration if available (experimental)
4. Consider server-side processing for heavy workloads

This guide covers ffmpeg.wasm and WebAssembly deployment. For native FFmpeg, see other skill documents.
