---
name: workflow-workflow
description: Automate {{WORKFLOW}} tasks. Use when {{TRIGGER_CONTEXTS}}. Supports
  {{CAPABILITIES}}.
---

---
name: {{WORKFLOW}}-workflow
description: Automate {{WORKFLOW}} tasks. Use when {{TRIGGER_CONTEXTS}}. Supports {{CAPABILITIES}}.
---

# {{WORKFLOW}} Workflow

## Commands

### {{COMMAND_1}}

{{Description}}

```bash
bun run scripts/run.ts {{command_1}} [options]
```

**Options:**
- `--dry-run` — Preview without executing
- `--verbose` — Show detailed output

### {{COMMAND_2}}

{{Description}}

```bash
bun run scripts/run.ts {{command_2}} [options]
```

## Safety

Destructive operations require confirmation:

```bash
bun run scripts/run.ts dangerous-op
# Prompts: "This will delete X. Continue? [y/N]"

bun run scripts/run.ts dangerous-op --force
# Skips confirmation (use with caution)
```

## Common Workflows

### Workflow 1: {{WORKFLOW_NAME}}

1. Run `{{command_1}}` to {{step 1 purpose}}
2. Review the output
3. Run `{{command_2}}` to {{step 2 purpose}}

### Workflow 2: {{WORKFLOW_NAME_2}}

1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}

## Idempotency

All commands are designed to be safely re-run:

- `init` — Creates only if not exists
- `update` — Applies only changed items
- `clean` — Removes only managed files

## Requirements

- Bun runtime
- {{DEPENDENCIES}}

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Permission denied | Insufficient access | Check file/directory permissions |
| Already exists | Resource conflict | Use `--force` to overwrite |
| Not found | Missing dependency | Ensure prerequisites are installed |

## Tips

- Always use `--dry-run` first for destructive operations
- Check `--verbose` output for debugging
- Commands are idempotent and safe to re-run
