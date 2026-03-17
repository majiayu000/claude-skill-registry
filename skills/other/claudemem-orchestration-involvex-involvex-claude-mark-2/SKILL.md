---
name: claudemem-orchestration
description: "Multi-agent code analysis orchestration using claudemem. Share claudemem output across parallel agents. Enables parallel investigation, consensus analysis, and role-based command mapping."
allowed-tools: Bash, Task, Read, Write, AskUserQuestion
skills: orchestration:multi-model-validation
---

# Claudemem Multi-Agent Orchestration

**Version:** 1.0.0
**Purpose:** Coordinate multiple agents using shared claudemem output

## Overview

When multiple agents need to investigate the same codebase:
1. **Run claudemem ONCE** to get structural overview
2. **Write output to shared file** in session directory
3. **Launch agents in parallel** - all read the same file
4. **Consolidate results** with consensus analysis

This pattern avoids redundant claudemem calls and enables consensus-based prioritization.

**For parallel execution patterns, see:** `orchestration:multi-model-validation` skill

## Claudemem-Specific Patterns

This skill focuses on claudemem-specific orchestration. For general parallel execution:
- **4-Message Pattern** - See `orchestration:multi-model-validation` Pattern 1
- **Session Setup** - See `orchestration:multi-model-validation` Pattern 0
- **Statistics Collection** - See `orchestration:multi-model-validation` Pattern 7

### Pattern 1: Shared Claudemem Output

**Purpose:** Run expensive claudemem commands ONCE, share results across agents.

```bash
# Create unique session directory (per orchestration:multi-model-validation Pattern 0)
SESSION_ID="analysis-$(date +%Y%m%d-%H%M%S)-$(head -c 4 /dev/urandom | xxd -p)"
SESSION_DIR="/tmp/${SESSION_ID}"
mkdir -p "$SESSION_DIR"

# Run claudemem ONCE, write to shared files
claudemem --nologo map "feature area" --raw > "$SESSION_DIR/structure-map.md"
claudemem --nologo test-gaps --raw > "$SESSION_DIR/test-gaps.md" 2>&1 || echo "No gaps found" > "$SESSION_DIR/test-gaps.md"
claudemem --nologo dead-code --raw > "$SESSION_DIR/dead-code.md" 2>&1 || echo "No dead code" > "$SESSION_DIR/dead-code.md"

# Export session info
echo "$SESSION_ID" > "$SESSION_DIR/session-id.txt"
```

**Why shared output matters:**
- Claudemem indexing is expensive (full AST parse)
- Same index serves all queries in session
- Parallel agents reading same file = no redundant computation

### Pattern 2: Role-Based Agent Distribution

After running claudemem, distribute to role-specific agents:

```
# Parallel Execution (ONLY Task calls - per 4-Message Pattern)
Task: architect-detective
  Prompt: "Analyze architecture from $SESSION_DIR/structure-map.md.
           Focus on layer boundaries and design patterns.
           Write findings to $SESSION_DIR/architect-analysis.md"
---
Task: tester-detective
  Prompt: "Analyze test gaps from $SESSION_DIR/test-gaps.md.
           Prioritize coverage recommendations.
           Write findings to $SESSION_DIR/tester-analysis.md"
---
Task: developer-detective
  Prompt: "Analyze dead code from $SESSION_DIR/dead-code.md.
           Identify cleanup opportunities.
           Write findings to $SESSION_DIR/developer-analysis.md"

All 3 execute simultaneously (3x speedup!)
```

### Pattern 3: Consolidation with Ultrathink

```
Task: ultrathink-detective
  Prompt: "Consolidate analyses from:
           - $SESSION_DIR/architect-analysis.md
           - $SESSION_DIR/tester-analysis.md
           - $SESSION_DIR/developer-analysis.md

           Create unified report with prioritized action items.
           Write to $SESSION_DIR/consolidated-analysis.md"
```

## Role-Based Command Mapping

