---
name: session-replay
version: 1.0.0
description: |
  Analyze claude-trace JSONL files for session health, patterns, and actionable insights.
  Use when debugging session issues, understanding token usage, or identifying failure patterns.
auto_activates:
  - "analyze session"
  - "session health"
  - "trace analysis"
  - "debug session"
  - "token usage patterns"
  - "session failures"
priority_score: 38.0
evaluation_criteria:
  frequency: MEDIUM
  impact: HIGH
  complexity: LOW
  reusability: HIGH
  philosophy_alignment: HIGH
  uniqueness: MEDIUM
dependencies:
  tools:
    - Read
    - Glob
  external: []
maturity: production
---

# Session Replay Skill

## Purpose

This skill analyzes claude-trace JSONL files to provide insights into Claude Code session health, token usage patterns, error frequencies, and agent effectiveness. It complements the `/transcripts` command by focusing on API-level trace data rather than conversation transcripts.

## When to Use This Skill

- **Session debugging**: Diagnose why a session was slow or failed
- **Token analysis**: Understand token consumption patterns
- **Error patterns**: Identify recurring failures across sessions
- **Performance optimization**: Find bottlenecks in tool usage
- **Agent effectiveness**: Measure which agents/tools are most productive

## Quick Start

### Analyze Latest Session

```
User: Analyze my latest session health
```

I'll analyze the most recent trace file:

```python
# Read latest trace file from .claude-trace/
trace_dir = Path(".claude-trace")
trace_files = sorted(trace_dir.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)
latest = trace_files[-1] if trace_files else None

# Parse and analyze
if latest:
    analysis = analyze_trace_file(latest)
    print(format_session_report(analysis))
```

### Compare Multiple Sessions

```
User: Compare token usage across my last 5 sessions
```

I'll aggregate metrics across sessions:

```python
trace_files = sorted(Path(".claude-trace").glob("*.jsonl"))[-5:]
comparison = compare_sessions(trace_files)
print(format_comparison_table(comparison))
```

## Actions

### Action: `health`

Analyze session health metrics from a trace file.

**What to do:**

1. Read the trace file (JSONL format)
2. Extract API requests and responses
3. Calculate metrics:
   - Total tokens (input/output)
   - Request count and timing
   - Error rate
   - Tool usage distribution
4. Generate health report

**Metrics to extract:**

```python
# From each JSONL line containing a request/response pair:
{
    "timestamp": "...",
    "request": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "body": {
            "model": "claude-...",
            "messages": [...],
            "tools": [...]
        }
    },
    "response": {
        "usage": {
            "input_tokens": N,
            "output_tokens": N
        },
        "content": [...],
        "stop_reason": "..."
    }
}
```

**Output format:**

```
Session Health Report
=====================
File: log-2025-11-23-19-32-36.jsonl
Duration: 45 minutes

Token Usage:
- Input: 125,432 tokens
- Output: 34,521 tokens
- Total: 159,953 tokens
- Efficiency: 27.5% output ratio

Request Stats:
- Total requests: 23
- Average latency: 2.3s
- Errors: 2 (8.7%)

Tool Usage:
- Read: 45 calls
- Edit: 12 calls
- Bash: 8 calls
- Grep: 15 calls

Health Score: 82/100 (Good)
- Minor issue: 2 errors detected
```

### Action: `errors`

Identify error patterns across sessions.

**What to do:**

1. Scan trace files for error responses
2. Categorize errors by type
3. Identify recurring patterns
4. Suggest fixes

**Error categories to detect:**

- Rate limit errors (429)
- Token limit exceeded
- Tool execution failures
- Timeout errors
- API errors

**Output format:**

```
Error Analysis
==============
Sessions analyzed: 5
Total errors: 12

Error Categories:
1. Rate limit (429): 5 occurrences
   - Recommendation: Add delays between requests

2. Token limit: 3 occurrences
   - Recommendation: Use context management skill

3. Tool failures: 4 occurrences
   - Bash timeout: 2
   - File not found: 2
   - Recommendation: Check paths before operations
```

