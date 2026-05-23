---
name: data-integrity-guardian
description: Maintain database quality, ensure data alignment, verify mission compliance, prepare for JusticeHub syndication.
---

# Data Integrity Guardian

Ensure database quality, cultural safety, mission alignment, and API readiness.

## When to Use
- Before JusticeHub API syndication
- Adding stories to public catalog
- Migrating data between tables
- Weekly data quality audits

## Quick Health Check
```sql
SELECT
  'Stories' as metric, COUNT(*)::text as value FROM stories
UNION ALL
SELECT 'Published', COUNT(*)::text FROM stories WHERE status = 'published'
UNION ALL
SELECT 'Active Storytellers', COUNT(*)::text FROM storytellers WHERE is_active = true
UNION ALL
SELECT 'Avatar Coverage %',
  ROUND(COUNT(*) FILTER (WHERE avatar_url IS NOT NULL) * 100.0 / COUNT(*), 1)::text
FROM storytellers;
```

## Critical Checks

### Orphaned Records
```sql
-- Stories without storytellers (should be 0)
SELECT COUNT(*) FROM stories s
LEFT JOIN storytellers st ON s.storyteller_id = st.id
WHERE s.storyteller_id IS NOT NULL AND st.id IS NULL;
```

### Cultural Safety
```sql
-- Public stories without elder review (should be 0)
SELECT COUNT(*) FROM stories
WHERE requires_elder_review = true AND elder_reviewed = false AND is_public = true;
```

### Consent Verification
```sql
-- Public stories missing consent (should be 0)
SELECT COUNT(*) FROM stories
WHERE status = 'published' AND is_public = true
AND (has_explicit_consent = false OR has_explicit_consent IS NULL);
```

## Reference Files
| Topic | File |
|-------|------|
| All integrity checks | `refs/integrity-checks.md` |
| JusticeHub readiness | `refs/justicehub-readiness.md` |

## Mission Alignment
- **OCAP Compliance**: Ownership, Control, Access, Possession
- **Cultural Safety**: Elder review, traditional knowledge protection
- **Storyteller Empowerment**: Full control over narratives

## Related Skills
- `frontend-backend-auditor` - Frontend alignment
- `database-navigator` - Schema exploration
- `cultural-review` - Cultural sensitivity
