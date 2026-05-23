---
name: todoist-task-creator
description: Create well-structured Todoist tasks with Description and Definition of Done sections. Use this skill when creating new Todoist tasks to ensure they have enough context for any team member to understand and clear completion criteria.
---

# Todoist Task Creator

Create tasks with consistent, actionable structure.

## Task Format

Every task description MUST include two sections:

### Description
Context anyone on the team could understand. Include:
- What problem or goal this addresses
- Why it matters (motivation)
- Any relevant background or links

### Definition of Done
Specific, measurable completion criteria. Use checkboxes:
- `- [ ]` for each criterion
- Be concrete (e.g., "accuracy >= 0.85" not "good accuracy")
- Include verification steps where applicable

## Example

**Task title:** Test validity of noise experiment data

**Description:**
```
## Description
Validate the noise experiment data quality before proceeding with analysis. Need to confirm we have statistically meaningful sample sizes and that the data distributions match expected patterns from the experimental design.

## Definition of Done
- [ ] Count total samples per noise level and confirm n >= 30 per condition
- [ ] Plot distribution of results and verify no obvious anomalies
- [ ] Check that accuracy values are in [0, 1] range
- [ ] Verify all expected noise conditions are present in the data
- [ ] Document findings in a brief summary
```

## Creating Tasks

**Important**: The Todoist MCP tool often returns 401 errors even with correct tokens. **Use the REST API directly via curl instead** - it's more reliable.

### Preferred: REST API

```bash
# Always source .env first to get TODOIST_API_TOKEN
source /Users/terrytong/Documents/CCG/ToolProj/.env && curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Task title here",
    "description": "## Description\n...\n\n## Definition of Done\n- [ ] ...",
    "project_id": "2363714490",
    "priority": 2
  }'
```

### Other REST API Operations

```bash
# Get tasks
source .env && curl -s "https://api.todoist.com/rest/v2/tasks?project_id=2363714490" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"

# Delete a task
source .env && curl -s -X DELETE "https://api.todoist.com/rest/v2/tasks/{task_id}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"

# Complete a task
source .env && curl -s -X POST "https://api.todoist.com/rest/v2/tasks/{task_id}/close" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

### MCP Tool (Fallback)

The MCP tool `mcp__todoist__todoist_create_task` can be tried but may fail with 401. If it fails, fall back to REST API.

Priority levels: 1 (normal) to 4 (urgent).

## Project IDs

| Project | ID |
|---------|-----|
| Inbox | 2363711982 |
| Astra Research Todo | 2363714334 |
| Research | 2363714490 |
| Reading List | 2364338633 |

## Integration with Research Executor

The **research-executor** agent uses this skill to create tasks for:
- Paper writeup tasks after successful experiments
- Follow-up experiment ideas discovered during execution
- Documentation tasks at experiment milestones

**Example for successful experiment:**
```
## Description
Write up results from exp/cot-faithfulness experiment. Code vs NL representation comparison showed significant MI difference (1.2 bits avg).

## Definition of Done
- [ ] Draft results section with key figures
- [ ] Include methodology description
- [ ] Add statistical analysis (p-values, effect sizes)
- [ ] Update Notion with experiment entry
```
