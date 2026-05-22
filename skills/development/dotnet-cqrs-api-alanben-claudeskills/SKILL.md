---
name: dotnet-cqrs-api
description: Guide for building .NET APIs using CQRS pattern with MediatR, FluentValidation, and Carter modules
---

# .NET CQRS API Development Skill

## Purpose
This skill guides the specification and creation of .NET APIs using the CQRS pattern with MediatR, FluentValidation, and Carter modules. It provides a structured approach to building feature-based, vertically-sliced APIs with robust validation and clear separation of concerns.

## Core Principles

### Architectural Philosophy
- **Vertical Slice Architecture**: Features are self-contained units organized by business capability
- **CQRS Separation**: Commands (write operations) and Queries (read operations) are explicitly separated
- **Result Pattern**: All operations return `Result<T>` for explicit success/failure handling
- **Functional Composition**: Prefer declarative, immutable approaches over imperative mutations

### Technology Stack
- **MediatR**: Implements mediator pattern for decoupling endpoint handlers from business logic
- **FluentValidation**: Provides declarative, strongly-typed validation rules
- **Carter**: Enables minimal API-style endpoint definition with module organization
- **Mapster** (inferred): Used for object mapping (`.Adapt<T>()` pattern)

## Project Structure

```
/Features
  /{FeatureName}
    - Add{Feature}.cs          # Command endpoint + handler
    - Update{Feature}.cs       # Command endpoint + handler
    - Get{Feature}.cs          # Single item query endpoint + handler
    - Get{Feature}s.cs         # Collection query endpoint + handler
    - {Feature}AddRequest.cs   # Command DTO
    - {Feature}UpdateRequest.cs # Command DTO
    - {Feature}Response.cs     # Query response DTO
```

## Feature Specification Process

### Step 1: Define the Feature Domain
Before writing code, establish:
1. **Feature Name**: Clear, business-focused identifier (e.g., "Order", "Customer", "Invoice")
2. **Business Context**: What problem does this feature solve?
3. **Operations Needed**: Which CQRS operations are required?
   - Create (Add)
   - Read Single (Get)
   - Read Collection (GetAll/List)
   - Update
   - Delete (not in templates, but may be needed)
4. **Domain Model**: What properties define this entity?
5. **Validation Rules**: What business rules must be enforced?
6. **Authorization Requirements**: Who can access these endpoints?

### Step 2: Design the Data Contract
Define three types of DTOs:

**Request DTOs** (for commands):
- Contain only the data needed to perform the operation
- Exclude computed or system-managed fields (IDs, timestamps)
- Should be immutable or follow init-only patterns

**Response DTOs** (for queries):
- May inherit from domain models
- Include data needed by consumers
- Can include computed/derived properties

**Domain Models** (internal):
- Represent the entity in the data layer
- Should not be directly exposed via API

### Step 3: Specify Validation Rules
For each operation, define:
- Required fields and null checks
- Range validations (GreaterThan, LessThan)
- Format validations (Regex patterns, date formats)
- Business rule validations (cross-field rules)
- Custom validation logic requirements

### Step 4: Define Routing Strategy
Establish URL patterns following RESTful conventions:
- Collection routes: `/{feature-plural}` or `/Features/{FeatureName}`
- Item routes: `/{feature-plural}/{id}` or `/Features/{FeatureName}/{id}`
- Consider route parameters vs query strings
- Maintain consistency across features

## Implementation Templates

### Command Pattern (Add/Create)

**Use when**: Creating new entities

