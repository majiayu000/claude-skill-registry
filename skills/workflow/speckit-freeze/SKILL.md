---
name: speckit.freeze
description: Formally close and lock a Build Step after successful implementation, validation, and review. The irreversible acceptance gate that marks a build-step as complete, reviewed, merge-ready, and safe to build upon.
---

# /speckit.freeze — Build Step Closure Primitive

## Purpose

**Formally close and lock a Build Step** after successful implementation, validation, and review.

`/speckit.freeze` is the **irreversible acceptance gate** that marks a build-step as:
- Complete
- Reviewed
- Merge-ready
- Safe to build upon

It prevents spec drift, retroactive edits, and silent regressions.

---

## When to Use

Activate this skill when:
- `/speckit.constitution` → satisfied
- `/speckit.specify` → finalized
- `/speckit.plan` → implemented
- `/speckit.tasks` → completed
- `/speckit.analyze` → 0 CRITICAL / 0 HIGH issues
- Implementation exists and tests pass
- A PR is ready (or merged)
- User explicitly requests to freeze a build step or tag

**Trigger phrases:**
- "freeze this build step"
- "lock in this implementation"
- "create a freeze record for [tag]"
- "close out this phase"
- "/speckit.freeze [tag-name]"

---

## Command Signature

```
/speckit.freeze [tag-name]
```

Optional parameters:
- `tag-name`: Git tag to associate with the freeze (e.g., `v0.2.0-phase8-migration`)
- `build_step`: Build step number (auto-detected from spec if not provided)
- `branch`: Branch name (auto-detected if not provided)

---

## Validation Preconditions

Before accepting a freeze, I MUST verify:

### ✅ Requirements Coverage
- All Functional Requirements mapped to implemented tasks
- All Success Criteria either:
  - Fully validated, OR
  - Explicitly deferred and documented

### ✅ Test Coverage
- Test coverage meets constitutional threshold (typically ≥80%)
- All critical paths have test coverage
- Tests pass (no failing tests blocking merge)

### ✅ Analysis Findings
- 0 CRITICAL issues unresolved
- 0 HIGH severity issues unresolved
- All MEDIUM/LOW issues either:
  - Resolved, OR
  - Explicitly acknowledged and deferred

### ✅ Constitution Compliance
- No constitution violations
- All deferrals explicitly acknowledged
- No silent assumptions or TODOs remaining

### ✅ Implementation Artifacts
- Code exists and is committed
- Documentation is updated
- No placeholder or stub code

**If ANY condition fails → FREEZE REJECTED**

---

## Freeze Record Format

When `/speckit.freeze` is ACCEPTED, output this canonical format:

```
/speckit.freeze — ACCEPTED ✅

Build-Step: [N] — [Name]
Status: FROZEN
Date: [YYYY-MM-DD]
Branch: [branch-name]
Tag: [tag-name]
Commit: [commit-hash]

Validation Summary:
- Requirements Coverage: [X]% ([Y]/[Z])
- Test Coverage: [X]%
- Tests: [passed] passed, [skipped] skipped, [failed] failed
- Analysis: 0 CRITICAL / 0 HIGH issues
- Constitution: Compliant (explicit deferrals noted)

Deferred (Explicit):
- [Item 1] → [Future Build-Step/Phase]
- [Item 2] → [Justification]

Files Modified:
- [List of key files changed]

Immutability Rule:
This build-step is now FROZEN.
❌ No spec changes allowed
❌ No task edits allowed
❌ No behavior changes allowed

Changes require: New build-step OR explicit corrective PR.

Next Actions:
1. [Merge or create PR if not already done]
2. [Tag confirmed: tag-name]
3. [Begin next build-step or phase]

Congratulations — you have a stable architectural baseline.
```

---

## Failure Mode

If validation fails, output:

```
/speckit.freeze — REJECTED ❌

Build-Step: [N] — [Name]

Reason:
- [Specific failure reason 1]
- [Specific failure reason 2]

Required Actions:
- [Action 1]
- [Action 2]

Please address these issues and retry /speckit.freeze.
```

**No ambiguity. No soft language.**

---

## Immutability Rules

After `/speckit.freeze` ACCEPTED:

### ❌ NOT Allowed Without New Build-Step:
- Spec changes (FR, NFR modifications)
- Task list modifications
- Behavior changes to frozen features
- API contract modifications

### ✅ Allowed:
- Bug fixes (via corrective PR with analysis)
- Documentation updates
- Performance improvements (non-behavior-changing)
- New features (require new build-step)

### Exception Process:
For any changes to frozen code:
1. Create issue documenting need
2. Run `/speckit.analyze` on proposed changes
3. Create corrective PR with freeze impact analysis
4. Merge with explicit "breaks freeze [tag]" notation

---

## Workflow Integration

