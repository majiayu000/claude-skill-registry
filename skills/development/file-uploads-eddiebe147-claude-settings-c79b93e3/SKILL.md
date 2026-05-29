---
name: file-uploads
description: Expert guide for handling file uploads, image optimization, cloud storage (Supabase, S3, Cloudinary), and file management. Use when implementing file upload features or managing user assets.
---

# File Uploads Skill

## Overview

This skill helps you implement secure, efficient file uploads in your Next.js application. From basic file handling to cloud storage integration, this covers everything you need for robust file management.

## File Upload Basics

### HTML File Input
```typescript
'use client'
import { useState } from 'react'

export function FileUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      console.log('Uploaded:', data.url)
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <input
        type="file"
        onChange={handleFileChange}
        accept="image/*"
      />
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
    </div>
  )
}
```

### Drag and Drop
```typescript
'use client'
import { useState, useCallback } from 'react'

export function DragDropUpload() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      setFile(files[0])
    }
  }, [])

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragOver={(e) => e.preventDefault()}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        border-2 border-dashed rounded-lg p-8 text-center
        ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
      `}
    >
      {file ? (
        <p>{file.name}</p>
      ) : (
        <p>Drag and drop a file here, or click to select</p>
      )}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="hidden"
      />
    </div>
  )
}
```

## Supabase Storage

### Upload to Supabase
```typescript
// lib/supabase/storage.ts
import { createClient } from '@/lib/supabase/client'

export async function uploadFile(
  file: File,
  bucket: string = 'avatars',
  path?: string
): Promise<{ url: string | null; error: any }> {
  const supabase = createClient()

  // Generate unique filename
  const fileExt = file.name.split('.').pop()
  const fileName = path || `${Math.random()}.${fileExt}`
  const filePath = `${fileName}`

  // Upload file
  const { error: uploadError } = await supabase.storage
    .from(bucket)
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false,
    })

  if (uploadError) {
    return { url: null, error: uploadError }
  }

  // Get public URL
  const { data } = supabase.storage.from(bucket).getPublicUrl(filePath)

  return { url: data.publicUrl, error: null }
}

// Usage in component
const handleUpload = async (file: File) => {
  const { url, error } = await uploadFile(file, 'avatars')

  if (error) {
    console.error('Upload failed:', error)
    return
  }

  console.log('File uploaded:', url)
}
```

### Upload with Progress
```typescript
'use client'
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function UploadWithProgress() {
  const [progress, setProgress] = useState(0)
  const supabase = createClient()

  const handleUpload = async (file: File) => {
    const fileExt = file.name.split('.').pop()
    const fileName = `${Math.random()}.${fileExt}`

    // Create upload with progress tracking
    const { error } = await supabase.storage
      .from('files')
      .upload(fileName, file, {
        cacheControl: '3600',
        onUploadProgress: (progress) => {
          const percent = (progress.loaded / progress.total) * 100
          setProgress(Math.round(percent))
        },
      })

    if (error) {
      console.error('Upload failed:', error)
      return
    }

    setProgress(100)
  }

  return (
    <div>
      <input type="file" onChange={(e) => handleUpload(e.target.files![0])} />
      {progress > 0 && (
        <div className="w-full bg-gray-200 rounded">
          <div
            className="bg-blue-600 h-2 rounded"
            style={{ width: `${progress}%` }}
          />
          <p>{progress}%</p>
        </div>
      )}
    </div>
  )
}
```

### Private Files (RLS)
```sql
-- Enable RLS on storage bucket
CREATE POLICY "Users can upload their own files"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'private-files'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

CREATE POLICY "Users can read their own files"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'private-files'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

```typescript
// Upload to user's folder
const userId = user.id
const filePath = `${userId}/${file.name}`

await supabase.storage.from('private-files').upload(filePath, file)

// Get signed URL (expires in 1 hour)
const { data } = await supabase.storage
  .from('private-files')
  .createSignedUrl(filePath, 3600)
```

## Image Optimization

### Client-Side Image Compression
```bash
npm install browser-image-compression
```

