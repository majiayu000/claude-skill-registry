---
name: sharp
description: 高性能Node.js图片处理库。使用libvips最快速地调整JPEG、PNG、WebP、AVIF和TIFF图片大小。
metadata:
  short-description: 高性能图片处理
source:
  repository: https://github.com/lovell/sharp
  license: Apache-2.0
  stars: 29k+
---

# Sharp Tool

## Description
High-performance image processing for resizing, converting, and manipulating images.

## Source
- Repository: [lovell/sharp](https://github.com/lovell/sharp)
- License: Apache-2.0

## Installation

```bash
npm install sharp
```

## Usage Examples

### Resize Image

```typescript
import sharp from 'sharp';

// Resize to specific dimensions
await sharp('input.jpg')
  .resize(800, 600)
  .toFile('output.jpg');

// Resize with aspect ratio preserved
await sharp('input.jpg')
  .resize(800, null)  // Width 800, auto height
  .toFile('output.jpg');

// Resize with fit options
await sharp('input.jpg')
  .resize(800, 600, {
    fit: 'cover',      // cover, contain, fill, inside, outside
    position: 'center' // center, top, right, bottom, left
  })
  .toFile('output.jpg');
```

### Convert Format

```typescript
// Convert to WebP
await sharp('input.jpg')
  .webp({ quality: 80 })
  .toFile('output.webp');

// Convert to AVIF (modern format)
await sharp('input.jpg')
  .avif({ quality: 60 })
  .toFile('output.avif');

// Convert to PNG with transparency
await sharp('input.jpg')
  .png({ compressionLevel: 9 })
  .toFile('output.png');
```

### Image Manipulation

```typescript
// Rotate and flip
await sharp('input.jpg')
  .rotate(90)
  .flip()
  .toFile('output.jpg');

// Blur and sharpen
await sharp('input.jpg')
  .blur(5)
  .sharpen()
  .toFile('output.jpg');

// Grayscale and tint
await sharp('input.jpg')
  .grayscale()
  .tint({ r: 255, g: 128, b: 0 })
  .toFile('output.jpg');

// Crop
await sharp('input.jpg')
  .extract({ left: 100, top: 100, width: 500, height: 300 })
  .toFile('output.jpg');
```

### Add Watermark

```typescript
async function addWatermark(input: string, watermark: string, output: string) {
  const image = sharp(input);
  const { width, height } = await image.metadata();
  
  // Resize watermark
  const watermarkBuffer = await sharp(watermark)
    .resize(Math.round(width! * 0.2))
    .toBuffer();
  
  await image
    .composite([{
      input: watermarkBuffer,
      gravity: 'southeast',
      blend: 'over',
    }])
    .toFile(output);
}
```

### Generate Thumbnails

```typescript
async function generateThumbnails(input: string, sizes: number[]) {
  const image = sharp(input);
  
  await Promise.all(sizes.map(size =>
    image
      .clone()
      .resize(size, size, { fit: 'cover' })
      .jpeg({ quality: 80 })
      .toFile(`thumb-${size}.jpg`)
  ));
}

// Usage
await generateThumbnails('photo.jpg', [64, 128, 256, 512]);
```

### Stream Processing

```typescript
import { createReadStream, createWriteStream } from 'fs';

// Process large images with streams
createReadStream('large-input.jpg')
  .pipe(sharp().resize(1920, 1080).jpeg({ quality: 85 }))
  .pipe(createWriteStream('output.jpg'));
```

## Tags
`image`, `resize`, `convert`, `thumbnail`, `processing`

## Compatibility
- Codex: ✅
- Claude Code: ✅
