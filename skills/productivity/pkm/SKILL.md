---
name: pkm
description: Use pkm for personal knowledge management with temporal awareness, quality filtering, hybrid search, and relationship tracking with LSP and MCP server integration.
---
# PKM - Personal Knowledge Management Skill

You are a specialist in using `pkm`, a Personal Knowledge Management system that provides a knowledge layer between Claude Code (MCP) and lancer/LanceDB. PKM offers temporal awareness, quality filtering, token-efficient search, and document curation tools for managing workspace knowledge.

## What is PKM?

`pkm` is an advanced knowledge management system that provides:
- **Temporal awareness**: Track document freshness and identify stale content
- **Quality filtering**: Filter by certainty level and information type (facts, analysis, ideas)
- **Hybrid search**: Combines vector (semantic) and BM25 (full-text) search
- **Relationship tracking**: Document wikilinks, references, and backlinks
- **Quality audits**: Systematic review of knowledge base quality
- **LSP server**: Wikilink autocomplete in editors
- **MCP integration**: Claude Desktop integration for intelligent search

## Core Capabilities

1. **Index**: Index workspace documents (titles and/or content)
2. **Search**: Search with quality filters (certainty, info type, freshness)
3. **Relationships**: Track document relationships and wikilinks
4. **Backlinks**: Query what links to a document
5. **Quality Audit**: Review and improve knowledge base quality
6. **Stats**: Analyze indexed content statistics
7. **LSP/MCP**: Editor integration and Claude Desktop integration

## Quick Start

### Basic Search

```bash
# Search workspace documents
pkm search "kubernetes deployment strategies"

# Search with quality filters
pkm search --facts-only --fresh-only "API authentication"

# Search with result limit
pkm search -n 5 "error handling patterns"
```

### Basic Indexing

```bash
# Index current directory (both titles and content)
pkm index

# Index specific directory
pkm index ~/Documents/notes/

# Index specific files
pkm index note1.md note2.md
```

## Document Indexing

### Index Command Options

```bash
# Index both titles and content (default)
pkm index ./notes/

# Index only titles (LSP autocomplete)
pkm index --titles-only ./notes/

# Index only content (search)
pkm index --content-only ./notes/

# Index to specific table
pkm index --table my_knowledge ./notes/

# Index specific file extensions
pkm index --extensions md,txt,pdf ./documents/

# Force re-index
pkm index --force ./notes/
```

### Index from stdin

```bash
# Pipe file paths to index
find ~/Documents -name "*.md" -mtime -7 | pkm index --stdin

# From git changed files
git diff --name-only main | grep "\.md$" | pkm index --stdin
```

### Index Modes

**Hybrid index (default):**
```bash
# Vector + BM25 full-text search
pkm index ./notes/
```

**Vector-only index:**
```bash
# Skip BM25 (faster indexing, semantic search only)
pkm index --no-hybrid ./notes/
```

### Index Management

```bash
# Quiet mode (suppress progress)
pkm index --quiet ./large-corpus/

# Dry run (see what would be indexed)
pkm index --dry-run ./notes/

# Verbose logging
pkm index -v ./notes/
```

## Search Operations

### Search Command Options

```bash
# Basic search
pkm search "machine learning algorithms"

# Limit results
pkm search -n 10 "API design patterns"

# Set minimum score threshold
pkm search --min-score 0.1 "database optimization"

# Specify database path
pkm search --db-path ~/my-db "query"

# Specify workspace root
pkm search --workspace-root ~/Documents "query"

# Custom table name
pkm search --table-name custom_table "query"
```

### Quality Filters

**Filter by information type:**
```bash
# Show only facts
pkm search --info-type fact "kubernetes architecture"
pkm search --facts-only "docker commands"

# Show only analysis
pkm search --info-type analysis "performance bottlenecks"

# Show only ideas
pkm search --info-type idea "feature proposals"
```

**Filter by certainty:**
```bash
# High certainty only
pkm search --certainty high "security best practices"

# Medium certainty
pkm search --certainty medium "migration strategies"

# Low certainty (speculative)
pkm search --certainty low "future trends"
```

**Filter by freshness:**
```bash
# Maximum age in days
pkm search --max-age 30 "recent updates"

# Only fresh documents
pkm search --fresh-only "current status"

# Exclude stale documents
pkm search --exclude-stale "active projects"
```

### Combined Filters

