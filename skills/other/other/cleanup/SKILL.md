---
description: Run data retention cleanup jobs (quiz responses, PDFs, magic links, blacklist)
---

## User Input

```text
$ARGUMENTS
```

Options: `dry-run` (preview only), `force` (execute deletions)

## Task

Execute data retention cleanup according to the privacy policy.

### Steps

1. **Parse Arguments**:
   - `dry-run` or empty: Preview deletions without executing
   - `force`: Execute actual deletions

2. **Cleanup Paid Quiz Responses** (24h after PDF delivery):
   ```bash
   cd backend
   python scripts/cleanup_paid_quiz.py --dry-run

   # Expected: Delete quiz_responses where pdf_delivered_at < NOW() - 24h
   ```

3. **Cleanup Unpaid Quiz Responses** (7 days after creation):
   ```bash
   python scripts/cleanup_unpaid_quiz.py --dry-run

   # Expected: Delete quiz_responses where created_at < NOW() - 7d AND payment_id IS NULL
   ```

4. **Cleanup Meal Plans** (90 days after creation):
   ```bash
   python scripts/cleanup_meal_plans.py --dry-run

   # Expected: Delete meal_plans where created_at < NOW() - 90d
   ```

5. **Cleanup PDFs from Vercel Blob** (91 days = 90d + 24h grace):
   ```bash
   python scripts/cleanup_pdfs.py --dry-run

   # Expected: Delete blobs where created_at < NOW() - 91d
   ```

6. **Cleanup Expired Magic Links** (24h after creation):
   ```bash
   python scripts/cleanup_magic_links.py --dry-run

   # Expected: Delete magic_link_tokens where created_at < NOW() - 24h
   ```

7. **Cleanup Email Blacklist** (90-day TTL):
   ```bash
   python scripts/cleanup_blacklist.py --dry-run

   # Expected: Delete email_blacklist where created_at < NOW() - 90d
   ```

8. **Generate Deletion Report**:
   ```
   ✅ Data Retention Cleanup Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Mode: DRY RUN (no deletions executed)

   Quiz Responses (Paid):
   📊 Found: 145 records eligible for deletion
   📅 Oldest: 25 days since PDF delivery
   🗑️  Would delete: 145 records

   Quiz Responses (Unpaid):
   📊 Found: 23 records eligible for deletion
   📅 Oldest: 15 days old
   🗑️  Would delete: 23 records

   Meal Plans:
   📊 Found: 8 records eligible for deletion
   📅 Oldest: 95 days old
   🗑️  Would delete: 8 records

   PDFs (Vercel Blob):
   📊 Found: 8 blobs eligible for deletion
   💾 Space to reclaim: 4.2 MB
   🗑️  Would delete: 8 blobs

   Magic Links:
   📊 Found: 67 expired tokens
   🗑️  Would delete: 67 records

   Email Blacklist:
   📊 Found: 3 expired entries
   🗑️  Would delete: 3 records

   Total Deletions: 254 records + 8 blobs
   Space Reclaimed: 4.2 MB

   ⚠️ This was a DRY RUN. Use '/cleanup force' to execute.
   ```

9. **Execute Deletions** (if --force):
   - Run all cleanup scripts with --force flag
   - Log all deletions to Sentry for audit trail
   - Generate post-cleanup report

10. **Audit Logging**:
    ```bash
    # Log to Sentry
    python -c "
    import sentry_sdk
    sentry_sdk.capture_message(
        'Data cleanup executed',
        level='info',
        extra={
            'quiz_deleted': 168,
            'meal_plans_deleted': 8,
            'pdfs_deleted': 8,
            'magic_links_deleted': 67,
            'blacklist_deleted': 3
        }
    )
    "
    ```

## Example Usage

```bash
/cleanup              # Dry run - preview deletions
/cleanup dry-run      # Same as above
/cleanup force        # Execute actual deletions
```

## Exit Criteria

- All cleanup scripts executed
- Deletion counts reported
- Audit logs created (for force mode)
- Storage space reclaimed calculated

## Safety Notes

- **Always run dry-run first** to verify deletions
- **Deletions are permanent** - no undo
- **Audit trail required** - all deletions logged to Sentry
- **Compliance** - retention policy must be enforced