### Action: `compare`

Compare metrics across multiple sessions.

**What to do:**

1. Load multiple trace files
2. Extract comparable metrics
3. Calculate trends
4. Identify anomalies

**Output format:**

```
Session Comparison
==================
                    Session 1   Session 2   Session 3   Trend
Tokens (total)      150K        180K        120K        -17%
Requests            25          30          18          -28%
Errors              2           0           1           stable
Duration (min)      45          60          30          -33%
Efficiency          0.27        0.32        0.35        +7%
```

### Action: `tools`

Analyze tool usage patterns.

**What to do:**

1. Extract tool calls from traces
2. Calculate frequency and timing
3. Identify inefficient patterns
4. Suggest optimizations

**Patterns to detect:**

- Sequential calls that could be parallel
- Repeated reads of same file
- Excessive grep/glob calls
- Unused tool results

**Output format:**

```
Tool Usage Analysis
===================
Tool          Calls   Avg Time   Success Rate
Read          45      0.1s       100%
Edit          12      0.3s       92%
Bash          8       1.2s       75%
Grep          15      0.2s       100%
Task          3       45s        100%

Optimization Opportunities:
1. 5 Read calls to same file within 2 minutes
   - Consider caching strategy

2. 3 sequential Bash calls could be parallelized
   - Use multiple Bash calls in single message
```

## Implementation Notes

### Parsing JSONL Traces

Claude-trace files are JSONL format with request/response pairs:

```python
import json
from pathlib import Path
from typing import Dict, List, Any

def parse_trace_file(path: Path) -> List[Dict[str, Any]]:
    """Parse a claude-trace JSONL file."""
    entries = []
    with open(path) as f:
        for line in f:
            if line.strip():
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue
    return entries

def extract_metrics(entries: List[Dict]) -> Dict[str, Any]:
    """Extract session metrics from trace entries."""
    metrics = {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "request_count": 0,
        "error_count": 0,
        "tool_usage": {},
        "timestamps": [],
    }

    for entry in entries:
        if "request" in entry:
            metrics["request_count"] += 1
            metrics["timestamps"].append(entry.get("timestamp", 0))

        if "response" in entry:
            usage = entry["response"].get("usage", {})
            metrics["total_input_tokens"] += usage.get("input_tokens", 0)
            metrics["total_output_tokens"] += usage.get("output_tokens", 0)

            # Check for errors
            if entry["response"].get("error"):
                metrics["error_count"] += 1

        # Extract tool usage from request body
        if "request" in entry and "body" in entry["request"]:
            body = entry["request"]["body"]
            if isinstance(body, dict) and "tools" in body:
                for tool in body["tools"]:
                    name = tool.get("name", "unknown")
                    metrics["tool_usage"][name] = metrics["tool_usage"].get(name, 0) + 1

    return metrics
```

### Locating Trace Files

```python
def find_trace_files(trace_dir: str = ".claude-trace") -> List[Path]:
    """Find all trace files, sorted by modification time."""
    trace_path = Path(trace_dir)
    if not trace_path.exists():
        return []
    return sorted(
        trace_path.glob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True  # Most recent first
    )
```

### Error Handling

Handle common error scenarios gracefully:

```python
def safe_parse_trace_file(path: Path) -> Tuple[List[Dict], List[str]]:
    """Parse trace file with error collection for malformed lines.

    Returns:
        Tuple of (valid_entries, error_messages)
    """
    entries = []
    errors = []

    if not path.exists():
        return [], [f"Trace file not found: {path}"]

    try:
        with open(path) as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")
    except PermissionError:
        return [], [f"Permission denied: {path}"]
    except UnicodeDecodeError:
        return [], [f"Encoding error: {path} (expected UTF-8)"]

    return entries, errors


def format_error_report(errors: List[str], path: Path) -> str:
    """Format error report for user display."""
    if not errors:
        return ""

    report = f"""
Trace File Issues
=================
File: {path.name}
Issues found: {len(errors)}

"""
    for error in errors[:10]:  # Limit to first 10
        report += f"- {error}\n"

    if len(errors) > 10:
        report += f"\n... and {len(errors) - 10} more issues"

    return report
```