```typescript
'use client'
import imageCompression from 'browser-image-compression'

export async function compressImage(file: File): Promise<File> {
  const options = {
    maxSizeMB: 1,
    maxWidthOrHeight: 1920,
    useWebWorker: true,
  }

  try {
    const compressedFile = await imageCompression(file, options)
    return compressedFile
  } catch (error) {
    console.error('Compression failed:', error)
    return file
  }
}

// Usage
const handleUpload = async (file: File) => {
  const compressed = await compressImage(file)
  await uploadFile(compressed)
}
```

### Server-Side Image Processing (Sharp)
```bash
npm install sharp
```

```typescript
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server'
import sharp from 'sharp'

export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = formData.get('file') as File

  if (!file) {
    return NextResponse.json({ error: 'No file provided' }, { status: 400 })
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // Process image
  const processed = await sharp(buffer)
    .resize(1200, 1200, { fit: 'inside', withoutEnlargement: true })
    .jpeg({ quality: 85 })
    .toBuffer()

  // Upload processed image
  // ... upload to Supabase/S3

  return NextResponse.json({ success: true })
}
```

### Generate Thumbnails
```typescript
import sharp from 'sharp'

export async function generateThumbnail(
  buffer: Buffer,
  width: number = 300
): Promise<Buffer> {
  return await sharp(buffer)
    .resize(width, width, {
      fit: 'cover',
      position: 'center',
    })
    .jpeg({ quality: 80 })
    .toBuffer()
}

// Usage
const handleUpload = async (file: File) => {
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // Generate multiple sizes
  const [original, thumbnail, medium] = await Promise.all([
    uploadBuffer(buffer, 'original'),
    uploadBuffer(await generateThumbnail(buffer, 300), 'thumb'),
    uploadBuffer(await generateThumbnail(buffer, 800), 'medium'),
  ])

  return { original, thumbnail, medium }
}
```

## Cloudinary Integration

### Setup
```bash
npm install cloudinary
```

```typescript
// lib/cloudinary.ts
import { v2 as cloudinary } from 'cloudinary'

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
})

export async function uploadToCloudinary(
  file: File,
  folder: string = 'uploads'
): Promise<string> {
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  return new Promise((resolve, reject) => {
    cloudinary.uploader
      .upload_stream(
        {
          folder,
          resource_type: 'auto',
        },
        (error, result) => {
          if (error) reject(error)
          else resolve(result!.secure_url)
        }
      )
      .end(buffer)
  })
}
```

### Image Transformations
```typescript
import { getCldImageUrl } from 'next-cloudinary'

// Generate transformed URL
const url = getCldImageUrl({
  src: 'sample',
  width: 800,
  height: 600,
  crop: 'fill',
  gravity: 'face',
  format: 'webp',
  quality: 'auto',
})
```

## AWS S3 Integration

### Setup
```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

```typescript
// lib/s3.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

const s3Client = new S3Client({
  region: process.env.AWS_REGION!,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

export async function uploadToS3(
  file: File,
  key: string
): Promise<string> {
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  const command = new PutObjectCommand({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: key,
    Body: buffer,
    ContentType: file.type,
  })

  await s3Client.send(command)

  return `https://${process.env.AWS_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`
}
```

### Presigned URLs (Direct Upload)
```typescript
import { PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

export async function getUploadUrl(fileName: string): Promise<string> {
  const key = `uploads/${Date.now()}-${fileName}`

  const command = new PutObjectCommand({
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: key,
  })

  const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 })
  return url
}

// Client-side direct upload
const handleUpload = async (file: File) => {
  // Get presigned URL from backend
  const { url } = await fetch('/api/upload/get-url', {
    method: 'POST',
    body: JSON.stringify({ fileName: file.name }),
  }).then((r) => r.json())

  // Upload directly to S3
  await fetch(url, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': file.type,
    },
  })
}
```

## File Validation

### Validate File Type
```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_SIZE = 5 * 1024 * 1024 // 5MB

export function validateFile(file: File): { valid: boolean; error?: string } {
  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: 'Invalid file type. Only JPEG, PNG, and WebP are allowed.',
    }
  }

  if (file.size > MAX_SIZE) {
    return {
      valid: false,
      error: 'File too large. Maximum size is 5MB.',
    }
  }

  return { valid: true }
}

