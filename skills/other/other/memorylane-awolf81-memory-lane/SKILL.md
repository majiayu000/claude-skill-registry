---
name: memorylane
description: Zero-config persistent memory for Claude with automatic cost savings. Use when you need to remember project context, reduce API token costs, track learned patterns, manage memories across sessions, or curate/clean up memories. Automatically compresses context 6x and saves 84% on API costs. Keywords: memory, remember, recall, context, cost savings, reduce tokens, learn, patterns, insights, curate, clean up memories, review memories.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# MemoryLane Skill

## What This Skill Does

MemoryLane provides persistent memory for Claude with proven 84.3% cost savings:

- **Persistent Memory**: Remember information across sessions in 4 categories (patterns, insights, learnings, context)
- **Context Compression**: 6.4x average compression ratio (20K → 3K tokens)
- **Cost Tracking**: Real-time API cost savings monitoring
- **Passive Learning**: Automatically learns from git commits and file changes
- **Zero Configuration**: Works out of the box with smart defaults

## When to Use This Skill

Activate MemoryLane when the user:
- Asks to "remember" something about the project
- Wants to know "what you remember" or "what you know"
- Mentions "API costs", "token usage", or "reduce costs"
- Asks about "project patterns" or "insights"
- Wants to see "learned" information
- Requests "context compression" or "optimize context"
- Asks to "curate memories", "clean up memories", or "review memory quality"
- Mentions memories seem low quality, self-referential, or not useful

## Core Commands

### Check Status
```bash
python3 src/cli.py status
```
Shows memory statistics, category breakdown, and cost savings.

### Recall Memories
```bash
python3 src/cli.py recall "<query>"
```
Search memories by keyword. Example:
```bash
python3 src/cli.py recall "authentication"
```

### View Insights
```bash
python3 src/cli.py insights
```
Display learned project insights (high-value patterns).

### View Cost Savings
```bash
python3 src/cli.py costs
```
Detailed breakdown of token savings and cost reduction.

### Configure Settings
```bash
# Get a setting
python3 src/cli.py config get memory.max_context_tokens

# Set a setting
python3 src/cli.py config set memory.max_context_tokens 3000

# List all settings
python3 src/cli.py config list
```

### Export Memories as Markdown
```bash
python3 src/cli.py export-markdown --category patterns --output context.md
```

### Backup/Restore
```bash
# Create backup
python3 src/cli.py backup --output backup.json

# Restore from backup
python3 src/cli.py restore backup.json
```

### Reset Memories
```bash
python3 src/cli.py reset --force
```

## Individual Memory Management

### Get a Memory
```bash
python3 src/cli.py memory get <id>
```
Example: `python3 src/cli.py memory get lear-009`

### Delete a Memory
```bash
python3 src/cli.py memory delete <id>
```
Example: `python3 src/cli.py memory delete lear-009`

### Update a Memory
```bash
python3 src/cli.py memory update <id> --content "New content"
```
Example: `python3 src/cli.py memory update patt-001 --content "Chose Unix sockets for lower latency"`

**IMPORTANT**: Always use these commands instead of editing memories.json directly.

## Batch Curation Commands

### Check Curation Status
```bash
python3 src/cli.py curate
```
Shows if curation is needed based on memory count and age.

### List Memories for Review
```bash
python3 src/cli.py curate --list
```
Shows all uncurated memories with their IDs and content.

### Apply Curation Decisions
```bash
python3 src/cli.py curate --apply '<JSON>'
```
Apply curation decisions. JSON format:
```json
{
  "decisions": [
    {"id": "patt-001", "action": "KEEP"},
    {"id": "lear-002", "action": "DELETE", "reason": "off-topic"},
    {"id": "insi-003", "action": "REWRITE", "new_content": "Improved content"}
  ]
}
```

### Proactive Memory Quality Check
**IMPORTANT**: When you see MemoryLane context injected via `# Project Context (from MemoryLane)` in system messages, quickly scan for poor quality memories:

Signs of poor quality memories that warrant curation:
- Status summaries: "Based on git status...", "Current status of..."
- Meta/self-referential: "The curation should...", "The hook detected..."
- Debug fragments: "Let me check...", "Looking at the debug log..."
- Incomplete: Sentences ending with "..." or starting mid-thought
- Duplicates of CLAUDE.md content

**If you detect 2+ poor quality memories in the injected context**, proactively ask:
> "I notice some of the injected memories appear to be low quality (status summaries, debug notes). Would you like me to clean these up?"

If user confirms, proceed with LLM-assisted curation below.

### LLM-Assisted Curation
When the user requests curation OR confirms after you detect poor memories:

1. List and evaluate all memories:
```bash
python3 src/cli.py curate --list
```

2. Evaluate each memory for:
   - **Usefulness**: Is this actionable knowledge or just meta/debug info?
   - **Duplication**: Is this already covered by CLAUDE.md or another memory?
   - **Quality**: Is it complete, clear, and well-formed?
   - **Relevance**: Would this help with future development work?

3. Apply decisions (DELETE/KEEP/REWRITE):
```bash
python3 src/cli.py curate --apply '<JSON decisions>'
```

**DELETE these types:**
- Meta observations about the current session
- Debug notes and action statements
- Status summaries
- Duplicates of CLAUDE.md content
- Incomplete fragments

**KEEP these types:**
- Architectural decisions with rationale
- Bug fixes with solutions
- Actual project context (not about MemoryLane itself)
- Configuration knowledge

