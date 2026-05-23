---
name: bookstrap-plan-write
description: Generate writing tasks from BRD structure and corpus, creating chapter/section tasks with dependencies, pre-write queries, and consistency checks
disable-model-invocation: true
allowed-tools: Bash, Read
---

# /bookstrap-plan-write - Generate Writing Tasks

Analyze the Book Requirements Document (BRD) structure and existing corpus to generate prioritized writing tasks with full metadata, dependencies, and consistency checks.

## Purpose

Transform the BRD outline into executable writing tasks, each specifying required knowledge, pre-write database queries, post-write storage operations, and consistency constraints. Tasks are generated with dependencies (blockedBy relationships) to ensure proper writing order.

This command delegates the planning work to the `outline-planner` agent.

## Input Arguments

None. This command reads from the database:
- BRD structure and chapter outline
- Existing corpus and coverage
- Entities and relationships already extracted
- Resolved knowledge gaps

## Processing Workflow

### 1. Load BRD Structure

Query the database to retrieve the Book Requirements Document:

```bash
# Query BRD from database
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns bookstrap --db <database-name> \
  --query "SELECT * FROM brd ORDER BY version DESC LIMIT 1;"
```

Extract structural requirements:
- Planned chapters and sections
- Chapter sequence and dependencies
- Section topics and themes
- Target word counts per section
- Voice, tone, and style requirements
- POV and tense specifications

### 2. Analyze Corpus Coverage

Check what knowledge exists to support each planned section:

```surql
-- Coverage by planned chapter/topic
SELECT chapter, count() as sources
FROM section->cites->source
GROUP BY chapter;

-- Entity availability
SELECT * FROM character;
SELECT * FROM location;
SELECT * FROM event ORDER BY sequence;
SELECT * FROM concept;

-- Resolved knowledge gaps
SELECT * FROM knowledge_gap
WHERE resolved = true;

-- Source distribution
SELECT source_type, reliability, count() as total
FROM source
GROUP BY source_type, reliability;

-- Timeline completeness
SELECT sequence, count() as events
FROM event
GROUP BY sequence
ORDER BY sequence;
```

### 3. Generate Chapter/Section Writing Tasks

For each chapter/section in the BRD, create a writing task with comprehensive metadata:

#### Task Metadata Structure

```json
{
  "taskId": "chapter-3-scene-2",
  "subject": "Write Chapter 3, Scene 2: The Confrontation",
  "description": "Write the confrontation scene between Anna and Erik at the safehouse, revealing the betrayal and establishing the stakes for the final act.",
  "blockedBy": ["chapter-3-scene-1"],
  "metadata": {
    "chapter": 3,
    "section": 2,
    "sequence": 12,
    "target_words": 2500,
    "scene_type": "dialogue_heavy",
    "required_knowledge": [
      "character:anna.background",
      "character:anna.status",
      "character:erik.background",
      "character:erik.relationships",
      "location:safehouse.description",
      "location:safehouse.introduced",
      "event:discovery.details",
      "event:discovery.sequence",
      "concept:betrayal_theme"
    ],
    "pre_queries": [
      "SELECT * FROM section WHERE embedding <|5|> $theme_vector ORDER BY vector::similarity(embedding, $theme_vector) DESC",
      "SELECT * FROM character:anna->knows->character",
      "SELECT * FROM character:erik->knows->character",
      "SELECT * FROM event WHERE sequence < 12 ORDER BY sequence DESC LIMIT 5",
      "SELECT * FROM section WHERE chapter = 3 AND sequence < 2 ORDER BY sequence"
    ],
    "post_writes": [
      "CREATE section SET content=$content, embedding=$vec, chapter=3, sequence=12, word_count=$word_count, status='draft'",
      "RELATE character:anna->confronts->character:erik SET context=$confrontation_context",
      "RELATE event:confrontation->follows->event:discovery SET narrative_link=true",
      "RELATE section:$section_id->cites->source:$source_ids",
      "RELATE section:$section_id->appears_in<-character:anna",
      "RELATE section:$section_id->appears_in<-character:erik",
      "RELATE section:$section_id->located_in->location:safehouse"
    ],
    "consistency_checks": [
      "character:anna.status != 'dead'",
      "character:erik.status != 'dead'",
      "location:safehouse.introduced = true",
      "event:discovery.sequence < 12",
      "character:anna->knows->character:erik EXISTS"
    ],
    "voice_requirements": {
      "pov": "third_limited",
      "tense": "past",
      "tone": "tense_suspenseful",
      "comparable": "tension like le Carré"
    }
  }
}
```

