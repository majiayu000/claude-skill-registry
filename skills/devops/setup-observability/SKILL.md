---
name: setup-observability
description: "Step-by-step guide for implementing comprehensive observability with structured logging, metrics, distributed tracing, and alerting using cloud-agnostic patterns."
---

# Skill: Setup Observability

This skill teaches you how to implement comprehensive observability for your  microservices. You'll set up the three pillars of observability—logs, metrics, and traces—with proper correlation, dashboards, and alerting.

Without observability, you cannot run distributed systems. When something breaks, you need to answer: What broke? Where? Why? What was the customer impact? This skill ensures you can answer all these questions within minutes.

Observability is not optional instrumentation added after the fact. It's a core architectural concern that must be built into every service from day one.

## Prerequisites

- Understanding of Clean Architecture and handler patterns
- Existing microservice following  patterns
- Cloud provider monitoring services access (CloudWatch, Stackdriver, Azure Monitor)
- Distributed tracing service access (X-Ray, Cloud Trace, Jaeger)

## Overview

In this skill, you will:
1. Set up structured JSON logging with consistent fields
2. Implement correlation ID propagation across services
3. Configure metrics collection (latency, errors, saturation)
4. Enable distributed tracing with OpenTelemetry patterns
5. Set up DLQ monitoring for async processing
6. Create monitoring dashboards
7. Configure alerting with thresholds and owners

## Step 1: Set Up Structured Logging

Structured logging is the foundation of observability. All logs must be JSON with consistent fields for machine parsing.

### Logger Interface

```pseudocode
TYPE LogLevel
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
END TYPE

TYPE LogEntry
    timestamp: String
    level: LogLevel
    service: String
    correlationId: String (optional)
    traceId: String (optional)
    spanId: String (optional)
    message: String
    error: String (optional)
    fields: Map<String, Any> (optional)
END TYPE

INTERFACE LoggerPort
    METHOD Info(ctx: Context, msg: String, fields: Map<String, Any>)
    METHOD Error(ctx: Context, msg: String, err: Error, fields: Map<String, Any>)
    METHOD Warn(ctx: Context, msg: String, fields: Map<String, Any>)
    METHOD Debug(ctx: Context, msg: String, fields: Map<String, Any>)
    METHOD WithFields(fields: Map<String, Any>) RETURNS FieldLogger
END INTERFACE

TYPE Logger IMPLEMENTS LoggerPort
    serviceName: String
    output: JsonEncoder

CONSTRUCTOR NewLogger(serviceName: String) RETURNS Logger
    RETURN Logger{
        serviceName: serviceName,
        output: NewJsonEncoder(stdout)
    }
END CONSTRUCTOR

METHOD Logger.log(ctx: Context, level: LogLevel, msg: String, fields: Map<String, Any>, err: Error)
    entry = LogEntry{
        timestamp: CurrentTimeUTC().Format(RFC3339Nano),
        level: level,
        service: this.serviceName,
        correlationId: GetCorrelationID(ctx),
        traceId: GetTraceID(ctx),
        spanId: GetSpanID(ctx),
        message: msg,
        fields: fields
    }

    IF err IS NOT NULL THEN
        entry.error = err.Message()
    END IF

    // Write to stdout for log aggregation
    this.output.Encode(entry)
END METHOD

METHOD Logger.Info(ctx: Context, msg: String, fields: Map<String, Any>)
    this.log(ctx, LogLevel.INFO, msg, fields, NULL)
END METHOD

METHOD Logger.Error(ctx: Context, msg: String, err: Error, fields: Map<String, Any>)
    this.log(ctx, LogLevel.ERROR, msg, fields, err)
END METHOD

METHOD Logger.Warn(ctx: Context, msg: String, fields: Map<String, Any>)
    this.log(ctx, LogLevel.WARN, msg, fields, NULL)
END METHOD

METHOD Logger.Debug(ctx: Context, msg: String, fields: Map<String, Any>)
    this.log(ctx, LogLevel.DEBUG, msg, fields, NULL)
END METHOD

METHOD Logger.WithFields(fields: Map<String, Any>) RETURNS FieldLogger
    RETURN FieldLogger{logger: this, fields: fields}
END METHOD

TYPE FieldLogger
    logger: Logger
    fields: Map<String, Any>

METHOD FieldLogger.Info(ctx: Context, msg: String, additionalFields: Map<String, Any>)
    merged = MergeMaps(this.fields, additionalFields)
    this.logger.Info(ctx, msg, merged)
END METHOD
```

