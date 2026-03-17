---
name: clean-architecture-rules
description: Enforces Clean Architecture dependency rules (Domain → Application → Infrastructure → API/Blazor). Blocks violations to maintain architectural integrity.
type: guardrail
enforcement: block
priority: critical
---

# Clean Architecture Dependency Rules

> **Project-Agnostic Clean Architecture Guidelines**
>
> Placeholders use `{Placeholder}` syntax - see [docs/TEMPLATE_GLOSSARY.md](../../../docs/TEMPLATE_GLOSSARY.md).

## Purpose

This is a **CRITICAL GUARDRAIL** that enforces Clean Architecture's fundamental dependency rule: **dependencies flow inward only**. Violations are **BLOCKED** to prevent architectural degradation.

## When This Skill Activates

**Automatically BLOCKS when**:
- Attempting to add wrong project references
- Importing namespaces that violate dependency rules
- Detecting prohibited `using` statements in Domain or Application layers

**Triggered by**:
- Keywords: "dependency", "reference", "architecture", "layer", "add project"
- File patterns: Domain/**/*.cs, Application/**/*.cs
- Content patterns: `using {Project}.Infrastructure`, `using Microsoft.EntityFrameworkCore` in Domain

## The Dependency Rule

```
┌─────────────────────────────────────────────────────────────┐
│              CLEAN ARCHITECTURE LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              1. DOMAIN (Core)                       │   │
│  │              {Project}.Domain                       │   │
│  │              ↑ NO DEPENDENCIES                      │   │
│  │  • Entities, Enums, Value Objects, Domain Events    │   │
│  │  • Pure C# - No framework dependencies             │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ▲                                   │
│                         │ References                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         2. APPLICATION (Use Cases)                  │   │
│  │         {Project}.Application                       │   │
│  │         ↑ References: Domain ONLY                   │   │
│  │  • CQRS Commands/Queries, DTOs, Interfaces          │   │
│  │  • MediatR, FluentValidation, AutoMapper            │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ▲                                   │
│                         │ References                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    3. INFRASTRUCTURE (Implementation)               │   │
│  │    {Project}.Persistence + {Project}.Infrastructure │   │
│  │    ↑ References: Application, Domain                │   │
│  │  • DbContext, Repositories, External APIs           │   │
│  │  • EF Core, Database Provider, Email, File Storage  │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ▲                                   │
│                         │ References                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │       4. PRESENTATION (Entry Points)                │   │
│  │       {Project}.API + {Project}.Blazor              │   │
│  │       ↑ References: ALL (Composition Root)          │   │
│  │  • Controllers, Pages, Dependency Registration      │   │
│  │  • ASP.NET Core, Blazor, SignalR                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Resources

| Resource | Description |
|----------|-------------|
| [dependency-rules.md](resources/dependency-rules.md) | Complete dependency matrix and flow diagram |
| [layer-responsibilities.md](resources/layer-responsibilities.md) | What code belongs in each layer |
| [violation-examples.md](resources/violation-examples.md) | Common violations and error messages |
| [fix-patterns.md](resources/fix-patterns.md) | How to fix violations using interfaces and DI |

## Valid Dependency Examples

```csharp
// ✅ VALID: Application references Domain
namespace {Project}.Application.Features.{Entities}.Commands;

using {Project}.Domain.Entities;  // ✅ OK - App can reference Domain
using {Project}.Domain.Enums;     // ✅ OK
using MediatR;                    // ✅ OK - Framework dependency

// ✅ VALID: Infrastructure references Application and Domain
namespace {Project}.Persistence.Repositories;

using {Project}.Application.Interfaces;  // ✅ OK - Implements interfaces
using {Project}.Domain.Entities;         // ✅ OK - Works with entities
using Microsoft.EntityFrameworkCore;     // ✅ OK - Infrastructure can use EF Core

// ✅ VALID: API references all layers
namespace {Project}.API.Controllers;

using {Project}.Application.Features.{Entities}.Commands;  // ✅ OK
using {Project}.Infrastructure.Services;                   // ✅ OK
using MediatR;                                             // ✅ OK
```

## BLOCKED Violations

```csharp
// ❌ BLOCKED: Domain referencing ANYTHING
namespace {Project}.Domain.Entities;

using Microsoft.EntityFrameworkCore;    // ❌ BLOCKED! Domain must be pure
using {Project}.Application.DTOs;       // ❌ BLOCKED! Dependency flows wrong way

// ❌ BLOCKED: Application referencing Infrastructure
namespace {Project}.Application.Features.{Entities}.Queries;

using {Project}.Infrastructure.Persistence;  // ❌ BLOCKED! Use interfaces instead
using {Project}.API.Controllers;             // ❌ BLOCKED! Wrong direction

