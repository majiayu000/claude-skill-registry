---
name: s3-file-storage
description: AWS S3 (and compatible) file storage patterns. Use when implementing file uploads, image storage, document management, CDN delivery, or any cloud file storage.
---

# S3 File Storage Patterns

## Setup (boto3 + Python)
```python
# storage.py
import boto3
from botocore.exceptions import ClientError
import uuid, mimetypes

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    # For S3-compatible services (Cloudflare R2, MinIO):
    # endpoint_url=settings.S3_ENDPOINT_URL,
)
BUCKET = settings.S3_BUCKET
CDN_URL = settings.CDN_URL  # e.g. "https://cdn.example.com"
```

## Upload Patterns

### Direct upload from server
```python
async def upload_file(file: UploadFile, folder: str = "uploads") -> str:
    """Upload file, return public URL."""
    # Validate
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise ValueError(f"File too large (max {MAX_SIZE // 1024 // 1024}MB)")
    if file.content_type not in ALLOWED_TYPES:
        raise ValueError(f"File type not allowed: {file.content_type}")

    # Generate unique key
    ext = mimetypes.guess_extension(file.content_type) or ".bin"
    key = f"{folder}/{uuid.uuid4()}{ext}"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=content,
        ContentType=file.content_type,
        CacheControl="max-age=31536000",  # 1 year cache for immutable files
    )

    return f"{CDN_URL}/{key}"
```

### Presigned URL (client uploads directly — no server bottleneck)
```python
def generate_upload_url(filename: str, content_type: str, folder: str = "uploads") -> dict:
    """Client uploads directly to S3 — bypasses your server entirely."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    key = f"{folder}/{uuid.uuid4()}.{ext}"

    url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET,
            "Key": key,
            "ContentType": content_type,
            "ContentLength": 5 * 1024 * 1024,  # Max 5MB
        },
        ExpiresIn=300,  # URL valid for 5 minutes
    )
    return {
        "upload_url": url,
        "key": key,
        "public_url": f"{CDN_URL}/{key}",
    }

# FastAPI endpoint
@router.post("/upload-url")
async def get_upload_url(
    filename: str = Query(...),
    content_type: str = Query(...),
    user: User = Depends(get_current_user),
):
    return generate_upload_url(filename, content_type, folder=f"users/{user.id}")
```

### Client-side direct upload
```typescript
async function uploadFile(file: File): Promise<string> {
  // 1. Get presigned URL from your API
  const { upload_url, public_url } = await fetch('/api/upload-url?' + new URLSearchParams({
    filename: file.name,
    content_type: file.type,
  })).then(r => r.json())

  // 2. Upload directly to S3 (no server in the middle)
  await fetch(upload_url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': file.type },
  })

  return public_url
}
```

## Delete
```python
async def delete_file(key: str):
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
    except ClientError as e:
        logger.error(f"S3 delete failed for {key}: {e}")

def extract_key_from_url(url: str) -> str:
    """Extract S3 key from CDN URL."""
    return url.replace(f"{CDN_URL}/", "")
```

## Image Resizing (on upload)
```python
from PIL import Image
import io

def resize_image(content: bytes, max_size: tuple[int, int] = (1920, 1080)) -> bytes:
    img = Image.open(io.BytesIO(content))
    img.thumbnail(max_size, Image.LANCZOS)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    output = io.BytesIO()
    img.save(output, format="JPEG", optimize=True, quality=85)
    return output.getvalue()
```

## Bucket Policy (public read for CDN)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicRead",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::your-bucket/*"
  }]
}
```

## Rules
- NEVER store files on local disk in production (not portable, not scalable)
- Validate file type server-side (don't trust Content-Type from client)
- Validate file size before uploading (not after reading all bytes into RAM)
- Use presigned URLs for large files (avoids server memory/bandwidth)
- Generate unique keys (UUID) — never use original filenames (path traversal risk)
- Set CacheControl headers for immutable files (images don't change after upload)
- Delete from S3 when deleting the record in DB (no orphaned files)
- Use lifecycle rules to auto-delete tmp/ folder after 24h
