---
name: bookstrap-plan-research
description: Analyze BRD and existing corpus to identify knowledge gaps, then generate prioritized research tasks for filling those gaps
disable-model-invocation: true
allowed-tools: Bash, Read
---

# /bookstrap-plan-research - Identify Knowledge Gaps

Analyze the Book Requirements Document (BRD) against the existing research corpus to identify knowledge gaps and generate prioritized research tasks.

## Purpose

Compare what the book requires (from BRD) with what knowledge currently exists in the database (from prior ingestion). Generate a prioritized list of research tasks that will fill the identified gaps before writing begins.

This command delegates the analysis work to the `corpus-analyst` agent.

## Input Arguments

None. This command reads from the database:
- BRD content and requirements
- Existing sources and their coverage
- Entities already extracted
- Current knowledge gaps

## Processing Workflow

### 1. Load BRD Requirements

Query the database to retrieve the Book Requirements Document:

```bash
# Query BRD from database
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "SELECT * FROM brd ORDER BY version DESC LIMIT 1;"
```

Extract key requirements:
- Planned chapters and sections
- Key concepts, characters, locations, events
- Research areas specified in BRD
- Genre-specific knowledge needs
- Target audience and depth requirements

### 2. Query Existing Corpus Coverage

Analyze what knowledge already exists in the database:

```surql
-- Coverage by chapter/topic
SELECT chapter, count() as sources
FROM section->cites->source
GROUP BY chapter;

-- Entity coverage
SELECT name, count() as mentions
FROM concept<-related_to<-source
GROUP BY name;

-- Existing knowledge gaps (unresolved)
SELECT * FROM knowledge_gap
WHERE resolved = false
ORDER BY created_at;

-- Source distribution by type
SELECT source_type, count() as total
FROM source
GROUP BY source_type;

-- Timeline coverage
SELECT sequence, count() as events
FROM event
GROUP BY sequence;
```

### 3. Compare BRD Against Corpus

For each chapter/topic/concept in the BRD:
- Check if sufficient sources exist in the database
- Identify entities mentioned in BRD but missing from corpus
- Find topics with low source coverage
- Detect chronological gaps in timeline
- Flag concepts lacking supporting evidence

### 4. Generate Prioritized Research Tasks

Create research tasks with priorities based on:

**High Priority**:
- Core plot/argument elements with no sources
- Main characters/concepts missing from corpus
- Critical events lacking documentation
- Topics that block multiple writing tasks

**Medium Priority**:
- Supporting details with thin coverage
- Secondary characters/locations needing depth
- Background context for credibility
- Genre-specific atmosphere/accuracy needs

**Low Priority**:
- Optional enrichment details
- Tangential background information
- Nice-to-have but not essential

### 5. Store Tasks in Database

For each research task, create a database record:

```surql
CREATE knowledge_gap SET
  question = $research_question,
  context = $why_needed,
  priority = $priority_level,
  chapter_blocking = $chapters_affected,
  resolved = false,
  created_at = time::now()
;
```

### 6. Delegate to Corpus Analyst

Invoke the `corpus-analyst` agent to perform the detailed gap analysis:

```bash
# Load corpus-analyst agent with context
# Agent will:
# 1. Read BRD from database
# 2. Execute coverage queries
# 3. Perform gap analysis
# 4. Generate prioritized research tasks
# 5. Store tasks in database
# 6. Generate report
```

The corpus-analyst agent has read-only database access and uses the `corpus-analysis` and `surrealdb` skills.

## Output Format

Report generated research tasks to the user:

