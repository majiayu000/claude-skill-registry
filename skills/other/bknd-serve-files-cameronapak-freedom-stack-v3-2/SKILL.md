---
name: bknd-serve-files
description: Use when serving uploaded files to users. Covers API-proxied file serving, direct storage URLs (S3/R2/Cloudinary), CDN configuration, public file URLs, caching headers, image optimization with Cloudinary, and serving files in frontend applications.
---

# Serve Files

Serve uploaded files from Bknd storage to users via API proxy or direct storage URLs.

## Prerequisites

- Media module enabled in Bknd config
- Storage adapter configured (S3, R2, Cloudinary, or local)
- Files uploaded via `bknd-file-upload` skill
- For CDN: storage provider with CDN support (S3/R2/Cloudinary)

## When to Use UI Mode

- Admin panel > Media section > view/preview files
- Copy file URLs from admin interface
- Quick verification that files are accessible

## When to Use Code Mode

- Build file URLs programmatically
- Configure CDN or custom domains
- Implement image optimization
- Access control for file downloads

## File Serving Methods

Bknd supports two approaches to serve files:

| Method | Use Case | Performance | Control |
|--------|----------|-------------|---------|
| API Proxy | Simple setup, private files | Moderate | Full (auth, permissions) |
| Direct URL | High traffic, public files | Best (CDN) | Limited (bucket ACLs) |

## Step-by-Step: API Proxy (via Bknd)

Files served through Bknd API at `/api/media/file/{filename}`.

### Step 1: Get File URL

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// Build file URL
const fileUrl = `${api.host}/api/media/file/image.png`;
// "http://localhost:7654/api/media/file/image.png"
```

### Step 2: Display in Frontend

```tsx
function Image({ filename }) {
  const { api } = useApp();
  const src = `${api.host}/api/media/file/${filename}`;

  return <img src={src} alt="" />;
}
```

### Step 3: Download File (SDK)

```typescript
// Get as File object
const file = await api.media.download("image.png");

// Get as stream (for large files)
const stream = await api.media.getFileStream("image.png");
```

### Step 4: Verify Access

```bash
# Test file access
curl -I http://localhost:7654/api/media/file/image.png

# Response includes:
# Content-Type: image/png
# Content-Length: 12345
# ETag: "abc123..."
```

## Step-by-Step: Direct Storage URLs

Serve files directly from S3/R2/Cloudinary for better performance.

### S3/R2 Direct URLs

```typescript
// S3 URL pattern
const s3Url = `https://${bucket}.s3.${region}.amazonaws.com/${filename}`;
// "https://mybucket.s3.us-east-1.amazonaws.com/image.png"

// R2 URL pattern (public bucket)
const r2Url = `https://${customDomain}/${filename}`;
// "https://media.myapp.com/image.png"
```

### Cloudinary Direct URLs

Cloudinary provides automatic CDN and transformations:

```typescript
// Basic URL
const cloudinaryUrl = `https://res.cloudinary.com/${cloudName}/image/upload/${filename}`;