Structured logging ensures every log entry can be queried at scale. The consistent field names (`correlation_id`, `service`, `level`) enable log analytics queries.

### Example Log Output

```json
{
  "timestamp": "2024-01-15T10:30:00.123456Z",
  "level": "info",
  "service": "facilitysvc",
  "correlation_id": "corr-abc-123",
  "trace_id": "1-5f84c7a1-abcdef123456789",
  "message": "Facility created",
  "fields": {
    "facility_id": "fac-456",
    "duration_ms": 45
  }
}
```

## Step 2: Implement Correlation ID Propagation

Every request must have a correlation ID that follows it through all service calls. This is critical for debugging distributed failures.

### Context Keys and Middleware

```pseudocode
TYPE ContextKey
    CORRELATION_ID = "correlation_id"
    TRACE_ID = "trace_id"
    SPAN_ID = "span_id"
END TYPE

TYPE HeaderName
    CORRELATION_ID = "X-Correlation-ID"
    TRACE_ID = "X-Trace-Id"
END TYPE

FUNCTION GetCorrelationID(ctx: Context) RETURNS String
    value = ctx.Value(ContextKey.CORRELATION_ID)
    IF value IS NOT NULL THEN
        RETURN value AS String
    END IF
    RETURN ""
END FUNCTION

FUNCTION GetTraceID(ctx: Context) RETURNS String
    value = ctx.Value(ContextKey.TRACE_ID)
    IF value IS NOT NULL THEN
        RETURN value AS String
    END IF
    RETURN ""
END FUNCTION

FUNCTION GetSpanID(ctx: Context) RETURNS String
    value = ctx.Value(ContextKey.SPAN_ID)
    IF value IS NOT NULL THEN
        RETURN value AS String
    END IF
    RETURN ""
END FUNCTION

FUNCTION WithCorrelationID(ctx: Context, correlationId: String) RETURNS Context
    RETURN ctx.WithValue(ContextKey.CORRELATION_ID, correlationId)
END FUNCTION

FUNCTION WithTraceID(ctx: Context, traceId: String) RETURNS Context
    RETURN ctx.WithValue(ContextKey.TRACE_ID, traceId)
END FUNCTION

FUNCTION WithSpanID(ctx: Context, spanId: String) RETURNS Context
    RETURN ctx.WithValue(ContextKey.SPAN_ID, spanId)
END FUNCTION

FUNCTION NewCorrelationID() RETURNS String
    RETURN "corr-" + GenerateUUID().Substring(0, 8)
END FUNCTION

FUNCTION ExtractOrCreateCorrelationID(headers: Map<String, String>) RETURNS String
    IF headers.Contains(HeaderName.CORRELATION_ID) AND headers[HeaderName.CORRELATION_ID] != "" THEN
        RETURN headers[HeaderName.CORRELATION_ID]
    END IF
    // Also check lowercase variant
    IF headers.Contains("x-correlation-id") AND headers["x-correlation-id"] != "" THEN
        RETURN headers["x-correlation-id"]
    END IF
    RETURN NewCorrelationID()
END FUNCTION

FUNCTION PropagateHeaders(ctx: Context) RETURNS Headers
    headers = NewHeaders()
    correlationId = GetCorrelationID(ctx)
    IF correlationId != "" THEN
        headers.Set(HeaderName.CORRELATION_ID, correlationId)
    END IF
    traceId = GetTraceID(ctx)
    IF traceId != "" THEN
        headers.Set(HeaderName.TRACE_ID, traceId)
    END IF
    RETURN headers
END FUNCTION
```

### Handler Middleware for Correlation

