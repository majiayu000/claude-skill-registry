---
description: OpenTelemetry expert for full-stack observability including distributed tracing, metrics, and log correlation. Covers OTel Collector configuration, auto-instrumentation for Node.js/Python/Java/.NET/Go, sampling strategies, backend integration (Grafana, Jaeger, Datadog), and cost optimization. Activates for: OpenTelemetry, OTel, distributed tracing, tracing, spans, metrics, observability, Jaeger, Grafana Tempo, OTLP.
allowed-tools: Read, Write, Edit, Bash
model: opus
context: fork
---

# OpenTelemetry Observability Expert

## Purpose

Design and implement comprehensive observability using OpenTelemetry (OTel). Provide expert guidance on instrumentation, collector deployment, backend selection, and cost-effective telemetry pipelines across all major languages and platforms.

## When to Use

- Setting up distributed tracing across microservices
- Configuring OpenTelemetry Collector pipelines
- Adding auto-instrumentation to applications
- Custom span and metric creation
- Correlating logs with traces
- Sampling strategy decisions
- Migrating from proprietary APM to OTel
- Kubernetes observability setup
- Cost optimization for telemetry data

## Scope Boundaries

This skill covers **OTEL IMPLEMENTATION**: Collector configuration, auto-instrumentation, sampling strategies.

- For high-level observability strategy and SLOs → use `/sw-infra:observability`

## OTel Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                   Application                         │
│  ┌─────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ OTel API │  │ OTel SDK │  │ Auto-Instrumentation│  │
│  └────┬─────┘  └────┬─────┘  └────────┬───────────┘  │
│       └──────────────┴────────────────┘               │
│                      │ OTLP                           │
└──────────────────────┼────────────────────────────────┘
                       ▼
          ┌────────────────────────┐
          │   OTel Collector       │
          │  ┌──────────────────┐  │
          │  │ Receivers        │  │  ← OTLP, Prometheus, Jaeger
          │  ├──────────────────┤  │
          │  │ Processors       │  │  ← batch, filter, attributes
          │  ├──────────────────┤  │
          │  │ Exporters        │  │  ← OTLP, Prometheus, backends
          │  └──────────────────┘  │
          └──────────┬─────────────┘
                     ▼
     ┌───────────────────────────────────┐
     │  Backends                          │
     │  Traces: Tempo, Jaeger, Datadog   │
     │  Metrics: Prometheus, Grafana     │
     │  Logs: Loki, Elasticsearch        │
     └───────────────────────────────────┘
```

## Distributed Tracing

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Trace** | End-to-end request journey across services |
| **Span** | Single unit of work within a trace |
| **SpanContext** | Trace ID + Span ID + flags, propagated across boundaries |
| **Attributes** | Key-value metadata on spans |
| **Events** | Timestamped annotations within a span |
| **Links** | References to related spans in other traces |
| **Status** | OK, ERROR, or UNSET |

### Span Best Practices

```
Naming: <component>.<operation>  (e.g., http.request, db.query, cache.get)
Attributes: Follow semantic conventions (http.method, db.system, etc.)
Granularity: One span per meaningful unit of work, not per function call
```

### Custom Spans (Node.js)

```typescript
import { trace, SpanStatusCode, SpanKind } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service', '1.0.0');

