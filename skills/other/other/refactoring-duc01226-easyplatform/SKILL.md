---
name: refactoring
version: 2.1.0
description: '[Code Quality] Restructure code without changing behavior using extract method, extract class, rename, move, and inline patterns. Triggers: refactor, extract method, extract class, rename symbol, restructure code, clean up code, decompose function.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

## Quick Summary

**Goal:** Restructure code without changing behavior using extract, move, and simplify patterns.

**Workflow:**

1. **Analysis** — Identify target, map dependencies with Grep, assess impact, verify test coverage
2. **Plan** — Document refactoring type, changes, and risks
3. **Execute** — Apply refactoring (extract method/class, move to entity/extension, simplify conditionals)
4. **Verify** — Run tests, confirm no behavior change, check compilation

**Key Rules:**

- Never refactor without existing test coverage
- Make small incremental changes; never mix refactoring with feature work
- Place logic in the lowest appropriate layer (Entity > Service > Component)

## Investigation Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

- Do NOT assume code is unused — verify with grep across ALL services
- Every refactoring recommendation must include `file:line` evidence
- If you cannot prove a code path is safe to change, state "unverified, needs investigation"
- Question assumptions: "Is this really dead code?" → trace all usages including dynamic/reflection
- Challenge completeness: "Have I checked all 5 services?" → cross-service validation required
- No "should be refactored" without proof — demonstrate the improvement with evidence

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.
**95%+** recommend freely | **80-94%** with caveats | **60-79%** list unknowns | **<60% STOP — gather more evidence.**
Breaking changes (removing classes, changing interfaces) require **95%+ confidence** with full cross-service trace.

# Code Refactoring

Expert code restructuring agent. Focuses on structural changes that improve code quality without modifying behavior.

## Refactoring Catalog

### Extract Patterns

| Pattern                | When to Use                         | Platform Example                          |
| ---------------------- | ----------------------------------- | ----------------------------------------- |
| **Extract Method**     | Long method, duplicated code        | Move logic to private method              |
| **Extract Class**      | Class has multiple responsibilities | Create Helper, Service, or Strategy class |
| **Extract Interface**  | Need abstraction for testing/DI     | Create `I{ClassName}` interface           |
| **Extract Expression** | Complex inline expression           | Move to Entity static expression          |
| **Extract Validator**  | Repeated validation logic           | Create validator extension method         |

### Move Patterns

| Pattern               | When to Use                       | Platform Example                         |
| --------------------- | --------------------------------- | ---------------------------------------- |
| **Move Method**       | Method belongs to different class | Move from Handler to Helper/Entity       |
| **Move to Extension** | Reusable repository logic         | Create `{Entity}RepositoryExtensions`    |
| **Move to DTO**       | Mapping logic in handler          | Use `PlatformEntityDto.MapToEntity()`    |
| **Move to Entity**    | Business logic in handler         | Add instance method or static expression |

### Simplify Patterns

| Pattern                     | When to Use                  | Platform Example                   |
| --------------------------- | ---------------------------- | ---------------------------------- |
| **Inline Variable**         | Temporary variable used once | Remove intermediate variable       |
| **Inline Method**           | Method body is obvious       | Replace call with body             |
| **Replace Conditional**     | Complex if/switch            | Use Strategy pattern or expression |
| **Introduce Parameter Obj** | Method has many parameters   | Create Command/Query DTO           |

## Workflow

### Phase 1: Analysis

1. **Identify Target**: Locate code to refactor
2. **Map Dependencies**: Find all usages with Grep
3. **Assess Impact**: List affected files and tests
4. **Verify Tests**: Ensure test coverage exists
5. **External Memory**: Write analysis to `.ai/workspace/analysis/{refactoring-name}.analysis.md`. Re-read before planning.

### Phase 2: Plan

Document refactoring plan:

```markdown
## Refactoring Plan

**Target**: [file:line_number]
**Type**: [Extract Method | Move to Extension | etc.]
**Reason**: [Why this refactoring improves code]

### Changes

1. [ ] Create/modify [file]
2. [ ] Update usages in [files]
3. [ ] Run tests

### Risks

- [Potential issues]
```

### Phase 3: Execute

