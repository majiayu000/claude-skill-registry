---
name: cloudflare-images
description: This skill should be used when the user asks to "upload images to Cloudflare", "implement direct creator upload", "configure image transformations", "optimize WebP/AVIF", "create image variants", "generate signed URLs", "add image watermarks", "integrate with Next.js/Remix", "configure webhooks", "debug CORS errors", "troubleshoot error 5408/9401-9413", or "build responsive images with Cloudflare Images API".

  Keywords: cloudflare images, image upload cloudflare, imagedelivery.net, cloudflare image transformations, /cdn-cgi/image/, direct creator upload, image variants, cf.image workers, signed urls images, flexible variants, webp avif conversion, responsive images cloudflare, error 5408, error 9401, error 9403, CORS direct upload, multipart/form-data, image optimization cloudflare, image watermarks, webhooks images, nextjs cloudflare images, remix cloudflare images, custom domains images, content credentials, c2pa
license: MIT
metadata:
  version: "3.0.0"
  last_verified: "2025-12-27"
  workers_types_version: "4.20250110.0"
  typescript_version: "5.7.2"
  wrangler_version: "3.91.0"
  production_tested: true
  token_savings: "~65%"
  errors_prevented: 10
  templates_included: 16
  references_included: 16
  agents_included: 3
  commands_included: 3
  examples_included: 3
  diagrams_included: 3
  scripts_included: 5
---

# Cloudflare Images

**Status**: Production Ready ✅ | **Version**: 3.0.0 | **Last Verified**: 2025-12-27

---

## What Is Cloudflare Images?

Two powerful features:

1. **Images API**: Upload, store, serve images globally
2. **Image Transformations**: Resize/optimize ANY image

**Key benefits:**
- Global CDN delivery
- Automatic WebP/AVIF conversion
- Up to 100 variants
- Direct creator upload (no API keys in frontend)
- Signed URLs for private images
- Transform any image via URL or Workers

---

## Quick Start (5 Minutes)

### 1. Enable Cloudflare Images

Dashboard → **Images** → **Enable**

Get your **Account ID** and create **API token** (Cloudflare Images: Edit permission)

### 2. Upload Image

```bash
curl --request POST \
  --url https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/images/v1 \
  --header 'Authorization: Bearer <API_TOKEN>' \
  --header 'Content-Type: multipart/form-data' \
  --form 'file=@./image.jpg'
```

**CRITICAL:** Use `multipart/form-data`, not JSON

### 3. Serve Image

```html
<img src="https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/public" />
```

### 4. Enable Transformations

Dashboard → **Images** → **Transformations** → **Enable for zone**

Transform ANY image:

```html
<img src="/cdn-cgi/image/width=800,quality=85/uploads/photo.jpg" />
```

### 5. Transform via Workers

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    return fetch("https://example.com/image.jpg", {
      cf: {
        image: {
          width: 800,
          quality: 85,
          format: "auto"  // WebP/AVIF
        }
      }
    });
  }
};
```

**Load `references/setup-guide.md` for complete walkthrough.**

---

## The 3 Core Features

### Feature 1: Images API (Upload & Storage)

**Upload methods:**
1. File upload (server-side)
2. Upload via URL (ingest from external)
3. Direct creator upload (user uploads, no API keys)

**Load `templates/upload-api-basic.ts` for file upload example.**
**Load `references/direct-upload-complete-workflow.md` for user uploads.**

### Feature 2: Image Transformations

Optimize ANY image (uploaded or external).

**Methods:**
1. URL: `/cdn-cgi/image/width=800,quality=85/path/to/image.jpg`
2. Workers: `cf.image` fetch option

**Load `references/transformation-options.md` for all options.**
**Load `templates/transform-via-workers.ts` for Workers example.**

### Feature 3: Variants

Predefined transformations (up to 100).

**Examples:**
- `thumbnail`: 200x200, fit=cover
- `hero`: 1920x1080, quality=90
- `mobile`: 640, quality=75

**Load `references/variants-guide.md` for complete guide.**

---

## Critical Rules

### Always Do ✅

1. **Use multipart/form-data** for uploads (not JSON)
2. **Enable transformations for zones** before using `/cdn-cgi/image/`
3. **Use direct creator upload** for user uploads (don't expose API tokens)
4. **Set CORS headers** for direct uploads from browser
5. **Use signed URLs** for private images
6. **Configure variants** for common sizes (avoid dynamic transformations)
7. **Use format=auto** for automatic WebP/AVIF
8. **Handle error codes** (9401, 9403, 9413, 5408)
9. **Set quality=85** for optimal size/quality balance
10. **Use fit=cover** for consistent aspect ratios

### Never Do ❌

1. **Never expose API tokens** in frontend code
2. **Never use JSON encoding** for file uploads
3. **Never skip CORS configuration** for direct uploads
4. **Never exceed 100 variants** (hard limit)
5. **Never use transformations without enabling for zone**
6. **Never hardcode account IDs** in public code
7. **Never skip error handling** (uploads can fail)
8. **Never use quality >90** (diminishing returns)
9. **Never skip image validation** (size, format, dimensions)
10. **Never use transformations on non-proxied requests**

---

## Top 2 Use Cases

### Use Case 1: User Profile Pictures

Direct creator upload pattern for user-uploaded images:

```typescript
// Backend: Generate upload URL
const response = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/images/v2/direct_upload`,
  { method: 'POST', headers: { 'Authorization': `Bearer ${API_TOKEN}` } }
);
const { result } = await response.json();
return Response.json({ uploadURL: result.uploadURL });

// Frontend: Upload file
const formData = new FormData();
formData.append('file', file);
await fetch(uploadURL, { method: 'POST', body: formData });
```