async function processOrder(orderId: string) {
  return tracer.startActiveSpan('order.process', {
    kind: SpanKind.INTERNAL,
    attributes: {
      'order.id': orderId,
    },
  }, async (span) => {
    try {
      // Nested span for validation
      const validated = await tracer.startActiveSpan('order.validate', async (validationSpan) => {
        const result = await validateOrder(orderId);
        validationSpan.setAttribute('order.item_count', result.items.length);
        validationSpan.end();
        return result;
      });

      // Add event for significant milestones
      span.addEvent('order.validated', {
        'order.total': validated.total,
      });

      await chargePayment(validated);
      span.setStatus({ code: SpanStatusCode.OK });
      return validated;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message,
      });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

### Custom Spans (Python)

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind, StatusCode

tracer = trace.get_tracer("order-service", "1.0.0")

async def process_order(order_id: str):
    with tracer.start_as_current_span(
        "order.process",
        kind=SpanKind.INTERNAL,
        attributes={"order.id": order_id},
    ) as span:
        try:
            result = await validate_order(order_id)
            span.add_event("order.validated", {"order.total": result.total})
            await charge_payment(result)
            span.set_status(StatusCode.OK)
            return result
        except Exception as e:
            span.set_status(StatusCode.ERROR, str(e))
            span.record_exception(e)
            raise
```

## Metrics

### Metric Instruments

| Instrument | Use Case | Example |
|-----------|----------|---------|
| **Counter** | Monotonically increasing values | `http.requests.total` |
| **UpDownCounter** | Values that go up and down | `queue.depth` |
| **Histogram** | Distribution of values | `http.request.duration` |
| **Gauge** | Point-in-time values | `cpu.utilization` |
| **Observable** (async) | Callback-based collection | `jvm.memory.used` |

### Recording Metrics (Node.js)

```typescript
import { metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('order-service', '1.0.0');

// Counter
const orderCounter = meter.createCounter('orders.processed', {
  description: 'Total orders processed',
  unit: '{orders}',
});

// Histogram
const orderDuration = meter.createHistogram('orders.duration', {
  description: 'Order processing duration',
  unit: 'ms',
  advice: {
    explicitBucketBoundaries: [10, 50, 100, 250, 500, 1000, 2500, 5000],
  },
});

// UpDownCounter
const activeOrders = meter.createUpDownCounter('orders.active', {
  description: 'Currently processing orders',
});

function processOrder(order: Order) {
  activeOrders.add(1, { 'order.type': order.type });
  const start = performance.now();

  try {
    // ... process
    orderCounter.add(1, {
      'order.type': order.type,
      'order.status': 'success',
    });
  } catch (error) {
    orderCounter.add(1, {
      'order.type': order.type,
      'order.status': 'error',
    });
  } finally {
    orderDuration.record(performance.now() - start, {
      'order.type': order.type,
    });
    activeOrders.add(-1, { 'order.type': order.type });
  }
}
```

## Logs and Log Correlation

### Correlating Logs with Traces

```typescript
import { trace, context } from '@opentelemetry/api';

function getLogContext() {
  const span = trace.getSpan(context.active());
  if (!span) return {};

  const spanContext = span.spanContext();
  return {
    trace_id: spanContext.traceId,
    span_id: spanContext.spanId,
    trace_flags: spanContext.traceFlags,
  };
}

// Usage with any logger (pino, winston, etc.)
const logger = pino({
  mixin() {
    return getLogContext();
  },
});

// Log output includes trace context automatically:
// {"level":30,"trace_id":"abc123","span_id":"def456","msg":"Order processed"}
```

### OTel Log Bridge (Node.js)

```typescript
import { logs, SeverityNumber } from '@opentelemetry/api-logs';

const logger = logs.getLogger('order-service', '1.0.0');

logger.emit({
  severityNumber: SeverityNumber.INFO,
  severityText: 'INFO',
  body: 'Order processed successfully',
  attributes: {
    'order.id': orderId,
    'order.total': total,
  },
});
```

## OTel Collector Configuration

### Full Pipeline Example

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  prometheus:
    config:
      scrape_configs:
        - job_name: 'kubernetes-pods'
          kubernetes_sd_configs:
            - role: pod
          relabel_configs:
            - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
              action: keep
              regex: true

  jaeger:
    protocols:
      thrift_http:
        endpoint: 0.0.0.0:14268

processors:
  batch:
    send_batch_size: 8192
    send_batch_max_size: 16384
    timeout: 5s

  attributes:
    actions:
      - key: environment
        value: production
        action: upsert
      - key: internal.secret
        action: delete

  filter:
    error_mode: ignore
    traces:
      span:
        - 'attributes["http.route"] == "/health"'
        - 'attributes["http.route"] == "/ready"'

  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      - name: errors-always
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 1000
      - name: probabilistic
        type: probabilistic
        probabilistic:
          sampling_percentage: 10

  memory_limiter:
    check_interval: 1s
    limit_mib: 2048
    spike_limit_mib: 512

exporters:
  otlp:
    endpoint: tempo.monitoring.svc:4317
    tls:
      insecure: true

  otlp/datadog:
    endpoint: https://api.datadoghq.com
    headers:
      DD-API-KEY: ${env:DD_API_KEY}

  prometheusremotewrite:
    endpoint: http://mimir.monitoring.svc:9009/api/v1/push

  loki:
    endpoint: http://loki.monitoring.svc:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp, jaeger]
      processors: [memory_limiter, batch, attributes, filter, tail_sampling]
      exporters: [otlp]

    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch, attributes]
      exporters: [prometheusremotewrite]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [loki]

  telemetry:
    logs:
      level: info
    metrics:
      address: 0.0.0.0:8888
```

## Auto-Instrumentation

### Node.js

```typescript
// tracing.ts - import FIRST, before any other module
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { Resource } from '@opentelemetry/resources';
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
  ATTR_DEPLOYMENT_ENVIRONMENT_NAME,
} from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: 'order-service',
    [ATTR_SERVICE_VERSION]: '1.2.0',
    [ATTR_DEPLOYMENT_ENVIRONMENT_NAME]: process.env.NODE_ENV,
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter(),
    exportIntervalMillis: 30000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingPaths: ['/health', '/ready'],
      },
      '@opentelemetry/instrumentation-express': { enabled: true },
      '@opentelemetry/instrumentation-pg': { enabled: true },
      '@opentelemetry/instrumentation-redis': { enabled: true },
    }),
  ],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());
```

### Python

```python
# Auto-instrumentation via CLI (zero-code)
# pip install opentelemetry-distro opentelemetry-exporter-otlp
# opentelemetry-bootstrap -a install
# opentelemetry-instrument python app.py

# Or programmatic setup:
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

resource = Resource.create({
    "service.name": "order-service",
    "service.version": "1.2.0",
    "deployment.environment": "production",
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
)
trace.set_tracer_provider(provider)

# Auto-instrument frameworks
FlaskInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument(engine=db_engine)
```

### Java (Agent)

```bash
# Download the Java agent
curl -Lo opentelemetry-javaagent.jar \
  https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar

# Run with agent
java -javaagent:opentelemetry-javaagent.jar \
  -Dotel.service.name=order-service \
  -Dotel.exporter.otlp.endpoint=http://otel-collector:4317 \
  -Dotel.traces.sampler=parentbased_traceidratio \
  -Dotel.traces.sampler.arg=0.1 \
  -jar app.jar
```

### Go (Manual Instrumentation)

```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
    "go.opentelemetry.io/otel/trace"
)

func initTracer(ctx context.Context) (*sdktrace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("order-service"),
            semconv.ServiceVersionKey.String("1.2.0"),
        )),
    )
    otel.SetTracerProvider(tp)
    return tp, nil
}

var tracer = otel.Tracer("order-service")

func processOrder(ctx context.Context, orderID string) error {
    ctx, span := tracer.Start(ctx, "order.process",
        trace.WithAttributes(attribute.String("order.id", orderID)),
    )
    defer span.End()

    // Nested span
    ctx, valSpan := tracer.Start(ctx, "order.validate")
    err := validateOrder(ctx, orderID)
    valSpan.End()

    if err != nil {
        span.RecordError(err)
        return err
    }
    return nil
}
```

## Context Propagation

### W3C TraceContext (Default)

```
# HTTP header format
traceparent: 00-<trace-id>-<span-id>-<trace-flags>
tracestate: vendor1=value1,vendor2=value2

# Example
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```

### Baggage (Cross-Service Metadata)

```typescript
import { propagation, context, ROOT_CONTEXT } from '@opentelemetry/api';

// Set baggage (upstream service)
const baggage = propagation.createBaggage({
  'user.id': { value: 'u-12345' },
  'tenant.id': { value: 't-67890' },
});
const ctx = propagation.setBaggage(context.active(), baggage);

// Read baggage (downstream service)
const bag = propagation.getBaggage(context.active());
const userId = bag?.getEntry('user.id')?.value;
```

## Sampling Strategies

| Strategy | Where | Use Case | Config |
|----------|-------|----------|--------|
| **AlwaysOn** | SDK | Dev/debug | `otel.traces.sampler=always_on` |
| **AlwaysOff** | SDK | Disable traces | `otel.traces.sampler=always_off` |
| **TraceIdRatio** | SDK (head) | Uniform sampling | `parentbased_traceidratio` + `arg=0.1` |
| **Tail Sampling** | Collector | Error/latency-based | `tail_sampling` processor |

### Decision Framework

```
Traffic < 100 RPS → AlwaysOn (keep everything)
Traffic 100-1000 RPS → Head-based 50% + tail sampling for errors
Traffic 1000-10000 RPS → Head-based 10% + tail sampling
Traffic > 10000 RPS → Head-based 1% + tail sampling for errors/slow
```

## Kubernetes Deployment

### DaemonSet Collector (Recommended for Production)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
        - name: collector
          image: otel/opentelemetry-collector-contrib:0.96.0
          ports:
            - containerPort: 4317  # OTLP gRPC
            - containerPort: 4318  # OTLP HTTP
            - containerPort: 8888  # Collector metrics
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 2Gi
          volumeMounts:
            - name: config
              mountPath: /etc/otelcol-contrib
      volumes:
        - name: config
          configMap:
            name: otel-collector-config
```

### Application Pods Configuration

```yaml
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://$(NODE_NAME):4317"  # Talk to local DaemonSet pod
  - name: OTEL_SERVICE_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.labels['app']
  - name: OTEL_RESOURCE_ATTRIBUTES
    value: "k8s.namespace.name=$(NAMESPACE),k8s.pod.name=$(POD_NAME)"
  - name: NODE_NAME
    valueFrom:
      fieldRef:
        fieldPath: spec.nodeName
```

## Cost Optimization

### Cardinality Control

```
HIGH CARDINALITY (AVOID as metric attributes):
  - user.id, request.id, session.id
  - full URL paths with IDs (/users/12345)
  - timestamps, UUIDs

LOW CARDINALITY (GOOD for metric attributes):
  - http.method (GET, POST, PUT, DELETE)
  - http.status_code (200, 404, 500)
  - service.name, environment
  - http.route template (/users/{id})
```

### Attribute Filtering in Collector

```yaml
processors:
  attributes:
    actions:
      # Remove high-cardinality attributes before export
      - key: http.url
        action: delete
      - key: user.id
        action: delete
      # Keep route template instead of full URL
      - key: http.target
        action: delete
```

### Volume Reduction Strategies

1. **Filter health checks** in collector (not in SDK) to keep local debugging
2. **Use tail sampling** to keep errors at 100% while sampling success at 1-10%
3. **Reduce metric export interval** from 15s to 60s for non-critical metrics
4. **Drop unused attributes** in the collector before exporting
5. **Use delta temporality** for counters to reduce storage (backend-dependent)

## Backend Selection Guide

| Backend | Traces | Metrics | Logs | Cost Model |
|---------|--------|---------|------|------------|
| Grafana Cloud | Tempo | Mimir | Loki | Per-usage |
| Datadog | Yes | Yes | Yes | Per-host + ingestion |
| New Relic | Yes | Yes | Yes | Per-GB ingested |
| Jaeger | Yes | No | No | Self-hosted |
| Elastic APM | Yes | Yes | Yes | Per-node or cloud |
| AWS X-Ray | Yes | CloudWatch | CloudWatch | Per-trace |

### Recommended Stack (Self-Hosted)

```
Traces  → Grafana Tempo (S3/GCS/Azure backend, low cost)
Metrics → Prometheus/Mimir (battle-tested, PromQL)
Logs    → Grafana Loki (label-based, S3 storage)
UI      → Grafana (unified dashboards, trace-metric-log correlation)
```

## Naming Conventions

### Spans

```
Format: <component>.<operation>
Examples:
  http.request
  db.query
  cache.get
  queue.publish
  order.process
  payment.charge
```

### Metrics

```
Format: <domain>.<target>.<measurement>
Examples:
  http.server.request.duration     (histogram)
  http.server.active_requests      (updowncounter)
  db.client.connections.usage      (updowncounter)
  messaging.process.duration       (histogram)
  order.processed.total            (counter)
```

Follow [OTel Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) for standard attributes and metric names.
