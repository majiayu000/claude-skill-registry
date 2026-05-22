---
name: tasks-feature-implementation
description: Use when implementing new features or enhancements requiring multi-layer changes (Domain, Application, Persistence, API, Frontend).
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **autonomous feature implementation** with structured workflows. For interactive feature development with user feedback, use `feature-implementation` instead. For investigating existing features (READ-ONLY), use `feature-investigation`.

# Feature Implementation Workflow

**IMPORTANT**: Always think hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT

Before every major operation:

1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION

Before claiming any relationship:

- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

### CONTEXT_ANCHOR_SYSTEM

Every 10 operations:

1. Re-read the original task from `## Metadata`
2. Verify current operation aligns with goals
3. Update `Current Focus` in `## Progress`

---

## Quick Reference Checklist

Before any major operation:

- [ ] ASSUMPTION_VALIDATION_CHECKPOINT
- [ ] EVIDENCE_CHAIN_VALIDATION

Every 10 operations:

- [ ] CONTEXT_ANCHOR_CHECK
- [ ] Update 'Current Focus' in `## Progress`

Emergency:

- **Context Drift** → Re-read `## Metadata`
- **Assumption Creep** → Halt, validate with code
- **Evidence Gap** → Mark as "inferred"

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
- **Affected Services**: [TextSnippet, TextSnippet, etc.]
- **Scope**: [New entity? New command? UI change?]
```

### Step 1.2: Codebase Investigation

```bash
# Find related entities
grep -r "class.*{RelatedConcept}" --include="*.cs" src/PlatformExampleApp/

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
export class FeatureStore extends PlatformVmStore<FeatureState> {
    // State management
}
```

3. **Components**

```typescript
@Component({ selector: 'app-feature-list' })
export class FeatureListComponent extends AppBaseVmStoreComponent<FeatureState, FeatureStore> {}
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
- `debugging --autonomous` - Autonomous debugging workflow
- `.github/AI-DEBUGGING-PROTOCOL.md` - Debugging protocol
- `.ai/prompts/context.md` - Platform patterns and context
- `CLAUDE.md` - Codebase instructions

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
