---
name: tasks-feature-implementation
version: 1.0.1
description: '[Subagent Tasks] Autonomous subagent variant of feature-implementation. Use when implementing new features or enhancements requiring multi-layer changes (Domain, Application, Persistence, API, Frontend).'

allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Autonomous feature implementation with structured discovery, knowledge graph, and approval gates (subagent variant of `feature-implementation`).

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Discovery & Analysis** — Requirement decomposition, codebase investigation (grep patterns), pattern recognition
2. **Knowledge Graph** — Backend impact (Domain, Application, Persistence, API), Frontend impact (Components, State, Services, Routing)
3. **Implementation Plan** — Create external memory file `.ai/workspace/analysis/{feature}-implementation.md` with checklist
4. **Approval Gate** — Present plan (summary, files to create/modify, risks, questions), await user approval
5. **Implementation** — Backend layer-by-layer (Domain → Persistence → Application → API), then Frontend (API Service → Store → Components)
6. **Verification** — Backend, Frontend, Integration testing

**Key Rules:**

- **INVESTIGATE before implementing**: Find similar features, identify patterns, map dependencies
- **External Memory**: Track all decisions in analysis file with Evidence Log
- **Approval Required**: CHECKPOINT before implementation - present plan and wait for user confirmation
- **Layer Order**: Backend (Domain → Persistence → Application → API), Frontend (Service → Store → Components)

> **Skill Variant:** Use this skill for **autonomous feature implementation** with structured workflows. For interactive feature development with user feedback, use `feature-implementation` instead. For investigating existing features (READ-ONLY), use `feature-investigation`.

# Feature Implementation Workflow

**IMPORTANT**: Always think hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

**Prerequisites:** **⚠️ MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

---

## Core Principles

- INVESTIGATE before implementing
- Follow established patterns in existing code
- Use External Memory for complex features
- Request user approval at checkpoint gates
- Never assume - verify with code evidence

## Phase 1: Discovery & Analysis

### Step 1.1: Requirement Decomposition

```markdown
## Feature Analysis

- **Feature Name**: [Name]
- **Business Objective**: [What problem does this solve?]
- **Affected Services**: [ServiceB, ServiceA, etc.]
- **Scope**: [New entity? New command? UI change?]
```

### Step 1.2: Codebase Investigation

```bash
# Find related entities
grep -r "class.*{RelatedConcept}" --include="*.cs" services directory/

# Find existing patterns
grep -r "{SimilarFeature}Command" --include="*.cs"

# Check domain boundaries
grep -r "namespace.*{ServiceName}\.Domain" --include="*.cs"

# Find API endpoints
grep -r "\[Route.*{feature}\]" --include="*.cs"
```

### Step 1.3: Pattern Recognition

- [ ] Find similar features in codebase
- [ ] Identify which patterns apply (CQRS, Event-driven, etc.)
- [ ] Check for reusable components
- [ ] Map dependencies

## Phase 2: Knowledge Graph Construction

### Backend Impact Analysis

```markdown
## Backend Changes Required

### Domain Layer

- [ ] New Entity: `{EntityName}.cs`
- [ ] Entity Expressions: Static query expressions
- [ ] Value Objects: `{ValueObject}.cs`

### Application Layer

- [ ] Commands: `Save{Entity}Command.cs`
- [ ] Queries: `Get{Entity}ListQuery.cs`
- [ ] Event Handlers: `{Action}On{Event}EntityEventHandler.cs`
- [ ] DTOs: `{Entity}Dto.cs`

### Persistence Layer

- [ ] Entity Configuration: `{Entity}EntityConfiguration.cs`
- [ ] Migrations: Add/Update schema

### API Layer

- [ ] Controller: `{Entity}Controller.cs`
- [ ] Endpoints: POST/GET/PUT/DELETE
```

### Frontend Impact Analysis

```markdown
## Frontend Changes Required

### Components

- [ ] List Component: `{entity}-list.component.ts`
- [ ] Form Component: `{entity}-form.component.ts`
- [ ] Detail Component: `{entity}-detail.component.ts`

### State Management

- [ ] Store: `{entity}.store.ts`
- [ ] State Interface: `{Entity}State`

### Services

- [ ] API Service: `{entity}-api.service.ts`

### Routing

- [ ] Route definitions
- [ ] Guards if needed
```

## Phase 3: Implementation Plan

### Create External Memory File

```markdown
# File: .ai/workspace/analysis/{feature-name}-implementation.md

## Feature: {Feature Name}

## Status: Planning

## Implementation Order

1. Domain Layer (Entity, Expressions)
2. Persistence Layer (Configuration, Migration)
3. Application Layer (Commands, Queries, DTOs)
4. API Layer (Controller)
5. Frontend (Store, Components, Routing)

## Checklist

- [ ] Step 1: Create Entity
- [ ] Step 2: Create Entity Configuration
- [ ] Step 3: Generate Migration
- [ ] Step 4: Create DTO
- [ ] Step 5: Create Save Command
- [ ] Step 6: Create List Query
- [ ] Step 7: Create Controller
- [ ] Step 8: Create Frontend Store
- [ ] Step 9: Create Frontend Components
- [ ] Step 10: Add Routing
- [ ] Step 11: Test Integration

## Evidence Log

[Track all decisions and findings here]
```

