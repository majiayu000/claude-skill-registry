---
name: bookstrap-write
description: Execute writing tasks autonomously by loading pending tasks, running pre-write queries, checking consistency, writing grounded content, and storing results
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, TaskGet, TaskUpdate
---

# /bookstrap-write - Execute Writing Tasks

Execute writing tasks autonomously to produce manuscript content grounded in the research corpus. This command loads pending writing tasks from the database, runs pre-write queries for context, checks consistency constraints, writes sections based on retrieved knowledge, and stores results in both database and files.

## Purpose

Write manuscript sections based on corpus knowledge without web access. This command operates in **write mode** where it strictly uses database content for writing. If knowledge gaps are discovered during writing, they are flagged for later research but never filled with web searches.

This command delegates the writing work to the `writer` agent, which operates in write mode with database-only access.

## Input Arguments

None. This command reads pending writing tasks from the database:
- Unresolved writing tasks with dependencies
- Required knowledge checks
- Pre-write query specifications
- Post-write storage operations
- Consistency constraint definitions

## Processing Workflow

### 1. Load Pending Writing Tasks

Query the database to retrieve pending writing tasks respecting dependencies:

```bash
# Query pending writing tasks
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "SELECT * FROM writing_task WHERE status = 'pending' AND blockedBy = [] ORDER BY priority DESC, sequence ASC;"
```

Filter and prioritize:
- Tasks with no blocking dependencies (blockedBy = [])
- High priority tasks first (core chapters, key scenes)
- Sequential order within chapters (sequence ASC)
- Tasks with all required knowledge available in database
- Skip tasks blocked by unresolved knowledge gaps

### 2. For Each Writing Task

Execute writing tasks one at a time, committing progress after each completed section.

#### 2.1 Run Pre-Write Queries

Each writing task specifies pre-write queries to gather context from the database. These queries use hybrid RAG combining semantic search, graph traversal, and timeline checks:

**Semantic Search** - Find similar content by theme:
```surql
SELECT * FROM section
WHERE embedding <|5|> $query_vector
ORDER BY vector::similarity(embedding, $query_vector) DESC;
```

**Graph Traversal** - Get relevant entities and relationships:
```surql
-- Character appearances and relationships
SELECT
  ->appears_in->section.content,
  ->knows->character.name,
  ->confronts->character.name
FROM character:anna;

-- Source support for concepts
SELECT
  <-supports<-source.title,
  <-supports<-source.reliability
FROM concept:wireless_protocols;
```

**Timeline Queries** - Establish what happened before this point:
```surql
-- Events before current sequence
SELECT * FROM event
WHERE sequence < $current_sequence
ORDER BY sequence DESC
LIMIT 10;

-- Previous sections in chapter
SELECT * FROM section
WHERE chapter = $chapter AND sequence < $section_sequence
ORDER BY sequence DESC;
```

**Combined Hybrid Query**:
```surql
-- Semantic + graph + timeline
SELECT * FROM section
WHERE embedding <|3|> $query_vector
AND ->appears_in->character:anna
AND sequence < 5
ORDER BY sequence;
```

Run all pre-write queries specified in task metadata and collect results for context.

#### 2.2 Check Consistency Constraints

Before writing, verify consistency constraints from task metadata:

```surql
-- Character state violations (can't appear if dead)
SELECT * FROM character:anna
WHERE status = 'dead'
AND death_sequence < $current_sequence;

-- Location not introduced yet
SELECT * FROM location:safehouse
WHERE introduced = false;

-- Timeline contradictions
SELECT * FROM event
WHERE sequence > $current_sequence
AND date < $current_section_date;
```

If any constraint fails:
1. Log the constraint violation
2. Flag as knowledge gap or consistency error
3. Skip this task (mark as blocked)
4. Continue to next task

Do NOT write if consistency checks fail.

#### 2.3 Check for Knowledge Gaps

Verify all required knowledge exists in the database:

```surql
-- Check required knowledge from task metadata
SELECT * FROM knowledge_gap
WHERE id IN $required_knowledge
AND resolved = false;
```

If gaps found:
1. Flag the gap in database
2. Mark task as blocked by gap
3. Skip this task (do NOT web search)
4. Continue to next task

**CRITICAL**: Write mode NEVER accesses web. Gaps are flagged, not filled.

#### 2.4 Write Section Grounded in Context

With context gathered and constraints verified, write the section:

**Writing Principles**:
- Ground all content in retrieved database context
- Cite sources for factual claims
- Maintain voice consistency per BRD
- Follow genre conventions from loaded genre skills
- Use pre-write query results for accuracy
- Integrate character relationships from graph
- Respect timeline sequence
- Flag any new gaps discovered during writing

**Output**: Section content as markdown text

#### 2.5 Run Post-Write Storage

After writing, execute post-write operations specified in task metadata:

**1. Generate Embedding**:
```bash
python ./scripts/generate-embedding.py \
  --text "$section_content" \
  --provider <configured-provider> \
  --model <configured-model>
```

**2. Store Section in Database**:
```surql
CREATE section SET
  content = $content,
  embedding = $embedding_vector,
  chapter = $chapter_number,
  sequence = $section_sequence,
  word_count = $word_count,
  status = 'draft',
  created_at = time::now();
```

**3. Extract Entities Mentioned**:
```bash
python ./scripts/extract-entities.py \
  --content "$section_content" \
  --section-id <section-id> \
  --mode writing
```

This extracts:
- New characters introduced
- Locations mentioned
- Events that occurred
- Concepts discussed
- Dates/times referenced

**4. Create Relationships**:
```surql
-- Link section to cited sources
RELATE section:<id>->cites->source:<source-id>;

-- Track character appearances
RELATE character:<id>->appears_in->section:<id>;

-- Location usage
RELATE section:<id>->located_in->location:<id>;

-- Event sequence
RELATE event:<new-id>->follows->event:<previous-id>;
```

**5. Update Timeline**:
```surql
-- Add events to timeline
CREATE event SET
  name = $event_name,
  description = $event_description,
  sequence = $sequence_number,
  date = $event_date,
  section = section:<id>;

-- Link to previous events
RELATE event:<id>->precedes->event:<next-id>;
```

**6. Write to Manuscript File**:
```bash
# Create manuscript file using configured naming pattern
mkdir -p ./manuscript/chapter-$chapter_number/
cat > "./manuscript/chapter-$chapter_number/section-$section_sequence-$slug.md" <<EOF
# $section_title

$section_content

---
*Generated: $(date)*
*Word count: $word_count*
*Status: draft*
EOF
```

#### 2.6 Flag Any New Knowledge Gaps

If writing reveals missing knowledge (character backstory, historical detail, technical specification):

```surql
CREATE knowledge_gap SET
  question = $gap_question,
  context = $gap_context,
  discovered_during = 'writing',
  discovered_in = section:<id>,
  blocks_tasks = [task:<id>],
  resolved = false,
  created_at = time::now();
```

Log the gap for later research cycle.

#### 2.7 Commit Progress

After each successfully written section:

```bash
git add manuscript/ data/
git commit -m "[bookstrap] Write: Completed section '$section_title' (Chapter $chapter)

Section: chapter-$chapter-section-$sequence
Word count: $word_count
Entities extracted: $entity_count
Relationships created: $relationship_count
Citations: $citation_count
Gaps flagged: $gap_count

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 3. Delegate to Writer Agent

Invoke the `writer` agent to perform the detailed writing work:

```bash
# Load writer agent with context
# Agent will:
# 1. Load next pending writing task
# 2. Run pre-write queries
# 3. Check consistency constraints
# 4. Verify required knowledge exists
# 5. Write section grounded in context
# 6. Generate embeddings
# 7. Extract entities and create relationships
# 8. Write to manuscript file
# 9. Flag any gaps discovered
# 10. Commit progress
# 11. Continue to next task or exit if blocked
```

The writer agent has read+write database access, NO web access, and uses the `writing`, `surrealdb`, `outlining`, and genre-specific skills.

### 4. Continue Until Complete or Blocked

The writer agent continues processing tasks until:
- **All tasks complete**: All sections written
- **Blocked by gaps**: Required knowledge missing (flag gaps, recommend research)
- **Consistency failure**: Timeline contradiction or character state violation
- **Database error**: Cannot store results or query fails
- **Manual intervention needed**: BRD clarification required

## Output Format

Report writing progress to the user:

```
WRITING EXECUTION
=================

Configuration:
- Embedding provider: Gemini (text-embedding-004)
- Database: bookstrap/my_book
- Manuscript dir: ./manuscript
- Auto-commit: enabled

TASK 1/32: Chapter 1, Section 2
--------------------------------
Title: "The Training Begins"
Sequence: chapter-1-section-2
Required knowledge: ✓ All available
Dependencies: ✓ None blocking

