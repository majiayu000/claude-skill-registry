---
name: dotnet-api
description: Patterns and best practices for building .NET Web APIs with ASP.NET Core
---

# .NET API Development Skill

This skill provides patterns and best practices for building production-ready .NET Web APIs with ASP.NET Core 8+. It covers architecture decisions, validation, error handling, and testing strategies.

## Controllers vs Minimal APIs

Choose the right approach based on your project needs:

| Aspect | Minimal APIs | Controllers |
|--------|--------------|-------------|
| Best for | Microservices, small APIs | Large APIs, complex routing |
| Ceremony | Low (less boilerplate) | Higher (class-based) |
| Filters | Endpoint filters | Action filters, extensive |
| Model binding | Manual or auto | Automatic, comprehensive |
| OpenAPI | Built-in support | Swashbuckle integration |
| Testing | Direct endpoint testing | Controller unit testing |
| Performance | Slightly faster startup | Negligible difference |

**When to use Minimal APIs:**
- Microservices with few endpoints
- Rapid prototyping
- Simple CRUD operations
- Lambda/serverless deployments

**When to use Controllers:**
- Large enterprise applications
- Complex authorization scenarios
- Need extensive filter pipelines
- Team familiar with MVC patterns

## Routing and Model Binding

### Minimal API Routing

```csharp
var app = builder.Build();

// Route groups for organization
var api = app.MapGroup("/api");
var v1 = api.MapGroup("/v1");

// Basic CRUD routes
v1.MapGet("/products", GetAllProducts);
v1.MapGet("/products/{id:int}", GetProductById);
v1.MapPost("/products", CreateProduct);
v1.MapPut("/products/{id:int}", UpdateProduct);
v1.MapDelete("/products/{id:int}", DeleteProduct);

// Route constraints
v1.MapGet("/orders/{id:guid}", GetOrderById);
v1.MapGet("/users/{username:alpha:minlength(3)}", GetUserByUsername);
```

### Controller Routing

```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetAll() { }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<Product>> GetById(int id) { }

    [HttpPost]
    public async Task<ActionResult<Product>> Create(CreateProductRequest request) { }
}
```

### Model Binding Sources

```csharp
// Minimal API - explicit binding
app.MapPost("/products", async (
    [FromBody] CreateProductRequest body,
    [FromQuery] bool? notify,
    [FromHeader(Name = "X-Correlation-Id")] string? correlationId,
    [FromServices] IProductRepository repository) => { });

// Controller - automatic binding
[HttpPost]
public async Task<ActionResult> Create(
    [FromBody] CreateProductRequest body,
    [FromQuery] bool? notify = false) { }
```

## Validation

### FluentValidation (Recommended)

Note: `FluentValidation.AspNetCore` is deprecated. Use manual validation:

```csharp
// Validator definition
public class CreateProductValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Price)
            .GreaterThan(0)
            .PrecisionScale(10, 2, false);

        RuleFor(x => x.Sku)
            .NotEmpty()
            .Matches(@"^[A-Z]{3}-\d{4}$")
            .WithMessage("SKU must be in format XXX-0000");
    }
}

// Register validators
builder.Services.AddValidatorsFromAssemblyContaining<CreateProductValidator>();

// Manual validation in endpoint
app.MapPost("/api/products", async (
    CreateProductRequest request,
    IValidator<CreateProductRequest> validator,
    IProductRepository repository) =>
{
    var result = await validator.ValidateAsync(request);
    if (!result.IsValid)
        return Results.ValidationProblem(result.ToDictionary());

    var product = await repository.CreateAsync(request);
    return Results.Created($"/api/products/{product.Id}", product);
});
```

### Data Annotations (Simple Cases)

```csharp
public record CreateProductRequest
{
    [Required]
    [StringLength(100, MinimumLength = 1)]
    public string Name { get; init; } = string.Empty;

    [Range(0.01, 999999.99)]
    public decimal Price { get; init; }

    [RegularExpression(@"^[A-Z]{3}-\d{4}$")]
    public string Sku { get; init; } = string.Empty;
}
```

## Error Handling

### Problem Details (RFC 7807)

```csharp
// Configure Problem Details
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] =
            context.HttpContext.TraceIdentifier;
        context.ProblemDetails.Extensions["instance"] =
            context.HttpContext.Request.Path;
    };
});

// Use with controllers
builder.Services.AddControllers()
    .ConfigureApiBehaviorOptions(options =>
    {
        options.InvalidModelStateResponseFactory = context =>
        {
            var problemDetails = new ValidationProblemDetails(context.ModelState)
            {
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                Title = "Validation failed",
                Status = StatusCodes.Status400BadRequest,
                Instance = context.HttpContext.Request.Path
            };
            return new BadRequestObjectResult(problemDetails);
        };
    });
```

### Global Exception Handler (.NET 8+)

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext, Exception exception, CancellationToken ct)
    {
        var problemDetails = exception switch
        {
            NotFoundException => new ProblemDetails
                { Status = 404, Title = "Resource not found" },
            _ => new ProblemDetails
                { Status = 500, Title = "An error occurred" }
        };
        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, ct);
        return true;
    }
}

// Registration
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

## Dependency Injection

### Service Lifetimes

