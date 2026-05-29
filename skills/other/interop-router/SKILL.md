---
name: interop-router
description: >
  Automatically routes tasks to external AI CLIs (Codex or Gemini) when more efficient.
  No manual commands needed - routing decisions are made automatically based on task type.
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Automatic Routing to External AI CLIs

**Auto-trigger**: This skill evaluates tasks automatically and decides whether to delegate to an external CLI. No manual invocation needed.

---

## Auto-Trigger Conditions

Automatically evaluate when detecting:
- Large refactoring (10+ files affected)
- Batch file changes
- Template generation tasks
- Multi-model cross-validation needs

---

## Decision Scoring

Calculate delegation score using 3 factors:

| Factor | Range | Description |
|--------|-------|-------------|
| Benefit | 0.0 - 0.6 | Can external CLI produce faster/more reliable results? |
| Cost | -0.3 - 0.0 | Overhead of wrapping, normalizing, reviewing |
| Risk | -0.3 - 0.0 | Permission/write/secret leakage risks |

**Threshold**: Score >= 0.15 with auto-interop enabled -> auto-execute delegation

---

## Routing Targets

| Task Type | Target CLI | Reason |
|-----------|------------|--------|
| Large codebase exploration | Gemini | 1M token context |
| Batch implementation | Codex | Fast bulk generation |
| Complex architecture analysis | Gemini | Deep reasoning |
| Template generation | Codex | Efficient structured output |

---

## Process

### 1. Check CLI Availability

```bash
bash "$CLAUDE_PROJECT_DIR/skills/interop-router/scripts/check_cli_available.sh" --json
```

### 2. Score the Decision

```bash
python3 "$CLAUDE_PROJECT_DIR/skills/interop-router/scripts/score_decision.py" \
  --task "task description" \
  --files 15 \
  --complexity high \
  --json
```

### 3. Wrap Context (if delegating)

```bash
python3 "$CLAUDE_PROJECT_DIR/skills/interop-router/scripts/wrap_context.py" \
  --files src/*.py \
  --diff \
  --output /tmp/context.md
```

### 4. Execute with External CLI

```bash
# Codex
codex "Your task description" < /tmp/context.md

# Gemini
gemini "Your task description" -f /tmp/context.md
```

---

## Safety Constraints

- Default read-only mode
- Automatic secret filtering (API keys, passwords, tokens, connection strings)
- All results must be reviewed before landing
- Sensitive files (.env, credentials, private keys) are always skipped

---

## Configuration

Enable auto-interop:

```bash
# Project-level (takes precedence)
mkdir -p .claude/flags
echo '{"enabled": true}' > .claude/flags/auto-interop.json

# User-level
mkdir -p ~/.claude/flags
echo '{"enabled": true}' > ~/.claude/flags/auto-interop.json
```