**Load `templates/direct-creator-upload-backend.ts` for complete example.**
**See `examples/basic-upload/` for complete working project.**

### Use Case 2: Responsive Images

Responsive images with srcset for optimal performance:

```html
<img
  srcset="
    https://imagedelivery.net/abc/xyz/width=400 400w,
    https://imagedelivery.net/abc/xyz/width=800 800w,
    https://imagedelivery.net/abc/xyz/width=1200 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="https://imagedelivery.net/abc/xyz/width=800"
/>
```

**Load `templates/responsive-images-srcset.html` for complete example.**
**See `examples/responsive-gallery/` for complete working project.**

**Additional Use Cases:**
- **Transform Existing Images**: Load `references/transformation-options.md`
- **Private Images**: Load `references/signed-urls-guide.md` or see `examples/private-images/`
- **Batch Upload**: Load `templates/batch-upload.ts`
- **Framework Integration**: Load `references/framework-integration.md` for Next.js, Remix, Astro
- **Watermarking**: Load `references/overlays-watermarks.md` and `templates/overlay-watermark.ts`
- **Custom Domains**: Load `references/custom-domains.md`
- **Webhooks**: Load `references/webhooks-guide.md` and `templates/webhook-handler.ts`

---

## Top 2 Errors Prevented

### Error 1: CORS Issues with Direct Upload

**Problem:** Browser blocks direct upload from your domain.

**Solution:** Configure CORS headers when generating upload URL:

