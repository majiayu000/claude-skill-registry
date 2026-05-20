---
name: rlama
description: Local RAG system management with RLAMA. Create semantic knowledge bases from local documents (PDF, MD, code, etc.), query them using natural language, and manage document lifecycles. This skill should be used when building local knowledge bases, searching personal documents, or performing document Q&A. Runs 100% locally with Ollama - no cloud, no data leaving your machine.
allowed-tools: Bash(rlama:*), Read
---

# RLAMA - Local RAG System

**RLAMA** (Retrieval-Augmented Language Model Adapter) provides fully local, offline RAG for semantic search over your documents.

## When to Use This Skill

- Building knowledge bases from local documents
- Searching personal notes, research papers, or code documentation
- Document-based Q&A without sending data to the cloud
- Indexing project documentation for quick semantic lookup
- Creating searchable archives of PDFs, markdown, or code files

## Prerequisites

RLAMA requires Ollama running locally:

```bash
# Verify Ollama is running
ollama list

# If not running, start it
brew services start ollama  # macOS
# or: ollama serve
```

## Quick Reference

### Query a RAG (Most Common)

Query an existing RAG system with a natural language question:

```bash
# Non-interactive query (returns answer and exits)
rlama run <rag-name> --query "your question here"

# With more context chunks for complex questions
rlama run <rag-name> --query "explain the authentication flow" --context-size 30

# Show which documents contributed to the answer
rlama run <rag-name> --query "what are the API endpoints?" --show-context

# Use a different model for answering
rlama run <rag-name> --query "summarize the architecture" -m deepseek-r1:8b
```

**Script wrapper** for cleaner output:

```bash
python3 ~/.claude/skills/rlama/scripts/rlama_query.py <rag-name> "your query"
python3 ~/.claude/skills/rlama/scripts/rlama_query.py my-docs "what is the main idea?" --show-sources
```

### Retrieve-Only Mode (Claude Synthesizes)

Get raw chunks without local LLM generation. Claude reads the chunks directly and synthesizes a stronger answer than local models can produce.

**When to use retrieve vs standard query:**

| Scenario | Use |
|----------|-----|
| Quick lookup, local model sufficient | `rlama_query.py` (standard) |
| Complex synthesis, nuanced reasoning | `rlama_retrieve.py` (retrieve-only) |
| Claude needs raw evidence to cite | `rlama_retrieve.py` (retrieve-only) |
| Offline/no Ollama for generation | `rlama_retrieve.py` (retrieve-only) |

```bash
# Retrieve top 10 chunks (human-readable)
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query"

# Retrieve as JSON for programmatic use
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --json

# More chunks for broad queries
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" -k 20

# Force rebuild embedding cache
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --rebuild-cache

# List RAGs with cache status
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py --list
```

**External LLM Synthesis** (optional—retrieve chunks AND synthesize via OpenRouter, TogetherAI, Ollama, or any OpenAI-compatible endpoint):

```bash
# Synthesize via OpenRouter (auto-detected from model with /)
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --synthesize --synth-model anthropic/claude-sonnet-4

# Synthesize via TogetherAI
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --synthesize --provider togetherai

# Synthesize via local Ollama (fully offline, uses research-grade system prompt)
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --synthesize --provider ollama

# Synthesize via custom endpoint
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py <rag-name> "your query" --synthesize --endpoint https://my-api.com/v1/chat/completions
```

**Environment variables for synthesis:**

| Variable | Provider |
|----------|----------|
| `OPENROUTER_API_KEY` | OpenRouter (default, auto-detected first) |
| `TOGETHER_API_KEY` | TogetherAI |
| `SYNTH_API_KEY` | Custom endpoint (via `--endpoint`) |
| *(none needed)* | Ollama (local, no auth) |

Provider auto-detection: model names with `/` → OpenRouter, otherwise → TogetherAI. Falls back to whichever API key is set.

**Quality tiers:**

