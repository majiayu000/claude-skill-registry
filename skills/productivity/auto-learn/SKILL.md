---
name: auto-learn
description: Automatic learning from session command patterns
user-invocable: false
---

# Auto-Learn

Automatically detects recurring command patterns during sessions and suggests or applies learnings to CLAUDE.md files.

## Overview

The auto-learn system observes commands run during a Claude Code session and, when patterns emerge (same command run multiple times), either suggests adding them as learnings to CLAUDE.md or automatically applies them.

**Flow:**

1. **Observe** (PreToolUse on Bash): Tracks commands during the session
2. **Synthesize** (Stop event): Analyzes patterns and generates suggestions
3. **Apply/Suggest**: Writes to CLAUDE.md (auto mode) or shows suggestions (suggest mode)

## Configuration

Enable and configure via `/bluera-base:config`:

```bash
# Enable auto-learning (opt-in, disabled by default)
/bluera-base:config enable auto-learn

# Set mode: suggest (default) or auto
/bluera-base:config set .autoLearn.mode auto

# Set occurrence threshold (default: 3)
/bluera-base:config set .autoLearn.threshold 5

# Set target file: local (default) or shared
/bluera-base:config set .autoLearn.target shared
```

### Configuration Options

| Option | Path | Values | Default | Description |
|--------|------|--------|---------|-------------|
| Enabled | `.autoLearn.enabled` | `true`/`false` | `false` | Opt-in to enable tracking |
| Mode | `.autoLearn.mode` | `suggest`/`auto` | `suggest` | How to handle learnings |
| Threshold | `.autoLearn.threshold` | number | `3` | Occurrences before acting |
| Target | `.autoLearn.target` | `local`/`shared` | `local` | Where to write learnings |

### Modes

| Mode | Behavior |
|------|----------|
| `suggest` | Shows learnings as systemMessage at session end. User runs `/bluera-base:claude-md learn` to apply. |
| `auto` | Writes learnings directly to target file. Shows confirmation message. |

### Targets

| Target | File | Shared | Notes |
|--------|------|--------|-------|
| `local` | `CLAUDE.local.md` | No | Auto-gitignored by Claude Code |
| `shared` | `CLAUDE.md` | Yes | Committed to repo, shared with team |

## Pattern Detection

Commands are normalized and counted during each session:

| Pattern | Example Commands | Suggested Learning |
|---------|-----------------|-------------------|
| `npm:test`, `bun:test`, `yarn:test` | `npm test`, `bun run test` | "Run tests frequently during development" |
| `npm:lint`, `bun:lint`, `cargo:clippy` | `npm run lint` | "Run linter before committing" |
| `npm:build`, `cargo:build`, `go:build` | `npm run build` | "Build verification is part of workflow" |
| `git:status`, `git:diff` | `git status` | "Check git status before commits" |

Commands are normalized to `tool:subcommand` format for consistent tracking.

## File Format

Learnings are stored in a marker-delimited region:

```markdown
## Auto-Learned (bluera-base)
<!-- AUTO:bluera-base:learned -->
- Run tests frequently during development
- Run linter before committing
<!-- END:bluera-base:learned -->
```

**Marker rules:**

- Section header: `## Auto-Learned (bluera-base)`
- Start marker: `<!-- AUTO:bluera-base:learned -->`
- End marker: `<!-- END:bluera-base:learned -->`
- Each learning is a bullet point (`-`)

## Safety Features

### Secrets Detection

Learnings matching sensitive patterns are **always rejected**:

```text
api[_-]?key|token|password|secret|-----BEGIN|AWS_|GITHUB_TOKEN|ANTHROPIC_API|OPENAI_API|private[_-]?key|credential
```

### Deduplication

Before writing, learnings are normalized (lowercase, trimmed) and compared against existing content. Duplicates are silently skipped.

### Hard Cap

Maximum **50 learnings** in the auto-managed section. If exceeded, a warning is shown and no new learnings are written.

### Opt-In

Auto-learn is **disabled by default**. Users must explicitly enable it:

```bash
/bluera-base:config enable auto-learn
```

## State Files

| File | Purpose |
|------|---------|
| `.bluera/bluera-base/state/session-signals.json` | Tracks command counts per session |

The signals file is cleared after synthesis (at session end).

## Implementation Files

| File | Purpose |
|------|---------|
| `hooks/observe-learning.sh` | PreToolUse hook - tracks Bash commands |
| `hooks/session-end-learn.sh` | Stop hook - synthesizes and applies learnings |
| `hooks/lib/autolearn.sh` | Library - writing functions (target resolution, dedup, secrets check) |
| `hooks/lib/signals.sh` | Library - session signals state management |
| `hooks/lib/config.sh` | Library - configuration loading |

## Related

- `/bluera-base:config` - Enable and configure auto-learn
- `/bluera-base:claude-md learn` - Manually add a learning
- `skills/claude-md-maintainer` - Full CLAUDE.md management skill