### 4. Determine Task Dependencies

Establish blockedBy relationships based on:

**Sequential Dependencies**:
- Chapter N blocks Chapter N+1
- Section M blocks Section M+1 within same chapter
- Chronological event order (flashbacks excepted)

**Knowledge Dependencies**:
- Character introduction blocks appearances
- Location introduction blocks scenes set there
- Event establishment blocks references to it
- Concept definition blocks thematic callbacks

**Graph Dependencies**:
- Relationship creation blocks relationship references
- Timeline placement blocks temporal references

### 5. Specify Required Knowledge

For each task, list the entities and facts that MUST exist in the database before writing:

```json
"required_knowledge": [
  "character:protagonist_id.name",
  "character:protagonist_id.description",
  "character:protagonist_id.background",
  "character:protagonist_id.status",
  "location:setting_id.description",
  "location:setting_id.introduced",
  "event:prior_event_id.sequence",
  "concept:theme_id.description"
]
```

If any required knowledge is missing, the task should be flagged as blocked by a knowledge gap.

### 6. Generate Pre-Write Queries

For each task, specify the database queries to run BEFORE writing to gather context:

**Semantic Search Queries**:
```surql
-- Find thematically similar passages
SELECT * FROM section
WHERE embedding <|5|> $theme_vector
ORDER BY vector::similarity(embedding, $theme_vector) DESC;

-- Find related concepts
SELECT * FROM concept
WHERE embedding <|3|> $concept_vector;
```

**Graph Traversal Queries**:
```surql
-- Character relationships
SELECT * FROM character:$char_id->knows->character;
SELECT * FROM character:$char_id<-appears_in<-section ORDER BY sequence;

-- Source support
SELECT * FROM source WHERE ->supports->concept:$concept_id;

-- Location context
SELECT * FROM location:$loc_id<-located_in<-section;
```

**Timeline Queries**:
```surql
-- Prior events
SELECT * FROM event
WHERE sequence < $current_sequence
ORDER BY sequence DESC
LIMIT 5;

-- Chronological section order
SELECT * FROM section
WHERE chapter = $chapter AND sequence < $current_sequence
ORDER BY sequence;
```

### 7. Specify Post-Write Operations

For each task, define the database operations to execute AFTER writing:

**Content Storage**:
```surql
CREATE section SET
  content = $content,
  embedding = $embedding_vector,
  chapter = $chapter_num,
  sequence = $section_num,
  word_count = $word_count,
  status = 'draft',
  created_at = time::now();
```

**Entity Extraction and Creation**:
```surql
-- Extract and create new entities mentioned in the section
-- (Performed by writer agent using LLM entity extraction)

-- Link existing entities
RELATE section:$section_id->appears_in<-character:$char_ids;
RELATE section:$section_id->located_in->location:$loc_ids;
```

**Relationship Creation**:
```surql
-- Character interactions
RELATE character:$char1->interacts_with->character:$char2
  SET context = $interaction_description;

-- Event sequencing
RELATE event:$event_id->follows->event:$prior_event_id;
```

**Source Citations**:
```surql
-- Link to supporting sources
RELATE section:$section_id->cites->source:$source_ids
  SET claim = $cited_claim;
```

**Timeline Updates**:
```surql
-- Update event sequence
UPDATE event:$event_id SET sequence = $sequence_num;
```

### 8. Define Consistency Checks

For each task, specify constraints that MUST be true before writing:

**Entity State Checks**:
```surql
character:$char_id.status != 'dead'
character:$char_id.introduced = true
location:$loc_id.introduced = true
```

**Relationship Checks**:
```surql
character:$char1->knows->character:$char2 EXISTS
character:$char_id->located_at->location:$loc_id EXISTS
```

**Timeline Checks**:
```surql
event:$prior_event.sequence < $current_sequence
event:$event_id.date < time::now()
```

**Contradiction Checks**:
```surql
-- No conflicting facts
SELECT * FROM section
WHERE ->cites->source->contradicts->source<-cites<-section:$section_id;
```

### 9. Store Tasks in Database

Create task records with all metadata:

```bash
# Tasks are stored in Harness task system via TaskCreate
# Metadata is stored as JSON in the task's metadata field
```

### 10. Delegate to Outline Planner

Invoke the `outline-planner` agent to perform the detailed planning:

```bash
# Load outline-planner agent with context
# Agent will:
# 1. Read BRD structure from database
# 2. Execute corpus coverage queries
# 3. Generate chapter/section tasks
# 4. Determine dependencies and blockedBy
# 5. Specify required knowledge per task
# 6. Generate pre-write queries
# 7. Define post-write operations
# 8. Set consistency checks
# 9. Store tasks via TaskCreate
# 10. Generate report
```

The outline-planner agent has read-only database access and uses the `outlining` and `surrealdb` skills.

## Output Format

Report generated writing tasks to the user:

```
WRITING PLAN GENERATED
======================

BRD: <Book Title>
Structure: <N> chapters, <M> sections
Total Word Target: <X> words

CHAPTER BREAKDOWN
-----------------
Chapter 1: Introduction
  Section 1: Opening (Task #1) - 1,500 words
    Required: character:anna, location:london
    Blocked by: None

  Section 2: Training Begins (Task #2) - 2,000 words
    Required: character:anna, location:beaulieu, event:recruitment
    Blocked by: Task #1

Chapter 2: Deployment
  Section 1: The Flight (Task #3) - 1,800 words
    Required: character:anna, location:france, event:deployment
    Blocked by: Task #2

  Section 2: First Contact (Task #4) - 2,200 words
    Required: character:anna, character:henri, location:safehouse
    Blocked by: Task #3

[... continued for all chapters ...]

TASK SUMMARY
------------
Total Tasks: 32
Ready to Write: 1 (Task #1)
Blocked by Dependencies: 31
Blocked by Knowledge Gaps: 0

DEPENDENCIES GRAPH
------------------
Task #1 → Task #2 → Task #3 → Task #4 → ...
       ↘ Task #5 → Task #6 → ...

KNOWLEDGE REQUIREMENTS
----------------------
All required knowledge present in corpus:
  ✓ 23 characters defined
  ✓ 45 locations described
  ✓ 88 events sequenced
  ✓ 34 concepts documented

NEXT STEPS
----------
Run /bookstrap-write to begin autonomous writing.
Tasks will execute in dependency order.
Use /bookstrap-status to monitor progress.
```

## Statistics to Track

Calculate and report:
- Total chapters and sections planned
- Total target word count
- Tasks ready to write (no blockedBy)
- Tasks blocked by dependencies
- Tasks blocked by knowledge gaps
- Required entities and their availability
- Estimated writing time (sections × avg time)
- Coverage percentage (corpus vs. requirements)

## Implementation Notes

### Agent Delegation

This command is a thin wrapper that:
1. Verifies database connection
2. Checks that BRD exists
3. Verifies sufficient corpus coverage
4. Invokes the `outline-planner` agent
5. Displays the agent's output

The actual planning logic lives in the `outline-planner` agent to keep concerns separated.

### Task Generation Strategies

The outline-planner uses multiple approaches:
- **BRD structure parsing**: Extract chapter/section outline
- **Corpus analysis**: Determine what knowledge supports each section
- **Dependency mapping**: Build task graph from sequential/knowledge dependencies
- **Query generation**: Create semantic/graph/timeline queries per task
- **Metadata enrichment**: Add voice, tone, style requirements from BRD

