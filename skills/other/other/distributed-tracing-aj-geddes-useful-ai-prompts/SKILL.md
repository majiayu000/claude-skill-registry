---
name: distributed-tracing
description: Implement distributed tracing with Jaeger and Zipkin for tracking requests across microservices. Use when debugging distributed systems, tracking request flows, or analyzing service performance.
---

# Distributed Tracing

## Overview

Set up distributed tracing infrastructure with Jaeger or Zipkin to track requests across microservices and identify performance bottlenecks.

## When to Use

- Debugging microservice interactions
- Identifying performance bottlenecks
- Tracking request flows
- Analyzing service dependencies
- Root cause analysis

## Instructions

### 1. **Jaeger Setup**

```yaml
# docker-compose.yml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "16686:16686"
      - "14268:14268"
    networks:
      - tracing

networks:
  tracing:
```

### 2. **Node.js Jaeger Instrumentation**

```javascript
// tracing.js
const initTracer = require('jaeger-client').initTracer;
const opentracing = require('opentracing');

const initJaegerTracer = (serviceName) => {
  const config = {
    serviceName: serviceName,
    sampler: {
      type: 'const',
      param: 1
    },
    reporter: {
      logSpans: true,
      agentHost: process.env.JAEGER_AGENT_HOST || 'localhost',
      agentPort: process.env.JAEGER_AGENT_PORT || 6831
    }
  };

  return initTracer(config, {});
};

const tracer = initJaegerTracer('api-service');
module.exports = { tracer };
```

### 3. **Express Tracing Middleware**

```javascript
// middleware.js
const { tracer } = require('./tracing');
const opentracing = require('opentracing');

const tracingMiddleware = (req, res, next) => {
  const wireCtx = tracer.extract(
    opentracing.FORMAT_HTTP_HEADERS,
    req.headers
  );

  const span = tracer.startSpan(req.path, {
    childOf: wireCtx,
    tags: {
      [opentracing.Tags.SPAN_KIND]: opentracing.Tags.SPAN_KIND_RPC_SERVER,
      [opentracing.Tags.HTTP_METHOD]: req.method,
      [opentracing.Tags.HTTP_URL]: req.url
    }
  });

  req.span = span;

  res.on('finish', () => {
    span.setTag(opentracing.Tags.HTTP_STATUS_CODE, res.statusCode);
    span.finish();
  });

  next();
};

module.exports = tracingMiddleware;
```

### 4. **Python Jaeger Integration**

```python
# tracing.py
from jaeger_client import Config
from opentracing.propagation import Format

def init_jaeger_tracer(service_name):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {
                'reporting_host': 'localhost',
                'reporting_port': 6831,
            },
            'logging': True,
        },
        service_name=service_name,
    )
    return config.initialize_tracer()

# Flask integration
from flask import Flask, request

app = Flask(__name__)
tracer = init_jaeger_tracer('api-service')

@app.before_request
def before_request():
    ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    request.span = tracer.start_span(
        request.path,
        child_of=ctx,
        tags={
            'http.method': request.method,
            'http.url': request.url,
        }
    )

@app.after_request
def after_request(response):
    request.span.set_tag('http.status_code', response.status_code)
    request.span.finish()
    return response

@app.route('/api/users/<user_id>')
def get_user(user_id):
    with tracer.start_span('fetch-user', child_of=request.span) as span:
        span.set_tag('user.id', user_id)
        # Fetch user from database
        return {'user': {'id': user_id}}
```

### 5. **Distributed Context Propagation**

```javascript
// propagation.js
const axios = require('axios');
const { tracer } = require('./tracing');
const opentracing = require('opentracing');

async function callDownstreamService(span, url, data) {
  const headers = {};

  // Inject trace context
  tracer.inject(span, opentracing.FORMAT_HTTP_HEADERS, headers);

  try {
    const response = await axios.post(url, data, { headers });
    span.setTag('downstream.success', true);
    return response.data;
  } catch (error) {
    span.setTag(opentracing.Tags.ERROR, true);
    span.log({
      event: 'error',
      message: error.message
    });
    throw error;
  }
}

module.exports = { callDownstreamService };
```

### 6. **Zipkin Integration**

```javascript
// zipkin-setup.js
const CLSContext = require('zipkin-context-cls');
const { Tracer, BatchRecorder, HttpLogger } = require('zipkin');
const zipkinMiddleware = require('zipkin-instrumentation-express').expressMiddleware;

const recorder = new BatchRecorder({
  logger: new HttpLogger({
    endpoint: 'http://localhost:9411/api/v2/spans',
    headers: { 'Content-Type': 'application/json' }
  })
});

const ctxImpl = new CLSContext('zipkin');
const tracer = new Tracer({ recorder, ctxImpl });

module.exports = {
  tracer,
  zipkinMiddleware: zipkinMiddleware({
    tracer,
    serviceName: 'api-service'
  })
};
```

### 7. **Trace Analysis**

```python
# query-traces.py
import requests

def query_traces(service_name, operation=None, limit=20):
    params = {
        'service': service_name,
        'limit': limit
    }
    if operation:
        params['operation'] = operation

    response = requests.get('http://localhost:16686/api/traces', params=params)
    return response.json()['data']

def find_slow_traces(service_name, min_duration_ms=1000):
    traces = query_traces(service_name, limit=100)
    slow_traces = [
        t for t in traces
        if t['duration'] > min_duration_ms * 1000
    ]
    return sorted(slow_traces, key=lambda t: t['duration'], reverse=True)
```

## Best Practices

### ✅ DO
- Sample appropriately for your traffic volume
- Propagate trace context across services
- Add meaningful span tags
- Log errors with spans
- Use consistent service naming
- Monitor trace latency
- Document trace format
- Keep instrumentation lightweight

### ❌ DON'T
- Sample 100% in production
- Skip trace context propagation
- Log sensitive data in spans
- Create excessive spans
- Ignore sampling configuration
- Use unbounded cardinality tags
- Deploy without testing collection

## Key Concepts

- **Trace**: Complete request flow across services
- **Span**: Single operation within a trace
- **Tag**: Metadata attached to spans
- **Log**: Timestamped events within spans
- **Context**: Trace information propagated between services
