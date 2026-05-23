---
name: sparc-planning
description: Creates comprehensive implementation plans using the SPARC framework (Specification, Pseudocode, Architecture, Refinement, Completion). Automatically invokes check-history for context, generates detailed plans with ranked task lists, dependency graphs, security/performance considerations. For significant features (>8 hours), major refactoring, breaking changes, or multi-component work.
version: 2.0.0
---

# SPARC Implementation Planning Skill

## Purpose

Create comprehensive, structured implementation plans for significant development work using the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) framework.

## SPARC Framework Overview

**SPARC** is a five-phase development methodology:

1. **Specification**: Define requirements, constraints, and success criteria
2. **Pseudocode**: Create high-level algorithm descriptions
3. **Architecture**: Design system structure and component interactions
4. **Refinement**: Iteratively improve and optimize
5. **Completion**: Finalize, document, and verify

## When to Load Additional References

The workflow below covers the essential SPARC planning process. Load detailed references when:

**For detailed phase descriptions and templates:**

```
Read `~/.claude/skills/sparc-planning/references/REFERENCE.md`
```

Use when: Need specification templates, pseudocode examples, architecture patterns, refinement checklists, completion criteria templates

**For implementation templates:**

```
Read `~/.claude/skills/sparc-planning/references/TEMPLATE.md`
```

Use when: Creating actual planning documents, need document structure, formatting guidelines

**For test scenarios and examples:**

```
Read `~/.claude/skills/sparc-planning/references/test-scenarios.md`
```

Use when: Planning test strategy, defining test cases, comprehensive testing examples

---

## Workflow

### Quick 12-Step SPARC Process

1. **Invoke check-history** - Gather context about existing work
2. **Gather Requirements** - Ask clarifying questions, document responses
3. **Research Dependencies** - Use Context7 for library documentation if needed
4. **Create Phase 1 - Specification** - Functional/non-functional requirements, constraints, success criteria
5. **Create Phase 2 - Pseudocode** - Algorithm pseudocode, component interfaces
6. **Create Phase 3 - Architecture** - Components, patterns, data models, interactions, security/performance architecture
7. **Create Phase 4 - Refinement Plan** - Code quality, optimization, security review, test coverage
8. **Create Phase 5 - Completion Criteria** - Completion checklist, documentation requirements, deployment plan
9. **Generate Ranked Task List** - Break down into ordered, estimated tasks with owners
10. **Identify Dependencies and Blockers** - Create dependency graph, identify risks and mitigations
11. **Create Security & Performance Plans** - Security checkpoints, performance targets and measurement
12. **Document and Present Plan** - Save all planning docs, present summary to user

**For detailed step-by-step workflow with templates, examples, and code samples, see `references/WORKFLOW-STEPS.md`.**

---

## Integration with Other Skills

This skill invokes:

- **`check-history`** - Step 1 (gather context)

This skill may be followed by:

- **`manage-branch`** - Create feature branch
- **`safe-commit`** - Commit planning documents

---

## Best Practices

1. **Be thorough** - Better to over-plan than under-plan
2. **Be specific** - Vague plans lead to vague implementations
3. **Consider all aspects** - Security, performance, testing, documentation
4. **Identify risks early** - Mitigation is easier with planning
5. **Make it reviewable** - User should be able to understand and validate plan
6. **Save everything** - Plans are valuable documentation
7. **Be realistic** - Estimate time conservatively

---

## When to Skip Planning

Some tasks don't need full SPARC planning:

- **Simple bug fixes** - Go straight to implementation
- **Documentation updates** - No architecture needed
- **Trivial refactoring** - Single file, obvious change
- **Configuration changes** - Low risk, reversible

**Rule of thumb:** If implementation is < 4 hours and touches < 3 files, skip formal planning.

---

## Adapting SPARC for Different Project Sizes

### Small feature (< 8 hours)

- Brief specification (1 paragraph)
- Simplified pseudocode
- Component list (no diagrams)
- Basic task list
- Standard checklist

### Medium feature (8-40 hours)

- Detailed specification
- Comprehensive pseudocode
- Architecture diagrams
- Detailed task list with estimates
- Security & performance plans

### Large feature (> 40 hours)

- Full SPARC documentation
- Multiple architecture views
- Dependency graphs
- Risk assessment matrix
- Milestone planning

---

## Troubleshooting

**Common Planning Problems:**

- Requirements incomplete or vague → Break down, focus on MVP
- Too many dependencies/blockers → Re-scope, identify alternatives
- Estimated time unrealistic → Use time-boxing, add research spikes
- Architecture reveals fundamental issues → STOP, revise requirements
- Plan too detailed/taking too long → Simplify, time-box to 90 minutes
- Plan doesn't match team conventions → Review check-history, align patterns
- User rejects plan → Iterate, clarify gaps, revise and re-present

**For detailed troubleshooting with symptoms, solutions, and examples, see `references/TROUBLESHOOTING.md`.**

---

## Quick Reference

**Invoke SPARC planning when:**

- User requests implementation plan
- Starting significant feature (> 8 hours)
- Making breaking changes
- Refactoring multiple components
- Need architecture decision record

**Output artifacts:**

1. Specification document
2. Pseudocode for algorithms
3. Architecture design
4. Refinement plan
5. Completion checklist
6. Ranked task list
7. Security plan
8. Performance plan

**Next step after planning:**
Review with user, get approval, create branch, begin implementation.
