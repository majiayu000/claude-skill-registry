---
name: 183-observability-tracing-opentelemetry
description: Use when you need to implement or improve distributed tracing with OpenTelemetry in Java — including trace/span modeling, context propagation, semantic conventions, span attributes/events/status, sampling strategy, baggage usage, privacy safeguards, and backend integration with OTLP collectors.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Distributed Tracing with OpenTelemetry

## Role

You are a Senior software engineer with extensive experience in Java software development

## Goal

Effective distributed tracing with OpenTelemetry in Java requires clear span boundaries, reliable context propagation,
semantic consistency, and strict privacy controls.
Traces should help diagnose latency, failure causes, and cross-service dependencies without introducing excessive overhead.

## Constraints

Tracing data must remain safe and operationally useful. Incorrect propagation or sensitive attributes reduce trust in telemetry.

- **CONTEXT CONTINUITY**: Ensure trace context is propagated across HTTP/messaging/async boundaries
- **SEMANTIC CONSISTENCY**: Use stable span names and OpenTelemetry semantic conventions where applicable
- **DATA MINIMIZATION**: Avoid high-cardinality and sensitive attributes in spans/events
- **SAMPLING STRATEGY**: Configure sampling per environment to balance cost and diagnostic depth

## Examples

### Table of contents

- Example 1: Create Spans with Clear Boundaries
- Example 2: Propagate Context and Keep Attributes Safe
- Example 3: Apply OpenTelemetry Semantic Conventions
- Example 4: Configure Sampling Strategy per Environment
- Example 5: Validate Span Correctness with Tests
- Example 6: Use Annotation-Based Instrumentation for Service Methods

### Example 1: Create Spans with Clear Boundaries

Title: Model request and dependency calls as parent/child spans
Description: 

**Good example:**

```java
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

public final class CheckoutTracing {

    private final Tracer tracer;

    public CheckoutTracing(OpenTelemetry openTelemetry) {
        this(openTelemetry.getTracer("checkout-service"));
    }

    CheckoutTracing(Tracer tracer) {
        this.tracer = tracer;
    }

    public void checkout(String orderId) {
        Span parent = tracer.spanBuilder("checkout.process")
                .setSpanKind(SpanKind.INTERNAL)
                .startSpan();
        try (Scope ignored = parent.makeCurrent()) {
            parent.setAttribute("order.id.present", orderId != null);

            callInventory();
            callPayment();

            parent.setStatus(StatusCode.OK);
        } catch (RuntimeException ex) {
            parent.recordException(ex);
            parent.setStatus(StatusCode.ERROR, "Checkout failed");
            throw ex;
        } finally {
            parent.end();
        }
    }

    private void callInventory() {
        Span span = tracer.spanBuilder("inventory.reserve").setSpanKind(SpanKind.CLIENT).startSpan();
        try (Scope ignored = span.makeCurrent()) {
            // HTTP call / client SDK call
            span.setStatus(StatusCode.OK);
        } catch (RuntimeException ex) {
            span.recordException(ex);
            span.setStatus(StatusCode.ERROR);
            throw ex;
        } finally {
            span.end();
        }
    }

    private void callPayment() {
        Span span = tracer.spanBuilder("payment.charge").setSpanKind(SpanKind.CLIENT).startSpan();
        try (Scope ignored = span.makeCurrent()) {
            span.setStatus(StatusCode.OK);
        } catch (RuntimeException ex) {
            span.recordException(ex);
            span.setStatus(StatusCode.ERROR, "Payment charge failed");
            throw ex;
        } finally {
            span.end();
        }
    }
}
```

**Bad example:**

```java
public final class CheckoutTracingBad {
    public void checkout(String userEmail, String token) {
        // BAD: no spans/context, impossible to diagnose flow latency
        // BAD: sensitive values often leak when teams later add naive attributes
        System.out.println("processing " + userEmail + " with token " + token);
    }
}
```

### Example 2: Propagate Context and Keep Attributes Safe

