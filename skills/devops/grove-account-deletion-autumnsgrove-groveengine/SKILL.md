---
name: grove-account-deletion
description: Delete a Grove tenant account via wrangler D1 commands. Use when the user wants to remove a test account, clean up after a walkthrough, or fully delete a user's data. Handles D1 CASCADE cleanup, R2 media purge, and Heartwood session invalidation.
---

# Grove Account Deletion

Safely delete a tenant account and all associated data from the Grove platform using wrangler CLI commands.

## When to Activate

- User says something like "delete Alice's account" or "Alice is done"
- User mentions wanting to remove a test account
- User asks to clean up after a walkthrough or demo
- User explicitly calls `/grove-account-deletion`
- User says "nuke that account" or "wipe their data"

---

## The Pipeline

```
Identify → Verify → Snapshot → Delete Tenant → Clean Orphans → Purge R2 → Verify
```

### Step 1: Identify the Tenant

The user will provide a username (subdomain), email, or display name. Look them up:

```bash
# By username/subdomain (most common)
npx wrangler d1 execute grove-engine-db --remote --command="SELECT id, subdomain, display_name, email, plan, created_at FROM tenants WHERE subdomain = 'USERNAME';"

# By email (if username unknown)
npx wrangler d1 execute grove-engine-db --remote --command="SELECT id, subdomain, display_name, email, plan, created_at FROM tenants WHERE email = 'EMAIL';"

# By display name (fuzzy match)
npx wrangler d1 execute grove-engine-db --remote --command="SELECT id, subdomain, display_name, email, plan, created_at FROM tenants WHERE display_name LIKE '%NAME%';"
```

**Run these from the project root** (`/Users/mini/Documents/Projects/GroveEngine`).

### Step 2: Confirm with the User

Before deleting ANYTHING, show the user what you found and ask for explicit confirmation:

```
Found tenant:
  ID:       abc-123-def
  Username: alice
  Name:     Alice Wonderland
  Email:    alice@example.com
  Plan:     seedling
  Created:  2026-01-24

This will permanently delete:
  - All blog posts and pages
  - All media files (R2 storage)
  - All sessions and settings
  - Commerce data (orders, products, customers)
  - Curio configurations (timeline, journey, gallery)
  - Onboarding and billing records

Proceed with deletion?
```

**NEVER skip this confirmation step.** Even for test accounts.

### Step 3: Pre-Deletion Snapshot (Optional but Recommended)

For non-test accounts, capture a quick count of what's being deleted:

```bash
npx wrangler d1 execute grove-engine-db --remote --command="
  SELECT
    (SELECT COUNT(*) FROM posts WHERE tenant_id = 'TENANT_ID') as posts,
    (SELECT COUNT(*) FROM pages WHERE tenant_id = 'TENANT_ID') as pages,
    (SELECT COUNT(*) FROM media WHERE tenant_id = 'TENANT_ID') as media_files,
    (SELECT COUNT(*) FROM sessions WHERE tenant_id = 'TENANT_ID') as sessions;
"
```

### Step 4: Delete the Tenant (CASCADE Handles 29 Tables)

This single DELETE cascades to: posts, pages, media records, tenant_settings, sessions, products, product_variants, customers, orders, order_line_items, subscriptions, connect_accounts, platform_billing, refunds, discount_codes, post_views, timeline_curio_config, timeline_summaries, timeline_activity, timeline_ai_usage, journey_curio_config, journey_snapshots, journey_summaries, journey_jobs, gallery_curio_config, gallery_images, gallery_tags, gallery_collections, git_dashboard_config.

```bash
npx wrangler d1 execute grove-engine-db --remote --command="DELETE FROM tenants WHERE id = 'TENANT_ID';"
```

### Step 5: Clean Up Orphaned Records

These tables don't CASCADE from tenants and need manual cleanup:

```bash
# Remove onboarding record (linked by username, not FK)
npx wrangler d1 execute grove-engine-db --remote --command="DELETE FROM user_onboarding WHERE username = 'USERNAME';"

# Remove email verification codes for that user (cascades from user_onboarding via FK, but verify)
npx wrangler d1 execute grove-engine-db --remote --command="DELETE FROM email_verification_codes WHERE user_id IN (SELECT id FROM user_onboarding WHERE username = 'USERNAME');"
```

If the user signed up via Heartwood and has no other tenants:

