---
name: ffmpeg-cloudflare-containers
description: Complete Cloudflare Container FFmpeg system. PROACTIVELY activate for: (1) Cloudflare Containers setup, (2) Native FFmpeg at edge, (3) GPU-accelerated containers, (4) Durable Objects integration, (5) R2 storage for video files, (6) Container autoscaling, (7) Streaming large files, (8) Workers + Containers architecture, (9) Live streaming relay at edge, (10) Container vs Workers comparison. Provides: Dockerfile examples, Worker code, container configuration, GPU setup, R2 integration, production patterns. Ensures: Native FFmpeg performance at Cloudflare edge with full GPU support.
---

## Quick Reference

| Component | Configuration |
|-----------|---------------|
| Container Class | `export class FFmpegContainer extends Container` |
| Dockerfile | `FROM jrottenberg/ffmpeg:7.1-alpine` |
| wrangler.toml | `[[containers]]` with `class_name` and `image` |

| Feature | Workers (ffmpeg.wasm) | Containers (Native) |
|---------|----------------------|---------------------|
| Size Limit | 10MB | Unlimited |
| Performance | 10-100x slower | Native speed |
| GPU Support | None | NVIDIA available |
| Cold Start | Instant | 2-3 seconds |

## When to Use This Skill

Use for **edge video processing at scale**:
- Native FFmpeg performance at Cloudflare edge
- GPU-accelerated transcoding in containers
- Large file processing (>10MB)
- Complex FFmpeg pipelines
- R2 storage integration for video files

---

# FFmpeg in Cloudflare Containers (2025)

## Overview

Cloudflare Containers (launched June 2025) enable running FFmpeg natively in a full Linux container environment at the edge. This overcomes all limitations of Workers-based approaches (ffmpeg.wasm size limits, SharedArrayBuffer restrictions).

## Key Benefits

| Feature | Workers (ffmpeg.wasm) | Containers (Native) |
|---------|----------------------|---------------------|
| Binary Size | Limited to 10MB | Unlimited (disk space) |
| Performance | WebAssembly overhead | Native speed |
| GPU Support | None | NVIDIA GPUs available |
| Filesystem | Virtual/memory only | Full Linux FS |
| Dependencies | Must compile to WASM | Any Linux package |
| Cold Start | Instant | 2-3 seconds |

## Getting Started

### Prerequisites

```bash
# Docker must be running locally
docker info

# Verify wrangler installation
npx wrangler --version
```

### Create Container Project

```bash
# Create from template
npm create cloudflare@latest -- --template=cloudflare/templates/containers-template

# Or manually configure existing project
```

### wrangler.toml Configuration

```toml
name = "ffmpeg-processor"
main = "src/index.ts"
compatibility_date = "2025-12-19"

# Container configuration
[[containers]]
class_name = "FFmpegContainer"
image = "./Dockerfile"
max_instances = 10

# Durable Object binding for container
[[durable_objects.bindings]]
name = "FFMPEG_CONTAINER"
class_name = "FFmpegContainer"

# Required migration for SQLite-backed containers
[[migrations]]
tag = "v1"
new_sqlite_classes = ["FFmpegContainer"]
```

### Dockerfile for FFmpeg

```dockerfile
# Use official FFmpeg image
FROM jrottenberg/ffmpeg:7.1-alpine AS ffmpeg

# Production image
FROM node:22-alpine

# Install FFmpeg from the official image
COPY --from=ffmpeg /usr/local /usr/local

# Install additional dependencies
RUN apk add --no-cache \
    libva \
    libva-utils \
    mesa-va-gallium

# Set up application
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Container must listen on a port
EXPOSE 8080

CMD ["node", "server.js"]
```

### Worker Code

```typescript
// src/index.ts
import { Container, DurableObject } from "cloudflare:workers";

interface Env {
  FFMPEG_CONTAINER: DurableObjectNamespace<FFmpegContainer>;
}

export class FFmpegContainer extends Container {
  // Default port the container listens on
  defaultPort = 8080;

  // Sleep after 5 minutes of inactivity
  sleepAfter = "5m";

  // Environment variables for container
  envVars = {
    NODE_ENV: "production",
    FFMPEG_PATH: "/usr/local/bin/ffmpeg"
  };

  async onStart() {
    console.log("FFmpeg container started");
  }

  async onStop() {
    console.log("FFmpeg container stopped");
  }

  async onError(error: Error) {
    console.error("Container error:", error);
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Route to container for video processing
    if (url.pathname.startsWith("/process")) {
      // Create unique container instance per job
      const id = env.FFMPEG_CONTAINER.idFromName(crypto.randomUUID());
      const container = env.FFMPEG_CONTAINER.get(id);

      // Forward request to container
      return container.fetch(request);
    }

    // Load balance across containers
    if (url.pathname === "/lb") {
      const id = env.FFMPEG_CONTAINER.newUniqueId();
      const container = env.FFMPEG_CONTAINER.get(id);
      return container.fetch(request);
    }

    return new Response("FFmpeg Container Service", { status: 200 });
  }
};
```

