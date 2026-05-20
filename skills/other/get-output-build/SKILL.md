---
name: get-output-build
description: Fetch VectorShift pipeline outputs by task_id (or span_id) and pass them to a builder skill
user_invocable: true
arguments: "<task_id> [<task_id2> ...] --builder <skill_command>"
allowed-tools: Read, Write, Edit, Shell, Glob, Grep
---

# Get Output & Build

Fetches completed VectorShift pipeline outputs using task_id(s) and chains them into a builder skill for processing.

**Note:** `task_id` and `span_id` are interchangeable. VectorShift confirmed that the `task_id` returned when you submit a job can be used directly to query results.

## Slash Command Usage

```
/get-output-build <task_id> --builder "<skill_command>"
```

**Examples:**
- `/get-output-build 6961e088862a01eeb682196b --builder "/process-ngm-lectures 1-OeTj2AseENWJFN-0jKz8tZqFDkLsFR2 --module-id module-1"`
- `/get-output-build task1 task2 task3 --builder "/process-ngm-lectures 1ABC123 --module-id foundations"`

## Required Configuration

### Environment Variables
```bash
VECTORSHIFT_API_KEY=sk_6L1cRGLL5qN2d9rjViLVAFr6ATqE1OAE78L5bgYltWBkryoE
```

## How It Works

### Step 1: Fetch Pipeline Output

For each `task_id`, make a GET request to:
```
GET https://api.vectorshift.ai/v1/pipeline/6961308d6fdec16163ee0e2f/run/status/{task_id}
Authorization: Bearer {VECTORSHIFT_API_KEY}
```

**Note:** `task_id` (from job submission) works interchangeably with `span_id` for status queries.

**Response (completed):**
```json
{
  "task_id": "...",
  "status": "completed",
  "result": {
    "content_analysis": "...",
    "lecture_json": "{ ... JSON lecture object ... }",
    "research_dossier": "...",
    "slide_blueprint": "...",
    "transcript": "..."
  }
}
```

### Step 2: Extract Output Data

The pipeline returns multiple outputs. The key output for lecture building is `lecture_json`.

```python
import json
import re

def extract_json(raw_output):
    """Extract JSON from VectorShift output (may be wrapped in markdown fences)"""
    content = raw_output.strip()
    if content.startswith('```json'):
        content = content[7:]
    elif content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]
    
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        return json.loads(match.group())
    return None
```

### Step 3: Pass to Builder Skill

The fetched outputs are passed to the builder skill command. The builder skill receives:
- The extracted `lecture_json` data
- Any additional parameters from the original command

## Execution Workflow

```
User: /get-output-build abc123 def456 --builder "/process-ngm-lectures 1-OeTj --module-id module-1"

Step 1: Fetch outputs from VectorShift
  GET /v1/pipeline/.../run/status/abc123 → lecture data
  GET /v1/pipeline/.../run/status/def456 → lecture data

Step 2: Collect all lecture JSON outputs
  - Lecture 1: { "title": "...", "sections": [...] }
  - Lecture 2: { "title": "...", "sections": [...] }

Step 3: Pass to process-ngm-lectures
  - Save lecture JSONs to content/ngm-lectures/{module-id}/
  - Update registry.ts with new imports and entries
```

## Python Script

Use the provided `fetch_outputs.py` script:

```bash
python3 .claude/skills/get-output-build/fetch_outputs.py \
  --task-ids abc123 def456 ghi789 \
  --output-dir /tmp/vs-outputs
```

This creates JSON files for each task_id in the output directory.

**Note:** The script accepts both `--task-ids` and `--span-ids` (they're equivalent).

## Error Handling

| Status | Action |
|--------|--------|
| `completed` | Extract `result` and continue |
| `in_progress` | Wait and retry (poll every 10s) |
| `failed` | Log error and skip this task_id |
| HTTP 404 | Invalid task_id, skip |
| HTTP 401 | Invalid API key |

## Integration with process-ngm-lectures

When using with `/process-ngm-lectures`, the workflow becomes:

1. **You already have task_ids** from a previous VectorShift run
2. **Run this skill** to fetch the completed outputs
3. **Outputs are saved** to `content/ngm-lectures/{module-id}/`
4. **Registry is updated** automatically

### Bypassing Google Drive

This skill is useful when:
- Pipeline jobs were submitted earlier and you have the task_ids
- You want to resume a failed run using cached task_ids
- Pipeline outputs are ready but weren't processed

## File Locations

| File | Purpose |
|------|---------|
| `.claude/skills/get-output-build/SKILL.md` | This documentation |
| `.claude/skills/get-output-build/fetch_outputs.py` | Output fetching script |
| `content/ngm-lectures/{module-id}/` | Where lecture JSONs are saved |
| `content/ngm-lectures/registry.ts` | Module/lecture registry |

## API Details

| Property | Value |
|----------|-------|
| Base URL | `https://api.vectorshift.ai/v1` |
| Pipeline ID | `6961308d6fdec16163ee0e2f` |
| Status Endpoint | `GET /pipeline/{id}/run/status/{task_id}` |
| Auth | `Authorization: Bearer {api_key}` |

**Note:** `task_id` and `span_id` are interchangeable in the status endpoint.

## Example Complete Session

```
User: /get-output-build 6961e088862a01eeb682196b 6961e089862a01eeb682196c --builder "/process-ngm-lectures 1-OeTj2AseENWJFN-0jKz8tZqFDkLsFR2 --module-id module-1"

Claude: I'll fetch the VectorShift outputs and process them.

Step 1: Fetching outputs from VectorShift API...
  task_id 6961e088862a01eeb682196b: ✓ completed
    → Lecture: "Cellular Senescence and the SASP"
  task_id 6961e089862a01eeb682196c: ✓ completed
    → Lecture: "The SHIFT Framework"

Step 2: Extracting lecture JSON data...
  Extracted 2 lectures

Step 3: Executing builder command...
  Running: /process-ngm-lectures (skip to Phase 4)
  
  Saving lecture JSON files...
    Saved: content/ngm-lectures/module-1/cellular-senescence-and-the-sasp.json
    Saved: content/ngm-lectures/module-1/the-shift-framework.json
  
  Updating registry.ts...
    Added 2 imports
    Updated module-1 entry

Step 4: Preview URLs ready!
  http://localhost:3000/preview/ngm/module-1/cellular-senescence-and-the-sasp
  http://localhost:3000/preview/ngm/module-1/the-shift-framework
```
