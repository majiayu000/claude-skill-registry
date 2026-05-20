---
name: warden-skill
description: Guide for using Warden CLI locally to analyze code changes. Use when running warden commands, configuring warden.toml, creating custom skills, understanding triggers, or troubleshooting analysis issues. Triggers on "run warden", "warden config", "warden.toml", "create warden skill", "add trigger", or any Warden-related local development task.
---

# Warden Usage

Warden is an event-driven AI agent that analyzes code changes and executes configurable skills to produce structured reports with findings.

## Quick Start

```bash
# Set API key
export WARDEN_ANTHROPIC_API_KEY=sk-ant-...

# Analyze uncommitted changes (uses warden.toml triggers)
warden

# Run specific skill on uncommitted changes
warden --skill find-bugs

# Analyze specific files
warden src/auth.ts src/database.ts

# Analyze changes from git ref
warden main..HEAD
warden HEAD~3
```

## CLI Reference

```
warden [command] [targets...] [options]
```

**Commands:**
- `(default)` - Run analysis
- `init` - Initialize warden.toml and GitHub workflow
- `add [skill]` - Add skill trigger to warden.toml
- `sync [repo]` - Update cached remote skills to latest
- `setup-app` - Create GitHub App via manifest flow

**Targets:**
- `<files>` - Specific files (e.g., `src/auth.ts`)
- `<glob>` - Pattern match (e.g., `src/**/*.ts`)
- `<git-ref>` - Git range (e.g., `main..HEAD`, `HEAD~3`)
- `(none)` - Uncommitted changes

**Key Options:**
| Option | Description |
|--------|-------------|
| `--skill <name>` | Run only this skill |
| `--config <path>` | Path to warden.toml (default: ./warden.toml) |
| `-m, --model <model>` | Model to use |
| `--json` | Output as JSON |
| `-o, --output <path>` | Write output to JSONL file |
| `--fail-on <severity>` | Exit 1 if findings >= severity |
| `--comment-on <severity>` | Show findings >= severity |
| `--fix` | Auto-apply suggested fixes |
| `--parallel <n>` | Concurrent executions (default: 4) |
| `--offline` | Use cached remote skills only |
| `-q, --quiet` | Errors and summary only |
| `-v, --verbose` | Show real-time findings |
| `-vv` | Debug info (tokens, latency) |

**Severity levels:** `critical`, `high`, `medium`, `low`, `info`, `off`

## Configuration (warden.toml)

See [references/config-schema.md](references/config-schema.md) for complete schema.

**Minimal example:**

```toml
version = 1

[defaults]
model = "claude-sonnet-4-20250514"

[[triggers]]
name = "find-bugs"
event = "pull_request"
actions = ["opened", "synchronize"]
skill = "find-bugs"

[triggers.filters]
paths = ["src/**/*.ts"]
```

**With custom output thresholds:**

```toml
[[triggers]]
name = "security-strict"
event = "pull_request"
actions = ["opened", "synchronize"]
skill = "security-review"

[triggers.filters]
paths = ["src/auth/**", "src/payments/**"]

[triggers.output]
failOn = "critical"
commentOn = "high"
maxFindings = 20
```

## Creating Custom Skills

Skills live in `.warden/skills/`, `.agents/skills/`, or `.claude/skills/`.

**Structure:**
```
.warden/skills/my-skill/
└── SKILL.md
```

**SKILL.md format:**

```markdown
---
name: my-skill
description: What this skill analyzes
allowed-tools: Read Grep Glob
---

[Analysis instructions for the agent]

## What to Look For
- Specific issue type 1
- Specific issue type 2

## Output Format
Report findings with severity, location, and suggested fix.
```

**Available tools:** `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Bash`, `Write`, `Edit`

## Remote Skills

Skills can be fetched from GitHub repositories:

```bash
# Add a remote skill
warden add --remote getsentry/skills --skill security-review

# Add with version pinning (recommended for reproducibility)
warden add --remote getsentry/skills@abc123 --skill security-review

# List skills in a remote repo
warden add --remote getsentry/skills --list

# Update all unpinned remote skills
warden sync

# Update specific repo
warden sync getsentry/skills

# Run with cached skills only (no network)
warden --offline
```

**Remote trigger in warden.toml:**

```toml
[[triggers]]
name = "security-review"
event = "pull_request"
actions = ["opened", "synchronize"]
skill = "security-review"
remote = "getsentry/skills@abc123"
```

**Cache location:** `~/.local/warden/skills/` (override with `WARDEN_STATE_DIR`)

**Cache TTL:** 24 hours for unpinned refs (override with `WARDEN_SKILL_CACHE_TTL` in seconds)

## Common Patterns

**Strict security on critical files:**
```toml
[[triggers]]
name = "auth-security"
event = "pull_request"
actions = ["opened", "synchronize"]
skill = "security-review"
model = "claude-opus-4-20250514"
maxTurns = 100

[triggers.filters]
paths = ["src/auth/**", "src/payments/**"]

[triggers.output]
failOn = "critical"
```

**Skip test files:**
```toml
[triggers.filters]
paths = ["src/**/*.ts"]
ignorePaths = ["**/*.test.ts", "**/*.spec.ts"]
```

**Whole-file analysis for configs:**
```toml
[defaults.chunking.filePatterns]
pattern = "*.config.*"
mode = "whole-file"
```

## Troubleshooting

**No findings reported:**
- Check `--comment-on` threshold (default shows all)
- Verify skill matches file types in `filters.paths`
- Use `-v` to see which files are being analyzed

**Files being skipped:**
- Built-in skip patterns: lock files, minified, `node_modules/`, `dist/`
- Check `ignorePaths` in config
- Use `-vv` to see skip reasons

**Token/cost issues:**
- Reduce `maxTurns` (default: 50)
- Use chunking settings to control chunk size
- Filter to relevant files with `paths`
