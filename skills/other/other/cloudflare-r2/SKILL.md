---
name: cloudflare-r2
description: |
  Store objects with R2's S3-compatible storage on Cloudflare's edge. Use when: uploading/downloading files, configuring CORS, generating presigned URLs, multipart uploads, managing metadata, or troubleshooting R2_ERROR, CORS failures, presigned URL issues, quota errors, 429 rate limits, list() metadata missing, or platform outages. Prevents 13 documented errors including r2.dev rate limiting, concurrent write limits, API token permissions, and CORS format confusion.
user-invocable: true
---

# Cloudflare R2 Object Storage

**Status**: Production Ready ✅
**Last Updated**: 2026-01-20
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.59.2, @cloudflare/workers-types@4.20260109.0, aws4fetch@1.0.20

**Recent Updates (2025)**:
- **September 2025**: R2 SQL open beta (serverless query engine for Apache Iceberg), Pipelines GA (real-time stream ingestion), Remote bindings GA (local dev connects to deployed R2)
- **May 2025**: Dashboard redesign (deeplink support, bucket settings centralization), Super Slurper 5x faster (rebuilt with Workers/Queues/Durable Objects)
- **April 2025**: R2 Data Catalog open beta (managed Apache Iceberg catalog), Event Notifications open beta (5,000 msg/s per Queue)
- **2025**: Bucket limits increased (1 million max), CRC-64/NVME checksums, Server-side encryption with customer keys, Infrequent Access storage class (beta), Oceania region, S3 API enhancements (sha256/sha1 checksums, ListParts, conditional CopyObject)

---

## Quick Start (5 Minutes)

```bash
# 1. Create bucket
npx wrangler r2 bucket create my-bucket

# 2. Add binding to wrangler.jsonc
# {
#   "r2_buckets": [{
#     "binding": "MY_BUCKET",
#     "bucket_name": "my-bucket",
#     "preview_bucket_name": "my-bucket-preview"  // Optional: separate dev/prod
#   }]
# }

# 3. Upload/download from Worker
type Bindings = { MY_BUCKET: R2Bucket };

// Upload
await env.MY_BUCKET.put('file.txt', data, {
  httpMetadata: { contentType: 'text/plain' }
});

// Download
const object = await env.MY_BUCKET.get('file.txt');
if (!object) return c.json({ error: 'Not found' }, 404);

return new Response(object.body, {
  headers: {
    'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
    'ETag': object.httpEtag,
  },
});

# 4. Deploy
npx wrangler deploy
```

---

## R2 Workers API

### Core Methods

```typescript
// put() - Upload objects
await env.MY_BUCKET.put('file.txt', data, {
  httpMetadata: {
    contentType: 'text/plain',
    cacheControl: 'public, max-age=3600',
  },
  customMetadata: { userId: '123' },
  md5: await crypto.subtle.digest('MD5', data),  // Checksum verification
});

// Conditional upload (prevent overwrites)
const object = await env.MY_BUCKET.put('file.txt', data, {
  onlyIf: { uploadedBefore: new Date('2020-01-01') }
});
if (!object) return c.json({ error: 'File already exists' }, 409);

// get() - Download objects
const object = await env.MY_BUCKET.get('file.txt');
if (!object) return c.json({ error: 'Not found' }, 404);

const text = await object.text();           // As string
const json = await object.json();           // As JSON
const buffer = await object.arrayBuffer();  // As ArrayBuffer

// Range requests (partial downloads)
const partial = await env.MY_BUCKET.get('video.mp4', {
  range: { offset: 0, length: 1024 * 1024 }  // First 1MB
});

// head() - Get metadata only (no body download)
const object = await env.MY_BUCKET.head('file.txt');
console.log(object.size, object.etag, object.customMetadata);

// delete() - Delete objects
await env.MY_BUCKET.delete('file.txt');  // Single delete (idempotent)
await env.MY_BUCKET.delete(['file1.txt', 'file2.txt']);  // Bulk delete (max 1000)

// list() - List objects
const listed = await env.MY_BUCKET.list({
  prefix: 'images/',  // Filter by prefix
  limit: 100,
  cursor: cursor,     // Pagination
  delimiter: '/',     // Folder-like listing
  include: ['httpMetadata', 'customMetadata'],  // IMPORTANT: Opt-in for metadata
});

for (const object of listed.objects) {
  console.log(`${object.key}: ${object.size} bytes`);
  console.log(object.httpMetadata?.contentType);  // Now populated with include parameter
  console.log(object.customMetadata);             // Now populated with include parameter
}
```

