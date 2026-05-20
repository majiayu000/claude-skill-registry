---
name: webapicontrib
description: |
  USE FOR: Extending ASP.NET Core Web API with custom formatters, content negotiation, and media type handling using WebApiContrib.Core. Use when you need to serve or consume CSV, BSON, MessagePack, Protocol Buffers, or other non-JSON formats alongside JSON in the same API.
  DO NOT USE FOR: Building entire APIs from scratch (use ASP.NET Core minimal APIs or controllers), GraphQL endpoints (use Hot Chocolate), or gRPC services (use ASP.NET Core gRPC).
license: MIT
metadata:
  displayName: WebApiContrib
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "WebAPIContrib.Core GitHub Repository"
    url: "https://github.com/WebApiContrib/WebAPIContrib.Core"
  - title: "WebApiContrib.Core NuGet Package"
    url: "https://www.nuget.org/packages/WebApiContrib.Core"
---

# WebApiContrib

## Overview

WebApiContrib.Core is a community-driven collection of extensions for ASP.NET Core Web API that adds custom input/output formatters, content negotiation strategies, and utility middleware. The library provides formatters for CSV, BSON, MessagePack, Protocol Buffers, and plain text, enabling APIs to serve multiple content types through standard HTTP content negotiation (the `Accept` header). WebApiContrib.Core integrates with the ASP.NET Core MVC formatter pipeline, allowing controllers and minimal APIs to return data in the format requested by the client without changing action method signatures. It also includes additional filters, model binders, and helper utilities.

## CSV Formatter Setup

Add CSV input/output formatting to an ASP.NET Core API.

```csharp
using WebApiContrib.Core.Formatter.Csv;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers(options =>
{
    options.RespectBrowserAcceptHeader = true;
    options.ReturnHttpNotAcceptable = true;
})
.AddCsvSerializerFormatters(new CsvFormatterOptions
{
    UseSingleLineHeaderInCsv = true,
    CsvDelimiter = ",",
    IncludeExcelDelimiterHeader = false,
    Encoding = System.Text.Encoding.UTF8
});

var app = builder.Build();

app.MapControllers();
app.Run();
```

```csharp
using Microsoft.AspNetCore.Mvc;

namespace MyApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ReportsController : ControllerBase
{
    private readonly IReportService _reportService;

    public ReportsController(IReportService reportService)
    {
        _reportService = reportService;
    }

    // Returns JSON by default; returns CSV when Accept: text/csv
    [HttpGet("sales")]
    [Produces("application/json", "text/csv")]
    public async Task<IActionResult> GetSalesReport(
        [FromQuery] DateTime startDate,
        [FromQuery] DateTime endDate)
    {
        var data = await _reportService.GetSalesDataAsync(startDate, endDate);
        return Ok(data);
    }

    // Force CSV download with content disposition
    [HttpGet("sales/download")]
    [Produces("text/csv")]
    public async Task<IActionResult> DownloadSalesReport(
        [FromQuery] DateTime startDate,
        [FromQuery] DateTime endDate)
    {
        var data = await _reportService.GetSalesDataAsync(startDate, endDate);

        Response.Headers.Append(
            "Content-Disposition",
            $"attachment; filename=sales_{startDate:yyyyMMdd}_{endDate:yyyyMMdd}.csv");

        return Ok(data);
    }
}

public record SalesRecord(
    string ProductName,
    int Quantity,
    decimal Revenue,
    DateTime Date);
```

## MessagePack Formatter

Add high-performance binary serialization with MessagePack.

