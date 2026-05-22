# spaarke-conventions

---
description: Apply Spaarke coding standards from CLAUDE.md - naming, structure, file organization, and technology patterns
tags: [conventions, standards, naming, code-style, patterns]
techStack: [csharp, typescript, aspnet-core, react]
appliesTo: ["**/*.cs", "**/*.ts", "**/*.tsx"]
alwaysApply: true
---

## Purpose

Enforces Spaarke-specific coding conventions when generating or reviewing code. This skill is **always applied** to ensure consistency across the codebase. It codifies the standards from root `CLAUDE.md` into actionable rules.

## Always-Apply Rules

These conventions apply automatically to ALL code generation and review:

### File Naming

| File Type | Convention | Example |
|-----------|------------|---------|
| C# class files | PascalCase | `AuthorizationService.cs` |
| C# interface files | `I` + PascalCase | `IAuthorizationService.cs` |
| TypeScript components | PascalCase | `DataGrid.tsx` |
| TypeScript utilities | camelCase | `formatters.ts` |
| Test files | `{ClassName}.Tests.cs` | `AuthorizationService.Tests.cs` |
| ADRs | `ADR-{NNN}-{slug}.md` | `ADR-001-minimal-api-and-workers.md` |
| Config files | kebab-case + `.local.json` | `azure-config.local.json` |

### C# Naming Conventions

```csharp
// Types: PascalCase
public class DocumentService { }
public interface IDocumentService { }
public record DocumentDto { }
public enum DocumentStatus { }

// Methods: PascalCase
public async Task<Document> GetDocumentAsync(string id) { }

// Properties: PascalCase
public string DocumentId { get; set; }

// Private fields: _camelCase
private readonly GraphServiceClient _graphClient;
private int _retryCount;

// Parameters & locals: camelCase
public void Process(string documentId)
{
    var localResult = DoWork();
}

// Constants: PascalCase
public const int MaxRetryAttempts = 3;
public static readonly TimeSpan DefaultTimeout = TimeSpan.FromSeconds(30);
```

### TypeScript/React Naming Conventions

```typescript
// Components: PascalCase (file and export)
// File: DataGrid.tsx
export const DataGrid: React.FC<IDataGridProps> = (props) => { }

// Interfaces: IPascalCase
interface IDataGridProps {
  items: IDataItem[];
  onSelect: (item: IDataItem) => void;
}

// Types: PascalCase (no I prefix)
type ButtonVariant = 'primary' | 'secondary';

// Functions: camelCase
function formatDate(date: Date): string { }
const calculateTotal = (items: number[]) => items.reduce((a, b) => a + b, 0);

// Variables: camelCase
const selectedItems: IDataItem[] = [];
let isLoading = false;

// Constants: SCREAMING_SNAKE_CASE (module-level) or camelCase (local)
const API_BASE_URL = '/api/v1';
const maxRetries = 3;
```

### Directory Structure

```
src/
├── client/                    # Frontend code
│   ├── pcf/                   # PCF Controls
│   │   └── {ControlName}/     # One folder per control
│   │       ├── {ControlName}.tsx
│   │       ├── {ControlName}.css
│   │       └── index.ts
│   └── shared/                # Shared UI components
│       └── components/
├── server/                    # Backend code
│   ├── api/                   # Minimal API project
│   │   ├── Api/               # Endpoint groups
│   │   │   └── {Domain}Endpoints.cs
│   │   ├── Services/          # Business logic
│   │   ├── Infrastructure/    # External integrations (Graph, etc.)
│   │   └── Models/            # DTOs, domain models
│   └── shared/                # Shared .NET libraries
└── solutions/                 # Dataverse solution projects

tests/
├── unit/                      # Unit tests mirror src/ structure
├── integration/               # Integration tests
└── e2e/                       # End-to-end tests
```

## Technology-Specific Patterns

### .NET 8 Minimal API

```csharp
// ✅ DO: Use endpoint groups
public static class DocumentEndpoints
{
    public static void MapDocumentEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/documents")
            .WithTags("Documents");
        
        group.MapGet("/", GetAllDocuments);
        group.MapGet("/{id}", GetDocument);
        group.MapPost("/", CreateDocument);
    }
    
    private static async Task<Results<Ok<DocumentDto>, NotFound>> GetDocument(
        string id,
        DocumentService service)
    {
        var doc = await service.GetByIdAsync(id);
        return doc is null ? TypedResults.NotFound() : TypedResults.Ok(doc);
    }
}

// ✅ DO: Use endpoint filters for auth (ADR-008)
group.MapGet("/{id}", GetDocument)
    .AddEndpointFilter<DocumentAuthorizationFilter>();

// ❌ DON'T: Use global middleware for resource auth
app.UseMiddleware<AuthorizationMiddleware>();

// ✅ DO: Use concrete types unless seam needed (ADR-010)
services.AddSingleton<SpeFileStore>();

// ❌ DON'T: Create interfaces for single implementations
services.AddSingleton<ISpeFileStore, SpeFileStore>(); // unnecessary
```

### TypeScript/PCF Controls

