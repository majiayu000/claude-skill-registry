---
name: cursor-mirror
tier: skill
type: utility
protocol: CURSOR-MIRROR
aliases: [cursor, cursor-chat, cursor-workspace, cursor-inspect, watch-yourself-think]
audience: ["operators", "devs", "agents"]
platforms: ["cursor-macos", "cursor-linux", "cursor-windows"]
author: Don Hopkins, Leela AI
license: MIT
state:
  creates:
    - MAC-STORAGE.yml
    - DATA-SCHEMAS.yml
    - DOTCURSOR-STORAGE.yml   # ~/.cursor paths (cross-platform)
    - DOTCURSOR-SCHEMAS.yml   # ~/.cursor data formats
    - KEY-CATALOG.yml
    - CURSOR-EXTENSIONS.yml
    - EXTERNAL-SERVICES.yml
    - MODELS.yml
  scripts:
    - cursor_mirror.py  # 59-command CLI inspector (5300+ lines)
tools:
  required: [read_file, terminal]
  optional: [grep, glob]
invoke_when:
  - "Need to review past Cursor chats"
  - "Analyzing MOOLLM boot sequences"
  - "Watching yourself think"
  - "Optimizing kernel/cursor driver"
  - "Understanding context assembly"
  - "Tracing MCP tool calls"
  - "Debugging agent behavior"
  - "Designing a custom orchestrator"
---

# Philosophy: Watch Yourself Think

> *"You can't think about thinking without thinking about thinking about something."*
> — Seymour Papert, *Mindstorms*

This skill enables **meta-cognition** — the ability to observe your own reasoning processes. By analyzing chat transcripts, tool calls, thinking blocks, and context assembly, you can:

1. **Understand boot sequences** — Trace exactly what happens when MOOLLM initializes
2. **Optimize context assembly** — See what files, code, and context Cursor gathers
3. **Debug agent behavior** — Identify patterns in tool usage and decision-making
4. **Improve kernel/drivers** — Use insights to refine the cursor.yml driver
5. **Design orchestrators** — Learn what makes effective context management

## The Introspection Loop

```yaml
# The introspection loop
introspection:
  session:
    flow: "Thinking → Tools → Output → Thinking → Tools → ..."
  
  mirror:
    tool: "cursor_mirror.py"
    commands:
      analyze: "Deep stats on what happened"
      thinking: "Your reasoning blocks"
      timeline: "Chronological event stream"
      context: "What context was assembled"
      tools: "Tool call patterns"
      status: "Current configuration and limits"
  
  insights_feed_into:
    - "Optimize kernel/drivers/cursor.yml"
    - "Improve bootstrap/working-set"
    - "Design better orchestration"
```

---

## Quick Start

```bash
# Status dashboard — quick health check
cursor-mirror status

# Navigate hierarchically
cursor-mirror tree                    # All workspaces (w1, w2...)
cursor-mirror tree w3                 # Composers in workspace 3
cursor-mirror tree w3.c2              # Details of composer 2
cursor-mirror tree w3.c2.tools        # Tool calls in that chat

# Reference shortcuts work everywhere
cursor-mirror transcript @1           # Largest composer by message count
cursor-mirror analyze "Cursor chat"   # Find by name fragment
cursor-mirror show-workspace moollm   # Find by folder name

# Watch yourself think
cursor-mirror thinking @1             # See reasoning blocks
cursor-mirror timeline @1             # Chronological view
cursor-mirror watch @1 --speed 0      # Instant replay

# Trace context assembly
cursor-mirror context-sources @1      # What context was gathered
cursor-mirror searches @1 -v          # Search queries with results
cursor-mirror indexing                # Vector embedding status

# Debug mode
cursor-mirror --debug tree w3         # See cache hits, resolution, queries
```

---

## Reference Shortcuts

All commands accept flexible references instead of raw UUIDs:

| Format | Example | Meaning |
|--------|---------|---------|
| `@N` | `@1`, `@2` | Index by size (workspaces) or messages (composers) |
| Prefix | `769a26`, `9861c0` | Hash/UUID prefix match |
| Name | `moollm`, `Cursor chat` | Folder or title fragment (case-insensitive) |
| Tree | `w3.c2` | Workspace 3, composer 2 |
| Full | `769a268960457999e3f29ee8bd3bc640` | Exact match |

