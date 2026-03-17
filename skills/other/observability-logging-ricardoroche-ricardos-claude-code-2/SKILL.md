---
name: observability-logging
description: Automatically applies when adding logging and observability. Ensures structured logging, OpenTelemetry tracing, LLM-specific metrics (tokens, cost, latency), and proper log correlation.
category: observability
---

# Observability and Logging Patterns

When instrumenting AI/LLM applications, follow these patterns for comprehensive observability.

**Trigger Keywords**: logging, observability, tracing, monitoring, metrics, OpenTelemetry, structured logs, correlation ID, request tracking, telemetry

**Agent Integration**: Used by `ml-system-architect`, `llm-app-engineer`, `mlops-ai-engineer`, `performance-and-cost-engineer-llm`

## ✅ Correct Pattern: Structured Logging

```python
import logging
import json
from typing import Any, Dict
from datetime import datetime
import uuid


class StructuredLogger:
    """Structured JSON logger for AI applications."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_handler()

    def _setup_handler(self):
        """Configure JSON formatting."""
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str, **extra: Any):
        """Log info with structured data."""
        self.logger.info(message, extra=self._enrich(extra))

    def error(self, message: str, **extra: Any):
        """Log error with structured data."""
        self.logger.error(message, extra=self._enrich(extra), exc_info=True)

    def _enrich(self, extra: Dict[str, Any]) -> Dict[str, Any]:
        """Add standard fields to log entry."""
        return {
            **extra,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "llm-service"
        }


class JSONFormatter(logging.Formatter):
    """Format logs as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


# Usage
logger = StructuredLogger(__name__)

logger.info(
    "LLM request started",
    request_id="req_123",
    model="claude-sonnet-4",
    prompt_length=150
)
```

## LLM-Specific Logging

```python
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LLMMetrics:
    """Metrics for LLM call."""
    request_id: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    duration_ms: float
    cost_usd: float
    prompt_length: int
    response_length: int
    success: bool
    error: Optional[str] = None


class LLMLogger:
    """Specialized logger for LLM operations."""

    def __init__(self):
        self.logger = StructuredLogger("llm")

    async def log_llm_call(
        self,
        request_id: str,
        model: str,
        prompt: str,
        response: str,
        usage: dict,
        duration_ms: float,
        success: bool = True,
        error: Optional[str] = None
    ):
        """
        Log complete LLM interaction with metrics.

        Args:
            request_id: Unique request identifier
            model: Model name
            prompt: Input prompt (will be truncated/redacted)
            response: Model response (will be truncated)
            usage: Token usage dict
            duration_ms: Request duration in milliseconds
            success: Whether request succeeded
            error: Error message if failed
        """
        # Calculate cost
        cost = self._estimate_cost(
            model,
            usage["input_tokens"],
            usage["output_tokens"]
        )

        # Create metrics
        metrics = LLMMetrics(
            request_id=request_id,
            model=model,
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            total_tokens=usage["total_tokens"],
            duration_ms=duration_ms,
            cost_usd=cost,
            prompt_length=len(prompt),
            response_length=len(response),
            success=success,
            error=error
        )

        # Log with structured data
        self.logger.info(
            "LLM call completed" if success else "LLM call failed",
            **vars(metrics),
            # Redact sensitive content, keep prefix for debugging
            prompt_preview=self._redact(prompt[:100]),
            response_preview=self._redact(response[:100]) if response else None
        )

    def _redact(self, text: str) -> str:
        """Redact PII from logs."""
        # Implement PII redaction
        return text  # TODO: Add actual redaction

    def _estimate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estimate cost in USD."""
        # Pricing logic
        pricing = {
            "claude-sonnet-4-20250514": {
                "input": 3.00 / 1_000_000,
                "output": 15.00 / 1_000_000
            }
        }
        rates = pricing.get(model, pricing["claude-sonnet-4-20250514"])
        return (input_tokens * rates["input"]) + (output_tokens * rates["output"])
```

## Request Correlation with Context

```python
from contextvars import ContextVar
from typing import Optional
import uuid

# Context variable for request ID
request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class RequestContext:
    """Manage request context for distributed tracing."""

    @staticmethod
    def set_request_id(request_id: Optional[str] = None) -> str:
        """Set request ID for current context."""
        if request_id is None:
            request_id = f"req_{uuid.uuid4().hex[:12]}"
        request_id_ctx.set(request_id)
        return request_id

    @staticmethod
    def get_request_id() -> Optional[str]:
        """Get current request ID."""
        return request_id_ctx.get()

    @staticmethod
    def clear():
        """Clear request context."""
        request_id_ctx.set(None)


class CorrelatedLogger(StructuredLogger):
    """Logger that automatically includes request context."""

    def _enrich(self, extra: Dict[str, Any]) -> Dict[str, Any]:
        """Add request ID to all logs."""
        enriched = super()._enrich(extra)
        request_id = RequestContext.get_request_id()
        if request_id:
            enriched["request_id"] = request_id
        return enriched


# Usage in FastAPI
from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests."""

    async def dispatch(self, request: Request, call_next):
        # Set request ID from header or generate new
        request_id = request.headers.get("X-Request-ID") or RequestContext.set_request_id()
        request.state.request_id = request_id

        response = await call_next(request)

        # Add to response headers
        response.headers["X-Request-ID"] = request_id

        RequestContext.clear()
        return response


app = FastAPI()
app.add_middleware(RequestIDMiddleware)
```

## OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from typing import Any


def setup_tracing(service_name: str = "llm-service"):
    """Configure OpenTelemetry tracing."""
    # Set up tracer provider
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Get tracer
    return trace.get_tracer(service_name)


tracer = setup_tracing()


class TracedLLMClient:
    """LLM client with distributed tracing."""

    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete with tracing."""
        with tracer.start_as_current_span("llm.complete") as span:
            # Add span attributes
            span.set_attribute("llm.model", self.model)
            span.set_attribute("llm.prompt_length", len(prompt))
            span.set_attribute("llm.max_tokens", kwargs.get("max_tokens", 1024))

            try:
                response = await self._do_complete(prompt, **kwargs)

                # Add response metrics to span
                span.set_attribute("llm.response_length", len(response))
                span.set_attribute("llm.success", True)

                return response

            except Exception as e:
                span.set_attribute("llm.success", False)
                span.set_attribute("llm.error", str(e))
                span.record_exception(e)
                raise


# Instrument FastAPI automatically
from fastapi import FastAPI

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
```

## Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge
import time


# Define metrics
llm_requests_total = Counter(
    "llm_requests_total",
    "Total LLM requests",
    ["model", "status"]
)

llm_request_duration = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration",
    ["model"]
)

llm_tokens_total = Counter(
    "llm_tokens_total",
    "Total tokens processed",
    ["model", "type"]  # type: input/output
)

llm_cost_total = Counter(
    "llm_cost_usd_total",
    "Total LLM cost in USD",
    ["model"]
)

llm_active_requests = Gauge(
    "llm_active_requests",
    "Currently active LLM requests",
    ["model"]
)


class MeteredLLMClient:
    """LLM client with Prometheus metrics."""

    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete with metrics collection."""
        llm_active_requests.labels(model=self.model).inc()
        start_time = time.time()

        try:
            response = await self._do_complete(prompt, **kwargs)

            # Record success metrics
            duration = time.time() - start_time
            llm_request_duration.labels(model=self.model).observe(duration)
            llm_requests_total.labels(model=self.model, status="success").inc()

            # Token metrics (if available)
            if hasattr(response, "usage"):
                llm_tokens_total.labels(
                    model=self.model,
                    type="input"
                ).inc(response.usage.input_tokens)

                llm_tokens_total.labels(
                    model=self.model,
                    type="output"
                ).inc(response.usage.output_tokens)

                # Cost metric
                cost = self._estimate_cost(response.usage)
                llm_cost_total.labels(model=self.model).inc(cost)

            return response

        except Exception as e:
            llm_requests_total.labels(model=self.model, status="error").inc()
            raise

        finally:
            llm_active_requests.labels(model=self.model).dec()
```

## ❌ Anti-Patterns

```python
# ❌ Unstructured logging
print(f"LLM call took {duration}s")  # Can't parse!
logger.info("Request completed")  # No context!

# ✅ Better: Structured with context
logger.info(
    "LLM request completed",
    duration_seconds=duration,
    model=model,
    tokens=tokens,
    request_id=request_id
)


# ❌ No request correlation
logger.info("Started processing")
# ... other logs ...
logger.info("Finished processing")  # Can't correlate!

# ✅ Better: Use request IDs
RequestContext.set_request_id()
logger.info("Started processing")  # Has request_id
logger.info("Finished processing")  # Same request_id


# ❌ Logging full prompts/responses
logger.info(f"Prompt: {full_prompt}")  # PII leak + huge logs!

# ✅ Better: Log length and preview
logger.info(
    "LLM request",
    prompt_length=len(prompt),
    prompt_preview=redact(prompt[:100])
)


# ❌ No metrics
await llm_complete(prompt)  # No visibility!

# ✅ Better: Track metrics
with metrics.track_llm_call(model):
    result = await llm_complete(prompt)
```

## Best Practices Checklist

- ✅ Use structured (JSON) logging
- ✅ Include request IDs in all logs
- ✅ Track LLM-specific metrics (tokens, cost, latency)
- ✅ Implement distributed tracing (OpenTelemetry)
- ✅ Redact PII from logs
- ✅ Use log levels appropriately (INFO, ERROR)
- ✅ Add context to all log messages
- ✅ Collect metrics in Prometheus format
- ✅ Monitor error rates and latencies
- ✅ Set up alerts for anomalies

## Auto-Apply

When adding observability:
1. Use StructuredLogger for JSON logs
2. Add RequestContext middleware
3. Implement LLM-specific logging
4. Set up OpenTelemetry tracing
5. Define Prometheus metrics
6. Redact sensitive data

## Related Skills

- `llm-app-architecture` - For LLM integration
- `pii-redaction` - For data redaction
- `fastapi-patterns` - For middleware
- `async-await-checker` - For async logging
