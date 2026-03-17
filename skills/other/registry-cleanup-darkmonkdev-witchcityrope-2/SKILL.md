---
name: registry-cleanup
description: Automates cleanup of old container images from DigitalOcean registries based on retention policies. Keeps last 10 tags for staging, 30 for production, always preserves :latest.
---

# Registry Cleanup Skill

**Purpose**: Clean up old container images to manage storage costs in DigitalOcean Container Registries.

**When to Use**:
- Weekly maintenance (recommended)
- When storage usage is high
- After major deployment cycles
- Before month-end to reduce storage costs

**When NOT to Use**:
- During active deployments (wait for deployment to complete)
- If unsure about which tags are safe to delete (use dry-run mode first)
- Without reviewing dry-run output first

---

## 🚨 SINGLE SOURCE OF TRUTH

**This skill is the ONLY registry cleanup procedure.**

**DO NOT duplicate registry cleanup automation in:**
- ❌ Agent definitions
- ❌ Lessons learned (reference this skill instead)
- ❌ Process documentation
- ❌ Deployment guides

---

## Retention Policies

### WitchCityRope Registry

| Repository | Retention | Always Keep | Purpose |
|------------|-----------|-------------|---------|
| `witchcityrope-api-staging` | **10 tags** | `:latest` | Staging API images |
| `witchcityrope-web-staging` | **10 tags** | `:latest` | Staging Web images |
| `witchcityrope-api-production` | **30 tags** | `:latest` | Production API images |
| `witchcityrope-web-production` | **30 tags** | `:latest` | Production Web images |

### Accounting Registry

| Repository | Retention | Always Keep | Purpose |
|------------|-----------|-------------|---------|
| `accounting-api` | **30 tags** | `:latest` | Production API (treat as production) |
| `accounting-web` | **30 tags** | `:latest` | Production Web (treat as production) |

**Rationale**:
- **Staging (10 tags)**: Fast iteration, lower rollback depth needed
- **Production (30 tags)**: Longer rollback window, compliance, audit trail
- **:latest tag**: Always preserved for consistent deployments

---

## How to Use This Skill

**Executable Script**: `execute.sh`

### Dry-Run Mode (Default - Recommended First)

```bash
# From project root - shows what WOULD be deleted
bash .claude/skills/registry-cleanup/execute.sh
```

**Output**: Shows repositories, tag counts, tags that would be deleted, estimated storage savings.

**NO CHANGES MADE** - Safe to run anytime.

### Confirm Mode (Actually Delete)

```bash
# From project root - ACTUALLY DELETES old tags
bash .claude/skills/registry-cleanup/execute.sh --confirm
```

**Output**: Shows repositories, deletes old tags, reports actual deletions, storage freed.

**DESTRUCTIVE** - Tags deleted cannot be recovered.

### What the Script Does

1. **Retrieves DigitalOcean API token** from .NET User Secrets
2. **Validates prerequisites**:
   - API token accessible
   - `curl` and `jq` installed
   - Registry access working
3. **For each repository**:
   - Lists all tags via DigitalOcean API
   - Sorts by creation date (newest first)
   - Identifies tags beyond retention limit
   - Skips `:latest` tag (always preserved)
   - Shows/deletes old tags based on mode
4. **Reports summary**:
   - Total tags processed
   - Tags deleted (or would be deleted)
   - Estimated storage freed

---

## Safety Features

### Built-In Protections

- ✅ **Dry-run by default** - No deletions unless `--confirm` flag used
- ✅ **:latest tag protected** - Never deleted, even if old
- ✅ **Sorted by date** - Keeps newest tags, deletes oldest
- ✅ **Detailed logging** - Shows exactly what will be deleted
- ✅ **Error handling** - Stops on API errors, doesn't continue blindly
- ✅ **Audit trail** - Logs all deletions to stdout (redirect to file for records)

### Recommended Workflow

1. **Run dry-run first**: `bash execute.sh`
2. **Review output carefully**: Check tags to be deleted
3. **Verify no active deployments**: Wait for deploys to finish
4. **Run with confirmation**: `bash execute.sh --confirm`
5. **Save audit log**: Redirect output to file for compliance

```bash
# Example: Save audit log
bash .claude/skills/registry-cleanup/execute.sh --confirm 2>&1 | tee registry-cleanup-$(date +%Y-%m-%d).log
```

---

## Example Output

### Dry-Run Mode

```
🧹 Registry Cleanup - DRY RUN MODE
===================================

📊 Analyzing WitchCityRope Registry
-----------------------------------

Repository: witchcityrope-api-staging
  Total tags: 25
  Retention policy: 10 most recent
  Tags to delete: 15

  Keeping (10 newest + :latest):
    ✅ sha-abc123f (2025-11-22)
    ✅ sha-def456g (2025-11-21)
    ... (8 more)
    ✅ latest (protected)

  Would delete (15 oldest):
    🗑️  sha-xyz789h (2025-10-15)
    🗑️  sha-uvw456i (2025-10-10)
    ... (13 more)

  Estimated storage freed: ~350 MB

Repository: witchcityrope-web-staging
  Total tags: 18
  Retention policy: 10 most recent
  Tags to delete: 8

  Would delete (8 oldest):
    🗑️  sha-rst234j (2025-10-18)
    ... (7 more)

  Estimated storage freed: ~200 MB

📊 Summary
----------
Total repositories: 6
Total tags: 125
Tags to keep: 72
Tags to delete: 53
Estimated storage freed: ~850 MB

⚠️  DRY RUN - No changes made
ℹ️  Run with --confirm to actually delete tags
```

