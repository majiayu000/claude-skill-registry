---
name: compound-engineering
description: Compound Engineering methodology - Plan→Work→Review→Compound loop where each unit of work makes subsequent work easier. Use when implementing features, fixing bugs, or any development work.
agents: [rex, nova, blaze, grizz, bolt, tap, spark, vex]
triggers: [compound, plan, review, learnings, patterns, methodology]
---

# Compound Engineering

A development methodology where each unit of work makes subsequent work easier—not harder.

## Core Philosophy

> "Each unit of engineering work should make subsequent units of work easier—not harder."

Traditional development accumulates technical debt. Every feature adds complexity. Compound engineering inverts this by creating a learning loop where each bug, failed test, or problem-solving insight gets documented and reused.

## The Compound Loop

```
Plan (40%) → Work (20%) → Review (20%) → Compound (20%)
```

**80% of compound engineering is in planning and review. 20% is in execution.**

---

## Phase 1: Plan (40% of effort)

Before writing any code, create a comprehensive plan.

### Research Phase

1. **Codebase Analysis**: Search for similar patterns, conventions, and prior art
2. **Commit History**: Use `git log` to understand how related features were built
3. **Documentation**: Check AGENTS.md files in relevant directories
4. **External Research**: Search for best practices relevant to the problem

### Plan Structure

```markdown
# Feature: [Name]

## Context
- What problem does this solve?
- Who is affected?
- Current vs desired behavior?

## Research Findings
- Similar patterns in codebase: [file links]
- Relevant prior implementations: [commit refs]
- Best practices discovered: [references]

## Acceptance Criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)

## Technical Approach
1. Step 1: [specific action]
2. Step 2: [specific action]

## Risks & Mitigations
- Risk 1: [mitigation]
```

---

## Phase 2: Work (20% of effort)

Execute the plan systematically.

### Execution Workflow

1. **Create isolated environment**: Feature branch or worktree
2. **Break into tasks**: One task at a time
3. **Validate continuously**: Run tests after each change
4. **Commit incrementally**: Small, focused commits

### Working Principles

- Follow existing patterns discovered in research
- Run tests after every meaningful change
- If something fails, understand WHY before proceeding
- Keep changes focused—no scope creep

### Quality Checks

```bash
# After each change:
cargo fmt --all --check    # or npm run lint
cargo clippy --all-targets # or npm run typecheck
cargo test                 # or npm test
```

---

## Phase 3: Review (20% of effort)

Before completing, perform comprehensive review.

### Review Checklist

**Code Quality**
- [ ] Follows existing codebase patterns and conventions
- [ ] No unnecessary complexity
- [ ] Clear naming that matches project conventions
- [ ] No debug code left behind

**Testing**
- [ ] Tests cover acceptance criteria
- [ ] Edge cases considered
- [ ] Tests are maintainable, not brittle

**Architecture**
- [ ] Change is consistent with system design
- [ ] No unnecessary coupling introduced

### Multi-Perspective Review

Consider code from different angles:
- **Maintainer**: Will this be easy to modify in 6 months?
- **Performance**: Any bottlenecks?
- **Security**: Any vulnerabilities?
- **Simplicity**: Can this be simpler?

---

## Phase 4: Compound (20% of effort)

Capture learnings to make future work easier.

### What to Compound

**Patterns**: Document new patterns discovered
```markdown
## Pattern: [Name]
When to use: [context]
Implementation: [example]
See: [file reference]
```

**Decisions**: Record why approaches were chosen
```markdown
## Decision: [Choice Made]
Context: [situation]
Options: [alternatives]
Rationale: [why this choice]
```

**Failures**: Turn every bug into a lesson
```markdown
## Lesson: [What Went Wrong]
Symptom: [observed]
Root cause: [actual problem]
Fix: [solution]
Prevention: [how to avoid]
```

### Where to Codify Learnings

| Type | Location | Duration |
|------|----------|----------|
| Feature-specific context | `progress.txt` | Current feature only |
| Permanent patterns | `AGENTS.md` | Forever |
| Code-level gotchas | Inline comments | With the code |
| Regression prevention | Test cases | Forever |

