---
name: logging-observability
description: Comprehensive logging and observability patterns for production systems including structured logging, distributed tracing, metrics collection, log aggregation, and alerting. Triggers for this skill - log, logging, logs, trace, tracing, traces, metrics, observability, OpenTelemetry, OTEL, Jaeger, Zipkin, structured logging, log level, debug, info, warn, error, fatal, correlation ID, span, spans, ELK, Elasticsearch, Loki, Datadog, Prometheus, Grafana, distributed tracing, log aggregation, alerting, monitoring, JSON logs, telemetry.
---

# Logging and Observability

## Overview

Observability enables understanding system behavior through logs, metrics, and traces. This skill provides patterns for:

- **Structured Logging**: JSON logs with correlation IDs and contextual data
- **Distributed Tracing**: Span-based request tracking across services (OpenTelemetry, Jaeger, Zipkin)
- **Metrics Collection**: Counters, gauges, histograms for system health (Prometheus patterns)
- **Log Aggregation**: Centralized log management (ELK, Loki, Datadog)
- **Alerting**: Symptom-based alerts with runbooks

## Instructions

### 1. Structured Logging (JSON Logs)

#### Python Implementation

```python
import json
import logging
import sys
from datetime import datetime
from contextvars import ContextVar
from typing import Any

# Context variables for request tracking
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')
span_id: ContextVar[str] = ContextVar('span_id', default='')

class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
            "span_id": span_id.get(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'structured_data'):
            log_data.update(record.structured_data)

        return json.dumps(log_data)

def setup_logging():
    """Configure structured logging."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

# Usage
logger = logging.getLogger(__name__)
logger.info("User logged in", extra={
    "structured_data": {
        "user_id": "123",
        "ip_address": "192.168.1.1",
        "action": "login"
    }
})
```

#### TypeScript Implementation

```typescript
interface LogContext {
  correlationId?: string;
  spanId?: string;
  [key: string]: unknown;
}

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  context: LogContext;
}

class StructuredLogger {
  private context: LogContext = {};

  withContext(context: LogContext): StructuredLogger {
    const child = new StructuredLogger();
    child.context = { ...this.context, ...context };
    return child;
  }

  private log(
    level: string,
    message: string,
    data?: Record<string, unknown>,
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: { ...this.context, ...data },
    };
    console.log(JSON.stringify(entry));
  }

  debug(message: string, data?: Record<string, unknown>): void {
    this.log("DEBUG", message, data);
  }

  info(message: string, data?: Record<string, unknown>): void {
    this.log("INFO", message, data);
  }

  warn(message: string, data?: Record<string, unknown>): void {
    this.log("WARN", message, data);
  }

  error(message: string, data?: Record<string, unknown>): void {
    this.log("ERROR", message, data);
  }
}
```

### 2. Log Levels and When to Use Each

| Level     | Usage                        | Examples                                          |
| --------- | ---------------------------- | ------------------------------------------------- |
| **TRACE** | Fine-grained debugging       | Loop iterations, variable values                  |
| **DEBUG** | Diagnostic information       | Function entry/exit, intermediate states          |
| **INFO**  | Normal operations            | Request started, job completed, user action       |
| **WARN**  | Potential issues             | Deprecated API usage, retry attempted, slow query |
| **ERROR** | Failures requiring attention | Exception caught, operation failed                |
| **FATAL** | Critical failures            | System cannot continue, data corruption           |

```python
# Log level usage examples
logger.debug("Processing item", extra={"structured_data": {"item_id": item.id}})
logger.info("Order processed successfully", extra={"structured_data": {"order_id": order.id, "total": order.total}})
logger.warning("Rate limit approaching", extra={"structured_data": {"current": 95, "limit": 100}})
logger.error("Payment failed", extra={"structured_data": {"order_id": order.id, "error": str(e)}})
```

### 3. Distributed Tracing

#### Correlation IDs and Spans

```python
import uuid
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Optional
import time

@dataclass
class Span:
    name: str
    trace_id: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: dict = field(default_factory=dict)

    def end(self):
        self.end_time = time.time()

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0

current_span: ContextVar[Optional[Span]] = ContextVar('current_span', default=None)

class Tracer:
    def __init__(self, service_name: str):
        self.service_name = service_name

    def start_span(self, name: str, parent: Optional[Span] = None) -> Span:
        parent = parent or current_span.get()
        trace_id = parent.trace_id if parent else str(uuid.uuid4())[:32]
        parent_span_id = parent.span_id if parent else None

        span = Span(
            name=name,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            attributes={"service": self.service_name}
        )
        current_span.set(span)
        return span

    def end_span(self, span: Span):
        span.end()
        self._export(span)
        # Restore parent span if exists
        # In production, use a span stack

    def _export(self, span: Span):
        """Export span to tracing backend."""
        logger.info(f"Span completed: {span.name}", extra={
            "structured_data": {
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "parent_span_id": span.parent_span_id,
                "duration_ms": span.duration_ms,
                "attributes": span.attributes
            }
        })

# Context manager for spans
from contextlib import contextmanager

@contextmanager
def trace_span(tracer: Tracer, name: str):
    span = tracer.start_span(name)
    try:
        yield span
    except Exception as e:
        span.attributes["error"] = True
        span.attributes["error.message"] = str(e)
        raise
    finally:
        tracer.end_span(span)

# Usage
tracer = Tracer("order-service")

async def process_order(order_id: str):
    with trace_span(tracer, "process_order") as span:
        span.attributes["order_id"] = order_id

        with trace_span(tracer, "validate_order"):
            await validate(order_id)

        with trace_span(tracer, "charge_payment"):
            await charge(order_id)
```

