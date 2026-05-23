---
name: vercel-blob
description: |
  Integrate Vercel Blob for file uploads and CDN-delivered assets in Next.js. Supports client-side uploads with presigned URLs and multipart transfers for large files.

  Use when implementing file uploads (images, PDFs, videos) or troubleshooting missing tokens, size limits, client upload failures, token expiration errors, or browser compatibility issues. Prevents 16 documented errors.
user-invocable: true
---

# Vercel Blob

**Last Updated**: 2026-01-21
**Version**: @vercel/blob@2.0.0
**Skill Version**: 2.1.0

---

## Quick Start

```bash
# Create Blob store: Vercel Dashboard → Storage → Blob
vercel env pull .env.local  # Creates BLOB_READ_WRITE_TOKEN
npm install @vercel/blob
```

**Server Upload**:
```typescript
'use server';
import { put } from '@vercel/blob';

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File;
  const blob = await put(file.name, file, { access: 'public' });
  return blob.url;
}
```

**CRITICAL**: Never expose `BLOB_READ_WRITE_TOKEN` to client. Use `handleUpload()` for client uploads.

---

## Client Upload (Secure)

**Server Action** (generates presigned token):
```typescript
'use server';
import { handleUpload } from '@vercel/blob/client';

export async function getUploadToken(filename: string) {
  return await handleUpload({
    body: {
      type: 'blob.generate-client-token',
      payload: { pathname: `uploads/${filename}`, access: 'public' }
    },
    request: new Request('https://dummy'),
    onBeforeGenerateToken: async (pathname) => ({
      allowedContentTypes: ['image/jpeg', 'image/png'],
      maximumSizeInBytes: 5 * 1024 * 1024
    })
  });
}
```

**Client Component**:
```typescript
'use client';
import { upload } from '@vercel/blob/client';

const tokenResponse = await getUploadToken(file.name);
const blob = await upload(file.name, file, {
  access: 'public',
  handleUploadUrl: tokenResponse.url
});
```

---

## File Management

**List/Delete**:
```typescript
import { list, del } from '@vercel/blob';

// List with pagination
const { blobs, cursor } = await list({ prefix: 'uploads/', cursor });

// Delete
await del(blobUrl);
```

**Multipart (>500MB)**:
```typescript
import { createMultipartUpload, uploadPart, completeMultipartUpload } from '@vercel/blob';

const upload = await createMultipartUpload('large-video.mp4', { access: 'public' });
// Upload chunks in loop...
await completeMultipartUpload({ uploadId: upload.uploadId, parts });
```

---

## Critical Rules

**Always**:
- ✅ Use `handleUpload()` for client uploads (never expose `BLOB_READ_WRITE_TOKEN`)
- ✅ Validate file type/size before upload
- ✅ Use pathname organization (`avatars/`, `uploads/`)
- ✅ Add timestamp/UUID to filenames (avoid collisions)

**Never**:
- ❌ Expose `BLOB_READ_WRITE_TOKEN` to client
- ❌ Upload >500MB without multipart
- ❌ Skip file validation

---

## Known Issues Prevention

This skill prevents **16 documented issues**:

### Issue #1: Missing Environment Variable
**Error**: `Error: BLOB_READ_WRITE_TOKEN is not defined`
**Source**: https://vercel.com/docs/storage/vercel-blob
**Why It Happens**: Token not set in environment
**Prevention**: Run `vercel env pull .env.local` and ensure `.env.local` in `.gitignore`.

### Issue #2: Client Upload Token Exposed
**Error**: Security vulnerability, unauthorized uploads
**Source**: https://vercel.com/docs/storage/vercel-blob/client-upload
**Why It Happens**: Using `BLOB_READ_WRITE_TOKEN` directly in client code
**Prevention**: Use `handleUpload()` to generate client-specific tokens with constraints.

### Issue #3: File Size Limit Exceeded
**Error**: `Error: File size exceeds limit` (500MB)
**Source**: https://vercel.com/docs/storage/vercel-blob/limits
**Why It Happens**: Uploading file >500MB without multipart upload
**Prevention**: Validate file size before upload, use multipart upload for large files.

### Issue #4: Wrong Content-Type
**Error**: Browser downloads file instead of displaying (e.g., PDF opens as text)
**Source**: Production debugging
**Why It Happens**: Not setting `contentType` option, Blob guesses incorrectly
**Prevention**: Always set `contentType: file.type` or explicit MIME type.

### Issue #5: Public File Not Cached
**Error**: Slow file delivery, high egress costs
**Source**: Vercel Blob best practices
**Why It Happens**: Using `access: 'private'` for files that should be public
**Prevention**: Use `access: 'public'` for publicly accessible files (CDN caching).

