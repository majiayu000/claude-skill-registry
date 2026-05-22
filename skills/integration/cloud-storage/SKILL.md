---
name: cloud-storage
description: Cloud storage integration with signed URLs, visibility control, multi-tenant path conventions, and presigned uploads for direct client uploads.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: infrastructure
  time: 4h
  source: drift-masterguide
---

# Cloud Storage

Cloud storage integration with signed URLs and multi-tenant isolation.

## When to Use This Skill

- Storing user-uploaded files
- Serving private assets with expiring URLs
- Multi-tenant file isolation
- Direct client uploads (presigned URLs)

## Core Concepts

Key patterns for cloud storage:

1. **Multi-tenant paths** - Isolate files by user/tenant
2. **Signed URLs** - Time-limited access to private files
3. **Visibility control** - Public vs private buckets
4. **Presigned uploads** - Direct client-to-storage uploads

## Implementation

### Python

```python
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import uuid4
import hashlib
import os

from supabase import create_client, Client


@dataclass
class StorageConfig:
    supabase_url: str
    supabase_key: str
    bucket_name: str = "assets"
    public_bucket_name: str = "public-assets"
    signed_url_expiration: int = 3600  # seconds
    max_file_size: int = 10485760  # 10MB
    allowed_mime_types: tuple = (
        "image/png", "image/jpeg", "image/webp", "image/gif"
    )
    
    @classmethod
    def from_env(cls) -> "StorageConfig":
        return cls(
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_key=os.environ["SUPABASE_SERVICE_KEY"],
        )


@dataclass
class UploadResult:
    path: str
    url: str
    file_size: int
    content_type: str
    checksum: str


@dataclass
class PresignedUpload:
    upload_url: str
    path: str
    expires_at: datetime


class StorageService:
    """Cloud storage service with multi-tenant isolation."""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.client: Client = create_client(config.supabase_url, config.supabase_key)
    
    def _generate_path(
        self, user_id: str, job_id: str, content_type: str, suffix: str = ""
    ) -> str:
        """Generate storage path with multi-tenant isolation."""
        ext_map = {
            "image/png": "png",
            "image/jpeg": "jpg",
            "image/webp": "webp",
            "image/gif": "gif",
        }
        ext = ext_map.get(content_type, "bin")
        filename = f"{uuid4()}{suffix}.{ext}"
        return f"{user_id}/{job_id}/{filename}"
    
    async def upload_asset(
        self,
        user_id: str,
        job_id: str,
        data: bytes,
        content_type: str,
        suffix: str = "",
        is_public: bool = False,
    ) -> UploadResult:
        """Upload an asset to storage."""
        if content_type not in self.config.allowed_mime_types:
            raise ValueError(f"Invalid content type: {content_type}")
        
        if len(data) > self.config.max_file_size:
            raise ValueError(f"File too large: {len(data)} bytes")
        
        path = self._generate_path(user_id, job_id, content_type, suffix)
        checksum = hashlib.sha256(data).hexdigest()
        
        bucket = self.config.public_bucket_name if is_public else self.config.bucket_name
        
        self.client.storage.from_(bucket).upload(
            path=path,
            file=data,
            file_options={
                "content-type": content_type,
                "cache-control": "public, max-age=31536000",
            },
        )
        
        if is_public:
            url = self._get_public_url(bucket, path)
        else:
            url = await self.get_signed_url(path)
        
        return UploadResult(
            path=path,
            url=url,
            file_size=len(data),
            content_type=content_type,
            checksum=checksum,
        )
    
    async def get_signed_url(self, path: str, expiration: int = None) -> str:
        """Generate a signed URL for private asset access."""
        exp = expiration or self.config.signed_url_expiration
        result = self.client.storage.from_(self.config.bucket_name).create_signed_url(
            path=path, expires_in=exp
        )
        return result["signedURL"]
    
    async def get_signed_urls_batch(self, paths: list, expiration: int = None) -> dict:
        """Generate signed URLs for multiple assets."""
        exp = expiration or self.config.signed_url_expiration
        result = self.client.storage.from_(self.config.bucket_name).create_signed_urls(
            paths=paths, expires_in=exp
        )
        return {item["path"]: item["signedURL"] for item in result}
    
    def _get_public_url(self, bucket: str, path: str) -> str:
        return f"{self.config.supabase_url}/storage/v1/object/public/{bucket}/{path}"
    
    async def update_visibility(self, path: str, is_public: bool, user_id: str) -> str:
        """Move asset between public and private buckets."""
        if not path.startswith(f"{user_id}/"):
            raise PermissionError("Cannot modify asset owned by another user")
        
        source_bucket = self.config.bucket_name if is_public else self.config.public_bucket_name
        dest_bucket = self.config.public_bucket_name if is_public else self.config.bucket_name
        
        # Download, upload to new bucket, delete from old
        data = self.client.storage.from_(source_bucket).download(path)
        self.client.storage.from_(dest_bucket).upload(path=path, file=data, file_options={"x-upsert": "true"})
        self.client.storage.from_(source_bucket).remove([path])
        
        if is_public:
            return self._get_public_url(dest_bucket, path)
        return await self.get_signed_url(path)
    
    async def delete_asset(self, path: str, user_id: str) -> None:
        """Delete an asset from storage."""
        if not path.startswith(f"{user_id}/"):
            raise PermissionError("Cannot delete asset owned by another user")
        
        try:
            self.client.storage.from_(self.config.bucket_name).remove([path])
        except:
            pass
        try:
            self.client.storage.from_(self.config.public_bucket_name).remove([path])
        except:
            pass
    
    async def create_presigned_upload(
        self, user_id: str, job_id: str, content_type: str, file_size: int
    ) -> PresignedUpload:
        """Create a presigned URL for direct client upload."""
        if content_type not in self.config.allowed_mime_types:
            raise ValueError(f"Invalid content type: {content_type}")
        
        if file_size > self.config.max_file_size:
            raise ValueError(f"File too large: {file_size}")
        
        path = self._generate_path(user_id, job_id, content_type)
        result = self.client.storage.from_(self.config.bucket_name).create_signed_upload_url(path=path)
        
        return PresignedUpload(
            upload_url=result["signedURL"],
            path=path,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        )
```