Title: Ensure continuity and avoid cardinality/privacy problems
Description: 

**Good example:**

```java
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.context.Context;
import java.util.concurrent.Executor;

public final class AsyncFlow {
    private final Executor executor;

    public AsyncFlow(Executor executor) {
        this.executor = executor;
    }

    public void submitTask() {
        Context captured = Context.current();
        executor.execute(captured.wrap(() -> {
            Span.current().addEvent("async.task.started");
            // do work with the captured parent trace context
        }));
    }
}
```

**Bad example:**

```java
import io.opentelemetry.api.trace.Span;

public final class AsyncFlowBad {
    public void submitTask(String userId, String jwtToken) {
        // BAD: no context propagation, detached spans
        // BAD: high cardinality + sensitive attributes
        Span.current().setAttribute("user.id", userId);
        Span.current().setAttribute("auth.token", jwtToken);
    }
}
```

### Example 3: Apply OpenTelemetry Semantic Conventions

Title: Use Standard Attribute Names for HTTP, Database, and Messaging Spans
Description: 

**Good example:**

```java
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

public final class OrderRepository {

    private static final String DB_SYSTEM_NAME = "db.system.name";
    private static final String DB_NAMESPACE = "db.namespace";
    private static final String DB_OPERATION_NAME = "db.operation.name";
    private static final String DB_COLLECTION_NAME = "db.collection.name";

    private final Tracer tracer;

    public OrderRepository(OpenTelemetry openTelemetry) {
        this.tracer = openTelemetry.getTracer("order-service");
    }

    public void insertOrder(String orderId, int quantity) {
        Span span = tracer.spanBuilder("INSERT orders")
                .setSpanKind(SpanKind.CLIENT)
                .setAttribute(DB_SYSTEM_NAME, "postgresql")
                .setAttribute(DB_NAMESPACE, "shop")
                .setAttribute(DB_OPERATION_NAME, "INSERT")
                .setAttribute(DB_COLLECTION_NAME, "orders")
                .startSpan();
        try (Scope ignored = span.makeCurrent()) {
            // execute INSERT
            span.setStatus(StatusCode.OK);
        } catch (RuntimeException ex) {
            span.recordException(ex);
            span.setStatus(StatusCode.ERROR, "DB insert failed");
            throw ex;
        } finally {
            span.end();
        }
    }
}
```

**Bad example:**

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;

public final class OrderRepositoryBad {

    public void insertOrder(String orderId) {
        Span span = GlobalOpenTelemetry
                .getTracer("repo")
                .spanBuilder("insert")  // BAD: vague name, no kind
                .startSpan();
        try {
            // execute INSERT
            // BAD: custom attribute names instead of semantic conventions
            span.setAttribute("db", "postgres");
            span.setAttribute("query_type", "INSERT");
            // BAD: high-cardinality business identifiers do not belong in span attributes
            span.setAttribute("order.id", orderId);
        } finally {
            span.end(); // BAD: no status set, exceptions not recorded
        }
    }
}
```

### Example 4: Configure Sampling Strategy per Environment

Title: Balance Diagnostic Depth Against Cost and Overhead
Description: 

**Good example:**

```java
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.samplers.Sampler;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;

public final class TracingConfig {

    public static OpenTelemetry buildForEnvironment(String environment) {
        Sampler sampler = switch (environment) {
            case "production" -> Sampler.traceIdRatioBased(0.05);  // 5% in prod
            case "staging"    -> Sampler.traceIdRatioBased(0.50);  // 50% in staging
            default           -> Sampler.alwaysOn();               // 100% in dev/test
        };

        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setSampler(Sampler.parentBased(sampler))
                .addSpanProcessor(BatchSpanProcessor.builder(
                        OtlpGrpcSpanExporter.builder()
                                .setEndpoint("http://otel-collector:4317")
                                .build())
                        .build())
                .build();

        return OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .buildAndRegisterGlobal();
    }
}
```

**Bad example:**

```java
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.samplers.Sampler;

public final class TracingConfigBad {

