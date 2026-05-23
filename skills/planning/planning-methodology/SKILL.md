---
name: planning-methodology
description: Create minimal-change, reversible implementation plans with verification steps. Use when user requests "create a plan", "how should we implement", "plan this feature", "implementation strategy", or mentions planning, roadmap, architecture.
auto_invoke: true
tags: [planning, architecture, minimal-change, reversibility]
---

# Planning Methodology Skill

This skill provides a systematic methodology for creating implementation plans that are surgical, reversible, and minimize risk while maximizing clarity.

## When Claude Should Use This Skill

Claude will automatically invoke this skill when:
- ResearchPack is ready and implementation planning is needed
- User asks "how should we implement...", "create a plan for..."
- Complex feature requires structured approach
- Need to break down requirements into executable steps
- Transforming research into actionable blueprint

## Core Principles (BRAHMA Constitution)

1. **Simplicity over complexity** (KISS, YAGNI)
2. **Minimal changes only** - Touch fewest files possible
3. **Reversibility mandatory** - Every change must be undoable
4. **Verification at each step** - Clear success criteria

## Planning Methodology Protocol

### Step 1: Codebase Discovery (< 90 seconds)

**Objective**: Understand existing structure before planning changes

**Actions**:

1. **Structure scan** (use Glob tool):
   ```
   Search patterns:
   - Source files: src/**/*.{ext}
   - Config files: *.config.{ext}, .{ext}rc
   - Test files: **/*.test.{ext}, **/*.spec.{ext}
   - Documentation: docs/*.md, README.md
   ```

2. **Pattern recognition** (use Grep + Read):
   - How similar features are currently implemented
   - Naming conventions (file names, function names)
   - Code style (indentation, formatting)
   - Import/export patterns
   - Test patterns and frameworks

3. **Integration point identification**:
   - Where does new code connect to existing code?
   - Configuration files that need updates
   - Entry points (main.ts, index.js, etc.)
   - Dependency injection patterns

4. **Constraint discovery**:
   - Existing dependencies that limit choices
   - Framework conventions that must be followed
   - Security/auth patterns that must be maintained
   - Performance SLAs to meet

**Output**:
```
Codebase Profile:
- Primary language: [TypeScript/Python/Go/etc.]
- Framework: [Next.js/Django/Gin/etc.]
- Structure: [src/ organization pattern]
- Test framework: [Jest/pytest/etc.]
- Key patterns: [Dependency injection / Factory / etc.]
- Integration points: [config.ts, app.ts, etc.]
```

**Anti-stagnation**: Max 90 seconds - if codebase is large, focus on areas relevant to feature only

### Step 2: Minimal Change Analysis (< 60 seconds)

**Objective**: Identify the smallest set of changes that accomplishes the goal

**Questions to answer**:

1. **New vs Modify**:
   - Can we extend existing code (better) or must we modify it?
   - Can new functionality live in new files (preferred)?
   - What's the smallest interface between new and existing code?

2. **Reuse vs Rebuild**:
   - What existing utilities/services can be reused?
   - What patterns can we follow from similar features?
   - What must be built from scratch (minimize this)?

3. **Scope boundaries**:
   - What's the absolute minimum to make feature work?
   - What's "nice to have" that can be deferred?
   - What edge cases must be handled vs can be documented as limitations?

4. **Reversibility**:
   - How easily can each change be undone?
   - Are we modifying core/critical files (higher risk)?
   - Can we use feature flags for gradual rollout?

**Output**:
```
Minimal Change Strategy:
- New files: [N] (primary work here)
- Modified files: [N] (minimal edits)
- Deleted files: 0 (avoid deletions, use deprecation)
- Core files touched: [N] (minimize this)
- Reversibility: [Git revert / Config toggle / Feature flag]
```

**Principles**:
- Prefer extension over modification
- Prefer new files over editing existing
- Prefer configuration over code
- Prefer composition over inheritance

### Step 3: Risk Assessment (< 30 seconds)

**Objective**: Identify what could go wrong and plan mitigations

**Categories of risk**:

1. **Breaking changes**:
   - Will this affect existing functionality?
   - Are we modifying shared/core modules?
   - Could this break other features?

2. **Performance risks**:
   - Will this add latency to critical paths?
   - Memory/CPU impact on existing operations?
   - Database query performance degradation?

3. **Security risks**:
   - Does this handle user input (validate & sanitize)?
   - Are credentials/secrets managed properly?
   - Could this introduce injection vulnerabilities?