| Tier | Method | Quality | Latency |
|------|--------|---------|---------|
| Best | Retrieve-only → Claude synthesizes | Strongest synthesis | ~1s retrieve |
| Good | `--synthesize --synth-model anthropic/claude-sonnet-4` | Strong, cited | ~3s |
| Decent | `--synthesize --provider togetherai` (Llama 70B) | Solid for factual | ~2s |
| Local | `--synthesize --provider ollama` (Qwen 7B) | Basic, may hedge | ~5s |
| Baseline | `rlama_query.py` (RLAMA built-in) | Weakest, no prompt control | ~3s |

Small local models (7B) use a tuned prompt optimized for Qwen (structured output, anti-hedge, domain-keyword aware). Cloud providers use a strict research-grade prompt with mandatory citations.

First run builds an embedding cache (~30s for 3K chunks, ~10min for 25K chunks). Subsequent queries are <1s. Large RAGs use incremental checkpointing—if Ollama crashes mid-build, re-run to resume from the last checkpoint. Individual chunks are truncated to 5K chars to stay within nomic-embed-text's context window.

**Benchmarking:**

```bash
# Retrieval quality only
python3 ~/.claude/skills/rlama/scripts/rlama_bench.py <rag-name> --retrieval-only

# Full synthesis benchmark (8 test cases)
python3 ~/.claude/skills/rlama/scripts/rlama_bench.py <rag-name> --provider ollama --verbose

# Single test case
python3 ~/.claude/skills/rlama/scripts/rlama_bench.py <rag-name> --provider ollama --case 0

# JSON output for analysis
python3 ~/.claude/skills/rlama/scripts/rlama_bench.py <rag-name> --provider ollama --json
```

Scores: retrieval precision, topic coverage, grounding, directness (anti-hedge), composite (0-100).

### Create a RAG

Index documents from a folder into a new RAG system:

```bash
# Basic creation (uses llama3.2 by default)
rlama rag llama3.2 <rag-name> <folder-path>

# Examples
rlama rag llama3.2 my-notes ~/Notes
rlama rag llama3.2 project-docs ./docs
rlama rag llama3.2 research-papers ~/Papers

# With exclusions
rlama rag llama3.2 codebase ./src --exclude-dir=node_modules,dist,.git --exclude-ext=.log,.tmp

# Only specific file types
rlama rag llama3.2 markdown-docs ./docs --process-ext=.md,.txt

# Custom chunking strategy
rlama rag llama3.2 my-rag ./docs --chunking=semantic --chunk-size=1500 --chunk-overlap=300
```

**Chunking strategies:**
- `hybrid` (default) - Combines semantic and fixed chunking
- `semantic` - Respects document structure (paragraphs, sections)
- `fixed` - Fixed character count chunks
- `hierarchical` - Preserves document hierarchy

### List RAG Systems

```bash
# List all RAGs
rlama list

# List documents in a specific RAG
rlama list-docs <rag-name>

# Inspect chunks (debugging)
rlama list-chunks <rag-name> --document=filename.pdf
```

### Manage Documents

**Add documents to existing RAG:**

```bash
rlama add-docs <rag-name> <folder-or-file>

# Examples
rlama add-docs my-notes ~/Notes/new-notes
rlama add-docs research ./papers/new-paper.pdf
```

**Remove a document:**

```bash
rlama remove-doc <rag-name> <document-id>

# Document ID is typically the filename
rlama remove-doc my-notes old-note.md
rlama remove-doc research outdated-paper.pdf

# Force remove without confirmation
rlama remove-doc my-notes old-note.md --force
```

### Delete a RAG

```bash
rlama delete <rag-name>

# Or manually remove the data directory
rm -rf ~/.rlama/<rag-name>
```

## Advanced Features

### Web Crawling

Create a RAG from website content:

```bash
# Crawl a website and create RAG
rlama crawl-rag llama3.2 docs-rag https://docs.example.com

# Add web content to existing RAG
rlama crawl-add-docs my-rag https://blog.example.com
```

### Directory Watching

Automatically update RAG when files change:

```bash
# Enable watching
rlama watch <rag-name> <folder-path>

# Check for new files manually
rlama check-watched <rag-name>

# Disable watching
rlama watch-off <rag-name>
```