```bash
# Check if user has other tenants
npx wrangler d1 execute grove-engine-db --remote --command="SELECT id, subdomain FROM tenants WHERE email = 'USER_EMAIL';"

# If no other tenants exist, clean orphaned user record (if applicable)
# NOTE: The 'users' table may or may not exist depending on auth approach used
```

### Step 6: Purge R2 Media (If Media Existed)

R2 keys follow the pattern `{tenant_id}/{filename}`. The D1 `media` table records are already gone (CASCADE), but the actual R2 objects remain.

```bash
# List objects with tenant prefix
npx wrangler r2 object list grove-media --prefix="TENANT_ID/" --remote

# Delete each object (wrangler doesn't support bulk delete, so iterate)
# For a small number of files:
npx wrangler r2 object delete grove-media --remote "TENANT_ID/filename1.webp"
npx wrangler r2 object delete grove-media --remote "TENANT_ID/filename2.webp"
```

**For many files**, generate a deletion script:

```bash
# List all keys, then delete in a loop
npx wrangler r2 object list grove-media --prefix="TENANT_ID/" --remote 2>/dev/null | jq -r '.[] .key' | while read key; do
  echo "Deleting: $key"
  npx wrangler r2 object delete grove-media --remote "$key"
done
```

**Skip this step** if the pre-deletion snapshot showed 0 media files.

### Step 7: Post-Deletion Verification

Confirm the tenant is fully gone:

```bash
# Verify tenant deleted
npx wrangler d1 execute grove-engine-db --remote --command="SELECT COUNT(*) as remaining FROM tenants WHERE subdomain = 'USERNAME';"

# Verify cascade worked (spot-check a few tables)
npx wrangler d1 execute grove-engine-db --remote --command="
  SELECT
    (SELECT COUNT(*) FROM posts WHERE tenant_id = 'TENANT_ID') as posts,
    (SELECT COUNT(*) FROM media WHERE tenant_id = 'TENANT_ID') as media,
    (SELECT COUNT(*) FROM sessions WHERE tenant_id = 'TENANT_ID') as sessions;
"

# Verify onboarding cleaned
npx wrangler d1 execute grove-engine-db --remote --command="SELECT COUNT(*) as remaining FROM user_onboarding WHERE username = 'USERNAME';"
```

### Step 8: Report

Give the user a clean summary:

```
Tenant "alice" (Alice Wonderland) has been fully deleted.

Cleaned up:
  - Tenant record + 29 cascaded tables
  - Onboarding record
  - 3 R2 media files
  - Email verification codes

The subdomain "alice.grove.place" is now available for reuse.
```

---

## Safety Rules

1. **Always confirm before deleting** - Even if the user seems sure, show them the tenant details first
2. **Never delete by ID alone** - Always resolve to a human-readable identifier (subdomain/email) for confirmation
3. **Check for active subscriptions** - Warn if `platform_billing.status = 'active'` or LemonSqueezy subscription exists
4. **Test accounts are still accounts** - Same process, same confirmation, same verification
5. **R2 is permanent** - Once R2 objects are deleted, they're gone. The D1 media records (which held the keys) are already cascaded away, so do R2 cleanup BEFORE losing track of what was stored

---

## Quick Mode (Test Accounts)

For accounts the user explicitly calls "test accounts" or accounts created in the current session:

- Still confirm the username/email
- Skip the pre-deletion snapshot
- Skip R2 cleanup if no media was uploaded
- Still verify deletion completed

---

## Edge Cases

### User has multiple tenants
One email can own multiple subdomains. Only delete the specified tenant. Don't touch others.

### Tenant not found
If the subdomain/email doesn't match any tenant, tell the user. Don't guess.

### Heartwood session cleanup
Heartwood sessions are stored in KV, not D1. The D1 `sessions` table is for legacy/local sessions. Heartwood sessions will expire naturally (24h TTL). No manual cleanup needed unless urgency is specified.

### LemonSqueezy subscription active
If `user_onboarding.lemonsqueezy_subscription_id` is set, warn the user that they may need to cancel the subscription in the LemonSqueezy dashboard separately. D1 deletion doesn't cancel external billing.

---

## Environment

All commands run from the project root: `/Users/mini/Documents/Projects/GroveEngine`

The database is: `grove-engine-db` (D1)
The media bucket is: `grove-media` (R2)

---

*A clean deletion is a kind goodbye. Leave no orphans behind.*
