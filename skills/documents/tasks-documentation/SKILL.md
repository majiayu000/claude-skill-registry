---
name: tasks-documentation
description: Use for WRITING documentation with ready-to-use code templates (C# XML docs, TypeScript JSDoc, API docs, README patterns). Best for implementing actual documentation, adding code comments, and creating docs from scratch. NOT for documentation planning (use documentation instead).
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Documentation Workflow

## When to Use This Skill

- Creating API documentation
- Writing code comments
- Updating README files
- Generating architecture documentation

## Documentation Types

### 1. Code Comments

- XML docs for public APIs
- Inline comments for complex logic
- TODO/FIXME for technical debt

### 2. API Documentation

- Endpoint descriptions
- Request/response schemas
- Error codes and handling

### 3. Architecture Documentation

- Component diagrams
- Data flow documentation
- Integration guides

## Pattern 1: C# XML Documentation

```csharp
/// <summary>
/// Saves or updates an employee entity.
/// </summary>
/// <remarks>
/// This command handles both create and update operations.
/// For new employees, the Id should be null or empty.
/// </remarks>
/// <example>
/// <code>
/// var command = new SaveEmployeeCommand
/// {
///     Name = "John Doe",
///     Email = "john@example.com"
/// };
/// var result = await handler.HandleAsync(command, cancellationToken);
/// </code>
/// </example>
public sealed class SaveEmployeeCommand : PlatformCqrsCommand<SaveEmployeeCommandResult>
{
    /// <summary>
    /// The unique identifier of the employee.
    /// Null or empty for new employees.
    /// </summary>
    public string? Id { get; set; }

    /// <summary>
    /// The employee's full name.
    /// </summary>
    /// <value>Must be non-empty and max 200 characters.</value>
    public string Name { get; set; } = string.Empty;
}

/// <summary>
/// Represents a unique expression for finding an employee.
/// </summary>
/// <param name="companyId">The company identifier.</param>
/// <param name="userId">The user identifier.</param>
/// <returns>An expression that matches the unique employee.</returns>
public static Expression<Func<Employee, bool>> UniqueExpr(string companyId, string userId)
    => e => e.CompanyId == companyId && e.UserId == userId;
```

## Pattern 2: TypeScript JSDoc

````typescript
/**
 * Manages the feature list state and operations.
 *
 * @example
 * ```typescript
 * @Component({
 *   providers: [FeatureListStore]
 * })
 * export class FeatureListComponent {
 *   constructor(private store: FeatureListStore) {
 *     store.loadItems();
 *   }
 * }
 * ```
 */
@Injectable()
export class FeatureListStore extends PlatformVmStore<FeatureListState> {
  /**
   * Loads items from the API with current filters.
   *
   * @remarks
   * This effect automatically tracks loading state under the key 'loadItems'.
   * Use `isLoading$('loadItems')` to check loading status.
   *
   * @see {@link FeatureApiService.getList}
   */
  public loadItems = this.effectSimple(() => /* ... */);

  /**
   * Updates the filter criteria and resets to first page.
   *
   * @param filters - Partial filter object to merge with current filters
   *
   * @example
   * ```typescript
   * // Filter by status
   * store.setFilters({ status: FeatureStatus.Active });
   *
   * // Filter by search text
   * store.setFilters({ searchText: 'keyword' });
   * ```
   */
  public setFilters(filters: Partial<FeatureFilters>): void {
    // ...
  }
}

/**
 * Represents a feature entity from the API.
 */
export interface FeatureDto {
  /** Unique identifier */
  id: string;

  /** Display name of the feature */
  name: string;

  /**
   * Current status of the feature.
   * @default FeatureStatus.Draft
   */
  status: FeatureStatus;
}
````

## Pattern 3: API Endpoint Documentation

```csharp
/// <summary>
/// Employee management endpoints.
/// </summary>
[ApiController]
[Route("api/[controller]")]
[PlatformAuthorize]
public class EmployeeController : PlatformBaseController
{
    /// <summary>
    /// Retrieves a paginated list of employees.
    /// </summary>
    /// <param name="query">Query parameters for filtering and pagination.</param>
    /// <returns>Paginated list of employees.</returns>
    /// <response code="200">Returns the employee list.</response>
    /// <response code="400">Invalid query parameters.</response>
    /// <response code="401">Unauthorized - authentication required.</response>
    /// <response code="403">Forbidden - insufficient permissions.</response>
    [HttpGet]
    [ProducesResponseType(typeof(GetEmployeeListQueryResult), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> GetList([FromQuery] GetEmployeeListQuery query)
        => Ok(await Cqrs.SendAsync(query));

    /// <summary>
    /// Creates or updates an employee.
    /// </summary>
    /// <param name="command">Employee data to save.</param>
    /// <returns>The saved employee.</returns>
    /// <response code="200">Employee saved successfully.</response>
    /// <response code="400">Validation failed.</response>
    /// <response code="404">Employee not found (for updates).</response>
    [HttpPost]
    [ProducesResponseType(typeof(SaveEmployeeCommandResult), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Save([FromBody] SaveEmployeeCommand command)
        => Ok(await Cqrs.SendAsync(command));
}
```

## Pattern 4: README Documentation

```markdown
# Feature Name

Brief description of what this feature does.

## Overview

More detailed explanation of the feature's purpose and functionality.

## Architecture
```

┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Frontend │────▶│ API Layer │────▶│ Domain Layer │
│ Component │ │ Controller │ │ Entity │
└─────────────────┘ └──────────────────┘ └─────────────────┘

````

## Usage

### Backend

```csharp
// Example usage
var command = new SaveFeatureCommand { Name = "Example" };
var result = await handler.HandleAsync(command, cancellationToken);
````

### Frontend

```typescript
// Example usage
this.store.loadItems();
```

## Configuration

| Setting        | Description               | Default |
| -------------- | ------------------------- | ------- |
| `MaxItems`     | Maximum items per page    | 50      |
| `CacheTimeout` | Cache duration in seconds | 300     |

## API Endpoints

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| GET    | `/api/feature`      | List features         |
| POST   | `/api/feature`      | Create/update feature |
| DELETE | `/api/feature/{id}` | Delete feature        |

## Error Handling

| Code | Description          |
| ---- | -------------------- |
| 400  | Invalid request data |
| 404  | Feature not found    |
| 409  | Conflict (duplicate) |

## Related

- [Entity Documentation](./Entity.md)
- [API Reference](./API.md)

````

## Pattern 5: Inline Code Comments

```csharp
protected override async Task<SaveEmployeeCommandResult> HandleAsync(
    SaveEmployeeCommand request, CancellationToken cancellationToken)
{
    // Step 1: Determine if this is a create or update operation
    var isCreate = request.Id.IsNullOrEmpty();

    // Step 2: Get or create the entity
    var employee = isCreate
        ? request.MapToNewEntity()
            .With(e => e.CreatedBy = RequestContext.UserId())
        : await repository.GetByIdAsync(request.Id, cancellationToken)
            .EnsureFound($"Employee not found: {request.Id}")
            .Then(existing => request.UpdateEntity(existing));

    // Step 3: Validate business rules
    // NOTE: This checks for duplicate codes within the same company
    await employee.ValidateAsync(repository, cancellationToken).EnsureValidAsync();

    // Step 4: Persist changes
    // The repository automatically raises entity events for cross-service sync
    var saved = await repository.CreateOrUpdateAsync(employee, cancellationToken);

    // Step 5: Return result
    return new SaveEmployeeCommandResult
    {
        Employee = new EmployeeDto(saved)
    };
}
````

## Documentation Guidelines

### DO

- Document public APIs with XML/JSDoc
- Explain "why" not "what"
- Include usage examples
- Keep documentation close to code
- Update docs when code changes

### DON'T

- State the obvious
- Leave TODO comments indefinitely
- Write documentation that duplicates code
- Create separate docs that become stale

## Comment Types

| Type             | When to Use               |
| ---------------- | ------------------------- |
| `/// <summary>`  | Public API documentation  |
| `// Explanation` | Complex logic explanation |
| `// TODO:`       | Planned improvements      |
| `// FIXME:`      | Known issues              |
| `// HACK:`       | Temporary workarounds     |
| `// NOTE:`       | Important information     |

## Verification Checklist

- [ ] Public APIs have XML/JSDoc documentation
- [ ] Complex logic has explanatory comments
- [ ] Examples are provided where helpful
- [ ] Documentation is accurate and up-to-date
- [ ] No obvious/redundant comments
- [ ] TODO/FIXME items are actionable