---

## Multipart Uploads

For files >100MB or resumable uploads. Use when: large files, browser uploads, parallelization needed.

```typescript
// 1. Create multipart upload
const multipart = await env.MY_BUCKET.createMultipartUpload('large-file.zip', {
  httpMetadata: { contentType: 'application/zip' }
});

// 2. Upload parts (5MB-100MB each, max 10,000 parts)
const multipart = env.MY_BUCKET.resumeMultipartUpload(key, uploadId);
const part1 = await multipart.uploadPart(1, chunk1);
const part2 = await multipart.uploadPart(2, chunk2);

// 3. Complete upload
const object = await multipart.complete([
  { partNumber: 1, etag: part1.etag },
  { partNumber: 2, etag: part2.etag },
]);

// 4. Abort if needed
await multipart.abort();
```

**Limits**: Parts 5MB-100MB, max 10,000 parts per upload. Don't use for files <5MB (overhead).

---

## Presigned URLs

Allow clients to upload/download directly to/from R2 (bypasses Worker). Use aws4fetch library.

```typescript
import { AwsClient } from 'aws4fetch';

const r2Client = new AwsClient({
  accessKeyId: env.R2_ACCESS_KEY_ID,
  secretAccessKey: env.R2_SECRET_ACCESS_KEY,
});

const url = new URL(
  `https://${bucketName}.${accountId}.r2.cloudflarestorage.com/${filename}`
);
url.searchParams.set('X-Amz-Expires', '3600');  // 1 hour expiry

const signed = await r2Client.sign(
  new Request(url, { method: 'PUT' }),  // or 'GET' for downloads
  { aws: { signQuery: true } }
);

// Client uploads directly to R2
await fetch(signed.url, { method: 'PUT', body: file });
```

**CRITICAL Security:**
- ❌ **NEVER** expose R2 access keys in client-side code
- ✅ **ALWAYS** generate presigned URLs server-side
- ✅ **ALWAYS** set expiry times (1-24 hours typical)
- ✅ **ALWAYS** add authentication before generating URLs
- ✅ **CONSIDER** scoping to user folders: `users/${userId}/${filename}`

### Presigned URL Domain Requirements

**CRITICAL**: Presigned URLs **ONLY work with the S3 API domain**, not custom domains.

```typescript
// ❌ WRONG - Presigned URLs don't work with custom domains
const url = new URL(`https://cdn.example.com/${filename}`);
const signed = await r2Client.sign(
  new Request(url, { method: 'PUT' }),
  { aws: { signQuery: true } }
);
// This URL will fail - presigning requires S3 domain

// ✅ CORRECT - Use R2 storage domain for presigned URLs
const url = new URL(
  `https://${accountId}.r2.cloudflarestorage.com/${filename}`
);
const signed = await r2Client.sign(
  new Request(url, { method: 'PUT' }),
  { aws: { signQuery: true } }
);

// Pattern: Upload via presigned S3 URL, serve via custom domain
async function generateUploadUrl(filename: string) {
  const uploadUrl = new URL(
    `https://${accountId}.r2.cloudflarestorage.com/${filename}`
  );
  const signed = await r2Client.sign(
    new Request(uploadUrl, { method: 'PUT' }),
    { aws: { signQuery: true } }
  );

  return {
    uploadUrl: signed.url,  // For client upload (S3 domain)
    publicUrl: `https://cdn.example.com/${filename}`  // For serving (custom domain)
  };
}
```

**Source**: [Community Knowledge](https://ruanmartinelli.com/blog/cloudflare-r2-pre-signed-urls/)

### API Token Requirements for Wrangler

⚠️ **Wrangler CLI requires "Admin Read & Write" permissions**, not "Object Read & Write".

When creating API tokens for wrangler operations:
- ✅ **Use**: R2 → Admin Read & Write
- ❌ **Don't use**: R2 → Object Read & Write (causes 403 Forbidden errors)

**Why**: "Object Read & Write" is for S3 API direct access only. Wrangler needs admin-level permissions for bucket operations.

```bash
# With wrong permissions:
export CLOUDFLARE_API_TOKEN="token_with_object_readwrite"
wrangler r2 object put my-bucket/file.txt --file=./file.txt --remote
# ✘ [ERROR] Failed to fetch - 403: Forbidden

