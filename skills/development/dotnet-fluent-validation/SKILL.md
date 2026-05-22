---
name: dotnet-fluent-validation
description: Guides the implementation of FluentValidation validators for DTOs in a .NET 8 project. Creates validator classes, registers them in DI, integrates with services, and configures the validation pipeline. Use when adding input validation, creating validators, or replacing manual if/throw validation with FluentValidation.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Task
---

# FluentValidation — Implementation Guide

You are an expert assistant that helps developers implement FluentValidation in .NET 8 projects. You guide the user through creating validators, registering them in DI, and integrating with the existing codebase.

## Input

The user will describe the DTO or entity to validate: `$ARGUMENTS`

Before generating code:
1. **Read the project structure** — Identify the projects/layers in the solution (API, Domain/Business, DTO, Infra, etc.)
2. **Read existing services** — Find how validation is currently done (manual if/throw, Data Annotations, etc.)
3. **Read existing DI setup** — Find where services are registered (Program.cs, Startup.cs, Initializer.cs, etc.)
4. **Match existing patterns** — Follow the project's naming conventions, namespaces, and code style

---

## Architecture & Data Flow

```
Controller → Service → Validator → (if invalid) throw ValidationException
                     → (if valid) proceed with business logic
```

**Typical current pattern:** Services validate inline with `if/throw new Exception("message")`.
**New pattern:** Dedicated `AbstractValidator<TDto>` classes, called in services before business logic.

---

## Step-by-Step Implementation

### Step 1: Install NuGet Packages

Add FluentValidation to the project where validators will live (typically the Domain/Business layer, same as services):

```bash
dotnet add {ProjectName}.csproj package FluentValidation
dotnet add {ProjectName}.csproj package FluentValidation.DependencyInjectionExtensions
```

---

### Step 2: Create Validator — `Validators/{DtoName}Validator.cs`

Create a `Validators/` folder in the project where services live.

**Naming convention:** `{DtoName}Validator.cs` — one validator per DTO.

**Example — CreateUserDtoValidator:**

```csharp
using FluentValidation;

namespace {ProjectNamespace}.Validators
{
    public class CreateUserDtoValidator : AbstractValidator<CreateUserDto>
    {
        public CreateUserDtoValidator()
        {
            RuleFor(x => x.Name)
                .NotEmpty().WithMessage("Name is required")
                .MaximumLength(200).WithMessage("Name must not exceed 200 characters");

            RuleFor(x => x.Email)
                .NotEmpty().WithMessage("Email is required")
                .EmailAddress().WithMessage("Email is not valid");

            RuleFor(x => x.Age)
                .GreaterThan(0).WithMessage("Age must be greater than 0")
                .LessThanOrEqualTo(150).WithMessage("Age is invalid");
        }
    }
}
```

### Common Validation Rules Reference

```csharp
// String
RuleFor(x => x.Name).NotEmpty().WithMessage("Name is required");
RuleFor(x => x.Name).MaximumLength(200).WithMessage("Name is too long");
RuleFor(x => x.Name).MinimumLength(3).WithMessage("Name is too short");
RuleFor(x => x.Name).Matches(@"^[a-zA-Z\s]+$").WithMessage("Name contains invalid characters");

// Email
RuleFor(x => x.Email).NotEmpty().EmailAddress().WithMessage("Email is not valid");

// Numeric
RuleFor(x => x.Price).GreaterThan(0).WithMessage("Price must be greater than 0");
RuleFor(x => x.Percentage).InclusiveBetween(0, 100).WithMessage("Must be between 0 and 100");

// Enum
RuleFor(x => x.Status).IsInEnum().WithMessage("Invalid status");

// Date
RuleFor(x => x.BirthDate).LessThan(DateTime.Now).WithMessage("Birth date must be in the past");

// Conditional
RuleFor(x => x.Slug)
    .NotEmpty().WithMessage("Slug is required")
    .When(x => x.Id > 0); // Only required on update

// Nested object
RuleFor(x => x.Address).SetValidator(new AddressValidator());

// Collection
RuleForEach(x => x.Items).SetValidator(new OrderItemValidator());

// Custom rule
RuleFor(x => x.Document)
    .Must(doc => IsValidCpf(doc)).WithMessage("Invalid CPF")
    .When(x => !string.IsNullOrEmpty(x.Document));
```

