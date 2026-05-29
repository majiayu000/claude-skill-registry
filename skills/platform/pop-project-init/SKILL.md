---
name: project-init
description: "Initialize .claude/ structure and surgically add PopKit section to CLAUDE.md without overwriting. Detects conflicts, creates config, prompts for Power Mode. Use for new projects only - use analyze-project for existing."
---

# Project Initialization

Initialize project with Claude Code configuration. **Never destroys user content** - surgically adds PopKit section using HTML markers.

**Trigger:** `/popkit:project init` or new project setup

## Critical Rules

1. **NEVER overwrite CLAUDE.md** - Read first, then EDIT (not Write)
2. **ALWAYS use `<!-- POPKIT:START/END -->` markers** - Required for updates
3. **ALWAYS create `.claude/popkit/`** - Required for deploy, routines, state
4. **Check plugin conflicts first**
5. **MANDATORY: Use AskUserQuestion** for all decisions (enforced by hooks)
6. **Preserve existing .claude/ content**

## Required Decision Points

| Step | When                      | Decision ID        |
| ---- | ------------------------- | ------------------ |
| 0    | Plugin conflicts detected | `plugin_conflict`  |
| 6    | After directory creation  | `power_mode_setup` |
| 8    | After init complete       | `next_action`      |

**Skipping these violates PopKit UX standard.**

## Process

### Step 0: Check Plugin Conflicts

```python
from plugin_detector import run_detection, format_conflict_report
result, plugins = run_detection()
if result["total"] > 0:
    # Use AskUserQuestion: "View details" | "Continue anyway" | "Cancel"
```

### Step 1-2: Detect Type & Create Structure

```bash
# Detect: package.json→node, Cargo.toml→rust, pyproject.toml→python, go.mod→go
mkdir -p .claude/{agents,commands,hooks,skills,scripts,logs,plans}
mkdir -p .claude/popkit/routines/{morning,nightly}
```

### Step 2b: Create PopKit Config

```python
# .claude/popkit/config.json
{
  "version": "1.0",
  "project_name": "<name>",
  "project_prefix": "<prefix>",  # First letters
  "default_routines": {"morning": "pk", "nightly": "pk"},
  "tier": "free",
  "features": {"power_mode": "not_configured"}
}
```

### Step 3: Surgically Update CLAUDE.md (CRITICAL)

**Decision Flow:**

```
CLAUDE.md exists?
├─ NO  → Create with: header + PopKit section
└─ YES → Read content
    ├─ Has markers? → Edit ONLY between markers
    └─ No markers?  → Append at END
```

**Markers (REQUIRED):**

```markdown
<!-- POPKIT:START -->

## PopKit Integration

Quick Commands: /popkit:next, /popkit:routine morning, /popkit:git commit
Config: .claude/popkit/, Power Mode: [status]

<!-- POPKIT:END -->
```

See `examples/claude-md-update.py` for full implementation.

### Step 4-5: Create STATUS.json & settings.json

Only if missing. See `examples/` for schemas.

### Step 6: Power Mode Setup (MANDATORY)

```
Use AskUserQuestion:
- question: "Set up Power Mode for multi-agent orchestration?"
- options:
  - "Native Async (Recommended)" - 5+ agents, zero setup (requires Claude Code 2.0.64+)
  - "Upstash Redis (Optional)" - 10+ agents, cloud-based, env vars only (no Docker)
  - "File Mode (Fallback)" - 2-3 agents, automatic fallback
  - "Skip for now"
```

Update CLAUDE.md with selected mode.

### Step 7: Update .gitignore

```
.claude/logs/
.claude/STATUS.json
.claude/power-mode-state.json
.claude/popkit/state.json
.worktrees/
.generated/
```

### Step 8: Next Action (MANDATORY)

```
Use AskUserQuestion:
- question: "What would you like to do next?"
- options:
  - "Analyze codebase" → /popkit:project analyze
  - "Setup quality gates" → /popkit:project setup
  - "View issues" → /popkit:issue list
  - "Done for now"
```

## Output Format

```
PopKit Project Initialization
═════════════════════════════
[1/5] Checking conflicts... ✓ No conflicts
[2/5] Detecting type... ✓ Node.js (Next.js 14)
[3/5] Creating structure... ✓ .claude/popkit/config.json
[4/5] Updating CLAUDE.md... ✓ Section appended with markers
[5/5] Power Mode... ✓ [Based on selection]

Summary:
  Config: .claude/popkit/config.json
  CLAUDE.md: <!-- POPKIT:START/END --> markers
  Power Mode: [status]
  Ready: /popkit:routine morning
```

## Verification

| Path                         | Purpose         |
| ---------------------------- | --------------- |
| `.claude/popkit/config.json` | Project config  |
| `.claude/popkit/routines/`   | Custom routines |
| `.claude/STATUS.json`        | Session state   |
| `CLAUDE.md`                  | Has markers     |

## Integration

**Triggers:** `/popkit:project init`, manual skill invocation

**Followed by:** analyze, mcp, setup, power init, issue list

## Visual Style

From `output-styles/visual-components.md`:

- Progress: `[1/5]`, `[2/5]`
- Status: ✓ (success), ✗ (failure), ⚠️ (warning)
- Headers: `═════════════════`

## Related

| Skill                 | Relationship          |
| --------------------- | --------------------- |
| `pop-analyze-project` | Run after init        |
| `pop-doc-sync`        | Keeps section in sync |
| `pop-plugin-test`     | Validates plugin      |

## Examples

See `examples/` for:

- `claude-md-update.py` - Full surgical update logic
- `config-schema.json` - PopKit config schema
- `status-schema.json` - STATUS.json schema
- `tier-comparison.md` - Free vs Premium vs Pro features