# With correct permissions (Admin Read & Write):
wrangler r2 object put my-bucket/file.txt --file=./file.txt --remote
# ✔ Success
```

**Source**: [GitHub Issue #9235](https://github.com/cloudflare/workers-sdk/issues/9235)

---

## CORS Configuration

Configure CORS in bucket settings (Dashboard → R2 → Bucket → Settings → CORS Policy) before browser access.

### Dashboard Format vs CLI Format

⚠️ **The wrangler CLI and Dashboard UI use DIFFERENT CORS formats**. This commonly causes confusion.

**Dashboard Format** (works in UI only):
```json
[{
  "AllowedOrigins": ["https://example.com"],
  "AllowedMethods": ["GET", "PUT"],
  "AllowedHeaders": ["*"],
  "ExposeHeaders": ["ETag"],
  "MaxAgeSeconds": 3600
}]
```

**CLI Format** (required for `wrangler r2 bucket cors`):
```json
{
  "rules": [{
    "allowed": {
      "origins": ["https://www.example.com"],
      "methods": ["GET", "PUT"],
      "headers": ["Content-Type", "Authorization"]
    },
    "exposeHeaders": ["ETag", "Content-Length"],
    "maxAgeSeconds": 8640
  }]
}
```

```bash
# Using CLI format
wrangler r2 bucket cors set my-bucket --file cors-config.json

# Error if using Dashboard format:
# "The CORS configuration file must contain a 'rules' array"
```

**Source**: [GitHub Issue #10076](https://github.com/cloudflare/workers-sdk/issues/10076)

### Custom Domain CORS

When using custom domains with R2, CORS is handled in **two layers**:

1. **R2 Bucket CORS**: Applies to all access methods (presigned URLs, direct S3 access)
2. **Transform Rules CORS**: Additional CORS headers via Cloudflare Cache settings on custom domain

```typescript
// Bucket CORS (set via dashboard or wrangler)
{
  "rules": [{
    "allowed": {
      "origins": ["https://app.example.com"],
      "methods": ["GET", "PUT"],
      "headers": ["Content-Type"]
    },
    "maxAgeSeconds": 3600
  }]
}

// Additional CORS via Transform Rules (Dashboard → Rules → Transform Rules)
// Modify Response Header: Access-Control-Allow-Origin: https://app.example.com

// Order of CORS evaluation:
// 1. R2 bucket CORS (if presigned URL or direct R2 access)
// 2. Transform Rules CORS (if via custom domain)
```

**Source**: [Community Knowledge](https://mikeesto.medium.com/pre-signed-urls-cors-on-cloudflare-r2-c90d43370dc4)

**For presigned URLs**: CORS handled by R2 directly (configure on bucket, not Worker).

---

## HTTP Metadata & Custom Metadata

```typescript
// HTTP metadata (standard headers)
await env.MY_BUCKET.put('file.pdf', data, {
  httpMetadata: {
    contentType: 'application/pdf',
    cacheControl: 'public, max-age=31536000, immutable',
    contentDisposition: 'attachment; filename="report.pdf"',
    contentEncoding: 'gzip',
  },
  customMetadata: {
    userId: '12345',
    version: '1.0',
  }  // Max 2KB total, keys/values must be strings
});