### 4. Metrics Collection

```python
from dataclasses import dataclass
from typing import Dict, List
from enum import Enum
import time
import threading

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"

@dataclass
class Counter:
    name: str
    labels: Dict[str, str]
    value: float = 0

    def inc(self, amount: float = 1):
        self.value += amount

@dataclass
class Gauge:
    name: str
    labels: Dict[str, str]
    value: float = 0

    def set(self, value: float):
        self.value = value

    def inc(self, amount: float = 1):
        self.value += amount

    def dec(self, amount: float = 1):
        self.value -= amount

@dataclass
class Histogram:
    name: str
    labels: Dict[str, str]
    buckets: List[float]
    values: List[float] = None

    def __post_init__(self):
        self.values = []
        self._bucket_counts = {b: 0 for b in self.buckets}
        self._bucket_counts[float('inf')] = 0
        self._sum = 0
        self._count = 0

    def observe(self, value: float):
        self.values.append(value)
        self._sum += value
        self._count += 1
        for bucket in sorted(self._bucket_counts.keys()):
            if value <= bucket:
                self._bucket_counts[bucket] += 1

class MetricsRegistry:
    def __init__(self):
        self._metrics: Dict[str, any] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, labels: Dict[str, str] = None) -> Counter:
        key = f"{name}:{labels}"
        with self._lock:
            if key not in self._metrics:
                self._metrics[key] = Counter(name, labels or {})
            return self._metrics[key]

    def gauge(self, name: str, labels: Dict[str, str] = None) -> Gauge:
        key = f"{name}:{labels}"
        with self._lock:
            if key not in self._metrics:
                self._metrics[key] = Gauge(name, labels or {})
            return self._metrics[key]

    def histogram(self, name: str, buckets: List[float], labels: Dict[str, str] = None) -> Histogram:
        key = f"{name}:{labels}"
        with self._lock:
            if key not in self._metrics:
                self._metrics[key] = Histogram(name, labels or {}, buckets)
            return self._metrics[key]

# Usage
metrics = MetricsRegistry()

# Counter for requests
request_counter = metrics.counter("http_requests_total", {"method": "GET", "path": "/api/orders"})
request_counter.inc()

# Gauge for active connections
active_connections = metrics.gauge("active_connections")
active_connections.inc()
# ... handle connection ...
active_connections.dec()

# Histogram for request duration
request_duration = metrics.histogram(
    "http_request_duration_seconds",
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

start = time.time()
# ... handle request ...
request_duration.observe(time.time() - start)
```

### 5. OpenTelemetry Patterns

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_opentelemetry(service_name: str, otlp_endpoint: str):
    """Initialize OpenTelemetry with OTLP export."""

    # Tracing setup
    trace_provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics setup
    metric_provider = MeterProvider(
        resource=Resource.create({"service.name": service_name})
    )
    metrics.set_meter_provider(metric_provider)

    # Auto-instrumentation
    RequestsInstrumentor().instrument()

    return trace.get_tracer(service_name), metrics.get_meter(service_name)

# Usage with FastAPI
from fastapi import FastAPI

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

tracer, meter = setup_opentelemetry("order-service", "http://otel-collector:4317")

# Custom spans
@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    with tracer.start_as_current_span("fetch_order") as span:
        span.set_attribute("order.id", order_id)
        order = await order_repository.get(order_id)
        span.set_attribute("order.status", order.status)
        return order
```

### 6. Log Aggregation Patterns

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# Logstash pipeline configuration
input {
  file {
    path => "/var/log/app/*.log"
    codec => json
  }
}

filter {
  # Parse structured JSON logs
  json {
    source => "message"
  }

  # Add Elasticsearch index based on date
  mutate {
    add_field => {
      "[@metadata][index]" => "app-logs-%{+YYYY.MM.dd}"
    }
  }

  # Enrich with geolocation (if IP present)
  geoip {
    source => "ip_address"
    target => "geo"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index]}"
  }
}
```

#### Grafana Loki

```yaml
# Promtail scrape configuration
scrape_configs:
  - job_name: app-logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: app-logs
          __path__: /var/log/app/*.log

    # Extract JSON fields as labels
    pipeline_stages:
      - json:
          expressions:
            level: level
            correlation_id: correlation_id
            service: service
      - labels:
          level:
          correlation_id:
          service:
```

