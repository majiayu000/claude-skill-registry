---
name: video-query
description: "Analyzes video files using Google Gemini API and answers questions about content. Triggers on keywords: video query, analyze video, video analysis, query video"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Video Query Command

Analyze a video file using Google Gemini API and answer questions about its content.

**Video Path:** $1
**Query:** $2

## Pre-Flight Checks

1. **Verify Video Path Provided**
   - If `$1` is empty: STOP with "Error: Video path required. Usage: /video-query <video-path> <query>"

2. **Verify Query Provided**
   - If `$2` is empty: STOP with "Error: Query required. Usage: /video-query <video-path> <query>"

3. **Verify Script Exists**
   - Resolve script path from `${CLAUDE_PLUGIN_ROOT}`
   - Check that script exists at resolved path
   - If not found: STOP with "Error: video-query.py script not found in plugin"

4. **Verify GEMINI_API_KEY**
   - Check if GEMINI_API_KEY environment variable is set
   - If not set: STOP with "Error: GEMINI_API_KEY not set. Export it: `export GEMINI_API_KEY=your_key`"

## Execution

1. **Resolve Script Path**
   - Use plugin-root path resolution:
   ```bash
   SCRIPT_PATH="${CLAUDE_PLUGIN_ROOT}/scripts/video-query.py"
   ```

2. **Run Video Query Script**
   - Execute: `uv run "$SCRIPT_PATH" "$1" "$2" --json`
   - Capture output

3. **Parse JSON Response**
   - Extract: video_path, query, model, response, usage, cost, time_seconds

4. **Format and Present Results**

Present results as:

```
## Video Analysis Results

**Video:** <video_path>
**Model:** <model>
**Query:** <query>

### Response

<model response text>

---
**Cost:** $<total_cost_usd> | **Tokens:** <input_tokens> in / <output_tokens> out | **Time:** <time_seconds>s
```

## Error Handling

| Error | Action |
|-------|--------|
| Video not found | Show: "Video file not found: $1" |
| API key not set | Show: "GEMINI_API_KEY not set. Export it: `export GEMINI_API_KEY=your_key`" |
| API error | Show full error output |
| Script error | Show full error output |
| Script not found | Show: "video-query.py not found in plugin" |

## Setup

Requires `GEMINI_API_KEY` environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get API key from: https://aistudio.google.com/apikey

## Dependencies

- UV package manager (for running PEP 723 scripts)
- GEMINI_API_KEY environment variable
