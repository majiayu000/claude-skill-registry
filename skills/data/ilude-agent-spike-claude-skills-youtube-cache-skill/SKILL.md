---
name: youtube-cache
description: YouTube video cache operations with Qdrant. Auto-checks cache when YouTube URLs detected. Provides semantic search, verification, ingestion, and archive access. Shows metadata by default, transcript on request.
---

# YouTube Cache Operations

**Activation triggers:**
- YouTube URLs in conversation (`youtube.com/watch?v=...`, `youtu.be/...`)
- Mentions: "youtube", "video", "cache", "qdrant", "transcript"
- Working with `compose/cli/` or `compose/services/` directories

**Token efficiency:**
- Upfront: ~50 tokens (just YAML description)
- On activation: ~2-3k tokens (this full document)
- Compare to MCP: 5-10k tokens loaded immediately

## Core Principles

1. **Auto-check YouTube URLs** - When user pastes URL, immediately verify cache status
2. **Metadata-first display** - Show title, summary, tags by default (NOT full transcript)
3. **Archive-aware** - Check both Qdrant cache and archive for historical data
4. **Leverage existing scripts** - All operations use tested `compose/cli/*` commands

## Quick Commands

### Auto-Check (Automatic on URL Detection)

When user pastes a YouTube URL, automatically run:

```bash
uv run python compose/cli/verify_video.py VIDEO_ID
```

**Display format (metadata only):**
```
Video ID: {video_id}
URL: {url}
Title: {title}
Summary: {summary[:100]}...
Subject: {subject_matter[:3]}
Style: {content_style}
Transcript: {length:,} characters
```

**If not cached:**
```
[INFO] Video not found in cache.

To ingest:
uv run python compose/cli/ingest_video.py "URL"
```

### Search Videos (Semantic)

For natural language queries:

```bash
uv run python compose/cli/search_videos.py "query text" --limit 10
```

**Examples:**
```bash
# Find videos about MCP
uv run python compose/cli/search_videos.py "MCP protocol" --limit 5

# Python tutorials
uv run python compose/cli/search_videos.py "python async programming"

# Custom collection
uv run python compose/cli/search_videos.py "agents" --collection test_basic
```

**Output:** Relevance scores + metadata (no transcript unless requested)

### List All Cached Videos

```bash
# Default collection (cached_content)
uv run python compose/cli/list_videos.py

# Custom collection
uv run python compose/cli/list_videos.py my_collection

# Limit results
uv run python compose/cli/list_videos.py cached_content 20
```

### Ingest New Video

**Single video (recommended):**
```bash
uv run python compose/cli/ingest_video.py "https://youtube.com/watch?v=VIDEO_ID"
```

**Batch/REPL mode:**
```bash
make ingest
# Or: uv run python compose/cli/ingest_youtube.py
```

**What happens:**
1. Fetch transcript (via Webshare proxy if configured)
2. Archive transcript immediately → `projects/data/archive/youtube/YYYY-MM/`
3. Generate metadata with Claude Haiku (title, summary, tags)
4. Archive LLM output
5. Cache in Qdrant with embeddings

**Features:**
- Dry run: `--dry-run` flag
- Custom collection: Add collection name as second arg
- Archive-first: All expensive data saved before processing

### Delete from Cache

```bash
# Delete with confirmation prompt (safe)
uv run python compose/cli/delete_video.py VIDEO_ID

# Custom collection
uv run python compose/cli/delete_video.py VIDEO_ID --collection my_collection

# Skip confirmation (use with caution!)
uv run python compose/cli/delete_video.py VIDEO_ID --yes
```

**Note:** Only deletes from Qdrant cache, NOT from archive. Always prompts for confirmation unless `--yes` flag is used.

## Advanced Operations

### Search by Reference/Entity

Filter videos mentioning specific people, companies, or concepts:

```bash
uv run python compose/cli/search_by_reference.py "entity_name"

# Examples
uv run python compose/cli/search_by_reference.py "Anthropic"
uv run python compose/cli/search_by_reference.py "MCP"
```

