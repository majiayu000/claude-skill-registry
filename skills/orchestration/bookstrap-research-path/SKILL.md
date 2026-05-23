---
name: bookstrap-research-path
description: Execute research workflow orchestration - processes pending research tasks sequentially
invoke: skill
category: orchestration
---

# Research Path Orchestrator

Execute the research workflow end-to-end, processing pending research tasks sequentially.

## What It Does

This orchestrator command:

1. **Queries pending research tasks** from the database
2. **Invokes the researcher agent** for each task sequentially
3. **Verifies gap resolution** after each source ingestion
4. **Tracks progress** and handles failures
5. **Reports completion** statistics

## Usage

```bash
/bookstrap-research-path
```

### Optional Parameters

```bash
/bookstrap-research-path --max-tasks 5
/bookstrap-research-path --priority high
/bookstrap-research-path --gap-id gap_123
```

## Workflow

### 1. Query Pending Research Tasks

```sql
SELECT * FROM task
WHERE type = 'research'
AND status = 'pending'
ORDER BY priority DESC, created_at ASC
LIMIT $max_tasks;
```

### 2. For Each Task

#### a. Mark Task In Progress

```
TaskUpdate: {taskId: "[task-id]", status: "in_progress"}
```

#### b. Invoke Researcher Agent

```
Skill: {skill: "researcher", args: "--task-id [task-id]"}
```

The researcher agent will:
- Search for sources
- Evaluate reliability
- Ingest content
- Extract entities
- Create relationships
- Resolve knowledge gap

#### c. Verify Gap Resolution

After researcher completes, verify the gap was adequately resolved:

```python
from scripts.researcher_methods import ResearcherMethods

verification_queries = [
    {
        'query': "SELECT * FROM source WHERE id = $source_id",
        'min_results': 1,
        'description': 'Source was created'
    },
    {
        'query': "SELECT * FROM chunk WHERE source = $source_id",
        'min_results': 3,
        'description': 'Sufficient chunks created'
    },
    {
        'query': "SELECT * FROM [character, location, event, concept] WHERE ->supports<-source.id = $source_id",
        'min_results': 1,
        'description': 'Entities extracted'
    }
]

is_resolved, issues = researcher.verify_gap_resolution(gap_id, verification_queries)
```

#### d. Update Task Status

If verification passes:
```
TaskUpdate: {taskId: "[task-id]", status: "completed"}
```

If verification fails:
```
TaskUpdate: {taskId: "[task-id]", status: "blocked", metadata: {issues: [...]}}
```

### 3. Report Progress

After processing all tasks, report:

```
RESEARCH PATH COMPLETE
======================

Tasks processed: [count]
Tasks completed: [count]
Tasks blocked: [count]
Total sources ingested: [count]
Total entities extracted: [count]
Knowledge gaps resolved: [count]

NEXT STEPS
----------
- Run /bookstrap-status to see updated project state
- Run /bookstrap-plan-write to generate writing tasks
- Run /bookstrap-write to begin writing grounded in new research
```

## Error Handling

### Task Blocked

If a research task cannot be completed:
- Mark task as `blocked` with reason
- Continue to next task
- Report blocked tasks at end

### API Rate Limits

If search API rate limit hit:
- Wait appropriate backoff period
- Retry task
- If still failing, mark as blocked

### No Sources Found

If no reliable sources found after thorough search:
- Mark task as blocked
- Suggest alternative research strategies
- Recommend manual research

## Configuration

Respects settings from `bookstrap.config.json`:

```json
{
  "orchestration": {
    "research_path": {
      "max_tasks_per_run": 10,
      "require_verification": true,
      "continue_on_error": true,
      "min_source_reliability": "medium"
    }
  }
}
```

## Example Output

```
Starting research path orchestration...

Processing task 1 of 3: "SOE training protocols 1943"
├─ Searching for sources...
├─ Found 3 candidate sources
├─ Evaluating reliability...
├─ Ingesting: "The Secret History of SOE" (high reliability)
├─ Extracting entities... 12 entities found
├─ Creating relationships... 8 relationships created
├─ Verifying gap resolution... PASSED
└─ Task completed ✓

Processing task 2 of 3: "Wireless operator equipment specifications"
├─ Searching for sources...
├─ Found 1 candidate source
├─ Evaluating reliability...
├─ Ingesting: "SOE Equipment Manual 1943" (high reliability)
├─ Extracting entities... 5 entities found
├─ Creating relationships... 3 relationships created
├─ Verifying gap resolution... PASSED
└─ Task completed ✓

Processing task 3 of 3: "French resistance network structure Lyon"
├─ Searching for sources...
├─ Found 0 reliable sources
├─ Task marked as BLOCKED
└─ Reason: No sources found meeting reliability threshold

RESEARCH PATH COMPLETE
======================

Tasks processed: 3
Tasks completed: 2
Tasks blocked: 1
Total sources ingested: 2
Total entities extracted: 17
Knowledge gaps resolved: 2

BLOCKED TASKS
-------------
- Task 3: "French resistance network structure Lyon"
  Reason: No sources found meeting reliability threshold
  Suggestion: Try more specific search terms or lower reliability threshold

NEXT STEPS
----------
Run /bookstrap-plan-write to generate writing tasks using new research
```

## Integration with Other Commands

### Before

- `/bookstrap-plan-research` - Generate research tasks to feed this orchestrator

### After

- `/bookstrap-status` - Check updated corpus state
- `/bookstrap-query` - Verify specific knowledge is now available
- `/bookstrap-plan-write` - Generate writing tasks grounded in research
- `/bookstrap-write` - Begin writing with full knowledge coverage

## Best Practices

1. **Run plan-research first** to generate research tasks
2. **Process in batches** if many tasks (use --max-tasks)
3. **Monitor for blocked tasks** and resolve manually if needed
4. **Verify knowledge coverage** before proceeding to writing
5. **Commit after completion** to save research progress

## Implementation Notes

This orchestrator is implemented as a skill that:
- Uses `TaskList` to find pending research tasks
- Invokes `researcher` agent skill for each task
- Uses `researcher_methods.py` for verification
- Updates tasks using `TaskUpdate`
- Reports progress to user

The orchestrator does NOT run research itself - it coordinates the researcher agent.