// Read metadata
const object = await env.MY_BUCKET.head('file.pdf');
console.log(object.httpMetadata, object.customMetadata);
```

---

## Error Handling

### Common R2 Errors

```typescript
try {
  await env.MY_BUCKET.put(key, data);
} catch (error: any) {
  const message = error.message;

  if (message.includes('R2_ERROR')) {
    // Generic R2 error
  } else if (message.includes('exceeded')) {
    // Quota exceeded
  } else if (message.includes('precondition')) {
    // Conditional operation failed
  } else if (message.includes('multipart')) {
    // Multipart upload error
  }

  console.error('R2 Error:', message);
  return c.json({ error: 'Storage operation failed' }, 500);
}
```

### Retry Logic

R2 experienced two major outages in Q1 2025 (February 6: 59 minutes, March 21: 1h 7min) due to operational issues. Implement robust retry logic with exponential backoff for platform errors.

```typescript
async function r2WithRetry<T>(
  operation: () => Promise<T>,
  maxRetries = 5
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error: any) {
      const message = error.message;

      // Retry on transient errors and platform issues
      const is5xxError =
        message.includes('500') ||
        message.includes('502') ||
        message.includes('503') ||
        message.includes('504');

      const isRetryable =
        is5xxError ||
        message.includes('network') ||
        message.includes('timeout') ||
        message.includes('temporarily unavailable');

      if (!isRetryable || attempt === maxRetries - 1) {
        throw error;
      }

      // Exponential backoff (longer for platform errors)
      // 5xx errors: 1s, 2s, 4s, 8s, 16s (up to 31s total)
      // Other errors: 1s, 2s, 4s, 5s, 5s (up to 17s total)
      const delay = is5xxError
        ? Math.min(1000 * Math.pow(2, attempt), 16000)
        : Math.min(1000 * Math.pow(2, attempt), 5000);

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Max retries exceeded');
}

// Usage
const object = await r2WithRetry(() =>
  env.MY_BUCKET.get('important-file.txt')
);
```

**Platform Reliability**: While R2 is generally reliable, the 2025 Q1 outages demonstrate the importance of retry logic for production applications. All 5xx errors should be retried with exponential backoff.

**Sources**:
- [February 6 Incident](https://blog.cloudflare.com/cloudflare-incident-on-february-6-2025/)
- [March 21 Incident](https://blog.cloudflare.com/cloudflare-incident-march-21-2025/)

---

## Performance Optimization

```typescript
// Batch delete (up to 1000 keys)
await env.MY_BUCKET.delete(['file1.txt', 'file2.txt', 'file3.txt']);

// Range requests for large files
const partial = await env.MY_BUCKET.get('video.mp4', {
  range: { offset: 0, length: 10 * 1024 * 1024 }  // First 10MB
});

// Cache headers for immutable assets
await env.MY_BUCKET.put('static/app.abc123.js', jsData, {
  httpMetadata: { cacheControl: 'public, max-age=31536000, immutable' }
});

// Checksums for data integrity
const md5Hash = await crypto.subtle.digest('MD5', fileData);
await env.MY_BUCKET.put('important.dat', fileData, { md5: md5Hash });
```

### Concurrent Write Rate Limits

⚠️ **High-frequency concurrent writes to the same object key will trigger HTTP 429 rate limiting**.

```typescript
// ❌ BAD: Multiple Workers writing to same key rapidly
async function logToSharedFile(env: Env, logEntry: string) {
  const existing = await env.LOGS.get('global-log.txt');
  const content = (await existing?.text()) || '';
  await env.LOGS.put('global-log.txt', content + logEntry);
  // High write frequency to same key = 429 errors
}

// ✅ GOOD: Shard by timestamp or ID (distribute writes)
async function logWithSharding(env: Env, logEntry: string) {
  const timestamp = Date.now();
  const shard = Math.floor(timestamp / 60000); // 1-minute shards

  await env.LOGS.put(`logs/${shard}.txt`, logEntry, {
    customMetadata: { timestamp: timestamp.toString() }
  });
  // Different keys = no rate limiting
}

// ✅ ALTERNATIVE: Use Durable Objects for append operations
// Durable Objects can handle high-frequency updates to same state

// ✅ ALTERNATIVE: Use Queues + batch processing
// Buffer writes and batch them with unique keys
```

**Source**: [R2 Limits Documentation](https://developers.cloudflare.com/r2/platform/limits/)

### R2.dev Domain Rate Limiting

🚨 **CRITICAL**: The `{bucket}.{account}.r2.cloudflarestorage.com` (r2.dev) domain is **NOT for production use**.

**r2.dev limitations:**
- ❌ Variable rate limiting (starts at ~hundreds of requests/second)
- ❌ Bandwidth throttling
- ❌ No SLA or performance guarantees
- ❌ You'll receive 429 Too Many Requests under load

**For production: ALWAYS use custom domains**

```typescript
// ❌ NOT for production - r2.dev endpoint
const publicUrl = `https://${bucketName}.${accountId}.r2.cloudflarestorage.com/${key}`;
// This will be rate limited in production

