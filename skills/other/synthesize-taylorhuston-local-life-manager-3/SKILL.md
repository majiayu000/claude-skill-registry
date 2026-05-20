---
name: synthesize
description: Synthesize information across multiple sources into a structured document. Processes sources in batches across sessions to handle more data than fits in context. Discovers and queues related sources automatically. Use for research synthesis, topic deep-dives, or consolidating scattered notes. Triggers on "synthesize", "synthesis", "research [topic]".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch
---

Create and incrementally build synthesis documents from multiple sources.

## Output Location

All synthesis documents go in: `my-vault/06 Knowledge Base/Synthesis/[Topic]/`

Structure:
```
my-vault/06 Knowledge Base/Synthesis/
└── ADHD/
    ├── ADHD Synthesis.md              # Main synthesis
    ├── ADHD Sources.md                # Sources table + processing log
    └── ADHD Medications Synthesis.md  # Sub-topic (if created)
```

## Queue Files

Queues live in: `.claude/skills/synthesize/references/queues/[topic].json`

```json
{
  "name": "ADHD",
  "topic_folder": "ADHD",
  "batch_size": 3,
  "max_discovered_per_source": 3,
  "watch_patterns": [
    "my-vault/06 Knowledge Base/Capture/Videos/**/*ADHD*.md",
    "my-vault/01 Inbox/*adhd*.md",
    "my-vault/04 Personal/Health/*ADHD*.md"
  ],
  "sources": [
    {"path": "my-vault/path/to/note.md", "status": "pending", "type": "local"},
    {"path": "my-vault/path/to/video.md", "status": "processed", "type": "local"},
    {"url": "https://example.com/study", "status": "pending", "type": "web",
     "discovered_from": "src-2", "context": "Key study on medication timing"},
    {"search": "Barkley 2023 executive function", "status": "pending", "type": "search",
     "discovered_from": "src-2", "context": "Referenced as foundational research"}
  ],
  "last_run": "2026-01-14T10:00:00Z"
}
```

**Source types:**
- `local` - Path to existing note in my-vault
- `web` - URL to fetch and process
- `search` - Search query to find the source (use WebSearch, then fetch best result)

**Source status values:** `pending`, `processed`, `skipped`

**watch_patterns:** Glob patterns for `/synthesize update` to scan. Paths matching these patterns get added to the queue automatically (if not already present).

## Commands

- `/synthesize [topic]` - Continue processing the named synthesis
- `/synthesize list` - Show all active synthesis queues and progress
- `/synthesize new [topic]` - Create a new synthesis queue
- `/synthesize add [topic] [path-or-glob]` - Add sources to a queue
- `/synthesize update [topic]` - Scan watch_patterns for new sources and add to queue

## Architecture

This skill uses a **coordinator + subagent** pattern for efficient processing:
- **Coordinator (Sonnet/Opus)**: Manages state, spawns extractors, merges findings into synthesis
- **Extractors (Haiku subagents)**: Each reads one source, extracts structured findings in parallel

This allows processing 6-10 sources per batch instead of 2-3, with ~3x throughput improvement.

## Workflow

### Starting a Session

1. Load queue file for the topic
2. Read the main synthesis doc (or create from template if first run)
3. Read the sources file
4. Identify next N pending sources (N = 6-10 for parallel extraction)

### Phase 1: Parallel Extraction (Haiku Subagents)

Spawn 6-10 Haiku extractors in parallel using the Task tool:

```
Task tool call:
- model: haiku
- subagent_type: general-purpose
- prompt: (see Extractor Prompt Template below)
```

**Extractor Prompt Template:**
```
Read this file and extract [TOPIC]-relevant findings in a structured format.

FILE: [full path to source]

Return your findings as a simple list in this format:
CATEGORY: [Category Name]
- Finding 1 (be specific, include numbers/names if mentioned)
- Finding 2
...

Only include substantive findings relevant to understanding [TOPIC].
Skip metadata, timestamps, and filler.
If the source has little new information, just return "MINIMAL_CONTENT".
```

**For `web` sources**, modify prompt to use WebFetch first:
```
1. Use WebFetch to retrieve: [URL]
2. Extract [TOPIC]-relevant findings from the content...
```

**For `search` sources**, modify prompt to search first:
```
1. Use WebSearch to find: [search query]
2. Use WebFetch on the best result
3. Extract [TOPIC]-relevant findings...
```

### Phase 2: Merge Findings (Coordinator)

Once all extractors return:

1. Collect all extraction results
2. Review for:
   - New findings to add to existing categories
   - Findings that warrant new categories
   - Contradictions with existing content → add to Open Questions
   - Dense categories → add to Suggested Sub-Topics
3. Update synthesis doc with citations (^[src-N])
4. Add sources to Sources table
5. Mark sources as `processed` in queue

### Phase 3: Discovery (Coordinator)

While reviewing extractions, watch for references worth following up:
- Studies or papers cited
- Articles or books mentioned
- Other videos or talks referenced
- Experts or researchers named

**Limit: 3 discovered sources per source processed.**

### Discovery

While processing each source, watch for references worth following up:
- Studies or papers cited
- Articles or books mentioned
- Other videos or talks referenced
- Experts or researchers named (for potential lookup)

**Limit: 3 discovered sources per source processed.**

For each valuable reference:
1. Check if already in queue (deduplicate by URL, title, or path)
2. Add to queue with:
   - `type`: `web` if URL available, `search` if just a name/title
   - `discovered_from`: source ID where you found it
   - `context`: why it's relevant (1 sentence)
   - `status`: `pending`