Pre-write queries:
  → Semantic search: 5 similar passages found
  → Graph query: character:anna relationships (3 connections)
  → Timeline: 2 previous events established
  → Sources: 4 relevant sources retrieved

Consistency checks:
  ✓ Characters: anna (status: alive, introduced: true)
  ✓ Location: beaulieu_training_facility (introduced: true)
  ✓ Timeline: sequence valid (no contradictions)

Writing section...
  → Content: 1,250 words written
  → Voice: matches BRD specifications
  → Citations: 3 sources cited
  → Genre conventions: thriller pacing maintained

Post-write storage:
  → Embedding generated (768 dimensions)
  → Section stored: section:ch1-sec2
  → Entities extracted: 2 new characters, 1 event
  → Relationships: 5 edges created
  → Manuscript file: ./manuscript/chapter-01/section-02-training-begins.md

Gaps flagged: 1
  ! "Specific wireless code protocols used in 1943" (flagged for research)

Committed: [def5678]

---

TASK 2/32: Chapter 1, Section 3
--------------------------------
Title: "First Transmission"
Sequence: chapter-1-section-3
Required knowledge: ✗ Gap blocking
Dependencies: ✓ Previous section complete

Consistency checks:
  ✓ All constraints pass

Knowledge gaps:
  ✗ Required: "Wireless code protocols 1943" (unresolved)

Task blocked by knowledge gap.
Skipping to next unblocked task...

---

TASK 3/32: Chapter 2, Section 1
--------------------------------
Title: "Arrival in Lyon"
[...]

---

PROGRESS SUMMARY
================

Tasks completed: 8/32
Tasks blocked by gaps: 3
Sections written: 8
Total word count: 9,850 / 80,000 target (12.3%)
Chapters started: 3/10

Entities extracted: 24
  - Characters: 8
  - Locations: 5
  - Events: 11
  - Concepts: 7

Relationships created: 47
Citations: 22 sources cited
Gaps flagged: 3

Commits: 8
Time elapsed: 24 minutes

NEXT STEPS
----------
Knowledge gaps blocking 3 tasks:
  1. "Wireless code protocols 1943"
  2. "Lyon Resistance safe house locations"
  3. "German counter-intelligence procedures"

Recommended: /bookstrap-plan-research (generate research tasks for gaps)
Then: /bookstrap-research (fill gaps)
Then: /bookstrap-write (resume writing)

