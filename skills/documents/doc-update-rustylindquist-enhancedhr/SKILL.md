---
name: doc-update
description: Updates documentation after code changes to keep docs in sync with code reality. Use AFTER implementation is complete. Covers feature docs, workflow docs, and index files.
allowed-tools: Read, Write, Glob, Grep
---

# Doc Update

Keep documentation evergreen by updating immediately after code changes.

## When to Use

- After completing any code change
- After fixing a bug or adding a feature
- Before running `/handoff`
- When `/drift-check` identifies stale docs

## Hierarchy

Updates flow from specific to general:
1. **Feature Docs** → `docs/features/{feature}.md`
2. **Workflow Docs** → `docs/workflows/{role}-workflows.md`
3. **Index Files** → FEATURE_INDEX.md, WORKFLOW_INDEX.md
4. **Architecture Docs** → `docs/engine/*.md` (if patterns changed)

## Quick Reference

| Files Changed | Update |
|---------------|--------|
| `app/actions/*.ts` | Feature doc → Server Actions |
| `app/(routes)/**` | Feature doc → User Surfaces |
| `components/**` | Feature doc + Component Index |
| `supabase/migrations/*` | Feature doc → Data Model + prod SQL |
| `lib/ai/**` | AI context docs + feature docs |

## Feature Doc Sections to Update

- **User Surfaces**: Routes, UI elements
- **Data Model**: Tables, columns, relationships
- **Server Actions**: Action name, purpose, tables, auth
- **Permissions**: RLS policies, admin client usage
- **Invariants**: Add newly discovered rules
- **Testing Checklist**: Update verification steps

## Output

```markdown
## Doc Update Complete

### Updated
| Doc | Sections |
|-----|----------|
| [feature].md | User Surfaces, Data Model |

### Production SQL
- Provided: [Yes/No]

### Verification
Run `/drift-check` to confirm no remaining drift.
```

## Related

- Section templates: See [reference/section-templates.md](reference/section-templates.md)
- Common patterns: See [reference/update-patterns.md](reference/update-patterns.md)
- Next step: `/drift-check`
