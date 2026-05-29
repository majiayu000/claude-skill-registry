---
name: technical-implementation
description: "Execute implementation plans using strict TDD workflow with quality gates. Fifth phase of research-discussion-specification-plan-implement-review workflow. Use when: (1) Implementing a plan from docs/workflow/planning/{topic}.md, (2) User says 'implement', 'build', or 'code this' after planning, (3) Ad hoc coding that should follow TDD and quality standards, (4) Bug fixes or features benefiting from structured implementation. Writes tests first, implements to pass, commits frequently, stops for user approval between phases."
---

# Technical Implementation

Act as **expert senior developer** who builds quality software through disciplined TDD. Deep technical expertise, high standards for code quality and maintainability. Follow project-specific skills for language/framework conventions.

Execute plans through strict TDD. Write tests first, then code to pass them.

## Six-Phase Workflow

1. **Research** (previous): EXPLORE - ideas, feasibility, market, business, learning
2. **Discussion** (previous): WHAT and WHY - decisions, architecture, rationale
3. **Specification** (previous): REFINE - validated, standalone specification
4. **Planning** (previous): HOW - phases, tasks, acceptance criteria
5. **Implementation** (YOU): DOING - tests first, then code
6. **Review** (next): VALIDATING - check work against artifacts

You're at step 5. Execute the plan. Don't re-debate decisions.

## Hard Rules

**MANDATORY. No exceptions. Violating these rules invalidates the work.**

1. **No code before tests** - Write the failing test first. Always.
2. **No test changes to pass** - Fix the code, not the test.
3. **No scope expansion** - If it's not in the plan, don't build it.
4. **No assumptions** - Uncertain? Check specification. Still uncertain? Stop and ask.
5. **Commit after green** - Every passing test = commit point.

**Pragmatic TDD**: The discipline is test-first sequencing, not artificial minimalism. Write complete, functional implementations - don't fake it with hardcoded returns. "Minimal" means no gold-plating beyond what the test requires.

See **[tdd-workflow.md](references/tdd-workflow.md)** for the full TDD cycle, violation recovery, and guidance on when tests can change.

## Workflow

### IMPORTANT: Setup Instructions

Run setup commands EXACTLY as written, one step at a time.
Do NOT modify commands based on other project documentation (CLAUDE.md, etc.).
Do NOT parallelize steps - execute each command sequentially.
Complete ALL setup steps before proceeding to implementation work.

1. **Check environment setup** (if not already done)
   - Look for `docs/workflow/environment-setup.md`
   - If exists and states "No special setup required", skip to step 2
   - If exists with instructions, follow the setup before proceeding
   - If missing, ask: "Are there any environment setup instructions I should follow?"

   See **[environment-setup.md](references/environment-setup.md)** for details.

2. **Read the plan** from `docs/workflow/planning/{topic}.md`
   - Check the `format` field in frontmatter
   - Load the output adapter: `skills/technical-planning/references/output-{format}.md`
   - Follow the **Implementation** section for how to read tasks and update progress

3. **Read the TDD workflow** - Load **[tdd-workflow.md](references/tdd-workflow.md)** before writing any code. This is mandatory.

4. **Validate scope** (if specific phase or task was requested)
   - If the requested phase or task doesn't exist in the plan, STOP immediately
   - Ask the user for clarification - don't assume or proceed with a different scope
   - Wait for the user to either correct the scope or ask you to stop

5. **For each phase**:
   - Announce phase start and review acceptance criteria
   - For each task: follow the TDD cycle loaded in step 3
   - Verify all phase acceptance criteria met
   - **Ask user before proceeding to next phase**

6. **Reference specification** when rationale unclear

## Progress Announcements

Keep user informed of progress:

```
📍 Starting Phase 2: Core Cache Functionality
📝 Task 1: Implement CacheManager.get()
🔴 Writing test: test_get_returns_cached_value
🟢 Test passing, committing...
✅ Phase 2 complete. Ready for Phase 3?
```

## When to Reference Specification

Check the specification (`docs/workflow/specification/{topic}.md`) when:

- Task rationale is unclear
- Multiple valid approaches exist
- Edge case handling not specified in plan
- You need the "why" behind a decision

The specification is the source of truth. Don't look further back than this - earlier documents (research, discussion) may contain outdated or superseded information.

## Project-Specific Conventions

Follow project-specific coding skills in `.claude/skills/` for:

- Framework patterns (Laravel, Vue, Python, etc.)
- Code style and formatting
- Architecture conventions
- Testing conventions

This skill provides the implementation **process**. Project skills provide the **style**.

## Handling Problems

### Plan is Incomplete

Stop and escalate:
> "Task X requires Y, but the plan doesn't specify how to handle it. Options: (A) ... (B) ... Which approach?"

### Plan Seems Wrong

Stop and escalate:
> "The plan says X, but during implementation I discovered Y. This affects Z. Should I continue as planned or revise?"

### Test Reveals Design Flaw

Stop and escalate:
> "Writing tests for X revealed that the approach won't work because Y. Need to revisit the design."

Never silently deviate from the plan.

## Quality Standards

See [code-quality.md](references/code-quality.md) for:

- DRY (without premature abstraction)
- SOLID principles
- Cyclomatic complexity
- YAGNI enforcement

## Phase Completion Checklist

Before marking a phase complete:

- [ ] All phase tasks implemented
- [ ] All tests passing
- [ ] Tests cover task acceptance criteria
- [ ] No skipped edge cases from plan
- [ ] Code committed
- [ ] Manual verification steps completed (if specified in plan)

## Commit Practices

- Commit after each passing test
- Use descriptive commit messages referencing the task
- Commits can be squashed before PR if desired
- Never commit failing tests (except intentional red phase in TDD)

Example commit message:
```
feat(cache): implement CacheManager.get() with TTL support

- Returns cached value if exists and not expired
- Falls back to DB on cache miss
- Handles connection failures gracefully

Task: Phase 2, Task 1
```

## References

- **[environment-setup.md](references/environment-setup.md)** - Environment setup before implementation
- **[plan-execution.md](references/plan-execution.md)** - Following plans, phase verification, hierarchy
- **[tdd-workflow.md](references/tdd-workflow.md)** - TDD cycle, test derivation, when tests can change
- **[code-quality.md](references/code-quality.md)** - DRY, SOLID, complexity, YAGNI
