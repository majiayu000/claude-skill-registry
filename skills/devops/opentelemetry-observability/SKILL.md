/*============================================================================*/
/* OPENTELEMETRY-OBSERVABILITY SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: opentelemetry-observability
version: 1.0.0
description: |
  [assert|neutral] OpenTelemetry specialist for distributed tracing, metrics collection, log correlation, auto-instrumentation, custom spans, trace context propagation, and sampling strategies. Use when implementing obs [ground:given] [conf:0.95] [state:confirmed]
category: Observability
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute opentelemetry-observability workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic Observability processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "opentelemetry-observability",
  category: "Observability",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["opentelemetry-observability", "Observability", "workflow"],
  context: "user needs opentelemetry-observability capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# OpenTelemetry Observability Specialist

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Expert distributed tracing, metrics, and logging with OpenTelemetry for production observability.

## Purpose

Comprehensive OpenTelemetry expertise including auto-instrumentation, custom spans, metrics collection, log correlation, trace context propagation, and sampling. Ensures applications are fully observable with actionable telemetry data.

## When to Use

- Implementing distributed tracing in microservices
- Monitoring application performance (APM)
- Debugging production issues across services
- Setting up metrics collection and dashboards
- Correlating logs with traces
- Optimizing sampling strategies for cost/performance
- Migrating from proprietary APM to OpenTelemetry

## Prerequisites

**Required**: Understanding of distributed systems, HTTP, basic observability concepts

**Agents**: `cicd-engineer`, `perf-analyzer`, `backend-dev`, `system-architect`

## Core Workflows

### Workflow 1: Node.js Auto-Instrumentation

**Step 1: Install OpenTelemetry Packages**

```bash
npm install @opentelemetry/sdk-node \
  @opentelemetry/auto-instrumentations-node \
  @opentelemetry/exporter-trace-otlp-http \
  @opentelemetry/exporter-metrics-otlp-http
```

**Step 2: Initialize OpenTelemetry**

```javascript
// instrumentation.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-http');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4318/v1/traces',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: 'http://localhost:4318/v1/metrics',
    }),
    exportIntervalMillis: 60000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': { enabled: true },
      '@opentelemetry/instrumentation-express': { enabled: true },
      '@opentelemetry/instrumentation-pg': { enabled: true },
      '@opentelemetry/instrumentation-redis': { enabled: true },
    }),
  ],
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown().then(
    () => console.log('Tracing terminated'),
    (err) => console.log('Error terminating tracing', err)
  );
});
```

**Step 3: Start Application with Instrumentation**

```bash
node --require ./instrumentation.js app.js
```

### Workflow 2: Custom Spans and Attributes

```javascript
const { trace } = require('@opentelemetry/api');

const tracer = trace.getTracer('my-service', '1.0.0');

async function processOrder(orderId) {
  const span = tracer.startSpan('processOrder', {
    attributes: {
      'order.id': orderId,
      'order.priority': 'high',
    },
  });

  try {
    // Set span status
    span.setStatus({ code: SpanStatusCode.OK });

    // Add event to span
    span.addEvent('order_validated', {
      'validation.result': 'success',
    });

    // Child span
    const childSpan = tracer.startSpan('calculateTotal', {
      parent: span,
    });
    const total = await calculateTotal(orderId);
    childSpan.setAttribute('order.total', total);
    childSpan.end();

    return total;
  } catch (error) {
    // Record exception
    span.recordException(error);
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    throw error;
  } finally {
    span.end();
  }
}
```

### Workfl

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/Observability/opentelemetry-observability/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "opentelemetry-observability-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>OPENTELEMETRY_OBSERVABILITY_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
