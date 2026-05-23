---
name: image-processing
description: >
  Implement image processing for PhotoVault using Sharp and streaming patterns.
  Use when working with photo uploads, thumbnail generation, EXIF handling,
  ZIP extraction, or optimizing images for web. Includes memory management
  for serverless and PhotoVault storage structure.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\image-processing-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/image-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/image-[task-name]-plan.md
   Write critique to: docs/claude/plans/image-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Image Processing Integration

## Core Principles

### Never Load Large Files Into Memory

Use streams for anything over a few MB. Serverless functions have memory limits.

```typescript
// ❌ BAD: Loads entire file into memory
const buffer = await readFile(largeFile)
const result = await sharp(buffer).resize(1920).toBuffer()

// ✅ GOOD: Stream processing
import { pipeline } from 'stream/promises'

await pipeline(
  createReadStream(inputPath),
  sharp().resize(1920).jpeg({ quality: 85 }),
  createWriteStream(outputPath)
)
```

### Generate Multiple Sizes Upfront

Don't resize on-demand - generate all needed sizes at upload time.

```typescript
const SIZES = {
  thumbnail: { width: 300, height: 300 },   // Grid view
  preview: { width: 800, height: 800 },     // Quick preview
  display: { width: 1920, height: 1920 },   // Full screen
  original: null,                           // Keep original
}
```

### Always Auto-Orient

EXIF orientation metadata can make photos display rotated.

```typescript
sharp(buffer)
  .rotate()  // Auto-rotate based on EXIF
  .resize(1920, 1920, { fit: 'inside' })
  .jpeg({ quality: 85 })
```

## Anti-Patterns

**Loading entire ZIP into memory**
```typescript
// WRONG: ZIP could be 2GB
const zipBuffer = await readFile(zipPath)
const zip = new AdmZip(zipBuffer)

// RIGHT: Stream extraction
import unzipper from 'unzipper'
const directory = await unzipper.Open.file(zipPath)
for (const entry of directory.files) {
  // Process one at a time
}
```

**Processing all photos in parallel**
```typescript
// WRONG: Memory explosion with 100 photos
await Promise.all(photos.map(p => processPhoto(p)))

// RIGHT: Limit concurrency
import pLimit from 'p-limit'
const limit = pLimit(3)
await Promise.all(photos.map(p => limit(() => processPhoto(p))))
```

**Not cleaning up temp files**
```typescript
// WRONG: Temp files accumulate
const tempPath = `/tmp/${uuid()}.jpg`
await writeFile(tempPath, buffer)
await processImage(tempPath)

// RIGHT: Always cleanup
try {
  await writeFile(tempPath, buffer)
  await processImage(tempPath)
} finally {
  await unlink(tempPath).catch(() => {})
}
```

**Over-compressing images**
```typescript
// WRONG: Quality 50 looks terrible
sharp(buffer).jpeg({ quality: 50 })

// RIGHT: Balance quality and size
sharp(buffer).jpeg({ quality: 85, progressive: true })
```

**Enlarging small images**
```typescript
// WRONG: 800px enlarged to 1920px looks bad
sharp(buffer).resize(1920, 1920)

// RIGHT: Prevent enlargement
sharp(buffer).resize(1920, 1920, {
  fit: 'inside',
  withoutEnlargement: true
})
```

## Photo Processing Pipeline

```typescript
// src/lib/image/processor.ts
import sharp from 'sharp'
import pLimit from 'p-limit'

export async function processPhoto(inputBuffer: Buffer, filename: string) {
  const image = sharp(inputBuffer)
  const metadata = await image.metadata()
  const oriented = sharp(inputBuffer).rotate()

  const [original, thumbnail, display] = await Promise.all([
    oriented.clone()
      .jpeg({ quality: 92, progressive: true })
      .toBuffer(),
    oriented.clone()
      .resize(300, 300, { fit: 'inside', withoutEnlargement: true })
      .jpeg({ quality: 80, progressive: true })
      .toBuffer(),
    oriented.clone()
      .resize(1920, 1920, { fit: 'inside', withoutEnlargement: true })
      .jpeg({ quality: 85, progressive: true })
      .toBuffer(),
  ])

  return {
    filename,
    original,
    thumbnail,
    display,
    metadata: {
      width: metadata.width!,
      height: metadata.height!,
      format: metadata.format!,
      size: inputBuffer.length,
    },
  }
}

// Process batch with concurrency limit
export async function processPhotoBatch(photos: Array<{ buffer: Buffer; filename: string }>) {
  const limit = pLimit(3)  // Max 3 concurrent
  return Promise.all(photos.map(photo =>
    limit(() => processPhoto(photo.buffer, photo.filename))
  ))
}
```

## ZIP Extraction with Streaming

```typescript
// src/lib/image/zip-extractor.ts
import unzipper from 'unzipper'
import path from 'path'

const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic']

export async function extractPhotosFromZip(zipPath: string) {
  const directory = await unzipper.Open.file(zipPath)
  const photos: Array<{ filename: string; buffer: Buffer }> = []

  for (const entry of directory.files) {
    if (entry.type === 'Directory') continue
    if (entry.path.includes('__MACOSX')) continue
    if (entry.path.startsWith('.')) continue

    const ext = path.extname(entry.path).toLowerCase()
    if (!IMAGE_EXTENSIONS.includes(ext)) continue

    const buffer = await entry.buffer()
    photos.push({ filename: path.basename(entry.path), buffer })
  }

  return photos
}
```

## PhotoVault Configuration

### Storage Structure

```
gallery-photos/
├── {gallery_id}/
│   ├── originals/      # Full quality, for download
│   ├── thumbnails/     # 300px, for grid
│   └── full/           # 1920px, for display
```

### Size Guidelines

| Version | Max Size | Quality | Use Case |
|---------|----------|---------|----------|
| Original | Unchanged | 92% | Download |
| Display | 1920px | 85% | Full screen view |
| Thumbnail | 300px | 80% | Grid/gallery |

### Dependencies

```bash
npm install sharp p-limit unzipper exif-reader blurhash
```

### Serverless Limits (Vercel)

- Memory: 1024MB default, up to 3008MB
- Timeout: 10s (Hobby), 60s (Pro)
- Payload: 4.5MB

For large uploads, use the desktop app with chunked uploads.

## Debugging Checklist

1. Are large files being streamed, not loaded into memory?
2. Is concurrency limited with pLimit?
3. Is .rotate() called to fix EXIF orientation?
4. Are progressive JPEGs being generated?
5. Is withoutEnlargement preventing upscaling?
6. Are temp files cleaned up in finally blocks?