| Agent Role | Primary Commands | Secondary Commands | Focus |
|------------|------------------|-------------------|-------|
| Architect | `map`, `dead-code` | `context` | Structure, cleanup |
| Developer | `callers`, `callees`, `impact` | `symbol` | Modification scope |
| Tester | `test-gaps` | `callers` | Coverage priorities |
| Debugger | `context`, `impact` | `symbol`, `callers` | Error tracing |
| Ultrathink | ALL | ALL | Comprehensive |

## Sequential Investigation Flow

For complex bugs or features requiring ordered investigation:

```
Phase 1: Architecture Understanding
  claudemem --nologo map "problem area" --raw
  Identify high-PageRank symbols (> 0.05)

Phase 2: Symbol Deep Dive
  For each high-PageRank symbol:
    claudemem --nologo context <symbol> --raw
    Document dependencies and callers

Phase 3: Impact Assessment (v0.4.0+)
  claudemem --nologo impact <primary-symbol> --raw
  Document full blast radius

Phase 4: Gap Analysis (v0.4.0+)
  claudemem --nologo test-gaps --min-pagerank 0.01 --raw
  Identify coverage holes in affected code

Phase 5: Action Planning
  Prioritize by: PageRank * impact_depth * test_coverage
```

## Agent System Prompt Integration

When an agent needs deep code analysis, it should reference the claudemem skill:

```yaml
---
skills: code-analysis:claudemem-search, code-analysis:claudemem-orchestration
---
```

The agent then follows this pattern:

1. **Check claudemem status**: `claudemem status`
2. **Index if needed**: `claudemem index`
3. **Run appropriate command** based on role
4. **Write results to session file** for sharing
5. **Return brief summary** to orchestrator

## Best Practices

**Do:**
- Run claudemem ONCE per investigation type
- Write all output to session directory
- Use parallel execution for independent analyses (see `orchestration:multi-model-validation`)
- Consolidate with ultrathink for cross-perspective insights
- Handle empty results gracefully

**Don't:**
- Run same claudemem command multiple times
- Let each agent run its own claudemem (wasteful)
- Skip the consolidation step
- Forget to clean up session directory (automatic TTL cleanup via `session-start.sh`)

## Session Lifecycle Management

**Automatic TTL Cleanup:**

The `session-start.sh` hook automatically cleans up expired session directories:
- Default TTL: 24 hours
- Runs at session start
- Cleans `/tmp/analysis-*`, `/tmp/review-*` directories older than TTL
- See `plugins/code-analysis/hooks/session-start.sh` for implementation

**Manual Cleanup:**

```bash
# Clean up specific session
rm -rf "$SESSION_DIR"

# Clean all old sessions (24+ hours)
find /tmp -maxdepth 1 -name "analysis-*" -o -name "review-*" -mtime +1 -exec rm -rf {} \;
```

## Error Handling Templates

For robust orchestration, handle common claudemem errors. See `claudemem-search` skill for complete error handling templates:

### Empty Results
```bash
RESULT=$(claudemem --nologo map "query" --raw 2>/dev/null)
if [ -z "$RESULT" ] || echo "$RESULT" | grep -q "No results found"; then
  echo "No results - try broader keywords or check index status"
fi
```

### Version Compatibility
```bash
# Check if command is available (v0.4.0+ commands)
if claudemem --nologo dead-code --raw 2>&1 | grep -q "unknown command"; then
  echo "dead-code requires claudemem v0.4.0+"
  echo "Fallback: Use map command instead"
fi
```

### Index Status
```bash
# Verify index before running commands
if ! claudemem status 2>&1 | grep -qE "[0-9]+ (chunks|symbols)"; then
  echo "Index not found - run: claudemem index"
  exit 1
fi
```

**Reference:** For complete error handling patterns, see templates in `code-analysis:claudemem-search` skill (Templates 1-5)

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis v2.6.0
**Last Updated:** December 2025
