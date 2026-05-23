---
name: transcript-intelligence
description: Search and analyze Claude Code transcripts for past decisions, solutions, and discussions. Use when recalling past context, finding solutions to previously-solved problems, understanding session history, or restoring context after compact/clear.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Transcript Intelligence

Search, analyze, and extract knowledge from Claude Code session transcripts - your deep memory for past conversations, decisions, and solutions.

## Quick Reference

| Element | Value |
|---------|-------|
| Transcript Location | `~/.claude/projects/<project-hash>/<session-id>.jsonl` |
| Format | JSONL (one JSON object per line) |
| Line Types | `user`, `assistant`, `system`, `summary`, `file-history-snapshot` |
| Key Tools | `rg` (ripgrep), `jq`, `Grep`, `Read`, `sesh` |
| Integration | Works with `/recall` command and `sesh` CLI |

## Using sesh for Easy Access

The `sesh` CLI provides human-friendly access to transcripts by session name:

```bash
# Get transcript path by session name
sesh transcript my-session
# Output: /Users/you/.claude/projects/.../abc123.jsonl

# View transcript directly
cat $(sesh transcript my-session)

# Search within a named session
rg "keyword" $(sesh transcript my-session)

# Pipe to jq for structured queries
cat $(sesh transcript my-session) | jq 'select(.type == "user")'

# Get session info (includes transcript path)
sesh info my-session

# List sessions for current project
sesh list --project .

# List recent sessions
sesh list --limit 10
```

### Benefits Over Manual Path Navigation

| Manual Approach | With sesh |
|----------------|-----------|
| `ls ~/.claude/projects/` to find hash | `sesh list` to see all sessions |
| Remember session UUIDs | Use memorable names like "auth-feature" |
| Navigate nested directories | `sesh transcript <name>` returns path |
| Search across unknown paths | `sesh list --project /path` filters by project |

## Transcript Location

Transcripts are stored in project-specific directories:

```
~/.claude/projects/
├── <project-hash-1>/
│   ├── <session-id-1>.jsonl
│   ├── <session-id-2>.jsonl
│   └── ...
├── <project-hash-2>/
│   └── ...
└── ...
```

### Finding Your Project's Transcripts

**Using sesh (recommended):**
```bash
# List sessions for current project
sesh list --project .

# Get transcript path by name
sesh transcript my-session

# View session details including transcript
sesh info my-session
```

**Manual approach:**
```bash
# List all Claude project directories
ls -la ~/.claude/projects/

# Find transcripts for current project (by recent modification)
ls -lt ~/.claude/projects/*/  | head -20

# Find all transcripts modified in last 7 days
find ~/.claude/projects -name "*.jsonl" -mtime -7
```

## Transcript Line Structure

Each line is a JSON object:

```typescript
interface TranscriptLine {
  type: 'user' | 'assistant' | 'file-history-snapshot' | 'system' | 'summary';
  uuid: string;
  parentUuid: string | null;
  sessionId: string;
  timestamp: string;           // ISO 8601 format
  cwd: string;                 // Working directory
  version: string;             // Claude Code version
  gitBranch?: string;          // Git branch (if in repo)
  message: {
    role: 'user' | 'assistant';
    content: ContentBlock[] | string;
    model?: string;            // e.g., "claude-sonnet-4-20250514"
    usage?: {
      input_tokens: number;
      output_tokens: number;
    };
  };
  toolUseResult?: any;         // Result from tool execution
}
```

### Content Block Types

The `message.content` field can contain:

| Type | Description |
|------|-------------|
| `text` | Plain text content |
| `tool_use` | Claude invoking a tool |
| `tool_result` | Result from tool execution |
| `thinking` | Claude's reasoning (extended thinking) |

## Common Search Patterns

### Search for Decisions

```bash
# Find discussions about specific topics
rg -i "decided|decision|chose|choice" ~/.claude/projects/<hash>/*.jsonl

# Find architectural decisions
rg -i "architecture|design|pattern" ~/.claude/projects/<hash>/*.jsonl

# Find trade-off discussions
rg -i "tradeoff|trade-off|pros and cons|alternative" ~/.claude/projects/<hash>/*.jsonl
```

### Search for Solutions