Prioritize discoveries that:
- Are directly cited as evidence for claims
- Come from credible sources (peer-reviewed, recognized experts)
- Fill gaps in the current synthesis

Skip discovering:
- Tangential references not central to the topic
- Sources that would require paid access (note in processing log if significant)
- Generic resources (e.g., "see Wikipedia for more")

### Ending a Session

1. Write updated synthesis doc
2. Write updated sources file
3. Write updated queue file with new `last_run` timestamp
4. Add entry to Processing Log (include discovery count)
5. Report:
   ```
   Processed X items. Discovered Y new sources.
   Z items remaining. Run `/synthesize [topic]` to continue.
   ```

If all sources processed:
```
Synthesis complete. X total sources processed.
Review Suggested Sub-Topics for potential expansion.
```

### Updating a Synthesis (`/synthesize update [topic]`)

Use this to find new sources that match watch_patterns without reprocessing old ones.

1. Load queue file for the topic
2. Collect all paths from `watch_patterns` using Glob
3. Filter out any paths already in `sources` (regardless of status)
4. Add new matches to `sources` with:
   - `type`: `local`
   - `status`: `pending`
5. Update queue file
6. Report:
   ```
   Found X new sources matching watch_patterns.
   Queue now has Y pending items. Run `/synthesize [topic]` to process.
   ```

If no new sources found:
```
No new sources found. Synthesis is up to date with watch_patterns.
```

**Tip:** Run `/synthesize update [topic]` periodically after adding new notes or video summaries to keep the synthesis current.

## Synthesis Document Template

Create at: `my-vault/06 Knowledge Base/Synthesis/[Topic]/[Topic] Synthesis.md`

```markdown
---
class: Synthesis
topic: [Topic Name]
created: [Date]
lastUpdated: [Date]
status: in-progress
---

## Overview

[2-3 sentence summary of the topic - updated as understanding deepens]

## Key Findings

### [Category]

- Finding with specific details ^[src-1]
- Another finding that multiple sources support ^[src-1] ^[src-3]

<!-- Add categories as needed based on source content -->

## Open Questions

<!-- Contradictions, uncertainties, areas needing human judgment -->

- **[Topic]**: Source A says X ^[src-1], but Source B says Y ^[src-2].

## Suggested Sub-Topics

<!-- Categories that could warrant their own synthesis -->

- **[Sub-topic]** - X sources touched on this; may warrant dedicated synthesis

---
*Sources and processing log: [[Topic Sources]]*
```

## Sources Document Template

Create at: `my-vault/06 Knowledge Base/Synthesis/[Topic]/[Topic] Sources.md`

```markdown
---
class: Note
parent: "[[Topic Synthesis]]"
---

## Sources

| ID | Title | Date | Type | Discovered | Path/URL |
|----|-------|------|------|------------|----------|
| src-1 | Source Title | 2025-03 | Video | - | [[path/to/note]] |
| src-2 | Study Name | 2024-11 | Web | from src-1 | [link](url) |

## Processing Log

- **2026-01-14**: Initial synthesis. Processed 3 items. Created categories for X, Y, Z. Discovered 2 new sources.
- **2026-01-15**: Processed 3 items. Flagged contradiction on [topic]. Discovered 1 new source.
```

## Length Discipline

**Core content (Overview through Suggested Sub-Topics) must stay under 300 lines.**

Guidelines:
- Overview: 5 lines max
- Categories: 8 max in main doc
- Points per category: 15 max
- Open Questions: 10 max

When a category exceeds ~40-50 lines or has 5+ sources going deep:
1. Summarize tightly in the main doc (5-10 key points)
2. Add to Suggested Sub-Topics
3. Sub-topic syntheses get their own doc in the same folder, linking back to parent

## Handling Contradictions

When new information conflicts with existing content:

1. **Do not silently replace** the existing information
2. Move both claims to Open Questions with citations:
   ```
   - **Medication timing**: Take with food for reduced side effects ^[src-2],
     but empty stomach for faster absorption ^[src-5]. May depend on specific medication.
   ```
3. If a clear resolution exists (newer research, more credible source, broader consensus), note it:
   ```
   - **Resolved**: Earlier sources suggested X, but consensus now supports Y ^[src-8] ^[src-9] ^[src-10]
   ```

## Citation Format

Use `^[source-id]` inline, where source-id matches the ID column in the Sources table.

- Single source: `Finding here ^[src-1]`
- Multiple sources: `Well-supported finding ^[src-1] ^[src-3] ^[src-7]`
- Conflicting sources: Note in Open Questions section

## Adding Sources to Queue

### Manual Addition
```
/synthesize add adhd my-vault/path/to/specific/note.md
```

### Glob Pattern
```
/synthesize add adhd "my-vault/06 Knowledge Base/Capture/Videos/**/*ADHD*.md"
```

### By Tag (search and add)
When adding, search for relevant notes:
- Notes with topic in filename
- Notes with relevant tags
- Video summaries from relevant channels

Deduplicate against existing sources in queue before adding.

## Creating Sub-Topic Syntheses

When a sub-topic warrants its own document:

1. Create new queue: `/synthesize new "ADHD Medications"`
2. Set `topic_folder` to match parent: `"ADHD"` (keeps files together)
3. Add relevant sources (can include already-processed sources from parent for deeper dive)
4. In parent synthesis, add link: `See also: [[ADHD Medications Synthesis]]`
5. In sub-topic synthesis Overview, note parent: `Deep-dive from [[ADHD Synthesis]]`
