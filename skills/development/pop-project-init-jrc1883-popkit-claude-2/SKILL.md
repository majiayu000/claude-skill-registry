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
| 1b   | Monorepo detected         | `monorepo_config`  |
| 1c   | Stack/framework selection | `stack_selection`  |
| 5b   | Quality gate level        | `quality_gates`    |
| 6    | After directory creation  | `power_mode_setup` |
| 6b   | If authenticated          | `premium_features` |
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

### Step 1: Run Interactive Detection

```bash
python scripts/interactive_init.py --dir .
```

This runs all 4 detections (monorepo, stack, quality, premium) and outputs JSON with detection results and question configurations.

### Step 1b: Monorepo Configuration (if detected)

Only shown if `interactive_init.py` detects a monorepo workspace.

```
Use AskUserQuestion:
- question: "Monorepo detected ({type}, {N} packages). How should PopKit be configured?"
- header: "Workspace"
- options:
  - "App-specific config (Recommended)" - Configure PopKit for this app only
  - "Shared workspace config" - Single config at workspace root
  - "Both (hybrid)" - Workspace config with app-specific overrides
```

### Step 1c: Stack Selection (MANDATORY)

Uses detection results to pre-select the most likely option.

```
Use AskUserQuestion:
- question: "Detected {stack}. Confirm or change project type?" (or "What type of project?" if no detection)
- header: "Stack"
- options: (top 4 from detection, detected stack marked as "(Detected)")
  - "Next.js Application" / "Python FastAPI" / "Cloudflare Workers" / "React SPA"
```

The selected stack determines: config templates, quality tool defaults, and CLAUDE.md content.

### Step 2: Create Structure

```bash
# Create directories based on stack selection
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

### Step 5b: Quality Gates Selection (MANDATORY)

Uses detection to recommend a level based on existing tools.

```
Use AskUserQuestion:
- question: "What quality gate level? (eslint, prettier detected)" (tools vary)
- header: "Quality"
- options:
  - "Basic" - Formatting only (Prettier/Ruff). Fast, minimal overhead.
  - "Standard (Recommended)" - Formatting + linting + type checking.
  - "Strict" - All of Standard + pre-commit hooks + test requirements.
  - "Enterprise" - All of Strict + security scanning + audit logging.
```

Configure pre-commit hooks, linting, and type checking based on selection.
Map to `/popkit:project setup` levels: basic, standard, strict, enterprise.

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

### Step 6b: Premium Features (if authenticated)

Only shown if `POPKIT_API_KEY` or `VOYAGE_API_KEY` environment variables are set.

```
Use AskUserQuestion:
- question: "Which premium features would you like to enable?"
- header: "Features"
- multiSelect: true
- options:
  - "Power Mode (Recommended)" - Multi-agent orchestration for parallel task execution
  - "Semantic Search" - Natural language search for skills, agents, and commands
  - "Cloud Sync" - Cross-session state and analytics via PopKit Cloud
```

Update `.claude/popkit/config.json` with selected features.

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
[1/7] Checking conflicts... ✓ No conflicts
[2/7] Detecting environment... ✓ Monorepo (pnpm, 6 packages) | Next.js
[3/7] Creating structure... ✓ .claude/popkit/config.json
[4/7] Updating CLAUDE.md... ✓ Section appended with markers
[5/7] Quality gates... ✓ Standard (ESLint + TypeScript + Ruff)
[6/7] Power Mode... ✓ [Based on selection]
[7/7] Premium features... ✓ Power Mode + Semantic Search

Summary:
  Stack: Next.js Application
  Config: .claude/popkit/config.json
  Quality: Standard (3 tools configured)
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