```pseudocode
TYPE ObservabilityMiddleware
    logger: Logger

CONSTRUCTOR NewObservabilityMiddleware(serviceName: String) RETURNS ObservabilityMiddleware
    RETURN ObservabilityMiddleware{
        logger: NewLogger(serviceName)
    }
END CONSTRUCTOR

METHOD ObservabilityMiddleware.WrapAPIHandler(handler: APIHandlerFunc) RETURNS APIHandlerFunc
    RETURN FUNCTION(ctx: Context, request: APIRequest) RETURNS Result<APIResponse, Error>
        // Extract or create correlation ID
        correlationId = ExtractOrCreateCorrelationID(request.Headers)
        ctx = WithCorrelationID(ctx, correlationId)

        // Extract trace ID if present from environment or headers
        traceId = GetEnvironmentVariable("TRACE_ID")
        IF traceId != "" THEN
            ctx = WithTraceID(ctx, traceId)
        END IF

        // Log request start
        this.logger.Info(ctx, "Request started", {
            "method": request.HTTPMethod,
            "path": request.Path,
            "request_id": request.RequestId
        })

        // Call handler
        result = handler(ctx, request)

        // Log request completion
        IF result.IsError() THEN
            this.logger.Error(ctx, "Request failed", result.Error(), {
                "method": request.HTTPMethod,
                "path": request.Path
            })
        ELSE
            response = result.Value()
            this.logger.Info(ctx, "Request completed", {
                "method": request.HTTPMethod,
                "path": request.Path,
                "status_code": response.StatusCode
            })
        END IF

        // Add correlation ID to response headers
        IF result.IsOk() THEN
            response = result.Value()
            IF response.Headers IS NULL THEN
                response.Headers = NewMap()
            END IF
            response.Headers[HeaderName.CORRELATION_ID] = correlationId
        END IF

        RETURN result
    END FUNCTION
END METHOD
```

Correlation IDs flow through the entire request path. When a customer reports an issue, search by correlation ID to see the complete trace across all services.

## Step 3: Configure Metrics Collection

Metrics tell you how the system behaves over time. Focus on latency percentiles, error rates, and saturation metrics.

### Metrics Collector

```pseudocode
INTERFACE MetricsPublisher
    METHOD PublishMetrics(ctx: Context, metrics: List<MetricDatum>) RETURNS Result<Void, Error>
END INTERFACE

TYPE MetricDatum
    name: String
    value: Float64
    unit: MetricUnit
    dimensions: Map<String, String>
    timestamp: DateTime

TYPE MetricUnit
    MILLISECONDS = "milliseconds"
    COUNT = "count"
    PERCENT = "percent"
    BYTES = "bytes"
END TYPE

TYPE MetricsCollector
    publisher: MetricsPublisher
    namespace: String
    serviceName: String
    dimensions: Map<String, String>
    buffer: List<MetricDatum>

CONSTRUCTOR NewMetricsCollector(publisher: MetricsPublisher, namespace: String, serviceName: String) RETURNS MetricsCollector
    RETURN MetricsCollector{
        publisher: publisher,
        namespace: namespace,
        serviceName: serviceName,
        dimensions: {"Service": serviceName},
        buffer: NewList()
    }
END CONSTRUCTOR

METHOD MetricsCollector.RecordLatency(ctx: Context, operation: String, duration: Duration)
    datum = MetricDatum{
        name: "Latency",
        value: duration.Milliseconds(),
        unit: MetricUnit.MILLISECONDS,
        dimensions: MergeMaps(this.dimensions, {"Operation": operation}),
        timestamp: CurrentTimeUTC()
    }
    this.buffer.Add(datum)
END METHOD

METHOD MetricsCollector.RecordError(ctx: Context, operation: String, errorType: String)
    datum = MetricDatum{
        name: "Errors",
        value: 1,
        unit: MetricUnit.COUNT,
        dimensions: MergeMaps(this.dimensions, {"Operation": operation, "ErrorType": errorType}),
        timestamp: CurrentTimeUTC()
    }
    this.buffer.Add(datum)
END METHOD

METHOD MetricsCollector.RecordSuccess(ctx: Context, operation: String)
    datum = MetricDatum{
        name: "Success",
        value: 1,
        unit: MetricUnit.COUNT,
        dimensions: MergeMaps(this.dimensions, {"Operation": operation}),
        timestamp: CurrentTimeUTC()
    }
    this.buffer.Add(datum)
END METHOD

METHOD MetricsCollector.Flush(ctx: Context) RETURNS Result<Void, Error>
    IF this.buffer.IsEmpty() THEN
        RETURN Ok(Void)
    END IF

    // Publish in batches (max 20 per call typically)
    FOR batch IN this.buffer.Chunk(20) DO
        result = this.publisher.PublishMetrics(ctx, batch)
        IF result.IsError() THEN
            RETURN result
        END IF
    END FOR

    this.buffer.Clear()
    RETURN Ok(Void)
END METHOD
```

