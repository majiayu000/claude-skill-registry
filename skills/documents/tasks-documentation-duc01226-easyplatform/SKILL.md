---
name: tasks-documentation
version: 1.0.0
description: Autonomous subagent variant of documentation. Use when creating or updating technical documentation, API documentation, or inline code documentation.
infer: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

> **Skill Variant:** Use this skill for **autonomous documentation generation** with structured templates. For interactive documentation tasks with user feedback, use `documentation` instead.

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
```

## Pattern 2: TypeScript JSDoc

```typescript
/**
 * Manages the feature list state and operations.
 *
 * @example
 * ```typescript
 * @Component({ providers: [FeatureListStore] })
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
   * Use `isLoading$('loadItems')` to check loading status.
   */
  public loadItems = this.effectSimple(() => /* ... */);
}
```

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
    /// <response code="200">Returns the employee list.</response>
    /// <response code="401">Unauthorized.</response>
    [HttpGet]
    [ProducesResponseType(typeof(GetEmployeeListQueryResult), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetList([FromQuery] GetEmployeeListQuery query)
        => Ok(await Cqrs.SendAsync(query));
}
```

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

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
