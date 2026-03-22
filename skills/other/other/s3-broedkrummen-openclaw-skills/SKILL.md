---
name: S3
description: Work with S3-compatible object storage with proper security, lifecycle policies, and access patterns.
metadata: {"clawdbot":{"emoji":"🪣","os":["linux","darwin","win32"]}}
---

## Public Access Control

- Default deny public access—only open when explicitly needed (static hosting)
- Bucket policy vs IAM: bucket policy for cross-account/public, IAM for same-account roles
- Check both bucket-level AND account-level block settings—account can override bucket
- For web assets, prefer CDN in front of bucket over direct public access

## Presigned URLs

- Set shortest expiration practical—minutes for immediate use, not days
- URL is a bearer token—anyone with it has access; treat as secret
- Specify HTTP method in signature—GET for download, PUT for upload
- Include Content-Type for uploads—mismatch between signature and request causes 403
- Generate server-side, never expose credentials to client

## Lifecycle Rules

- Transition to cheaper tiers for infrequent access—but check minimum storage duration penalties
- Auto-delete for temp files, logs, old versions—prevents unbounded storage growth
- Clean incomplete multipart uploads—accumulate invisibly; set abort rule (7 days typical)
- Versioned buckets: separate rules for current vs noncurrent versions

## Versioning Behavior

- Enable before you need it—can't recover deleted objects without versioning
- "Delete" creates delete marker—object hidden but versions remain; storage still consumed
- Permanent deletion requires explicit version ID—without it, just adds marker
- Noncurrent version expiration essential—otherwise old versions accumulate forever

## Multipart Uploads

- Required above 5GB, recommended above 100MB—single PUT has size limits
- Incomplete uploads invisible in normal listings—consume storage silently
- Abort incomplete uploads via lifecycle—or manually with `list-multipart-uploads`
- Parallel part uploads for speed—parts can upload concurrently

## CORS for Browser Access

- Required for JavaScript direct upload/download—blocked without CORS headers
- Specify exact origins—avoid wildcard `*` for authenticated requests
- Expose headers that JavaScript needs to read—Content-Length, ETag, custom headers
- AllowedMethods: GET for download, PUT for upload, DELETE if needed

## Key Naming

- Use prefixes like directories: `users/123/avatar.jpg`—but S3 is flat, not hierarchical
- Avoid sequential prefixes for high throughput—`2024-01-01/file1` can hotspot
- Random prefix or hash for write-heavy buckets—distributes across partitions
- No leading slash—`/images/file.jpg` creates empty-string prefix

## Cost Awareness

- Request volume matters—many small files more expensive than few large files
- Egress typically costly—CDN reduces egress by caching at edge
- Minimum storage duration varies by tier—early deletion still charged full period
- Lifecycle transitions have per-object cost—millions of tiny files expensive to transition

## Replication

- Cross-region for disaster recovery, same-region for compliance copies
- Versioning required on both source and destination
- Only new objects replicate—existing objects need manual copy or batch operation
- Delete markers not replicated by default—explicitly enable if needed

## Provider Differences

- AWS S3: full feature set, most tools assume AWS behavior
- Cloudflare R2: no egress fees, subset of features
- Backblaze B2: S3-compatible API, different pricing model
- MinIO: self-hosted, full S3 API compatibility
- Check presigned URL compatibility—some providers have quirks
