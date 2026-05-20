---
name: trace-it
description: |
  Before modifying shared code (utilities, types, configs, base classes), traces
  all callers and dependents first. Activates when editing files in shared/,
  utils/, lib/, or anything imported by 3+ files. Prevents "fixed one thing,
  broke three others."
allowed-tools: |
  bash: grep, find, git
  file: read
---

# Trace It

<purpose>
Shared code is high-leverage but high-risk. Change a utility function and you
might break 10 callers. Change a type definition and you invalidate assumptions
across the codebase. This skill forces you to trace impact before editing.
</purpose>

## When To Activate

<triggers>
- Editing files in: `utils/`, `lib/`, `shared/`, `common/`, `core/`
- Modifying exported functions, classes, or types
- Changing function signatures (parameters, return types)
- Editing config files or constants
- Renaming anything that might be imported elsewhere
- Modifying base classes or interfaces
- User says "change how X works" for foundational code
</triggers>

## Instructions

### Before Modifying Shared Code

<trace_callers>
## Step 1: Find All Callers

```bash
# Find imports/requires of this file
grep -r "from.*['\"].*filename" src/
grep -r "import.*filename" src/
grep -r "require.*filename" src/

# Find usages of specific function/class
grep -r "functionName" src/ --include="*.ts"
```

Document what you find:

```markdown
## Dependency Trace: [file or function name]

**Direct callers:** [count]
- `src/api/handler.ts:23` - uses for validation
- `src/services/user.ts:45` - uses for formatting
- `src/utils/helpers.ts:12` - re-exports it

**Indirect dependents:** [count]
- Files that import the direct callers
```
</trace_callers>

<assess_impact>
## Step 2: Assess Impact

For each caller, determine:

| Caller | How it uses this | Will change break it? |
|--------|------------------|----------------------|
| `handler.ts` | Calls `validate(input)` | Yes - signature changes |
| `user.ts` | Uses return value | No - return type same |

**Impact level:**
- **Low:** 1-2 callers, simple usages
- **Medium:** 3-5 callers, varied usages
- **High:** 6+ callers OR complex/varied usages
</assess_impact>

<plan_migration>
## Step 3: Plan the Change

For **Low impact:** Proceed, update callers inline.

For **Medium impact:**
1. Make change backward-compatible if possible
2. Update all callers in same commit
3. Test each caller's behavior

For **High impact:**
1. Consider: Is this change necessary?
2. Create migration plan
3. Consider deprecation period
4. Update incrementally with tests
</plan_migration>

### Signature Changes

When changing function signatures:

```markdown
## Signature Change

**Before:** `function process(data: string): Result`
**After:** `function process(data: string, options?: Options): Result`

**Breaking:** No (new param is optional)
**Callers to update:** 0 required, 5 could benefit

## OR

**Before:** `function process(data: string): Result`
**After:** `function process(data: ProcessInput): Result`

**Breaking:** Yes
**Callers to update:** 8 files
**Migration:** [list each file and required change]
```

## Output Format

```markdown
## Trace: [what you're changing]

**Callers found:** [count]
**Impact level:** [Low/Medium/High]

**Changes required:**
- [ ] `file1.ts:line` - [what needs updating]
- [ ] `file2.ts:line` - [what needs updating]

**Verified after change:**
- [ ] All callers updated
- [ ] No new type errors
- [ ] Tests pass
```

## NEVER

- Modify shared code without tracing callers first
- Change function signatures assuming "it's probably fine"
- Update shared code and only test one caller
- Forget to check re-exports (file A exports from file B)
- Assume grep found everything (check for dynamic imports)

## ALWAYS

- Trace before touching shared code
- Document the caller count and impact level
- Update ALL callers in the same change
- Verify no type errors after the change
- Check for string-based references (dynamic imports, configs)

## Example

**User:** "Rename the `formatDate` function to `formatDateTime`"

**Trace:**
```bash
grep -r "formatDate" src/
```

**Found:**
```
src/utils/date.ts:15 - definition
src/components/Header.tsx:8 - import
src/components/EventCard.tsx:12 - import
src/pages/Dashboard.tsx:45 - import
src/api/events.ts:23 - import
src/utils/index.ts:5 - re-export
```

**Impact:** 6 files reference this. High impact.

**Plan:**
1. Rename in `date.ts`
2. Update re-export in `utils/index.ts`
3. Update imports in all 4 consumer files
4. Verify: `grep -r "formatDate" src/` returns nothing

**After completion:**
> Renamed `formatDate` → `formatDateTime` across 6 files.
> Verified: no remaining references to old name.