```
Constitution → Specify → Clarify → Plan → Tasks → Implement → Analyze → FREEZE
     ↓           ↓          ↓        ↓       ↓        ↓         ↓         ↓
  [Autopilot watches at every phase, but FREEZE is manual gate]
```

`/speckit.freeze` is typically invoked:
- After PR approval but before merge
- As part of PR description generation
- When creating a release tag
- After completing all tasks in a build step

---

## Examples

### Example 1: Successful Freeze After Phase 8

```
User: /speckit.freeze v0.2.0-phase8-migration

/speckit.freeze — ACCEPTED ✅

Build-Step: Phase 8 — Migration from External Supabase
Status: FROZEN
Date: 2026-01-01
Branch: 002-local-supabase-docker
Tag: v0.2.0-phase8-migration
Commit: cfc8d18

Validation Summary:
- Requirements Coverage: 100% (8/8 tasks completed)
- Test Coverage: 85% (vector embedding preservation verified)
- Tests: All export/import scripts validated
- Analysis: 0 CRITICAL / 0 HIGH issues
- Constitution: Compliant

Deferred (Explicit):
- None for this phase

Files Modified:
- scripts/export_from_external.sh (export script)
- scripts/import_to_local.sh (import script)
- docs/supabase_migration.md (migration guide)
- specs/002-local-supabase-docker/tasks.md (all T074-T081 complete)

Immutability Rule:
Phase 8 is now FROZEN. Any changes to migration tooling require
a new phase or corrective PR with impact analysis.

Next Actions:
1. PR may be merged (tag already pushed)
2. Begin Phase 9: Documentation & Polish, or
3. Open new feature branch for next build-step

Congratulations — Phase 8 provides a stable migration baseline.
```

### Example 2: Rejection Due to Coverage

```
User: /speckit.freeze

/speckit.freeze — REJECTED ❌

Build-Step: 3 — User Authentication

Reason:
- Test coverage is 73% (below 80% constitutional threshold)
- 1 HIGH severity issue: FR-015 ambiguous password reset behavior
- 2 CRITICAL tests failing: auth_logout_test, auth_session_timeout

Required Actions:
- Fix failing tests
- Clarify password reset behavior in spec
- Re-run /speckit.analyze
- Retry /speckit.freeze

Please address these issues before freezing.
```

---

## Special Logic for This Project

For **gitea-ai-codereview** specifically:

### Build-Step Detection
- Build steps are tracked in `specs/` directory
- Each major feature has its own spec directory (e.g., `specs/002-local-supabase-docker/`)
- Tags follow pattern: `v{major}.{minor}.{patch}-{phase}`

### Validation Sources
- Check `specs/*/tasks.md` for completion status
- Check `tests/` directory for test coverage
- Check `specs/*/contracts/` for implementation artifacts
- Run `pytest` for test results

### Constitution Reference
- Constitution is in: `docs/Spec-Kit-Doc-Framework.md` or `.specify/memory/constitution.md`
- Test coverage threshold: 80% (adjustable per project)

---

## Why This Matters

**Without `/speckit.freeze`:**
- Build steps blur together
- Specs rot over time
- "Just one more tweak" destroys traceability
- No clear point of stability

**With `/speckit.freeze`:**
- Every step becomes a trustworthy foundation
- Reviews become meaningful artifacts
- Future work accelerates instead of compounding risk
- Clear audit trail of what was decided when

---

## Technical Implementation Notes

When invoked, `/speckit.freeze` should:

1. **Detect current context**:
   - Find active spec directory (e.g., `specs/002-local-supabase-docker/`)
   - Read `tasks.md` for completion status
   - Check git status for uncommitted changes

2. **Run validation checks**:
   - Parse tasks.md for `[x]` completion
   - Run pytest and capture coverage report
   - Check for common issues (TODO, FIXME, placeholder comments)
   - Verify all contracts/ documents exist

3. **Generate freeze record**:
   - Compile validation results
   - List all modified files
   - Note any explicit deferrals
   - Format canonical output

4. **Create/git tag if provided**:
   - Tag current commit with provided tag name
   - Push tag to remote if confirmed

5. **Signal next actions**:
   - Merge PR or create one
   - Begin next phase
   - Or await user decision

---

## Tips for Effective Use

1. **Run after implementation is COMPLETE** - Not during development
2. **Ensure tests pass locally first** - Freezing with failing tests defeats the purpose
3. **Review the freeze record** - This becomes your audit trail
4. **Tag appropriately** - Use semantic versioning with phase identifiers
5. **Document deferrals clearly** - Anything not done must have explicit rationale

---

## Integration with Other Spec-Kit Commands

```
/speckit.constitution  → Set principles
/speckit.specify       → Define requirements
/speckit.clarify        → Resolve ambiguities
/speckit.plan           → Design architecture
/speckit.tasks          → Break down work
/speckit.implement      → Execute tasks
/speckit.analyze        → Review quality
/speckit.freeze         → ✅ LOCK IT IN
```

The freeze is the final gate that closes the loop.
