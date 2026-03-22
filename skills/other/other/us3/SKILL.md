---
name: us3
description: Upload files to UCloud US3 object storage and generate public URLs
user-invocable: true
metadata: {"clawdbot":{"emoji":"☁️","requires":{"env":["US3_PUBLIC_KEY","US3_PRIVATE_KEY","US3_BUCKET","US3_ENDPOINT"]},"primaryEnv":"US3_PUBLIC_KEY","homepage":"https://www.ucloud.cn/site/product/ufile.html"}}
---

# UCloud US3 Storage Skill

Upload files to UCloud US3 object storage and generate public URLs.

## When to use this skill

Use this skill when:
- The user wants to upload files to cloud storage
- You need to share files via public URLs
- You need to store images, videos, or documents in the cloud
- You need to generate shareable links for files

## Prerequisites

- UCloud US3 account and bucket from https://www.ucloud.cn/
- Set environment variables:
  - `US3_PUBLIC_KEY` - UCloud Public Key (Token)
  - `US3_PRIVATE_KEY` - UCloud Private Key
  - `US3_BUCKET` - Bucket domain (e.g., xqm.cn-sh2.ufileos.com)
  - `US3_ENDPOINT` - API endpoint (e.g., https://api.ucloud.cn/)

## Usage

Upload files and get public URLs:

```bash
# Upload a file
node /root/clawdbot/skills/us3/upload.mjs --file "/path/to/file.jpg"

# Upload with custom key name
node /root/clawdbot/skills/us3/upload.mjs --file "/path/to/file.jpg" --key "custom/path/file.jpg"

# Upload and get URL only
node /root/clawdbot/skills/us3/upload.mjs --file "/path/to/file.jpg" --url-only
```

### Parameters

- `--file` (required): Local file path to upload
- `--key` (optional): Custom object key (path) in bucket. If not provided, uses filename
- `--url-only` (optional): Output only the public URL (default: false)

### Examples

```bash
# Upload an image
node /root/clawdbot/skills/us3/upload.mjs --file "/tmp/screenshot.png"

# Upload to specific path
node /root/clawdbot/skills/us3/upload.mjs --file "/tmp/video.mp4" --key "videos/2026/video.mp4"

# Upload Feishu downloaded image
node /root/clawdbot/skills/us3/upload.mjs --file "/tmp/feishu_image_123.png" --key "feishu/$(date +%Y%m%d_%H%M%S).png"

# Get just the URL
node /root/clawdbot/skills/us3/upload.mjs --file "/tmp/report.pdf" --url-only
```

## Output

Returns JSON with upload results:

```json
{
  "success": true,
  "url": "https://xqm.cn-sh2.ufileos.com/path/to/file.jpg",
  "key": "path/to/file.jpg",
  "bucket": "xqm.cn-sh2.ufileos.com",
  "size": 123456
}
```

With `--url-only` flag, outputs only the URL string:
```
https://xqm.cn-sh2.ufileos.com/path/to/file.jpg
```

## Supported File Types

- Images: JPG, PNG, GIF, WEBP, BMP, SVG
- Videos: MP4, MOV, AVI, MKV, WEBM
- Documents: PDF, DOC, DOCX, TXT, MD
- Audio: MP3, WAV, OGG, M4A
- Archives: ZIP, TAR, GZ
- Any other file type

## Common Use Cases

### Upload Feishu Images
When user sends an image via Feishu and wants to share:
1. Image is auto-downloaded to `/tmp/feishu_*.png`
2. Upload to US3: `node upload.mjs --file "/tmp/feishu_image_123.png"`
3. Share the returned public URL

### Upload Processed Files
After converting/processing files:
```bash
# Convert and upload
convert input.jpg -resize 800x600 /tmp/resized.jpg
node /root/clawdbot/skills/us3/upload.mjs --file "/tmp/resized.jpg" --key "images/resized_$(date +%s).jpg"
```

### Batch Upload
Upload multiple files:
```bash
for file in /tmp/*.png; do
  node /root/clawdbot/skills/us3/upload.mjs --file "$file" --key "batch/$(basename $file)"
done
```

## Notes

- Files are uploaded to a public bucket - URLs are directly accessible
- File size limit: Check your UCloud US3 plan limits
- The bucket domain format: `bucket-name.region.ufileos.com`
- Use meaningful key names for better organization
- Automatic content-type detection based on file extension

## Error Handling

Common errors and solutions:
- `missing_credentials`: Set all required environment variables
- `file_not_found`: Check file path exists
- `upload_failed`: Check network connection and credentials
- `invalid_bucket`: Verify bucket name and region

## Integration Tips

Works well with:
- **feishu-media**: Upload images from Feishu messages
- **ffmpeg**: Upload processed videos
- **baidu-ocr**: Upload images before/after OCR processing
