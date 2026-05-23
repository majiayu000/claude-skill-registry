---
name: lancer
description: Use lancer CLI for LanceDB semantic and multi-modal search with document ingestion, vector embeddings, and MCP server integration for knowledge retrieval.
---
# Lancer - LanceDB CLI and MCP Server Skill

You are a specialist in using `lancer`, a CLI and MCP server for LanceDB that provides semantic and full-text search with multi-modal support (text and images). This skill provides comprehensive workflows, best practices, and common patterns for document ingestion, search, and table management.

## What is Lancer?

`lancer` is a powerful tool for:
- **Semantic search**: Find documents by meaning, not just keywords
- **Multi-modal support**: Index and search both text and images
- **LanceDB integration**: Efficient vector database storage and retrieval
- **Flexible ingestion**: Support for multiple file formats (txt, md, pdf, sql, images)
- **MCP server mode**: Integration with Claude Desktop and other MCP clients

## Core Capabilities

1. **Ingest**: Add documents to LanceDB with automatic chunking and embedding
2. **Search**: Semantic similarity search across documents
3. **Tables**: Manage LanceDB tables (list, info, delete)
4. **Remove**: Remove documents from tables
5. **MCP**: Run as Model Context Protocol server

## Quick Start

### Basic Search

```bash
# Search all tables
lancer search "how to deploy kubernetes"

# Search specific table with more results
lancer search -t docs -l 20 "authentication methods"

# Search with similarity threshold
lancer search --threshold 0.7 "error handling patterns"
```

### Basic Ingestion

```bash
# Ingest a single file
lancer ingest document.md

# Ingest a directory
lancer ingest ./docs/

# Ingest multiple paths
lancer ingest file1.md file2.pdf ./images/
```

## Document Ingestion

### Ingest Command Options

```bash
# Ingest to specific table
lancer ingest -t my_docs document.md

# Ingest with file extension filter
lancer ingest -e md,txt,pdf ./docs/

# Ingest from stdin (pipe file paths)
find ./docs -name "*.md" | lancer ingest --stdin

# Ingest from file list
lancer ingest --files-from paths.txt

# Custom chunk size and overlap
lancer ingest --chunk-size 2000 --chunk-overlap 400 document.md
```

### Supported File Types

**Text formats:**
- `txt` - Plain text files
- `md` - Markdown documents
- `pdf` - PDF documents
- `sql` - SQL scripts

**Image formats:**
- `jpg`, `jpeg` - JPEG images
- `png` - PNG images
- `gif` - GIF images
- `bmp` - Bitmap images
- `webp` - WebP images
- `tiff`, `tif` - TIFF images
- `svg` - SVG vector graphics
- `ico` - Icon files

### Embedding Models

**Text models:**
```bash
# Default: all-MiniLM-L6-v2 (fast, good quality)
lancer ingest document.md

# Larger model for better quality
lancer ingest --text-model all-MiniLM-L12-v2 document.md

# BGE models (better semantic understanding)
lancer ingest --text-model bge-small-en-v1.5 document.md
lancer ingest --text-model bge-base-en-v1.5 document.md
```

**Image models:**
```bash
# Default: clip-vit-b-32 (cross-modal text/image)
lancer ingest image.jpg

# ResNet50 for image-only search
lancer ingest --image-model resnet50 image.jpg
```

**Advanced: Force specific model:**
```bash
# Force CLIP for text (enables future image additions)
lancer ingest --embedding-model clip-vit-b-32 document.md

# Force BGE for performance (text-only)
lancer ingest --embedding-model BAAI/bge-small-en-v1.5 document.md
```

### Ingestion Optimization

```bash
# Filter by file size
lancer ingest --min-file-size 1000 --max-file-size 10000000 ./docs/

# Skip embedding generation (metadata only)
lancer ingest --no-embeddings document.md

# Custom batch size for database writes
lancer ingest --batch-size 200 ./large-dataset/

# JSON output for scripting
lancer ingest --format json document.md
```

## Search Operations

### Search Command Options

```bash
# Basic search
lancer search "kubernetes deployment"

# Search specific table
lancer search -t docs "authentication"

# Limit results
lancer search -l 5 "error handling"

# Set similarity threshold (0.0-1.0)
lancer search --threshold 0.6 "database migration"

# Include embeddings in results
lancer search --include-embeddings "API design"

# JSON output
lancer search --format json "machine learning"
```

### Metadata Filters

```bash
# Single filter (field:operator:value)
lancer search --filter "author:eq:John" "AI research"

# Multiple filters
lancer search \
  --filter "author:eq:John" \
  --filter "year:gt:2020" \
  "deep learning"

# Available operators:
# eq (equals), ne (not equals)
# gt (greater than), lt (less than)
# gte (greater/equal), lte (less/equal)
# in (in list), contains (string contains)
```

### Search Examples

```bash
# Find recent documentation
lancer search \
  -t docs \
  --filter "date:gte:2024-01-01" \
  -l 10 \
  "API endpoints"

# Search by category
lancer search \
  --filter "category:eq:tutorial" \
  "getting started"

# Multi-criteria search
lancer search \
  -t technical_docs \
  --filter "language:eq:python" \
  --filter "level:eq:advanced" \
  --threshold 0.7 \
  -l 15 \
  "async programming patterns"
```