// Usage
const handleFileSelect = (file: File) => {
  const validation = validateFile(file)

  if (!validation.valid) {
    alert(validation.error)
    return
  }

  // Proceed with upload
  uploadFile(file)
}
```

### Server-Side Validation
```typescript
// app/api/upload/route.ts
export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = formData.get('file') as File

  // Validate file type by magic bytes (more secure than extension)
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  const isJPEG = buffer[0] === 0xff && buffer[1] === 0xd8
  const isPNG = buffer[0] === 0x89 && buffer[1] === 0x50

  if (!isJPEG && !isPNG) {
    return NextResponse.json(
      { error: 'Invalid file type' },
      { status: 400 }
    )
  }

  // Proceed with upload
}
```

## Multiple File Uploads

### Upload Multiple Files
```typescript
'use client'
import { useState } from 'react'

export function MultipleFileUpload() {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)

  const handleFilesSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const handleUploadAll = async () => {
    setUploading(true)

    try {
      const uploadPromises = files.map((file) => uploadFile(file))
      const results = await Promise.all(uploadPromises)
      console.log('All files uploaded:', results)
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <input
        type="file"
        multiple
        onChange={handleFilesSelect}
        accept="image/*"
      />
      <p>{files.length} files selected</p>
      <button onClick={handleUploadAll} disabled={!files.length || uploading}>
        {uploading ? 'Uploading...' : 'Upload All'}
      </button>
    </div>
  )
}
```

## Resumable Uploads (Large Files)

### Chunked Upload
```typescript
const CHUNK_SIZE = 1024 * 1024 // 1MB chunks

export async function uploadLargeFile(file: File) {
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE)
  const uploadId = crypto.randomUUID()

  for (let i = 0; i < totalChunks; i++) {
    const start = i * CHUNK_SIZE
    const end = Math.min(start + CHUNK_SIZE, file.size)
    const chunk = file.slice(start, end)

    const formData = new FormData()
    formData.append('chunk', chunk)
    formData.append('uploadId', uploadId)
    formData.append('chunkIndex', i.toString())
    formData.append('totalChunks', totalChunks.toString())

    await fetch('/api/upload/chunk', {
      method: 'POST',
      body: formData,
    })

    console.log(`Uploaded chunk ${i + 1}/${totalChunks}`)
  }

  // Finalize upload
  await fetch('/api/upload/finalize', {
    method: 'POST',
    body: JSON.stringify({ uploadId, fileName: file.name }),
  })
}
```

## File Management

### List Files
```typescript
const { data, error } = await supabase.storage.from('avatars').list('', {
  limit: 100,
  offset: 0,
  sortBy: { column: 'created_at', order: 'desc' },
})
```

### Delete Files
```typescript
const { error } = await supabase.storage
  .from('avatars')
  .remove(['file1.jpg', 'file2.jpg'])
```

### Move/Rename Files
```typescript
const { error } = await supabase.storage
  .from('avatars')
  .move('old-name.jpg', 'new-name.jpg')
```

## Best Practices Checklist

- [ ] Validate file types (client and server)
- [ ] Enforce file size limits
- [ ] Compress images before upload
- [ ] Generate thumbnails for images
- [ ] Use unique file names (avoid collisions)
- [ ] Implement upload progress indicators
- [ ] Handle upload errors gracefully
- [ ] Use presigned URLs for direct uploads
- [ ] Implement RLS for private files
- [ ] Clean up failed uploads
- [ ] Use CDN for file delivery
- [ ] Optimize images automatically
- [ ] Scan files for malware (if needed)
- [ ] Implement rate limiting on uploads

## When to Use This Skill

Invoke this skill when:
- Implementing file upload functionality
- Integrating cloud storage (Supabase/S3/Cloudinary)
- Optimizing image uploads
- Creating avatar upload systems
- Building file management features
- Implementing drag-and-drop uploads
- Handling large file uploads
- Creating thumbnail generation
- Debugging upload issues
- Setting up file validation
