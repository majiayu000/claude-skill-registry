---
name: langfuse-extraction
description: Extracts traces, observations, and metrics from Langfuse Cloud (EU) API for debugging, telemetry analysis, and regulatory audit trails. Generates ALCOA+ compliant reports, exports to pandas DataFrame, and supports time-range/user/session filtering. Use when investigating production issues, generating compliance documentation, or analyzing LLM costs and performance. MUST BE USED for pharmaceutical audit trail generation requiring GAMP-5 traceability.
allowed-tools: ["Bash", "Read", "Write", "Grep"]
---

# Langfuse Extraction Skill

**Purpose**: Extract observability data from Langfuse Cloud API for analysis, debugging, and compliance reporting.

---

## When to Use This Skill

✅ **Use when**:
- Investigating production workflow failures or performance issues
- Generating ALCOA+ compliant audit trails for regulatory review
- Analyzing LLM token usage and costs across sessions
- Exporting trace data to pandas for statistical analysis
- Creating compliance reports for GAMP-5 validation
- Debugging specific user sessions or workflows

❌ **Do NOT use when**:
- Adding instrumentation to code (use `langfuse-integration` skill)
- Interacting with Langfuse dashboard UI (use `langfuse-dashboard` skill)

---

## Prerequisites

1. **Langfuse API Keys** configured in environment
2. **langfuse** Python package installed
3. Traces already exist in Langfuse Cloud from instrumented workflows

---

## Workflow Phases

### Phase 1: Extract Recent Traces (Time-Range Query)

**Use case**: Get last 24 hours of traces for monitoring/debugging.

```python
# scripts/extract_traces.py --hours 24 --output recent_traces.json

from langfuse import Langfuse
from datetime import datetime, timedelta
import json

langfuse = Langfuse()

from_time = datetime.now() - timedelta(hours=24)
traces = langfuse.api.trace.list(
    from_timestamp=from_time.isoformat(),
    tags=["pharmaceutical", "gamp5"],
    limit=100
)

# Export to JSON
with open("recent_traces.json", "w") as f:
    json.dump([{
        "trace_id": t.id,
        "timestamp": t.timestamp,
        "user_id": t.user_id,
        "session_id": t.session_id,
        "duration_ms": t.duration,
        "status": t.status
    } for t in traces.data], f, indent=2)
```

### Phase 2: Extract Detailed Observations (Span Analysis)

**Use case**: Investigate specific trace with all span details.

```python
# scripts/extract_traces.py --trace-id <id> --detailed

trace = langfuse.api.trace.get("trace_id_here")

observations = []
for obs in trace.observations:
    observations.append({
        "id": obs.id,
        "type": obs.type,  # "SPAN", "GENERATION", "EVENT"
        "name": obs.name,
        "latency_ms": obs.latency,
        "input_tokens": obs.usage.input if obs.usage else 0,
        "output_tokens": obs.usage.output if obs.usage else 0,
        "cost": obs.calculated_total_cost or 0.0,
        "metadata": obs.metadata
    })
```

### Phase 3: Generate ALCOA+ Audit Trail

**Use case**: Regulatory compliance reporting.

```python
# scripts/generate_audit_trail.py --user-id <clerk_id> --session-id <job_id>

def generate_audit_trail(user_id: str, session_id: str = None):
    traces = langfuse.api.trace.list(
        user_id=user_id,
        session_id=session_id
    )

    audit_trail = []
    for trace in traces.data:
        audit_entry = {
            "timestamp": trace.timestamp,
            "user_id": trace.user_id,
            "session_id": trace.session_id,
            "trace_id": trace.id,
            "compliance": {
                "attributable": bool(trace.user_id),
                "contemporaneous": True,
                "complete": trace.status == "COMPLETED",
                "gamp5_category": trace.metadata.get("compliance.gamp5.category")
            },
            "operations": [
                {"name": obs.name, "duration_ms": obs.latency}
                for obs in trace.observations
            ]
        }
        audit_trail.append(audit_entry)

    return audit_trail
```

### Phase 4: Export to Pandas DataFrame

**Use case**: Statistical analysis, cost tracking, performance metrics.

```python
# scripts/export_to_dataframe.py --output traces.csv

import pandas as pd

traces = langfuse.api.trace.list(limit=1000)

records = []
for trace in traces.data:
    records.append({
        "trace_id": trace.id,
        "timestamp": trace.timestamp,
        "duration_ms": trace.duration,
        "user_id": trace.user_id,
        "session_id": trace.session_id,
        "total_cost": trace.total_cost or 0.0,
        "input_tokens": trace.usage.input if trace.usage else 0,
        "output_tokens": trace.usage.output if trace.usage else 0,
        "status": trace.status,
        "gamp5_category": trace.metadata.get("compliance.gamp5.category")
    })

df = pd.DataFrame(records)
df.to_csv("traces.csv", index=False)
```

---

## Success Criteria

- ✅ API keys configured and tested
- ✅ Traces extracted with all required fields
- ✅ ALCOA+ audit trail includes user/session attribution
- ✅ DataFrame export includes token usage and costs
- ✅ No FALLBACK LOGIC (errors propagate with diagnostics)
- ✅ Compliance metadata preserved in exports

---

## Reference Materials

- **api-reference.md**: Complete Langfuse API documentation
- **audit-trail-formats.md**: ALCOA+/GAMP-5 compliant output formats
- **query_templates.json**: Common API query patterns

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-17
**API Version**: Langfuse REST API v1
**EU Data Residency**: cloud.langfuse.com