// With transformations
const optimizedUrl = `https://res.cloudinary.com/${cloudName}/image/upload/w_800,q_auto,f_auto/${filename}`;
```

### Building URLs in Code

```typescript
// Helper to get direct URL based on adapter type
function getFileUrl(filename: string, config: MediaConfig): string {
  const { adapter } = config;

  switch (adapter.type) {
    case "s3":
      // S3/R2 URL from configured endpoint
      return `${adapter.config.url}/${filename}`;

    case "cloudinary":
      return `https://res.cloudinary.com/${adapter.config.cloud_name}/image/upload/${filename}`;

    case "local":
      // Always use API proxy for local
      return `/api/media/file/${filename}`;

    default:
      return `/api/media/file/${filename}`;
  }
}
```

## CDN Configuration

### Cloudflare R2 with Custom Domain

1. **Create R2 bucket** in Cloudflare dashboard

2. **Enable public access** on bucket

3. **Configure custom domain** (Cloudflare DNS):
   - Add CNAME: `media.yourapp.com` -> `<bucket>.<account>.r2.dev`

4. **Use in Bknd config:**

```typescript
export default defineConfig({
  media: {
    enabled: true,
    adapter: {
      type: "s3",
      config: {
        access_key: process.env.R2_ACCESS_KEY,
        secret_access_key: process.env.R2_SECRET_KEY,
        url: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com/${process.env.R2_BUCKET}`,
      },
    },
  },
});
```

5. **Serve files via custom domain:**

```typescript
const publicUrl = `https://media.yourapp.com/${filename}`;
```

### AWS S3 with CloudFront

1. **Create S3 bucket** with public read (or CloudFront OAI)

2. **Create CloudFront distribution:**
   - Origin: S3 bucket
   - Cache policy: CachingOptimized
   - Custom domain (optional)

3. **Use CloudFront URL:**

```typescript
const cdnUrl = `https://d123abc.cloudfront.net/${filename}`;
// Or with custom domain
const cdnUrl = `https://cdn.yourapp.com/${filename}`;
```

### Cloudinary (Built-in CDN)

Cloudinary includes global CDN automatically:

```typescript
export default defineConfig({
  media: {
    enabled: true,
    adapter: {
      type: "cloudinary",
      config: {
        cloud_name: "your-cloud-name",
        api_key: process.env.CLOUDINARY_API_KEY,
        api_secret: process.env.CLOUDINARY_API_SECRET,
      },
    },
  },
});
```

Files served from `res.cloudinary.com` with global CDN.

## Image Optimization

### Cloudinary Transformations

```typescript
// Build optimized image URL
function getOptimizedImage(filename: string, options: {
  width?: number;
  height?: number;
  quality?: "auto" | number;
  format?: "auto" | "webp" | "avif" | "jpg" | "png";
  crop?: "fill" | "fit" | "scale" | "thumb";
} = {}) {
  const cloudName = process.env.CLOUDINARY_CLOUD_NAME;
  const transforms: string[] = [];

  if (options.width) transforms.push(`w_${options.width}`);
  if (options.height) transforms.push(`h_${options.height}`);
  if (options.quality) transforms.push(`q_${options.quality}`);
  if (options.format) transforms.push(`f_${options.format}`);
  if (options.crop) transforms.push(`c_${options.crop}`);

  const transformStr = transforms.length > 0 ? transforms.join(",") + "/" : "";

  return `https://res.cloudinary.com/${cloudName}/image/upload/${transformStr}${filename}`;
}

// Usage
const thumb = getOptimizedImage("avatar.png", {
  width: 100,
  height: 100,
  crop: "fill",
  quality: "auto",
  format: "auto",
});
// "https://res.cloudinary.com/mycloud/image/upload/w_100,h_100,c_fill,q_auto,f_auto/avatar.png"
```

### Common Transformation Patterns

```typescript
// Responsive images
const srcSet = [400, 800, 1200].map(w =>
  `${getOptimizedImage(filename, { width: w, format: "auto" })} ${w}w`
).join(", ");

// Thumbnail generation
const thumb = getOptimizedImage(filename, {
  width: 150,
  height: 150,
  crop: "thumb",
});

// Automatic format (WebP/AVIF when supported)
const optimized = getOptimizedImage(filename, {
  quality: "auto",
  format: "auto",
});
```

## React Integration

### Image Component with Fallback

```tsx
function StoredImage({ filename, alt, ...props }) {
  const { api } = useApp();
  const [error, setError] = useState(false);

  // API proxy URL as fallback
  const apiUrl = `${api.host}/api/media/file/${filename}`;

  // Direct CDN URL (configure based on your adapter)
  const cdnUrl = `https://media.yourapp.com/${filename}`;

  return (
    <img
      src={error ? apiUrl : cdnUrl}
      alt={alt}
      onError={() => setError(true)}
      {...props}
    />
  );
}
```

### Responsive Image Component

```tsx
function ResponsiveImage({ filename, alt, sizes = "100vw" }) {
  const cloudName = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME;
  const base = `https://res.cloudinary.com/${cloudName}/image/upload`;

  const srcSet = [400, 800, 1200, 1600].map(w =>
    `${base}/w_${w},q_auto,f_auto/${filename} ${w}w`
  ).join(", ");

  return (
    <img
      src={`${base}/w_800,q_auto,f_auto/${filename}`}
      srcSet={srcSet}
      sizes={sizes}
      alt={alt}
      loading="lazy"
    />
  );
}
```

### File Download Button

```tsx
function DownloadButton({ filename, label }) {
  const { api } = useApp();
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const file = await api.media.download(filename);

      // Create download link
      const url = URL.createObjectURL(file);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <button onClick={handleDownload} disabled={downloading}>
      {downloading ? "Downloading..." : label || "Download"}
    </button>
  );
}
```

## Caching Configuration

### S3/R2 Cache Headers

Set cache headers when uploading:

```typescript
// Custom adapter with cache headers (advanced)
// S3 adapter doesn't expose this directly; configure via bucket policy
// or CloudFront cache behaviors
```

### Cloudflare R2 Cache Rules

In Cloudflare dashboard:
1. Go to Caching > Cache Rules
2. Create rule for your R2 subdomain
3. Set Edge TTL (e.g., 1 year for immutable assets)

### API Proxy Caching

Bknd's API proxy supports standard HTTP caching:

```bash
# Client can use conditional requests
curl -H "If-None-Match: \"abc123\"" \
  http://localhost:7654/api/media/file/image.png

# Returns 304 Not Modified if unchanged
```

## Access Control

### Public Files (No Auth)

Configure default role with media.read permission:

```typescript
export default defineConfig({
  auth: {
    guard: {
      roles: {
        anonymous: {
          is_default: true,
          permissions: {
            "media.read": true,  // Public read access
          },
        },
      },
    },
  },
});
```

### Private Files (Auth Required)

Remove media.read from anonymous:

```typescript
export default defineConfig({
  auth: {
    guard: {
      roles: {
        user: {
          permissions: {
            "media.read": true,
            "media.create": true,
          },
        },
        // No anonymous role, or no media.read permission
      },
    },
  },
});
```

Access requires auth:

```bash
# Fails without auth
curl http://localhost:7654/api/media/file/private.pdf
# 401 Unauthorized

# Works with auth
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:7654/api/media/file/private.pdf
```

### Signed URLs (Time-Limited Access)

For S3/R2, generate presigned URLs:

```typescript
// Custom endpoint for signed URLs (advanced)
// Requires S3 SDK directly, not through Bknd adapter
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

async function getSignedDownloadUrl(filename: string): Promise<string> {
  const client = new S3Client({ /* config */ });
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: filename,
  });
  return getSignedUrl(client, command, { expiresIn: 3600 }); // 1 hour
}
```

## REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/media/file/:filename` | Download/view file |
| GET | `/api/media/files` | List all files |

### Request Headers

| Header | Description |
|--------|-------------|
| `Authorization` | Bearer token (if auth required) |
| `If-None-Match` | ETag for conditional request |
| `Range` | Byte range for partial download |

### Response Headers

| Header | Description |
|--------|-------------|
| `Content-Type` | File MIME type |
| `Content-Length` | File size in bytes |
| `ETag` | File hash for caching |
| `Accept-Ranges` | Indicates range support |

## Common Pitfalls

### 404 File Not Found

**Problem:** File URL returns 404.

**Causes:**
1. Filename doesn't exist
2. Wrong path/case sensitivity
3. File was deleted

**Fix:** Verify file exists:

```typescript
const { data: files } = await api.media.listFiles();
const exists = files.some(f => f.key === filename);
```

### CORS Errors on Direct S3 URL

**Problem:** Browser blocks direct S3 access.

**Fix:** Configure CORS on S3 bucket:

```json
{
  "CORSRules": [{
    "AllowedOrigins": ["https://yourapp.com"],
    "AllowedMethods": ["GET"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }]
}
```

### Slow File Serving

**Problem:** Files load slowly via API proxy.

**Fix:** Use direct storage URLs with CDN:

```typescript
// Instead of API proxy
const slow = "/api/media/file/image.png";

// Use direct CDN URL
const fast = "https://cdn.yourapp.com/image.png";
```

### Mixed Content (HTTP/HTTPS)

**Problem:** HTTPS page loading HTTP file URLs.

**Fix:** Ensure storage URL uses HTTPS:

```typescript
// WRONG
url: "http://bucket.s3.amazonaws.com",

// CORRECT
url: "https://bucket.s3.amazonaws.com",
```

### Large File Download Fails

**Problem:** Download times out or memory error.

**Fix:** Use streaming for large files:

```typescript
// Stream instead of loading into memory
const stream = await api.media.getFileStream("large-file.zip");

// Or direct download link
const downloadUrl = `${api.host}/api/media/file/large-file.zip`;
window.location.href = downloadUrl;
```

### Cloudinary File Not Found

**Problem:** Cloudinary returns 404 for uploaded file.

**Cause:** Cloudinary uses eventual consistency; file not yet indexed.

**Fix:** Wait briefly or use upload response URL directly:

```typescript
const { data } = await api.media.upload(file);
// Use data.name immediately rather than re-fetching
```

## Verification

Test file serving setup:

```typescript
async function testFileServing() {
  const filename = "test-image.png";

  // 1. Verify file exists
  const { data: files } = await api.media.listFiles();
  const file = files.find(f => f.key === filename);
  console.log("File exists:", !!file);

  // 2. Test API proxy
  const apiUrl = `${api.host}/api/media/file/${filename}`;
  const apiRes = await fetch(apiUrl);
  console.log("API proxy status:", apiRes.status);
  console.log("Content-Type:", apiRes.headers.get("content-type"));

  // 3. Test conditional request
  const etag = apiRes.headers.get("etag");
  if (etag) {
    const conditionalRes = await fetch(apiUrl, {
      headers: { "If-None-Match": etag },
    });
    console.log("Conditional request:", conditionalRes.status === 304 ? "304 (cached)" : conditionalRes.status);
  }

  // 4. Test SDK download
  const downloadedFile = await api.media.download(filename);
  console.log("SDK download:", downloadedFile.name, downloadedFile.size);
}
```

## DOs and DON'Ts

**DO:**
- Use CDN (Cloudinary/R2/CloudFront) for public high-traffic files
- Set proper cache headers for static assets
- Use API proxy for private/auth-required files
- Implement lazy loading for images
- Use responsive images with srcSet
- Handle file not found gracefully

**DON'T:**
- Expose private files via public S3 URLs
- Serve large files without streaming
- Hardcode storage URLs (use config/env)
- Forget CORS configuration for direct access
- Use local adapter in production
- Skip error handling for missing files

## Related Skills

- **bknd-file-upload** - Upload files to storage
- **bknd-storage-config** - Configure storage backends
- **bknd-assign-permissions** - Set media.read permission
- **bknd-public-vs-auth** - Configure public vs authenticated access