**Structure**:
```csharp
namespace {ProjectName}.Features.{FeatureName};

// 1. Carter Endpoint Module
public class Add{Feature}Endpoint : ICarterModule {
    public void AddRoutes(IEndpointRouteBuilder app) {
        app.MapPost("{route}", async ({Feature}AddRequest request, ISender sender) => {
            var command = new Add{Feature}.Command { {Feature} = request };
            var result = await sender.Send(command);
            
            if (result.IsFailure) {
                return Results.BadRequest(result.Error);
            }
            
            return Results.Ok(result.Value);
        })
        .Produces<int>() // Or appropriate return type
        .RequireAuthorization("{PolicyName}")
        .WithMetadata(new RouteMetadata { Tags = new[] { "{TagName}" } });
    }
}

// 2. Command Definition
public static partial class Add{Feature} {
    public class Command : IRequest<Result<int>> { // Or TResult
        public {Feature}AddRequest? {Feature} { get; set; }
    }
    
    // 3. Validation Rules
    public class Validator : AbstractValidator<Command> {
        public Validator() {
            RuleFor(x => x.{Feature})
                .NotNull()
                .WithMessage("No {feature} data provided.");
            
            // Add specific field validations
            RuleFor(x => x.{Feature}!.PropertyName)
                .GreaterThan(0)
                .WithMessage("PropertyName cannot be zero.");
        }
    }
    
    // 4. Command Handler
    internal sealed partial class {Feature}Handler : IRequestHandler<Command, Result<int>> {
        private readonly ILogger<{Feature}Handler> _logger;
        private readonly IValidator<Command> _validator;
        private readonly I{Feature}Data _data;
        
        public {Feature}Handler(
            IValidator<Command> validator,
            ILogger<{Feature}Handler> logger,
            I{Feature}Data data
        ) {
            _validator = validator;
            _logger = logger;
            _data = data;
        }
        
        public async Task<Result<int>> Handle(Command request, CancellationToken cancellationToken) {
            // Validate
            var validationResult = _validator.Validate(request);
            if (!validationResult.IsValid) {
                return Result.Failure<int>(new Error("Add{Feature}.Validation", validationResult.ToString()));
            }
            
            try {
                // Map and execute
                {Feature}Model new{Feature} = request.{Feature}!.Adapt<{Feature}Model>();
                var {feature} = await _data.Add{Feature}(new{Feature});
                
                if ({feature} is null) {
                    return Result.Failure<int>(new Error("Add{Feature}", "Failed to add {feature}"));
                }
                
                return {feature}.ID;
            } catch (Exception ex) {
                return Result.Failure<int>(new Error("Add{Feature}.Exception", ex.Message));
            }
        }
    }
}
```

**Key Patterns**:
- Endpoint delegates to MediatR command via `ISender`
- Validation happens in handler, not endpoint
- Result pattern for explicit error handling
- Exception handling wraps unexpected failures
- Returns entity ID on success

### Query Pattern (Get Single)

**Use when**: Retrieving a specific entity by identifier

**Structure**:
```csharp
namespace {ProjectName}.Features.{FeatureName};

// 1. Carter Endpoint Module
public class Get{Feature}Endpoint : ICarterModule {
    public void AddRoutes(IEndpointRouteBuilder app) {
        app.MapGet("{route}/{id:int}", async (int id, ISender sender) => {
            var query = new Get{Feature}.{Feature}Query { ID = id };
            var result = await sender.Send(query);
            
            if (result.IsFailure) {
                return Results.NotFound(result.Error);
            }
            
            return Results.Ok(result.Value);
        })
        .Produces<{Feature}Response>()
        .RequireAuthorization("{PolicyName}")
        .WithMetadata(new RouteMetadata { Tags = new[] { "{TagName}" } });
    }
}

// 2. Query Definition
public static class Get{Feature} {
    public class {Feature}Query : IRequest<Result<{Feature}Response>> {
        public int ID { get; set; } = 0;
        // Additional filter properties
    }
    
    // 3. Validation Rules
    public class Validator : AbstractValidator<{Feature}Query> {
        public Validator() {
            RuleFor(x => x.ID)
                .GreaterThan(0)
                .WithMessage("ID cannot be zero.");
        }
    }
    
    // 4. Query Handler
    internal sealed class Handler : IRequestHandler<{Feature}Query, Result<{Feature}Response>> {
        private readonly ILogger<Handler> _logger;
        private readonly IValidator<{Feature}Query> _validator;
        private readonly I{Feature}Data _data;
        
        public Handler(
            ILogger<Handler> logger,
            IValidator<{Feature}Query> validator,
            I{Feature}Data data
        ) {
            _logger = logger;
            _validator = validator;
            _data = data;
        }
        
        public async Task<Result<{Feature}Response>> Handle({Feature}Query request, CancellationToken cancellationToken) {
            // Validate
            var validationResult = _validator.Validate(request);
            if (!validationResult.IsValid) {
                return Result.Failure<{Feature}Response>(new Error("Get{Feature}.Validation", validationResult.ToString()));
            }
            
            // Retrieve and map
            var {feature} = await _data.Get{Feature}(request.ID);
            
            if ({feature} is null) {
                return Result.Failure<{Feature}Response>(new Error(
                    "Get{Feature}.Null",
                    "The {feature} with the specified ID was not found"));
            }
            
            var response = {feature}.Adapt<{Feature}Response>();
            
            // Optional: Enrich response with additional data
            
            return response;
        }
    }
}
```