### Archive Access

**Location:** `projects/data/archive/youtube/YYYY-MM/VIDEO_ID.json`

**Structure:**
```json
{
  "video_id": "...",
  "url": "...",
  "fetched_at": "...",
  "raw_transcript": "...",
  "llm_outputs": [...],
  "processing_history": [...]
}
```

**Reading archive:**
```python
from compose.services.archive import create_local_archive_reader

archive = create_local_archive_reader()
video_data = archive.get("VIDEO_ID")
```

**Reingest from archive:**
```bash
uv run python compose/cli/reingest_from_archive.py VIDEO_ID
```

### Batch Processing

**Fetch channel videos to CSV:**
```bash
uv run python compose/cli/fetch_channel_videos.py "@channel_handle"
uv run python compose/cli/fetch_channel_videos.py "@channel_handle" output.csv
```

**Requires:** `YOUTUBE_API_KEY` in `.env`

**Then ingest CSV:**
```bash
make ingest
# Select CSV file when prompted
```

### Collection Management

**Default collection:** `cached_content`

**Custom collections:** Pass as argument to most scripts

**Check what's in a collection:**
```bash
uv run python compose/cli/list_videos.py my_collection
```

**No auto-discovery:** Must specify collection name explicitly.

## Usage Examples

### Example 1: User Pastes YouTube URL

**User:** "Check this out: https://www.youtube.com/watch?v=1_z3h2r93OY"

**Auto-action:**
```bash
uv run python compose/cli/verify_video.py 1_z3h2r93OY
```

**Response:**
```
Video ID: 1_z3h2r93OY
URL: https://www.youtube.com/watch?v=1_z3h2r93OY
Title: MCP token waste and the solution: skills and code execution
Summary: A breakdown of MCP's token inefficiency and context-rot, and how Anthropic's Claude Skills...
Subject: MCP protocol and token inefficiency, context window and context rot, real-time discovery...
Style: demonstration
Transcript: 11,460 characters

[FOUND] Video is cached in Qdrant.
```

### Example 2: Search for Related Content

**User:** "Do we have other videos about MCP servers?"

**Action:**
```bash
uv run python compose/cli/search_videos.py "MCP servers" --limit 5
```

**Response:**
```
Found 5 results:

1. OIKTsVjTVJE (relevance: 0.575)
   Title: MCP server implementation guide
   Summary: Building MCP servers with practical examples...

2. D92aDGVFcRE (relevance: 0.488)
   Title: Seven MCP architecture failure modes
   ...
```

### Example 3: Ingest New Video

**User:** "Can you ingest https://youtube.com/watch?v=ABC123 into the cache?"

**Action:**
```bash
uv run python compose/cli/ingest_video.py "https://youtube.com/watch?v=ABC123"
```

**Response:**
```
[1/5] Checking cache...
[2/5] Fetching transcript...
[3/5] Archiving transcript...
[4/5] Generating metadata...
[5/5] Caching in Qdrant...

SUCCESS! Video cached.
```

### Example 4: Video Not Cached

**User:** "https://youtube.com/watch?v=XYZ789"

**Auto-check result:**
```
[INFO] Video XYZ789 not found in cache.

To ingest this video:
uv run python compose/cli/ingest_video.py "https://youtube.com/watch?v=XYZ789"

Would you like me to ingest it now?
```

## Metadata Structure

**Full metadata format (from LLM tagging):**

```python
{
    "video_id": str,
    "url": str,
    "transcript": str,           # Full transcript text
    "transcript_length": int,    # Character count
    "metadata": {
        "title": str,
        "summary": str,          # 1-2 sentence overview
        "subject_matter": list[str],  # Main topics (3-6 items)
        "content_style": str,    # tutorial | demonstration | lecture | discussion
        "difficulty": str,       # beginner | intermediate | advanced
        "entities": {
            "named_things": list[str],
            "people": list[str],
            "companies": list[str]
        },
        "techniques_or_concepts": list[str],
        "tools_or_materials": list[str],
        "key_points": list[str],
        "references": list[{
            "type": str,
            "name": str,
            "url": str | None,
            "description": str
        }]
    }
}
```