#### Datadog Agent Configuration

```yaml
# datadog.yaml
logs_enabled: true

logs_config:
  processing_rules:
    - type: exclude_at_match
      name: exclude_healthcheck
      pattern: "GET /health"

  # Auto-parse JSON logs
  auto_multi_line_detection: true

# Log collection from files
logs:
  - type: file
    path: "/var/log/app/*.log"
    service: "order-service"
    source: "python"
    tags:
      - "env:production"
```

### 7. Alert Design

#### Prometheus Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: service-alerts
    rules:
      # High error rate alert
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over the last 5 minutes"
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

      # High latency alert
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"

      # Service down alert
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.job }} has been down for more than 1 minute"
```

#### Alert Severity Levels

| Level        | Response Time | Examples                                      |
| ------------ | ------------- | --------------------------------------------- |
| **Critical** | Immediate     | Service down, high error rate, data loss      |
| **Warning**  | Business hrs  | High latency, approaching limits, retry spikes|
| **Info**     | Log only      | Deployment started, config changed            |

## Best Practices

### Logging

1. **Log at Appropriate Levels**: DEBUG for development, INFO for normal operations, WARN for potential issues, ERROR for failures, FATAL for critical failures.

2. **Include Context**: Always include correlation IDs, trace IDs, user IDs, and relevant business identifiers in structured fields.

3. **Avoid Sensitive Data**: Never log passwords, tokens, credit cards, or PII. Implement automatic redaction when necessary.

4. **Use Structured Logging**: JSON logs enable easy parsing and querying in log aggregation systems (ELK, Loki, Datadog).

5. **Consistent Field Names**: Standardize field names across services (e.g., always use `correlation_id`, not sometimes `request_id`).

### Distributed Tracing

6. **Trace Boundaries**: Create spans at service boundaries, database calls, external API calls, and significant operations.

7. **Propagate Context**: Pass trace IDs and span IDs across service boundaries via HTTP headers (OpenTelemetry standards).

8. **Add Meaningful Attributes**: Include business context (user_id, order_id) and technical context (db_query, cache_hit) in span attributes.

9. **Sample Appropriately**: Use adaptive sampling - trace 100% of errors, sample successful requests based on traffic volume.

### Metrics

10. **Track Golden Signals**: Monitor the Four Golden Signals - latency, traffic, errors, saturation.

11. **Use Correct Metric Types**: Counters for totals (requests), Gauges for current values (memory), Histograms for distributions (latency).

12. **Label Cardinality**: Keep label cardinality low - avoid high-cardinality values like user IDs in metric labels.

13. **Naming Conventions**: Follow Prometheus naming - `http_requests_total` (counter), `process_memory_bytes` (gauge), `http_request_duration_seconds` (histogram).

### Alerting

14. **Alert on Symptoms**: Alert on user-impacting issues (error rate, latency), not causes (CPU usage). Symptoms indicate what is broken, causes explain why.

15. **Include Runbooks**: Every alert must link to a runbook with investigation steps, common causes, and remediation procedures.

16. **Use Appropriate Thresholds**: Set thresholds based on SLOs and historical data, not arbitrary values.

17. **Alert Fatigue**: Ensure alerts are actionable. Non-actionable alerts lead to alert fatigue and ignored critical issues.

### Integration

18. **End-to-End Correlation**: Link logs, traces, and metrics using correlation IDs to enable cross-system debugging.

19. **Centralize**: Use centralized log aggregation (ELK, Loki) and trace collection (Jaeger, Zipkin) for cross-service visibility.

20. **Test Observability**: Verify logging, tracing, and metrics in development - don't discover gaps in production.

## Examples

### Complete Request Logging Middleware

```python
import time
import uuid
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class ObservabilityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, tracer, metrics):
        super().__init__(app)
        self.tracer = tracer
        self.request_counter = metrics.counter("http_requests_total")
        self.request_duration = metrics.histogram(
            "http_request_duration_seconds",
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
        )

    async def dispatch(self, request: Request, call_next):
        # Extract or generate correlation ID
        corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        correlation_id.set(corr_id)

        start_time = time.time()

        with self.tracer.start_as_current_span(
            f"{request.method} {request.url.path}"
        ) as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("correlation_id", corr_id)

            try:
                response = await call_next(request)

                span.set_attribute("http.status_code", response.status_code)

                # Record metrics
                labels = {
                    "method": request.method,
                    "path": request.url.path,
                    "status": str(response.status_code)
                }
                self.request_counter.labels(**labels).inc()
                self.request_duration.labels(**labels).observe(
                    time.time() - start_time
                )

                # Add correlation ID to response
                response.headers["X-Correlation-ID"] = corr_id

                return response

            except Exception as e:
                span.set_attribute("error", True)
                span.record_exception(e)
                raise
```