### TypeScript

```typescript
interface StorageConfig {
  supabaseUrl: string;
  supabaseKey: string;
  bucketName: string;
  publicBucketName: string;
  signedUrlExpiration: number;
  maxFileSize: number;
  allowedMimeTypes: string[];
}

interface UploadResult {
  path: string;
  url: string;
  fileSize: number;
  contentType: string;
  checksum: string;
}

interface PresignedUpload {
  uploadUrl: string;
  path: string;
  expiresAt: Date;
}

class StorageService {
  private client: SupabaseClient;
  private config: StorageConfig;

  constructor(config: StorageConfig) {
    this.config = config;
    this.client = createClient(config.supabaseUrl, config.supabaseKey);
  }

  private generatePath(userId: string, jobId: string, contentType: string, suffix = ''): string {
    const extMap: Record<string, string> = {
      'image/png': 'png',
      'image/jpeg': 'jpg',
      'image/webp': 'webp',
      'image/gif': 'gif',
    };
    const ext = extMap[contentType] || 'bin';
    const filename = `${crypto.randomUUID()}${suffix}.${ext}`;
    return `${userId}/${jobId}/${filename}`;
  }

  async uploadAsset(
    userId: string,
    jobId: string,
    data: Buffer,
    contentType: string,
    options: { suffix?: string; isPublic?: boolean } = {}
  ): Promise<UploadResult> {
    if (!this.config.allowedMimeTypes.includes(contentType)) {
      throw new Error(`Invalid content type: ${contentType}`);
    }

    if (data.length > this.config.maxFileSize) {
      throw new Error(`File too large: ${data.length} bytes`);
    }

    const path = this.generatePath(userId, jobId, contentType, options.suffix || '');
    const checksum = crypto.createHash('sha256').update(data).digest('hex');
    const bucket = options.isPublic ? this.config.publicBucketName : this.config.bucketName;

    await this.client.storage.from(bucket).upload(path, data, {
      contentType,
      cacheControl: 'public, max-age=31536000',
    });

    const url = options.isPublic
      ? this.getPublicUrl(bucket, path)
      : await this.getSignedUrl(path);

    return { path, url, fileSize: data.length, contentType, checksum };
  }

  async getSignedUrl(path: string, expiration?: number): Promise<string> {
    const exp = expiration || this.config.signedUrlExpiration;
    const { data } = await this.client.storage
      .from(this.config.bucketName)
      .createSignedUrl(path, exp);
    return data!.signedUrl;
  }

  async getSignedUrlsBatch(paths: string[], expiration?: number): Promise<Record<string, string>> {
    const exp = expiration || this.config.signedUrlExpiration;
    const { data } = await this.client.storage
      .from(this.config.bucketName)
      .createSignedUrls(paths, exp);
    
    return Object.fromEntries(data!.map(item => [item.path, item.signedUrl]));
  }

  private getPublicUrl(bucket: string, path: string): string {
    return `${this.config.supabaseUrl}/storage/v1/object/public/${bucket}/${path}`;
  }

  async deleteAsset(path: string, userId: string): Promise<void> {
    if (!path.startsWith(`${userId}/`)) {
      throw new Error('Cannot delete asset owned by another user');
    }

    await Promise.allSettled([
      this.client.storage.from(this.config.bucketName).remove([path]),
      this.client.storage.from(this.config.publicBucketName).remove([path]),
    ]);
  }

  async createPresignedUpload(
    userId: string,
    jobId: string,
    contentType: string,
    fileSize: number
  ): Promise<PresignedUpload> {
    if (!this.config.allowedMimeTypes.includes(contentType)) {
      throw new Error(`Invalid content type: ${contentType}`);
    }

    if (fileSize > this.config.maxFileSize) {
      throw new Error(`File too large: ${fileSize}`);
    }

    const path = this.generatePath(userId, jobId, contentType);
    const { data } = await this.client.storage
      .from(this.config.bucketName)
      .createSignedUploadUrl(path);

    return {
      uploadUrl: data!.signedUrl,
      path,
      expiresAt: new Date(Date.now() + 5 * 60 * 1000),
    };
  }
}
```