## Phase 4: Approval Gate

**CHECKPOINT**: Present plan to user before implementation

```markdown
## Implementation Proposal

### Summary

[Brief description of what will be implemented]

### Files to Create

1. `{path/to/file1.cs}` - Entity definition
2. `{path/to/file2.cs}` - Command handler
3. ...

### Files to Modify

1. `{path/to/existing.cs}` - Add new method
2. ...

### Risks & Considerations

- [Risk 1]
- [Risk 2]

### Questions for Clarification

- [Question 1]?
- [Question 2]?

**Ready to proceed?**
```

## Phase 5: Implementation

### Backend Implementation Order

1. **Domain Layer First**

```csharp
// 1. Create Entity
public sealed class Feature : RootEntity<Feature, string>
{
    public string Name { get; set; } = "";
    // ... properties, expressions, validation
}
```

2. **Persistence Layer**

```csharp
// 2. Entity Configuration
public class FeatureEntityConfiguration : IEntityTypeConfiguration<Feature>
{
    public void Configure(EntityTypeBuilder<Feature> builder)
    {
        builder.ToTable("Features");
        builder.HasKey(x => x.Id);
        // ...
    }
}

// 3. Generate Migration
// dotnet ef migrations add AddFeature
```

3. **Application Layer**

```csharp
// 4. DTO (in EntityDtos/ folder)
public class FeatureDto : PlatformEntityDto<Feature, string> { }

// 5. Command (Command + Handler + Result in ONE file)
public sealed class SaveFeatureCommand : PlatformCqrsCommand<SaveFeatureCommandResult> { }

// 6. Query
public sealed class GetFeatureListQuery : PlatformCqrsPagedQuery<GetFeatureListQueryResult, FeatureDto> { }
```

4. **API Layer**

```csharp
// 7. Controller
[ApiController]
[Route("api/[controller]")]
public class FeatureController : PlatformBaseController
{
    [HttpPost]
    public async Task<IActionResult> Save([FromBody] SaveFeatureCommand cmd)
        => Ok(await Cqrs.SendAsync(cmd));
}
```

### Frontend Implementation Order

1. **API Service**

```typescript
@Injectable({ providedIn: 'root' })
export class FeatureApiService extends PlatformApiService {
    protected get apiUrl() {
        return environment.apiUrl + '/api/Feature';
    }
}
```

2. **Store**

```typescript
@Injectable()
export class FeatureStore extends project store base (search for: store base class)<FeatureState> {
    // State management
}
```

3. **Components**

```typescript
@Component({ selector: 'app-feature-list' })
export class FeatureListComponent extends project store component base (search for: store component base class)<FeatureState, FeatureStore> {}
```

## Phase 6: Verification

### Backend Verification

- [ ] Entity compiles without errors
- [ ] Migration applies successfully
- [ ] Command handler saves entity correctly
- [ ] Query returns expected data
- [ ] API endpoint responds correctly

### Frontend Verification

- [ ] Store loads data correctly
- [ ] Component renders without errors
- [ ] Form validation works
- [ ] CRUD operations complete

### Integration Verification

- [ ] End-to-end flow works
- [ ] Error handling works
- [ ] Authorization applied correctly

## Anti-Patterns to AVOID

:x: **Starting implementation without investigation**

```
# WRONG: Jump straight to coding
```

:x: **Implementing multiple layers simultaneously**

```
# WRONG: Creating entity, command, and controller at once
```

:x: **Skipping the approval gate**

```
# WRONG: Implementing large features without user confirmation
```

:x: **Not following existing patterns**

```csharp
// WRONG: Creating custom patterns when platform patterns exist
```

## Verification Checklist

- [ ] Discovery phase completed with evidence
- [ ] Knowledge graph documented
- [ ] Implementation plan approved by user
- [ ] Backend layers implemented in order
- [ ] Frontend layers implemented in order
- [ ] Integration tested
- [ ] External memory file updated with progress

---

## See Also

- `feature-implementation` skill - Interactive variant with user feedback
- `feature-investigation` skill - READ-ONLY exploration (no code changes)
- `debug` skill - Autonomous debugging workflow
- `.ai/docs/AI-DEBUGGING-PROTOCOL.md` - Debugging protocol
- `.ai/docs/prompt-context.md` - Platform patterns and context
- `CLAUDE.md` - Codebase instructions

## Related

- `feature-implementation`
- `tasks-code-review`
- `tasks-test-generation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
