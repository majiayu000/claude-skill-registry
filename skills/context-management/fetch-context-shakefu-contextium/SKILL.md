---
name: fetch-context
description: Load minimal relevant context for the current task
allowed-tools: Bash, Read, Grep, Glob
---

# Context Fetcher

Load minimal, task-relevant context following the "minimal by default" philosophy.

## Execution

Run the context fetcher agent:

```bash
./agents/context-fetcher.sh
```

## Context Philosophy

**Minimal by default.** Only load what's directly relevant to the current task:

- Full file contents → Just file paths
- All documentation → Only relevant sections
- Complete history → Just recent relevant commits
- Every test → Only tests for current scope

## Context Sources

| Source | What's Loaded |
|--------|---------------|
| `context/purpose.md` | Project goals (first 50 lines) |
| `.claude/claude.md` | Project-specific instructions |
| `.contextium/tasks.json` | Current task scope |
| `.contextium/context-cache/` | Task-specific cached context |

## Project Detection

Automatically detects project type:
- **Node.js** - package.json
- **Rust** - Cargo.toml
- **Python** - pyproject.toml, setup.py
- **Go** - go.mod

## Memory Systems

Reports availability of:
- **Memvid** - `.contextium/memory.mv2`
- **GibRAM** - Knowledge graph on port 6161

## Output

```
=== CONTEXT FOR SESSION ===
Project: contextium (docs)
Task: implement-feature-x

Key Files:
- src/features/x/index.ts: Main feature entry
- tests/features/x.test.ts: Feature tests

Available Memory:
- Memvid: no
- GibRAM: no
===========================
```

## Caching Task Context

To cache context for a task:

```bash
mkdir -p .contextium/context-cache
cat > .contextium/context-cache/my-task.md << 'EOF'
# Context for my-task

## Relevant Files
- src/module.ts - Main implementation
- tests/module.test.ts - Tests

## Notes
- Uses pattern X for Y
- Must maintain backwards compatibility
EOF
```
