---
name: bknd-storage-config
description: Use when configuring storage backends for file uploads. Covers S3-compatible storage (AWS S3, Cloudflare R2, DigitalOcean Spaces), Cloudinary media storage, local filesystem adapter for development, adapter configuration options, environment variables, and production storage setup.
---

# Storage Configuration

Configure storage backends for Bknd's media module.

## Prerequisites

- `bknd` package installed
- For S3: bucket created with appropriate permissions
- For Cloudinary: account with API credentials
- For R2: Cloudflare Workers environment with R2 binding

## When to Use UI Mode

- Admin panel doesn't support storage configuration
- Storage must be configured in code

## When to Use Code Mode

- All storage configuration (required)
- Setting up different adapters per environment
- Production storage with credentials

## Storage Adapter Overview

| Adapter | Type | Use Case |
|---------|------|----------|
| `s3` | S3-compatible | AWS S3, Cloudflare R2 (external), DigitalOcean Spaces, MinIO |
| `cloudinary` | Media-optimized | Image/video transformations, CDN delivery |
| `local` | Filesystem | Development only (Node.js/Bun runtime) |
| `r2` | Cloudflare R2 | Cloudflare Workers with R2 binding |

## Step-by-Step: S3 Adapter

### Step 1: Create S3 Bucket

Create bucket in AWS console or via CLI:

```bash
aws s3 mb s3://my-app-uploads --region us-east-1
```

### Step 2: Configure CORS (if browser uploads)

```json
{
  "CORSRules": [{
    "AllowedOrigins": ["https://yourapp.com"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"]
  }]
}
```

### Step 3: Get Access Credentials

Create IAM user with S3 access and get:
- Access Key ID
- Secret Access Key

### Step 4: Configure Bknd

```typescript
import { defineConfig } from "bknd";

export default defineConfig({
  media: {
    enabled: true,
    adapter: {
      type: "s3",
      config: {
        access_key: process.env.S3_ACCESS_KEY,
        secret_access_key: process.env.S3_SECRET_KEY,
        url: "https://my-bucket.s3.us-east-1.amazonaws.com",
      },
    },
  },
});
```

### Step 5: Add Environment Variables

```bash
# .env
S3_ACCESS_KEY=AKIA...
S3_SECRET_KEY=wJalr...
```

## S3 URL Formats

Different S3-compatible services use different URL formats:

```typescript
// AWS S3
url: "https://{bucket}.s3.{region}.amazonaws.com"
// Example: "https://my-bucket.s3.us-east-1.amazonaws.com"

// Cloudflare R2 (external access via S3 API)
url: "https://{account_id}.r2.cloudflarestorage.com/{bucket}"
// Example: "https://abc123.r2.cloudflarestorage.com/my-bucket"

// DigitalOcean Spaces
url: "https://{bucket}.{region}.digitaloceanspaces.com"
// Example: "https://my-bucket.nyc3.digitaloceanspaces.com"

// MinIO (self-hosted)
url: "http://localhost:9000/{bucket}"
```

## Step-by-Step: Cloudinary Adapter

### Step 1: Get Cloudinary Credentials

From Cloudinary dashboard, copy:
- Cloud name
- API Key
- API Secret

### Step 2: Configure Bknd

```typescript
import { defineConfig } from "bknd";

export default defineConfig({
  media: {
    enabled: true,
    adapter: {
      type: "cloudinary",
      config: {
        cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
        api_key: process.env.CLOUDINARY_API_KEY,
        api_secret: process.env.CLOUDINARY_API_SECRET,
      },
    },
  },
});
```

### Step 3: Add Environment Variables

```bash
# .env
CLOUDINARY_CLOUD_NAME=my-cloud
CLOUDINARY_API_KEY=123456789
CLOUDINARY_API_SECRET=abcdef...
```

### Optional: Upload Preset

For unsigned uploads or custom transformations:

```typescript
adapter: {
  type: "cloudinary",
  config: {
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET,
    upload_preset: "my-preset",  // Optional
  },
},
```

## Step-by-Step: Local Adapter (Development)

### Step 1: Create Upload Directory

```bash
mkdir -p ./uploads
```

