---
name: claude-mem
description: Persistent memory compression system for Claude Code enabling context preservation across sessions with automatic observations, semantic search, and privacy controls
version: 1.0.0
tags: [claude-code, memory, context, persistence, mcp, plugin, sqlite, observations, sessions]
---

# Claude-Mem

Claude-Mem is a persistent memory compression system for Claude Code that enables context preservation across multiple sessions. It automatically captures tool usage observations, generates semantic summaries, and makes them available to future sessions, maintaining project knowledge continuity.

## Key Features

- **Persistent Memory** - Context survives between sessions automatically
- **Folder Context Files** - Auto-generated `CLAUDE.md` files with activity timelines
- **Multilingual Support** - 28+ languages including Spanish, Chinese, French, Japanese
- **Mode System** - Switchable workflows (Code, Email Investigation, Chill)
- **MCP Search Tools** - Natural language queries across project history
- **Web Viewer UI** - Real-time memory visualization at `http://localhost:37777`
- **Privacy Controls** - `<private>` tags exclude sensitive content from storage
- **FTS5 Search** - Full-text search across all observations
- **Citation System** - Reference past observations by ID

## System Requirements

- **Node.js**: 18.0.0 or higher
- **Claude Code**: Latest version with plugin support
- **Bun**: JavaScript runtime (auto-installed if missing)
- **SQLite 3**: Bundled for persistent storage

## Installation

### Quick Start (Recommended)

```bash
# In Claude Code terminal
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

Restart Claude Code after installation. Context from previous sessions will automatically appear.

### Advanced Installation (Source Build)

```bash
git clone https://github.com/thedotmack/claude-mem.git
cd claude-mem
npm install
npm run build
npm run worker:start
npm run worker:status
```

### Verification

```bash
# Check hook installation
cat plugin/hooks/hooks.json

# View worker logs
npm run worker:logs

# Test context injection
npm run test:context
```

## How It Works

### Five-Stage Pipeline

1. **Session Start** - Injects context from last 10 sessions
2. **User Prompts** - Creates session and saves user input
3. **Tool Executions** - Captures observations from Read, Write, Bash operations
4. **Worker Processes** - Extracts learnings via Claude Agent SDK
5. **Session End** - Generates summaries for next session

### Hook Architecture

| Hook | Timeout | Purpose |
|------|---------|---------|
| SessionStart | 120s | Inject context from recent sessions |
| UserPromptSubmit | 60s | Create session, save prompt |
| PostToolUse | 120s | Capture tool observations |
| Stop | 60s | Generate session summary |

### Captured Activities

The system records every tool interaction:
- File operations (reads, writes, edits)
- Command executions via bash
- File pattern searches and content queries
- All other Claude Code tools

### Processing Pipeline

Captured observations produce:
- Brief titles describing what occurred
- Contextual subtitles
- Detailed narrative explanations
- Key learnings as bullet points
- Relevant concept tags
- Work classifications (bugfix, feature, decision, etc.)
- Affected file listings

## Configuration

### Environment Variables

**AI Model Selection:**
```bash
export CLAUDE_MEM_MODEL=sonnet      # haiku, sonnet, opus
export CLAUDE_MEM_PROVIDER=claude   # claude, gemini, openrouter
```

**Provider-Specific:**
```bash
# Gemini
export CLAUDE_MEM_GEMINI_API_KEY="your-key"
export CLAUDE_MEM_GEMINI_MODEL="gemini-2.5-flash-lite"