### Instrumenting Use Cases

```pseudocode
FUNCTION InstrumentedOperation<T>(
    ctx: Context,
    metrics: MetricsCollector,
    logger: Logger,
    operationName: String,
    operation: Function() RETURNS Result<T, Error>
) RETURNS Result<T, Error>
    start = CurrentTime()

    result = operation()

    duration = CurrentTime() - start

    // Record latency
    metrics.RecordLatency(ctx, operationName, duration)

    // Record success or error
    IF result.IsError() THEN
        metrics.RecordError(ctx, operationName, GetErrorType(result.Error()))
        logger.Error(ctx, "Operation failed", result.Error(), {
            "operation": operationName,
            "duration_ms": duration.Milliseconds()
        })
    ELSE
        metrics.RecordSuccess(ctx, operationName)
        logger.Info(ctx, "Operation completed", {
            "operation": operationName,
            "duration_ms": duration.Milliseconds()
        })
    END IF

    RETURN result
END FUNCTION
```

## Step 4: Enable Distributed Tracing

Distributed tracing shows the path a request took across services. Use OpenTelemetry patterns for comprehensive traces.

### Tracing Integration

```pseudocode
INTERFACE TracingPort
    METHOD StartSegment(ctx: Context, name: String) RETURNS (Context, SegmentCloser)
    METHOD StartSubsegment(ctx: Context, name: String) RETURNS (Context, SegmentCloser)
    METHOD AddAnnotation(ctx: Context, key: String, value: Any)
    METHOD AddMetadata(ctx: Context, key: String, value: Any)
END INTERFACE

TYPE SegmentCloser
    METHOD Close(err: Error)
END TYPE

TYPE Tracer IMPLEMENTS TracingPort
    serviceName: String

CONSTRUCTOR NewTracer(serviceName: String) RETURNS Tracer
    // Configure tracing provider
    ConfigureTracing({
        serviceVersion: "1.0.0"
    })

    RETURN Tracer{serviceName: serviceName}
END CONSTRUCTOR

METHOD Tracer.StartSegment(ctx: Context, name: String) RETURNS (Context, SegmentCloser)
    ctx, segment = BeginSegment(ctx, name)

    // Add service metadata
    segment.AddMetadata("service", this.serviceName)

    closer = SegmentCloser{
        segment: segment,
        Close: FUNCTION(err: Error)
            IF err IS NOT NULL THEN
                segment.AddError(err)
            END IF
            segment.Close(err)
        END FUNCTION
    }

    RETURN (ctx, closer)
END METHOD

METHOD Tracer.AddAnnotation(ctx: Context, key: String, value: Any)
    segment = GetSegment(ctx)
    IF segment IS NOT NULL THEN
        segment.AddAnnotation(key, value)
    END IF
END METHOD
```

Traces show the complete request path. Annotations like `correlation_id` enable searching traces by customer-reported issues.

## Step 5: Monitor Dead-Letter Queues

DLQs catch failed async messages. Without monitoring, failed messages disappear silently.

### DLQ Monitor

```pseudocode
INTERFACE QueueClient
    METHOD GetQueueAttributes(ctx: Context, queueUrl: String, attributes: List<String>) RETURNS Result<Map<String, String>, Error>
END INTERFACE

TYPE DLQMonitor
    queueClient: QueueClient
    logger: Logger
    metrics: MetricsCollector
    queues: Map<String, String>  // name -> URL mapping

CONSTRUCTOR NewDLQMonitor(client: QueueClient, logger: Logger, metrics: MetricsCollector) RETURNS DLQMonitor
    RETURN DLQMonitor{
        queueClient: client,
        logger: logger,
        metrics: metrics,
        queues: NewMap()
    }
END CONSTRUCTOR

METHOD DLQMonitor.RegisterQueue(name: String, url: String)
    this.queues[name] = url
END METHOD

METHOD DLQMonitor.CheckAllQueues(ctx: Context) RETURNS Result<Void, Error>
    FOR EACH (name, url) IN this.queues DO
        result = this.checkQueue(ctx, name, url)
        IF result.IsError() THEN
            this.logger.Error(ctx, "Failed to check DLQ", result.Error(), {
                "queue_name": name
            })
        END IF
    END FOR
    RETURN this.metrics.Flush(ctx)
END METHOD
```

