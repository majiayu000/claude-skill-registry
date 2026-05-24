---
name: cloud-recall
description: |
  Search cloud memory backup when local results are insufficient.
  Use when memory_search returns few/no results for a topic you
  know was discussed before. Cloud preserves everything - even
  memories that were deleted or compacted locally.

user-invocable: true
disable-model-invocation: false
argument-hint: "[search query]"
---

# Cloud Recall - Search Permanent Cloud Memory

Search the Supabase cloud backup for memories that may have been
consolidated, compressed, or deleted locally. The cloud NEVER
deletes memories - it preserves everything forever.

## When to Use

- Local `memory_search` returns few or no results
- User asks about something from a past session that seems missing
- User says "I told you about X" but local memory doesn't have it
- Restoring context after a fresh install or device switch

## Execution Steps

1. **Search cloud backup**:
   ```bash
   python3 -m cloud.cli search "$ARGUMENTS" --limit 10 --include-deleted
   ```
   Run this from the claude-memory directory (~/coding/claude-memory/)

2. **If results found that don't exist locally**:
   - Present results to user with [CLOUD] indicator
   - Offer to restore: "Found X memories in cloud. Restore to local?"

3. **Restore if requested**:
   ```bash
   python3 -m cloud.cli restore --hash <hash1>,<hash2>
   ```

4. **For full restore** (new device or data loss):
   ```bash
   python3 -m cloud.cli restore --all
   ```

## Important Notes

- Cloud search uses text matching (not embeddings) by default
- Deleted memories show as [DELETED LOCALLY] but full content is preserved
- Summary memories show as [SUMMARY] and link to original memories
- All cloud operations are read-only unless explicitly restoring

## Example Flow

User: "What did we decide about the API authentication?"
Local search: 0 results

1. Run: `python3 -m cloud.cli search "API authentication decision" --include-deleted`
2. Found: 3 results from cloud (2 were deleted during consolidation)
3. Display: "Found 3 memories in cloud backup about API authentication:"
   - [CLOUD] Decision: Use JWT with refresh tokens (deleted locally Jan 15)
   - [CLOUD] Reference: Auth middleware at /src/auth/jwt.py
   - [CLOUD] Pattern: Always validate tokens server-side
4. Ask: "Want me to restore these to local memory?"