// ❌ BLOCKED: Application referencing Presentation
namespace {Project}.Application.Commands;

using Microsoft.AspNetCore.Mvc;  // ❌ BLOCKED! Application must be framework-agnostic
```

## Quick Fix: Use Dependency Inversion

**Problem**: Application needs database access (Infrastructure)

**❌ Wrong - Direct dependency**:
```csharp
// In {Project}.Application
using {Project}.Infrastructure.Persistence;  // ❌ BLOCKED

public class Get{Entities}Handler
{
    private readonly {DbContext} _context;  // ❌ Concrete class
}
```

**✅ Correct - Interface in Application, Implementation in Infrastructure**:
```csharp
// Step 1: Define interface in Application layer
// File: {Project}.Application/Contracts/Persistence/I{Entity}Repository.cs
namespace {Project}.Application.Contracts.Persistence;

public interface I{Entity}Repository
{
    Task<List<{Entity}>> GetAllAsync(CancellationToken cancellationToken);
}

// Step 2: Use interface in Application
// File: {Project}.Application/Features/{Entities}/Handlers/Queries/Get{Entity}ListRequestHandler.cs
namespace {Project}.Application.Features.{Entities}.Handlers.Queries;

using {Project}.Application.Contracts.Persistence;  // ✅ OK - Same layer

public class Get{Entity}ListRequestHandler : IRequestHandler<Get{Entity}ListRequest, List<{Entity}ListDto>>
{
    private readonly I{Entity}Repository _repository;  // ✅ Abstraction

    public Get{Entity}ListRequestHandler(I{Entity}Repository repository)
    {
        _repository = repository;
    }

    public async Task<List<{Entity}ListDto>> Handle(Get{Entity}ListRequest request, CancellationToken cancellationToken)
    {
        var {entities} = await _repository.GetAllAsync(cancellationToken);
        return {entities}.Select(e => e.ToDto()).ToList();
    }
}

// Step 3: Implement in Infrastructure layer
// File: {Project}.Persistence/Repositories/{Entity}Repository.cs
namespace {Project}.Persistence.Repositories;

using {Project}.Application.Contracts.Persistence;  // ✅ OK - Implements interface
using {Project}.Domain.Entities;                    // ✅ OK - Works with entities
using Microsoft.EntityFrameworkCore;                // ✅ OK - Infrastructure can use EF Core

public class {Entity}Repository : I{Entity}Repository
{
    private readonly {DbContext} _context;

    public async Task<List<{Entity}>> GetAllAsync(CancellationToken cancellationToken)
    {
        return await _context.{Entities}.ToListAsync(cancellationToken);
    }
}

// Step 4: Register in API/Blazor (Composition Root)
// File: {Project}.API/Program.cs
builder.Services.AddScoped<I{Entity}Repository, {Entity}Repository>();  // ✅ DI binding
```

## Why This Matters

**Benefits of Clean Architecture**:
1. **Testability**: Domain and Application can be tested without database
2. **Flexibility**: Swap database providers without changing business logic
3. **Maintainability**: Business logic isolated from framework changes
4. **Team Scalability**: Clear boundaries for parallel development
5. **Deployment Options**: Domain can be reused across API, Blazor, CLI, etc.

**Cost of Violations**:
- Tight coupling makes testing difficult
- Framework upgrades break business logic
- Cannot reuse domain logic across projects
- Circular dependencies cause build failures

## CRITICAL: Validator Manual Instantiation Pattern

### Rule: Validators Must Be Instantiated Manually, NOT DI Injected

**BLOCKED Violation**: Validators injected via DI in handler constructor

```csharp
// ❌ BLOCKED: DI injection of validators
public class Create{Entity}CommandHandler : IRequestHandler<Create{Entity}Command, BaseCommandResponse<{IdType}>>
{
    private readonly IValidator<Create{Entity}Dto> _validator;  // ❌ BLOCKED!

    public Create{Entity}CommandHandler(
        I{Entity}Repository {entity}Repository,
        IMapper mapper,
        IValidator<Create{Entity}Dto> validator)  // ❌ BLOCKED - DI injection
    {
        _validator = validator;  // ❌ BLOCKED
    }

    public async Task<BaseCommandResponse<{IdType}>> Handle(...)
    {
        var validationResult = await _validator.ValidateAsync(request.{Entity}Dto);  // ❌ BLOCKED
        ...
    }
}
```

**✅ Correct Pattern**: Validator instantiated with dependencies passed to constructor

```csharp
// ✅ CORRECT: Manual instantiation with dependencies
namespace {Project}.Application.Features.{Entities}.Handlers.Commands;

using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using AutoMapper;
using {Project}.Application.Contracts.Persistence;
using {Project}.Application.DTOs.{Entity}.Validators;
using {Project}.Application.Features.{Entities}.Requests.Commands;
using {Project}.Application.Responses;
using {Project}.Domain;
using MediatR;

