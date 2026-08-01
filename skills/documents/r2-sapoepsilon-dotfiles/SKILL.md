---
name: r2
description: Manage Cloudflare R2 object storage buckets and objects using Wrangler
  CLI. Use when working with R2 buckets, uploading/downloading files, configuring
  custom domains, CORS, lifecycle policies, or mana
---

---
name: r2
description: Manage Cloudflare R2 object storage buckets and objects using Wrangler CLI. Use when working with R2 buckets, uploading/downloading files, configuring custom domains, CORS, lifecycle policies, or managing R2 storage. Trigger keywords: R2, bucket, object storage, Cloudflare storage, wrangler r2.
allowed-tools: Bash, Read, Grep, Glob
---

# Cloudflare R2 Storage Management

This skill provides commands and patterns for managing Cloudflare R2 object storage using the Wrangler CLI.

## Prerequisites

- Wrangler CLI installed (`npm install -g wrangler` or use `npx wrangler`)
- Authenticated with Cloudflare (`wrangler login`)

## Quick Reference

### Bucket Operations

```bash
# Create a bucket
wrangler r2 bucket create <BUCKET_NAME>

# List all buckets
wrangler r2 bucket list

# Delete a bucket (must be empty)
wrangler r2 bucket delete <BUCKET_NAME>
```

### Object Operations

```bash
# Upload an object
wrangler r2 object put <BUCKET>/<KEY> --file <LOCAL_FILE> --remote

# Download an object
wrangler r2 object get <BUCKET>/<KEY> --file <LOCAL_FILE> --remote

# Delete an object
wrangler r2 object delete <BUCKET>/<KEY> --remote
```

### Custom Domains

```bash
# Add custom domain to bucket
wrangler r2 bucket domain add <BUCKET_NAME> --domain <DOMAIN> --zone-id <ZONE_ID>

# List custom domains
wrangler r2 bucket domain list <BUCKET_NAME>

# Remove custom domain
wrangler r2 bucket domain remove <BUCKET_NAME> --domain <DOMAIN>
```

### CORS Configuration

```bash
# Set CORS rules
wrangler r2 bucket cors put <BUCKET_NAME> --file cors.json

# Get CORS configuration
wrangler r2 bucket cors get <BUCKET_NAME>

# Clear CORS configuration
wrangler r2 bucket cors delete <BUCKET_NAME>
```

Example `cors.json`:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://example.com", "https://*.example.com"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### Event Notifications

```bash
# Enable notifications to a queue
wrangler r2 bucket notification create <BUCKET_NAME> \
  --event-type object-create \
  --queue <QUEUE_NAME>
```

### Bucket Lock Rules

```bash
# List lock rules
wrangler r2 bucket lock list <BUCKET_NAME>
```

## Detailed Operations

For detailed API reference and advanced usage, see [REFERENCE.md](REFERENCE.md).

## Common Patterns

### Bulk Upload Directory

```bash
# Upload all files from a directory
for file in ./assets/*; do
  wrangler r2 object put my-bucket/assets/$(basename "$file") --file "$file" --remote
done
```

### Migrate from S3 (Sippy)

R2 supports incremental migration from S3 using Sippy. Configure via the Cloudflare dashboard or API.

### Public Access via Custom Domain

1. Create bucket: `wrangler r2 bucket create my-bucket`
2. Get zone ID for your domain from Cloudflare dashboard
3. Add custom domain: `wrangler r2 bucket domain add my-bucket --domain assets.example.com --zone-id <ZONE_ID>`
4. Objects are now accessible at `https://assets.example.com/<key>`

## wrangler.toml Binding

To use R2 in Workers, add to `wrangler.toml`:

```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket-name"
```

## Important Notes

- Bucket names: lowercase, numbers, hyphens only (3-63 chars, no leading/trailing hyphens)
- Use `--remote` flag to interact with remote R2 (default is local dev)
- R2 is S3-compatible - AWS SDK works with R2 endpoint
- No egress fees for R2
