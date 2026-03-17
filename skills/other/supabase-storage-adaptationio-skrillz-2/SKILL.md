---
name: supabase-storage
description: Supabase Storage for file uploads, downloads, buckets, and signed URLs. Use when uploading files, managing storage buckets, generating signed URLs, or handling images.
---

# Supabase Storage Skill

File storage, uploads, downloads, and bucket management.

## Quick Reference

| Task | Method |
|------|--------|
| Upload file | `storage.from('bucket').upload(path, file)` |
| Download file | `storage.from('bucket').download(path)` |
| Get public URL | `storage.from('bucket').getPublicUrl(path)` |
| Get signed URL | `storage.from('bucket').createSignedUrl(path, 3600)` |
| Delete file | `storage.from('bucket').remove([path])` |
| List files | `storage.from('bucket').list(folder)` |
| Move file | `storage.from('bucket').move(from, to)` |
| Copy file | `storage.from('bucket').copy(from, to)` |

## Bucket Configuration

### Public vs Private

- **Public**: Files accessible via URL without authentication
- **Private**: Requires authentication or signed URLs

### Create Bucket (Dashboard)

1. Go to Storage in Dashboard
2. Click "New bucket"
3. Set name and public/private
4. Configure file size limits and allowed MIME types

### Create Bucket (SQL)

```sql
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'avatars',
  'avatars',
  true,
  5242880,  -- 5MB
  ARRAY['image/jpeg', 'image/png', 'image/webp']
);
```

### Create Bucket (config.toml)

```toml
[storage.buckets.avatars]
public = true
file_size_limit = "5MiB"
allowed_mime_types = ["image/png", "image/jpeg", "image/webp"]

[storage.buckets.documents]
public = false
file_size_limit = "50MiB"
allowed_mime_types = ["application/pdf"]
```

## Upload Files

### Basic Upload

```javascript
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('user-123/avatar.png', file)
```

### Upload with Options

```javascript
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('user-123/avatar.png', file, {
    cacheControl: '3600',
    contentType: 'image/png',
    upsert: true  // Replace if exists
  })
```

### Upload from Browser

```javascript
const fileInput = document.querySelector('input[type="file"]')
const file = fileInput.files[0]

const { data, error } = await supabase.storage
  .from('uploads')
  .upload(`${userId}/${file.name}`, file)
```

### Upload Base64

```javascript
const base64Data = 'data:image/png;base64,iVBOR...'
const base64 = base64Data.split(',')[1]
const buffer = Uint8Array.from(atob(base64), c => c.charCodeAt(0))

const { data, error } = await supabase.storage
  .from('images')
  .upload('photo.png', buffer, {
    contentType: 'image/png'
  })
```

## Download Files

### Download as Blob

```javascript
const { data, error } = await supabase.storage
  .from('documents')
  .download('report.pdf')

// data is a Blob
const url = URL.createObjectURL(data)
```

### Download to Browser

```javascript
const { data } = await supabase.storage
  .from('documents')
  .download('report.pdf')

const link = document.createElement('a')
link.href = URL.createObjectURL(data)
link.download = 'report.pdf'
link.click()
```

## Get URLs

### Public URL (Public Buckets)

```javascript
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-123/avatar.png')

console.log(data.publicUrl)
// https://xxx.supabase.co/storage/v1/object/public/avatars/user-123/avatar.png
```

### Signed URL (Private Buckets)

```javascript
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUrl('private/report.pdf', 3600)  // 1 hour

console.log(data.signedUrl)
```

### Multiple Signed URLs

```javascript
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUrls(['doc1.pdf', 'doc2.pdf'], 3600)
```

### Signed Upload URL

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .createSignedUploadUrl('user-123/file.pdf')

// data.signedUrl is valid for 2 hours
// data.token is the upload token
```

## List Files

### List All in Folder

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .list('user-123')

// data: [{ name, id, metadata, ... }]
```

### With Options

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .list('user-123', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' }
  })
```

### Search Files

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .list('user-123', {
    search: 'report'  // Filename contains 'report'
  })
```

## Delete Files

### Single File

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .remove(['user-123/old-file.pdf'])
```

### Multiple Files

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .remove([
    'user-123/file1.pdf',
    'user-123/file2.pdf',
    'user-123/file3.pdf'
  ])
```

## Move & Copy

### Move File

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .move('old-path/file.pdf', 'new-path/file.pdf')
```

### Copy File

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .copy('original/file.pdf', 'backup/file.pdf')
```

## Image Transformations

Available on Pro plan and above.

### Resize

```javascript
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user-123/photo.jpg', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover'  // cover, contain, fill
    }
  })
```

### Quality

```javascript
const { data } = supabase.storage
  .from('images')
  .getPublicUrl('photo.jpg', {
    transform: {
      width: 800,
      quality: 75  // 20-100
    }
  })
```

### Format Conversion

```javascript
const { data } = supabase.storage
  .from('images')
  .getPublicUrl('photo.png', {
    transform: {
      format: 'webp'  // webp, jpeg, png
    }
  })
```

## Storage RLS Policies

### Enable RLS

```sql
-- RLS is enabled by default on storage.objects
```

### Common Policies

```sql
-- Users can view their own files
CREATE POLICY "Users can view own files"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Users can upload to their folder
CREATE POLICY "Users can upload own files"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Users can delete their files
CREATE POLICY "Users can delete own files"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### Public Bucket Policy

```sql
-- Anyone can view public files
CREATE POLICY "Public read"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'public-images');
```

## Error Handling

```javascript
const { data, error } = await supabase.storage
  .from('uploads')
  .upload('file.pdf', file)

if (error) {
  if (error.message === 'The resource already exists') {
    console.log('File already exists')
  } else if (error.message.includes('exceeded')) {
    console.log('File too large')
  } else if (error.message.includes('mime type')) {
    console.log('Invalid file type')
  } else {
    console.error('Upload error:', error.message)
  }
}
```

## Size Limits

| Plan | Max File Size |
|------|--------------|
| Free | 50 MB |
| Pro+ | 500 GB |

## References

- [storage-policies.md](references/storage-policies.md) - RLS policy patterns
- [upload-patterns.md](references/upload-patterns.md) - Upload best practices