### Website Watching

Monitor websites for content updates:

```bash
rlama web-watch <rag-name> https://docs.example.com
rlama check-web-watched <rag-name>
rlama web-watch-off <rag-name>
```

### Reranking

Improve result relevance with reranking:

```bash
# Add reranker to existing RAG
rlama add-reranker <rag-name>

# Configure reranker weight (0-1, default 0.7)
rlama update-reranker <rag-name> --reranker-weight=0.8

# Disable reranking
rlama rag llama3.2 my-rag ./docs --disable-reranker
```

### API Server

Run RLAMA as an API server for programmatic access:

```bash
# Start API server
rlama api --port 11249

# Query via API
curl -X POST http://localhost:11249/rag \
  -H "Content-Type: application/json" \
  -d '{
    "rag_name": "my-docs",
    "prompt": "What are the key points?",
    "context_size": 20
  }'
```

### Model Management

```bash
# Update the model used by a RAG
rlama update-model <rag-name> <new-model>

# Example: Switch to a more powerful model
rlama update-model my-rag deepseek-r1:8b

# Use Hugging Face models
rlama rag hf.co/username/repo my-rag ./docs
rlama rag hf.co/username/repo:Q4_K_M my-rag ./docs

# Use OpenAI models (requires OPENAI_API_KEY)
export OPENAI_API_KEY="your-key"
rlama rag gpt-4-turbo my-openai-rag ./docs
```

## Configuration

### Data Directory

By default, RLAMA stores data in `~/.rlama/`. Change this with `--data-dir`:

```bash
# Use custom data directory
rlama --data-dir=/path/to/custom list
rlama --data-dir=/projects/rag-data rag llama3.2 project-rag ./docs

# Or set via environment (add to ~/.zshrc)
export RLAMA_DATA_DIR="/path/to/custom"
```

### Ollama Configuration

```bash
# Custom Ollama host
rlama --host=192.168.1.100 --port=11434 run my-rag

# Or via environment
export OLLAMA_HOST="http://192.168.1.100:11434"
```

### Default Model

The skill uses `qwen2.5:7b` by default (changed from llama3.2 in Jan 2026). For legacy mode:

```bash
# Use the old llama3.2 default
python3 ~/.claude/skills/rlama/scripts/rlama_manage.py create my-rag ./docs --legacy

# Per-command model override
rlama rag deepseek-r1:8b my-rag ./docs

# For queries
rlama run my-rag --query "question" -m deepseek-r1:8b
```

**Recommended models:**
| Model | Size | Best For |
|-------|------|----------|
| `qwen2.5:7b` | 7B | Default - better reasoning (recommended) |
| `llama3.2` | 3B | Fast, legacy default (use `--legacy`) |
| `deepseek-r1:8b` | 8B | Complex questions |
| `llama3.3:70b` | 70B | Highest quality (slow) |

## Supported File Types

RLAMA indexes these formats:
- **Text**: `.txt`, `.md`, `.markdown`
- **Documents**: `.pdf`, `.docx`, `.doc`
- **Code**: `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.rb`, `.cpp`, `.c`, `.h`
- **Data**: `.json`, `.yaml`, `.yml`, `.csv`
- **Web**: `.html`, `.htm`
- **Org-mode**: `.org`

## Example Workflows

### Personal Knowledge Base

```bash
# Create from multiple folders
rlama rag llama3.2 personal-kb ~/Documents
rlama add-docs personal-kb ~/Notes
rlama add-docs personal-kb ~/Downloads/papers

# Query
rlama run personal-kb --query "what did I write about project management?"
```

### Code Documentation

```bash
# Index project docs
rlama rag llama3.2 project-docs ./docs ./README.md

# Query architecture
rlama run project-docs --query "how does authentication work?" --context-size 25
```

### Research Papers

```bash
# Create research RAG
rlama rag llama3.2 papers ~/Papers --exclude-ext=.bib

# Add specific paper
rlama add-docs papers ./new-paper.pdf

# Query with high context
rlama run papers --query "what methods are used for evaluation?" --context-size 30
```