### Container Server (Node.js)

```javascript
// server.js - Runs inside the container
import express from 'express';
import { spawn } from 'child_process';
import fs from 'fs/promises';
import path from 'path';

const app = express();
app.use(express.raw({ type: '*/*', limit: '100mb' }));

const TEMP_DIR = '/tmp/ffmpeg-work';

app.post('/transcode', async (req, res) => {
  const jobId = Date.now().toString();
  const workDir = path.join(TEMP_DIR, jobId);

  await fs.mkdir(workDir, { recursive: true });

  try {
    // Write input file
    const inputPath = path.join(workDir, 'input');
    await fs.writeFile(inputPath, req.body);

    // Get output format from query
    const format = req.query.format || 'mp4';
    const outputPath = path.join(workDir, `output.${format}`);

    // Run FFmpeg
    const result = await runFFmpeg([
      '-i', inputPath,
      '-c:v', 'libx264',
      '-preset', 'veryfast',
      '-crf', '23',
      '-c:a', 'aac',
      '-b:a', '128k',
      '-movflags', '+faststart',
      outputPath
    ]);

    if (result.exitCode !== 0) {
      throw new Error(result.stderr);
    }

    // Return processed file
    const output = await fs.readFile(outputPath);
    res.set('Content-Type', `video/${format}`);
    res.send(output);

  } finally {
    // Cleanup
    await fs.rm(workDir, { recursive: true, force: true });
  }
});

app.post('/gif', async (req, res) => {
  const jobId = Date.now().toString();
  const workDir = path.join(TEMP_DIR, jobId);

  await fs.mkdir(workDir, { recursive: true });

  try {
    const inputPath = path.join(workDir, 'input');
    const palettePath = path.join(workDir, 'palette.png');
    const outputPath = path.join(workDir, 'output.gif');

    await fs.writeFile(inputPath, req.body);

    // Two-pass GIF for better quality
    // Pass 1: Generate palette
    await runFFmpeg([
      '-i', inputPath,
      '-vf', 'fps=15,scale=480:-1:flags=lanczos,palettegen',
      '-y', palettePath
    ]);

    // Pass 2: Generate GIF with palette
    await runFFmpeg([
      '-i', inputPath,
      '-i', palettePath,
      '-lavfi', 'fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse',
      '-y', outputPath
    ]);

    const output = await fs.readFile(outputPath);
    res.set('Content-Type', 'image/gif');
    res.send(output);

  } finally {
    await fs.rm(workDir, { recursive: true, force: true });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', ffmpeg: process.env.FFMPEG_PATH });
});

function runFFmpeg(args) {
  return new Promise((resolve) => {
    const proc = spawn('ffmpeg', args, { stdio: ['pipe', 'pipe', 'pipe'] });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => { stdout += data; });
    proc.stderr.on('data', (data) => { stderr += data; });

    proc.on('close', (exitCode) => {
      resolve({ exitCode, stdout, stderr });
    });
  });
}

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`FFmpeg server listening on port ${PORT}`);
});
```

## GPU-Accelerated Containers

Cloudflare Containers support NVIDIA GPUs for hardware-accelerated encoding:

### GPU Container Configuration

```toml
[[containers]]
class_name = "FFmpegGPU"
image = "./Dockerfile.gpu"
max_instances = 5
# GPU instances have higher resource allocation
```

### GPU Dockerfile

```dockerfile
FROM nvidia/cuda:12.4-runtime-ubuntu24.04

# Install FFmpeg with NVIDIA support
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libnvidia-encode-550 \
    libnvidia-decode-550 \
    && rm -rf /var/lib/apt/lists/*

# Verify NVENC support
RUN ffmpeg -encoders | grep nvenc

WORKDIR /app
COPY . .

EXPOSE 8080
CMD ["node", "server.js"]
```

### NVENC Encoding in Container

```javascript
app.post('/transcode-gpu', async (req, res) => {
  const args = [
    '-hwaccel', 'cuda',
    '-hwaccel_output_format', 'cuda',
    '-i', inputPath,
    '-c:v', 'h264_nvenc',
    '-preset', 'p4',
    '-cq', '23',
    '-c:a', 'aac',
    '-b:a', '128k',
    outputPath
  ];

  await runFFmpeg(args);
});
```

## Autoscaling Configuration

```typescript
export class FFmpegContainer extends Container {
  // Autoscaling based on CPU usage
  static scaling = {
    minInstances: 1,      // Always keep one warm
    maxInstances: 20,
    targetCPU: 75,        // Scale up at 75% CPU
    scaleDownDelay: "5m"  // Wait before scaling down
  };

  sleepAfter = "10m";  // Sleep idle containers after 10 min
}
```

## Pricing Considerations

| Metric | Billing |
|--------|---------|
| Compute | Per 10ms while active |
| Idle | No charge (containers sleep) |
| Storage | Per GB-month |
| Egress | Standard Cloudflare egress |

