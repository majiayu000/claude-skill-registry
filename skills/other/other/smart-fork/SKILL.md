---
# VERSION: 2.88.0
name: smart-fork
description: Smart Forking - Find and fork from relevant historical sessions using parallel memory search across claude-mem, memvid, handoffs, and ledgers
author: Multi-Agent Ralph
version: 2.47.2
model: sonnet
context: fork
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - mcp__plugin_claude-mem_*
hooks:
  PostToolUse:
    - event: "Task"
      script: "~/.claude/hooks/smart-memory-search.sh"
---

# /smart-fork - Smart Memory-Driven Session Forking

Based on @PerceptualPeak's Smart Forking concept:

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars
> "Why not utilize the knowledge gained from your hundreds/thousands of other Claude code sessions? Don't let that valuable context go to waste!!"

## Quick Start

```bash
# Find relevant sessions to fork from
/smart-fork "Implement OAuth authentication"

# Show fork suggestions for current task
/smart-fork --suggest

# Generate fork command for specific session
/smart-fork --fork <session_id>

# Show memory statistics
/smart-fork --stats
```

## How It Works

### 1. PARALLEL Memory Search

When you invoke `/smart-fork`, we search across ALL memory sources **in parallel**:

```
┌──────────────────────────────────────────────────────────────┐
│                    PARALLEL MEMORY SEARCH                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ │
│   │ claude-mem │ │  memvid    │ │  handoffs  │ │  ledgers │ │
│   │    MCP     │ │  search    │ │   scan     │ │   scan   │ │
│   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └────┬─────┘ │
│         │ PARALLEL     │ PARALLEL     │ PARALLEL    │        │
│         └──────────────┴──────────────┴─────────────┘        │
│                            ↓                                  │
│                    AGGREGATOR (top 5)                        │
│                            ↓                                  │
│              .claude/memory-context.json                     │
└──────────────────────────────────────────────────────────────┘
```

### 2. Relevance Scoring

Results are scored by:
- **Keyword Match**: How many search terms appear in the session
- **Recency**: More recent sessions score higher
- **Outcome**: Sessions with successful completion score higher
- **Similarity**: Semantic similarity to current task

### 3. Fork Suggestions

Top 5 most relevant sessions are suggested with:
- Session ID
- Timestamp
- Brief summary
- Fork command

## Commands

### `/smart-fork "task description"`

Search for relevant sessions based on task description.

**Example:**
```
/smart-fork "Implement JWT authentication with refresh tokens"
```

**Output:**
```
SMART FORK RESULTS v2.47
========================

Search: "Implement JWT authentication with refresh tokens"

TOP 5 RELEVANT SESSIONS:
------------------------
1. [HIGH] Session: abc123-def456 (2026-01-15)
   Summary: Implemented OAuth2 with JWT, similar auth patterns
   Fork: claude --continue abc123-def456

2. [HIGH] Session: xyz789-uvw012 (2026-01-10)
   Summary: Token refresh implementation in Node.js
   Fork: claude --continue xyz789-uvw012

3. [MEDIUM] Session: pqr345-stu678 (2026-01-05)
   Summary: Authentication middleware setup
   Fork: claude --continue pqr345-stu678

Memory sources searched: claude-mem (5), memvid (3), handoffs (8), ledgers (2)
Total results: 18
```

### `/smart-fork --suggest`

Show fork suggestions based on current project context.

### `/smart-fork --fork <session_id>`

Generate fork command for a specific session.

### `/smart-fork --stats`

Show memory statistics across all sources.

## Integration with Orchestrator

The Smart Fork system integrates with the orchestrator at **Step 0b**:

```
Step 0: EVALUATE
├── 0a: 3-Dimension Classification (v2.46)
└── 0b: SMART MEMORY SEARCH (v2.47) ◄── NEW
        │
        ├── Search claude-mem for relevant observations
        ├── Search memvid for semantic matches
        ├── Search handoffs for recent context
        └── Search ledgers for session continuity
        │
        ▼
    .claude/memory-context.json
    │
    ├── past_successes: Implementation patterns that worked
    ├── past_errors: Mistakes to avoid
    ├── recommended_patterns: Best practices
    └── fork_suggestions: Top 5 sessions to fork from
```

## Memory Sources

| Source | Content | Speed | Retention |
|--------|---------|-------|-----------|
| **claude-mem MCP** | Semantic observations | Fast | Permanent |
| **memvid** | Vector-encoded context | Sub-5ms | Permanent |
| **handoffs** | Session context snapshots | Fast | 30 days |
| **ledgers** | Continuity data | Fast | Permanent |

## Benefits

### 1. Avoid Repeating Mistakes
Past errors are surfaced to prevent the same issues.

### 2. Reuse Successful Patterns
Implementation patterns that worked before are recommended.

### 3. Faster Context Loading
Fork from a relevant session instead of re-explaining everything.

### 4. Cross-Project Learning
Patterns from other projects inform current implementation.

## Configuration

Smart Fork is configured via `~/.ralph/config/smart-fork.json`:

```json
{
    "version": "2.47",
    "cache_duration_seconds": 1800,
    "max_results_per_source": 10,
    "top_k_suggestions": 5,
    "search_recency_days": 30,
    "parallel_timeout_seconds": 30
}
```

## CLI Commands

```bash
# Via ralph CLI
ralph fork-suggest "task description"
ralph memory-search "query"
ralph memory-stats

# Via skill
/smart-fork "task description"
```

## Technical Notes

- **PARALLEL by Default**: All memory searches run concurrently
- **30-minute Cache**: Results are cached to avoid repeated searches
- **Graceful Degradation**: Missing memory sources are skipped
- **JSON Output**: Results stored in `.claude/memory-context.json`

## Files

| Path | Purpose |
|------|---------|
| `~/.claude/hooks/smart-memory-search.sh` | PreToolUse hook for parallel search |
| `.claude/memory-context.json` | Aggregated memory results |
| `~/.ralph/config/smart-fork.json` | Configuration |
| `~/.ralph/logs/smart-memory-search-*.log` | Search logs |

## Troubleshooting (v2.52.0)

### "No memory sources available"

**Cause**: None of the 4 memory sources (claude-mem, memvid, handoffs, ledgers) are initialized.

**Fix**:
```bash
# Initialize handoffs
ralph handoff create

# Initialize ledgers
ralph ledger save

# Initialize memvid (optional)
ralph memvid init

# Verify claude-mem MCP is running
claude --server-list | grep claude-mem
```

### "Search timeout after 30s"

**Cause**: Memory sources are too large or slow to search within timeout.

**Fix**:
1. Increase timeout in config: `~/.ralph/config/smart-fork.json`
   ```json
   {"parallel_timeout_seconds": 60}
   ```
2. Reduce search scope: `{"search_recency_days": 14}`
3. Limit results: `{"max_results_per_source": 5}`

### "PreToolUse:Task hook error"

**Cause**: Hook execution failed (but usually non-critical).

**Fix**:
1. Check logs: `tail -f ~/.ralph/logs/smart-memory-search-*.log`
2. Verify hook is executable: `chmod +x ~/.claude/hooks/smart-memory-search.sh`
3. Test manually: `echo '{"tool_name":"Read"}' | bash ~/.claude/hooks/smart-memory-search.sh`

### "Empty fork_suggestions"

**Cause**: No matching sessions found for your keywords.

**Fix**:
1. Try broader keywords
2. Ensure handoffs exist: `ls ~/.ralph/handoffs/`
3. Verify recent activity: `ls -la ~/.ralph/ledgers/`

### "Cache not invalidating"

**Cause**: Cache file still valid within 30-minute window.

**Fix**:
```bash
# Force fresh search by removing cache
rm .claude/memory-context.json
```

## Performance Tuning (v2.52.0)

### Configuration Options

Edit `~/.ralph/config/smart-fork.json`:

| Setting | Default | Impact |
|---------|---------|--------|
| `cache_duration_seconds` | 1800 | Lower = fresher results, more searches |
| `parallel_timeout_seconds` | 30 | Higher = more complete results, slower startup |
| `max_results_per_source` | 10 | Higher = more context, slower aggregation |
| `search_recency_days` | 30 | Higher = deeper history, slower search |
| `top_k_suggestions` | 5 | Higher = more options, more tokens |

### Optimal Configurations

**Fast Startup (minimal latency)**:
```json
{
    "cache_duration_seconds": 3600,
    "parallel_timeout_seconds": 10,
    "max_results_per_source": 3,
    "search_recency_days": 7
}
```

**Comprehensive Search (maximum context)**:
```json
{
    "cache_duration_seconds": 900,
    "parallel_timeout_seconds": 60,
    "max_results_per_source": 20,
    "search_recency_days": 90
}
```

**Balanced (recommended)**:
```json
{
    "cache_duration_seconds": 1800,
    "parallel_timeout_seconds": 30,
    "max_results_per_source": 10,
    "search_recency_days": 30
}
```

### Performance Benchmarks

| Configuration | Search Time | Results Quality |
|---------------|-------------|-----------------|
| Fast | ~2s | Good (recent only) |
| Balanced | ~5s | Very Good |
| Comprehensive | ~15s | Excellent |

### Monitoring Performance

```bash
# Check last search duration
tail -1 ~/.ralph/logs/smart-memory-search-*.log | grep "completed in"

# Monitor memory source health
ralph memory-stats

# Profile individual sources
time claude-mem search "test query" --limit 5
```

## Security Notes (v2.52.0)

The smart-memory-search hook includes these security hardening measures:

| Vulnerability | Fix | Details |
|--------------|-----|---------|
| **SECURITY-001** | Command Injection | Keywords escaped before grep -E usage |
| **SECURITY-002** | Path Traversal | Symlinks validated via realpath before reading |
| **SECURITY-003** | Race Condition | Atomic temp file creation with restrictive permissions |

All security tests pass: `pytest tests/test_v2_47_security.py -v`