### Step 2: Register and Configure

```typescript
import { defineConfig } from "bknd";
import { registerLocalMediaAdapter } from "bknd/adapter/node";

// Register the local adapter
const local = registerLocalMediaAdapter();

export default defineConfig({
  media: {
    enabled: true,
    adapter: local({ path: "./uploads" }),
  },
});
```

Files served at `/api/media/file/{filename}`.

### Note on Runtime

Local adapter requires Node.js or Bun runtime (filesystem access). It won't work in:
- Cloudflare Workers
- Vercel Edge Functions
- Browser environments

## Step-by-Step: Cloudflare R2 (Workers)

### Step 1: Create R2 Bucket

```bash
wrangler r2 bucket create my-bucket
```

### Step 2: Add R2 Binding to wrangler.toml

```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

### Step 3: Configure Bknd

```typescript
import { serve, type CloudflareBkndConfig } from "bknd/adapter/cloudflare";

const config: CloudflareBkndConfig = {
  app: (env) => ({
    connection: { url: env.DB },
    config: {
      media: {
        enabled: true,
        adapter: {
          type: "r2",
          config: {
            binding: "MY_BUCKET",
          },
        },
      },
    },
  }),
};

export default serve(config);
```

R2 adapter uses the Cloudflare Workers binding directly, no external credentials needed.

## Media Module Options

### Size Limit

```typescript
export default defineConfig({
  media: {
    enabled: true,
    body_max_size: 10 * 1024 * 1024,  // 10MB max upload
    adapter: { ... },
  },
});
```

### Default Size Behavior

If `body_max_size` not set, uploads have no size limit. Always set a reasonable limit in production.

## Environment-Based Configuration

Different adapters for dev vs production:

```typescript
import { defineConfig } from "bknd";
import { registerLocalMediaAdapter } from "bknd/adapter/node";

const local = registerLocalMediaAdapter();
const isDev = process.env.NODE_ENV !== "production";

export default defineConfig({
  media: {
    enabled: true,
    body_max_size: 25 * 1024 * 1024,  // 25MB
    adapter: isDev
      ? local({ path: "./uploads" })
      : {
          type: "s3",
          config: {
            access_key: process.env.S3_ACCESS_KEY,
            secret_access_key: process.env.S3_SECRET_KEY,
            url: process.env.S3_BUCKET_URL,
          },
        },
  },
});
```

## Verify Storage Configuration

### Check Media Module Enabled

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// List files (empty if no uploads yet)
const { ok, data, error } = await api.media.listFiles();

if (ok) {
  console.log("Media module working, files:", data.length);
} else {
  console.error("Media error:", error);
}
```

### Test Upload

```typescript
async function testStorage() {
  const testFile = new File(["test content"], "test.txt", {
    type: "text/plain"
  });

  const { ok, data, error } = await api.media.upload(testFile);

  if (ok) {
    console.log("Upload succeeded:", data.name);

    // Clean up
    await api.media.deleteFile(data.name);
    console.log("Cleanup complete");
  } else {
    console.error("Upload failed:", error);
  }
}
```

### Check via REST

```bash
# List files
curl http://localhost:7654/api/media/files

# Upload test file
echo "test" | curl -X POST \
  -H "Content-Type: text/plain" \
  --data-binary @- \
  http://localhost:7654/api/media/upload/test.txt
```

## Complete Configuration Examples

### AWS S3 Production

```typescript
import { defineConfig } from "bknd";

export default defineConfig({
  connection: {
    url: process.env.DATABASE_URL,
  },
  config: {
    media: {
      enabled: true,
      body_max_size: 50 * 1024 * 1024,  // 50MB
      adapter: {
        type: "s3",
        config: {
          access_key: process.env.AWS_ACCESS_KEY_ID,
          secret_access_key: process.env.AWS_SECRET_ACCESS_KEY,
          url: `https://${process.env.S3_BUCKET}.s3.${process.env.AWS_REGION}.amazonaws.com`,
        },
      },
    },
  },
});
```

### Cloudflare R2 + D1

```typescript
import { serve, type CloudflareBkndConfig } from "bknd/adapter/cloudflare";