```
KNOWLEDGE GAP ANALYSIS
======================

BRD: <Book Title>
Corpus: <N> sources, <M> entities

COVERAGE ANALYSIS
-----------------
High Coverage:
  ✓ Chapter 1: Introduction (8 sources, 15 entities)
  ✓ Concept: SOE Training (12 sources)

Medium Coverage:
  ~ Chapter 3: Lyon Operation (3 sources, 8 entities)
  ~ Location: Lyon Safehouse (2 sources)

Low/No Coverage:
  ✗ Chapter 5: Wireless Protocols (0 sources)
  ✗ Event: Gestapo Raid 1943 (0 sources)
  ✗ Character: Marie Dubois (mentioned in BRD, not in corpus)

RESEARCH TASKS GENERATED: 12
=============================

HIGH PRIORITY (4 tasks)
-----------------------
1. SOE wireless operator training protocols 1942-1943
   Why: Core to protagonist's role, zero sources
   Blocks: Chapters 2, 4, 6

2. Lyon Resistance network structure and key figures
   Why: Primary setting, only 2 tangential sources
   Blocks: Chapters 3, 5, 7

3. Gestapo counter-intelligence methods in Lyon 1943
   Why: Antagonist strategy, no documentation
   Blocks: Chapters 5, 8

4. Daily life details in occupied Lyon (food, curfews, rationing)
   Why: Atmosphere and authenticity, minimal coverage
   Blocks: Chapters 3, 4, 5, 7

MEDIUM PRIORITY (5 tasks)
-------------------------
5. SOE Beaulieu training facility layout and procedures
6. Wireless set types used by F Section agents
7. Lyon geography and landmarks 1943
8. French Resistance communication codes
9. Black market operations in wartime Lyon

LOW PRIORITY (3 tasks)
----------------------
10. Fashion and clothing styles 1943 France
11. Popular culture and entertainment during occupation
12. Weather patterns in Lyon region

NEXT STEPS
----------
Run /bookstrap-research to execute these tasks autonomously.
Use /bookstrap-status to monitor progress.
```

## Statistics to Track

Calculate and report:
- Total chapters planned vs. covered
- Entities in BRD vs. entities in corpus
- Source count per major topic
- Percentage of BRD requirements met
- Number of high/medium/low priority gaps
- Estimated research tasks needed

## Implementation Notes

### Agent Delegation

This command is a thin wrapper that:
1. Verifies database connection
2. Checks that BRD exists
3. Invokes the `corpus-analyst` agent
4. Displays the agent's output

The actual analysis logic lives in the `corpus-analyst` agent to keep concerns separated.

### Gap Detection Strategies

The corpus-analyst uses multiple approaches:
- **Keyword matching**: BRD entities vs. database entities
- **Semantic search**: BRD concepts vs. source embeddings
- **Graph analysis**: Required relationships missing from graph
- **Timeline gaps**: Chronological holes in event sequence
- **Citation density**: Sections with claims but no sources

### Idempotency

Re-running `/bookstrap-plan-research` should:
- Update existing gaps if BRD changed
- Add new gaps if corpus changed
- Not duplicate existing unresolved gaps
- Re-prioritize based on current state

### Configuration

Gap detection thresholds can be configured in `bookstrap.config.json`:

```json
{
  "gap_detection": {
    "min_sources_per_chapter": 5,
    "min_sources_per_concept": 2,
    "high_priority_threshold": 0,
    "medium_priority_threshold": 2
  }
}
```

## Error Handling

| Error | Recovery |
|-------|----------|
| BRD not found | Abort with message to run `/bookstrap-init` first |
| Database connection failed | Abort with message to start SurrealDB |
| No corpus exists | Warning that all BRD requirements are gaps, generate exhaustive research plan |
| Corpus-analyst agent error | Display error, suggest re-running or checking logs |

## Pre-requisites

Before running `/bookstrap-plan-research`:

1. **BRD created**: `/bookstrap-init` must have been run
2. **SurrealDB running**: Database must be accessible
3. **Schema initialized**: Database schema loaded
4. **Initial corpus ingested** (optional): `/bookstrap-ingest` provides baseline, but can run on empty corpus

## Related Commands

- `/bookstrap-init` - Create BRD
- `/bookstrap-ingest` - Load initial corpus
- `/bookstrap-research` - Execute research tasks generated by this command
- `/bookstrap-status` - View gap resolution progress
- `/bookstrap-plan-write` - Generate writing tasks after gaps filled

## Supporting Agents

| Agent | Role |
|-------|------|
| `corpus-analyst` | Performs gap analysis, generates research tasks |

## Supporting Skills

| Skill | Purpose |
|-------|---------|
| `corpus-analysis/` | Gap detection strategies and coverage analysis |
| `surrealdb/` | Database query patterns for coverage analysis |

## Example Usage

```bash
# After initial ingestion, identify what's missing
/bookstrap-plan-research

# Re-run after additional ingestion to update gap list
/bookstrap-ingest ./more-sources/
/bookstrap-plan-research

# Check gaps before starting to write
/bookstrap-plan-research
/bookstrap-status
```

## Integration with Research Loop

This command is part of the research cycle:

```
init → ingest → plan-research → research
                     ↑              │
                     └──────────────┘
                    (iterate until
                     gaps resolved)
```

Once gaps are identified, `/bookstrap-research` executes the tasks autonomously. If new gaps are discovered during writing, re-run this command to generate new research tasks.