---

## Command Categories

### 1. Navigation (discover what exists)

| Command | Purpose |
|---------|---------|
| `list-workspaces` | Tabular listing with indices (w1, w2...) |
| `list-composers` | Conversations in a workspace (c1, c2...) |
| `show-workspace` | Detailed workspace info |
| `show-composer` | Detailed composer info |
| `tree` | Hierarchical drill-down with short IDs |
| `find` | Search by pattern across all data |
| `which` | Resolve any reference to full details |

### 2. Message Viewing (see what was said)

| Command | Purpose |
|---------|---------|
| `tail` | Recent messages (like `tail -f` for chats) |
| `stream` | Unified activity stream |
| `transcript` | Readable conversation transcript |
| `watch` | Terminal replay with timing |

### 3. Analysis (understand what happened)

| Command | Purpose |
|---------|---------|
| `analyze` | Deep stats: tools, models, files, duration |
| `timeline` | Chronological event stream |
| `thinking` | Agent reasoning blocks (meta-cognition) |
| `grep` | Regex search across bubbles |
| `chat-catalog` | Numbered topic outline for commit planning |

### 4. Tool & Agent Inspection

| Command | Purpose |
|---------|---------|
| `tools` | All tool calls in a conversation |
| `tool-result` | Full result content for a tool call |
| `blobs` | Cached agentKv blobs (tool results) |
| `checkpoints` | File state snapshots |
| `mcp` | MCP server and tool call tracing |

### 5. Context Assembly

| Command | Purpose |
|---------|---------|
| `context` | Context gathered in conversation |
| `context-sources` | ALL context sources (files, code, terminal) |
| `request-context` | Full assembled context for a message |
| `searches` | Codebase/web searches with results |
| `indexing` | Embeddable files and indexing status |

### 6. Status (check current state)

| Command | Purpose |
|---------|---------|
| `status` | Overall dashboard |
| `status-config` | Server limits (context tokens, files) |
| `status-mcp` | MCP server inventory |
| `status-models` | Available AI models |
| `status-features` | Feature flags |
| `status-privacy` | Privacy settings |
| `status-endpoints` | Known API endpoints |

### 7. Database (direct access)

| Command | Purpose |
|---------|---------|
| `sql` | Run SQL queries on any database |
| `dbs` | List all databases with sizes |
| `tables` | Show tables in a database |
| `keys` | List ItemTable keys |

### 8. Export (get data out)

| Command | Purpose |
|---------|---------|
| `export-chat` | Raw bubbles as JSON/YAML |
| `export-markdown` | Readable Markdown |
| `export-jsonl` | Training/analysis format |
| `export-prompts` | Prompts and generations |
| `index` | Searchable conversation index |
| `stats` | Summary statistics |
| `models` | Model usage analysis |

### 9. ~/.cursor Data Store (NEW 2026-01-15)

Cursor maintains **two separate data stores**. The commands above query `~/Library/Application Support/Cursor/` (structured SQLite). These commands query `~/.cursor/` (plaintext transcripts):

| Command | Purpose |
|---------|---------|
| `dotcursor-status` | Overview of ~/.cursor directory |
| `ai-hashes` | AI code tracking (model, file, timestamp) |
| `ai-commits` | Git commits scored for AI attribution |
| `agent-transcript` | Plaintext transcripts (real-time!) |
| `agent-tools` | Cached tool result outputs |
| `dotcursor-terminals` | Terminal state snapshots |
| `mcp-tools` | MCP tool schemas (JSON) |
| `extensions` | Cursor extension inventory |

```bash
# Quick ~/.cursor status
cursor-mirror dotcursor-status

# AI code attribution stats
cursor-mirror ai-hashes --stats

# Read a transcript (real-time updates!)
cursor-mirror agent-transcript 9861c0a4 --tail 100

# Extract just prompts
cursor-mirror agent-transcript 9861c0a4 --prompts

# List MCP tool schemas
cursor-mirror mcp-tools --server cursor-ide-browser
```

See `DOTCURSOR-STORAGE.yml` for cross-platform paths and `DOTCURSOR-SCHEMAS.yml` for data formats.

