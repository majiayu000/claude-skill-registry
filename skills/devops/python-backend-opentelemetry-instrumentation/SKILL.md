---
name: python-backend-opentelemetry-instrumentation
description: OpenTelemetry instrumentation for Python backend services
version: 1.0.0
author: Agentient Labs
category: Backend
tags: [opentelemetry, python, tracing, fastapi, flask]
activation_criteria:
  keywords: [opentelemetry python, otel python, flask trace, fastapi trace, setup-tracing]
  file_patterns: ["main.py", "app.py", "requirements.txt"]
  modes: [error_monitoring, python_dev]
always_loaded: true
dependencies:
  required: [cross-platform-structured-logging, distributed-tracing-context-propagation]
---

# Python Backend OpenTelemetry Instrumentation

Instrument Python backend services with OpenTelemetry for distributed tracing and continuing traces from upstream services.

## Installation

```bash
pip install opentelemetry-api opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-fastapi \
  opentelemetry-instrumentation-requests
```

## FastAPI Auto-Instrumentation

```python
# main.py
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracing
resource = Resource.create({"service.name": "python-api", "service.version": "1.0.0"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)  # Automatic tracing

@app.get("/users")
async def get_users():
    return {"users": []}
```

## Manual Spans

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("database-query") as span:
    span.set_attribute("db.system", "postgresql")
    result = await db.query("SELECT * FROM users")
    span.set_attribute("result.count", len(result))
```

## Log Correlation

```python
span = trace.get_current_span()
ctx = span.get_span_context()
logger.info("query", trace_id=format(ctx.trace_id, '032x'))
```
