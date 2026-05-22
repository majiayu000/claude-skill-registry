---
name: cloudflare-images
description: "Store, transform, and deliver optimized images with Cloudflare Images. Covers image upload (API, Worker, Direct Creator Upload), variants, transformations (URL and Workers), bindings, Polish, signed URLs, formats (AVIF, WebP), R2 integration, watermarks. Keywords: Cloudflare Images, image transformations, variants, /cdn-cgi/image/, imagedelivery.net, Polish, AVIF, WebP, signed URLs, Direct Creator Upload, Images binding, R2, watermark."
---

# Cloudflare Images

End-to-end image storage, transformation, and delivery solution on Cloudflare's global network.

## Quick Navigation

- Upload methods → `references/upload.md`
- Transformations → `references/transformations.md`
- Variants → `references/variants.md`
- Workers binding → `references/binding.md`
- Polish → `references/polish.md`
- Signed URLs → `references/security.md`
- Pricing → `references/pricing.md`

## When to Use

- Storing and delivering optimized images at scale
- Transforming remote images on-the-fly
- Resizing, cropping, converting image formats
- Adding watermarks to images
- Serving responsive images with `srcset`
- Protecting images with signed URLs
- Optimizing images from R2 storage

## Two Usage Modes

| Mode              | Description                                     | Billing                          |
| ----------------- | ----------------------------------------------- | -------------------------------- |
| Storage in Images | Upload images to Cloudflare, serve via variants | Images Stored + Images Delivered |
| Transform remote  | Optimize images from any origin (R2, S3, etc.)  | Images Transformed (unique/30d)  |

## Quick Start

### Upload an Image (API)

```bash
curl --request POST \
  --url https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/images/v1 \
  --header 'Authorization: Bearer <API_TOKEN>' \
  --header 'Content-Type: multipart/form-data' \
  --form file=@./image.jpg
```

### Transform via URL

```html
<img src="/cdn-cgi/image/width=400,quality=80,format=auto/uploads/hero.jpg" />
```

### Transform via Workers

```js
fetch(imageURL, {
  cf: {
    image: {
      width: 800,
      height: 600,
      fit: "cover",
      format: "auto",
    },
  },
});
```

## URL Format

```
https://<ZONE>/cdn-cgi/image/<OPTIONS>/<SOURCE-IMAGE>
```

- `<ZONE>` — your Cloudflare domain
- `/cdn-cgi/image/` — fixed prefix for image transformations
- `<OPTIONS>` — comma-separated: `width=400,quality=80,format=auto`
- `<SOURCE-IMAGE>` — absolute path or full URL

### Stored Images Delivery

```
https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/<VARIANT_NAME>
```

## Transformation Options

| Option    | Description                  | Example                        |
| --------- | ---------------------------- | ------------------------------ |
| `width`   | Max width in pixels          | `width=800`                    |
| `height`  | Max height in pixels         | `height=600`                   |
| `fit`     | Resize mode                  | `fit=cover`                    |
| `format`  | Output format                | `format=auto`                  |
| `quality` | JPEG/WebP/AVIF quality 1-100 | `quality=85`                   |
| `gravity` | Crop focus point             | `gravity=face`, `gravity=auto` |
| `blur`    | Blur radius 1-250            | `blur=50`                      |
| `sharpen` | Sharpening 0-10              | `sharpen=1`                    |
| `rotate`  | Rotation degrees             | `rotate=90`                    |
| `trim`    | Remove pixels from edges     | `trim=20;30;20;0`              |

### Fit Modes

| Mode         | Behavior                                     |
| ------------ | -------------------------------------------- |
| `scale-down` | Shrink only, never enlarge                   |
| `contain`    | Fit within dimensions, preserve aspect ratio |
| `cover`      | Fill dimensions, crop if needed              |
| `crop`       | Like cover but never enlarges                |
| `pad`        | Fit within, add background color             |

### Format Auto

`format=auto` serves WebP or AVIF based on browser support. Use with Accept header parsing in Workers.

