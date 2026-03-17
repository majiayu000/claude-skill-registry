---
name: batch-report
description: >
  Generate post-run analysis reports for batch processing jobs. Analyzes manifests,
  timings, and failures to produce comprehensive markdown reports. Optionally sends
  to agent-inbox for cross-project communication.
allowed-tools: Bash, Read, Write
triggers:
  - batch report
  - generate report
  - analyze batch
  - summarize extraction
metadata:
  short-description: Post-run batch analysis and reporting

provides:
  - batch-report
composes:
  - create-figure
  - task-monitor
---

# Batch Report Skill

Generate comprehensive analysis reports for completed batch processing jobs.

## Features

- **Manifest analysis** - Count successes, failures, partial completions
- **Timing breakdown** - Per-step latency analysis, identify bottlenecks
- **Failure patterns** - Categorize and summarize failure modes
- **Quality metrics** - Sample outputs for quality assessment
- **Markdown report** - Human-readable summary
- **Agent-inbox integration** - Auto-send to project inbox

## Quick Start

```bash
cd .pi/skills/batch-report

# Generate report for extractor batch (auto-detects format)
uv run python report.py analyze /path/to/batch/output

# Generate and send to agent-inbox
uv run python report.py analyze /path/to/batch/output --send-to extractor

# Just show summary stats
uv run python report.py summary /path/to/batch/output

# Analyze a standalone state file
uv run python report.py state /path/to/.batch_state.json

# JSON output for piping
uv run python report.py summary /path/to/output --json | jq .success_rate
```

## Commands

### `analyze` - Full analysis report

```bash
uv run python report.py analyze /path/to/output \
    --output report.md \
    --send-to extractor \
    --priority high
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output file path (default: stdout) |
| `--send-to` | `-s` | Send report to agent-inbox project |
| `--priority` | `-p` | Priority for agent-inbox (low/normal/high/critical) |
| `--sample` | `-n` | Number of samples to include (default: 5) |
| `--format` | `-f` | Batch format: `extractor`, `youtube`, `generic`, `auto` (default: auto) |
| `--json` | `-j` | Output as JSON for piping to other tools |

### `summary` - Quick stats only

```bash
uv run python report.py summary /path/to/output
uv run python report.py summary /path/to/output --json
```

Output:
```
Batch: run-2025-12-18_144426-2eb428c
Total: 230 | Success: 180 | Failed: 35 | Partial: 15
Success rate: 78.3%
Avg time: 4.2 min | Slowest: 09_section_summarizer (45%)
```

JSON Output:
```json
{
  "batch": "run-2025-12-18_144426-2eb428c",
  "format": "extractor",
  "total": 230,
  "successful": 180,
  "partial": 15,
  "failed": 35,
  "success_rate": 78.3,
  "avg_time_min": 4.2
}
```

### `state` - Analyze standalone state files

```bash
uv run python report.py state /path/to/.batch_state.json
uv run python report.py state /path/to/.batch_state.json --json
```

Works with any `.batch_state.json` file from any batch job.

### `failures` - List failures with reasons

```bash
uv run python report.py failures /path/to/output
uv run python report.py failures /path/to/output --json
```

## Report Format

```markdown
# Batch Report: run-2025-12-18_144426-2eb428c

## Summary
- **Total items:** 230
- **Successful:** 180 (78.3%)
- **Failed:** 35 (15.2%)
- **Partial:** 15 (6.5%)

## Timing Analysis
| Step | Avg (s) | Max (s) | % of Total |
|------|---------|---------|------------|
| 09_section_summarizer | 120.5 | 341.0 | 45.2% |
| 05_table_extractor | 65.3 | 105.0 | 24.5% |
...

## Failure Patterns
| Pattern | Count | Example |
|---------|-------|---------|
| Empty text_content | 12 | 047ca6ef... |
| CUDA OOM | 5 | 9497a4e5... |
...

## Recommendations
1. Consider --text-only mode for knowledge extraction
2. Add table confidence threshold before VLM
...
```

## Visualization

After generating reports (especially with `--json`), offer to visualize via `/create-figure`:

```bash
# Timing waterfall by pipeline step
create-figure metrics --input batch.json --output timing.png --type hbar --title "Step Timing"

# Success/failure distribution
create-figure metrics --input batch.json --output results.png --type pie --title "Batch Results"

# Failure pattern breakdown
create-figure metrics --input batch.json --output failures.png --type bar --title "Failure Patterns"
```

**When to offer:** After presenting batch analysis, ask: "Want me to visualize the timing breakdown?"

## Supported Batch Formats

The `--format` flag accepts: `extractor`, `youtube`, `generic`, or `auto` (default).

Auto-detect logic:
1. If `*/manifest.json` and `*/timings_summary.json` exist → `extractor`
2. If `.batch_state.json` has "transcript" in description → `youtube`
3. If `.batch_state.json` exists → `generic`

### Extractor batches
Expects:
- `*/manifest.json` - Per-item manifests
- `*/timings_summary.json` - Timing data
- `*/14_report_generator/json_output/final_report.json` - Quality metrics
- `failed_urls.txt` - Failed items list

### YouTube transcript batches
Expects:
- `.batch_state.json` - State file with transcript-related description

### Generic batches
Expects:
- `.batch_state.json` - State file with completed/failed counts
- `*.log` files for failure analysis (optional)

## Integration with agent-inbox

```bash
# Send report as bug
uv run python report.py analyze /path/to/output \
    --send-to extractor \
    --priority high

# Message sent: extractor_abc123
```

## Dependencies

```toml
dependencies = [
    "typer",
    "rich",
]
```
