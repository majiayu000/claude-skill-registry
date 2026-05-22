---
name: otlp-logging
description: >
  Guidance for OpenTelemetry Protocol (OTLP) logging and observability in .NET.
  USE FOR: OTLP log export, OpenTelemetry traces and metrics, distributed tracing with Activity API, configuring OTel collectors, correlating logs with traces, custom metrics and instruments.
  DO NOT USE FOR: Serilog-specific sinks and enrichers (use serilog), NLog-specific targets and routing (use nlog), Microsoft.Extensions.Logging abstractions (use extensions-logging).
license: MIT
metadata:
  displayName: "OTLP Logging and Observability"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "OpenTelemetry .NET Documentation"
    url: "https://opentelemetry.io/docs/languages/dotnet/"
  - title: "OpenTelemetry .NET GitHub Repository"
    url: "https://github.com/open-telemetry/opentelemetry-dotnet"
  - title: "OpenTelemetry NuGet Package"
    url: "https://www.nuget.org/packages/OpenTelemetry"
---

# OTLP Logging and Observability

## Overview

OpenTelemetry (OTel) is the vendor-neutral observability standard for collecting logs, traces, and metrics from distributed systems. In .NET, the `OpenTelemetry.Extensions.Hosting` and `OpenTelemetry.Exporter.OpenTelemetryProtocol` packages provide first-class integration with the generic host and ASP.NET Core. OTLP (OpenTelemetry Protocol) is the wire format used to export telemetry data to backends like Jaeger, Zipkin, Grafana Tempo, Azure Monitor, Datadog, and the OpenTelemetry Collector.

The three pillars of observability -- logs, traces, and metrics -- are configured independently but share a common `Resource` that identifies the service. By correlating log entries with trace and span IDs, developers can navigate from a log message to the exact distributed trace that produced it.

## Configuring All Three Pillars

Set up logging, tracing, and metrics in a single place using the OpenTelemetry builder.

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using OpenTelemetry;
using OpenTelemetry.Exporter;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

var serviceName = "OrderApi";
var serviceVersion = "1.0.0";

var resourceBuilder = ResourceBuilder.CreateDefault()
    .AddService(
        serviceName: serviceName,
        serviceVersion: serviceVersion)
    .AddAttributes(new Dictionary<string, object>
    {
        ["deployment.environment"] =
            builder.Environment.EnvironmentName
    });

// Tracing
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService(serviceName, serviceVersion))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddEntityFrameworkCoreInstrumentation()
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://collector:4317");
            options.Protocol = OtlpExportProtocol.Grpc;
        }))
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddMeter("MyApp.Orders")
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://collector:4317");
            options.Protocol = OtlpExportProtocol.Grpc;
        }));

// Logging
builder.Logging.AddOpenTelemetry(logging =>
{
    logging.SetResourceBuilder(resourceBuilder);
    logging.IncludeFormattedMessage = true;
    logging.IncludeScopes = true;
    logging.AddOtlpExporter(options =>
    {
        options.Endpoint = new Uri("http://collector:4317");
        options.Protocol = OtlpExportProtocol.Grpc;
    });
});

var app = builder.Build();
app.MapGet("/", () => "Hello");
app.Run();
```

## Distributed Tracing with Activity API

.NET uses `System.Diagnostics.Activity` as the tracing primitive. Create custom spans for business operations.

```csharp
using System.Diagnostics;
using Microsoft.Extensions.Logging;

namespace MyApp.Services;

public class OrderProcessor
{
    private static readonly ActivitySource ActivitySource =
        new("MyApp.Orders", "1.0.0");

    private readonly ILogger<OrderProcessor> _logger;

    public OrderProcessor(ILogger<OrderProcessor> logger)
    {
        _logger = logger;
    }

