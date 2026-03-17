---
name: process-ngm-lectures
description: Process Google Docs from Drive through VectorShift pipeline and publish to NGM preview system
user_invocable: true
arguments: "<folder_id> --module-id <id> [--module-title <title>] [--max-concurrent N]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__google-drive__list_files, mcp__google-drive__export_google_doc
---

# Process NGM Lectures

End-to-end workflow to process Google Docs from a Drive folder through the HTML-to-Lecture-JSON-SVG VectorShift pipeline and publish them to the NGM preview system.

## Slash Command Usage

```
/process-ngm-lectures <folder_id> --module-id <id> [options]
```

**Examples:**
- `/process-ngm-lectures 1-OeTj2AseENWJFN-0jKz8tZqFDkLsFR2 --module-id module-1`
- `/process-ngm-lectures 1ABC123 --module-id foundations --module-title "Foundations of Longevity"`

## Required Configuration

### Environment Variables
```bash
VECTORSHIFT_API_KEY=sk_fkyJyb86LyHQR9IaomQq52xCdL7a31uyYbuHDxuqoTVqdf6n
```

### Google Drive MCP Server
The MCP server must be configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["ts-node", "mcp-servers/google-drive/src/index.ts"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_PATH": "/path/to/service-account.json"
      }
    }
  }
}
```

Service account must have Viewer access to the Google Drive folder.

## Complete Workflow

### Phase 1: List Google Docs in Folder

Use the Google Drive MCP server to list files:

```typescript
// MCP tool call
mcp__google-drive__list_files({ folder_id: "<folder_id>" })
```

Filter results to only Google Docs:
```javascript
const docs = files.filter(f => f.mimeType === 'application/vnd.google-apps.document');
```

### Phase 2: Export Google Docs as HTML

For each Google Doc, export as HTML:

```typescript
// MCP tool call
mcp__google-drive__export_google_doc({ file_id: "<doc_id>", format: "html" })
```

**Alternative via googleapis (if MCP not available):**
```javascript
const { google } = require('googleapis');
const drive = google.drive({ version: 'v3', auth });

const response = await drive.files.export({
  fileId: docId,
  mimeType: 'text/html'
});
const htmlContent = response.data;
```

### Phase 3: Run VectorShift Pipeline

#### API Configuration (CRITICAL)
```
Base URL: https://api.vectorshift.ai/v1  (NOT /api)
Pipeline ID: 6961308d6fdec16163ee0e2f
Auth Header: Authorization: Bearer {api_key}
```

#### Submit Job
```bash
POST https://api.vectorshift.ai/v1/pipeline/{pipeline_id}/run
Headers:
  Authorization: Bearer {api_key}
  Content-Type: application/json
Body:
{
  "inputs": {
    "html_content": "<exported HTML>",
    "lecture_title": "Lecture Title",
    "module_name": "module-id"
  },
  "background": true
}
Response:
{
  "task_id": "6961e088862a01eeb682196b",
  "status": "in_progress"
}
```

#### Poll for Completion
```bash
GET https://api.vectorshift.ai/v1/pipeline/{pipeline_id}/run/status/{task_id}
Headers:
  Authorization: Bearer {api_key}

Response (in progress):
{
  "task_id": "...",
  "status": "in_progress"
}

Response (completed):
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

#### Bulk Processing Script
Use the provided Python script for parallel processing:
```bash
VECTORSHIFT_API_KEY="sk_xxx" python3 \
  .claude/skills/process-ngm-lectures/ngm_bulk_processor.py \
  --module-id "module-1" \
  --lectures-file "/tmp/lectures.json" \
  --output-dir "content/ngm-lectures" \
  --max-concurrent 5
```

Input JSON format:
```json
[
  {
    "lecture_number": 3,
    "lecture_title": "The SHIFT Framework",
    "html_content": "<html>...</html>"
  }
]
```

### Phase 4: Extract and Save Lecture JSON

The `lecture_json` field contains a JSON string (often wrapped in markdown code fences). Extract and save:

```python
import json
import re

def extract_json(raw_output):
    # Remove markdown code fences if present
    content = raw_output.strip()
    if content.startswith('```json'):
        content = content[7:]
    elif content.startswith('```'):
        content = content[3:]

    # Find JSON object
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        return json.loads(match.group())
    return None

# Save to file
lecture_data = extract_json(result["lecture_json"])
with open(f"content/ngm-lectures/{module_id}/lecture-{n}.json", "w") as f:
    json.dump(lecture_data, f, indent=2)
