---
name: rlm
description: Recursive Language Models (RLM) CLI - enables LLMs to recursively process large contexts by decomposing inputs and calling themselves over parts. Use for code analysis, diff reviews, codebase exploration. Triggers on "rlm ask", "rlm complete", "rlm search", "rlm index".
---

# RLM CLI

Recursive Language Models (RLM) CLI - enables LLMs to handle near-infinite context by recursively decomposing inputs and calling themselves over parts. Supports files, directories, URLs, and stdin.

## Installation

```bash
pip install rlm-cli    # or: pipx install rlm-cli
uvx rlm-cli ask ...    # run without installing
```

Set an API key for your backend (openrouter is default):
```bash
export OPENROUTER_API_KEY=...  # default backend
export OPENAI_API_KEY=...      # for --backend openai
export ANTHROPIC_API_KEY=...   # for --backend anthropic
```

## Commands

### ask - Query with context

```bash
rlm ask <inputs> -q "question"
```

**Inputs** (combinable):
| Type | Example | Notes |
|------|---------|-------|
| Directory | `rlm ask . -q "..."` | Recursive, respects .gitignore |
| File | `rlm ask main.py -q "..."` | Single file |
| URL | `rlm ask https://x.com -q "..."` | Auto-converts to markdown |
| stdin | `git diff \| rlm ask - -q "..."` | `-` reads from pipe |
| Literal | `rlm ask "text" -q "..." --literal` | Treat as raw text |
| Multiple | `rlm ask a.py b.py -q "..."` | Combine any types |

**Options:**
| Flag | Description |
|------|-------------|
| `-q "..."` | Question/prompt (required) |
| `--backend` | Provider: `openrouter` (default), `openai`, `anthropic` |
| `--model NAME` | Model override (format: `provider/model` or just `model`) |
| `--json` | Machine-readable output |
| `--output-format` | Output format: `text`, `json`, or `json-tree` |
| `--summary` | Show execution summary with depth statistics |
| `--extensions .py .ts` | Filter by extension |
| `--include/--exclude` | Glob patterns |
| `--max-iterations N` | Limit REPL iterations (default: 30) |
| `--max-depth N` | Recursive RLM depth (default: 1 = no recursion) |
| `--max-budget N.NN` | Spending limit in USD (requires OpenRouter) |
| `--max-timeout N` | Time limit in seconds |
| `--max-tokens N` | Total token limit (input + output) |
| `--max-errors N` | Consecutive error limit before stopping |
| `--no-index` | Skip auto-indexing |
| `--exa` | Enable Exa web search (requires `EXA_API_KEY`) |
| `--inject-file FILE` | Execute Python code between iterations |

**JSON output structure:**
```json
{"ok": true, "exit_code": 0, "result": {"response": "..."}, "stats": {...}}
```

**JSON-tree output (`--output-format=json-tree`):**
Adds execution tree showing nested RLM calls:
```json
{
  "result": {
    "response": "...",
    "tree": {
      "depth": 0,
      "model": "openai/gpt-4",
      "duration": 2.3,
      "cost": 0.05,
      "iterations": [...],
      "children": [...]
    }
  }
}
```

**Summary output (`--summary`):**
Shows depth-wise statistics after completion:
- JSON mode: adds `summary` field to `stats`
- Text mode: prints summary to stderr

```
=== RLM Execution Summary ===
Total depth: 2 | Nodes: 3 | Cost: $0.0054 | Duration: 17.38s
Depth 0: 1 call(s) ($0.0047, 13.94s)
Depth 1: 2 call(s) ($0.0007, 3.44s)
```

### complete - Query without context

```bash
rlm complete "prompt text"
rlm complete "Generate SQL" --json --backend openai
```

### search - Search indexed files

```bash
rlm search "query" [options]
```

| Flag | Description |
|------|-------------|
| `--limit N` | Max results (default: 20) |
| `--language python` | Filter by language |
| `--paths-only` | Output file paths only |
| `--json` | JSON output |

Auto-indexes on first use. Manual index: `rlm index .`

### index - Build search index

```bash
rlm index .              # Index current dir
rlm index ./src --force  # Force full reindex
```

### doctor - Check setup

```bash
rlm doctor       # Check config, API keys, deps
rlm doctor --json
```

## Workflows

**Git diff review:**
```bash
git diff | rlm ask - -q "Review for bugs"
git diff --cached | rlm ask - -q "Ready to commit?"
git diff HEAD~3 | rlm ask - -q "Summarize changes"
```

**Codebase analysis:**
```bash
rlm ask . -q "Explain architecture"
rlm ask src/ -q "How does auth work?" --extensions .py
```

**Search + analyze:**
```bash
rlm search "database" --paths-only
rlm ask src/db.py -q "How is connection pooling done?"
```