## Supported Formats

### Input

- JPEG, PNG, GIF (animated), WebP (animated), SVG, HEIC

### Output

- JPEG, PNG, GIF, WebP, AVIF, SVG (passthrough)

**Note:** HEIC must be served as AVIF/WebP/JPEG/PNG. SVG is not resized (inherently scalable).

## Limits

| Constraint                      | Limit                     |
| ------------------------------- | ------------------------- |
| Max image dimension             | 12,000 pixels             |
| Max image area                  | 100 megapixels            |
| Max file size (transformations) | 70 MB                     |
| Max file size (storage)         | 10 MB                     |
| GIF/WebP animation              | 50 megapixels total       |
| AVIF output hard limit          | 1,200 px (1,600 explicit) |
| Variants per account            | 100                       |

## Workers Integration

### Images Binding Setup

```toml
# wrangler.toml
[images]
binding = "IMAGES"
```

### Transform with Binding

```ts
const response = (await env.IMAGES.input(stream).transform({ width: 800 }).transform({ blur: 20 }).output({ format: "image/avif" })).response();
```

### Draw Watermark

```ts
const watermark = await fetch("https://example.com/watermark.png");
const image = await fetch("https://example.com/photo.jpg");

const response = (
  await env.IMAGES.input(image.body)
    .draw(env.IMAGES.input(watermark.body).transform({ width: 100 }), { bottom: 10, right: 10, opacity: 0.75 })
    .output({ format: "image/avif" })
).response();
```

### Get Image Info

```ts
const info = await env.IMAGES.info(stream);
// { format, fileSize, width, height }
```

## Recipes

### Responsive Images with srcset

```html
<img srcset="/cdn-cgi/image/width=320/photo.jpg 320w, /cdn-cgi/image/width=640/photo.jpg 640w, /cdn-cgi/image/width=1280/photo.jpg 1280w" sizes="(max-width: 640px) 100vw, 640px" src="/cdn-cgi/image/width=640/photo.jpg" alt="Responsive image" />
```

### Face-Aware Cropping

```js
fetch(imageURL, {
  cf: {
    image: {
      width: 200,
      height: 200,
      fit: "cover",
      gravity: "face",
      zoom: 0.5, // 0 = more background, 1 = tight crop
    },
  },
});
```

### Direct Creator Upload

```bash
# Get one-time upload URL
curl --request POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v2/direct_upload \
  --header "Authorization: Bearer <API_TOKEN>"

# Response: { "uploadURL": "https://upload.imagedelivery.net/..." }
```

### Upload from Worker

```ts
const image = await fetch("https://example.com/image.png");
const bytes = await image.bytes();

const formData = new FormData();
formData.append("file", new File([bytes], "image.png"));

await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/images/v1`, {
  method: "POST",
  headers: { Authorization: `Bearer ${TOKEN}` },
  body: formData,
});
```

## Critical Prohibitions

1. **NEVER** set up Image Resizing Worker for entire zone (`/*`) — blocks non-image requests
2. **NEVER** activate Polish and image transformations simultaneously — redundant compression
3. **NEVER** use flexible variants with signed URL tokens — incompatible
4. **NEVER** use custom ID paths with `requireSignedURLs=true` — not supported
5. **NEVER** expect SVG resizing — SVGs are passed through as-is
6. **NEVER** include resizing options in `cacheKey` — fragments cache

## Troubleshooting

### No `Cf-Resized` Header

- Transformations not enabled on zone
- Another Worker intercepting request
- Using dashboard preview (doesn't simulate transforms)

### Common Error Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 9401 | Invalid transformation options         |
| 9402 | Image too large                        |
| 9403 | Request loop detected                  |
| 9422 | Free tier limit exceeded (5,000/month) |
| 9520 | Unsupported format                     |

## Related Skills

- `cloudflare-workers` - For serverless compute
- `cloudflare-pages` - For full-stack apps
- `cloudflare-r2` - R2 object storage
