---
name: bookstrap-write-path
description: Execute writing workflow orchestration - writes sections sequentially from outline
invoke: skill
category: orchestration
---

# Write Path Orchestrator

Execute the writing workflow end-to-end, writing sections sequentially from the outline.

## What It Does

This orchestrator command:

1. **Queries pending write tasks** from the database (ordered by sequence)
2. **Invokes the writer agent** for each section sequentially
3. **Verifies completion** after each section
4. **Handles knowledge gaps** by triggering research
5. **Tracks progress** through the outline
6. **Reports completion** statistics

## Usage

```bash
/bookstrap-write-path
```

### Optional Parameters

```bash
/bookstrap-write-path --chapter 3
/bookstrap-write-path --max-sections 5
/bookstrap-write-path --start-sequence 12
```

## Workflow

### 1. Query Pending Write Tasks

```sql
SELECT * FROM task
WHERE type = 'write'
AND status = 'pending'
ORDER BY sequence ASC
LIMIT $max_sections;
```

### 2. For Each Section Task

#### a. Mark Task In Progress

```
TaskUpdate: {taskId: "[task-id]", status: "in_progress"}
```

#### b. Invoke Writer Agent

```
Skill: {skill: "writer", args: "--task-id [task-id]"}
```

The writer agent will:
- Run pre-write queries
- Check consistency constraints
- Detect knowledge gaps (if any)
- Write the section (if no gaps)
- Extract entities
- Generate embeddings
- Create citations
- Save to manuscript

#### c. Check for Knowledge Gaps

If writer flagged a knowledge gap:

```sql
SELECT * FROM knowledge_gap
WHERE section_ref = $section_id
AND resolved = false
ORDER BY created_at DESC
LIMIT 1;
```

If gap found:
1. **Mark section task as blocked**
2. **Trigger research path** for the gap
3. **Pause write path** until gap resolved
4. **Report to user** what research is needed

#### d. Verify Section Completion

Check that section was properly stored:

```python
from scripts.writer_methods import WriterMethods

# Verify section exists in database
section = db.query(f"SELECT * FROM section WHERE id = $section_id")

# Verify embedding generated
has_embedding = section[0].get('embedding') is not None

# Verify entities extracted
entity_count = db.query(f"SELECT count() FROM [character, location] WHERE ->appears_in<-section.id = $section_id")

# Verify citations created
citation_count = db.query(f"SELECT count() FROM section->cites->source WHERE section.id = $section_id")
```

#### e. Update Task Status

If verification passes:
```
TaskUpdate: {taskId: "[task-id]", status: "completed"}
```

If blocked on knowledge gap:
```
TaskUpdate: {
    taskId: "[task-id]",
    status: "blocked",
    metadata: {gap_id: "[gap-id]", gap_question: "[question]"}
}
```

### 3. Handle Gaps

When a knowledge gap blocks writing:

```
KNOWLEDGE GAP DETECTED
======================

Gap: "Need details about wireless operator training protocols in 1943"
Context: Required for Chapter 3, Section 2

Triggering research path...
Run /bookstrap-research-path to resolve this gap
Or continue with /bookstrap-write-path --skip-blocked
```

### 4. Report Progress

After processing all tasks (or hitting a gap), report:

```
WRITE PATH PROGRESS
===================

Sections processed: [count]
Sections completed: [count]
Sections blocked: [count]
Total words written: [count]
Citations created: [count]
Entities extracted: [count]

MANUSCRIPT STATUS
-----------------
Chapter 1: [completed/in-progress/pending]
Chapter 2: [completed/in-progress/pending]
Chapter 3: [in-progress] (blocked on section 3.2)

NEXT STEPS
----------
- Resolve knowledge gap to continue Chapter 3
- Run /bookstrap-research-path
- Or run /bookstrap-edit to review completed sections
```

## Error Handling

### Knowledge Gap Detected

When writer discovers missing knowledge:
- **Pause write path**
- **Create knowledge gap record**
- **Generate research task**
- **Report to user**
- User must run `/bookstrap-research-path` to proceed

### Consistency Check Failed

If pre-write consistency check fails:
- **Mark task as blocked**
- **Report which constraint failed**
- **Suggest fix** (update entity, write missing intro)
- User must resolve manually

### Embedding Generation Failed

If embedding cannot be generated:
- **Retry once**
- **If still fails, report configuration issue**
- **Do not proceed** (section needs embedding for queries)

## Configuration

Respects settings from `bookstrap.config.json`:

```json
{
  "orchestration": {
    "write_path": {
      "max_sections_per_run": 10,
      "pause_on_gap": true,
      "auto_trigger_research": false,
      "require_verification": true,
      "commit_after_each": true
    }
  }
}
```

## Example Output

```
Starting write path orchestration...

Processing section 1 of 5: Chapter 3, Section 1 - "Arrival"
├─ Running pre-write queries...
├─ Consistency checks... PASSED
├─ Knowledge coverage... SUFFICIENT
├─ Writing section... 1,247 words
├─ Generating embedding... Done
├─ Extracting entities... 3 characters, 2 locations
├─ Creating citations... 4 sources cited
├─ Saving to manuscript/chapter-03-rising-action/section-01-arrival.md
└─ Section completed ✓

Processing section 2 of 5: Chapter 3, Section 2 - "Confrontation"
├─ Running pre-write queries...
├─ Consistency checks... PASSED
├─ Knowledge coverage... INSUFFICIENT
├─ Gap detected: "Wireless operator training protocols 1943"
└─ Section BLOCKED (gap flagged)

WRITE PATH PAUSED
=================

Reason: Knowledge gap detected
Gap: "Need details about wireless operator training protocols in 1943"
Context: Required for Chapter 3, Section 2 confrontation scene

Created research task: task_789
Created knowledge gap: gap_456

NEXT STEPS
----------
1. Run /bookstrap-research-path to resolve the gap
2. Once resolved, resume with /bookstrap-write-path --start-sequence 13

PROGRESS SO FAR
---------------
Sections completed: 1
Total words: 1,247
Next section: 3.2 (blocked)
```

## Integration with Other Commands

### Before

- `/bookstrap-plan-write` - Generate write tasks from outline
- `/bookstrap-research-path` - Ensure knowledge coverage

### During

- May trigger `/bookstrap-research-path` if gaps discovered

### After

- `/bookstrap-status` - Check manuscript progress
- `/bookstrap-edit` - Review completed sections
- `/bookstrap-export-chapter` - Export completed chapters

## Best Practices

1. **Run plan-write first** to generate section tasks
2. **Complete research path** before writing to minimize gaps
3. **Write in sequence** to maintain narrative flow
4. **Commit after each section** (automatic if configured)
5. **Review regularly** with /bookstrap-edit
6. **Resolve gaps promptly** to maintain momentum

## Recovery from Interruption

If orchestrator is interrupted:

```bash
# Resume from last completed section
/bookstrap-write-path --start-sequence [next-sequence]

# Or skip blocked sections temporarily
/bookstrap-write-path --skip-blocked
```

The orchestrator remembers progress via task status in database.

## Implementation Notes

This orchestrator is implemented as a skill that:
- Uses `TaskList` to find pending write tasks
- Invokes `writer` agent skill for each section
- Uses `writer_methods.py` for verification
- Detects gaps and triggers research coordination
- Updates tasks using `TaskUpdate`
- Commits after each section if configured
- Reports progress and blocks to user

The orchestrator does NOT write content itself - it coordinates the writer agent.