### Interactive Wizard

For guided RAG creation:

```bash
rlama wizard
```

## Resilient Indexing (Skip Problem Files)

For folders with mixed content where some files may exceed embedding context limits (e.g., large PDFs), use the resilient script that processes files individually and skips failures:

```bash
# Create RAG, skipping files that fail
python3 ~/.claude/skills/rlama/scripts/rlama_resilient.py create my-rag ~/Documents

# Add to existing RAG, skipping failures
python3 ~/.claude/skills/rlama/scripts/rlama_resilient.py add my-rag ~/MoreDocs

# With docs-only filter
python3 ~/.claude/skills/rlama/scripts/rlama_resilient.py create research ~/Papers --docs-only

# With legacy model
python3 ~/.claude/skills/rlama/scripts/rlama_resilient.py create my-rag ~/Docs --legacy
```

The script reports which files were added and which were skipped due to errors.

## Progress Monitoring

Monitor long-running RLAMA operations in real-time using the logging system.

### Tail the Log File

```bash
# Watch all operations in real-time
tail -f ~/.rlama/logs/rlama.log

# Filter by RAG name
tail -f ~/.rlama/logs/rlama.log | grep my-rag

# Pretty-print with jq
tail -f ~/.rlama/logs/rlama.log | jq -r '"\(.ts) [\(.cat)] \(.msg)"'

# Show only progress updates
tail -f ~/.rlama/logs/rlama.log | jq -r 'select(.data.i) | "\(.ts) [\(.cat)] \(.data.i)/\(.data.total) \(.data.file // .data.status)"'
```

### Check Operation Status

```bash
# Show active operations
python3 ~/.claude/skills/rlama/scripts/rlama_status.py

# Show recent completed operations
python3 ~/.claude/skills/rlama/scripts/rlama_status.py --recent

# Show both active and recent
python3 ~/.claude/skills/rlama/scripts/rlama_status.py --all

# Follow mode (formatted tail -f)
python3 ~/.claude/skills/rlama/scripts/rlama_status.py --follow

# JSON output
python3 ~/.claude/skills/rlama/scripts/rlama_status.py --json
```

### Log File Format

Logs are written in JSON Lines format to `~/.rlama/logs/rlama.log`:

```json
{"ts": "2026-02-03T12:34:56.789", "level": "info", "cat": "INGEST", "msg": "Progress 45/100", "data": {"op_id": "ingest_abc123", "i": 45, "total": 100, "file": "doc.pdf", "eta_sec": 85}}
```

### Operations State

Active and recent operations are tracked in `~/.rlama/logs/operations.json`:

```json
{
  "active": {
    "ingest_abc123": {
      "type": "ingest",
      "rag_name": "my-docs",
      "started": "2026-02-03T12:30:00",
      "processed": 45,
      "total": 100,
      "eta_sec": 85
    }
  },
  "recent": [...]
}
```

## Troubleshooting

### "Ollama not found"

```bash
# Check Ollama status
ollama --version
ollama list

# Start Ollama
brew services start ollama  # macOS
ollama serve                # Manual start
```

### "Model not found"

```bash
# Pull the required model
ollama pull llama3.2
ollama pull nomic-embed-text  # Embedding model
```

### Slow Indexing

- Use smaller embedding models
- Exclude large binary files: `--exclude-ext=.bin,.zip,.tar`
- Exclude build directories: `--exclude-dir=node_modules,dist,build`

### Poor Query Results

1. Increase context size: `--context-size=30`
2. Use a better model: `-m deepseek-r1:8b`
3. Re-index with semantic chunking: `--chunking=semantic`
4. Enable reranking: `rlama add-reranker <rag-name>`

### Index Corruption

```bash
# Delete and recreate
rm -rf ~/.rlama/<rag-name>
rlama rag llama3.2 <rag-name> <folder-path>
```

## CLI Reference

Full command reference available at:

```bash
rlama --help
rlama <command> --help
```

Or see `references/rlama-commands.md` for complete documentation.
