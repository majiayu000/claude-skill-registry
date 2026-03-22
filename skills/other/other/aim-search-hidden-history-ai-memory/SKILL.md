---
name: aim-search
description: 'Search memory system with advanced filtering and intent detection'
allowed-tools: Read, Bash
---

# Search Memory - Advanced Memory Retrieval

Search the AI Memory Module using semantic similarity with advanced filtering by collection, type, and intent detection.

## Memory System V2.0

The memory system has 3 collections:
- **code-patterns** - HOW things are built (implementation, error_fix, refactor, file_pattern)
- **conventions** - WHAT rules to follow (rule, guideline, port, naming, structure)
- **discussions** - WHY things were decided (decision, session, blocker, preference, context)

## Usage

```bash
# Basic semantic search (searches code-patterns by default)
/aim-search "how do I implement authentication"

# Search specific collection
/aim-search "error handling patterns" --collection conventions

# Filter by memory type
/aim-search "recent bugs" --type error_fix

# Filter by multiple types
/aim-search "code patterns" --type implementation,refactor

# Use intent detection with cascading search
/aim-search "how do I implement auth" --intent how

# Limit results
/aim-search "database patterns" --limit 10

# Hide decay scores
/aim-search "authentication" --no-decay
```

## Options

- `--collection <name>` - Target specific collection (code-patterns, conventions, discussions)
- `--type <type>` - Filter by memory type (see types below)
- `--intent <intent>` - Use intent detection (how, what, why)
- `--limit <n>` - Maximum results to return (default: 5)
- `--group-id <id>` - Filter by project (default: auto-detect from cwd)
- `--decay` - Show decay scores per result (default: enabled)
- `--no-decay` - Hide decay scores from output

## Memory Types by Collection

### code-patterns
- `implementation` - How features/components were built
- `error_fix` - Errors encountered and solutions
- `refactor` - Refactoring patterns applied
- `file_pattern` - File or module-specific patterns

### conventions
- `rule` - Hard rules that MUST be followed
- `guideline` - Soft guidelines (SHOULD follow)
- `port` - Port configuration rules
- `naming` - Naming conventions
- `structure` - File and folder structure conventions

### discussions
- `decision` - Architectural/design decisions (DEC-xxx)
- `session` - Session summaries
- `blocker` - Blockers and resolutions (BLK-xxx)
- `preference` - User preferences and working style
- `context` - Important conversation context

## Intent Detection

When using `--intent`, the system routes to the appropriate primary collection:
- `how` → code-patterns (implementation examples)
- `what` → conventions (rules and guidelines)
- `why` → discussions (decisions and context)

If primary collection has insufficient results, automatically expands to secondary collections.

## Output Format

Each result shows relevance score, content summary, metadata, and decay scores:

```
1. [0.85] Implementation of authentication middleware
   Collection: code-patterns | Type: implementation | 2026-01-15
   Decay: 0.72 (temporal: 0.61, semantic: 0.85)

2. [0.78] JWT token validation pattern
   Collection: code-patterns | Type: implementation | 2026-01-10
   Decay: 0.65 (temporal: 0.52, semantic: 0.78)
```

When decay scoring is disabled or timestamp is unavailable:
```
1. [0.85] Implementation of authentication middleware
   Collection: code-patterns | Type: implementation | 2026-01-15
   Decay: n/a (temporal: n/a, semantic: 0.85)
```

## Score Interpretation

Results include three scores:
- **Relevance** (primary sort): Combined score from semantic + temporal
- **Semantic**: How closely the content matches your query (vector similarity)
- **Temporal**: How recent the memory is (exponential decay)

A memory with semantic=0.90 and temporal=0.30 is very relevant but old.
A memory with semantic=0.60 and temporal=0.95 is less relevant but very recent.

### Decay Formula

```
final_score = 0.7 * semantic + 0.3 * 0.5^(age_days / half_life)
```

Sub-scores are recomputed client-side (Qdrant returns only the combined score):

```python
age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(stored_at)).days
temporal_score = 0.5 ** (age_days / half_life)
semantic_score = (combined_score - 0.3 * temporal_score) / 0.7
```

Half-life varies by memory type (configured via `decay_type_overrides`):
- `conversation`, `session_summary`: 21 days
- `github_commit`, `github_code_blob`: 14 days
- `github_issue`, `github_pr`: 30 days
- `rule`, `guideline`: 60 days

## Examples

```bash
# Find implementation examples in current project
/aim-search "authentication implementation"

# Find shared conventions across all projects
/aim-search "naming conventions" --collection conventions

# Find specific error fixes
/aim-search "database connection" --type error_fix

# Use cascading search with intent
/aim-search "why did we choose postgres" --intent why

# Find architectural decisions
/aim-search "database choice" --type decision --collection discussions

# Search multiple types
/aim-search "auth patterns" --type implementation,error_fix --limit 10

# Search without decay score display
/aim-search "auth patterns" --no-decay
```

## Python Implementation Reference

This skill uses `search_memories()` from `src/memory/search.py`:

```python
from memory.search import search_memories

results = search_memories(
    query="your search query",
    collection="code-patterns",  # Optional
    memory_type="implementation",  # Optional, can be list
    use_cascading=True,  # Enable cascading search
    intent="how",  # Optional: auto-detects from query
    limit=5
)
```

## Technical Details

- **Semantic Search**: Uses jina-embeddings-v2-base-en for vector similarity
- **Project Scoping**: Automatically detects project from current working directory
- **Cascading**: Searches primary collection first, expands only if insufficient results
- **Attribution**: All results include collection and type attribution
- **Performance**: < 2s for typical searches (NFR-P1)
- **Decay Scoring**: Uses AD-5 formula (SPEC-001). Sub-scores recomputed client-side.

## Notes

- Results sorted by relevance score (highest first)
- Score threshold defaults to 0.7 (configurable in .env)
- Project auto-detection uses git repository root
- code-patterns filtered by project, conventions/discussions are cross-project
- Decay scores displayed to 2 decimal places
