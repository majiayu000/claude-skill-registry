---
name: AWS S3 Storage Operations
description: AWS SDK v3 S3 client operations for video uploads with credential management and error handling. Use this when uploading videos to S3, configuring S3 client, handling upload failures, or implementing retry logic for object storage operations.
---

# AWS S3 Storage Operations

This Skill provides Claude Code with specific guidance on how it should handle AWS S3 storage operations.

## When to use this skill:

- Uploading rendered videos to S3 storage
- Configuring S3Client with credentials and region
- Implementing PutObjectCommand operations
- Handling S3 upload errors and retries
- Managing object keys and content-type headers
- Cleaning up temporary files after upload

## Instructions

- **AWS SDK v3**: Use `@aws-sdk/client-s3` for S3 operations with proper credential configuration
- **Credential Management**: Load credentials from Docker secrets at `/run/secrets/` in production
- **Error Handling**: Wrap S3 operations in try-catch; implement retry logic for transient failures
- **Presigned URLs**: Consider using presigned URLs for temporary access instead of public objects
- **Object Keys**: Use consistent naming pattern for video files (e.g., `videos/YYYY-MM-recap-{uuid}.mp4`)
- **Content Type**: Set correct content-type header (`video/mp4`) when uploading
- **Cleanup**: Delete temporary local files after successful S3 upload

**Examples:**
```typescript
// Good: Proper error handling, retry logic, cleanup
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import fs from 'fs';

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

async function uploadToS3(filePath: string, key: string): Promise<string> {
  const fileStream = fs.createReadStream(filePath);

  try {
    await s3Client.send(new PutObjectCommand({
      Bucket: process.env.S3_BUCKET_NAME!,
      Key: key,
      Body: fileStream,
      ContentType: 'video/mp4',
    }));

    const url = `https://${process.env.S3_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`;
    return url;
  } catch (error) {
    throw new Error(`S3 upload failed: ${error.message}`);
  } finally {
    fileStream.close();
    fs.unlinkSync(filePath); // Cleanup temp file
  }
}

// Bad: No error handling, no cleanup, missing config
async function upload(file) {
  const s3 = new S3Client({});
  await s3.send(new PutObjectCommand({ Bucket: 'bucket', Key: 'video.mp4', Body: file }));
}
```
