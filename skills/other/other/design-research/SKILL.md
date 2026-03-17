---
name: design-research
description: >-
  Conduct research and create design documents before implementation.
  Use when analyzing requirements, exploring solutions, creating architecture
  designs, or investigating codebase patterns.
  Invoked by: "research", "design", "analyze", "investigate", "explore codebase".
context: fork
agent: Explore
---

# Research and Design Process SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
This process is the critical first phase before creating a design document. It ensures the user request is fully understood, the codebase is thoroughly analyzed, multiple solutions are considered, and the best approach is selected with solid foundation for design.

### When to Use
**ALWAYS**: New features, complex refactorings, architectural changes, breaking changes
**SKIP**: Simple bug fixes, trivial changes, explicit implementation instructions

---

## Process Workflow

### Flow Diagram
```
[User Request] --> [Request Understanding] --> [Repository Analysis]
                            |
                            v
              [Solution Exploration] --> [Recommendation & Decision]
                            |
                            v
                    [Design Document]
```

### Phase Summary
| Phase | Duration | Focus |
|-------|----------|-------|
| 1. Request Understanding | 10-20 min | Clarify requirements |
| 2. Repository Analysis | 20-40 min | Understand codebase |
| 3. Solution Exploration | 15-30 min | Generate alternatives |
| 4. Recommendation | 5-10 min | Document & approve |

**Total Duration**: 50-90 minutes

---

## Key Principles

1. **Conversation First** - Collaborative, not automated
2. **Deep Understanding** - Use comprehensive approach, read ALL relevant code
3. **Question Everything** - Challenge assumptions, ask clarifying questions
4. **Explore Alternatives** - Always present multiple approaches
5. **Align with Patterns** - Follow existing codebase conventions
6. **Document Findings** - Create clear, actionable research reports
7. **Platform Considerations** - Consider platform-specific differences when applicable

---

## Research Agent Responsibilities

### Must Do
- Act as consultant (advise and guide)
- Be thorough (read ALL code, no assumptions)
- Be conversational (engage, ask questions, discuss)
- Be critical (question if better approaches exist)
- Be comprehensive (consider all layers)
- Be pattern-aware (identify and follow existing patterns)
- Be honest (admit uncertainty, ask for help)
- Document everything (findings, conversations, decisions)
- Consider platform differences when applicable

### Must NOT Do
- Jump to implementation (no code changes during research)
- Make unilateral decisions (always collaborate)
- Skip analysis (every request deserves investigation)
- Ignore alternatives (always present multiple options)
- Assume understanding (ask clarifying questions)
- Violate architecture (respect established patterns)
- Ignore platform differences when applicable

---

## Phase 1: Request Understanding

**Objective**: Fully understand what user wants to achieve
**Duration**: 10-20 minutes

See [RESEARCH_GUIDE.md](RESEARCH_GUIDE.md) for detailed steps.

### Quick Checklist

- [ ] Read user request thoroughly
- [ ] Identify core objective
- [ ] Note constraints mentioned
- [ ] Flag ambiguous points
- [ ] Ask clarifying questions
- [ ] Define success criteria
- [ ] Get user confirmation

### Questions to Ask
- What is user trying to achieve?
- Is this new feature, bug fix, refactoring, or optimization?
- What is the scope? (UI? State management? Routing? API?)
- Are there explicit/implicit requirements?
- Are there platform-specific requirements?

---

## Phase 2: Repository Analysis

**Objective**: Deeply understand current codebase and architecture
**Duration**: 20-40 minutes

See [RESEARCH_GUIDE.md](RESEARCH_GUIDE.md) for detailed steps.

### Quick Checklist

- [ ] Use Glob/Grep to find relevant files
- [ ] Read all relevant files (components, screens, Redux, navigation, tests)
- [ ] Read project rules for guidelines
- [ ] Identify existing patterns
- [ ] Map dependencies and impacts
- [ ] Find similar implementations

