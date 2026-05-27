---
name: cloud-uploader
description: Upload promo videos and content to Cloudflare R2 or AWS S3
model: claude-sonnet-4-5-20250929
allowed-tools:
  - Read
  - Bash
  - Glob
requirements:
  python:
    - boto3
---

# Cloud Uploader Skill

Upload promo videos and other album content to cloud storage (Cloudflare R2 or AWS S3).

## Purpose

After generating promo videos with `/bitwize-music:promo-director`, upload them to cloud storage for:
- Hosting on websites
- Sharing via direct links
- CDN distribution
- Backup and archival

## When to Use

- After promo videos generated, user wants to upload to cloud
- User says "upload promos to R2" or "upload to S3"
- User says "upload promo videos for [album]"
- Manual invocation only (not automatic)

## Position in Workflow

```
Generate → Master → Promo Videos → **[Cloud Upload]** → Release
```

Optional step after promo-director, before release-director.

## Prerequisites

### Cloud Configuration

Cloud credentials must be configured in `~/.bitwize-music/config.yaml`:

```yaml
cloud:
  enabled: true
  provider: "r2"  # or "s3"

  # For Cloudflare R2
  r2:
    account_id: "your-account-id"
    access_key_id: "your-access-key"
    secret_access_key: "your-secret-key"
    bucket: "promo-videos"

  # For AWS S3
  s3:
    region: "us-west-2"
    access_key_id: "your-access-key"
    secret_access_key: "your-secret-key"
    bucket: "promo-videos"
```

See `/reference/cloud/setup-guide.md` for detailed setup instructions.

### Required Files

- Promo videos generated (run `/bitwize-music:promo-director` first)
- Located at: `{audio_root}/{artist}/{album}/promo_videos/`
- Album sampler at: `{audio_root}/{artist}/{album}/album_sampler.mp4`

### Python Dependencies

```bash
python3 -m venv ~/.bitwize-music/cloud-env
source ~/.bitwize-music/cloud-env/bin/activate
pip install -r {plugin_root}/requirements-cloud.txt
```

**Always use the venv** — activate it before running the upload script.

## Workflow

### 1. Verify Prerequisites

**Check config:**
```bash
cat ~/.bitwize-music/config.yaml | grep -A 20 "cloud:"
```

Verify:
- `cloud.enabled: true`
- Provider credentials configured (r2 or s3)
- Bucket name set

**Check promo videos exist:**
```bash
ls {audio_root}/{artist}/{album}/promo_videos/
ls {audio_root}/{artist}/{album}/album_sampler.mp4
```

If missing:
```
Error: Promo videos not found.

Generate with: /bitwize-music:promo-director {album}
```

### 2. Preview Upload (Dry Run)

Always activate the venv and preview first:
```bash
source ~/.bitwize-music/cloud-env/bin/activate
cd {plugin_root}
python3 tools/cloud/upload_to_cloud.py {album} --dry-run
```

Output shows:
- Provider and bucket
- Files to upload
- S3 keys (paths in bucket)
- File sizes

### 3. Upload Files

**Upload all (promos + sampler):**
```bash
cd {plugin_root}
python3 tools/cloud/upload_to_cloud.py {album}
```

**Upload only track promos:**
```bash
python3 tools/cloud/upload_to_cloud.py {album} --type promos
```

**Upload only album sampler:**
```bash
python3 tools/cloud/upload_to_cloud.py {album} --type sampler
```

**Upload with public access:**
```bash
python3 tools/cloud/upload_to_cloud.py {album} --public
```

### 4. Verify Upload

**For R2:**
- Check Cloudflare dashboard → R2 → Your bucket
- Files should appear under `{artist}/{album}/`

**For S3:**
- Check AWS Console → S3 → Your bucket
- Or use AWS CLI: `aws s3 ls s3://{bucket}/{artist}/{album}/`

### 5. Report Results

```
## Cloud Upload Complete

**Provider:** R2 (or S3)
**Bucket:** {bucket}
**Album:** {album}

**Uploaded Files:**
- {artist}/{album}/promos/01-track_promo.mp4
- {artist}/{album}/promos/02-track_promo.mp4
- ...
- {artist}/{album}/promos/album_sampler.mp4

**Total:** 11 files, 125.4 MB

**Next Steps:**
1. Verify files in cloud dashboard
2. If public: Test URLs work
3. Continue to release: /bitwize-music:release-director {album}
```