Continue writing unblocked tasks: /bookstrap-write
Check status: /bookstrap-status
Query content: /bookstrap-query "Show me all scenes with Anna"
```

## Behavior Characteristics

### Write Mode (Database Only)

This command operates in **write mode**:
- ✗ NO web access
- ✓ Database queries only
- ✓ Flags gaps instead of filling them
- ✓ Clean, grounded writing
- ✓ Commits after each section
- ✓ Enforces consistency constraints
- ✓ Maintains voice per BRD

### Autonomous Execution

Runs fully autonomously:
- No human approval needed per section
- Processes tasks sequentially (maintains coherence)
- Commits atomic progress (recoverable if interrupted)
- Skips blocked tasks (logs reason)
- Flags gaps for research cycle
- Logs all writing decisions

### Consistency Over Completeness

Prioritizes consistency:
- Better to skip than write without grounding
- Enforces timeline consistency
- Verifies character states
- Checks location introductions
- Validates source citations
- Flags contradictions

## Configuration

Writing behavior configured in `bookstrap.config.json`:

```json
{
  "output": {
    "manuscript_dir": "./manuscript",
    "file_format": "markdown",
    "naming": {
      "chapter": "chapter-{{sequence}}-{{slug}}.md",
      "section": "{{chapter}}/section-{{sequence}}-{{slug}}.md"
    }
  },
  "git": {
    "auto_commit": true,
    "commit_after": "task",
    "message_format": "[bookstrap] {{task_type}}: {{task_subject}}"
  },
  "writing": {
    "min_sources_per_claim": 1,
    "enforce_consistency": true,
    "auto_flag_gaps": true,
    "voice_check": true,
    "genre_conventions": true
  }
}
```

Settings:
- `manuscript_dir`: Output directory for manuscript files
- `file_format`: Output format (markdown)
- `naming`: Filename templates for chapters and sections
- `auto_commit`: Commit after each section (recommended)
- `min_sources_per_claim`: Minimum citations for factual claims
- `enforce_consistency`: Check constraints before writing
- `auto_flag_gaps`: Automatically detect and flag knowledge gaps
- `voice_check`: Verify voice matches BRD
- `genre_conventions`: Apply genre-specific patterns

## Error Handling

| Error | Recovery |
|-------|----------|
| Knowledge gap found | Flag gap, skip task, continue to next |
| Consistency check fails | Log violation, skip task, continue |
| Required knowledge missing | Mark task blocked, continue |
| Database write failure | Abort, report error, preserve uncommitted work |
| Embedding generation fails | Retry up to 3 times, then skip section |
| Manuscript file write fails | Abort, report error (database still has content) |
| Timeline contradiction | Flag inconsistency, skip task, recommend edit |
| Character state violation | Flag violation, skip task, recommend fix |

## Pre-requisites

Before running `/bookstrap-write`:

1. **BRD created**: `/bookstrap-init` must have been run
2. **SurrealDB running**: Database must be accessible
3. **Corpus populated**: `/bookstrap-ingest` and `/bookstrap-research` completed
4. **Writing tasks generated**: `/bookstrap-plan-write` must have created tasks
5. **Embedding provider configured**: For new content embeddings
6. **Manuscript directory exists**: Output folder created

## Related Commands

- `/bookstrap-plan-write` - Generate writing tasks (run this first)
- `/bookstrap-research` - Fill knowledge gaps (run when blocked)
- `/bookstrap-edit` - Review and polish written content (run after writing)
- `/bookstrap-status` - Monitor writing progress and gap status
- `/bookstrap-query` - Query written content and entities

## Supporting Agents

| Agent | Role |
|-------|------|
| `writer` | Executes writing tasks, enforces consistency, flags gaps |

## Supporting Skills

| Skill | Purpose |
|-------|---------|
| `writing/` | Core writing workflow, voice consistency, citation integration |
| `surrealdb/` | Database query patterns for context retrieval and storage |
| `outlining/` | Story structure, chapter organization, pacing |
| `genres/*` | Genre-specific conventions (thriller pacing, historical accuracy, etc.) |

## Supporting Scripts

| Script | Purpose |
|--------|---------|
| `generate-embedding.py` | Generate embeddings via configured provider |
| `extract-entities.py` | LLM-based entity extraction from written content |

## Example Usage

```bash
# After generating writing tasks, execute writing
/bookstrap-plan-write
/bookstrap-write

# Writing interrupted? Resume where you left off
/bookstrap-write

# Check progress
/bookstrap-status

# If blocked by gaps, run research cycle
/bookstrap-plan-research
/bookstrap-research
/bookstrap-write

# Continue writing after gaps filled
/bookstrap-write

# Review written content
/bookstrap-edit
```

## Integration with Research-Write Cycle

This command is part of the research-write cycle:

```
init → ingest → plan-research → research
                     ↑              │
                     │              ▼
                     │         plan-write → write → edit
                     │              │
                     └──── gaps ────┘
```

When writing discovers knowledge gaps:
1. Writing task flags gap and skips to next task
2. User runs `/bookstrap-plan-research` to generate research tasks
3. User runs `/bookstrap-research` to fill gaps
4. User runs `/bookstrap-write` to resume writing (now unblocked)

This separation ensures:
- Research mode fills gaps with web access
- Write mode produces grounded content without web
- No hallucination or unsourced claims
- Clean separation of concerns

## Statistics to Track

Calculate and report:
- Tasks completed vs. remaining
- Sections written per chapter
- Total word count vs. target
- Words per section (average)
- Entities extracted per section (average)
- Citations per section (average)
- Gaps flagged (with details)
- Consistency violations found
- Time per section (estimate remaining time)
- Chapters in progress vs. complete

## Logging

Detailed logging for transparency:

```
[2024-01-15 16:45:12] [WRITE] Task 1/32 started: Chapter 1, Section 2
[2024-01-15 16:45:13] [QUERY] Pre-write: semantic search (5 results)
[2024-01-15 16:45:14] [QUERY] Pre-write: graph traversal (3 relationships)
[2024-01-15 16:45:15] [QUERY] Pre-write: timeline check (2 events)
[2024-01-15 16:45:16] [CHECK] Consistency: All constraints pass
[2024-01-15 16:45:17] [CHECK] Knowledge: All required knowledge available
[2024-01-15 16:45:25] [WRITE] Section complete: 1,250 words
[2024-01-15 16:45:26] [EMBED] Embedding generated (768 dims)
[2024-01-15 16:45:27] [DB] Section stored: section:ch1-sec2
[2024-01-15 16:45:28] [EXTRACT] Entities: 2 characters, 1 event, 1 location
[2024-01-15 16:45:29] [GRAPH] Created 5 relationships
[2024-01-15 16:45:30] [FILE] Written: ./manuscript/chapter-01/section-02-training-begins.md
[2024-01-15 16:45:31] [GAP] Flagged: "Wireless code protocols 1943"
[2024-01-15 16:45:33] [GIT] Committed: def5678
[2024-01-15 16:45:34] [WRITE] Task 1/32 complete (22s)
```

## Implementation Notes

### Agent Delegation

This command is a thin wrapper that:
1. Verifies database connection
2. Checks that writing tasks exist
3. Loads writing configuration
4. Invokes the `writer` agent
5. Displays the agent's output
6. Reports final statistics

The actual writing logic lives in the `writer` agent to keep concerns separated.

### Idempotency

Re-running `/bookstrap-write` is safe:
- Only processes pending tasks
- Skips already-written sections
- Maintains sequential order within chapters
- Can be interrupted and resumed
- No duplicate content

### Separation of Concerns

Research mode vs. Write mode:
- **Research mode**: Web access, fills gaps, commits per task
- **Write mode**: Database only, flags gaps, commits per section

This command operates exclusively in write mode and never accesses the web. Writing discovers gaps but never fills them.

## Advanced Features

### Voice Consistency Checking

Verify each section matches BRD voice specifications:
- Load BRD voice sample
- Compare tone, formality, sentence structure
- Flag sections that drift from established voice
- Suggest revisions if voice inconsistent

### Genre Convention Application

Apply genre-specific patterns from loaded genre skills:
- **Thriller**: Maintain pacing, tension, reveals
- **Historical**: Verify period accuracy, avoid anachronisms
- **Memoir**: Balance truth and narrative flow
- **Technical**: Ensure clarity, provide examples

### Citation Tracking

Maintain citation coverage:
- Track which sources cited in each section
- Flag uncited factual claims
- Build bibliography automatically
- Cross-reference claims to sources

### Timeline Validation

Ensure chronological consistency:
- Verify event sequences match timeline
- Check character ages and lifespans
- Validate date references
- Flag temporal contradictions

## Troubleshooting

### All tasks blocked by gaps

```
Status: 32/32 tasks blocked by knowledge gaps
Action: Run research cycle
```

Solution:
```bash
/bookstrap-plan-research
/bookstrap-research
/bookstrap-write
```

### Consistency check failures

```
Task: Chapter 3, Section 2
Error: Character 'anna' marked dead in previous chapter
Action: Task skipped, flagged for review
```

Possible solutions:
- Review timeline in previous chapters
- Correct character state in database
- Adjust section sequence
- Update consistency constraints

### Database connection lost

```
Error: Cannot connect to SurrealDB at localhost:2665
Action: Writing paused, no progress lost
```

Automatic recovery:
- Check SurrealDB is running
- Restart database if needed
- Re-run `/bookstrap-write` to resume

### Embedding generation fails

```
Section: Chapter 2, Section 5
Error: Embedding API rate limit exceeded
Action: Retrying in 60s (attempt 1/3)
```

Automatic recovery:
- Wait for rate limit reset
- Retry up to 3 times
- Skip section if all retries fail
- Log for manual review

## Security Considerations

### No Web Access

Write mode NEVER accesses web:
- Prevents hallucination
- Ensures source grounding
- Maintains consistency
- Avoids copyright issues

### Citation Requirements

All factual claims must cite sources:
- Minimum 1 source per factual claim
- Source reliability tracked
- Citations stored in database
- Bibliography auto-generated

### Version Control

All writing committed to git:
- Atomic commits per section
- Full audit trail
- Easy rollback
- Collaboration support

### Data Persistence

Dual storage for safety:
- Database: Queryable, relational
- Files: Human-readable, editable
- Git: Version-controlled, backed up

## Quality Metrics

Track writing quality:
- **Source grounding**: Percentage of claims with citations
- **Voice consistency**: Deviation from BRD specifications
- **Genre adherence**: Conformance to genre conventions
- **Timeline accuracy**: Consistency check pass rate
- **Character consistency**: State violation rate
- **Completeness**: Percentage of tasks unblocked
- **Efficiency**: Words per hour
- **Gap detection**: Percentage of gaps flagged vs. missed
