---
name: file-storage-patterns
description: Implement file upload, storage, and delivery with S3, CDN, and image processing pipelines
---

# File Storage Patterns

## Decision Table

| Approach | Access Pattern | Cost | Latency | Best For |
|----------|---------------|------|---------|----------|
| **S3 + Presigned URLs** | Direct upload/download | Low | Medium | User uploads, private files |
| **S3 + CloudFront** | Read-heavy, global | Medium | Low (edge) | Public assets, media delivery |
| **Cloudflare R2** | Read-heavy, no egress | Low (zero egress) | Low | High-bandwidth, cost-sensitive |
| **Content-Addressed** | Immutable, deduped | Low | Medium | Artifacts, build outputs |
| **S3 Glacier** | Archival, rare access | Very Low | Hours | Compliance, cold backups |

### Storage Class Selection

| S3 Class | Access Frequency | Min Duration | Use Case |
|----------|-----------------|--------------|----------|
| Standard | Frequent | None | Active files |
| Standard-IA | Monthly | 30 days | Backups, older uploads |
| Glacier Instant | Quarterly | 90 days | Compliance archives |
| Glacier Deep | Yearly | 180 days | Legal hold, cold storage |

## S3 Presigned URL Generation

### Upload (PUT and POST)

```python
import boto3
import uuid
from datetime import datetime
from botocore.config import Config

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))
BUCKET = "my-app-uploads"

def generate_upload_url(content_type: str, max_size_mb: int = 10,
                        prefix: str = "uploads", expires_in: int = 3600) -> dict:
    """Generate presigned PUT URL for direct browser upload."""
    date_prefix = datetime.utcnow().strftime("%Y/%m/%d")
    file_key = f"{prefix}/{date_prefix}/{uuid.uuid4()}"
    url = s3.generate_presigned_url("put_object", Params={
        "Bucket": BUCKET, "Key": file_key, "ContentType": content_type,
    }, ExpiresIn=expires_in)
    return {"upload_url": url, "key": file_key}

def generate_presigned_post(content_type: str, max_size_mb: int = 10,
                            prefix: str = "uploads", expires_in: int = 3600) -> dict:
    """POST-based upload with server-enforced size/type constraints."""
    file_key = f"{prefix}/{datetime.utcnow():%Y/%m/%d}/{uuid.uuid4()}"
    return s3.generate_presigned_post(
        Bucket=BUCKET, Key=file_key,
        Fields={"Content-Type": content_type},
        Conditions=[
            ["content-length-range", 1, max_size_mb * 1024 * 1024],
            ["starts-with", "$Content-Type", content_type.split("/")[0]],
        ], ExpiresIn=expires_in)

def generate_download_url(file_key: str, filename: str = None,
                          expires_in: int = 3600) -> str:
    """Presigned GET with optional Content-Disposition for download."""
    params = {"Bucket": BUCKET, "Key": file_key}
    if filename:
        params["ResponseContentDisposition"] = f'attachment; filename="{filename}"'
    return s3.generate_presigned_url("get_object", Params=params, ExpiresIn=expires_in)
```

## Multipart Upload with Progress

```python
import os
from boto3.s3.transfer import TransferConfig

def upload_large_file(file_path: str, bucket: str, key: str,
                      progress_callback=None) -> None:
    """Multipart upload for files >100MB with progress tracking."""
    file_size = os.path.getsize(file_path)
    config = TransferConfig(
        multipart_threshold=100 * 1024 * 1024,
        max_concurrency=10,
        multipart_chunksize=100 * 1024 * 1024,
    )
    class Progress:
        def __init__(self):
            self.uploaded = 0
        def __call__(self, bytes_transferred):
            self.uploaded += bytes_transferred
            if progress_callback:
                progress_callback(self.uploaded / file_size * 100)

    s3.upload_file(file_path, bucket, key, Config=config, Callback=Progress())

def abort_stale_multipart_uploads(bucket: str, max_age_days: int = 7):
    """Clean up incomplete uploads to avoid hidden storage charges."""
    from datetime import timezone, timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    for upload in s3.list_multipart_uploads(Bucket=bucket).get("Uploads", []):
        if upload["Initiated"] < cutoff:
            s3.abort_multipart_upload(
                Bucket=bucket, Key=upload["Key"], UploadId=upload["UploadId"])
```

## CDN Integration

### CloudFront Signed URLs

```python
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

def create_cf_signer(key_id: str, private_key_pem: str):
    pk = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    return CloudFrontSigner(key_id,
        lambda msg: pk.sign(msg, padding.PKCS1v15(), hashes.SHA1()))

def signed_cf_url(domain: str, key: str, signer, expires_hours=24):
    url = f"https://{domain}/{key}"
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours)
    return signer.generate_presigned_url(url, date_less_than=expires)
```

