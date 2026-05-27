---
name: cloudinary
slug: cloudinary-integration
version: 1.0.0
category: integration
description: Cloudinary media management with image upload, transformation, and optimization
triggers:
  - pattern: "cloudinary|image|upload|media|transform|optimize"
    confidence: 0.8
    examples:
      - "upload images with Cloudinary"
      - "add image upload functionality"
      - "optimize images"
      - "transform uploaded images"
      - "setup media management"
mcp_dependencies:
  - server: cloudinary
    required: false
    capabilities:
      - "upload"
      - "transform"
      - "optimize"
---

# Cloudinary Integration Skill

Complete Cloudinary media management template with image upload, transformations, and React components for seamless media handling.

## Overview

This template includes:
- **Cloudinary Client Setup** - SDK configuration and utilities
- **React Upload Hook** - useImageUpload with progress tracking
- **Upload Component** - Drag-and-drop image upload
- **Image Transformations** - Resize, crop, optimize on-the-fly
- **Type Safety** - Full TypeScript support

## When to Use This Template

Use this template when you need:
- Image upload functionality
- Avatar/profile picture uploads
- Product image galleries
- Automatic image optimization
- Image transformations and filters
- Video upload and processing
- Media library management

## What's Included

### Code Files

- `code/client.ts` - Cloudinary SDK setup and utilities
- `code/hooks.ts` - React hooks for upload with progress
- `code/components/image-upload.tsx` - Upload UI component

### Configuration

- `mcp/config.json` - MCP server configuration
- `env/.env.template` - Required environment variables

### Documentation

- `docs/README.md` - Complete setup and usage guide

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install cloudinary next-cloudinary
   ```

2. **Configure Environment Variables**
   ```bash
   cp templates/cloudinary/env/.env.template .env.local
   # Add your Cloudinary credentials
   ```

3. **Copy Template Files**
   ```bash
   npx tsx scripts/load-template.ts cloudinary
   ```

4. **Setup Upload Preset**
   - Go to Cloudinary Dashboard
   - Settings → Upload
   - Create unsigned upload preset

## Key Features

### 1. Image Upload

```typescript
import { uploadImage } from '@/lib/cloudinary/client'

const result = await uploadImage({
  file: imageFile,
  folder: 'avatars',
})

console.log('Image URL:', result.secure_url)
```

### 2. Image Transformations

```typescript
import { getOptimizedImageUrl } from '@/lib/cloudinary/client'

const url = getOptimizedImageUrl('my-image.jpg', {
  width: 400,
  height: 400,
  crop: 'fill',
  quality: 'auto',
  format: 'auto',
})
```

### 3. React Upload Hook

```tsx
import { useImageUpload } from '@/lib/cloudinary/hooks'

function MyComponent() {
  const { upload, progress, isUploading, imageUrl } = useImageUpload()

  const handleUpload = async (file: File) => {
    const result = await upload(file)
    console.log('Uploaded:', result.url)
  }

  return (
    <div>
      <input
        type="file"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        disabled={isUploading}
      />
      {isUploading && <p>Upload progress: {progress}%</p>}
      {imageUrl && <img src={imageUrl} alt="Uploaded" />}
    </div>
  )
}
```

### 4. Upload Component

```tsx
import { ImageUpload } from '@/lib/cloudinary/components/image-upload'

function ProfilePage() {
  const handleUploadComplete = (url: string) => {
    console.log('Image uploaded:', url)
    // Save URL to database
  }

  return (
    <ImageUpload
      folder="profiles"
      onUploadComplete={handleUploadComplete}
      maxSizeMB={5}
    />
  )
}
```

## Image Transformations

### Resize and Crop

```typescript
// Resize to 300x300, crop to fill
getOptimizedImageUrl('image.jpg', {
  width: 300,
  height: 300,
  crop: 'fill',
})

// Resize width, maintain aspect ratio
getOptimizedImageUrl('image.jpg', {
  width: 800,
  crop: 'scale',
})
```

### Quality and Format

```typescript
// Auto quality and format (WebP when supported)
getOptimizedImageUrl('image.jpg', {
  quality: 'auto',
  format: 'auto',
})

// Specific quality
getOptimizedImageUrl('image.jpg', {
  quality: 80,
  format: 'jpg',
})
```

### Filters and Effects

```typescript
// Apply filters
getOptimizedImageUrl('image.jpg', {
  effects: ['grayscale', 'blur:300'],
  quality: 'auto',
})
```

## Security Best Practices

- Use signed uploads for sensitive content
- Implement upload presets
- Validate file types and sizes
- Set proper folder permissions
- Use transformation parameters safely

## Resources

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Cloudinary Dashboard](https://cloudinary.com/console)
- [Transformation Reference](https://cloudinary.com/documentation/image_transformations)

---

**Template Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
