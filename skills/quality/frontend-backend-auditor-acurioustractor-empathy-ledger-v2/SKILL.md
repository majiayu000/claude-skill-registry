---
name: frontend-backend-auditor
description: Ensure frontend components match database infrastructure, identify deprecated patterns, maintain data consistency.
---

# Frontend-Backend Auditor

Audit frontend-database alignment. Identify deprecated AI analysis, wrong table usage, type mismatches.

## When to Use
- After database migrations/consolidation
- Reviewing component database access
- Identifying deprecated data patterns
- Ensuring TypeScript types match schema

## Quick Audit Commands
```bash
# Find deprecated table usage
grep -r "from('profiles')" src/ --include="*.tsx" --include="*.ts"
grep -r "from('analysis_jobs')" src/ --include="*.tsx" --include="*.ts"

# Find deprecated columns
grep -r "legacy_" src/ --include="*.tsx" --include="*.ts"

# Check type sync
npm run types:generate
git diff src/types/database/
```

## Common Migrations

### Storyteller Data
```typescript
// ❌ OLD: profiles table
supabase.from('profiles').select('*').eq('is_storyteller', true)

// ✅ NEW: storytellers table
supabase.from('storytellers').select('*').eq('is_active', true)
```

### AI Analysis
```typescript
// ❌ OLD: analysis_jobs
supabase.from('analysis_jobs').select('*')

// ✅ NEW: versioned results
supabase.from('transcript_analysis_results')
  .select('*')
  .eq('analysis_version', 'v2')
```

## Current AI Systems
- `transcript_analysis_results` - Versioned analysis
- `narrative_themes` - AI-extracted themes
- `story_themes` - Junction table
- `knowledge_chunks` - RAG embeddings

## Reference Files
| Topic | File |
|-------|------|
| Deprecated patterns | `refs/deprecated-patterns.md` |
| Audit process | `refs/audit-process.md` |

## Related Skills
- `data-integrity-guardian` - Data quality checks
- `supabase-deployment` - Schema management
- `database-navigator` - Schema exploration