**Key Patterns**:
- Returns `NotFound` for missing entities
- Validation ensures query parameters are valid
- Response mapping allows projection/transformation
- Separate method for complex retrieval logic

### Query Pattern (Get Collection)

**Use when**: Retrieving multiple entities with filtering

**Structure**:
```csharp
namespace {ProjectName}.Features.{FeatureName};

// 1. Carter Endpoint Module
public class Get{Feature}sEndpoint : ICarterModule {
    public void AddRoutes(IEndpointRouteBuilder app) {
        app.MapGet("{route}", async (int param1, string param2, ISender sender) => {
            var query = new Get{Feature}s.{Feature}Query { 
                Param1 = param1, 
                Param2 = param2 
            };
            var result = await sender.Send(query);
            
            if (result.IsFailure) {
                return Results.NotFound(result.Error);
            }
            
            return Results.Ok(result.Value);
        })
        .Produces<IEnumerable<{Feature}Response>>()
        .RequireAuthorization("{PolicyName}")
        .WithMetadata(new RouteMetadata { Tags = new[] { "{TagName}" } });
    }
}

// 2. Query Definition
public static class Get{Feature}s {
    public class {Feature}Query : IRequest<Result<IEnumerable<{Feature}Response>>> {
        public int Param1 { get; set; } = 0;
        public string Param2 { get; set; } = string.Empty;
        // Filter/pagination properties
    }
    
    // 3. Validation Rules
    public class Validator : AbstractValidator<{Feature}Query> {
        public Validator() {
            RuleFor(x => x.Param1)
                .GreaterThan(0)
                .WithMessage("Param1 cannot be zero.");
            
            // Date format validation example
            RuleFor(x => x.DateParam)
                .Matches(@"\d{4}-\d{2}-\d{2}")
                .WithMessage("DateParam must be in the format yyyy-MM-dd.");
        }
    }
    
    // 4. Query Handler
    internal sealed class Handler : IRequestHandler<{Feature}Query, Result<IEnumerable<{Feature}Response>>> {
        private readonly ILogger<Handler> _logger;
        private readonly IValidator<{Feature}Query> _validator;
        private readonly I{Feature}Data _data;
        
        public Handler(
            ILogger<Handler> logger,
            IValidator<{Feature}Query> validator,
            I{Feature}Data data
        ) {
            _logger = logger;
            _validator = validator;
            _data = data;
        }
        
        public async Task<Result<IEnumerable<{Feature}Response>>> Handle({Feature}Query request, CancellationToken cancellationToken) {
            // Validate
            var validationResult = _validator.Validate(request);
            if (!validationResult.IsValid) {
                return Result.Failure<IEnumerable<{Feature}Response>>(new Error("Get{Feature}s.Validation", validationResult.ToString()));
            }
            
            // Retrieve collection
            var {feature}s = await _data.List{Feature}s(/* filter params */);
            
            if ({feature}s is null) {
                return Result.Failure<IEnumerable<{Feature}Response>>(new Error(
                    "Get{Feature}s.Null",
                    "Failed to get {feature}s"));
            }
            
            var response = {feature}s.Adapt<List<{Feature}Response>>();
            
            return response;
        }
    }
}
```

**Key Patterns**:
- Query parameters come from route or query string
- Returns collections (IEnumerable<T>)
- Validation includes format checks (dates, etc.)
- Consider pagination for large datasets

