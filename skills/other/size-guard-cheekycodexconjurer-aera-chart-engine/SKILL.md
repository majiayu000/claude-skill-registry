---
name: size-guard
description: "Enforce line budgets on context files by rotating or splitting large files. Use when context-heavy files exceed configured line limits and need archiving, splitting, or index updates to keep load times fast."
metadata:
  short-description: Line budget guard
  version: "1.0.0"
---

# Size Guard

Enforce line budgets on context-heavy files to keep them within loading limits.

## When to Use

- A context file exceeds its configured line budget
- Memory or documentation files grow too large for fast agent loading
- You need to archive, rotate, or split oversized files while preserving history

## Budget Configuration

Read budgets from `.agent-docs/memory/LINE_BUDGETS.yaml`:

```yaml
# LINE_BUDGETS.yaml
budgets:
  decisions.md: 500
  action-log.md: 300
  context.md: 400
```

## Workflow

### 1. Check sizes against budgets

```bash
# Count lines and compare against budget
wc -l .agent-docs/memory/decisions.md
# If output exceeds budget (e.g., 623 > 500), proceed to step 2
```

### 2. Archive the current file

```bash
# Rename with timestamp to preserve history
mv .agent-docs/memory/decisions.md \
   .agent-docs/memory/decisions.2026-04-24T14-00-00Z.md
```

### 3. Create fresh file with recent entries

Keep the most recent entries (e.g., last 100 lines) in a new file:

```bash
tail -n 100 .agent-docs/memory/decisions.2026-04-24T14-00-00Z.md \
  > .agent-docs/memory/decisions.md
```

### 4. Update indexes

Update any index file that references the rotated file:

```markdown
<!-- index.md -->
- [decisions (current)](decisions.md)
- [decisions (archived 2026-04-24)](decisions.2026-04-24T14-00-00Z.md)
```

### 5. Verify and log

```bash
# Verify new file is within budget
wc -l .agent-docs/memory/decisions.md
# Verify archived file exists
ls -la .agent-docs/memory/decisions.2026-04-24T14-00-00Z.md
```

Append an entry to the Action Log:

```markdown
## 2026-04-24 — Size Guard: decisions.md
- **Action**: Rotated (623 lines → 100 lines)
- **Archived to**: decisions.2026-04-24T14-00-00Z.md
- **Reason**: Exceeded 500-line budget
```

## Guardrails

- Always archive before splitting — never delete history
- Preserve chronological ordering within split parts
- Verify index references resolve correctly after updates
- If splitting (not rotating), number parts sequentially: `file.part1.md`, `file.part2.md`