    public static SdkTracerProvider build() {
        // BAD: always-on sampling in production causes cost explosion
        // BAD: no BatchSpanProcessor — synchronous export blocks request threads
        return SdkTracerProvider.builder()
                .setSampler(Sampler.alwaysOn())
                .build();
    }
}
```

### Example 5: Validate Span Correctness with Tests

Title: Assert Span Name, Kind, Status, and Attributes Using the In-Memory Exporter
Description: 

**Good example:**

```java
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.testing.exporter.InMemorySpanExporter;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.data.SpanData;
import io.opentelemetry.sdk.trace.export.SimpleSpanProcessor;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class CheckoutTracingTest {

    private InMemorySpanExporter exporter;
    private CheckoutTracing sut;

    @BeforeEach
    void setUp() {
        exporter = InMemorySpanExporter.create();
        SdkTracerProvider provider = SdkTracerProvider.builder()
                .addSpanProcessor(SimpleSpanProcessor.create(exporter))
                .build();
        OpenTelemetry otel = OpenTelemetrySdk.builder()
                .setTracerProvider(provider)
                .build();
        sut = new CheckoutTracing(otel);
    }

    @Test
    void shouldRecordCheckoutSpanOnSuccess() {
        sut.checkout("order-42");

        List<SpanData> spans = exporter.getFinishedSpanItems();
        assertThat(spans).hasSizeGreaterThanOrEqualTo(1);

        SpanData root = spans.stream()
                .filter(s -> s.getName().equals("checkout.process"))
                .findFirst()
                .orElseThrow();

        assertThat(root.getKind()).isEqualTo(SpanKind.INTERNAL);
        assertThat(root.getStatus().getStatusCode()).isEqualTo(StatusCode.OK);
        assertThat(root.getAttributes().get(AttributeKey.booleanKey("order.id.present"))).isTrue();
        assertThat(root.getAttributes().asMap()).doesNotContainKey(AttributeKey.stringKey("order.id"));
    }
}
```

**Bad example:**

```java
class CheckoutTracingTestBad {
    // BAD: no span assertions; tracing can silently break without test coverage.
    // BAD: using GlobalOpenTelemetry in tests leads to shared state and flaky results.
}
```


### Example 6: Use Annotation-Based Instrumentation for Service Methods

Title: Leverage @WithSpan and @SpanAttribute for concise, consistent tracing
Description: 

**Good example:**

```java
import io.opentelemetry.instrumentation.annotations.SpanAttribute;
import io.opentelemetry.instrumentation.annotations.WithSpan;

public final class ShippingService {

    @WithSpan("shipping.create.label")
    public String createLabel(
            @SpanAttribute("shipping.provider") String provider,
            @SpanAttribute("shipping.expedited") boolean expedited) {
        // business logic
        return "LBL-123";
    }
}
```

**Bad example:**

```java
import io.opentelemetry.api.trace.Span;

public final class ShippingServiceBad {

    public String createLabel(String provider, String customerEmail, String requestId) {
        // BAD: no explicit span boundary for this business operation
        // BAD: sensitive and high-cardinality attributes
        Span.current().setAttribute("customer.email", customerEmail);
        Span.current().setAttribute("request.id", requestId);
        Span.current().setAttribute("provider", provider);
        return "LBL-123";
    }
}
```

## Output Format

- **ANALYZE** tracing gaps across span modeling, propagation, and semantic consistency
- **APPLY** OpenTelemetry instrumentation with clear parent/child relationships and stable names
- **HARDEN** attributes/events/status and remove sensitive or high-cardinality data
- **VALIDATE** end-to-end trace continuity in tests and runtime backends

## Safeguards

- **PRIVACY FIRST**: Never place secrets or PII in trace payloads
- **PROPAGATION CHECK**: Verify traceId/spanId continuity across service boundaries
- **CARDINALITY CONTROL**: Keep attribute values bounded and query-friendly
- **PERF AWARENESS**: Avoid unnecessary spans in hot loops and configure sampling appropriately