```

### Phase 5: Update Registry

Edit `content/ngm-lectures/registry.ts`:

#### Add Imports
```typescript
// Add after existing imports
import module1Lecture3 from './module-1/lecture-3.json';
import module1Lecture4 from './module-1/lecture-4.json';
// ... etc
```

#### Add Module Entry
```typescript
export const ngmModules: Record<string, NGMModule> = {
  'module-1': {
    id: 'module-1',
    title: 'Foundations of Longevity Medicine',
    description: 'Core concepts in cellular aging and hallmarks',
    order: 1,
    status: 'preview',
    lectures: [
      { id: 'lecture-3', title: 'The SHIFT Framework', order: 1, lecture: module1Lecture3 as Lecture },
      { id: 'lecture-4', title: 'Systems-thinking in Medicine', order: 2, lecture: module1Lecture4 as Lecture },
      // ... etc
    ],
  },
};
```

### Phase 6: Verify and Preview

Preview URLs:
```
Module Catalog: http://localhost:3000/preview/ngm
Module Index:   http://localhost:3000/preview/ngm/{module-id}
Lecture View:   http://localhost:3000/preview/ngm/{module-id}/lecture-{n}
```

## Known Issues and Troubleshooting

### Issue 1: Pipeline Timeout (15+ minutes)
**Symptom:** All lectures timeout after 15 minutes
**Cause:** Large HTML content (~100KB) takes longer to process
**Solution:** Increase `MAX_POLL_MINUTES` in ngm_bulk_processor.py to 30-45 minutes

### Issue 2: API Returns 404
**Symptom:** HTTP 404 on pipeline run
**Cause:** Wrong API endpoint format
**Solution:** Ensure using `/v1/pipeline/{id}/run` NOT `/api/pipelines/run`

### Issue 3: Polling Shows "Processing" but Pipeline Completed
**Symptom:** VectorShift UI shows completed but script keeps polling
**Cause:** Incorrect response parsing
**Solution:** Check for `status == "completed"` and get outputs from `result` object directly

### Issue 4: JSON Extraction Fails
**Symptom:** "Could not extract JSON" error
**Cause:** VectorShift wraps JSON in markdown code fences
**Solution:** Use the `extract_json()` function to strip fences and find JSON object

### Issue 5: Output Capture Fails (Fallback Pattern)
**Symptom:** Pipeline completes in VectorShift UI but output wasn't captured locally
**Cause:** Timeout, network issues, or process interruption
**Solution:** The **task_id fallback** triggers automatically—no manual intervention required.

**VectorShift confirmed:** The `task_id` returned when submitting a job can be used directly to query results (task_id == span_id for queries).

The bulk processor stores all `task_id` values and automatically retries failed fetches. For manual recovery:

```bash
# Use task_id directly (same as span_id)
python3 "/Users/anantvinjamoori/Vectorshift Pipelines/cli/fetch_by_span_id.py" \
    6961308d6fdec16163ee0e2f \
    <TASK_ID> \
    --output-dir ./output
```

See [vectorshift-pipeline-deployment.md](../vectorshift-pipeline-deployment.md#output-retrieval-fallback-pattern) for full documentation.

## File Locations

| File | Purpose |
|------|---------|
| `.claude/skills/process-ngm-lectures/SKILL.md` | This skill documentation |
| `.claude/skills/process-ngm-lectures/ngm_bulk_processor.py` | Parallel processing script |
| `content/ngm-lectures/registry.ts` | Module/lecture registry |
| `content/ngm-lectures/{module-id}/lecture-{n}.json` | Lecture JSON files |
| `mcp-servers/google-drive/` | Google Drive MCP server |
| `src/views/preview/NGMCourseCatalog.tsx` | Catalog page component |
| `src/views/preview/NGMModuleIndex.tsx` | Module index component |
| `src/views/preview/NGMLectureViewer.tsx` | Lecture viewer component |

## Google Drive Folder Structure

NGM Courses root folder: `1KJaqJ3EGA9rItcsWICeIWe5PVeMpI1Lz`

| Module | Folder ID |
|--------|-----------|
| Module 1 [EN] | `1-OeTj2AseENWJFN-0jKz8tZqFDkLsFR2` |
| Module 2 [EN] | `123LK1CzHDDrqT4xafmlZ6HOWnRl6El2a` |
| Module 3 [EN] | `1a_Y9wvQMpTE78U5CDFScwHeR2gTRElCs` |
| Module 4 [EN] | `1dbJvTtmu4CLBfhtJFq9iNvkRVsQt1Hrt` |
| Module 5 [EN] | `1S-AAYPyA1e8Xap-7S9c0BqhhHedDxHcl` |
| Module 6 [EN] | `1VplISQTl9nNVR5jwgis_jmMo8FKkEsF3` |
| Module 7 [EN] | `1oNge81f36H7cZRtjcnk6VHj3AUFNqDbA` |
| Module 8 [EN] | `1tH8WR2NPlxECTrM0H0hfcxALkDkIdXhO` |
| Module 9 [EN] | `1B2GNBtDIYc83SqHObEcpw0UBsdD8pgg3` |
| Module 10 [EN] | `1s7yghBxQSvRVswDYpUaYWQpmI66qB4Is` |
| Module 11 [EN] | `1pYI8HrMlrQYdenMbdgmWifB0rPOQ0lU5` |
| Module 12 [EN] | `1FmOZe9ZHtZU4xrjV6MuZLfGW8l2a0mhx` |

## VectorShift Pipeline Details

| Property | Value |
|----------|-------|
| Pipeline ID | `6961308d6fdec16163ee0e2f` |
| Pipeline Name | HTML to Lecture JSON (SVG Diagrams) |
| Inputs | `html_content`, `lecture_title`, `module_name` |
| Outputs | `content_analysis`, `lecture_json`, `research_dossier`, `slide_blueprint`, `transcript` |

## Example Complete Session

```
User: /process-ngm-lectures 1-OeTj2AseENWJFN-0jKz8tZqFDkLsFR2 --module-id module-1

