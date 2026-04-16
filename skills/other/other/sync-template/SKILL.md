---
name: sync-template
description: Update an existing project's Claude Code configuration against the current dotforge template, without losing local customizations.
---

# Sync Template

Update the current project's Claude Code configuration against the latest version of dotforge.

## Principle: merge, not overwrite

NEVER overwrite existing files without confirmation. Compare and propose changes.
NEVER touch `settings.local.json` — it is the user's personal configuration.
NEVER modify sections marked with `<!-- forge:custom -->` in CLAUDE.md.

## Step 0: Verify global

Before syncing the project, verify that `~/.claude/CLAUDE.md` exists and contains behavior rules (communication, planning, autonomy). If global rules are active, the project's `_common.md` only needs technical rules (git, naming, testing, security). Do not duplicate what is already in global.

## Step 1: Detect current state

1. Read the current `.claude/settings.json`
2. Read the current `CLAUDE.md`
3. Read existing `.claude/rules/`
4. Read existing `.claude/hooks/`
5. Detect stacks using `$DOTFORGE_DIR/stacks/detect.md`
6. Read `~/.claude/CLAUDE.md` to know which rules are already covered globally

## Step 2: Compare against template

For each component, compare with the dotforge version:

### settings.json — Smart merge
- **allow**: union of sets. Add missing permissions from base template + stacks. NEVER remove local permissions the project already has.
- **deny**: union of sets. Add missing security denies. NEVER remove local denies.
- **hooks**: add missing hooks from template. Preserve custom project hooks.
- **Other fields**: preserve everything that is not allow/deny/hooks (e.g., MCP configs).

### Rules
- Is `_common.md` missing? → propose adding it
- Are rules for the detected stack missing? → propose adding them
- Are existing rules outdated? → show diff, propose update
- Custom project rules (not in template) → DO NOT TOUCH
- `.claude/rules/domain/` → NEVER TOUCH. Domain rules are project-owned knowledge, not template-managed. Skip entirely during sync.

### Hooks
- Is `block-destructive.sh` missing? → propose adding + chmod +x
- Is the stack's lint hook missing? → propose adding + chmod +x
- Custom project hooks → DO NOT TOUCH
- Verify that existing hooks are executable (chmod +x)

### CLAUDE.md
- Compare standard template sections with the project's sections
- Sections with `<!-- forge:custom -->` → SKIP entirely
- Missing template sections → propose adding
- Custom project sections → DO NOT TOUCH

## Step 3: Generate dry-run

Show the user what would change BEFORE applying anything:
```
═══ SYNC DRY-RUN: {{project}} ═══
dotforge: {{version}} (current project: {{previous_version or "unknown"}})

NEW FILES (will be created):
+ .claude/rules/_common.md
+ .claude/hooks/block-destructive.sh

UPDATED FILES (merge):
~ .claude/settings.json
  + allow: "Bash(docker *)", "Bash(docker compose *)"
  + deny: "**/.env.local"
  (local permissions preserved: "Bash(custom-script *)")

~ .claude/rules/backend.md
  diff: +3 lines (new common errors)

NO CHANGES:
= .claude/rules/frontend.md (already up to date)
= .claude/hooks/lint-ts.sh (already up to date)

IGNORED (custom):
⊘ .claude/rules/strategies.md (not in template)
⊘ CLAUDE.md section "<!-- forge:custom -->"

Apply changes? (yes/no/select)
```

## Step 4: Apply with confirmation

Only apply the changes the user approves.
- `yes` → apply all
- `no` → cancel
- `select` → show each change and ask yes/no individually

For settings.json: build the final merged JSON. Before writing, validate that the JSON is valid:

```bash
echo '<json_content>' | python3 -c 'import json,sys; json.load(sys.stdin)'
```

If validation fails, show the exact error and DO NOT write the file. Fix the JSON before continuing.

For hooks: copy + `chmod +x`.

## Step 4b: Update manifest

After applying changes, update (or create) `.claude/.forge-manifest.json`:

1. If manifest exists, read it
2. For each file created or modified during sync, recalculate hash:
   ```bash
   shasum -a 256 <file> | cut -d' ' -f1
   ```
3. Update `dotforge_version`, `synced_at`, and `stacks` (from detected stacks)
4. Write the updated manifest

Format:
```json
{
  "dotforge_version": "<version from $DOTFORGE_DIR/VERSION>",
  "synced_at": "<current date YYYY-MM-DD>",
  "stacks": ["<detected-stack-1>", "<detected-stack-2>"],
  "files": {
    ".claude/settings.json": {"hash": "sha256:<hash>", "source": "template+stacks"},
    ".claude/rules/_common.md": {"hash": "sha256:<hash>", "source": "template"}
  }
}
```

Include ALL files in `.claude/` that are managed by dotforge (not only those that changed in this sync).

## Step 5: Update registry

Update in `$DOTFORGE_DIR/registry/projects.yml`:
- `last_sync:` → current date
- `dotforge_version:` → current dotforge version

## Step 6: Verify

Run the `/audit-project` logic to confirm the score improved or held steady.
Show score before and after.
