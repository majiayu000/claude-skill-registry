---
name: tracing-patterns
description: OpenTelemetry setup, span context propagation, sampling strategies, Jaeger queries
---

# Tracing Patterns

## OpenTelemetry Setup (Node.js)

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { Resource } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';
import { ParentBasedSampler, TraceIdRatioBasedSampler } from '@opentelemetry/sdk-trace-base';

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: 'order-service',
    [ATTR_SERVICE_VERSION]: process.env.APP_VERSION || '1.0.0',
    'deployment.environment': process.env.NODE_ENV || 'development',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
  }),
  sampler: new ParentBasedSampler({
    root: new TraceIdRatioBasedSampler(0.1), // 10% sampling
  }),
  instrumentations: [getNodeAutoInstrumentations({
    '@opentelemetry/instrumentation-fs': { enabled: false },
  })],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());
```

## Manual Span Creation

```typescript
import { trace, SpanStatusCode, SpanKind } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

async function processOrder(orderId: string): Promise<Order> {
  return tracer.startActiveSpan('processOrder', {
    kind: SpanKind.INTERNAL,
    attributes: { 'order.id': orderId },
  }, async (span) => {
    try {
      const order = await tracer.startActiveSpan('validateOrder', async (valSpan) => {
        const result = await validateOrder(orderId);
        valSpan.setAttribute('order.items_count', result.items.length);
        valSpan.end();
        return result;
      });

      await tracer.startActiveSpan('chargePayment', {
        kind: SpanKind.CLIENT,
        attributes: { 'payment.method': order.paymentMethod },
      }, async (paySpan) => {
        await chargePayment(order);
        paySpan.addEvent('payment_charged', { 'payment.amount': order.total });
        paySpan.end();
      });

      span.setStatus({ code: SpanStatusCode.OK });
      return order;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## Context Propagation (HTTP)

```typescript
import { propagation, context } from '@opentelemetry/api';

// Inject context into outgoing request
function makeRequest(url: string, options: RequestInit = {}): Promise<Response> {
  const headers: Record<string, string> = {};
  propagation.inject(context.active(), headers);
  return fetch(url, {
    ...options,
    headers: { ...options.headers, ...headers },
  });
}

// Extract context from incoming request (middleware)
function tracingMiddleware(req: Request, res: Response, next: NextFunction) {
  const parentContext = propagation.extract(context.active(), req.headers);
  context.with(parentContext, () => next());
}
```

## Sampling Strategies

```yaml
# Head-based: Decide at trace start
parent_based:
  root: trace_id_ratio(0.1)   # 10% of new traces
  # Child spans inherit parent decision

# Tail-based (Collector config): Decide after trace complete
processors:
  tail_sampling:
    policies:
      - name: error-traces
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-traces
        type: latency
        latency: { threshold_ms: 1000 }
      - name: baseline
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

## Jaeger Query Patterns

```
# Find slow traces for a service
service=order-service operation=processOrder minDuration=500ms

# Find error traces
service=order-service tags={"error":"true"}

# Cross-service trace
service=order-service operation=processOrder tags={"order.id":"ORD-123"}
```

## Checklist

- [ ] Every service has OTEL SDK initialized before app code
- [ ] Service name and version set in Resource attributes
- [ ] Context propagation configured for all HTTP/gRPC clients
- [ ] Error spans have exception recorded and status set to ERROR
- [ ] Sampling strategy defined (not 100% in production)
- [ ] Span attributes follow semantic conventions
- [ ] Sensitive data excluded from span attributes (no PII, passwords)
- [ ] Graceful shutdown calls sdk.shutdown() to flush pending spans

## Anti-Patterns

- Sampling 100% of traces in production (storage explosion)
- Not propagating context across async boundaries
- Adding PII (emails, SSNs) as span attributes
- Creating too many small spans (noise, overhead)
- Not recording exceptions on error spans
- Missing `span.end()` calls causing memory leaks
- Using span names with high cardinality (e.g., including IDs)
- Ignoring parent context in downstream services