---

### Step 3: Register Validators in DI

Find the project's DI registration file (e.g., `Program.cs`, `Startup.cs`, or a custom `Initializer.cs`).

**Option A — Auto-register all validators (recommended):**

```csharp
using FluentValidation;

// Scans the assembly and registers all AbstractValidator<T> implementations
services.AddValidatorsFromAssemblyContaining<CreateUserDtoValidator>(ServiceLifetime.Scoped);
```

**Option B — Register individually:**

```csharp
using FluentValidation;

services.AddScoped<IValidator<CreateUserDto>, CreateUserDtoValidator>();
services.AddScoped<IValidator<UpdateUserDto>, UpdateUserDtoValidator>();
```

> **Note:** Match the service lifetime used by the project (Scoped, Transient, etc.).

---

### Step 4: Inject and Use in Services

Inject `IValidator<TDto>` into the service and call it before the business logic.

**Before (manual validation):**

```csharp
public UserModel Insert(CreateUserDto dto)
{
    if (string.IsNullOrEmpty(dto.Name))
        throw new Exception("Name is required");
    if (string.IsNullOrEmpty(dto.Email))
        throw new Exception("Email is required");
    // ... more manual checks

    // business logic
}
```

**After (FluentValidation):**

```csharp
public class UserService : IUserService
{
    private readonly IValidator<CreateUserDto> _createValidator;
    // ... other dependencies

    public UserService(IValidator<CreateUserDto> createValidator /* ... */)
    {
        _createValidator = createValidator;
    }

    public UserModel Insert(CreateUserDto dto)
    {
        // FluentValidation — replaces manual if/throw checks
        _createValidator.ValidateAndThrow(dto);

        // Business rules that require database (keep in service)
        var existing = _repository.GetByEmail(dto.Email);
        if (existing != null)
            throw new Exception("Email already registered");

        // ... proceed with insert
    }
}
```

> **Important distinction:**
> - **Input/format validations** → Move to FluentValidation (empty, email format, range, length)
> - **Business rules with DB access** → Keep in the service (duplicate checks, authorization, cross-entity rules)

---

### Step 5 (Optional): Validation Filter for Automatic Pipeline Validation

Automatically validate request DTOs before the controller action runs, returning 400 Bad Request on failure.

**Create `Filters/ValidationFilter.cs` in the API project:**

```csharp
using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace {ApiNamespace}.Filters
{
    public class ValidationFilter : IAsyncActionFilter
    {
        private readonly IServiceProvider _serviceProvider;

        public ValidationFilter(IServiceProvider serviceProvider)
        {
            _serviceProvider = serviceProvider;
        }

        public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
        {
            foreach (var argument in context.ActionArguments.Values)
            {
                if (argument == null) continue;

                var validatorType = typeof(IValidator<>).MakeGenericType(argument.GetType());
                var validator = _serviceProvider.GetService(validatorType) as IValidator;

                if (validator == null) continue;

                var validationContext = new ValidationContext<object>(argument);
                var result = await validator.ValidateAsync(validationContext);

                if (!result.IsValid)
                {
                    var errors = result.Errors.Select(e => e.ErrorMessage).ToList();
                    context.Result = new BadRequestObjectResult(new
                    {
                        success = false,
                        message = "Validation failed",
                        errors
                    });
                    return;
                }
            }

            await next();
        }
    }
}
```

**Register the filter:**

```csharp
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ValidationFilter>();
});
```

> **Adapt the error response** to match the project's existing error response contract (e.g., `StatusResult`, `ApiResponse`, or a custom error DTO).

---

### Step 6 (Optional): Validator with Dependency Injection