// ✅ Production: Custom domain
const productionUrl = `https://cdn.example.com/${key}`;

// Setup custom domain:
// 1. Dashboard → R2 → Bucket → Settings → Custom Domains
// 2. Add your domain (e.g., cdn.example.com)
// 3. Benefits:
//    - No rate limiting beyond account limits
//    - Cloudflare Cache support
//    - Custom cache rules via Workers
//    - Full CDN features
```

**r2.dev is ONLY for testing/development. Custom domains are required for production.**

**Source**: [R2 Limits Documentation](https://developers.cloudflare.com/r2/platform/limits/)

---

## Best Practices Summary

**Always Do:**
- Set `contentType` for all uploads
- Use batch delete for multiple objects (up to 1000)
- Set cache headers for static assets
- Use presigned URLs for large client uploads (S3 domain only)
- Use multipart for files >100MB
- Set CORS before browser uploads (use CLI format for wrangler)
- Set expiry times on presigned URLs (1-24 hours)
- Use `head()` when you only need metadata
- Use conditional operations to prevent overwrites
- Use custom domains for production (never r2.dev)
- Shard writes across keys to avoid rate limits
- Use `include` parameter with `list()` to get metadata
- Implement retry logic with exponential backoff for 5xx errors

**Never Do:**
- Never expose R2 access keys in client-side code
- Never skip `contentType` (files download as binary)
- Never delete in loops (use batch delete)
- Never skip CORS for browser uploads
- Never use multipart for small files (<5MB)
- Never delete >1000 keys in single call
- Never skip presigned URL expiry (security risk)
- Never use r2.dev domain for production (rate limited)
- Never use presigned URLs with custom domains (use S3 domain)
- Never write to same key at high frequency (causes 429)
- Never use "Object Read & Write" tokens for wrangler (use "Admin Read & Write")

### Multi-Tenant Architecture

With the bucket limit increased to **1 million buckets per account**, per-tenant buckets are now viable for large-scale applications.

```typescript
// Option 1: Per-tenant buckets (now scalable to 1M tenants)
const bucketName = `tenant-${tenantId}`;
const bucket = env[bucketName]; // Dynamic binding

// Option 2: Key prefixing (still preferred for most use cases)
await env.MY_BUCKET.put(`tenants/${tenantId}/file.txt`, data);

// Choose based on:
// - Per-tenant buckets: Strong isolation, separate billing/quotas
// - Key prefixing: Simpler, fewer resources, easier to manage
```

**Source**: [R2 Limits Documentation](https://developers.cloudflare.com/r2/platform/limits/)

---

## Known Issues Prevented

This skill prevents **13** documented issues:

| Issue # | Issue | Error | Prevention |
|---------|-------|-------|------------|
| **#1** | **CORS errors in browser** | Browser can't upload/download | Configure CORS in bucket settings, use correct CLI format |
| **#2** | **Files download as binary** | Missing content-type | Always set `httpMetadata.contentType` on upload |
| **#3** | **Presigned URL expiry** | URLs never expire | Always set `X-Amz-Expires` (1-24 hours) |
| **#4** | **Multipart upload limits** | Parts exceed limits | Keep parts 5MB-100MB, max 10,000 parts |
| **#5** | **Bulk delete limits** | >1000 keys fails | Chunk deletes into batches of 1000 |
| **#6** | **Custom metadata overflow** | Exceeds 2KB limit | Keep custom metadata under 2KB |
| **#7** | **list() metadata missing** | `httpMetadata` undefined | Use `include: ['httpMetadata', 'customMetadata']` parameter ([Issue #10870](https://github.com/cloudflare/workers-sdk/issues/10870)) |
| **#8** | **CORS format confusion** | "Must contain 'rules' array" | Use CLI format with `rules` wrapper for wrangler ([Issue #10076](https://github.com/cloudflare/workers-sdk/issues/10076)) |
| **#9** | **API token 403 errors** | "Failed to fetch - 403" | Use "Admin Read & Write" not "Object Read & Write" for wrangler ([Issue #9235](https://github.com/cloudflare/workers-sdk/issues/9235)) |
| **#10** | **r2.dev rate limiting** | HTTP 429 in production | Use custom domains, never r2.dev for production ([R2 Limits](https://developers.cloudflare.com/r2/platform/limits/)) |
| **#11** | **Concurrent write 429s** | Same key written frequently | Shard writes across different keys ([R2 Limits](https://developers.cloudflare.com/r2/platform/limits/)) |
| **#12** | **Presigned URL domain error** | Presigned URLs fail | Use S3 domain only, not custom domains ([Community](https://ruanmartinelli.com/blog/cloudflare-r2-pre-signed-urls/)) |
| **#13** | **Platform outages** | 5xx errors during outages | Implement retry logic with exponential backoff ([Feb 6](https://blog.cloudflare.com/cloudflare-incident-on-february-6-2025/), [Mar 21](https://blog.cloudflare.com/cloudflare-incident-march-21-2025/)) |

---

## Development Best Practices

### Local R2 Storage Cleanup

⚠️ **Local R2 DELETE operations don't cleanup blob files**. When using `wrangler dev`, deleted objects remain in `.wrangler/state/v3/r2/{bucket-name}/blobs/`, causing local storage to grow indefinitely.

```bash
# Symptom: .wrangler/state grows large during development
du -sh .wrangler/state/v3/r2/

