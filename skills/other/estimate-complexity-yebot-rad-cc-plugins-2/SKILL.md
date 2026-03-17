---
description: Estimate implementation complexity for features and technical tasks
disable-model-invocation: false
---

# Estimate Complexity

Provide structured complexity estimates for features and tasks to help with planning and prioritization.

## When to Use

- During sprint planning
- When scoping new features
- Before committing to timelines
- When breaking down large initiatives

## Used By

- Full-Stack Engineer
- Frontend Engineer
- Backend Engineer
- DevOps Engineer

---

## Complexity Estimation Framework

### T-Shirt Sizes

| Size | Description | Typical Scope |
|------|-------------|---------------|
| **XS** | Trivial change | Config change, copy update, minor fix |
| **S** | Small, well-understood | Single component, simple API endpoint |
| **M** | Moderate complexity | Multiple components, some unknowns |
| **L** | Significant effort | Cross-cutting changes, new patterns |
| **XL** | Major initiative | New system, architectural changes |

---

## Estimation Template

```markdown
## Complexity Estimate: [Feature/Task Name]

### Summary
**T-Shirt Size**: [XS / S / M / L / XL]
**Confidence**: [High / Medium / Low]

### Breakdown

| Component | Effort | Notes |
|-----------|--------|-------|
| [Component 1] | [XS-XL] | [Details] |
| [Component 2] | [XS-XL] | [Details] |
| [Component 3] | [XS-XL] | [Details] |

### Key Complexity Drivers

1. **[Driver 1]**: [Why this adds complexity]
2. **[Driver 2]**: [Why this adds complexity]
3. **[Driver 3]**: [Why this adds complexity]

### Risk Factors

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [H/M/L] | [Strategy] |
| [Risk 2] | [H/M/L] | [Strategy] |

### Unknowns

- [ ] [Unknown 1] - Could affect estimate by [amount]
- [ ] [Unknown 2] - Need to spike/investigate

### Suggested Breakdown

If size is L or XL, break into smaller deliverables:

1. **Phase 1**: [Scope] - Size: [S/M]
2. **Phase 2**: [Scope] - Size: [S/M]
3. **Phase 3**: [Scope] - Size: [S/M]

### Dependencies

- Blocked by: [Dependency]
- Blocks: [Other work]

### Recommendations

[Any suggestions for approach, sequencing, or risk reduction]
```

---

## Complexity Indicators

### Factors That Increase Complexity

**Technical**
- New technology or pattern not used before
- Integration with external systems
- Performance-critical requirements
- Complex state management
- Database migrations on large tables
- Security-sensitive functionality

**Organizational**
- Cross-team coordination required
- Unclear or changing requirements
- Multiple stakeholder approval needed
- Compliance or legal review required

**Code Quality**
- Working in unfamiliar codebase area
- Technical debt in affected areas
- Missing test coverage
- Poor documentation

### Factors That Decrease Complexity

- Similar work done before (pattern exists)
- Well-defined requirements
- Strong test coverage
- Clear ownership and decision-making
- Good documentation
- Modern, maintained dependencies

---

## Confidence Levels

### High Confidence
- Similar work completed before
- All requirements are clear
- Technology is well-understood
- No significant unknowns

### Medium Confidence
- Some new elements but core is understood
- Requirements are mostly clear
- Some unknowns that are bounded

### Low Confidence
- New technology or pattern
- Requirements are still evolving
- Significant unknowns exist
- External dependencies unclear

**When confidence is low**: Consider a spike/investigation before committing to estimate.

---

## Breaking Down Large Tasks

If the estimate is L or XL, it should be broken down. Use these strategies:

### 1. Vertical Slicing
Break by user-facing functionality:
- Slice 1: Minimal viable flow
- Slice 2: Add edge cases
- Slice 3: Polish and optimization

### 2. Horizontal Slicing
Break by technical layer:
- Phase 1: Data model and API
- Phase 2: Frontend implementation
- Phase 3: Integration and testing

### 3. Risk-First Slicing
Address unknowns first:
- Phase 1: Spike on risky parts
- Phase 2: Core implementation
- Phase 3: Polish and edge cases

---

## Estimation Anti-Patterns

### Don't Do This

1. **Pressure-driven estimates**: Fitting estimate to desired timeline
2. **Best-case thinking**: Assuming everything goes perfectly
3. **Ignoring testing**: Development isn't done until it's tested
4. **Forgetting integration**: Time for connecting pieces
5. **Missing review cycles**: Code review, design review, etc.

### Do This Instead

1. **Add buffer**: Include time for unknowns and interruptions
2. **Include all work**: Testing, documentation, review, deployment
3. **Communicate uncertainty**: Be honest about confidence level
4. **Update as you learn**: Revise estimates when new info emerges
5. **Track actuals**: Compare estimates to actual to improve

---

## Quick Estimation Checklist

Before providing an estimate, consider:

### Scope
- [ ] Are requirements clear and complete?
- [ ] Is scope explicitly bounded?
- [ ] Are acceptance criteria defined?

### Technical
- [ ] Have you worked in this area before?
- [ ] Are there existing patterns to follow?
- [ ] Are dependencies understood?
- [ ] Is the data model clear?

### Testing
- [ ] What testing is required?
- [ ] Is there existing test coverage?
- [ ] Are there test data needs?

### Deployment
- [ ] Any database migrations?
- [ ] Feature flag needed?
- [ ] Configuration changes?
- [ ] Documentation updates?

### Coordination
- [ ] Other teams involved?
- [ ] Review cycles needed?
- [ ] Stakeholder approval required?

---

## Example Estimates

### XS Example: Copy Update
```
Task: Update error message text
Size: XS
Confidence: High
Breakdown:
- Edit: 10 min
- Test: 10 min
- Deploy: Automatic
```

### S Example: New API Endpoint
```
Task: Add endpoint to fetch user preferences
Size: S
Confidence: High
Breakdown:
- API implementation: 2 hours
- Tests: 1 hour
- Documentation: 30 min
```

### M Example: New Feature Component
```
Task: Add notification preferences UI
Size: M
Confidence: Medium
Breakdown:
- Component design: 2 hours
- State management: 2 hours
- API integration: 2 hours
- Testing: 3 hours
- Accessibility: 2 hours
```

### L Example: New Subsystem
```
Task: Implement real-time notifications
Size: L
Confidence: Medium
Key Drivers:
- WebSocket infrastructure needed
- Multiple notification types
- Delivery guarantees
- UI notifications component

Suggested Breakdown:
1. WebSocket infrastructure (M)
2. Backend notification service (M)
3. Frontend notification component (S)
4. Integration and testing (S)
```