```typescript
const response = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/images/v2/direct_upload`,
  {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${API_TOKEN}` },
    body: JSON.stringify({
      requireSignedURLs: false,
      metadata: { source: 'user-upload' }
    })
  }
);
```

### Error 2: Multipart Form Data Encoding

**Problem:** JSON encoding fails for file uploads (must use multipart/form-data).

**Solution:**

```typescript
// ✅ CORRECT
const formData = new FormData();
formData.append('file', file);
await fetch(uploadURL, { method: 'POST', body: formData });

// ❌ WRONG
const json = JSON.stringify({ file: base64File });
```

**Additional Common Errors:**
- **Error 9401** (Transformations not enabled): Load `references/top-errors.md`
- **Error 9403** (Invalid transformation): Load `references/top-errors.md`
- **Error 9413** (Variant limit exceeded): Load `references/top-errors.md`
- **Error 5408** (Upload timeout): Load `references/top-errors.md`
- **Missing requireSignedURLs**: Load `references/signed-urls-guide.md`

**Load `references/top-errors.md` for all 10 errors with complete solutions.**

---

## When to Load References

### Core References

**Load `references/setup-guide.md` when:**
- First-time Cloudflare Images setup
- Need step-by-step walkthrough

**Load `references/api-reference.md` when:**
- Need complete API documentation
- All endpoints and parameters

**Load `references/top-errors.md` when:**
- Encountering any error code (5408, 9401-9413)
- Troubleshooting upload/transformation issues

### Upload References

**Load `references/direct-upload-complete-workflow.md` when:**
- Implementing user uploads
- Need frontend + backend example
- Configuring CORS

**Load `references/signed-urls-guide.md` when:**
- Implementing private images with access control
- Need HMAC-SHA256 signature generation

**Load `references/webhooks-guide.md` when:**
- Processing upload completion events
- Implementing webhook handlers with signature verification

### Transformation References

**Load `references/transformation-options.md` when:**
- Need complete transformation reference
- Exploring all fit/format/effect options

**Load `references/format-optimization.md` when:**
- Optimizing format selection (WebP/AVIF)
- Quality vs size tradeoffs

**Load `references/polish-compression.md` when:**
- Need details on Lossless/Lossy/WebP compression modes
- Metadata handling (EXIF removal)

**Load `references/overlays-watermarks.md` when:**
- Adding text or logo watermarks
- Implementing branding/copyright protection

### Advanced Features

**Load `references/variants-guide.md` when:**
- Creating/managing variants (up to 100 max)
- Need flexible variants vs named variants

**Load `references/responsive-images-patterns.md` when:**
- Building responsive images with srcset
- Implementing picture element for art direction

**Load `references/framework-integration.md` when:**
- Integrating with Next.js, Remix, Astro, SvelteKit
- Need framework-specific patterns and loaders

**Load `references/custom-domains.md` when:**
- Serving images from branded domains
- CNAME configuration and SSL setup

**Load `references/content-credentials.md` when:**
- Preserving EXIF/IPTC metadata
- Implementing C2PA Content Credentials for authenticity

**Load `references/sourcing-kit.md` when:**
- Migrating from Cloudinary, Imgix, or S3
- Bulk import from external CDNs

---

## Using Bundled Resources

### References (16 reference files)

**Core**: setup-guide.md, api-reference.md, top-errors.md

**Upload**: direct-upload-complete-workflow.md, signed-urls-guide.md, webhooks-guide.md

**Transform**: transformation-options.md, format-optimization.md, polish-compression.md, overlays-watermarks.md

**Advanced**: variants-guide.md, responsive-images-patterns.md, framework-integration.md, custom-domains.md, content-credentials.md, sourcing-kit.md

### Templates (16 template files)

**Upload**: upload-api-basic.ts, upload-via-url.ts, direct-creator-upload-backend.ts, direct-creator-upload-frontend.html, batch-upload.ts

**Transform**: transform-via-url.ts, transform-via-workers.ts, overlay-watermark.ts

**Variants**: variants-management.ts, signed-urls-generation.ts, responsive-images-srcset.html

**Integration**: nextjs-integration.tsx, remix-integration.tsx, webhook-handler.ts

**Config**: wrangler-images-binding.jsonc, package.json

### Agents (3 autonomous agents)

- **troubleshooting-agent** - Diagnose upload/transformation errors (5408, 9401-9413)
- **upload-workflow-agent** - Guide complete upload implementation (frontend + backend)
- **optimization-agent** - Recommend image optimization strategies

Use: `/agent <agent-name>` or let Claude auto-detect when relevant

### Commands (3 slash commands)

- **/check-images** - Quick API health check and configuration validation
- **/validate-config** - Validate wrangler.jsonc bindings and configuration
- **/generate-variant** - Interactive variant generator

Use: `/<command-name>`

### Examples (3 complete working projects)

- **basic-upload/** - Minimal upload implementation with Hono + Workers
- **responsive-gallery/** - Responsive image gallery with srcset and lazy loading
- **private-images/** - Signed URLs with time-based expiry and access control

Clone and run: `cd examples/<example-name> && npm install && npm run dev`

### Architecture Diagrams (3 diagrams)

- **direct-upload-workflow.md** - Sequence diagram of direct creator upload flow
- **transformation-pipeline.md** - Flowchart showing transformation processing
- **variants-structure.md** - Named vs flexible variants comparison

View in: `assets/diagrams/`

### Utility Scripts (5 scripts)

- **test-upload.sh** - Test API connectivity with sample image upload
- **generate-signed-url.sh** - CLI tool to generate signed URLs with expiry
- **validate-variants.sh** - List all variants and check variant count (max 100)
- **analyze-usage.sh** - Query API for storage usage and estimated costs
- **check-versions.sh** - Verify package versions are current

Run: `./scripts/<script-name>.sh` (requires CF_ACCOUNT_ID and CF_API_TOKEN in .env)

---

## Pricing

**Images API**: $5/100k stored, $1/100k delivered
**Transformations**: $0.50/1k (100k/month free per zone)
**Direct Upload**: Included in API pricing

---

## Official Documentation

- **Images Overview**: https://developers.cloudflare.com/images/
- **Upload API**: https://developers.cloudflare.com/images/upload-images/
- **Transformations**: https://developers.cloudflare.com/images/transform-images/
- **Direct Creator Upload**: https://developers.cloudflare.com/images/upload-images/direct-creator-upload/
- **Variants**: https://developers.cloudflare.com/images/manage-images/create-variants/

