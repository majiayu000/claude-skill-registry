# confluence-to-agent-knowledge-base

**Confluence to Agent Knowledge Base**

Turn any Confluence Cloud instance into a private, searchable AI knowledge base on GitHub.

A [Claude Code](https://claude.ai/download) skill that walks you through converting your company's Confluence spaces into a structured, LLM-powered knowledge base — with access-tiered repos so sensitive docs stay locked down.

## What It Does

```
Your Confluence ──► Private GitHub Repos ──► Searchable AI Knowledge Base
                    (access-tiered)          (search, Q&A, auto-sync)
```

**6-phase interactive walkthrough:**

1. **Discovery** — Finds your Confluence instance and lists all spaces (no API tokens needed)
2. **Access Tiers** — Groups spaces by who should see them (general, leadership, sales, etc.)
3. **Ingest** — Pulls all pages into clean markdown with metadata
4. **Compile** — Builds a categorized wiki with summaries and indexes
5. **GitHub** — Creates private repos per tier and pushes
6. **Auto-Sync** — Sets up weekly sync to keep the Knowledge Base current

## Install

```bash
claude skill add jpmim/confluence-to-agent-knowledge-base
```

Or manually:
```bash
git clone https://github.com/jpmim/confluence-to-agent-knowledge-base.git ~/.claude/skills/confluence-to-agent-knowledge-base
```

## Prerequisites

- [Claude Code](https://claude.ai/download) with Claude Pro or Max subscription
- [Atlassian MCP connector](https://claude.ai/settings) connected in Claude Code
- Python 3.9+
- Git with push access to your GitHub org

## Usage

In Claude Code, just say:

> "Set up a knowledge base from our Confluence"

Or:

> "Migrate our Confluence to a private GitHub knowledge base"

Claude will walk you through the entire process interactively.

## What You Get

For each access tier, you get a private GitHub repo containing:

```
your-company-kb/
  raw/              # Original Confluence pages as markdown
  wiki/             # Compiled knowledge base
    _index.md       # Master index
    _summaries.md   # One-line summaries of all pages
    operations/     # Categorized articles
    technical/
    onboarding/
    ...
  confluence_kb/    # Python CLI tool
  CLAUDE.md         # Agent instructions (so your AI agents can use the KB)
```

**CLI commands included:**
- `ckb search "query"` — Full-text search (no API key needed)
- `ckb query "question"` — LLM-powered Q&A with citations
- `ckb interactive` — Chat-style Q&A session
- `ckb compile --fast` — Recompile the wiki
- `ckb lint` — Health checks and quality audit
- `ckb status` — Show Knowledge Base stats

## Why Access Tiers?

Most companies have sensitive content in Confluence that shouldn't be visible to everyone:
- **Management** spaces with strategy, financials, board docs
- **Sales** spaces with pricing, contracts, client data
- **HR** spaces with compensation, performance reviews

This skill separates those into different private repos with different GitHub collaborator lists. Everyone gets the general Knowledge Base, but restricted content stays restricted.

## How It Works Under the Hood

- Uses the **Atlassian MCP connector** for all Confluence access — no API tokens to manage
- Converts pages to **markdown with YAML frontmatter** for maximum portability
- Compiles a **structured wiki** with categories, summaries, and indexes
- Includes a **TF-IDF search engine** for instant full-text search
- Sets up **weekly auto-sync** via Claude Code scheduled tasks
- Each repo includes **CLAUDE.md** so AI agents can read and contribute to the Knowledge Base

## Inspired By

[Karpathy's LLM Knowledge Base approach](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — raw data compiled by LLMs into a wiki that agents maintain and query.

## License

MIT