## Best Practices

### 1. Container Size Optimization

```dockerfile
# Use multi-stage builds
FROM jrottenberg/ffmpeg:7.1-alpine AS ffmpeg
FROM node:22-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Final minimal image
FROM node:22-alpine
COPY --from=ffmpeg /usr/local/bin/ffmpeg /usr/local/bin/
COPY --from=ffmpeg /usr/local/bin/ffprobe /usr/local/bin/
COPY --from=builder /app/node_modules ./node_modules
COPY . .

CMD ["node", "server.js"]
```

### 2. Warm Instance Strategy

```typescript
// Keep containers warm for low-latency
export class FFmpegContainer extends Container {
  sleepAfter = "30m";  // Longer idle before sleep
}

// Pre-warm containers on deploy
export default {
  async scheduled(controller: ScheduledController, env: Env) {
    // Ping containers to keep them warm
    const id = env.FFMPEG_CONTAINER.idFromName("warmup");
    const container = env.FFMPEG_CONTAINER.get(id);
    await container.fetch(new Request("http://internal/health"));
  }
};
```

### 3. Streaming Large Files

```javascript
// Stream output instead of buffering
app.post('/transcode-stream', async (req, res) => {
  const ffmpeg = spawn('ffmpeg', [
    '-i', 'pipe:0',
    '-c:v', 'libx264',
    '-f', 'mp4',
    '-movflags', 'frag_keyframe+empty_moov',
    'pipe:1'
  ]);

  req.pipe(ffmpeg.stdin);
  ffmpeg.stdout.pipe(res);

  ffmpeg.stderr.on('data', (data) => {
    console.log('FFmpeg:', data.toString());
  });
});
```

### 4. R2 Storage Integration

```typescript
// Store processed files in R2
export default {
  async fetch(request: Request, env: Env) {
    // Process video in container
    const result = await container.fetch(request);

    // Store in R2
    const key = `processed/${Date.now()}.mp4`;
    await env.R2_BUCKET.put(key, result.body);

    return new Response(JSON.stringify({ key }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

## Common Use Cases

### Video Thumbnails at Edge

```javascript
app.post('/thumbnail', async (req, res) => {
  await runFFmpeg([
    '-i', inputPath,
    '-ss', '00:00:01',
    '-vframes', '1',
    '-vf', 'scale=320:-1',
    outputPath
  ]);
});
```

### Audio Extraction

```javascript
app.post('/extract-audio', async (req, res) => {
  await runFFmpeg([
    '-i', inputPath,
    '-vn',
    '-c:a', 'aac',
    '-b:a', '192k',
    outputPath
  ]);
});
```

### Live Streaming Relay

```javascript
// Relay RTMP to HLS at edge
const ffmpeg = spawn('ffmpeg', [
  '-i', rtmpInput,
  '-c:v', 'copy',
  '-c:a', 'copy',
  '-hls_time', '4',
  '-hls_list_size', '10',
  '-hls_flags', 'delete_segments',
  '/output/stream.m3u8'
]);
```

## Deployment

```bash
# Deploy to Cloudflare
wrangler deploy

# First deployment takes several minutes
# Subsequent deploys are faster with incremental image updates
```

## Monitoring

```javascript
// Health check endpoint
app.get('/metrics', async (req, res) => {
  const metrics = {
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    deploymentId: process.env.CLOUDFLARE_DEPLOYMENT_ID
  };
  res.json(metrics);
});
```

## Comparison: Workers vs Containers

| Use Case | Recommendation |
|----------|----------------|
| Simple filters (resize, crop) | Workers + ffmpeg.wasm |
| Full transcoding | Containers |
| GPU acceleration | Containers (GPU instances) |
| Low latency (<100ms) | Workers |
| Large files (>10MB) | Containers |
| Complex pipelines | Containers |

## Troubleshooting

### Container Not Starting

```bash
# Check Docker locally
docker build -t test-ffmpeg .
docker run --rm test-ffmpeg ffmpeg -version

# Verify architecture
docker inspect test-ffmpeg | grep Architecture
# Must be linux/amd64
```

### FFmpeg Not Found

```dockerfile
# Ensure FFmpeg is in PATH
ENV PATH="/usr/local/bin:${PATH}"

# Verify installation
RUN which ffmpeg && ffmpeg -version
```

### Timeout Issues

```typescript
// Increase timeout for long operations
export class FFmpegContainer extends Container {
  // Extend request timeout
  async fetch(request: Request) {
    // Container internal timeout handling
    const controller = new AbortController();
    setTimeout(() => controller.abort(), 300000); // 5 min

    return super.fetch(request, { signal: controller.signal });
  }
}
```

## References

- [Cloudflare Containers Documentation](https://developers.cloudflare.com/containers/)
- [Cloudflare Containers Announcement](https://blog.cloudflare.com/containers-are-available-in-public-beta-for-simple-global-and-programmable/)
- [Container Image Management](https://developers.cloudflare.com/containers/platform-details/image-management/)
