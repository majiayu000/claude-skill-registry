---
name: bookstrap-status
description: Display comprehensive project progress including BRD status, corpus statistics, research progress, and writing progress with recommendations for next actions
disable-model-invocation: true
allowed-tools: Bash, Read
---

# /bookstrap-status - Display Progress Dashboard

Display comprehensive project status without making any changes. This is a read-only command that queries the database for all project metrics and recommends the next action based on current state.

## Purpose

Provide a clear, actionable overview of the entire book project's status. Show what's complete, what's in progress, what's blocking progress, and what should be done next. This command helps users understand the project state at a glance and guides them toward the next logical step.

## Input Arguments

None. This command reads all status information from the database and project files.

## Output Format

Display a comprehensive status dashboard with the following sections:

### 1. Project Overview

```
BOOKSTRAP STATUS
================

Project: <book-title-from-BRD>
Database: <status> (SurrealDB <version>)
BRD: <status> (v<version>)
Config: <config-file-path>
```

Status indicators:
- BRD: `✓ Complete (v2)` or `✗ Missing` or `⚠ Outdated`
- Database: `Running (SurrealDB 2.0)` or `✗ Not running` or `⚠ Connection issues`

### 2. Corpus Statistics

```
CORPUS
------
Sources: <N> ingested
  - Primary: <N>
  - Secondary: <N>
  - Web: <N>
Entities: <N> extracted
  - Characters: <N>
  - Locations: <N>
  - Events: <N>
  - Concepts: <N>
```

Query database for source and entity counts:
```surql
-- Count sources by type
SELECT count() AS total,
       source_type,
       reliability
FROM source
GROUP BY source_type, reliability;

-- Count entities by type
SELECT
  (SELECT count() FROM character) AS characters,
  (SELECT count() FROM location) AS locations,
  (SELECT count() FROM event) AS events,
  (SELECT count() FROM concept) AS concepts;
```

### 3. Research Progress

```
RESEARCH
--------
Tasks: <N>/<total> complete
Gaps: <N> open, <N> resolved
Sources needed: <N> high priority
```

Query for research status:
```surql
-- Knowledge gaps status
SELECT
  count() AS total,
  count(resolved = true) AS resolved,
  count(resolved = false) AS open
FROM knowledge_gap;

-- High priority gaps
SELECT count()
FROM knowledge_gap
WHERE resolved = false
  AND priority = 'high';
```

### 4. Writing Progress

```
WRITING
-------
Tasks: <N>/<total> complete
Chapters: <N>/<total> drafted
  - Complete: <N>
  - In progress: <N>
  - Not started: <N>
Word count: <N> / <target> target (<N>%)
```

Query for writing status:
```surql
-- Chapter status
SELECT
  count() AS total,
  count(status = 'complete') AS complete,
  count(status = 'draft') AS in_progress,
  count(status = 'planned') AS not_started
FROM chapter;

-- Total word count
SELECT sum(word_count) AS total_words
FROM chapter
WHERE status IN ['draft', 'complete'];

-- Target word count from BRD
SELECT target_word_count FROM brd ORDER BY version DESC LIMIT 1;
```

### 5. Next Action Recommendation

```
NEXT ACTION
-----------
Recommended: /bookstrap-<command> (<reason>)
```

Recommendation logic based on current state:

| Condition | Recommendation |
|-----------|----------------|
| No BRD exists | `/bookstrap-init` (Create Book Requirements Document) |
| BRD exists, no sources | `/bookstrap-ingest` (Load initial research corpus) |
| Sources exist, no research tasks | `/bookstrap-plan-research` (Identify knowledge gaps) |
| Unresolved gaps exist | `/bookstrap-research` (<N> gaps blocking writing) |
| Gaps resolved, no writing tasks | `/bookstrap-plan-write` (Generate writing tasks from corpus) |
| Writing tasks exist, gaps block them | `/bookstrap-research` (<N> gaps blocking <N> tasks) |
| Writing tasks ready | `/bookstrap-write` (<N> tasks ready to write) |
| Writing complete, not edited | `/bookstrap-edit` (Run consistency and voice checks) |
| All complete | `All tasks complete! Run /bookstrap-query or /bookstrap-edit for refinements` |

## Implementation Workflow

### 1. Check Database Connection