**Compare files:**
```bash
rlm ask old.py new.py -q "What changed?"
```

## Configuration

**Precedence:** CLI flags > env vars > config file > defaults

**Config locations:** `./rlm.yaml`, `./.rlm.yaml`, `~/.config/rlm/config.yaml`

```yaml
backend: openrouter
model: google/gemini-3-flash-preview
max_iterations: 30
```

**Environment variables:**
- `RLM_BACKEND` - Default backend
- `RLM_MODEL` - Default model
- `RLM_CONFIG` - Config file path
- `RLM_JSON=1` - Always output JSON

## Recursion and Budget Limits

### Recursive RLM (`--max-depth`)

Enable recursive `llm_query()` calls where child RLMs process sub-tasks:

```bash
# 2 levels of recursion
rlm ask . -q "Research thoroughly" --max-depth 2

# With budget cap
rlm ask . -q "Analyze codebase" --max-depth 3 --max-budget 0.50
```

### Budget Control (`--max-budget`)

Limit spending per completion. Raises `BudgetExceededError` when exceeded:

```bash
# Cap at $1.00
rlm complete "Complex task" --max-budget 1.00

# Very low budget (will likely exceed)
rlm ask . -q "Analyze everything" --max-budget 0.001
```

**Requirements:** OpenRouter backend (returns cost data in responses).

### Other Limits

**Timeout (`--max-timeout`)** - Stop after N seconds:
```bash
rlm complete "Complex task" --max-timeout 30
```

**Token limit (`--max-tokens`)** - Stop after N total tokens:
```bash
rlm ask . -q "Analyze" --max-tokens 10000
```

**Error threshold (`--max-errors`)** - Stop after N consecutive code errors:
```bash
rlm complete "Write code" --max-errors 3
```

### Stop Conditions

RLM execution stops when any of these occur:
1. **Final answer** - LLM calls `FINAL_VAR("variable_name")` with the NAME of a variable (as a string)
2. **Max iterations** - Exceeds `--max-iterations` (exit code 0, graceful - forces final answer)

**FINAL_VAR usage** (common mistake - pass variable NAME, not value):
```python
# CORRECT:
result = {"answer": "hello", "score": 42}
FINAL_VAR("result")  # pass the variable NAME as a string

# WRONG:
FINAL_VAR(result)  # passing the dict directly causes AttributeError
```
3. **Max budget exceeded** - Spending > `--max-budget` (exit code 20, error)
4. **Max timeout exceeded** - Time > `--max-timeout` (exit code 20, error with partial answer)
5. **Max tokens exceeded** - Tokens > `--max-tokens` (exit code 20, error with partial answer)
6. **Max errors exceeded** - Consecutive errors > `--max-errors` (exit code 20, error with partial answer)
7. **User cancellation** - Ctrl+C or SIGUSR1 (exit code 0, returns partial answer as success)
8. **Max depth reached** - Child RLM at depth 0 cannot recurse further

**Note on max iterations:** This is a soft limit. When exceeded, RLM prompts the LLM one more time to provide a final answer. Modern LLMs typically complete in 1-2 iterations.

**Partial answers:** When timeout, tokens, or errors stop execution, the error includes `partial_answer` if any response was generated before stopping.

**Early exit (Ctrl+C):** Pressing Ctrl+C (or sending SIGUSR1) returns the partial answer as success (exit code 0) with `early_exit: true` in the result.

### Inject File (--inject-file)

Update REPL variables mid-run by modifying an inject file:

```bash
# Create inject file
echo 'focus = "authentication"' > inject.py

# Run with inject file
rlm ask . -q "Analyze based on 'focus'" --inject-file inject.py

# In another terminal, update mid-run
echo 'focus = "authorization"' > inject.py
```

The file is checked before each iteration and executed if modified.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | CLI usage error |
| 10 | Input error (file not found) |
| 11 | Config error (missing API key) |
| 20 | Backend/API error (includes budget exceeded) |
| 30 | Runtime error |
| 40 | Index/search error |

## LLM Search Tools

When `rlm ask` runs on a directory, the LLM gets search tools:

| Tool | Cost | Privacy | Use For |
|------|------|---------|---------|
| `rg.search()` | Free | Local | Exact patterns, function names, imports |
| `tv.search()` | Free | Local | Topics, concepts, related files |
| `exa.search()` | **$** | **API** | Web search (requires `--exa` flag) |
| `pi.*` | **$$$** | **API** | Hierarchical PDF/document navigation |

### Free Local Tools (auto-loaded)

- **rg.search(pattern, paths, globs)** - ripgrep for exact patterns
- **tv.search(query, limit)** - Tantivy BM25 for concepts

### Exa Web Search (--exa flag, Costs Money)