```bash
# Facts from last 30 days
pkm search \
  --facts-only \
  --max-age 30 \
  "authentication implementation"

# High certainty analysis (fresh)
pkm search \
  --info-type analysis \
  --certainty high \
  --fresh-only \
  "performance optimization"

# Recent ideas with threshold
pkm search \
  --info-type idea \
  --max-age 14 \
  --min-score 0.15 \
  -n 5 \
  "feature enhancements"
```

### Output Formats

```bash
# Text output (default)
pkm search "query"

# JSON output for scripting
pkm search --output json "query" | jq '.results[] | .path'

# Verbose logging
pkm search -v "query"
```

## Relationship Tracking

### Query Outgoing Relationships

```bash
# Show all links from a document
pkm relationships --source notes/architecture.md

# Filter by relationship type
pkm relationships --source notes/api.md --rel-type wikilink

# JSON output
pkm relationships --source notes/design.md --output json
```

### Query Backlinks

```bash
# Show what links to a document
pkm backlinks notes/concepts/auth.md

# Filter by relationship type
pkm backlinks notes/api-spec.md --rel-type reference

# JSON output
pkm backlinks notes/design.md --output json
```

### Relationship Use Cases

```bash
# Find related documents
pkm relationships --source current-work.md

# Discover document impact
pkm backlinks important-concept.md

# Build knowledge graph
pkm relationships --source index.md --output json | \
  jq '.relationships[] | .target'

# Find orphaned documents (no backlinks)
pkm backlinks my-note.md | grep -q "No backlinks" && \
  echo "Orphaned document"
```

## Index a Single Document

```bash
# Index document for relationship tracking
pkm index-doc notes/new-concept.md

# With custom database
pkm index-doc --db-path ~/kb notes/article.md

# Verbose output
pkm index-doc -v notes/research.md
```

## Quality Management

### Quality Audit

```bash
# Audit entire workspace
pkm quality-audit

# Audit specific area/topic
pkm quality-audit --area kubernetes

# JSON output
pkm quality-audit --output json

# Verbose audit
pkm quality-audit -v
```

**What quality-audit checks:**
- Documents missing quality metadata
- Stale documents needing updates
- Low certainty information
- Missing or unclear info types
- Document completeness

### Find Stale Documents

```bash
# Find documents exceeding freshness threshold
pkm find-stale

# With workspace root
pkm find-stale --workspace-root ~/Documents/notes

# Verbose output
pkm find-stale -v
```

### Verification Queue

```bash
# Show documents needing review
pkm verify-queue

# With specific workspace
pkm verify-queue --workspace-root ~/kb

# Verbose output
pkm verify-queue -v
```

## Statistics and Analysis

### Workspace Statistics

```bash
# Show basic stats
pkm stats

# Detailed breakdown by file extension
pkm stats -d

# Detailed stats with custom database
pkm stats --db-path ~/my-kb -d

# JSON output
pkm stats --output json
```

**Stats include:**
- Total documents indexed
- Document counts by type
- Table information
- Embedding models used
- Index sizes

## Table Management

### List Tables

```bash
# List all tables in database
pkm tables

# With custom database path
pkm tables --db-path ~/my-kb

# Verbose output
pkm tables -v
```

## Server Modes

### LSP Server (Wikilink Autocomplete)

```bash
# Start LSP server for editor integration
pkm lsp

# With verbose logging
pkm lsp -v
```

**Purpose**: Provides wikilink autocomplete in editors (VSCode, Neovim, etc.)

### MCP Server (Claude Desktop)

```bash
# Start MCP server
pkm mcp

# With verbose logging
pkm mcp -v
```

**Purpose**: Integrates PKM search into Claude Desktop for intelligent document retrieval.

## Environment Variables

```bash
# Set default database path
export PKM_DB_PATH=~/my-knowledge-base
pkm search "query"

# Set workspace root
export PKM_ROOT=~/Documents/notes
pkm index

# Both together
export PKM_DB_PATH=~/kb
export PKM_ROOT=~/notes
pkm search "query"
```

## Common Workflows

### Workflow 1: Initial Workspace Setup

```bash
# 1. Index your workspace
cd ~/Documents/notes
pkm index

# 2. Check statistics
pkm stats -d

# 3. Test search
pkm search "recent projects"

# 4. Run quality audit
pkm quality-audit
```

### Workflow 2: Daily Knowledge Work

```bash
# 1. Find stale documents to review
pkm find-stale

# 2. Search for high-quality facts
pkm search --facts-only --certainty high "project status"

# 3. Index new/modified documents
find . -name "*.md" -mtime -1 | pkm index --stdin

# 4. Check relationships
pkm relationships --source today-notes.md
```