## Table Management

### List Tables

```bash
# List all tables
lancer tables list

# JSON output
lancer tables list --format json
```

### Table Information

```bash
# Get table details
lancer tables info my_table

# JSON output for scripting
lancer tables info my_table --format json
```

### Delete Table

```bash
# Delete a table (be careful!)
lancer tables delete old_table
```

## Remove Documents

```bash
# Remove specific documents from a table
lancer remove -t docs document_id

# Remove multiple documents
lancer remove -t docs id1 id2 id3
```

## Configuration

### Using Config File

```bash
# Specify config file
lancer -c ~/.lancer/config.toml search "query"

# Set default table in config
lancer -c config.toml ingest document.md
```

### Environment Variables

```bash
# Set default table
export LANCER_TABLE=my_docs
lancer search "query"  # Searches my_docs

# Set log level
export LANCER_LOG_LEVEL=debug
lancer ingest document.md
```

### Log Levels

```bash
# Error only
lancer --log-level error search "query"

# Warning
lancer --log-level warn ingest document.md

# Info (default)
lancer --log-level info search "query"

# Debug
lancer --log-level debug ingest document.md

# Trace (verbose)
lancer --log-level trace search "query"
```

## Common Workflows

### Workflow 1: Index Documentation

```bash
# 1. Ingest markdown docs
lancer ingest -t docs -e md ./documentation/

# 2. Verify ingestion
lancer tables info docs

# 3. Test search
lancer search -t docs "installation guide"

# 4. Refine search with threshold
lancer search -t docs --threshold 0.7 -l 5 "configuration"
```

### Workflow 2: Multi-modal Image Search

```bash
# 1. Ingest images with CLIP model
lancer ingest -t images -e jpg,png,webp \
  --image-model clip-vit-b-32 \
  ./photos/

# 2. Search images with text query
lancer search -t images "sunset over mountains"

# 3. Search with higher threshold for precision
lancer search -t images --threshold 0.8 "red car"
```

### Workflow 3: Mixed Content Corpus

```bash
# 1. Ingest with CLIP for cross-modal search
lancer ingest -t knowledge_base \
  --embedding-model clip-vit-b-32 \
  -e md,pdf,jpg,png \
  ./content/

# 2. Search text and images together
lancer search -t knowledge_base "architecture diagrams"

# 3. Filter by file type
lancer search -t knowledge_base \
  --filter "file_type:eq:png" \
  "system design"
```

### Workflow 4: Batch Ingestion

```bash
# 1. Generate file list
find ./corpus -type f -name "*.md" > files.txt

# 2. Ingest from list with custom settings
lancer ingest -t corpus \
  --files-from files.txt \
  --chunk-size 1500 \
  --chunk-overlap 300 \
  --batch-size 150

# 3. Verify ingestion
lancer tables info corpus

# 4. Test search quality
lancer search -t corpus -l 10 "sample query"
```

### Workflow 5: Update Existing Corpus

```bash
# 1. Ingest new documents
lancer ingest -t docs ./new_docs/

# 2. Search to verify new content
lancer search -t docs "recent feature"

# 3. Remove outdated documents
lancer remove -t docs old_doc_id

# 4. Verify final state
lancer tables info docs
```

## Best Practices

### 1. Choose the Right Embedding Model

**For text-only corpora:**
```bash
# Fast and efficient
lancer ingest --text-model all-MiniLM-L6-v2 document.md

# Better quality
lancer ingest --text-model bge-base-en-v1.5 document.md
```

**For images or mixed content:**
```bash
# Cross-modal search (text queries → image results)
lancer ingest --embedding-model clip-vit-b-32 content/
```

### 2. Optimize Chunk Settings

**Short documents (< 500 words):**
```bash
lancer ingest --chunk-size 500 --chunk-overlap 100 article.md
```

**Long documents (> 2000 words):**
```bash
lancer ingest --chunk-size 2000 --chunk-overlap 400 book.pdf
```

**Code documentation:**
```bash
lancer ingest --chunk-size 1000 --chunk-overlap 200 docs/
```

### 3. Use Tables to Organize Content

```bash
# Separate tables by content type
lancer ingest -t api_docs ./api/*.md
lancer ingest -t tutorials ./tutorials/*.md
lancer ingest -t images ./screenshots/*.png

# Search specific context
lancer search -t api_docs "authentication endpoints"
```

### 4. Set Appropriate Thresholds

**Broad exploration:**
```bash
lancer search --threshold 0.4 "general topic"
```

**Precise matching:**
```bash
lancer search --threshold 0.75 "specific concept"
```

**Very high precision:**
```bash
lancer search --threshold 0.85 -l 3 "exact information"
```

### 5. Use Filters for Structured Data

```bash
# Combine semantic search with metadata
lancer search \
  --filter "status:eq:published" \
  --filter "category:eq:tutorial" \
  --threshold 0.6 \
  "getting started guide"
```

