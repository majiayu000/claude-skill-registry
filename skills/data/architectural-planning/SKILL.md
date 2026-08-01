---
name: architectural-planning
description: Create detailed technical plans and implementation roadmaps by analyzing
  project architecture and designing solutions that integrate seamlessly with existing
  patterns. Use when designing features, pla
---

---
name: architectural-planning
description: Create detailed technical plans and implementation roadmaps by analyzing project architecture and designing solutions that integrate seamlessly with existing patterns. Use when designing features, planning integrations, making architectural decisions. Triggers: 'plan', 'design', 'architecture', 'approach', 'how should I', 'best way', 'integrate', '계획', '설계', '아키텍처', '접근법', '어떻게 해야', '가장 좋은 방법', '통합', '마이그레이션', working with multi-module features, system boundaries, complex migrations.
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__sequential-thinking__sequentialthinking
  - mcp__memory__*
---

# Architectural Planning Methodology

This skill enables creating comprehensive technical plans for features and changes by discovering and following project architectural patterns.

**Leverages:** [codebase-analysis] skill for project discovery and pattern recognition.

## Planning Philosophy

### Integration Over Innovation
- Design solutions that fit naturally into existing architecture
- Respect established boundaries and responsibilities
- Follow discovered organizational patterns
- Use existing libraries and approaches

### Clarity and Actionability
- Create plans others can execute without clarification
- Break work into atomic, testable steps
- Identify dependencies and risks explicitly
- Provide clear success criteria

## Planning Workflow

### Phase 1: Architectural Discovery
Using [codebase-analysis] methodology:
1. Understand overall architecture (layered, microservices, modular, etc.)
2. Identify existing components and their responsibilities
3. Map dependencies and integration points
4. Learn architectural boundaries and conventions
5. Find similar features as reference examples

### Phase 1.5: Deep Reasoning (If Complex)

After architectural discovery, evaluate if systematic thinking is needed for complex decisions.

**Quick assessment**:
- 3+ approaches AND 5+ dimensions AND unclear path → **Sequential Thinking**
- Otherwise → **Direct analysis, proceed to Phase 2**

**After decision**: Consider using **Memory MCP** to record architectural decisions and rationale for future reference.

**Detailed guidance**: See `../shared/mcp-decision-guide.md` for:
- Sequential Thinking decision criteria and usage
- Memory MCP usage patterns
- Decision flow examples

### Phase 2: Solution Design
Design within discovered constraints:
1. Identify which existing components are affected
2. Determine if new components are needed
3. Choose integration points that match existing patterns
4. Plan data flows following project conventions
5. Design APIs consistent with current style

### Phase 3: Implementation Planning
Create actionable steps:
1. Order tasks by dependency and logical progression
2. Specify exact files to modify or create
3. Reference existing code as implementation examples
4. Identify potential conflicts or breaking changes
5. Plan validation and testing approach

## Plan Structure Guidelines

### Essential Elements

**Context Section**:
- Discovered architecture pattern
- Technology stack
- Similar existing features
- Integration points

**Approach Section**:
- High-level solution
- Why it fits the architecture
- New vs existing components
- Pattern references

**Implementation Section**:
- Atomic, ordered steps
- File paths (create/modify)
- Code examples from codebase
- Rationale for each step

**Risk Section**:
- Dependencies (internal/external)
- Potential issues and mitigations
- Breaking changes and migrations
- Performance impact

**Validation Section**:
- Testing strategy
- Success criteria
- Manual verification steps

## Planning Best Practices

### Reference Real Examples
```
✅ "Following the UserService pattern in services/user.service.ts,
   OrderService will inject repositories via constructor and
   use the same error handling approach."

❌ "Create OrderService using dependency injection."
```

### Be Specific About Locations
```
✅ "Create auth/middleware/jwt-validator.ts following the
   pattern from auth/middleware/session-validator.ts"

❌ "Add JWT validation middleware"
```

### Quantify When Possible
```
✅ "Affects 3 API endpoints and 2 background jobs.
   Estimated: 2-3 hours implementation + 1 hour testing."

❌ "This will take some time to implement."
```

### Identify Patterns, Not Just Tasks
```
✅ "Implement using the Command pattern like existing
   payment/commands/ProcessPayment.java uses"

❌ "Implement the feature"
```

## Common Architectural Patterns

### Layered Architecture
```
Plan should respect layers:
- API/Presentation → UseCase/Application → Infrastructure → Domain
- Dependencies flow inward
- Each layer uses only the layer below
```

### Microservices
```
Plan should consider:
- Service boundaries
- Inter-service communication patterns
- Data consistency approaches
- Shared libraries vs duplication
```

### Hexagonal/Clean Architecture
```
Plan should:
- Keep business logic in core
- Adapt external dependencies at boundaries
- Use dependency inversion
- Preserve testability
```

### Event-Driven
```
Plan should:
- Identify events to publish/consume
- Follow existing event schemas
- Use project's message infrastructure
- Consider eventual consistency
```

## Anti-Patterns to Avoid

❌ **Generic Plans**:
- "Add authentication" without specifying how it integrates

✅ **Context-Specific Plans**:
- "Extend existing OAuth2 middleware in auth/oauth2.go to support
  refresh tokens, following the pattern from auth/session.go"

❌ **Technology Mismatch**:
- Recommending GraphQL when project uses REST

✅ **Technology Alignment**:
- "Add REST endpoint to api/v1/orders.ts following OpenAPI
  spec pattern from api/v1/users.ts"

❌ **Ignoring Existing Solutions**:
- Creating new pagination when project has existing implementation

✅ **Leverage Existing**:
- "Use existing utils/pagination.ts helper, same as
  services/user-service.ts uses"

## Quality Checklist

Before finalizing plan:
- [ ] Have I identified the architectural pattern?
- [ ] Does the solution fit naturally into existing structure?
- [ ] Are all steps grounded in discovered conventions?
- [ ] Have I referenced specific existing code as examples?
- [ ] Are integration points clearly identified?
- [ ] Is each step atomic and testable?
- [ ] Have I considered risks and provided mitigations?
- [ ] Will someone unfamiliar with my thinking understand this plan?

## Plan Templates

For detailed templates and architecture-specific examples, see:
- **templates.md** - Full plan template and common scenarios

---

**Remember**: A great plan reads like it was written by someone deeply familiar with the codebase. Use the [codebase-analysis] skill to become that familiar before planning.
