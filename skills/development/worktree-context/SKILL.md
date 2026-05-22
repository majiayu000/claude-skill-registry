# Worktree Context Skill

Provides centralized worktree handling for workflow commands, eliminating ~50 lines of inline code per command.

## Purpose

Git worktrees enable parallel development by allowing multiple branches to be checked out simultaneously. This skill provides a single source of truth for worktree detection, creation, and context generation.

## Quick Reference

```bash
# Check if in worktree
bash .spec-flow/scripts/bash/worktree-context.sh in-worktree && echo "yes" || echo "no"

# Get worktree info (JSON)
bash .spec-flow/scripts/bash/worktree-context.sh info

# Create worktree for feature
bash .spec-flow/scripts/bash/worktree-context.sh create "feature" "001-auth" "feature/001-auth"

# Generate Task() agent context block
bash .spec-flow/scripts/bash/worktree-context.sh context "/path/to/worktree"
```

## Output Format

### Info Command

Returns JSON with worktree details:

```json
{
  "is_worktree": true,
  "worktree_path": "/path/to/worktrees/feature/001-auth",
  "root_path": "/path/to/main/repo",
  "branch": "feature/001-auth",
  "worktree_type": "feature",
  "worktree_slug": "001-auth"
}
```

### Fields

| Field | Values | Description |
|-------|--------|-------------|
| `is_worktree` | boolean | Whether currently in a worktree |
| `worktree_path` | string | Absolute path to worktree |
| `root_path` | string | Absolute path to main repository |
| `branch` | string | Current git branch |
| `worktree_type` | `feature`, `epic` | Type of worktree |
| `worktree_slug` | string | Feature/epic slug |

## Compact Pattern (v11.2)

### In Command Process Section

Replace 50+ lines of inline worktree detection with this compact reference:

```markdown
### Step N: Worktree Context (Optional)

**Check worktree using centralized skill** (see `.claude/skills/worktree-context/SKILL.md`):

1. Check preference: `bash .spec-flow/scripts/utils/load-preferences.sh --key "worktrees.auto_create" --default "true"`
2. Check if already in worktree: `bash .spec-flow/scripts/bash/worktree-context.sh in-worktree`
3. If NOT in worktree AND auto_create is true:
   - Create: `bash .spec-flow/scripts/bash/worktree-context.sh create "feature" "$SLUG" "$BRANCH"`
   - Store path in state.yaml: `yq eval ".git.worktree_path = \"$PATH\"" -i state.yaml`
4. For Task() agents, generate context: `bash .spec-flow/scripts/bash/worktree-context.sh context "$PATH"`
```

### For Task() Agent Prompts

When spawning worker agents that need to operate in a worktree:

```markdown
## Worktree Context

${WORKTREE_PATH ? `
**WORKTREE MODE (CRITICAL)**

Path: ${WORKTREE_PATH}

Execute this FIRST:
\`\`\`bash
cd "${WORKTREE_PATH}"
\`\`\`

All paths are relative to worktree root.
Git commits stay local to worktree branch.
Do NOT merge or push - orchestrator handles that.
` : `
**NORMAL MODE**
Working in main repository.
`}
```

## Commands

| Command | Purpose |
|---------|---------|
| `in-worktree` | Check if in worktree (exit 0 = yes) |
| `info` | Get current worktree info (JSON) |
| `root` | Get main repository path |
| `create TYPE SLUG BRANCH` | Create new worktree |
| `path SLUG` | Get worktree path for slug |
| `context PATH` | Generate Task() agent context block |
| `run PATH CMD` | Run command in worktree |
| `git PATH ARGS` | Run git command in worktree |
| `merge SLUG` | Merge worktree branch to main |
| `sync PATH` | Sync state files from worktree |
| `cleanup [--dry-run]` | Remove merged worktrees |
| `relative-path PATH` | Extract worktree-relative path |
| `extract-slug PATH` | Extract slug from any path format |

## Usage in Commands

### /feature Command

Before (50+ lines inline):
```markdown
### Step 1.1.5: Create Worktree (If Preference Enabled)

Check worktree context and preference:

\`\`\`bash
# Check if already in a worktree
IS_WORKTREE=$(bash .spec-flow/scripts/bash/worktree-context.sh in-worktree && echo "true" || echo "false")

# Check worktree auto-create preference
WORKTREE_AUTO=$(bash .spec-flow/scripts/utils/load-preferences.sh --key "worktrees.auto_create" --default "true" 2>/dev/null)
...
# 40 more lines of worktree handling
\`\`\`
```

After (compact pattern):
```markdown
### Step 1.1.5: Create Worktree (If Preference Enabled)

**Handle worktree using centralized skill** (see `.claude/skills/worktree-context/SKILL.md`):

1. Check if worktree auto-create is enabled (preference: `worktrees.auto_create`)
2. If NOT in worktree AND enabled: Create via `worktree-context.sh create`
3. Store `worktree_path` in state.yaml for Task() agents
4. Generate context block for worker prompts
```

### /implement Command (Worker Agents)

Include worktree context in worker prompts:

```markdown
Task(worker):
  prompt: |
    ${WORKTREE_ENABLED ? generate_worktree_context(WORKTREE_PATH) : ""}

    Implement ONE feature from domain memory.
    ...
```

## Path Handling

### The Duplication Bug

When operating in worktrees, paths can get duplicated:
- Bad: `worktrees/epic/004-app/epics/004-app/epics/004-app`
- Good: `epics/004-app`

Use `relative-path` to fix:
```bash
bash .spec-flow/scripts/bash/worktree-context.sh relative-path "worktrees/epic/004-app/epics/004-app"
# Returns: epics/004-app
```

### Extracting Slugs

Extract slug from any path format:
```bash
bash .spec-flow/scripts/bash/worktree-context.sh extract-slug "specs/001-auth/domain-memory.yaml"
# Returns: 001-auth
```

## Related Files

- `.spec-flow/scripts/bash/worktree-context.sh` - Main implementation (540 lines)
- `.spec-flow/scripts/bash/worktree-manager.sh` - Worktree lifecycle management
- `docs/references/git-worktrees.md` - Deep documentation

## Benefits

| Before | After |
|--------|-------|
| 50+ lines inline per command | 5-10 lines referencing skill |
| Duplicated across 3+ commands | Single source of truth |
| Changes require multiple edits | Changes require 1 skill edit |
| Worktree bugs scattered | Worktree bugs centralized |