    public async Task<string> ProcessOrderAsync(
        string customerId, decimal total)
    {
        using var activity = ActivitySource.StartActivity(
            "ProcessOrder",
            ActivityKind.Internal);

        activity?.SetTag("order.customer_id", customerId);
        activity?.SetTag("order.total", total);

        _logger.LogInformation(
            "Processing order for customer {CustomerId} "
            + "with total {Total}",
            customerId, total);

        // Validate
        using (var validateSpan = ActivitySource.StartActivity(
            "ValidateOrder"))
        {
            await ValidateAsync(customerId, total);
            validateSpan?.SetTag("validation.result", "passed");
        }

        // Charge payment
        using (var paymentSpan = ActivitySource.StartActivity(
            "ChargePayment"))
        {
            await ChargePaymentAsync(total);
            paymentSpan?.SetTag("payment.amount", total);
        }

        var orderId = Guid.NewGuid().ToString();
        activity?.SetTag("order.id", orderId);

        activity?.SetStatus(ActivityStatusCode.Ok);
        return orderId;
    }

    private Task ValidateAsync(string customerId, decimal total)
        => Task.CompletedTask;
    private Task ChargePaymentAsync(decimal total)
        => Task.CompletedTask;
}
```

## Custom Metrics

Define and record custom metrics using `System.Diagnostics.Metrics`.

```csharp
using System.Diagnostics.Metrics;

namespace MyApp.Telemetry;

public static class OrderMetrics
{
    private static readonly Meter Meter =
        new("MyApp.Orders", "1.0.0");

    public static readonly Counter<long> OrdersCreated =
        Meter.CreateCounter<long>(
            "orders.created",
            unit: "{order}",
            description: "Number of orders created");

    public static readonly Histogram<double> OrderProcessingDuration =
        Meter.CreateHistogram<double>(
            "orders.processing.duration",
            unit: "ms",
            description: "Order processing duration in milliseconds");

    public static readonly UpDownCounter<int> ActiveOrders =
        Meter.CreateUpDownCounter<int>(
            "orders.active",
            unit: "{order}",
            description: "Number of orders currently being processed");

    public static readonly ObservableGauge<int> QueueDepth =
        Meter.CreateObservableGauge(
            "orders.queue.depth",
            observeValue: () => GetCurrentQueueDepth(),
            unit: "{order}",
            description: "Current order queue depth");

    private static int GetCurrentQueueDepth() => 0;
}
```

Use the metrics in service code:

```csharp
using System.Diagnostics;
using MyApp.Telemetry;

namespace MyApp.Services;

public class OrderService
{
    public async Task<string> CreateOrderAsync(
        string customerId, decimal total)
    {
        OrderMetrics.ActiveOrders.Add(1);
        var sw = Stopwatch.StartNew();

        try
        {
            var orderId = await ProcessAsync(customerId, total);

            OrderMetrics.OrdersCreated.Add(1,
                new KeyValuePair<string, object?>(
                    "customer.tier", "premium"));

            return orderId;
        }
        finally
        {
            sw.Stop();
            OrderMetrics.OrderProcessingDuration.Record(
                sw.Elapsed.TotalMilliseconds);
            OrderMetrics.ActiveOrders.Add(-1);
        }
    }

    private Task<string> ProcessAsync(
        string customerId, decimal total)
        => Task.FromResult(Guid.NewGuid().ToString());
}
```

## Log-Trace Correlation

When OpenTelemetry logging is configured with tracing, log entries automatically include `TraceId` and `SpanId`, enabling navigation from a log entry to its distributed trace.

```csharp
using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace MyApp.Services;

public class PaymentService
{
    private static readonly ActivitySource ActivitySource =
        new("MyApp.Payments");

    private readonly ILogger<PaymentService> _logger;

    public PaymentService(ILogger<PaymentService> logger)
    {
        _logger = logger;
    }