```bash
# Verify SurrealDB is running
curl -s http://localhost:2665/health || echo "Database not running"

# If running, get version
surreal version 2>/dev/null || echo "Unknown"
```

### 2. Check BRD Status

```bash
# Check if BRD.md exists
if [ -f "BRD.md" ]; then
  # Get version from BRD if tracked in database
  # Otherwise mark as "✓ Complete"
else
  echo "✗ Missing"
fi
```

### 3. Query Corpus Statistics

Execute SurrealDB queries to gather:
- Source counts by type and reliability
- Entity counts by category
- Total embeddings generated
- Relationship edge counts

```bash
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "<query-from-above>"
```

### 4. Query Research Progress

Execute queries for:
- Total knowledge gaps (open vs. resolved)
- Research tasks completion
- High priority gaps
- Gaps blocking writing tasks

### 5. Query Writing Progress

Execute queries for:
- Chapter status distribution
- Section completion counts
- Total word count vs. target
- Tasks complete vs. pending

### 6. Calculate Recommendation

Use the decision logic above to determine the next command to run based on:
- What exists (BRD, sources, tasks)
- What's blocking progress (gaps, dependencies)
- What's ready to execute (unblocked tasks)

### 7. Format and Display

Present all information in the formatted output shown above.

## Additional Statistics (Optional Verbose Mode)

If user requests detailed stats with `/bookstrap-status --verbose`:

```
DETAILED STATISTICS
===================

CORPUS BREAKDOWN
----------------
Total storage: <MB> in database
Average chunk size: <N> tokens
Average entities per source: <N>
Embedding coverage: <N>% of content

RESEARCH DETAILS
----------------
Average sources per gap: <N>
Source reliability distribution:
  - High: <N> (<N>%)
  - Medium: <N> (<N>%)
  - Low: <N> (<N>%)

Top unresolved gaps:
  1. <gap-question> (blocks <N> tasks)
  2. <gap-question> (blocks <N> tasks)
  3. <gap-question> (blocks <N> tasks)

WRITING DETAILS
---------------
Average section length: <N> words
Citations per section: <N> average
Longest chapter: <chapter-title> (<N> words)
Shortest chapter: <chapter-title> (<N> words)

Blocked tasks:
  - Task: <task-subject> (blocked by: <gap-question>)
  - Task: <task-subject> (blocked by: <dependency-task>)

TIMELINE
--------
Project started: <date>
Days elapsed: <N>
Last activity: <date> (<command>)
Estimated completion: <date> (based on current pace)
```

## Error Handling

| Error | Display |
|-------|---------|
| Database not running | `Database: ✗ Not running (run: docker-compose up -d)` |
| Database connection error | `Database: ⚠ Connection issues (check config)` |
| BRD missing | `BRD: ✗ Missing (run: /bookstrap-init)` |
| Query timeout | `⚠ Database query timeout, showing partial results` |
| Empty database | Show zeros for all stats, recommend `/bookstrap-ingest` |

## Configuration

Read database connection settings from `bookstrap.config.json`:

```json
{
  "surrealdb": {
    "host": "localhost",
    "port": 2665,
    "namespace": "bookstrap",
    "database": "my_book",
    "username": "root",
    "password_env": "SURREAL_PASSWORD"
  }
}
```

## Example Output

```
BOOKSTRAP STATUS
================

Project: The Silent Cipher (Historical Thriller)
Database: Running (SurrealDB 2.0)
BRD: ✓ Complete (v2)
Config: ./bookstrap.config.json

CORPUS
------
Sources: 47 ingested
  - Primary: 12
  - Secondary: 28
  - Web: 7
Entities: 156 extracted
  - Characters: 23
  - Locations: 45
  - Events: 88
  - Concepts: 38

RESEARCH
--------
Tasks: 3/15 complete
Gaps: 12 open, 8 resolved
Sources needed: 5 high priority

WRITING
-------
Tasks: 7/32 complete
Chapters: 2/10 drafted
  - Complete: 1
  - In progress: 1
  - Not started: 8
Word count: 12,450 / 80,000 target (16%)

NEXT ACTION
-----------
Recommended: /bookstrap-research (12 gaps blocking writing)
```

## Pre-requisites

None. This command can be run at any time to check project status. It gracefully handles missing components and reports their status.

## Related Commands