4. **Integration risks**:
   - Dependencies on external services (what if they're down)?
   - API version mismatches?
   - Race conditions or concurrency issues?

5. **Testing gaps**:
   - What's hard to unit test (integration test instead)?
   - What scenarios might we miss?
   - What's the fallback if tests don't catch an issue?

**For each identified risk**:
```
Risk: [Description]
Probability: [High/Medium/Low]
Impact: [High/Medium/Low]
Mitigation: [How to prevent]
Detection: [How we'll know if it happens]
Contingency: [What we'll do if it happens]
```

**Anti-pattern**: Don't identify risks without mitigations - every risk needs an answer

### Step 4: Implementation Sequence (< 30 seconds)

**Objective**: Order the work for safety and clarity

**Sequencing principles**:

1. **Dependencies first**: Build foundation before dependent features
2. **Tests alongside**: Write tests as you implement (or before - TDD)
3. **Incremental integration**: Connect to existing system gradually
4. **Verification checkpoints**: Each step has clear pass/fail criteria

**Step structure**:
```
Step N: [Action verb] [What]
- Task: [Detailed description]
- Files: [Which files to change]
- Code: [Specific code examples]
- Verification: [How to confirm success]
- Time estimate: [X minutes]
```

**Verification methods**:
- Unit test passes: `npm test path/to/test`
- Build succeeds: `npm run build`
- Manual check: "Navigate to X and confirm Y is visible"
- Integration test: `npm run test:integration`
- Performance check: `npm run benchmark` (if applicable)

**Total time estimate**: Sum of all step estimates + 20% buffer

### Step 5: Rollback Planning (< 20 seconds)

**Objective**: Ensure every change can be undone safely

**Rollback mechanisms** (in priority order):

1. **Git revert** (simplest):
   ```bash
   git reset --hard [checkpoint-commit]
   ```
   Good when: All changes in one commit, no DB migrations

2. **Feature flag toggle** (gradual rollout):
   ```javascript
   if (featureFlags.newFeature === true) {
     // new code
   } else {
     // old code
   }
   ```
   Good when: Want to test in production, quick rollback needed

3. **Configuration rollback**:
   Restore previous config files
   Good when: Changes are mostly configuration-driven

4. **Partial rollback**:
   Keep working parts, revert broken parts
   Good when: Multiple independent changes, some work

**Rollback plan must include**:
- Exact commands to execute
- Verification steps after rollback
- Data migration rollback (if DB changes made)
- Cache invalidation (if caching involved)

**Rollback triggers** (when to execute rollback):
- Tests fail in production
- Performance degrades > [threshold]%
- Error rate increases > [threshold]%
- Critical functionality breaks

### Step 6: Plan Documentation (< 30 seconds)

**Objective**: Structure all above findings into clear, executable plan

**Implementation Plan Format**:

```markdown
# 🗺️ Implementation Plan: [Feature Name]

## Summary
[2-3 lines: what + why + approach]

## 📁 File Changes
[New: N, Modified: N, with specific purposes]

## 🔢 Implementation Steps
[Numbered steps with verification]

## 🧪 Test Plan
[Unit + integration + manual tests]

## ⚠️ Risks & Mitigations
[Each risk with mitigation and contingency]

## 🔄 Rollback Plan
[Exact rollback procedure]

## ✅ Success Criteria
[Clear definition of "done"]
```

**Checklist before delivering**:
- ✓ Every file change has a clear purpose
- ✓ Every step has verification method
- ✓ All risks have mitigations
- ✓ Rollback plan is complete and tested (if possible)
- ✓ Success criteria are measurable
- ✓ Time estimates are realistic

## Quality Standards

### Completeness
- **File changes**: Specify exact files with line-level changes where possible
- **Steps**: Each step is atomic (can be done and verified independently)
- **Tests**: Cover happy path + at least 2 edge cases + 1 error case
- **Risks**: All major risks identified (breaking, performance, security)

### Clarity
- **Actionable**: Developer can execute without additional questions
- **Verifiable**: Each step has objective pass/fail criteria
- **Unambiguous**: No "probably" or "maybe" - specific instructions only

### Safety
- **Reversible**: Every change can be undone
- **Incremental**: Changes build up gradually (not big bang)
- **Validated**: Tests verify correctness at each step
- **Isolated**: Failure of one step doesn't break entire system

## Common Pitfalls to Avoid

❌ **Don't**:
- Plan modifications to many files simultaneously (hard to verify)
- Skip risk assessment ("hope for the best")
- Forget rollback plan
- Make plans that require perfect execution (allow for errors)
- Over-engineer ("we might need this someday")
- Under-estimate time (plans should be realistic)

✅ **Do**:
- Touch fewest files possible (minimal blast radius)
- Identify risks and plan mitigations explicitly
- Always include rollback procedure
- Build in verification checkpoints at every step
- Follow YAGNI (You Aren't Gonna Need It) - only what's needed now
- Add 20% time buffer for unexpected issues

## Integration with knowledge-core.md

**Before planning**:
Read `knowledge-core.md` to check for:
- Architectural patterns established in past projects
- Decisions that constrain current work
- Known gotchas in this codebase

**After planning**:
If plan establishes new patterns, note for knowledge-core update:
```
New Pattern Established:
- Pattern: [Name/description]
- Context: [When to use this]
- Example: [Which files demonstrate this]
```

## Performance Targets

- **Total planning time**: < 3 minutes for typical features
- **Plan accuracy**: 95%+ of files identified correctly
- **Risk coverage**: 100% of major risks identified
- **Time estimates**: Within 30% of actual implementation time

## Example Usage

**Scenario**: ResearchPack ready for Redis caching, need implementation plan

**Claude (using this skill)**:

```
[Internal: Need to plan Redis integration systematically]

📐 Activating planning-methodology skill

🔎 Analyzing codebase structure...
[Follows methodology: discover → analyze → assess → sequence → rollback → document]

# 🗺️ Implementation Plan: Redis Caching

## Summary
Add Redis-based caching layer to ProductService to reduce database load.
Approach: Create separate CacheService wrapper, inject into ProductService,
maintain backward compatibility via optional usage.

## 📁 File Changes (5 files)

### New Files (2)
1. `src/services/CacheService.ts` (~80 lines)
   - Purpose: Redis client wrapper with get/set/del/ttl operations
   - Exports: CacheService class
   - Dependencies: redis@4.6.0, config

[...rest of detailed plan following format]

✅ Plan ready for implementation
```

---

**This skill ensures plans are safe, minimal, clear, and executable - setting up @code-implementer for success.**