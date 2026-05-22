---
description: Living documentation updater that syncs implementation progress to product docs. Use when updating docs after task completion, changing DRAFT status to published, or ensuring documentation reflects current implementation state.
user-invocable: false
---

# Documentation Updater

## Project Overrides

!`s="docs-updater"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

Updates product documentation (.specweave/docs/) based on implementation progress.

## When to Use

- Task specifies documentation updates in tasks.md
- Feature implementation is complete
- User says "update documentation" or "sync docs"
- After closing increment to ensure docs reflect reality

## What It Does

1. **Reads task requirements** - Understands what was implemented from tasks.md
2. **Updates living docs** - Modifies `.specweave/docs/` files with actual implementation
3. **Status tracking** - Changes `[DRAFT]` � `[COMPLETE]` on doc sections
4. **Bidirectional links** - Maintains links between docs and increments
5. **Format adaptation** - Matches existing doc structure (features/ or modules/)

## Workflow

```
1. Read tasks.md � Find documentation tasks
2. Read implementation � Understand what changed
3. Update docs � Add real code examples, endpoints, configs
4. Mark complete � Change [DRAFT] to [COMPLETE]
5. Verify links � Ensure increment � doc references work
```

## Example

**tasks.md says:**
```markdown
**Documentation Updates**:
- [ ] .specweave/docs/features/payment.md [DRAFT]
- [ ] .specweave/docs/api/payments.md [DRAFT]
```

**docs-updater does:**
1. Reads payment implementation code
2. Updates `payment.md` with actual code examples
3. Updates API docs with real endpoints discovered in code
4. Changes status to `[COMPLETE]`

## Integration Points

- **Called by**: spec-generator, task completion hooks
- **Updates**: `.specweave/docs/**/*.md`
- **Reads**: `tasks.md`, implementation code

## Best Practices

- Run after completing feature tasks, not during
- Verify doc links are valid (use relative paths)
- Keep examples in sync with actual code
- Don't over-document - focus on what users need


