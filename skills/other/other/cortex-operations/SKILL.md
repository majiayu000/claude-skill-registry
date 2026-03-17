---
name: cortex-operations
description: Operate the Agent Hive Cortex orchestration engine. Use this skill when running Cortex commands, analyzing project dependencies, finding ready work, understanding the orchestration system, or troubleshooting Cortex issues.
---

# Cortex Operations

The Cortex is Agent Hive's orchestration engine - the central nervous system that reads project state, analyzes dependencies, and coordinates AI agents.

## Cortex Modes

### 1. Full LLM Analysis (Default)

Runs complete analysis using an LLM to identify blocked tasks, suggest state updates, and detect new project requests.

```bash
# Run full analysis
uv run python -m src.cortex

# Or using make
make cortex
```

**What it does:**
- Reads GLOBAL.md and all AGENCY.md files
- Calls LLM to analyze system state
- Identifies blocked tasks and recommendations
- Applies state updates to project files
- Updates `last_cortex_run` timestamp

**Requirements:**
- `OPENROUTER_API_KEY` environment variable
- `OPENROUTER_MODEL` (optional, defaults to `anthropic/claude-haiku-4.5`)

### 2. Ready Work Detection (Fast, No LLM)

Quickly finds projects ready for an agent to claim without requiring API calls.

```bash
# Human-readable output
uv run python -m src.cortex --ready

# JSON output for programmatic use
uv run python -m src.cortex --ready --json
```

**Ready criteria:**
- `status == 'active'`
- `blocked == false`
- `owner == null` (unclaimed)
- No unresolved `dependencies.blocked_by`

### 3. Dependency Graph Analysis (Fast, No LLM)

Visualizes project dependencies and detects cycles.

```bash
# Human-readable tree view
uv run python -m src.cortex --deps

# JSON output
uv run python -m src.cortex --deps --json
```

**Output includes:**
- All projects with their status
- Dependency relationships (blocks/blocked_by)
- Cycle detection warnings
- ASCII dependency tree

## Command Reference

| Command | Description |
|---------|-------------|
| `uv run python -m src.cortex` | Full LLM analysis |
| `uv run python -m src.cortex --ready` | Find ready work |
| `uv run python -m src.cortex --deps` | Show dependency graph |
| `uv run python -m src.cortex --json` | JSON output (with --ready or --deps) |
| `uv run python -m src.cortex --path /custom/path` | Use custom base path |

## Understanding Output

### Ready Work Output

```
============================================================
READY WORK
============================================================
Timestamp: 2025-01-15T14:30:00
Found 2 project(s) ready for work

!!  feature-auth
    Priority: high
    Tags: feature, security
    Path: projects/feature-auth/AGENCY.md

!   docs-update
    Priority: medium
    Tags: documentation
    Path: projects/docs-update/AGENCY.md
============================================================
```

Priority indicators:
- `!!!` - critical
- `!! ` - high
- `!  ` - medium
- `   ` - low

### Dependency Graph Output

```
============================================================
DEPENDENCY GRAPH
============================================================
BLOCKED PROJECTS:
----------------------------------------
*** phase-2
    Status: active
    Blocked by: phase-1
    Reason: Blocked by uncompleted: phase-1

UNBLOCKED PROJECTS:
----------------------------------------
    phase-1 [active]
      Blocks: phase-2
    standalone [active]

DEPENDENCY TREE:
----------------------------------------
[*] phase-1
  [*] phase-2
[*] standalone

Legend: [+] completed  [*] active  [!] blocked  [-] pending
============================================================
```

## Cycle Detection

The Cortex detects circular dependencies that can never be resolved:

```
!!! CYCLES DETECTED !!!
    project-a -> project-b -> project-c -> project-a
```

**To fix cycles:**
1. Review the dependency chain
2. Remove or modify one of the `blocked_by` relationships
3. Re-run `--deps` to verify resolution

## GitHub Actions Integration

The Cortex runs automatically every 4 hours via `.github/workflows/cortex.yml`:

```yaml
on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
```

**Workflow steps:**
1. Checkout repository
2. Install dependencies with uv
3. Run Cortex
4. Commit changes if state was updated

**Required secrets:**
- `OPENROUTER_API_KEY`

## Troubleshooting

### "OPENROUTER_API_KEY not set"

```bash
# Set in .env file
echo "OPENROUTER_API_KEY=sk-or-v1-xxxxx" >> .env

# Or export directly
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

### "GLOBAL.md not found"

Ensure you're running from the hive root directory:

```bash
cd /path/to/agent-hive
uv run python -m src.cortex
```

Or specify the path:

```bash
uv run python -m src.cortex --path /path/to/agent-hive
```

### "No projects found"

Verify projects directory exists with AGENCY.md files:

```bash
ls projects/*/AGENCY.md
```

### LLM Response Parse Error

The Cortex expects JSON from the LLM. If parsing fails:
- Check API key validity
- Try a different model in `OPENROUTER_MODEL`
- Check console output for raw response

## Programmatic Usage

```python
from src.cortex import Cortex

# Initialize
cortex = Cortex(base_path="/path/to/hive")

# Discover projects
projects = cortex.discover_projects()

# Get ready work
ready = cortex.ready_work(projects)

# Check if specific project is blocked
blocking_info = cortex.is_blocked("project-id", projects)

# Get full dependency summary
summary = cortex.get_dependency_summary(projects)
```