### Idempotency

Re-running `/bookstrap-plan-write` should:
- Update existing tasks if BRD changed
- Add new tasks if structure expanded
- Not duplicate existing tasks
- Re-evaluate dependencies based on current corpus state
- Update blockedBy if knowledge gaps resolved

### Configuration

Writing task generation can be configured in `bookstrap.config.json`:

```json
{
  "writing": {
    "default_section_words": 2000,
    "min_sources_per_section": 2,
    "require_knowledge_checks": true,
    "auto_generate_queries": true,
    "strict_dependencies": true
  }
}
```

## Error Handling

| Error | Recovery |
|-------|----------|
| BRD not found | Abort with message to run `/bookstrap-init` first |
| BRD missing structure | Abort with message that BRD needs chapter outline |
| Database connection failed | Abort with message to start SurrealDB |
| Insufficient corpus | Warning and flag tasks as blocked by knowledge gaps |
| Outline-planner agent error | Display error, suggest re-running or checking logs |

## Pre-requisites

Before running `/bookstrap-plan-write`:

1. **BRD created**: `/bookstrap-init` must have been run with structure defined
2. **SurrealDB running**: Database must be accessible
3. **Schema initialized**: Database schema loaded
4. **Corpus sufficient**: `/bookstrap-ingest` and `/bookstrap-research` completed
5. **Knowledge gaps resolved**: All high-priority gaps from `/bookstrap-plan-research` addressed

## Related Commands

- `/bookstrap-init` - Create BRD with chapter structure
- `/bookstrap-ingest` - Load initial corpus
- `/bookstrap-plan-research` - Identify and fill knowledge gaps
- `/bookstrap-research` - Execute research tasks to fill gaps
- `/bookstrap-write` - Execute writing tasks generated by this command
- `/bookstrap-status` - View writing progress

## Supporting Agents

| Agent | Role |
|-------|------|
| `outline-planner` | Generates writing tasks with full metadata and dependencies |

## Supporting Skills

| Skill | Purpose |
|-------|---------|
| `outlining/` | Story structure, planning strategies, task generation |
| `surrealdb/` | Database query patterns for coverage analysis |

## Example Usage

```bash
# After research complete, generate writing plan
/bookstrap-plan-write

# Re-run after BRD structure changes
/bookstrap-init  # Update BRD outline
/bookstrap-plan-write  # Regenerate tasks

# Check plan before starting to write
/bookstrap-plan-write
/bookstrap-status
```

## Integration with Writing Loop

This command bridges research and writing:

```
init → ingest → plan-research → research → plan-write → write → edit
                     ↑                          │            │
                     └────── gaps found ────────┴────────────┘
```

Once tasks are generated, `/bookstrap-write` executes them autonomously in dependency order. If new knowledge gaps are discovered during writing, the writer flags them, and the flow returns to research planning.

## Task Metadata Reference

Complete metadata structure for each writing task:

```json
{
  "taskId": "unique-task-id",
  "subject": "Brief task description",
  "description": "Detailed task description with context",
  "activeForm": "Writing Chapter X, Section Y",
  "blockedBy": ["task-id-1", "task-id-2"],
  "metadata": {
    "chapter": 1,
    "section": 1,
    "sequence": 1,
    "target_words": 2000,
    "scene_type": "action|dialogue|exposition|description",
    "required_knowledge": [
      "entity_type:entity_id.field"
    ],
    "pre_queries": [
      "SurrealQL query string"
    ],
    "post_writes": [
      "SurrealQL write operation"
    ],
    "consistency_checks": [
      "SurrealQL boolean expression"
    ],
    "voice_requirements": {
      "pov": "first|third_limited|third_omniscient",
      "tense": "past|present",
      "tone": "tone_description",
      "comparable": "comparable author/work"
    }
  }
}
```

This metadata structure enables the `writer` agent to:
- Gather necessary context via pre_queries
- Verify consistency before writing
- Write grounded in retrieved knowledge
- Store results with proper relationships via post_writes
- Flag gaps if required_knowledge is missing
