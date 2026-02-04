---
name: sharp
description: Processes images with Sharp, the high-performance Node.js library for resizing, converting, and optimizing images. Use when building image pipelines, generating thumbnails, or optimizing uploads server-side.
---

# Sharp

High-performance Node.js image processing. 4-5x faster than ImageMagick for resizing JPEG, PNG, WebP, AVIF, and TIFF.

## Quick Start

```bash
npm install sharp
```

```javascript
import sharp from 'sharp';

// Resize and convert
await sharp('input.jpg')
  .resize(800, 600)
  .toFormat('webp')
  .toFile('output.webp');

// From buffer
const buffer = await sharp(inputBuffer)
  .resize(400)
  .toBuffer();
```

## Resize

```javascript
// Fixed dimensions (may crop)
await sharp('input.jpg')
  .resize(800, 600)
  .toFile('output.jpg');

// Fit within dimensions (maintain aspect ratio)
await sharp('input.jpg')
  .resize(800, 600, { fit: 'inside' })
  .toFile('output.jpg');

// Fill dimensions (crop to fit)
await sharp('input.jpg')
  .resize(800, 600, { fit: 'cover' })
  .toFile('output.jpg');

// Width only (auto height)
await sharp('input.jpg')
  .resize({ width: 800 })
  .toFile('output.jpg');

// Without upscaling
await sharp('input.jpg')
  .resize(2000, null, { withoutEnlargement: true })
  .toFile('output.jpg');
```

### Fit Options

| Option | Description |
|--------|-------------|
| `cover` | Crop to cover dimensions (default) |
| `contain` | Fit within, add background if needed |
| `fill` | Stretch to fill (ignores aspect ratio) |
| `inside` | Fit within, never exceed |
| `outside` | Fit to cover, may exceed |

### Position (for cover/contain)

```javascript
await sharp('input.jpg')
  .resize(800, 600, {
    fit: 'cover',
    position: 'top'  // top, right top, right, right bottom, bottom, left bottom, left, left top, center
  })
  .toFile('output.jpg');

// Or use gravity
await sharp('input.jpg')
  .resize(800, 600, {
    fit: 'cover',
    position: sharp.strategy.attention  // Focus on interesting region
  })
  .toFile('output.jpg');
```

## Format Conversion

```javascript
// To WebP
await sharp('input.jpg')
  .webp({ quality: 80 })
  .toFile('output.webp');

// To AVIF (best compression)
await sharp('input.jpg')
  .avif({ quality: 60 })
  .toFile('output.avif');

// To PNG
await sharp('input.jpg')
  .png({ compressionLevel: 9 })
  .toFile('output.png');

// To JPEG
await sharp('input.png')
  .jpeg({ quality: 80, mozjpeg: true })
  .toFile('output.jpg');

// Auto format based on input
await sharp('input.jpg')
  .toFormat('webp', { quality: 80 })
  .toFile('output.webp');
```

### Format Options

```javascript
// JPEG
.jpeg({
  quality: 80,
  progressive: true,
  mozjpeg: true,  // Better compression
})

// PNG
.png({
  compressionLevel: 9,
  palette: true,     // For fewer colors
  quality: 80,       // For palette mode
})

// WebP
.webp({
  quality: 80,
  lossless: false,
  nearLossless: false,
  effort: 4,         // 0-6, higher = slower + smaller
})

// AVIF
.avif({
  quality: 60,
  effort: 4,         // 0-9, higher = slower + smaller
  chromaSubsampling: '4:4:4',
})
```

## Operations

### Crop/Extract

```javascript
// Extract region
await sharp('input.jpg')
  .extract({ left: 100, top: 100, width: 300, height: 200 })
  .toFile('output.jpg');

// Trim whitespace/borders
await sharp('input.jpg')
  .trim()
  .toFile('output.jpg');
```

### Rotate & Flip

```javascript
// Rotate (auto from EXIF by default)
await sharp('input.jpg')
  .rotate(90)  // Degrees clockwise
  .toFile('output.jpg');

// Flip
await sharp('input.jpg')
  .flip()   // Vertical
  .flop()   // Horizontal
  .toFile('output.jpg');
```

### Color Adjustments

```javascript
await sharp('input.jpg')
  .grayscale()
  .toFile('output.jpg');

await sharp('input.jpg')
  .tint({ r: 255, g: 200, b: 200 })
  .toFile('output.jpg');

await sharp('input.jpg')
  .modulate({
    brightness: 1.2,  // 1 = no change
    saturation: 0.8,
    hue: 180,         // Degrees
  })
  .toFile('output.jpg');

await sharp('input.jpg')
  .negate()
  .toFile('output.jpg');
```

### Effects

```javascript
// Blur
await sharp('input.jpg')
  .blur(5)  // Sigma value, 0.3-1000
  .toFile('output.jpg');

// Sharpen
await sharp('input.jpg')
  .sharpen()  // Default
  .toFile('output.jpg');

await sharp('input.jpg')
  .sharpen({
    sigma: 1,
    m1: 1,
    m2: 3,
  })
  .toFile('output.jpg');

// Normalize (stretch contrast)
await sharp('input.jpg')
  .normalize()
  .toFile('output.jpg');
```

### Composite (Overlays)