### Confirm Mode

```
🧹 Registry Cleanup - CONFIRM MODE
===================================
⚠️  WARNING: This will DELETE old tags permanently!

... (same analysis as dry-run) ...

🗑️  Deleting tags from witchcityrope-api-staging...
  Deleted: sha-xyz789h ✅
  Deleted: sha-uvw456i ✅
  ... (13 more)

✅ Deleted 15 tags from witchcityrope-api-staging

... (repeat for other repositories) ...

📊 Summary
----------
Total repositories: 6
Total tags deleted: 53
Actual storage freed: ~850 MB

✅ Registry cleanup complete
```

---

## Integration Points

### With Deployment Skills

- **staging-deploy** skill pushes new images with `:latest` and `:sha-XXXXXX` tags
- **production-deploy** skill pushes new images with `:latest` and `:sha-XXXXXX` tags
- This skill cleans up old SHA tags while preserving `:latest`

### With Weekly Maintenance

Recommended cron schedule:

```bash
# Every Sunday at 2 AM
0 2 * * 0 cd /home/chad/repos/witchcityrope && bash .claude/skills/registry-cleanup/execute.sh --confirm 2>&1 | tee -a /var/log/registry-cleanup.log
```

### With Cost Management

Monitor storage costs in DigitalOcean dashboard:
- Container Registry → Storage Usage
- Compare before/after cleanup
- Adjust retention policies if needed

---

## Troubleshooting

### Common Issues

#### API Token Not Found

**Error**: `User secrets not found or empty`

**Solution**:
```bash
cd /home/chad/repos/witchcityrope/apps/api
dotnet user-secrets list | grep DigitalOcean:Token
```

If empty, set token:
```bash
dotnet user-secrets set "DigitalOcean:Token" "YOUR_TOKEN_HERE"
```

#### Registry Access Denied

**Error**: `401 Unauthorized`

**Solution**: Token may be expired or invalid. Generate new token:
1. Go to https://cloud.digitalocean.com/account/api/tokens
2. Generate new Personal Access Token (read/write scopes)
3. Update user secrets with new token

#### Tag Deletion Fails

**Error**: `404 Not Found` or `500 Server Error`

**Solution**:
- Tag may already be deleted (concurrent deletion)
- Tag may be in use (active deployment)
- Wait 5 minutes, retry
- Check DigitalOcean status page for API issues

#### Storage Not Freed

**Symptom**: Tags deleted but storage usage unchanged

**Explanation**: DigitalOcean processes deletions asynchronously. Wait 1-2 hours for storage metrics to update.

---

## Configuration

### Adjusting Retention Policies

Edit `execute.sh` to modify retention counts:

```bash
# Repository configurations (line ~80)
declare -A RETENTION
RETENTION["witchcityrope-api-staging"]=10      # Change to 5, 15, etc.
RETENTION["witchcityrope-web-staging"]=10
RETENTION["witchcityrope-api-production"]=30   # Change to 20, 50, etc.
RETENTION["witchcityrope-web-production"]=30
```

**Consider**:
- **Lower retention** = More storage savings, shorter rollback window
- **Higher retention** = More storage costs, longer rollback window
- **Compliance requirements**: Some industries require longer retention

### Adding New Repositories

Edit `execute.sh` to add new repositories:

```bash
# Repository configurations (line ~80)
RETENTION["new-service-staging"]=10
RETENTION["new-service-production"]=30
```

Skill automatically processes all configured repositories.

---

## API Documentation

### DigitalOcean Container Registry API

**List Repository Tags**:
```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.digitalocean.com/v2/registry/witchcityrope/repositories/witchcityrope-api-staging/tags"
```

**Delete Tag**:
```bash
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.digitalocean.com/v2/registry/witchcityrope/repositories/witchcityrope-api-staging/tags/sha-abc123f"
```

**Response Codes**:
- `200 OK` - List successful
- `204 No Content` - Delete successful
- `401 Unauthorized` - Invalid token
- `404 Not Found` - Repository/tag not found
- `429 Too Many Requests` - Rate limited (wait 60 seconds)

---

## Version History

- **2025-11-22**: Initial creation
  - Support for 6 repositories (WitchCityRope + Accounting)
  - Dry-run and confirm modes
  - Retention policies (10 staging, 30 production)
  - :latest tag protection
  - Audit logging support

---

**For questions or issues**: Consult DigitalOcean Container Registry documentation or raise issue in repository.