| Lifetime | Description | Use Case |
|----------|-------------|----------|
| Singleton | One instance for app lifetime | Configuration, caching |
| Scoped | One instance per request | DbContext, repositories |
| Transient | New instance every time | Lightweight, stateless |

```csharp
// Registration patterns
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddTransient<IEmailService, EmailService>();

// Keyed services (.NET 8+)
builder.Services.AddKeyedSingleton<INotifier, EmailNotifier>("email");
builder.Services.AddKeyedSingleton<INotifier, SmsNotifier>("sms");

// Usage with keyed services
app.MapPost("/notify", ([FromKeyedServices("email")] INotifier notifier) =>
{
    notifier.Send("Hello");
});
```

Use extension methods to organize registrations: `builder.Services.AddApplicationServices();`

## OpenAPI/Swagger

### Swashbuckle Configuration

```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Products API",
        Version = "v1",
        Description = "API for managing products",
        Contact = new OpenApiContact
        {
            Name = "API Support",
            Email = "support@example.com"
        }
    });

    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);

    // Add security definition
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        Description = "Enter JWT token"
    });
});

// Middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "v1");
        options.RoutePrefix = string.Empty;
    });
}
```

### Endpoint Documentation

```csharp
app.MapGet("/api/products/{id}", async (int id, IProductRepository repo) =>
{
    var product = await repo.GetByIdAsync(id);
    return product is null ? Results.NotFound() : Results.Ok(product);
})
.WithName("GetProductById")
.WithTags("Products")
.Produces<Product>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status404NotFound)
.WithOpenApi(operation =>
{
    operation.Summary = "Get a product by ID";
    operation.Description = "Returns a single product";
    return operation;
});
```

## API Versioning

### Using Asp.Versioning

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("X-Api-Version"),
        new QueryStringApiVersionReader("api-version"));
})
.AddApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});

// Minimal API versioning
var versionSet = app.NewApiVersionSet()
    .HasApiVersion(new ApiVersion(1, 0))
    .HasApiVersion(new ApiVersion(2, 0))
    .ReportApiVersions()
    .Build();

app.MapGet("/api/v{version:apiVersion}/products", GetProducts)
    .WithApiVersionSet(versionSet)
    .MapToApiVersion(1, 0);

// Controller versioning
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
[ApiVersion("1.0")]
[ApiVersion("2.0")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    [MapToApiVersion("1.0")]
    public IActionResult GetV1() => Ok("v1");

    [HttpGet]
    [MapToApiVersion("2.0")]
    public IActionResult GetV2() => Ok("v2");
}
```

## Performance

### Response Caching

```csharp
builder.Services.AddResponseCaching();
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromMinutes(5)));
    options.AddPolicy("Products", builder =>
        builder.Expire(TimeSpan.FromMinutes(10)).Tag("products"));
});

app.UseOutputCache();

// Apply to endpoint
app.MapGet("/api/products", GetProducts)
    .CacheOutput("Products");

// Cache invalidation
app.MapPost("/api/products", async (
    CreateProductRequest request,
    IOutputCacheStore cache,
    IProductRepository repo) =>
{
    var product = await repo.CreateAsync(request);
    await cache.EvictByTagAsync("products", default);
    return Results.Created($"/api/products/{product.Id}", product);
});
```

### Response Compression

```csharp
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});

builder.Services.Configure<BrotliCompressionProviderOptions>(options =>
{
    options.Level = CompressionLevel.Fastest;
});

app.UseResponseCompression();
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy(), tags: ["live"])
    .AddSqlServer(connectionString, name: "database", tags: ["ready"]);

// Liveness probe (is app running?)
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live")
});

// Readiness probe (can app serve traffic?)
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

## Integration Testing

Use `WebApplicationFactory<Program>` for integration tests:

```csharp
public class ApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
            builder.ConfigureServices(services =>
            {
                services.RemoveAll<IProductRepository>();
                services.AddScoped<IProductRepository, InMemoryProductRepository>();
            }));
        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task GetProducts_ReturnsSuccess()
    {
        var response = await _client.GetAsync("/api/products");
        response.EnsureSuccessStatusCode();
    }

    [Fact]
    public async Task CreateProduct_WithInvalidData_ReturnsBadRequest()
    {
        var response = await _client.PostAsJsonAsync("/api/products",
            new { Name = "", Price = -1 });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
```

## Quick Reference

| Task | Code |
|------|------|
| Create endpoint | `app.MapGet("/path", Handler)` |
| Return 201 | `Results.Created(uri, object)` |
| Return 404 | `Results.NotFound()` |
| Return Problem | `Results.Problem(detail, statusCode)` |
| Validation Problem | `Results.ValidationProblem(errors)` |
| Inject service | `([FromServices] IService svc)` |
| Route param | `"/items/{id:int}"` |
| Query param | `([FromQuery] int? page)` |
| Require auth | `.RequireAuthorization()` |
| Add tag | `.WithTags("TagName")` |
| Cache output | `.CacheOutput("PolicyName")` |

## Additional Resources

- **templates/minimal-api-template.cs** - Starter for Minimal API projects
- **templates/controller-template.cs** - Starter for controller-based APIs
- **examples/task-api-dotnet.cs** - Task API (Minimal API approach)
- **examples/task-api-controller-dotnet.cs** - Task API (Controller approach)