## Usage Examples

### Upload Through Backend

```python
@router.post("/upload")
async def upload_file(
    file: UploadFile,
    job_id: str,
    current_user: User = Depends(get_current_user),
    storage: StorageService = Depends(get_storage_service),
):
    content = await file.read()
    
    result = await storage.upload_asset(
        user_id=current_user.id,
        job_id=job_id,
        data=content,
        content_type=file.content_type,
    )
    
    return {"path": result.path, "url": result.url}
```

### Direct Client Upload

```python
# Backend: Create presigned URL
@router.post("/presigned-upload")
async def create_presigned(
    content_type: str,
    file_size: int,
    job_id: str,
    current_user: User = Depends(get_current_user),
    storage: StorageService = Depends(get_storage_service),
):
    result = await storage.create_presigned_upload(
        user_id=current_user.id,
        job_id=job_id,
        content_type=content_type,
        file_size=file_size,
    )
    return {"upload_url": result.upload_url, "path": result.path}
```

```typescript
// Client: Upload directly to storage
const { uploadUrl, path } = await api.createPresignedUpload({
  contentType: file.type,
  fileSize: file.size,
  jobId,
});

await fetch(uploadUrl, {
  method: 'PUT',
  body: file,
  headers: { 'Content-Type': file.type },
});
```

### Batch Signed URLs

```python
# Get signed URLs for multiple assets
paths = [asset.storage_path for asset in assets]
urls = await storage.get_signed_urls_batch(paths)

for asset in assets:
    asset.url = urls[asset.storage_path]
```

## Path Conventions

```
{bucket}/
├── {user_id}/
│   ├── {job_id}/
│   │   ├── {uuid}.png           # Generated asset
│   │   ├── {uuid}_112x112.png   # Resized variant
│   │   └── {uuid}_56x56.png     # Another variant
│   └── profile/
│       └── avatar.png           # Profile picture
```

## Best Practices

1. Always prefix paths with user_id for isolation
2. Use UUIDs for filenames to prevent collisions
3. Set cache headers for CDN efficiency
4. Use presigned uploads for large files
5. Batch signed URL generation for lists

## Common Mistakes

- Exposing private bucket URLs directly
- Missing user_id prefix (no isolation)
- Not validating content types
- No file size limits
- Forgetting to clean up failed uploads

## Related Patterns

- file-uploads - Validation and processing
- idempotency - Prevent duplicate uploads
- rate-limiting - Limit upload frequency