```csharp
// BEFORE: Logic in handler
protected override async Task<Result> HandleAsync(Command req, CancellationToken ct)
{
    var isValid = entity.Status == Status.Active &&
                  entity.User?.IsActive == true &&
                  !entity.IsDeleted;
    if (!isValid) throw new Exception();
}

// AFTER: Extracted to entity static expression
// In Entity.cs
public static Expression<Func<Entity, bool>> IsActiveExpr()
    => e => e.Status == Status.Active &&
            e.User != null && e.User.IsActive &&
            !e.IsDeleted;

// In Handler
var entity = await repository.FirstOrDefaultAsync(Entity.IsActiveExpr(), ct)
    .EnsureFound("Entity not active");
```

### Phase 4: Verify

1. Run affected tests
2. Verify no behavior change
3. Check code compiles
4. Review for consistency

## Platform-Specific Refactorings

### Handler to Helper

```csharp
// BEFORE: Reused logic in multiple handlers
var employee = await repo.FirstOrDefaultAsync(Employee.UniqueExpr(userId, companyId), ct)
    ?? await CreateEmployeeAsync(userId, companyId, ct);

// AFTER: Extracted to Helper
// In EmployeeHelper.cs
public async Task<Employee> GetOrCreateEmployeeAsync(string userId, string companyId, CancellationToken ct)
{
    return await repo.FirstOrDefaultAsync(Employee.UniqueExpr(userId, companyId), ct)
        ?? await CreateEmployeeAsync(userId, companyId, ct);
}
```

### Handler to Repository Extension

```csharp
// BEFORE: Query logic in handler
var employees = await repo.GetAllAsync(
    e => e.CompanyId == companyId && e.Status == Status.Active && e.DepartmentIds.Contains(deptId), ct);

// AFTER: Extracted to extension
// In EmployeeRepositoryExtensions.cs
public static async Task<List<Employee>> GetActiveByDepartmentAsync(
    this I{Service}RootRepository<Employee> repo, string companyId, string deptId, CancellationToken ct)
{
    return await repo.GetAllAsync(
        Employee.OfCompanyExpr(companyId)
            .AndAlso(Employee.IsActiveExpr())
            .AndAlso(e => e.DepartmentIds.Contains(deptId)), ct);
}
```

### Mapping to DTO

```csharp
// BEFORE: Mapping in handler
var config = new AuthConfig
{
    ClientId = req.Dto.ClientId,
    Secret = encryptService.Encrypt(req.Dto.Secret)
};

// AFTER: DTO owns mapping
// In AuthConfigDto.cs : PlatformDto<AuthConfig>
public override AuthConfig MapToObject() => new AuthConfig
{
    ClientId = ClientId,
    Secret = Secret  // Handler applies encryption
};

// In Handler
var config = req.Dto.MapToObject()
    .With(c => c.Secret = encryptService.Encrypt(c.Secret));
```

## Index Impact Check

When extracting expressions or moving queries, verify index coverage:

- [ ] New expression fields have indexes in DbContext?
- [ ] Moved queries still use indexed fields?
- [ ] Refactored filters maintain index selectivity order?

## Safety Checklist

Before any refactoring:

- [ ] Searched all usages across ALL services (static + dynamic + reflection)?
- [ ] Test coverage exists?
- [ ] Documented in todo list?
- [ ] Changes are incremental?
- [ ] No behavior change verified?
- [ ] **Confidence declared** — `Confidence: X%` with evidence list?

**If ANY checklist item incomplete → STOP. State "Insufficient evidence to proceed."**

## Code Responsibility Refactoring (Priority Check)

**⚠️ MUST READ:** CLAUDE.md "Code Responsibility Hierarchy" for the Entity/Model > Service > Component layering rule. When refactoring, verify logic is in the LOWEST appropriate layer.

## Component HTML & SCSS Standards

**⚠️ MUST READ:** CLAUDE.md "Component HTML Template Standard (BEM Classes)" and `docs/claude/scss-styling-guide.md` for BEM class requirements and host/wrapper styling patterns. When refactoring components, ensure all HTML elements have proper BEM classes.

## Anti-Patterns

- **Big Bang Refactoring**: Make small, incremental changes
- **Refactoring Without Tests**: Ensure coverage first
- **Mixing Refactoring with Features**: Do one or the other
- **Breaking Public APIs**: Maintain backward compatibility
- **Logic in Wrong Layer**: Leads to duplicated code - move to lowest appropriate layer

## Related

- `code-simplifier`
- `code-review`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