---

## Task Discovery (During Work)

**Liberally create new tasks** when you discover issues during implementation.

### What Triggers a New Task

| Discovery | Action |
|-----------|--------|
| Failing test or test gap | Create task: "Write tests for X" |
| Code needing refactoring | Create task: "Refactor Y for clarity" |
| Missing error handling | Create task: "Add error handling for Z" |
| Documentation gap | Create task: "Document A module" |
| TODOs or FIXMEs in code | Create task with specific fix |
| Build/lint warnings | Create task: "Fix linting in B" |
| Performance issues | Create task: "Optimize C operation" |

### How to Create Tasks

Use the Linear API or MCP tools to create immediately:

```
Create task:
- Title: "Fix: [specific issue]"
- Description: "[What you found, why it matters]"
- Dependencies: Set appropriately
- Agent: Same service agent that found it
```

**Do NOT batch for later.** Create the task when you discover the issue, then continue your current work.

### Compounding Questions

After completing work, ask:
- What did I learn that others should know?
- What mistake can be prevented?
- What pattern did I discover or create?
- What decision was made and why?

Document in appropriate location so future work benefits.

---

## Memory Architecture

### Short-Term Memory: progress.txt

For the **current feature only**. Reset between features.

```markdown
# Progress Log
Started: [date]
Feature: [name]
Parent Task: [parent-task-id]

## Codebase Patterns  ← SCANNED FIRST EACH ITERATION
- Pattern 1 discovered
- Pattern 2 discovered

---
## [Date] - [Task]
- What was implemented
- Files changed
- Learnings for future iterations
```

### Long-Term Memory: AGENTS.md

Permanent learnings that anyone should know.

```markdown
## Learnings

### [Category]
- Pattern: [description]
- Gotcha: [what to avoid]
- Dependency: [what relies on what]
```

**Rule:** If it only matters for this feature → progress.txt. If anyone editing this code should know → AGENTS.md.

---

## Progress Archiving (Feature Boundaries)

When starting a **new feature**, archive the previous progress.txt.

### When to Archive

- Starting work on a different parent task
- Parent task ID in progress.txt differs from current task
- Previous feature is complete

### Archive Process

```bash
# 1. Check if progress.txt has content from previous feature
cat progress.txt

# 2. If different feature, archive it
DATE=$(date +%Y-%m-%d)
FEATURE="previous-feature-name"
mkdir -p archive/$DATE-$FEATURE
mv progress.txt archive/$DATE-$FEATURE/

# 3. Create fresh progress.txt
cat > progress.txt << 'EOF'
# Progress Log
Started: [today's date]
Feature: [new feature name]
Parent Task: [new-parent-task-id]

## Codebase Patterns
(Patterns discovered during this feature - copy relevant ones from archive)

---
EOF

# 4. Commit the archive
git add archive/ progress.txt
git commit -m "chore: archive progress for [previous-feature]"
```

### Preserving Valuable Patterns

When resetting progress.txt:

1. Review the archived "Codebase Patterns" section
2. Copy patterns that are **still relevant** to the new progress.txt
3. Do NOT copy task-specific entries (those belong in archive)

### Why Archive?

- Fresh context prevents tunnel vision
- Each feature starts clean
- Valuable patterns preserved, noise discarded
- Easy to reference past feature learnings

---

## Success Metrics

You're doing compound engineering well when:
- Each feature takes less effort than the last similar feature
- Bugs become one-time events (documented and prevented)
- New work can be started quickly (patterns are established)
- Code reviews surface fewer issues (patterns are followed)
- Technical debt decreases over time

---

## Iron Law

```
DOCUMENT BEFORE MOVING ON
```

If you learned something, write it down before starting the next task.

---

## Quick Reference

| Phase | Time | Key Activities |
|-------|------|----------------|
| **Plan** | 40% | Research, find patterns, write plan |
| **Work** | 20% | Execute plan, validate continuously |
| **Review** | 20% | Multi-perspective check, quality gates |
| **Compound** | 20% | Document patterns, decisions, lessons |