## Important Patterns

### 1. Archive-First Philosophy

**ALWAYS archive before processing:**
1. Fetch transcript → Archive immediately
2. Generate LLM output → Archive immediately
3. Process/embed/cache → Derived data (can be rebuilt)

**Why:** Protects against data loss, enables reprocessing, tracks costs.

### 2. Transcript Display Rules

**Default:** Show metadata only (title, summary, subject, style, length)

**Never show full transcript unless explicitly requested:**
- Transcripts are 10k-50k+ characters
- Floods context window
- User can request: "show me the transcript for VIDEO_ID"

**If user requests transcript:**
```bash
uv run python compose/cli/verify_video.py VIDEO_ID
# Then show full transcript field from output
```

### 3. URL Format Support

All formats supported:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- Just `VIDEO_ID` for verify/delete operations

### 4. Collection Defaults

- **Default collection:** `cached_content`
- **Override:** Pass `--collection NAME` or as positional arg
- **No validation:** Script will create collection if doesn't exist

### 5. Error Handling

**Video not found:**
```
[INFO] Video not found in cache.
```
→ Suggest ingestion command

**Transcript unavailable:**
```
[ERROR] Could not fetch transcript (disabled, private, etc.)
```
→ Cannot ingest, inform user

**Already cached:**
```
[INFO] Video already cached, skipping.
```
→ Use verify to show metadata

## Environment Requirements

**Required in `.env` (root directory):**
```bash
ANTHROPIC_API_KEY=sk-ant-...     # For metadata generation
OPENAI_API_KEY=sk-proj-...       # For embeddings (sentence-transformers)
```

**Optional:**
```bash
WEBSHARE_PROXY_USERNAME=...      # For YouTube rate limit bypass
WEBSHARE_PROXY_PASSWORD=...
YOUTUBE_API_KEY=...              # For fetch_channel_videos.py
```

**Data paths (auto-created):**
- Qdrant: `projects/data/qdrant/`
- Archive: `projects/data/archive/youtube/YYYY-MM/`

## Service Layer Reference

**If direct Python imports needed:**

```python
# Cache operations
from compose.services.cache import create_qdrant_cache

cache = create_qdrant_cache(collection_name="cached_content")
results = cache.search("query", limit=10)
exists = cache.exists("youtube:video:VIDEO_ID")
cache.close()

# Archive operations
from compose.services.archive import create_local_archive_reader

archive = create_local_archive_reader()
video = archive.get("VIDEO_ID")

# YouTube operations
from compose.services.youtube import extract_video_id, get_transcript

video_id = extract_video_id("https://youtube.com/watch?v=...")
transcript = await get_transcript(video_id)
```

## Script Design Philosophy

**From compose/cli/README.md:**

Scripts should:
1. **Build on services** - Use `compose.services.*` for business logic
2. **CLI-focused** - User-friendly command-line interfaces
3. **Self-contained** - Run directly or via make targets
4. **Well-documented** - Clear help text and examples
5. **Error handling** - Graceful exits and helpful messages

This skill wraps these scripts to provide Claude Code with the same capabilities in a token-efficient, context-aware manner.

## Future Enhancements (Phase 2)

**Not implemented yet, but potential additions:**
- Direct service imports (skip bash wrapper for speed)
- Batch operation helpers (process multiple URLs)
- Collection discovery and auto-switching
- Cost tracking from archive metadata
- Duplicate detection before ingestion
- Smart excerpt showing (relevant transcript sections based on query)

**Design philosophy:** Start simple, add features only when real pain points emerge.

---

**Token efficiency achieved:** This skill provides full YouTube cache access with ~50 tokens upfront, loading full documentation only when needed. Compare to MCP server approach which would load 5-10k tokens immediately for similar functionality.
