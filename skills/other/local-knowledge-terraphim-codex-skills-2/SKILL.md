---
name: local-knowledge
description: |
  Leverage personal notes and documentation through Terraphim's role-based search.
  AI agents can search developer's local knowledge organized by domain (Rust, frontend, architecture)
  using the terraphim-agent REPL commands.
license: Apache-2.0
---

# Local Knowledge Search

Use this skill when you need to search the developer's personal notes, documentation, or local knowledge base for context-specific information.

## Overview

Terraphim enables AI coding agents to search local knowledge through role-based haystacks. Different roles have access to different knowledge domains:

| Role | Knowledge Domain | Haystacks |
|------|------------------|-----------|
| Terraphim Engineer | Architecture, system design | Local docs + Knowledge Graph |
| Rust Engineer | Rust patterns, async, WASM | Local notes + Query.rs API |
| Frontend Engineer | JavaScript, TypeScript, React | GrepApp (GitHub code search) |

## When to Use This Skill

Search local knowledge when the user:
- Asks about topics in their personal notes ("in my notes", "my documentation")
- Needs domain-specific patterns they've documented before
- Asks "how do I usually do X" or "what's our pattern for Y"
- References previous solutions or bookmarked resources

**Trigger Phrases:**
- "check my notes about..."
- "search my documentation for..."
- "what do I have on..."
- "find my notes on..."
- Any domain-specific question (Rust async, frontend patterns, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Agent                         │
│  Uses /search and /role commands via terraphim-agent REPL   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    terraphim-agent REPL                      │
│  /search "query" --role rust-engineer --limit 10            │
└───────────────────────────┬─────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Terraphim Eng   │ │ Rust Engineer   │ │ Frontend Eng    │
│                 │ │                 │ │                 │
│ • Local docs    │ │ • Rust notes    │ │ • GrepApp JS    │
│ • expanded_docs │ │ • Query.rs      │ │ • GrepApp TS    │
│ • Knowledge KG  │ │ • Auto-gen KG   │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## For Humans

### Quick Start

```bash
# Build terraphim-agent with REPL features
cd /path/to/terraphim-ai
cargo build -p terraphim_agent --features repl-full --release

# Start the REPL
./target/release/terraphim-agent

# In REPL: List available roles
/role list

# Switch to Rust Engineer role
/role select rust-engineer

# Search your notes
/search "async iterator patterns" --limit 5
```

### Role Configuration

Roles are defined in JSON config files at `terraphim_server/default/`:

```json
{
  "roles": {
    "Rust Engineer": {
      "relevance_function": "title-scorer",
      "haystacks": [
        {
          "location": "/path/to/your/notes",
          "service": "Ripgrep",
          "extra_parameters": { "glob": "*rust*.md" }
        }
      ]
    }
  }
}
```

### Adding Your Own Notes

1. Create a notes directory (e.g., `~/notes/rust/`)
2. Add markdown files with your knowledge
3. Update role config to include the directory as a Ripgrep haystack
4. Optionally create a knowledge graph for semantic term expansion

## For AI Agents

### Detecting Terraphim Capabilities

Check if terraphim-agent is available:

```bash
# Find the agent binary
if command -v terraphim-agent >/dev/null 2>&1; then
    AGENT="terraphim-agent"
elif [ -x "./target/release/terraphim-agent" ]; then
    AGENT="./target/release/terraphim-agent"
elif [ -x "$HOME/projects/terraphim/terraphim-ai/target/release/terraphim-agent" ]; then
    AGENT="$HOME/projects/terraphim/terraphim-ai/target/release/terraphim-agent"
fi
```

### REPL Command Reference

**Search Commands:**

```bash
# Basic search (uses current role)
/search "query string"

# Search with specific role
/search "async patterns" --role rust-engineer

# Limit results
/search "error handling" --limit 5

# Semantic search (uses knowledge graph)
/search "error handling" --semantic

# Concept-based search
/search "error handling" --concepts
```

**Role Commands:**

```bash
# List available roles
/role list

# Select a role
/role select rust-engineer

# Show current role
/role current
```

**Graph Commands:**

```bash
# Show knowledge graph terms
/graph

# Show top K terms
/graph --top-k 20
```

### Search Patterns for AI Agents

**Pattern 1: Domain-Specific Search**

When the user asks about a specific domain, select the appropriate role first:

```bash
# User asks about Rust async
/role select rust-engineer
/search "async iterator" --limit 5
```

**Pattern 2: Broad Knowledge Search**

For general questions, use the Terraphim Engineer role with expanded_docs:

```bash
/role select terraphim-engineer
/search "atomic data server configuration"
```

**Pattern 3: Code Examples**

For frontend code examples, use GrepApp integration:

```bash
/role select frontend-engineer
/search "useState useEffect pattern"
```

### Interpreting Results

Search results include:
- **title**: Document/note title
- **url**: File path or source URL
- **body**: Content excerpt
- **description**: Summary (if LLM summarization enabled)
- **rank**: Relevance score

Example output:

```
Results for "async iterator":

1. [rust-matching-iterators.md]
   Path: /Users/alex/notes/rust-matching-iterators.md
   Async iterator over AWS S3 pagination using State enum...

2. [rust-python-extension.md]
   Path: /Users/alex/notes/rust-python-extension.md
   PyO3/Maturin async patterns for Python extensions...
```

### Error Handling

If terraphim-agent is not available or fails:

1. **Graceful degradation**: Continue without local search
2. **Notify user**: "Local knowledge search unavailable, using general knowledge"
3. **Fallback**: Use web search or built-in knowledge

```bash
# Check if search succeeded
if ! /search "query" 2>/dev/null; then
    echo "Local search unavailable, falling back to general knowledge"
fi
```

## Knowledge Graph Format

Knowledge graph files enable semantic term expansion:

```markdown
# term_name

Optional description of the term.

synonyms:: synonym1, synonym2, synonym3
```

**Example - Rust async terms:**

```markdown
# async_iterator

Async iterators in Rust using Stream trait and async/await.

synonyms:: Stream, AsyncIterator, futures::Stream, tokio::stream
```

## Configuration Examples

### Rust Engineer with Local Notes

```json
{
  "Rust Engineer": {
    "shortname": "rust-engineer",
    "relevance_function": "terraphim-graph",
    "kg": {
      "knowledge_graph_local": {
        "input_type": "markdown",
        "path": "docs/src/kg/rust_notes_kg"
      }
    },
    "haystacks": [
      {
        "location": "/Users/alex/synced/expanded_docs",
        "service": "Ripgrep",
        "extra_parameters": { "glob": "*rust*.md" }
      },
      {
        "location": "https://query.rs",
        "service": "QueryRs"
      }
    ]
  }
}
```

### Frontend Engineer with GrepApp

```json
{
  "Frontend Engineer": {
    "shortname": "frontend-engineer",
    "relevance_function": "title-scorer",
    "haystacks": [
      {
        "location": "https://grep.app",
        "service": "GrepApp",
        "extra_parameters": { "language": "JavaScript" }
      },
      {
        "location": "https://grep.app",
        "service": "GrepApp",
        "extra_parameters": { "language": "TypeScript" }
      }
    ]
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results returned | Check haystack path exists and contains .md files |
| Wrong role active | Use `/role select <name>` to switch |
| Search too slow | Reduce `--limit` or use more specific queries |
| KG not loading | Verify path in config and markdown format |
| Agent not found | Build with `cargo build -p terraphim_agent --features repl-full --release` |

## Related Skills

- `terraphim-hooks` - For text replacement using knowledge graph
- `session-search` - For searching AI coding session history
- `rust-development` - For Rust-specific patterns