⚠️ **Opt-in**: Requires `--exa` flag and `EXA_API_KEY` environment variable.

**Setup:**
```bash
export EXA_API_KEY=...  # Get from https://exa.ai
```

**Usage in REPL:**
```python
from rlm_cli.tools_search import exa, web

# Basic search
results = exa.search(query="Python async patterns", limit=5)
for r in results:
    print(f"{r['title']}: {r['url']}")

# With highlights (relevant excerpts)
results = exa.search(
    query="error handling best practices",
    limit=3,
    include_highlights=True
)

# Semantic alias
results = web(query="machine learning tutorial", limit=5)

# Find similar pages
results = exa.find_similar(url="https://example.com/article", limit=5)
```

**exa.search() parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `query` | required | Search query |
| `limit` | 10 | Max results |
| `search_type` | "auto" | "auto", "neural", or "keyword" |
| `include_domains` | None | Only these domains |
| `exclude_domains` | None | Exclude these domains |
| `include_text` | False | Include full page text |
| `include_highlights` | True | Include relevant excerpts |
| `category` | None | "company", "research paper", "news", etc. |

**When to use exa.search() / web():**
- Finding external documentation, tutorials, articles
- Researching topics beyond the local codebase
- Finding similar pages to a reference URL

### PageIndex (pi.* - Opt-in, Costs Money)

⚠️ **WARNING**: PageIndex sends document content to LLM APIs and costs money.

**Only use when:**
1. User explicitly requests document/PDF analysis
2. Document has hierarchical structure (reports, manuals)
3. User accepts cost/privacy tradeoffs

**Prerequisites:**
- `OPENROUTER_API_KEY` (or other backend key) must be set in environment
- PageIndex submodule must be initialized
- Run within rlm-cli's virtual environment (has required dependencies)

**Setup (REQUIRED before any pi.* operation):**
```python
import sys
sys.path.insert(0, "/path/to/rlm-cli/rlm")        # rlm submodule
sys.path.insert(0, "/path/to/rlm-cli/pageindex")  # pageindex submodule

from rlm.clients import get_client
from rlm_cli.tools_pageindex import pi

# Configure with existing rlm backend
client = get_client(backend="openrouter", backend_kwargs={"model_name": "google/gemini-2.0-flash-001"})
pi.configure(client)
```

**Indexing (costs $$$):**
```python
# Build tree index - THIS COSTS MONEY (no caching, re-indexes each call)
tree = pi.index(path="report.pdf")
# Returns: PITree object with doc_name, nodes, doc_description, raw
```

**Viewing structure (free after indexing):**
```python
# Display table of contents
print(pi.toc(tree))

# Get section by node_id (IDs are "0000", "0001", "0002", etc.)
section = pi.get_section(tree, "0003")
# Returns: PINode with title, node_id, start_index, end_index, summary, children
# Returns: None if not found

if section:
    print(f"{section.title}: pages {section.start_index}-{section.end_index}")
```

**Finding node IDs:**
Node IDs are assigned sequentially ("0000", "0001", ...) in tree traversal order.
To see all node IDs, access the raw tree structure:
```python
import json
print(json.dumps(tree.raw["structure"], indent=2))
# Each node has: title, node_id, start_index, end_index
```

**pi.* API Reference:**
| Method | Cost | Returns | Description |
|--------|------|---------|-------------|
| `pi.configure(client)` | Free | None | Set rlm backend (REQUIRED first) |
| `pi.status()` | Free | dict | Check availability, config, warning |
| `pi.index(path=str)` | $$$ | PITree | Build tree from PDF |
| `pi.toc(tree, max_depth=3)` | Free | str | Formatted table of contents |
| `pi.get_section(tree, node_id)` | Free | PINode or None | Get section by ID |
| `pi.available()` | Free | bool | Check if PageIndex installed |
| `pi.configured()` | Free | bool | Check if client configured |

**PITree attributes:** `doc_name`, `nodes` (list of PINode), `doc_description`, `raw` (dict)
**PINode attributes:** `title`, `node_id`, `start_index`, `end_index`, `summary` (may be None), `children` (may be None)

**Notes:**
- `summary` is only populated if `add_summaries=True` in `pi.index()`
- `children` is None for leaf nodes (sections with no subsections)
- `tree.raw["structure"]` is a flat list; hierarchy is in PINode.children
- PageIndex extracts document structure (TOC), not content. Use page numbers to locate sections in the original PDF.

**Example output from pi.toc():**
```
📄 annual_report.pdf

• Executive Summary (p.1-5)
• Financial Overview (p.6-20)
  • Revenue (p.6-10)
  • Expenses (p.11-15)
  • Projections (p.16-20)
• Risk Factors (p.21-35)
```
