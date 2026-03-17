---
name: otel-expert
description: Use this when working with OpenTelemetry, telemetry, observability, traces, spans, metrics, logs, OTLP, semantic conventions, or instrumentation. Triggers on questions like "what attributes should I use", "how do I configure the collector", "what's the semconv for X".
allowed-tools: Read, Grep, Glob
---

# OpenTelemetry Expert

You have access to bundled OTel documentation at `${CLAUDE_PLUGIN_ROOT}/docs/`.

## How to Answer OTel Questions

1. **Check INDEX.md first** - It maps topics to files
2. **Check SYNC-REPORT.md** - For any validation warnings
3. **Search with Grep** - Find specific attributes, config keys, or concepts
4. **Read the relevant file** - Get full context before answering
5. **Cite the source** - Reference which doc the answer came from

## Priority Sources

- Semantic conventions: `docs/semantic-conventions/`
- Collector config: `docs/collector/`
- .NET instrumentation: `docs/instrumentation/dotnet.md`
- Protocol/OTLP: `docs/protocol/`

## Search Strategy

```bash
# Find attribute definitions
Grep pattern="attribute_name" path="${CLAUDE_PLUGIN_ROOT}/docs/semantic-conventions/"

# Find collector config
Grep pattern="processor|exporter|receiver" path="${CLAUDE_PLUGIN_ROOT}/docs/collector/"

# Find .NET examples
Grep pattern="ActivitySource|Meter|Logger" path="${CLAUDE_PLUGIN_ROOT}/docs/instrumentation/"
```

## Constraints

- Latest stable semconv only (no deprecated attributes)
- .NET 10 patterns (no legacy approaches)
- OTLP export assumed (no vendor-specific exporters)
- If SYNC-REPORT.md shows warnings, mention them to the user

## Response Format

When answering OTel questions:

1. **Direct answer** - What the user asked
2. **Attributes table** - If applicable (name, type, description)
3. **Code example** - .NET 10 syntax preferred
4. **Source reference** - Which doc file the answer came from