# Fix: Manually cleanup local R2 storage
rm -rf .wrangler/state/v3/r2/

# Alternative: Use remote R2 for development
wrangler dev --remote
```

**Source**: [GitHub Issue #10795](https://github.com/cloudflare/workers-sdk/issues/10795)

### Remote R2 Access Issues

⚠️ **Local dev with `--remote` can have unreliable `.get()` operations**. Some users report `get()` returning undefined despite `put()` working correctly.

```bash
# If experiencing issues with remote R2 in local dev:

# Option 1: Use local buckets instead (recommended)
wrangler dev  # No --remote flag

# Option 2: Deploy to preview environment for testing
wrangler deploy --env preview

# Option 3: Add retry logic if must use --remote
async function safeGet(bucket: R2Bucket, key: string) {
  for (let i = 0; i < 3; i++) {
    const obj = await bucket.get(key);
    if (obj && obj.body) return obj;
    await new Promise(r => setTimeout(r, 1000));
  }
  throw new Error('Failed to get object after retries');
}
```

**Source**: [GitHub Issue #8868](https://github.com/cloudflare/workers-sdk/issues/8868) (Community-sourced)

---

## Wrangler Commands Reference

```bash
# Bucket management
wrangler r2 bucket create <BUCKET_NAME>
wrangler r2 bucket list
wrangler r2 bucket delete <BUCKET_NAME>

# Object management
wrangler r2 object put <BUCKET_NAME>/<KEY> --file=<FILE_PATH>
wrangler r2 object get <BUCKET_NAME>/<KEY> --file=<OUTPUT_PATH>
wrangler r2 object delete <BUCKET_NAME>/<KEY>

# List objects
wrangler r2 object list <BUCKET_NAME>
wrangler r2 object list <BUCKET_NAME> --prefix="folder/"
```

---

## Official Documentation

- **R2 Overview**: https://developers.cloudflare.com/r2/
- **Get Started**: https://developers.cloudflare.com/r2/get-started/
- **Workers API**: https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
- **Multipart Upload**: https://developers.cloudflare.com/r2/api/workers/workers-multipart-usage/
- **Presigned URLs**: https://developers.cloudflare.com/r2/api/s3/presigned-urls/
- **CORS Configuration**: https://developers.cloudflare.com/r2/buckets/cors/
- **Public Buckets**: https://developers.cloudflare.com/r2/buckets/public-buckets/

---

**Ready to store with R2!** 🚀

**Last verified**: 2026-01-20 | **Skill version**: 2.0.0 | **Changes**: Added 7 new known issues from community research (list() metadata, CORS format confusion, API token permissions, r2.dev rate limiting, concurrent write limits, presigned URL domain requirements, platform outage retry patterns). Enhanced retry logic for 5xx errors, added development best practices section, documented bucket limit increase to 1M.
