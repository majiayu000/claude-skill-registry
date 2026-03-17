---
name: session-search
description: |
  Search and analyze AI coding assistant session history using Terraphim.
  Find past conversations, discover patterns, and learn from previous work.
  Supports Claude Code, Cursor, Aider, and other AI coding assistants.
license: Apache-2.0
---

# Session Search

Use this skill when searching through AI coding assistant history to find relevant past work, patterns, or context from previous sessions.

## Overview

Terraphim provides unified session search across multiple AI coding assistants:

- **Claude Code** - Native session parsing from `~/.claude/projects/`
- **Cursor** - IDE session history
- **Aider** - Git-based conversation logs
- **OpenCode** - Session history

**Key Capabilities:**
- Full-text search across messages
- Knowledge graph-enriched concept search
- Related session discovery
- Timeline visualization
- Export to JSON/Markdown

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Session Sources                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Claude Code  │  │   Cursor     │  │    Aider     │          │
│  │ ~/.claude/   │  │ ~/.cursor/   │  │ .aider.chat  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │     terraphim_sessions        │
              │   (Connector Registry)        │
              └───────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
   ┌──────────────────────┐       ┌──────────────────────┐
   │   SessionService     │       │   SessionEnricher    │
   │   (Import, Search)   │       │   (Concept Matching) │
   └──────────────────────┘       └──────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Knowledge Graph Concepts    │
              │   (terraphim_automata)        │
              └───────────────────────────────┘
```

## For Humans

### Quick Start with REPL

```bash
# Build with session features
cargo build -p terraphim_agent --features repl-full --release

# Launch REPL
./target/release/terraphim-agent

# In REPL:
/sessions sources          # Detect available sources
/sessions import           # Import from all sources
/sessions search "rust"    # Search for "rust" in sessions
/sessions stats            # Show statistics
```

### Session Commands Reference

| Command | Description |
|---------|-------------|
| `/sessions sources` | Detect available session sources |
| `/sessions import [source] [--limit N]` | Import sessions from source |
| `/sessions list [source] [--limit N]` | List imported sessions |
| `/sessions search <query>` | Full-text search |
| `/sessions stats` | Show statistics |
| `/sessions show <id>` | Show session details |
| `/sessions concepts <concept>` | Search by knowledge graph concept |
| `/sessions related <id> [--min N]` | Find related sessions |
| `/sessions timeline [--group day|week|month]` | Timeline view |
| `/sessions export [--format json|md] [--output file]` | Export sessions |
| `/sessions enrich [id]` | Enrich with concepts |

### Example Workflows

**Find previous work on a topic:**
```
/sessions search "authentication"
/sessions show abc123-def456
```

**Discover patterns across projects:**
```
/sessions import
/sessions stats
/sessions timeline --group week --limit 10
```

**Find related solutions:**
```
/sessions concepts "error handling"
/sessions related abc123 --min 3
```

### CLI Usage

```bash
# Direct CLI search (without REPL)
terraphim-agent sessions search "database migration"

# Import and search in one pipeline
terraphim-agent sessions import && terraphim-agent sessions search "API design"

# Export specific session
terraphim-agent sessions export --session abc123 --format markdown --output session.md
```

## For AI Agents

### Detecting Session Capabilities

Check if sessions feature is available:

```bash
# Check if terraphim-agent has session support
if terraphim-agent sessions sources 2>/dev/null | grep -q "claude-code"; then
    echo "Session search available"
fi
```

### Programmatic Usage (Rust)

```rust
use terraphim_sessions::{SessionService, ImportOptions};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Create service
    let service = SessionService::new();

    // Detect sources
    let sources = service.detect_sources();
    for source in sources {
        println!("{}: {:?}", source.id, source.status);
    }

    // Import sessions
    let options = ImportOptions::default().with_limit(100);
    let sessions = service.import_all(&options).await?;

    // Search
    let results = service.search("async rust").await;
    for session in results {
        println!("{}: {} messages",
            session.id,
            session.message_count()
        );
    }

    Ok(())
}
```

### Knowledge Graph Enrichment

```rust
use terraphim_sessions::{SessionEnricher, EnrichmentConfig};

