---
name: tasks-feature-implementation
version: 1.0.1
description: Autonomous subagent variant of feature-implementation. Use when implementing new features or enhancements requiring multi-layer changes (Domain, Application, Persistence, API, Frontend).
infer: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **autonomous feature implementation** with structured workflows. For interactive feature development with user feedback, use `feature-implementation` instead. For investigating existing features (READ-ONLY), use `feature-investigation`.

# Feature Implementation Workflow

**IMPORTANT**: Always think hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

**Prerequisites:** **MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` before executing.

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
- **Affected Services**: [Which microservices are impacted?]
- **Scope**: [New entity? New command? UI change?]
```

### Step 1.2: Codebase Investigation

```bash
# Find related entities
grep -r "class.*{RelatedConcept}" --include="*.cs" src/

# Find existing patterns
grep -r "{SimilarFeature}Command" --include="*.cs"

# Check domain boundaries
grep -r "namespace.*{ServiceName}\.Domain" --include="*.cs"
```

### Step 1.3: Pattern Recognition

- [ ] Find similar features in codebase
- [ ] Identify which patterns apply (CQRS, Event-driven, etc.)
- [ ] Check for reusable components
- [ ] Map dependencies

## Phase 2: Impact Analysis

### Backend Impact

```markdown
### Domain Layer
- [ ] New Entity: `{EntityName}.cs`
- [ ] Entity Expressions: Static query expressions

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
```

### Frontend Impact

```markdown
### Components
- [ ] List Component: `{entity}-list.component.ts`
- [ ] Form Component: `{entity}-form.component.ts`

### State Management
- [ ] Store: `{entity}.store.ts`

### Services
- [ ] API Service: `{entity}-api.service.ts`
```

## Phase 3: Approval Gate

**CHECKPOINT**: Present plan to user before implementation.

## Phase 4: Implementation

### Backend Implementation Order

1. **Domain Layer First** — Entity, expressions, validation
2. **Persistence Layer** — Configuration, migration
3. **Application Layer** — Commands, queries, DTOs
4. **API Layer** — Controller, endpoints

### Frontend Implementation Order

1. **API Service** — Extend `PlatformApiService`
2. **Store** — Extend `PlatformVmStore`
3. **Components** — Extend `AppBaseComponent` / `AppBaseVmStoreComponent`

## Phase 5: Verification

- [ ] Entity compiles without errors
- [ ] Command handler saves entity correctly
- [ ] Query returns expected data
- [ ] API endpoint responds correctly
- [ ] Frontend loads data and renders
- [ ] Error handling works
- [ ] Authorization applied correctly

## Anti-Patterns to AVOID

- Starting implementation without investigation
- Implementing multiple layers simultaneously
- Skipping the approval gate
- Not following existing patterns

## Related

- `feature-implementation`
- `tasks-code-review`
- `tasks-test-generation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