### Issue #6: List Pagination Not Handled
**Error**: Only first 1000 files returned, missing files
**Source**: https://vercel.com/docs/storage/vercel-blob/using-blob-sdk#list
**Why It Happens**: Not iterating with cursor for large file lists
**Prevention**: Use cursor-based pagination in loop until `cursor` is undefined.

### Issue #7: Delete Fails Silently
**Error**: Files not deleted, storage quota fills up
**Source**: https://github.com/vercel/storage/issues/150
**Why It Happens**: Using wrong URL format, blob not found
**Prevention**: Use full blob URL from `put()` response, check deletion result.

### Issue #8: Upload Timeout (Large Files) + Server-Side 4.5MB Limit
**Error**: `Error: Request timeout` for files >100MB (server) OR file upload fails at 4.5MB (serverless function limit)
**Source**: [Vercel function timeout limits](https://vercel.com/docs/limits) + [4.5MB serverless limit](https://vercel.com/docs/limits) + [Community Discussion](https://github.com/payloadcms/payload/discussions/7569)
**Why It Happens**:
- Serverless function timeout (10s free tier, 60s pro) for server-side uploads
- **CRITICAL**: Vercel serverless functions have a hard 4.5MB request body limit. Using `put()` in server actions/API routes fails for files >4.5MB.

**Prevention**: Use client-side upload with `handleUpload()` for files >4.5MB OR use multipart upload.

```typescript
// ❌ Server-side upload fails at 4.5MB
export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('file') as File; // Fails if >4.5MB
  await put(file.name, file, { access: 'public' });
}

// ✅ Client upload bypasses 4.5MB limit (supports up to 500MB)
const blob = await upload(file.name, file, {
  access: 'public',
  handleUploadUrl: '/api/upload/token',
  multipart: true, // For files >500MB, use multipart
});
```

### Issue #9: Filename Collisions
**Error**: Files overwritten, data loss
**Source**: Production debugging
**Why It Happens**: Using same filename for multiple uploads
**Prevention**: Add timestamp/UUID: `` `uploads/${Date.now()}-${file.name}` `` or `addRandomSuffix: true`.

### Issue #10: Missing Upload Callback
**Error**: Upload completes but app state not updated
**Source**: https://vercel.com/docs/storage/vercel-blob/client-upload#callback-after-upload
**Why It Happens**: Not implementing `onUploadCompleted` callback
**Prevention**: Use `onUploadCompleted` in `handleUpload()` to update database/state.

### Issue #11: Client Upload Token Expiration for Large Files
**Error**: `Error: Access denied, please provide a valid token for this resource`
**Source**: [GitHub Issue #443](https://github.com/vercel/storage/issues/443)
**Why It Happens**: Default token expires after 30 seconds. Large files (>100MB) take longer to upload, causing token expiration before validation.
**Prevention**: Set `validUntil` parameter for large file uploads.

```typescript
// For large files (>100MB), extend token expiration
const jsonResponse = await handleUpload({
  body,
  request,
  onBeforeGenerateToken: async (pathname) => {
    return {
      maximumSizeInBytes: 200 * 1024 * 1024,
      validUntil: Date.now() + 300000, // 5 minutes
    };
  },
});
```

### Issue #12: v2.0.0 Breaking Change - onUploadCompleted Requires callbackUrl (Non-Vercel Hosting)
**Error**: onUploadCompleted callback doesn't fire when not hosted on Vercel
**Source**: [Release Notes @vercel/blob@2.0.0](https://github.com/vercel/storage/releases/tag/%40vercel/blob%402.0.0)
**Why It Happens**: v2.0.0 removed automatic callback URL inference from client-side `location.href` for security. When not using Vercel system environment variables, you must explicitly provide `callbackUrl`.
**Prevention**: Explicitly provide `callbackUrl` in `onBeforeGenerateToken` for non-Vercel hosting.

```typescript
// v2.0.0+ for non-Vercel hosting
await handleUpload({
  body,
  request,
  onBeforeGenerateToken: async (pathname) => {
    return {
      callbackUrl: 'https://example.com', // Required for non-Vercel hosting
    };
  },
  onUploadCompleted: async ({ blob, tokenPayload }) => {
    // Now fires correctly
  },
});

// For local development with ngrok:
// VERCEL_BLOB_CALLBACK_URL=https://abc123.ngrok-free.app
```

### Issue #13: ReadableStream Upload Not Supported in Firefox
**Error**: Upload never completes in Firefox
**Source**: [GitHub Issue #881](https://github.com/vercel/storage/issues/881)
**Why It Happens**: The TypeScript interface accepts `ReadableStream` as a body type, but Firefox does not support `ReadableStream` as a fetch body.
**Prevention**: Convert stream to Blob or ArrayBuffer for cross-browser support.

```typescript
// ❌ Works in Chrome/Edge, hangs in Firefox
const stream = new ReadableStream({ /* ... */ });
await put('file.bin', stream, { access: 'public' }); // Never completes in Firefox

// ✅ Convert stream to Blob for cross-browser support
const chunks: Uint8Array[] = [];
const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  chunks.push(value);
}
const blob = new Blob(chunks);
await put('file.bin', blob, { access: 'public' });
```

### Issue #14: Pathname Cannot Be Modified in onBeforeGenerateToken
**Error**: File uploaded to wrong path despite server-side pathname override attempt
**Source**: [GitHub Issue #863](https://github.com/vercel/storage/issues/863)
**Why It Happens**: The `pathname` parameter in `onBeforeGenerateToken` cannot be changed. It's set at `upload(pathname, ...)` time on the client side.
**Prevention**: Construct pathname on client, validate on server. Use `clientPayload` to pass metadata.

```typescript
// Client: Construct pathname before upload
await upload(`uploads/${Date.now()}-${file.name}`, file, {
  access: 'public',
  handleUploadUrl: '/api/upload',
  clientPayload: JSON.stringify({ userId: '123' }),
});

// Server: Validate pathname matches expected pattern
await handleUpload({
  body,
  request,
  onBeforeGenerateToken: async (pathname, clientPayload) => {
    const { userId } = JSON.parse(clientPayload || '{}');

    // Validate pathname starts with expected prefix
    if (!pathname.startsWith(`uploads/`)) {
      throw new Error('Invalid upload path');
    }

    return {
      allowedContentTypes: ['image/jpeg', 'image/png'],
      tokenPayload: JSON.stringify({ userId }), // Pass to onUploadCompleted
    };
  },
});
```

### Issue #15: Multipart Upload Minimum Chunk Size (5MB)
**Error**: Manual multipart upload fails with small chunks
**Source**: [Official Docs](https://vercel.com/docs/storage/vercel-blob/using-blob-sdk#manual) + [Community Discussion](https://community.vercel.com/t/4-5-mb-payload-limit/10500)
**Why It Happens**: Each part in manual multipart upload must be at least 5MB (except the last part). This conflicts with Vercel's 4.5MB serverless function limit, making manual multipart uploads impossible via server-side routes.
**Prevention**: Use automatic multipart (`multipart: true` in `put()`) or client uploads.

```typescript
// ❌ Manual multipart upload fails (can't upload 5MB chunks via serverless function)
const upload = await createMultipartUpload('large.mp4', { access: 'public' });
// uploadPart() requires 5MB minimum - hits serverless limit

// ✅ Use automatic multipart via client upload
await upload('large.mp4', file, {
  access: 'public',
  handleUploadUrl: '/api/upload',
  multipart: true, // Automatically handles 5MB+ chunks
});
```

### Issue #16: Missing File Extension Causes Access Denied Error
**Error**: `Error: Access denied, please provide a valid token for this resource`
**Source**: [GitHub Issue #664](https://github.com/vercel/storage/issues/664)
**Why It Happens**: Pathname without file extension causes non-descriptive access denied error.
**Prevention**: Always include file extension in pathname.

```typescript
// ❌ Fails with confusing error
await upload('user-12345', file, {
  access: 'public',
  handleUploadUrl: '/api/upload',
}); // Error: Access denied

// ✅ Extract extension and include in pathname
const extension = file.name.split('.').pop();
await upload(`user-${userId}.${extension}`, file, {
  access: 'public',
  handleUploadUrl: '/api/upload',
});
```

---

## Common Patterns

**Avatar Upload with Replacement**:
```typescript
'use server';
import { put, del } from '@vercel/blob';

export async function updateAvatar(userId: string, formData: FormData) {
  const file = formData.get('avatar') as File;
  if (!file.type.startsWith('image/')) throw new Error('Only images allowed');

  const user = await db.query.users.findFirst({ where: eq(users.id, userId) });
  if (user?.avatarUrl) await del(user.avatarUrl); // Delete old

  const blob = await put(`avatars/${userId}.jpg`, file, { access: 'public' });
  await db.update(users).set({ avatarUrl: blob.url }).where(eq(users.id, userId));
  return blob.url;
}
```

**Protected Upload** (`access: 'private'`):
```typescript
const blob = await put(`documents/${userId}/${file.name}`, file, { access: 'private' });
```
