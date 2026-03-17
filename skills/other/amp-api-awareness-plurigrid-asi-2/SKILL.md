---
name: amp-api-awareness
description: Extract hidden Amp API patterns from local thread data via DuckDB analysis
version: 1.0.0
trit: 0
---

# Amp API Awareness

Discover Amp's undocumented API by mining local thread storage.

## Data Sources

| Source | Path | Format |
|--------|------|--------|
| Threads | `~/.local/share/amp/threads/*.json` | JSON per thread |
| History | `~/.claude/history.jsonl` | JSONL sessions |
| Projects | `~/.claude/projects/*/*.jsonl` | JSONL per project |

## Quick Extraction

### Count all threads
```bash
ls ~/.local/share/amp/threads/*.json | wc -l
```

### Sample thread structure
```bash
cat ~/.local/share/amp/threads/T-*.json | head -1 | jq 'keys'
# Expected: ["id", "title", "created", "updatedAt", "messages", ...]
```

### DuckDB unified query
```sql
-- Load all threads
CREATE TABLE amp_threads AS
SELECT * FROM read_json('~/.local/share/amp/threads/*.json', 
  columns={id: 'VARCHAR', title: 'VARCHAR', created: 'BIGINT', 
           messages: 'JSON[]', creatorUserID: 'VARCHAR'},
  ignore_errors=true);

-- Extract message patterns
SELECT 
  id,
  title,
  len(messages) as msg_count,
  abs(hash(id)) % 3 - 1 as trit
FROM amp_threads
ORDER BY created DESC
LIMIT 20;
```

## API Discovery Patterns

### 1. Tool Usage Extraction
```sql
-- Find all tool invocations across threads
SELECT 
  json_extract_string(msg, '$.type') as msg_type,
  json_extract_string(msg, '$.name') as tool_name,
  count(*) as usage_count
FROM amp_threads, unnest(messages) as t(msg)
WHERE json_extract_string(msg, '$.type') = 'tool_use'
GROUP BY 1, 2
ORDER BY usage_count DESC;
```

### 2. MCP Server Detection
```sql
-- Extract MCP patterns from content
SELECT DISTINCT
  regexp_extract(content, 'mcp__([a-z_]+)__', 1) as mcp_server
FROM (
  SELECT json_extract_string(msg, '$.content') as content
  FROM amp_threads, unnest(messages) as t(msg)
)
WHERE mcp_server IS NOT NULL;
```

### 3. Thread Schema Discovery
```javascript
// TypeScript extraction from thread JSON
interface AmpThread {
  id: string;           // T-{uuid}
  title: string;
  created: number;      // Unix timestamp ms
  updatedAt: string;    // ISO8601
  creatorUserID: string;
  messages: AmpMessage[];
}

interface AmpMessage {
  role: 'user' | 'assistant';
  content: ContentBlock[];
}

type ContentBlock = 
  | { type: 'text'; text: string }
  | { type: 'thinking'; thinking: string }
  | { type: 'tool_use'; id: string; name: string; input: unknown }
  | { type: 'tool_result'; tool_use_id: string; content: string };
```

## Full Statistics (2,424 threads, 118,951 messages)

### Core Tools
| Tool | Invocations | Purpose |
|------|-------------|---------|
| `Bash` | 30,786 | Shell commands |
| `Read` | 10,373 | File reading |
| `edit_file` | 6,884 | File modification |
| `create_file` | 5,373 | File creation |
| `todo_write` | 3,862 | Task management |
| `Grep` | 2,837 | Pattern search |
| `skill` | 1,798 | Skill loading |
| `Task` | 1,314 | Sub-agent dispatch |
| `glob` | 1,121 | File patterns |
| `mermaid` | 1,014 | Diagrams |
| `find_thread` | 892 | Thread search |
| `read_thread` | 834 | Thread content |

### MCP Servers
| Server | Invocations | Top Function |
|--------|-------------|--------------|
| `firecrawl` | 1,715 | `firecrawl_scrape` (1,039) |
| `exa` | 1,323 | `web_search_exa` (1,150) |
| `gay` | 1,284 | `palette` (206), `next_color` (151) |
| `deepwiki` | 405 | `ask_question` (241) |
| `beeper` | 253 | `list_messages` (89) |
| `radare2` | 135 | Binary analysis |
| `huggingface` | 130 | ML model access |
| `tree_sitter` | ~100 | AST queries |

### Agent Modes
- `smart`: 2,398 threads (99%)
- `rush`: 1 thread
- `nil`: 25 threads

## Known Endpoints & APIs

| Endpoint/Command | Access | Notes |
|------------------|--------|-------|
| `ampcode.com/threads/T-*` | Public URL | Thread viewer |
| `ampcode.com/settings` | Auth required | API key, account management |
| `find_thread` tool | Agent API | Query by DSL, returns `creatorUserID` |
| `read_thread` tool | Agent API | Extract thread content by goal |

## CLI Commands

| Command | Purpose |
|---------|---------|
| `amp threads list` | Lists threads with ID, title, visibility, messages |
| `amp threads share --visibility <v>` | Set: private, public, unlisted, workspace, group |
| `amp threads share --support` | Share with Amp support for debugging |
| `amp login` / `amp logout` | Auth management |
| `amp skill list/add/remove` | Skill management |
| `amp mcp list/add/remove` | MCP server configuration |