```bash
# Find error resolutions
rg -i "fixed|resolved|solution|workaround" ~/.claude/projects/<hash>/*.jsonl

# Find specific error discussions
rg "error|exception|failed" ~/.claude/projects/<hash>/*.jsonl | rg -i "<error-text>"

# Find implementation discussions
rg -i "implemented|implementation|approach" ~/.claude/projects/<hash>/*.jsonl
```

### Search by Time

```bash
# Find recent transcripts (last 24 hours)
find ~/.claude/projects -name "*.jsonl" -mtime -1

# Search within date range (using jq)
cat transcript.jsonl | jq -r 'select(.timestamp >= "2025-01-01" and .timestamp < "2025-01-07")'
```

### Search User Messages Only

```bash
# Extract only user prompts
cat transcript.jsonl | jq -r 'select(.type == "user") | .message.content'

# Search user messages for keyword
cat transcript.jsonl | jq -r 'select(.type == "user") | .message.content' | rg -i "keyword"
```

### Search Assistant Responses Only

```bash
# Extract assistant text responses
cat transcript.jsonl | jq -r 'select(.type == "assistant") | .message.content[] | select(.type == "text") | .text'

# Search assistant responses
cat transcript.jsonl | jq -r 'select(.type == "assistant") | .message.content[] | select(.type == "text") | .text' | rg -i "keyword"
```

## Use Cases

### 1. Context Restoration After Compact

When context is compacted or cleared, search transcripts to restore important information:

```bash
# Using sesh (recommended) - search by session name
rg -C 3 "important|critical|remember|note" $(sesh transcript my-session)

# Find file modifications in named session
cat $(sesh transcript my-session) | jq '.message.content[] | select(.type == "tool_use" and (.name == "Write" or .name == "Edit"))'

# Manual approach with raw path
rg -C 3 "important|critical|remember|note" <transcript>.jsonl
```

### 2. Finding Past Solutions

Recall how you solved similar problems:

```bash
# Search for specific error across all sessions
rg -l "TypeError" ~/.claude/projects/<hash>/*.jsonl

# Get context around the solution
rg -C 5 "TypeError" <transcript>.jsonl
```

### 3. Session Analytics

Understand usage patterns:

```bash
# Count messages per session
wc -l ~/.claude/projects/<hash>/*.jsonl

# Token usage in session
cat transcript.jsonl | jq -r 'select(.message.usage) | .message.usage | "\(.input_tokens) in, \(.output_tokens) out"'

# Total tokens
cat transcript.jsonl | jq -s '[.[].message.usage | select(.) | .input_tokens + .output_tokens] | add'
```

### 4. Finding Specific Tool Uses

```bash
# Find all file writes
cat transcript.jsonl | jq 'select(.type == "assistant") | .message.content[] | select(.type == "tool_use" and .name == "Write")'

# Find all bash commands run
cat transcript.jsonl | jq 'select(.type == "assistant") | .message.content[] | select(.type == "tool_use" and .name == "Bash") | .input.command'

# Find files that were read
cat transcript.jsonl | jq 'select(.type == "assistant") | .message.content[] | select(.type == "tool_use" and .name == "Read") | .input.file_path'
```

### 5. Reconstructing Conversation Flow

```bash
# Get chronological conversation with timestamps
cat transcript.jsonl | jq -r '[.timestamp, .type, (if .type == "user" then .message.content else (.message.content[] | select(.type == "text") | .text[:100]) end)] | @tsv'

# Get user-assistant pairs
cat transcript.jsonl | jq -r 'select(.type == "user" or .type == "assistant") | "\(.type): \(if .message.content | type == "string" then .message.content else (.message.content[] | select(.type == "text") | .text[:200]) end)"'
```

## Integration with /recall Command

This skill works alongside the `/recall` command for structured memory retrieval:

```bash
# /recall uses this skill to search transcripts
/recall "what did we decide about the API design?"
```

When invoked via `/recall`:
1. Identify relevant project hash
2. Search across all session transcripts
3. Extract relevant context with surrounding lines
4. Summarize findings

## Workflow: Deep Memory Search

### Prerequisites
- [ ] Know the topic or keyword to search
- [ ] Have `sesh` CLI available (or access to `~/.claude/projects/`)
- [ ] Know approximate timeframe (optional)

### Steps (Using sesh - Recommended)