**Common error scenarios:**

| Scenario          | Cause                                | Handling                           |
| ----------------- | ------------------------------------ | ---------------------------------- |
| Empty file        | Session had no API calls             | Report "No data to analyze"        |
| Malformed JSON    | Corrupted trace or interrupted write | Skip line, count in error report   |
| Missing fields    | Older trace format                   | Use `.get()` with defaults         |
| Permission denied | File locked by another process       | Clear error message, suggest retry |
| Encoding error    | Non-UTF-8 characters                 | Report encoding issue              |

## Integration with Existing Tools

### Tool Selection Matrix

| Need                               | Use This                                    | Why                           |
| ---------------------------------- | ------------------------------------------- | ----------------------------- |
| "Why was my session slow?"         | **session-replay**                          | API latency and token metrics |
| "What did I discuss last session?" | **/transcripts**                            | Conversation content          |
| "Extract learnings from sessions"  | **CodexTranscriptsBuilder**                 | Knowledge extraction          |
| "Reduce my token usage"            | **session-replay** + **context_management** | Metrics + optimization        |
| "Resume interrupted work"          | **/transcripts**                            | Context restoration           |

### vs. /transcripts Command

**/transcripts** (conversation management):

- Focuses on conversation content
- Restores session context
- Used for context preservation
- **Trigger**: "restore session", "continue work", "what was I doing"

**session-replay skill** (API-level analysis):

- Focuses on API metrics
- Analyzes performance and errors
- Used for debugging and optimization
- **Trigger**: "session health", "token usage", "why slow", "debug session"

### vs. CodexTranscriptsBuilder

**CodexTranscriptsBuilder** (knowledge extraction):

- Extracts patterns from conversations
- Builds learning corpus
- Knowledge-focused
- **Trigger**: "extract patterns", "build knowledge base", "learn from sessions"

**session-replay skill** (metrics analysis):

- Extracts performance metrics
- Identifies technical issues
- Operations-focused
- **Trigger**: "performance metrics", "error patterns", "tool efficiency"

### Combined Workflows

**Workflow 1: Diagnose and Fix Token Issues**

```
1. session-replay: Analyze token usage patterns (health action)
2. Identify high-token operations
3. context_management skill: Apply proactive trimming
4. session-replay: Compare before/after sessions (compare action)
```

**Workflow 2: Post-Incident Analysis**

```
1. session-replay: Identify error patterns (errors action)
2. /transcripts: Review conversation context around errors
3. session-replay: Check tool usage around failures (tools action)
4. Document findings in DISCOVERIES.md
```

**Workflow 3: Performance Baseline**

```
1. session-replay: Analyze 5-10 recent sessions (compare action)
2. Establish baseline metrics (tokens, latency, errors)
3. Track deviations from baseline over time
```

## Storage Locations

- **Trace files**: `.claude-trace/*.jsonl`
- **Session logs**: `.claude/runtime/logs/<session_id>/`
- **Generated reports**: Output directly (no persistent storage needed)

## Philosophy Alignment

### Ruthless Simplicity

- **Single-purpose**: Analyze trace files only - no session management, no transcript editing
- **No external dependencies**: Uses only Python standard library (json, pathlib, datetime)
- **Direct file parsing**: No ORM, no database, no complex abstractions
- **Present-moment focus**: Analyzes what exists now, no future-proofing

### Zero-BS Implementation