## Visibility Levels

| Level | Description |
|-------|-------------|
| `private` | Only creator can see |
| `workspace` | All workspace members can see |
| `group` | Specific group access |
| `public` | Anyone with link |
| `unlisted` | Anyone with link (not indexed) |

## User ID Format

From `find_thread` API:
```
creatorUserID: "user_01JZZT0P50CFR9XKKW8SXQ7J74"
```
- Prefix: `user_`
- Body: 26-char ULID-like identifier (TypeID format)

## Workspace Member Discovery

Query workspace threads to find all `creatorUserID` values:
```bash
# Via find_thread DSL (repo: filter scopes to workspace)
find_thread "repo:i after:30d"
```

Example: Two users discovered in workspace `i`:
| User ID | Threads (7d) |
|---------|--------------|
| `user_01JZZT0P50CFR9XKKW8SXQ7J74` | 6 |
| `user_01K5ESNNPKQ43J06VRC1TS5AX0` | 4 |

## Local Storage

| Path | Contents |
|------|----------|
| `~/.local/share/amp/secrets.json` | API key (`apiKey@https://ampcode.com/`) |
| `~/.local/share/amp/session.json` | Current `agentMode` |
| `~/.local/share/amp/threads/*.json` | Thread JSON files |
| `~/.config/amp/settings.json` | User preferences, MCP configs |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AMP_API_KEY` | Access token (overrides stored key) |
| `AMP_URL` | Service URL (default: https://ampcode.com/) |
| `AMP_SETTINGS_FILE` | Custom settings path |

## GF(3) Classification

Threads are colored by hash:
```sql
abs(hash(id)) % 3 - 1 as trit
-- -1 = MINUS (validation threads)
--  0 = ERGODIC (coordination)
-- +1 = PLUS (generation)
```

## Usage

```bash
# Export to DuckDB
duckdb amp-threads.duckdb -c "
  CREATE TABLE threads AS 
  SELECT * FROM read_json('~/.local/share/amp/threads/*.json', 
    ignore_errors=true);
"

# Query patterns
duckdb amp-threads.duckdb -c "
  SELECT title, created FROM threads 
  ORDER BY created DESC LIMIT 10;
"
```

## Underlying LLM Cost Estimates (Jan 2026)

Amp uses multiple LLMs. Pricing per 1M tokens (input/output):

### Claude 4.5 Series (Anthropic)

| Model | Input | Output | Cache Write | Cache Read | Context |
|-------|-------|--------|-------------|------------|---------|
| **Opus 4.5** | $5.00 | $25.00 | $6.25 | $0.50 | 200K |
| **Sonnet 4.5** | $3.00 | $15.00 | $3.75 | $0.30 | 200K/1M |
| **Haiku 4.5** | $1.00 | $5.00 | $1.25 | $0.10 | 200K |

*Sonnet 4.5 >200K context: $6/$22.50 per 1M tokens*

### Gemini 3 Series (Google)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| **Gemini 3 Pro** (≤200K) | $2.00 | $12.00 | 1M |
| **Gemini 3 Pro** (>200K) | $4.00 | $18.00 | 1M |
| **Gemini 3 Flash** | $0.50 | $3.00 | 1M |

### Amp Mode → Model Mapping

| Mode | Primary Model | Cost Profile |
|------|---------------|--------------|
| `smart` | Claude Opus 4.5 | $5/$25 (flagship) |
| `rush` | Claude Haiku 4.5 | $1/$5 (efficient) |
| `large` | Extended context | +50-100% premium |

### Thread Usage Distribution (from 2,424 threads)

| Model | Occurrences | Est. % Usage |
|-------|-------------|--------------|
| `claude-opus-4-5-20251101` | 2,312 | 95.4% |
| `gemini-3-pro-preview` | 27 | 1.1% |
| `claude-sonnet-4-20250514` | 5 | 0.2% |
| `claude-haiku-4-5-20251001` | 1 | 0.04% |

### Cost Optimizations Available

| Strategy | Savings | Notes |
|----------|---------|-------|
| **Prompt Caching** | Up to 90% | For repeated system prompts |
| **Batch API** | 50% | Async processing |
| **Rush Mode** | ~80% | Haiku vs Opus |
| **Token Optimization** | Variable | Concise prompts |

### Amp Pricing Pass-Through

Amp passes LLM costs directly with **no markup** for individuals/teams.
- **Free tier**: $10/day grant (all modes including Opus 4.5)
- **Enterprise**: +50% over individual/team rates

### Example Cost Calculation

Typical thread (~50 messages, 100K tokens total):
```
Opus 4.5: ~$1.50/thread (50K in × $5 + 50K out × $25)
Haiku 4.5: ~$0.30/thread (80% savings)
Gemini 3 Pro: ~$0.70/thread (mid-tier)
```

## Related Skills

- `duckdb-ies` - IES analytics layer
- `amp-team-usage` - Team/session tracking
- `unified-reafference` - Cross-agent session DB

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
amp-api-awareness (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch2: Domain-Specific Languages
- Ch9: Generic Procedures
- Ch8: Degeneracy
- Ch4: Pattern Matching
- Ch5: Evaluation
- Ch6: Layering

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
