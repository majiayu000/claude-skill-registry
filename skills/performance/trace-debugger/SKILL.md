---
name: Trace Debugger
description: Debug performance issues and understand code flow using AILANG telemetry traces. Use when user asks to debug slow compilation, analyze benchmarks, find bottlenecks, investigate hangs, or understand system behavior.
---

# Trace Debugger

Debug and analyze AILANG operations using OpenTelemetry distributed tracing. This skill helps identify performance bottlenecks, understand code flow, and debug issues using trace data from GCP Cloud Trace.

## Quick Start

**Most common usage:**
```bash
# User says: "Why is compilation slow?"
# This skill will:
# 1. Check telemetry is configured
# 2. Run the slow operation with tracing
# 3. Query recent traces with ailang trace list
# 4. Analyze timing breakdown per phase
# 5. Identify the bottleneck

# Check telemetry status
ailang trace status

# List recent traces
ailang trace list --hours 2 --limit 20

# View specific trace hierarchy
ailang trace view <trace-id>
```

## When to Use This Skill

Invoke this skill when:
- User asks to debug slow compilation or type checking
- User wants to analyze benchmark performance
- User mentions "bottleneck", "slow", "hang", or "performance"
- User wants to understand execution flow across components
- User asks "why is X taking so long?"
- User needs to compare timing between runs

## Telemetry Prerequisites

Before debugging with traces:

```bash
# Option 1: Google Cloud Trace (recommended)
export GOOGLE_CLOUD_PROJECT=your-project-id

# Option 2: Local Jaeger
docker run -d -p 16686:16686 -p 4318:4318 jaegertracing/all-in-one
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# Option 3: AILANG Observatory Dashboard (local UI)
ailang server  # Starts server on localhost:1957
# View traces at http://localhost:1957 → Observatory tab

# Verify configuration
ailang trace status
```

## Observatory Dashboard Setup (v0.6.3+)

The Observatory provides a local dashboard for viewing traces from Claude Code, Gemini CLI, and AILANG.

### Start the Server

```bash
ailang server
# Or: make services-start
```

### Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/json",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:1957",
    "OTEL_RESOURCE_ATTRIBUTES": "ailang.source=user"
  }
}
```

**What Claude Code sends:** Events via OTLP logs (token counts, costs, model, session info)

### Configure Gemini CLI

**Important**: Gemini CLI only supports `local` (file-based) or `gcp` (GCP Cloud Trace) telemetry targets.
It does NOT support direct OTLP export to custom endpoints.

Add to `~/.gemini/settings.json`:

```json
{
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": true
  }
}
```

**Architecture**: Gemini traces go to GCP Cloud Trace, then Observatory pulls them via the GCP Trace API.

**Trace Linking**: The Observatory links Gemini traces to AILANG traces via:
- `session.id` - Links tool invocations in the same session
- `ailang.task_id` - Added by Coordinator for delegated tasks
- `ailang.workspace` - Groups traces by project

**What Gemini CLI sends to GCP:** Full traces (complete span hierarchy with parent-child relationships, token counts, model info, prompts)

### Environment Variables Reference

**Claude Code** (direct OTLP export to Observatory):
| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable Claude Code telemetry | `1` |
| `OTEL_LOGS_EXPORTER` | Log export protocol | `otlp` |
| `OTEL_METRICS_EXPORTER` | Metrics export protocol | `otlp` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Transport protocol | `http/json` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Observatory URL | `http://localhost:1957` |
| `OTEL_RESOURCE_ATTRIBUTES` | Span metadata | `ailang.source=user` |

**Gemini CLI** (GCP Cloud Trace only - configure via `~/.gemini/settings.json`):
| Setting | Purpose | Value |
|---------|---------|-------|
| `telemetry.enabled` | Enable telemetry | `true` |
| `telemetry.target` | Export destination | `gcp` |
| `telemetry.logPrompts` | Include prompt text | `true` |

### OTLP Endpoints

The Observatory receives data on:
- `/v1/traces` - Trace spans (Gemini CLI, AILANG)
- `/v1/logs` - Log records (Claude Code events)
- `/v1/metrics` - Metrics data

Both protobuf and JSON formats are supported.

### Verify Telemetry is Working

1. Ensure `ailang server` is running
2. Run a Claude Code or Gemini CLI command
3. Open http://localhost:1957 → Observatory tab
4. New traces should appear automatically

**Note:** If server is not running, OTLP exports fail silently (no impact on CLI tools).

## Available Scripts

### `scripts/check_traces.sh [hours] [filter]`
Quick check for recent traces with optional filtering.

**Usage:**
```bash
# Check last hour of traces
.claude/skills/trace-debugger/scripts/check_traces.sh

# Check last 4 hours, filter by eval
.claude/skills/trace-debugger/scripts/check_traces.sh 4 "eval.suite"

# Check compilation traces
.claude/skills/trace-debugger/scripts/check_traces.sh 1 "compile"
```

### `scripts/analyze_compilation.sh <file.ail>`
Run a file with tracing and analyze compilation phases.

**Usage:**
```bash
# Analyze compilation timing
.claude/skills/trace-debugger/scripts/analyze_compilation.sh examples/runnable/factorial.ail
```

## Workflow

### 1. Verify Telemetry Configuration

```bash
ailang trace status
```

Expected output shows either GCP or OTLP mode enabled. If disabled, set environment variables.

### 2. Reproduce the Issue with Tracing

Run the operation that's slow/problematic:

```bash
# For compilation issues
GOOGLE_CLOUD_PROJECT=your-project ailang run --caps IO --entry main file.ail

# For eval issues
GOOGLE_CLOUD_PROJECT=your-project ailang eval-suite --models gpt5-mini --benchmarks simple_hello

# For message system issues
GOOGLE_CLOUD_PROJECT=your-project ailang messages list
```

### 3. Query Recent Traces

```bash
# List recent traces
ailang trace list --hours 1 --limit 10

# Filter by operation type
ailang trace list --filter "compile"
ailang trace list --filter "eval.suite"
ailang trace list --filter "messages"
```

### 4. Analyze Trace Hierarchy

```bash
# Get full trace details
ailang trace view <trace-id>
```

Look for:
- **Deep nesting**: Indicates recursive operations
- **Long durations**: Shows bottlenecks
- **Missing child spans**: May indicate early exit or error
- **Parallel spans**: Shows concurrent operations

### 5. Interpret Results

**Compiler Pipeline Spans:**
| Span | What to Look For |
|------|------------------|
| `compile.parse` | Long = complex syntax, large file |
| `compile.elaborate` | Long = many surface→core transforms |
| `compile.typecheck` | Long = complex type inference, possible hang |
| `compile.validate` | Long = many nodes to validate |
| `compile.lower` | Long = complex operator lowering |

**Eval Harness Spans:**
| Span | What to Look For |
|------|------------------|
| `eval.suite` | Total benchmark run time |
| `eval.benchmark` | Individual benchmark, check `benchmark.success` |
| `*.generate` | AI API call time (openai, anthropic, gemini) |

**Messaging Spans:**
| Span | What to Look For |
|------|------------------|
| `messages.send` | Message creation time |
| `messages.list` | Query time, check `list.result_count` |
| `messages.search` | Semantic search time |

## Instrumented Components

Current trace coverage in AILANG:

### ✅ Fully Instrumented
- **Compiler Pipeline** (`compile.*`) - All 6 phases traced
- **Eval Harness** (`eval.suite`, `eval.benchmark`) - Suite and per-benchmark
- **Messaging** (`messages.*`) - Send, list, read, search
- **AI Providers** (`anthropic.generate`, `openai.generate`, `gemini.generate`, `ollama.generate`)
- **Server** (HTTP middleware) - Request/response tracing
- **Coordinator** (`coordinator.execute_task`) - Task lifecycle

### 🔜 Prioritized Future Instrumentation

Based on analysis of 280+ implemented design docs and actual bug patterns:

| Priority | Component | Spans | Debug Value |
|----------|-----------|-------|-------------|
| **P1** | Type System | `types.unify`, `types.substitute` | 4+ hours saved per cyclic type/metadata bug |
| **P2** | Module Resolution | `modules.resolve`, `modules.load` | 1-2 hours saved per import error |
| **P3** | Codegen | `codegen.type_lookup`, `codegen.record` | Catch fallbacks before Go compile |
| **P4** | Pattern Matching | `match.compile`, `match.coverage` | Rare but complex debugging |

See [resources/trace_patterns.md](resources/trace_patterns.md) for detailed span definitions and implementation patterns.

## Resources

### Trace Patterns Reference
See [`resources/trace_patterns.md`](resources/trace_patterns.md) for:
- Common debugging patterns
- Trace attribute reference
- Performance baseline expectations

### Span Reference
See [docs/docs/guides/telemetry.md](../../../docs/docs/guides/telemetry.md) for:
- Complete span list with attributes
- Environment variable configuration
- Architecture diagrams

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow overview)
2. **Execute as needed**: Scripts in `scripts/` directory
3. **Load on demand**: `resources/trace_patterns.md` (detailed patterns)

## Notes

- Traces require telemetry environment variables set
- GCP traces may take 30-60 seconds to appear in console
- Local Jaeger provides instant visibility
- Zero overhead when telemetry is disabled
- Use `--json` flag for programmatic trace analysis

### Proactive Trace Improvement

**When debugging with traces, actively look for opportunities to add more instrumentation!**

If you encounter:
- A debugging session where traces didn't help identify the issue
- A component that would benefit from finer-grained spans
- Missing attributes that would have been useful

**Suggest adding traces by:**
1. Noting the component and what information would help
2. Proposing span name and attributes (see [resources/trace_patterns.md](resources/trace_patterns.md))
3. Creating a design doc for significant additions

**Example suggestion format:**
```
Debugging [X] was difficult because traces didn't show [Y].

Suggested addition:
- Span: `component.operation`
- Attributes: `input`, `output`, `duration_ms`
- Location: `internal/package/file.go`
- Debug value: Would show [specific insight]
```

This helps continuously improve AILANG's observability based on real debugging needs.

### Tracing Scope Limitation

**Traces only cover AILANG tooling, NOT generated Go code!**

| What IS Traced | What is NOT Traced |
|----------------|-------------------|
| `ailang compile` phases | Generated Go binary execution |
| `ailang run` (AILANG interpreter) | Go code after `go build` |
| `ailang eval-suite` benchmarks | The actual AI-generated code running |
| `ailang messages` operations | User application runtime |

**To debug generated Go code:**
- Use Go's standard profiling (`go tool pprof`)
- Add your own tracing in generated code templates
- Use `DEBUG_CODEGEN=1` to see what code is generated
- Add `log.Printf` to `internal/codegen/templates/` if needed

**Future possibility:** Generate OTEL spans INTO Go code for runtime tracing (not implemented)