- **All functions work completely**: Every code example in this skill runs without modification
- **Real parsing, real metrics**: No mocked data, no placeholder calculations
- **No stubs or placeholders**: If a feature is documented, it works
- **Fail fast on errors**: Clear error messages, no silent failures

### Brick Philosophy

- **Self-contained analysis**: All functionality in this single skill
- **Clear inputs (trace files) and outputs (reports)**: No hidden state or side effects
- **Regeneratable from this specification**: This SKILL.md is the complete source of truth
- **Isolated responsibility**: Session analysis only - doesn't modify files or trigger actions

## Limitations

This skill CANNOT:

- **Modify trace files**: Read-only analysis, no editing or deletion
- **Generate traces**: Use `claude-trace` npm package to create trace files
- **Restore sessions**: Use `/transcripts` command for session restoration
- **Real-time monitoring**: Analyzes completed sessions, not live tracking
- **Cross-project analysis**: Analyzes traces in current project only
- **Parse non-JSONL formats**: Only claude-trace JSONL format supported
- **Access remote traces**: Local filesystem only, no cloud storage

## Tips for Effective Analysis

1. **Start with health check**: Run `health` action first
2. **Look for patterns**: Use `errors` to find recurring issues
3. **Optimize hot spots**: Use `tools` to find inefficiencies
4. **Track trends**: Use `compare` across sessions
5. **Combine with transcripts**: Use `/transcripts` for context

## Common Patterns

### Pattern 1: Debug Slow Session

```
User: My last session was really slow, analyze it

1. Run health action on latest trace
2. Check request latencies
3. Identify tool bottlenecks
4. Report findings with recommendations
```

### Pattern 2: Reduce Token Usage

```
User: I'm hitting token limits, help me understand usage

1. Compare token usage across sessions
2. Identify high-token operations
3. Suggest context management strategies
4. Recommend workflow optimizations
```

### Pattern 3: Fix Recurring Errors

```
User: I keep getting errors, find the pattern

1. Run errors action across last 10 sessions
2. Categorize and count error types
3. Identify root causes
4. Provide targeted fixes
```

## Resources

- **Trace directory**: `.claude-trace/`
- **Transcripts command**: `/transcripts`
- **Context management skill**: `context-management`
- **Philosophy**: `.claude/context/PHILOSOPHY.md`

## Troubleshooting

### No trace files found

**Symptom**: "No trace files in .claude-trace/"

**Causes and fixes**:

1. **claude-trace not enabled**: Set `AMPLIHACK_USE_TRACE=1` before starting session
2. **Wrong directory**: Check you're in project root with `.claude-trace/` directory
3. **Fresh project**: Run a session with tracing enabled first

### Incomplete metrics

**Symptom**: Missing token counts or zero values

**Causes and fixes**:

1. **Interrupted session**: Trace may be incomplete if session crashed
2. **Streaming responses**: Some streaming modes don't capture full metrics
3. **Older trace format**: Upgrade claude-trace to latest version

### Health score seems wrong

**Symptom**: Score doesn't match session experience

**Understanding the score**:

- 90-100: Excellent - low errors, good efficiency
- 70-89: Good - minor issues detected
- 50-69: Fair - significant issues worth investigating
- Below 50: Poor - likely errors or inefficiencies

**Factors in health score**:

- Error rate (40% weight)
- Token efficiency ratio (30% weight)
- Request success rate (20% weight)
- Tool success rate (10% weight)

### Large trace files

**Symptom**: Analysis is slow or memory-intensive

**Solutions**:

1. Analyze specific time range instead of full file
2. Use `tools` action for targeted analysis
3. Archive old traces: `mv .claude-trace/old-*.jsonl .claude-trace/archive/`

## Remember

This skill provides session-level debugging and optimization insights. It complements transcript management with API-level visibility. Use it to diagnose issues, optimize workflows, and understand Claude Code behavior patterns.

**Key Takeaway**: Trace files contain the raw truth about session performance. This skill extracts actionable insights from that data.
