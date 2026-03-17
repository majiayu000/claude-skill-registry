---
name: search
description: Semantic search across GTM knowledge base using qmd - find context by meaning, not just keywords
---

# Search

Semantic search across your GTM workspace. Find decisions, context, and knowledge by meaning.

Uses [qmd](https://github.com/tobi/qmd) - local hybrid search combining BM25 keywords, vector embeddings, and LLM reranking.

## Usage

```
/search "what did we decide about pricing"
/search "authentication flow"
/search --keyword "API"           # Fast keyword-only
/search --semantic "how to deploy" # Vector-only
```

## Setup

**New workspaces:** Search is set up automatically during `jfl init` if you choose to enable it.

**Existing workspaces:** Follow the manual setup below.

## On Skill Invoke

### Step 1: Check if qmd is installed

```bash
which qmd
```

**If not installed:**

```
qmd not found. It's a local search engine for your markdown files.

Install it?

  bun install -g https://github.com/tobi/qmd

[Yes] [No]
```

If yes, run:
```bash
bun install -g https://github.com/tobi/qmd
```

### Step 2: Check if GTM is indexed

```bash
qmd status
```

Look for a collection that matches this workspace (check `.jfl/config.json` for the collection name).

**If no collection exists, guide setup:**

```
This GTM workspace isn't indexed yet.

To set up search, run these commands:

  # Add the workspace as a collection
  qmd collection add . --name <project-name>

  # Add context to help search understand the content
  qmd context add qmd://<project-name> "GTM workspace: vision, narrative, specs, content, and decisions"
  qmd context add qmd://<project-name>/knowledge "Strategic docs: vision, thesis, roadmap, brand"
  qmd context add qmd://<project-name>/content "Marketing content: articles, threads, posts"

  # Generate embeddings (takes a minute, downloads ~1.5GB of models first time)
  qmd embed

After running these, try /search again.
```

**Note:** These commands are run automatically during `jfl init` if search is enabled. Only run manually for existing workspaces.

### Step 3: Run the search

**Default (hybrid with reranking - best quality):**
```bash
qmd query "USER_QUERY" -n 10
```

**Keyword-only (fast):**
```bash
qmd search "USER_QUERY" -n 10
```

**Semantic-only:**
```bash
qmd vsearch "USER_QUERY" -n 10
```

### Step 4: Present results

Show results with:
- File path (relative to workspace)
- Score (percentage)
- Snippet with context

```
Found 5 results for "pricing":

knowledge/PRODUCT_SPEC_V2.md (87%)
  "The day pass model: $5/day per person. Only pay days you use it..."

knowledge/THESIS.md (72%)
  "Before: $355k/year (tools + coordination headcount). After: $240/year..."

content/articles/YOU_SHOULD_BE_WORKING_ON_CONTEXT.md (58%)
  "The entire SaaS economy is a $300B/year patch..."
```

If user wants full content, use:
```bash
qmd get "FILE_PATH" --full
```

---

## Search Modes

| Mode | Command | Use When |
|------|---------|----------|
| **Hybrid** | `qmd query` | Best quality, default |
| **Keyword** | `qmd search` | Fast, exact matches |
| **Semantic** | `qmd vsearch` | Conceptual similarity |

---

## Keeping Index Fresh

When files change, the index needs updating:

```bash
# Re-index all collections
qmd update

# Re-index and pull git changes first
qmd update --pull

# Re-generate embeddings (after significant changes)
qmd embed
```

**Do not run these automatically.** Mention to user if results seem stale.

---

## Advanced Options

```bash
# Filter by collection
qmd query "API design" -c knowledge

# Minimum score threshold
qmd query "authentication" --min-score 0.5

# All results above threshold
qmd query "error handling" --all --min-score 0.3

# JSON output for processing
qmd query "deployment" --json

# Get full document content
qmd get "knowledge/VISION.md" --full
```

---

## MCP Server (Optional)

For deeper integration, qmd can run as an MCP server so Claude has it as a native tool.

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Then Claude can use `qmd_search`, `qmd_vsearch`, `qmd_query`, `qmd_get` directly without invoking the skill.

---

## What Gets Indexed

Default glob pattern indexes all markdown files:
- `knowledge/` - vision, narrative, thesis, brand, specs
- `content/` - articles, threads, posts
- `product/` - product specs, decisions
- `suggestions/` - contributor work
- `drafts/` - work in progress

Customize with `--mask` when adding collection:
```bash
qmd collection add . --name gtm --mask "**/*.md"
```

---

## Why Local Search

- **Private** - everything stays on your machine
- **Semantic** - finds related concepts, not just keywords
- **Fast** - SQLite + local models, no API calls
- **Context-aware** - understands your knowledge base structure

The context layer becomes searchable. Decisions don't get lost.