    public async Task ChargeAsync(string orderId, decimal amount)
    {
        using var activity = ActivitySource.StartActivity(
            "ChargePayment");

        // This log entry automatically includes:
        //   TraceId: from Activity.Current.TraceId
        //   SpanId:  from Activity.Current.SpanId
        _logger.LogInformation(
            "Charging {Amount:C} for order {OrderId}",
            amount, orderId);

        // Add structured event to the span
        activity?.AddEvent(new ActivityEvent(
            "PaymentCharged",
            tags: new ActivityTagsCollection
            {
                { "payment.amount", amount },
                { "payment.currency", "USD" }
            }));

        await Task.CompletedTask;
    }
}
```

## Environment-Based Configuration

Configure OTLP export via environment variables for container deployments.

```bash
# Standard OTel environment variables
OTEL_SERVICE_NAME=OrderApi
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production,service.version=1.0.0
```

```csharp
using Microsoft.AspNetCore.Builder;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

// Reads OTEL_* environment variables automatically
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r
        .AddService(builder.Environment.ApplicationName)
        .AddEnvironmentVariableDetector())
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddOtlpExporter()); // Uses OTEL_EXPORTER_OTLP_ENDPOINT

var app = builder.Build();
app.Run();
```

## OpenTelemetry Signal Types

| Signal | .NET API | OTel Package | Use Case |
|---|---|---|---|
| Traces | `System.Diagnostics.Activity` | `OpenTelemetry.Exporter.OpenTelemetryProtocol` | Request flow across services |
| Metrics | `System.Diagnostics.Metrics` | `OpenTelemetry.Exporter.OpenTelemetryProtocol` | Counters, histograms, gauges |
| Logs | `Microsoft.Extensions.Logging` | `OpenTelemetry.Exporter.OpenTelemetryProtocol` | Structured log events |

## Instrumentation Libraries

| Library | Package | What It Captures |
|---|---|---|
| ASP.NET Core | `OpenTelemetry.Instrumentation.AspNetCore` | HTTP server spans, request metrics |
| HttpClient | `OpenTelemetry.Instrumentation.Http` | Outbound HTTP client spans |
| EF Core | `OpenTelemetry.Instrumentation.EntityFrameworkCore` | Database query spans |
| SQL Client | `OpenTelemetry.Instrumentation.SqlClient` | SQL Server query spans |
| Runtime | `OpenTelemetry.Instrumentation.Runtime` | GC, threadpool, assembly metrics |
| gRPC | `OpenTelemetry.Instrumentation.GrpcNetClient` | gRPC client call spans |

## Best Practices

1. **Configure all three signals (traces, metrics, logs) together** with a shared `Resource` so the observability backend can correlate data from the same service instance.
2. **Use semantic conventions** for span names and attributes (e.g., `http.request.method`, `db.system`, `order.id`) so observability tools can provide automatic dashboards and alerts.
3. **Set an appropriate sampling rate** in production using `parentbased_traceidratio` (e.g., 10% via `OTEL_TRACES_SAMPLER_ARG=0.1`) to reduce storage costs while maintaining statistical significance.
4. **Add `ActivitySource.StartActivity` for business-critical operations** (order processing, payment charging, inventory updates) to create custom spans that appear in the trace timeline alongside framework spans.
5. **Use the `OTEL_*` environment variables** for configuration in containerized deployments, as the OpenTelemetry SDK reads them automatically without code changes.
6. **Include `IncludeFormattedMessage = true`** and `IncludeScopes = true` in the logging exporter configuration so log messages in the backend are human-readable and include scope properties.
7. **Register custom `Meter` names** in `AddMeter("MyApp.Orders")` on the metrics builder; meters not registered are silently ignored, which is a common configuration mistake.
8. **Export to an OpenTelemetry Collector** rather than directly to backends, so you can fan out to multiple destinations, apply transformations, and change backends without redeploying the application.
9. **Check `activity is not null`** before calling `SetTag` or `AddEvent` because `StartActivity` returns null when no listener (sampler) is active for the source, which is expected behavior.
10. **Record error details on spans** using `activity?.SetStatus(ActivityStatusCode.Error, exception.Message)` and `activity?.RecordException(exception)` so error rates and stack traces are visible in the tracing backend.
