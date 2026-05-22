---
name: review-commit
description: Quick quality review of staged changes for pre-commit validation. Checks Ruby best practices and flags critical issues.
agent: general-purpose
allowed-tools: Bash, Read, Grep, Glob
---

# Pre-Commit Quality Review

Review the staged changes in this commit for code quality issues before committing.

## Objectives

- **Fast**: Complete review in < 30 seconds
- **Focused**: Only review staged Ruby files
- **Actionable**: Clear pass/fail with specific fixes
- **Non-interactive**: Works in headless mode
- **Expert-driven**: Apply Ruby best practices from industry experts

## Expert Panel

Apply principles from these Ruby/software design experts:

1. **Sandi Metz** - POODR principles, small methods/classes, SRP, DRY
2. **Jeremy Evans** - Sequel best practices, transaction safety, performance
3. **Kent Beck** - Simple design, revealing names, Command-Query Separation
4. **Avdi Grimm** - Confident Ruby, null objects, tell-don't-ask, meaningful returns
5. **Gary Bernhardt** - Functional core/imperative shell, fast tests, immutability

## Review Process

1. **Get staged files:**
   ```bash
   git diff --cached --name-only --diff-filter=ACM | grep '\.rb$'
   ```

2. **For each staged Ruby file, check:**
   - Get the full diff: `git diff --cached <file>`
   - Review only the added/modified lines (lines starting with `+`)

3. **Look for critical issues (❌ BLOCK):**

   **Sandi Metz violations:**
   - ❌ Missing `frozen_string_literal: true` in new files
   - ❌ Methods > 15 lines (SRP violation, too complex)
   - ❌ Classes > 200 lines (god object)
   - ❌ Obvious code duplication (DRY violation)

   **Jeremy Evans (Sequel) violations:**
   - ❌ Raw SQL strings instead of Sequel dataset methods
   - ❌ Database writes without transaction wrapper
   - ❌ N+1 queries (multiple queries in loops)

   **Kent Beck violations:**
   - ❌ Overly complex solutions (nested conditionals > 3 levels)
   - ❌ Command-Query Separation violation (methods that both mutate and return calculated values)

   **Avdi Grimm violations:**
   - ❌ Defensive nil checks everywhere (should use null objects)
   - ❌ Implicit nil returns in public methods
   - ❌ Bare `raise` or `rescue` without exception class

   **Gary Bernhardt violations:**
   - ❌ I/O operations mixed with business logic (should separate)
   - ❌ Mutable state in value objects
   - ❌ Database/file I/O in unit tests (makes tests slow)

   **Testing:**
   - ❌ New public methods without corresponding tests

4. **Look for medium issues (⚠️ WARNING):**

   **Sandi Metz:**
   - ⚠️ Methods 10-15 lines (consider extracting)
   - ⚠️ Classes 100-200 lines (approaching god object)
   - ⚠️ Method parameters > 3 (use parameter object)

   **Jeremy Evans:**
   - ⚠️ Missing indexes on foreign keys
   - ⚠️ Connection not properly managed

   **Kent Beck:**
   - ⚠️ Poor naming (unclear variable/method names, abbreviations)
   - ⚠️ Methods doing multiple things (and/or in method name)

   **Avdi Grimm:**
   - ⚠️ Law of Demeter violations (chained method calls like `foo.bar.baz.qux`)
   - ⚠️ Asking instead of telling (lots of getters instead of sending commands)

   **Gary Bernhardt:**
   - ⚠️ Business logic scattered in imperative shell
   - ⚠️ Missing value objects (primitives passed around)

   **General:**
   - ⚠️ Missing documentation for public APIs
   - ⚠️ Tight coupling between modules

## Output Format

Provide a clear summary with expert attributions:

```
# Pre-Commit Quality Review

## Files Reviewed
- file1.rb (23 lines changed)
- file2.rb (8 lines changed)

## Status: ❌ BLOCK / ✅ PASS / ⚠️ WARNING

### Critical Issues ❌ (must fix before commit)

**Sandi Metz violations:**
- file1.rb:1 - Missing frozen_string_literal: true
- file2.rb:15-38 - Method too long (24 lines, max 15)

**Jeremy Evans violations:**
- file1.rb:42 - Raw SQL string instead of Sequel dataset method
- file1.rb:50 - Database write without transaction wrapper

**Avdi Grimm violations:**
- file2.rb:10 - Implicit nil return in public method

### Medium Issues ⚠️ (consider fixing)

**Sandi Metz:**
- file3.rb:20-32 - Method is 13 lines (consider extracting)

**Kent Beck:**
- file2.rb:5 - Variable name `x` is unclear (revealing intent)

**Avdi Grimm:**
- file3.rb:45 - Law of Demeter violation: user.account.settings.theme

### Recommendations

1. Add `frozen_string_literal: true` to file1.rb (Sandi Metz)
2. Convert raw SQL at file1.rb:42 to Sequel dataset (Jeremy Evans)
3. Wrap database write at file1.rb:50 in transaction (Jeremy Evans)
4. Extract file2.rb:15-38 into smaller methods (Sandi Metz)
5. Return explicit value instead of nil at file2.rb:10 (Avdi Grimm)
6. Rename `x` to describe what it contains (Kent Beck)
7. Extract file3.rb:20-32 for better readability (Sandi Metz)
8. Use tell-don't-ask at file3.rb:45 (Avdi Grimm)

## Suggested Actions

[If BLOCK] Run: git reset HEAD <files> && fix issues && git add <files>
[If WARNING] Consider fixing before commit or create a follow-up task
[If PASS] Commit looks good! 🚀
```

## Exit Behavior

- **Return clear judgment**: BLOCK, WARNING, or PASS
- **Be specific**: Include file:line references for all issues
- **Be helpful**: Suggest concrete fixes
- **Be fast**: Don't over-analyze, focus on obvious problems

## Quick Reference Checklist

For each added/modified line in the diff, scan for:

**Sandi Metz:**
- [ ] frozen_string_literal at top?
- [ ] Methods < 15 lines? (warn at 10+)
- [ ] Classes < 200 lines? (warn at 100+)
- [ ] No duplicate code?
- [ ] Parameters <= 3? (warn if more)

**Jeremy Evans:**
- [ ] Sequel datasets not raw SQL?
- [ ] DB writes in transactions?
- [ ] No N+1 queries in loops?

**Kent Beck:**
- [ ] Nested conditionals <= 3?
- [ ] Clear, revealing names?
- [ ] Methods do one thing?
- [ ] Command-Query Separation?

**Avdi Grimm:**
- [ ] Null objects instead of nil checks?
- [ ] Explicit returns (not implicit nil)?
- [ ] Specific exception classes?
- [ ] Law of Demeter (max 2 dots)?

**Gary Bernhardt:**
- [ ] Business logic separate from I/O?
- [ ] Value objects immutable?
- [ ] Tests avoid I/O?

## Success Criteria

The review is complete when:
- All staged Ruby files have been checked
- Clear BLOCK/WARNING/PASS verdict is given
- All critical issues have file:line references with expert attribution
- Concrete fix suggestions are provided with expert rationale
