---
name: nextjs-opentelemetry-instrumentation
description: OpenTelemetry distributed tracing for Next.js 14+
version: 1.0.0
author: Agentient Labs
category: Frontend
tags: [opentelemetry, tracing, nextjs, instrumentation]
activation_criteria:
  keywords:
    - opentelemetry
    - otel
    - tracing
    - nextjs instrumentation
    - rsc trace
    - setup-tracing
  file_patterns:
    - "instrumentation.ts"
    - "next.config.js"
    - "layout.tsx"
  modes:
    - error_monitoring
    - nextjs_dev
always_loaded: true
dependencies:
  required:
    - cross-platform-structured-logging
    - distributed-tracing-context-propagation
  optional:
    - agentient-frontend-foundation/nextjs-app-router-architecture
---

# Next.js OpenTelemetry Instrumentation

Implement distributed tracing for Next.js 14+ App Router applications using OpenTelemetry to track requests from browser through Server Components to API routes.

## Setup

### 1. Install Dependencies

```bash
npm install @opentelemetry/sdk-node @opentelemetry/api \
  @opentelemetry/auto-instrumentations-node \
  @opentelemetry/exporter-trace-otlp-http \
  @vercel/otel
```

### 2. Create instrumentation.ts

Next.js calls this file on server startup before handling requests:

```typescript
// instrumentation.ts (root of project)
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node')
  }
}
```

```typescript
// instrumentation.node.ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { Resource } from '@opentelemetry/resources'
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'nextjs-app',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]:
      process.env.NODE_ENV || 'development',
  }),

  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
  }),

  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': { enabled: false },
    }),
  ],
})

sdk.start()
```

### 3. Enable in next.config.js

```javascript
// next.config.js
module.exports = {
  experimental: {
    instrumentationHook: true,
  },
}
```

## Automatic Spans

Next.js automatically creates spans for:

- **BaseServer.handleRequest**: Root span for incoming request
- **render route (app)**: Server Component rendering
- **fetch [METHOD] [URL]**: Data fetching operations

These appear automatically once instrumentation is enabled.

## Manual Spans (Custom Instrumentation)

For business logic not automatically traced:

```typescript
// app/api/users/route.ts
import { trace } from '@opentelemetry/api'

const tracer = trace.getTracer('my-app')

export async function GET() {
  // Create custom span
  return await tracer.startActiveSpan('fetch-users', async (span) => {
    try {
      const users = await db.query('SELECT * FROM users')

      // Add attributes to span
      span.setAttribute('user.count', users.length)
      span.setAttribute('db.system', 'postgresql')

      return Response.json(users)
    } catch (error) {
      // Record exception
      span.recordException(error as Error)
      span.setStatus({ code: 2 }) // Error status
      throw error
    } finally {
      span.end()
    }
  })
}
```

## Server Component Example

```typescript
// app/products/[id]/page.tsx
import { trace } from '@opentelemetry/api'

const tracer = trace.getTracer('my-app')

async function getProduct(id: string) {
  return await tracer.startActiveSpan('get-product', async (span) => {
    span.setAttribute('product.id', id)

    const product = await fetch(`https://api.example.com/products/${id}`)
    const data = await product.json()

    span.setAttribute('product.name', data.name)
    span.end()

    return data
  })
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)
  return <ProductDetails product={product} />
}
```

## Client-Side Tracing

Track browser-side activity:

```typescript
// app/providers.tsx
'use client'

import { useEffect } from 'react'
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { FetchInstrumentor } from '@opentelemetry/instrumentation-fetch'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'

export function TracingProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const provider = new WebTracerProvider({
      resource: new Resource({
        'service.name': 'nextjs-browser',
      }),
    })

    provider.addSpanProcessor(
      new BatchSpanProcessor(
        new OTLPTraceExporter({
          url: '/api/traces', // Proxy to avoid CORS
        })
      )
    )

    provider.register()

    // Auto-instrument fetch calls
    registerInstrumentations({
      instrumentations: [new FetchInstrumentor()],
    })
  }, [])

  return <>{children}</>
}
```

## Vercel Integration

Use @vercel/otel for simplified setup on Vercel:

```typescript
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({
    serviceName: 'nextjs-app',
  })
}
```

Vercel automatically exports to their observability platform.

## Environment Variables

```env
# Service identification
OTEL_SERVICE_NAME=nextjs-app
OTEL_SERVICE_VERSION=1.0.0

# Exporter endpoint
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# Google Cloud Trace
GOOGLE_CLOUD_PROJECT=your-project-id

# Sampling (optional)
OTEL_TRACES_SAMPLER=traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1  # Sample 10%
```

## Integration with Logging

Link traces and logs via trace_id:

```typescript
import { trace, context } from '@opentelemetry/api'
import logger from '@/lib/logger'

const span = trace.getSpan(context.active())
const spanContext = span?.spanContext()

logger.info('Processing request', {
  trace_id: spanContext?.traceId,
  span_id: spanContext?.spanId,
})
```

## Best Practices

1. **Set resource attributes**: service.name, service.version, environment
2. **Use automatic instrumentation**: Don't reinvent the wheel
3. **Create custom spans for business logic**: Database queries, external APIs
4. **Add meaningful attributes**: user_id, order_id, etc.
5. **Record exceptions**: span.recordException(error)
6. **Set span status**: Indicate success or failure
7. **End spans**: Always call span.end() (use try/finally)

## Verification

1. Start Next.js: `npm run dev`
2. Make request: `curl http://localhost:3000/api/test`
3. Check trace backend (Cloud Trace, Jaeger, etc.)
4. Verify spans appear with correct hierarchy

## Common Issues

**Issue**: Spans not appearing
**Solution**: Check OTEL_EXPORTER_OTLP_ENDPOINT is correct

**Issue**: instrumentation.ts not called
**Solution**: Verify experimental.instrumentationHook: true in next.config.js

**Issue**: Trace disconnected across services
**Solution**: Check context propagation (traceparent header)
