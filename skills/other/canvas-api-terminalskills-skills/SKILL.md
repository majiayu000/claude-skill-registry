---
name: canvas-api
description: >-
  Draw 2D graphics with the HTML5 Canvas API — shapes, text, images, gradients,
  transformations, pixel manipulation, and offscreen rendering. Use when tasks
  involve generating images server-side (with node-canvas), creating charts,
  image compositing, watermarking, or browser-based drawing applications.
license: Apache-2.0
compatibility: "Browser or Node.js 14+ with node-canvas"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: design
  tags: ["canvas", "2d-graphics", "image-manipulation", "drawing", "node-canvas"]
---

# Canvas API

The Canvas 2D API draws shapes, text, and images to a bitmap. In Node.js, the `canvas` package provides the same API for server-side image generation.

## Setup (Node.js)

```bash
# Install node-canvas for server-side rendering. Requires system deps (Cairo).
npm install canvas
```

## Creating a Canvas and Drawing Shapes

```typescript
// src/canvas/shapes.ts — Create a canvas, draw rectangles, circles, and lines.
// Works identically in browser (document.createElement) and Node (createCanvas).
import { createCanvas } from "canvas";

const canvas = createCanvas(800, 600);
const ctx = canvas.getContext("2d");

// Background
ctx.fillStyle = "#1a1a2e";
ctx.fillRect(0, 0, 800, 600);

// Rectangle with rounded corners
ctx.beginPath();
ctx.roundRect(50, 50, 200, 120, 12);
ctx.fillStyle = "#e94560";
ctx.fill();

// Circle
ctx.beginPath();
ctx.arc(450, 110, 60, 0, Math.PI * 2);
ctx.fillStyle = "#0f3460";
ctx.fill();

// Line with gradient
const gradient = ctx.createLinearGradient(50, 300, 750, 300);
gradient.addColorStop(0, "#e94560");
gradient.addColorStop(1, "#0f3460");
ctx.strokeStyle = gradient;
ctx.lineWidth = 4;
ctx.beginPath();
ctx.moveTo(50, 300);
ctx.lineTo(750, 300);
ctx.stroke();
```

## Drawing Text

```typescript
// src/canvas/text.ts — Render styled text on canvas with measurements.
import { createCanvas } from "canvas";

const canvas = createCanvas(800, 200);
const ctx = canvas.getContext("2d");

ctx.fillStyle = "#ffffff";
ctx.fillRect(0, 0, 800, 200);

// Title text
ctx.font = "bold 48px sans-serif";
ctx.fillStyle = "#1a1a2e";
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.fillText("Hello Canvas", 400, 80);

// Measure text for positioning
const metrics = ctx.measureText("Hello Canvas");
console.log(`Width: ${metrics.width}px`);
```

## Image Compositing

```typescript
// src/canvas/composite.ts — Load images and composite them with blend modes.
// Useful for watermarking, overlays, and social media image generation.
import { createCanvas, loadImage } from "canvas";
import fs from "fs";

export async function addWatermark(imagePath: string, watermarkPath: string, outputPath: string) {
  const image = await loadImage(imagePath);
  const watermark = await loadImage(watermarkPath);

  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext("2d");

  // Draw base image
  ctx.drawImage(image, 0, 0);

  // Draw watermark with transparency
  ctx.globalAlpha = 0.3;
  ctx.drawImage(
    watermark,
    image.width - watermark.width - 20,
    image.height - watermark.height - 20
  );

  const buffer = canvas.toBuffer("image/png");
  fs.writeFileSync(outputPath, buffer);
}
```

## Pixel Manipulation

```typescript
// src/canvas/pixels.ts — Read and modify individual pixels for image processing.
// Apply filters like grayscale, invert, or custom convolution kernels.
import { createCanvas, loadImage } from "canvas";

export async function grayscale(imagePath: string): Promise<Buffer> {
  const image = await loadImage(imagePath);
  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext("2d");

  ctx.drawImage(image, 0, 0);
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imageData.data;

  for (let i = 0; i < data.length; i += 4) {
    const avg = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
    data[i] = data[i + 1] = data[i + 2] = avg;
  }

  ctx.putImageData(imageData, 0, 0);
  return canvas.toBuffer("image/png");
}
```

## Exporting

```typescript
// src/canvas/export.ts — Save canvas output as PNG, JPEG, or PDF.
import { createCanvas } from "canvas";
import fs from "fs";

const canvas = createCanvas(400, 400);
const ctx = canvas.getContext("2d");
ctx.fillStyle = "#e94560";
ctx.fillRect(0, 0, 400, 400);

// PNG
fs.writeFileSync("output.png", canvas.toBuffer("image/png"));

// JPEG with quality
fs.writeFileSync("output.jpg", canvas.toBuffer("image/jpeg", { quality: 0.9 }));

// PDF (node-canvas supports PDF backend)
const pdfCanvas = createCanvas(400, 400, "pdf");
const pdfCtx = pdfCanvas.getContext("2d");
pdfCtx.fillStyle = "#0f3460";
pdfCtx.fillRect(0, 0, 400, 400);
fs.writeFileSync("output.pdf", pdfCanvas.toBuffer("application/pdf"));
```
