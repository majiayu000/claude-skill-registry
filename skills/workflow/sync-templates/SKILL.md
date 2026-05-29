---
name: sync-templates
description: Bidirectional sync between scaffold templates and vault templates with interactive merge
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Bash(diff *), AskUserQuestion
---

# Sync Templates

Synchronize templates between the engine scaffold and your vault. Shows diffs and prompts for each changed file.

## Workflow

### 1. Load Configuration

**Use sub-skill: `_sub/fetch/get-config`**

Extract `vault_path` as `$VAULT`.

### 2. Define Template Pairs

Compare these locations:

| Scaffold (Engine) | Vault (User) |
|-------------------|--------------|
| `scaffold/00_Brain/Systemic/Templates/Captive/*.md` | `$VAULT/00_Brain/Systemic/Templates/Captive/*.md` |
| `scaffold/00_Brain/Systemic/Templates/Periodic/*.md` | `$VAULT/00_Brain/Systemic/Templates/Periodic/*.md` |
| `scaffold/03_Resources/_Templates/para/*.md` | `$VAULT/03_Resources/_Templates/para/*.md` |

### 3. Compare Each Template

For each template file, determine its sync status:

| Status | Condition | Action |
|--------|-----------|--------|
| **Identical** | Files match exactly | Skip (report as synced) |
| **Scaffold only** | File exists only in scaffold | Prompt: copy to vault? |
| **Vault only** | File exists only in vault | Prompt: copy to scaffold? |
| **Different** | Both exist but differ | Show diff, prompt for direction |

### 4. Interactive Merge (Per-File)

For each file that differs, present the diff and ask:

```
📄 Templates/Captive/today.md

--- scaffold (engine)
+++ vault (user)
[diff output]

Choose action:
- ← Pull (vault → scaffold) - bring user customizations to engine
- → Push (scaffold → vault) - apply engine updates to vault
- Skip - leave both unchanged
```

Use `AskUserQuestion` with options:
- `← Pull` - Copy from vault to scaffold
- `→ Push` - Copy from scaffold to vault
- `Skip` - No action for this file

### 5. Execute Actions

For each user decision:
- **Pull**: Copy `$VAULT/.../file.md` → `scaffold/.../file.md`
- **Push**: Copy `scaffold/.../file.md` → `$VAULT/.../file.md`
- **Skip**: No file operation

### 6. Report Summary

Show final summary:

```
Template Sync Complete

✓ Synced: 5 files (identical)
← Pulled: 2 files (vault → scaffold)
→ Pushed: 1 file (scaffold → vault)
⊘ Skipped: 1 file
```

## Notes

- This is a **development skill** for engine maintenance
- Always shows diffs before making changes
- Never overwrites without user confirmation
- Use after modifying templates in either location to keep them in sync