```csharp
using MessagePack;
using Microsoft.AspNetCore.Mvc.Formatters;
using Microsoft.Net.Http.Headers;

namespace MyApp.Formatters;

public class MessagePackOutputFormatter : OutputFormatter
{
    private readonly MessagePackSerializerOptions _options;

    public MessagePackOutputFormatter()
    {
        _options = MessagePackSerializerOptions.Standard
            .WithCompression(MessagePackCompression.Lz4BlockArray);

        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/x-msgpack"));
        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/msgpack"));
    }

    protected override bool CanWriteType(Type? type) => type != null;

    public override async Task WriteResponseBodyAsync(OutputFormatterWriteContext context)
    {
        var response = context.HttpContext.Response;
        var bytes = MessagePackSerializer.Serialize(
            context.ObjectType!,
            context.Object,
            _options);

        response.ContentType = "application/x-msgpack";
        response.ContentLength = bytes.Length;
        await response.Body.WriteAsync(bytes);
    }
}

public class MessagePackInputFormatter : InputFormatter
{
    private readonly MessagePackSerializerOptions _options;

    public MessagePackInputFormatter()
    {
        _options = MessagePackSerializerOptions.Standard
            .WithCompression(MessagePackCompression.Lz4BlockArray);

        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/x-msgpack"));
        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/msgpack"));
    }

    public override async Task<InputFormatterResult> ReadRequestBodyAsync(
        InputFormatterContext context)
    {
        var request = context.HttpContext.Request;

        using var memoryStream = new MemoryStream();
        await request.Body.CopyToAsync(memoryStream);
        memoryStream.Position = 0;

        var result = await MessagePackSerializer.DeserializeAsync(
            context.ModelType,
            memoryStream,
            _options);

        return await InputFormatterResult.SuccessAsync(result);
    }
}

// Registration
builder.Services.AddControllers(options =>
{
    options.OutputFormatters.Add(new MessagePackOutputFormatter());
    options.InputFormatters.Add(new MessagePackInputFormatter());
    options.RespectBrowserAcceptHeader = true;
    options.ReturnHttpNotAcceptable = true;
});
```

## Custom Content Negotiation

Configure content negotiation to support multiple formats per endpoint.

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Formatters;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers(options =>
{
    // Return 406 Not Acceptable instead of defaulting to JSON
    options.ReturnHttpNotAcceptable = true;

    // Respect the Accept header from browsers
    options.RespectBrowserAcceptHeader = true;

    // Add custom formatters
    options.OutputFormatters.Add(new MessagePackOutputFormatter());
    options.OutputFormatters.Add(new XmlSerializerOutputFormatter());

    // Remove text/plain formatter if not needed
    options.OutputFormatters.RemoveType<StringOutputFormatter>();

    // Configure format mapping for URL-based negotiation
    options.FormatterMappings.SetMediaTypeMappingForFormat(
        "csv", "text/csv");
    options.FormatterMappings.SetMediaTypeMappingForFormat(
        "xml", "application/xml");
    options.FormatterMappings.SetMediaTypeMappingForFormat(
        "msgpack", "application/x-msgpack");
})
.AddCsvSerializerFormatters()
.AddXmlSerializerFormatters();

var app = builder.Build();

app.MapControllers();
app.Run();
```

```csharp
using Microsoft.AspNetCore.Mvc;

namespace MyApp.Controllers;

[ApiController]
[Route("api/[controller]")]
[FormatFilter] // Enables /api/products.csv, /api/products.xml
public class ProductsController : ControllerBase
{
    private readonly IProductRepository _repo;

    public ProductsController(IProductRepository repo) => _repo = repo;

    // GET /api/products       -> JSON (Accept: application/json)
    // GET /api/products.csv   -> CSV (format mapping)
    // GET /api/products.xml   -> XML (format mapping)
    [HttpGet]
    [HttpGet("{format?}")]
    [Produces("application/json", "text/csv", "application/xml", "application/x-msgpack")]
    public async Task<IActionResult> GetAll()
    {
        var products = await _repo.GetAllAsync();
        return Ok(products);
    }

    [HttpPost]
    [Consumes("application/json", "application/xml", "application/x-msgpack")]
    public async Task<IActionResult> Create([FromBody] Product product)
    {
        await _repo.AddAsync(product);
        return CreatedAtAction(nameof(GetAll), new { id = product.Id }, product);
    }
}
```

## Protobuf Formatter

Add Protocol Buffers support for high-efficiency binary serialization.

```csharp
using Google.Protobuf;
using Microsoft.AspNetCore.Mvc.Formatters;
using Microsoft.Net.Http.Headers;

namespace MyApp.Formatters;

public class ProtobufOutputFormatter : OutputFormatter
{
    public ProtobufOutputFormatter()
    {
        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/x-protobuf"));
    }

    protected override bool CanWriteType(Type? type)
    {
        return type != null && typeof(IMessage).IsAssignableFrom(type);
    }

    public override async Task WriteResponseBodyAsync(OutputFormatterWriteContext context)
    {
        if (context.Object is IMessage message)
        {
            var bytes = message.ToByteArray();
            context.HttpContext.Response.ContentType = "application/x-protobuf";
            context.HttpContext.Response.ContentLength = bytes.Length;
            await context.HttpContext.Response.Body.WriteAsync(bytes);
        }
    }
}

