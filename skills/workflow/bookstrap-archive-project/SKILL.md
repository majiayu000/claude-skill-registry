---
name: bookstrap-archive-project
description: Archive project with compression and optional cloud upload
invoke: skill
category: export
---

# Project Archive Command

Archive a completed or paused Bookstrap project with compression and optional cloud storage.

## What It Does

- Exports complete project
- Compresses to minimal size
- Optionally uploads to cloud storage
- Creates archive metadata
- Optionally removes local files after archiving

## Usage

```bash
/bookstrap-archive-project \
  --output archives/my-book-final.tar.gz \
  --compress-level 9 \
  --upload s3://my-bucket/archives/
```

## Archive vs Export

| Feature | Export | Archive |
|---------|--------|---------|
| Compression | Standard | Maximum |
| Cloud upload | No | Optional |
| Remove local | No | Optional |
| Checksums | Basic | Full verification |
| Metadata | Simple | Comprehensive |

## Compression Levels

- `--compress-level 1`: Fast, larger files
- `--compress-level 5`: Balanced (default)
- `--compress-level 9`: Maximum compression, slower

## Cloud Upload

### S3-Compatible Storage

```bash
/bookstrap-archive-project \
  --output my-book.tar.gz \
  --upload s3://bucket-name/path/ \
  --s3-region us-east-1
```

### Google Cloud Storage

```bash
/bookstrap-archive-project \
  --output my-book.tar.gz \
  --upload gs://bucket-name/path/
```

### Azure Blob Storage

```bash
/bookstrap-archive-project \
  --output my-book.tar.gz \
  --upload azure://container-name/path/
```

## Archive Metadata

Creates `archive-metadata.json`:

```json
{
  "archive_name": "my-book-final.tar.gz",
  "created_at": "2026-02-01T12:00:00Z",
  "project_name": "My Book",
  "status": "completed",
  "archive_size_mb": 8.3,
  "compression": {
    "algorithm": "gzip",
    "level": 9,
    "original_size_mb": 45.2,
    "compressed_size_mb": 8.3,
    "ratio": 0.18
  },
  "contents": {
    "chapters": 12,
    "sections": 48,
    "words": 75420,
    "sources": 42,
    "entities": 156
  },
  "cloud_storage": {
    "uploaded": true,
    "location": "s3://my-bucket/archives/my-book-final.tar.gz",
    "checksum": "sha256:abc123..."
  },
  "restoration": {
    "command": "/bookstrap-restore-archive --input my-book-final.tar.gz",
    "requires": ["surrealdb", "python3"]
  }
}
```

## Options

- `--compress-level N`: Compression level (1-9)
- `--upload URL`: Upload to cloud storage
- `--remove-local`: Remove local files after archive
- `--encrypt`: Encrypt archive with password
- `--verify`: Verify archive integrity after creation

## Encryption

```bash
/bookstrap-archive-project \
  --output my-book.tar.gz.enc \
  --encrypt \
  --password-file .archive-password
```

## Verification

After archiving, automatically verifies:
- Archive can be extracted
- Database backup is valid
- Checksums match
- No file corruption

## Example

```
Archiving Bookstrap project...

Preparing archive...
├─ Collecting files... 1,247 files
├─ Compressing with level 9... 45.2 MB → 8.3 MB (81% reduction)
├─ Calculating checksums... Done
├─ Generating metadata... Done
└─ Verifying archive integrity... PASSED

Archive created: my-book-final.tar.gz (8.3 MB)

Uploading to cloud storage...
├─ Destination: s3://my-bucket/archives/my-book-final.tar.gz
├─ Upload progress: [████████████████████] 100%
├─ Verifying upload checksum... MATCH
└─ Upload complete

Archive complete!

Local archive: ./archives/my-book-final.tar.gz
Cloud location: s3://my-bucket/archives/my-book-final.tar.gz
Metadata: ./archives/my-book-final-metadata.json

To restore: /bookstrap-restore-archive --input my-book-final.tar.gz
```
