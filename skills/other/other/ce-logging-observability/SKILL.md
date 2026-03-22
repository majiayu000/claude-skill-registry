---
name: ce-logging-observability
description: >
  Apply ADR-028 and STD-005 logging and observability rules, including governance
  versus operational separation.
---

# CE Logging and Observability

You are managing the logging and observability surface of the library. All
changes must comply with the architectural rules in ADR-028 and the contributor
guidelines in Standard-005.

## Logger Domains (Mandatory)

All loggers must live under the `calibrated_explanations` root and use one of
the four reserved domains below:

| Domain | Usage | Example |
|---|---|---|
| `core` | Core runtime, caching, parallel, orchestration. | `explainer.fit`, `ParallelExecutor` |
| `plugins` | Builtin and external plugins, resolution. | `CalibratorPlugin`, `PlotPlugin` |
| `telemetry` | Metrics integration and performance shims. | `LatencyMonitor`, `ThroughputMetric` |
| `governance` | Audit events, checkpoints, trust decisions. | `CheckpointManager`, `PluginTrustPolicy` |

```python
import logging
# Pattern 1: Module-level (preferred if path matches domain)
logger = logging.getLogger(__name__)

# Pattern 2: Explicit domain (if path does not match)
logger = logging.getLogger("calibrated_explanations.governance.checkpoints")
```

## Operational vs. Governance Separation

- **Governance/Audit events** MUST use the `governance.*` domain. These include
  checkpoint creation, rollbacks, binary trust decisions (accept/deny), and
  policy changes.
- **Operational events** (fallbacks, cache hits, performance data) MUST use
  `core.*` or `plugins.*`.
- **Fallbacks** MUST use the `WARNING` level with a clear explanation of why
  the fallback was triggered.

## Logging Context (ADR-028 §3)

Use the structured context helpers from `calibrated_explanations.logging` to
propagate identifiers like `request_id`, `tenant_id`, and `explainer_id`.

```python
from calibrated_explanations.logging import update_logging_context, logging_context

# 1. Update global (thread-local) context
update_logging_context(explainer_id="exp-123", tenant_id="acme")

# 2. Scoped context (recommended for local blocks)
with logging_context(request_id="req-456", mode="factual"):
    logger.info("Starting explanation generation")
```

### Supported Context Keys
Must be one of: `request_id`, `tenant_id`, `explainer_id`, `checkpoint_id`,
`plugin_identifier`, `mode`.

---

## Contributor Checklist

1. [ ] **No `basicConfig`** — never call `logging.basicConfig()` in library code.
2. [ ] **No PII** — ensure no sensitive data (e.g., feature values, training data)
   is included in log messages.
3. [ ] **Structured fields** — prefer passing IDs via context rather than
   string concatenation.
4. [ ] **JSON compatibility** — ensure logs are compatible with structured
   formatters (standard fields like `extra` are supported).
5. [ ] **Level check** — use `DEBUG` for noise, `INFO` for normal state,
   `WARNING` for fallbacks/corrections.
6. [ ] **Exception context** — use `logger.exception("message")` inside except
   blocks to capture stack traces automatically.

## Testing Logging

Verify logging output in tests using the `caplog` fixture:

```python
def test_should_log_warning_when_plugin_fails(caplog):
    with caplog.at_level(logging.WARNING, logger="calibrated_explanations.plugins"):
        # ... trigger fallback ...
        assert "fallback triggered" in caplog.text
        assert any(r.explainer_id == "exp-1" for r in caplog.records)
```