```javascript
// Add watermark
await sharp('input.jpg')
  .composite([
    {
      input: 'watermark.png',
      gravity: 'southeast',
      blend: 'over',
    }
  ])
  .toFile('output.jpg');

// Multiple overlays
await sharp('base.jpg')
  .composite([
    { input: 'layer1.png', top: 0, left: 0 },
    { input: 'layer2.png', top: 100, left: 100, blend: 'multiply' },
    {
      input: Buffer.from('<svg>...</svg>'),
      top: 50,
      left: 50,
    }
  ])
  .toFile('output.jpg');
```

### Add Background/Extend

```javascript
// Add padding with background color
await sharp('input.png')
  .extend({
    top: 20,
    bottom: 20,
    left: 20,
    right: 20,
    background: { r: 255, g: 255, b: 255, alpha: 1 }
  })
  .toFile('output.png');

// Flatten transparency
await sharp('input.png')
  .flatten({ background: '#ffffff' })
  .toFile('output.jpg');
```

## Pipeline Chaining

```javascript
// All operations chain together
await sharp('input.jpg')
  .resize(800, 600, { fit: 'cover' })
  .rotate(90)
  .sharpen()
  .modulate({ brightness: 1.1 })
  .webp({ quality: 80 })
  .toFile('output.webp');
```

## Metadata

```javascript
// Get image info
const metadata = await sharp('input.jpg').metadata();
console.log(metadata);
// { width, height, format, space, channels, depth, density, hasAlpha, ... }

// Get stats (pixel analysis)
const stats = await sharp('input.jpg').stats();
console.log(stats);
// { channels: [{ min, max, sum, squaresSum, mean, stdev, ... }] }
```

## Streams & Buffers

```javascript
import fs from 'fs';

// Stream input/output
const readStream = fs.createReadStream('input.jpg');
const writeStream = fs.createWriteStream('output.webp');

readStream
  .pipe(sharp().resize(800).webp())
  .pipe(writeStream);

// Buffer to buffer
const inputBuffer = fs.readFileSync('input.jpg');
const outputBuffer = await sharp(inputBuffer)
  .resize(400)
  .toBuffer();

// With info
const { data, info } = await sharp(inputBuffer)
  .resize(400)
  .toBuffer({ resolveWithObject: true });

console.log(info);
// { format, width, height, channels, size }
```

## Next.js / API Routes

```typescript
// app/api/image/route.ts
import { NextRequest, NextResponse } from 'next/server';
import sharp from 'sharp';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const url = searchParams.get('url');
  const width = parseInt(searchParams.get('w') || '800');
  const quality = parseInt(searchParams.get('q') || '80');

  // Fetch original image
  const response = await fetch(url!);
  const buffer = Buffer.from(await response.arrayBuffer());

  // Process
  const processed = await sharp(buffer)
    .resize(width)
    .webp({ quality })
    .toBuffer();

  return new NextResponse(processed, {
    headers: {
      'Content-Type': 'image/webp',
      'Cache-Control': 'public, max-age=31536000',
    },
  });
}
```

## Generate Thumbnails

```javascript
async function generateThumbnails(inputPath, outputDir) {
  const sizes = [
    { name: 'thumb', width: 150, height: 150 },
    { name: 'small', width: 400 },
    { name: 'medium', width: 800 },
    { name: 'large', width: 1200 },
  ];

  const image = sharp(inputPath);
  const metadata = await image.metadata();
  const basename = path.basename(inputPath, path.extname(inputPath));

  const results = await Promise.all(
    sizes.map(async ({ name, width, height }) => {
      const outputPath = path.join(outputDir, `${basename}-${name}.webp`);

      await sharp(inputPath)
        .resize(width, height, { fit: height ? 'cover' : 'inside' })
        .webp({ quality: 80 })
        .toFile(outputPath);

      return { name, path: outputPath };
    })
  );

  return results;
}
```

## Handle Uploads

```javascript
import formidable from 'formidable';
import sharp from 'sharp';

async function handleUpload(req) {
  const form = formidable();
  const [fields, files] = await form.parse(req);
  const file = files.image[0];

  // Validate and process
  const metadata = await sharp(file.filepath).metadata();

  if (!['jpeg', 'png', 'webp'].includes(metadata.format)) {
    throw new Error('Invalid format');
  }

  // Process and save
  const filename = `${Date.now()}-${file.originalFilename}`;
  const processed = await sharp(file.filepath)
    .resize(1200, 1200, { fit: 'inside', withoutEnlargement: true })
    .webp({ quality: 80 })
    .toFile(`./uploads/${filename}.webp`);

  return {
    url: `/uploads/${filename}.webp`,
    width: processed.width,
    height: processed.height,
  };
}
```

## Batch Processing

```javascript
import sharp from 'sharp';
import { glob } from 'glob';
import path from 'path';

async function batchOptimize(inputGlob, outputDir) {
  const files = await glob(inputGlob);

  const results = await Promise.all(
    files.map(async (file) => {
      const basename = path.basename(file, path.extname(file));
      const output = path.join(outputDir, `${basename}.webp`);

      const info = await sharp(file)
        .resize(1920, 1080, { fit: 'inside', withoutEnlargement: true })
        .webp({ quality: 80 })
        .toFile(output);

      return { input: file, output, size: info.size };
    })
  );

  return results;
}
```

## Best Practices

1. **Use streams** for large files to reduce memory
2. **Set concurrency** with `sharp.concurrency(1)` for low-memory environments
3. **Pre-compute sizes** when possible (eager thumbnails)
4. **Use WebP or AVIF** for best compression
5. **Cache processed images** - don't reprocess on every request
6. **Handle EXIF rotation** - Sharp auto-rotates by default