### Workflow 3: Research and Analysis

```bash
# 1. Search for recent analysis
pkm search \
  --info-type analysis \
  --max-age 30 \
  --certainty high \
  -n 20 \
  "performance optimization"

# 2. Find related documents
pkm relationships --source research-notes.md

# 3. Discover citations
pkm backlinks key-concept.md

# 4. Export for review
pkm search --output json "research topic" | \
  jq '.results[] | {path, score, summary}' > research.json
```

### Workflow 4: Knowledge Base Maintenance

```bash
# 1. Find documents needing review
pkm verify-queue

# 2. Run quality audit
pkm quality-audit --output json > audit-results.json

# 3. Find stale content
pkm find-stale

# 4. Re-index updated documents
pkm index --force ./updated-notes/

# 5. Verify improvements
pkm stats -d
```

### Workflow 5: Incremental Updates

```bash
# 1. Find recently modified files
find ~/notes -name "*.md" -mtime -7 > recent.txt

# 2. Index only recent changes
pkm index --stdin < recent.txt

# 3. Search fresh content
pkm search --max-age 7 "latest updates"

# 4. Update statistics
pkm stats -d
```

### Workflow 6: Integration with Git

```bash
# Index files changed in current branch
git diff --name-only main | \
  grep "\.md$" | \
  pkm index --stdin

# Index uncommitted changes
git diff --name-only | \
  grep "\.md$" | \
  pkm index --stdin

# Re-index entire repository
pkm index --force .
```

## Best Practices

### 1. Index Strategically

**Title indexing (fast, for autocomplete):**
```bash
pkm index --titles-only ~/notes/
```

**Content indexing (comprehensive, for search):**
```bash
pkm index --content-only ~/important-docs/
```

**Full indexing (both):**
```bash
pkm index ~/knowledge-base/
```

### 2. Use Quality Filters Effectively

**For verified information:**
```bash
pkm search --facts-only --certainty high "API endpoints"
```

**For recent insights:**
```bash
pkm search --info-type analysis --max-age 14 "optimization"
```

**For brainstorming:**
```bash
pkm search --info-type idea --exclude-stale "features"
```

### 3. Maintain Freshness

```bash
# Regular freshness check
pkm find-stale

# Periodic re-indexing
pkm index --force ./active-projects/

# Exclude stale from searches
pkm search --exclude-stale "current work"
```

### 4. Track Relationships

```bash
# After creating new note with wikilinks
pkm index-doc new-note.md
pkm relationships --source new-note.md

# Understand impact before editing
pkm backlinks important-concept.md
```

### 5. Regular Quality Audits

```bash
# Weekly audit
pkm quality-audit --output json > audit-$(date +%Y%m%d).json

# Area-specific review
pkm quality-audit --area architecture

# Track verification queue
pkm verify-queue
```

### 6. Organize with Extensions

```bash
# Index markdown notes
pkm index --extensions md ~/notes/

# Include PDFs and markdown
pkm index --extensions md,pdf ~/research/

# Text files only
pkm index --extensions txt ~/logs/
```

### 7. Use Appropriate Thresholds

**Broad exploration:**
```bash
pkm search --min-score 0.05 "general topic"
```

**Balanced results:**
```bash
pkm search --min-score 0.1 "specific concept"
```

**High precision:**
```bash
pkm search --min-score 0.2 "exact information"
```

## Integration Setups

### Claude Desktop (MCP)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pkm": {
      "command": "pkm",
      "args": ["mcp"],
      "env": {
        "PKM_ROOT": "/Users/username/Documents/notes",
        "PKM_DB_PATH": "/Users/username/.pkm/db"
      }
    }
  }
}
```

### VSCode (LSP)

1. Start LSP server: `pkm lsp`
2. Configure editor to connect to LSP endpoint
3. Get wikilink autocomplete in markdown files

## Advanced Usage

### Custom Database Locations

```bash
# Work with multiple knowledge bases
pkm search --db-path ~/work-kb "work queries"
pkm search --db-path ~/personal-kb "personal queries"

# Separate workspace and database
pkm index \
  --workspace-root ~/Documents/notes \
  --db-path ~/kb/notes-index
```

### Scripting and Automation

```bash
# Daily index automation
#!/bin/bash
cd ~/notes
find . -name "*.md" -mtime -1 | pkm index --quiet --stdin
pkm stats --output json > ~/stats/$(date +%Y%m%d).json