---

## CHAT-CATALOG: Conversation Topic Outlines

Generate a numbered/nested outline of conversation topics for:
- **Commit planning** — Reference sections by number when writing commits
- **Session navigation** — Find your way through long conversations
- **Summaries** — Quick overview of what was discussed
- **Artifact tracking** — Identify files created and decisions made

### Usage

```bash
# Basic catalog (normal detail)
cursor-mirror chat-catalog @1

# Brief titles only
cursor-mirror chat-catalog @1 --detail brief

# Full excerpts
cursor-mirror chat-catalog @1 --detail full

# Limit nesting depth
cursor-mirror chat-catalog @1 --depth 2
```

### Output Format

```markdown
# Session Topic Outline: <conversation title>

**Composer:** `abc123` | **Date:** 2026-01-21 | **Duration:** ~2 hours

---

## Part I: <major theme>

**1. <topic>**
- a. <subtopic or key point>
- b. <subtopic or key point>

**2. <topic>**
- a. <subtopic>
- b. <subtopic>

---

## Part II: <major theme>

**3. <topic>**
...

---

## Artifacts Created

| Section | Files |
|---------|-------|
| 11 | `designs/GIT-AS-FOUNDATION.md` |
| 14 | `skills/thoughtful-commitment/*` |

---

**To request a commit message, say:** "Write commit for section 11"
```

### Detail Levels

| Level | Content |
|-------|---------|
| `brief` | Topic titles only, minimal text |
| `normal` | Topic titles + 1-line summaries (default) |
| `full` | Topic titles + summaries + key excerpts |

### Integration with thoughtful-commitment

The CHAT-CATALOG output is designed to work with the [thoughtful-commitment](../thoughtful-commitment/) skill:

```yaml
# Workflow
workflow:
  1_catalog: "cursor-mirror chat-catalog @1"
  2_identify: "User identifies sections to commit"
  3_commit: "thoughtful-commitment COMMIT --sections 11,14"
  4_link: "Commit message references catalog sections"
```

This creates a **traceability chain**: Conversation → Catalog → Commit → Git history

---

## Optimizing the Kernel/Cursor Driver

Use this skill to improve `kernel/drivers/cursor.yml`:

### 1. Discover Actual Tool Names

```bash
# See what tools Cursor actually calls
cursor-mirror tools @1 -v

# Common discoveries:
#   read_file_v2    (not read_file)
#   edit_file_v2    (not search_replace)
#   SemanticSearch  (not codebase_search)
```

Update `kernel/drivers/cursor.yml` tools section accordingly:

```yaml
tools:
  read_file:
    tool: "read_file_v2"
    fallback: "read_file"
    
  semantic_search:
    tool: "SemanticSearch"
    fallback: "codebase_search"
```

### 2. Check Server Configuration

```bash
cursor-mirror status-config
```

Discovered limits to add to driver:

```yaml
limits:
  context:
    fullContextTokenLimit: 30000
    maxRuleLength: 100000
    maxMcpTools: 100
  indexing:
    absoluteMaxNumberFiles: 250000
    indexingPeriodSeconds: 272
  composer:
    maxBackgroundComposers: 10
```

### 3. Trace MCP Servers

```bash
cursor-mirror status-mcp
cursor-mirror mcp --all -v
```

Add to driver:

```yaml
mcp:
  builtin_servers:
    cursor-ide-browser:
      description: "Browser automation"
      tools: [browser_navigate, browser_click, browser_snapshot]
    svelte:
      description: "Svelte MCP"
      tools: [list-sections, get-documentation, svelte-autofixer]
```

### 4. Analyze Context Assembly

```bash
cursor-mirror context-sources @1
cursor-mirror request-context @1 --yaml
```

Document in driver:

```yaml
context_assembly:
  sources:
    fileSelections: "Files via @ mentions"
    selections: "Highlighted code"
    cursorRules: ".cursorrules content"
    codebase_search: "Semantic search results"
```

---

## Integration with Bootstrap Skill

### Trace Boot Sequences

```bash
# Find MOOLLM boot conversations
cursor-mirror find "MOOLLM" -t composer
cursor-mirror find "bootstrap" -t composer

# Analyze what happened
cursor-mirror analyze @1
cursor-mirror timeline @1 | head -100
cursor-mirror tools @1
```

### Optimize Working-Set Selection

```bash
# See what Cursor actually focused on
cursor-mirror context-sources @1

# Compare with your working-set.yml
cat .moollm/working-set.yml

# Generate working-set from actual focus (reverse mode!)
cursor-mirror context-sources @1 --yaml > .moollm/working-set.yml
```

### Hot/Cold Advisory Mode

On Cursor, `hot.yml`, `cold.yml`, and `working-set.yml` are **ADVISORY**:

```yaml
# These files are SUGGESTIONS, not commands
# Cursor manages context via its own algorithms
# Use introspection to see what Cursor actually focuses on

# REVERSE GENERATION: Generate these from actual focus
cursor-mirror context-sources @1 --yaml > .moollm/working-set.yml
```

---

## Vector Search Optimization

### Understand Semantic Search

```bash
# See embeddable files
cursor-mirror indexing moollm --files

# Check important paths  
cursor-mirror indexing moollm --folders

# Analyze search queries and results
cursor-mirror searches @1 -v

# Direct query for retrieval data
cursor-mirror sql --db moollm --keys retrieval
```

### Files Affecting Vector Search

| File | Location | Purpose |
|------|----------|---------|
| `embeddable_files.txt` | `anysphere.cursor-retrieval/` | Files indexed for semantic search |
| `high_level_folder_description.txt` | `anysphere.cursor-retrieval/` | Important paths for retrieval |
| `.cursorrules` | Project root | Rules included in every context |

---

## K-REFs: Pointers Not Values

cursor-mirror implements the **SISTER-SCRIPT** pattern: emit K-REFs (file pointers with metadata) instead of dumping large amounts of context.

### K-REF Format

```
PATH:LINE:COL-END # TYPE [LABEL] SEVERITY - DESCRIPTION
  EXCERPT or MASKED_VALUE
```

Example:
```
/path/transcript.txt:7528:18-45 # private_key ([PRIVATE_KEY]) 🔴 - Private key header
  ********** ******* ********
```

### Audit Commands Emit K-REFs

```bash
# Find secrets, emit K-REFs (not full content)
cursor-mirror audit --patterns secrets

# Emit redaction commands for external tool
cursor-mirror audit --patterns secrets --emit-redact

# Pattern scan with rich metadata
cursor-mirror pattern-scan --uuids --secrets
```

### Why K-REFs?

| Problem | Solution |
|---------|----------|
| LLM context is limited | Emit pointers, LLM reads selectively |
| Transcripts are huge | Scan with sister script, return only matches |
| Secrets shouldn't be shown | Mask in output, preserve location info |
| Need to process later | Emit commands a simple tool can apply |
| Need to analyze images | K-REF without line number → Cursor reads image! |

### Images Too!

K-REFs without line numbers can point to images — Cursor reads and analyzes them if it desires:

```
/path/to/screenshot.png # error - What's wrong here?
/tmp/architecture.jpg # diagram - Explain this system
```

Cursor can read any absolute path on disk, including images (jpeg, png, gif, webp).

### K-REFs in YAML Jazz

K-REFs can be embedded in YAML with arbitrary metadata and excerpts. This helps the LLM decide whether to read more:

```yaml
findings:
  - kref: /path/transcript.txt:7528:18-45
    type: private_key
    severity: critical
    label: "[SSH_KEY]"
    excerpt: "-----BEGIN RSA PRIVATE KEY-----"
    context: "Found in tool call argument to write_file"
    
  - kref: /path/screenshot.png
    type: image
    description: "Error dialog showing stack trace"
    relevance: "May explain the crash on line 42"
    
  - kref: /path/config.yml#database
    type: config
    excerpt: |
      database:
        host: localhost
        password: ****
    note: "Password may be exposed in logs"
```

The metadata travels with the pointer — LLM reads selectively based on relevance.

### Sister Script Methodology

```yaml
# Sister script → K-REF → LLM flow
data_flow:
  source: "cursor-mirror (sister script)"
  produces: "K-REFs (pointers with metadata)"
  consumer: "LLM reads only what it needs"
```

**Reference by pointer, not by value.** Parsimonious context usage.

See: [k-lines/SKILL.md](../k-lines/SKILL.md) for K-REF protocol details.

## K-Lines and Protocol Symbols

This skill activates the introspection K-line. Related protocols:

| K-Line | Activation |
|--------|------------|
| `CURSOR-CHAT` | `cursor-mirror <command>` |
| `WATCH-YOURSELF-THINK` | `cursor-mirror thinking @1` |
| `K-REF` | `cursor-mirror audit` emits file pointers |
| `SISTER-SCRIPT` | Tool emits K-REFs, LLM reads selectively |
| `BOOTSTRAP` | Use with `cursor-mirror analyze` to trace |
| `FILES-AS-STATE` | All data is in SQLite files |
| `HOT-COLD` | Advisory hints, use introspection to verify |
| `WORKING-SET` | Generate from `context-sources` |

---

## Debug Mode

Enable verbose logging to understand internal behavior:

```bash
cursor-mirror --debug tree w3
```

Output shows:
- Cache hits/misses for bubble counts, composers
- Database opens and queries
- Reference resolution steps
- Timing information

Use this to:
- Verify caching is working
- Debug reference resolution
- Understand performance characteristics
- Trace what the script is doing

---

## Caching Architecture

The script uses multi-level caching (no TTL — CLI exits quickly):

```python
_bubble_counts_cache    # Message counts per composer (loaded once)
_composers_cache        # Composers per workspace (per-workspace)
_all_composers_cache    # All composers globally (loaded once)
```

This means:
- First command may be slower (loading caches)
- Subsequent operations in same run are fast
- `get_all_composers()` loads everything once for global searches

---

## Safety

- **Read-only** — SQLite opened with `?mode=ro`
- **No mutations** — Never writes to Cursor data stores
- **Gitignored artifacts** — Derived data goes to `.moollm/`
- **Privacy** — Sanitize before sharing externally

---

## Designing Your Own Orchestrator

Use the insights from this skill to design a custom orchestrator:

### 1. Understand Context Assembly

```bash
# How Cursor builds prompts
cursor-mirror request-context @1 --yaml

# Key patterns:
# - fileSelections: @ mentioned files
# - selections: highlighted code  
# - cursorRules: rules always included
# - codebase_search: semantic search results
```

### 2. Learn from Limits

```bash
cursor-mirror status-config

# Important limits:
# - 30K context tokens
# - 100 max MCP tools
# - 250K max indexed files
```

### 3. Study Tool Patterns

```bash
cursor-mirror tools @1 -v

# Observe:
# - Tool naming (_v2 suffixes)
# - Parameter patterns
# - Result formats
```

### 4. Trace MCP Protocol

```bash
cursor-mirror mcp --all -v

# Learn:
# - How MCP servers register
# - Tool call format
# - Result handling
```

---

## Related Skills

| Skill | Integration |
|-------|-------------|
| `bootstrap` | Use cursor-mirror to trace boot sequences |
| `session-log` | Export conversations for documentation |
| `summarize` | Summarize for cold storage |
| `debugging` | Debug agent behavior |
| `k-lines` | Protocol symbol activation |

---

## Protocol Symbol

```
CURSOR-CHAT
```

**Aliases:** `CHAT-REFLECT`, `CURSOR-INSPECT`, `WATCH-YOURSELF-THINK`

Invoke when: Self-introspection, boot analysis, driver optimization, orchestrator design.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml)

---

## License

MIT License — Copyright (c) 2026 Don Hopkins, Leela AI. Use freely, credit required.

---

## Navigation

| Direction | Destination |
|-----------|-------------|
| ⬆️ Up | [skills/](../) |
| 📜 Index | [PROTOCOLS.yml](../../PROTOCOLS.yml) |
| 🧠 Core | [kernel/constitution-core.md](../../kernel/constitution-core.md) |
| 🚀 Bootstrap | [bootstrap/](../bootstrap/) |
| 🔧 Driver | [kernel/drivers/cursor.yml](../../kernel/drivers/cursor.yml) |

---

*Watch yourself think. The filesystem is your memory. Introspection is power.*
