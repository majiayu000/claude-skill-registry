---
name: cloudinary
description: Manages images and videos with Cloudinary including upload, transformation, and CDN delivery. Use when building media-rich applications requiring resize, crop, format conversion, and optimization.
---

# Cloudinary

Image and video management platform with upload, transformation, optimization, and global CDN delivery.

## Quick Start

```bash
npm install cloudinary
```

### Configuration

```javascript
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
  secure: true
});
```

## Upload

### Basic Upload

```javascript
// From local file
const result = await cloudinary.uploader.upload('./image.jpg', {
  public_id: 'my-image',  // Optional custom ID
  folder: 'products',     // Optional folder
});

console.log(result.secure_url);
// https://res.cloudinary.com/cloud/image/upload/v1234/products/my-image.jpg

// From URL
const result = await cloudinary.uploader.upload(
  'https://example.com/image.jpg',
  { folder: 'external' }
);

// From base64
const result = await cloudinary.uploader.upload(
  'data:image/png;base64,iVBORw0KGgo...',
  { folder: 'uploads' }
);
```

### Upload Options

```javascript
const result = await cloudinary.uploader.upload('./image.jpg', {
  public_id: 'my-image',
  folder: 'products',

  // Transformations on upload
  transformation: [
    { width: 1000, height: 1000, crop: 'limit' },
    { quality: 'auto', fetch_format: 'auto' }
  ],

  // Eager transformations (pre-generate)
  eager: [
    { width: 200, height: 200, crop: 'thumb', gravity: 'face' },
    { width: 800, crop: 'scale' }
  ],

  // Tags for organization
  tags: ['product', 'shoes'],

  // Metadata
  context: 'caption=Nike Shoes|alt=Running shoes',

  // Overwrite existing
  overwrite: true,
  invalidate: true,

  // Resource type
  resource_type: 'image',  // 'image', 'video', 'raw', 'auto'

  // Access control
  type: 'upload',  // 'upload', 'private', 'authenticated'
});
```

### Upload Large Files

```javascript
// For files > 100MB
const result = await cloudinary.uploader.upload_large('./large-video.mp4', {
  resource_type: 'video',
  chunk_size: 6000000,  // 6MB chunks
});
```

## URL Transformations

Build URLs with on-the-fly transformations.

```javascript
// Using cloudinary.url()
const url = cloudinary.url('products/my-image', {
  width: 400,
  height: 300,
  crop: 'fill',
  gravity: 'auto',
  quality: 'auto',
  fetch_format: 'auto',
});
// https://res.cloudinary.com/cloud/image/upload/w_400,h_300,c_fill,g_auto,q_auto,f_auto/products/my-image

// Manual URL construction
const baseUrl = `https://res.cloudinary.com/${cloudName}/image/upload`;
const transformations = 'w_400,h_300,c_fill,g_auto,q_auto,f_auto';
const publicId = 'products/my-image';
const url = `${baseUrl}/${transformations}/${publicId}`;
```

## Transformation Parameters

### Resize & Crop

```javascript
{
  width: 400,
  height: 300,
  crop: 'fill',      // fill, fit, scale, thumb, crop, pad
  gravity: 'auto',   // auto, face, center, north, south, east, west
  aspect_ratio: '16:9',
}
```

### Crop Modes

| Mode | Description |
|------|-------------|
| `fill` | Fill dimensions, crop excess |
| `fit` | Fit within dimensions, maintain ratio |
| `scale` | Scale to dimensions (may distort) |
| `thumb` | Thumbnail with smart crop |
| `crop` | Crop from specified area |
| `pad` | Add padding to fit dimensions |
| `limit` | Like fit, but never upscale |

### Quality & Format

```javascript
{
  quality: 'auto',        // auto, auto:low, auto:good, auto:best, 1-100
  fetch_format: 'auto',   // auto, webp, avif, jpg, png
}
```

### Effects

```javascript
{
  effect: 'blur:500',
  effect: 'grayscale',
  effect: 'sepia',
  effect: 'brightness:30',
  effect: 'contrast:50',
  effect: 'saturation:70',
  effect: 'sharpen',
  effect: 'vignette',
  effect: 'art:athena',  // Artistic filters
}
```

### Face Detection

```javascript
{
  crop: 'thumb',
  gravity: 'face',       // Center on face
  width: 200,
  height: 200,
}

// Multiple faces
{
  crop: 'thumb',
  gravity: 'faces',
  width: 400,
  height: 300,
}
```

### Overlays

```javascript
// Text overlay
{
  overlay: {
    font_family: 'Arial',
    font_size: 40,
    text: 'Hello World'
  },
  gravity: 'south',
  y: 20,
  color: 'white',
}

