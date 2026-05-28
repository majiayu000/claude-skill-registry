---
name: strangler-pattern
version: 1.0.0
description: Use when implementing strangler pattern for legacy migrations. Safely migrates controllers with feature flag control.
---
<!-- Powered by Prism Coreâ„¢ -->

# strangler-pattern

Implement the strangler pattern to safely migrate controllers from express-web-api to actions.api with feature flag control.

## Purpose

Execute a controlled migration of legacy endpoints to the new actions.api using the strangler pattern, ensuring zero downtime and instant rollback capability through feature flags.

**Related Documents:**
- **Validation:** [strangler-migration-checklist.md](./reference/strangler-migration-checklist.md)
- **Orchestration:** [strangler-pattern-migration.yaml](./reference/strangler-pattern-migration.yaml)

---

## When to Use Strangler Pattern

Use strangler pattern for:
- âœ… **Active endpoints** with existing frontend usage
- âœ… **Complex business logic** that needs gradual migration
- âœ… **High-risk migrations** requiring rollback capability
- âœ… **Live systems** where downtime isn't acceptable

Skip strangler pattern for:
- Simple CRUD operations that can be rewritten quickly
- Unused or deprecated endpoints
- New features without legacy constraints

---

## Architecture Overview

### Express-Web-API (Legacy)
- .NET Framework Web API controllers
- Command/Manager/Service factory patterns
- JWT authentication with custom attributes
- ServiceResponse<T> wrapper pattern

### Actions.API (Target)
- .NET 6+ Minimal API endpoints
- MediatR Command/Request â†’ Handler pattern
- Multiple authentication schemes
- Direct return types with ApiError exceptions

---

## Implementation Pattern

### Simple Controller Strangling (4 Lines)

```csharp
// Express-Web-API Controller - Real example from WorkflowController
public async Task<HttpResponseMessage> StartWorkflowExecution([FromBody] EyeShareWorkflowDesignerModel workflowDesigner)
{
    var tenant = Features.ResolveTenant(Request.Headers);
    if (await FeatureResolverSingleton.GetIsFeatureEnabledAsync(Features.WorkflowStrangle, tenant))
        return CreateResponseMessage(await strangledService.Value.StartWorkflowExecution(workflowDesigner));

    return CreateResponseMessage(legacyService.Value.StartWorkflowExecution(workflowDesigner, EyeShareToken));
}
```

### Controller Setup Pattern

```csharp
public class WorkflowController : ApiBaseController
{
    private Lazy<EyeShareWorkflowService> legacyService;
    private Lazy<WorkflowService> strangledService;  // Handles actions.api communication

    public WorkflowController()
    {
        legacyService = new Lazy<EyeShareWorkflowService>(() => {
            var token = TokenManager.GetTokenInfo();
            return new EyeShareWorkflowService(token, new DalService(token));
        });
        strangledService = new Lazy<WorkflowService>(() => new WorkflowService(ControllerContext));
    }
}
```

---

## Actions.API Implementation

### Clean Endpoint Pattern
```csharp
// Actions.API - No strangler terminology
app.MapPost("/api/Workflow/startExecution", 
    async (StartWorkflowExecutionRequest request, IMediator mediator) =>
    {
        var result = await mediator.Send(request);
        return Results.Ok(result);
    }).RequireAuthorization();
```

### Request/Handler/Service Pattern
```csharp
public record StartWorkflowExecutionRequest : IRequest<WorkflowExecutionResponse>
{
    public EyeShareWorkflowDesignerModel WorkflowDesigner { get; init; }
}

public class StartWorkflowExecutionHandler : IRequestHandler<StartWorkflowExecutionRequest, WorkflowExecutionResponse>
{
    public async Task<WorkflowExecutionResponse> Handle(StartWorkflowExecutionRequest request, CancellationToken cancellationToken)
    {
        return await _service.StartWorkflowExecutionAsync(request.WorkflowDesigner);
    }
}
```

---

## TDD Implementation Process

### Phase 1: Capture Real Behavior
1. **Test live endpoint** with authentication
2. **Capture JSON responses** for all scenarios
3. **Document authentication method** (password grant, client credentials)
4. **Record performance baseline**

### Phase 2: Create Tests (RED)
1. **Create integration tests** in actions.api test suite
2. **Use captured responses** as expected results
3. **Ensure tests fail** before implementation
4. **Follow existing test patterns** (ActionsApiFactory, DatabaseFixture)

### Phase 3: Implement (GREEN)
1. **Build minimal implementation** to pass tests
2. **Preserve exact behavior** from captured responses
3. **Follow actions.api patterns** (Request/Handler/Service)
4. **Integrate with existing auth/db**

### Phase 4: Strangler Integration
1. **Modify express-web-api controller** with feature flag
2. **Set up lazy-loaded services**
3. **Enable gradual traffic switching**
4. **Test dual-path validation**

---

## Key Integration Points

### Authentication
- **Express-web-api:** JWT via custom attributes
- **Actions.api:** Multiple schemes (JWT/MasterToken/TenantToken)
- **Bridge:** Service layer handles auth forwarding

### Database Context
- **Express-web-api:** Custom DbContext patterns
- **Actions.api:** TenantDbContext with IDbContextResolver
- **Migration:** Update entity mappings and queries

### Response Formats
- **Express-web-api:** ServiceResponse<T> wrapper
- **Actions.api:** Direct Results pattern
- **Bridge:** CreateResponseMessage() unifies response format

### Feature Flags
- **Location:** Express-web-api controllers only
- **Pattern:** FeatureResolverSingleton.GetIsFeatureEnabledAsync
- **Scope:** Per-tenant or per-user switching

---

## Success Criteria

âœ… **Feature flag routing works** between legacy and new systems
âœ… **Response behavior identical** to captured baseline
âœ… **All tests pass** in actions.api integration suite
âœ… **No regressions** in existing functionality
âœ… **Performance maintains** or exceeds baseline
âœ… **Rollback capability** tested and verified

---

## Quick Reference

**For Implementation:**
1. Follow the 4-line controller pattern from WorkflowController
2. Use lazy-loaded services for performance
3. Keep actions.api implementation clean (no strangler references)
4. Test with real captured data, not mock responses

**For Validation:**
- Use [strangler-migration-checklist.md](./reference/strangler-migration-checklist.md) for systematic verification

**For Process:**
- Follow [strangler-pattern-migration.yaml](./reference/strangler-pattern-migration.yaml) workflow orchestration