### Command Pattern (Update)

**Use when**: Modifying existing entities

**Structure**:
```csharp
namespace {ProjectName}.Features.{FeatureName};

// 1. Carter Endpoint Module
public class Update{Feature}Endpoint : ICarterModule {
    public void AddRoutes(IEndpointRouteBuilder app) {
        app.MapPut("{route}", async ({Feature}UpdateRequest request, ISender sender) => {
            var command = new Update{Feature}.Command { {Feature} = request };
            var result = await sender.Send(command);
            
            if (result.IsFailure) {
                return Results.BadRequest(result.Error);
            }
            
            return Results.Ok(result.Value);
        })
        .Produces<int>()
        .RequireAuthorization("{PolicyName}")
        .WithMetadata(new RouteMetadata { Tags = new[] { "{TagName}" } });
    }
}

// 2. Command Definition
public static partial class Update{Feature} {
    public class Command : IRequest<Result<int>> {
        public {Feature}UpdateRequest? {Feature} { get; set; }
    }
    
    // 3. Validation Rules
    public class Validator : AbstractValidator<Command> {
        public Validator() {
            RuleFor(x => x.{Feature})
                .NotNull()
                .WithMessage("No {feature} data provided.");
            
            RuleFor(x => x.{Feature}!.ID)
                .GreaterThan(0)
                .WithMessage("ID cannot be zero.");
            
            // Additional field validations
        }
    }
    
    // 4. Command Handler
    internal sealed partial class {Feature}Handler : IRequestHandler<Command, Result<int>> {
        private readonly ILogger<{Feature}Handler> _logger;
        private readonly IValidator<Command> _validator;
        private readonly I{Feature}Data _data;
        
        public {Feature}Handler(
            IValidator<Command> validator,
            ILogger<{Feature}Handler> logger,
            I{Feature}Data data
        ) {
            _validator = validator;
            _logger = logger;
            _data = data;
        }
        
        public async Task<Result<int>> Handle(Command request, CancellationToken cancellationToken) {
            // Validate
            var validationResult = _validator.Validate(request);
            if (!validationResult.IsValid) {
                return Result.Failure<int>(new Error("Update{Feature}.Validation", validationResult.ToString()));
            }
            
            try {
                // Verify entity exists
                var existing{Feature} = await _data.Get{Feature}(request.{Feature}!.ID);
                if (existing{Feature} is null) {
                    return Result.Failure<int>(new Error("Update{Feature}", "The {feature} with the specified ID was not found"));
                }
                
                // Perform update
                await _data.Update{Feature}(/* updated values */);
                
                return existing{Feature}.ID;
            } catch (Exception ex) {
                return Result.Failure<int>(new Error("Update{Feature}.Exception", ex.Message));
            }
        }
    }
}
```

**Key Patterns**:
- Verify entity exists before update
- Update request includes entity ID
- Returns updated entity ID
- BadRequest for validation failures
- Consider optimistic concurrency with version tokens

## DTOs and Contracts

### Request DTOs (Commands)

```csharp
namespace {ProjectName}.Features.{FeatureName};

public class {Feature}AddRequest {
    public required string PropertyName { get; init; }
    public int NumericProperty { get; init; }
    // Only properties needed for creation
    // Exclude: ID, CreatedDate, UpdatedDate
}

public class {Feature}UpdateRequest {
    public required int ID { get; init; }  // Identity required
    public required string PropertyName { get; init; }
    public int NumericProperty { get; init; }
    // Properties that can be updated
}
```

