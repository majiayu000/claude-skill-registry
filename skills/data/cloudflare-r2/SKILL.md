---
name: cloudflare-r2
description: >
  Cloudflare R2 object storage - upload, download, list, delete files, presigned URLs.
  Trigger: When working with R2 storage, file uploads, object storage, presigned URLs.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Critical Patterns

### Setup Binding

```toml
# wrangler.toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

```typescript
export interface Env {
  MY_BUCKET: R2Bucket
}
```

### Upload

```typescript
// Upload file
await env.MY_BUCKET.put("path/to/file.txt", fileBuffer, {
  httpMetadata: {
    contentType: "text/plain",
    cacheControl: "max-age=31536000"
  },
  customMetadata: {
    uploadedBy: "user-123",
    originalName: "document.txt"
  }
})

// From FormData
app.post("/upload", async (c) => {
  const formData = await c.req.formData()
  const file = formData.get("file") as File
  
  if (!file) {
    return c.json({ error: "No file" }, 400)
  }
  
  const key = `uploads/${crypto.randomUUID()}-${file.name}`
  await c.env.MY_BUCKET.put(key, await file.arrayBuffer(), {
    httpMetadata: { contentType: file.type }
  })
  
  return c.json({ success: true, key })
})
```

### Download

```typescript
// Get object
const object = await env.MY_BUCKET.get("path/to/file.txt")

if (!object) {
  return new Response("Not found", { status: 404 })
}

// Stream to response (efficient for large files)
return new Response(object.body, {
  headers: {
    "Content-Type": object.httpMetadata.contentType,
    "ETag": object.etag,
    "Cache-Control": "max-age=3600"
  }
})

// Access metadata
console.log(object.key)              // File key
console.log(object.size)             // Size in bytes
console.log(object.uploaded)         // Upload date
console.log(object.customMetadata)   // Custom metadata
```

### List Objects

```typescript
// List with pagination
const listed = await env.MY_BUCKET.list({
  limit: 100,                    // Max 1000
  prefix: "images/",             // Filter by prefix
  cursor: cursorToken,           // For pagination
  include: ["customMetadata"]    // Include metadata
})

for (const obj of listed.objects) {
  console.log(obj.key, obj.size, obj.uploaded)
}

// Next page
if (listed.truncated) {
  const nextPage = await env.MY_BUCKET.list({
    cursor: listed.cursor
  })
}
```

### Delete

```typescript
// Delete single
await env.MY_BUCKET.delete("path/to/file.txt")

// Delete multiple
await env.MY_BUCKET.delete([
  "file1.txt",
  "file2.txt",
  "images/photo.jpg"
])
```

### Check Existence (Head)

```typescript
// Get metadata without downloading body
const object = await env.MY_BUCKET.head("file.txt")

if (!object) {
  return new Response("Not found", { status: 404 })
}

console.log(object.size)
console.log(object.etag)
// Note: object.body is undefined for head()
```

### Presigned URLs

```typescript
import { S3Client, GetObjectCommand, PutObjectCommand } from "@aws-sdk/client-s3"
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"

const S3 = new S3Client({
  region: "auto",
  endpoint: `https://${env.ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY
  }
})

// Download URL (valid 1 hour)
const downloadUrl = await getSignedUrl(
  S3,
  new GetObjectCommand({
    Bucket: "my-bucket",
    Key: "file.txt"
  }),
  { expiresIn: 3600 }
)

// Upload URL
const uploadUrl = await getSignedUrl(
  S3,
  new PutObjectCommand({
    Bucket: "my-bucket",
    Key: "upload.txt",
    ContentType: "text/plain"
  }),
  { expiresIn: 3600 }
)

// Client can PUT/GET to these URLs
```

## Performance Tips

```typescript
// ✅ Stream large files (don't load into memory)
const object = await env.MY_BUCKET.get("large-file.mp4")
return new Response(object.body, {
  headers: { "Content-Type": "video/mp4" }
})

// ✅ Use head() for existence checks (no body transfer)
const exists = await env.MY_BUCKET.head("file.txt") !== null

// ❌ Wasteful - downloads entire file
const exists = await env.MY_BUCKET.get("file.txt") !== null

// ✅ Set cache headers for static files
await env.MY_BUCKET.put("logo.png", file, {
  httpMetadata: {
    contentType: "image/png",
    cacheControl: "public, max-age=31536000, immutable"
  }
})
```

## Common Patterns

### File Download Endpoint

```typescript
app.get("/files/:key", async (c) => {
  const key = c.req.param("key")
  const object = await c.env.MY_BUCKET.get(key)
  
  if (!object) {
    return c.json({ error: "Not found" }, 404)
  }
  
  return new Response(object.body, {
    headers: {
      "Content-Type": object.httpMetadata.contentType,
      "Content-Disposition": `attachment; filename="${object.customMetadata?.originalName}"`,
      "ETag": object.etag
    }
  })
})
```

### List Files with Pagination

```typescript
app.get("/files", async (c) => {
  const cursor = c.req.query("cursor")
  const prefix = c.req.query("prefix")
  
  const listed = await c.env.MY_BUCKET.list({
    limit: 100,
    prefix,
    cursor,
    include: ["customMetadata"]
  })
  
  return c.json({
    files: listed.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded,
      metadata: obj.customMetadata
    })),
    cursor: listed.truncated ? listed.cursor : null
  })
})
```

## Commands

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Upload file
wrangler r2 object put my-bucket/file.txt --file=./local.txt

# List objects
wrangler r2 object list my-bucket

# Delete
wrangler r2 object delete my-bucket/file.txt
```

## Resources

- **Docs**: [developers.cloudflare.com/r2](https://developers.cloudflare.com/r2)
- R2 is S3-compatible
