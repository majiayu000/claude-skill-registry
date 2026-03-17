---
name: s3-upload-handler
description: Handle S3 file uploads including UI components, client-side logic, and server-side processing
tools: Read, Write, Edit
model: inherit
---

# S3 Upload Handler Skill

This skill provides methods to handle file uploads to AWS S3 using pre-built UI components, custom client-side logic, or server-side processing.

## Capabilities

1.  **UI Component**: Ready-to-use `S3Uploader` for drag-and-drop or button uploads.
2.  **Client SDK**: `ClientS3Uploader` class for custom upload interfaces.
3.  **Server Utilities**: `uploadFromServer` for backend file processing and uploading.

## Usage Patterns

### 1. Standard UI Component (Recommended)

Use the `S3Uploader` component for most user-facing upload needs.

```tsx
import { S3Uploader } from "@/components/ui/s3-uploader/s3-uploader";

// Usage in a form or page
<S3Uploader
  presignedRouteProvider="/api/app/your-upload-route" // API route to get signed URL
  variant="dropzone" // or "button"
  maxFiles={5}
  accept="image/*" // or specific extensions like ".pdf,.doc"
  onUpload={async (fileUrls) => {
    console.log("Files uploaded:", fileUrls);
    // Handle success (e.g., update form state)
  }}
/>
```

### 2. Custom Client-Side Upload

Use `ClientS3Uploader` when you need full control over the UI (e.g., hidden inputs, custom buttons).

```tsx
import { ClientS3Uploader } from "@/lib/s3/clientS3Uploader";

// Initialize
const uploader = new ClientS3Uploader({
  presignedRouteProvider: "/api/app/your-upload-route"
});

// Upload a file
const url = await uploader.uploadFile(fileObject);
```

### 3. Server-Side Upload

Use `uploadFromServer` in API routes or Server Actions for processing files (resizing, generating PDFs) before storage.

```typescript
import uploadFromServer from "@/lib/s3/uploadFromServer";

// In a server context (API route/Action)
const url = await uploadFromServer({
  file: base64String, // File content as base64
  path: "uploads/users/avatar.jpg", // Destination path in bucket
  contentType: "image/jpeg" // MIME type
});
```

## Environment Configuration

Ensure `.env.local` has the necessary AWS credentials:

```env
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_REGION="us-east-1"
AWS_S3_BUCKET_NAME="your-bucket-name"
```

## API Route Example (for Presigned URLs)

You typically need an API route to generate presigned URLs for the client uploader.

```typescript
// src/app/api/app/upload-input-images/route.ts
import { createPresignedPost } from "@aws-sdk/s3-presigned-post";
import { S3Client } from "@aws-sdk/client-s3";
import { v4 as uuidv4 } from "uuid";

export async function POST(request: Request) {
  const { fileName, fileType } = await request.json();
  const client = new S3Client({ region: process.env.AWS_REGION });

  const { url, fields } = await createPresignedPost(client, {
    Bucket: process.env.AWS_S3_BUCKET_NAME!,
    Key: `uploads/${uuidv4()}-${fileName}`,
    Conditions: [
      ["content-length-range", 0, 10485760], // up to 10 MB
      ["starts-with", "$Content-Type", fileType],
    ],
    Fields: {
      acl: "public-read",
      "Content-Type": fileType,
    },
    Expires: 600, // Seconds before the presigned post expires. 3600 by default.
  });

  return Response.json({ url, fields });
}
```

Refer to [reference.md](reference.md) for more details.