const config: CloudflareBkndConfig = {
  app: (env) => ({
    connection: { url: env.DB },  // D1 binding
    config: {
      media: {
        enabled: true,
        body_max_size: 25 * 1024 * 1024,
        adapter: {
          type: "r2",
          config: { binding: "UPLOADS" },
        },
      },
    },
  }),
};

export default serve(config);
```

### Development with Hot Reload

```typescript
import { defineConfig } from "bknd";
import { registerLocalMediaAdapter } from "bknd/adapter/node";

const local = registerLocalMediaAdapter();

export default defineConfig({
  connection: {
    url: "file:data.db",
  },
  config: {
    media: {
      enabled: true,
      adapter: local({ path: "./public/uploads" }),
    },
  },
});
```

## Common Pitfalls

### S3 403 Forbidden

**Problem:** Upload fails with 403 error.

**Causes:**
1. Invalid credentials
2. Bucket policy blocks access
3. URL format incorrect

**Fix:**
```typescript
// Check URL format - must NOT have trailing slash
url: "https://bucket.s3.region.amazonaws.com"  // CORRECT
url: "https://bucket.s3.region.amazonaws.com/" // WRONG

// Verify credentials
console.log("Key:", process.env.S3_ACCESS_KEY?.substring(0, 8) + "...");
```

### Local Adapter 404

**Problem:** Files not found after upload.

**Causes:**
1. Upload directory doesn't exist
2. Wrong path (absolute vs relative)

**Fix:**
```bash
# Create directory first
mkdir -p ./uploads

# Use relative path from project root
adapter: local({ path: "./uploads" })  // CORRECT
adapter: local({ path: "/uploads" })   // WRONG (absolute)
```

### R2 Binding Not Found

**Problem:** "No R2Bucket found with key" error.

**Fix:** Ensure wrangler.toml has correct binding:

```toml
[[r2_buckets]]
binding = "MY_BUCKET"      # This name goes in config
bucket_name = "actual-bucket"
```

### Cloudinary Upload Fails Silently

**Problem:** `putObject` returns undefined.

**Causes:**
1. Invalid credentials
2. API key doesn't have upload permission

**Fix:**
- Verify credentials in Cloudinary dashboard
- Ensure API key has write access (not read-only)

### Wrong Adapter for Runtime

**Problem:** Local adapter fails in serverless.

**Fix:** Use S3/R2/Cloudinary for serverless:

```typescript
// Cloudflare Workers - use r2
// Vercel - use s3
// AWS Lambda - use s3
// Node.js server - local is OK for dev
```

### Missing Environment Variables

**Problem:** Credentials undefined at runtime.

**Fix:**
```typescript
// Add validation
if (!process.env.S3_ACCESS_KEY) {
  throw new Error("S3_ACCESS_KEY not set");
}

// Or provide defaults for dev
const config = {
  access_key: process.env.S3_ACCESS_KEY ?? "dev-key",
  // ...
};
```

### CORS Not Configured

**Problem:** Browser uploads blocked.

**Fix:** Configure CORS on the bucket itself (AWS/R2 console), not in Bknd.

## Security Checklist

1. **Never commit credentials** - Use environment variables
2. **Restrict bucket access** - Don't make bucket public unless needed
3. **Set size limits** - Always configure `body_max_size`
4. **Use HTTPS** - Especially for credential-based uploads
5. **Rotate keys** - Periodically rotate access keys
6. **Principle of least privilege** - IAM user needs only S3 access to one bucket

## DOs and DON'Ts

**DO:**
- Use environment variables for credentials
- Set `body_max_size` in production
- Use S3/R2/Cloudinary for production
- Configure CORS for browser uploads
- Test storage before deploying

**DON'T:**
- Commit credentials to git
- Use local adapter in production
- Leave upload size unlimited
- Forget to create upload directory for local
- Use trailing slash in S3 URL

## Related Skills

- **bknd-file-upload** - Upload files after storage configured
- **bknd-serve-files** - Serve and deliver uploaded files
- **bknd-env-config** - Manage environment variables
- **bknd-deploy-hosting** - Deploy with production storage
- **bknd-assign-permissions** - Set media permissions
