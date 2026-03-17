---
name: NestJS File Uploads
description: Secure file handling, Validation, and S3 streaming.
metadata:
  labels: [nestjs, upload, multer, s3]
  triggers:
    files: ['**/*.controller.ts']
    keywords: [FileInterceptor, Multer, S3, UploadedFile]
---

# File Upload Patterns

## **Priority: P0 (FOUNDATIONAL)**

Secure file upload handling with validation and storage patterns.

- **Magic Bytes**: NEVER trust `content-type` header or file extension.
  - **Tool**: Use `file-type` or `mmmagic` to verify the actual buffer signature.
- **Limits**: Set strict `limits: { fileSize: 5000000 }` (5MB) in Multer config to prevent DoS.

## Streaming (Scalability)

- **Memory Warning**: Default Multer `MemoryStorage` crashes servers with large files.
- **Pattern**: Use **Streaming** for any file > 10MB.
  - **Library**: `multer-s3` (direct upload to bucket) or `busboy` (raw stream processing).
  - **Architecture**:
    1. Client requests Signed URL from API.
    2. Client uploads directly to S3/GCS (Bypassing API server completely).
    3. **Pro Tip**: This is the only way to scale file uploads infinitely.

## Processing

- **Async**: Don't process images/videos in the HTTP Request.
- **Flow**:
  1. Upload file.
  2. Push `FileUploadedEvent` to Queue (BullMQ).
  3. Worker downloads, resizes/converts, and re-uploads.