// Create enricher with automata
let config = EnrichmentConfig {
    thesaurus_path: "docs/src/kg/".into(),
    min_confidence: 0.8,
};
let enricher = SessionEnricher::new(config)?;

// Enrich session with concepts
let enriched = enricher.enrich(&session)?;

// Get matched concepts
for concept in enriched.concepts {
    println!("{}: {} occurrences",
        concept.term,
        concept.occurrences.len()
    );
}

// Find related sessions by shared concepts
let related = find_related_sessions(&sessions, &enriched, 3)?;
```

### MCP Integration

Session search can be exposed via MCP tools:

```json
{
  "tool": "session_search",
  "arguments": {
    "query": "error handling patterns",
    "limit": 10
  }
}
```

### claude-log-analyzer Usage

For detailed session analysis:

```rust
use claude_log_analyzer::{Analyzer, Reporter};

// Analyze from default location
let analyzer = Analyzer::from_default_location()?;
let analyses = analyzer.analyze(None)?;

// Get agent usage statistics
for analysis in &analyses {
    for agent in &analysis.agents {
        println!("{}: {} invocations",
            agent.agent_type,
            agent.invocation_count
        );
    }
}

// Generate report
let reporter = Reporter::new();
reporter.print_terminal(&analyses);
```

## Use Cases

### 1. Learning from Past Work

```
You: "How did I solve the authentication issue last month?"
Claude: [session-search skill]

Action:
1. /sessions search "authentication"
2. /sessions timeline --group week
3. /sessions show <relevant-id>

Output:
- Session summaries matching query
- Timeline of related work
- Full conversation details
```

### 2. Discovering Patterns

```
You: "What agents have I used most frequently?"
Claude: [session-search skill]

Action:
1. Import all sessions
2. Analyze agent usage via claude-log-analyzer
3. Generate statistics

Output:
- Agent usage breakdown
- Most productive agents
- Collaboration patterns
```

### 3. Context for New Tasks

```
You: "I need to implement caching again"
Claude: [session-search skill]

Action:
1. /sessions concepts "caching"
2. /sessions related <cache-session-id>
3. Extract relevant patterns

Output:
- Previous caching implementations
- Related design decisions
- Code patterns to reuse
```

### 4. Knowledge Transfer

```
You: "Export my sessions about the payment system"
Claude: [session-search skill]

Action:
1. /sessions search "payment"
2. /sessions export --format markdown --output payments-history.md

Output:
- Markdown file with full session history
- Ready for sharing or archival
```

## Session Data Model

```rust
pub struct Session {
    pub id: SessionId,
    pub source: String,           // "claude-code", "cursor", etc.
    pub title: Option<String>,
    pub messages: Vec<Message>,
    pub metadata: SessionMetadata,
}

pub struct Message {
    pub role: MessageRole,        // User, Assistant, System
    pub content: String,
    pub timestamp: Option<DateTime>,
}

pub struct SessionMetadata {
    pub project_path: Option<String>,
    pub started_at: Option<DateTime>,
    pub ended_at: Option<DateTime>,
    pub agent_types: Vec<String>,
}
```

## Configuration

### Feature Flags

```toml
[dependencies]
terraphim_agent = {
    version = "1.0",
    features = ["repl-sessions"]
}

terraphim_sessions = {
    version = "0.1",
    features = ["cla-full", "enrichment"]
}
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_SESSIONS_DIR` | Override Claude sessions location |
| `TERRAPHIM_VERBOSE` | Enable verbose logging |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No sessions found | Run `/sessions sources` to check available sources |
| Import fails | Check permissions on `~/.claude/projects/` |
| Search too slow | Use `--limit` to reduce scope |
| Concepts not matching | Verify knowledge graph files in `docs/src/kg/` |
| Feature not available | Rebuild with `--features repl-sessions` |

## Related Skills

- `terraphim-hooks` - Knowledge graph-based text replacement
- `debugging` - Use session history for debugging context
- `architecture` - Reference past architectural decisions