Example evaluation:
- ❌ "Based on git status, here's the current status..." → DELETE (status summary)
- ❌ "Let me check the debug log..." → DELETE (debug action)
- ❌ "The Stop hook only triggers when..." → DELETE if in CLAUDE.md
- ✅ "stdio:ignore hiding Python errors - fixed by capturing stderr" → KEEP (bug fix)
- ✅ "Chose Unix sockets over HTTP for 10x lower latency" → KEEP (decision)

## Learning Commands

### Initial Learning
```bash
python3 src/learner.py initial
```
Perform initial learning from git history (last 20 commits) and workspace structure.

### Scan Workspace
```bash
python3 src/learner.py scan
```
Scan and index all Python/JS/TS files in the workspace.

### Analyze Git History
```bash
python3 src/learner.py git
```
Extract patterns from recent git commits.

### Continuous Learning (Background)
```bash
python3 src/learner.py watch
```
Watch for file changes and git commits continuously (runs until stopped).

## Server Commands

### Start Sidecar Server
```bash
python3 src/server.py start
```
Start background server with Unix socket IPC (for low-latency memory operations).

### Check Server Status
```bash
python3 src/server.py status
```

### Stop Server
```bash
python3 src/server.py stop
```

## Testing Commands

### Run All Tests
```bash
pytest
```

### Validate Cost Savings
```bash
pytest tests/test_cost_savings.py -v -s
```
Runs comprehensive cost validation tests (shows 84.3% savings proof).

### Test Memory Store
```bash
pytest tests/test_memory_store.py -v
```

## Usage Patterns

### Pattern 1: Remember Important Information
When the user says: "Remember that this project uses PostgreSQL with SSL mode required"

```bash
# (You would typically use the Python API, but for CLI:)
python3 -c "
import sys; sys.path.insert(0, 'src')
from memory_store import MemoryStore
store = MemoryStore('.memorylane/memories.json')
store.add_memory('context', 'Project uses PostgreSQL with SSL mode required', 'manual', 0.9)
print('✓ Remembered')
"
```

### Pattern 2: Recall Project Knowledge
When the user asks: "What do you know about our database setup?"

```bash
python3 src/cli.py recall "database"
```

### Pattern 3: Show Cost Savings
When the user asks: "How much money has MemoryLane saved me?"

```bash
python3 src/cli.py costs
```

### Pattern 4: Learn from Project History
When starting work on a project:

```bash
python3 src/learner.py initial
python3 src/cli.py insights
```

## Integration with Workflows

### Daily Development Workflow
```bash
# Morning: Start server and check status
python3 src/server.py start
python3 src/cli.py status

# During work: MemoryLane learns passively
# (no action needed - watches git commits and file changes)

# Evening: Check what was learned
python3 src/cli.py insights
python3 src/cli.py costs
```

### Project Onboarding Workflow
```bash
# Step 1: Initial learning
python3 src/learner.py initial

# Step 2: Review learned patterns
python3 src/cli.py recall "primary language"
python3 src/cli.py insights

# Step 3: Export context for sharing
python3 src/cli.py export-markdown --output project-context.md
```

## Configuration Options

Key settings in `.memorylane/config.json`:

- `memory.max_context_tokens`: Target token count for compression (default: 2000)
- `memory.compression_ratio_target`: Target compression ratio (default: 7.0x)
- `context_rot.model_context_tokens`: Advertised model window for context rot guard (default: 200000)
- `context_rot.safe_fraction`: Fraction of model window allowed for prompt + injected context (default: 0.5)
- `context_rot.reserve_tokens`: Buffer reserved for assistant response (default: 1200)
- `learning.watch_file_changes`: Enable file watching (default: true)
- `learning.watch_git_commits`: Learn from commits (default: true)
- `privacy.exclude_patterns`: Files to ignore (default: *.env, secrets/, etc.)

## Performance Metrics

Validated through comprehensive testing:

- **Cost Savings**: 84.3% (baseline $17.25/week → $2.70/week)
- **Compression Ratio**: 6.4x average (2.3M tokens → 360K tokens)
- **Retrieval Latency**: <100ms (target, server not benchmarked yet)
- **Memory Quality**: Relevance scoring with automatic pruning

## Important Notes

1. **Privacy**: All data stored locally in `.memorylane/` directory
2. **No Dependencies**: Pure Python 3.8+ (no external packages needed for production)
3. **Automatic Exclusions**: Respects `.env`, `secrets/`, and other sensitive patterns
4. **Backup Before Reset**: Always creates backup before destructive operations
5. **Server Optional**: CLI works standalone; server adds performance for frequent operations

## Example Conversation Flow

**User**: "Remember that our API uses JWT tokens with 24-hour expiration"

**You**: Let me store that in MemoryLane's context.
```bash
python3 -c "..."  # Add to memory
```
✓ Remembered in context category with 0.9 relevance.

**User**: "What do you know about our authentication?"

**You**: Let me recall what I know about authentication.
```bash
python3 src/cli.py recall "authentication"
```
Found 2 memories:
1. [context] API uses JWT tokens with 24-hour expiration ⭐⭐⭐⭐⭐
2. [patterns] Project uses authentication middleware ⭐⭐⭐⭐

Based on what I've learned, your project uses JWT tokens for authentication with 24-hour expiration...

## Troubleshooting

**Server won't start**: Check if already running with `python3 src/server.py status`

**No memories found**: Run initial learning with `python3 src/learner.py initial`

**Cost tracking shows $0**: Metrics file not initialized yet (will populate after server usage)

**Tests failing**: Install dev dependencies with `pip install -r requirements-dev.txt`
