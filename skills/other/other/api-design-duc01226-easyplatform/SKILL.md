---
name: api-design
version: 2.1.0
description: "[Architecture] Use when designing or modifying REST API endpoints, controller structure, route patterns, request/response DTOs. Triggers on keywords like "API endpoint", "REST", "controller", "route", "HTTP", "request body", "response"."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

## Quick Summary

**Goal:** Design or modify REST API endpoints following the project platform patterns and REST best practices.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `backend-patterns-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Design** — Define routes using RESTful conventions (plural nouns, proper HTTP methods)
2. **Implement** — Create controller + CQRS command/query with validation and authorization
3. **Verify** — Run API design checklist (routes, auth, validation, paging, error handling)

**Key Rules:**

- Follow project base controller + CQRS pattern from CLAUDE.md (see docs/project-reference/backend-patterns-reference.md)
- Use proper route naming: `/api/{resource}` (plural, lowercase, no verbs)
- Validation in Command/Query `Validate()`, NOT in controller
- Always add authorization attributes (see docs/project-reference/backend-patterns-reference.md)
- MUST READ `docs/project-reference/backend-patterns-reference.md` before implementation

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# REST API Design

Expert API design agent for the project following platform patterns and REST best practices.

**Patterns:** Follow CLAUDE.md backend patterns for controller, CQRS command/query, validation, and authorization.

**MUST READ** before implementation:

- `docs/project-reference/backend-patterns-reference.md`

## Route Naming Conventions

| Action          | HTTP Method | Route Pattern                   | Example                            |
| --------------- | ----------- | ------------------------------- | ---------------------------------- |
| List            | GET         | `/api/{resource}`               | `GET /api/employees`               |
| Get by ID       | GET         | `/api/{resource}/{id}`          | `GET /api/employees/123`           |
| Create/Update   | POST        | `/api/{resource}`               | `POST /api/employees`              |
| Delete          | DELETE      | `/api/{resource}/{id}`          | `DELETE /api/employees/123`        |
| Complex Search  | POST        | `/api/{resource}/search`        | `POST /api/employees/search`       |
| Custom Action   | POST        | `/api/{resource}/{id}/{action}` | `POST /api/employees/123/activate` |
| Nested Resource | GET         | `/api/{parent}/{id}/{child}`    | `GET /api/departments/1/employees` |

**⚠️ MUST READ:** CLAUDE.md for CQRS command/query DTOs, validation patterns, and authorization patterns.

## File Upload Endpoints

```csharp
[HttpPost("upload")]
[RequestSizeLimit(50 * 1024 * 1024)]  // 50MB
public async Task<IActionResult> Upload([FromForm] UploadCommand command)
    => Ok(await Cqrs.SendAsync(command));

public sealed class UploadCommand : CqrsCommand<UploadCommandResult> // project CQRS base (see docs/project-reference/backend-patterns-reference.md)
{
    [FromForm]
    public IFormFile File { get; set; } = null!;

    [FromForm]
    public string? Description { get; set; }
}
```

## Error Response Format

```csharp
// Framework handles errors automatically with standard format
{
    "type": "validation",
    "title": "Validation Error",
    "status": 400,
    "errors": {
        "email": ["Email is required", "Invalid email format"],
        "firstName": ["FirstName is required"]
    }
}

// Business errors
{
    "type": "business",
    "title": "Business Rule Violation",
    "status": 422,
    "detail": "Employee is already assigned to this department"
}
```

## API Design Checklist

- [ ] RESTful route naming (plural nouns, lowercase)?
- [ ] Appropriate HTTP methods?
- [ ] Proper authorization attributes?
- [ ] Validation in Command/Query Validate()?
- [ ] Consistent response format?
- [ ] Paging for list endpoints?
- [ ] Error handling follows project patterns?

## Anti-Patterns

- **Verbs in URLs**: Use `/employees/123/activate` not `/activateEmployee`
- **Missing Authorization**: Always add authorization attributes (see docs/project-reference/backend-patterns-reference.md)
- **Validation in Controller**: Move to Command/Query `Validate()`
- **Business Logic in Controller**: Keep controllers thin, logic in handlers
- **Inconsistent Naming**: Follow `{Resource}Controller` pattern

## Related

- `arch-cross-service-integration`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