### 6. Format Output for Scripting

```bash
# JSON output for automation
lancer search --format json "query" | jq '.results[] | .path'

# List tables programmatically
lancer tables list --format json | jq '.[] | .name'
```

## MCP Server Mode

### Running as MCP Server

```bash
# Start MCP server for Claude Desktop integration
lancer mcp

# With custom config
lancer mcp -c ~/.lancer/config.toml

# With specific log level
lancer mcp --log-level info
```

### Integration with Claude Desktop

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lancer": {
      "command": "lancer",
      "args": ["mcp"]
    }
  }
}
```

## Performance Tips

### 1. Batch Operations

```bash
# Ingest multiple files at once
lancer ingest file1.md file2.md file3.md

# Use --stdin for large batches
find ./docs -name "*.md" | lancer ingest --stdin
```

### 2. Optimize Batch Size

```bash
# Larger batches for bulk ingestion
lancer ingest --batch-size 500 ./large-corpus/

# Smaller batches for limited memory
lancer ingest --batch-size 50 ./documents/
```

### 3. Skip Embeddings for Metadata-Only

```bash
# Index metadata without generating embeddings
lancer ingest --no-embeddings ./archive/
```

### 4. Use Appropriate Models

```bash
# Faster ingestion with smaller model
lancer ingest --text-model all-MiniLM-L6-v2 ./docs/

# Better quality with larger model (slower)
lancer ingest --text-model bge-base-en-v1.5 ./docs/
```

## Troubleshooting

### Issue: Search returns no results

**Solutions:**
```bash
# Lower the similarity threshold
lancer search --threshold 0.3 "query"

# Check table exists and has documents
lancer tables list
lancer tables info my_table

# Try different search terms
lancer search "alternative phrasing"
```

### Issue: Ingestion fails for some files

**Solutions:**
```bash
# Check supported extensions
lancer ingest -e md,txt,pdf ./docs/

# Set file size limits
lancer ingest --max-file-size 100000000 ./docs/

# Use debug logging
lancer --log-level debug ingest document.pdf
```

### Issue: Low search quality

**Solutions:**
```bash
# Use better embedding model
lancer ingest --text-model bge-base-en-v1.5 document.md

# Adjust chunk size
lancer ingest --chunk-size 1500 --chunk-overlap 300 document.md

# Adjust search threshold
lancer search --threshold 0.6 "query"
```

### Issue: Slow ingestion

**Solutions:**
```bash
# Increase batch size
lancer ingest --batch-size 300 ./docs/

# Use faster embedding model
lancer ingest --text-model all-MiniLM-L6-v2 ./docs/

# Skip embeddings if not needed
lancer ingest --no-embeddings ./docs/
```

## Quick Reference

```bash
# Ingestion
lancer ingest document.md                          # Ingest single file
lancer ingest -t docs ./directory/                 # Ingest to specific table
lancer ingest -e md,pdf ./docs/                    # Filter by extensions
lancer ingest --chunk-size 2000 document.md        # Custom chunk size

# Search
lancer search "query"                              # Search all tables
lancer search -t docs "query"                      # Search specific table
lancer search -l 20 "query"                        # Limit results
lancer search --threshold 0.7 "query"              # Set similarity threshold
lancer search --filter "author:eq:John" "query"    # Metadata filter

# Table management
lancer tables list                                 # List all tables
lancer tables info my_table                        # Table information
lancer tables delete old_table                     # Delete table

# Configuration
lancer -c config.toml search "query"               # Use config file
lancer --log-level debug ingest doc.md             # Set log level
export LANCER_TABLE=docs                           # Set default table

# MCP server
lancer mcp                                         # Start MCP server
```

## Common Patterns

### Pattern 1: Quick Documentation Search

```bash
lancer search -t docs --threshold 0.7 -l 5 "how to configure authentication"
```

### Pattern 2: Ingest and Test

```bash
lancer ingest -t test_docs document.md && \
lancer search -t test_docs "key concept from document"
```

### Pattern 3: Find Similar Images

```bash
lancer search -t images --threshold 0.8 "sunset landscape photography"
```

### Pattern 4: Batch Ingest with Verification

```bash
find ./docs -name "*.md" | lancer ingest -t docs --stdin && \
lancer tables info docs
```

### Pattern 5: Precise Technical Search

```bash
lancer search -t technical_docs \
  --filter "language:eq:rust" \
  --threshold 0.75 \
  -l 10 \
  "async trait implementation patterns"
```

## Summary

**Primary use cases:**
- Semantic search across documentation
- Multi-modal search (text and images)
- Knowledge base indexing and retrieval
- Integration with Claude via MCP

**Key advantages:**
- Semantic similarity (not just keyword matching)
- Multi-modal support (text and images)
- Flexible metadata filtering
- Multiple embedding model options
- Fast vector search with LanceDB

**Most common commands:**
- `lancer ingest document.md` - Index documents
- `lancer search "query"` - Search semantically
- `lancer tables list` - Manage tables
- `lancer search -t docs --threshold 0.7 "query"` - Precise search
