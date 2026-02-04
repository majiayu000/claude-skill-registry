---
name: dapr-observability-setup
description: Configure OpenTelemetry tracing, metrics, and structured logging for DAPR applications. Integrates with Azure Monitor, Jaeger, Prometheus, and other observability backends.
---

# DAPR Observability Setup

Configure comprehensive observability for DAPR microservices.

## When to Activate

This skill should be invoked when:
- Setting up a new DAPR project
- Adding monitoring/tracing to existing services
- Configuring Azure Monitor or other backends
- Debugging distributed system issues

## Observability Components

### 1. Distributed Tracing (OpenTelemetry)

Configure tracing in Python applications:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def configure_tracing(service_name: str):
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument()

    # Instrument HTTP requests
    RequestsInstrumentor().instrument()
```

### 2. Metrics (Prometheus)

Configure metrics collection:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
REQUEST_COUNT = Counter(
    'dapr_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'dapr_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

# Start metrics server
start_http_server(9090)
```

### 3. Structured Logging

Configure JSON logging:

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "my-service",
            "trace_id": getattr(record, 'trace_id', None),
            "span_id": getattr(record, 'span_id', None),
        }
        return json.dumps(log_obj)

def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(logging.INFO)
```

## DAPR Configuration

### Tracing Configuration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing-config
spec:
  tracing:
    samplingRate: "1"  # 100% for dev, reduce for production
    otel:
      endpointAddress: "otel-collector:4317"
      isSecure: false
      protocol: grpc
```

### Azure Monitor Integration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: azure-monitor-config
spec:
  tracing:
    samplingRate: "0.1"  # 10% sampling for production
    otel:
      endpointAddress: "https://dc.services.visualstudio.com/v2/track"
      isSecure: true
      protocol: http
```

## Observability Stack

### OpenTelemetry Collector Config

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  prometheus:
    endpoint: 0.0.0.0:8889

  azuremonitor:
    connection_string: ${APPLICATIONINSIGHTS_CONNECTION_STRING}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger, azuremonitor]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

## Best Practices

1. **Correlation IDs**: Always propagate trace context
2. **Sampling**: Use 10-20% sampling in production
3. **Log Levels**: Use INFO for normal, DEBUG for troubleshooting
4. **Metrics Cardinality**: Limit label values to prevent explosion
5. **Retention**: Set appropriate retention for traces (7-30 days)