For validators that need access to repositories or external services (e.g., uniqueness checks):

```csharp
using FluentValidation;

namespace {ProjectNamespace}.Validators
{
    public class CreateUserBusinessValidator : AbstractValidator<CreateUserDto>
    {
        public CreateUserBusinessValidator(IUserRepository userRepository)
        {
            RuleFor(x => x.Name)
                .NotEmpty().WithMessage("Name is required");

            RuleFor(x => x.Email)
                .NotEmpty().WithMessage("Email is required")
                .EmailAddress().WithMessage("Email is not valid")
                .MustAsync(async (email, cancellation) =>
                {
                    var existing = await userRepository.GetByEmailAsync(email);
                    return existing == null;
                }).WithMessage("Email already registered");
        }
    }
}
```

> **Use with caution:** Validators with DB access are heavier and harder to unit test in isolation. Prefer keeping database-dependent checks in the service layer.

---

### Step 7 (Optional): Handling ValidationException in Controllers

If using FluentValidation's built-in `ValidateAndThrow` (which throws `ValidationException`), catch it in controllers or use a global exception handler:

**Per-controller approach:**

```csharp
[HttpPost]
public IActionResult Create([FromBody] CreateUserDto dto)
{
    try
    {
        var result = _service.Insert(dto);
        return Ok(result);
    }
    catch (ValidationException ex)
    {
        var errors = ex.Errors.Select(e => e.ErrorMessage).ToList();
        return BadRequest(new { success = false, errors });
    }
    catch (Exception ex)
    {
        return StatusCode(500, ex.Message);
    }
}
```

**Global exception middleware approach:**

```csharp
// In Program.cs or a middleware class:
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        var exception = context.Features.Get<IExceptionHandlerFeature>()?.Error;

        if (exception is ValidationException validationEx)
        {
            context.Response.StatusCode = 400;
            var errors = validationEx.Errors.Select(e => e.ErrorMessage).ToList();
            await context.Response.WriteAsJsonAsync(new { success = false, errors });
        }
        else
        {
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new { success = false, message = exception?.Message });
        }
    });
});
```

---

## Validation Separation Guide

| Type | Where | Example |
|------|-------|---------|
| **Input/Format** | FluentValidation (`AbstractValidator`) | Empty fields, email format, min/max length, numeric range, enum values |
| **Business Rules** | Service layer | Duplicate name/email (requires DB), access control, cross-entity rules |
| **Cross-field** | FluentValidation with `When`/`Must` | "EndDate must be after StartDate", conditional required fields |
| **Async/DB rules** | FluentValidation with `MustAsync` or service layer | Uniqueness checks — prefer service unless reused across multiple services |

---

## Checklist

| # | Action | Description |
|---|--------|-------------|
| 1 | Install | `dotnet add package FluentValidation` on the project with services |
| 2 | Install | `dotnet add package FluentValidation.DependencyInjectionExtensions` |
| 3 | Create | `Validators/{DtoName}Validator.cs` — one per DTO |
| 4 | Register | Add `services.AddValidatorsFromAssemblyContaining<...>()` in DI setup |
| 5 | Integrate | Inject `IValidator<TDto>` in services, call `ValidateAndThrow()` |
| 6 | Handle errors | Catch `ValidationException` in controllers or add global exception handler |
| 7 | Optional | Create `ValidationFilter` for automatic pipeline validation |
| 8 | Optional | Create validators with DI for business rules with DB access |

---

## Response Guidelines

1. **Read the project first** — Understand the structure, naming, namespaces, and DI setup before writing code
2. **Follow project conventions** — Match existing code style, namespace patterns, and folder structure
3. **Match existing error messages** — Reuse the exact same error strings to avoid breaking frontend/clients
4. **Keep business rules in services** — Only move input/format validations to FluentValidation
5. **One validator per DTO** — Don't combine validators for different DTOs
6. **Adapt error responses** — Match the project's existing error response contract
7. **Follow the order** — Package → Validator → DI → Service integration → Error handling
