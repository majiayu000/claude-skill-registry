---
name: observability-analyze-logs
description: |
  Parses OpenTelemetry-formatted logs to reconstruct execution traces, extract errors with call chains,
  and provide AI-powered root cause analysis. Use when investigating errors, checking logs, debugging issues,
  viewing traces, or analyzing execution flow. Triggers on "check the logs", "analyze errors", "what's failing",
  "debug this issue", "show me the traces", or "investigate the error".
allowed-tools:
  - Bash
  - Read
---

# Analyze Logs

## Table of Contents

### Core Sections
- [What This Skill Does](#what-this-skill-does) - Intelligent OpenTelemetry log analysis with trace reconstruction
- [When to Use This Skill](#when-to-use-this-skill) - Trigger phrases and common scenarios
- [Quick Start](#quick-start) - Most common usage for quick health checks
- [Analysis Workflow](#analysis-workflow) - Complete step-by-step implementation guide
  - [Step 1: Determine User's Need](#step-1-determine-users-need) - Identify analysis type (health check, error investigation, trace debugging)
  - [Step 2: Choose Analysis Mode](#step-2-choose-analysis-mode) - 6 modes: Summary, Error Detail, Trace Analysis, File Filter, Fast Parsing, Real-Time
  - [Step 3: Execute Analysis](#step-3-execute-analysis) - Running commands with Bash tool
  - [Step 4: Interpret Results](#step-4-interpret-results) - Understanding summary tables, detailed output, AI analysis
  - [Step 5: Report Findings](#step-5-report-findings) - Communicating results to users
- [Command Reference](#command-reference) - All analyzer commands with examples
  - Basic Commands (summary, markdown, JSON)
  - Filtering Commands (--error-id, --trace, --file)
  - Performance Commands (--no-ai, --output, tail)
- [Understanding the Output](#understanding-the-output) - Log format, summary tables, trace execution
- [Best Practices](#best-practices) - 7 essential practices for effective log analysis
- [Common Scenarios](#common-scenarios) - Real-world examples with commands
- [Integration with CLAUDE.md](#integration-with-claudemd) - How this skill implements CLAUDE.md conventions

### Advanced Topics
- [Troubleshooting](#troubleshooting) - Common issues and fixes
- [Advanced Usage](#advanced-usage) - Custom scripts, programmatic access, budget tracking
- [Expected Outcomes](#expected-outcomes) - Success criteria and common results
- [Requirements](#requirements) - Tools, files, dependencies, verification

### Supporting Resources
- [Technical Reference](references/reference.md) - OpenTelemetry format, data models, parsing logic, AI configuration
- [Response Templates](templates/response-template.md) - 8 response templates for different contexts
- [Related Documentation](#related-documentation) - Tool implementation, usage examples, LangChain client
- [Quick Reference Card](#quick-reference-card) - One-line command cheatsheet

---

## Purpose

Intelligent log analysis for any project using OpenTelemetry trace reconstruction and AI-powered error diagnosis. Parses OTEL-formatted logs, reconstructs execution traces, extracts errors with call chain context, and provides root cause analysis.

## What This Skill Does

Intelligent log analysis for any project using OpenTelemetry trace reconstruction and AI-powered error diagnosis. Works with projects that generate OpenTelemetry-formatted logs in a configurable log directory.

**Core capabilities:**
- Parse OpenTelemetry-formatted logs with trace/span IDs
- Reconstruct complete execution traces
- Extract errors with full call chain context
- AI-powered root cause analysis
- Multiple output formats (summary, markdown, JSON)
- Advanced filtering (by error ID, trace ID, file)

## When to Use This Skill

Invoke this skill when users mention:
- "check the logs"
- "look at the logs"
- "analyze errors"
- "what's failing?"
- "debug this issue"
- "show me the traces"
- "investigate the error"
- "view log file"
- Any mention of project log files ({{LOG_DIR}}/{{LOG_FILE}}.log)

## Quick Start

**Most common usage (quick health check):**
```bash
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

This gives you a summary table with error IDs and trace IDs, perfect for quick health checks. Replace `{{LOG_DIR}}` with your project's log directory (e.g., `logs`) and `{{LOG_FILE}}` with the log filename (e.g., `app.log`).

## Instructions

### Step 1: Determine User's Need

**Quick Health Check:**
- User asks: "Are there any errors?" or "What's happening in the logs?"
- Action: Run summary mode (default)

**Specific Error Investigation:**
- User mentions specific error or asks for details
- Action: Get error ID from summary, then use --error-id

**Trace-Based Debugging:**
- User asks "what led to this error?" or wants execution flow
- Action: Use --trace with trace ID

**File-Specific Analysis:**
- User mentions specific file or module
- Action: Use --file filter

**Real-Time Monitoring:**
- User wants to watch logs as they happen
- Action: Use tail -f

### Step 2: Choose Analysis Mode

**Mode 1: Summary (Default) - Start here 90% of the time**
```bash
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

Output: Compact table with error IDs, trace IDs, file:line, function, and message preview.

**Use when:**
- Initial investigation
- Quick health check
- Getting error IDs for deeper analysis
- User asks "what errors do we have?"

**Mode 2: Error Detail - Deep dive into specific error**
```bash
python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown
```

Output: Full error details including complete message, call chain, stack trace, related errors.

**Use when:**
- User asks about specific error from summary
- Need full error message (summary truncates)
- Want to see complete stack trace
- Investigating single failure

**Mode 3: Trace Analysis - Understand execution flow**
```bash
python3 .claude/tools/utils/log_analyzer.py --trace TRACE_ID --format markdown
```

Output: All errors in that trace with full execution context.

**Use when:**
- Multiple related errors in same trace
- Need to understand execution sequence
- Debugging distributed operations
- User asks "what happened in this execution?"

**Mode 4: File Filter - Find all errors in specific file**
```bash
python3 .claude/tools/utils/log_analyzer.py --file database.py --format markdown
```

Output: All errors from that file with trace context.

**Use when:**
- User mentions specific file
- Investigating module-specific issues
- Finding patterns in one component

**Mode 5: Fast Parsing (No AI) - Quick and free**
```bash
python3 .claude/tools/utils/log_analyzer.py --no-ai
```

Output: Same as summary but skips AI analysis (faster, no cost).

**Use when:**
- Quick checks during development
- Want to avoid LLM costs
- Just need parsed errors without analysis
- Automated scripts or frequent polling

**Mode 6: Real-Time Monitoring**
```bash
tail -f {{LOG_DIR}}/{{LOG_FILE}}.log
```

Output: Live log stream (Ctrl+C to exit).

**Use when:**
- Watching logs during testing
- Monitoring server startup
- Debugging in real-time
- User runs operations and wants to see results

### Step 3: Execute Analysis

**Execute the appropriate command using the Bash tool:**

```bash
# Example for summary
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

### Step 4: Interpret Results

**For Summary Output:**
1. Check "Total errors" count
2. Scan error table for patterns (same file, same trace)
3. Note error IDs for deeper investigation
4. Use provided Quick Commands to drill down

**For Detailed Output:**
1. Read Full Message (not truncated)
2. Review Call Chain (execution flow leading to error)
3. Check Related Errors (other failures in same trace)
4. Examine Stack Trace (if available)
5. Look for Recovery Attempts (logs after error)

**For AI Analysis (markdown with --no-ai not set):**
1. Read Root Causes section
2. Check Patterns (recurring issues)
3. Review Priority (what to fix first)
4. Follow Fixes (specific file:line changes)
5. Consider Systemic Issues (larger architectural problems)

### Step 5: Report Findings

**Always provide:**
1. Summary of error count and severity
2. Most critical issues (from AI analysis or your judgment)
3. Specific file:line references for user to investigate
4. Suggested next steps or commands to run

**Example response format:**
```
Found 5 errors in the logs:

Critical Issues:
1. Neo4j connection failure in database.py:123 (trace: abc123)
   - Appears 3 times across different operations
   - Root cause: Connection timeout after 5s

2. Invalid config in settings.py:45 (trace: def456)
   - Missing required parameter 'api_key'

To investigate further:
- View error 1 details: python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown
- See all Neo4j errors: python3 .claude/tools/utils/log_analyzer.py --file database.py --format markdown
```

## Command Reference

### Basic Commands

```bash
# Quick summary (default)
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log

# Detailed markdown with AI analysis
python3 .claude/tools/utils/log_analyzer.py --format markdown

# JSON output for programmatic use
python3 .claude/tools/utils/log_analyzer.py --format json
```

### Filtering Commands

```bash
# View specific error details (get ID from summary)
python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown

# View all errors in a trace
python3 .claude/tools/utils/log_analyzer.py --trace abc123def456 --format markdown

# Filter by file name
python3 .claude/tools/utils/log_analyzer.py --file database.py

# Combine filters
python3 .claude/tools/utils/log_analyzer.py --file database.py --trace abc123 --format markdown
```

### Performance Commands

```bash
# Skip AI analysis (faster, free)
python3 .claude/tools/utils/log_analyzer.py --no-ai

# Save to file instead of stdout
python3 .claude/tools/utils/log_analyzer.py --format markdown --output report.md

# Real-time log monitoring
tail -f {{LOG_DIR}}/{{LOG_FILE}}.log

# Last 50 lines
tail -n 50 {{LOG_DIR}}/{{LOG_FILE}}.log

# Follow and filter for errors
tail -f {{LOG_DIR}}/{{LOG_FILE}}.log | grep ERROR
```

## Understanding the Output

### Log Format

OpenTelemetry format with trace/span IDs:
```
2025-10-16 14:32:15 - [trace:abc123 | span:def456] - module.name - ERROR - [file.py:123] - function() - Error message
```

**Key fields:**
- **timestamp**: When the log occurred
- **trace**: Unique ID for entire execution (groups related logs)
- **span**: Unique ID for operation within trace
- **module**: Python module path
- **level**: ERROR, WARNING, INFO, DEBUG
- **file:line**: Source location
- **function**: Function name
- **message**: Log message

### Summary Table

```
ID   | Trace      | File:Line              | Function    | Message
-----|------------|------------------------|-------------|------------------
1    | abc123     | database.py:45         | connect     | Connection failed
2    | abc123     | database.py:67         | query       | No active connection
```

**Columns explained:**
- **ID**: Error number (use with --error-id)
- **Trace**: First 8 chars of trace ID (same trace = related errors)
- **File:Line**: Where error occurred
- **Function**: Function that logged error
- **Message**: Preview (truncated, use --error-id for full message)

### Trace Execution

A **trace** represents one complete execution flow:
- Starts at entry point (e.g., MCP tool call)
- Includes all operations in that execution
- Ends when execution completes
- Multiple errors in same trace are related

**Example trace flow:**
```
Trace abc123:
  1. automatic_indexing() [deprecated] called
  2. connect_to_neo4j() called
  3. ERROR: Connection timeout
  4. retry_connection() called
  5. ERROR: Retry failed
```

All errors share trace ID `abc123`, so they're related failures.

## Best Practices

### 1. Always Start with Summary

Don't jump straight to markdown or detail view. Get the overview first:
```bash
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

### 2. Use Error IDs for Deep Dives

Summary gives you error IDs. Use them:
```bash
# From summary, identify interesting error (e.g., ID 3)
python3 .claude/tools/utils/log_analyzer.py --error-id 3 --format markdown
```

### 3. Group Related Errors by Trace

If multiple errors share a trace ID in summary, view the whole trace:
```bash
python3 .claude/tools/utils/log_analyzer.py --trace abc123def456 --format markdown
```

### 4. Use --no-ai for Quick Checks

During active development, skip AI to save time and cost:
```bash
python3 .claude/tools/utils/log_analyzer.py --no-ai
```

### 5. Combine with Real-Time Monitoring

When running tests or operations:
```bash
# Terminal 1: Run operation
uv run pytest tests/integration/

# Terminal 2: Watch logs
tail -f {{LOG_DIR}}/{{LOG_FILE}}.log
```

### 6. Save Reports for Later

Generate markdown reports for documentation:
```bash
python3 .claude/tools/utils/log_analyzer.py --format markdown --output reports/$(date +%Y-%m-%d)-errors.md
```

### 7. Check Logs BEFORE Making Changes

When user reports an issue, check logs first:
1. Run summary to see current state
2. Identify error patterns
3. Then make code changes
4. Re-run summary to verify fix

## Common Scenarios

### Scenario 1: User says "check the logs"

```bash
# Step 1: Run summary
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log

# Step 2: Report findings
# "Found 3 errors. Most critical is Neo4j connection failure..."

# Step 3: Offer deeper analysis
# "Would you like me to investigate error #1 in detail?"
```

### Scenario 2: User says "why did X fail?"

```bash
# Step 1: Run summary to find X-related errors
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log

# Step 2: Get error ID for X
# Step 3: Analyze that error
python3 .claude/tools/utils/log_analyzer.py --error-id 2 --format markdown

# Step 4: Explain root cause from call chain and AI analysis
```

### Scenario 3: Debugging test failures

```bash
# Step 1: Monitor logs during test
tail -f {{LOG_DIR}}/{{LOG_FILE}}.log &

# Step 2: Run tests
uv run pytest tests/integration/test_xyz.py -v

# Step 3: Analyze results
python3 .claude/tools/utils/log_analyzer.py --file test_xyz.py --format markdown
```

### Scenario 4: Production issue investigation

```bash
# Step 1: Get full report with AI analysis
python3 .claude/tools/utils/log_analyzer.py --format markdown --output incident-report.md

# Step 2: Review AI Root Causes and Fixes
# Step 3: Identify trace IDs for critical errors
# Step 4: Drill into specific traces
python3 .claude/tools/utils/log_analyzer.py --trace TRACE_ID --format markdown
```

## Usage Examples

### Example 1: Quick Health Check

```bash
# User says: "Check the logs"
# Run summary mode:
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log

# Output: Summary table showing 3 errors
# Action: Report findings, offer detailed investigation
```

### Example 2: Detailed Error Investigation

```bash
# User says: "What caused error #1?"
# From summary, get error ID, then:
python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown

# Output: Full error details with call chain, stack trace, AI analysis
# Action: Explain root cause, suggest fix with file:line references
```

### Example 3: Trace-Based Debugging

```bash
# User says: "Show me everything that happened in that execution"
# From summary, get trace ID, then:
python3 .claude/tools/utils/log_analyzer.py --trace abc123def456 --format markdown

# Output: All errors in trace with execution context
# Action: Explain execution flow, identify failure cascade
```

## Expected Outcomes

### Successful Analysis

```
✓ Log Analysis Summary
  Total entries: 1,523
  Total traces: 12
  Errors found: 7
  Files affected: 4

  Error table with IDs, traces, files, functions, messages
  Quick commands for drill-down investigation
```

### Detailed Investigation

```
✓ Markdown report with:
  - AI-powered root cause analysis
  - Complete execution traces
  - Call chains leading to errors
  - Related errors grouped by trace
  - File:line references for fixes
  - Stack traces (if available)
```

## Integration Points

### With CLAUDE.md Convention

This skill implements the CLAUDE.md logging convention:

**CLAUDE.md says:**
> When users say "Logs", analyze `{{LOG_DIR}}/{{LOG_FILE}}.log` from your project

**This skill provides:**
1. Automatic log file location
2. Multiple analysis modes
3. AI-powered diagnosis
4. Trace reconstruction
5. Interactive debugging workflow

**Recommended workflow:**
1. User says "Logs" → Run this skill
2. Start with summary mode
3. Identify critical errors
4. Drill down with --error-id or --trace
5. Report findings with file:line references

### With Debug Workflows

Integrates with test debugging and issue investigation:

```
Test fails → Check logs → Identify error → Fix code → Re-run → Verify
```

### With Quality Gates

Use in pre-commit checks and CI/CD:

```bash
# Before committing, check for new errors
python3 .claude/tools/utils/log_analyzer.py --no-ai
# If errors found, investigate and fix
```

## Expected Benefits

| Metric | Without Skill | With Skill | Improvement |
|--------|--------------|------------|-------------|
| **Error Diagnosis Time** | 15-30 min (manual parsing) | 2-5 min (automated) | 6-10x faster |
| **Root Cause Accuracy** | ~60% (assumptions) | ~90% (AI analysis) | 50% improvement |
| **Trace Reconstruction** | Manual, error-prone | Automatic | 100% coverage |
| **Context Awareness** | Limited (single logs) | Full (trace grouping) | Complete context |
| **Report Generation** | Manual markdown | Automated | Instant reports |

## Success Metrics

After implementing this skill:

- **<5 second analysis time** - Fast log parsing and error extraction
- **100% trace reconstruction** - All related errors grouped by trace
- **90% root cause accuracy** - AI-powered diagnosis with high confidence
- **Markdown/JSON export** - Automated report generation
- **Zero manual log parsing** - Automated OpenTelemetry parsing

## Validation Process

### Step 1: Quick Health Check
```bash
# Summary mode for initial assessment
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

### Step 2: Identify Critical Errors
```bash
# Get error IDs from summary
# Focus on errors in critical paths
```

### Step 3: Deep Dive Analysis
```bash
# Use error IDs for detailed investigation
python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown
```

### Step 4: Trace Reconstruction
```bash
# Group related errors by trace
python3 .claude/tools/utils/log_analyzer.py --trace TRACE_ID --format markdown
```

### Step 5: Report Findings
```bash
# Generate markdown report for documentation
python3 .claude/tools/utils/log_analyzer.py --format markdown --output report.md
```

## Red Flags to Avoid

❌ **DON'T:**
- Parse logs manually with grep/sed (use analyzer tool)
- Ignore trace IDs (they group related errors)
- Look at single error in isolation (check full trace)
- Skip AI analysis when investigating production issues
- Assume errors are unrelated (verify with trace grouping)
- Make changes without seeing actual log output

✅ **DO:**
- Always start with summary mode
- Use error IDs for detailed investigation
- Group errors by trace ID
- Use --no-ai for quick checks, AI for production debugging
- Generate markdown reports for documentation
- Combine with real-time monitoring (tail -f)

## Troubleshooting

**Error: Log file not found**
```bash
# Check if log file exists
ls -lh {{LOG_DIR}}/{{LOG_FILE}}.log

# If missing, run the MCP server first to generate logs
./run-mcp-server.sh
```

**Error: Permission denied**
```bash
# Make script executable
chmod +x .claude/tools/utils/log_analyzer.py
```

**Error: Module not found (langchain_client)**
```bash
# Ensure you're in project root
pwd  # Should be your project root directory

# Script adds parent dir to path automatically
```

**AI analysis fails or skipped**
```bash
# Use --no-ai flag to skip AI analysis
python3 .claude/tools/utils/log_analyzer.py --no-ai

# Or check LangChain client configuration
cat .claude/tools/langchain_client.py
```

**Empty log file**
```bash
# Check log file size
ls -lh {{LOG_DIR}}/{{LOG_FILE}}.log

# If empty, server hasn't run yet or logging not configured
# Run server to generate logs
./run-mcp-server.sh
```

## Advanced Usage

### Custom Analysis Scripts

See [scripts/example_usage.py](scripts/example_usage.py) for advanced patterns:

**The example script demonstrates:**
1. **Basic log analysis** with default settings and LangChain client
2. **Custom LLM client** with budget tracking (monthly/daily limits)
3. **Parsing only** (no LLM) - faster, free error extraction
4. **Filtering specific errors** - finding Neo4j-related issues
5. **Trace-based analysis** - grouping errors by execution trace

```python
# Example: Parse without LLM (from scripts/example_usage.py)
from utils.log_analyzer import OTelLogParser, ErrorExtractor

parser = OTelLogParser()
entries = parser.parse_file(Path("{{LOG_DIR}}/{{LOG_FILE}}.log"))

extractor = ErrorExtractor(context_lines=3)
errors = extractor.extract_errors(entries)

# Filter specific patterns
neo4j_errors = [e for e in errors if "Neo4j" in e.error.message]
```

**Run the examples:**
```bash
python3 .claude/skills/observability-analyze-logs/scripts/example_usage.py
```

### Programmatic Access

```bash
# Get JSON output for scripts
python3 .claude/tools/utils/log_analyzer.py --format json > errors.json

# Parse with jq
python3 .claude/tools/utils/log_analyzer.py --format json | jq '.errors[] | select(.file == "database.py")'
```

### Budget Tracking

The analyzer uses LangChain client with budget tracking. See example_usage.py for details on monitoring costs.

## Requirements

**Tools needed:**
- Python 3.12+ (already in project)
- Log analyzer tool: `.claude/tools/utils/log_analyzer.py` (bundled)
- LangChain client: `.claude/tools/langchain_client.py` (bundled)

**Log file:**
- Default location: `{{LOG_DIR}}/{{LOG_FILE}}.log` (customize for your project)
- Generated by running your project's server startup script (e.g., `./run-server.sh`)

**Dependencies:**
- Standard library modules (no additional installation needed)
- LangChain client uses project's existing dependencies

**Verification:**
```bash
# Verify log analyzer exists
ls .claude/tools/utils/log_analyzer.py

# Verify log file exists (or generate by running server)
ls {{LOG_DIR}}/{{LOG_FILE}}.log || ./run-server.sh

# Test the analyzer
python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log
```

## Supporting Files

This skill follows progressive disclosure with supporting files for depth:

- **[references/reference.md](references/reference.md)** - Technical documentation:
  - OpenTelemetry log format specification
  - Data models (LogEntry, TraceExecution, ErrorContext)
  - Parsing logic and trace reconstruction algorithm
  - AI analysis configuration and cost tracking
  - Performance characteristics and scaling limits

- **[references/log-rotation-guide.md](references/log-rotation-guide.md)** - Log rotation configuration and management
- **[references/log-rotation-analysis.md](references/log-rotation-analysis.md)** - Log rotation analysis and patterns
- **[references/logging-and-rotation-guide.md](references/logging-and-rotation-guide.md)** - Complete logging and rotation guide

- **[templates/response-template.md](templates/response-template.md)** - Response formatting:
  - 8 response templates for different contexts
  - Summary, detailed error, trace analysis, file-specific
  - AI-powered pattern analysis, real-time monitoring
  - No errors found, before/after comparison

## Expected Outcomes

### Successful Analysis

**Summary mode output:**
```
✓ Log Analysis Summary
  Total entries: 1,523
  Total traces: 12
  Errors found: 7
  Files affected: 4

  Error table with IDs, traces, files, functions, messages
  Quick commands for drill-down investigation
```

**Detailed mode output:**
```
✓ Markdown report with:
  - AI-powered root cause analysis
  - Complete execution traces
  - Call chains leading to errors
  - Related errors grouped by trace
  - File:line references for fixes
  - Stack traces (if available)
```

### Common Outcomes

- **No errors found**: "✓ HEALTHY - Analyzed 1,234 entries, no errors found"
- **Configuration issues**: Clear error with fix steps (e.g., "Start Neo4j: `neo4j start`")
- **Test failures**: Trace showing execution flow to failure with root cause
- **Production issues**: AI analysis with priority ranking and systemic issues

## Related Documentation

- **Tool implementation:** `.claude/tools/utils/log_analyzer.py`
- **Usage examples:** `.claude/tools/utils/example_usage.py`
- **LangChain client:** `.claude/tools/langchain_client.py`
- **CLAUDE.md conventions:** `CLAUDE.md` (section on "Logs")
- **Log file location:** `{{LOG_DIR}}/{{LOG_FILE}}.log`

## Quick Reference Card

| Goal | Command |
|------|---------|
| Health check | `python3 .claude/tools/utils/log_analyzer.py {{LOG_DIR}}/{{LOG_FILE}}.log` |
| Detailed error | `python3 .claude/tools/utils/log_analyzer.py --error-id 1 --format markdown` |
| Trace analysis | `python3 .claude/tools/utils/log_analyzer.py --trace TRACE_ID --format markdown` |
| File-specific | `python3 .claude/tools/utils/log_analyzer.py --file database.py` |
| Fast & free | `python3 .claude/tools/utils/log_analyzer.py --no-ai` |
| Real-time | `tail -f {{LOG_DIR}}/{{LOG_FILE}}.log` |
| Save report | `python3 .claude/tools/utils/log_analyzer.py --format markdown -o report.md` |
| JSON output | `python3 .claude/tools/utils/log_analyzer.py --format json` |

---

**Remember:** Always start with summary mode, then drill down using error IDs or trace IDs based on what you find.