public class Create{Entity}CommandHandler : IRequestHandler<Create{Entity}Command, BaseCommandResponse<{IdType}>>
{
    private readonly I{Entity}Repository _{entity}Repository;
    private readonly I{RelatedEntity1}Repository _{relatedEntity1}Repository;
    private readonly I{RelatedEntity2}Repository _{relatedEntity2}Repository;
    private readonly IMapper _mapper;

    public Create{Entity}CommandHandler(
        I{Entity}Repository {entity}Repository,
        I{RelatedEntity1}Repository {relatedEntity1}Repository,
        I{RelatedEntity2}Repository {relatedEntity2}Repository,
        IMapper mapper)
    {
        _{entity}Repository = {entity}Repository;
        _{relatedEntity1}Repository = {relatedEntity1}Repository;
        _{relatedEntity2}Repository = {relatedEntity2}Repository;
        _mapper = mapper;
    }

    public async Task<BaseCommandResponse<{IdType}>> Handle(Create{Entity}Command request, CancellationToken cancellationToken)
    {
        var response = new BaseCommandResponse<{IdType}>();

        // ✅ CORRECT: Validator instantiated manually with all dependencies
        var validator = new Create{Entity}DtoValidator(
            _{relatedEntity1}Repository,
            _{relatedEntity2}Repository);

        var validationResult = await validator.ValidateAsync(request.{Entity}Dto, cancellationToken);

        if (!validationResult.IsValid)
        {
            response.Success = false;
            response.Message = "{Entity} creation failed.";
            response.Errors = validationResult.Errors.Select(e => e.ErrorMessage).ToList();
            return response;
        }

        // Map DTO to Entity
        var {entity} = _mapper.Map<{Entity}>(request.{Entity}Dto);

        // Save through repository
        {entity} = await _{entity}Repository.Create({entity});

        response.Success = true;
        response.Id = {entity}.Id;
        response.Message = "{Entity} created successfully.";

        return response;
    }
}
```

### Why Manual Instantiation?

1. **Fine-grained dependency control**: Each validator receives specific repositories it needs
2. **Prevents DI configuration issues**: No need to register validators in DI container
3. **Simplifies testing**: Easy to create test validators with mocked repositories
4. **Follows established pattern**: Consistent across all entity implementations

### Validator Constructor Pattern

Validators MUST accept repositories in constructor for FK validation.

```csharp
namespace {Project}.Application.DTOs.{Entity}.Validators;

using FluentValidation;
using {Project}.Application.Contracts.Persistence;

public class Create{Entity}DtoValidator : AbstractValidator<Create{Entity}Dto>
{
    private readonly I{RelatedEntity1}Repository _{relatedEntity1}Repository;
    private readonly I{RelatedEntity2}Repository _{relatedEntity2}Repository;

    public Create{Entity}DtoValidator(
        I{RelatedEntity1}Repository {relatedEntity1}Repository,
        I{RelatedEntity2}Repository {relatedEntity2}Repository)
    {
        _{relatedEntity1}Repository = {relatedEntity1}Repository;
        _{relatedEntity2}Repository = {relatedEntity2}Repository;

        // Standard validation rules
        RuleFor(x => x.Title)
            .NotEmpty().WithMessage("Title is required")
            .MaximumLength(200);

        RuleFor(x => x.Description)
            .MaximumLength(5000)
            .When(x => !string.IsNullOrEmpty(x.Description));

        // Foreign key validation with repository
        RuleFor(x => x.{RelatedEntity1}Id)
            .NotEmpty().WithMessage("{RelatedEntity1} is required")
            .MustAsync(async (id, cancellation) =>
            {
                var exists = await _{relatedEntity1}Repository.Exists(id);
                return exists;
            })
            .WithMessage("{RelatedEntity1} not found");

        RuleFor(x => x.{RelatedEntity2}Id)
            .MustAsync(async (id, cancellation) =>
            {
                if (!id.HasValue) return true;
                return await _{relatedEntity2}Repository.Exists(id.Value);
            })
            .When(x => x.{RelatedEntity2}Id.HasValue)
            .WithMessage("{RelatedEntity2} not found");
    }
}
```

---

## Deep Dive

For comprehensive guidance:
- **Dependency Matrix**: [dependency-rules.md](resources/dependency-rules.md)
- **Layer Responsibilities**: [layer-responsibilities.md](resources/layer-responsibilities.md)
- **Common Violations**: [violation-examples.md](resources/violation-examples.md)
- **Fix Patterns**: [fix-patterns.md](resources/fix-patterns.md)

---

**Enforcement Level**: BLOCK (Violations are prevented)
**Override**: Add `@skip-architecture-check` comment in file (use sparingly)