**Best Practices**:
- Use `init` accessors for immutability
- Mark non-nullable properties as `required` (C# 11+)
- Exclude computed/system properties
- Consider separate DTOs for different update scenarios

### Response DTOs (Queries)

```csharp
namespace {ProjectName}.Features.{FeatureName};

public class {Feature}Response {
    public int ID { get; init; }
    public string PropertyName { get; init; } = string.Empty;
    public int NumericProperty { get; init; }
    public DateTime CreatedDate { get; init; }
    // Include all properties consumers need
    // Can include computed properties
}
```

**Best Practices**:
- Inherit from domain model if structures align
- Add view-specific computed properties
- Use init-only properties
- Default string properties to `string.Empty`

## Validation Strategies

### FluentValidation Patterns

**Required Field Validation**:
```csharp
RuleFor(x => x.Property)
    .NotNull()
    .WithMessage("Property is required.");

RuleFor(x => x.StringProperty)
    .NotEmpty()
    .WithMessage("StringProperty cannot be empty.");
```

**Range Validation**:
```csharp
RuleFor(x => x.Age)
    .GreaterThan(0)
    .WithMessage("Age must be greater than zero.")
    .LessThanOrEqualTo(150)
    .WithMessage("Age must be realistic.");

RuleFor(x => x.Percentage)
    .InclusiveBetween(0, 100)
    .WithMessage("Percentage must be between 0 and 100.");
```

**Format Validation**:
```csharp
RuleFor(x => x.Email)
    .EmailAddress()
    .WithMessage("Invalid email format.");

RuleFor(x => x.DateString)
    .Matches(@"\d{4}-\d{2}-\d{2}")
    .WithMessage("Date must be in yyyy-MM-dd format.");

RuleFor(x => x.PhoneNumber)
    .Matches(@"^\+?[1-9]\d{1,14}$")
    .WithMessage("Invalid phone number format.");
```

**Nested Object Validation**:
```csharp
RuleFor(x => x.Address)
    .NotNull()
    .WithMessage("Address is required.")
    .SetValidator(new AddressValidator());  // Use separate validator
```

**Conditional Validation**:
```csharp
RuleFor(x => x.CompanyName)
    .NotEmpty()
    .When(x => x.CustomerType == CustomerType.Business)
    .WithMessage("Company name is required for business customers.");
```

**Cross-Field Validation**:
```csharp
RuleFor(x => x.EndDate)
    .GreaterThan(x => x.StartDate)
    .WithMessage("End date must be after start date.");
```

**Custom Validation**:
```csharp
RuleFor(x => x.Username)
    .Must(BeUniqueUsername)
    .WithMessage("Username already exists.");

private bool BeUniqueUsername(string username) {
    // Custom validation logic
    return !_userRepository.UsernameExists(username);
}
```

## Error Handling Patterns

### Result Pattern Implementation

The templates use a Result<T> pattern for explicit error handling:

```csharp
// Success case
return Result.Success(value);
return value;  // Implicit conversion

// Failure case
return Result.Failure<T>(new Error("Category.Operation", "Description"));

// Checking results
if (result.IsFailure) {
    return Results.BadRequest(result.Error);
}

return Results.Ok(result.Value);
```

### Error Categories

Organize errors by category for better diagnostics:

- **Validation**: `"{Feature}.Validation"` - Input validation failures
- **NotFound**: `"{Feature}.Null"` or `"{Feature}.NotFound"` - Entity not found
- **Exception**: `"{Feature}.Exception"` - Unexpected errors
- **Business**: `"{Feature}.BusinessRule"` - Business rule violations

### HTTP Status Code Mapping

- `200 OK`: Successful query/command
- `400 Bad Request`: Validation failure, business rule violation
- `404 Not Found`: Entity not found
- `401 Unauthorized`: Authentication failure
- `403 Forbidden`: Authorization failure
- `500 Internal Server Error`: Unhandled exceptions (should be rare)

## Dependency Injection Patterns

### Required Registrations

For each feature, register:

```csharp
// MediatR handlers (usually auto-registered)
services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(assembly));

// FluentValidation validators
services.AddValidatorsFromAssembly(assembly);

// Carter modules
services.AddCarter();

// Data access services
services.AddScoped<I{Feature}Data, {Feature}Data>();

// Logging is automatically available via ILogger<T>
```

### Handler Constructor Pattern

```csharp
public {Feature}Handler(
    IValidator<Command> validator,     // FluentValidation validator
    ILogger<{Feature}Handler> logger,  // Structured logging
    I{Feature}Data data                // Data access
    // Add other dependencies as needed
) {
    _validator = validator;
    _logger = logger;
    _data = data;
}
```

**Best Practices**:
- Constructor injection only
- Inject interfaces, not concrete types
- Use scoped lifetime for data services
- Use singleton for stateless services

## Carter Module Configuration

### Endpoint Registration

```csharp
public class {Feature}Endpoint : ICarterModule {
    public void AddRoutes(IEndpointRouteBuilder app) {
        app.MapPost("{route}", handler)
            .Produces<TResponse>()              // Documents response type
            .ProducesProblem(400)               // Documents error responses
            .RequireAuthorization("{Policy}")    // Authorization policy
            .WithMetadata(new RouteMetadata {   // OpenAPI metadata
                Tags = new[] { "{TagName}" }
            })
            .WithName("{OperationId}")          // OpenAPI operation ID
            .WithDescription("{Description}");   // OpenAPI description
    }
}
```

### Routing Conventions

**RESTful routes**:
- `GET /api/{features}` - Get collection
- `GET /api/{features}/{id}` - Get single item
- `POST /api/{features}` - Create new item
- `PUT /api/{features}` - Update item (ID in body)
- `PUT /api/{features}/{id}` - Update item (ID in route)
- `DELETE /api/{features}/{id}` - Delete item

**Nested resources**:
- `GET /api/{parent}/{parentId}/{features}` - Get child collection
- `GET /api/{parent}/{parentId}/{features}/{id}` - Get child item

## Testing Strategies

### Unit Testing Handlers

Test handlers in isolation:

```csharp
[Fact]
public async Task Handle_ValidCommand_ReturnsSuccess() {
    // Arrange
    var validator = new Add{Feature}.Validator();
    var logger = new Mock<ILogger<Add{Feature}.{Feature}Handler>>();
    var data = new Mock<I{Feature}Data>();
    
    data.Setup(x => x.Add{Feature}(It.IsAny<{Feature}Model>()))
        .ReturnsAsync(new {Feature}Model { ID = 1 });
    
    var handler = new Add{Feature}.{Feature}Handler(validator, logger.Object, data.Object);
    var command = new Add{Feature}.Command { /* ... */ };
    
    // Act
    var result = await handler.Handle(command, CancellationToken.None);
    
    // Assert
    Assert.True(result.IsSuccess);
    Assert.Equal(1, result.Value);
}

[Fact]
public async Task Handle_InvalidCommand_ReturnsValidationFailure() {
    // Test validation failures
}

[Fact]
public async Task Handle_DataLayerException_ReturnsFailure() {
    // Test exception handling
}
```

### Integration Testing Endpoints

Test full request/response cycle:

```csharp
[Fact]
public async Task Post_{Feature}_ValidRequest_Returns200() {
    // Arrange
    var client = _factory.CreateClient();
    var request = new {Feature}AddRequest { /* ... */ };
    
    // Act
    var response = await client.PostAsJsonAsync("/api/{features}", request);
    
    // Assert
    response.StatusCode.Should().Be(HttpStatusCode.OK);
    var id = await response.Content.ReadFromJsonAsync<int>();
    id.Should().BeGreaterThan(0);
}
```

## Best Practices Summary

### Do's ✓

1. **Organize by feature**, not technical layer
2. **Validate in handlers**, not endpoints
3. **Use Result<T>** for explicit error handling
4. **Separate commands and queries** clearly
5. **Make DTOs immutable** with init-only properties
6. **Use meaningful error messages** with context
7. **Log exceptions** with structured logging
8. **Document with OpenAPI** metadata
9. **Test handlers independently** from endpoints
10. **Follow RESTful conventions** for routing
11. **Use CancellationToken** for all async operations
12. **Apply authorization policies** at endpoint level

### Don'ts ✗

1. **Don't bypass validation** "for convenience"
2. **Don't return domain models** directly from endpoints
3. **Don't catch and swallow exceptions** without logging
4. **Don't mix query and command logic** in handlers
5. **Don't use primitive obsession** - use value objects
6. **Don't skip null checks** on nullable properties
7. **Don't hardcode strings** - use constants or enums
8. **Don't forget CancellationToken** parameter
9. **Don't create anemic DTOs** - include business logic where appropriate
10. **Don't ignore validation errors** - always check IsValid

## Advanced Patterns

### Pagination Support

```csharp
public class {Feature}Query : IRequest<Result<PagedResult<{Feature}Response>>> {
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 20;
    // Filter properties
}

public class PagedResult<T> {
    public IEnumerable<T> Items { get; init; } = Enumerable.Empty<T>();
    public int TotalCount { get; init; }
    public int PageNumber { get; init; }
    public int PageSize { get; init; }
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPrevious => PageNumber > 1;
    public bool HasNext => PageNumber < TotalPages;
}
```

### Sorting and Filtering

```csharp
public class {Feature}Query : IRequest<Result<IEnumerable<{Feature}Response>>> {
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
    public string? SearchTerm { get; set; }
    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }
}
```

### Soft Delete Pattern

```csharp
public class Delete{Feature}.Command : IRequest<Result<bool>> {
    public int ID { get; set; }
}

// Handler marks as deleted rather than removing
await _data.SoftDelete{Feature}(request.ID);
```

### Audit Trail

```csharp
public abstract class AuditableEntity {
    public DateTime CreatedDate { get; init; }
    public string CreatedBy { get; init; } = string.Empty;
    public DateTime? ModifiedDate { get; set; }
    public string? ModifiedBy { get; set; }
}

// Apply in handler
entity.CreatedBy = _currentUserService.Username;
entity.CreatedDate = DateTime.UtcNow;
```

### Enrichment Pattern

For queries that need additional data:

```csharp
private async Task<{Feature}Response> Enrich{Feature}Response({Feature}Model {feature}) {
    var response = {feature}.Adapt<{Feature}Response>();
    
    // Add related data
    response.RelatedItems = await _data.GetRelatedItems({feature}.ID);
    
    // Add computed properties
    response.DisplayName = $"{feature.FirstName} {feature.LastName}";
    
    return response;
}
```

## Common Pitfalls and Solutions

### Problem: Validation in Multiple Places
**Solution**: Centralize all validation in FluentValidation validators within handlers

### Problem: Anemic Domain Models
**Solution**: Add behavior methods to domain models, not just properties

### Problem: Tight Coupling to Data Layer
**Solution**: Use repository interfaces, inject via constructor

### Problem: Missing Null Checks
**Solution**: Use nullable reference types, validate with FluentValidation

### Problem: Poor Error Messages
**Solution**: Provide context in error messages - what failed and why

### Problem: Testing Difficulties
**Solution**: Keep handlers focused, inject dependencies, use interfaces

### Problem: Performance Issues with Large Collections
**Solution**: Implement pagination, filtering, and projection at data layer

### Problem: Inconsistent HTTP Status Codes
**Solution**: Follow the error handling patterns consistently

## Configuration Checklist

When implementing a new feature, verify:

- [ ] Feature organized in dedicated namespace/folder
- [ ] Request DTOs defined (Add, Update as needed)
- [ ] Response DTO defined
- [ ] Carter endpoint module created with correct HTTP verb
- [ ] Command/Query class defined with IRequest<Result<T>>
- [ ] Validator class defined with validation rules
- [ ] Handler class implements IRequestHandler
- [ ] Handler validates input using validator
- [ ] Handler implements error handling with Result<T>
- [ ] Handler returns appropriate result types
- [ ] Endpoint maps failures to HTTP status codes
- [ ] Authorization policy applied
- [ ] OpenAPI metadata configured
- [ ] Data interface and implementation created
- [ ] Dependencies registered in DI container
- [ ] Unit tests written for handler
- [ ] Integration tests written for endpoint

## Reference: Full Feature Example

See the provided templates (`AddXxxx.cs`, `GetXxxx.cs`, `GetXxxxs.cs`, `UpdateXxxx.cs`) for complete, working examples of each pattern.

## Summary

This skill provides a structured approach to building maintainable, testable .NET APIs using:
- **CQRS** for clear separation of reads and writes
- **MediatR** for loose coupling and testability
- **FluentValidation** for declarative validation rules
- **Carter** for clean endpoint organization
- **Result pattern** for explicit error handling

Follow these patterns consistently to create a cohesive, predictable API surface that's easy to understand, maintain, and extend.