# Weekly quality report
#!/bin/bash
pkm quality-audit --output json > audit.json
pkm find-stale > stale.txt
pkm verify-queue > queue.txt
```

### Batch Processing

```bash
# Process multiple directories
for dir in ~/notes/*/; do
  echo "Indexing $dir"
  pkm index "$dir"
done

# Selective re-indexing
pkm stats --output json | \
  jq -r '.tables[] | select(.doc_count < 10) | .name' | \
  xargs -I {} pkm index --force --table {}
```

## Troubleshooting

### Issue: Search returns no results

**Solutions:**
```bash
# Check if content is indexed
pkm stats -d

# Lower score threshold
pkm search --min-score 0.01 "query"

# Remove quality filters
pkm search "query"  # No filters

# Verify database path
pkm search --db-path ~/kb -v "query"
```

### Issue: Stale documents not detected

**Solutions:**
```bash
# Force re-index
pkm index --force .

# Check verbose output
pkm find-stale -v

# Verify workspace root
pkm find-stale --workspace-root ~/notes
```

### Issue: Relationships not tracked

**Solutions:**
```bash
# Index document for relationships
pkm index-doc document.md

# Verbose indexing
pkm index-doc -v document.md

# Re-index entire workspace
pkm index --force .
```

### Issue: Poor search quality

**Solutions:**
```bash
# Enable hybrid search (vector + BM25)
pkm index .  # Default is hybrid

# Adjust filters
pkm search --min-score 0.05 "query"

# Check for sufficient indexed content
pkm stats -d
```

### Issue: LSP/MCP not working

**Solutions:**
```bash
# Verify server starts
pkm lsp -v
pkm mcp -v

# Check environment variables
echo $PKM_ROOT
echo $PKM_DB_PATH

# Restart server
pkill -f "pkm lsp"
pkm lsp -v
```

## Quick Reference

```bash
# Indexing
pkm index                                # Index current directory
pkm index ~/notes/                       # Index specific directory
pkm index --titles-only ~/notes/         # Titles only (LSP)
pkm index --force ~/notes/               # Force re-index
pkm index --extensions md,pdf ~/docs/    # Specific file types

# Searching
pkm search "query"                       # Basic search
pkm search -n 10 "query"                 # Limit results
pkm search --facts-only "query"          # Facts only
pkm search --fresh-only "query"          # Fresh only
pkm search --certainty high "query"      # High certainty
pkm search --max-age 30 "query"          # Last 30 days

# Relationships
pkm relationships --source note.md       # Show outgoing links
pkm backlinks note.md                    # Show incoming links
pkm index-doc note.md                    # Index for relationships

# Quality management
pkm quality-audit                        # Audit workspace
pkm find-stale                          # Find stale documents
pkm verify-queue                        # Documents needing review
pkm stats -d                            # Detailed statistics

# Servers
pkm mcp                                 # Start MCP server
pkm lsp                                 # Start LSP server

# Output formats
pkm search --output json "query"        # JSON output
pkm stats --output json                 # JSON stats
pkm quality-audit --output json         # JSON audit
```

## Common Patterns

### Pattern 1: Quick Fact Lookup

```bash
pkm search --facts-only --certainty high -n 5 "API authentication"
```

### Pattern 2: Recent Analysis

```bash
pkm search --info-type analysis --max-age 30 --fresh-only "optimization"
```

### Pattern 3: Explore Related Content

```bash
pkm relationships --source research.md && \
pkm backlinks research.md
```

### Pattern 4: Daily Maintenance

```bash
find . -name "*.md" -mtime -1 | pkm index --quiet --stdin && \
pkm find-stale
```

### Pattern 5: Quality-Focused Search

```bash
pkm search \
  --facts-only \
  --certainty high \
  --fresh-only \
  --min-score 0.15 \
  -n 10 \
  "deployment procedures"
```

## Summary

**Primary use cases:**
- Personal knowledge management with quality awareness
- Temporal tracking of document freshness
- Relationship discovery and backlink tracking
- Quality audits and knowledge base maintenance
- Integration with Claude via MCP

**Key advantages:**
- Quality filtering (certainty, info type)
- Freshness tracking (temporal awareness)
- Hybrid search (semantic + full-text)
- Relationship tracking (wikilinks, backlinks)
- Token-efficient results for Claude
- LSP integration for editor autocomplete

**Most common commands:**
- `pkm index ~/notes/` - Index workspace
- `pkm search --facts-only --fresh-only "query"` - Quality search
- `pkm relationships --source note.md` - Find relationships
- `pkm quality-audit` - Audit knowledge base
- `pkm stats -d` - Analyze workspace