### Cloudflare R2 (S3-Compatible)

```python
# R2 uses S3-compatible API; just change endpoint. Zero egress fees.
r2 = boto3.client("s3",
    endpoint_url="https://<account_id>.r2.cloudflarestorage.com",
    aws_access_key_id="R2_KEY", aws_secret_access_key="R2_SECRET",
    region_name="auto")
# All S3 operations work: put_object, get_object, presigned URLs
```

## Image Processing Pipeline

```python
from PIL import Image
import io

def process_image(input_bytes: bytes, max_width: int = 1920,
                  max_height: int = 1080, quality: int = 85,
                  output_format: str = "WEBP") -> bytes:
    """Resize, strip EXIF, compress, and convert format."""
    img = Image.open(io.BytesIO(input_bytes))
    # Strip EXIF to reduce size and avoid orientation bugs
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    clean.thumbnail((max_width, max_height), Image.LANCZOS)
    buf = io.BytesIO()
    clean.save(buf, format=output_format, quality=quality, optimize=True)
    return buf.getvalue()

def generate_thumbnails(input_bytes: bytes) -> dict:
    """Generate standard sizes for responsive images."""
    sizes = {"thumb": (150, 150), "medium": (600, 600), "large": (1200, 1200)}
    results = {}
    for name, (w, h) in sizes.items():
        img = Image.open(io.BytesIO(input_bytes))
        img.thumbnail((w, h), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=80)
        results[name] = buf.getvalue()
    return results
```

## Content-Addressed Storage

```python
import hashlib

def content_addressed_key(data: bytes, prefix: str = "cas") -> str:
    sha = hashlib.sha256(data).hexdigest()
    return f"{prefix}/{sha[:2]}/{sha}"  # prefix for S3 partition distribution

def upload_content_addressed(data: bytes, bucket: str) -> str:
    """Upload only if not already stored (dedup by hash)."""
    key = content_addressed_key(data)
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return key  # already exists
    except s3.exceptions.ClientError:
        s3.put_object(Bucket=bucket, Key=key, Body=data)
        return key
```

## Lifecycle Policies

```python
def set_lifecycle_policy(bucket: str):
    s3.put_bucket_lifecycle_configuration(Bucket=bucket, LifecycleConfiguration={
        "Rules": [
            {"ID": "transition-to-ia", "Status": "Enabled",
             "Filter": {"Prefix": "uploads/"},
             "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                             {"Days": 90, "StorageClass": "GLACIER"}]},
            {"ID": "expire-temp", "Status": "Enabled",
             "Filter": {"Prefix": "tmp/"}, "Expiration": {"Days": 1}},
            {"ID": "cleanup-multipart", "Status": "Enabled",
             "Filter": {"Prefix": ""},
             "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
        ]})
```

## Virus Scanning Integration

```python
import subprocess, os

def scan_file_clamav(file_path: str) -> dict:
    result = subprocess.run(["clamdscan", "--no-summary", file_path],
                            capture_output=True, text=True, timeout=60)
    return {"clean": result.returncode == 0, "output": result.stdout.strip()}

def upload_with_scan(file_bytes: bytes, bucket: str, final_key: str):
    """Quarantine -> scan -> move to final location if clean."""
    qkey = f"quarantine/{uuid.uuid4()}"
    s3.put_object(Bucket=bucket, Key=qkey, Body=file_bytes)
    tmp = f"/tmp/claude/scan_{uuid.uuid4()}"
    s3.download_file(bucket, qkey, tmp)
    result = scan_file_clamav(tmp)
    os.unlink(tmp)
    if result["clean"]:
        s3.copy_object(Bucket=bucket, Key=final_key,
                       CopySource={"Bucket": bucket, "Key": qkey})
    s3.delete_object(Bucket=bucket, Key=qkey)
    return result
```

## Gotchas

- **Presigned URL expiry mismatch**: URL expires during slow upload; set generous expiry (1h+) for large files
- **CORS on S3**: Direct browser uploads fail without CORS config; allow PUT/POST from your domain
- **Content-Type not set**: S3 defaults to `application/octet-stream`; always set Content-Type on upload
- **Incomplete multipart uploads**: Stale parts cost money silently; add lifecycle rule to abort after 7 days
- **CDN cache invalidation is slow**: CloudFront takes 5-15 min; use versioned keys (hash in filename) instead
- **Pillow memory bombs**: Malicious images with huge dimensions OOM server; set `Image.MAX_IMAGE_PIXELS`
- **Egress costs surprise**: S3 egress $0.09/GB; use CloudFront (cheaper) or R2 (free) for high bandwidth
- **No encryption by default**: Enable SSE-S3 or SSE-KMS bucket policy; block unencrypted uploads