public class ProtobufInputFormatter : InputFormatter
{
    public ProtobufInputFormatter()
    {
        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("application/x-protobuf"));
    }

    protected override bool CanReadType(Type type)
    {
        return typeof(IMessage).IsAssignableFrom(type);
    }

    public override async Task<InputFormatterResult> ReadRequestBodyAsync(
        InputFormatterContext context)
    {
        using var memoryStream = new MemoryStream();
        await context.HttpContext.Request.Body.CopyToAsync(memoryStream);

        var messageDescriptor = (MessageDescriptor)context.ModelType
            .GetProperty("Descriptor", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static)!
            .GetValue(null)!;

        var message = messageDescriptor.Parser.ParseFrom(memoryStream.ToArray());
        return await InputFormatterResult.SuccessAsync(message);
    }
}
```

## WebApiContrib.Core vs Other Formatting Approaches

| Feature | WebApiContrib.Core | Custom Formatters | Content-Type Middleware | Separate Endpoints |
|---|---|---|---|---|
| CSV | Built-in formatter | Manual implementation | Not applicable | Manual serialization |
| BSON | Built-in formatter | Manual implementation | Not applicable | Manual serialization |
| Content negotiation | Standard Accept header | Standard Accept header | Custom header parsing | URL-based (/csv, /json) |
| Integration | MVC formatter pipeline | MVC formatter pipeline | Middleware pipeline | Per-endpoint |
| Configuration | One-liner `.Add*()` | Register in options | Custom middleware | Per-endpoint code |
| Format mapping | `[FormatFilter]` + URL | `[FormatFilter]` + URL | Not built-in | URL path |
| Complexity | Minimal | Moderate | High | High (duplication) |

## Best Practices

1. **Set `options.ReturnHttpNotAcceptable = true`** in `AddControllers()` so that clients requesting unsupported formats (e.g., `Accept: application/yaml` when only JSON and CSV are configured) receive a `406 Not Acceptable` response instead of silently falling back to JSON, making content negotiation failures explicit.

2. **Set `options.RespectBrowserAcceptHeader = true`** when you want browsers to receive non-JSON responses based on their `Accept` header, because ASP.NET Core ignores the browser's `Accept: text/html` by default and always returns JSON, which is correct for API clients but confusing for browser-based testing.

3. **Use `[Produces("application/json", "text/csv")]` on controller actions** to document which content types each endpoint supports, so that OpenAPI/Swagger generation includes the correct response content types and clients know which `Accept` values are valid.

4. **Use `[FormatFilter]` with `FormatterMappings.SetMediaTypeMappingForFormat()`** to enable URL-based format selection (e.g., `/api/products.csv`, `/api/products.xml`) as an alternative to the `Accept` header, because some clients (browsers, curl without headers) cannot easily set request headers.

5. **Register formatters in the correct order** in `options.OutputFormatters` (JSON first, then specialized formats) because the first formatter that can handle the request's `Accept` header wins, and placing a binary formatter first would cause it to be selected when the client sends `Accept: */*`.

6. **Use `[Consumes("application/json", "application/xml")]`** on POST/PUT actions to restrict which input formats are accepted, returning `415 Unsupported Media Type` for unrecognized content types rather than attempting to deserialize arbitrary payloads.

7. **Set `CsvFormatterOptions.CsvDelimiter`** explicitly (comma or semicolon) and `IncludeExcelDelimiterHeader` based on the target audience, because European locales use semicolons as CSV delimiters and Excel requires a `sep=` header to parse the file correctly.

8. **Implement both `InputFormatter` and `OutputFormatter` for binary formats** (MessagePack, Protobuf, BSON) to support both reading request bodies and writing response bodies, rather than only implementing output formatting which leaves POST/PUT endpoints unable to accept the same format.

9. **Add `Content-Disposition: attachment; filename=report.csv`** headers on endpoints intended for file download rather than inline display, so that browsers prompt the user to save the file instead of rendering the CSV text in the browser window.

10. **Write integration tests that send requests with different `Accept` headers** and assert on both the response `Content-Type` and the deserialized body shape, ensuring that content negotiation produces correct output for each format and that CSV column headers match the DTO property names.
