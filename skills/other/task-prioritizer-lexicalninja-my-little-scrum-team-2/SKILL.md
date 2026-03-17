---
name: task-prioritizer
description: Prioritizes tasks based on dependencies, business value, resource availability, and project goals. Use when you need to determine task execution order or prioritize work. Considers dependencies, value, urgency, and resource constraints.
---

# Task Prioritizer Skill

## Instructions

1. Review all tasks and their characteristics
2. Identify task dependencies
3. Assess business value and urgency
4. Consider resource availability
5. Apply prioritization criteria
6. Rank tasks by priority
7. Create prioritized task list

## Prioritization Process

### Step 1: Analyze Tasks
- Review all tasks
- Understand task requirements
- Identify task types
- Note task complexity

### Step 2: Identify Dependencies
- Map task dependencies
- Identify critical path
- Note blocking tasks
- Identify parallel opportunities

### Step 3: Assess Value
- Determine business value
- Assess user impact
- Consider strategic importance
- Note urgency

### Step 4: Consider Resources
- Check resource availability
- Consider agent capacity
- Note resource constraints
- Plan resource allocation

### Step 5: Apply Prioritization
- Apply prioritization criteria
- Rank tasks
- Create priority groups
- Plan execution order

## Prioritization Criteria

### Dependency-Based Priority
- **Blocking Tasks**: Tasks that block others (High priority)
- **Dependent Tasks**: Tasks that depend on others (After dependencies)
- **Independent Tasks**: Can run in parallel (Flexible priority)

### Value-Based Priority
- **High Value**: Critical features, user-facing, revenue-impacting
- **Medium Value**: Important features, nice-to-have
- **Low Value**: Nice-to-have, polish, optimization

### Urgency-Based Priority
- **Critical**: Must be done immediately
- **High**: Should be done soon
- **Medium**: Can be done in normal course
- **Low**: Can be deferred

### Risk-Based Priority
- **High Risk**: Complex, uncertain, high impact if fails
- **Medium Risk**: Moderate complexity and impact
- **Low Risk**: Simple, well-understood

## Priority Levels

### P0 - Critical
- Blocks other work
- Critical path items
- Must be done first
- High business value
- High urgency

### P1 - High
- Important features
- High business value
- Should be done soon
- May block some work

### P2 - Medium
- Standard features
- Medium business value
- Normal priority
- Can be done in normal course

### P3 - Low
- Nice-to-have features
- Low business value
- Can be deferred
- Optimization and polish

## Prioritization Output Format

```markdown
## Task Prioritization

### Priority Groups

#### P0 - Critical (Do First)
- TASK-001: [description] - [rationale]
- TASK-002: [description] - [rationale]

#### P1 - High (Do Soon)
- TASK-003: [description] - [rationale]
- TASK-004: [description] - [rationale]

#### P2 - Medium (Normal Priority)
- TASK-005: [description] - [rationale]

#### P3 - Low (Can Defer)
- TASK-006: [description] - [rationale]

### Execution Order
1. [Phase]: [tasks]
2. [Phase]: [tasks]

### Critical Path
[Tasks that must be done sequentially]

### Parallel Opportunities
[Tasks that can run in parallel]

### Rationale
[Overall prioritization rationale]
```

## Examples

### Example 1: Dependency-Based Prioritization

**Input**: Prioritize tasks with dependencies

**Output**:
```markdown
## Task Prioritization

### Priority Groups

#### P0 - Critical (Do First)
- TASK-001: Create specification - Blocks all other work
- TASK-002: Set up database schema - Blocks implementation tasks
- TASK-003: Break specification into tasks - Required before design/implementation

#### P1 - High (Do Soon)
- TASK-004: Design user interface - Blocks frontend implementation
- TASK-005: Design API structure - Blocks backend implementation

#### P2 - Medium (Normal Priority)
- TASK-006: Implement backend API - Depends on TASK-005
- TASK-007: Implement frontend - Depends on TASK-004

#### P3 - Low (Can Defer)
- TASK-008: Add documentation - Can be done after implementation
- TASK-009: Performance optimization - Can be deferred

### Execution Order
1. **Phase 1 (Sequential)**:
   - TASK-001: Create specification
   - TASK-003: Break into tasks
   - TASK-002: Set up database

2. **Phase 2 (Parallel)**:
   - TASK-004: Design UI
   - TASK-005: Design API

3. **Phase 3 (Parallel)**:
   - TASK-006: Implement backend
   - TASK-007: Implement frontend

4. **Phase 4**:
   - TASK-008: Documentation
   - TASK-009: Optimization

### Critical Path
TASK-001 → TASK-003 → TASK-002 → TASK-005 → TASK-006

### Parallel Opportunities
- Phase 2: TASK-004 and TASK-005 can run in parallel
- Phase 3: TASK-006 and TASK-007 can run in parallel

### Rationale
Prioritization is primarily dependency-based. Foundation tasks (specification, database) must come first. Design tasks can run in parallel, then implementation. Documentation and optimization can be deferred.
```

### Example 2: Value-Based Prioritization

**Input**: Prioritize tasks by business value

**Output**:
```markdown
## Task Prioritization

### Priority Groups

#### P0 - Critical (Do First)
- TASK-001: User authentication - Critical for security and user access
- TASK-002: Core feature implementation - Primary business value

#### P1 - High (Do Soon)
- TASK-003: User dashboard - High user value
- TASK-004: Payment integration - Revenue impact

#### P2 - Medium (Normal Priority)
- TASK-005: User profile page - Standard feature
- TASK-006: Email notifications - Important but not critical

#### P3 - Low (Can Defer)
- TASK-007: UI polish - Nice-to-have
- TASK-008: Advanced search - Can be added later

### Execution Order
1. **Phase 1**: Core functionality
   - TASK-001: Authentication
   - TASK-002: Core feature

2. **Phase 2**: High-value features
   - TASK-003: Dashboard
   - TASK-004: Payments

3. **Phase 3**: Standard features
   - TASK-005: Profile
   - TASK-006: Notifications

4. **Phase 4**: Polish and enhancements
   - TASK-007: UI polish
   - TASK-008: Advanced search

### Critical Path
TASK-001 → TASK-002 → TASK-003

### Parallel Opportunities
- TASK-005 and TASK-006 can run in parallel
- TASK-007 and TASK-008 can run in parallel

### Rationale
Prioritization is value-based. Critical security and core features come first, followed by high-value user features. Standard features and polish can be done later.
```

## Prioritization Strategies

### Strategy 1: Dependency-First
- Prioritize tasks that block others
- Complete dependencies before dependents
- Enable parallel execution when possible

### Strategy 2: Value-First
- Prioritize high-value tasks
- Focus on user impact
- Consider business goals

### Strategy 3: Risk-First
- Address high-risk tasks early
- Reduce uncertainty
- Validate assumptions

### Strategy 4: Hybrid
- Combine multiple criteria
- Balance dependencies, value, and risk
- Optimize for project goals

## Best Practices

- **Respect Dependencies**: Never prioritize dependent tasks before dependencies
- **Consider Value**: Prioritize high-value work
- **Enable Parallelism**: Identify tasks that can run in parallel
- **Balance Priorities**: Consider multiple factors, not just one
- **Be Flexible**: Adjust priorities as project evolves
- **Document Rationale**: Explain why tasks are prioritized