# OpenRouter
export CLAUDE_MEM_OPENROUTER_API_KEY="your-key"
export CLAUDE_MEM_OPENROUTER_MODEL="xiaomi/mimo-v2-flash:free"
```

**Storage & Networking:**
```bash
export CLAUDE_MEM_DATA_DIR=~/.claude-mem    # Database location
export CLAUDE_MEM_WORKER_PORT=37777         # Service port
export CLAUDE_MEM_WORKER_HOST=127.0.0.1     # Service address
export CLAUDE_MEM_LOG_LEVEL=INFO            # DEBUG, INFO, WARN, ERROR, SILENT
```

**Context Injection:**
```bash
export CLAUDE_MEM_CONTEXT_SESSION_COUNT=10       # Recent sessions to retrieve
export CLAUDE_MEM_CONTEXT_OBSERVATIONS=50        # Injected observations count
export CLAUDE_MEM_CONTEXT_FULL_COUNT=5           # Expanded observations
export CLAUDE_MEM_CONTEXT_FULL_FIELD=narrative   # narrative or facts
```

**Display Options:**
```bash
export CLAUDE_MEM_CONTEXT_SHOW_READ_TOKENS=true
export CLAUDE_MEM_CONTEXT_SHOW_WORK_TOKENS=true
export CLAUDE_MEM_CONTEXT_SHOW_SAVINGS_AMOUNT=true
export CLAUDE_MEM_CONTEXT_SHOW_LAST_SUMMARY=false
export CLAUDE_MEM_CONTEXT_SHOW_LAST_MESSAGE=false
```

**Tool Exclusions:**
```bash
# Comma-separated list of tools to skip
export CLAUDE_MEM_SKIP_TOOLS="ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion"
```

### Settings File

Edit `~/.claude-mem/settings.json`:

```json
{
  "CLAUDE_MEM_MODEL": "sonnet",
  "CLAUDE_MEM_MODE": "code",
  "CLAUDE_MEM_CONTEXT_OBSERVATIONS": 50,
  "CLAUDE_MEM_FOLDER_CLAUDEMD_ENABLED": false
}
```

Or run interactive setup:
```bash
./claude-mem-settings.sh
```

## MCP Search Tools

### Available Tools

**`search`** - Memory index lookup
```
Parameters:
  query      FTS5 search syntax
  limit      Results per page (default: 20)
  offset     Pagination offset
  type       Filter: bugfix, feature, decision, discovery, refactor, change
  project    Filter by project name
  dateStart  Filter from date
  dateEnd    Filter to date
  orderBy    Sort order
```

**`timeline`** - Chronological context retrieval
```
Parameters:
  anchor        Observation ID to center on
  query         Alternative to anchor
  depth_before  Observations before (default: 3)
  depth_after   Observations after (default: 3)
```

**`get_observations`** - Full detail fetching
```
Parameters:
  ids    Array of observation IDs (required)
```

### Search Syntax (FTS5)

```
# Boolean operators
"user auth" AND (JWT OR session) NOT deprecated

# Scoped searches
title:authentication
content:database
concepts:gotcha

# Phrase matching
"connection failed"
```

### Three-Layer Workflow

Achieves ~10x token savings through progressive disclosure:

1. **Search** - Lightweight index (~50-100 tokens per result)
2. **Timeline** - Contextual surroundings (~100-200 tokens per observation)
3. **Get Observations** - Full details only when needed (~500-1,000 tokens per record)

**Example:**
```
User: "What bugs did we fix last week?"