### Search Patterns
```bash
# Find components
Glob: "src/components/**/*{name}*.*"

# Find pages/screens/views
Glob: "src/{pages,screens,views}/**/*{name}*.*"

# Find state management
Glob: "src/{store,state,redux}/**/*{name}*.*"

# Find routing/navigation
Glob: "src/{routes,navigation,router}/**/*.*"

# Find tests
Glob: "{__tests__,tests,spec}/**/*{feature}*.*"
```

---

## Phase 3: Solution Exploration

**Objective**: Generate and evaluate multiple solution approaches
**Duration**: 15-30 minutes

### Always Create At Least 3 Alternatives

```markdown
### Approach 1: Minimal Change (Simplest)
**Description**: Add feature with minimal refactoring
**Effort**: 1-2 days | **Risk**: Low
**Pros**: Quick, low risk, backward compatible
**Cons**: Doesn't address technical debt, may not be extensible

### Approach 2: Refactoring (Recommended)
**Description**: Add feature + refactor to improve architecture
**Effort**: 3-4 days | **Risk**: Medium
**Pros**: Improves code quality, follows best practices, extensible
**Cons**: More work upfront, touches more files

### Approach 3: Complete Redesign (Thorough)
**Description**: Redesign system entirely
**Effort**: 10-15 days | **Risk**: High
**Pros**: Solves underlying issues, future-proof
**Cons**: High effort and risk, many breaking changes
```

### Trade-off Analysis

For each approach, document:
1. **Alignment with Architecture** - Project patterns compliance?
2. **Complexity** - Implementation complexity, files affected, risk?
3. **Maintainability** - Easy to understand/extend, technical debt?
4. **Performance** - Performance implications?
5. **Testing** - How testable? Coverage needed?
6. **Migration** - Rollback strategy? Backward compatibility?
7. **Platform Compatibility** - Works across target platforms?

---

## Phase 4: Recommendation & Decision

**Objective**: Make final recommendation and get user approval
**Duration**: 5-10 minutes

### Present Final Recommendation

```markdown
## Final Recommendation

### Chosen Approach: [Approach Name]

### Summary
[2-3 sentence summary]

### Why This Approach
1. [Alignment with architecture]
2. [Balances effort/quality]
3. [Follows existing patterns]
4. [Platform compatibility]

### What Will Be Changed
- Types: [files]
- Redux: [files]
- Components: [files]
- Screens: [files]
- Navigation: [files]

### Estimated Effort
- Duration: X days
- Complexity: Low/Medium/High
- Risk: Low/Medium/High

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| {Risk} | {Strategy} |
```

### Get User Approval

```markdown
Does this approach look good to you?
- [ ] Yes, proceed to design document
- [ ] I have questions/concerns
- [ ] I prefer a different approach
```

---

## Output: Create Research Report

Once approved, create feature folder and research file:

1. **Create folder**: `/docs/ignored/<feature_name>/`
2. **Create subfolders**: `design/`, `development/`, `research/`
3. **Create research file**: `/docs/ignored/<feature_name>/research/<feature_name>_research.md`

Use template: [DESIGN_TEMPLATE.md](DESIGN_TEMPLATE.md)

---

## Quick Reference

### Decision Criteria

**Choose Minimal Approach When**:
- Timeline very tight (< 2 days)
- Low complexity
- Temporary solution acceptable

**Choose Refactoring Approach When**:
- Moderate timeline (2-5 days)
- Medium complexity
- Quality improvement opportunity
- Reasonable effort/benefit ratio

**Choose Redesign Approach When**:
- Ample timeline (> 1 week)
- High complexity
- Existing design fundamentally flawed
- Long-term benefits justify cost

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Requirements unclear | Ask clarifying questions before proceeding |
| Too many alternatives | Focus on top 3 most viable approaches |
| Can't find existing patterns | Search broader, check similar features |
| User wants to skip research | Explain risks, offer abbreviated process |
| Platform-specific issues | Document separately per platform |

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/dev-feature` | Full feature workflow | After research, for implementation |
| `/review-code` | Code review | After implementation |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