1. **List available sessions**
   - [ ] List project sessions: `sesh list --project .`
   - [ ] Or list all recent: `sesh list --limit 20`

2. **Search by session name**
   - [ ] Search named session: `rg -i "<keyword>" $(sesh transcript my-session)`
   - [ ] Or get path first: `sesh transcript my-session`

3. **Get context around matches**
   - [ ] `rg -C 5 "<keyword>" $(sesh transcript my-session)`

4. **Extract structured data**
   - [ ] `cat $(sesh transcript my-session) | jq 'select(.type == "user")'`

5. **Summarize findings**
   - [ ] Compile key decisions/solutions
   - [ ] Note related discussions

### Steps (Manual - Without sesh)

1. **Identify project directory**
   - [ ] List projects: `ls ~/.claude/projects/`
   - [ ] Find relevant project hash by examining recent files

2. **Perform broad search**
   - [ ] Search across all sessions: `rg -i "<keyword>" ~/.claude/projects/<hash>/*.jsonl`
   - [ ] Note which sessions have matches

3. **Narrow to specific session**
   - [ ] Focus on most relevant session
   - [ ] Get context: `rg -C 5 "<keyword>" <session>.jsonl`

4. **Extract structured data**
   - [ ] Use `jq` for specific fields
   - [ ] Parse tool uses if relevant

5. **Summarize findings**
   - [ ] Compile key decisions/solutions
   - [ ] Note related discussions

### Validation
- [ ] Found relevant context
- [ ] Decisions/solutions extracted
- [ ] Context is sufficient to continue work

## Performance Tips

| Scenario | Recommendation |
|----------|----------------|
| Large transcripts | Use `rg -l` first to find files, then search specific ones |
| Many sessions | Narrow by date with `find -mtime` |
| Complex queries | Pipe through `jq` for structured filtering |
| Slow searches | Limit with `head` or `-m` (max matches) |

## Common jq Patterns

```bash
# Pretty print specific line types
cat transcript.jsonl | jq 'select(.type == "user")'

# Extract timestamps
cat transcript.jsonl | jq -r '.timestamp'

# Get unique models used
cat transcript.jsonl | jq -r '.message.model // empty' | sort -u

# Count by type
cat transcript.jsonl | jq -r '.type' | sort | uniq -c

# Get git branches used
cat transcript.jsonl | jq -r '.gitBranch // empty' | sort -u
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transcripts found | Check `~/.claude/projects/` exists and has subdirectories |
| Empty results | Try broader search terms, check project hash |
| jq errors | Ensure each line is valid JSON (some may be malformed) |
| Slow searches | Use file-level filtering first (`rg -l`), then content search |
| Can't find project | Look at recent modification times, or search all projects |
| sesh returns "no transcript path" | Session was created before transcript tracking was enabled |
| sesh session not found | Check `sesh list` to see available session names |
| Need to search older sessions | Use `sesh list --all-machines` to see sessions from all machines |

## Security Notes

- Transcripts may contain sensitive information
- Avoid searching for/exposing secrets, API keys, passwords
- Be cautious when sharing transcript excerpts
- Transcripts are local to your machine

## Hook Event Integration

When the `event-logger` hook handler is enabled, hook events are logged to `~/.claude/hooks/` and can be indexed alongside transcripts for unified analysis.

### Enabling Hook Event Logging

Add to your `hooks.yaml`:

```yaml
builtins:
  event-logger:
    enabled: true
```

### Unified Index

The transcript CLI indexes both transcripts and hook events:

```bash
# Build unified index
bun run bin/transcript.ts index build

# Check status (shows transcript + hook counts)
bun run bin/transcript.ts index status

# Run daemon to watch both
bun run bin/transcript.ts index daemon start
```

### SQL JOINs

Query across transcripts and hook events:

```sql
-- Find blocked tool calls with transcript context
SELECT h.toolName, h.decision, l.content_text
FROM hook_events h
JOIN lines l ON h.session_id = l.session_id AND h.tool_use_id = l.uuid
WHERE h.decision = 'block';
```

See [TYPES.md](./TYPES.md) for complete hook event schema and JOIN patterns.

## Reference Files

| File | Contents |
|------|----------|
| [TYPES.md](./TYPES.md) | Complete TypeScript type definitions (includes hook events) |
| [SEARCH.md](./SEARCH.md) | Advanced search patterns and queries |