## Upload Path Structure

**IMPORTANT: Cloud paths are FLAT - no genre folder.**

The cloud path structure is different from the local content structure:

| Location | Path Structure |
|----------|----------------|
| Local content | `{content_root}/artists/{artist}/albums/{genre}/{album}/` |
| Local audio | `{audio_root}/{artist}/{album}/` |
| **Cloud** | `{artist}/{album}/` (no genre!) |

Files are organized in the bucket as:

```
{bucket}/
└── {artist}/
    └── {album}/
        └── promos/
            ├── 01-track_promo.mp4
            ├── 02-track_promo.mp4
            ├── ...
            └── album_sampler.mp4
```

**Example for album "my-album" by "bitwize" in rock genre:**
- Local: `~/music/artists/bitwize/albums/rock/my-album/`
- Cloud: `bitwize/my-album/promos/` (NOT `bitwize/albums/rock/my-album/`)

## Command Options

| Option | Description |
|--------|-------------|
| `--type promos` | Upload only track promo videos |
| `--type sampler` | Upload only album sampler |
| `--type all` | Upload both (default) |
| `--dry-run` | Preview without uploading |
| `--public` | Set files as public-read |
| `--audio-root PATH` | Override audio_root from config |

## Invocation Examples

**Basic upload:**
```
/bitwize-music:cloud-uploader my-album
```

**Preview only:**
```
/bitwize-music:cloud-uploader my-album --dry-run
```

**Upload promos only:**
```
/bitwize-music:cloud-uploader my-album --type promos
```

**Upload with public access:**
```
/bitwize-music:cloud-uploader my-album --public
```

## Error Handling

**"Cloud uploads not enabled"**
- Add `cloud.enabled: true` to config
- See `/reference/cloud/setup-guide.md`

**"Credentials not configured"**
- Add credentials to config file
- For R2: account_id, access_key_id, secret_access_key
- For S3: access_key_id, secret_access_key

**"Album not found"**
- Check album exists in `{audio_root}/{artist}/{album}/`
- Verify artist name in config matches

**"No files found to upload"**
- Generate promo videos first: `/bitwize-music:promo-director {album}`

**"Access Denied"**
- Check credentials are correct
- For R2: Verify API token has write permissions
- For S3: Verify IAM policy allows s3:PutObject

**"Bucket not found"**
- Create bucket first in cloud dashboard
- Verify bucket name in config

## Security Notes

- Credentials stored in config file (ensure proper file permissions)
- Config file should be gitignored in user's content repo
- Default: Files uploaded as private (not public)
- Use `--public` flag only for files intended for public access
- Consider using environment variables for CI/CD (future enhancement)

## Integration with Other Skills

### Handoff FROM

**promo-director:**

After promo generation:
```
Promo videos generated successfully.

**Optional:** Upload to cloud storage: /bitwize-music:cloud-uploader {album}
```

### Handoff TO

**release-director:**

After cloud upload:
```
Cloud upload complete.

Ready for release workflow: /bitwize-music:release-director {album}
```

## Supported Providers

### Cloudflare R2

- S3-compatible API
- No egress fees
- Global CDN integration
- Good for high-traffic content

### AWS S3

- Industry standard
- Fine-grained IAM permissions
- CloudFront CDN available
- Good for AWS ecosystem integration

## Future Enhancements

- Environment variable credentials (for CI/CD)
- Multiple bucket support
- Automatic CDN invalidation
- Progress bar for large uploads
- Resume failed uploads
- Bucket creation if missing
- Additional providers (Backblaze B2, DigitalOcean Spaces)

## Related Documentation

- `/reference/cloud/setup-guide.md` - Detailed setup instructions
- `/skills/promo-director/SKILL.md` - Generate promo videos
- `/skills/release-director/SKILL.md` - Release workflow

## Model Recommendation

**Sonnet 4.5** - This skill runs scripts and coordinates workflow. No creative output from LLM.

## Version History

- v0.14.0 - Initial implementation
  - R2 and S3 support via boto3
  - Dry-run mode
  - Public/private upload options
  - Path organization by artist/album