```typescript
// ✅ DO: Import from Fluent UI v9
import { Button, Input, DataGrid } from "@fluentui/react-components";

// ❌ DON'T: Import from Fluent UI v8
import { PrimaryButton } from "@fluentui/react"; // WRONG

// ✅ DO: Import from shared library (ADR-012)
import { DataGrid, StatusBadge } from "@spaarke/ui-components";

// ✅ DO: Use proper TypeScript types
interface IProps {
  items: IDataItem[];
  onSelect: (item: IDataItem) => void;
}

// ❌ DON'T: Use any type
const handleClick = (e: any) => { }; // WRONG

// ✅ DO: Use React.FC with props interface
export const MyComponent: React.FC<IProps> = ({ items, onSelect }) => {
  return <div>...</div>;
};
```

### Dataverse Plugins

```csharp
// ✅ DO: Keep plugins thin (<200 LoC, <50ms)
public class ValidateDocumentPlugin : IPlugin
{
    public void Execute(IServiceProvider serviceProvider)
    {
        var context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
        var target = context.InputParameters["Target"] as Entity;
        
        ValidateRequiredFields(target);
        // That's it - no HTTP calls, no external services
    }
    
    private void ValidateRequiredFields(Entity entity)
    {
        if (!entity.Contains("sp_name"))
            throw new InvalidPluginExecutionException("Name is required");
    }
}

// ❌ DON'T: Make HTTP/Graph calls from plugins (ADR-002)
public class BadPlugin : IPlugin
{
    public void Execute(IServiceProvider serviceProvider)
    {
        using var client = new HttpClient(); // WRONG
        var result = client.GetAsync("...").Result; // WRONG
    }
}
```

## Error Handling Patterns

### API Responses

```csharp
// ✅ DO: Use ProblemDetails for errors
app.MapGet("/api/documents/{id}", async (string id, DocumentService service) =>
{
    try
    {
        var doc = await service.GetByIdAsync(id);
        return doc is null 
            ? Results.Problem(
                statusCode: 404,
                title: "Document not found",
                detail: $"No document exists with ID '{id}'")
            : Results.Ok(doc);
    }
    catch (UnauthorizedAccessException)
    {
        return Results.Problem(
            statusCode: 403,
            title: "Access denied",
            detail: "You do not have permission to access this document");
    }
});

// ❌ DON'T: Return raw exceptions
catch (Exception ex)
{
    return Results.BadRequest(ex.Message); // Leaks internal details
}
```

### PCF Controls

```typescript
// ✅ DO: Show user-friendly errors
try {
  const data = await fetchData();
  setItems(data);
} catch (error) {
  setError("Unable to load documents. Please try again.");
  console.error("Fetch failed:", error); // Log for debugging
}

// ❌ DON'T: Show technical errors to users
catch (error) {
  setError(error.stack); // WRONG - users don't need stack traces
}
```

## Async Patterns

```csharp
// ✅ DO: Use async/await properly
public async Task<Document> GetDocumentAsync(string id)
{
    return await _graphClient.GetAsync(id);
}

// ❌ DON'T: Block on async (sync-over-async)
public Document GetDocument(string id)
{
    return _graphClient.GetAsync(id).Result; // WRONG - can deadlock
}

// ✅ DO: Use ConfigureAwait(false) in library code
public async Task<Document> GetDocumentAsync(string id)
{
    return await _graphClient.GetAsync(id).ConfigureAwait(false);
}

// ✅ DO: Return Task directly when no await needed
public Task<Document> GetDocumentAsync(string id)
{
    return _graphClient.GetAsync(id); // No await, just pass through
}
```

## Documentation Standards

### C# XML Documentation

```csharp
/// <summary>
/// Retrieves a document by its unique identifier.
/// </summary>
/// <param name="id">The document's unique identifier.</param>
/// <returns>The document if found; otherwise, null.</returns>
/// <exception cref="UnauthorizedAccessException">
/// Thrown when the user doesn't have access to the document.
/// </exception>
public async Task<Document?> GetDocumentAsync(string id)
```

### TypeScript JSDoc

```typescript
/**
 * Formats a date for display in the UI.
 * @param date - The date to format
 * @param locale - Optional locale string (default: 'en-US')
 * @returns Formatted date string
 */
function formatDate(date: Date, locale = 'en-US'): string {
  return date.toLocaleDateString(locale);
}
```

## Quick Validation Rules

When generating or reviewing code, automatically check:

| Rule | Check | Severity |
|------|-------|----------|
| File naming | Matches conventions above | Warning |
| Import source | Fluent UI v9, not v8 | Warning |
| Interface necessity | Single implementation? | Info |
| Async pattern | No `.Result` or `.Wait()` | Warning |
| Error handling | Uses ProblemDetails | Warning |
| Plugin size | <200 LoC | Warning |
| Type safety | No `any` without justification | Warning |

## Resources

- Root `CLAUDE.md` - Full coding standards reference
- `docs/ai-knowledge/architecture/` - Pattern documentation
- `docs/reference/adr/` - Decision rationale (if needed)

## Related Skills

- **code-review**: Uses these conventions for review checklist
- **adr-check**: Deeper architectural validation
- **project-init**: Ensures new projects follow structure