Claude: I'll process Module 1 lectures from Google Drive.

Step 1: Listing files in folder...
Found 18 Google Docs (Lessons 3-20)

Step 2: Exporting HTML content...
  Lesson 3: The SHIFT framework (98KB)
  Lesson 4: Systems-thinking in medicine (107KB)
  ... (18 total)

Step 3: Running VectorShift pipeline (5 concurrent)...
[00:30] Processing: 18
[05:00] Processing: 15 | Completed: 3
[10:00] Processing: 8 | Completed: 10
[15:00] Processing: 2 | Completed: 16
[18:00] Completed: 18

Step 4: Saving lecture JSON files...
  Saved: content/ngm-lectures/module-1/lecture-3.json
  Saved: content/ngm-lectures/module-1/lecture-4.json
  ... (18 total)

Step 5: Updating registry.ts...
  Added 18 imports
  Added module-1 entry with 18 lectures

Step 6: Preview URLs ready!
  Module: http://localhost:3000/preview/ngm/module-1
  Lectures:
    - http://localhost:3000/preview/ngm/module-1/lecture-3
    - http://localhost:3000/preview/ngm/module-1/lecture-4
    ... (18 total)
```

## Handoff Notes for Engineer

### Current Status
- Google Drive integration: Working (via googleapis)
- VectorShift API format: Verified correct (`/v1/pipeline/{id}/run`)
- Bulk processor: Submits jobs successfully, but times out waiting for completion
- Polling logic: Fixed to check `status == "completed"` and extract from `result` object

### Remaining Issues to Fix
1. **Timeout**: Increase `MAX_POLL_MINUTES` from 15 to 30-45 minutes
2. **Test end-to-end**: Run full workflow and verify JSON extraction works
3. **Registry update**: Test the TypeScript import generation

### Testing Commands
```bash
# Test single API call
python3 << 'EOF'
import urllib.request, json
api_key = "sk_fkyJyb86LyHQR9IaomQq52xCdL7a31uyYbuHDxuqoTVqdf6n"
req = urllib.request.Request(
    "https://api.vectorshift.ai/v1/pipeline/6961308d6fdec16163ee0e2f/run",
    data=json.dumps({"inputs": {"html_content": "<html><body>Test</body></html>", "lecture_title": "Test", "module_name": "test"}, "background": True}).encode(),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=60) as r:
    print(json.loads(r.read()))
EOF

# Check task status
python3 << 'EOF'
import urllib.request, json
api_key = "sk_fkyJyb86LyHQR9IaomQq52xCdL7a31uyYbuHDxuqoTVqdf6n"
task_id = "YOUR_TASK_ID"
req = urllib.request.Request(
    f"https://api.vectorshift.ai/v1/pipeline/6961308d6fdec16163ee0e2f/run/status/{task_id}",
    headers={"Authorization": f"Bearer {api_key}"}
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
    print("Status:", data.get("status"))
    if data.get("result"):
        print("Result keys:", list(data["result"].keys()))
EOF
```