DLQ monitoring is critical for async systems. A growing DLQ means messages are failing silently. Alert on depth and age.

## Step 6: Create Monitoring Dashboards

Dashboards provide at-a-glance health visibility. Create a dashboard for each service.

### Dashboard Builder

```pseudocode
TYPE DashboardBuilder
    publisher: DashboardPublisher
    namespace: String
    serviceName: String
    widgets: List<Map<String, Any>>

CONSTRUCTOR NewDashboardBuilder(publisher: DashboardPublisher, namespace: String, serviceName: String) RETURNS DashboardBuilder
    RETURN DashboardBuilder{
        publisher: publisher,
        namespace: namespace,
        serviceName: serviceName,
        widgets: NewList()
    }
END CONSTRUCTOR

METHOD DashboardBuilder.AddLatencyWidget(title: String, operations: List<String>, x: Int, y: Int, width: Int, height: Int)
    metrics = NewList()
    FOR EACH op IN operations DO
        metrics.Add([this.namespace, "Latency", "Service", this.serviceName, "Operation", op, {"stat": "p50"}])
        metrics.Add(["...", {"stat": "p95"}])
        metrics.Add(["...", {"stat": "p99"}])
    END FOR

    widget = {
        "type": "metric",
        "x": x, "y": y, "width": width, "height": height,
        "properties": {
            "title": title,
            "view": "timeSeries",
            "metrics": metrics
        }
    }
    this.widgets.Add(widget)
END METHOD

METHOD DashboardBuilder.Build(ctx: Context) RETURNS Result<Void, Error>
    body = {"widgets": this.widgets}
    dashboardName = this.serviceName + "-dashboard"
    RETURN this.publisher.PutDashboard(ctx, dashboardName, JsonSerialize(body))
END METHOD
```

## Step 7: Set Up Alerting

Metrics without alerts mean you only find problems when customers complain. Set thresholds and alert.

### Alarm Configuration

```pseudocode
TYPE AlarmConfig
    name: String
    description: String
    metricName: String
    namespace: String
    statistic: String
    period: Int32
    evaluationPeriods: Int32
    threshold: Float64
    comparisonOperator: ComparisonOperator
    dimensions: Map<String, String>
    notificationTarget: String
    owner: String

TYPE AlarmManager
    publisher: AlarmPublisher

METHOD AlarmManager.CreateStandardAlarms(ctx: Context, serviceName: String, namespace: String, notificationTarget: String) RETURNS Result<Void, Error>
    alarms = [
        AlarmConfig{
            name: serviceName + "-high-error-rate",
            description: "Error rate exceeds 1% of requests",
            metricName: "Errors",
            threshold: 10,
            owner: "Platform Team"
        },
        AlarmConfig{
            name: serviceName + "-high-latency-p99",
            description: "P99 latency exceeds 5 seconds",
            metricName: "Latency",
            threshold: 5000,
            owner: "Platform Team"
        },
        AlarmConfig{
            name: serviceName + "-dlq-depth",
            description: "DLQ has messages - async processing failures",
            metricName: "DLQDepth",
            threshold: 1,
            owner: "Platform Team"
        }
    ]

    FOR EACH alarm IN alarms DO
        result = this.CreateAlarm(ctx, alarm)
        IF result.IsError() THEN
            RETURN result
        END IF
    END FOR

    RETURN Ok(Void)
END METHOD
```

Every alarm needs: a threshold, an owner, and a response plan. Alarms without response plans are noise.

## Verification Checklist

After setting up observability, verify:

- [ ] All logs are JSON with consistent fields (timestamp, level, service, correlation_id)
- [ ] Correlation ID is generated at edge and propagated through all service calls
- [ ] Correlation ID appears in all log entries and traces
- [ ] Latency metrics record p50, p95, p99 for each operation
- [ ] Error rate is tracked per operation and error type
- [ ] Distributed tracing is enabled with searchable annotations
- [ ] DLQ depth is monitored with alerts
- [ ] Dashboard exists with latency, errors, and DLQ widgets
- [ ] Alarms have thresholds, owners, and response plans
- [ ] Business metrics are tracked (optimizations completed, schedules calculated)
- [ ] Log analytics queries work with correlation ID filter
- [ ] Team can answer "what, where, why, impact" for any incident
