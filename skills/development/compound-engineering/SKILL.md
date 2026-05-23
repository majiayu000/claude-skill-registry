---
name: compound-engineering
description: "Compound Engineering workflow for AI-assisted development. Use when planning features, executing work, reviewing code, or codifying learnings. Follows the Plan → Work → Review → Compound loop where each unit of engineering makes subsequent work easier. Triggers on: plan this feature, implement this, review this code, compound learnings, create implementation plan, systematic development."
---
This skill implements Compound Engineering—a development methodology where each unit of work makes subsequent work easier, not harder. Inspired by Every.to's engineering approach.

## Core Philosophy

**Each unit of engineering work should make subsequent units of work easier—not harder.**

Traditional development accumulates technical debt. Every feature adds complexity. Every change increases maintenance burden. Compound engineering inverts this by creating a learning loop where each bug, failed test, or problem-solving insight gets documented and used by future work.

## The Compound Engineering Loop

```
Plan → Work → Review → Compound → (repeat)
```

1. **Plan (40%)**: Research approaches, synthesize information into detailed implementation plans
2. **Work (20%)**: Execute the plan systematically with continuous validation
3. **Review (20%)**: Evaluate output quality and identify learnings
4. **Compound (20%)**: Feed results back into the system to make the next loop better

80% of compound engineering is in planning and review. 20% is in execution.

## Step 1: Plan

Before writing any code, create a comprehensive plan. Good plans start with research:

### Research Phase
1. **Codebase Analysis**: Search for similar patterns, conventions, and prior art in the codebase
2. **Commit History**: Use `git log` to understand how related features were built
3. **Documentation**: Check README, AGENTS.md, and inline documentation
4. **External Research**: Search for best practices relevant to the problem

### Plan Document Structure
Create a plan document (markdown) with:

```markdown
# Feature: [Name]

## Context
- What problem does this solve?
- Who is affected?
- What's the current behavior vs desired behavior?

## Research Findings
- Similar patterns found in codebase: [list with file links]
- Relevant prior implementations: [commit references]
- Best practices discovered: [external references]

## Acceptance Criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Technical Approach
1. Step 1: [specific action]
2. Step 2: [specific action]
3. Step 3: [specific action]

## Code Examples
[Include code snippets that follow existing patterns]

## Testing Strategy
- Unit tests: [what to test]
- Integration tests: [what to test]
- Manual verification: [steps]

## Risks & Mitigations
- Risk 1: [mitigation]
- Risk 2: [mitigation]
```

### Detail Levels
- **Minimal**: Quick issues for simple features (1-2 hours work)
- **Standard**: Issues with technical considerations (1-2 days work)
- **Comprehensive**: Major features requiring architecture decisions (multi-day work)

## Step 2: Work

Execute the plan systematically:

### Execution Workflow
1. **Create isolated environment**: Use feature branch or git worktree
2. **Break down into tasks**: Create TODO list from plan
3. **Execute systematically**: One task at a time
4. **Validate continuously**: Run tests after each change
5. **Commit incrementally**: Small, focused commits with clear messages

### Working Principles
- Follow existing patterns discovered in research
- Run tests after every meaningful change
- If something fails, understand why before proceeding
- Keep changes focused—don't scope creep

### Quality Checks During Work
```bash
# After each change, verify:
npm run typecheck  # or equivalent
npm test           # run affected tests
npm run lint       # check code quality
```

## Step 3: Review

Before merging, perform comprehensive review:

### Review Checklist

**Code Quality**
- [ ] Follows existing codebase patterns and conventions
- [ ] No unnecessary complexity—prefer duplication over wrong abstraction
- [ ] Clear naming that matches project conventions
- [ ] No debug code or console.logs left behind

**Security**
- [ ] No secrets or sensitive data exposed
- [ ] Input validation where needed
- [ ] Safe handling of user data

**Performance**
- [ ] No obvious performance regressions
- [ ] Database queries are efficient (no N+1)
- [ ] Appropriate caching if applicable

**Testing**
- [ ] Tests cover acceptance criteria
- [ ] Edge cases considered
- [ ] Tests are maintainable, not brittle

**Architecture**
- [ ] Change is consistent with system design
- [ ] No unnecessary coupling introduced
- [ ] Follows separation of concerns

### Multi-Perspective Review
Consider the code from different angles:
- **Maintainer perspective**: Will this be easy to modify in 6 months?
- **Performance perspective**: Any bottlenecks?
- **Security perspective**: Any vulnerabilities?
- **Simplicity perspective**: Can this be simpler?

## Step 4: Compound

This is where the magic happens—capture learnings to make future work easier:

### What to Compound

**Patterns**: Document new patterns discovered or created
```markdown
## Pattern: [Name]
When to use: [context]
Implementation: [example code]
See: [file reference]
```

**Decisions**: Record why certain approaches were chosen
```markdown
## Decision: [Choice Made]
Context: [situation]
Options considered: [alternatives]
Rationale: [why this choice]
Consequences: [trade-offs]
```

**Failures**: Turn every bug into a lesson
```markdown
## Lesson: [What Went Wrong]
Symptom: [what was observed]
Root cause: [actual problem]
Fix: [solution]
Prevention: [how to avoid in future]
```

### Where to Codify Learnings

1. **AGENTS.md**: Project-wide guidance that applies everywhere
2. **Subdirectory AGENTS.md**: Specific guidance for subsystems
3. **Inline comments**: Only when the code isn't self-explanatory
4. **Test cases**: Turn bugs into regression tests

### Compounding in Practice

After completing work, ask:
- What did I learn that others should know?
- What mistake did I make that can be prevented?
- What pattern did I discover or create?
- What decision was made and why?

Document these in the appropriate location so future agents (and humans) benefit.

## Practical Commands

### Planning a Feature
```
Plan implementation for: [describe feature]
- Research the codebase for similar patterns
- Check git history for related changes
- Create a detailed plan with acceptance criteria
- Include code examples that match existing patterns
```

### Executing Work
```
Execute this plan: [plan reference]
- Create feature branch
- Break into TODO list
- Work through systematically
- Run tests after each change
- Create PR when complete
```

### Reviewing Code
```
Review this change: [PR/diff reference]
- Check for code quality issues
- Look for security concerns
- Evaluate performance implications
- Verify test coverage
- Suggest improvements
```

### Compounding Learnings
```
Compound learnings from: [work just completed]
- What patterns were used or created?
- What decisions were made and why?
- What failures occurred and how to prevent them?
- Update AGENTS.md with relevant guidance
```

## Key Principles

1. **Prefer duplication over wrong abstraction**: Simple, clear code beats complex abstractions
2. **Document as you go**: Every command generates documentation that makes future work easier
3. **Quality compounds**: High-quality code is easier to modify
4. **Systematic beats heroic**: Consistent processes beat individual heroics
5. **Knowledge should be codified**: Learnings should be captured and reused

## Success Metrics

You're doing compound engineering well when:
- Each feature takes less effort than the last similar feature
- Bugs become one-time events (documented and prevented)
- New team members can be productive quickly (institutional knowledge is accessible)
- Code reviews surface fewer issues (patterns are established and followed)
- Technical debt decreases over time (learnings compound)

Remember: You're not just building features—you're building a development system that gets better with each use.