Claude automatically:
1. Calls search(type: "bugfix", dateStart: "2025-01-09")
2. Reviews index results
3. Calls timeline(anchor: [relevant_id]) if context needed
4. Calls get_observations(ids: [...]) for specific details
```

## Modes

### What is a Mode?

A mode defines four aspects:
1. **Observer Role** - How Claude analyzes work (e.g., "Software Engineer")
2. **Observation Types** - Valid categories (Bug Fix, Feature, etc.)
3. **Concepts** - Semantic tags for indexing
4. **Language** - Output language for observations

### Available Modes

| Mode | Description |
|------|-------------|
| `code` | Default software development mode |
| `code--chill` | Fewer observations, only records painful-to-rediscover items |
| `email-investigation` | Email archive analysis, entity tracking |
| `code--es` | Spanish output |
| `code--fr` | French output |
| `code--de` | German output |
| `code--ja` | Japanese output |
| `code--zh` | Chinese output |

### Switching Modes

**Via settings.json:**
```json
{
  "CLAUDE_MEM_MODE": "code--es"
}
```

**Via environment:**
```bash
export CLAUDE_MEM_MODE="code--fr"
```

### Mode Inheritance

Uses `--` separator notation:
- `code--es` loads `code` config, then merges `code--es` overrides
- Child settings override parent values

## Privacy Controls

### Private Tags

Wrap sensitive content to exclude from storage:

```
<private>
Your sensitive content here
</private>
```

**Behavior:**
- Claude sees content during current session
- Content stripped before database storage
- Works in user prompts and tool outputs
- Multiple tags per message allowed
- Multiline content supported

### Use Cases

**Sensitive Information:**
```
<private>
Error: Database connection failed
Host: internal-db-prod.company.com
Port: 5432
User: admin_user
</private>
```

**Temporary Context:**
```
<private>
Deadline: Friday 5pm
Contact: john@company.com
</private>
```

**Debug Output:**
```
<private>
[DEBUG] Full stack trace...
[DEBUG] Memory dump...
</private>
```

### Verification

```bash
# Check that private content was filtered
sqlite3 ~/.claude-mem/claude-mem.db "SELECT prompt_text FROM user_prompts LIMIT 5;"
sqlite3 ~/.claude-mem/claude-mem.db "SELECT narrative FROM observations LIMIT 5;"
```

## Data Storage

### Database Location

Default: `~/.claude-mem/`
- `claude-mem.db` - SQLite database
- `.worker.pid` - Worker process ID
- `logs/worker-YYYY-MM-DD.log` - Daily logs
- `settings.json` - Configuration

### Database Queries

```sql
-- Recent sessions
SELECT session_id, project, created_at, status
FROM sdk_sessions
ORDER BY created_at DESC LIMIT 10;

-- Search observations
SELECT title, type, created_at
FROM observations
WHERE project = 'my-project';
```

## Worker Management

```bash
npm run worker:start    # Start background service
npm run worker:stop     # Stop service
npm run worker:restart  # Restart service
npm run worker:status   # Check status
npm run worker:logs     # View logs
```

## Multi-Prompt Sessions

Sessions span multiple prompts:
- Total prompt count tracked
- Individual prompt identification
- Cross-prompt observation linking
- `/clear` doesn't terminate session (continues with new prompt number)

## Troubleshooting

### Worker Not Starting

```bash
# Check port availability
lsof -i :37777

# Use alternative port
export CLAUDE_MEM_WORKER_PORT=38000
npm run worker:restart
```

### No Context Appearing

```bash
# Verify hooks installed
cat plugin/hooks/hooks.json

# Check database has data
sqlite3 ~/.claude-mem/claude-mem.db "SELECT COUNT(*) FROM observations;"

# View worker logs
npm run worker:logs
```

### High Token Usage

```bash
# Reduce observations
export CLAUDE_MEM_CONTEXT_OBSERVATIONS=25

# Use chill mode
export CLAUDE_MEM_MODE="code--chill"
```

### Database Issues

```bash
# Backup and recreate
cp ~/.claude-mem/claude-mem.db ~/.claude-mem/claude-mem.db.bak
rm ~/.claude-mem/claude-mem.db
npm run worker:restart
```

## Best Practices

1. **Start simple** - Use default settings initially
2. **Tune observations** - Adjust `CLAUDE_MEM_CONTEXT_OBSERVATIONS` based on project size
3. **Use private tags** - Protect credentials and sensitive data
4. **Review periodically** - Check stored observations match expectations
5. **Use chill mode** - For projects with high activity but few critical insights
6. **Search first** - Use MCP tools before asking general questions

## Version History

- **v9.0.0** - Folder context files, git worktree support, configurable limits
- **v7.1.0** - Bun replaces PM2, bun:sqlite replaces better-sqlite3
- **v7.0.0** - 11 configuration settings, dual privacy tags
- **v5.4.0** - Skill-based search (~2,250 tokens saved per session)

## Resources

- **Documentation**: https://docs.claude-mem.ai
- **GitHub**: https://github.com/thedotmack/claude-mem
- **Changelog**: https://github.com/thedotmack/claude-mem/blob/main/CHANGELOG.md
- **Web Viewer**: http://localhost:37777 (when running)