// Image overlay (watermark)
{
  overlay: 'logo',
  gravity: 'south_east',
  x: 10,
  y: 10,
  width: 100,
  opacity: 50,
}
```

### Chained Transformations

```javascript
const url = cloudinary.url('products/shoe', {
  transformation: [
    // First: resize
    { width: 800, height: 600, crop: 'fill' },
    // Then: apply effect
    { effect: 'improve' },
    // Finally: optimize
    { quality: 'auto', fetch_format: 'auto' }
  ]
});
```

## React SDK

```bash
npm install @cloudinary/react @cloudinary/url-gen
```

```jsx
import { Cloudinary } from '@cloudinary/url-gen';
import { AdvancedImage } from '@cloudinary/react';
import { fill } from '@cloudinary/url-gen/actions/resize';
import { autoGravity } from '@cloudinary/url-gen/qualifiers/gravity';
import { format, quality } from '@cloudinary/url-gen/actions/delivery';
import { auto } from '@cloudinary/url-gen/qualifiers/format';

// Configure
const cld = new Cloudinary({
  cloud: { cloudName: 'your-cloud-name' }
});

function ProductImage({ publicId }) {
  const image = cld
    .image(publicId)
    .resize(fill().width(400).height(300).gravity(autoGravity()))
    .delivery(format(auto()))
    .delivery(quality('auto'));

  return <AdvancedImage cldImg={image} />;
}
```

### With Placeholder & Lazy Loading

```jsx
import { AdvancedImage, lazyload, placeholder } from '@cloudinary/react';

<AdvancedImage
  cldImg={myImage}
  plugins={[
    lazyload(),
    placeholder({ mode: 'blur' })  // blur, pixelate, vectorize
  ]}
/>
```

## Next.js Integration

### With next/image

```jsx
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
      },
    ],
  },
};
```

```jsx
import Image from 'next/image';

function CloudinaryImage({ publicId, width, height }) {
  const cloudName = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME;

  const src = `https://res.cloudinary.com/${cloudName}/image/upload/c_fill,w_${width},h_${height},q_auto,f_auto/${publicId}`;

  return (
    <Image
      src={src}
      alt=""
      width={width}
      height={height}
    />
  );
}
```

### next-cloudinary Package

```bash
npm install next-cloudinary
```

```jsx
import { CldImage, CldUploadWidget } from 'next-cloudinary';

// Display image
<CldImage
  src="products/shoe"
  width="400"
  height="300"
  crop="fill"
  gravity="auto"
  alt="Product"
/>

// Upload widget
<CldUploadWidget
  uploadPreset="my_preset"
  onUpload={(result) => {
    console.log(result.info.secure_url);
  }}
>
  {({ open }) => (
    <button onClick={() => open()}>Upload</button>
  )}
</CldUploadWidget>
```

## Video Transformations

```javascript
// Video URL
const videoUrl = cloudinary.url('videos/sample', {
  resource_type: 'video',
  width: 640,
  height: 360,
  crop: 'fill',
  quality: 'auto',
  format: 'mp4',
});

// Thumbnail from video
const thumbnail = cloudinary.url('videos/sample', {
  resource_type: 'video',
  format: 'jpg',
  start_offset: '5',  // 5 seconds in
  width: 400,
  crop: 'fill',
});

// Animated GIF from video
const gif = cloudinary.url('videos/sample', {
  resource_type: 'video',
  format: 'gif',
  start_offset: '2',
  end_offset: '5',
  width: 300,
});
```

## Admin API

```javascript
// List resources
const resources = await cloudinary.api.resources({
  type: 'upload',
  prefix: 'products/',
  max_results: 100,
});

// Get resource details
const resource = await cloudinary.api.resource('products/shoe');

// Delete resource
await cloudinary.uploader.destroy('products/old-shoe');

// Rename resource
await cloudinary.uploader.rename('old-name', 'new-name');

// Create folder
await cloudinary.api.create_folder('new-folder');
```

## Upload Presets

Configure in Cloudinary dashboard for unsigned uploads.

```javascript
// Unsigned upload (client-side)
const formData = new FormData();
formData.append('file', file);
formData.append('upload_preset', 'my_preset');

const response = await fetch(
  `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
  { method: 'POST', body: formData }
);

const data = await response.json();
console.log(data.secure_url);
```

## Signed Uploads (Secure)

```javascript
// Server: Generate signature
const timestamp = Math.round(new Date().getTime() / 1000);
const signature = cloudinary.utils.api_sign_request(
  { timestamp, folder: 'uploads' },
  apiSecret
);

// Client: Upload with signature
const formData = new FormData();
formData.append('file', file);
formData.append('api_key', apiKey);
formData.append('timestamp', timestamp);
formData.append('signature', signature);
formData.append('folder', 'uploads');

await fetch(
  `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
  { method: 'POST', body: formData }
);
```

## Best Practices

1. **Use auto format and quality** - `f_auto,q_auto` for best optimization
2. **Generate eager transformations** - Pre-generate common sizes
3. **Use responsive images** - Serve appropriately sized images
4. **Enable lazy loading** - With blur placeholder
5. **Use upload presets** - For consistent upload settings
6. **Tag and organize** - Use folders and tags for management