- `/bookstrap-init` - Create BRD (if missing)
- `/bookstrap-ingest` - Load initial corpus (if needed)
- `/bookstrap-plan-research` - Generate research tasks
- `/bookstrap-research` - Execute research to fill gaps
- `/bookstrap-plan-write` - Generate writing tasks
- `/bookstrap-write` - Execute writing tasks
- `/bookstrap-edit` - Run editing passes
- `/bookstrap-query` - Query database for specific information

## Supporting Queries

### BRD Status Query

```surql
-- Get latest BRD version
SELECT content, version, created_at
FROM brd
ORDER BY version DESC
LIMIT 1;
```

### Comprehensive Corpus Query

```surql
-- Get all corpus statistics in one query
SELECT
  (SELECT count() FROM source) AS total_sources,
  (SELECT count() FROM source WHERE source_type = 'primary') AS primary_sources,
  (SELECT count() FROM source WHERE source_type = 'secondary') AS secondary_sources,
  (SELECT count() FROM source WHERE source_type = 'web') AS web_sources,
  (SELECT count() FROM character) AS characters,
  (SELECT count() FROM location) AS locations,
  (SELECT count() FROM event) AS events,
  (SELECT count() FROM concept) AS concepts,
  (SELECT count() FROM knowledge_gap WHERE resolved = false) AS open_gaps,
  (SELECT count() FROM knowledge_gap WHERE resolved = true) AS resolved_gaps,
  (SELECT count() FROM chapter) AS total_chapters,
  (SELECT count() FROM chapter WHERE status = 'complete') AS complete_chapters,
  (SELECT count() FROM chapter WHERE status = 'draft') AS draft_chapters,
  (SELECT sum(word_count) FROM chapter WHERE status IN ['draft', 'complete']) AS total_words;
```

### Blocking Analysis Query

```surql
-- Find what's blocking progress
SELECT
  question,
  context,
  created_at,
  (SELECT count() FROM task WHERE blocked_by CONTAINS $parent.id) AS blocking_task_count
FROM knowledge_gap
WHERE resolved = false
ORDER BY blocking_task_count DESC
LIMIT 10;
```

## Implementation Notes

### Read-Only Guarantee

This command:
- ✓ Reads from database and files
- ✓ Displays statistics and recommendations
- ✗ Does NOT modify any data
- ✗ Does NOT create or update records
- ✗ Does NOT trigger any workflows

### Performance

For large projects:
- Cache query results for 5 minutes
- Use COUNT queries instead of fetching full records
- Execute queries in parallel where possible
- Timeout long queries and show partial results

### Refresh

Status can be refreshed by simply re-running `/bookstrap-status`. The command always shows current state from the database.

## Troubleshooting

### Database not accessible

```
Database: ✗ Not running

Start database:
  docker-compose up -d
  OR
  ./scripts/start-surreal.sh
```

### No data in database

```
CORPUS
------
Sources: 0 ingested
Entities: 0 extracted

NEXT ACTION
-----------
Recommended: /bookstrap-ingest (Load initial research corpus)
```

### Stale recommendations

If recommendation doesn't match your intent:
- Run the recommended command to update state
- Or run a different command if you know what's needed
- Recommendations are guidance, not requirements

## Advanced Features

### Progress Tracking

Track velocity and estimate completion:
```surql
-- Calculate average tasks per day
SELECT
  count() AS total_tasks,
  count(status = 'completed') AS completed_tasks,
  time::diff(min(created_at), max(updated_at)) AS time_elapsed
FROM task;
```

Use this to estimate remaining time based on historical completion rate.

### Visualization Export

For future enhancement, export data for visualization:
```bash
/bookstrap-status --export json > status.json
/bookstrap-status --export csv > status.csv
```

### Continuous Monitoring

For long-running sessions, watch status updates:
```bash
watch -n 60 '/bookstrap-status'
```

## Example Use Cases

### Starting a new project
```bash
/bookstrap-status
# Output: "Recommended: /bookstrap-init"
/bookstrap-init
```

### Mid-project check
```bash
/bookstrap-status
# See what's done, what's next
# Run recommended command
```

### Debugging stalls
```bash
/bookstrap-status --verbose
# See what's blocking progress
# Identify gaps or dependencies
```

### Final review
```bash
/bookstrap-status
# Verify all chapters complete
# Check word count against target
# Run final edit pass
```
